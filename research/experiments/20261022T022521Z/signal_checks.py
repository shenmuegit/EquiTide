"""EMA seed, MACD relations and zero boundaries only; not financial evidence."""
import math
from decimal import Decimal as D
from evaluate import ema_values,macd_features,desired_position
assert ema_values([1,3,5],3)==[D(1),D(2),D('3.5')]
assert all(x==0 for x in macd_features([100]*20,3,8,4)[2])
up=macd_features(list(range(1,21)),3,8,4);down=macd_features(list(range(20,0,-1)),3,8,4)
assert up[2][1]>0 and down[2][1]<0
prices=[10,11,9,13,12,15]
a=macd_features(prices,3,8,4);b=macd_features(prices+[99999],3,8,4)
assert all(x==y[:len(prices)] for x,y in zip(a,b))
for series,scaled,shifted in zip(a,macd_features([x*10 for x in prices],3,8,4),macd_features([x+10 for x in prices],3,8,4)):
 assert all(math.isclose(float(y),float(x)*10,abs_tol=1e-10) and math.isclose(float(z),float(x),abs_tol=1e-10) for x,y,z in zip(series,scaled,shifted))
assert desired_position(False,D(0))[0] is False
assert desired_position(True,D(0))[0] is False
assert desired_position(False,D('.00001'))[0] is True
assert desired_position(True,D('-.00001'))[0] is False
for prices in ([1,0,3],[1,-2,3],[1,float('nan'),3]):
 try:macd_features(prices,3,8,4)
 except AssertionError:pass
 else:raise AssertionError('Invalid prices accepted')
print('PASS: first seed/recursion, flat/up/down, MACD-signal relation, future prefix, scale/translation and zero boundary')
