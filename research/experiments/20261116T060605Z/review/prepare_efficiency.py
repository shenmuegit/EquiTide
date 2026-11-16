"""Exact synthetic path geometry, strict gate, zero-path and prefix tests before reserve."""
import ast,copy,json,sys
from fractions import Fraction as F
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];P=ROOT/'research/experiments/20261116T040504Z';sys.path.insert(0,str(R));from common import *
prior=json.loads((R/'native_efficiency_prior_lookup.json').read_text())['matching_mechanism_definitions']
fixed={'lookback_days':29,'return_hurdle':.03,'exit_buffer_fraction':.005,'entry_volatility_window_days':10,'entry_volatility_ceiling':.0275,'continuous_oos_days':391,'initial_capital_usdt':3750,'fixed_entry_notional_usdt':1000}
exact=[z for z in prior if all(z['parameters'].get(k)==v for k,v in fixed.items()) and z['parameters'].get('entry_path_efficiency_floor') in [.125,.25]];assert not any(z['result_available'] or z['status']=='reserved' for z in exact)
import engine
cases=[]
for values in [[F(100)]*70,[F(100+j) for j in range(70)],[F(200-j) for j in range(70)],[F(100+j%2*3)+F(j,10) for j in range(70)]]:
 i=50;deltas=[values[j]-values[j-1] for j in range(i-29,i)];distance=sum(map(abs,deltas),F(0));ratio=abs(sum(deltas,F(0)))/distance if distance else F(0);assert engine.btc_path_efficiency(values,i,29)==ratio==engine.btc_path_efficiency(values[:i]+[F(10**12),F(1)],i,29) and 0<=ratio<=1
 for floor in [F(0),F('.125'),F('.25')]:
  for raw in [-1,0,1]:
   for actual in [-1,0,1]:
    assert engine.efficiency_filter(raw,actual,floor,floor)==raw and engine.efficiency_filter(raw,actual,floor-F('1e-12'),floor)==(0 if raw and raw!=actual else raw) and engine.efficiency_filter(raw,actual,ratio,floor)==(0 if raw and raw!=actual and ratio<floor else raw)
  cases.append({'floor':str(floor),'independent_exact_ratio':str(ratio),'zero_or_monotone_or_choppy_path_strict_filter_and_prefix_checked':True})
records=reg.read_records(ROOT/'research/automation/registry.jsonl');sp=copy.deepcopy(records['078ecce7a424462c86b0559ffae47e176f267d2841790565d4f092976bd88797']['spec']);values=[F(100+j) for j in range(70)]
old=module(ROOT/'research/experiments/20261116T020401Z/engine.py','old_total_risk_synthetic')
for floor in [0,.125,.25]:
 q=copy.deepcopy(sp)
 if floor:q['parameters'].update(entry_path_efficiency_estimator='absolute_net_price_displacement_over_sum_absolute_daily_price_changes',entry_path_efficiency_floor=floor,entry_path_efficiency_window_days=29,entry_path_efficiency_gate_scope='new_or_reversed_position_only')
 for actual in [-1,0,1]:
  a=engine.base_decide(q,{'asset':'BTC','closes':values},50,actual);assert a==engine.base_decide(q,{'asset':'BTC','closes':values[:50]+[F(10**12),F(1)]},50,actual) and a[0]==1
  if floor==0:
   b=old.base_decide(sp,{'asset':'BTC','closes':values},50,actual);assert a[0]==b[0] and all(a[1][k]==v for k,v in b[1].items())
  cases.append({'floor':floor,'actual':actual,'real_engine_precondition_and_prefix_checked':True,'old_total_risk_equivalence_when_floor0':floor==0})
assert sha(P/'core391_tail_safe.py')==sha(R/'core391_tail_safe.py')
put(R/'exact_parameter_registry_screen.json',{'passed':True,'recorded_utc':now(),'new_path_efficiency_floors':[.125,.25],'fixed':fixed,'broad_prior_related_configurations':len(prior),'related_KAMA_and_ETH_results_preserved_not_equated_to_current_BTC_gate':True,'exact_matching_actual_or_running_configs':len(exact),'no_market_or_account_calculations':True})
put(R/'prebinding_parameter_guard_verification.json',{'passed':True,'recorded_utc':now(),'old_source':rel(P/'engine.py'),'old_sha256':sha(P/'engine.py'),'new_source':rel(R/'engine.py'),'new_sha256':sha(R/'engine.py'),'intentional_policy_changes':['Replace previous adverse-volatility blend research with original total-vol gate plus completed29day net-displacement/path-length entry floor;oldfloor0 readonly','Exact Fraction arithmetic,zero path0,strict below threshold blocks new/reversed only;normal exits and same-direction q retained'],'policy_and_money_source_bytes_exactly_unchanged':False,'money_core_bytes_unchanged':True,'simulate_and_money_core_bytes_unchanged':True,'synthetic_checks':cases,'before_first_reservation_or_market_calculation':True,'current_evaluation_failures':0,'current_preparation_failures':0})
checked=[]
for p in R.rglob('*.py'):
 tree=ast.parse(p.read_text());assert not[n for n in ast.walk(tree) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id in ['ROOT','R','P']],str(p);checked.append(rel(p))
put(R/'path_join_guard.json',{'passed':True,'checked':checked,'Path_names_not_subscripted':True,'before_binding_and_evaluation':True,'no_model_or_account_calculations':True})
print('PASS21 exact path/strict threshold/actual position/real entry/prefix/zero-floor equivalence checks;0 market or account calculations')
