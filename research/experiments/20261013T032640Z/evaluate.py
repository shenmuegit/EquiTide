#!/usr/bin/env python3
"""Run the preregistered Cutler-RSI(2) daily regime-filtered spot grid."""
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
DAY = 1440 * MIN
sys.path.insert(0, str(ROOT / "research/automation"))
import registry


def loadmod(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


engine = loadmod("daily_rsi_cost_engine", ROOT / "research/experiments/20261001T013355Z/evaluate.py")
from importlib.util import spec_from_file_location
ks = spec_from_file_location("daily_rsi_fill_kernel", ROOT / "research/experiments/20261001T133655Z/kernel.py")
kernel = importlib.util.module_from_spec(ks); sys.modules[ks.name] = kernel; ks.loader.exec_module(kernel)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stamp(ns):
    return datetime.fromtimestamp(ns / 1e9, timezone.utc).isoformat().replace("+00:00", "Z")


def load_asset(asset):
    paths = [
        ROOT / f"data/normalized/binance/{asset}/binance_{asset}_20240916T000000Z_20250916T000000Z_transfer_20261001/spot_bars.parquet",
        ROOT / f"data/normalized/binance/{asset}/binance_{asset}_20250916T000000Z_20260916T000000Z_archive_20260929/spot_bars.parquet",
    ]
    frames, source_files = [], []
    for path in paths:
        frame = pl.read_parquet(path, columns=["open_ts", "available_ts", "open", "close", "base_volume", "quote_volume", "is_closed"])
        assert frame.height == 365 * 1440 and frame["is_closed"].all() and frame["open_ts"].is_sorted()
        assert (frame["open_ts"].diff().drop_nulls() == MIN).all()
        assert (frame["available_ts"] - frame["open_ts"] == MIN).all()
        assert (frame["quote_volume"] >= 0).all() and (frame["base_volume"] >= 0).all()
        source_files.append({"path": str(path.relative_to(ROOT)), "sha256": sha(path), "bytes": path.stat().st_size, "bars": frame.height})
        frames.append(frame)
    frame = pl.concat(frames, how="vertical_relaxed").sort("open_ts")
    assert frame.height == 730 * 1440 and (frame["open_ts"].diff().drop_nulls() == MIN).all()
    op = frame["open"].to_list(); cl = frame["close"].to_list()
    bv = frame["base_volume"].to_list(); qv = frame["quote_volume"].to_list()
    ts = frame["open_ts"].to_list(); av = frame["available_ts"].to_list()
    daily = []
    for d in range(730):
        lo, hi = d * 1440, (d + 1) * 1440
        close_i, trade_i = hi - 1, lo + 1
        assert av[close_i] == ts[lo] + DAY and ts[trade_i] == ts[lo] + MIN
        base5 = sum((D(str(x)) for x in bv[trade_i - 5:trade_i]), D(0))
        quote5 = sum((D(str(x)) for x in qv[trade_i - 5:trade_i]), D(0))
        row = {
            "date": datetime.fromtimestamp(ts[lo] / 1e9, timezone.utc).date().isoformat(),
            "day_open_ns": int(ts[lo]), "close": D(str(cl[close_i])),
            "close_available_ts": int(av[close_i]), "quote_volume": sum((D(str(x)) for x in qv[lo:hi]), D(0)),
            "base_volume": sum((D(str(x)) for x in bv[lo:hi]), D(0)),
            "trade_ts": int(ts[trade_i]), "trade_open": D(str(op[trade_i])),
            "proxy_vwap5": quote5 / base5 if base5 else D(0),
        }
        daily.append(row)
    assert daily[0]["date"] == "2024-09-16" and daily[-1]["date"] == "2026-09-15"
    return {"asset": asset, "daily": daily, "minute_open": op, "minute_close": cl, "minute_ts": ts,
            "source_files": source_files,
            "daily_close_sha256_f64le": hashlib.sha256(np.asarray([float(x["close"]) for x in daily], dtype="<f8").tobytes()).hexdigest()}


def features(daily, rsi_n, trend_n):
    closes = [x["close"] for x in daily]
    rsi = [None] * len(daily); sma = [None] * len(daily)
    for i in range(1, len(daily)):
        if i >= rsi_n:
            changes = [closes[j] - closes[j - 1] for j in range(i - rsi_n + 1, i + 1)]
            gains = sum((max(x, D(0)) for x in changes), D(0)) / rsi_n
            losses = sum((max(-x, D(0)) for x in changes), D(0)) / rsi_n
            total = gains + losses
            rsi[i] = D(50) if total == 0 else D(100) * gains / total
    for i in range(trend_n - 1, len(daily)):
        sma[i] = sum(closes[i - trend_n + 1:i + 1], D(0)) / trend_n
    return rsi, sma


def nav_metrics(values):
    assert len(values) > 1 and all(x > 0 and math.isfinite(x) for x in values)
    peak, dd = values[0], 0.0
    for value in values:
        peak = max(peak, value); dd = max(dd, (peak - value) / peak)
    ret = [b / a - 1 for a, b in zip(values, values[1:])]
    sd = statistics.stdev(ret) if len(ret) > 1 else 0.0
    cagr = (values[-1] / values[0]) ** (365 / len(ret)) - 1
    return {"net_return_pct": 100 * (values[-1] / values[0] - 1), "max_drawdown_pct": 100 * dd,
            "sharpe_annualized_daily": statistics.mean(ret) / sd * math.sqrt(365) if sd else None,
            "cagr_pct": 100 * cagr, "calmar": cagr / dd if dd else None, "daily_marks": len(values) - 1}


def run(spec, market, filters, multiplier, hold_reference=False):
    p = spec["parameters"]; rows = market["daily"]
    start = next(i for i, x in enumerate(rows) if x["date"] == p["oos_start_utc"][:10])
    end = next(i for i, x in enumerate(rows) if x["date"] == p["oos_terminal_utc"][:10])
    assert start >= max(p["trend_sma_days"] if not hold_reference else 1, p.get("rsi_lookback_changes", 1))
    rsi, sma = features(rows, p.get("rsi_lookback_changes", 1), p.get("trend_sma_days", 1))
    capital = D(str(p["initial_capital_usdt"])); cash, units = capital, D(0)
    nav = [float(capital)]; trades = []; actions = []

    def execute(day_i, buy, terminal=False, signal_i=None):
        nonlocal cash, units
        row = rows[day_i]; adv, sigma = engine.lagged_cost_inputs(rows, day_i)
        before_cash, before_units = cash, units
        cash, units, trade = kernel.fill(cash, units, buy, row["trade_open"], D(str(adv)), D(str(sigma)), multiplier,
                                         filters, row["proxy_vwap5"])
        trade.update({"asset": market["asset"], "date": row["date"], "day_index": day_i,
                      "signal_day": rows[signal_i]["date"] if signal_i is not None else None,
                      "signal_available_utc": stamp(rows[signal_i]["close_available_ts"]) if signal_i is not None else None,
                      "execution_utc": stamp(row["trade_ts"]),
                      "signal_to_execution_seconds": (row["trade_ts"] - rows[signal_i]["close_available_ts"]) / 1e9 if signal_i is not None else None,
                      "terminal": terminal, "cash_before": str(before_cash), "units_before": str(before_units),
                      "cash_after": str(cash), "units_after": str(units)})
        trades.append(trade)
        nav.append(float(cash + units * row["trade_open"]))
        return trade

    state = "cash"
    for day_i in range(start, end):
        signal_i = day_i - 1
        assert rows[signal_i]["close_available_ts"] < rows[day_i]["trade_ts"]
        if hold_reference:
            action = "buy" if day_i == start and state == "cash" else None
        else:
            desired_enter = rsi[signal_i] is not None and rsi[signal_i] <= D(str(p["entry_rsi"])) and rows[signal_i]["close"] > sma[signal_i]
            should_exit = rsi[signal_i] is not None and (rsi[signal_i] >= D(str(p["exit_rsi"])) or rows[signal_i]["close"] <= sma[signal_i])
            action = "sell" if state == "coin" and should_exit else ("buy" if state == "cash" and desired_enter else None)
        if action:
            t = execute(day_i, action == "buy", False, signal_i)
            if t["status"] == "filled": state = "coin" if action == "buy" else "cash"
            actions.append({"signal_day": rows[signal_i]["date"], "execution_day": rows[day_i]["date"], "action": action,
                            "rsi2": str(rsi[signal_i]) if rsi[signal_i] is not None else None,
                            "sma": str(sma[signal_i]) if sma[signal_i] is not None else None,
                            "close": str(rows[signal_i]["close"])})
        nav.append(float(cash + units * rows[day_i]["close"]))
    if state == "coin":
        t = execute(end, False, True, end - 1)
        if t["status"] == "filled": state = "cash"
    terminal_nav = float(cash + units * rows[end]["trade_open"])
    nav.append(terminal_nav)
    # Rebuild daily marks from the continuous cash/units ledger, carrying positions across folds.
    cash_m, units_m = capital, D(0); daily_nav = [float(capital)]; by_day = {}
    for t in trades:
        if t["status"] == "filled": by_day.setdefault(t["day_index"], []).append(t)
    for day_i in range(start, end):
        for t in by_day.get(day_i, []):
            cash_m, units_m = D(t["cash_after"]), D(t["units_after"])
        daily_nav.append(float(cash_m + units_m * rows[day_i]["close"]))
    if not hold_reference and state == "cash" and daily_nav[-1] != terminal_nav:
        pass
    # The year has exactly twelve folds; include costed terminal liquidation in the final fold endpoint.
    daily_nav[-1] = terminal_nav
    stats = nav_metrics(daily_nav)
    peak, sample_dd = nav[0], 0.0
    for mark in nav:
        peak = max(peak, mark); sample_dd = max(sample_dd, (peak - mark) / peak)
    day_count = end - start
    folds = []
    for f in range(12):
        a, b = f * 30, (f + 1) * 30
        folds.append({"fold": f + 1, "start_utc": rows[start + a]["date"], "end_utc_inclusive": rows[start + b - 1]["date"],
                      "net_return_pct": 100 * (daily_nav[b] / daily_nav[a] - 1), "nav_start": daily_nav[a], "nav_end": daily_nav[b]})
    costs = {k: str(sum((D(t["cost_parts"][k]) for t in trades if t["status"] == "filled"), D(0))) for k in ("fee", "half_spread", "slippage", "impact", "tick_rounding")}
    cost = sum((D(x) for x in costs.values()), D(0)); pnl = D(str(terminal_nav)) - capital
    summary = {**stats, "max_drawdown_pct": 100 * sample_dd, "daily_close_sample_drawdown_pct": stats["max_drawdown_pct"],
               "net_pnl_usdt": str(pnl), "terminal_nav_usdt": str(terminal_nav), "terminal_cash_usdt": str(cash),
               "terminal_units": str(units), "terminal_state": state, "cost_usdt": str(cost), "cost_parts_usdt": costs,
               "gross_reference_pnl_usdt": str(pnl + cost), "gross_reference_pnl_to_cost": float((pnl + cost) / cost) if cost else None,
               "round_trips": sum(t["status"] == "filled" and t["side"] == "sell" for t in trades),
               "filled_orders": sum(t["status"] == "filled" for t in trades), "rejected_orders": sum(t["status"] != "filled" for t in trades),
               "positive_1x_folds": sum(x["net_return_pct"] > 0 for x in folds), "folds": folds,
               "cost_multiplier": multiplier, "daily_nav_samples": len(daily_nav),
               "drawdown_scope": "daily close NAV plus immediate post-fill reference marks and terminal liquidation; no minute/intraday extrema",
               "unfolded_remainder_days": day_count - 360}
    return {"summary": summary, "trades": trades, "actions": actions, "daily_nav_usdt": daily_nav,
            "daily_nav_sha256_f64le": hashlib.sha256(np.asarray(daily_nav, dtype="<f8").tobytes()).hexdigest()}


def main():
    plan = json.loads((ROUND / "plan.json").read_text())
    reserve = json.loads((ROUND / "reserve.json").read_text())
    benchmark_reserve = json.loads((ROUND / "benchmark_reserve.json").read_text())
    assert all(x["exit_code"] == 0 for x in reserve + benchmark_reserve)
    base_report = json.loads((ROOT / "research/experiments/20261012T035429Z/report.json").read_text())
    filters = base_report["plan"]["execution"]["filters"]
    markets = {a: load_asset(a) for a in ("BTC", "ETH")}
    filter_path = ROOT / "research/experiments/20261012T035429Z/report.json"
    manifest = {"source_files": {a: markets[a]["source_files"] for a in markets},
                "daily_close_sha256_f64le": {a: markets[a]["daily_close_sha256_f64le"] for a in markets},
                "exchange_filter_source": "research/experiments/20261012T035429Z/report.json",
                "exchange_filter_source_sha256": sha(filter_path),
                "data_period_utc": "2024-09-16/2026-09-16", "oos_period_utc": "2026-03-16/2026-09-15"}
    configs = {}
    run_dir = ROOT / "data/runs" / ROUND.name; run_dir.mkdir(parents=True, exist_ok=True)
    for row in reserve:
        spec = json.loads((ROOT / row["spec"]).read_text())
        asset = spec["universe"][0].split("/")[0]
        outcomes = {str(m): run(spec, markets[asset], filters[asset + "USDT"], m) for m in (1, 2, 3)}
        cfg = {"fingerprint": row.get("fingerprint") or row["output"], "spec": row["spec"], "asset": asset, "scenarios": {m: x["summary"] for m, x in outcomes.items()},
               "trades_1x": outcomes["1"]["trades"], "actions_1x": outcomes["1"]["actions"], "daily_nav_1x": outcomes["1"]["daily_nav_usdt"],
               "daily_nav_hashes": {m: x["daily_nav_sha256_f64le"] for m, x in outcomes.items()}}
        configs[spec["name"]] = cfg
        for m, out in outcomes.items():
            p = run_dir / f"{spec['name']}_cost{m}.json.gz"
            with p.open("wb") as f:
                with gzip.GzipFile(filename="", mode="wb", fileobj=f, mtime=0) as gz:
                    gz.write(json.dumps(out, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode())
        print(spec["name"], *(round(outcomes[str(m)]["summary"]["net_return_pct"], 4) for m in (1, 2, 3)), flush=True)
    # Reused interval benchmark, using the same lot/cost kernel and capital as each candidate.
    benchmarks = {}
    for row in benchmark_reserve:
        spec = json.loads((ROOT / row["spec"]).read_text())
        asset = spec["universe"][0].split("/")[0]
        outcomes = {str(m): run(spec, markets[asset], filters[asset + "USDT"], m, True) for m in (1, 2, 3)}
        for m, out in outcomes.items():
            with (run_dir / f"buy_hold_{asset.lower()}_cost{m}.json.gz").open("wb") as f:
                with gzip.GzipFile(filename="", mode="wb", fileobj=f, mtime=0) as gz:
                    gz.write(json.dumps(out, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode())
        benchmarks[asset] = {"fingerprint": row.get("fingerprint") or row["output"], "spec": row["spec"],
                             "artifacts": {m: f"data/runs/{ROUND.name}/buy_hold_{asset.lower()}_cost{m}.json.gz" for m in outcomes},
                             "scenarios": {m: out["summary"] for m, out in outcomes.items()}}
    for cfg in configs.values():
        cfg["excess_vs_asset_buy_hold_1x_percentage_points"] = cfg["scenarios"]["1"]["net_return_pct"] - benchmarks[cfg["asset"]]["scenarios"]["1"]["net_return_pct"]
    for cfg in configs.values():
        s = json.loads((ROOT / cfg["spec"]).read_text()); p = s["parameters"]
        near = []
        for other in configs.values():
            if other["asset"] != cfg["asset"]: continue
            q = json.loads((ROOT / other["spec"]).read_text())["parameters"]
            if abs(q["entry_rsi"] - p["entry_rsi"]) <= 5 and abs(q["trend_sma_days"] - p["trend_sma_days"]) <= 50:
                near.append(other)
        positive_fraction = sum(x["scenarios"]["3"]["net_return_pct"] > 0 for x in near) / len(near)
        for val in cfg["scenarios"].values():
            val["neighborhood_positive_fraction_3x"] = positive_fraction; val["neighborhood_size"] = len(near)
        c = cfg["scenarios"]; base = c["1"]
        gates = {"all_cost_multipliers_positive": all(c[str(m)]["net_return_pct"] > 0 for m in (1, 2, 3)),
                 "positive_1x_folds_at_least_8_of_12": base["positive_1x_folds"] >= 8,
                 "3x_drawdown_at_most_25pct": c["3"]["max_drawdown_pct"] <= 25,
                 "3x_neighborhood_positive_fraction_at_least_0_60": positive_fraction >= 0.6,
                 "minimum_two_round_trips": base["round_trips"] >= 2,
                 "gross_reference_pnl_to_1x_cost_at_least_2_5": base["gross_reference_pnl_to_cost"] is not None and base["gross_reference_pnl_to_cost"] >= 2.5,
                 "no_rejected_orders": all(c[str(m)]["rejected_orders"] == 0 for m in (1, 2, 3)),
                 "terminal_flat": all(D(c[str(m)]["terminal_units"]) == 0 for m in (1, 2, 3))}
        cfg["gates"] = gates; cfg["status"] = "passed" if all(gates.values()) else "rejected"
    statuses = {k: sum(v["status"] == k for v in configs.values()) for k in ("passed", "rejected")}
    cliffs = {}
    for asset in ("BTC", "ETH"):
        for mult in ("1", "2", "3"):
            surface = []
            for name, cfg in configs.items():
                if cfg["asset"] != asset: continue
                p = json.loads((ROOT / cfg["spec"]).read_text())["parameters"]
                surface.append((p["entry_rsi"], p["trend_sma_days"], cfg["scenarios"][mult]["net_return_pct"]))
            diffs = []
            for a in surface:
                for b in surface:
                    if (a[0] == b[0] and abs(a[1] - b[1]) == 50) or (a[1] == b[1] and abs(a[0] - b[0]) == 5):
                        if a < b: diffs.append(abs(a[2] - b[2]))
            sd = statistics.stdev(diffs) if len(diffs) > 1 else 0.0
            cliffs[f"{asset}_{mult}x"] = {"adjacent_pair_count": len(diffs), "maximum_absolute_adjacent_return_difference_pp": max(diffs, default=0.0),
                                           "stddev_absolute_adjacent_return_difference_pp": sd,
                                           "cliff_over_two_stddev": bool(sd and max(diffs) > 2 * sd)}
    robustness = {asset: {str(m): sum(c["asset"] == asset and c["scenarios"][str(m)]["net_return_pct"] > 0 for c in configs.values()) / 9 for m in (1, 2, 3)} for asset in ("BTC", "ETH")}
    report = {"round": ROUND.name, "evaluation_started_utc": datetime.now(timezone.utc).isoformat(), "plan": plan,
              "data_manifest": manifest, "summary": {"configs": len(configs), **statuses, "assets": 2, "cost_scenes": (len(configs) + len(benchmarks)) * 3,
              "oos_days": 360, "walk_forward_folds": 12, "fold_days": 30, "remainder_days": 0,
              "positive_configuration_fraction_by_asset_cost": robustness,
              "prior_completed_unique_fingerprint_count": 4349,
              "ranking_1x": sorted(configs, key=lambda k: configs[k]["scenarios"]["1"]["net_return_pct"], reverse=True)},
              "configs": configs, "benchmarks": benchmarks,
              "sensitivity": {"adjacent_surface_cliff_diagnostics": cliffs, "axes": ["entry_rsi", "trend_sma_days"], "neighbor_positive_fraction_basis": "3x net return over own asset's 3x3 neighboring grid including center"},
              "validation_note": "This interval is repeatedly used development/validation history, not a final untouched holdout; no candidate fitting occurred.",
              "reproduce": f"./.venv/bin/python {ROUND.relative_to(ROOT)}/evaluate.py"}
    (ROUND / "data_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    (ROUND / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False) + "\n")
    with (ROUND / "sensitivity.csv").open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n"); w.writerow(["name", "asset", "entry_rsi", "trend_sma_days", "1x_return_pct", "2x_return_pct", "3x_return_pct", "3x_max_dd_pct", "3x_neighbor_positive_fraction", "status"])
        for name in report["summary"]["ranking_1x"]:
            c = configs[name]; p = json.loads((ROOT / c["spec"]).read_text())["parameters"]
            w.writerow([name, c["asset"], p["entry_rsi"], p["trend_sma_days"], *(c["scenarios"][str(m)]["net_return_pct"] for m in (1, 2, 3)), c["scenarios"]["3"]["max_drawdown_pct"], c["scenarios"]["3"]["neighborhood_positive_fraction_3x"], c["status"]])
    print(json.dumps(report["summary"], indent=2))


if __name__ == "__main__": main()
