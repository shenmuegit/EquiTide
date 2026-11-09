"""Verify all L/E definitions and bind complete financial/observation source bytes before reserve."""
import ast,json
from common import *
p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(batch)==12 and len(p['read_only_references'])==10 and sum(z['scope']=='native' for z in p['read_only_references'].values())==6
assert len(p['grid'])==len(p['native_grid'])==9 and sum(x['readonly'] for x in p['grid'])==sum(x['readonly'] for x in p['native_grid'])==3
assert p['fast_lookbacks']==[4,5,6] and p['exit_buffers']==[.00625,.0075,.00875] and p['slope_strengths']==[.0075] and p['slope_lags']==[3] and p['entry_hurdles']==[.02] and p['slow_windows']==[16] and p['volatility_ceilings']==[.05]
for r in batch:
 sp=json.loads((ROOT/r['spec']).read_text());q=sp['parameters'];assert reg.fingerprint(sp)==r['fingerprint'] and r['fingerprint'] not in rs and r['L'] in [4,6] and r['E'] in [.00625,.0075,.00875] and r['K']==.0075 and r['D']==3 and r['VC']==.05 and r['H']==.02 and r['S']==16
 if r['scope']=='native':
  oq=rs[r['reference_fingerprint']]['spec']['parameters'];assert q=={**oq,'lookback_days':r['L']} and q['initial_capital_usdt']==15000 and q['fixed_entry_notional_usdt']==4500 and q['lookback_days']==r['L'] and q['return_hurdle']==q['long_entry_return_hurdle']==q['short_entry_return_hurdle']==.02 and q['exit_buffer_fraction']==r['E'] and q['entry_volatility_ceiling']==.05 and q['trend_slope_lag_days']==3 and q['trend_slope_hurdle_fraction']==.0075 and q['trend_lookback_days']==q['trend_window_days']==16 and q['trend_decay_numerator']==15 and q['trend_decay_denominator']==17 and q['trend_gate_scope']=='new_or_reversed_position_only' and q['entry_volatility_window_days']==10
 else:
  assert [x['weight'] for x in sp['components']]==[1,1] and q['component_capitals_usdt']==[3750,15000] and q['component_initial_entry_notionals_usdt']==[1000,4500] and q['BTC_lookback_days']==29 and q['BTC_return_hurdle']==.03 and q['BTC_exit_buffer_fraction']==.01
  assert q['ETH_lookback_days']==r['L'] and q['ETH_exit_buffer_fraction']==r['E'] and q['ETH_entry_volatility_ceiling']==.05 and q['ETH_trend_slope_lag_days']==3 and q['ETH_trend_slope_hurdle_fraction']==.0075 and q['ETH_trend_lookback_days']==q['ETH_trend_window_days']==16
for fp,ref in p['read_only_references'].items():
 assert rs[fp]['result_available'] and rs[fp]['status']==ref['status'] and rs[fp]['report_sha256']==ref['report_sha256']
 for k in ['spec','report','archive']:assert sha(ROOT/ref[k])==ref[k+'_sha256']
old=ROOT/'research/experiments/20261109T170751Z/engine.py';functions=lambda f:{n.name:ast.dump(n,include_attributes=False) for n in ast.parse(f.read_text()).body if isinstance(n,ast.FunctionDef)};a,b=functions(old),functions(R/'engine.py');assert a['simulate']==b['simulate'] and all(a[k]==b[k] for k in a if k!='decide')
source={rel(x):sha(x) for x in R.glob('*.py') if x.name not in ['commands.py','summarize.py','finalize.py','publish.py']};assert len(source)==36
immutable={rel(z):sha(z) for z in [ROOT/'checks/monitor_snapshot.py',ROOT/'research/monitor/snapshot.py',CORE_PATH,old,R/'account_windows.json',R/'l4h02_resume_plan.json']}
for n in ['funding_midnight_preflight.json','funding_midnight_preflight_receipts.json','review/capture_midnight_public.py','funding08_current_preflight.json','funding08_current_preflight_receipts.json','review/capture_current08_public.py','funding08_current_reuse.json','review/public08_reuse.py','funding16_current_preflight.json','funding16_current_preflight_receipts.json','review/capture_current16_public.py','funding16_current_reuse.json','review/public16_reuse.py']:immutable[rel(R/n)]=sha(R/n)
for n in ['20261025T145537Z/run.py','20261025T065405Z/engine.py','20261026T070542Z/engine.py','20261026T110637Z/prospective_core.py','20261026T110637Z/prospective_observer.py','20261011T014626Z/forward.py','20261001T113625Z/signals.py','20261001T013355Z/evaluate.py','20261108T025309Z/forward_inputs.json.gz','20261109T030420Z/forward_inputs.json.gz']:
 z=ROOT/'research/experiments'/n;immutable[rel(z)]=sha(z)
for sub,files in [('20261031T174613Z/prospective_l4',['plan.json','binding.json','core.py','observer.py']),('20261104T201939Z/prospective_fewm',['plan.json','binding.json','core.py','observer.py','check.py','readiness.json'])]:
 for name in files:z=ROOT/'research/experiments'/sub/name;immutable[rel(z)]=sha(z)
for folder in {(ROOT/z['report']).parent for z in p['read_only_references'].values()}:
 for z in folder.glob('*.py'):immutable[rel(z)]=sha(z)
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':immutable,'no_new_financial_calculation_yet':True,'actual_new_native_models_predeclared':6,'native_simulate_AST_unchanged':True,'ETH_ROC_L_parameterization_fixed_K_VC_S_H_D':True,'maximum_required_context_days':30,'ETH_required_context_days':21,'ETH_signal_context_days':19,'ETH_cost_context_days':21})
put(R/'definition_check.json',{'passed':True,**p['expected_counts'],'two_candidate_axes':['ETH_ROC_L','ETH_exit_E'],'native_component_axis_count':2,'raw_component_weights':[1,1],'all_12_specs_unreserved_before_binding':True,'actual_new_quantity_and_impact_required':True,'ETH_ROC_L_parameterization_fixed_K_VC_S_H_D':True});print('PASS12L/Enewdefinitions,10oldresults/6banks,36sources+actualpublic16reuseboundbeforefirstreserve;accounting/frozenaccountsunchanged')
