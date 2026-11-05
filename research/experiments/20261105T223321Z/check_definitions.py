"""Bind exact new K3 parameter changes, original accounting and frozen accounts."""
import ast,json
from common import *
p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(batch)==6 and len(p['read_only_references'])==16 and sum(z['scope']=='native' for z in p['read_only_references'].values())==9
assert len(p['grid'])==len(p['native_grid'])==9 and sum(g['readonly'] for g in p['grid'])==sum(g['readonly'] for g in p['native_grid'])==6 and p['slope_lags']==[6,7,8] and p['slope_strengths']==[.01,.02,.03]
allsp={fp:z['spec'] for fp,z in rs.items() if 'spec' in z};allsp.update({x['fingerprint']:json.loads((ROOT/x['spec']).read_text()) for x in batch});newnative={x['fingerprint'] for x in batch if x['scope']=='native'};assert len(newnative)==3
for row in batch:
 sp=allsp[row['fingerprint']];q=sp['parameters'];old=rs[row['reference_fingerprint']]['spec'];oq=old['parameters'];assert reg.fingerprint(sp)==row['fingerprint'] and row['fingerprint'] not in rs and row['D'] in [6,7,8] and row['K']==.03 and row['S']+row['D']<=32 and row['reference_D']==row['D'] and row['reference_K']==.02
 pre='' if row['scope']=='native' else 'ETH_';assert q[pre+'trend_slope_lag_days']==oq[pre+'trend_slope_lag_days']==row['D'] and q[pre+'trend_slope_hurdle_fraction']==.03 and oq[pre+'trend_slope_hurdle_fraction']==.02 and q[pre+'trend_gate_scope']==oq[pre+'trend_gate_scope']=='new_or_reversed_position_only'
 if row['scope']=='native':
  assert sp['kind']=='strategy' and q=={**oq,'trend_slope_hurdle_fraction':.03} and q['initial_capital_usdt']==15000 and q['fixed_entry_notional_usdt']==4500 and q['lookback_days']==5 and q['return_hurdle']==.02 and q['exit_buffer_fraction']==.005 and q['entry_volatility_window_days']==10 and q['entry_volatility_ceiling']==.045 and q['trend_decay_numerator']==23 and q['trend_decay_denominator']==25 and q['trend_window_days']==q['trend_lookback_days']==24
 else:
  assert sp['kind']=='combination' and [x['weight'] for x in sp['components']]==[1,1] and q['initial_capital_usdt']==18750 and q['component_capitals_usdt']==[3750,15000] and q['component_initial_entry_notionals_usdt']==[750,4500] and q['capital_allocation_fractions']==[.2,.8] and sp['components'][0]==old['components'][0] and sp['components'][1]['fingerprint'] in newnative
  expected={**oq,'ETH_trend_slope_hurdle_fraction':.03,'ETH_new_native_quantity_and_impact_computed':True,'actual_native_quantity_and_impact_reused':False,'source_component_spec_sha256':[sha(ROOT/(p['read_only_references'][sp['components'][0]['fingerprint']]['spec'])),sha(ROOT/next(x['spec'] for x in batch if x['fingerprint']==sp['components'][1]['fingerprint']))]};assert q==expected
  b=allsp[sp['components'][0]['fingerprint']]['parameters'];assert b['fixed_entry_notional_usdt']==750 and b['initial_capital_usdt']==3750 and b['lookback_days']==31 and b['return_hurdle']==.04 and b['exit_buffer_fraction']==.01
assert p['rules']['allocation'].startswith('IndependentBTCbank3750/N750 andETHbank15000/N4500,total18750')
for fp,ref in p['read_only_references'].items():
 assert rs[fp]['result_available'] and rs[fp]['status']==ref['status'] and rs[fp]['report_sha256']==ref['report_sha256']
 for k in ['spec','report','archive']:assert sha(ROOT/ref[k])==ref[k+'_sha256']
oldpath=ROOT/'research/experiments/20261105T203116Z/engine.py';fn=lambda t:next(n for n in ast.parse(t).body if isinstance(n,ast.FunctionDef) and n.name=='simulate');assert ast.dump(fn((R/'engine.py').read_text()),include_attributes=False)==ast.dump(fn(oldpath.read_text()),include_attributes=False);assert sha(R/'engine.py')==p['new_engine_sha256']
source={rel(x):sha(x) for x in R.glob('*.py') if x.name not in ['commands.py','summarize.py','finalize.py','publish.py']};assert len(source)==36
immutable={rel(CORE_PATH):sha(CORE_PATH),rel(oldpath):sha(oldpath)}
for n in ['20261025T145537Z/run.py','20261025T065405Z/engine.py','20261026T070542Z/engine.py','20261026T110637Z/prospective_core.py','20261026T110637Z/prospective_observer.py']:
 z=ROOT/'research/experiments'/n;immutable[rel(z)]=sha(z)
for sub,files in [('20261031T174613Z/prospective_l4',['plan.json','binding.json','core.py','observer.py']),('20261104T201939Z/prospective_fewm',['plan.json','binding.json','core.py','observer.py','check.py','readiness.json'])]:
 for name in files:z=ROOT/'research/experiments'/sub/name;immutable[rel(z)]=sha(z)
for folder in {(ROOT/z['report']).parent for z in p['read_only_references'].values()}:
 for z in folder.glob('*.py'):immutable[rel(z)]=sha(z)
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':immutable,'no_new_financial_calculation_yet':True,'actual_new_native_models_predeclared':3,'entire_native_engine_bytes_unchanged':False,'native_simulate_AST_unchanged':True,'maximum_required_context_days':32})
put(R/'definition_check.json',{'passed':True,**p['expected_counts'],'two_candidate_axes':['ETHslopeD','ETHslopeK'],'native_component_axis_count':2,'native_reason':p['sensitivity']['native_reason'],'raw_component_weights':[1,1],'fullbank_source_sum_only':True,'actual_new_quantity_and_impact_required':True,'all_native_paths_readonly':False,'native_simulate_AST_unchanged':True});print('PASS6newdefinitions,3native/3parents,16oldresults/9nativebanks,36sourcesbound; accountingAST/allfrozenaccountbytes unchanged,maxcontext32')
