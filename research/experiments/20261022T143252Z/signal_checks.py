"""Synthetic formula checks only; these are not market backtest evidence."""
from decimal import Decimal as D
from fractions import Fraction as F
import evaluate as ev

def ratio(x):
    return F(x[0], x[1])

def main():
    h, l, c, v = [3, 3, 3, 3], [1, 1, 1, 1], [3, 1, 2, 3], [1, 2, 3, 4]
    out = ev.cmf_features(h, l, c, v, 2)
    assert out[0] is None and ratio(out[1]) == F(-1, 3)
    assert ratio(out[2]) == F(-2, 5) and ratio(out[3]) == F(4, 7)
    assert ratio(ev.cmf_features([2, 3], [2, 1], [2, 3], [9, 1], 2)[1]) == F(1, 10)
    assert ratio(ev.cmf_features([3, 3], [1, 1], [3, 1], [0, 0], 2)[1]) == 0
    for scale, offset, volume_scale in [(10, 0, 1), (1, 100, 1), (1, 0, 100)]:
        z = ev.cmf_features([x*scale+offset for x in h], [x*scale+offset for x in l], [x*scale+offset for x in c], [x*volume_scale for x in v], 2)
        assert z == out
    assert ev.cmf_features(h[:3], l[:3], c[:3], v[:3], 2) == out[:3]
    for threshold in (D(0), D('.05'), D('.10')):
        score = F(threshold)
        assert not ev.desired_position(False, score.numerator, score.denominator, threshold)[0]
        above = score + F(1, 10**60)
        assert ev.desired_position(False, above.numerator, above.denominator, threshold)[0]
    assert ev.desired_position(True, -1, 20, D('.05'))[0]
    assert not ev.desired_position(True, -51, 1000, D('.05'))[0]
    assert ev.desired_position(True, 0, 1, D('.05'))[0]
    for args in [([2, 2], [3, 1], [2, 2], [1, 1], 2), ([3, 3], [1, 1], [2, 2], [-1, 1], 2)]:
        try:
            ev.cmf_features(*args)
        except AssertionError:
            pass
        else:
            raise AssertionError('Invalid price range or negative volume accepted')
    assert ev.ratio_sha(1, 20) == ev.ratio_sha(F('.05').numerator, F('.05').denominator)
    print('PASS: exact CMF window, flat range/zero volume, strict boundaries, prefix/scaling/translation, invalid inputs; synthetic only')

if __name__ == '__main__':
    main()
