import json
from common import *
p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(batch)==6 and len(p['read_only_references'])==16
for row in batch:
 sp=json.loads((ROOT/row['spec']).read_text());assert sp['kind']=='combination' and reg.fingerprint(sp)==row['fingerprint'] and row['fingerprint'] not in rs and row['scope']=='parent' and row['role']=='candidate'
 assert [a['weight'] for a in sp['components']]==[1,1] and sp['parameters']['initial_capital_usdt']==18750 and sp['parameters']['BTC_entry_notional_usdt']==750 and sp['parameters']['ETH_trend_lookback_days']==28 and sp['parameters']['ETH_exit_buffer_fraction']==row['E'] and row['E'] in [.00375,.00625] and sp['parameters']['ETH_lookback_days']==row['L']
 assert sum(rs[a['fingerprint']]['spec']['parameters']['initial_capital_usdt'] for a in sp['components'])==18750 and all(rs[a['fingerprint']]['result_available'] for a in sp['components'])
for fp,x in p['read_only_references'].items():assert rs[fp]['result_available'] and rs[fp]['status']==x['status'] and rs[fp]['report_sha256']==x['report_sha256'] and sha(ROOT/x['archive'])==x['archive_sha256']
source={rel(x):sha(x) for x in R.glob('*.py') if x.name not in ['commands.py','summarize.py','finalize.py','publish.py']};immutable={rel(CORE_PATH):sha(CORE_PATH)}
for n in ['20261025T145537Z/run.py','20261026T110637Z/prospective_core.py','20261026T110637Z/prospective_observer.py']:x=ROOT/'research/experiments'/n;immutable[rel(x)]=sha(x)
for n in ['plan.json','binding.json','core.py','observer.py']:
 x=ROOT/'research/experiments/20261031T174613Z/prospective_l4'/n;immutable[rel(x)]=sha(x)
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':immutable,'no_new_financial_calculation_yet':True,'no_current_native_engine_or_new_source_simulation':True});put(R/'definition_check.json',{'passed':True,**p['expected_counts'],'two_candidate_axes':['ETHfastL','ETHexitE'],'raw_component_weights':[1,1],'fullbank_source_sum_only':True});print('PASS6new parent definitions,16immutable results,0newnative models;code bound')
