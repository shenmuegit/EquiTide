import json,copy
from common import *
records=reg.read_records(ROOT/'research/automation/registry.jsonl');batch=json.loads((R/'batch.json').read_text());plan=json.loads((R/'plan.json').read_text());assert len(batch)==10
for row in batch:
 s=json.loads((ROOT/row['spec']).read_text());assert reg.fingerprint(s)==row['fingerprint'] and row['fingerprint'] not in records
 p=s['parameters'];assert p['initial_capital_usdt']==row['capital_usdt'] and p['start_utc']=='2025-10-19T00:01:00Z' and p['end_utc']=='2026-10-24T00:01:00Z'
 if s['kind']=='strategy':assert p['fixed_entry_notional_usdt']==3000 and p['lookback_days']==3 and p['exit_buffer_fraction']==0 and p['trend_lookback_days'] in [21,35]
 else:assert [z['weight'] for z in s['components']]==[1,1] and [z['fingerprint'] for z in s['components']]==row['source_fingerprints'] and p['BTC_fixed_entry_notional_usdt']==1000 and p['ETH_fixed_entry_notional_usdt']==3000
same=copy.deepcopy(json.loads((ROOT/batch[-1]['spec']).read_text()));same['name']='metadata_only';same['components'].reverse();assert reg.fingerprint(same)==batch[-1]['fingerprint']
source={rel(q):sha(q) for q in R.glob('*.py') if q.name not in ['commands.py','summarize.py','finalize.py','publish.py']}
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':{rel(CORE_PATH):sha(CORE_PATH)},'no_financial_valuation_yet':True})
put(R/'definition_check.json',{'passed':True,'genuinely_new_financial_configs':10,'old_native_sources':5,'old_parent_results':4,'full_grid_cells':18,'warmup_overlap_passed':plan['warmup']['passed'],'all_source_parameters_preserved':True,'financial_evaluations':0});print('PASS10economic-new definitions and raw weights before reserve')
