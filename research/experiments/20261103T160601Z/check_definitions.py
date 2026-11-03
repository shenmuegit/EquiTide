import json
from common import *
p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(batch)==18 and len(p['read_only_references'])==10 and sum(x['scope']=='native' for x in batch)==9
allsp={fp:r['spec'] for fp,r in rs.items() if 'spec' in r};allsp.update({x['fingerprint']:json.loads((ROOT/x['spec']).read_text()) for x in batch})
for row in batch:
 sp=allsp[row['fingerprint']];q=sp['parameters'];assert reg.fingerprint(sp)==row['fingerprint'] and row['fingerprint'] not in rs and row['L'] in [7,14,21] and row['H'] in [.01,.02,.03] and row['S']==28 and row['E']==.005
 if row['scope']=='native':assert sp['kind']=='strategy' and q['initial_capital_usdt']==15000 and q['fixed_entry_notional_usdt']==4500 and q['lookback_days']==row['L'] and q['return_hurdle']==q['long_entry_return_hurdle']==row['H'] and q['trend_lookback_days']==28 and q['exit_buffer_fraction']==.005 and q['signal_mode']=='trend_roc_buffered_exit_slowgate_entry_vol' and q['entry_volatility_window_days']==10 and q['entry_volatility_ceiling']==.045
 else:
  assert sp['kind']=='combination' and [x['weight'] for x in sp['components']]==[1,1] and q['initial_capital_usdt']==18750 and q['BTC_entry_notional_usdt']==750 and q['ETH_lookback_days']==row['L'] and q['ETH_return_hurdle']==q['ETH_long_entry_return_hurdle']==q['ETH_short_entry_return_hurdle']==row['H'];assert sum(allsp[x['fingerprint']]['parameters']['initial_capital_usdt'] for x in sp['components'])==18750
for fp,x in p['read_only_references'].items():assert rs[fp]['result_available'] and rs[fp]['status']==x['status'] and rs[fp]['report_sha256']==x['report_sha256'] and sha(ROOT/x['archive'])==x['archive_sha256']
assert sha(R/'engine.py')==p['new_native_policy_implementation']['sha256'];source={rel(x):sha(x) for x in R.glob('*.py') if x.name not in ['commands.py','summarize.py','finalize.py','publish.py']};assert len(source)==33
immutable={rel(CORE_PATH):sha(CORE_PATH)}
for n in ['20261025T145537Z/run.py','20261025T065405Z/engine.py','20261026T070542Z/engine.py','20261103T020232Z/engine.py','20261026T110637Z/prospective_core.py','20261026T110637Z/prospective_observer.py']:
 x=ROOT/'research/experiments'/n;immutable[rel(x)]=sha(x)
for n in ['plan.json','binding.json','core.py','observer.py']:
 x=ROOT/'research/experiments/20261031T174613Z/prospective_l4'/n;immutable[rel(x)]=sha(x)
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':immutable,'no_new_financial_calculation_yet':True,'actual_new_native_models_predeclared':9});put(R/'definition_check.json',{'passed':True,**p['expected_counts'],'two_candidate_axes':['momentumL','symmetricH'],'raw_component_weights':[1,1],'fullbank_source_sum_only':True});print('PASS18newdefinitions/10readonlyresults,9actualnewETHmomenta+9parents;33sourcefiles bound')
