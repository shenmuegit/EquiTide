#!/usr/bin/env python3
"""Evaluate reserved 4h downside-reversal variants on Binance spot 1m bars."""
from __future__ import annotations
import csv, gzip, hashlib, importlib.util, json, math, statistics, sys
from datetime import datetime, timezone
from decimal import Decimal as D
from pathlib import Path
import numpy as np
import polars as pl

ROOT = Path(__file__).resolve().parents[3]
ROUND = Path(__file__).resolve().parent
MIN = 60_000_000_000
H4 = 240 * MIN
DAY = 1440 * MIN
sys.path.insert(0, str(ROOT / "research/automation"))
import registry
sys.path.insert(0, str(ROOT / "research/experiments/20261001T133655Z"))
from kernel import fill

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

cost_engine = load_module("rev4h_lagged_daily_cost_engine", ROOT / "research/experiments/20261001T013355Z/evaluate.py")

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def stamp(ns):
    return datetime.fromtimestamp(ns / 1e9, timezone.utc).isoformat().replace("+00:00", "Z")

def gzwrite(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as zipped:
            zipped.write(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                                    allow_nan=False, default=str).encode())

def load_asset(asset):
    paths = [
        ROOT / f"data/normalized/binance/{asset}/binance_{asset}_20240916T000000Z_20250916T000000Z_transfer_20261001/spot_bars.parquet",
        ROOT / f"data/normalized/binance/{asset}/binance_{asset}_20250916T000000Z_20260916T000000Z_archive_20260929/spot_bars.parquet",
    ]
    frames, manifests = [], []
    for path in paths:
        frame = pl.read_parquet(path, columns=["open_ts", "available_ts", "open", "close", "base_volume", "quote_volume", "is_closed"])
        assert frame.height == 365 * 1440 and frame["is_closed"].all() and frame["open_ts"].is_sorted()
        assert (frame["open_ts"].diff().drop_nulls() == MIN).all()
        assert (frame["available_ts"] - frame["open_ts"] == MIN).all()
        assert (frame["open"] > 0).all() and (frame["close"] > 0).all()
        manifests.append({"path": str(path.relative_to(ROOT)), "sha256": sha(path), "bytes": path.stat().st_size,
                          "bars": frame.height, "first_open_utc": stamp(int(frame["open_ts"][0])),
                          "last_available_utc": stamp(int(frame["available_ts"][-1]))})
        frames.append(frame)
    frame = pl.concat(frames, how="vertical_relaxed").sort("open_ts")
    assert frame.height == 730 * 1440 and (frame["open_ts"].diff().drop_nulls() == MIN).all()
    minute_open = frame["open"].cast(pl.Float64).to_numpy()
    minute_close = frame["close"].cast(pl.Float64).to_numpy()
    minute_quote = frame["quote_volume"].cast(pl.Float64).to_numpy()
    minute_base = frame["base_volume"].cast(pl.Float64).to_numpy()
    minute_ts = frame["open_ts"].to_numpy()
    assert len(minute_ts) % 240 == 0
    bars = []
    for index in range(len(minute_ts) // 240):
        lo, hi = index * 240, (index + 1) * 240
        bars.append({"open_ts": int(minute_ts[lo]), "available_ts": int(minute_ts[hi - 1]) + MIN,
                     "close": D(str(frame["close"][hi - 1])),
                     "quote_volume": sum((D(str(x)) for x in minute_quote[lo:hi]), D(0))})
    daily = []
    for day in range(730):
        lo, hi = day * 1440, (day + 1) * 1440
        daily.append({"date": stamp(int(minute_ts[lo]))[:10], "close": D(str(frame["close"][hi - 1])),
                      "quote_volume": sum((D(str(x)) for x in minute_quote[lo:hi]), D(0))})
    proxy = []
    for bar_index in range(len(bars) + 1):
        mi = bar_index * 240 + 1
        if mi < 5:
            proxy.append(D(0)); continue
        base = sum((D(str(x)) for x in minute_base[mi - 5:mi]), D(0))
        quote = sum((D(str(x)) for x in minute_quote[mi - 5:mi]), D(0))
        proxy.append(quote / base if base else D(0))
    assert stamp(bars[0]["open_ts"]) == "2024-09-16T00:00:00Z"
    assert stamp(bars[-1]["available_ts"]) == "2026-09-16T00:00:00Z"
    assert all(bars[i]["available_ts"] <= bars[i + 1]["open_ts"] for i in range(len(bars) - 1))
    return {"asset": asset, "minute_open": minute_open, "minute_close": minute_close,
            "minute_quote": minute_quote, "minute_base": minute_base, "minute_ts": minute_ts,
            "bars": bars, "daily": daily, "proxy": proxy, "source_files": manifests,
            "bar_close_sha256_f64le": hashlib.sha256(np.asarray([float(x["close"]) for x in bars], dtype="<f8").tobytes()).hexdigest(),
            "daily_close_sha256_f64le": hashlib.sha256(np.asarray([float(x["close"]) for x in daily], dtype="<f8").tobytes()).hexdigest()}

def drawdown(values):
    values = np.asarray(values, dtype=np.float64)
    peaks = np.maximum.accumulate(values)
    ratio = 1.0 - values / peaks
    trough = int(np.argmax(ratio))
    peak = int(np.argmax(values[:trough + 1]))
    return float(ratio[trough] * 100), peak, trough

def metric_summary(values, bars_per_year):
    values = np.asarray(values, dtype=np.float64)
    assert len(values) > 1 and np.all(np.isfinite(values)) and np.all(values > 0)
    returns = values[1:] / values[:-1] - 1
    sd = float(np.std(returns, ddof=1)) if len(returns) > 1 else 0.0
    dd, peak, trough = drawdown(values)
    cagr = (float(values[-1]) / float(values[0])) ** (bars_per_year / (len(values) - 1)) - 1
    return {"net_return_pct": float((values[-1] / values[0] - 1) * 100),
            "max_drawdown_pct": dd,
            "sharpe_annualized": float(np.mean(returns) / sd * math.sqrt(bars_per_year)) if sd else None,
            "cagr_pct": float(cagr * 100), "calmar": float(cagr / (dd / 100)) if dd else None,
            "drawdown_peak_index": peak, "drawdown_trough_index": trough, "observations": len(values) - 1}

def run_one(spec, market, filters, multiplier, comparator=False):
    params = spec["parameters"]
    bars, daily = market["bars"], market["daily"]
    start, end = int(params["oos_start_bar_index"]), int(params["oos_end_exclusive_bar_index"])
    assert (start, end) == (2208, 4368) and end < len(bars)
    capital = D(str(params["initial_capital_usdt"]))
    cash, units = capital, D(0)
    trades, decisions = [], []
    entry_bar = None
    recovery_reference = None
    entry_fraction = D(str(params.get("entry_drop_fraction", 0)))
    max_hold = int(params.get("max_holding_4h_bars", 1))
    close4 = [bar["close"] for bar in bars]

    def execute(bar_index, buy, signal_index, terminal=False):
        nonlocal cash, units
        minute_index = bar_index * 240 + 1
        trade_day = bar_index // 6
        adv, sigma = cost_engine.lagged_cost_inputs(daily, trade_day)
        ref = D(str(market["minute_open"][minute_index]))
        avg_price = market["proxy"][bar_index]
        before_cash, before_units = cash, units
        cash, units, trade = fill(cash, units, buy, ref, D(str(adv)), D(str(sigma)),
                                  multiplier, filters, avg_price)
        signal_available = bars[signal_index]["available_ts"] if signal_index is not None else None
        exec_ns = int(market["minute_ts"][minute_index])
        trade.update({"bar_index": bar_index, "signal_bar_index": signal_index,
                      "signal_available_utc": stamp(signal_available) if signal_available is not None else None,
                      "execution_utc": stamp(exec_ns),
                      "signal_to_execution_seconds": ((exec_ns - signal_available) / 1e9) if signal_available is not None else None,
                      "minute_index": minute_index, "terminal": terminal,
                      "cash_before": str(before_cash), "units_before": str(before_units),
                      "cash_after": str(cash), "units_after": str(units)})
        trades.append(trade)
        return trade, ref

    if comparator:
        trade, ref = execute(start, True, None)
        if trade["status"] == "filled":
            entry_bar = start
    else:
        # The first in-sample OOS decision uses the first newly completed test bar;
        # execution is one bar later, after the fixed 60-second availability buffer.
        for i in range(start + 1, end):
            j = i - 1
            bar_return = close4[j] / close4[j - 1] - 1
            action, reason = None, None
            if units > 0:
                elapsed = i - int(entry_bar)
                if close4[j] >= recovery_reference:
                    action, reason = "sell", "recovered_to_entry_signal_close"
                elif elapsed >= max_hold:
                    action, reason = "sell", "time_exit"
            elif bar_return <= -entry_fraction:
                action, reason = "buy", "completed_4h_return_threshold"
            if action:
                trade, ref = execute(i, action == "buy", j)
                decisions.append({"decision_bar_index": i, "signal_bar_index": j,
                                  "signal_available_utc": stamp(bars[j]["available_ts"]),
                                  "execution_utc": trade["execution_utc"],
                                  "decision_return_fraction": str(bar_return), "action": action,
                                  "reason": reason, "fill_status": trade["status"],
                                  "signal_delay_seconds": trade["signal_to_execution_seconds"]})
                if trade["status"] == "filled":
                    if action == "buy":
                        entry_bar, recovery_reference = i, close4[j]
                    else:
                        entry_bar, recovery_reference = None, None
            # A completed exit decision consumes this bar even after a successful fill;
            # no same-bar re-entry is possible because the loop takes one action/bar.

    start_day, end_day = start // 6, end // 6
    if units > 0:
        trade, terminal_ref = execute(end, False, end - 1, terminal=True)
    else:
        terminal_ref = D(str(market["minute_open"][end * 240 + 1]))

    # Continuous one-minute-close NAV plus an extra immediate post-fill mark for every fill.
    start_min, end_min = start * 240 + 1, end * 240 + 1
    minute_close_nav = np.empty(end_min - start_min, dtype=np.float64)
    immediate_marks = []
    state_cash, state_units = capital, D(0)
    cursor = start_min
    filled = [t for t in trades if t["status"] == "filled"]
    for trade in filled:
        mi = int(trade["minute_index"])
        if mi < cursor:
            continue
        if mi > cursor:
            segment = market["minute_close"][cursor:mi]
            minute_close_nav[cursor - start_min:mi - start_min] = float(state_cash) + float(state_units) * segment
        state_cash = D(trade["cash_after"]); state_units = D(trade["units_after"])
        immediate_marks.append(float(state_cash + state_units * D(trade["reference"])))
        if mi < end_min:
            minute_close_nav[mi - start_min] = float(state_cash) + float(state_units) * float(market["minute_close"][mi])
            cursor = mi + 1
        else:
            cursor = mi
    if cursor < end_min:
        segment = market["minute_close"][cursor:end_min]
        minute_close_nav[cursor - start_min:end_min - start_min] = float(state_cash) + float(state_units) * segment
    terminal_nav = cash + units * terminal_ref
    # Include starting capital, immediate fill marks, each minute close, and the terminal state.
    sampled_nav = np.concatenate((np.asarray([float(capital)]), np.asarray(immediate_marks), minute_close_nav,
                                  np.asarray([float(terminal_nav)])))
    minute_metrics = metric_summary(sampled_nav, 365 * 1440)
    daily_nav = [float(capital)]
    for offset_days in range(1, 360):
        mi = start_min + offset_days * 1440 - 1
        daily_nav.append(float(cash_at_minute(mi, start_min, trades, capital, market)))
    daily_nav.append(float(terminal_nav))
    daily_metrics = metric_summary(daily_nav, 365)
    folds = []
    for fold in range(12):
        a, b = fold * 30, (fold + 1) * 30
        folds.append({"fold": fold + 1, "start_utc": daily[start_day + a]["date"],
                      "end_utc_inclusive": daily[start_day + b - 1]["date"],
                      "net_return_pct": float((daily_nav[b] / daily_nav[a] - 1) * 100)})
    cost_parts = {key: sum((D(t.get("cost_parts", {}).get(key, "0")) for t in trades if t["status"] == "filled"), D(0))
                  for key in ("fee", "half_spread", "slippage", "impact", "tick_rounding")}
    total_cost = sum(cost_parts.values(), D(0))
    pnl = terminal_nav - capital
    gross = pnl + total_cost
    ledger_bytes = b"\n".join(json.dumps(t, sort_keys=True, separators=(",", ":")).encode() for t in trades)
    summary = {**minute_metrics, "daily_mark_max_drawdown_pct": daily_metrics["max_drawdown_pct"],
               "terminal_nav_usdt": str(terminal_nav), "terminal_cash_usdt": str(cash),
               "terminal_units": str(units), "terminal_flat": units == 0,
               "net_pnl_usdt": str(pnl), "cost_usdt": str(total_cost),
               "cost_parts_usdt": {k: str(v) for k, v in cost_parts.items()},
               "gross_reference_pnl_usdt": str(gross),
               "gross_reference_pnl_to_cost": float(gross / total_cost) if total_cost else None,
               "decision_bars_evaluated": end - start - 1, "attempts": len(trades),
               "filled_orders": sum(t["status"] == "filled" for t in trades),
               "round_trips": sum(t["status"] == "filled" and t["side"] == "sell" for t in trades),
               "rejected_orders": sum(t["status"] != "filled" for t in trades),
               "capacity_rejections": sum(t.get("reason") == "participation" for t in trades),
               "positive_1x_folds": sum(f["net_return_pct"] > 0 for f in folds),
               "folds": folds, "cost_multiplier": multiplier,
               "daily_nav_sha256_f64le": hashlib.sha256(np.asarray(daily_nav, dtype="<f8").tobytes()).hexdigest(),
               "minute_sample_nav_sha256_f64le": hashlib.sha256(np.asarray(sampled_nav, dtype="<f8").tobytes()).hexdigest(),
               "minute_close_samples": len(minute_close_nav), "immediate_postfill_marks": len(immediate_marks),
               "event_ledger_sha256": hashlib.sha256(ledger_bytes).hexdigest(),
               "drawdown_scope": "OOS 1m bar-close samples plus immediate post-fill reference marks; no within-minute extrema."}
    archive = {"name": spec["name"], "fingerprint": registry.fingerprint(spec), "spec": spec,
               "decisions": decisions, "trades": trades, "daily_nav_usdt": daily_nav, "summary": summary}
    return archive

def cash_at_minute(minute_index, start_minute, trades, capital, market):
    cash, units = capital, D(0)
    for trade in trades:
        if trade["status"] != "filled" or trade["minute_index"] > minute_index:
            continue
        cash, units = D(trade["cash_after"]), D(trade["units_after"])
    return cash + units * D(str(market["minute_close"][minute_index]))

def main():
    batch = json.loads((ROUND / "batch.json").read_text())
    reservations = json.loads((ROUND / "reserve.json").read_text())
    assert len(batch) == 20 and all(x["exit_code"] == 0 for x in reservations)
    plan = json.loads((ROUND / "plan.json").read_text())
    source = json.loads((ROOT / "research/experiments/20261012T035429Z/report.json").read_text())
    filters = source["plan"]["execution"]["filters"]
    markets = {asset: load_asset(asset) for asset in ("BTC", "ETH")}
    manifest = {"assets": {asset: {"source_files": markets[asset]["source_files"],
                                   "bars_4h": len(markets[asset]["bars"]),
                                   "bar_close_sha256_f64le": markets[asset]["bar_close_sha256_f64le"],
                                   "daily_close_sha256_f64le": markets[asset]["daily_close_sha256_f64le"]}
                           for asset in markets},
                "filters_source": "research/experiments/20261012T035429Z/report.json",
                "filters_source_sha256": sha(ROOT / "research/experiments/20261012T035429Z/report.json"),
                "oos_days": 360, "folds": 12}
    (ROUND / "data_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    run_dir = ROOT / "data/runs" / ROUND.name
    summaries, configs, benchmarks = {}, {}, {}
    for row in batch:
        spec = json.loads((ROOT / row["spec"]).read_text())
        scenarios = {}
        for mult in (1, 2, 3):
            archive = run_one(spec, markets[row["asset"]], filters[row["asset"] + "USDT"], mult, row["is_comparator"])
            scenarios[str(mult)] = archive["summary"]
            gzwrite(run_dir / f"{row['name']}_cost{mult}.json.gz", archive)
        summaries[row["name"]] = scenarios
        if row["is_comparator"]:
            benchmarks[row["name"]] = {"fingerprint": row["fingerprint"], "asset": row["asset"], "scenarios": scenarios}
        else:
            params = spec["parameters"]
            configs[row["name"]] = {"fingerprint": row["fingerprint"], "spec": row["spec"],
                                     "asset": row["asset"], "entry_drop_fraction": params["entry_drop_fraction"],
                                     "max_holding_4h_bars": params["max_holding_4h_bars"], "scenarios": scenarios}
        print(f"{row['name']} 1x={scenarios['1']['net_return_pct']:.5f}% 3x={scenarios['3']['net_return_pct']:.5f}%", flush=True)

    levels = [0.005, 0.01, 0.015]
    holds = [1, 2, 4]
    for name, cfg in configs.items():
        neighbors = [other for other in configs.values() if other["asset"] == cfg["asset"]
                     and abs(levels.index(other["entry_drop_fraction"]) - levels.index(cfg["entry_drop_fraction"])) <= 1
                     and abs(holds.index(other["max_holding_4h_bars"]) - holds.index(cfg["max_holding_4h_bars"])) <= 1]
        fraction = sum(x["scenarios"]["3"]["net_return_pct"] > 0 for x in neighbors) / len(neighbors)
        cfg["neighborhood_size"] = len(neighbors)
        cfg["neighbor_3x_positive_fraction"] = fraction
        s1, s2, s3 = (cfg["scenarios"][str(m)] for m in (1, 2, 3))
        gates = {"all_1x_2x_3x_positive": all(x["net_return_pct"] > 0 for x in (s1, s2, s3)),
                 "minimum_positive_1x_folds": s1["positive_1x_folds"] >= 6,
                 "maximum_3x_drawdown_pct_25": s3["max_drawdown_pct"] <= 25,
                 "neighbor_3x_positive_fraction_60": fraction >= 0.60,
                 "minimum_1x_round_trips_20": s1["round_trips"] >= 20,
                 "gross_pnl_to_1x_cost_2_5": s1["gross_reference_pnl_to_cost"] is not None and s1["gross_reference_pnl_to_cost"] >= 2.5,
                 "no_rejections_or_capacity_breaches": all(x["rejected_orders"] == 0 and x["capacity_rejections"] == 0 for x in (s1, s2, s3)),
                 "terminal_flat": all(x["terminal_flat"] for x in (s1, s2, s3))}
        cfg["gates"] = gates
        cfg["status"] = "passed" if all(gates.values()) else "rejected"

    ranked = sorted(configs, key=lambda name: configs[name]["scenarios"]["1"]["net_return_pct"], reverse=True)
    report = {"round": ROUND.name, "evaluated_at_utc": datetime.now(timezone.utc).isoformat(),
              "plan": plan, "data_manifest": manifest,
              "summary": {"candidate_configs": len(configs), "candidate_passed": sum(configs[n]["status"] == "passed" for n in configs),
                          "candidate_rejected": sum(configs[n]["status"] == "rejected" for n in configs),
                          "benchmarks": len(benchmarks), "cost_scenes": (len(configs) + len(benchmarks)) * 3,
                          "oos_days": 360, "folds": 12, "ranking_1x": ranked},
              "configs": configs, "benchmarks": benchmarks,
              "comparison": "Cash has 0% net return; benchmarks use matched BTC or ETH exposure and the same cost model.",
              "selection_bias": "All 2024-09-16/2026-09-16 source history has appeared in repeated research and is not an untouched final test.",
              "nav_scope": "Continuous 1m close NAV plus immediate post-fill marks for sampled maximum drawdown; no sub-minute path or L2 order book is available."}
    (ROUND / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False, default=str) + "\n")
    with (ROUND / "sensitivity.csv").open("w", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["name", "asset", "entry_drop_fraction", "max_holding_4h_bars", "return_1x", "return_2x", "return_3x", "dd_3x", "neighbor_3x_positive_fraction", "status"])
        for name in ranked:
            cfg = configs[name]
            writer.writerow([name, cfg["asset"], cfg["entry_drop_fraction"], cfg["max_holding_4h_bars"],
                             *[cfg["scenarios"][str(m)]["net_return_pct"] for m in (1, 2, 3)],
                             cfg["scenarios"]["3"]["max_drawdown_pct"], cfg["neighbor_3x_positive_fraction"], cfg["status"]])
    print(json.dumps(report["summary"], indent=2, ensure_ascii=False), flush=True)

if __name__ == "__main__":
    main()
