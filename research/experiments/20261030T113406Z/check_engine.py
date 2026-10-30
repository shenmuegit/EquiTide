"""BoundedS26domainextension,allcommonparameteroutputs/causalityandunchangedaccounting verified synthetically."""
import ast,copy
from decimal import Decimal as D
from run import ROOT,R,sha,put,module
import engine
p=ROOT/'research/experiments/20261030T093306Z/engine.py';old=p.read_text();new=(R/'engine.py').read_text();needle='trend_lookback_days in [27,28,29,30,31]';assert old.count(needle)==1 and new==old.replace(needle,'trend_lookback_days in [26,27,28,29,30,31]')
legacy=module(p,'legacy_fast_price_domain');values=[D(100)+D((i*7)%23-11)/D(2) for i in range(90)];causal=common=0
for L in [3,4,5]:
 for S in [26,27,28]:
  assert 33-2-S>=0
  for direction in [-1,0,1]:
   for i in [33,60]:
    args=(i,L,.025,direction,-.01,S,'entries_only');got=engine.majority_target(values,*args);future=values[:i]+[D('99999')]*(len(values)-i);assert engine.majority_target(future,*args)==got;causal+=1
    if S>=27:assert legacy.majority_target(values,*args)==got;common+=1
assert causal==54 and common==36 and sum([5000,7500,7500])==20000 and sum([500,2250,750])/20000==.175
for n in ['engine.py','audit_native.py','run.py','audit.py']:ast.parse((R/n).read_text())
put(R/'engine_change_verification.json',{'passed':True,'base_engine_sha256':sha(p),'new_engine_sha256':sha(R/'engine.py'),'only_change':'majority_targetassertallowsS26','all_formulas_costs_cash_funding_risk_and_old_parameter_behavior_unchanged':True,'synthetic_future_price_mutation_cases':causal,'common_old_parameter_exact_output_cases':common,'full_context_minimum_nonnegative':True,'new_native_cells_planned':5,'financial_evaluations':0});print('PASS S26-onlyassertdomainpatch,54causal/36exactlegacycases,unchangedaccounting')
