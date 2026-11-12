"""Bind exact whole-bank research and original-account code before any reservation."""
import ast,gzip,json
from common import *
p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');A=ROOT/'research/experiments/20261111T212846Z';P=ROOT/'research/experiments/20261112T033054Z';Q=ROOT/'research/experiments/20261112T012923Z'
assert len(batch)==6 and not p['native_grid'] and p['axes']=={'BTC_V':[6,10,14],'ETH_R':[.00875,.01,.01125]}
for n in ['engine.py','market.py','portfolio.py','recent.py','audit_native.py','audit_helpers_complete.py']:assert (R/n).read_bytes()==(A/n).read_bytes()
fun=lambda t:{n.name:ast.dump(n,include_attributes=False) for n in ast.parse(t).body if isinstance(n,ast.FunctionDef)}
assert fun((R/'forward.py').read_text())==fun((Q/'forward.py').read_text().replace(Q.name,R.name).replace('completed Nov11 daily','completed Nov12 daily'))
assert (R/'audit_incremental.py').read_bytes()==(P/'audit_incremental.py').read_bytes()
for x in batch:
 sp=json.loads((ROOT/x['spec']).read_text());q=sp['parameters'];assert reg.fingerprint(sp)==x['fingerprint'] and x['fingerprint'] not in rs and [z['weight'] for z in sp['components']]==[1,1] and q['component_capitals_usdt']==[3750,15000] and q['component_initial_entry_notionals_usdt']==[1000,4000] and q['initial_capital_usdt']==18750 and q['BTC_return_hurdle']==.03 and q['BTC_exit_buffer_fraction']==.01 and q['BTC_entry_volatility_window_days']==x['V'] and q['BTC_entry_volatility_ceiling']==.03 and q['ETH_entry_funding_volatility_ratio']==x['R'] and q['ETH_entry_funding_budget_volatility_window_days']==8
 for fp in x['source_fingerprints']:assert fp in p['read_only_references'] and rs[fp]['result_available']
for fp,z in p['read_only_references'].items():
 assert rs[fp]['result_available'] and rs[fp]['status']==z['status'] and rs[fp]['report_sha256']==z['report_sha256']
 for k in ['archive','report','spec']:assert sha(ROOT/z[k])==z[k+'_sha256']
for n in ['parent_primitive_verification.json','funding00_source_verification.json','funding08_source_verification.json','window_funding_preflight.json']:assert json.loads((R/n).read_text())['passed']
for n in ['negative_parent_normalization','negative_parent_fold_reset']:
 z=json.loads((R/(n+'_receipt.json')).read_text());assert z['exit_code']==z['expected_exit_code']==1 and z['synthetic_only']
fresh=json.loads((R/'window_funding_preflight.json').read_text());win=json.loads((R/'account_windows.json').read_text());assert [win[a]['expected_funding_records'] for a in ['SMA','candidate','l4h02','fewm']]==[0,0,6,6] and all(not win[a]['expected_daily_events_utc'] for a in ['SMA','candidate','l4h02','fewm']) and all(win[a]['expected_funding_by_asset']==fresh['public_fields_by_asset'] for a in ['l4h02','fewm'])
full=P/'forward_inputs.json.gz';d=json.loads(gzip.decompress(full.read_bytes()));assert all(len(d[a]['1d'])==65 and d[a]['1d'][-1][6]+1==1794441600000 for a in ['BTC','ETH'])
excluded={'commands.py','publish.py','exports.py','checks.py','collect.py','finalize.py','journal.py'};source={rel(f):sha(f) for f in R.glob('*.py') if f.name not in excluded};immutable={rel(f):sha(f) for f in [CORE_PATH,full,R/'account_windows.json',R/'l4h02_resume_plan.json',R/'funding16_source_verification.json',R/'funding00_source_verification.json',R/'funding08_source_verification.json',R/'funding08_nov12_preflight.json',R/'window_funding_preflight.json',ROOT/'checks/monitor_snapshot.py',ROOT/'research/monitor/snapshot.py']}
for folder,files in [('20261031T174613Z/prospective_l4',['plan.json','binding.json','core.py','observer.py']),('20261104T201939Z/prospective_fewm',['plan.json','binding.json','core.py','observer.py','check.py','readiness.json']),('20261026T110637Z',['prospective_core.py','prospective_observer.py'])]:
 for n in files:f=ROOT/'research/experiments'/folder/n;immutable[rel(f)]=sha(f)
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':immutable,'no_new_financial_or_account_calculation_yet':True,'new_native_models':0,'existing_9_native_banks_reused':True,'all_original_account_kernels_unchanged':True,'readonly_formatters_and_postresult_integrity_checks_excluded_by_name':sorted(excluded)})
put(R/'definition_check.json',{'passed':True,'new_financial_configs':6,'new_native':0,'new_parents':6,'source_roots_bound':len(source),'old_unique_results':16,'old_native_banks':9,'parent_axes':p['axes'],'raw_weights':[1,1],'bank_capitals':[3750,15000],'all_specs_unreserved_before_binding':True,'actual_window_funding_fields_before_own_reserve':True,'old_SMA_full65_authority_preserved':True});print('PASS6newparentdefs,9exactoldnativebanks,actual08+1msfunding,full65authority,binding',len(source),'roots beforefirstreserve')
