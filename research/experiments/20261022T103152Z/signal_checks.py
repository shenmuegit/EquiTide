"""CCI algebra only; fabricated HLC bars are not financial backtest evidence."""
import math
from decimal import Decimal as D
from evaluate import cci_features,desired_position
up=cci_features([10,11,12],[8,9,10],[9,10,11],3);down=cci_features([12,11,10],[10,9,8],[11,10,9],3)
assert up[:2]==[None,None] and up[2][2]==100 and down[2][2]==-100
assert not desired_position(False,*up[2][:2],D(100))[0] and desired_position(False,*up[2][:2],D(99))[0]
assert not desired_position(True,*down[2][:2],D(100))[0]
flat=cci_features([11]*5,[9]*5,[10]*5,3)
assert all(v==(D(0),D(0),D(0)) for v in flat[2:])
assert desired_position(True,D(0),D(0),D(100))[0] and not desired_position(False,D(0),D(0),D(100))[0]
last=cci_features([1000,10,11,12],[1,8,9,10],[2,9,10,11],3);assert last[-1][2]==100
h=[10,11,12,11,14,13,14,16];l=[8,9,10,9,11,8,12,13];c=[9,10,11,10,12,10,13,14];a=cci_features(h,l,c,3)
assert a==cci_features(h+[99999],l+[D('.01')],c+[100],3)[:len(a)]
scaled=cci_features([v*10 for v in h],[v*10 for v in l],[v*10 for v in c],3);shifted=cci_features([v+100 for v in h],[v+100 for v in l],[v+100 for v in c],3)
for j,x in enumerate(a):
 if x is None:assert scaled[j] is None and shifted[j] is None;continue
 assert all(math.isclose(float(x[2]),float(v[j][2]),abs_tol=1e-10) for v in [scaled,shifted])
for hi,lo,cl in [([2,3,4],[1,0,2],[1,2,3]),([2,3,4],[1,4,2],[1,2,3]),([2,float('nan'),4],[1,2,3],[1,2,3])]:
 try:cci_features(hi,lo,cl,2)
 except AssertionError:pass
 else:raise AssertionError('Invalid HLC accepted')
print('PASS: N complete bars, exact CCI100 boundary, mean absolute deviation, zero-deviation held state, future prefix and scale/translation invariance')
