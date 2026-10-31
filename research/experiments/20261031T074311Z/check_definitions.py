import copy,json
from common import *
batch=json.loads((R/'batch.json').read_text());plan=json.loads((R/'plan.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(batch)==12 and len(plan['grid'])==18
for x in batch:
 s=json.loads((ROOT/x['spec']).read_text());w=[x['raw_BTC_weight'],x['raw_ETH_weight']];assert reg.fingerprint(s)==x['fingerprint'] and x['fingerprint'] not in records and [c['weight'] for c in s['components']]==w and s['parameters']['raw_component_multipliers']==w and x['capital_usdt']==10000*sum(w)==s['parameters']['initial_capital_usdt'];assert s['parameters']['component_capitals_usdt']==[10000*z for z in w] and s['parameters']['native_orders_scaled_or_resimulated'] is False
s=copy.deepcopy(json.loads((ROOT/batch[0]['spec']).read_text()));s['components'].reverse();s['name']='metadata-only';assert reg.fingerprint(s)==batch[0]['fingerprint']
for fp,x in plan['read_only_references'].items():assert records[fp]['result_available'] and records[fp]['status']==x['status'] and records[fp]['report_sha256']==x['report_sha256']
binding={rel(p):sha(p) for p in R.glob('*.py') if p.name not in ['commands.py','summarize.py','finalize.py','publish.py']};immutable={rel(CORE_PATH):sha(CORE_PATH)}
for n in ['20261025T145537Z/run.py','20261025T085436Z/run.py','20261026T110637Z/prospective_core.py','20261026T110637Z/prospective_observer.py']:p=ROOT/'research/experiments'/n;immutable[rel(p)]=sha(p)
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':binding,'immutable_source_sha256':immutable,'no_new_financial_valuation_yet':True});put(R/'definition_check.json',{'passed':True,'new_candidates':8,'new_matched_hold_controls':4,'new_native_models':0,'old_actual_centers':2,'old_actual_hold_noncenters':4,'old_native_components':4,'raw_weight_axes':[.5,1,1.5],'no_auto_normalization':True,'financial_evaluations':0});print('PASS12economic-new rawweightdefinitions;6actualgridresults readonly')
