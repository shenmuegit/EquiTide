"""Synthetic strict-hurdle and future-data checks for already implemented majority rule; no PnL."""
from decimal import Decimal as D
import engine
for H,pct in [(.02,D(2)),(.03,D(3))]:
 v=[D(100)]*64;j=63;v[j]=100+pct;v[j-3]=D(100)
 for n,x in zip([27,28,29],[D(110),D(90),D(120)]):v[j-n]=x
 assert engine.majority_target(v,64,3,H,0,0,28)[0]==0,'equality must not enter'
 v[j]+=D('.001');short=engine.majority_target(v,64,3,H,0,0,28);assert short[0]==-1
 assert short==engine.majority_target(v+[D(1),D(100000)],64,3,H,0,0,28)
 v=[D(100)]*64;v[j]=100-pct
 for n,x in zip([27,28,29],[D(90),D(110),D(80)]):v[j-n]=x
 assert engine.majority_target(v,64,3,H,0,0,28)[0]==0
 v[j]-=D('.001');assert engine.majority_target(v,64,3,H,0,0,28)[0]==1
print('PASS:bothnewH2/H3strictequality/epsilon-entrylongandshort,adjacentmajority,andfutureinvariance;syntheticonly,no PnL.')
