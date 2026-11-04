"""Exact S/E new definitions and old-cell continuity before reserve/valuation."""
import ast,json
from common import *
p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(batch)==16 and len(p['read_only_references'])==6 and sum(x['scope']=='native' for x in p['read_only_references'].values())==4 and sum(x['scope']=='native' for x in batch)==8
assert len(p['grid'])==len(p['native_grid'])==9 and sum(g['readonly'] for g in p['grid'])==sum(g['readonly'] for g in p['native_grid'])==1
allsp={fp:x['spec'] for fp,x in rs.items() if 'spec' in x};allsp.update({x['fingerprint']:json.loads((ROOT/x['spec']).read_text()) for x in batch})
for row in batch:
 sp=allsp[row['fingerprint']];q=sp['parameters'];assert reg.fingerprint(sp)==row['fingerprint'] and row['fingerprint'] not in rs and row['L']==5 and row['H']==.02 and row['S'] in [16,24,32] and row['E'] in [.00375,.005,.00625] and (row['S'],row['E'])!=(32,.005)
 if row['scope']=='native':
  assert sp['kind']=='strategy' and q['initial_capital_usdt']==15000 and q['fixed_entry_notional_usdt']==4500 and q['lookback_days']==5 and q['return_hurdle']==q['long_entry_return_hurdle']==q['short_entry_return_hurdle']==.02 and q['trend_lookback_days']==q['trend_window_days']==row['S'] and q['trend_decay_numerator']==row['S']-1 and q['trend_decay_denominator']==row['S']+1 and q['trend_estimator']=='finite_normalized_exponentially_weighted_mean_level' and q['exit_buffer_fraction']==row['E'] and q['entry_volatility_window_days']==10 and q['entry_volatility_ceiling']==.045
 else:
  assert sp['kind']=='combination' and [x['weight'] for x in sp['components']]==[1,1] and q['initial_capital_usdt']==18750 and q['component_capitals_usdt']==[3750,15000] and q['component_initial_entry_notionals_usdt']==[500,4500] and q['capital_allocation_fractions']==[.2,.8] and q['ETH_lookback_days']==5 and q['ETH_return_hurdle']==.02 and q['ETH_trend_lookback_days']==q['ETH_trend_window_days']==row['S'] and q['ETH_trend_decay_numerator']==row['S']-1 and q['ETH_trend_decay_denominator']==row['S']+1 and q['ETH_exit_buffer_fraction']==row['E']
  assert sum(allsp[x['fingerprint']]['parameters']['initial_capital_usdt'] for x in sp['components'])==18750 and sp['components'][0]['fingerprint'] in p['read_only_references'] and sp['components'][1]['fingerprint'] in {x['fingerprint'] for x in batch if x['scope']=='native'}
for fp,ref in p['read_only_references'].items():
 assert rs[fp]['result_available'] and rs[fp]['status']==ref['status'] and rs[fp]['report_sha256']==ref['report_sha256']
 for k in ['spec','report','archive']:assert sha(ROOT/ref[k])==ref[k+'_sha256']
for g in p['grid']+p['native_grid']:
 if g['readonly']:assert g['fingerprint'] in rs and rs[g['fingerprint']]['result_available'] and g['S']==32 and g['E']==.005
assert sha(R/'engine.py')==p['new_native_policy_implementation']['sha256'];source={rel(x):sha(x) for x in R.glob('*.py') if x.name not in ['commands.py','summarize.py','finalize.py','publish.py']};assert len(source)==33
oldpath=ROOT/'research/experiments/20261104T041304Z/engine.py';fn=lambda t:next(n for n in ast.parse(t).body if isinstance(n,ast.FunctionDef) and n.name=='simulate');assert ast.dump(fn((R/'engine.py').read_text()),include_attributes=False)==ast.dump(fn(oldpath.read_text()),include_attributes=False)
immutable={rel(CORE_PATH):sha(CORE_PATH),rel(oldpath):sha(oldpath)}
for n in ['20261025T145537Z/run.py','20261025T065405Z/engine.py','20261026T070542Z/engine.py','20261026T110637Z/prospective_core.py','20261026T110637Z/prospective_observer.py']:
 x=ROOT/'research/experiments'/n;immutable[rel(x)]=sha(x)
for n in ['plan.json','binding.json','core.py','observer.py']:
 x=ROOT/'research/experiments/20261031T174613Z/prospective_l4'/n;immutable[rel(x)]=sha(x)
for folder in {(ROOT/x['report']).parent for x in p['read_only_references'].values()}:
 for x in folder.glob('*.py'):immutable[rel(x)]=sha(x)
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':immutable,'no_new_financial_calculation_yet':True,'actual_new_native_models_predeclared':8,'old_native_parent_grid_cells_reused':2,'native_simulate_AST_unchanged':True});put(R/'definition_check.json',{'passed':True,**p['expected_counts'],'two_candidate_axes':['EWMwindowS','exitE'],'raw_component_weights':[1,1],'fullbank_source_sum_only':True,'old_grid_cells_not_retested':True,'native_simulate_AST_unchanged':True});print('PASS16newS/Edefinitions,2oldgridcellsreadonly,6oldresults/4nativebooks,33sourcesbound')
