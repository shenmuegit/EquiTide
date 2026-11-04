"""Bind actual BTC sizing and parent N/D definitions before first reservation."""
import ast,json
from common import *
p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl')
assert len(batch)==3 and all(x['scope']=='parent' and x['role']=='candidate' and x['N']==625 for x in batch)
assert len(p['read_only_references'])==19 and sum(z['scope']=='native' for z in p['read_only_references'].values())==10 and len(p['grid'])==9 and len(p['native_grid'])==3 and len(p['benchmarks'])==3
allsp={fp:x['spec'] for fp,x in rs.items() if 'spec' in x};allsp.update({x['fingerprint']:json.loads((ROOT/x['spec']).read_text()) for x in batch})
for row in batch:
 sp=allsp[row['fingerprint']];q=sp['parameters'];assert reg.fingerprint(sp)==row['fingerprint'] and row['fingerprint'] not in rs and row['N'] in [500,625,750]
 if row['scope']=='native':
  assert row['N']==1250
  assert sp['kind']=='strategy' and sp['universe']==['BTC/USDT'] and q['initial_capital_usdt']==3750 and q['fixed_entry_notional_usdt']==row['N'] and q['raw_entry_notional_fraction_of_initial_capital']==row['N']/3750
  if row['role'].startswith('benchmark'):assert q['signal_mode']=='constant_long_reference'
  else:assert q['lookback_days']==31 and q['return_hurdle']==.04 and q['exit_buffer_fraction']==.01 and q.get('signal_mode') is None
 else:
  assert sp['kind']=='combination' and [x['weight'] for x in sp['components']]==[1,1] and q['initial_capital_usdt']==18750 and q['component_capitals_usdt']==[3750,15000] and q['component_initial_entry_notionals_usdt']==[row['N'],4500] and q['capital_allocation_fractions']==[.2,.8] and q['BTC_entry_notional_usdt']==row['N']
  assert sum(allsp[x['fingerprint']]['parameters']['initial_capital_usdt'] for x in sp['components'])==18750
  bp,ep=[allsp[x['fingerprint']]['parameters'] for x in sp['components']];assert bp['fixed_entry_notional_usdt']==row['N'] and ep['fixed_entry_notional_usdt']==4500 and sp['components'][1]['fingerprint'] in p['read_only_references']
  if row['role']=='candidate':
   assert row['D']==1 and row['K'] in [.00025,.0005,.00075] and ep['trend_slope_lag_days']==row['D'] and ep['trend_slope_hurdle_fraction']==row['K'] and ep['trend_gate_scope']=='new_or_reversed_position_only' and ep['lookback_days']==5 and ep['return_hurdle']==.02 and ep['exit_buffer_fraction']==.005
   old=allsp[row['reference_fingerprint']];assert old['parameters']['component_initial_entry_notionals_usdt']==[500,4500] and old['components'][1]['fingerprint']==sp['components'][1]['fingerprint']
  else:assert bp['signal_mode']==ep['signal_mode']=='constant_long_reference'
for fp,ref in p['read_only_references'].items():
 assert rs[fp]['result_available'] and rs[fp]['status']==ref['status'] and rs[fp]['report_sha256']==ref['report_sha256']
 for k in ['spec','report','archive']:assert sha(ROOT/ref[k])==ref[k+'_sha256']
assert sum(g['readonly'] for g in p['grid'])==6 and all(g['readonly'] for g in p['native_grid']+p['benchmarks'])
oldpath=ROOT/'research/experiments/20261104T181839Z/engine.py';assert sha(R/'engine.py')==sha(oldpath)==p['new_engine_sha256']
source={rel(x):sha(x) for x in R.glob('*.py') if x.name not in ['commands.py','summarize.py','finalize.py','publish.py']};assert len(source)==33
immutable={rel(CORE_PATH):sha(CORE_PATH),rel(oldpath):sha(oldpath)}
for n in ['20261025T145537Z/run.py','20261025T065405Z/engine.py','20261026T070542Z/engine.py','20261026T110637Z/prospective_core.py','20261026T110637Z/prospective_observer.py']:
 z=ROOT/'research/experiments'/n;immutable[rel(z)]=sha(z)
for n in ['plan.json','binding.json','core.py','observer.py']:
 z=ROOT/'research/experiments/20261031T174613Z/prospective_l4'/n;immutable[rel(z)]=sha(z)
for folder in {(ROOT/z['report']).parent for z in p['read_only_references'].values()}:
 for z in folder.glob('*.py'):immutable[rel(z)]=sha(z)
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':immutable,'no_new_financial_calculation_yet':True,'actual_new_native_models_predeclared':0,'entire_native_engine_bytes_unchanged':True,'native_simulate_AST_unchanged':True,'maximum_required_context_days':32})
put(R/'definition_check.json',{'passed':True,**p['expected_counts'],'two_candidate_axes':['BTCfixedentryN','ETHminimumSlopeK'],'native_component_axis_count':1,'native_reason':p['sensitivity']['native_reason'],'raw_component_weights':[1,1],'fullbank_source_sum_only':True,'actual_new_quantity_and_impact_required':False,'all_native_paths_readonly':True,'entire_engine_bytes_unchanged':True});print('PASS3newparent definitions,0newnative,19readonly results,33sources bound;entire native engine unchanged')
