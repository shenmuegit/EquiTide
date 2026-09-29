"""Native rc5 capability probes. These are offline fixtures, not live acceptance.

Run: uv run --locked python checks/execution.py
"""
from decimal import Decimal
import json
from pathlib import Path

import nautilus_trader
from nautilus_trader.adapters.sandbox import (
    SandboxExecutionClientConfig,
    SandboxExecutionClientFactory,
)
from nautilus_trader.backtest import BacktestEngine
from nautilus_trader.common import Environment, LoggerConfig
from nautilus_trader.config import BacktestEngineConfig
from nautilus_trader.execution import LimitOrderPartialFillModel
from nautilus_trader.live import LiveNode
from nautilus_trader.model import (
    AccountId, AccountType, Currency, Money, OmsType, OrderSide, QuoteTick,
    TraderId, Venue,
)
from nautilus_trader.testkit.providers import TestInstrumentProvider
from nautilus_trader.trading import Strategy


USDT = Currency.from_str("USDT")
START = 1_704_067_200_000_000_000
SECOND = 1_000_000_000


def sandbox_registration(venue_name: str, count: int) -> str | None:
    """No connections or real execution clients are used."""
    builder = LiveNode.builder("routing-check", TraderId("CHECK-001"), Environment.SANDBOX)
    builder = builder.with_logging(LoggerConfig(bypass_logging=True))
    for index in range(count):
        builder = builder.add_simulated_exec_client(
            f"SIM_{index}", SandboxExecutionClientFactory(),
            SandboxExecutionClientConfig(
                venue=Venue(venue_name),
                account_id=AccountId(f"{venue_name}-{index}"),
                starting_balances=[Money(10000, USDT)],
                account_type=AccountType.CASH if index == 0 else AccountType.MARGIN,
            ),
        )
    try:
        node = builder.build()
    except RuntimeError as error:
        return str(error)
    node.dispose()
    return None


def quote(instrument, quantity="1", second=0):
    return QuoteTick(
        instrument.id, instrument.make_price(Decimal("50000")),
        instrument.make_price(Decimal("50000")),
        instrument.make_qty(Decimal(quantity)), instrument.make_qty(Decimal(quantity)),
        START + second * SECOND, START + second * SECOND,
    )


class Probe(Strategy):
    """Observes native events only; no project execution policy is implemented here."""

    def __init__(self):
        super().__init__()

    def configure(self, instruments, *, partial=False, reject_second=False):
        self.instruments = {instrument.id: instrument for instrument in instruments}
        self.partial = partial
        self.reject_second = reject_second
        self.seen = set()
        self.events = []
        self.stopped = False
        return self

    def on_start(self):
        for instrument_id in self.instruments:
            self.subscribe_quotes(instrument_id)

    def on_quote(self, event):
        if event.instrument_id in self.seen:
            return
        self.seen.add(event.instrument_id)
        instrument = self.instruments[event.instrument_id]
        side = OrderSide.SELL if "PERP" in str(instrument.id) else OrderSide.BUY
        if self.partial:
            order = self.order_factory.limit(
                instrument.id, side, instrument.make_qty(Decimal("10")),
                instrument.make_price(Decimal("50000")),
            )
        elif self.reject_second and side == OrderSide.SELL:
            # A reduce-only short with no position is rejected natively.
            order = self.order_factory.market(
                instrument.id, side, instrument.make_qty(Decimal("0.1")), reduce_only=True,
            )
        else:
            order = self.order_factory.market(
                instrument.id, side, instrument.make_qty(Decimal("0.1")),
            )
        self.submit_order(order)

    def on_order_filled(self, event):
        self.events.append({
            "type": "filled", "instrument": str(event.instrument_id),
            "quantity": str(event.last_qty.as_decimal()),
            "side": str(event.order_side), "commission": str(event.commission),
            "order_status": str(self.cache.order(event.client_order_id).status),
        })

    def on_order_rejected(self, event):
        self.events.append({"type": "rejected", "instrument": str(event.instrument_id),
                            "reason": str(event.reason)})

    def on_order_denied(self, event):
        self.events.append({"type": "denied", "instrument": str(event.instrument_id),
                            "reason": str(event.reason)})

    def on_stop(self):
        # Observing stop does not manufacture a liquidation or account reset.
        self.stopped = True


def run_fixture(account_type, *, partial=False, reject_second=False):
    spot = TestInstrumentProvider.btcusdt_binance()
    perp = TestInstrumentProvider.btcusdt_perp_binance()
    instruments = [spot] if partial else [spot, perp]
    engine = BacktestEngine(BacktestEngineConfig(
        run_analysis=False, logging=LoggerConfig(bypass_logging=True),
    ))
    try:
        engine.add_venue(
            venue=spot.id.venue, oms_type=OmsType.NETTING, account_type=account_type,
            starting_balances=[Money(1000000 if partial else 20000, USDT)], base_currency=None,
            fill_model=LimitOrderPartialFillModel(1.0, 0.0, 1) if partial else None,
        )
        for instrument in instruments:
            engine.add_instrument(instrument)
            engine.add_data([quote(instrument)])
        strategy = Probe().configure(instruments, partial=partial, reject_second=reject_second)
        engine.add_strategy(strategy)
        engine.run()
        account = engine.cache.account_for_venue(spot.id.venue)
        return {
            "account_type": str(account_type),
            "initial_usdt": "1000000" if partial else "20000",
            "quote_price_usdt": "50000",
            "fill_model": "LimitOrderPartialFillModel" if partial else "native default",
            "balances": {str(currency): str(money.as_decimal())
                         for currency, money in account.balances_total().items()},
            "events": strategy.events,
            "positions": [{"instrument": str(position.instrument_id),
                           "signed_quantity": str(position.signed_qty)}
                          for position in engine.cache.positions_open()],
            "orders": [{"instrument": str(order.instrument_id), "status": str(order.status),
                        "quantity": str(order.quantity), "filled_quantity": str(order.filled_qty)}
                       for order in engine.cache.orders()],
            "stop_callback_seen": strategy.stopped,
        }
    finally:
        engine.dispose()


def main():
    assert nautilus_trader.__version__ == "2.0.0rc5"
    routing = {}
    for venue in ("BINANCE", "OKX"):
        assert sandbox_registration(venue, 1) is None
        error = sandbox_registration(venue, 2)
        assert f"Venue {venue} already routed to SIM_" in error
        assert "cannot register SIM_" in error and "for the same venue" in error
        routing[venue] = {"single_sandbox_build": True, "dual_sandbox_error": error}
    margin = run_fixture(AccountType.MARGIN)
    assert margin["balances"] == {"USDT": "19994.10000000"}
    assert len(margin["positions"]) == 2
    assert "BTC" not in margin["balances"]  # This is not cash spot inventory.
    try:
        run_fixture(AccountType.CASH)
    except RuntimeError as error:
        cash_error = str(error)
        assert "Cash account cannot trade futures or perpetuals" in cash_error
    else:
        raise AssertionError("Cash account unexpectedly accepted a perpetual")
    partial = run_fixture(AccountType.CASH, partial=True)
    assert [Decimal(row["quantity"]) for row in partial["events"]] == [5, 5]
    assert partial["events"][0]["order_status"] == "PARTIALLY_FILLED"
    assert partial["orders"][0]["status"] == "FILLED"
    assert Decimal(partial["orders"][0]["quantity"]) == 10
    assert Decimal(partial["balances"]["BTC"]) == 10
    rejected = run_fixture(AccountType.MARGIN, reject_second=True)
    assert any(row["type"] == "rejected" and row["instrument"] == "BTCUSDT-PERP.BINANCE"
               and "Reduce-only" in row["reason"] for row in rejected["events"])
    assert rejected["positions"] == [{"instrument": "BTCUSDT.BINANCE", "signed_quantity": "0.1"}]
    assert rejected["balances"] == {"USDT": "19995.00000000"}
    assert rejected["stop_callback_seen"] and rejected["positions"]
    result = {
        "version": nautilus_trader.__version__,
        "scope": "offline native capabilities; no project execution policy or live acceptance",
        "routing": routing,
        "one_margin_account": margin,
        "one_cash_account_error": cash_error,
        "partial_fill": partial,
        "one_leg_rejected_and_stop": rejected,
        "live_trading_ready": False,
        "unverified": [
            "cash spot plus perpetual in one live node",
            "project hedging after partial fills or rejected orders",
            "data interruption and reconnection with existing exposure",
            "exchange account margin, liquidation, ADL and private bills",
        ],
    }
    output = Path("data/execution/native_rc5.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
