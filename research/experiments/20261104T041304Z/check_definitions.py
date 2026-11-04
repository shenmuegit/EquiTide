"""Exact new finite-EWM definitions, immutable actual controls and code binding."""
import ast,json
from common import *
p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(batch)==18 and len(p['read_only_references'])==22 and sum(x['scope']=='native' for x in p['read_only_references'].values())==12 and sum(x['scope']=='native' for x in batch)==9
allsp={fp:x['spec'] for fp,x in rs.items() if 'spec' in x};allsp.update({x['fingerprint']:json.loads((ROOT/x['spec']).read_text()) for x in batch})
for row in batch:
 sp=allsp[row['fingerprint']];q=sp['parameters'];assert reg.fingerprint(sp)==row['fingerprint'] and row['fingerprint'] not in rs and row['L'] in [3,5,7] and row['H'] in [.015,.02,.025] and row['S']==32 and row['E']==.005
 if row['scope']=='native':
  assert sp['kind']=='strategy' and q['initial_capital_usdt']==15000 and q['fixed_entry_notional_usdt']==4500 and q['lookback_days']==row['L'] and q['return_hurdle']==q['long_entry_return_hurdle']==q['short_entry_return_hurdle']==row['H'] and q['trend_lookback_days']==q['trend_window_days']==32 and q['trend_decay_numerator']==31 and q['trend_decay_denominator']==33 and q['trend_estimator']=='finite_normalized_exponentially_weighted_mean_level' and q['signal_mode']=='finite_EWMlevel_gated_reversal_entry_vol' and q['exit_buffer_fraction']==.005 and q['entry_volatility_window_days']==10 and q['entry_volatility_ceiling']==.045
 else:
  assert sp['kind']=='combination' and [x['weight'] for x in sp['components']]==[1,1] and q['initial_capital_usdt']==18750 and q['component_capitals_usdt']==[3750,15000] and q['component_initial_entry_notionals_usdt']==[500,4500] and q['capital_allocation_fractions']==[.2,.8] and q['ETH_lookback_days']==row['L'] and q['ETH_return_hurdle']==row['H'] and q['ETH_trend_estimator']=='finite_normalized_exponentially_weighted_mean_level' and q['ETH_trend_decay_numerator']==31 and q['ETH_trend_decay_denominator']==33 and q['ETH_trend_window_days']==32
  assert sum(allsp[x['fingerprint']]['parameters']['initial_capital_usdt'] for x in sp['components'])==18750 and sp['components'][0]['fingerprint'] in p['read_only_references'] and sp['components'][1]['fingerprint'] in {x['fingerprint'] for x in batch if x['scope']=='native'}
 old=p['read_only_references'][row['old_estimator_fingerprint']];assert old['scope']==row['scope'] and old['capital_usdt']==row['capital_usdt']
for fp,ref in p['read_only_references'].items():
 assert rs[fp]['result_available'] and rs[fp]['status']==ref['status'] and rs[fp]['report_sha256']==ref['report_sha256']
 for k in ['spec','report','archive']:assert sha(ROOT/ref[k])==ref[k+'_sha256']
assert sha(R/'engine.py')==p['new_native_policy_implementation']['sha256'];source={rel(x):sha(x) for x in R.glob('*.py') if x.name not in ['commands.py','summarize.py','finalize.py','publish.py']};assert len(source)==33
oldpath=ROOT/'research/experiments/20261103T200934Z/engine.py';fn=lambda t:next(n for n in ast.parse(t).body if isinstance(n,ast.FunctionDef) and n.name=='simulate');assert ast.dump(fn((R/'engine.py').read_text()),include_attributes=False)==ast.dump(fn(oldpath.read_text()),include_attributes=False)
immutable={rel(CORE_PATH):sha(CORE_PATH),rel(oldpath):sha(oldpath)}
for n in ['20261025T145537Z/run.py','20261025T065405Z/engine.py','20261026T070542Z/engine.py','20261026T110637Z/prospective_core.py','20261026T110637Z/prospective_observer.py']:
 x=ROOT/'research/experiments'/n;immutable[rel(x)]=sha(x)
for n in ['plan.json','binding.json','core.py','observer.py']:
 x=ROOT/'research/experiments/20261031T174613Z/prospective_l4'/n;immutable[rel(x)]=sha(x)
for folder in {(ROOT/x['report']).parent for x in p['read_only_references'].values()}:
 for x in folder.glob('*.py'):immutable[rel(x)]=sha(x)
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':immutable,'no_new_financial_calculation_yet':True,'actual_new_native_models_predeclared':9,'native_simulate_AST_unchanged':True});put(R/'definition_check.json',{'passed':True,**p['expected_counts'],'two_candidate_axes':['reversalL','symmetricH'],'raw_component_weights':[1,1],'time_signal_kernel_normalization_is_not_portfolio_normalization':True,'fullbank_source_sum_only':True,'native_simulate_AST_unchanged':True});print('PASS18new finiteEWM definitions,22readonlyresults/12nativebooks,33sourcesbound;simulateASTunchanged')
