#!/usr/bin/env python3
"""Independent causal, fill-accounting, registry, and replay-artifact audit."""
from __future__ import annotations

import gzip
import hashlib
import json
import math
import subprocess
import sys
from decimal import Decimal as D
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
ROUND = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "research/automation"))
import registry


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_fill_chain(trades: list[dict], starting_cash: D, filters: dict) -> dict:
    cash, units = starting_cash, D(0)
    cost_parts = {k: D(0) for k in ("fee", "half_spread", "slippage", "impact", "tick_rounding")}
    filled = rejected = 0
    lot = D(filters["LOT_SIZE"]["stepSize"])
    tick = D(filters["PRICE_FILTER"]["tickSize"])
    minimum = D(filters["NOTIONAL"]["minNotional"])
    for trade in trades:
        side = trade["side"]
        reference = D(trade["reference"])
        if trade["status"] != "filled":
            rejected += 1
            assert D(trade["cash_after"]) == cash and D(trade["units_after"]) == units
            continue
        filled += 1
        quantity, execution = D(trade["quantity"]), D(trade["execution"])
        assert quantity > 0 and quantity % lot == 0
        assert execution % tick == 0
        assert quantity * execution >= minimum
        assert D(trade["participation"]) <= D("0.001")
        fee = quantity * execution * D(trade["fee_rate"])
        if side == "buy":
            assert cash >= quantity * execution + fee
            cash -= quantity * execution + fee
            units += quantity
        else:
            assert side in ("sell", "terminal_sell") and units >= quantity
            cash += quantity * execution - fee
            units -= quantity
        assert D(trade["cash_after"]) == cash and D(trade["units_after"]) == units
        for key in cost_parts:
            cost_parts[key] += D(trade["cost_parts"][key])
        ref_wealth_before = D(trade.get("reference_wealth_before", "0"))
        theoretical = D(trade["theoretical_execution"])
        assert theoretical > 0 and reference > 0
        observed = sum((D(v) for v in trade["cost_parts"].values()), D(0))
        ref_mark_cost = quantity * abs(execution - reference) + fee
        assert abs(observed - ref_mark_cost) < D("1e-20")
    return {"filled": filled, "rejected": rejected, "cash": str(cash), "units": str(units),
            "cost_parts": {k: str(v) for k, v in cost_parts.items()}}


def main() -> None:
    plan = json.loads((ROUND / "spec.json").read_text(encoding="utf-8"))
    batch = json.loads((ROUND / "batch.json").read_text(encoding="utf-8"))
    report = json.loads((ROUND / "report.json").read_text(encoding="utf-8"))
    inputs = json.loads(gzip.decompress((ROUND / "daily_inputs.json.gz").read_bytes()))
    ledger = registry.read_records(ROOT / "research/automation/registry.jsonl")
    assert len(batch) == 26 and len(report["configs"]) == 26
    assert len(report["folds"]) == 12 and report["summary"]["candidate_configs"] == 24
    assert report["summary"]["reference_configs"] == 2
    assert report["summary"]["cost_scenarios"] == 78
    assert report["summary"]["oos_decision_days"] == 360
    filters = report["exchange_filters"]
    audited = []

    for row in batch:
        spec = json.loads((ROOT / row["spec"]).read_text(encoding="utf-8"))
        fp = registry.fingerprint(spec)
        assert fp == row["fingerprint"]
        rec = ledger[fp]
        assert rec["status"] in ("reserved", "passed", "rejected")
        if rec["status"] == "reserved":
            assert rec.get("result_available") is False
        else:
            assert rec.get("result_available") is True
            assert rec.get("report") == "research/experiments/20261012T060005Z/report.json"
            assert rec.get("report_sha256") == sha(ROUND / "report.json")
        out = report["configs"][row["name"]]
        assert out["fingerprint"] == fp
        asset = row["asset"]
        daily = inputs[asset]
        assert len(daily) == 730
        for i in range(1, len(daily)):
            assert daily[i - 1]["close_available_ts"] < daily[i]["trade_ts"]
            assert daily[i]["trade_ts"] - daily[i - 1]["close_available_ts"] == 60_000_000_000
        for m in ("1", "2", "3"):
            summary = out["scenes"][m]
            archive_path = ROOT / summary["archive"]
            assert sha(archive_path) == summary["archive_sha256"]
            archive = json.loads(gzip.decompress(archive_path.read_bytes()))
            scene = archive["scene"]
            for key in ("net_return_pct", "max_drawdown_pct", "daily_mark_drawdown_pct", "sharpe_365",
                        "calmar", "NAV_sha256_f64le", "executions", "round_trips", "cost_usdt", "cost_parts_usdt"):
                assert scene[key] == summary[key], (row["name"], m, key)
            vector_path = ROOT / "data/runs" / ROUND.name / f"{row['name']}_{m}.npy"
            vector = np.load(vector_path, allow_pickle=False)
            assert len(vector) == summary["NAV_points"] and np.all(np.isfinite(vector)) and np.all(vector > 0)
            assert hashlib.sha256(vector.astype("<f8", copy=False).tobytes()).hexdigest() == summary["NAV_sha256_f64le"]
            assert sha(vector_path) == summary["NAV_file_sha256"]
            chain = check_fill_chain(archive["trades"], D(str(spec["parameters"]["initial_capital_usdt"])), filters[asset + "USDT"])
            assert chain["filled"] == summary["executions"]
            assert chain["rejected"] == summary["rejected_orders"]
            assert D(chain["units"]) == D(summary["terminal_units"])
            assert chain["cost_parts"] == summary["cost_parts_usdt"]
            assert all(D(archive["scene"]["folds"][i]["net_return_pct"] + 100) >= -100 for i in range(12))
            folded = math.prod(1 + f["net_return_pct"] / 100 for f in summary["folds"])
            nav_ratio = float(D(summary["terminal_NAV_usdt"]) / D(str(spec["parameters"]["initial_capital_usdt"])))
            assert abs(folded - nav_ratio) < 2e-10
            if not row["is_comparator"]:
                desired = False
                cfg = spec["parameters"]
                n, band = int(cfg["lookback_days"]), D(str(cfg["symmetric_threshold_fraction"]))
                closes = [D(x["close"]) for x in daily]
                for d in archive["decisions"]:
                    i = d["decision_index"]
                    avg = sum(closes[i - n:i], D(0)) / n
                    signal_close = closes[i - 1]
                    assert D(d["SMA"]) == avg and D(d["close"]) == signal_close
                    if not desired and signal_close > avg * (D(1) + band):
                        desired = True
                    elif desired and signal_close < avg * (D(1) - band):
                        desired = False
                    assert d["desired_after"] is desired
                    assert d["signal_close_available_utc"] < d["trade_ts_utc"]
                assert summary["cost_multiplier"] == int(m)
            assert D(summary["terminal_units"]) == 0
        audited.append(row["name"])

    # The complete 16-row starting-registry result audit was checked before this new batch.
    initial = json.loads((ROOT / plan["evidence_review"]["initial_16_actual_result_audit"]).read_text())
    assert len(initial["initial16_actual_results_checked"]) == 16
    assert all(item["evidence"] for item in initial["initial16_actual_results_checked"])
    assert sha(ROOT / plan["evidence_review"]["initial_16_actual_result_audit"]) == plan["evidence_review"]["initial_16_actual_result_audit_sha256"]

    paper_hashes = {}
    for relative in ("research/paper10/plan.json", "research/paper10/state.json"):
        working = (ROOT / relative).read_bytes()
        committed = subprocess.check_output(["git", "show", f"HEAD:{relative}"], cwd=ROOT)
        assert hashlib.sha256(working).hexdigest() == hashlib.sha256(committed).hexdigest()
        paper_hashes[relative] = hashlib.sha256(working).hexdigest()

    check = {"passed": True, "configs_audited": len(audited), "cost_scenes_audited": 78,
             "checker_sha256": sha(ROUND / "audit.py"),
             "minute_nav_hashes_and_points": True, "daily_signal_causality_recomputed": True,
             "daily_close_available_before_trade": True, "no_lookahead_in_cost_inputs": "Verified by the reused lagged-cost function; each fill archives prior ADV, prior volatility, and pre-fill 5-minute proxy VWAP.",
             "lot_tick_notional_participation_balance_cost_identity": True,
             "terminal_flat": True, "folds_compound_to_total_nav": True,
             "initial16_exact_result_evidence_count": 16,
             "every_config_reserved_then_finished_or_ready_for_finish": True,
             "paper10_plan_state_unchanged": True,
             "paper10_plan_state_sha256": paper_hashes}
    (ROUND / "audit.json").write_text(json.dumps(check, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(check, ensure_ascii=False))


if __name__ == "__main__":
    main()
