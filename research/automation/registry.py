"""Append-only strategy reservations: reserve before any backtest."""
import argparse
import fcntl
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path


def digest(value):
    def normalize(item):
        if isinstance(item, dict):
            return {key:normalize(child) for key,child in item.items()}
        if isinstance(item, list):
            return [normalize(child) for child in item]
        return int(item) if isinstance(item, float) and item.is_integer() else item
    return hashlib.sha256(json.dumps(normalize(value), sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def fingerprint(spec):
    kind, family, logic = spec["kind"], spec["family"], spec["logic"]
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", family) or not isinstance(logic, dict) or not logic:
        raise ValueError("family must be a stable lowercase ID; logic must be a nonempty object")
    if kind == "strategy":
        if not isinstance(spec["parameters"], dict) or not spec["universe"]:
            raise ValueError("parameters and universe are required")
        if any(asset not in ("BTC/USDT", "ETH/USDT") for asset in spec["universe"]):
            raise ValueError("universe must use BTC/USDT and/or ETH/USDT")
        definition = {key: spec[key] for key in ("kind", "market", "timeframe", "logic", "parameters")}
        definition["universe"] = sorted(set(spec["universe"]))
    elif kind == "combination":
        weights = {}
        for component in spec["components"]:
            fp, weight = component["fingerprint"], Fraction(str(component["weight"]))
            if not re.fullmatch(r"[0-9a-f]{64}", fp) or weight <= 0:
                raise ValueError("components need valid fingerprints and positive sleeve weights")
            weights[fp] = weights.get(fp, Fraction(0)) + weight
        if len(weights) < 2:
            raise ValueError("a combination requires at least two distinct components")
        parameters = spec.get("parameters", {})
        if not isinstance(parameters, dict):
            raise ValueError("combination parameters must be an object")
        definition = {"kind":kind, "logic":logic, "parameters":parameters, "components":[{"fingerprint":fp,"weight":str(weights[fp])} for fp in sorted(weights)]}
    else:
        raise ValueError("kind must be strategy or combination")
    return digest(definition)


def read_records(path):
    records = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            row = json.loads(line)  # Corruption stops execution; never silently discard history.
            records.setdefault(row["fingerprint"], {}).update(row)
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, default=Path(__file__).with_name("registry.jsonl"))
    commands = parser.add_subparsers(dest="command", required=True)
    reserve = commands.add_parser("reserve")
    reserve.add_argument("spec", type=Path)
    finish = commands.add_parser("finish")
    finish.add_argument("spec", type=Path)
    finish.add_argument("status", choices=("passed","rejected","blocked","abandoned"))
    finish.add_argument("report", type=Path)
    args = parser.parse_args()
    try:
        spec = json.loads(args.spec.read_text(encoding="utf-8"))
        fp = fingerprint(spec)
        args.ledger.parent.mkdir(parents=True, exist_ok=True)
        with args.ledger.with_suffix(".lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            records = read_records(args.ledger)
            # Recompute historical definitions without rewriting their IDs or losing component references.
            matches = [(key,row) for key,row in records.items() if key == fp or fingerprint(row["spec"]) == fp]
            if args.command == "reserve":
                for key,row in matches:
                    if row.get("result_available") is False and row["status"] != "reserved":
                        continue
                    print(f"DUPLICATE: {key} ({row['status']})")
                    return 3
                if spec["kind"] == "combination" and any(c["fingerprint"] not in records for c in spec["components"]):
                    raise ValueError("reserve every component before its combination")
                row = {"fingerprint":fp, "spec":spec, "status":"reserved", "result_available":False}
                if matches:
                    row["retest_of"] = [key for key,_ in matches]
            else:
                pending = [key for key,row in matches if row["status"] == "reserved"]
                if not pending:
                    raise ValueError("only an existing reserved trial can be finished")
                fp = pending[0]
                row = {"fingerprint":fp, "status":args.status, "result_available":args.status in ("passed","rejected"), "report":str(args.report), "report_sha256":hashlib.sha256(args.report.read_bytes()).hexdigest()}
            row["recorded_at_utc"] = datetime.now(timezone.utc).isoformat()
            with args.ledger.open("a", encoding="utf-8") as output:
                output.write(json.dumps(row, ensure_ascii=False, allow_nan=False)+"\n")
                output.flush()
                os.fsync(output.fileno())
        print(fp)
        return 0
    except (KeyError, ValueError, TypeError, OSError, ZeroDivisionError) as error:
        print(f"REGISTRY_ERROR: {error}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
