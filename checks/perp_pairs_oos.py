"""One fixed, causal BTC/ETH perpetual-pair holdout test for Issue #2."""

import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import polars as pl
from statsmodels.tsa.stattools import adfuller


ROOT = Path(__file__).resolve().parents[1]
VERSION = "20250916T000000Z_20260916T000000Z_archive_20260929"
START, END = "2026-03-16T00:00:00Z", "2026-09-15T00:00:00Z"
HOUR, MINUTE = 3_600_000_000_000, 60_000_000_000
WINDOW = 720
CAPITAL = 2_000.0
FEE, HALF_SPREAD, SLIPPAGE = 0.0005, 0.0001, 0.0002


def stamp(ns):
    return datetime.fromtimestamp(ns / 1e9, timezone.utc).isoformat().replace("+00:00", "Z")


def load_asset(asset):
    directory = ROOT / "data/normalized/binance" / asset / f"binance_{asset}_{VERSION}"
    bar_path = directory / "perp_bars.parquet"
    bars = pl.read_parquet(bar_path, columns=["open_ts", "available_ts", "open", "close", "is_closed"])
    assert bars.height == 525_600 and bars["open_ts"].is_sorted()
    assert (bars["open_ts"].diff().drop_nulls() == MINUTE).all() and bars["is_closed"].all()
    closes = bars.filter(pl.col("open_ts") % HOUR == HOUR - MINUTE).select(
        pl.col("available_ts").alias("ts"), pl.col("close").cast(pl.Float64).alias("close")
    )
    opens = bars.filter(pl.col("open_ts") % HOUR == MINUTE).select(
        (pl.col("open_ts") - MINUTE).alias("ts"), pl.col("open").cast(pl.Float64).alias("open")
    )
    hourly = closes.join(opens, on="ts", how="inner").sort("ts")
    assert hourly.height == 8_759 and (hourly["ts"].diff().drop_nulls() == HOUR).all()
    funding_path = directory / "funding_settlement.parquet"
    funding = pl.read_parquet(funding_path, columns=[
        "settlement_ts", "realized_rate", "mark_price_at_settlement"
    ]).sort("settlement_ts")
    assert funding.height == 1_095 and funding["realized_rate"].null_count() == 0
    assert funding["mark_price_at_settlement"].null_count() == 0
    meta = pl.read_parquet(directory / "perp_instrument_meta.parquet").to_dicts()[0]
    return (hourly, funding.to_dicts(), meta, {
        "version": f"binance_{asset}_{VERSION}",
        "perp_bars_sha256": hashlib.sha256(bar_path.read_bytes()).hexdigest(),
        "funding_settlement_sha256": hashlib.sha256(funding_path.read_bytes()).hexdigest(),
    })


def signal(btc_history, eth_history, btc_now, eth_now):
    """Current close enters only the Z numerator; all estimates end one hour earlier."""
    x, y = np.log(eth_history), np.log(btc_history)
    beta = float(np.dot(x - x.mean(), y - y.mean()) / np.dot(x - x.mean(), x - x.mean()))
    spread = y - beta * x
    z = float((math.log(btc_now) - beta * math.log(eth_now) - spread.mean())
              / spread.std(ddof=1))
    return beta, z, spread


def main():
    btc, bf, bm, bd = load_asset("BTC")
    eth, ef, em, ed = load_asset("ETH")
    assert btc["ts"].to_list() == eth["ts"].to_list()
    rows = btc.join(eth, on="ts", suffix="_eth").to_dicts()
    times = [row["ts"] for row in rows]
    start = times.index(int(datetime.fromisoformat(START.replace("Z", "+00:00")).timestamp() * 1e9))
    end = times.index(int(datetime.fromisoformat(END.replace("Z", "+00:00")).timestamp() * 1e9))
    assert start >= WINDOW and end > start
    btc_close = np.array([row["close"] for row in rows])
    eth_close = np.array([row["close_eth"] for row in rows])
    # Entry sizing uses all available equity, split 1:beta across the two legs.
    lots = [float(bm["lot_size"]), float(em["lot_size"])]
    ticks = [float(bm["tick_size"]), float(em["tick_size"])]
    minimums = [float(bm["min_notional"]), float(em["min_notional"])]
    funding = sorted([(r["settlement_ts"], 0, float(r["realized_rate"]),
                       float(r["mark_price_at_settlement"])) for r in bf] +
                     [(r["settlement_ts"], 1, float(r["realized_rate"]),
                       float(r["mark_price_at_settlement"])) for r in ef])
    funding = [row for row in funding if times[start] <= row[0] <= times[end] + MINUTE]
    cash, quantity, funding_index = CAPITAL, [0.0, 0.0], 0
    trades, funding_events, equity = [], [], [{"ts": START, "usdt": CAPITAL}]
    candidate_entries = adf_passes = 0

    def nav(prices):
        return cash + sum(q * p for q, p in zip(quantity, prices))

    def trade(ts, target, prices, reason, beta=None, z=None, p=None):
        nonlocal cash
        for leg, asset in enumerate(("BTC", "ETH")):
            change = target[leg] - quantity[leg]
            if abs(change) < lots[leg] / 2:
                continue
            reference = prices[leg]
            adjusted = reference * (1 + math.copysign(HALF_SPREAD + SLIPPAGE, change))
            execution = (math.ceil(adjusted / ticks[leg] - 1e-9) if change > 0 else
                         math.floor(adjusted / ticks[leg] + 1e-9)) * ticks[leg]
            fee = abs(change * execution) * FEE
            cash -= change * execution + fee
            quantity[leg] = target[leg]
            trades.append({"ts": stamp(ts + MINUTE), "asset": asset,
                           "side": "buy" if change > 0 else "sell", "reason": reason,
                           "quantity": change, "reference": reference,
                           "execution": execution, "fee_usdt": fee,
                           "beta": beta, "z": z, "adf_p": p})

    for i in range(start, end + 1):
        row = rows[i]
        ts = row["ts"]
        prices = [row["open"], row["open_eth"]]
        # Settlement belongs to the position held at the actual settlement instant.
        while funding_index < len(funding) and funding[funding_index][0] <= ts + MINUTE:
            settled, leg, rate, mark = funding[funding_index]
            amount = -quantity[leg] * mark * rate
            if quantity[leg]:
                cash += amount
                funding_events.append({"ts": stamp(settled), "asset": ("BTC", "ETH")[leg],
                                       "rate": rate, "mark": mark, "quantity": quantity[leg],
                                       "amount_usdt": amount})
            funding_index += 1
        if i == end:
            if any(quantity):
                trade(ts, [0.0, 0.0], prices, "scheduled_terminal_exit")
        else:
            beta, z, spread = signal(btc_close[i-WINDOW:i], eth_close[i-WINDOW:i],
                                     btc_close[i], eth_close[i])
            if any(quantity):
                if abs(z) < 0.5 or abs(z) > 4:
                    trade(ts, [0.0, 0.0], prices, "z_exit", beta, z)
            elif beta > 0 and abs(z) > 2:
                candidate_entries += 1
                p = float(adfuller(spread, maxlag=10, regression="c", autolag="BIC")[1])
                if p < 0.05:
                    adf_passes += 1
                    direction = -1 if z > 2 else 1
                    gross_btc = nav(prices) / (1 + beta)
                    targets = [direction * math.floor(gross_btc / prices[0] / lots[0]) * lots[0],
                               -direction * math.floor(beta * gross_btc / prices[1] / lots[1]) * lots[1]]
                    if all(abs(q * price) >= minimum for q, price, minimum in
                           zip(targets, prices, minimums)):
                        trade(ts, targets, prices, "entry", beta, z, p)
        value = nav(prices)
        assert math.isfinite(value) and value > 0
        equity.append({"ts": stamp(ts + MINUTE), "usdt": value})

    assert quantity == [0.0, 0.0]
    peaks = np.maximum.accumulate([point["usdt"] for point in equity])
    drawdown = 1 - np.array([point["usdt"] for point in equity]) / peaks
    report = {
        "source": "https://github.com/Bauch0430/crypto-pairs-trading-btc-eth",
        "rule": "previous 720 hourly closes: OLS log(BTC) on log(ETH) with intercept; historical spread mean/sample std and ADF(c,BIC,maxlag=10); current Z >2 or <-2 with p<.05 enters short or long spread; |Z|<.5 or >4 exits; entry beta fixes ETH/BTC notional ratio; no time stop",
        "method": "single chronological holdout, earlier data for rolling estimates only; hourly close available at hour boundary, next hh:01 minute open execution; pre-scheduled terminal exit",
        "oos_start_utc": START, "oos_end_utc": stamp(times[end] + MINUTE),
        "oos_hours": end - start, "initial_capital_usdt": CAPITAL,
        "fee_per_leg_per_side": FEE, "half_spread_per_leg_per_side": HALF_SPREAD,
        "slippage_per_leg_per_side": SLIPPAGE,
        "funding": "actual Binance settlement rate * settlement mark * signed open base quantity; no delivery cost for perpetuals",
        "data": {"BTC": bd, "ETH": ed}, "statsmodels_version": __import__("statsmodels").__version__,
        "candidate_entry_hours": candidate_entries, "adf_pass_entry_hours": adf_passes,
        "net_return_pct": (cash / CAPITAL - 1) * 100,
        "max_drawdown_pct": float(drawdown.max() * 100),
        "executions": len(trades), "round_trips": len([t for t in trades if t["reason"] == "entry"]) // 2,
        "funding_usdt": sum(event["amount_usdt"] for event in funding_events),
        "fee_usdt": sum(t["fee_usdt"] for t in trades),
        "final_equity_usdt": cash, "trades": trades,
        "funding_events": funding_events, "hourly_equity": equity,
        "reproduce": ".\\.venv\\Scripts\\python.exe checks\\perp_pairs_oos.py",
    }
    output = ROOT / "data/runs/perp_pairs_oos_20260929.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in (
        "oos_start_utc", "oos_end_utc", "net_return_pct", "max_drawdown_pct",
        "executions", "funding_usdt", "fee_usdt", "candidate_entry_hours",
        "adf_pass_entry_hours")}, indent=2))
    print(output)


if __name__ == "__main__":
    # A future close changes the numerator, never the historical fit.
    history = np.linspace(100, 120, WINDOW)
    _, z1, _ = signal(history, history / 20, 121, 6)
    _, z2, _ = signal(history, history / 20, 122, 6)
    assert z1 != z2
    main()
