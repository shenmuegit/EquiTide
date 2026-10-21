"""Indicator and equality-boundary fixtures only; not backtest evidence."""
from decimal import Decimal as D
from evaluate import median_reference, hysteresis

assert median_reference([1, 3, 9], 2, 3) == D(3)
assert median_reference([1, 3, 5, 7], 3, 4) == D(4)
assert median_reference([10, 10, 99999], 2, 3) == D(10)
assert median_reference([1, 3, 5, 7, 99999], 3, 4) == D(4)
assert median_reference([10, 30, 50, 70], 3, 4) == D(40)
assert hysteresis.step(False, D('101'), D('100'), D('.01'))[0] is False
assert hysteresis.step(True, D('99'), D('100'), D('.01'))[0] is True
assert hysteresis.step(False, D('101.0001'), D('100'), D('.01'))[0] is True
assert hysteresis.step(True, D('98.9999'), D('100'), D('.01'))[0] is False
print('PASS: odd/even median, outlier, future prefix, scale, exact Decimal band equality')
