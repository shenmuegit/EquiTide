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
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def identities(spec):
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
        # ponytail: structural fingerprints plus stable family IDs; review prose synonyms before reserving.
        idea = {"kind":kind, "logic":logic}
    elif kind == "combination":
        weights = {}
        for component in spec["components"]:
            fp, weight = component["fingerprint"], Fraction(str(component["weight"]))
            if not re.fullmatch(r"[0-9a-f]{64}", fp) or weight <= 0:
                raise ValueError("components need valid fingerprints and positive sleeve weights")
            weights[fp] = weights.get(fp, Fraction(0)) + weight
        if len(weights) < 2:
            raise ValueError("a combination requires at least two distinct components")
        total = sum(weights.values())
        definition = {"kind":kind, "logic":logic, "components":[{"fingerprint":fp,"weight":str(weights[fp]/total)} for fp in sorted(weights)]}
        idea = {"kind":kind, "logic":logic, "components":sorted(weights)}
    else:
        raise ValueError("kind must be strategy or combination")
    return digest(definition), digest(idea)


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
        fp, idea = identities(spec)
        args.ledger.parent.mkdir(parents=True, exist_ok=True)
        with args.ledger.with_suffix(".lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            records = read_records(args.ledger)
            if args.command == "reserve":
                for row in records.values():
                    same_family = spec["kind"] == "strategy" and row["spec"]["kind"] == "strategy" and row["spec"]["family"] == spec["family"]
                    if row["fingerprint"] == fp or row["idea_fingerprint"] == idea or same_family:
                        print(f"DUPLICATE: {row['fingerprint']} ({row['status']})")
                        return 3
                if spec["kind"] == "combination" and any(c["fingerprint"] not in records for c in spec["components"]):
                    raise ValueError("reserve every component before its combination")
                row = {"fingerprint":fp, "idea_fingerprint":idea, "spec":spec, "status":"reserved"}
            else:
                if fp not in records or records[fp]["status"] != "reserved":
                    raise ValueError("only an existing reserved trial can be finished")
                row = {"fingerprint":fp, "status":args.status, "report":str(args.report), "report_sha256":hashlib.sha256(args.report.read_bytes()).hexdigest()}
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
