#!/usr/bin/env python3
"""Evaluate the reserved 150-300 day BTC/ETH SMA band grid on 1m Binance bars."""
from __future__ import annotations

import csv
import gzip
import hashlib
import importlib.util
import json
import math
import statistics
import sys
from datetime import datetime, timezone
from decimal import Decimal as D
from pathlib import Path

import numpy as np
import polars as pl

ROOT = Path(__file__).resolve().parents[3]
ROUND = Path(__file__).resolve().parent
MIN = 60_000_000_000
DAY = 86_400_000_000_000
SPAN = 1441
TRAIN_END_DATE = "2025-09-16"
OUT_START_DATE = "2025-09-19"
DATA_END_DATE = "2026-09-16"
MULTIPLIERS = (1, 2, 3)
sys.path.insert(0, str(ROOT / "research/automation"))
import registry

# The reused engine imports `kernel` by module name; match the working R49 harness.
sys.path.insert(0, str(ROOT / "research/experiments/20261001T133655Z"))


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


core = load_module("r50_shared_daily_engine", ROOT / "research/experiments/20261001T133655Z/evaluate.py")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value):
    return json.loads(json.dumps(value, ensure_ascii=False, default=str, allow_nan=False))


def gzwrite(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(canonical(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as zf:
            zf.write(payload)


def stamp(ns: int) -> str:
    return datetime.fromtimestamp(ns / 1e9, timezone.utc).isoformat().replace("+00:00", "Z")


def build_market(asset: str) -> tuple[list[dict], np.ndarray, dict]:
    paths = [
        ROOT / f"data/normalized/binance/{asset}/binance_{asset}_20240916T000000Z_20250916T000000Z_transfer_20261001/spot_bars.parquet",
        ROOT / f"data/normalized/binance/{asset}/binance_{asset}_20250916T000000Z_20260916T000000Z_archive_20260929/spot_bars.parquet",
    ]
    frames = []
    file_info = []
    for path in paths:
        frame = pl.read_parquet(path, columns=["open_ts", "available_ts", "open", "close", "base_volume", "quote_volume", "is_closed"])
        assert frame.height == 365 * 1440 and frame["is_closed"].all()
        assert frame["open_ts"].is_sorted()
        assert (frame["open_ts"].diff().drop_nulls() == MIN).all()
        assert (frame["available_ts"] - frame["open_ts"] == MIN).all()
        assert (frame["open"] > 0).all() and (frame["close"] > 0).all()
        assert (frame["base_volume"] >= 0).all() and (frame["quote_volume"] >= 0).all()
        file_info.append({"path": str(path.relative_to(ROOT)), "sha256": sha(path), "bars": frame.height,
                          "first_open_ns": int(frame["open_ts"][0]), "last_open_ns": int(frame["open_ts"][-1]),
                          "bytes": path.stat().st_size})
        frames.append(frame)
    minute = pl.concat(frames, how="vertical_relaxed").sort("open_ts")
    assert minute.height == 730 * 1440
    assert (minute["open_ts"].diff().drop_nulls() == MIN).all()
    open_ns = minute["open_ts"].to_numpy()
    close_prices = minute["close"].cast(pl.Float64).to_numpy()
    day = (pl.col("open_ts") // DAY).alias("day")
    daily = minute.group_by(day).agg(
        pl.col("close").last().alias("close"),
        pl.col("available_ts").last().alias("close_available_ts"),
        pl.col("quote_volume").sum().alias("quote_volume"),
        pl.col("base_volume").sum().alias("base_volume"),
    ).sort("day")
    opens = minute.filter((pl.col("open_ts") % DAY) == MIN).select(
        (pl.col("open_ts") // DAY).alias("day"), pl.col("open_ts").alias("trade_ts"), pl.col("open").alias("trade_open")
    )
    d = daily.join(opens, on="day", how="inner").sort("day")
    assert d.height == 730
    rows = []
    for i, row in enumerate(d.iter_rows(named=True)):
        day_open_ns = int(row["day"]) * DAY
        assert int(row["trade_ts"]) == day_open_ns + MIN
        assert int(row["close_available_ts"]) == day_open_ns + DAY
        assert int(row["close_available_ts"]) < (int(row["trade_ts"]) + DAY)
        # Five closed one-minute bars ending at the 00:00 UTC bar are available at 00:01.
        minute_index = i * 1440 + 1
        if minute_index >= 5:
            prior = minute.slice(minute_index - 5, 5)
            assert int(prior["available_ts"].max()) <= int(row["trade_ts"])
            qv = sum((D(str(v)) for v in prior["quote_volume"].to_list()), D(0))
            bv = sum((D(str(v)) for v in prior["base_volume"].to_list()), D(0))
            proxy = qv / bv if bv > 0 else D(0)
        else:
            # Cost logic has no valid 20-day ADV input at the dataset origin either.
            proxy = D(0)
        rows.append({
            "date": datetime.fromtimestamp(day_open_ns / 1e9, timezone.utc).date().isoformat(),
            "day_open_ns": day_open_ns,
            "close": str(row["close"]),
            "close_available_ts": int(row["close_available_ts"]),
            "quote_volume": str(row["quote_volume"]),
            "base_volume": str(row["base_volume"]),
            "trade_ts": int(row["trade_ts"]),
            "trade_open": str(row["trade_open"]),
            "proxy_vwap5": str(proxy),
        })
    assert rows[0]["date"] == "2024-09-16" and rows[-1]["date"] == "2026-09-15"
    assert all(rows[i]["close_available_ts"] < rows[i + 1]["trade_ts"] for i in range(len(rows) - 1))
    return rows, close_prices, {"asset": asset, "files": file_info, "total_minutes": minute.height,
                                "daily_count": len(rows), "first_daily_close_utc": rows[0]["date"],
                                "last_daily_close_utc": rows[-1]["date"],
                                "minute_close_array_sha256_f64le": hashlib.sha256(close_prices.astype("<f8", copy=False).tobytes()).hexdigest()}


def drawdown(values: list[float] | np.ndarray) -> tuple[float, int, int]:
    peak = float(values[0])
    peak_index = 0
    best = 0.0
    best_peak = best_trough = 0
    for i, value in enumerate(values):
        value = float(value)
        if value > peak:
            peak, peak_index = value, i
        dd = 1.0 - value / peak
        if dd > best:
            best, best_peak, best_trough = dd, peak_index, i
    return best * 100.0, best_peak, best_trough


def daily_stats(values: list[float]) -> dict:
    assert len(values) > 1 and all(v > 0 and math.isfinite(v) for v in values)
    rets = [b / a - 1.0 for a, b in zip(values, values[1:])]
    sd = statistics.stdev(rets) if len(rets) > 1 else 0.0
    sharpe = statistics.mean(rets) / sd * math.sqrt(365) if sd else None
    dd, peak_i, trough_i = drawdown(values)
    n = len(rets)
    cagr = (values[-1] / values[0]) ** (365.0 / n) - 1.0
    return {"net_return_pct": (values[-1] / values[0] - 1.0) * 100.0,
            "daily_mark_drawdown_pct": dd, "sharpe_365": sharpe,
            "cagr_pct": 100 * cagr, "calmar": cagr / (dd / 100) if dd > 0 else None,
            "return_observations": n, "drawdown_peak_index": peak_i, "drawdown_trough_index": trough_i}


def scene_summary(vector: np.ndarray, daily_nav: list[float], trades: list[dict], capital: D,
                  terminal_cash: D, terminal_units: D, terminal_ref: D, folds: list[dict],
                  oos_start: int, cost_multiplier: int) -> dict:
    terminal_value = terminal_cash + terminal_units * terminal_ref
    # Replace the last daily close observation with terminal proceeds so the exit cost is in the final OOS return.
    daily_path = list(daily_nav)
    daily_path[-1] = float(terminal_value)
    daily = daily_stats(daily_path)
    minute_dd, peak_i, trough_i = drawdown(vector)
    fill_rows = [t for t in trades if t["status"] == "filled"]
    cost_parts = {key: str(sum((D(t["cost_parts"][key]) for t in fill_rows), D(0)))
                  for key in ("fee", "half_spread", "slippage", "impact", "tick_rounding")}
    cost_total = sum((D(x) for x in cost_parts.values()), D(0))
    gross_ref_pnl = terminal_value - capital + cost_total
    fold_rows = []
    for f in folds:
        a = f["test_start_index"] - oos_start
        b = f["test_end_exclusive_index"] - oos_start
        sub = daily_path[a:b + 1]
        fstats = daily_stats(sub)
        fold_rows.append({"fold": f["fold"], "test_start_index": f["test_start_index"],
                          "test_end_exclusive_index": f["test_end_exclusive_index"],
                          "start_utc": f["start_utc"], "end_exclusive_utc": f["end_exclusive_utc"], **fstats})
    nav_difference = terminal_value - capital
    assert abs(float(gross_ref_pnl - cost_total) - float(nav_difference)) < 1e-7 or terminal_units != 0
    return {
        **daily,
        "net_PnL_usdt": str(terminal_value - capital),
        "cost_usdt": str(cost_total),
        "cost_pct_initial": float(cost_total / capital * 100),
        "cost_parts_usdt": cost_parts,
        "gross_reference_PnL_usdt": str(gross_ref_pnl),
        "gross_reference_PnL_to_cost": float(gross_ref_pnl / cost_total) if cost_total > 0 else None,
        "max_drawdown_pct": minute_dd,
        "minute_close_sample_drawdown_scope": "Maximum drawdown sampled at each available one-minute bar close plus post-trade reference snapshots; does not capture within-minute extrema.",
        "drawdown_peak_index_minute_samples": peak_i,
        "drawdown_trough_index_minute_samples": trough_i,
        "executions": len(fill_rows),
        "attempts": len(trades),
        "round_trips": sum(t["side"] != "buy" for t in fill_rows),
        "rejected_orders": len(trades) - len(fill_rows),
        "cash_or_units_violations": sum(D(t["cash_after"]) < 0 or D(t["units_after"]) < 0 for t in trades),
        "terminal_units": str(terminal_units),
        "terminal_cash": str(terminal_cash),
        "terminal_NAV_usdt": str(terminal_value),
        "terminal_cost_included": True,
        "cost_multiplier": cost_multiplier,
        "folds": fold_rows,
        "NAV_points": int(len(vector)),
        "NAV_sha256_f64le": hashlib.sha256(vector.astype("<f8", copy=False).tobytes()).hexdigest(),
    }


def simulate_candidate(spec: dict, rows: list[dict], minute_closes: np.ndarray, start: int, end: int,
                       folds: list[dict], multiplier: int, filters: dict) -> dict:
    p = spec["parameters"]
    n = int(p["lookback_days"])
    band = D(str(p["symmetric_threshold_fraction"]))
    capital = D(str(p["initial_capital_usdt"]))
    closes = [D(r["close"]) for r in rows]
    sma = [None] * len(rows)
    running = sum(closes[:n], D(0))
    if n < len(rows):
        sma[n] = running / n
    for i in range(n + 1, len(rows)):
        running += closes[i - 1] - closes[i - n - 1]
        sma[i] = running / n

    cash, units = capital, D(0)
    desired = False
    trades, decisions = [], []
    days = end - start
    point_count = days * SPAN + 2
    vector = np.empty(point_count, dtype=np.float64)
    vector[0] = float(capital)
    daily_path = [float(capital)]

    def execute(i: int, buy: bool, terminal: bool = False) -> None:
        nonlocal cash, units
        adv, sigma = core.engine.lagged_cost_inputs(rows, i)
        cash, units, trade = core.fill(cash, units, bool(buy), D(rows[i]["trade_open"]),
                                      D(str(adv)), D(str(sigma)), multiplier, filters,
                                      D(rows[i]["proxy_vwap5"]))
        trade.update({"decision_index": i, "signal_close_date": rows[i - 1]["date"] if i > 0 else None,
                      "signal_close_available_ts": rows[i - 1]["close_available_ts"] if i > 0 else None,
                      "trade_date": rows[i]["date"], "trade_ts_ns": rows[i]["trade_ts"],
                      "signal_to_execution_seconds": (rows[i]["trade_ts"] - rows[i - 1]["close_available_ts"]) / 1e9,
                      "terminal": terminal})
        trades.append(trade)

    for offset, i in enumerate(range(start, end)):
        assert i >= n and rows[i - 1]["close_available_ts"] < rows[i]["trade_ts"]
        last_close = closes[i - 1]
        avg = sma[i]
        assert avg is not None and avg > 0
        prev_desired = desired
        if not desired and last_close > avg * (D(1) + band):
            desired = True
        elif desired and last_close < avg * (D(1) - band):
            desired = False
        action = None
        if desired and units == 0:
            execute(i, True)
            action = "buy_attempt"
        elif not desired and units > 0:
            execute(i, False)
            action = "sell_attempt"
        decisions.append({"decision_index": i, "signal_close_date": rows[i - 1]["date"],
                          "signal_close_available_utc": stamp(rows[i - 1]["close_available_ts"]),
                          "trade_ts_utc": stamp(rows[i]["trade_ts"]), "close": str(last_close),
                          "SMA": str(avg), "desired_before": prev_desired, "desired_after": desired,
                          "action_attempt": action})

        base = offset * SPAN
        trade_ref = D(rows[i]["trade_open"])
        vector[base + 1] = float(cash + units * trade_ref)
        price_start = i * 1440 + 1
        marks = minute_closes[price_start:price_start + 1440]
        assert len(marks) == 1440
        vector[base + 2:(offset + 1) * SPAN + 1] = float(cash) + float(units) * marks
        daily_path.append(float(cash + units * closes[i]))

    terminal_ref = D(rows[end]["trade_open"])
    if units > 0:
        execute(end, False, True)
    terminal_value = cash + units * terminal_ref
    vector[-1] = float(terminal_value)
    assert np.all(np.isfinite(vector)) and np.all(vector > 0)
    assert len(vector) == point_count
    summary = scene_summary(vector, daily_path, trades, capital, cash, units, terminal_ref,
                            folds, start, multiplier)
    archive = {"spec": spec, "fingerprint": registry.fingerprint(spec), "decisions": decisions,
               "trades": trades, "terminal_cash": str(cash), "terminal_units": str(units),
               "daily_path_usdt": daily_path, "scene": summary}
    return vector, archive, summary


def simulate_hold(spec: dict, rows: list[dict], minute_closes: np.ndarray, start: int, end: int,
                  folds: list[dict], multiplier: int, filters: dict) -> tuple[np.ndarray, dict, dict]:
    capital = D(str(spec["parameters"]["initial_capital_usdt"]))
    cash, units = capital, D(0)
    trades = []
    days = end - start
    vector = np.empty(days * SPAN + 2, dtype=np.float64)
    vector[0] = float(capital)
    daily_path = [float(capital)]

    def execute(i: int, buy: bool, terminal: bool = False):
        nonlocal cash, units
        adv, sigma = core.engine.lagged_cost_inputs(rows, i)
        cash, units, trade = core.fill(cash, units, buy, D(rows[i]["trade_open"]), D(str(adv)), D(str(sigma)),
                                      multiplier, filters, D(rows[i]["proxy_vwap5"]))
        trade.update({"decision_index": i, "signal_close_available_ts": None,
                      "trade_date": rows[i]["date"], "trade_ts_ns": rows[i]["trade_ts"],
                      "signal_to_execution_seconds": None, "terminal": terminal})
        trades.append(trade)

    execute(start, True)
    for offset, i in enumerate(range(start, end)):
        base = offset * SPAN
        trade_ref = D(rows[i]["trade_open"])
        vector[base + 1] = float(cash + units * trade_ref)
        price_start = i * 1440 + 1
        marks = minute_closes[price_start:price_start + 1440]
        vector[base + 2:(offset + 1) * SPAN + 1] = float(cash) + float(units) * marks
        daily_path.append(float(cash + units * D(rows[i]["close"])))
    terminal_ref = D(rows[end]["trade_open"])
    if units > 0:
        execute(end, False, True)
    terminal_value = cash + units * terminal_ref
    vector[-1] = float(terminal_value)
    summary = scene_summary(vector, daily_path, trades, capital, cash, units, terminal_ref,
                            folds, start, multiplier)
    archive = {"spec": spec, "fingerprint": registry.fingerprint(spec), "decisions": [],
               "trades": trades, "terminal_cash": str(cash), "terminal_units": str(units),
               "daily_path_usdt": daily_path, "scene": summary}
    return vector, archive, summary


def fold_definitions() -> list[dict]:
    wf = load_module("r50_walk_forward_skill", ROOT / ".agents/skills/walk-forward-validation/scripts/walk_forward.py")
    cfg = wf.WalkForwardConfig(train_size=365, test_size=30, step_size=30,
                               window_type="rolling", purge_size=0, embargo_size=3)
    raw = list(wf.WalkForwardValidator(cfg).split(730))
    folds = []
    for index, f in enumerate(raw, 1):
        a, b = int(f.test_indices[0]), int(f.test_indices[-1]) + 1
        folds.append({"fold": index, "train_start_index": int(f.train_indices[0]),
                      "train_end_exclusive_index": int(f.train_indices[-1]) + 1,
                      "test_start_index": a, "test_end_exclusive_index": b,
                      "start_utc": None, "end_exclusive_utc": None})
    assert len(folds) == 12
    assert folds[0]["test_start_index"] == 368 and folds[-1]["test_end_exclusive_index"] == 728
    for a, b in zip(folds, folds[1:]):
        assert a["test_end_exclusive_index"] == b["test_start_index"]
    return folds


def main() -> None:
    replay = "--reproduce" in sys.argv
    plan = json.loads((ROUND / "spec.json").read_text(encoding="utf-8"))
    batch = json.loads((ROUND / "batch.json").read_text(encoding="utf-8"))
    old_report = json.loads((ROUND / "report.json").read_text(encoding="utf-8")) if replay else None
    ledger = registry.read_records(ROOT / "research/automation/registry.jsonl")
    expected_status = ("passed", "rejected") if replay else ("reserved",)
    for row in batch:
        assert ledger[row["fingerprint"]]["status"] in expected_status, row["name"]
        loaded = json.loads((ROOT / row["spec"]).read_text(encoding="utf-8"))
        assert registry.fingerprint(loaded) == row["fingerprint"]

    now = old_report["evaluation_started_utc"] if replay else datetime.now(timezone.utc).isoformat()
    markets, data_manifest = {}, {}
    for asset in ("BTC", "ETH"):
        markets[asset] = build_market(asset)
        data_manifest[asset] = markets[asset][2]
    assert markets["BTC"][0][0]["date"] == markets["ETH"][0][0]["date"]
    assert [r["trade_ts"] for r in markets["BTC"][0]] == [r["trade_ts"] for r in markets["ETH"][0]]
    date_index = {r["date"]: i for i, r in enumerate(markets["BTC"][0])}
    start = date_index[OUT_START_DATE]
    folds = fold_definitions()
    end = folds[-1]["test_end_exclusive_index"]
    assert markets["BTC"][0][start]["date"] == OUT_START_DATE
    assert markets["BTC"][0][end]["date"] == "2026-09-14"
    for f in folds:
        f["start_utc"] = markets["BTC"][0][f["test_start_index"]]["date"] + "T00:01:00Z"
        f["end_exclusive_utc"] = markets["BTC"][0][f["test_end_exclusive_index"]]["date"] + "T00:01:00Z"
    assert start == folds[0]["test_start_index"]
    assert end - start == 360

    source_report_path = ROOT / "research/experiments/20261012T035429Z/report.json"
    source_report = json.loads(source_report_path.read_text(encoding="utf-8"))
    filters = source_report["plan"]["execution"]["filters"]
    cache = ROOT / "data/runs" / ROUND.name
    cache.mkdir(parents=True, exist_ok=True)
    (ROUND / "results").mkdir(parents=True, exist_ok=True)
    daily_cache = ROUND / "daily_inputs.json.gz"
    if replay:
        assert sha(daily_cache) == json.loads((ROUND / "data_manifest.json").read_text())["daily_inputs_sha256"]
    else:
        gzwrite(daily_cache, {a: markets[a][0] for a in ("BTC", "ETH")})

    report = {
        "round": ROUND.name,
        "evaluation_started_utc": now,
        "plan": plan,
        "folds": folds,
        "data": data_manifest,
        "daily_inputs": {"path": str(daily_cache.relative_to(ROOT)), "sha256": sha(daily_cache)},
        "exchange_filters": {"source_report": str(source_report_path.relative_to(ROOT)),
                             "source_report_sha256": sha(source_report_path),
                             "metadata_path": source_report["plan"]["execution"]["metadata_path"],
                             "metadata_sha256": source_report["plan"]["execution"]["metadata_sha256"],
                             "BTCUSDT": filters["BTCUSDT"], "ETHUSDT": filters["ETHUSDT"]},
        "execution": {
            "fill_kernel": "research/experiments/20261001T133655Z/kernel.py::fill",
            "cost_inputs": "research/experiments/20261001T013355Z/evaluate.py::lagged_cost_inputs",
            "decision": "last closed UTC daily bar close against SMA_N built from the previous N closed UTC daily closes, including the compared close; state carries inside symmetric band.",
            "fill_time": "Next daily UTC 00:01 one-minute open; signal close available at 00:00, so 60-second recorded decision-to-execution interval.",
            "cost_scenarios": [1, 2, 3],
            "real_orders": 0,
        },
        "configs": {},
        "sensitivity": {},
        "summary": {},
        "source_hashes": {},
        "read_only_prior_comparators": {
            "initial_16_evidence_audit": {"path": str((ROOT / "research/experiments/20261012T035429Z/prior_evidence_audit.json").relative_to(ROOT)),
                                          "sha256": sha(ROOT / "research/experiments/20261012T035429Z/prior_evidence_audit.json"),
                                          "initial_rows_with_actual_evidence": 16},
        },
    }
    archive_by_name, vectors_by_name = {}, {}
    for b in batch:
        spec = json.loads((ROOT / b["spec"]).read_text(encoding="utf-8"))
        asset = b["asset"]
        rows, minute_closes, _ = markets[asset]
        scenes = {}
        archive = {"spec": spec, "fingerprint": b["fingerprint"], "scenes": {}}
        for mult in MULTIPLIERS:
            if b["is_comparator"]:
                vector, scene_archive, summary = simulate_hold(spec, rows, minute_closes, start, end, folds, mult, filters[asset + "USDT"])
            else:
                vector, scene_archive, summary = simulate_candidate(spec, rows, minute_closes, start, end, folds, mult, filters[asset + "USDT"])
            vectors_by_name[f"{b['name']}_{mult}"] = vector
            scenes[str(mult)] = summary
            archive["scenes"][str(mult)] = scene_archive
            cache_path = cache / f"{b['name']}_{mult}.npy"
            archive_path = ROUND / "results" / f"{b['name']}_{mult}.json.gz"
            if replay:
                summary["NAV_file_sha256"] = sha(cache_path)
                assert core.navhash(np.load(cache_path, allow_pickle=False)) == summary["NAV_sha256_f64le"]
                assert json.loads(gzip.decompress(archive_path.read_bytes())) == canonical(scene_archive)
            else:
                np.save(cache_path, vector, allow_pickle=False)
                summary["NAV_file_sha256"] = sha(cache_path)
                gzwrite(archive_path, scene_archive)
            summary["archive"] = str(archive_path.relative_to(ROOT))
            summary["archive_sha256"] = sha(archive_path)
            print(json.dumps({"config": b["name"], "cost": mult,
                              "net_return_pct": round(summary["net_return_pct"], 6),
                              "minute_close_sample_DD_pct": round(summary["max_drawdown_pct"], 6),
                              "fills": summary["executions"], "cost_usdt": summary["cost_usdt"]}), flush=True)
        archive_by_name[b["name"]] = archive
        report["configs"][b["name"]] = {**b, "scenes": scenes,
                                        "positive_folds_1x": sum(f["net_return_pct"] > 0 for f in scenes["1"]["folds"]),
                                        "status": "reference_only" if b["is_comparator"] else None,
                                        "criteria": {}}

    candidate_grid = {}
    for asset in ("BTC", "ETH"):
        cells = {name: row for name, row in report["configs"].items() if row["asset"] == asset and not row["is_comparator"]}
        assert len(cells) == 12
        axes = sorted({r["lookback_days"] for r in cells.values()}), sorted({r["symmetric_threshold_fraction"] for r in cells.values()})
        coord_by_name = {n: (r["lookback_days"], r["symmetric_threshold_fraction"]) for n, r in cells.items()}
        edges = []
        for a_name, a_row in cells.items():
            for b_name, b_row in cells.items():
                if a_name >= b_name:
                    continue
                a, b = coord_by_name[a_name], coord_by_name[b_name]
                adjacent = (a[0] == b[0] and abs(a[1] - b[1]) == 0.005) or (a[1] == b[1] and abs(a[0] - b[0]) == 50)
                if adjacent:
                    edges.append({"a": a_name, "b": b_name,
                                  "return_difference_3x_pct": abs(a_row["scenes"]["3"]["net_return_pct"] - b_row["scenes"]["3"]["net_return_pct"]),
                                  "sharpe_difference_3x": abs((a_row["scenes"]["3"]["sharpe_365"] or 0) - (b_row["scenes"]["3"]["sharpe_365"] or 0))})
        assert len(edges) == 17
        cliff_cutoff = 2 * statistics.stdev(e["sharpe_difference_3x"] for e in edges) if len(edges) > 1 else 0
        for edge in edges:
            edge["cliff_flag_2sd"] = edge["sharpe_difference_3x"] > cliff_cutoff
        positive_fraction = {k: sum(row["scenes"][k]["net_return_pct"] > 0 for row in cells.values()) / len(cells) for k in ("1", "2", "3")}
        candidate_grid[asset] = {"cells": len(cells), "lookback_days": list(axes[0]),
                                 "symmetric_threshold_fraction": list(axes[1]),
                                 "positive_return_fraction_by_cost": positive_fraction,
                                 "adjacent_edges": edges, "cliff_cutoff_2sd_sharpe": cliff_cutoff}
    report["sensitivity"] = candidate_grid

    for name, row in report["configs"].items():
        if row["is_comparator"]:
            row["status"] = "reference_only"
            row["criteria"] = {"candidate_gate": False, "reason": "同期持有比较，不作为研究候选。"}
            continue
        s = row["scenes"]
        gross_ratio = s["1"]["gross_reference_PnL_to_cost"]
        candidates = report["sensitivity"][row["asset"]]
        criteria = {
            "positive_all_cost_scenarios": all(s[k]["net_return_pct"] > 0 for k in ("1", "2", "3")),
            "at_least_7_of_12_positive_1x_folds": row["positive_folds_1x"] >= 7,
            "minute_close_sample_DD3_lte25pct": s["3"]["max_drawdown_pct"] <= 25,
            "neighbourhood_3x_positive_fraction_gte60pct": candidates["positive_return_fraction_by_cost"]["3"] >= 0.6,
            "at_least_2_1x_round_trips": s["1"]["round_trips"] >= 2,
            "gross_reference_pnl_to_cost1_gte2_5": gross_ratio is not None and gross_ratio >= 2.5,
            "no_balance_violations": all(s[k]["cash_or_units_violations"] == 0 for k in ("1", "2", "3")),
            "terminal_flat": all(D(s[k]["terminal_units"]) == 0 for k in ("1", "2", "3")),
        }
        row["criteria"] = criteria
        row["failed_criteria"] = [k for k, ok in criteria.items() if not ok]
        row["status"] = "passed" if all(criteria.values()) else "rejected"

    configs = report["configs"]
    candidates = [r for r in configs.values() if not r["is_comparator"]]
    comparators = [r for r in configs.values() if r["is_comparator"]]
    report["summary"] = {
        "candidate_configs": len(candidates), "reference_configs": len(comparators),
        "cost_scenarios": 3 * len(configs),
        "candidate_passed": sum(r["status"] == "passed" for r in candidates),
        "candidate_rejected": sum(r["status"] == "rejected" for r in candidates),
        "candidate_positive_1x": sum(r["scenes"]["1"]["net_return_pct"] > 0 for r in candidates),
        "candidate_positive_3x": sum(r["scenes"]["3"]["net_return_pct"] > 0 for r in candidates),
        "new_virtual_or_real_orders": 0,
        "actual_historical_simulated_executions_1x": sum(r["scenes"]["1"]["executions"] for r in configs.values()),
        "oos_start_utc": markets["BTC"][0][start]["date"] + "T00:01:00Z",
        "oos_last_decision_utc": markets["BTC"][0][end - 1]["date"] + "T00:01:00Z",
        "terminal_execution_utc": markets["BTC"][0][end]["date"] + "T00:01:00Z",
        "oos_decision_days": end - start,
        "folds": len(folds),
        "history_reused": True,
    }
    report["oos_start_utc"] = report["summary"]["oos_start_utc"]
    report["terminal_exit_utc"] = report["summary"]["terminal_execution_utc"]
    for name, row in report["configs"].items():
        row["is_new"] = not row["is_comparator"]
    new_candidates = [name for name, row in report["configs"].items() if not row["is_comparator"]]
    report["summary"].update({
        "new_configs": len(new_candidates),
        "passed": [name for name in new_candidates if report["configs"][name]["status"] == "passed"],
        "rejected": [name for name in new_candidates if report["configs"][name]["status"] == "rejected"],
        "new_cross_period_pairs": [],
    })

    files = [ROUND / x for x in ("spec.json", "batch.json", "prepare.py", "evaluate.py")]
    files += [ROOT / "research/experiments/20261001T133655Z/evaluate.py",
              ROOT / "research/experiments/20261001T133655Z/kernel.py",
              ROOT / "research/experiments/20261001T013355Z/evaluate.py",
              ROOT / "research/experiments/20261012T035429Z/report.json",
              ROOT / "research/experiments/20261012T035429Z/prior_evidence_audit.json",
              ROOT / ".agents/skills/walk-forward-validation/scripts/walk_forward.py",
              ROOT / "research/automation/registry.py"]
    report["source_hashes"] = {str(p.relative_to(ROOT)): sha(p) for p in files}
    report["environment"] = {"python": sys.version, "numpy": np.__version__, "polars": pl.__version__}

    if replay:
        assert core.canonical(report) == old_report, "full report mismatch"
        print("PASS: all 78 cost scenes, archives, minute NAV hashes, and full report exactly reproduced without registry writes")
        return

    (ROUND / "data_manifest.json").write_text(json.dumps({"data": data_manifest,
        "daily_inputs_path": str(daily_cache.relative_to(ROOT)), "daily_inputs_sha256": sha(daily_cache),
        "source_exchange_metadata": report["exchange_filters"],
        "minute_data_downloaded_this_round": False}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROUND / "report.json").write_text(json.dumps(canonical(report), ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    with (ROUND / "sensitivity.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(["config", "asset", "lookback_days", "symmetric_threshold_fraction", "cost_multiplier",
                         "net_return_pct", "minute_close_sample_DD_pct", "daily_DD_pct", "Sharpe365", "Calmar",
                         "positive_folds_1x", "round_trips", "executions", "cost_usdt", "gross_reference_pnl_to_cost", "status"])
        for name, row in configs.items():
            for multiplier, s in row["scenes"].items():
                writer.writerow([name, row["asset"], row["lookback_days"], row["symmetric_threshold_fraction"], multiplier,
                                 s["net_return_pct"], s["max_drawdown_pct"], s["daily_mark_drawdown_pct"], s["sharpe_365"],
                                 s["calmar"], row.get("positive_folds_1x"), s["round_trips"], s["executions"],
                                 s["cost_usdt"], s["gross_reference_PnL_to_cost"], row["status"]])
    print(json.dumps(report["summary"], ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
