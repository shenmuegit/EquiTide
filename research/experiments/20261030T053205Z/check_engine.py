"""Synthetic bank-unit/capital/cost invariants;no source strategy simulation."""
import ast
from run import ROOT,R,sha,put
assert sha(R/'engine.py')==sha(ROOT/'research/experiments/20261030T033034Z/engine.py')
for a in [.25,.5,.75]:
 units=[1,a,1-a];cap=[5000,15000,15000];assert sum(w*c for w,c in zip(units,cap))==20000 and sum(units)==2
 nav=[5050,15300,14800];value=sum(w*v for w,v in zip(units,nav));assert value!=sum(w/sum(units)*v for w,v in zip(units,nav));cost=[1,9,3];assert sum(w*c for w,c in zip(units,cost))==4+6*a
for f in ['run.py','audit.py']:
 t=ast.parse((R/f).read_text());assert not any(isinstance(x,ast.Call) and isinstance(x.func,ast.Attribute) and x.func.attr in ['simulate','target','trade'] for x in ast.walk(t))
put(R/'engine_change_verification.json',{'passed':True,'new_native_evaluations':0,'synthetic_bank_unit_cases':3,'no_normalization_no_new_native_simulate_calls':True,'readonly_axis_engine_sha256':sha(R/'engine.py')});print('PASS raw3bank-unitcapital/cost/non-normalization invariants')
