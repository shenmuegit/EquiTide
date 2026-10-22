"""Synthetic RSI seed, exact boundaries and causality checks; not backtest evidence."""
from decimal import Decimal as D
from fractions import Fraction as F
import evaluate as ev

def ratio(x):
    return F(x[0], x[1])

def main():
    c = [100, 99, 98, 99, 100]
    out = ev.rsi2_features(c, 5)
    assert out[:4] == [None]*4 and ratio(out[4]) == 75
    assert out[4][3:] == (F(sum(c)), F(sum(c)))
    assert ratio(ev.rsi2_features([100, 101, 100, 102, 101], 5)[4]) == 50
    assert ratio(ev.rsi2_features([1, 2, 3, 4, 5], 5)[4]) == 100
    assert ratio(ev.rsi2_features([5, 4, 3, 2, 1], 5)[4]) == 0
    assert ratio(ev.rsi2_features([2]*5, 5)[4]) == 50
    for scale, offset in [(10, 0), (1, 100)]:
        z = ev.rsi2_features([x*scale+offset for x in c], 5)[4]
        assert z[:3] == out[4][:3]
        assert z[3] == out[4][3]*scale + 5*offset and z[4] == out[4][4]*scale + 5*offset
    assert ev.rsi2_features(c+[90], 5)[:5] == out
    for threshold in (D(10), D(20), D(30)):
        score = F(threshold)
        assert not ev.desired_position(False, score.numerator, score.denominator, threshold, F(2), F(19), F(11), 10)[0]
        below = score-F(1, 10**60)
        assert ev.desired_position(False, below.numerator, below.denominator, threshold, F(2), F(19), F(11), 10)[0]
    assert not ev.desired_position(False, 0, 1, D(20), F(2), F(20), F(11), 10)[0]
    assert ev.desired_position(True, 0, 1, D(20), F(2), F(20), F(11), 10)[0]
    assert ev.desired_position(True, 0, 1, D(20), F(2), F(19), F(10), 10)[0]
    assert not ev.desired_position(True, 0, 1, D(20), F(2), F(19), F(9), 10)[0]
    assert not ev.desired_position(True, 0, 1, D(20), F(2), F(21), F(11), 10)[0]
    for data, n in [([2]*5, 4), ([2, 2, 0, 2, 2], 5)]:
        try:
            ev.rsi2_features(data, n)
        except AssertionError:
            pass
        else:
            raise AssertionError('Invalid close or trend window accepted')
    print('PASS: Wilder2 seed/recursion, zero/gain/loss limits, exact SMA sums, strict entry/trend/fast-exit boundaries, affine invariance and future-prefix; synthetic only')

if __name__ == '__main__':
    main()
