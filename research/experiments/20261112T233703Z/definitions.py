"""Bind actual389day data and exact unchanged money/policy kernels before first reserve."""
import ast,gzip,json
from common import *
P=ROOT/'research/experiments/20261112T213530Z';p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(batch)==18 and len(p['native_grid'])==6 and len(p['grid'])==9 and p['time_boundaries']['continuous_oos_days']==389
fun=lambda f:{n.name:ast.dump(n,include_attributes=False) for n in ast.parse(f.read_text()).body if isinstance(n,ast.FunctionDef)}
old=fun(ROOT/'research/experiments/20261030T173813Z/engine.py');new=fun(R/'core389.py');assert set(old)==set(new) and all(old[k]==new[k] for k in old if k!='load_market')
assert (R/'engine.py').read_bytes()==(ROOT/'research/experiments/20261112T073021Z/engine.py').read_bytes()
pid=str(json.loads((R/'startup.json').read_text())['branch_lock_broker_pid']);prevpid=str(json.loads((P/'startup.json').read_text())['branch_lock_broker_pid'])
for n in ['audit_incremental.py','audit_candidate.py','audit_l4h02.py','audit_fewm.py']:assert (R/n).read_bytes()==(P/n).read_bytes()
for n in ['forward.py','observe_candidate.py','observe_l4h02.py','observe_fewm.py']:assert (R/n).read_text()==(P/n).read_text().replace(P.name,R.name).replace(prevpid,pid)
for x in batch:
 sp=json.loads((ROOT/x['spec']).read_text());assert reg.fingerprint(sp)==x['fingerprint'] and x['fingerprint'] not in rs and sp['parameters']['end_utc']=='2026-11-12T00:01:00Z' and sp['parameters']['continuous_oos_days']==389
 if x['scope']=='parent':assert [q['weight'] for q in sp['components']]==[1,1] and sp['parameters']['initial_capital_usdt']==18750
 else:
  prior=rs[x['prior_fingerprint']]['spec']['parameters'];q=sp['parameters'];assert q['initial_capital_usdt']==prior['initial_capital_usdt'] and q['fixed_entry_notional_usdt']==prior['fixed_entry_notional_usdt']
  changed={k for k in set(prior)|set(q) if prior.get(k)!=q.get(k)};assert changed<=set(['end_utc','continuous_oos_days','tail_fold_days','walk_forward_tail_days','prior_370day_source_fingerprint','input_hashes']),changed
for fp,z in p['read_only_references'].items():
 assert rs[fp]['result_available'] and rs[fp]['status']==z['status'] and rs[fp]['report_sha256']==z['report_sha256']
 for key in ['spec','report','archive']:assert sha(ROOT/z[key])==z[key+'_sha256']
for n in ['calendar_verification.json','parent_primitive_verification.json','extended_data_manifest.json']:assert json.loads((R/n).read_text())['passed']
for n in ['negative_parent_normalization','negative_parent_fold_reset','negative_old_terminal','negative_recent_origin']:
 z=json.loads((R/(n+'_receipt.json')).read_text());assert z['exit_code']==z['expected_exit_code']==1 and z['synthetic_only'] if n.startswith('negative_parent') else z['exit_code']==z['expected_exit_code']==1 and z['new_financial_or_account_calculations']==0
win=json.loads((R/'account_windows.json').read_text());assert all(win[x]['expected_funding_records']==0 and not win[x]['expected_daily_events_utc'] for x in ['SMA','candidate','l4h02','fewm'])
full=ROOT/'research/experiments/20261112T033054Z/forward_inputs.json.gz';dd=json.loads(gzip.decompress(full.read_bytes()));assert all(len(dd[a]['1d'])==65 and dd[a]['1d'][-1][6]+1==1794441600000 for a in ['BTC','ETH'])
excluded={'commands.py','publish.py','exports.py','checks.py','collect.py','finalize.py','journal.py'};source={rel(f):sha(f) for f in R.glob('*.py') if f.name not in excluded};immutable={rel(f):sha(f) for f in [full,R/'account_windows.json',R/'l4h02_resume_plan.json',R/'plan.json',R/'spec.json',R/'batch.json',R/'extended_data_manifest.json',ROOT/'checks/monitor_snapshot.py',ROOT/'research/monitor/snapshot.py']}
for folder,files in [('20261031T174613Z/prospective_l4',['plan.json','binding.json','core.py','observer.py']),('20261104T201939Z/prospective_fewm',['plan.json','binding.json','core.py','observer.py','check.py','readiness.json']),('20261026T110637Z',['prospective_core.py','prospective_observer.py'])]:
 for n in files:f=ROOT/'research/experiments'/folder/n;immutable[rel(f)]=sha(f)
for x in batch:immutable[x['spec']]=sha(ROOT/x['spec'])
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':immutable,'no_new_financial_or_account_calculation_yet':True,'new_native_models':8,'new_parent_models':10,'all_original_account_kernels_unchanged':True,'trade_fund_summary_and_policy_AST_unchanged':True,'readonly_formatters_and_postresult_integrity_checks_excluded_by_name':sorted(excluded)})
put(R/'definition_check.json',{'passed':True,'new_financial_configs':18,'new_native':8,'new_parents':10,'source_roots_bound':len(source),'old_unique_results':18,'parent_axes':p['axes'],'raw_weights':[1,1],'bank_capitals':[3750,15000],'all_specs_unreserved_before_binding':True,'calendar_only_extension_of_native_parameters':True});print('PASS18new389day configs, unchanged monetary/policy kernels,calendar/source/units and original accounts bound beforefirstreserve')
