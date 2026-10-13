#!/usr/bin/env python3
"""Freeze and reserve the 4h drawdown-reversal sensitivity batch."""
import hashlib, json, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ROUND = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "research/automation"))
import registry

SOURCE = ROOT / "research/experiments/20261012T035429Z/report.json"
source_report = json.loads(SOURCE.read_text())
filters = source_report["plan"]["execution"]["filters"]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def source_files():
    files = {}
    for asset in ("BTC", "ETH"):
        files[asset] = []
        for suffix in (f"{asset}_20240916T000000Z_20250916T000000Z_transfer_20261001",
                       f"{asset}_20250916T000000Z_20260916T000000Z_archive_20260929"):
            path = ROOT / f"data/normalized/binance/{asset}/binance_{suffix}/spot_bars.parquet"
            files[asset].append({"path": str(path.relative_to(ROOT)), "sha256": sha(path),
                                 "bytes": path.stat().st_size})
    return files

FILES = source_files()
COMMON_PARAMETERS = {
    "bar_return_lookback": 1,
    "rebound_exit_fraction": 0.0,
    "initial_capital_usdt": 2000,
    "oos_start_bar_index": 2208,
    "oos_end_exclusive_bar_index": 4368,
    "rolling_train_bars": 2190,
    "test_bars": 180,
    "step_bars": 180,
    "embargo_bars": 18,
    "folds": 12,
    "cost_multipliers": [1, 2, 3],
    "fee_rate_per_side": 0.001,
    "half_spread_estimate_per_side": 0.0001,
    "slippage_estimate_per_side": 0.0002,
    "impact_model": "0.5 * sample_stdev(previous 20 complete UTC daily log returns) * sqrt(order quote budget / previous 20 complete UTC daily quote-volume ADV)",
    "maximum_participation": 0.001,
    "exchange_filters": "Frozen Binance PRICE_FILTER, LOT_SIZE, NOTIONAL and PERCENT_PRICE_BY_SIDE snapshot; adverse tick rounding, lot floor, prior closed 5m VWAP proxy.",
}

grid = {"entry_drop_fraction": [0.005, 0.01, 0.015], "max_holding_4h_bars": [1, 2, 4]}
plan = {
    "round": ROUND.name,
    "frozen_at_utc": "2026-10-13T01:27:32Z",
    "direction": "Long-only spot reversal after a completed UTC 4h downside move, with fixed rebound or time exit.",
    "hypothesis": "Primary Bitcoin intraday research reports negative return autocorrelation at 1h, 2h and 4h horizons and stronger percentage reversal after larger moves. Test a simple 4h close-to-close downside threshold in current BTC/ETH spot data; no claim that the paper's effect persists or survives current costs.",
    "source_paper": {
        "citation": "De Nicola, G. (2021). On the Intraday Behavior of Bitcoin. Ledger, 6. DOI:10.5195/ledger.2021.213.",
        "url": "https://doi.org/10.5195/ledger.2021.213",
        "accessed_utc": "2026-10-13",
        "reported_finding": "The paper reports significant negative first-order autocorrelation on 1h, 2h and 4h returns and stronger percentage reversals after larger moves. It uses historical BTC data; this batch separately tests Binance BTC/ETH under explicit current cost assumptions.",
    },
    "grid": {"assets": ["BTC", "ETH"], **grid, "candidate_configs": 18, "matched_buy_hold_benchmarks": 2,
             "total_registry_definitions": 20, "cost_scenarios": [1, 2, 3]},
    "rule": "For each newly completed UTC 4h bar j, calculate simple close-to-close return close[j]/close[j-1]-1. If flat and return <= -entry_drop_fraction (equality qualifies), buy at the first 1m open one minute after the next UTC 4h block begins; store close[j] as recovery_reference. While long, exit when a later completed 4h close >= recovery_reference or elapsed completed 4h bars since entry execution >= max_holding_4h_bars. Exit has priority; after an exit signal, do not re-enter on that decision bar. A rejected entry is not retried/backfilled; a rejected exit remains held and is reconsidered only at later completed 4h decisions. Force a costed terminal liquidation at the first executable minute after the common OOS end if filters permit.",
    "time_boundaries": {
        "input_history_utc": "2024-09-16T00:00:00Z/2026-09-16T00:00:00Z",
        "warmup_days": 365,
        "embargo_days": 3,
        "oos_start_utc": "2025-09-19T00:00:00Z",
        "oos_end_exclusive_utc": "2026-09-14T00:00:00Z",
        "walk_forward": "12 contiguous, non-overlapping 30-day folds (180 4h bars each); unlevered account state carries through folds; parameters are frozen before evaluation.",
        "reuse_disclosure": "This interval is repeatedly used repository development/validation history and is not an untouched final holdout.",
    },
    "execution": {
        "market": "Binance spot historical 1m open as a scheduled reference, after closed 4h signal availability plus a fixed 60-second buffer.",
        "positioning": "Independent 2,000 USDT account per asset and configuration; long-only, one position at a time, no leverage, transfers, yield, or add-ons.",
        "terminal": "Costed liquidation at OOS end, subject to current frozen exchange filters.",
        "source_ohlcv": FILES,
        "filters_source": "research/experiments/20261012T035429Z/report.json",
        "filters_source_sha256": sha(SOURCE),
    },
    "costs": {
        "fee_each_side": "10bp", "half_spread_estimate_each_side": "1bp", "slippage_estimate_each_side": "2bp",
        "impact": "0.5 × prior 20 complete UTC daily return sample standard deviation × sqrt(order quote budget / prior 20 complete UTC daily quote-volume ADV)",
        "max_participation": "0.1% of prior 20-day quote ADV", "multipliers": [1, 2, 3],
        "spread_counted_once": True, "funding_or_borrow": "Not applicable: unlevered long-only spot.",
        "depth_limit": "No historical L2 snapshots in this experiment; spread and impact are estimates, with exchange filters/participation explicitly enforced.",
    },
    "sensitivity_axes": ["entry_drop_fraction", "max_holding_4h_bars"],
    "failure_gates": {
        "all_1x_2x_3x_net_returns_positive": True,
        "minimum_positive_1x_folds": 6,
        "maximum_3x_minute_close_sample_drawdown_pct": 25,
        "minimum_3x_adjacent_neighborhood_positive_fraction": 0.60,
        "minimum_1x_round_trips": 20,
        "minimum_1x_gross_reference_pnl_to_cost": 2.5,
        "no_balance_capacity_or_execution_filter_violations": True,
        "terminal_flat": True,
        "interpretation": "Any pass applies only to repeatedly used historical screening data and is not independent or live-profit evidence.",
    },
    "data_files": FILES,
}
(ROUND / "plan.json").write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n")

batch = []
for asset in ("BTC", "ETH"):
    for entry in grid["entry_drop_fraction"]:
        for hold in grid["max_holding_4h_bars"]:
            name = f"rev4h_{asset.lower()}_drop{int(entry*10000):03d}_hold{hold}"
            spec = {
                "kind": "strategy", "family": "spot-4h-extreme-return-reversal", "market": "spot",
                "timeframe": "4h", "universe": [f"{asset}/USDT"], "name": name,
                "logic": {
                    "entry": "At a newly completed UTC 4h bar j, simple close[j]/close[j-1]-1 <= -entry_drop_fraction; equality qualifies.",
                    "exit": "At a later completed UTC 4h close, exit when close >= the entry signal close (rebound_exit_fraction=0), or after max_holding_4h_bars have elapsed since execution. Exit takes precedence and no same-bar re-entry occurs.",
                    "timing": "Signals use completed UTC 4h bars. Simulated execution reference is the first 1m open at next 4h block start + 60 seconds; no bar from the entry or holding period determines the prior entry.",
                    "rejected_orders": "Do not backfill rejected historical entries. A rejected exit keeps the holding and is reconsidered on the next completed 4h signal bar; terminal liquidation is separately recorded.",
                    "sizing": "Independent 2,000 USDT unlevered long-only spot account; max affordable LOT_SIZE entry, whole valid-position exit, no cross-asset transfer, add-on, or cash yield.",
                },
                "parameters": {**COMMON_PARAMETERS, "entry_drop_fraction": entry,
                               "max_holding_4h_bars": hold, "rebound_exit_fraction": 0.0,
                               "sensitivity_axes": ["entry_drop_fraction", "max_holding_4h_bars"]},
                "sources": [plan["source_paper"]],
                "failure_gates": plan["failure_gates"],
            }
            path = ROUND / "specs" / f"{name}.json"
            path.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")
            batch.append({"name": name, "asset": asset, "spec": str(path.relative_to(ROOT)),
                          "fingerprint": registry.fingerprint(spec), "is_comparator": False})

for asset in ("BTC", "ETH"):
    name = f"hold_360d_{asset}_reversal_period"
    spec = {
        "kind": "strategy", "family": "spot-4h-reversal-hold-reference", "market": "spot",
        "timeframe": "4h", "universe": [f"{asset}/USDT"], "name": name,
        "logic": {"entry": "Buy at first OOS executable 1m open, without a signal.",
                  "exit": "Hold to common OOS terminal execution and liquidate at cost.",
                  "sizing": "Independent 2,000 USDT unlevered long-only spot comparator."},
        "parameters": {"initial_capital_usdt": 2000, "oos_start_bar_index": 2208,
                       "oos_end_exclusive_bar_index": 4368, "cost_multipliers": [1, 2, 3]},
        "sources": [plan["source_paper"]],
    }
    path = ROUND / "specs" / f"{name}.json"
    path.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")
    batch.append({"name": name, "asset": asset, "spec": str(path.relative_to(ROOT)),
                  "fingerprint": registry.fingerprint(spec), "is_comparator": True})

(ROUND / "batch.json").write_text(json.dumps(batch, indent=2) + "\n")
reservations = []
for row in batch:
    result = subprocess.run([sys.executable, str(ROOT / "research/automation/registry.py"),
                             "reserve", str(ROOT / row["spec"])], cwd=ROOT,
                            capture_output=True, text=True)
    reservations.append({"name": row["name"], "spec": row["spec"], "fingerprint": row["fingerprint"],
                         "exit_code": result.returncode, "stdout": result.stdout.strip(),
                         "stderr": result.stderr.strip()})
    if result.returncode != 0:
        (ROUND / "reserve.json").write_text(json.dumps(reservations, indent=2) + "\n")
        raise SystemExit(f"reserve failed before computation: {row['name']} rc={result.returncode}")
(ROUND / "reserve.json").write_text(json.dumps(reservations, indent=2) + "\n")
print(json.dumps({"round": ROUND.name, "reserved": len(reservations),
                  "unique_fingerprints": len({r['fingerprint'] for r in reservations}),
                  "assets": ["BTC", "ETH"], "candidate_configs": 18,
                  "benchmarks": 2, "scenes_to_evaluate": 60}, indent=2))
