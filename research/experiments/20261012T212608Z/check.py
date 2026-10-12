#!/usr/bin/env python3
"""Audit the daily RSI experiment outputs without fetching or recalculating market data."""
import gzip, hashlib, importlib.util, json, math, struct, sys
from decimal import Decimal as D
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
R = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "research/automation"))
import registry


def loadmod(name, path):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s); sys.modules[name] = m; s.loader.exec_module(m); return m


fillmod = loadmod("rsi_audit_kernel", ROOT / "research/experiments/20261001T133655Z/kernel.py")
report = json.loads((R / "report.json").read_text())
reservations = json.loads((R / "reserve.json").read_text()) + json.loads((R / "benchmark_reserve.json").read_text())
records = [json.loads(x) for x in (ROOT / "research/automation/registry.jsonl").read_text().splitlines() if x.strip()]
latest = {}
for row in records:
    if row.get("fingerprint"):
        latest[row["fingerprint"]] = row
finished = "--pre-finish" not in sys.argv
assert len(reservations) == 20 and all(x["exit_code"] == 0 for x in reservations)
assert len(report["configs"]) == 18 and len(report["benchmarks"]) == 2
assert report["summary"]["cost_scenes"] == 54
assert report["summary"]["walk_forward_folds"] == 6 and report["summary"]["fold_days"] == 30
assert report["summary"]["oos_days"] == 183 and report["summary"]["remainder_days"] == 3
assert report["summary"]["passed"] + report["summary"]["rejected"] == 18
all_fps = set()
for entry in reservations:
    fp = entry.get("fingerprint") or entry.get("output")
    assert fp and fp not in all_fps
    all_fps.add(fp)
    assert fp in latest
    expected = ("passed" if "buy_hold_" in entry["spec"] else "rejected") if finished else "reserved"
    assert latest[fp].get("status") == expected, (fp, latest[fp].get("status"), expected)
    if finished:
        assert latest[fp].get("result_available") is True
        assert latest[fp].get("report") == "research/experiments/20261012T212608Z/report.json"
for asset in ("BTC", "ETH"):
    for info in report["data_manifest"]["source_files"][asset]:
        p = ROOT / info["path"]
        assert hashlib.sha256(p.read_bytes()).hexdigest() == info["sha256"]
    fp = report["benchmarks"][asset]["fingerprint"]
    assert fp in all_fps

scenes = 0
for name, cfg in report["configs"].items():
    assert cfg["fingerprint"] in all_fps
    assert len(cfg["scenarios"]) == 3
    assert len(cfg["scenarios"]["1"]["folds"]) == 6
    for mult in ("1", "2", "3"):
        path = ROOT / "data/runs" / R.name / f"{name}_cost{mult}.json.gz"
        assert path.exists()
        with gzip.open(path, "rt", encoding="utf-8") as f: ledger = json.load(f)
        assert all(cfg["scenarios"][mult].get(k) == v for k, v in ledger["summary"].items())
        nav = ledger["daily_nav_usdt"]
        assert len(nav) == 185 and math.isclose(nav[0], 2000.0, rel_tol=0, abs_tol=1e-10)
        digest = hashlib.sha256(b"".join(struct.pack("<d", float(v)) for v in nav)).hexdigest()
        assert digest == cfg["daily_nav_hashes"][mult]
        for trade in ledger["trades"]:
            assert D(trade["cash_after"]) >= 0 and D(trade["units_after"]) >= 0
            if trade["status"] == "filled":
                before = D(trade["cash_before"]) + D(trade["units_before"]) * D(trade["reference"])
                after = D(trade["cash_after"]) + D(trade["units_after"]) * D(trade["reference"])
                parts = sum((D(v) for v in trade["cost_parts"].values()), D(0))
                assert abs(before - after - D(trade["cost_usdt"])) < D("1e-18")
                assert abs(parts - D(trade["cost_usdt"])) < D("1e-18")
                if not trade["terminal"]:
                    assert trade["signal_available_utc"] < trade["execution_utc"]
                    assert trade["signal_to_execution_seconds"] == 60.0
            else:
                assert trade["reason"] in ("participation", "price", "quantity", "notional", "percent_price_proxy")
        s = cfg["scenarios"][mult]
        assert s["terminal_state"] == "cash" and D(s["terminal_units"]) == 0
        assert s["rejected_orders"] == 0
        assert s["cost_multiplier"] == int(mult)
        scenes += 1
for asset, cfg in report["benchmarks"].items():
    for mult, path in cfg["artifacts"].items():
        p = ROOT / path
        assert p.exists()
        with gzip.open(p, "rt", encoding="utf-8") as f: ledger = json.load(f)
        assert ledger["summary"] == cfg["scenarios"][mult]
        assert ledger["summary"]["terminal_state"] == "cash"
        assert D(ledger["summary"]["terminal_units"]) == 0
        scenes += 1
assert scenes == 60
assert report["summary"]["passed"] == 0  # Frozen fold-stability gate is deliberately not relaxed.
print(json.dumps({"passed": True, "portfolio_configs": 18, "benchmarks": 2, "cost_scenes_verified": scenes,
                  "reservations": 20, "finished_status_expected": finished, "cost_balance_identities": "PASS",
                  "causality_seconds": 60, "data_hashes": "PASS", "continuous_folds": 6}, indent=2))
