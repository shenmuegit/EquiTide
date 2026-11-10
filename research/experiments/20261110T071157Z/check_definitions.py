"""Bind full VW/R definitions and unchanged native accounting before reserves."""
import ast,json,copy
from common import *
p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(batch)==16 and len(p['read_only_references'])==10 and sum(z['scope']=='native' for z in p['read_only_references'].values())==6
assert len(p['grid'])==len(p['native_grid'])==9 and sum(z['readonly'] for z in p['grid'])==1 and p['budget_vol_windows']==[8,10,12] and p['carry_ratios']==[.00625,.0075,.00875] and p['funding_counts']==[4]
for row in batch:
 sp=json.loads((ROOT/row['spec']).read_text());q=sp['parameters'];pre='' if row['scope']=='native' else 'ETH_';assert reg.fingerprint(sp)==row['fingerprint'] and row['fingerprint'] not in rs and q[pre+'entry_funding_volatility_ratio']==row['R'] and q[pre+'entry_funding_budget_volatility_window_days']==row['VW'] and q[pre+'entry_funding_settlement_count']==row['M']==4 and q[pre+'entry_funding_outflow_cap']==.0002 and q[pre+'entry_volatility_window_days']==10 and q[pre+'entry_volatility_ceiling']==.05 and (row['VW'],row['R'])!=(10,.0075)
 if row['scope']=='native':
  oq=rs[row['reference_fingerprint']]['spec']['parameters'];assert {k:v for k,v in q.items() if not k.startswith('entry_funding_')}=={k:v for k,v in oq.items() if not k.startswith('entry_funding_')} and q['initial_capital_usdt']==15000 and q['fixed_entry_notional_usdt']==4500
 else:assert [x['weight'] for x in sp['components']]==[1,1] and q['component_capitals_usdt']==[3750,15000] and q['component_initial_entry_notionals_usdt']==[1000,4500]
for fp,ref in p['read_only_references'].items():
 assert rs[fp]['result_available'] and rs[fp]['status']==ref['status'] and rs[fp]['report_sha256']==ref['report_sha256']
 for k in ['spec','report','archive']:assert sha(ROOT/ref[k])==ref[k+'_sha256']
old=ROOT/'research/experiments/20261110T051156Z/engine.py';functions=lambda f:{n.name:ast.dump(n,include_attributes=False) for n in ast.parse(f.read_text()).body if isinstance(n,ast.FunctionDef)};a,b=functions(old),functions(R/'engine.py');assert all(a[k]==b[k] for k in a if k!='decide') and set(b)-set(a)=={'budget_sigma'}
source={rel(x):sha(x) for x in R.glob('*.py') if x.name not in ['commands.py','summarize.py','finalize.py','publish.py']};assert len(source)==36
immutable={rel(z):sha(z) for z in [ROOT/'checks/monitor_snapshot.py',ROOT/'research/monitor/snapshot.py',CORE_PATH,old,R/'account_windows.json',R/'l4h02_resume_plan.json']}
immutable[rel(ROOT/'research/experiments/20261110T031055Z/forward_inputs.json.gz')]=sha(ROOT/'research/experiments/20261110T031055Z/forward_inputs.json.gz')
immutable[rel(R/'review/test_relative_budget.py')]=sha(R/'review/test_relative_budget.py')
immutable[rel(R/'review/test_budget_window.py')]=sha(R/'review/test_budget_window.py')
for n in ['funding_signal_preflight.json','review/funding_signal_preflight.py','funding00_current_preflight.json','funding00_current_preflight_receipts.json','review/capture_current00_public.py','review/public00_reuse.py','funding00_current_reuse.json','funding_midnight_preflight.json','funding_midnight_preflight_receipts.json','review/capture_midnight_public.py','funding08_current_preflight.json','funding08_current_preflight_receipts.json','review/capture_current08_public.py','funding08_current_reuse.json','review/public08_reuse.py','funding16_current_preflight.json','funding16_current_preflight_receipts.json','review/capture_current16_public.py','funding16_current_reuse.json','review/public16_reuse.py']:immutable[rel(R/n)]=sha(R/n)
for n in ['20261025T145537Z/run.py','20261025T065405Z/engine.py','20261026T070542Z/engine.py','20261026T110637Z/prospective_core.py','20261026T110637Z/prospective_observer.py','20261011T014626Z/forward.py','20261001T113625Z/signals.py','20261001T013355Z/evaluate.py','20261108T025309Z/forward_inputs.json.gz','20261109T030420Z/forward_inputs.json.gz','20261109T030420Z/forward.py','20261109T030420Z/audit_forward.py','20261109T030420Z/forward_registry.py']:
 z=ROOT/'research/experiments'/n;immutable[rel(z)]=sha(z)
for sub,files in [('20261031T174613Z/prospective_l4',['plan.json','binding.json','core.py','observer.py']),('20261104T201939Z/prospective_fewm',['plan.json','binding.json','core.py','observer.py','check.py','readiness.json'])]:
 for name in files:z=ROOT/'research/experiments'/sub/name;immutable[rel(z)]=sha(z)
for folder in {(ROOT/z['report']).parent for z in p['read_only_references'].values()}:
 for z in folder.glob('*.py'):immutable[rel(z)]=sha(z)
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':immutable,'no_new_financial_calculation_yet':True,'actual_new_native_models_predeclared':8,'native_simulate_AST_unchanged':True,'ETH_entry_H_parameterization_fixed_K_VC_S_L_D':True,'maximum_required_context_days':30,'ETH_required_context_days':21,'ETH_signal_context_days':19,'ETH_cost_context_days':21})
put(R/'definition_check.json',{'passed':True,**p['expected_counts'],'two_candidate_axes':['ETH_budget_volatility_window_VW','ETH_carry_volatility_ratio_R'],'native_component_axis_count':2,'raw_component_weights':[1,1],'all_16_specs_unreserved_before_binding':True,'actual_new_quantity_and_impact_required':True,'ETH_entry_H_parameterization_fixed_K_VC_S_L_D':True});print('PASS16VW/Rnewdefinitions,10oldresults/6banks,36sources+actualpublic16reuseboundbeforefirstreserve;accounting/frozenaccountsunchanged')
