"""Synthetic strict majority threshold and no-hidden-state/causality checks;no PnL."""
from fractions import Fraction as F
import inspect,importlib.util
from pathlib import Path
import engine
assert 'slow_return_hurdle_fraction' in inspect.signature(engine.majority_target).parameters,'Missing explicit slow-hurdle argument'
p=Path(__file__).resolve().parents[3]/'research/experiments/20261028T232123Z/engine.py';sp=importlib.util.spec_from_file_location('unchanged_zero_gate_engine',p);old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old)
checks=0
def values(L,S,fast,slow):
 v=[F(100)]*64
 for n,x in zip([S-1,S,S+1],slow):v[63-n]=F(100)/(1+x)
 v[63-L]=F(100)/(1+fast);return v
for L in [3,4]:
 for S in [27,28,29]:
  for G in [F(1,200),F(1,100),F(1,50)]:
   for sign in [-1,1]:
    fast=-sign*F(3,100);eps=F(1,100000)
    v=values(L,S,fast,[sign*G,sign*(G+eps),sign*(G-eps)])
    for held in [-1,0,1]:assert engine.majority_target(v,64,L,.025,held,0,S,float(G))[0]==0;checks+=1
    v=values(L,S,fast,[sign*(G+eps),sign*(G+2*eps),-sign*F(1,5)]);out=engine.majority_target(v,64,L,.025,0,0,S,float(G));assert out[0]==sign and out==engine.majority_target(v+[F(1),F(100000)],64,L,.025,0,0,S,float(G));checks+=2
    for held in [-1,0,1]:assert engine.majority_target(v,64,L,.025,held,0,S,0)==old.majority_target(v,64,L,.025,held,0,S);checks+=1
    equal=values(L,S,-sign*F(25,1000),[sign*(G+eps)]*3);assert engine.majority_target(equal,64,L,.025,0,0,S,float(G))[0]==0;checks+=1
    retain=values(L,S,-sign*F(1,100),[sign*(G+eps)]*3);assert engine.majority_target(retain,64,L,.025,sign,0,S,float(G))[0]==sign and engine.majority_target(retain,64,L,.025,0,0,S,float(G))[0]==0;checks+=2
print('PASS:',checks,'slow-equality/2of3/fast-equality/actualposition/cash/future/zero-gate-regression checks;syntheticonly,no market evaluation')
