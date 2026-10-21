"""Indicator fixtures and strict boundaries only; not financial backtest evidence."""
import math
from evaluate import trend_score, desired_position
assert trend_score([100.]*21,20,21)[0]==0
up=[math.exp(.01*j) for j in range(21)]
assert trend_score(up,20,21)[0]>1e6
assert trend_score(up[::-1],20,21)[0]<-1e6
prices=[100,104,99,108,103,112,106]
a=trend_score(prices,6,7)[0]
assert math.isclose(a,trend_score([x*10 for x in prices],6,7)[0],rel_tol=1e-12)
assert a==trend_score(prices+[1e8],6,7)[0]
assert desired_position(False,2.,2.)[0] is False
assert desired_position(False,2.00001,2.)[0] is True
assert desired_position(True,0.,2.)[0] is False
assert desired_position(True,.00001,2.)[0] is True
for invalid in ([1,0,3],[1,-2,3],[1,float('nan'),3]):
 try:trend_score(invalid,2,3)
 except AssertionError:pass
 else:raise AssertionError('Invalid price accepted')
print('PASS: flat/perfect up/down, scale, future prefix, invalid prices, strict entry and zero exit')
