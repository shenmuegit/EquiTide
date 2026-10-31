import json
from common import *
plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(batch)==plan['expected_counts']['new_configs']==20
for row in batch:
 s=json.loads((ROOT/row['spec']).read_text());p=s['parameters'];assert reg.fingerprint(s)==row['fingerprint'] and row['fingerprint'] not in records and p['initial_capital_usdt']==row['capital_usdt']
 if row['scope']=='native':assert p['fixed_entry_notional_usdt']==row['fixed_entry_notional_usdt'] and row['capital_usdt']==10000*row['bank_scale'] and row['fixed_entry_notional_usdt']==(1000 if row['asset']=='BTC' else 3000)*row['bank_scale']
 else:assert [x['weight'] for x in s['components']]==[1,1] and p['raw_bank_scale_coefficients']==[row['raw_BTC_bank_scale'],row['raw_ETH_bank_scale']] and p['initial_capital_usdt']==sum(p['component_capitals_usdt'])
for fp,ref in plan['read_only_references'].items():assert records[fp]['result_available'] and records[fp]['status']==ref['status'] and records[fp]['report_sha256']==ref['report_sha256']
source={rel(p):sha(p) for p in R.glob('*.py') if p.name not in ['commands.py','summarize.py','finalize.py','publish.py']};immutable={rel(CORE_PATH):sha(CORE_PATH)}
for n in ['20261025T065405Z/engine.py','20261026T070542Z/engine.py','20261025T145537Z/run.py','20261026T110637Z/prospective_core.py','20261026T110637Z/prospective_observer.py']:p=ROOT/'research/experiments'/n;immutable[rel(p)]=sha(p)
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':immutable,'no_new_financial_calculation_yet':True});put(R/'definition_check.json',{'passed':True,**plan['expected_counts'],'actual_native_scale_and_order_budget_fixed':True,'parent_children_whole_actual_banks':True,'prior_NAV_interest_model_readonly':True});print('PASS20 new native/parent definitions, raw scales and26readonly sources')
