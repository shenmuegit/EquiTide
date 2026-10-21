"""Range formula and equality fixtures only; not financial backtest evidence."""
from decimal import Decimal as D
from evaluate import range_position,desired_position
assert range_position([1,5,3],2,3)==(D('.5'),D(1),D(5))
assert range_position([10,10,10],2,3)==(D('.5'),D(10),D(10))
assert range_position([1,2,3],2,3)[0]==D(1)
assert range_position([3,2,1],2,3)[0]==D(0)
assert range_position([1,5,3,999999],2,3)==range_position([1,5,3],2,3)
assert range_position([10,50,30],2,3)[0]==range_position([1,5,3],2,3)[0]
assert range_position([11,15,13],2,3)[0]==range_position([1,5,3],2,3)[0]
assert desired_position(False,D('.7'),D('.7'),D('.2'))[0] is False
assert desired_position(False,D('.70001'),D('.7'),D('.2'))[0] is True
assert desired_position(True,D('.2'),D('.7'),D('.2'))[0] is True
assert desired_position(True,D('.19999'),D('.7'),D('.2'))[0] is False
for prices in ([1,0,3],[1,-2,3],[1,float('nan'),3]):
 try:range_position(prices,2,3)
 except AssertionError:pass
 else:raise AssertionError('Invalid price accepted')
print('PASS: inclusive range, flat/up/down, future prefix, scale/translation invariance and exact entry/exit equality')
