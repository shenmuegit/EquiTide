"""Synthetic exact hurdle/sign/holding/causality tests before any reserve or market calculation."""
import ast,copy,json,sys
from fractions import Fraction as F
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];P=ROOT/'research/experiments/20261116T100739Z';sys.path.insert(0,str(R));from common import *
import engine
prior=json.loads((R/'native_confirmation_prior_lookup.json').read_text())['matching_fixed_BTC_definitions'];assert not any(z['parameters'].get('entry_directional_confirmation_lookback_days')==5 and z['parameters'].get('entry_directional_confirmation_hurdle',0) in [.0025,.005] and (z['result_available'] or z['status']=='reserved') for z in prior)
cases=[]
for A in [F(0),F('.0025'),F('.005')]:
 for raw in [-1,0,1]:
  for actual in [-1,0,1]:
   for recent in sorted(set([-A-F('1e-12'),-A,-A+F('1e-12'),F(0),A-F('1e-12'),A,A+F('1e-12')])):
    expected=0 if raw and raw!=actual and raw*recent<=A else raw;got=engine.confirmation_filter(raw,actual,recent,A);assert got==expected;cases.append({'A':str(A),'raw':raw,'actual':actual,'recent_ROC':str(recent),'exact_strict_hurdle_and_same_direction_hold':got})
   assert engine.confirmation_filter(raw,actual,None,A)==raw
rs=reg.read_records(ROOT/'research/automation/registry.jsonl');sp=copy.deepcopy(rs['4820334331e1c14d0a37fcea1453968338ab94aaa9e4a77db68a8289d310a928']['spec']);old=module(P/'engine.py','old_confirmation_zero_hurdle_for_synthetic')
for sign in [-1,1]:
 values=[F(200+sign*j) for j in range(70)];i=50;recent=values[i-1]/values[i-6]-1;assert engine.btc_confirmation_return(values,i,5)==recent==engine.btc_confirmation_return(values[:i]+[F(10**12),F(1)],i,5)
 for actual in [-1,0,1]:
  center=old.base_decide(sp,{'asset':'BTC','closes':values},i,actual)
  for A in [0,.0025,.005]:
   q=copy.deepcopy(sp);q['parameters'].update(entry_directional_confirmation_hurdle=A)
   if A:q['parameters']['entry_directional_confirmation_rule']='strict_direction_times_completed_recent_ROC_above_hurdle'
   got=engine.base_decide(q,{'asset':'BTC','closes':values},i,actual);assert got==engine.base_decide(q,{'asset':'BTC','closes':values[:i]+[F(10**12),F(1)]},i,actual);before=center[1]['raw_desired_before_confirmation_filter'];expected=0 if before and before!=actual and before*recent<=F(str(A)) else before;assert got[0]==expected
   if A==0:assert got[0]==center[0] and all(got[1][k]==v for k,v in center[1].items())
   cases.append({'A':A,'trend':sign,'actual':actual,'real_engine_entry_gate_prefix_and_old_zero_hurdle_equivalence_checked':True})
assert sha(P/'core391_tail_safe.py')==sha(R/'core391_tail_safe.py')
put(R/'exact_parameter_registry_screen.json',{'passed':True,'recorded_utc':now(),'new_confirmation_hurdles':[.0025,.005],'confirmation_days_fixed':5,'matching_fixed_BTC_definitions_read':len(prior),'exact_matching_actual_or_running_configs':0,'fixed':{'L':29,'H':.03,'E':.005,'V':10,'cap':.0275,'capital':3750,'notional':1000,'days':391},'no_market_or_account_calculations':True})
put(R/'prebinding_parameter_guard_verification.json',{'passed':True,'recorded_utc':now(),'old_source':rel(P/'engine.py'),'old_sha256':sha(P/'engine.py'),'new_source':rel(R/'engine.py'),'new_sha256':sha(R/'engine.py'),'intentional_policy_changes':['Strict fixed5day directionalROC>minimum25/50bp on new/reversed entries only;oldzero exact readonly bank retained','Equality blocks new/reversed;normal exits/same-direction quantities,totalvol gate and all money kernels unchanged'],'policy_and_money_source_bytes_exactly_unchanged':False,'money_core_bytes_unchanged':True,'simulate_and_money_core_bytes_unchanged':True,'synthetic_checks':cases,'before_first_reservation_or_market_calculation':True,'current_evaluation_failures':0,'current_preparation_failures':1})
checked=[]
for p in R.rglob('*.py'):
 tree=ast.parse(p.read_text());assert not[n for n in ast.walk(tree) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id in ['ROOT','R','P']],str(p);checked.append(rel(p))
put(R/'path_join_guard.json',{'passed':True,'checked':checked,'Path_names_not_subscripted':True,'before_binding_and_evaluation':True,'no_model_or_account_calculations':True});print('PASS',len(cases),'synthetic strictminimum/sign/holding/futureprefix/oldzero equivalence cases;0market/account valuations')
