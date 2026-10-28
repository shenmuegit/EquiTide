"""Synthetic signal boundary/state/causality checks; no market or PnL evaluation."""
from decimal import Decimal as D
import engine
checks=0
for L in [2,3,4,5]:
 for H in [.02,.025,.03]:
  for S in [27,28,29]:
   for sign in [-1,1]:
    v=[D(100)]*64;j=63;v[j]=D(100)*(1+sign*D(str(H)))
    for n,x in zip([S-1,S,S+1],([110,90,120] if sign==1 else [90,110,80])):v[j-n]=D(x)
    assert engine.majority_target(v,64,L,H,0,0,S)[0]==0,'Equality cannot open from cash'
    v[j]+=sign*D('.001');out=engine.majority_target(v,64,L,H,0,0,S);assert out[0]==-sign and out==engine.majority_target(v+[D(1),D(100000)],64,L,H,0,0,S);checks+=3
   for direction in [-1,1]:
    v=[D(100)]*64;v[63]=D(100)-direction*D(1)
    for n,x in zip([S-1,S,S+1],([90,110,80] if direction==1 else [110,90,120])):v[63-n]=D(x)
    assert engine.majority_target(v,64,L,H,direction,0,S)[0]==direction and engine.majority_target(v,64,L,H,0,0,S)[0]==0;checks+=2
print('PASS:',checks,'strict equality/epsilon,actual-position retention,cash reentry and future invariance checks;synthetic only,no PnL')
