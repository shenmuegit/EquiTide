"""Synthetic IBS, exact threshold and causal-prefix checks; not backtest evidence."""
from decimal import Decimal as D
from fractions import Fraction as F
import evaluate as ev

def ratio(x):
    return F(x[0], x[1])

def main():
    h, l, c = [3, 3, 3], [1, 1, 1], [1, 2, 3]
    out = ev.ibs_features(h, l, c)
    assert [ratio(x) for x in out] == [0, F(1, 2), 1]
    assert ratio(ev.ibs_features([2], [2], [2])[0]) == F(1, 2)
    for scale, offset in [(10, 0), (1, 100)]:
        assert ev.ibs_features([x*scale+offset for x in h], [x*scale+offset for x in l], [x*scale+offset for x in c]) == out
    assert ev.ibs_features(h+[3], l+[1], c+[1])[:3] == out
    for entry in (D('.1'), D('.2'), D('.3')):
        for exit_threshold in (D('.6'), D('.7'), D('.8')):
            a, b = F(entry), F(exit_threshold)
            assert not ev.desired_position(False, a.numerator, a.denominator, entry, exit_threshold)[0]
            below = a-F(1, 10**60)
            assert ev.desired_position(False, below.numerator, below.denominator, entry, exit_threshold)[0]
            assert ev.desired_position(True, b.numerator, b.denominator, entry, exit_threshold)[0]
            above = b+F(1, 10**60)
            assert not ev.desired_position(True, above.numerator, above.denominator, entry, exit_threshold)[0]
            assert ev.desired_position(True, 1, 2, entry, exit_threshold)[0]
            assert not ev.desired_position(False, 1, 2, entry, exit_threshold)[0]
    for args in [([2], [3], [2]), ([3], [1], [4]), ([], [], [])]:
        try:
            ev.ibs_features(*args)
        except AssertionError:
            pass
        else:
            raise AssertionError('Invalid range, close or empty bars accepted')
    print('PASS: one-bar IBS extrema/midpoint, zero-range0.5, 9strict entry/exit boundary pairs, affine invariance and future-prefix; synthetic only')

if __name__ == '__main__':
    main()
