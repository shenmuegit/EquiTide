"""Independent synthetic formula, policy-entry, sign and prefix checks before reserve."""
import ast,copy,json,math,statistics,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];P=ROOT/'research/experiments/20261116T020401Z';sys.path.insert(0,str(R));from common import *
prior=json.loads((R/'native_blend_prior_lookup.json').read_text())['matching_mechanism_definitions'];assert not any(z['result_available'] or z['status']=='reserved' for z in prior)
funs=lambda p:{n.name:ast.dump(n,include_attributes=False) for n in ast.parse(p.read_text()).body if isinstance(n,ast.FunctionDef)}
before,after=funs(P/'engine.py'),funs(R/'engine.py');assert set(after)-set(before)=={'btc_directional_risk'} and all(after[n]==v for n,v in before.items() if n!='base_decide') and before['base_decide']!=after['base_decide'] and sha(P/'core391_tail_safe.py')==sha(R/'core391_tail_safe.py')
import engine
rs=reg.read_records(ROOT/'research/automation/registry.jsonl');sp=copy.deepcopy(rs['078ecce7a424462c86b0559ffae47e176f267d2841790565d4f092976bd88797']['spec']);cases=[]
# Distinct signed returns make long/short adverse RMS different; future suffix excluded.
returns=[.04,-.01,.02,-.03,.05,.01,-.005,.03,-.02,.01];closes=[100.]*30
for ret in returns:closes.append(closes[-1]*math.exp(ret))
closes+= [7.,11.]
xs=[math.log(closes[j]/closes[j-1]) for j in range(30,40)];sigma=statistics.stdev(xs)
for gamma in [0,.25,.5]:
 for d in [-1,0,1]:
  adverse=math.sqrt(sum((d*x)**2 for x in xs if d*x<0)/10);risk=(1-gamma)*sigma+gamma*adverse;got=engine.btc_directional_risk(closes,40,10,d,gamma);assert math.isclose(got[0],risk,rel_tol=1e-14) and math.isclose(got[1],adverse,rel_tol=1e-14) and got==engine.btc_directional_risk(closes[:40]+[1e15,1],40,10,d,gamma)
  for actual in [-1,0,1]:
   assert engine.entry_filter(d,actual,risk,risk)==d
   assert engine.entry_filter(d,actual,risk+1e-12,risk)==(0 if d and actual!=d else d)
  cases.append({'gamma':gamma,'raw_direction':d,'synthetic_risk':risk,'independent_formula_and_future_prefix_and_strict_entry_hold_checked':True})
assert engine.btc_directional_risk(closes,40,10,1,.5)[1]!=engine.btc_directional_risk(closes,40,10,-1,.5)[1]
# Invoke the actual engine entry, including its precondition guard, with new specs.
for gamma in [.25,.5]:
 q=copy.deepcopy(sp);q['parameters'].update(entry_adverse_volatility_blend=gamma,entry_volatility_estimator='directional_adverse_RMS_blend',entry_adverse_volatility_target_logreturn=0,entry_adverse_volatility_denominator='population_n')
 for actual in [-1,0,1]:
  m={'asset':'BTC','closes':closes};a=engine.base_decide(q,m,40,actual);b=engine.base_decide(q,{'asset':'BTC','closes':closes[:40]+[1e15,1]},40,actual);assert a==b
  raw=a[1]['raw_desired_before_entry_filter'];effective=engine.btc_directional_risk(closes,40,10,raw,gamma)[0];assert a[0]==(0 if raw and raw!=actual and effective>.0275 else raw)
  cases.append({'gamma':gamma,'actual':actual,'real_engine_guard_and_policy_entry_checked':True})
old=module(P/'engine.py','old_policy_for_gamma0_synthetic');plain=engine.base_decide(sp,{'asset':'BTC','closes':closes},40,0);orig=old.base_decide(sp,{'asset':'BTC','closes':closes},40,0);assert plain[0]==orig[0] and all(plain[1][k]==v for k,v in orig[1].items())
put(R/'exact_parameter_registry_screen.json',{'passed':True,'recorded_utc':now(),'new_entry_adverse_blends':[.25,.5],'matching_mechanism_definitions':prior,'fixed':{'L':29,'H':.03,'E':.005,'V':10,'cap':.0275,'capital':3750,'notional':1000,'days':391},'no_market_or_account_calculations':True})
put(R/'prebinding_parameter_guard_verification.json',{'passed':True,'recorded_utc':now(),'old_source':rel(P/'engine.py'),'old_sha256':sha(P/'engine.py'),'new_source':rel(R/'engine.py'),'new_sha256':sha(R/'engine.py'),'intentional_policy_changes':['BTC effective entry vol=(1-gamma)*sample_stdev+gamma*directional_adverse_RMS,target0,population10','BTC policy audit fields retain raw sample vol and separately record effective/adverse vol'],'policy_and_money_source_bytes_exactly_unchanged':False,'money_core_bytes_unchanged':True,'simulate_and_money_core_bytes_unchanged':True,'all_existing_helpers_except_BTC_base_policy_AST_unchanged':True,'synthetic_checks':cases,'before_first_reservation_or_market_calculation':True,'current_evaluation_failures':0,'current_preparation_failures':0})
checked=[]
for p in R.rglob('*.py'):
 tree=ast.parse(p.read_text());assert not[n for n in ast.walk(tree) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id in ['ROOT','R','P']],str(p);checked.append(rel(p))
put(R/'path_join_guard.json',{'passed':True,'checked':checked,'Path_names_not_subscripted':True,'before_binding_and_evaluation':True,'no_model_or_account_calculations':True})
print('PASS new directional formula/sign/boundary/real-entry/future-prefix and gamma0 equivalence synthetic checks;money core and simulate unchanged')
