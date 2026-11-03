import json
from common import *
p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(batch)==12 and sum(x['role']=='candidate' for x in batch)==6 and sum(x['scope']=='native' for x in batch)==4
allsp={fp:z['spec'] for fp,z in rs.items() if 'spec' in z};allsp.update({x['fingerprint']:json.loads((ROOT/x['spec']).read_text()) for x in batch})
for row in batch:
 sp=allsp[row['fingerprint']];assert reg.fingerprint(sp)==row['fingerprint'] and row['fingerprint'] not in rs
 if row['scope']=='parent':
  assert [x['weight'] for x in sp['components']]==[1,1] and sum(allsp[fp]['parameters']['initial_capital_usdt'] for fp in row['source_fingerprints'])==row['capital_usdt']==18750
  assert sp['parameters']['BTC_entry_notional_usdt']==row['N'] and sp['parameters']['component_initial_entry_notionals_usdt']==[row['N'],4500]
 else:
  q=sp['parameters'];assert q['initial_capital_usdt']==3750 and q['fixed_entry_notional_usdt']==row['N'] and row['N'] in [250,500] and q['raw_entry_notional_fraction_of_initial_capital']==row['N']/3750
  assert sp['universe']==['BTC/USDT'] and ('signal_mode' in q if row['role'].startswith('benchmark') else q['lookback_days']==31 and q['return_hurdle']==.04 and q['exit_buffer_fraction']==.01)
for g in p['native_grid']:
 if g['readonly']:assert allsp[g['fingerprint']]['parameters']['fixed_entry_notional_usdt']==g['N']==375
for fp,x in p['read_only_references'].items():assert rs[fp]['result_available'] and rs[fp]['status']==x['status'] and rs[fp]['report_sha256']==x['report_sha256'] and sha(ROOT/x['archive'])==x['archive_sha256']
source={rel(x):sha(x) for x in R.glob('*.py') if x.name not in ['commands.py','summarize.py','finalize.py','publish.py']};immutable={rel(CORE_PATH):sha(CORE_PATH)}
for n in ['20261025T145537Z/run.py','20261026T110637Z/prospective_core.py','20261026T110637Z/prospective_observer.py']:x=ROOT/'research/experiments'/n;immutable[rel(x)]=sha(x)
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':immutable,'no_new_financial_calculation_yet':True});put(R/'definition_check.json',{'passed':True,**p['expected_counts'],'two_candidate_axes':['ETHfastL','BTCfixedentryN'],'native_component_axis_count':1,'native_reason':p['sensitivity']['native_reason'],'raw_component_weights':[1,1],'actual_new_quantity_and_impact_required':True});print('PASS12new definitions,4actual BTC banks,8parent paths,10oldreadonly results;code bound')
