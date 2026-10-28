"""Synthetic rule counterexamples only; no market data, strategy PnL or registration."""
from decimal import Decimal as D
from fractions import Fraction as F
import engine

def prices(fast,neighbors):
 v=[D(100)]*64;j=63;v[j-3]=D(fast)
 for n,x in zip([27,28,29],neighbors):v[j-n]=D(x)
 return v
vote=getattr(engine,'majority_target',engine.target)
v=prices(90,[110,90,120]);assert engine.target(v,64,3,.025,0,0,28)[0]==0
assert vote(v,64,3,.025,0,0,28)[0]==-1,'two negative adjacent horizons must permit the contrarian short despite the positive center;legacy single horizon stays flat'
v=prices(110,[90,110,80]);assert engine.target(v,64,3,.025,0,0,28)[0]==0;assert vote(v,64,3,.025,0,0,28)[0]==1
v=prices(90,[100,90,110]);assert vote(v,64,3,.025,0,0,28)[0]==0,'positive/neutral/negative has no majority'
v=prices(99,[110,90,120]);assert vote(v,64,3,.025,0,0,28)[0]==0,'cash must not enter inside the fast ROC band';assert vote(v,64,3,.025,-1,0,28)[0]==-1,'retain an actual short while positive fast ROC stays inside the entry band'
v=prices(101,[90,110,80]);assert vote(v,64,3,.025,1,0,28)[0]==1
v=prices(100,[90,110,80]);assert vote(v,64,3,.025,1,0,28)[0]==0,'zero fast ROC exits even with a slow majority'
v=prices(90,[110,90,120]);answer=vote(v,64,3,.025,0,0,28);assert answer==vote(v+[D(1),D(100000)],64,3,.025,0,0,28),'future closes cannot affect the earlier decision';assert F(answer[2])==F(100,110)-1
print('PASS:majority-vs-single-horizon short/long counterexamples,neutralvote,cash-entryhurdle,actualpositionhysteresis,zeroexit,exactmedian,andfutureinvariance;syntheticonly,no PnL.')
