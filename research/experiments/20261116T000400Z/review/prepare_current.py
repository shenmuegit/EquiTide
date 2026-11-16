"""Check new narrower exits with synthetic prefixes and a full-ledger exact lookup."""
import ast,json,sys
from fractions import Fraction as F
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];P=ROOT/'research/experiments/20261115T220354Z';sys.path.insert(0,str(R))
from common import *
prior=json.loads((R/'native_exit_prior_lookup.json').read_text())['matching_fixed_definitions']
assert prior and not any(x['E'] in [0.,.0025] and (x['result_available'] or x['status']=='reserved') for x in prior)
assert sha(P/'engine.py')==sha(R/'engine.py') and sha(P/'core391_tail_safe.py')==sha(R/'core391_tail_safe.py')
import engine
cases=[];L=29;H=F('.03')
for E in [F(0),F('.0025'),F('.005')]:
 for actual in [-1,0,1]:
  for roc in sorted(set([-H-F('1e-8'),-H,-E-F('1e-8'),-E,F(0),E,E+F('1e-8'),H,H+F('1e-8')])):
   c=[F(200)]*60;c[39-L]=F(100);c[39]=100*(1+roc)
   expected=1 if roc>H else -1 if roc<-H else 1 if actual==1 and roc>-E else -1 if actual==-1 and roc<E else 0
   out=engine.btc.target(c,40,L,float(H),actual,float(E))
   assert out[0]==expected and F(out[1])==roc
   assert out==engine.btc.target(c[:40]+[F(10**12),F(1)],40,L,float(H),actual,float(E))
   cases.append({'E':str(E),'actual':actual,'ROC':str(roc),'passed':True})
put(R/'exact_parameter_registry_screen.json',{'passed':True,'recorded_utc':now(),'new_exit_buffers':[0.,.0025],'matching_fixed_definitions':prior,'fixed':{'L':29,'H':.03,'V':10,'cap':.0275,'capital':3750,'notional':1000,'days':391},'no_market_or_account_calculations':True})
put(R/'prebinding_parameter_guard_verification.json',{'passed':True,'recorded_utc':now(),'old_source':rel(P/'engine.py'),'old_sha256':sha(P/'engine.py'),'new_source':rel(R/'engine.py'),'new_sha256':sha(R/'engine.py'),'exact_only_source_changes':[],'policy_and_money_source_bytes_exactly_unchanged':True,'formulas_and_full_AST_unchanged_after_validation_list_normalization':True,'simulate_and_money_core_bytes_unchanged':True,'synthetic_checks':cases,'synthetic_case_count':len(cases),'before_first_reservation_or_market_calculation':True,'current_evaluation_failures':0,'current_preparation_failures':0})
checked=[]
for f in R.rglob('*.py'):
 tree=ast.parse(f.read_text())
 assert not[n for n in ast.walk(tree) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id in ['ROOT','R','P']],str(f)
 checked.append(rel(f))
put(R/'path_join_guard.json',{'passed':True,'checked':checked,'Path_names_not_subscripted':True,'before_binding_and_evaluation':True,'no_model_or_account_calculations':True})
print('PASS E0/E0.25 planned;engine/core unchanged;synthetic strict/future-prefix cases',len(cases),'0market/account calculations')
