"""Wilder formula and strict-state fixtures only; not market backtest evidence."""
import math
from decimal import Decimal as D
from evaluate import wilder_rsi, desired_position
assert wilder_rsi([10]*8,2)[2:]==[D(50)]*6
assert wilder_rsi(range(1,9),2)[2:]==[D(100)]*6
assert wilder_rsi(range(8,0,-1),2)[2:]==[D(0)]*6
values=[10,11,10,12,12]
a=wilder_rsi(values,2)
assert a[:2]==[None,None] and a[2]==D(50)
assert math.isclose(float(a[3]),100*1.25/1.5,abs_tol=1e-12)
assert a==wilder_rsi(values+[999999],2)[:len(values)]
assert all(x is None or math.isclose(float(x),float(y),abs_tol=1e-12) for x,y in zip(a,wilder_rsi([x*10 for x in values],2)))
assert desired_position(False,D(60),D(60),D(45))[0] is False
assert desired_position(False,D('60.001'),D(60),D(45))[0] is True
assert desired_position(True,D(45),D(60),D(45))[0] is True
assert desired_position(True,D('44.999'),D(60),D(45))[0] is False
assert desired_position(True,D(50),D(60),D(45))[0] is True
assert desired_position(False,D(50),D(60),D(45))[0] is False
for prices in ([1,0,3],[1,-2,3],[1,float('nan'),3]):
 try:wilder_rsi(prices,2)
 except AssertionError:pass
 else:raise AssertionError('Invalid price accepted')
print('PASS: seed/update, flat/up/down, scaling, future prefix, invalid input, strict momentum entry, exit equality and position deadband')
