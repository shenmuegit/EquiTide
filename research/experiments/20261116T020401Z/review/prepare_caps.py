"""Check exact novelty, complete entry guards, causal prefixes and unchanged money before reserve."""
import ast,copy,json,math,sys
from fractions import Fraction as F
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];P=ROOT/'research/experiments/20261116T000400Z';sys.path.insert(0,str(R));from common import *
prior=json.loads((R/'native_cap_prior_lookup.json').read_text())['matching_fixed_definitions'];assert prior and not any(z['cap'] in [.02625,.02875] and (z['result_available'] or z['status']=='reserved') for z in prior)
oldcaps='[.0225,.025,.0275,.03,.035,.04,.05]';newcaps='[.0225,.025,.02625,.0275,.02875,.03,.035,.04,.05]';old=(P/'engine.py').read_text();new=(R/'engine.py').read_text();assert old.count(oldcaps)==1 and ast.dump(ast.parse(old.replace(oldcaps,newcaps)),include_attributes=False)==ast.dump(ast.parse(new),include_attributes=False)
assert sha(P/'core391_tail_safe.py')==sha(R/'core391_tail_safe.py')
import engine
records=reg.read_records(ROOT/'research/automation/registry.jsonl');sp=json.loads((ROOT/records['078ecce7a424462c86b0559ffae47e176f267d2841790565d4f092976bd88797']['spec_path']).read_text()) if 'spec_path' in records['078ecce7a424462c86b0559ffae47e176f267d2841790565d4f092976bd88797'] else copy.deepcopy(records['078ecce7a424462c86b0559ffae47e176f267d2841790565d4f092976bd88797']['spec'])
cases=[]
for cap in [.02625,.0275,.02875]:
 spec=copy.deepcopy(sp);spec['parameters']['entry_volatility_ceiling']=cap
 m={'asset':'BTC','closes':[100*math.exp(.002*i) for i in range(60)]}
 for actual in [-1,0,1]:
  a=engine.base_decide(spec,m,40,actual);b=engine.base_decide(spec,{'asset':'BTC','closes':m['closes'][:40]+[10**12,1]},40,actual);assert a==b and a[0]==1
  assert engine.entry_filter(1,0,cap,cap)==1 and engine.entry_filter(1,0,cap+1e-12,cap)==0 and engine.entry_filter(1,1,cap+1e-12,cap)==1
  cases.append({'cap':cap,'actual':actual,'first_real_entry_function_guard_checked':True,'future_suffix_excluded':True,'strict_new_entry_filter_and_same_direction_retention_checked':True})
H=F('.03');E=F('.005')
for actual in [-1,0,1]:
 for roc in [-H-F('1e-8'),-H,-E-F('1e-8'),-E,F(0),E,E+F('1e-8'),H,H+F('1e-8')]:
  closes=[F(200)]*60;closes[39-29]=F(100);closes[39]=100*(1+roc);want=1 if roc>H else -1 if roc<-H else 1 if actual==1 and roc>-E else -1 if actual==-1 and roc<E else 0;got=engine.btc.target(closes,40,29,.03,actual,.005);assert got[0]==want and F(got[1])==roc and got==engine.btc.target(closes[:40]+[F(10**12),F(1)],40,29,.03,actual,.005);cases.append({'fixed_E':str(E),'actual':actual,'ROC':str(roc),'strict_boundary_and_future_prefix_passed':True})
put(R/'exact_parameter_registry_screen.json',{'passed':True,'recorded_utc':now(),'new_entry_volatility_ceilings':[.02625,.02875],'matching_fixed_definitions':prior,'fixed':{'L':29,'H':.03,'E':.005,'V':10,'capital':3750,'notional':1000,'days':391},'no_market_or_account_calculations':True})
put(R/'prebinding_parameter_guard_verification.json',{'passed':True,'recorded_utc':now(),'old_source':rel(P/'engine.py'),'old_sha256':sha(P/'engine.py'),'new_source':rel(R/'engine.py'),'new_sha256':sha(R/'engine.py'),'exact_only_source_changes':[{'old':oldcaps,'new':newcaps,'scope':'predeclared cap assertion allowlist only'}],'policy_and_money_source_bytes_exactly_unchanged':False,'money_core_bytes_unchanged':True,'formulas_and_full_AST_unchanged_after_validation_list_normalization':True,'simulate_and_money_core_bytes_unchanged':True,'synthetic_checks':cases,'before_first_reservation_or_market_calculation':True,'current_evaluation_failures':0,'current_preparation_failures':0})
checked=[]
for p in R.rglob('*.py'):
 tree=ast.parse(p.read_text());assert not[n for n in ast.walk(tree) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id in ['ROOT','R','P']],str(p);checked.append(rel(p))
put(R/'path_join_guard.json',{'passed':True,'checked':checked,'Path_names_not_subscripted':True,'before_binding_and_evaluation':True,'no_model_or_account_calculations':True})
print('PASS2exact new caps,fullengineAST except assertion allowlist,moneycorebytes,36direct/boundary synthetic checks before first reserve')
