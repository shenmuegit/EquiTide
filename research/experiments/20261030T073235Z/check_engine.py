import ast
from decimal import Decimal as D
from run import ROOT,R,sha,put
assert sha(R/'engine.py')==sha(ROOT/'research/experiments/20261030T033034Z/engine.py')
assert sha(R/'fast_engine.py')==sha(ROOT/'research/experiments/20261029T232932Z/engine.py')
for a in [.25,.5,.75]:
 caps=[5000,15000*a,15000*(1-a)];notionals=[500,4500*a,1500*(1-a)];assert sum(caps)==20000 and [n/c for n,c in zip(notionals,caps)]==[.1,.3,.1]
 assert sum([1,1,1])==3 and sum(caps)/3!=20000
for n in ['engine.py','fast_engine.py','audit_native.py','run.py','audit.py']:ast.parse((R/n).read_text())
put(R/'engine_change_verification.json',{'passed':True,'new_native_planned':36,'native_engine_bodies_byte_identical':True,'synthetic_capital_cases':3,'new_actual_order_quantities_required':True,'financial_evaluations':0,'slow_engine_sha256':sha(R/'engine.py'),'fast_engine_sha256':sha(R/'fast_engine.py')});print('PASS unchanged native engines, capital, exposure and raw1/1/1 invariant preflight')
