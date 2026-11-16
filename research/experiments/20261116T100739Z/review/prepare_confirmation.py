"""Synthetic strict directional confirmation and old-gate equivalence checks before reserve."""
import ast,copy,json,sys
from fractions import Fraction as F
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];P=ROOT/'research/experiments/20261116T080637Z';sys.path.insert(0,str(R));from common import *
prior=json.loads((R/'native_confirmation_prior_lookup.json').read_text())['matching_fixed_BTC_definitions'];assert not any(z['parameters'].get('entry_directional_confirmation_lookback_days') in [4,6] and (z['result_available'] or z['status']=='reserved') for z in prior)
import engine
cases=[]
for W in [0,4,5,6]:
 for values in [[F(100)]*70,[F(100+j) for j in range(70)],[F(200-j) for j in range(70)]]:
  i=50;recent=F(values[i-1])/F(values[i-W-1])-1 if W else None;assert engine.btc_confirmation_return(values,i,W)==recent==engine.btc_confirmation_return(values[:i]+[F(10**12),F(1)],i,W)
  for actual in [-1,0,1]:
   for raw in [-1,0,1]:
    expected=0 if raw and raw!=actual and recent is not None and raw*recent<=0 else raw;assert engine.confirmation_filter(raw,actual,recent)==expected
   assert engine.confirmation_filter(1,actual,F(0))==(1 if actual==1 else 0) and engine.confirmation_filter(-1,actual,F(0))==(-1 if actual==-1 else 0)
  cases.append({'W':W,'recent_ROC':str(recent),'strict_zero_boundary_sign_actual_position_future_suffix_checked':True})
rs=reg.read_records(ROOT/'research/automation/registry.jsonl');sp=copy.deepcopy(rs['078ecce7a424462c86b0559ffae47e176f267d2841790565d4f092976bd88797']['spec']);old=module(ROOT/'research/experiments/20261116T020401Z/engine.py','old_total_vol_for_confirmation_synthetic')
for W in [0,4,5,6]:
 q=copy.deepcopy(sp)
 if W:q['parameters'].update(entry_directional_confirmation_lookback_days=W,entry_directional_confirmation_hurdle=0,entry_directional_confirmation_scope='new_or_reversed_position_only',entry_directional_confirmation_rule='strict_positive_direction_times_completed_recent_ROC')
 for sign in [-1,1]:
  values=[F(200+sign*j) for j in range(70)]
  for actual in [-1,0,1]:
   a=engine.base_decide(q,{'asset':'BTC','closes':values},50,actual);assert a==engine.base_decide(q,{'asset':'BTC','closes':values[:50]+[F(10**12),F(1)]},50,actual) and a[0]==sign
   if not W:
    b=old.base_decide(sp,{'asset':'BTC','closes':values},50,actual);assert a[0]==b[0] and all(a[1][k]==v for k,v in b[1].items())
   cases.append({'W':W,'trend':sign,'actual':actual,'real_engine_entry_guard_prefix_and_disabled_equivalence_checked':True})
assert sha(P/'core391_tail_safe.py')==sha(R/'core391_tail_safe.py')
put(R/'exact_parameter_registry_screen.json',{'passed':True,'recorded_utc':now(),'new_confirmation_days':[4,6],'matching_fixed_BTC_definitions_read':len(prior),'exact_matching_actual_or_running_configs':0,'fixed':{'L':29,'H':.03,'E':.005,'V':10,'cap':.0275,'capital':3750,'notional':1000,'days':391},'no_market_or_account_calculations':True})
put(R/'prebinding_parameter_guard_verification.json',{'passed':True,'recorded_utc':now(),'old_source':rel(P/'engine.py'),'old_sha256':sha(P/'engine.py'),'new_source':rel(R/'engine.py'),'new_sha256':sha(R/'engine.py'),'intentional_policy_changes':['Use original total-vol gate plus strict candidate-direction completed4/6day ROC>0 confirmation;same strict recent-direction formula,onlypredeclared4/6allowlist added','Zero recent ROC blocks new/reversed; normal exits and same-direction quantity unchanged;W5 actualoldbank readonly;W0 syntheticdisabled equivalence only'],'policy_and_money_source_bytes_exactly_unchanged':False,'money_core_bytes_unchanged':True,'simulate_and_money_core_bytes_unchanged':True,'synthetic_checks':cases,'before_first_reservation_or_market_calculation':True,'current_evaluation_failures':0,'current_preparation_failures':0})
checked=[]
for p in R.rglob('*.py'):
 tree=ast.parse(p.read_text());assert not[n for n in ast.walk(tree) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id in ['ROOT','R','P']],str(p);checked.append(rel(p))
put(R/'path_join_guard.json',{'passed':True,'checked':checked,'Path_names_not_subscripted':True,'before_binding_and_evaluation':True,'no_model_or_account_calculations':True});print('PASS27 sign/strictzero/new-versus-held/real-entry/causal-prefix/old-disabled-gate synthetic checks;zero market or account valuations')
