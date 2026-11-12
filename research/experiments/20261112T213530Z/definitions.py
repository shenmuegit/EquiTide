"""Bind exact existing-bank pairings and unchanged original-account creators before reserve."""
import ast,gzip,json
from common import *
p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');A=ROOT/'research/experiments/20261111T212846Z';P=ROOT/'research/experiments/20261112T193458Z'
assert len(batch)==4 and p['native_grid']==[] and p['axes']=={'BTC_VOL_CAP':[.03,.04,.05],'ETH_FUND_R':[.00875,.01,.01125]} and p['representative_preset']=={'BVC':.04,'R':.01}
for n in ['market.py','portfolio.py','recent.py','audit_native.py','audit_helpers_complete.py']:assert (R/n).read_bytes()==(A/n).read_bytes()
for n in ['audit_incremental.py','audit_candidate.py','audit_l4h02.py','audit_fewm.py']:assert (R/n).read_bytes()==(P/n).read_bytes()
for n in ['forward.py','observe_candidate.py','observe_l4h02.py','observe_fewm.py']:
 expected=(P/n).read_text().replace(P.name,R.name).replace('1043515','1071430');assert (R/n).read_text()==expected
for x in batch:
 sp=json.loads((ROOT/x['spec']).read_text());q=sp['parameters'];assert reg.fingerprint(sp)==x['fingerprint'] and x['fingerprint'] not in rs and x['scope']=='parent';assert [z['weight'] for z in sp['components']]==[1,1] and [z['fingerprint'] for z in sp['components']]==x['source_fingerprints'] and q['component_capitals_usdt']==[3750,15000] and q['component_initial_entry_notionals_usdt']==[1000,4000] and q['initial_capital_usdt']==18750 and q['BTC_return_hurdle']==x['H']==.03 and q['BTC_entry_volatility_window_days']==10 and q['BTC_entry_volatility_ceiling']==x['BVC'] and q['ETH_entry_funding_volatility_ratio']==x['R'] and q['ETH_entry_funding_budget_volatility_window_days']==8 and q['actual_native_quantity_and_impact_reused'] and not q['ETH_new_native_quantity_and_impact_computed']
for fp,z in p['read_only_references'].items():
 assert rs[fp]['result_available'] and rs[fp]['status']==z['status'] and rs[fp]['report_sha256']==z['report_sha256']
 for k in ['archive','report','spec']:assert sha(ROOT/z[k])==z[k+'_sha256']
assert len(p['read_only_references'])==16 and sum(x['scope']=='native' for x in p['read_only_references'].values())==9
for n in ['parent_primitive_verification.json','window_funding_preflight.json','funding16_nov12_source_verification.json','component_graph_dedup.json']:assert json.loads((R/n).read_text())['passed']
for n in ['negative_parent_normalization','negative_parent_fold_reset']:
 z=json.loads((R/(n+'_receipt.json')).read_text());assert z['exit_code']==z['expected_exit_code']==1 and z['synthetic_only']
fresh=json.loads((R/'window_funding_preflight.json').read_text());win=json.loads((R/'account_windows.json').read_text());assert fresh['public_fields_by_asset']=={'BTC':[],'ETH':[]} and [win[a]['expected_funding_records'] for a in ['SMA','candidate','l4h02','fewm']]==[0,0,0,0] and all(win[a]['expected_funding_by_asset']=={'BTC':[],'ETH':[]} and not win[a]['expected_daily_events_utc'] for a in ['SMA','candidate','l4h02','fewm'])
full=ROOT/'research/experiments/20261112T033054Z/forward_inputs.json.gz';d=json.loads(gzip.decompress(full.read_bytes()));assert all(len(d[a]['1d'])==65 and d[a]['1d'][-1][6]+1==1794441600000 for a in ['BTC','ETH'])
excluded={'commands.py','publish.py','exports.py','checks.py','collect.py','finalize.py','journal.py'};source={rel(f):sha(f) for f in R.glob('*.py') if f.name not in excluded};immutable={rel(f):sha(f) for f in [CORE_PATH,full,R/'account_windows.json',R/'l4h02_resume_plan.json',R/'plan.json',R/'spec.json',R/'batch.json',R/'funding16_nov12_preflight.json',R/'funding16_nov12_source_verification.json',R/'window_funding_preflight.json',ROOT/'checks/monitor_snapshot.py',ROOT/'research/monitor/snapshot.py']}
for folder,files in [('20261031T174613Z/prospective_l4',['plan.json','binding.json','core.py','observer.py']),('20261104T201939Z/prospective_fewm',['plan.json','binding.json','core.py','observer.py','check.py','readiness.json']),('20261026T110637Z',['prospective_core.py','prospective_observer.py'])]:
 for n in files:f=ROOT/'research/experiments'/folder/n;immutable[rel(f)]=sha(f)
for row in batch:immutable[row['spec']]=sha(ROOT/row['spec'])
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':immutable,'no_new_financial_or_account_calculation_yet':True,'new_native_models':0,'existing_9_native_banks_reused':True,'all_original_account_kernels_unchanged':True,'readonly_formatters_and_postresult_integrity_checks_excluded_by_name':sorted(excluded)})
put(R/'definition_check.json',{'passed':True,'new_financial_configs':4,'new_native':0,'new_parents':4,'source_roots_bound':len(source),'old_unique_results':16,'old_native_banks':9,'parent_axes':p['axes'],'raw_weights':[1,1],'bank_capitals':[3750,15000],'all_specs_unreserved_before_binding':True,'actual_window_funding_fields_before_own_reserve':True,'old_SMA_full65_authority_preserved':True});print('PASS4newparents/9exactoldbanks, two axes, original account binding before first reserve',len(source))
