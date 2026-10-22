"""MFI boundaries only; fabricated bars are not financial backtest evidence."""
import math
from decimal import Decimal as D
from evaluate import mfi_features,desired_position
f=lambda prices,vol:mfi_features([x+1 for x in prices],[x-1 for x in prices],prices,vol,2)
up=f([10,11,12,13],[1]*4);down=f([13,12,11,10],[1]*4)
assert up[:2]==[None,None] and up[2][2]==100 and down[2][2]==0
balanced=f([10,12,10],[1,5,6]);assert balanced[2][2]==50 and not desired_position(False,*balanced[2][:2],D(50))[0]
sixty=f([10,12,10],[1,5,4]);assert sixty[2][2]==60 and not desired_position(False,*sixty[2][:2],D(60))[0] and desired_position(False,*sixty[2][:2],D(59))[0]
fortyfive=f([10,12,10],[1,D('3.75'),D('5.5')]);assert fortyfive[2][2]==45 and desired_position(True,*fortyfive[2][:2],D(60))[0]
assert not desired_position(True,D(4499),D(100),D(60))[0]
for series in [f([10]*5,[1]*5),f([10,11,12,13,14],[0]*5)]:
 assert all(x[2]==50 for x in series[2:])
 assert desired_position(True,*series[2][:2],D(60))[0] and not desired_position(False,*series[2][:2],D(50))[0]
assert f([100,10,11,12],[1,1000,1,1])[-1][2]==100
h=[10,11,12,11,14,13,14,16];l=[8,9,10,9,11,8,12,13];c=[9,10,11,10,12,10,13,14];v=[3,7,2,9,6,1,8,4];a=mfi_features(h,l,c,v,3)
assert a==mfi_features(h+[99999],l+[D('.01')],c+[100],v+[99999],3)[:len(a)]
scaled=mfi_features([x*10 for x in h],[x*10 for x in l],[x*10 for x in c],v,3);shifted=mfi_features([x+100 for x in h],[x+100 for x in l],[x+100 for x in c],v,3)
assert all(math.isclose(float(x[2]),float(scaled[j][2]),abs_tol=1e-10) for j,x in enumerate(a) if x is not None)
# A common price translation changes price*volume weights; it must not be assumed invariant.
assert any(not math.isclose(float(x[2]),float(shifted[j][2]),abs_tol=1e-10) for j,x in enumerate(a) if x is not None)
for hi,lo,cl,vol in [([2,3,4],[1,0,2],[1,2,3],[1]*3),([2,3,4],[1,2,3],[1,2,3],[1,-1,1])]:
 try:mfi_features(hi,lo,cl,vol,2)
 except AssertionError:pass
 else:raise AssertionError('Invalid HLCV accepted')
print('PASS: Nflows/N+1prices, strict50/60 and45exit boundaries, positive/negative/zero/tied flows, future prefix, scaling and non-invariance to price translation')
