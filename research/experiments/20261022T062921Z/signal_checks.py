"""HMA arithmetic and boundaries only; fabricated prices are not backtest evidence."""
import math
from decimal import Decimal as D
from evaluate import wma_values,hma_values,desired_position
w=wma_values([10,20,30],2);assert w[0] is None and math.isclose(float(w[1]),50/3) and math.isclose(float(w[2]),80/3)
for span in [4,9,16]:
 a=hma_values([100]*50,span);first=span+math.isqrt(span)-2
 assert all(x is None for x in a[:first]) and all(x==100 for x in a[first:])
ramp=hma_values(list(range(1,21)),4);assert all(math.isclose(float(v),i+1) for i,v in enumerate(ramp) if v is not None)
prices=[10,11,9,13,12,15,11,17,15,20,13,22]
a=hma_values(prices,4);b=hma_values(prices+[99999],4);assert a==b[:len(a)]
scaled=hma_values([x*10 for x in prices],4);shifted=hma_values([x+100 for x in prices],4)
for j,x in enumerate(a):
 if x is None:assert scaled[j] is None and shifted[j] is None;continue
 assert math.isclose(float(scaled[j]),float(x)*10,abs_tol=1e-10) and math.isclose(float(shifted[j]),float(x)+100,abs_tol=1e-10)
assert not desired_position(False,D(0))[0] and desired_position(True,D(0))[0]
assert desired_position(False,D('.000001'))[0] and desired_position(True,D('.000001'))[0]
assert not desired_position(False,D('-.000001'))[0] and not desired_position(True,D('-.000001'))[0]
for values in ([1,0,3,4,5],[1,-2,3,4,5],[1,float('nan'),3,4,5]):
 try:hma_values(values,4)
 except AssertionError:pass
 else:raise AssertionError('Invalid prices accepted')
print('PASS: WMA weight order, full-window warmup, floor half/root periods, flat/ramp values, future prefix, scale/translation and zero-slope held-state boundaries')
