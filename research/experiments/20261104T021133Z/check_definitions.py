import json
from common import *
p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(batch)==9 and len(p['read_only_references'])==23 and sum(z['scope']=='native' for z in p['read_only_references'].values())==13
for row in batch:
 sp=json.loads((ROOT/row['spec']).read_text());q=sp['parameters'];assert reg.fingerprint(sp)==row['fingerprint'] and row['fingerprint'] not in rs and sp['kind']=='combination' and row['L'] in [3,5,7] and row['H'] in [.015,.02,.025] and [x['weight'] for x in sp['components']]==[1,1] and q['initial_capital_usdt']==18750 and q['component_capitals_usdt']==[3750,15000] and q['component_initial_entry_notionals_usdt']==[500,4500] and q['raw_component_multipliers']==[1,1] and q['capital_allocation_fractions']==[.2,.8] and q['ETH_lookback_days']==row['L'] and q['ETH_return_hurdle']==row['H'] and q['ETH_trend_lookback_days']==32 and q['ETH_exit_buffer_fraction']==.005
 for j,x in enumerate(sp['components']):assert x['fingerprint'] in p['read_only_references'] and p['read_only_references'][x['fingerprint']]['scope']=='native' and p['read_only_references'][x['fingerprint']]['capital_usdt']==[3750,15000][j]
for fp,z in p['read_only_references'].items():
 assert rs[fp]['result_available'] and rs[fp]['status']==z['status'] and rs[fp]['report_sha256']==z['report_sha256']
 for k in ['spec','report','archive']:assert sha(ROOT/z[k])==z[k+'_sha256']
assert not(R/'engine.py').exists();source={rel(x):sha(x) for x in R.glob('*.py') if x.name not in ['commands.py','summarize.py','finalize.py','publish.py']};assert len(source)==32
immutable={rel(CORE_PATH):sha(CORE_PATH)}
for n in ['20261025T145537Z/run.py','20261026T110637Z/prospective_core.py','20261026T110637Z/prospective_observer.py']:
 z=ROOT/'research/experiments'/n;immutable[rel(z)]=sha(z)
for n in ['plan.json','binding.json','core.py','observer.py']:
 z=ROOT/'research/experiments/20261031T174613Z/prospective_l4'/n;immutable[rel(z)]=sha(z)
for folder in {str((ROOT/z['report']).parent) for z in p['read_only_references'].values()}:
 for z in Path(folder).glob('*.py'):immutable[rel(z)]=sha(z)
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':immutable,'no_new_portfolio_valuation_yet':True,'actual_new_native_models_predeclared':0,'actual_readonly_native_models':13});put(R/'definition_check.json',{'passed':True,**p['expected_counts'],'two_candidate_axes':['ETHreversalL','symmetricH'],'raw_component_weights':[1,1],'fullbank_source_sum_only':True,'no_new_native_engine':True});print('PASS9newportfolio definitions,23readonlyresults/13nativebooks;32sourcefiles bound')
