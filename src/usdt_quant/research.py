from __future__ import annotations

from bisect import bisect_left, bisect_right
from decimal import Decimal
from dataclasses import replace
import argparse
import json
from pathlib import Path

import numpy as np
import polars as pl
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import brier_score_loss, mean_absolute_error, mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from usdt_quant.backtest import (
    BacktestData, _config_from_json, execution_points, merge_funding_observations, position_quantities,
    run_backtest,
)


HOUR = 3_600_000_000_000
MINUTE = HOUR // 60
FACTORS = tuple(f"F{i:02d}" for i in range(1, 13))
FACTOR_DICTIONARY = {
    "F01": {"formula": "median(rate / actual_interval_hours)", "window": "21 settlements", "unit": "per hour"},
    "F02": {"formula": "sum(positive interval hours) / sum(interval hours)", "window": "21 settlements", "unit": "ratio"},
    "F03": {"formula": "EWMA(rate / hours, span=9, adjust=False)", "window": "all available; minimum 9 settlements", "unit": "per hour"},
    "F04": {"formula": "population std(rate / actual_interval_hours)", "window": "21 settlements", "unit": "per hour"},
    "F05": {"formula": "mean(indicative rate visible 30m before settlement - realized rate)", "window": "21 paired settlements", "unit": "rate"},
    "F06": {"formula": "(basis - previous median) / (1.4826 * previous MAD)", "window": "previous 7 days, excludes current", "unit": "ratio"},
    "F07": {"formula": "basis(t) - basis(t - 1 hour)", "window": "1 hour", "unit": "ratio"},
    "F08": {"formula": "latest OI base quantity / latest OI base quantity available at t-8h - 1", "window": "8 hours", "unit": "ratio"},
    "F09": {"formula": "standardized funding times standardized OI change", "window": "training statistics", "unit": "score"},
    "F10": {"formula": "perp taker-buy quote ratio - spot taker-buy quote ratio", "window": "60 closed 1m bars", "unit": "ratio"},
    "F11": {"formula": "main realized funding - cross-exchange realized funding", "window": "continuous 24 hours", "unit": "rate"},
    "F12": {"formula": "synchronized two-leg roundtrip fees and book shortfall", "window": "current executable books", "unit": "basis points"},
}


def _input_rows(inputs, name, columns):
    frame = (inputs or {}).get(name)
    if not isinstance(frame, pl.DataFrame) or not set(columns) <= set(frame.columns):
        return []
    return frame.select(columns).to_dicts()


def _group_rows(rows, key):
    grouped = {}
    for row in rows:
        value = row.get(key)
        if value is not None:
            grouped.setdefault(int(value), []).append(row)
    return grouped


def _load_factor_inputs(directory):
    directory = Path(directory)
    inputs = {}
    for name in ("spot_bars", "perp_bars", "funding_quotes", "open_interest",
                 "cross_funding_settlement"):
        path = directory / f"{name}.parquet"
        if path.is_file():
            inputs[name] = pl.read_parquet(path)
    return inputs


def _factor_experiments(frame):
    result = []
    for name in ("F05", "F08", "F09", "F10", "F11", "F12"):
        samples = frame[name].drop_nulls().len() if name in frame.columns else 0
        row = {"name": name, "status": "evaluated" if samples else "not_run",
               "samples": samples}
        if not samples:
            row["reason"] = "no_non_null_samples"
        result.append(row)
    return result


def _flow_ratio(index, timestamp):
    times, grouped = index
    selected_times = times[bisect_right(times, timestamp - HOUR):bisect_right(times, timestamp)]
    if (len(selected_times) != 60 or
            any(right - left != MINUTE for left, right in zip(selected_times, selected_times[1:]))):
        return None, []
    selected = []
    for close_ts in selected_times:
        candidates = [row for row in grouped[close_ts]
                      if row["available_ts"] is not None and int(row["available_ts"]) <= timestamp
                      and row["is_closed"] is True and row["quote_volume"] is not None
                      and row["taker_buy_quote_volume"] is not None]
        if not candidates:
            return None, []
        selected.append(max(candidates, key=lambda row: int(row["available_ts"])))
    quote_volume = sum(float(row["quote_volume"]) for row in selected)
    if quote_volume <= 0:
        return None, []
    return (sum(float(row["taker_buy_quote_volume"]) for row in selected) / quote_volume,
            [int(row["available_ts"]) for row in selected])


def _funding_window(rows, end_ts):
    selected = []
    cursor = end_ts
    hours = Decimal(0)
    while hours < 24:
        row = rows.get(cursor)
        if row is None:
            return None
        interval = Decimal(str(row[3]))
        if interval <= 0 or hours + interval > 24:
            return None
        previous = Decimal(cursor) - interval * HOUR
        if previous != previous.to_integral_value():
            return None
        selected.append(row)
        hours += interval
        cursor = int(previous)
    return selected


def _fit_f09_stats(frame):
    if not {"F01", "F08"} <= set(frame.columns):
        return {"n": 0, "mean": {"F01": None, "F08": None},
                "scale": {"F01": None, "F08": None}}
    paired = frame.select("F01", "F08").drop_nulls()
    if not paired.height:
        return {"n": 0, "mean": {"F01": None, "F08": None},
                "scale": {"F01": None, "F08": None}}
    values = paired.to_numpy()
    return {
        "n": paired.height,
        "mean": {name: float(values[:, index].mean())
                 for index, name in enumerate(("F01", "F08"))},
        "scale": {name: float(values[:, index].std())
                  for index, name in enumerate(("F01", "F08"))},
    }


def _apply_f09(frame, stats):
    means, scales = stats["mean"], stats["scale"]
    if (stats["n"] < 2 or any(means[name] is None or scales[name] is None or scales[name] == 0
                              for name in ("F01", "F08"))):
        return frame.with_columns(pl.lit(None, dtype=pl.Float64).alias("F09"))
    return frame.with_columns(
        (((pl.col("F01") - means["F01"]) / scales["F01"]) *
         ((pl.col("F08") - means["F08"]) / scales["F08"])).alias("F09"),
    )


def factor_frame(data: BacktestData, decisions: list[int], inputs=None) -> pl.DataFrame:
    times = [point.ts for point in data.market]
    basis = np.array([float((point.perp_bid + point.perp_ask) /
                            (point.spot_bid + point.spot_ask) - 1) for point in data.market])
    observations = merge_funding_observations(data.funding_history, data.funding)
    funding_quotes = _group_rows(_input_rows(
        inputs, "funding_quotes", ("target_settlement_ts", "available_ts", "indicative_rate"),
    ), "target_settlement_ts")
    open_interest = sorted(_input_rows(
        inputs, "open_interest", ("available_ts", "oi_base_qty"),
    ), key=lambda row: int(row["available_ts"]) if row["available_ts"] is not None else -1)
    oi_times = [int(row["available_ts"]) for row in open_interest
                if row["available_ts"] is not None]
    open_interest = [row for row in open_interest if row["available_ts"] is not None]
    flow_indexes = []
    for name in ("spot_bars", "perp_bars"):
        grouped = _group_rows(_input_rows(
            inputs, name, ("close_ts", "available_ts", "is_closed", "quote_volume",
                           "taker_buy_quote_volume"),
        ), "close_ts")
        flow_indexes.append((sorted(grouped), grouped))
    cross_funding = _group_rows(_input_rows(
        inputs, "cross_funding_settlement",
        ("settlement_ts", "available_ts", "realized_rate", "actual_interval_hours"),
    ), "settlement_ts")
    rows = []
    for timestamp in decisions:
        last = bisect_right(times, timestamp) - 1
        row = {"decision_ts": timestamp, "input_max_available_ts": None,
               **{name: None for name in FACTORS}}
        used = []
        available = [item for item in observations if item.available_ts <= timestamp]
        rates = np.array([float(item.realized_rate / item.interval_hours) for item in available])
        if len(available) >= 9:
            ewma = rates[0]
            for rate in rates[1:]:
                ewma = 0.2 * rate + 0.8 * ewma
            row["F03"] = float(ewma)
            used.extend(item.available_ts for item in available)
        if len(available) >= 21:
            hours = np.array([float(item.interval_hours) for item in available[-21:]])
            recent = rates[-21:]
            row.update(F01=float(np.median(recent)), F02=float(hours[recent > 0].sum() / hours.sum()),
                       F04=float(np.std(recent)))

        recent_events = [event for event in data.funding
                         if event.settlement_ts <= timestamp and event.available_ts <= timestamp][-21:]
        paired = []
        for event in recent_events:
            candidates = [quote for quote in funding_quotes.get(event.settlement_ts, ())
                          if quote["available_ts"] is not None
                          and int(quote["available_ts"]) <= event.settlement_ts - HOUR // 2
                          and quote["indicative_rate"] is not None]
            if candidates:
                quote = max(candidates, key=lambda item: int(item["available_ts"]))
                paired.append((event.settlement_ts,
                               float(quote["indicative_rate"]) - float(event.realized_rate),
                               event.available_ts, int(quote["available_ts"])))
        if len(recent_events) == len(paired) == 21:
            row["F05"] = float(np.mean([item[1] for item in paired]))
            used.extend(value for item in paired for value in item[2:])

        if last >= 0 and times[last] == timestamp:
            used.append(times[last])
            week_start = timestamp - 168 * HOUR
            first = bisect_left(times, week_start)
            previous = basis[first:last]
            if times[0] <= week_start and len(previous) > 1:
                center = np.median(previous)
                mad = np.median(np.abs(previous - center))
                # A zero MAD has no defined z-score; retain missing instead of inventing a floor.
                if mad > 0:
                    row["F06"] = float((basis[last] - center) / (1.4826 * mad))
            hour_ago = bisect_left(times, timestamp - HOUR)
            if hour_ago < len(times) and times[hour_ago] == timestamp - HOUR:
                row["F07"] = float(basis[last] - basis[hour_ago])

        current_oi = bisect_right(oi_times, timestamp) - 1
        prior_oi = bisect_right(oi_times, timestamp - 8 * HOUR) - 1
        if current_oi >= 0 and prior_oi >= 0:
            current_qty = open_interest[current_oi]["oi_base_qty"]
            prior_qty = open_interest[prior_oi]["oi_base_qty"]
            if current_qty is not None and prior_qty is not None and float(prior_qty) > 0:
                row["F08"] = float(current_qty) / float(prior_qty) - 1
                used.extend((oi_times[current_oi], oi_times[prior_oi]))

        spot_flow, spot_used = _flow_ratio(flow_indexes[0], timestamp)
        perp_flow, perp_used = _flow_ratio(flow_indexes[1], timestamp)
        if spot_flow is not None and perp_flow is not None:
            row["F10"] = perp_flow - spot_flow
            used.extend(spot_used + perp_used)

        main = {event.settlement_ts: (event.settlement_ts, event.available_ts,
                                      event.realized_rate, event.interval_hours)
                for event in data.funding
                if event.settlement_ts <= timestamp and event.available_ts <= timestamp
                and event.interval_hours is not None}
        cross = {}
        for settlement_ts, versions in cross_funding.items():
            candidates = [item for item in versions
                          if settlement_ts <= timestamp and item["available_ts"] is not None
                          and int(item["available_ts"]) <= timestamp
                          and item["realized_rate"] is not None
                          and item["actual_interval_hours"] is not None]
            if candidates:
                item = max(candidates, key=lambda value: int(value["available_ts"]))
                cross[settlement_ts] = (settlement_ts, int(item["available_ts"]),
                                        item["realized_rate"], item["actual_interval_hours"])
        common = set(main) & set(cross)
        if common:
            end_ts = max(common)
            main_window = _funding_window(main, end_ts)
            cross_window = _funding_window(cross, end_ts)
            if main_window is not None and cross_window is not None:
                row["F11"] = (sum(float(item[2]) for item in main_window) -
                              sum(float(item[2]) for item in cross_window))
                used.extend(int(item[1]) for item in main_window + cross_window)
        row["input_max_available_ts"] = max(used) if used else None
        rows.append(row)
    schema = {"decision_ts": pl.Int64, "input_max_available_ts": pl.Int64,
              **{name: pl.Float64 for name in FACTORS}}
    return pl.DataFrame(rows, schema=schema)


def purged_split(frame: pl.DataFrame, train_end: int, validation_end: int, test_end: int):
    if not train_end < validation_end < test_end:
        raise ValueError("training, validation and test boundaries must increase")
    mature = pl.max_horizontal("label_end_ts", "label_available_ts")
    return tuple(frame.filter((pl.col("decision_ts") >= start) &
                              (pl.col("decision_ts") < end) & (mature < end))
                 for start, end in ((0, train_end), (train_end, validation_end),
                                    (validation_end, test_end)))


def fit_models(train, validation, test, *, ridge_alpha, logistic_c):
    if ridge_alpha <= 0 or logistic_c <= 0:
        raise ValueError("ridge_alpha and logistic_c must be positive")
    factor_coverage = {
        name: train[name].drop_nulls().len() / train.height
        if train.height and name in train.columns else 0.0
        for name in FACTORS
    }
    active_factors = tuple(name for name in FACTORS if factor_coverage[name] >= 0.98)
    results = {"status": "evaluated", "active_factors": list(active_factors),
               "factor_coverage": factor_coverage}
    if not active_factors:
        return {**results, "status": "no_active_factors", "n": train.height}, {}
    if train.height < len(active_factors) + 1:
        return {**results, "status": "insufficient_training_labels", "n": train.height}, {}
    models = {}
    for name, estimator, target in (("ridge", Ridge(alpha=ridge_alpha), "y_net"),
                                     ("logistic", LogisticRegression(C=logistic_c, max_iter=1000), "y_loss")):
        if name == "logistic" and train[target].n_unique() < 2:
            results[name] = {"status": "training_has_one_class"}
            continue
        pipeline = Pipeline([("impute", SimpleImputer(strategy="median")),
                             ("scale", StandardScaler()), ("model", estimator)])
        pipeline.active_factors = active_factors
        pipeline.fit(train.select(active_factors).to_numpy(), train[target].to_numpy())
        models[name], results[name] = pipeline, {"status": "evaluated"}
        for split_name, split in (("validation", validation), ("test", test)):
            if not split.height:
                results[name][split_name] = {"status": "no_mature_labels", "n": 0}
                continue
            x, y = split.select(active_factors).to_numpy(), split[target].to_numpy()
            if name == "ridge":
                prediction = pipeline.predict(x)
                metrics = {"mae": float(mean_absolute_error(y, prediction)),
                           "mse": float(mean_squared_error(y, prediction))}
            else:
                prediction = pipeline.predict_proba(x)[:, 1]
                bins = np.minimum((prediction * 5).astype(int), 4)
                metrics = {"brier_score": float(brier_score_loss(y, prediction)),
                           "base_rate": float(train[target].mean()),
                           "base_rate_brier_score": float(np.mean((y - train[target].mean()) ** 2)),
                           "calibration": [{"bin": i, "n": int(np.sum(bins == i)),
                                            "predicted": float(np.mean(prediction[bins == i])),
                                            "observed": float(np.mean(y[bins == i]))}
                                           for i in range(5) if np.any(bins == i)]}
            results[name][split_name] = {"n": split.height, **metrics}
    return results, models


def label_frame(config, data: BacktestData, decisions: list[int]) -> pl.DataFrame:
    points = execution_points(config, data)
    times = [point.ts for point in points]
    settlement_times = [point.settlement_ts for point in data.funding]
    spot_qty, contracts = position_quantities(config, data.metadata)
    perp_qty = contracts * data.metadata.contract_multiplier
    nav = config.initial_spot_usdt + config.initial_perp_usdt
    precision = Decimal("0.00000001")
    rows = []
    for timestamp in decisions:
        for horizon, hours in (("next", None), ("24h", 24), ("7d", 168)):
            row = {"decision_ts": timestamp, "horizon": horizon, "entry_ts": None,
                   "label_end_ts": None, "label_available_ts": None, "y_funding": None,
                   "y_net": None, "y_flip": None, "y_loss": None, "fees_usdt": None,
                   "execution_cost_usdt": None, "max_basis_expansion": None, "reason": None}
            next_settlement = bisect_right(settlement_times, timestamp)
            if hours is None and next_settlement == len(settlement_times):
                row["reason"] = "next_settlement_unavailable"
                rows.append(row)
                continue
            target = timestamp + hours * HOUR if hours else settlement_times[next_settlement]
            entry_index, exit_index = bisect_right(times, timestamp), bisect_left(times, target)
            if exit_index >= len(times) or entry_index >= exit_index:
                row["reason"] = "incomplete_price_horizon"
                rows.append(row)
                continue
            entry, exit = points[entry_index], points[exit_index]
            if hours is not None and exit.ts != target:
                row["reason"] = "missing_horizon_exit_record"
                rows.append(row)
                continue
            events = data.funding[bisect_right(settlement_times, entry.ts):bisect_right(settlement_times, exit.ts)]
            if any(event.mark_price is None for event in events):
                row["reason"] = "settlement_mark_missing"
                rows.append(row)
                continue
            fees = sum((amount.quantize(precision) for amount in (
                spot_qty * entry.spot_ask * config.spot_taker_fee,
                spot_qty * exit.spot_bid * config.spot_taker_fee,
                perp_qty * entry.perp_bid * config.perp_taker_fee,
                perp_qty * exit.perp_ask * config.perp_taker_fee)), Decimal(0))
            funding = sum(((perp_qty * event.mark_price * event.realized_rate).quantize(precision)
                           for event in events), Decimal(0))
            pnl = spot_qty * (exit.spot_bid - entry.spot_ask) + perp_qty * (entry.perp_bid - exit.perp_ask)
            entry_mid = data.market[entry_index]
            exit_mid = data.market[exit_index]
            reference_spot = (entry_mid.spot_ask + entry_mid.spot_bid) / 2
            mid_pnl = spot_qty * ((exit_mid.spot_bid + exit_mid.spot_ask) / 2 - reference_spot)
            mid_pnl += perp_qty * ((entry_mid.perp_bid + entry_mid.perp_ask -
                                   exit_mid.perp_bid - exit_mid.perp_ask) / 2)
            basis_values = [float((point.perp_bid + point.perp_ask) /
                                  (point.spot_bid + point.spot_ask) - 1)
                            for point in data.market[entry_index:exit_index + 1]]
            net = (pnl + funding - fees).quantize(precision)
            row.update(entry_ts=entry.ts, label_end_ts=exit.ts,
                       label_available_ts=max([exit.ts] + [event.available_ts for event in events]),
                       y_funding=float(funding / (spot_qty * reference_spot)), y_net=float(net / nav),
                       y_flip=int(any(event.realized_rate < 0 for event in events)), y_loss=int(net < 0),
                       fees_usdt=float(fees), execution_cost_usdt=float(mid_pnl - pnl),
                       max_basis_expansion=max(basis_values) - basis_values[0])
            rows.append(row)
    schema = {"decision_ts": pl.Int64, "horizon": pl.String, "entry_ts": pl.Int64,
              "label_end_ts": pl.Int64, "label_available_ts": pl.Int64,
              **{name: pl.Float64 for name in ("y_funding", "y_net", "fees_usdt",
                                             "execution_cost_usdt", "max_basis_expansion")},
              "y_flip": pl.Int64, "y_loss": pl.Int64, "reason": pl.String}
    return pl.DataFrame(rows, schema=schema)


def _correlation(x, y):
    if len(x) < 3 or np.ptp(x) == 0 or np.ptp(y) == 0:
        return None
    return float(np.corrcoef(x, y)[0, 1])


def factor_diagnostics(train, test, *, seed, bootstrap_samples):
    result = {}
    rng = np.random.default_rng(seed)
    for name in FACTORS:
        training = train.select(name, "y_net").drop_nulls()
        sample = test.select("decision_ts", name, "y_net").drop_nulls()
        if training.height < 3 or sample.height < 3:
            result[name] = {"status": "insufficient_samples", "n": sample.height}
            continue
        boundaries = np.quantile(training[name].to_numpy(), [1 / 3, 2 / 3])
        x, y = sample[name].to_numpy(), sample["y_net"].to_numpy()
        groups = np.searchsorted(boundaries, x)
        day = sample["decision_ts"].to_numpy() // (24 * HOUR)
        blocks = [np.flatnonzero(day == value) for value in np.unique(day)]
        correlations = []
        if len(blocks) >= 2:
            for _ in range(bootstrap_samples):
                selected = np.concatenate([blocks[index] for index in rng.integers(0, len(blocks), len(blocks))])
                value = _correlation(x[selected], y[selected])
                if value is not None:
                    correlations.append(value)
        midpoint = len(x) // 2
        result[name] = {
            "status": "evaluated", "n": len(x), "pearson_ic": _correlation(x, y),
            "rank_ic": _correlation(sample[name].rank().to_numpy(), sample["y_net"].rank().to_numpy()),
            "ic_95pct_interval": np.quantile(correlations, [0.025, 0.975]).tolist() if correlations else None,
            "bootstrap_block": "UTC day; 24-hour labels", "bootstrap_blocks": len(blocks),
            "train_group_boundaries": boundaries.tolist(),
            "groups": [{"group": i, "n": int(np.sum(groups == i)),
                        "mean_net_return": float(np.mean(y[groups == i]))}
                       for i in range(3) if np.any(groups == i)],
            "test_halves_ic": [_correlation(x[:midpoint], y[:midpoint]), _correlation(x[midpoint:], y[midpoint:])],
            "label_quantiles": np.quantile(y, [0.01, 0.05, 0.5, 0.95, 0.99]).tolist(),
        }
    return result


def compare_strategies(config, data, test_start, predictions, output_dir, entry_analysis_ns=None):
    """Registered single-episode native runs, with the same capital, H and costs."""
    test_decisions = [row["decision_ts"] for row in predictions
                      if row["split"] == "test" and test_start <= row["decision_ts"] < config.end_ns]
    if entry_analysis_ns is not None:
        test_decisions = [timestamp for timestamp in test_decisions if timestamp == entry_analysis_ns]
    if not test_decisions:
        return {name: {"status": "not_run", "reason": "no_test_decisions"} for name in ("B0", "B1", "M1")}
    first_decision = min(test_decisions)
    forecasts = {row["decision_ts"]: Decimal(str(row["predicted_net_return"]))
                 for row in predictions if row["split"] == "test" and "predicted_net_return" in row}
    result = {}
    for baseline in ("B0", "B1", "M1"):
        if baseline == "M1" and not forecasts:
            result[baseline] = {"status": "not_run", "reason": "no_fitted_ridge_forecasts"}
            continue
        settings = replace(
            config,
            baseline=baseline,
            start_ns=first_decision,
            end_ns=first_decision + config.holding_period_ns,
        )
        folder = output_dir / baseline
        try:
            report = run_backtest(settings, data, folder, predictions=forecasts if baseline == "M1" else None)
            result[baseline] = {"status": "evaluated", "summary": report["summary"],
                                "config": report["config"],
                                "assumptions": report["assumptions"], "unverified": report["unverified"],
                                "report_path": report["artifacts"]["summary"]}
        except (ValueError, RuntimeError) as error:
            result[baseline] = {"status": "failed", "reason": str(error)}
    return result


def run_research(values: dict, dataset_dir: Path, output_dir: Path) -> dict:
    """One registered split and model pair; no parameter search or test-set refit."""
    research_keys = {"train_end_ns", "validation_end_ns", "ridge_alpha", "logistic_c", "seed", "bootstrap_samples"}
    if not research_keys <= values.keys():
        raise ValueError(f"missing research parameters: {sorted(research_keys - values.keys())}")
    optional_research_keys = {"entry_analysis_ns"}
    config = _config_from_json({
        key: value for key, value in values.items()
        if key not in research_keys | optional_research_keys
    })
    train_end, validation_end = int(values["train_end_ns"]), int(values["validation_end_ns"])
    if not config.start_ns < train_end < validation_end < config.end_ns:
        raise ValueError("split boundaries must be inside the requested time range")
    if config.holding_period_ns != 24 * HOUR:
        raise ValueError("first research comparison registers a 24-hour holding horizon")
    entry_analysis_ns = values.get("entry_analysis_ns")
    if entry_analysis_ns is not None:
        if type(entry_analysis_ns) is not int:
            raise ValueError("entry_analysis_ns must be an integer")
        if not validation_end <= entry_analysis_ns <= config.end_ns - config.holding_period_ns:
            raise ValueError("entry_analysis_ns must be inside the test range with a full holding period")
        if (entry_analysis_ns - validation_end) % config.decision_interval_ns:
            raise ValueError("entry_analysis_ns must match the registered decision grid")
    if not 1 <= int(values["bootstrap_samples"]) <= 10_000:
        raise ValueError("bootstrap_samples must be between 1 and 10000")
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    # Save attempted parameters even when loading or evaluation subsequently fails.
    (output_dir / "config.json").write_text(json.dumps(values, indent=2), encoding="utf-8")
    data = BacktestData.from_parquet(dataset_dir)
    first = max(config.start_ns, data.market[0].ts)
    next_decision = first
    decisions = []
    for point in data.market:
        if point.ts >= next_decision and point.ts < config.end_ns:
            decisions.append(point.ts)
            next_decision = point.ts + config.decision_interval_ns
    factors = factor_frame(data, decisions, _load_factor_inputs(dataset_dir))
    labels = label_frame(config, data, decisions)
    raw_rows = factors.join(labels.filter(pl.col("horizon") == "24h"), on="decision_ts")
    raw_rows = raw_rows.filter(pl.col("y_net").is_not_null())
    raw_train, _, _ = purged_split(raw_rows, train_end, validation_end, config.end_ns)
    f09_stats = _fit_f09_stats(raw_train)
    factors = _apply_f09(factors, f09_stats)
    factors.write_parquet(output_dir / "factors.parquet")
    labels.write_parquet(output_dir / "labels.parquet")
    rows = factors.join(labels.filter(pl.col("horizon") == "24h"), on="decision_ts")
    rows = rows.filter(pl.col("y_net").is_not_null())
    train, validation, test = purged_split(rows, train_end, validation_end, config.end_ns)
    metrics, models = fit_models(train, validation, test,
                                 ridge_alpha=float(values["ridge_alpha"]), logistic_c=float(values["logistic_c"]))
    predictions = []
    for split_name, split_start, split_end in (("validation", train_end, validation_end),
                                             ("test", validation_end, config.end_ns)):
        # Forecast eligibility uses only decision time, never future label coverage.
        split = factors.filter((pl.col("decision_ts") >= split_start) &
                               (pl.col("decision_ts") < split_end))
        if not split.height:
            continue
        prediction = {"decision_ts": split["decision_ts"], "split": [split_name] * split.height}
        if "ridge" in models:
            prediction["predicted_net_return"] = models["ridge"].predict(
                split.select(models["ridge"].active_factors).to_numpy())
        if "logistic" in models:
            prediction["predicted_loss_probability"] = models["logistic"].predict_proba(
                split.select(models["logistic"].active_factors).to_numpy())[:, 1]
        predictions.extend(pl.DataFrame(prediction).to_dicts())
    (output_dir / "predictions.jsonl").write_text("".join(json.dumps(row) + "\n" for row in predictions), encoding="utf-8")
    # Standard sklearn/joblib serialization is local output; never load an untrusted model file.
    if models:
        import joblib
        joblib.dump(models, output_dir / "models.joblib")
    report = {
        "schema_version": 1, "config": values,
        "data": {"data_version": config.data_version, "dataset_dir": str(dataset_dir),
                 "start_ns": data.market[0].ts, "end_ns": data.market[-1].ts},
        "factor_dictionary": {key: {**value, "version": 1,
                              "availability": "all inputs <= decision_ts; prices require synchronized record",
                               "missing": "null; imputation fitted on training only"}
                               for key, value in FACTOR_DICTIONARY.items()},
        "factor_training": {"F09": f09_stats},
        "labels": {"horizons": ["next", "24h", "7d"], "rows": labels.height,
                   "mature_net_labels": labels["y_net"].drop_nulls().len(),
                   "cost_model": "shared next-record execution prices and quantity; four fees; no second slippage charge",
                   "entry": "first shared record after decision",
                   "exit": "24h/7d require an exact expiry record; next settlement uses the first shared record at or after settlement",
                   "maturity": "max(exit time, all realized funding availability times)",
                   "missing_reasons": labels.filter(pl.col("reason").is_not_null()).group_by("reason").len().to_dicts()},
        "split": {"train": train.height, "validation": validation.height, "test": test.height,
                  "purged_or_unmatured": rows.height - train.height - validation.height - test.height,
                  "test_status": "registered evaluation split; not claimed untouched by prior research",
                  "refit_on_validation": False},
        "models": metrics,
        "strategy_comparison": compare_strategies(
            config, data, validation_end, predictions, output_dir,
            entry_analysis_ns=entry_analysis_ns,
        ),
        "strategy_scope": "single holding episode per baseline within test interval; not a continuous trading performance claim",
        "factor_diagnostics": factor_diagnostics(train, test, seed=int(values["seed"]),
                                                 bootstrap_samples=int(values["bootstrap_samples"])),
        "experiments": [{"name": "M1 Ridge net return", "status": metrics.get("ridge", {}).get("status", metrics["status"])},
                        {"name": "M2 Logistic loss probability", "status": metrics.get("logistic", {}).get("status", metrics["status"])},
                        *_factor_experiments(factors)],
        "artifacts": {name: str(output_dir / name) for name in
                      ("factors.parquet", "labels.parquet", "predictions.jsonl", "config.json")},
        "unverified": ["exchange margin and liquidation labels", "USD NAV without independent fiat anchor",
                       "current instrument rules applied as an explicit simulation assumption"],
        "decision": "experimental results; no factor or model accepted for real capital",
    }
    for baseline, outcome in report["strategy_comparison"].items():
        report["experiments"].append({"name": baseline + " native backtest", "status": outcome["status"],
                                      "reason": outcome.get("reason")})
    (output_dir / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")
    return report


def main():
    parser = argparse.ArgumentParser(description="Registered factor and model experiment")
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--config-json", type=Path, required=True)
    args = parser.parse_args()
    report = run_research(json.loads(args.config_json.read_text(encoding="utf-8")), args.data_dir, args.output_dir)
    print(json.dumps({"split": report["split"], "models": report["models"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
