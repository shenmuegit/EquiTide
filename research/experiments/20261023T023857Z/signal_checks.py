"""Synthetic VWMA window, exact-threshold and causal-prefix checks; not real backtests."""
from decimal import Decimal as D
from fractions import Fraction as F
from evaluate import vwma_features,desired_position

p=[10,20,30,40];v=[1,3,2,4]
a=vwma_features(p,v,2);assert a==[None,F(35,2),F(24),F(110,3)]
assert vwma_features(p,[1]*4,2)==[None,F(15),F(25),F(35)]
assert vwma_features(p,[x*100 for x in v],2)==a
assert vwma_features([x+100 for x in p],v,2)==[None]+[x+100 for x in a[1:]]
assert vwma_features(p+[999],v+[99],2)[:4]==a
assert vwma_features(p,[0]*4,2)==[None]*4
for b in [D('.005'),D('.01'),D('.02')]:
 anchor=F(100);upper=anchor*(1+F(b));lower=anchor*(1-F(b));eps=F(1,10**60)
 assert not desired_position(False,upper,anchor,b)[0] and desired_position(False,upper+eps,anchor,b)[0]
 assert desired_position(True,lower,anchor,b)[0] and not desired_position(True,lower-eps,anchor,b)[0]
 assert desired_position(True,F(100),anchor,b)[0] and not desired_position(False,F(100),anchor,b)[0]
 assert desired_position(True,F(100),None,b)[0] and not desired_position(False,F(100),None,b)[0]
for args in [([],[],2),([1],[1],0),([1],[-1],1),([0],[1],1),([1,2],[1],2)]:
 try:vwma_features(*args)
 except (AssertionError,ValueError):pass
 else:raise AssertionError('Invalid input accepted')
print('PASS: exact volume-weighted windows, uniform/zero volume, scale/shift and prefix invariants, three strict boundary pairs and position preservation; synthetic only')
