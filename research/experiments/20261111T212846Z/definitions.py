"""Bind actual accounting/decision sources and predeclared N definitions before reserve."""
import ast,copy,gzip,json
from common import *
p=json.loads((R/'plan.json').read_text());b=json.loads((R/'batch.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');P=ROOT/'research/experiments/20261111T192849Z'
assert len(b)==16 and p['axes']=={'ETH_V':[5,6,7],'ETH_VW':[8,10,12]} and sum(z['scope']=='native' for z in b)==8 and len(p['read_only_references'])==6
assert (R/'engine.py').read_bytes()==(P/'engine.py').read_bytes();fun=lambda s:{n.name:ast.dump(n,include_attributes=False) for n in ast.parse(s).body if isinstance(n,ast.FunctionDef)}
assert fun((R/'forward.py').read_text())==fun((P/'forward.py').read_text().replace(P.name,R.name))
assert (R/'audit_incremental.py').read_text()==(P/'audit_incremental.py').read_text().replace(P.name,R.name)
assert json.loads((R/'funding16_source_verification.json').read_text())['passed'] and json.loads((R/'policy_primitive_verification.json').read_text())['passed']
for z in b:
 sp=json.loads((ROOT/z['spec']).read_text());q=sp['parameters'];assert reg.fingerprint(sp)==z['fingerprint'] and z['fingerprint'] not in rs
 if z['scope']=='native':
  old=rs[z['reference_fingerprint']]['spec']['parameters'];changed={'entry_volatility_window_days','entry_funding_budget_volatility_window_days'};assert z['asset']=='ETH' and {k:v for k,v in q.items() if k not in changed}=={k:v for k,v in old.items() if k not in changed} and q['entry_volatility_window_days']==z['V'] and q['entry_funding_budget_volatility_window_days']==z['VW'] and q['fixed_entry_notional_usdt']==4000 and q['initial_capital_usdt']==15000
 else:
  assert [x['weight'] for x in sp['components']]==[1,1] and q['component_capitals_usdt']==[3750,15000] and q['initial_capital_usdt']==18750 and q['component_initial_entry_notionals_usdt']==[1000,4000] and q['BTC_return_hurdle']==z['H'] and q['ETH_entry_funding_volatility_ratio']==z['R'] and q['ETH_entry_volatility_window_days']==z['V'] and q['ETH_entry_funding_budget_volatility_window_days']==z['VW']

for fp,z in p['read_only_references'].items():
 assert rs[fp]['result_available'] and rs[fp]['status']==z['status'] and rs[fp]['report_sha256']==z['report_sha256']
 for k in ['archive','report','spec']:assert sha(ROOT/z[k])==z[k+'_sha256']
for n in ['negative_fixed_N','negative_future_open','negative_linear_impact','negative_doubleweight','negative_price_future','negative_budget_future','negative_population']:
 z=json.loads((R/(n+'_receipt.json')).read_text());assert z['exit_code']==z['expected_exit_code']==1 and z['synthetic_only']
assert json.loads((R/'primitive_verification.json').read_text())['passed']
full=ROOT/'research/experiments/20261111T032206Z/forward_inputs.json.gz';d=json.loads(gzip.decompress(full.read_bytes()));assert all(len(d[a]['1d'])==65 and d[a]['1d'][-1][6]+1==1794355200000 for a in ['BTC','ETH'])
win=json.loads((R/'account_windows.json').read_text());assert all(not win[a]['expected_daily_events_utc'] for a in ['SMA','candidate','l4h02','fewm']) and [win[a]['expected_funding_records'] for a in ['SMA','candidate','l4h02','fewm']]==[0,0,0,0]
# Financial/account creators and the independent monetary auditor are immutable after this point.
excluded={'commands.py','publish.py','exports.py','checks.py','collect.py','finalize.py','journal.py'}
source={rel(f):sha(f) for f in R.glob('*.py') if f.name not in excluded};immutable={rel(f):sha(f) for f in [CORE_PATH,ROOT/'research/experiments/20261025T065405Z/engine.py',ROOT/'research/experiments/20261026T070542Z/engine.py',full,R/'account_windows.json',R/'l4h02_resume_plan.json',R/'funding16_source_verification.json',ROOT/'research/experiments/20261111T172818Z/funding16_nov11_preflight.json',ROOT/'checks/monitor_snapshot.py',ROOT/'research/monitor/snapshot.py',P/'engine.py']}
for folder,files in [('20261031T174613Z/prospective_l4',['plan.json','binding.json','core.py','observer.py']),('20261104T201939Z/prospective_fewm',['plan.json','binding.json','core.py','observer.py','check.py','readiness.json']),('20261026T110637Z',['prospective_core.py','prospective_observer.py'])]:
 for n in files:f=ROOT/'research/experiments'/folder/n;immutable[rel(f)]=sha(f)
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':immutable,'no_new_financial_calculation_yet':True,'new_native_models_predeclared':8,'engine_byte_identical':True,'actual_sizing_rather_than_NAV_scaling':True,'native_independent_auditor_bound':True,'readonly_formatters_and_postresult_integrity_checks_excluded_by_name':sorted(excluded),'source_binding_policy':'Allfinancial/accountstatecreatorsandindependentmonetaryauditimmutablebeforefirstreserve;readonlyexports/formatting/postresultchecksourceversionandfailuresretainedintheirseparatenativereceiptsandfinalmanifest.'});put(R/'definition_check.json',{'passed':True,'new_financial_configs':16,'new_native':8,'new_parents':8,'source_roots_bound':len(source),'old_unique_results':6,'old_native_banks':4,'parent_axes':p['axes'],'ETH_native_and_parent_two_applicable_horizon_axes':True,'raw_weights':[1,1],'bank_capitals':[3750,15000],'all_specs_unreserved_before_binding':True,'SMA_original_main_AST_unchanged':True,'perp_auditor_display_restored9_before_binding':True});print('PASS16defs/8newnative/8parents,originalenginebytes/Nparams/wholebanks/frozenaccounts bound',len(source),'roots before reserve')
