"""Fixed BTC Binance-spot / OKX-perp cross-venue funding holdout for Issue #2."""

import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import polars as pl


ROOT = Path(__file__).resolve().parents[1]
OKX = ROOT / "data/normalized/okx/BTC/cross_exchange_carry_20260930"
BINANCE = ROOT / "data/normalized/binance/BTC/binance_BTC_20250916T000000Z_20260916T000000Z_archive_20260929"
PLAN = ROOT / "data/research/cross_exchange_carry_20260930_plan.json"
OUT = ROOT / "data/runs/cross_exchange_carry_oos_20260930.json"
DATA_START = 1765843200000  # 2025-12-16 00:00 UTC
OOS_START = 1773619200000  # 2026-03-16 00:00 UTC
LAST_SETTLEMENT = 1789430400000  # 2026-09-15 00:00 UTC
MINUTE, HOUR, CYCLE = 60_000, 3_600_000, 28_800_000
WINDOW = 270  # prior 90 days of 8-hour settlements
CAPITAL = 100_000.0
SPOT_FEE, PERP_FEE = 0.001, 0.0005
HALF_SPREAD, SLIPPAGE = 0.0001, 0.0002


def stamp(ms):
    return datetime.fromtimestamp(ms / 1000, timezone.utc).isoformat().replace("+00:00", "Z")


def signals(current, prior):
    deviation = float(np.std(prior, ddof=1))
    return (current - float(np.mean(prior))) / deviation if deviation > 0 else 0.0


def load():
    manifest = json.loads((OKX / "manifest.json").read_text(encoding="utf-8"))
    paths = (OKX / "perp_bars.parquet", OKX / "funding_settlement.parquet")
    assert hashlib.sha256(paths[0].read_bytes()).hexdigest() == manifest["bars_sha256"]
    assert hashlib.sha256(paths[1].read_bytes()).hexdigest() == manifest["funding_sha256"]
    perp = pl.read_parquet(paths[0])
    assert perp.height == 394_560 and perp["open_ts"][0] == DATA_START
    assert (perp["open_ts"].diff().drop_nulls() == MINUTE).all()
    spot_path = BINANCE / "spot_bars.parquet"
    spot = pl.read_parquet(spot_path, columns=["open_ts", "open", "close"])
    spot = spot.filter((pl.col("open_ts") >= DATA_START * 1_000_000) &
                       (pl.col("open_ts") < (DATA_START + perp.height * MINUTE) * 1_000_000))
    assert spot.height == perp.height
    assert (spot["open_ts"] // 1_000_000 == perp["open_ts"]).all()
    okx_funding = pl.read_parquet(paths[1]).to_dicts()
    binance_path = BINANCE / "funding_settlement.parquet"
    binance_funding = pl.read_parquet(binance_path, columns=["settlement_ts", "realized_rate"]).to_dicts()
    okx_rates = {r["settlement_ts"]: r["realized_rate"] for r in okx_funding}
    binance_rates = {}
    for row in binance_funding:
        ns = row["settlement_ts"]
        slot = (ns + 14_400_000_000_000) // 28_800_000_000_000 * CYCLE
        assert abs(ns - slot * 1_000_000) < 1_000_000_000
        if DATA_START <= slot < DATA_START + perp.height * MINUTE:
            assert slot not in binance_rates
            binance_rates[slot] = float(row["realized_rate"])
    common = sorted(okx_rates.keys() & binance_rates.keys())
    assert len(common) == 822 and common[0] == DATA_START
    assert all(b - a == CYCLE for a, b in zip(common, common[1:]))
    return (perp["open"].to_numpy(), perp["close"].to_numpy(),
            spot["open"].cast(pl.Float64).to_numpy(), spot["close"].cast(pl.Float64).to_numpy(),
            okx_rates, binance_rates, common,
            {"okx_manifest": manifest, "binance_spot_sha256": hashlib.sha256(spot_path.read_bytes()).hexdigest(),
             "binance_funding_sha256": hashlib.sha256(binance_path.read_bytes()).hexdigest(),
             "plan_sha256": hashlib.sha256(PLAN.read_bytes()).hexdigest()})


def main():
    perp_open, perp_close, spot_open, spot_close, okx, binance, common, data = load()
    peaks = np.array([max(okx[t], binance[t]) for t in common])
    cash, quantity, entry_perp = CAPITAL, 0.0, 0.0
    trades, settlements, equity, decisions = [], [], [], []

    def bar_at(ts):
        i = (ts - DATA_START) // MINUTE
        assert 0 <= i < len(perp_open) and (ts - DATA_START) % MINUTE == 0
        return i

    def nav(ts):
        i = bar_at(ts)
        return cash + quantity * spot_open[i] + quantity * (entry_perp - perp_open[i])

    for j, settlement_ts in enumerate(common):
        if settlement_ts < OOS_START or settlement_ts > LAST_SETTLEMENT:
            continue
        assert j >= WINDOW
        # Funding settles on the position held before any new signal is executed.
        if quantity:
            mark = perp_close[bar_at(settlement_ts - MINUTE)]  # pre-settlement proxy
            amount = quantity * mark * okx[settlement_ts]
            cash += amount
            settlements.append({"ts": stamp(settlement_ts), "rate": okx[settlement_ts],
                                "mark_proxy": mark, "quantity_btc": quantity, "usdt": amount})

        decision_ts, fill_ts = settlement_ts + HOUR, settlement_ts + HOUR + MINUTE
        z = signals(peaks[j], peaks[j-WINDOW:j])
        okx_best = okx[settlement_ts] > binance[settlement_ts]
        decisions.append({"ts": stamp(decision_ts), "z": z, "okx_rate": okx[settlement_ts],
                          "binance_rate": binance[settlement_ts], "okx_best": okx_best})
        i = bar_at(fill_ts)
        spot_mid, perp_mid = spot_open[i], perp_open[i]
        if quantity and (z <= 0 or not okx_best or settlement_ts == LAST_SETTLEMENT):
            spot_px = spot_mid * (1 - HALF_SPREAD - SLIPPAGE)
            perp_px = perp_mid * (1 + HALF_SPREAD + SLIPPAGE)
            spot_fee, perp_fee = quantity * spot_px * SPOT_FEE, quantity * perp_px * PERP_FEE
            cash += quantity * spot_px - spot_fee + quantity * (entry_perp - perp_px) - perp_fee
            trades.append({"ts": stamp(fill_ts), "side": "exit", "reason": "scheduled_end" if settlement_ts == LAST_SETTLEMENT else "signal",
                           "quantity_btc": quantity, "spot_reference": spot_mid, "spot_execution": spot_px,
                           "perp_reference": perp_mid, "perp_execution": perp_px,
                           "spot_fee_usdt": spot_fee, "perp_fee_usdt": perp_fee})
            quantity, entry_perp = 0.0, 0.0
        elif not quantity and z > 2 and okx_best and settlement_ts < LAST_SETTLEMENT:
            spot_px = spot_mid * (1 + HALF_SPREAD + SLIPPAGE)
            perp_px = perp_mid * (1 - HALF_SPREAD - SLIPPAGE)
            quantity = math.floor((nav(fill_ts) / 14) / max(spot_px, perp_mid) / 0.01) * 0.01
            if quantity:
                spot_fee, perp_fee = quantity * spot_px * SPOT_FEE, quantity * perp_px * PERP_FEE
                cash -= quantity * spot_px + spot_fee + perp_fee
                entry_perp = perp_px
                trades.append({"ts": stamp(fill_ts), "side": "entry", "reason": "z_gt_2_okx_best",
                               "quantity_btc": quantity, "spot_reference": spot_mid, "spot_execution": spot_px,
                               "perp_reference": perp_mid, "perp_execution": perp_px,
                               "spot_fee_usdt": spot_fee, "perp_fee_usdt": perp_fee})
        value = nav(fill_ts)
        assert math.isfinite(value) and value > 0
        equity.append({"ts": stamp(fill_ts), "usdt": value})

    assert quantity == 0 and equity[-1]["ts"] == stamp(LAST_SETTLEMENT + HOUR + MINUTE)
    curve = np.array([CAPITAL] + [r["usdt"] for r in equity])
    drawdown = 1 - curve / np.maximum.accumulate(curve)
    report = {
        "rule_plan": str(PLAN), "source": "https://khanh1ng.github.io/writing/2026/cross-exchange-funding-carry/",
        "method": "causal 270 prior 8-hour settlements for each rolling Z; one-hour publication buffer; next-minute execution; one chronological 183-day holdout",
        "oos_start_utc": stamp(OOS_START + HOUR + MINUTE),
        "oos_end_utc": stamp(LAST_SETTLEMENT + HOUR + MINUTE),
        "initial_capital_usdt": CAPITAL, "data": data,
        "costs": {"spot_taker_fee": SPOT_FEE, "perp_taker_fee": PERP_FEE,
                  "half_spread_per_side": HALF_SPREAD, "slippage_per_side": SLIPPAGE,
                  "funding": "actual OKX rate * pre-settlement minute close proxy for mark; no delivery"},
        "net_return_pct": (cash / CAPITAL - 1) * 100,
        "max_drawdown_pct": float(drawdown.max() * 100),
        "decision_cycles": len(decisions), "max_signal_z": max(r["z"] for r in decisions),
        "z_gt_2_cycles": int(sum(r["z"] > 2 for r in decisions)),
        "okx_best_cycles": sum(r["okx_best"] for r in decisions),
        "eligible_entry_cycles": int(sum(r["z"] > 2 and r["okx_best"] for r in decisions)),
        "executions": len(trades) * 2, "pair_round_trips": sum(t["side"] == "entry" for t in trades),
        "fees_usdt": sum(t["spot_fee_usdt"] + t["perp_fee_usdt"] for t in trades),
        "funding_usdt": sum(s["usdt"] for s in settlements),
        "final_equity_usdt": cash, "trades": trades, "funding_settlements": settlements,
        "eight_hour_equity": equity, "decisions": decisions,
        "reproduce": ".\\.venv\\Scripts\\python.exe checks\\download_okx_carry.py; .\\.venv\\Scripts\\python.exe checks\\cross_exchange_carry_oos.py"
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("oos_start_utc", "oos_end_utc", "net_return_pct",
                        "max_drawdown_pct", "decision_cycles", "max_signal_z", "z_gt_2_cycles",
                        "eligible_entry_cycles", "executions", "pair_round_trips", "funding_usdt", "fees_usdt")}, indent=2))
    print(OUT)


if __name__ == "__main__":
    assert signals(3, np.array([1, 2], dtype=float)) > 0
    assert signals(1, np.array([1, 1], dtype=float)) == 0
    main()
