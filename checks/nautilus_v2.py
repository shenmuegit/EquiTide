"""Offline release-candidate probe, not application code; synthetic data, no exchange connections.

Run from the project root:
    uv run --locked python checks/nautilus_v2.py
"""
from decimal import Decimal
import inspect
import json
import nautilus_trader
from nautilus_trader.backtest import BacktestEngine
from nautilus_trader.config import BacktestEngineConfig, LoggerConfig
from nautilus_trader.common import LogLevel
from nautilus_trader.model import AccountType, Currency, FundingRateUpdate, MarkPriceUpdate
from nautilus_trader.model import Money, OmsType, OrderSide, QuoteTick
from nautilus_trader.testkit.providers import TestInstrumentProvider
from nautilus_trader.trading import Strategy

INSTRUMENT = TestInstrumentProvider.btcusdt_perp_binance()
USDT = Currency.from_str('USDT')
SETTLEMENT = 1_704_096_000_000_000_000
SECOND = 1_000_000_000


class ShortOnce(Strategy):
    def __init__(self):
        super().__init__()
        self.submitted = False
        self.funding_seen = 0

    def on_start(self):
        self.subscribe_quotes(INSTRUMENT.id)
        self.subscribe_funding_rates(INSTRUMENT.id)

    def on_quote(self, quote):
        if not self.submitted:
            self.submitted = True
            self.submit_order(self.order_factory.market(
                INSTRUMENT.id, OrderSide.SELL, INSTRUMENT.make_qty(Decimal('0.1')),
            ))

    def on_funding_rate(self, funding):
        self.funding_seen += 1


def run(rate):
    engine = BacktestEngine(BacktestEngineConfig(
        run_analysis=False, logging=LoggerConfig(stdout_level=LogLevel.ERROR),
    ))
    try:
        engine.add_venue(
            venue=INSTRUMENT.id.venue, oms_type=OmsType.NETTING,
            account_type=AccountType.MARGIN, base_currency=USDT,
            starting_balances=[Money(10_000, USDT)],
        )
        engine.add_instrument(INSTRUMENT)
        price = INSTRUMENT.make_price(Decimal('50000'))
        quotes = [QuoteTick(
            INSTRUMENT.id, price, price, INSTRUMENT.make_qty(Decimal('1')),
            INSTRUMENT.make_qty(Decimal('1')), ts, ts,
        ) for ts in (SETTLEMENT - 2 * SECOND, SETTLEMENT - SECOND, SETTLEMENT + SECOND)]
        engine.add_data(quotes)
        engine.add_data([MarkPriceUpdate(INSTRUMENT.id, price, q.ts_event, q.ts_init) for q in quotes])
        # One final rate record at its actual settlement boundary avoids counting
        # a forecast and its realized update as two separate settlement events.
        engine.add_data([FundingRateUpdate(INSTRUMENT.id, Decimal(rate), SETTLEMENT,
                                          SETTLEMENT, interval=480)])
        strategy = ShortOnce()
        engine.add_strategy(strategy)
        engine.run()
        positions = engine.cache.positions_open()
        assert len(positions) == 1 and positions[0].is_short
        assert positions[0].quantity.as_decimal() == Decimal('0.1')
        assert strategy.funding_seen == 1
        return engine.cache.account_for_venue(INSTRUMENT.id.venue).balance_total(USDT).as_decimal()
    finally:
        engine.dispose()


def run_carry(rate: str) -> dict:
    from nautilus_trader.model import CurrencyPair

    spot_values = TestInstrumentProvider.btcusdt_binance().to_dict()
    spot_values['id'] = 'BTCUSDT.SIM_SPOT'
    spot = CurrencyPair.from_dict(spot_values)
    perp = INSTRUMENT
    quantity = Decimal('0.1')
    entry_ts = SETTLEMENT - 2 * SECOND
    exit_ts = SETTLEMENT + SECOND

    class CarryProbe(Strategy):
        def __init__(self):
            super().__init__()
            self.latest = {}
            self.entered = False
            self.exited = False
            self.fills = []

        def on_start(self):
            self.subscribe_quotes(spot.id)
            self.subscribe_quotes(perp.id)

        def on_quote(self, quote):
            self.latest[quote.instrument_id] = quote.ts_event
            if len(self.latest) != 2:
                return
            if not self.entered:
                self.entered = True
                self.submit_order(self.order_factory.market(
                    spot.id, OrderSide.BUY, spot.make_qty(quantity),
                ))
                self.submit_order(self.order_factory.market(
                    perp.id, OrderSide.SELL, perp.make_qty(quantity),
                ))
            elif not self.exited and min(self.latest.values()) >= exit_ts:
                self.exited = True
                self.close_all_positions(spot.id)
                self.close_all_positions(perp.id)

        def on_order_filled(self, event):
            assert event.commission.currency == USDT
            self.fills.append((
                event.instrument_id, event.order_side,
                event.last_qty.as_decimal(), event.last_px.as_decimal(),
                event.commission.as_decimal(),
            ))

    engine = BacktestEngine(BacktestEngineConfig(
        run_analysis=False, logging=LoggerConfig(stdout_level=LogLevel.ERROR),
    ))
    try:
        engine.add_venue(
            venue=spot.id.venue, oms_type=OmsType.NETTING,
            account_type=AccountType.CASH, base_currency=None,
            starting_balances=[Money(10_000, USDT)],
        )
        engine.add_venue(
            venue=perp.id.venue, oms_type=OmsType.NETTING,
            account_type=AccountType.MARGIN, base_currency=USDT,
            starting_balances=[Money(10_000, USDT)],
        )
        for instrument, entry_price, exit_price in (
            (spot, '50000', '50100'), (perp, '50100', '50150'),
        ):
            engine.add_instrument(instrument)
            quotes = []
            for timestamp, value in ((entry_ts, entry_price), (exit_ts, exit_price)):
                price = instrument.make_price(Decimal(value))
                depth = instrument.make_qty(Decimal('1'))
                quotes.append(QuoteTick(
                    instrument.id, price, price, depth, depth, timestamp, timestamp,
                ))
            engine.add_data(quotes)
        engine.add_data([MarkPriceUpdate(
            perp.id, perp.make_price(Decimal('50000')), entry_ts, entry_ts,
        )])
        engine.add_data([FundingRateUpdate(
            perp.id, Decimal(rate), SETTLEMENT, SETTLEMENT, interval=480,
        )])
        strategy = CarryProbe()
        engine.add_strategy(strategy)
        engine.run()
        assert len(strategy.fills) == 4
        for instrument_id, side, price, fee in (
            (spot.id, OrderSide.BUY, '50000', '5'),
            (perp.id, OrderSide.SELL, '50100', '0.9018'),
            (spot.id, OrderSide.SELL, '50100', '5.01'),
            (perp.id, OrderSide.BUY, '50150', '0.9027'),
        ):
            assert (instrument_id, side, quantity, Decimal(price), Decimal(fee)) in strategy.fills
        assert not engine.cache.positions_open()
        spot_account = engine.cache.account_for_venue(spot.id.venue)
        assert spot_account.balance_total(Currency.from_str('BTC')).as_decimal() == 0
        spot_balance = spot_account.balance_total(USDT).as_decimal()
        perp_balance = engine.cache.account_for_venue(perp.id.venue).balance_total(USDT).as_decimal()
        assert spot_balance == Decimal('9999.99')
        assert perp_balance == Decimal('9993.1955') + Decimal('5000') * Decimal(rate)
        fills = [
            {
                'instrument': str(instrument_id),
                'side': str(side),
                'qty': quantity,
                'price': price,
                'commission': fee,
            }
            for instrument_id, side, quantity, price, fee in strategy.fills
        ]
        return {
            'rate': rate,
            'spot_balance': spot_balance,
            'perp_balance': perp_balance,
            'total_balance': spot_balance + perp_balance,
            'fills': fills,
            'total_commission': sum((fill['commission'] for fill in fills), Decimal('0')),
        }
    finally:
        engine.dispose()


if __name__ == '__main__':
    assert nautilus_trader.__version__ == '2.0.0rc5'
    baseline = run('0')
    positive = run('0.0001')
    negative = run('-0.0001')
    assert positive - baseline == Decimal('0.5')
    assert negative - baseline == Decimal('-0.5')
    carry_zero = run_carry('0')
    carry_positive = run_carry('0.0001')
    carry_negative = run_carry('-0.0001')
    assert carry_zero['total_balance'] == Decimal('19993.1855')
    assert carry_positive['total_balance'] == Decimal('19993.6855')
    assert carry_negative['total_balance'] == Decimal('19992.6855')
    carry_pnl = carry_positive['total_balance'] - Decimal('20000')
    assert carry_pnl / Decimal('20000') == Decimal('-0.000315725')
    print(json.dumps({
        'version': nautilus_trader.__version__,
        'scope': 'offline synthetic single-leg funding and two-leg cashflow',
        'baseline_balance': str(baseline),
        'positive_rate_balance': str(positive),
        'negative_rate_balance': str(negative),
        'native_positive_funding_cashflow': str(positive-baseline),
        'native_negative_funding_cashflow': str(negative-baseline),
        'carry_rate_balances': {
            label: {
                'rate': result['rate'],
                'spot_balance': str(result['spot_balance']),
                'perp_balance': str(result['perp_balance']),
                'total_balance': str(result['total_balance']),
            }
            for label, result in (
                ('zero', carry_zero),
                ('positive', carry_positive),
                ('negative', carry_negative),
            )
        },
        'carry_fills': [
            {
                'instrument': fill['instrument'],
                'side': fill['side'],
                'qty': str(fill['qty']),
                'price': str(fill['price']),
                'commission': str(fill['commission']),
            }
            for fill in carry_zero['fills']
        ],
        'carry_total_commission_usdt': str(carry_zero['total_commission']),
        'carry_net_pnl_usdt': str(carry_pnl),
        'carry_total_capital_return': str(carry_pnl / Decimal('20000')),
        'liquidation_enabled_argument': 'liquidation_enabled' in inspect.signature(BacktestEngine.add_venue).parameters,
    }, indent=2))
