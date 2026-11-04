"""Exact causal S/D slope definitions, readonly controls and code binding before reserve."""
import ast,json
from common import *
p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(batch)==18 and len(p['read_only_references'])==8 and sum(z['scope']=='native' for z in p['read_only_references'].values())==5 and sum(z['scope']=='native' for z in batch)==9
assert len(p['grid'])==len(p['native_grid'])==9 and not any(g['readonly'] for g in p['grid']+p['native_grid']);allsp={fp:x['spec'] for fp,x in rs.items() if 'spec' in x};allsp.update({x['fingerprint']:json.loads((ROOT/x['spec']).read_text()) for x in batch})
for row in batch:
 sp=allsp[row['fingerprint']];q=sp['parameters'];assert reg.fingerprint(sp)==row['fingerprint'] and row['fingerprint'] not in rs and row['L']==5 and row['H']==.02 and row['E']==.005 and row['S'] in [16,24,28] and row['D'] in [1,3,5] and row['S']+row['D']<=33
 if row['scope']=='native':
  assert sp['kind']=='strategy' and q['initial_capital_usdt']==15000 and q['fixed_entry_notional_usdt']==4500 and q['lookback_days']==5 and q['return_hurdle']==q['long_entry_return_hurdle']==q['short_entry_return_hurdle']==.02 and q['trend_lookback_days']==q['trend_window_days']==row['S'] and q['trend_decay_numerator']==row['S']-1 and q['trend_decay_denominator']==row['S']+1 and q['trend_slope_lag_days']==row['D'] and q['trend_estimator']=='finite_normalized_exponentially_weighted_mean_slope' and q['exit_buffer_fraction']==.005 and q['entry_volatility_window_days']==10 and q['entry_volatility_ceiling']==.045
 else:
  assert sp['kind']=='combination' and [x['weight'] for x in sp['components']]==[1,1] and q['initial_capital_usdt']==18750 and q['component_capitals_usdt']==[3750,15000] and q['component_initial_entry_notionals_usdt']==[500,4500] and q['capital_allocation_fractions']==[.2,.8] and q['ETH_lookback_days']==5 and q['ETH_return_hurdle']==.02 and q['ETH_exit_buffer_fraction']==.005 and q['ETH_trend_lookback_days']==q['ETH_trend_window_days']==row['S'] and q['ETH_trend_slope_lag_days']==row['D'] and q['ETH_trend_estimator']=='finite_normalized_exponentially_weighted_mean_slope'
  assert sum(allsp[x['fingerprint']]['parameters']['initial_capital_usdt'] for x in sp['components'])==18750 and sp['components'][0]['fingerprint'] in p['read_only_references'] and sp['components'][1]['fingerprint'] in {z['fingerprint'] for z in batch if z['scope']=='native'}
 assert row['reference_window_S']==(16 if row['S']==16 else 24) and row['reference_window_matched']==(row['S'] in [16,24]) and p['reference_window_by_fingerprint'][row['fingerprint']]==row['reference_window_S']
for fp,ref in p['read_only_references'].items():
 assert rs[fp]['result_available'] and rs[fp]['status']==ref['status'] and rs[fp]['report_sha256']==ref['report_sha256']
 for k in ['spec','report','archive']:assert sha(ROOT/ref[k])==ref[k+'_sha256']
assert sha(R/'engine.py')==p['new_native_policy_implementation']['sha256'];source={rel(x):sha(x) for x in R.glob('*.py') if x.name not in ['commands.py','summarize.py','finalize.py','publish.py']};assert len(source)==33
oldpath=ROOT/'research/experiments/20261104T061335Z/engine.py';fn=lambda s:next(n for n in ast.parse(s).body if isinstance(n,ast.FunctionDef) and n.name=='simulate');assert ast.dump(fn((R/'engine.py').read_text()),include_attributes=False)==ast.dump(fn(oldpath.read_text()),include_attributes=False)
immutable={rel(CORE_PATH):sha(CORE_PATH),rel(oldpath):sha(oldpath)}
for n in ['20261025T145537Z/run.py','20261025T065405Z/engine.py','20261026T070542Z/engine.py','20261026T110637Z/prospective_core.py','20261026T110637Z/prospective_observer.py']:
 z=ROOT/'research/experiments'/n;immutable[rel(z)]=sha(z)
for n in ['plan.json','binding.json','core.py','observer.py']:
 z=ROOT/'research/experiments/20261031T174613Z/prospective_l4'/n;immutable[rel(z)]=sha(z)
for folder in {(ROOT/z['report']).parent for z in p['read_only_references'].values()}:
 for z in folder.glob('*.py'):immutable[rel(z)]=sha(z)
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':immutable,'no_new_financial_calculation_yet':True,'actual_new_native_models_predeclared':9,'native_simulate_AST_unchanged':True,'maximum_required_context_days':33});put(R/'definition_check.json',{'passed':True,**p['expected_counts'],'two_candidate_axes':['EWMwindowS','slopeLagD'],'raw_component_weights':[1,1],'fullbank_source_sum_only':True,'all_current_grid_cells_new':True,'S28_reference_window_difference_explicit':True,'native_simulate_AST_unchanged':True});print('PASS18newS/Ddefinitions,8readonlyresults/5nativebooks,33sourcesbound,maxSplusD33,simulateASTunchanged')
