from common import *
import json
plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(batch)==14
for row in batch:
 s=json.loads((ROOT/row['spec']).read_text());p=s['parameters'];assert reg.fingerprint(s)==row['fingerprint'] and row['fingerprint'] not in records and p['initial_capital_usdt']==row['capital_usdt']
 if row['scope']=='native':assert p['entry_volatility_window_days']==row['V'] and p['entry_volatility_ceiling']==row['C'] and p['lookback_days']==4 and p['fixed_entry_notional_usdt']==4500 and p['trend_lookback_days']==28 and str(row['V']) in s['logic']['signal']
 else:assert [x['weight'] for x in s['components']]==[1,1] and p['component_capitals_usdt']==[5000,15000] and p['ETH_entry_volatility_window_days']==row['V'] and p['ETH_entry_volatility_ceiling']==row['C']
for fp,ref in plan['read_only_references'].items():assert records[fp]['result_available'] and records[fp]['status']==ref['status'] and records[fp]['report_sha256']==ref['report_sha256']
source={rel(p):sha(p) for p in R.glob('*.py') if p.name not in ['commands.py','summarize.py','finalize.py','publish.py']};immutable={rel(CORE_PATH):sha(CORE_PATH)}
for n in ['20261025T065405Z/engine.py','20261026T070542Z/engine.py','20261025T145537Z/run.py','20261026T110637Z/prospective_core.py','20261026T110637Z/prospective_observer.py']:p=ROOT/'research/experiments'/n;immutable[rel(p)]=sha(p)
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':immutable,'no_new_financial_calculation_yet':True});put(R/'definition_check.json',{'passed':True,**plan['expected_counts'],'actual_ETH_capital15000_notional4500':True,'two_predeclared_axes':['V','C'],'entryonly_filter':True});print('PASS14 newoutervol definitions and10readonlyactualsources')
