"""Bind complete predeclared price grid, old actual evidence and original mark-only accounts."""
import ast,json,copy,gzip
from common import *
p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');P=ROOT/'research/experiments/20261111T092544Z'
assert len(batch)==16 and len(p['read_only_references'])==10 and sum(z['scope']=='native' for z in p['read_only_references'].values())==6
assert len(p['grid'])==len(p['native_grid'])==9 and sum(z['readonly'] for z in p['grid'])==1 and p['funding_counts']==[2,3,4] and p['carry_ratios']==[.0075,.00875,.01] and p['entry_hurdles']==[.02] and p['exit_buffers']==[.0075] and p['fast_lookbacks']==[5] and p['price_vol_windows']==[6] and p['volatility_ceilings']==[.05625] and p['representative_preset']['M']==3 and p['representative_preset']['R']==.00875
for row in batch:
 sp=json.loads((ROOT/row['spec']).read_text());q=sp['parameters'];pre='' if row['scope']=='native' else 'ETH_';assert reg.fingerprint(sp)==row['fingerprint'] and row['fingerprint'] not in rs and (row['M'],row['R'])!=(4,.00875)
 expected={'trend_slope_lag_days':3,'trend_slope_hurdle_fraction':.0075,'entry_volatility_window_days':row['V'],'entry_volatility_ceiling':row['VC'],'lookback_days':row['L'],'return_hurdle':row['H'],'long_entry_return_hurdle':row['H'],'short_entry_return_hurdle':row['H'],'exit_buffer_fraction':row['E'],'trend_lookback_days':16,'trend_window_days':16,'trend_decay_numerator':15,'trend_decay_denominator':17,'entry_funding_budget_volatility_window_days':8,'entry_funding_settlement_count':row['M'],'entry_funding_volatility_ratio':row['R'],'entry_funding_outflow_cap':.0002};assert all(q[pre+k]==v for k,v in expected.items())
 if row['scope']=='native':
  oq=rs[row['reference_fingerprint']]['spec']['parameters'];ignore=['entry_funding_settlement_count','entry_funding_volatility_ratio'];assert {k:v for k,v in q.items() if k not in ignore}=={k:v for k,v in oq.items() if k not in ignore} and q['initial_capital_usdt']==15000 and q['fixed_entry_notional_usdt']==4500
 else:assert [x['weight'] for x in sp['components']]==[1,1] and q['component_capitals_usdt']==[3750,15000] and q['component_initial_entry_notionals_usdt']==[1000,4500]
for fp,ref in p['read_only_references'].items():
 assert rs[fp]['result_available'] and rs[fp]['status']==ref['status'] and rs[fp]['report_sha256']==ref['report_sha256']
 for k in ['spec','report','archive']:assert sha(ROOT/ref[k])==ref[k+'_sha256']
functions=lambda s:{n.name:ast.dump(n,include_attributes=False) for n in ast.parse(s).body if isinstance(n,ast.FunctionDef)};old=P/'engine.py';a,b=functions(old.read_text()),functions((R/'engine.py').read_text());assert a==b and (R/'engine.py').read_bytes()==old.read_bytes()
for n in ['TDD_doubleweight_red','TDD_funding_causality_red','TDD_median_red','TDD_ratio_red']:
 z=json.loads((R/(n+'_receipt.json')).read_text());assert z['exit_code']==z['expected_exit_code']==1

T=ROOT/'research/experiments/20261111T012135Z';assert functions((R/'forward.py').read_text())==functions((T/'forward.py').read_text().replace('20261111T012135Z',R.name).replace('Nov9 daily','Nov11 daily').replace('2026-11-11UTC00:01','2026-11-12UTC00:01'));full=ROOT/'research/experiments/20261111T032206Z/forward_inputs.json.gz';d=json.loads(gzip.decompress(full.read_bytes()));assert all(len(d[z]['1d'])==65 and d[z]['1d'][-1][6]+1==1794355200000 for z in ['BTC','ETH'])
source={rel(x):sha(x) for x in R.glob('*.py') if x.name not in ['commands.py','summarize.py','finalize.py','publish.py']};assert len(source)==36
immutable={rel(z):sha(z) for z in [ROOT/'checks/monitor_snapshot.py',ROOT/'research/monitor/snapshot.py',CORE_PATH,old,R/'account_windows.json',R/'l4h02_resume_plan.json',full]}
for n in ['test_price_gates.py','test_relative_budget.py','test_budget_window.py','funding_signal_preflight.py','public00_reuse.py','public08_reuse.py','public16_reuse.py','public_nov10_08_reuse.py','public_nov10_16_reuse.py','public_nov11_00_reuse.py']:
 f=R/'review'/n;immutable[rel(f)]=sha(f)
for n in ['funding_signal_preflight.json','funding00_current_preflight.json','funding00_current_preflight_receipts.json','funding_midnight_preflight.json','funding_midnight_preflight_receipts.json','funding08_current_preflight.json','funding08_current_preflight_receipts.json','funding16_current_preflight.json','funding16_current_preflight_receipts.json','funding08_nov10_preflight.json','funding08_nov10_preflight_receipts.json','funding16_nov10_preflight.json','funding16_nov10_preflight_receipts.json','funding00_nov11_preflight.json','funding00_nov11_preflight_receipts.json']:
 f=R/n;immutable[rel(f)]=sha(f)
for n in ['public00_reuse','public08_reuse','public16_reuse','public_nov10_08_reuse','public_nov10_16_reuse','public_nov11_00_reuse']:
 f=R/('review_'+n+'.py_receipt.json');assert json.loads(f.read_text())['actual_exit_code']==0;immutable[rel(f)]=sha(f)
for folder in {T,P}|{(ROOT/z['report']).parent for z in p['read_only_references'].values()}:
 for z in folder.glob('*.py'):immutable[rel(z)]=sha(z)
for sub,files in [('20261031T174613Z/prospective_l4',['plan.json','binding.json','core.py','observer.py']),('20261104T201939Z/prospective_fewm',['plan.json','binding.json','core.py','observer.py','check.py','readiness.json']),('20261026T110637Z',['prospective_core.py','prospective_observer.py'])]:
 for name in files:z=ROOT/'research/experiments'/sub/name;immutable[rel(z)]=sha(z)
fresh=json.loads((R/'funding08_nov11_preflight.json').read_text());cap=json.loads((P/'review_capture_nov11_08_public.py_receipt.json').read_text());reuse=json.loads((R/'review_public_nov11_08_reuse.py_receipt.json').read_text());assert cap['actual_exit_code']==reuse['actual_exit_code']==0 and fresh['account_or_strategy_calculations']==0 and fresh['nominal_UTC']=='2026-11-11T08:00:00Z'
for f in [R/'funding08_nov11_preflight.json',R/'funding08_nov11_preflight_receipts.json',P/'review/capture_nov11_08_public.py',P/'review_capture_nov11_08_public.py_receipt.json',R/'review/public_nov11_08_reuse.py',R/'review_public_nov11_08_reuse.py_receipt.json']:immutable[rel(f)]=sha(f)
for z in json.loads((R/'funding08_nov11_preflight_receipts.json').read_text()):assert sha(ROOT/z['raw'])==z['sha256'];immutable[z['raw']]=z['sha256']
win=json.loads((R/'account_windows.json').read_text());assert win['candidate']['expected_funding_records']==6 and win['l4h02']['expected_funding_records']==win['fewm']['expected_funding_records']==win['SMA']['expected_funding_records']==0

put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':immutable,'no_new_financial_calculation_yet':True,'actual_new_native_models_predeclared':8,'native_simulate_AST_unchanged':True,'ETH_M_R_parameterization_fixed_L5_PRICE_V6_VC05625_S16_D3_K0075_H02_E0075':True,'executor_byte_identical_and_all_function_AST_unchanged':True,'maximum_required_context_days':30,'ETH_required_context_days':21,'ETH_signal_context_days':19,'ETH_cost_context_days':21,'SMA_full65_authority':rel(full),'SMA_mark_only_original_main_AST_unchanged':True})
put(R/'definition_check.json',{'passed':True,**p['expected_counts'],'two_candidate_axes':['ETH_funding_median_count_M','ETH_funding_budget_ratio_R'],'native_component_axis_count':2,'raw_component_weights':[1,1],'all_16_specs_unreserved_before_binding':True,'actual_new_quantity_and_impact_required':True,'readonly_grid_cells_per_scope':1,'SMA_full65_source_unchanged':True});print('PASS16new definitions/10old results/6banks/36sources and all mark-only windows bound before first reserve')
