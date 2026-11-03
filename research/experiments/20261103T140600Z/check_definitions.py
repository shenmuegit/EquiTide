import json
from common import *
p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(batch)==8 and len(p['read_only_references'])==14 and sum(x['scope']=='native' for x in batch)==4
allsp={fp:r['spec'] for fp,r in rs.items() if 'spec' in r};allsp.update({x['fingerprint']:json.loads((ROOT/x['spec']).read_text()) for x in batch})
for row in batch:
 sp=allsp[row['fingerprint']];assert reg.fingerprint(sp)==row['fingerprint'] and row['fingerprint'] not in rs and row['L']==4 and row['S'] in [27,29] and row['E'] in [.00375,.00625]
 q=sp['parameters']
 if row['scope']=='native':assert sp['kind']=='strategy' and q['initial_capital_usdt']==15000 and q['fixed_entry_notional_usdt']==4500 and q['lookback_days']==4 and q['trend_lookback_days']==row['S'] and q['exit_buffer_fraction']==row['E'] and (q['return_hurdle'],q['long_entry_return_hurdle'],q['entry_volatility_window_days'],q['entry_volatility_ceiling'])==(.025,.015,10,.045)
 else:
  assert sp['kind']=='combination' and [z['weight'] for z in sp['components']]==[1,1] and q['initial_capital_usdt']==18750 and q['BTC_entry_notional_usdt']==750 and q['ETH_lookback_days']==4 and q['ETH_trend_lookback_days']==row['S'] and q['ETH_exit_buffer_fraction']==row['E'];assert sum(allsp[z['fingerprint']]['parameters']['initial_capital_usdt'] for z in sp['components'])==18750
for fp,x in p['read_only_references'].items():assert rs[fp]['result_available'] and rs[fp]['status']==x['status'] and rs[fp]['report_sha256']==x['report_sha256'] and sha(ROOT/x['archive'])==x['archive_sha256']
source={rel(x):sha(x) for x in R.glob('*.py') if x.name not in ['commands.py','summarize.py','finalize.py','publish.py']};immutable={rel(CORE_PATH):sha(CORE_PATH)}
for n in ['20261025T145537Z/run.py','20261025T065405Z/engine.py','20261026T070542Z/engine.py','20261103T020232Z/engine.py','20261026T110637Z/prospective_core.py','20261026T110637Z/prospective_observer.py']:
 x=ROOT/'research/experiments'/n;immutable[rel(x)]=sha(x)
for n in ['plan.json','binding.json','core.py','observer.py']:
 x=ROOT/'research/experiments/20261031T174613Z/prospective_l4'/n;immutable[rel(x)]=sha(x)
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':immutable,'no_new_financial_calculation_yet':True,'actual_new_native_models_predeclared':4});put(R/'definition_check.json',{'passed':True,**p['expected_counts'],'two_candidate_axes':['ETHslowS','ETHexitE'],'raw_component_weights':[1,1],'fullbank_source_sum_only':True});print('PASS8newdefinitions/14actualreadonly results,4newnative+4parents;codebound')
