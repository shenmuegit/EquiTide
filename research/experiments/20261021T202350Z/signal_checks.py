"""Channel exclusion, strict boundaries and filled age; not market backtest evidence."""
from decimal import Decimal as D
from evaluate import close_channels,desired_position
assert close_channels([1,2,3,4],3,3,2)==(D(3),D(2))
assert close_channels([1,2,3,4,999999],3,3,2)==(D(3),D(2))
assert close_channels([10,20,30,40],3,3,2)==(D(30),D(20))
assert desired_position(False,D(3),D(3),D(2),0,5)[0] is False
assert desired_position(False,D('3.01'),D(3),D(2),0,5)[0] is True
assert desired_position(True,D(2),D(3),D(2),4,5)[0] is True
assert desired_position(True,D('1.99'),D(3),D(2),4,5)==(False,'exit_below_prior_close_channel')
assert desired_position(True,D(4),D(3),D(2),5,5)==(False,'exit_maximum_holding_time')
assert desired_position(True,D(1),D(3),D(2),5,5)==(False,'exit_maximum_holding_time')
assert desired_position(True,D(4),D(3),D(2),4,5)[0] is True
assert desired_position(True,D(2),D(3),D(1),1,5)[0] is True
assert any(D(2)>=v for v in (D(1),D(3))) and not all(D(2)>=v for v in (D(1),D(3)))
for prices in ([1,0,3],[1,-2,3],[1,float('nan'),3]):
 try:close_channels(prices,2,2,2)
 except AssertionError:pass
 else:raise AssertionError('Invalid price accepted')
print('PASS: lagged channel exclusion, future prefix, scaling, strict boundaries, timeout and exit precedence')
