"""Indicator-only boundary checks; fixtures are not backtest evidence."""
import math
import numpy as np
from evaluate import signed_efficiency

assert signed_efficiency([1, 2, 3, 4], 3, 3) == 1
assert signed_efficiency([4, 3, 2, 1], 3, 3) == -1
assert signed_efficiency([2, 2, 2, 2], 3, 3) == 0
assert math.isclose(signed_efficiency([1, 2, 1, 2], 3, 3), 1 / 3)
prefix = [1, 2, 1, 2]
assert signed_efficiency(prefix + [1e9], 3, 3) == signed_efficiency(prefix, 3, 3)
assert signed_efficiency(np.array(prefix) * 100, 3, 3) == signed_efficiency(prefix, 3, 3)
print('PASS: monotone, falling, flat, noisy, future-prefix and scale boundaries')
