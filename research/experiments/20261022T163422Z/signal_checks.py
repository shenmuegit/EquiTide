"""Synthetic boundary/formula checks only, not market backtest evidence."""
from decimal import Decimal as D
from fractions import Fraction as F
import evaluate as ev

def ratio(x):
    return F(x[0], x[1])

def main():
    h, l, c = [3]*5, [1]*5, [2, 3, 1, 2, 3]
    out = ev.ultosc_features(h, l, c, 1)
    assert out[:4] == [None]*4 and ratio(out[4]) == F(175, 2)
    constant = ev.ultosc_features([3]*9, [1]*9, [2]*9, 2)
    assert constant[:8] == [None]*8 and ratio(constant[8]) == 50
    assert ratio(ev.ultosc_features([2]*5, [2]*5, [2]*5, 1)[4]) == 0
    gap = [10, 20, 20, 20, 20]
    assert ratio(ev.ultosc_features(gap, gap, gap, 1)[4]) == F(100, 7)
    for scale, offset in [(10, 0), (1, 100)]:
        assert ev.ultosc_features([x*scale+offset for x in h], [x*scale+offset for x in l], [x*scale+offset for x in c], 1) == out
    assert ev.ultosc_features(h+[3], l+[1], c+[1], 1)[:5] == out
    for threshold in (D(50), D(55), D(60)):
        score = F(threshold)
        assert not ev.desired_position(False, score.numerator, score.denominator, threshold)[0]
        above = score + F(1, 10**60)
        assert ev.desired_position(False, above.numerator, above.denominator, threshold)[0]
    assert ev.desired_position(True, 45, 1, D(55))[0]
    assert not ev.desired_position(True, 44999, 1000, D(55))[0]
    assert not ev.desired_position(True, 0, 1, D(55))[0]
    for args in [([2]*5, [3]*5, [2]*5, 1), ([3]*5, [1]*5, [2]*5, 0)]:
        try:
            ev.ultosc_features(*args)
        except AssertionError:
            pass
        else:
            raise AssertionError('Invalid range or lookback accepted')
    print('PASS: UO weighted windows, exact first index, flat/zero range, prior-close gap, strict thresholds, affine invariance, future-prefix and invalid inputs; synthetic only')

if __name__ == '__main__':
    main()
