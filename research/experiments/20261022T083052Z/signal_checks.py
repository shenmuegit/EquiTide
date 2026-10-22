"""Aroon boundaries only; fabricated bars are not financial backtest evidence."""
from decimal import Decimal as D
from evaluate import aroon_features,desired_position
up=aroon_features([2,3,4,5,6],[1,2,3,4,5],3);down=aroon_features([6,5,4,3,2],[5,4,3,2,1],3)
assert up[:3]==[None]*3 and up[3]==(0,3,D(100),D(0)) and down[3]==(3,0,D(0),D(100))
flat=aroon_features([10]*5,[9]*5,3);assert all(v==(0,0,D(100),D(100)) for v in flat[3:])
oldest=aroon_features([10,2,3,4],[1,D('1.5'),2,3],3);assert oldest[3]==(3,3,D(0),D(0))
tied=aroon_features([3,2,3,3],[1,1,2,1],3);assert tied[3]==(0,0,D(100),D(100))
h=[10,11,12,11,14,13,14,16];l=[8,9,10,9,11,8,12,13];a=aroon_features(h,l,3)
assert a==aroon_features(h+[99999],l+[D('.01')],3)[:len(a)]
assert a==aroon_features([v*10 for v in h],[v*10 for v in l],3)==aroon_features([v+100 for v in h],[v+100 for v in l],3)
assert not desired_position(False,D(20),D(20))[0] and desired_position(False,D('20.0001'),D(20))[0]
assert desired_position(True,D(0),D(60))[0] and not desired_position(True,D('-.0001'),D(60))[0]
assert not desired_position(False,D(0),D(20))[0] and desired_position(True,D(1),D(60))[0]
for hi,lo in [([2,3,4],[1,0,2]),([2,3,4],[1,4,2]),([2,float('nan'),4],[1,2,3])]:
 try:aroon_features(hi,lo,2)
 except AssertionError:pass
 else:raise AssertionError('Invalid ranges accepted')
print('PASS: N+1 window and oldest endpoint, newest tied extremes, flat/up/down, future prefix, scale/translation, strict entry and zero exit boundaries')
