"""Bind complete predeclared price grid, old actual evidence and original mark-only accounts."""
import ast,json,copy,gzip
from common import *
p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');OLD=[(6,.055),(6,.0575),(7,.055),(7,.0575),(8,.055)];P=ROOT/'research/experiments/20261111T032206Z'
assert len(batch)==8 and len(p['read_only_references'])==18 and sum(z['scope']=='native' for z in p['read_only_references'].values())==10
assert len(p['grid'])==len(p['native_grid'])==9 and sum(z['readonly'] for z in p['grid'])==5 and p['price_vol_windows']==[6,7,8] and p['volatility_ceilings']==[.055,.0575,.06] and p['representative_preset']['V']==6 and p['representative_preset']['VC']==.06
for row in batch:
 sp=json.loads((ROOT/row['spec']).read_text());q=sp['parameters'];pre='' if row['scope']=='native' else 'ETH_';assert reg.fingerprint(sp)==row['fingerprint'] and row['fingerprint'] not in rs and (row['V'],row['VC']) not in OLD
 expected={'trend_slope_lag_days':3,'trend_slope_hurdle_fraction':.0075,'entry_volatility_window_days':row['V'],'entry_volatility_ceiling':row['VC'],'lookback_days':5,'return_hurdle':.02,'long_entry_return_hurdle':.02,'short_entry_return_hurdle':.02,'exit_buffer_fraction':.0075,'trend_lookback_days':16,'trend_window_days':16,'trend_decay_numerator':15,'trend_decay_denominator':17,'entry_funding_budget_volatility_window_days':8,'entry_funding_settlement_count':4,'entry_funding_volatility_ratio':.00875,'entry_funding_outflow_cap':.0002};assert all(q[pre+k]==v for k,v in expected.items())
 if row['scope']=='native':
  oq=rs[row['reference_fingerprint']]['spec']['parameters'];ignore=['entry_volatility_window_days','entry_volatility_ceiling'];assert {k:v for k,v in q.items() if k not in ignore}=={k:v for k,v in oq.items() if k not in ignore} and q['initial_capital_usdt']==15000 and q['fixed_entry_notional_usdt']==4500
 else:assert [x['weight'] for x in sp['components']]==[1,1] and q['component_capitals_usdt']==[3750,15000] and q['component_initial_entry_notionals_usdt']==[1000,4500]
for fp,ref in p['read_only_references'].items():
 assert rs[fp]['result_available'] and rs[fp]['status']==ref['status'] and rs[fp]['report_sha256']==ref['report_sha256']
 for k in ['spec','report','archive']:assert sha(ROOT/ref[k])==ref[k+'_sha256']
functions=lambda s:{n.name:ast.dump(n,include_attributes=False) for n in ast.parse(s).body if isinstance(n,ast.FunctionDef)};old=P/'engine.py';a,b=functions(old.read_text()),functions((R/'engine.py').read_text());assert {k for k in a if a[k]!=b[k]}=={'decide'} and (R/'engine.py').read_text()==old.read_text().replace('cap in [.045,.05,.0525,.055,.0575]','cap in [.045,.05,.0525,.055,.0575,.06]')
assert json.loads((R/'TDD_red_receipt.json').read_text())['real_executor_missing_domain_failure']
T=ROOT/'research/experiments/20261111T012135Z';assert functions((R/'forward.py').read_text())==functions((T/'forward.py').read_text().replace('20261111T012135Z',R.name).replace('Nov9 daily','Nov11 daily').replace('2026-11-11UTC00:01','2026-11-12UTC00:01'));full=P/'forward_inputs.json.gz';d=json.loads(gzip.decompress(full.read_bytes()));assert all(len(d[z]['1d'])==65 and d[z]['1d'][-1][6]+1==1794355200000 for z in ['BTC','ETH'])
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
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':immutable,'no_new_financial_calculation_yet':True,'actual_new_native_models_predeclared':4,'native_simulate_AST_unchanged':True,'ETH_PRICE_V_VC_parameterization_fixed_L5_S16_D3_K0075_H02_E0075':True,'executor_decide_PRICE_guard_only_changed':True,'maximum_required_context_days':30,'ETH_required_context_days':21,'ETH_signal_context_days':19,'ETH_cost_context_days':21,'SMA_full65_authority':rel(full),'SMA_mark_only_original_main_AST_unchanged':True})
put(R/'definition_check.json',{'passed':True,**p['expected_counts'],'two_candidate_axes':['ETH_PRICE_V','ETH_volatility_ceiling_VC'],'native_component_axis_count':2,'raw_component_weights':[1,1],'all_8_specs_unreserved_before_binding':True,'actual_new_quantity_and_impact_required':True,'readonly_grid_cells_per_scope':5,'SMA_full65_source_unchanged':True});print('PASS8new definitions/18old results/10banks/36sources and all mark-only windows bound before first reserve')
