#!/usr/bin/env python3
"""Freeze and register the long-horizon daily SMA sensitivity batch."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ROUND = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "research/automation"))
import registry


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def main() -> None:
    ROUND.mkdir(parents=True, exist_ok=True)
    prior_audit = ROOT / "research/experiments/20261012T035429Z/prior_evidence_audit.json"
    audit = json.loads(prior_audit.read_text(encoding="utf-8"))
    assert len(audit["initial16_actual_results_checked"]) == 16
    assert all(row["evidence"] for row in audit["initial16_actual_results_checked"])

    source_report_path = ROOT / "research/experiments/20261012T035429Z/report.json"
    source_report = json.loads(source_report_path.read_text(encoding="utf-8"))
    filters = source_report["plan"]["execution"]["filters"]
    metadata = {
        "path": source_report["plan"]["execution"]["metadata_path"],
        "sha256": source_report["plan"]["execution"]["metadata_sha256"],
        "source_report": str(source_report_path.relative_to(ROOT)),
        "source_report_sha256": sha(source_report_path),
    }

    round_id = ROUND.name
    common = {
        "source": {
            "title": "Trend-following Strategies for Crypto Investors, section 4.1",
            "url": "https://www.monash.edu/__data/assets/pdf_file/0011/3744821/Trend-following-Strategies-for-Crypto-Investors.pdf",
            "accessed_utc": "2026-10-12",
            "use": "Long-only moving-average trend rule; 150/200-day horizons follow cited horizon set, 250/300 are predeclared extensions.",
        },
        "development_data": {
            "BTC": [
                "data/normalized/binance/BTC/binance_BTC_20240916T000000Z_20250916T000000Z_transfer_20261001/spot_bars.parquet",
                "data/normalized/binance/BTC/binance_BTC_20250916T000000Z_20260916T000000Z_archive_20260929/spot_bars.parquet",
            ],
            "ETH": [
                "data/normalized/binance/ETH/binance_ETH_20240916T000000Z_20250916T000000Z_transfer_20261001/spot_bars.parquet",
                "data/normalized/binance/ETH/binance_ETH_20250916T000000Z_20260916T000000Z_archive_20260929/spot_bars.parquet",
            ],
            "reuse_disclosure": "The same 2024-09-16 through 2026-09-16 Binance history has appeared in prior research. It is development/validation history, not an untouched final holdout.",
        },
        "walk_forward": {
            "engine": ".agents/skills/walk-forward-validation/scripts/walk_forward.py",
            "window_type": "rolling",
            "train_days": 365,
            "test_days": 30,
            "step_days": 30,
            "purge_days": 0,
            "embargo_days": 3,
            "expected_folds": 12,
            "continuous_oos": True,
            "first_test_index": 368,
            "last_test_end_exclusive_index": 728,
            "start_equity_flat": True,
            "parameter_fit": "None. Rules are frozen before results; prior daily closes are used only for SMA warm-up and signals.",
            "oos_trade_dates_utc": "2025-09-19 through 2026-09-13; terminal execution at next available 00:01 UTC minute open.",
        },
        "cost_model": {
            "fee_per_side": 0.001,
            "half_spread_estimate_per_side": 0.0001,
            "slippage_estimate_per_side": 0.0002,
            "impact_coefficient": 0.5,
            "impact_formula": "0.5 * prior-20-complete-UTC-day sample volatility * sqrt(order budget / prior-20-day mean quote ADV)",
            "max_lagged_quote_ADV_participation": 0.001,
            "scenarios": [1, 2, 3],
            "spread_observation": "Historical one-minute OHLCV has no historical L2 quotes; half-spread is an estimate and is charged once.",
            "filters_source": metadata,
            "filters_sha256_by_symbol": {symbol: sha_value for symbol, sha_value in (("BTCUSDT", hashlib.sha256(json.dumps(filters["BTCUSDT"], sort_keys=True, separators=(",", ":")).encode()).hexdigest()), ("ETHUSDT", hashlib.sha256(json.dumps(filters["ETHUSDT"], sort_keys=True, separators=(",", ":")).encode()).hexdigest()))},
            "perpetual_funding_borrow": "Not applicable; unlevered long-only spot.",
            "execution_model": "Historical executable reference is the next UTC day 00:01 one-minute open, after the completed prior daily close is available. Decimal28 fill, adverse tick, LOT_SIZE/NOTIONAL, 5-minute VWAP proxy, and participation checks are reused from the repository execution kernel. Simulated fills are not exchange acceptance guarantees.",
        },
        "failure_gates": {
            "all_cost_scenarios_positive": True,
            "minimum_positive_1x_folds": 7,
            "maximum_3x_minute_close_sample_drawdown_pct": 25,
            "minimum_3x_neighbourhood_positive_fraction": 0.60,
            "minimum_1x_round_trips": 2,
            "minimum_1x_gross_reference_pnl_to_cost": 2.5,
            "no_negative_balance_or_units": True,
            "terminal_flat": True,
            "interpretation": "Passed means this repeated historical walk-forward screen only; it is not independent or live-profit evidence.",
        },
    }

    plan = {
        "round": round_id,
        "frozen_at_utc": "2026-10-12T06:00:05Z",
        "direction": "Long-horizon daily BTC/ETH SMA trend-following with a symmetric hysteresis band.",
        "hypothesis": "Longer 150-300-day trend filters may suppress short-horizon whipsaws; a predeclared 0-1% symmetric band may improve net results by reducing marginal crossings, at the cost of later entries/exits.",
        "grid": {"assets": ["BTC", "ETH"], "lookback_days": [150, 200, 250, 300], "symmetric_threshold_fraction": [0.0, 0.005, 0.01], "initial_capital_usdt_per_config": 2000},
        "sensitivity_axes": ["lookback_days", "symmetric_threshold_fraction"],
        "logic": "For daily decision index i, compare completed close C[i-1] to the arithmetic mean of C[i-lookback:i], all fully closed UTC daily bars. If flat, enter when C[i-1] > SMA*(1+band). If long, exit when C[i-1] < SMA*(1-band). Otherwise preserve the prior desired state. New OOS account starts flat; no warm-up fills or pre-OOS state replay.",
        "allocation": "Each config is a separate 2,000 USDT account with a single BTC or ETH sleeve; the full amount is the maximum risky sleeve, no leverage, no transfers, no rebalancing, and no cross-config averaging.",
        "evidence_review": {
            "initial_16_actual_result_audit": str(prior_audit.relative_to(ROOT)),
            "initial_16_actual_result_audit_sha256": sha(prior_audit),
            "finding": "All 16 exact initial registry rows already have actual backtest/report evidence; do not rerun completed exact configs.",
            "freqtrade_trial_results": "Read backtest-result metadata and three walk-forward JSON reports; their 2026-07-21 through 2026-09-15 15m results are not the present daily long-horizon configs.",
        },
        **common,
    }
    (ROUND / "spec.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    records = []
    for asset in ("BTC", "ETH"):
        for lookback in plan["grid"]["lookback_days"]:
            for band in plan["grid"]["symmetric_threshold_fraction"]:
                name = f"sma{lookback}_band{int(band*10000):03d}_{asset}"
                asset_full = asset + "/USDT"
                band_pct = f"{band*100:.2f}%"
                logic = {
                    "entry": f"At a newly completed UTC daily bar i, enter long only when C[i-1] > arithmetic_mean(C[i-{lookback}:i]) * (1 + {band_pct}); SMA uses the {lookback} most recent completed daily closes including C[i-1].",
                    "exit": f"When long, exit when C[i-1] < arithmetic_mean(C[i-{lookback}:i]) * (1 - {band_pct}); otherwise retain prior desired state. Equality and values inside the symmetric band retain state.",
                    "sizing": "Independent unlevered long-only spot account, initial capital 2000 USDT; buy maximum affordable quantity after signal close at next UTC day 00:01 one-minute open; preserve cash/units; terminal liquidation is costed. No pre-OOS fills, leverage, shorting, rebalancing, or cross-asset transfer.",
                    "signal_timing": "Daily input is closed UTC candles only; last closed signal is available before next-day 00:01 UTC execution.",
                }
                params = {
                    "lookback_days": lookback,
                    "symmetric_threshold_fraction": band,
                    "initial_capital_usdt": 2000,
                    "oos_first_test_index": 368,
                    "oos_end_exclusive_index": 728,
                    "oos_start_utc": "2025-09-19T00:01:00Z",
                    "oos_terminal_execution_utc": "2026-09-14T00:01:00Z",
                    "walk_forward_train_days": 365,
                    "walk_forward_test_days": 30,
                    "walk_forward_step_days": 30,
                    "walk_forward_embargo_days": 3,
                    "cost_multipliers": [1, 2, 3],
                }
                spec = {"kind": "strategy", "family": "daily-price-sma-hysteresis", "market": "spot", "timeframe": "1d", "universe": [asset_full], "logic": logic, "parameters": params, "name": name}
                fp = registry.fingerprint(spec)
                path = ROUND / "specs" / f"{name}.json"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                records.append({"name": name, "asset": asset, "lookback_days": lookback, "symmetric_threshold_fraction": band, "fingerprint": fp, "spec": str(path.relative_to(ROOT)), "is_comparator": False})

    for asset in ("BTC", "ETH"):
        asset_full = asset + "/USDT"
        name = f"buy_hold_360d_{asset}"
        spec = {
            "kind": "strategy", "family": "daily-buy-hold-reference", "market": "spot", "timeframe": "1d", "universe": [asset_full],
            "logic": {
                "entry": "At the first OOS 00:01 UTC one-minute open, enter long once and hold regardless of subsequent signals.",
                "exit": "Scheduled terminal exit at the end of the common OOS interval.",
                "sizing": "Independent unlevered long-only spot reference with 2000 USDT initial capital; same exchange filters, lot/notional, costs, and terminal cost as candidates.",
                "signal_timing": "Fixed OOS start/end; historical closes are not used for a signal.",
            },
            "parameters": {"initial_capital_usdt": 2000, "oos_first_test_index": 368, "oos_end_exclusive_index": 728, "cost_multipliers": [1, 2, 3]},
            "name": name,
        }
        fp = registry.fingerprint(spec)
        path = ROUND / "specs" / f"{name}.json"
        path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        records.append({"name": name, "asset": asset, "lookback_days": None, "symmetric_threshold_fraction": None, "fingerprint": fp, "spec": str(path.relative_to(ROOT)), "is_comparator": True})

    (ROUND / "batch.json").write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (ROUND / "reserve.log").open("w", encoding="utf-8") as log:
        for row in records:
            cmd = [sys.executable, str(ROOT / "research/automation/registry.py"), "reserve", str(ROOT / row["spec"])]
            proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
            log.write(json.dumps({"name": row["name"], "command": cmd, "returncode": proc.returncode, "stdout": proc.stdout.strip(), "stderr": proc.stderr.strip()}, ensure_ascii=False) + "\n")
            log.flush()
            if proc.returncode != 0:
                raise SystemExit(f"reserve failed for {row['name']}: rc={proc.returncode}; {proc.stdout}{proc.stderr}")
    print(json.dumps({"batch_size": len(records), "candidate_configs": sum(not x["is_comparator"] for x in records), "comparators": 2, "reserved": True, "plan": str((ROUND / 'spec.json').relative_to(ROOT))}, ensure_ascii=False))


if __name__ == "__main__":
    main()
