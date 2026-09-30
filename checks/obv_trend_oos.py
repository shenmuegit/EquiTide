"""Fixed daily OBV rule from Deprez and Frömmel, tested once on a later holdout."""

import hashlib
import json
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

import polars as pl


ROOT = Path(__file__).resolve().parents[1]
VERSION = "20250916T000000Z_20260916T000000Z_archive_20260929"
START, EXIT_DAY = "2026-03-16", "2026-09-15"
DAY_NS, MINUTE_NS = 86_400_000_000_000, 60_000_000_000
# Appendix B: first distinct permitted daily OBV averages; no band, delay, or timed exit.
SHORT_DAYS, LONG_DAYS = 2, 6
FEE, HALF_SPREAD, SLIPPAGE = Decimal("0.001"), Decimal("0.0001"), Decimal("0.0002")
CAPITAL = Decimal("1000")


def obv_signal(closes: list[Decimal], volumes: list[Decimal]) -> list[bool]:
    obv = [Decimal(0)]
    for i in range(1, len(closes)):
        obv.append(obv[-1] + (volumes[i] if closes[i] >= closes[i - 1] else -volumes[i]))
    return [sum(obv[i - SHORT_DAYS + 1:i + 1]) / SHORT_DAYS >=
            sum(obv[i - LONG_DAYS + 1:i + 1]) / LONG_DAYS
            for i in range(LONG_DAYS - 1, len(obv))]


def daily_data(path: Path) -> tuple[list[dict], str]:
    frame = pl.read_parquet(path, columns=["open_ts", "available_ts", "open", "close", "base_volume", "is_closed"])
    assert frame.height == 365 * 1440 and frame["open_ts"].is_sorted()
    assert (frame["open_ts"].diff().drop_nulls() == MINUTE_NS).all() and frame["is_closed"].all()
    daily = frame.group_by((pl.col("open_ts") // DAY_NS).alias("day")).agg(
        pl.col("close").last(), pl.col("base_volume").sum().alias("volume"),
        pl.col("available_ts").last().alias("close_available_ts"),
    ).sort("day")
    trade = frame.filter(pl.col("open_ts") % DAY_NS == MINUTE_NS).select(
        (pl.col("open_ts") // DAY_NS).alias("day"), pl.col("open").alias("trade_open"),
        pl.col("open_ts").alias("trade_ts"),
    )
    rows = daily.join(trade, on="day").sort("day").to_dicts()
    assert len(rows) == 365
    for row in rows:
        row["date"] = datetime.fromtimestamp(row["day"] * 86400, timezone.utc).date().isoformat()
    return rows, hashlib.sha256(path.read_bytes()).hexdigest()


def max_drawdown(equity: list[Decimal]) -> float:
    peak, largest = equity[0], Decimal(0)
    for value in equity:
        peak = max(peak, value)
        largest = max(largest, 1 - value / peak)
    return float(largest * 100)


def test_asset(asset: str) -> tuple[dict, list[Decimal]]:
    version = f"binance_{asset}_{VERSION}"
    path = ROOT / "data" / "normalized" / "binance" / asset / version / "spot_bars.parquet"
    rows, digest = daily_data(path)
    dates = [row["date"] for row in rows]
    assert dates[0] == "2025-09-16" and dates[-1] == EXIT_DAY
    start, end = dates.index(START), dates.index(EXIT_DAY)
    signals = obv_signal([r["close"] for r in rows], [r["volume"] for r in rows])
    assert start > LONG_DAYS
    cash, units = CAPITAL, Decimal(0)
    equity, trades = [CAPITAL], []
    for i in range(start, end):
        previous, today = rows[i - 1], rows[i]
        assert previous["close_available_ts"] < today["trade_ts"]
        want_coin = signals[i - LONG_DAYS]
        if want_coin and not units:
            execution = today["trade_open"] * (1 + HALF_SPREAD + SLIPPAGE)
            units = cash / (execution * (1 + FEE))
            trades.append({"date": today["date"], "side": "buy", "reference": str(today["trade_open"]),
                           "execution": str(execution), "quantity": str(units)})
            cash = Decimal(0)
        elif not want_coin and units:
            execution = today["trade_open"] * (1 - HALF_SPREAD - SLIPPAGE)
            cash = units * execution * (1 - FEE)
            trades.append({"date": today["date"], "side": "sell", "reference": str(today["trade_open"]),
                           "execution": str(execution), "quantity": str(units)})
            units = Decimal(0)
        equity.append(cash + units * today["close"])
    if units:
        today = rows[end]
        assert rows[end - 1]["close_available_ts"] < today["trade_ts"]
        execution = today["trade_open"] * (1 - HALF_SPREAD - SLIPPAGE)
        cash = units * execution * (1 - FEE)
        trades.append({"date": EXIT_DAY, "side": "terminal_sell", "reference": str(today["trade_open"]),
                       "execution": str(execution), "quantity": str(units)})
    equity.append(cash)
    marks = [f"{dates[i + 1]}T00:00:00Z" for i in range(start, end)] + [f"{EXIT_DAY}T00:01:00Z"]
    return {
        "data_version": version, "spot_parquet_sha256": digest,
        "net_return_pct": float((equity[-1] / CAPITAL - 1) * 100),
        "max_drawdown_pct": max_drawdown(equity), "executions": len(trades),
        "round_trips": sum(t["side"] != "buy" for t in trades), "final_usdt": float(equity[-1]),
        "trades": trades, "equity_timestamps_utc": marks,
        "equity_points_usdt": [float(value) for value in equity[1:]],
    }, equity


def main() -> None:
    # One check for the paper's unusual rule that unchanged closes add volume.
    assert obv_signal(list(map(Decimal, [1, 2, 2, 1, 2, 3])), [Decimal(1)] * 6) == [True]
    results, curves = {}, []
    for asset in ("BTC", "ETH"):
        results[asset], curve = test_asset(asset)
        curves.append(curve)
    combined = [sum(day) for day in zip(*curves)]
    report = {
        "source": "https://backoffice.biblio.ugent.be/download/01HY3C3S169G1N6QNYR55NZMFB/01HY60XZGZYHNQ6188MSVJT0SG",
        "rule": "daily OBV: add base volume when close >= prior close, subtract otherwise; hold spot if SMA(OBV,2) >= SMA(OBV,6), else USDT; no band/delay/timed holding; parameters fixed before test",
        "method": "chronological holdout; pre-test history warms OBV only; prior 23:59 minute close available at next 00:00 UTC, trade at 00:01 UTC open; scheduled terminal exit",
        "oos_start_utc": START, "oos_end_utc": "2026-09-15T00:01:00Z",
        "oos_complete_days": len(results["BTC"]["equity_points_usdt"]) - 1,
        "capital_usdt_per_asset": str(CAPITAL), "fee_per_side": str(FEE),
        "half_spread_per_side": str(HALF_SPREAD), "slippage_per_side": str(SLIPPAGE),
        "funding_and_delivery": "not applicable to unlevered spot; USDT cash yield zero",
        "assets": results, "equal_capital_net_return_pct": float((combined[-1] / (2 * CAPITAL) - 1) * 100),
        "equal_capital_max_drawdown_pct": max_drawdown(combined),
        "equal_capital_executions": sum(r["executions"] for r in results.values()),
        "reproduce": "./.venv/Scripts/python.exe checks/obv_trend_oos.py",
    }
    output = ROOT / "data" / "runs" / "obv_trend_oos_20260929.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"result": str(output), "assets": {
        asset: {key: row[key] for key in ("net_return_pct", "max_drawdown_pct", "executions", "round_trips")}
        for asset, row in results.items()},
        "equal_capital_net_return_pct": report["equal_capital_net_return_pct"],
        "equal_capital_max_drawdown_pct": report["equal_capital_max_drawdown_pct"]}, indent=2))


if __name__ == "__main__":
    main()
