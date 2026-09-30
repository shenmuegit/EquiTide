"""Fixed-rule, chronological holdout for Issue #2's spot price trend."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

import polars as pl


ROOT = Path(__file__).resolve().parents[1]
VERSION = "20250916T000000Z_20260916T000000Z_archive_20260929"
START = "2026-03-16"
EXIT_DAY = "2026-09-15"
DAY_NS = 86_400_000_000_000
MINUTE_NS = 60_000_000_000
FEE = Decimal("0.001")
HALF_SPREAD = Decimal("0.0001")
SLIPPAGE = Decimal("0.0002")
CAPITAL = Decimal("1000")
LOOKBACK = {"BTC": 65, "ETH": 20}  # Monash paper, section 4.1; fixed before OOS run.


def daily_prices(path: Path) -> tuple[dict, str]:
    frame = pl.read_parquet(path, columns=["open_ts", "available_ts", "open", "close"])
    assert frame.height == 365 * 1440
    assert frame["open_ts"].is_sorted()
    assert (frame["open_ts"].diff().drop_nulls() == MINUTE_NS).all()
    rows = {}
    for row in frame.filter((pl.col("open_ts") % DAY_NS).is_in([MINUTE_NS, 1439 * MINUTE_NS])).iter_rows(named=True):
        day = datetime.fromtimestamp(row["open_ts"] // DAY_NS * 86400, timezone.utc).date().isoformat()
        entry = rows.setdefault(day, {})
        if row["open_ts"] % DAY_NS == MINUTE_NS:
            entry["trade_open"] = row["open"]
            entry["trade_ts"] = row["open_ts"]
        else:
            entry["close"] = row["close"]
            entry["close_available_ts"] = row["available_ts"]
    assert len(rows) == 365 and all(len(row) == 4 for row in rows.values())
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return rows, digest


def max_drawdown(values: list[Decimal]) -> float:
    peak = values[0]
    largest = Decimal(0)
    for value in values:
        peak = max(peak, value)
        largest = max(largest, 1 - value / peak)
    return float(largest)


def test_asset(asset: str) -> tuple[dict, list[Decimal]]:
    version = f"binance_{asset}_{VERSION}"
    path = ROOT / "data" / "normalized" / "binance" / asset / version / "spot_bars.parquet"
    prices, digest = daily_prices(path)
    dates = sorted(prices)
    assert dates[0] == "2025-09-16" and dates[-1] == EXIT_DAY
    start_idx = dates.index(START)
    assert start_idx >= LOOKBACK[asset]
    cash, units = CAPITAL, Decimal(0)
    equity = [CAPITAL]
    trades = []
    for i in range(start_idx, dates.index(EXIT_DAY)):
        date = dates[i]
        previous = prices[dates[i - 1]]
        today = prices[date]
        assert previous["close_available_ts"] < today["trade_ts"]
        average = sum(prices[d]["close"] for d in dates[i - LOOKBACK[asset]:i]) / LOOKBACK[asset]
        want_coin = previous["close"] > average
        if want_coin and units == 0:
            execution = today["trade_open"] * (1 + HALF_SPREAD + SLIPPAGE)
            units = cash / (execution * (1 + FEE))
            trades.append({"date": date, "side": "buy", "reference": str(today["trade_open"]),
                           "execution": str(execution), "quantity": str(units)})
            cash = Decimal(0)
        elif not want_coin and units > 0:
            execution = today["trade_open"] * (1 - HALF_SPREAD - SLIPPAGE)
            cash = units * execution * (1 - FEE)
            trades.append({"date": date, "side": "sell", "reference": str(today["trade_open"]),
                           "execution": str(execution), "quantity": str(units)})
            units = Decimal(0)
        equity.append(cash + units * today["close"])
    if units > 0:
        assert prices[dates[dates.index(EXIT_DAY) - 1]]["close_available_ts"] < prices[EXIT_DAY]["trade_ts"]
        execution = prices[EXIT_DAY]["trade_open"] * (1 - HALF_SPREAD - SLIPPAGE)
        cash = units * execution * (1 - FEE)
        trades.append({"date": EXIT_DAY, "side": "terminal_sell", "reference": str(prices[EXIT_DAY]["trade_open"]),
                       "execution": str(execution), "quantity": str(units)})
        units = Decimal(0)
    equity.append(cash)
    marks = [f"{dates[i + 1]}T00:00:00Z" for i in range(start_idx, dates.index(EXIT_DAY))]
    marks.append(f"{EXIT_DAY}T00:01:00Z")
    assert len(marks) == len(equity) - 1
    result = {
        "data_version": version, "spot_parquet_sha256": digest,
        "lookback_days": LOOKBACK[asset], "net_return_pct": float((equity[-1] / CAPITAL - 1) * 100),
        "max_drawdown_pct": max_drawdown(equity) * 100,
        "executions": len(trades), "round_trips": sum(t["side"] != "buy" for t in trades),
        "final_usdt": float(equity[-1]), "trades": trades,
        "equity_timestamps_utc": marks,
        "equity_points_usdt": [float(value) for value in equity[1:]],
    }
    return result, equity


def main() -> None:
    results = {}
    curves = []
    for asset in LOOKBACK:
        results[asset], curve = test_asset(asset)
        curves.append(curve)
    combined = [sum(day) for day in zip(*curves)]
    report = {
        "source": "https://www.monash.edu/__data/assets/pdf_file/0011/3744821/Trend-following-Strategies-for-Crypto-Investors.pdf",
        "method": "chronological holdout; prior history only warms up fixed paper lookbacks; 23:59 minute close available at next day 00:00 UTC, trade at 00:01 UTC open; scheduled terminal exit at 2026-09-15 00:01 UTC",
        "oos_start_utc": START, "oos_end_utc": "2026-09-15T00:01:00Z",
        "oos_complete_days": len(results["BTC"]["equity_points_usdt"]) - 1,
        "capital_usdt_per_asset": str(CAPITAL),
        "fee_per_side": str(FEE), "half_spread_per_side": str(HALF_SPREAD),
        "slippage_per_side": str(SLIPPAGE),
        "funding_and_delivery": "not applicable to unlevered spot holdings; USDT cash yield assumed zero",
        "assets": results,
        "equal_weight_net_return_pct": float((combined[-1] / (2 * CAPITAL) - 1) * 100),
        "equal_weight_max_drawdown_pct": max_drawdown(combined) * 100,
        "equal_weight_executions": sum(row["executions"] for row in results.values()),
        "reproduce": "./.venv/Scripts/python.exe checks/price_trend_oos.py",
    }
    output = ROOT / "data" / "runs" / "price_trend_oos_20260929.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"result": str(output), "assets": {
        asset: {key: row[key] for key in ("net_return_pct", "max_drawdown_pct", "executions", "round_trips")}
        for asset, row in results.items()},
        "equal_weight_net_return_pct": report["equal_weight_net_return_pct"],
        "equal_weight_max_drawdown_pct": report["equal_weight_max_drawdown_pct"]}, indent=2))


if __name__ == "__main__":
    main()
