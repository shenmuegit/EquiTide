"""Indicator edge checks only; fabricated prices are not backtest evidence."""
import math
from decimal import Decimal as D
from evaluate import kama_features,desired_position
ers,sc,kama=kama_features([1,2,3,4,5],3,30)
assert kama[:2]==[None,None] and kama[2]==2 and ers[3]==ers[4]==1
assert math.isclose(float(sc[3]),4/9) and math.isclose(float(kama[3]),26/9)
ers,sc,kama=kama_features([100]*20,3,30)
assert all(v==100 for v in kama[2:]) and all(v==0 for v in ers[3:])
assert all(math.isclose(float(v),(2/31)**2) for v in sc[3:])
a=kama_features([10,11,10,11,10],2,30);assert a[0][2:]==[D(0)]*3
prices=[10,11,9,13,12,15,11,17]
a=kama_features(prices,3,30);b=kama_features(prices+[99999],3,30)
assert all(x==y[:len(prices)] for x,y in zip(a,b))
scaled=kama_features([x*10 for x in prices],3,30);shifted=kama_features([x+100 for x in prices],3,30)
for idx,series in enumerate(a):
 for j,x in enumerate(series):
  if x is None:assert scaled[idx][j] is None and shifted[idx][j] is None;continue
  sy=float(x)*10 if idx==2 else float(x);sh=float(x)+100 if idx==2 else float(x)
  assert math.isclose(float(scaled[idx][j]),sy,abs_tol=1e-10) and math.isclose(float(shifted[idx][j]),sh,abs_tol=1e-10)
assert not desired_position(False,D(101),D(100))[0]
assert desired_position(False,D('101.0001'),D(100))[0]
assert desired_position(True,D(99),D(100))[0]
assert not desired_position(True,D('98.9999'),D(100))[0]
assert desired_position(True,D(100),D(100))[0] and not desired_position(False,D(100),D(100))[0]
for values in ([1,0,3],[1,-2,3],[1,float('nan'),3]):
 try:kama_features(values,2,30)
 except AssertionError:pass
 else:raise AssertionError('Invalid prices accepted')
print('PASS: SMA seed, monotone/choppy/flat ER and squared smoothing, future prefix, scale/translation and strict hysteresis boundaries')
