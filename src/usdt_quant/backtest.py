from __future__ import annotations

import argparse
from dataclasses import dataclass
from decimal import Decimal, ROUND_CEILING, ROUND_DOWN, ROUND_FLOOR
import json
from pathlib import Path
from typing import Iterable, Mapping

import polars as pl
from nautilus_trader.backtest import BacktestEngine
from nautilus_trader.common import LogLevel
from nautilus_trader.config import BacktestEngineConfig, LoggerConfig
from nautilus_trader.model import (
    AccountType,
    CryptoPerpetual,
    Currency,
    CurrencyPair,
    FundingRateUpdate,
    MarkPriceUpdate,
    Money,
    OmsType,
    Price,
    QuoteTick,
)
from nautilus_trader.testkit.providers import TestInstrumentProvider

from usdt_quant.strategy import BacktestConfig, CarryStrategy, FundingObservation


USDT = Currency.from_str("USDT")
EIGHT_PLACES = Decimal("0.00000001")


def _decimal(value) -> Decimal:
    return Decimal(value).normalize()


def _decimal_str(value: Decimal) -> str:
    return format(_decimal(value), "f")


@dataclass(frozen=True)
class InstrumentMetadata:
    contract_multiplier: Decimal
    spot_size_increment: Decimal
    perp_contract_increment: Decimal
    spot_price_increment: Decimal
    perp_price_increment: Decimal

    def __post_init__(self) -> None:
        values = (
            self.contract_multiplier, self.spot_size_increment,
            self.perp_contract_increment, self.spot_price_increment,
            self.perp_price_increment,
        )
        if any(not isinstance(value, Decimal) or not value.is_finite() for value in values):
            raise ValueError("instrument multiplier and increments must be finite Decimals")
        if min(
            *values,
        ) <= 0:
            raise ValueError("instrument multiplier and increments must be positive")


@dataclass(frozen=True)
class MarketPoint:
    ts: int
    spot_bid: Decimal
    spot_ask: Decimal
    perp_bid: Decimal
    perp_ask: Decimal
    mark_price: Decimal

    def __post_init__(self) -> None:
        if type(self.ts) is not int:
            raise ValueError("market ts must be an integer")
        prices = (
            self.spot_bid, self.spot_ask, self.perp_bid, self.perp_ask, self.mark_price,
        )
        if any(not isinstance(value, Decimal) or not value.is_finite() for value in prices):
            raise ValueError("market prices must be finite Decimals")
        if self.ts < 0 or min(
            *prices,
        ) <= 0:
            raise ValueError("market timestamps and prices must be positive")
        if self.spot_bid > self.spot_ask or self.perp_bid > self.perp_ask:
            raise ValueError("bid cannot exceed ask")

    @classmethod
    def from_mid(
        cls,
        ts: int,
        spot_mid: Decimal | str,
        perp_mid: Decimal | str,
        mark_price: Decimal | str,
        execution_bps_per_leg: Decimal,
    ) -> "MarketPoint":
        spot_mid = Decimal(spot_mid)
        perp_mid = Decimal(perp_mid)
        half_spread = execution_bps_per_leg / Decimal("10000")
        return cls(
            ts=ts,
            spot_bid=spot_mid * (1 - half_spread),
            spot_ask=spot_mid * (1 + half_spread),
            perp_bid=perp_mid * (1 - half_spread),
            perp_ask=perp_mid * (1 + half_spread),
            mark_price=Decimal(mark_price),
        )


@dataclass(frozen=True)
class FundingPoint:
    settlement_ts: int
    available_ts: int
    realized_rate: Decimal
    mark_price: Decimal | None
    interval_hours: Decimal | None

    def __post_init__(self) -> None:
        if type(self.settlement_ts) is not int or type(self.available_ts) is not int:
            raise ValueError("funding timestamps must be integers")
        if not isinstance(self.realized_rate, Decimal) or not self.realized_rate.is_finite():
            raise ValueError("funding realized_rate must be a finite Decimal")
        if self.mark_price is not None and (
            not isinstance(self.mark_price, Decimal) or not self.mark_price.is_finite()
        ):
            raise ValueError("funding mark_price must be a finite Decimal")
        if self.interval_hours is not None and (
            not isinstance(self.interval_hours, Decimal) or not self.interval_hours.is_finite()
        ):
            raise ValueError("funding interval_hours must be a finite Decimal")
        if self.available_ts < self.settlement_ts:
            raise ValueError("funding available_ts cannot precede settlement_ts")
        if self.interval_hours is not None and self.interval_hours <= 0:
            raise ValueError("funding interval_hours must be positive")
        if self.mark_price is not None and self.mark_price <= 0:
            raise ValueError("funding mark_price must be positive")

    def observation(self) -> FundingObservation | None:
        if self.interval_hours is None:
            return None
        return FundingObservation(
            settlement_ts=self.settlement_ts,
            available_ts=self.available_ts,
            realized_rate=self.realized_rate,
            interval_hours=self.interval_hours,
        )


@dataclass(frozen=True)
class BacktestData:
    market: tuple[MarketPoint, ...]
    funding: tuple[FundingPoint, ...]
    funding_history: tuple[FundingObservation, ...]
    metadata: InstrumentMetadata

    def __post_init__(self) -> None:
        timestamps = [point.ts for point in self.market]
        if not timestamps or timestamps != sorted(set(timestamps)):
            raise ValueError("market points must have unique increasing timestamps")
        settlements = [point.settlement_ts for point in self.funding]
        if settlements != sorted(set(settlements)):
            raise ValueError("funding settlements must have unique increasing timestamps")

    @classmethod
    def from_parquet(cls, directory: Path | str) -> "BacktestData":
        directory = Path(directory)
        spot = _bars_by_close(directory / "spot_bars.parquet")
        perp = _bars_by_close(directory / "perp_bars.parquet")
        mark = _bars_by_close(directory / "mark_bars.parquet")
        shared = sorted(set(spot) & set(perp) & set(mark))
        if not shared:
            raise ValueError("no shared closed spot/perp/mark bars")
        market = tuple(MarketPoint(
            ts=max(int(spot[key]["available_ts"]), int(perp[key]["available_ts"]),
                   int(mark[key]["available_ts"])),
            spot_bid=_decimal(spot[key]["close"]),
            spot_ask=_decimal(spot[key]["close"]),
            perp_bid=_decimal(perp[key]["close"]),
            perp_ask=_decimal(perp[key]["close"]),
            mark_price=_decimal(mark[key]["close"]),
        ) for key in shared)

        funding_rows = pl.read_parquet(directory / "funding_settlement.parquet").to_dicts()
        missing_rates = [row["settlement_ts"] for row in funding_rows if row["realized_rate"] is None]
        if missing_rates:
            raise ValueError(f"missing realized_rate at settlement_ts (ns): {missing_rates}")
        funding = tuple(sorted((FundingPoint(
            settlement_ts=int(row["settlement_ts"]),
            available_ts=int(row["available_ts"]),
            realized_rate=_decimal(row["realized_rate"]),
            mark_price=(_decimal(row["mark_price_at_settlement"])
                        if row["mark_price_at_settlement"] is not None else None),
            interval_hours=(_decimal(row["actual_interval_hours"])
                            if row["actual_interval_hours"] is not None else None),
        ) for row in funding_rows),
            key=lambda row: row.settlement_ts))

        spot_meta = _single_meta(directory / "spot_instrument_meta.parquet")
        perp_meta = _single_meta(directory / "perp_instrument_meta.parquet")
        metadata = InstrumentMetadata(
            contract_multiplier=_decimal(perp_meta["contract_multiplier"]),
            spot_size_increment=_decimal(spot_meta["lot_size"]),
            perp_contract_increment=_decimal(perp_meta["lot_size"]),
            spot_price_increment=_decimal(spot_meta["tick_size"]),
            perp_price_increment=_decimal(perp_meta["tick_size"]),
        )
        return cls(
            market,
            funding,
            tuple(observation for row in funding
                  if (observation := row.observation()) is not None),
            metadata,
        )


def _bars_by_close(path: Path) -> dict[int, dict]:
    rows = pl.read_parquet(path).filter(pl.col("is_closed") == True).to_dicts()  # noqa: E712
    return {int(row["close_ts"]): row for row in rows}


def _single_meta(path: Path) -> dict:
    rows = pl.read_parquet(path).sort("effective_from").to_dicts()
    if not rows:
        raise ValueError(f"missing instrument metadata: {path}")
    return rows[-1]


def _precision(increment: Decimal) -> int:
    return max(0, -increment.normalize().as_tuple().exponent)


def _instruments(config: BacktestConfig, metadata: InstrumentMetadata):
    spot_values = TestInstrumentProvider.btcusdt_binance().to_dict()
    spot_values.update({
        "id": f"{config.base_asset}USDT.SIM_SPOT",
        "raw_symbol": f"{config.base_asset}USDT",
        "base_currency": config.base_asset,
        "price_precision": _precision(metadata.spot_price_increment),
        "size_precision": _precision(metadata.spot_size_increment),
        "price_increment": _decimal_str(metadata.spot_price_increment),
        "size_increment": _decimal_str(metadata.spot_size_increment),
        "lot_size": _decimal_str(metadata.spot_size_increment),
        "maker_fee": _decimal_str(config.spot_taker_fee),
        "taker_fee": _decimal_str(config.spot_taker_fee),
        "max_quantity": None,
        "min_quantity": _decimal_str(metadata.spot_size_increment),
        "max_price": None,
        "min_price": _decimal_str(metadata.spot_price_increment),
    })
    perp_values = TestInstrumentProvider.btcusdt_perp_binance().to_dict()
    perp_values.update({
        "id": f"{config.base_asset}USDT-PERP.SIM_PERP",
        "raw_symbol": f"{config.base_asset}USDT",
        "base_currency": config.base_asset,
        "price_precision": _precision(metadata.perp_price_increment),
        "size_precision": _precision(metadata.perp_contract_increment),
        "price_increment": _decimal_str(metadata.perp_price_increment),
        "size_increment": _decimal_str(metadata.perp_contract_increment),
        "multiplier": _decimal_str(metadata.contract_multiplier),
        "lot_size": _decimal_str(metadata.perp_contract_increment),
        "maker_fee": _decimal_str(config.perp_taker_fee),
        "taker_fee": _decimal_str(config.perp_taker_fee),
        "max_quantity": None,
        "min_quantity": _decimal_str(metadata.perp_contract_increment),
        "max_price": None,
        "min_price": _decimal_str(metadata.perp_price_increment),
    })
    return CurrencyPair.from_dict(spot_values), CryptoPerpetual.from_dict(perp_values)


def _round_down(value: Decimal, increment: Decimal) -> Decimal:
    return ((value / increment).to_integral_value(rounding=ROUND_DOWN) * increment).normalize()


def position_quantities(
    config: BacktestConfig,
    metadata: InstrumentMetadata,
) -> tuple[Decimal, Decimal]:
    spot_quantity = _round_down(config.target_spot_base, metadata.spot_size_increment)
    perp_contracts = _round_down(
        spot_quantity / metadata.contract_multiplier,
        metadata.perp_contract_increment,
    )
    return spot_quantity, perp_contracts


def _tick(price: Decimal, increment: Decimal, rounding: str) -> Decimal:
    return ((price / increment).to_integral_value(rounding=rounding) * increment).normalize()


def execution_points(
    config: BacktestConfig,
    data: BacktestData,
) -> tuple[MarketPoint, ...]:
    """Apply configured bar execution cost once, then round to instrument ticks."""
    rate = config.execution_bps_per_leg / Decimal("10000")
    points = []
    for row in data.market:
        if row.spot_bid == row.spot_ask:
            spot_bid, spot_ask = row.spot_bid * (1 - rate), row.spot_ask * (1 + rate)
        else:
            spot_bid, spot_ask = row.spot_bid, row.spot_ask
        if row.perp_bid == row.perp_ask:
            perp_bid, perp_ask = row.perp_bid * (1 - rate), row.perp_ask * (1 + rate)
        else:
            perp_bid, perp_ask = row.perp_bid, row.perp_ask
        points.append(MarketPoint(
            ts=row.ts,
            spot_bid=_tick(spot_bid, data.metadata.spot_price_increment, ROUND_FLOOR),
            spot_ask=_tick(spot_ask, data.metadata.spot_price_increment, ROUND_CEILING),
            perp_bid=_tick(perp_bid, data.metadata.perp_price_increment, ROUND_FLOOR),
            perp_ask=_tick(perp_ask, data.metadata.perp_price_increment, ROUND_CEILING),
            mark_price=row.mark_price.normalize(),
        ))
    return tuple(points)


def merge_funding_observations(
    history: tuple[FundingObservation, ...],
    funding: tuple[FundingPoint, ...],
) -> tuple[FundingObservation, ...]:
    by_settlement = {row.settlement_ts: row for row in history}
    by_settlement.update({
        row.settlement_ts: observation
        for row in funding
        if (observation := row.observation()) is not None
    })
    return tuple(sorted(
        by_settlement.values(), key=lambda row: (row.settlement_ts, row.available_ts),
    ))


def _native_funding_details(account, funding: tuple[FundingPoint, ...], fills: list[dict], multiplier):
    events = list(account.events)
    details = []
    for point in funding:
        if point.mark_price is None:
            continue
        signed_contracts = Decimal("0")
        for fill in fills:
            if "PERP" not in fill["instrument"] or fill["ts"] >= point.settlement_ts:
                continue
            signed_contracts += (
                -fill["quantity"] if fill["side"].endswith("SELL") else fill["quantity"]
            )
        if signed_contracts == 0:
            continue
        expected = (-signed_contracts * multiplier * point.mark_price
                    * point.realized_rate).quantize(EIGHT_PLACES)
        before = [event for event in events if int(event.ts_event) < point.settlement_ts]
        at_boundary = [
            event for event in events
            if int(event.ts_event) == point.settlement_ts and event.is_reported
        ]
        if not before or not at_boundary:
            raise RuntimeError(f"missing native funding account event at {point.settlement_ts}")
        before_total = before[-1].balances[0].total.as_decimal()
        after_total = at_boundary[-1].balances[0].total.as_decimal()
        native_amount = (after_total - before_total).quantize(EIGHT_PLACES)
        if native_amount != expected:
            raise RuntimeError(
                f"native funding mismatch at {point.settlement_ts}: {native_amount} != {expected}",
            )
        details.append({
            "settlement_ts": point.settlement_ts,
            "available_ts": point.available_ts,
            "realized_rate": point.realized_rate,
            "mark_price": point.mark_price,
            "interval_hours": point.interval_hours,
            "signed_contracts": signed_contracts,
            "contract_multiplier": multiplier,
            "native_amount_usdt": native_amount,
            "native_account_balance_after_usdt": after_total,
        })
    return details


def _equity_rows(config, market, metadata, fills, funding_details):
    rows = []
    initial = config.initial_spot_usdt + config.initial_perp_usdt
    for point in market:
        spot_cashflow = Decimal("0")
        spot_base = Decimal("0")
        perp_cashflow = Decimal("0")
        perp_base = Decimal("0")
        spot_fees = Decimal("0")
        perp_fees = Decimal("0")
        for fill in fills:
            if fill["ts"] > point.ts:
                continue
            buy = fill["side"].endswith("BUY")
            if "SIM_SPOT" in fill["instrument"]:
                spot_fees += fill["commission"]
                spot_cashflow += (-1 if buy else 1) * fill["quantity"] * fill["price"]
                spot_base += (1 if buy else -1) * fill["quantity"]
            else:
                perp_fees += fill["commission"]
                base_qty = fill["quantity"] * metadata.contract_multiplier
                perp_cashflow += (-1 if buy else 1) * base_qty * fill["price"]
                perp_base += (1 if buy else -1) * base_qty
        funding = sum((row["native_amount_usdt"] for row in funding_details
                       if row["settlement_ts"] <= point.ts), Decimal("0"))
        spot_mark = spot_base * (point.spot_bid if spot_base >= 0 else point.spot_ask)
        perp_mark = perp_base * (point.perp_bid if perp_base >= 0 else point.perp_ask)
        perp_total_pnl = perp_cashflow + perp_mark
        perp_unrealized = perp_total_pnl if perp_base != 0 else Decimal("0")
        perp_realized = perp_total_pnl - perp_unrealized
        spot_cash = config.initial_spot_usdt + spot_cashflow - spot_fees
        perp_balance = (
            config.initial_perp_usdt + perp_realized + funding - perp_fees
        )
        nav = (spot_cash + spot_mark + perp_balance + perp_unrealized).quantize(
            EIGHT_PLACES,
        )
        rows.append({
            "ts": point.ts,
            "spot_cash_usdt": spot_cash.quantize(EIGHT_PLACES),
            "spot_base_quantity": spot_base,
            "spot_base_value_usdt": spot_mark.quantize(EIGHT_PLACES),
            "perp_margin_balance_usdt": perp_balance.quantize(EIGHT_PLACES),
            "perp_base_quantity": perp_base,
            "perp_unrealized_pnl_usdt": perp_unrealized.quantize(EIGHT_PLACES),
            "nav_usdt": nav,
        })
    peak = initial
    max_drawdown = Decimal("0")
    for row in rows:
        peak = max(peak, row["nav_usdt"])
        max_drawdown = max(max_drawdown, peak - row["nav_usdt"])
        row["drawdown_usdt"] = (peak - row["nav_usdt"]).quantize(EIGHT_PLACES)
        row["drawdown_rate"] = ((peak - row["nav_usdt"]) / peak).quantize(EIGHT_PLACES)
    return rows, max_drawdown.quantize(EIGHT_PLACES)


def _margin_pressure(account) -> tuple[Decimal, Decimal]:
    max_maintenance = Decimal("0")
    min_free = None
    for event in account.events:
        maintenance = sum(
            (margin.maintenance.as_decimal() for margin in event.margins),
            Decimal("0"),
        )
        max_maintenance = max(max_maintenance, maintenance)
        free = event.balances[0].free.as_decimal()
        min_free = free if min_free is None else min(min_free, free)
    return max_maintenance, min_free or Decimal("0")


def run_backtest(
    config: BacktestConfig,
    data: BacktestData,
    output_dir: Path | str,
    predictions: dict[int, Decimal] | None = None,
) -> dict:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    metadata = data.metadata
    market = tuple(row for row in execution_points(config, data)
                   if config.start_ns <= row.ts <= config.end_ns)
    funding = tuple(row for row in data.funding
                    if config.start_ns <= row.settlement_ts <= config.end_ns)
    spot_qty, perp_contracts = position_quantities(config, metadata)
    if spot_qty <= 0 or perp_contracts <= 0:
        raise ValueError("target quantity rounds to zero")
    first_after_start = next(iter(market), None)
    if first_after_start is None:
        raise ValueError("no market data inside the requested interval")
    if spot_qty * first_after_start.spot_ask * (1 + config.spot_taker_fee) > config.initial_spot_usdt:
        raise ValueError("initial_spot_usdt cannot fund the requested spot quantity")

    spot, perp = _instruments(config, metadata)
    engine = BacktestEngine(BacktestEngineConfig(
        run_analysis=False,
        logging=LoggerConfig(stdout_level=LogLevel.ERROR),
    ))
    try:
        engine.add_venue(
            venue=spot.id.venue,
            oms_type=OmsType.NETTING,
            account_type=AccountType.CASH,
            base_currency=None,
            starting_balances=[Money(config.initial_spot_usdt, USDT)],
        )
        engine.add_venue(
            venue=perp.id.venue,
            oms_type=OmsType.NETTING,
            account_type=AccountType.MARGIN,
            base_currency=USDT,
            starting_balances=[Money(config.initial_perp_usdt, USDT)],
        )
        engine.add_instrument(spot)
        engine.add_instrument(perp)
        depth = Decimal("1000000")
        settlement_timestamps = {
            row.settlement_ts for row in funding if row.mark_price is not None
        }
        spot_quotes = [QuoteTick(
            spot.id,
            spot.make_price(row.spot_bid),
            spot.make_price(row.spot_ask),
            spot.make_qty(depth),
            spot.make_qty(depth),
            row.ts,
            row.ts + 1 if row.ts in settlement_timestamps else row.ts,
        ) for row in market]
        perp_quotes = [QuoteTick(
            perp.id,
            perp.make_price(row.perp_bid),
            perp.make_price(row.perp_ask),
            perp.make_qty(depth),
            perp.make_qty(depth),
            row.ts,
            row.ts + 1 if row.ts in settlement_timestamps else row.ts,
        ) for row in market]
        engine.add_data(spot_quotes)
        engine.add_data(perp_quotes)
        marks = {row.ts: row.mark_price for row in market}
        marks.update({row.settlement_ts: row.mark_price for row in funding
                      if row.mark_price is not None})
        engine.add_data([MarkPriceUpdate(
            perp.id, Price.from_str(format(price.normalize(), "f")), timestamp, timestamp,
        ) for timestamp, price in sorted(marks.items())])
        precise_funding = tuple(row for row in funding if row.mark_price is not None)
        funding_updates = [FundingRateUpdate(
            perp.id,
            row.realized_rate.normalize(),
            row.settlement_ts,
            row.settlement_ts,
            interval=(int(row.interval_hours * 60) if row.interval_hours is not None else None),
            next_funding_ns=row.settlement_ts,
        ) for row in precise_funding]
        if funding_updates:
            engine.add_data(funding_updates)
        feature_history = merge_funding_observations(data.funding_history, data.funding)
        strategy = CarryStrategy().configure(
            config, spot, perp, spot_qty, perp_contracts, feature_history, predictions,
        )
        engine.add_strategy(strategy)
        engine.run()

        fills = strategy.fills
        if strategy.entered and not strategy.exited:
            raise RuntimeError(f"no executable quote at fixed expiry {strategy.scheduled_exit_ts}")
        if strategy.entered and (len(fills) != 4 or engine.cache.positions_open()):
            raise RuntimeError(
                f"two-leg backtest did not complete four fills and close: fills={len(fills)}",
            )
        spot_account = engine.cache.account_for_venue(spot.id.venue)
        perp_account = engine.cache.account_for_venue(perp.id.venue)
        funding_details = _native_funding_details(
            perp_account, precise_funding, fills, metadata.contract_multiplier,
        )
        fee_total = sum((row["commission"] for row in fills), Decimal("0"))
        funding_total = sum(
            (row["native_amount_usdt"] for row in funding_details), Decimal("0"),
        )
        spot_gross = sum((
            (-1 if row["side"].endswith("BUY") else 1) * row["quantity"] * row["price"]
            for row in fills if "SIM_SPOT" in row["instrument"]
        ), Decimal("0"))
        perp_gross = sum((
            (-1 if row["side"].endswith("BUY") else 1)
            * row["quantity"] * metadata.contract_multiplier * row["price"]
            for row in fills if "PERP" in row["instrument"]
        ), Decimal("0"))
        perp_base_quantity = perp_contracts * metadata.contract_multiplier
        hedged_base = min(spot_qty, perp_base_quantity)
        basis_pnl = (
            spot_gross * hedged_base / spot_qty
            + perp_gross * hedged_base / perp_base_quantity
        ).quantize(EIGHT_PLACES)
        two_leg_price_pnl = (spot_gross + perp_gross).quantize(EIGHT_PLACES)
        residual_directional_pnl = (two_leg_price_pnl - basis_pnl).quantize(
            EIGHT_PLACES,
        )
        initial_nav = config.initial_spot_usdt + config.initial_perp_usdt
        final_nav = (
            spot_account.balance_total(USDT).as_decimal()
            + perp_account.balance_total(USDT).as_decimal()
        ).quantize(EIGHT_PLACES)
        reconciled_pnl = (spot_gross + perp_gross + funding_total - fee_total).quantize(
            EIGHT_PLACES,
        )
        reconciled_nav = (initial_nav + reconciled_pnl).quantize(EIGHT_PLACES)
        if final_nav != reconciled_nav:
            raise RuntimeError(f"native NAV does not reconcile: {final_nav} != {reconciled_nav}")
        equity, max_drawdown = _equity_rows(
            config, market, metadata, fills, funding_details,
        )
        max_maintenance, min_perp_free = _margin_pressure(perp_account)
        residual = spot_qty - perp_contracts * metadata.contract_multiplier
        residual_nav = (residual * first_after_start.spot_bid / initial_nav).quantize(
            EIGHT_PLACES,
        )
        no_trade = not fills
        status = "no_trade" if no_trade else "completed"
        no_trade_reason = strategy.no_trade_reason if no_trade else None
        unverified = [
            "usd_anchor_missing",
            "exchange_margin_and_liquidation_rules",
            "capacity_without_orderbook",
        ]
        if any(row.mark_price is None for row in funding):
            unverified.append("precise_funding_missing_settlement_mark")

        artifacts = {
            "summary": str(output_dir / "summary.json"),
            "fills": str(output_dir / "fills.jsonl"),
            "funding": str(output_dir / "funding.jsonl"),
            "equity": str(output_dir / "equity.jsonl"),
        }
        report = {
            "schema_version": "1",
            "config": config.as_json(),
            "data": {
                "data_version": config.data_version,
                "spot_base_currency": str(spot.base_currency),
                "perp_base_currency": str(perp.base_currency),
                "market_points": len(market),
                "funding_settlements": len(funding),
                "contract_multiplier": str(metadata.contract_multiplier),
                "spot_size_increment": str(metadata.spot_size_increment),
                "perp_contract_increment": str(metadata.perp_contract_increment),
            },
            "assumptions": {
                "account_structure": "isolated_simulation_ledgers",
                "account_structure_scope": "offline assumption; not verified exchange account structure",
                "execution": "native market fills against supplied bid/ask",
                "funding_settlement": "native at settlement_ts using exact mark when present",
                "settlement_tie_break": "same-ts quotes replay 1ns after funding without changing event_ts",
                "minute_bar_signal": "closed available bar; entry on next shared price record",
                "holding_horizon": "single entry; signal_ts + H expiry requires an exact shared quote",
                "run_interval": "quotes, fills and settlements restricted to [start_ns, end_ns]",
                "model_prediction": "M1 exact decision timestamp OOS net return over H, including costs; no carry-forward",
            },
            "summary": {
                "status": status,
                "no_trade_reason": no_trade_reason,
                "initial_nav_usdt": str(initial_nav.quantize(EIGHT_PLACES)),
                "final_nav_usdt": str(final_nav),
                "reconciled_nav_usdt": str(reconciled_nav),
                "net_pnl_usdt": str((final_nav - initial_nav).quantize(EIGHT_PLACES)),
                "reconciled_net_pnl_usdt": str(reconciled_pnl),
                "return_on_total_capital": str(
                    (final_nav - initial_nav) / initial_nav,
                ),
                "max_drawdown_usdt": str(max_drawdown),
                "max_drawdown_rate": str(max(row["drawdown_rate"] for row in equity)),
                "turnover_usdt": str(sum((
                    row["quantity"] * row["price"]
                    * (metadata.contract_multiplier if "PERP" in row["instrument"] else 1)
                    for row in fills
                ), Decimal("0")).quantize(EIGHT_PLACES)),
                "max_capital_used_usdt": str(initial_nav.quantize(EIGHT_PLACES)),
                "max_native_maintenance_margin_usdt": str(
                    max_maintenance.quantize(EIGHT_PLACES),
                ),
                "min_native_perp_free_balance_usdt": str(
                    min_perp_free.quantize(EIGHT_PLACES),
                ),
                "spot_quantity": str(spot_qty),
                "perp_contracts": str(perp_contracts),
                "residual_delta_base": str(residual),
                "residual_delta_nav": str(residual_nav),
                "funding_usdt": str(funding_total.quantize(EIGHT_PLACES)),
                "fees_usdt": str(fee_total.quantize(EIGHT_PLACES)),
                "two_leg_price_pnl_usdt": str(two_leg_price_pnl),
                "basis_pnl_usdt": str(basis_pnl),
                "residual_directional_pnl_usdt": str(residual_directional_pnl),
                "fill_count": len(fills),
                "entry_signal_ts": next((row["ts"] for row in strategy.decisions
                                         if row["action"] == "enter"), None),
                "entry_fill_ts": strategy.entry_fill_ts,
                "exit_fill_ts": strategy.exit_fill_ts,
                "actual_funding_intervals_hours": [
                    (str(row["interval_hours"]) if row["interval_hours"] is not None else None)
                    for row in funding_details
                ],
                "funding_settlement_status": (
                    "unverified_missing_mark"
                    if any(row.mark_price is None for row in funding)
                    else "exact_native"
                ),
                "additional_slippage_charge_usdt": "0",
                "usd_nav": None,
            },
            "decisions": strategy.decisions,
            "artifacts": artifacts,
            "unverified": unverified,
        }
        _write_jsonl(output_dir / "fills.jsonl", fills)
        _write_jsonl(output_dir / "funding.jsonl", funding_details)
        _write_jsonl(output_dir / "equity.jsonl", equity)
        (output_dir / "summary.json").write_text(
            json.dumps(_jsonable(report), ensure_ascii=False, indent=2), encoding="utf-8",
        )
        return _jsonable(report)
    finally:
        engine.dispose()


def _jsonable(value):
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def _write_jsonl(path: Path, rows: Iterable[Mapping]) -> None:
    path.write_text(
        "".join(json.dumps(_jsonable(row), ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )


def _config_from_json(values: Mapping) -> BacktestConfig:
    decimal_fields = {
        "initial_spot_usdt", "initial_perp_usdt", "target_spot_base",
        "spot_taker_fee", "perp_taker_fee", "execution_bps_per_leg", "buffer_usdt",
        "future_basis_change_prediction",
    }
    normalized = {
        key: Decimal(str(value)) if key in decimal_fields else value
        for key, value in values.items()
    }
    return BacktestConfig(**normalized)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run native B0/B1 carry backtest")
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--config-json", required=True,
                        help="JSON object or path to a JSON file")
    args = parser.parse_args()
    candidate = Path(args.config_json)
    raw = candidate.read_text(encoding="utf-8") if candidate.is_file() else args.config_json
    result = run_backtest(
        _config_from_json(json.loads(raw)),
        BacktestData.from_parquet(args.data_dir),
        args.output_dir,
    )
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
