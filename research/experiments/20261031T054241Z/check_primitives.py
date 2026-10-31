"""Synthetic arithmetic boundaries only; no financial evidence or market evaluation."""
import copy
from decimal import Decimal as D
from common import *
import engine
v={i:D('100') for i in range(-3,60)};v[32]=D('90');v[29]=D('100');v[-3]=D('80')
z=engine.target(v,33,3,.02,0,0,35);assert z[0]==1
future=copy.deepcopy(v);future[33]=D('999999');assert engine.target(future,33,3,.02,0,0,35)==z
earlier=copy.deepcopy(v);earlier[-3]=D('110');assert engine.target(earlier,33,3,.02,0,0,35)[0]==0
flat=copy.deepcopy(v);flat[32]=flat[29];assert engine.target(flat,33,3,.02,1,0,35)[0]==0
edge=copy.deepcopy(v);edge[32]=D('98');assert engine.target(edge,33,3,.02,0,0,35)[0]==0
edge[32]=D('97.999');assert engine.target(edge,33,3,.02,0,0,35)[0]==1
reopen=copy.deepcopy(v);reopen[32]=D('99');assert engine.target(reopen,33,3,.02,0,0,35)[0]==0 and engine.target(reopen,33,3,.02,1,0,35)[0]==1
base,amount=engine.funding_amount(D('-1'),D('100'),D('.001'),3);assert base==amount==D('.1')
base,amount=engine.funding_amount(D('1'),D('100'),D('.001'),3);assert base==D('-.1') and amount==D('-.3')
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'cases':['S35 explicit negative dictionary key','future-close perturbation no effect','slow-gate incompatible cash','ROC zero exit','exact hurdle cash','strict hurdle entry','no hidden position when gate reopens','asymmetric funding stress']});print('PASS8causal synthetic boundary cases')
