"""Offline capability probe, not application code; synthetic data, no exchange connections.

Run from the project root:
    uv run --no-project --python 3.12 --with nautilus_trader==1.231.0 python checks/nautilus_v1.py
"""
from decimal import Decimal
import inspect
import json

import nautilus_trader
from nautilus_trader.backtest.engine import BacktestEngine
from nautilus_trader.backtest.modules import SimulationModule
from nautilus_trader.config import BacktestEngineConfig, LoggingConfig, SimulationModuleConfig
from nautilus_trader.model.currencies import USDT
from nautilus_trader.model.data import FundingRateUpdate, MarkPriceUpdate, QuoteTick
from nautilus_trader.model.enums import AccountType, OmsType, OrderSide
from nautilus_trader.model.objects import Money
from nautilus_trader.test_kit.providers import TestInstrumentProvider
from nautilus_trader.trading.strategy import Strategy


INSTRUMENT = TestInstrumentProvider.btcusdt_perp_binance()
SETTLEMENT = 1_704_096_000_000_000_000  # 2024-01-01 08:00 UTC
SECOND = 1_000_000_000


class ShortOnce(Strategy):
    def __init__(self):
        super().__init__()
        self.submitted = False
        self.funding_seen = 0

    def on_start(self):
        self.subscribe_quote_ticks(INSTRUMENT.id)
        self.subscribe_funding_rates(INSTRUMENT.id)

    def on_quote_tick(self, tick):
        if not self.submitted:
            self.submitted = True
            self.submit_order(self.order_factory.market(
                instrument_id=INSTRUMENT.id,
                order_side=OrderSide.SELL,
                quantity=INSTRUMENT.make_qty(0.1),
            ))

    def on_funding_rate(self, funding):
        self.funding_seen += 1


class AdjustmentProbe(SimulationModule):
    """Checks only the native balance extension point, not a funding implementation."""
    def __init__(self):
        super().__init__(SimulationModuleConfig())
        self.applied = False

    def process(self, ts_now):
        if ts_now >= SETTLEMENT and not self.applied:
            self.exchange.adjust_account(Money(Decimal('0.5'), USDT))
            self.applied = True

    def log_diagnostics(self, logger):
        pass

    def reset(self):
        self.applied = False


def run(rate, extension=False):
    engine = BacktestEngine(BacktestEngineConfig(logging=LoggingConfig(bypass_logging=True)))
    try:
        engine.add_venue(
            venue=INSTRUMENT.id.venue, oms_type=OmsType.NETTING,
            account_type=AccountType.MARGIN, base_currency=USDT,
            starting_balances=[Money(10_000, USDT)],
            modules=[AdjustmentProbe()] if extension else [],
        )
        engine.add_instrument(INSTRUMENT)
        price = INSTRUMENT.make_price(50_000)
        quotes = [QuoteTick(
            INSTRUMENT.id, price, price, INSTRUMENT.make_qty(1),
            INSTRUMENT.make_qty(1), ts, ts,
        ) for ts in (SETTLEMENT - 2 * SECOND, SETTLEMENT - SECOND, SETTLEMENT + SECOND)]
        engine.add_data(quotes)
        engine.add_data([MarkPriceUpdate(INSTRUMENT.id, price, q.ts_event, q.ts_init) for q in quotes])
        engine.add_data([FundingRateUpdate(INSTRUMENT.id, Decimal(rate), SETTLEMENT,
                                          SETTLEMENT, interval=480)])
        strategy = ShortOnce()
        engine.add_strategy(strategy)
        engine.run()
        positions = engine.cache.positions_open()
        assert len(positions) == 1 and positions[0].is_short
        assert positions[0].quantity.as_decimal() == Decimal('0.1')
        assert strategy.funding_seen == 1
        balance = engine.cache.account_for_venue(INSTRUMENT.id.venue).balance_total(USDT).as_decimal()
        return balance
    finally:
        engine.dispose()


if __name__ == '__main__':
    assert nautilus_trader.__version__ == '1.231.0'
    baseline = run('0')
    positive = run('0.0001')
    extended = run('0.0001', extension=True)
    assert positive - baseline == 0, 'Re-evaluate v1 funding settlement capability'
    assert extended - baseline == Decimal('0.5')
    result = {
        'version': nautilus_trader.__version__,
        'scope': 'legacy Python/Cython BacktestEngine; offline synthetic data',
        'short_quantity_btc': '0.1', 'mark_price_usdt': '50000',
        'positive_funding_rate': '0.0001', 'funding_callbacks_each_run': 1,
        'baseline_balance': str(baseline), 'positive_rate_balance': str(positive),
        'expected_funding_cashflow': '0.5', 'observed_native_funding_cashflow': str(positive-baseline),
        'native_extension_balance_delta': str(extended-baseline),
        'liquidation_enabled_argument': 'liquidation_enabled' in inspect.signature(BacktestEngine.add_venue).parameters,
    }
    print(json.dumps(result, indent=2))
