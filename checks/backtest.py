from dataclasses import replace
from decimal import Decimal
import json
from pathlib import Path
from tempfile import TemporaryDirectory

import polars as pl

from usdt_quant.backtest import (
    BacktestData,
    FundingPoint,
    InstrumentMetadata,
    MarketPoint,
    execution_points,
    merge_funding_observations,
    position_quantities,
    run_backtest,
)
from usdt_quant.strategy import BacktestConfig, FundingObservation


SECOND = 1_000_000_000
HOUR = 3_600 * SECOND
START = 1_704_067_200 * SECOND


def config(baseline: str) -> BacktestConfig:
    return BacktestConfig(
        baseline=baseline,
        data_version="synthetic-v1",
        exchange="synthetic",
        base_asset="BTC",
        start_ns=START,
        end_ns=START + 8 * HOUR,
        decision_interval_ns=HOUR,
        holding_period_ns=8 * HOUR,
        funding_window=21,
        initial_spot_usdt=Decimal("10000"),
        initial_perp_usdt=Decimal("10000"),
        target_spot_base=Decimal("12"),
        spot_taker_fee=Decimal("0.001"),
        perp_taker_fee=Decimal("0.0002"),
        execution_bps_per_leg=Decimal("5"),
        buffer_usdt=Decimal("1"),
    )


def sample_data(*, include_history: bool = True) -> BacktestData:
    # Entry signal is generated at START and must fill on the next shared record.
    points = tuple(
        MarketPoint.from_mid(ts, spot, perp, mark, Decimal("5"))
        for ts, spot, perp, mark in (
            (START, "100", "101", "101"),
            (START + HOUR, "101", "102", "102"),
            (START + 4 * HOUR, "103", "104", "104"),
            # B0's known end may close on the scheduled end record itself.
            (START + 8 * HOUR, "104", "104.5", "104.5"),
        )
    )
    available_history = tuple(
        FundingObservation(
            settlement_ts=START - (21 - index) * 4 * HOUR,
            available_ts=START - (21 - index) * 4 * HOUR + SECOND,
            realized_rate=Decimal("0.004"),
            interval_hours=Decimal("4"),
        )
        for index in range(21)
    ) if include_history else ()
    delayed_history = tuple(
        FundingObservation(
            settlement_ts=START - (11 - index) * 4 * HOUR + SECOND,
            available_ts=START + 4 * HOUR + SECOND,
            realized_rate=Decimal("-0.02"),
            interval_hours=Decimal("4"),
        )
        for index in range(11)
    ) if include_history else ()
    # This negative realized rate is unavailable at START, so it cannot alter
    # B1's entry feature, but native settlement must still debit the open short.
    funding = (FundingPoint(
        settlement_ts=START + 4 * HOUR,
        available_ts=START + 4 * HOUR + SECOND,
        realized_rate=Decimal("-0.001"),
        mark_price=Decimal("104"),
        interval_hours=Decimal("4"),
    ),)
    return BacktestData(
        points,
        funding,
        available_history + delayed_history,
        InstrumentMetadata(
            contract_multiplier=Decimal("5"),
            spot_size_increment=Decimal("1"),
            perp_contract_increment=Decimal("1"),
            spot_price_increment=Decimal("0.01"),
            perp_price_increment=Decimal("0.01"),
        ),
    )


def check_missing_funding() -> None:
    with TemporaryDirectory() as directory:
        dataset = Path(directory)
        bars = pl.DataFrame({"close_ts": [START], "available_ts": [START],
                             "is_closed": [True], "close": [Decimal("100")]})
        for name in ("spot_bars", "perp_bars", "mark_bars"):
            bars.write_parquet(dataset / f"{name}.parquet")
        metadata = pl.DataFrame({"effective_from": [START], "contract_multiplier": [Decimal(1)],
                                "lot_size": [Decimal("0.01")], "tick_size": [Decimal("0.01")]})
        for name in ("spot_instrument_meta", "perp_instrument_meta"):
            metadata.write_parquet(dataset / f"{name}.parquet")
        funding = pl.DataFrame({
            "settlement_ts": [START, START + HOUR], "available_ts": [START, START + HOUR],
            "realized_rate": [Decimal("0.001"), None],
            "mark_price_at_settlement": [Decimal(100), Decimal(100)],
            "actual_interval_hours": [None, Decimal(1)],
        })
        path = dataset / "funding_settlement.parquet"
        funding.write_parquet(path)
        try:
            BacktestData.from_parquet(dataset)
        except ValueError as error:
            assert "missing realized_rate" in str(error) and str(START + HOUR) in str(error)
        else:
            raise AssertionError("missing actual funding rate was silently discarded")
        funding.with_columns(pl.col("realized_rate").fill_null(Decimal(0))).write_parquet(path)
        assert len(BacktestData.from_parquet(dataset).funding) == 2


def main() -> None:
    check_missing_funding()
    data = sample_data()
    unknown_interval = FundingPoint(
        settlement_ts=START - HOUR,
        available_ts=START - HOUR + SECOND,
        realized_rate=Decimal("0.001"),
        mark_price=Decimal("100"),
        interval_hours=None,
    )
    assert merge_funding_observations((), (unknown_interval,)) == ()
    sized = position_quantities(config("B1"), data.metadata)
    assert sized == (Decimal("12"), Decimal("2"))
    priced = execution_points(config("B1"), data)
    assert priced[1].spot_ask == Decimal("101.06")
    assert priced[1].perp_bid == Decimal("101.94")
    duplicate = data.funding[0].observation()
    merged = merge_funding_observations((duplicate,), data.funding)
    assert len(merged) == 1

    with TemporaryDirectory() as directory:
        for baseline in ("B0", "B1"):
            clipped = run_backtest(
                replace(config(baseline), end_ns=START + 2 * HOUR),
                data, Path(directory) / f"clipped-{baseline}",
            )
            assert clipped["summary"]["status"] == "no_trade"
            assert Decimal(clipped["summary"]["funding_usdt"]) == 0
            equity = [json.loads(line) for line in Path(clipped["artifacts"]["equity"]).read_text().splitlines()]
            assert all(START <= row["ts"] <= START + 2 * HOUR for row in equity)
        short_hold = run_backtest(
            replace(config("B0"), holding_period_ns=4 * HOUR),
            data, Path(directory) / "short-hold",
        )
        assert short_hold["summary"]["exit_fill_ts"] == START + 4 * HOUR
        bounded = run_backtest(
            replace(config("B0"), end_ns=START + 4 * HOUR, holding_period_ns=4 * HOUR),
            replace(data, funding=data.funding + (FundingPoint(
                START + 7 * HOUR, START + 7 * HOUR, Decimal("-1"), None, Decimal(3),
            ),)), Path(directory) / "outside-funding",
        )
        assert bounded["summary"]["net_pnl_usdt"] == short_hold["summary"]["net_pnl_usdt"]
        assert bounded["summary"]["funding_settlement_status"] == "exact_native"
        assert bounded["data"]["market_points"] == 3 and bounded["data"]["funding_settlements"] == 1
        try:
            run_backtest(replace(config("B0"), holding_period_ns=2 * HOUR),
                         data, Path(directory) / "missing-expiry")
        except RuntimeError as error:
            assert "expiry" in str(error)
        else:
            raise AssertionError("missing expiry quote was silently filled later")

        drawdown_data = BacktestData(
            tuple(MarketPoint.from_mid(START + n * HOUR, str(spot), "100", "100", Decimal(0))
                  for n, spot in ((0, 100), (1, 100), (2, 11000), (8, 6000))),
            (), (), InstrumentMetadata(Decimal(1), Decimal(1), Decimal(1), Decimal(".01"), Decimal(".01")),
        )
        drawdown = run_backtest(
            replace(config("B0"), target_spot_base=Decimal(1), spot_taker_fee=Decimal(0),
                    perp_taker_fee=Decimal(0), execution_bps_per_leg=Decimal(0)),
            drawdown_data, Path(directory) / "drawdown",
        )
        assert drawdown["summary"]["max_drawdown_usdt"] == "5000.00000000"
        assert Decimal(drawdown["summary"]["max_drawdown_rate"]) == (Decimal(5000) / 30900).quantize(Decimal(".00000001"))

        m1 = run_backtest(config("M1"), data, Path(directory) / "m1",
                          predictions={START: Decimal(".0001"), START + HOUR: Decimal("-1")})
        assert m1["summary"]["fill_count"] == 4  # 2 USDT predicted net > 1 buffer; no second fee deduction.
        assert m1["summary"]["exit_fill_ts"] == START + 8 * HOUR
        assert m1["decisions"][0]["predicted_net_usdt"] == "2.0000"
        for name, predictions in (("missing", None), ("stale", {START - SECOND: Decimal(1)})):
            skipped = run_backtest(config("M1"), data, Path(directory) / name, predictions=predictions)
            assert skipped["summary"]["status"] == "no_trade"
            assert skipped["summary"]["no_trade_reason"] == "missing_prediction"
        m1_points = tuple(sorted(data.market + (MarketPoint.from_mid(
            START + 5 * HOUR, "104", "105", "105", Decimal(5),
        ),), key=lambda row: row.ts))
        later_prediction = run_backtest(
            replace(config("M1"), holding_period_ns=4 * HOUR),
            replace(data, market=m1_points), Path(directory) / "later-prediction",
            predictions={START: Decimal(-1), START + 4 * HOUR: Decimal(".001")},
        )
        assert later_prediction["summary"]["entry_signal_ts"] == START + 4 * HOUR
        assert later_prediction["summary"]["entry_fill_ts"] == START + 5 * HOUR
        assert later_prediction["summary"]["exit_fill_ts"] == START + 8 * HOUR

        b0 = run_backtest(config("B0"), data, Path(directory) / "b0")
        precise_mark = run_backtest(config("B0"), replace(data, funding=(
            replace(data.funding[0], mark_price=Decimal("104.12345678")),
        )), Path(directory) / "precise-mark")
        assert Decimal(precise_mark["summary"]["funding_usdt"]) == Decimal("-1.04123457")
        b1 = run_backtest(config("B1"), data, Path(directory) / "b1")
        no_history = run_backtest(
            config("B1"), sample_data(include_history=False), Path(directory) / "empty",
        )
        boundary = run_backtest(
            replace(
                config("B0"),
                end_ns=START + 4 * HOUR,
                holding_period_ns=4 * HOUR,
            ),
            data,
            Path(directory) / "boundary",
        )
        scaled_metadata = run_backtest(
            replace(config("B0"), base_asset="ETH"),
            replace(
                data,
                metadata=InstrumentMetadata(
                    contract_multiplier=Decimal("5.000000000000000000"),
                    spot_size_increment=Decimal("1.000000000000000000"),
                    perp_contract_increment=Decimal("1.000000000000000000"),
                    spot_price_increment=Decimal("0.010000000000000000"),
                    perp_price_increment=Decimal("0.010000000000000000"),
                ),
            ),
            Path(directory) / "scaled-metadata",
        )

        assert b0["summary"]["fill_count"] == 4
        assert b1["summary"]["fill_count"] == 4
        assert no_history["summary"]["status"] == "no_trade"
        assert no_history["summary"]["no_trade_reason"] == "insufficient_funding_history"
        assert boundary["summary"]["funding_usdt"] == "-1.04000000"
        assert boundary["summary"]["exit_fill_ts"] == START + 4 * HOUR
        assert scaled_metadata["summary"]["fill_count"] == 4
        assert scaled_metadata["data"]["spot_base_currency"] == "ETH"

        invalid_changes = (
            {"start_ns": 1.2},
            {"start_ns": True},
            {"spot_taker_fee": Decimal("NaN")},
            {"execution_bps_per_leg": Decimal("Infinity")},
            {"execution_bps_per_leg": Decimal("10000")},
            {"perp_taker_fee": Decimal("1")},
        )
        for changes in invalid_changes:
            try:
                replace(config("B0"), **changes)
            except ValueError:
                pass
            else:
                raise AssertionError(f"invalid config accepted: {changes}")

        # Multiplier 5 and whole-contract steps turn 12 spot BTC into two
        # contracts (10 BTC equivalent), leaving a visible 2 BTC delta.
        assert b1["summary"]["perp_contracts"] == "2"
        assert b1["summary"]["residual_delta_base"] == "2"
        assert b1["summary"]["entry_signal_ts"] == START
        assert b1["summary"]["entry_fill_ts"] == START + HOUR
        assert b0["summary"]["exit_fill_ts"] == START + 8 * HOUR
        assert b1["summary"]["funding_usdt"] == "-1.04000000"
        assert b1["summary"]["actual_funding_intervals_hours"] == ["4"]
        assert b1["summary"]["final_nav_usdt"] == b1["summary"]["reconciled_nav_usdt"]
        assert b1["summary"]["net_pnl_usdt"] == b1["summary"]["reconciled_net_pnl_usdt"]
        assert Decimal(b1["summary"]["two_leg_price_pnl_usdt"]) == (
            Decimal(b1["summary"]["basis_pnl_usdt"])
            + Decimal(b1["summary"]["residual_directional_pnl_usdt"])
        )
        assert b1["summary"]["usd_nav"] is None
        assert "usd_anchor_missing" in b1["unverified"]
        assert "exchange_margin_and_liquidation_rules" in b1["unverified"]
        assert b1["assumptions"]["account_structure"] == "isolated_simulation_ledgers"
        assert b1["config"]["future_basis_change_prediction"] == "0"

        fills = [line for line in (Path(directory) / "b1" / "fills.jsonl").read_text().splitlines()]
        funding_lines = [line for line in (Path(directory) / "b1" / "funding.jsonl").read_text().splitlines()]
        final_equity = json.loads(
            (Path(directory) / "b1" / "equity.jsonl").read_text().splitlines()[-1],
        )
        assert len(fills) == 4
        assert len(funding_lines) == 1
        assert Decimal(final_equity["nav_usdt"]) == sum((
            Decimal(final_equity["spot_cash_usdt"]),
            Decimal(final_equity["spot_base_value_usdt"]),
            Decimal(final_equity["perp_margin_balance_usdt"]),
            Decimal(final_equity["perp_unrealized_pnl_usdt"]),
        ))
        assert Decimal(b1["summary"]["max_native_maintenance_margin_usdt"]) > 0
        assert Decimal(b1["summary"]["min_native_perp_free_balance_usdt"]) > 0
        assert b1["summary"]["funding_settlement_status"] == "exact_native"
        # Execution bp is represented once by native bid/ask fills; the report
        # must not subtract a second synthetic slippage charge.
        assert b1["summary"]["additional_slippage_charge_usdt"] == "0"

    print("backtest checks passed")


if __name__ == "__main__":
    main()
