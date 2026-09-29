from dataclasses import replace
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
import polars as pl

from usdt_quant.backtest import BacktestData, FundingPoint, InstrumentMetadata, MarketPoint, run_backtest
from usdt_quant.strategy import BacktestConfig
from usdt_quant.research import (
    FACTORS, _apply_f09, _factor_experiments, _fit_f09_stats, _load_factor_inputs,
    compare_strategies, factor_frame, fit_models, label_frame, purged_split, run_research,
)


HOUR = 3_600_000_000_000
START = 1_704_067_200_000_000_000


def main():
    market = tuple(MarketPoint.from_mid(
        START + i * HOUR, Decimal(100 + i % 13),
        Decimal(101 + i % 13) + Decimal(i % 7) / 100, Decimal(101 + i % 13), Decimal(0),
    ) for i in range(24 * 40))
    funding = tuple(FundingPoint(
        START + i * 4 * HOUR + HOUR // 2, START + i * 4 * HOUR + HOUR * 3 // 2,
        Decimal("0.001") if i % 3 else Decimal("-0.0005"), Decimal(100), Decimal(4),
    ) for i in range(24 * 10))
    data = BacktestData(market, funding, tuple(row.observation() for row in funding),
                        InstrumentMetadata(*(Decimal("0.01"),) * 5))
    cutoff = START + 20 * 24 * HOUR
    decisions = list(range(START + 8 * 24 * HOUR, cutoff + HOUR, HOUR))
    original = factor_frame(data, decisions)
    unknown_interval = replace(data, funding=(replace(funding[0], interval_hours=None), *funding[1:]),
                               funding_history=data.funding_history[1:])
    assert factor_frame(unknown_interval, decisions).height == len(decisions)
    changed = replace(data,
        market=tuple(replace(row, spot_bid=Decimal(1), spot_ask=Decimal(1))
                     if row.ts > cutoff else row for row in market),
        funding=tuple(replace(row, realized_rate=Decimal(1))
                      if row.available_ts > cutoff else row for row in funding),
        funding_history=tuple(replace(row, realized_rate=Decimal(1))
                              if row.available_ts > cutoff else row
                              for row in data.funding_history))
    assert original.equals(factor_frame(changed, decisions)), "future inputs changed earlier factors"
    assert (original["input_max_available_ts"] <= original["decision_ts"]).all()
    assert original["F01"].null_count() == 0
    assert original["F06"].null_count() == 0
    assert FACTORS == tuple(f"F{i:02d}" for i in range(1, 13))

    feature_decision = START + 200 * HOUR
    feature_funding = tuple(FundingPoint(
        feature_decision - (20 - i) * 8 * HOUR,
        feature_decision - (20 - i) * 8 * HOUR,
        Decimal("0.001"), Decimal(100), Decimal(8),
    ) for i in range(21))
    feature_data = replace(
        data,
        funding=feature_funding,
        funding_history=tuple(row.observation() for row in feature_funding),
    )
    minute = HOUR // 60
    quotes = pl.DataFrame({
        "target_settlement_ts": [value for row in feature_funding
                                  for value in (row.settlement_ts, row.settlement_ts)],
        "available_ts": [value for row in feature_funding
                          for value in (row.settlement_ts - HOUR // 2,
                                        row.settlement_ts - 29 * minute)],
        "indicative_rate": [value for _ in feature_funding
                            for value in (0.0015, 99.0)],
    })
    closes = [feature_decision - (59 - i) * minute for i in range(60)]
    inputs = {
        "funding_quotes": quotes,
        "open_interest": pl.DataFrame({
            "available_ts": [feature_decision - 8 * HOUR, feature_decision],
            "oi_base_qty": [100.0, 125.0],
        }),
        "spot_bars": pl.DataFrame({
            "close_ts": closes, "available_ts": closes, "is_closed": [True] * 60,
            "quote_volume": [100.0] * 60, "taker_buy_quote_volume": [40.0] * 60,
        }),
        "perp_bars": pl.DataFrame({
            "close_ts": closes, "available_ts": closes, "is_closed": [True] * 60,
            "quote_volume": [200.0] * 60, "taker_buy_quote_volume": [120.0] * 60,
        }),
    }
    feature_row = factor_frame(feature_data, [feature_decision], inputs).row(0, named=True)
    assert np.isclose(feature_row["F05"], 0.0005)
    assert np.isclose(feature_row["F08"], 0.25)
    assert feature_row["F09"] is None
    assert np.isclose(feature_row["F10"], 0.2)
    assert feature_row["F11"] is None
    assert feature_row["F12"] is None
    assert feature_row["input_max_available_ts"] == feature_decision
    f09_training = pl.DataFrame({"F01": [1.0, 3.0], "F08": [10.0, 14.0]})
    f09_stats = _fit_f09_stats(f09_training)
    assert f09_stats == {
        "n": 2,
        "mean": {"F01": 2.0, "F08": 12.0},
        "scale": {"F01": 1.0, "F08": 2.0},
    }
    f09_applied = _apply_f09(
        pl.DataFrame({"F01": [4.0, None], "F08": [8.0, 8.0], "F09": [None, None]}),
        f09_stats,
    )
    assert f09_applied["F09"].to_list() == [-4.0, None]
    unusable_f09_stats = _fit_f09_stats(pl.DataFrame({
        "F01": [1.0, 1.0], "F08": [10.0, 10.0],
    }))
    assert _apply_f09(
        f09_training.with_columns(pl.lit(None).alias("F09")), unusable_f09_stats,
    )["F09"].null_count() == 2
    changed_f09_test = pl.DataFrame({"F01": [40_000.0], "F08": [-80_000.0]})
    assert _fit_f09_stats(f09_training) == f09_stats
    assert _fit_f09_stats(f09_training) != _fit_f09_stats(changed_f09_test)
    factor_status = {row["name"]: row for row in _factor_experiments(pl.DataFrame({
        "F05": [None], "F08": [0.25], "F09": [None],
        "F10": [0.2], "F11": [0.0045], "F12": [None],
    }))}
    assert factor_status["F08"] == {"name": "F08", "status": "evaluated", "samples": 1}
    assert {name for name, row in factor_status.items() if row["status"] == "evaluated"} == {
        "F08", "F10", "F11",
    }
    for name in ("F05", "F09", "F12"):
        assert factor_status[name]["status"] == "not_run"
        assert factor_status[name]["samples"] == 0
        assert factor_status[name]["reason"] == "no_non_null_samples"

    oldest_funding = FundingPoint(
        feature_funding[0].settlement_ts - 8 * HOUR,
        feature_funding[0].settlement_ts - 8 * HOUR,
        Decimal("0.001"), Decimal(100), Decimal(8),
    )
    missing_target = feature_funding[10].settlement_ts
    incomplete_quotes = pl.concat([
        quotes.filter(pl.col("target_settlement_ts") != missing_target),
        pl.DataFrame({
            "target_settlement_ts": [oldest_funding.settlement_ts],
            "available_ts": [oldest_funding.settlement_ts - HOUR // 2],
            "indicative_rate": [0.0015],
        }),
    ])
    twenty_two = (oldest_funding, *feature_funding)
    incomplete_data = replace(
        data, funding=twenty_two,
        funding_history=tuple(row.observation() for row in twenty_two),
    )
    assert factor_frame(
        incomplete_data, [feature_decision], {"funding_quotes": incomplete_quotes},
    )["F05"][0] is None, "an older pair filled a gap in the latest 21 settlements"

    future_inputs = {
        **inputs,
        "funding_quotes": pl.concat([quotes, pl.DataFrame({
            "target_settlement_ts": [feature_decision],
            "available_ts": [feature_decision + 1], "indicative_rate": [999.0],
        })]),
        "open_interest": pl.concat([inputs["open_interest"], pl.DataFrame({
            "available_ts": [feature_decision + 1], "oi_base_qty": [999999.0],
        })]),
        "spot_bars": pl.concat([inputs["spot_bars"], pl.DataFrame({
            "close_ts": [feature_decision], "available_ts": [feature_decision + 1],
            "is_closed": [True], "quote_volume": [1.0],
            "taker_buy_quote_volume": [1.0],
        })]),
        "perp_bars": pl.concat([inputs["perp_bars"], pl.DataFrame({
            "close_ts": [feature_decision], "available_ts": [feature_decision + 1],
            "is_closed": [True], "quote_volume": [1.0],
            "taker_buy_quote_volume": [0.0],
        })]),
    }
    assert factor_frame(feature_data, [feature_decision], inputs).equals(
        factor_frame(feature_data, [feature_decision], future_inputs),
    ), "future optional inputs changed earlier factors"
    with TemporaryDirectory() as directory:
        input_directory = Path(directory)
        inputs["spot_bars"].write_parquet(input_directory / "spot_bars.parquet")
        inputs["perp_bars"].write_parquet(input_directory / "perp_bars.parquet")
        inputs["open_interest"].write_parquet(input_directory / "open_interest.parquet")
        loaded = _load_factor_inputs(input_directory)
        assert set(loaded) == {"spot_bars", "perp_bars", "open_interest"}

    gap_funding = tuple(FundingPoint(
        feature_decision - (2 - i) * 8 * HOUR,
        feature_decision - (2 - i) * 8 * HOUR,
        rate, Decimal(100), Decimal(8),
    ) for i, rate in enumerate(map(Decimal, ("0.001", "0.002", "0.003"))))
    gap_data = replace(
        data,
        funding=gap_funding,
        funding_history=tuple(row.observation() for row in gap_funding),
    )
    cross = pl.DataFrame({
        "settlement_ts": [row.settlement_ts for row in gap_funding],
        "available_ts": [row.available_ts for row in gap_funding],
        "realized_rate": [0.0005] * 3,
        "actual_interval_hours": [8.0] * 3,
    })
    gap_row = factor_frame(
        gap_data, [feature_decision], {"cross_funding_settlement": cross},
    ).row(0, named=True)
    assert np.isclose(gap_row["F11"], 0.0045)
    future_cross = pl.concat([cross, pl.DataFrame({
        "settlement_ts": [feature_decision], "available_ts": [feature_decision + 1],
        "realized_rate": [99.0], "actual_interval_hours": [8.0],
    })])
    assert np.isclose(factor_frame(
        gap_data, [feature_decision], {"cross_funding_settlement": future_cross},
    )["F11"][0], 0.0045)
    misaligned = cross.with_columns(
        pl.when(pl.col("settlement_ts") == feature_decision - 8 * HOUR)
        .then(pl.col("settlement_ts") + 1)
        .otherwise(pl.col("settlement_ts")).alias("settlement_ts"),
    )
    assert factor_frame(
        gap_data, [feature_decision], {"cross_funding_settlement": misaligned},
    )["F11"][0] is None
    # Each label matures one day later, so the final training day must be purged.
    rows = original.with_columns(
        (pl.col("decision_ts") + 24 * HOUR).alias("label_end_ts"),
        (pl.col("decision_ts") + 25 * HOUR).alias("label_available_ts"),
        (pl.col("F07") * 0.02).alias("y_net"),
        (pl.col("F07") < 0).cast(pl.Int64).alias("y_loss"),
    )
    train_end, val_end = START + 13 * 24 * HOUR, START + 17 * 24 * HOUR
    train, validation, test = purged_split(rows, train_end, val_end, cutoff + 30 * HOUR)
    assert train["label_available_ts"].max() < train_end
    assert validation["label_available_ts"].max() < val_end
    assert test["decision_ts"].min() >= val_end
    coverage_train = pl.DataFrame({
        "F01": [float(index) for index in range(99)] + [None],
        "F08": [1.0, 2.0] + [None] * 98,
        "F11": [float(index) for index in range(29)] + [None] * 71,
        "F12": [None] * 100,
        "y_net": [index / 1000 for index in range(100)],
        "y_loss": [index % 2 for index in range(100)],
    })
    coverage_result, coverage_models = fit_models(
        coverage_train, coverage_train.head(0), coverage_train.head(0),
        ridge_alpha=1.0, logistic_c=1.0,
    )
    assert coverage_result["active_factors"] == ["F01"]
    assert set(coverage_result["factor_coverage"]) == set(FACTORS)
    assert coverage_result["factor_coverage"]["F01"] == 0.99
    assert coverage_result["factor_coverage"]["F08"] == 0.02
    assert coverage_result["factor_coverage"]["F11"] == 0.29
    assert coverage_result["factor_coverage"]["F12"] == 0.0
    assert coverage_models["ridge"].active_factors == ("F01",)
    result, models = fit_models(train, validation, test, ridge_alpha=1.0, logistic_c=1.0)
    assert set(result["active_factors"]) == {"F01", "F02", "F03", "F04", "F06", "F07"}
    assert not ({"F05", "F08", "F09", "F10", "F11", "F12"} & set(result["active_factors"]))
    assert tuple(result["active_factors"]) == models["ridge"].active_factors
    no_feature_result, no_feature_models = fit_models(
        pl.DataFrame({"y_net": [0.1, -0.1], "y_loss": [0, 1]}),
        pl.DataFrame({"y_net": [], "y_loss": []}, schema={"y_net": pl.Float64, "y_loss": pl.Int64}),
        pl.DataFrame({"y_net": [], "y_loss": []}, schema={"y_net": pl.Float64, "y_loss": pl.Int64}),
        ridge_alpha=1.0, logistic_c=1.0,
    )
    assert no_feature_result["status"] == "no_active_factors"
    assert no_feature_result["active_factors"] == [] and no_feature_models == {}
    changed_test = test.with_columns(*(pl.col(name) + 10_000 for name in FACTORS))
    _, changed_models = fit_models(train, validation, changed_test, ridge_alpha=1.0, logistic_c=1.0)
    np.testing.assert_array_equal(models["ridge"].named_steps["scale"].mean_,
                                  changed_models["ridge"].named_steps["scale"].mean_)
    assert result["ridge"]["test"]["n"] == test.height
    assert 0 <= result["logistic"]["test"]["brier_score"] <= 1
    configuration = BacktestConfig(
        baseline="B0", data_version="synthetic-research", exchange="synthetic", base_asset="BTC",
        start_ns=decisions[0], end_ns=decisions[0] + 24 * HOUR,
        decision_interval_ns=HOUR, holding_period_ns=24 * HOUR, funding_window=21,
        initial_spot_usdt=Decimal(10000), initial_perp_usdt=Decimal(10000),
        target_spot_base=Decimal(1), spot_taker_fee=Decimal("0.001"),
        perp_taker_fee=Decimal("0.0002"), execution_bps_per_leg=Decimal(5), buffer_usdt=Decimal(0))
    labels = label_frame(configuration, data, [decisions[0]])
    label = labels.filter(pl.col("horizon") == "24h").row(0, named=True)
    with TemporaryDirectory() as directory:
        native = run_backtest(configuration, data, Path(directory))
        comparison = compare_strategies(configuration, data, decisions[0],
            [{"decision_ts": decisions[0], "split": "test", "predicted_net_return": 0.01}],
            Path(directory) / "comparison")
        assert comparison["M1"]["summary"]["fill_count"] == 4
        assert Path(comparison["M1"]["report_path"]).is_file()
        assert comparison["M1"]["summary"]["exit_fill_ts"] == configuration.end_ns
        assert comparison["B0"]["summary"]["net_pnl_usdt"] == comparison["M1"]["summary"]["net_pnl_usdt"]
        off_grid = compare_strategies(
            replace(configuration, decision_interval_ns=2 * HOUR, end_ns=decisions[0] + 48 * HOUR),
            data, decisions[0] + HOUR,
            [{"decision_ts": decisions[0], "split": "test", "predicted_net_return": 0.01},
             {"decision_ts": decisions[0] + 2 * HOUR, "split": "test", "predicted_net_return": 0.01}],
            Path(directory) / "off-grid", entry_analysis_ns=decisions[0] + 2 * HOUR)
        assert off_grid["M1"]["summary"]["entry_signal_ts"] == decisions[0] + 2 * HOUR
        skipped = compare_strategies(
            replace(configuration, end_ns=decisions[0] + 48 * HOUR), data, decisions[0],
            [{"decision_ts": decisions[0], "split": "test", "predicted_net_return": -0.01},
             {"decision_ts": decisions[0] + HOUR, "split": "test", "predicted_net_return": 0.01}],
            Path(directory) / "selected-skip", entry_analysis_ns=decisions[0])
        assert skipped["M1"]["summary"]["status"] == "no_trade"
        assert skipped["M1"]["summary"]["entry_signal_ts"] is None
        assert skipped["M1"]["summary"]["no_trade_reason"] == "expected_net_not_above_buffer"

    with TemporaryDirectory() as directory:
        root = Path(directory)
        dataset, output = root / "dataset", root / "output"
        dataset.mkdir()
        closes = [point.ts for point in market]
        for name, values in (
            ("spot_bars", [point.spot_bid for point in market]),
            ("perp_bars", [point.perp_bid for point in market]),
            ("mark_bars", [point.mark_price for point in market]),
        ):
            pl.DataFrame({
                "close_ts": closes, "available_ts": closes,
                "is_closed": [True] * len(closes),
                "close": [str(value) for value in values],
            }).write_parquet(dataset / f"{name}.parquet")
        pl.DataFrame({
            "settlement_ts": [row.settlement_ts for row in funding],
            "available_ts": [row.available_ts for row in funding],
            "realized_rate": ["0.001" if (index // 8) % 2 else "-0.0005"
                              for index in range(len(funding))],
            "mark_price_at_settlement": [str(row.mark_price) for row in funding],
            "actual_interval_hours": [str(row.interval_hours) for row in funding],
        }).write_parquet(dataset / "funding_settlement.parquet")
        for name, increment, multiplier in (
            ("spot_instrument_meta", data.metadata.spot_size_increment, Decimal(1)),
            ("perp_instrument_meta", data.metadata.perp_contract_increment,
             data.metadata.contract_multiplier),
        ):
            pl.DataFrame({
                "effective_from": [0], "contract_multiplier": [str(multiplier)],
                "lot_size": [str(increment)], "tick_size": ["0.01"],
            }).write_parquet(dataset / f"{name}.parquet")
        pl.DataFrame({
            "available_ts": closes,
            "oi_base_qty": [1000.0 + index + (index % 17) ** 2 for index in range(len(closes))],
        }).write_parquet(dataset / "open_interest.parquet")
        research_values = {
            **configuration.as_json(), "data_version": "synthetic-f09",
            "start_ns": decisions[0], "end_ns": cutoff,
            "train_end_ns": train_end, "validation_end_ns": val_end,
            "ridge_alpha": 1.0, "logistic_c": 1.0, "seed": 7,
            "bootstrap_samples": 2,
        }
        report = run_research(research_values, dataset, output)
        persisted_factors = pl.read_parquet(output / "factors.parquet")
        persisted_labels = pl.read_parquet(output / "labels.parquet")
        persisted_rows = persisted_factors.join(
            persisted_labels.filter(pl.col("horizon") == "24h"), on="decision_ts",
        ).filter(pl.col("y_net").is_not_null())
        persisted_train, _, _ = purged_split(persisted_rows, train_end, val_end, cutoff)
        assert report["factor_training"]["F09"]["n"] > 1
        assert report["factor_training"]["F09"] == _fit_f09_stats(persisted_train)
        assert all(value > 0 for value in
                   report["factor_training"]["F09"]["scale"].values())
        assert persisted_factors["F09"].drop_nulls().len() > 0
        assert "F09" in report["models"]["active_factors"]
    assert abs(label["y_net"] - float(native["summary"]["return_on_total_capital"])) < 1e-10
    assert label["entry_ts"] > label["decision_ts"]
    assert label["label_available_ts"] >= label["label_end_ts"]
    print("research checks passed: availability, label purge, train-only preprocessing, native PnL match")


if __name__ == "__main__":
    main()
