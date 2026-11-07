"""Bind all new financial definitions and account adapters before first reserve."""
import ast,json
from common import *
p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(batch)==12 and len(p['read_only_references'])==10 and sum(z['scope']=='native' for z in p['read_only_references'].values())==6
assert len(p['grid'])==len(p['native_grid'])==9 and sum(x['readonly'] for x in p['grid'])==sum(x['readonly'] for x in p['native_grid'])==3
for r in batch:
 sp=json.loads((ROOT/r['spec']).read_text());q=sp['parameters'];assert reg.fingerprint(sp)==r['fingerprint'] and r['fingerprint'] not in rs and r['L'] in [23,25,27] and r['H'] in [.03,.04,.05] and r['L'] in [23,25]
 if r['scope']=='native':assert q['initial_capital_usdt']==3750 and q['fixed_entry_notional_usdt']==1000 and q['lookback_days']==r['L'] and q['return_hurdle']==r['H'] and q['exit_buffer_fraction']==.01
 else:
  assert [x['weight'] for x in sp['components']]==[1,1] and q['component_capitals_usdt']==[3750,15000] and q['component_initial_entry_notionals_usdt']==[1000,4500] and q['BTC_lookback_days']==r['L'] and q['BTC_return_hurdle']==r['H']
  assert q['ETH_trend_slope_lag_days']==7 and q['ETH_trend_slope_hurdle_fraction']==.02 and q['ETH_trend_window_days']==24 and q['ETH_entry_volatility_ceiling']==.045
for fp,ref in p['read_only_references'].items():
 assert rs[fp]['result_available'] and rs[fp]['status']==ref['status'] and rs[fp]['report_sha256']==ref['report_sha256']
 for k in ['spec','report','archive']:assert sha(ROOT/ref[k])==ref[k+'_sha256']
old=ROOT/'research/experiments/20261106T083855Z/engine.py';functions=lambda path:{n.name:ast.dump(n,include_attributes=False) for n in ast.parse(path.read_text()).body if isinstance(n,ast.FunctionDef)};a,b=functions(old),functions(R/'engine.py');assert a['simulate']==b['simulate'];assert all(a[k]==b[k] for k in a if k!='decide')
source={rel(x):sha(x) for x in R.glob('*.py') if x.name not in ['commands.py','summarize.py','finalize.py','publish.py']};assert len(source)==36
immutable={rel(CORE_PATH):sha(CORE_PATH),rel(old):sha(old)}
for n in ['20261025T145537Z/run.py','20261025T065405Z/engine.py','20261026T070542Z/engine.py','20261026T110637Z/prospective_core.py','20261026T110637Z/prospective_observer.py','20261011T014626Z/forward.py','20261001T113625Z/signals.py','20261001T013355Z/evaluate.py','20261107T024625Z/forward_inputs.json.gz']:
 z=ROOT/'research/experiments'/n;immutable[rel(z)]=sha(z)
for sub,files in [('20261031T174613Z/prospective_l4',['plan.json','binding.json','core.py','observer.py']),('20261104T201939Z/prospective_fewm',['plan.json','binding.json','core.py','observer.py','check.py','readiness.json'])]:
 for name in files:z=ROOT/'research/experiments'/sub/name;immutable[rel(z)]=sha(z)
for folder in {(ROOT/z['report']).parent for z in p['read_only_references'].values()}:
 for z in folder.glob('*.py'):immutable[rel(z)]=sha(z)
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':immutable,'no_new_financial_calculation_yet':True,'actual_new_native_models_predeclared':6,'native_simulate_AST_unchanged':True,'only_BTC_signal_L_H_parameterization_changed':True,'maximum_required_context_days':31})
put(R/'definition_check.json',{'passed':True,**p['expected_counts'],'two_candidate_axes':['BTClookbackL','BTCentryH'],'native_component_axis_count':2,'raw_component_weights':[1,1],'all_12_specs_unreserved_before_binding':True,'actual_new_quantity_and_impact_required':True,'only_BTC_decide_parameterization_changed':True});print('PASS12newBTCnative/parentdefinitions,10oldresults/6banks,36sourcesbound beforefirstreserve;simulate/frozenaccountsunchanged')
