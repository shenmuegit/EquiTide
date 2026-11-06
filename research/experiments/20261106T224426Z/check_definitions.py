"""Bind novel parent graphs and all unchanged native books before first valuation."""
import ast,json
from common import *
p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(batch)==12 and len(p['read_only_references'])==30 and sum(x['scope']=='native' for x in p['read_only_references'].values())==14
assert len(p['grid'])==27 and len(p['native_grid'])==9 and sum(g['readonly'] for g in p['grid'])==15 and all(g['readonly'] for g in p['native_grid']);assert p['BTC_hurdles']==[.03,.04,.05] and p['fixed_ETH_K']==.02
for row in batch:
 sp=json.loads((ROOT/row['spec']).read_text());q=sp['parameters'];assert reg.fingerprint(sp)==row['fingerprint'] and row['fingerprint'] not in rs and row['scope']=='parent' and row['role']=='candidate' and row['BTC_H'] in [.03,.05] and row['D'] in [6,7,8] and row['VC'] in [.04,.05] and row['K']==.02
 assert [x['weight'] for x in sp['components']]==[1,1] and q['component_capitals_usdt']==[3750,15000] and q['component_initial_entry_notionals_usdt']==[1000,4500] and q['BTC_lookback_days']==29 and q['BTC_return_hurdle']==row['BTC_H'] and q['ETH_entry_volatility_ceiling']==row['VC'] and q['actual_native_quantity_and_impact_reused'] and not q['ETH_new_native_quantity_and_impact_computed'] and not q['BTC_new_native_quantity_and_impact_computed']
 b,e=[rs[x['fingerprint']]['spec']['parameters'] for x in sp['components']];assert b['initial_capital_usdt']==3750 and b['fixed_entry_notional_usdt']==1000 and b['lookback_days']==29 and b['return_hurdle']==row['BTC_H'] and e['initial_capital_usdt']==15000 and e['fixed_entry_notional_usdt']==4500 and e['lookback_days']==5 and e['return_hurdle']==.02 and e['exit_buffer_fraction']==.005 and e['trend_slope_hurdle_fraction']==.02 and e['entry_volatility_ceiling']==row['VC'] and e['trend_slope_lag_days']==row['D']
 ref=rs[row['reference_fingerprint']]['spec'];assert ref['parameters']['BTC_return_hurdle']==.04 and ref['components'][1]['fingerprint']==sp['components'][1]['fingerprint']
for fp,z in p['read_only_references'].items():
 assert rs[fp]['result_available'] and rs[fp]['status']==z['status'] and rs[fp]['report_sha256']==z['report_sha256']
 for k in ['spec','report','archive']:assert sha(ROOT/z[k])==z[k+'_sha256']
old=ROOT/'research/experiments/20261106T204429Z/engine.py';assert old.read_bytes()==(R/'engine.py').read_bytes() and sha(R/'engine.py')==p['new_engine_sha256']
source={rel(f):sha(f) for f in R.glob('*.py') if f.name not in ['commands.py','summarize.py','finalize.py','publish.py']};assert len(source)==36
immutable={rel(CORE_PATH):sha(CORE_PATH),rel(old):sha(old)}
for n in ['20261025T145537Z/run.py','20261025T065405Z/engine.py','20261026T070542Z/engine.py','20261026T110637Z/prospective_core.py','20261026T110637Z/prospective_observer.py','20261011T014626Z/forward.py','20261001T113625Z/signals.py','20261001T013355Z/evaluate.py','20261106T023552Z/forward_inputs.json.gz']:
 f=ROOT/'research/experiments'/n;immutable[rel(f)]=sha(f)
for sub,files in [('20261031T174613Z/prospective_l4',['plan.json','binding.json','core.py','observer.py']),('20261104T201939Z/prospective_fewm',['plan.json','binding.json','core.py','observer.py','check.py','readiness.json'])]:
 for name in files:f=ROOT/'research/experiments'/sub/name;immutable[rel(f)]=sha(f)
for folder in {(ROOT/z['report']).parent for z in p['read_only_references'].values()}:
 for f in folder.glob('*.py'):immutable[rel(f)]=sha(f)
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':immutable,'no_new_financial_calculation_yet':True,'actual_new_native_models_predeclared':0,'native_simulate_AST_unchanged':True,'entire_engine_byte_unchanged':True,'maximum_required_context_days':32});put(R/'definition_check.json',{'passed':True,**p['expected_counts'],'three_candidate_axes':['BTC_H','ETH_D','ETH_VC'],'raw_weights':[1,1],'native_accounting_unchanged':True,'old_baseline_qualifications_readonly':True});print('PASS12newparentgraphs/27H-D-VCcells,30oldresults/14banks,36sourcesboundbeforefirstreserve')
