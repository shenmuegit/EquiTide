from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal
from statistics import median

from nautilus_trader.model import OrderSide
from nautilus_trader.trading import Strategy


NANOS_PER_HOUR = Decimal(3_600_000_000_000)


def _finite_decimal(name: str, value) -> Decimal:
    if not isinstance(value, Decimal) or not value.is_finite():
        raise ValueError(f"{name} must be a finite Decimal")
    return value


def _integer(name: str, value) -> int:
    if type(value) is not int:  # bool is intentionally rejected.
        raise ValueError(f"{name} must be an integer")
    return value


@dataclass(frozen=True)
class FundingObservation:
    settlement_ts: int
    available_ts: int
    realized_rate: Decimal
    interval_hours: Decimal

    def __post_init__(self) -> None:
        _integer("settlement_ts", self.settlement_ts)
        _integer("available_ts", self.available_ts)
        _finite_decimal("realized_rate", self.realized_rate)
        _finite_decimal("interval_hours", self.interval_hours)
        if self.interval_hours <= 0:
            raise ValueError("funding interval_hours must be positive")
        if self.available_ts < self.settlement_ts:
            raise ValueError("funding available_ts cannot precede settlement_ts")


@dataclass(frozen=True)
class BacktestConfig:
    baseline: str
    data_version: str
    exchange: str
    base_asset: str
    start_ns: int
    end_ns: int
    decision_interval_ns: int
    holding_period_ns: int
    funding_window: int
    initial_spot_usdt: Decimal
    initial_perp_usdt: Decimal
    target_spot_base: Decimal
    spot_taker_fee: Decimal
    perp_taker_fee: Decimal
    execution_bps_per_leg: Decimal
    buffer_usdt: Decimal
    future_basis_change_prediction: Decimal = Decimal("0")

    def __post_init__(self) -> None:
        for name in (
            "start_ns", "end_ns", "decision_interval_ns", "holding_period_ns",
            "funding_window",
        ):
            _integer(name, getattr(self, name))
        for name in (
            "initial_spot_usdt", "initial_perp_usdt", "target_spot_base",
            "spot_taker_fee", "perp_taker_fee", "execution_bps_per_leg",
            "buffer_usdt", "future_basis_change_prediction",
        ):
            _finite_decimal(name, getattr(self, name))
        if self.baseline not in {"B0", "B1", "M1"}:
            raise ValueError("baseline must be B0, B1 or M1")
        if not all(isinstance(value, str) and value.strip() for value in (
            self.data_version, self.exchange, self.base_asset,
        )):
            raise ValueError("data_version, exchange and base_asset are required")
        if self.base_asset not in {"BTC", "ETH"}:
            raise ValueError("base_asset must be BTC or ETH")
        if self.start_ns < 0:
            raise ValueError("start_ns cannot be negative")
        if self.start_ns >= self.end_ns:
            raise ValueError("start_ns must be before end_ns")
        if self.decision_interval_ns <= 0 or self.holding_period_ns <= 0:
            raise ValueError("decision interval and holding period must be positive")
        if self.funding_window != 21:
            raise ValueError("B1 funding_window is fixed at 21 settlements")
        if min(self.initial_spot_usdt, self.initial_perp_usdt, self.target_spot_base) <= 0:
            raise ValueError("capital and target_spot_base must be positive")
        if min(self.spot_taker_fee, self.perp_taker_fee,
               self.execution_bps_per_leg, self.buffer_usdt) < 0:
            raise ValueError("fees, execution cost and buffer cannot be negative")
        if self.spot_taker_fee >= 1 or self.perp_taker_fee >= 1:
            raise ValueError("taker fee rates must be less than one")
        if self.execution_bps_per_leg >= 10_000:
            raise ValueError("execution_bps_per_leg must be less than 10000")
        if self.future_basis_change_prediction != 0:
            raise ValueError("B1 fixes future basis change prediction at zero")

    def as_json(self) -> dict[str, str | int]:
        return {
            key: str(value) if isinstance(value, Decimal) else value
            for key, value in asdict(self).items()
        }


def b1_hourly_rate(
    observations: tuple[FundingObservation, ...],
    decision_ts: int,
    window: int,
) -> Decimal | None:
    available = sorted(
        (row for row in observations if row.available_ts <= decision_ts),
        key=lambda row: (row.settlement_ts, row.available_ts),
    )
    if len(available) < window:
        return None
    return median([row.realized_rate / row.interval_hours for row in available[-window:]])


class CarryStrategy(Strategy):
    """Shared carry rules; orders and fills stay native to Nautilus."""

    def __init__(self) -> None:
        super().__init__()

    def configure(
        self,
        config: BacktestConfig,
        spot,
        perp,
        spot_quantity: Decimal,
        perp_contracts: Decimal,
        funding_history: tuple[FundingObservation, ...],
        predictions: dict[int, Decimal] | None = None,
    ) -> "CarryStrategy":
        self.settings = config
        self.spot = spot
        self.perp = perp
        self.spot_quantity = spot_quantity
        self.perp_contracts = perp_contracts
        self.funding_history = funding_history
        self.predictions = dict(predictions or {})
        for timestamp, value in self.predictions.items():
            _integer("prediction timestamp", timestamp)
            _finite_decimal("predicted net return", value)
        self.latest_quotes = {}
        self.last_pair_ts = None
        self.pending_entry_ts = None
        self.pending_exit_ts = None
        self.entry_fill_ts = None
        self.exit_fill_ts = None
        self.scheduled_exit_ts = None
        self.next_decision_ts = config.start_ns
        self.entered = False
        self.exited = False
        self.no_trade_reason = None
        self.decisions: list[dict] = []
        self.fills: list[dict] = []
        return self

    def on_start(self) -> None:
        self.subscribe_quotes(self.spot.id)
        self.subscribe_quotes(self.perp.id)
        self.subscribe_funding_rates(self.perp.id)

    def on_quote(self, quote) -> None:
        self.latest_quotes[quote.instrument_id] = quote
        if self.spot.id not in self.latest_quotes or self.perp.id not in self.latest_quotes:
            return
        spot_quote = self.latest_quotes[self.spot.id]
        perp_quote = self.latest_quotes[self.perp.id]
        if spot_quote.ts_event != perp_quote.ts_event:
            return
        timestamp = spot_quote.ts_event
        if timestamp == self.last_pair_ts:
            return
        self.last_pair_ts = timestamp

        if timestamp < self.settings.start_ns or timestamp > self.settings.end_ns:
            return
        if self.pending_entry_ts is not None and timestamp > self.pending_entry_ts:
            if timestamp >= self.scheduled_exit_ts:
                self.pending_entry_ts = None
                self.no_trade_reason = "no_execution_before_expiry"
                return
            self._enter(timestamp)

        if self.entered and not self.exited:
            if self.scheduled_exit_ts is not None and timestamp >= self.scheduled_exit_ts:
                if timestamp == self.scheduled_exit_ts:
                    self._exit(timestamp)
                return
            if self.pending_exit_ts is not None and timestamp > self.pending_exit_ts:
                self._exit(timestamp)
                return

        if timestamp < self.next_decision_ts:
            return
        self.next_decision_ts = timestamp + self.settings.decision_interval_ns
        self._decide(timestamp, spot_quote, perp_quote)

    def _decide(self, timestamp, spot_quote, perp_quote) -> None:
        if self.exited:
            return
        if not self.entered and timestamp + self.settings.holding_period_ns > self.settings.end_ns:
            self.no_trade_reason = self.no_trade_reason or "insufficient_holding_horizon"
            self.decisions.append({"ts": timestamp, "action": "skip", "reason": "insufficient_holding_horizon"})
            return
        if self.settings.baseline == "B0":
            if not self.entered and self.pending_entry_ts is None:
                self.pending_entry_ts = timestamp
                self.scheduled_exit_ts = timestamp + self.settings.holding_period_ns
                self.decisions.append({"ts": timestamp, "action": "enter", "reason": "fixed_hold"})
            return

        if self.settings.baseline == "M1":
            if self.entered or self.pending_entry_ts is not None:
                return
            prediction = self.predictions.get(timestamp)
            if prediction is None:
                self.no_trade_reason = "missing_prediction"
                self.decisions.append({"ts": timestamp, "action": "skip", "reason": self.no_trade_reason})
                return
            predicted_net = prediction * (self.settings.initial_spot_usdt + self.settings.initial_perp_usdt)
            action = "enter" if predicted_net > self.settings.buffer_usdt else "skip"
            self.decisions.append({"ts": timestamp, "action": action,
                                   "predicted_net_return": str(prediction),
                                   "predicted_net_usdt": str(predicted_net),
                                   "buffer_usdt": str(self.settings.buffer_usdt)})
            if action == "enter":
                self.pending_entry_ts = timestamp
                self.scheduled_exit_ts = timestamp + self.settings.holding_period_ns
            else:
                self.no_trade_reason = "expected_net_not_above_buffer"
            return

        hourly_rate = b1_hourly_rate(
            self.funding_history, timestamp, self.settings.funding_window,
        )
        if hourly_rate is None:
            if not self.entered:
                self.no_trade_reason = "insufficient_funding_history"
                self.decisions.append({"ts": timestamp, "action": "skip", "reason": self.no_trade_reason})
            return

        spot_bid = spot_quote.bid_price.as_decimal()
        spot_ask = spot_quote.ask_price.as_decimal()
        perp_bid = perp_quote.bid_price.as_decimal()
        perp_ask = perp_quote.ask_price.as_decimal()
        spot_mid = (spot_bid + spot_ask) / 2
        perp_mid = (perp_bid + perp_ask) / 2
        perp_base = self.perp_contracts * self.perp.multiplier.as_decimal()
        spot_notional = self.spot_quantity * spot_mid
        perp_notional = perp_base * perp_mid
        if not self.entered and self.pending_entry_ts is None:
            horizon_hours = Decimal(self.settings.holding_period_ns) / NANOS_PER_HOUR
            expected_funding = perp_notional * hourly_rate * horizon_hours
            round_trip_cost = (
                2 * spot_notional * self.settings.spot_taker_fee
                + 2 * perp_notional * self.settings.perp_taker_fee
                + self.spot_quantity * (spot_ask - spot_bid)
                + perp_base * (perp_ask - perp_bid)
            )
            expected_net = expected_funding - round_trip_cost
            action = "enter" if expected_net > self.settings.buffer_usdt else "skip"
            self.decisions.append({
                "ts": timestamp,
                "action": action,
                "hourly_rate": str(hourly_rate),
                "expected_funding_usdt": str(expected_funding),
                "future_cost_usdt": str(round_trip_cost),
                "buffer_usdt": str(self.settings.buffer_usdt),
            })
            if action == "enter":
                self.pending_entry_ts = timestamp
                self.scheduled_exit_ts = timestamp + self.settings.holding_period_ns
            else:
                self.no_trade_reason = "expected_net_not_above_buffer"
            return

        if self.entered and timestamp < self.scheduled_exit_ts:
            remaining_hours = Decimal(self.scheduled_exit_ts - timestamp) / NANOS_PER_HOUR
            expected_increment = perp_notional * hourly_rate * remaining_hours
            future_exit_cost = (
                spot_notional * self.settings.spot_taker_fee
                + perp_notional * self.settings.perp_taker_fee
                + self.spot_quantity * (spot_mid - spot_bid)
                + perp_base * (perp_ask - perp_mid)
            )
            hold = expected_increment - future_exit_cost > self.settings.buffer_usdt
            self.decisions.append({
                "ts": timestamp,
                "action": "hold" if hold else "exit",
                "hourly_rate": str(hourly_rate),
                "expected_increment_usdt": str(expected_increment),
                "future_exit_cost_usdt": str(future_exit_cost),
                "entry_cost_reapplied": False,
            })
            if not hold:
                self.pending_exit_ts = timestamp

    def _enter(self, timestamp: int) -> None:
        self.pending_entry_ts = None
        self.entered = True
        self.entry_fill_ts = timestamp
        self.submit_order(self.order_factory.market(
            self.spot.id, OrderSide.BUY, self.spot.make_qty(self.spot_quantity),
        ))
        self.submit_order(self.order_factory.market(
            self.perp.id, OrderSide.SELL, self.perp.make_qty(self.perp_contracts),
        ))

    def _exit(self, timestamp: int) -> None:
        self.pending_exit_ts = None
        self.exited = True
        self.exit_fill_ts = timestamp
        self.close_all_positions(self.spot.id)
        self.close_all_positions(self.perp.id)

    def on_order_filled(self, event) -> None:
        self.fills.append({
            "ts": event.ts_event,
            "instrument": str(event.instrument_id),
            "side": str(event.order_side),
            "quantity": event.last_qty.as_decimal(),
            "price": event.last_px.as_decimal(),
            "commission": event.commission.as_decimal(),
            "commission_currency": str(event.commission.currency),
        })
