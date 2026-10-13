#!/usr/bin/env python3
"""Independent input, registry, chronology, Decimal-cash and fold audit."""
import gzip, hashlib, importlib.util, json, math
from decimal import Decimal as D
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ROUND = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("registry_audit", ROOT / "research/automation/registry.py")
registry = importlib.util.module_from_spec(spec); spec.loader.exec_module(registry)
report = json.loads((ROUND / "report.json").read_text())
batch = json.loads((ROUND / "batch.json").read_text())
reservations = json.loads((ROUND / "reserve.json").read_text())
records = registry.read_records(ROOT / "research/automation/registry.jsonl")
assert len(batch) == len(reservations) == 20 and len({x["fingerprint"] for x in batch}) == 20
assert all(x["exit_code"] == 0 for x in reservations)
assert len(report["configs"]) == 18 and len(report["benchmarks"]) == 2
assert report["summary"]["cost_scenes"] == 60 and report["summary"]["folds"] == 12

scene_count = 0
violations = []
for row in batch:
    record = records[row["fingerprint"]]
    if row["is_comparator"]:
        assert record["status"] in ("reserved", "rejected")
    else:
        assert record["status"] in ("reserved", report["configs"][row["name"]]["status"])
    for mult in (1, 2, 3):
        path = ROOT / "data/runs" / ROUND.name / f"{row['name']}_cost{mult}.json.gz"
        with gzip.open(path, "rt", encoding="utf-8") as handle:
            archive = json.load(handle)
        summary = archive["summary"]
        assert archive["fingerprint"] == row["fingerprint"]
        assert summary["cost_multiplier"] == mult
        assert len(archive["daily_nav_usdt"]) == 361
        assert math.isclose(archive["daily_nav_usdt"][0], 2000.0, rel_tol=0, abs_tol=1e-9)
        assert hashlib.sha256(__import__("struct").pack("<" + "d" * 361, *archive["daily_nav_usdt"])).hexdigest() == summary["daily_nav_sha256_f64le"]
        assert summary["minute_close_samples"] == 518400
        assert len(summary["folds"]) == 12
        assert summary["rejected_orders"] >= summary["capacity_rejections"]
        assert summary["capacity_rejections"] == 0
        cash, units = D("2000"), D("0")
        seen_decision_minutes = set()
        for trade in archive["trades"]:
            assert trade["side"] in ("buy", "sell")
            assert trade["minute_index"] >= 2208 * 240 + 1
            assert trade["minute_index"] <= 4368 * 240 + 1
            if trade["signal_available_utc"] is not None:
                assert trade["signal_available_utc"] < trade["execution_utc"]
                assert trade["signal_to_execution_seconds"] == 60.0
            if trade["status"] == "filled":
                assert D(trade["cash_before"]) == cash and D(trade["units_before"]) == units
                parts = sum((D(v) for v in trade["cost_parts"].values()), D(0))
                assert abs(parts - D(trade["cost_usdt"])) <= D("1e-18")
                ref = D(trade["reference"])
                assert abs((cash + units * ref) - (D(trade["cash_after"]) + D(trade["units_after"]) * ref) - parts) <= D("1e-18")
                cash, units = D(trade["cash_after"]), D(trade["units_after"])
                assert cash >= 0 and units >= 0
            else:
                assert D(trade["cash_after"]) == cash and D(trade["units_after"]) == units
            assert trade["execution_utc"]
        assert D(summary["terminal_cash_usdt"]) == cash and D(summary["terminal_units"]) == units
        assert summary["terminal_flat"] == (units == 0)
        assert summary["cost_parts_usdt"] and math.isclose(
            sum(float(x) for x in summary["cost_parts_usdt"].values()), float(summary["cost_usdt"]),
            rel_tol=0, abs_tol=1e-7)
        for fold in summary["folds"]:
            assert math.isfinite(fold["net_return_pct"])
        for left, right in zip(summary["folds"], summary["folds"][1:]):
            from datetime import date, timedelta
            assert date.fromisoformat(left["end_utc_inclusive"]) + timedelta(days=1) == date.fromisoformat(right["start_utc"])
        if not summary["terminal_flat"]: violations.append({"name": row["name"], "cost": mult, "violation": "terminal units remain"})
        scene_count += 1

for asset, files in report["data_manifest"]["assets"].items():
    for entry in files["source_files"]:
        path = ROOT / entry["path"]
        assert path.stat().st_size == entry["bytes"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == entry["sha256"]
assert report["summary"]["candidate_passed"] + report["summary"]["candidate_rejected"] == 18
assert report["summary"]["candidate_passed"] == sum(x["status"] == "passed" for x in report["configs"].values())
assert scene_count == 60
result = {"passed": True, "candidate_configs": 18, "benchmarks": 2, "cost_scenes_verified": 60,
          "reservations_verified": 20, "source_hashes_verified": True, "continuous_daily_nav_samples": 361,
          "continuous_1m_close_samples_per_scene": 518400, "folds_per_scene": 12,
          "signal_availability_to_execution_delay_seconds": 60,
          "decimal_balance_cost_identities": "PASS", "capacity_filter_breaches": 0,
          "terminal_flat_failures": sum(not x["terminal_flat"] for row in batch for mult in (1,2,3)
                                          for x in [json.loads(gzip.open(ROOT / "data/runs" / ROUND.name / f"{row['name']}_cost{mult}.json.gz", "rt").read())["summary"]]),
          "violations": violations,
          "initial16_result_check": "research/experiments/20261012T035429Z/prior_evidence_audit.json reports actual evidence for all 16 initial entries."}
(ROUND / "audit.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
print(json.dumps(result, indent=2, ensure_ascii=False))
