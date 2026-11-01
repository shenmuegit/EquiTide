import json
from common import *
p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(batch)==12 and sum(x['role']=='candidate' for x in batch)==6
allsp={fp:z['spec'] for fp,z in rs.items() if 'spec' in z};allsp.update({x['fingerprint']:json.loads((ROOT/x['spec']).read_text()) for x in batch})
for row in batch:
 sp=allsp[row['fingerprint']];assert reg.fingerprint(sp)==row['fingerprint'] and row['fingerprint'] not in rs
 if row['scope']=='parent':
  assert len(sp['components'])==2 and [x['weight'] for x in sp['components']]==[1,1] and sum(allsp[fp]['parameters']['initial_capital_usdt'] for fp in row['source_fingerprints'])==row['capital_usdt']
 else:assert sp['parameters']['initial_capital_usdt']==row['capital_usdt']==15000 and sp['parameters']['fixed_entry_notional_usdt']==4500 and sp['parameters']['trend_lookback_days']==28 and sp['parameters']['btc_return_control_weight'] in [.5,1] and sp['parameters']['benchmark_asset']=='BTC/USDT' and sp['parameters']['lookback_days'] in [3,4,5]
for fp,x in p['read_only_references'].items():assert rs[fp]['result_available'] and rs[fp]['status']==x['status'] and rs[fp]['report_sha256']==x['report_sha256'] and sha(ROOT/x['archive'])==x['archive_sha256']
source={rel(x):sha(x) for x in R.glob('*.py') if x.name not in ['commands.py','summarize.py','finalize.py','publish.py']};immutable={rel(CORE_PATH):sha(CORE_PATH)}
for n in ['20261025T145537Z/run.py','20261026T110637Z/prospective_core.py','20261026T110637Z/prospective_observer.py']:x=ROOT/'research/experiments'/n;immutable[rel(x)]=sha(x)
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':immutable,'no_new_financial_calculation_yet':True});put(R/'definition_check.json',{'passed':True,**p['expected_counts'],'actual_native_source_quantity_not_linear_scaling':True,'two_axes':['ETHlookbackL','BTCreturnControlA'],'raw_component_weights':[1,1]});print('PASS12newdefinitions/10immutable sources,6newnative;codebound')
