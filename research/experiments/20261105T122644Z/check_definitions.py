"""Bind all9 financial definitions and unchanged sources before any reservation."""
import ast,json
from common import *
p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(batch)==9 and len(p['read_only_references'])==23 and sum(z['scope']=='native' for z in p['read_only_references'].values())==13
assert len(p['grid'])==len(p['native_grid'])==9 and sum(g['readonly'] for g in p['grid'])==0 and all(g['readonly'] for g in p['native_grid']+p['benchmarks']) and len(p['benchmarks'])==1
for row in batch:
 sp=json.loads((ROOT/row['spec']).read_text());q=sp['parameters'];assert reg.fingerprint(sp)==row['fingerprint'] and row['fingerprint'] not in rs and row['scope']=='parent' and row['role']=='candidate' and row['N']==375 and row['D'] in [1,3,5] and row['K'] in [.00025,.0005,.00075]
 assert q['actual_native_quantity_and_impact_reused'] is True and q['ETH_new_native_quantity_and_impact_computed'] is False
 assert sp['kind']=='combination' and [x['weight'] for x in sp['components']]==[1,1] and q['initial_capital_usdt']==18750 and q['component_capitals_usdt']==[3750,15000] and q['component_initial_entry_notionals_usdt']==[375,4500] and q['capital_allocation_fractions']==[.2,.8] and q['BTC_entry_notional_usdt']==375
 b,e=[rs[x['fingerprint']]['spec']['parameters'] for x in sp['components']];assert b['initial_capital_usdt']==3750 and b['fixed_entry_notional_usdt']==375 and b['lookback_days']==31 and b['return_hurdle']==.04 and b['exit_buffer_fraction']==.01
 assert e['initial_capital_usdt']==15000 and e['fixed_entry_notional_usdt']==4500 and e['lookback_days']==5 and e['return_hurdle']==.02 and e['exit_buffer_fraction']==.005 and e['trend_lookback_days']==24 and e['trend_slope_lag_days']==row['D'] and e['trend_slope_hurdle_fraction']==row['K'] and e['trend_gate_scope']=='new_or_reversed_position_only' and e['entry_volatility_window_days']==10 and e['entry_volatility_ceiling']==.045
 old=rs[row['reference_fingerprint']]['spec'];assert old['parameters']['component_initial_entry_notionals_usdt']==[250,4500] and old['components'][1]==sp['components'][1] and all(rs[x['fingerprint']]['result_available'] for x in sp['components'])
for fp,ref in p['read_only_references'].items():
 assert rs[fp]['result_available'] and rs[fp]['status']==ref['status'] and rs[fp]['report_sha256']==ref['report_sha256']
 for k in ['spec','report','archive']:assert sha(ROOT/ref[k])==ref[k+'_sha256']
oldpath=ROOT/'research/experiments/20261105T102543Z/engine.py';assert sha(R/'engine.py')==sha(oldpath)==p['new_engine_sha256'];source={rel(x):sha(x) for x in R.glob('*.py') if x.name not in ['commands.py','summarize.py','finalize.py','publish.py']};assert len(source)==36
immutable={rel(CORE_PATH):sha(CORE_PATH),rel(oldpath):sha(oldpath)}
for n in ['20261025T145537Z/run.py','20261025T065405Z/engine.py','20261026T070542Z/engine.py','20261026T110637Z/prospective_core.py','20261026T110637Z/prospective_observer.py']:
 z=ROOT/'research/experiments'/n;immutable[rel(z)]=sha(z)
for sub,files in [('20261031T174613Z/prospective_l4',['plan.json','binding.json','core.py','observer.py']),('20261104T201939Z/prospective_fewm',['plan.json','binding.json','core.py','observer.py','check.py','readiness.json'])]:
 for name in files:z=ROOT/'research/experiments'/sub/name;immutable[rel(z)]=sha(z)
for folder in {(ROOT/z['report']).parent for z in p['read_only_references'].values()}:
 for z in folder.glob('*.py'):immutable[rel(z)]=sha(z)
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':immutable,'no_new_financial_calculation_yet':True,'actual_new_native_models_predeclared':0,'entire_native_engine_bytes_unchanged':True,'native_simulate_AST_unchanged':True,'maximum_required_context_days':32})
put(R/'definition_check.json',{'passed':True,**p['expected_counts'],'two_candidate_axes':['ETHslopeD','ETHslopeK'],'native_component_axis_count':2,'native_reason':p['sensitivity']['native_reason'],'raw_component_weights':[1,1],'fullbank_source_sum_only':True,'actual_new_quantity_and_impact_required':False,'all_native_paths_readonly':True,'entire_engine_bytes_unchanged':True});print('PASS9newparentD/Kdefinitions,23oldresults/13nativebanks,36sources bound;engine andallfrozenaccounts unchanged')
