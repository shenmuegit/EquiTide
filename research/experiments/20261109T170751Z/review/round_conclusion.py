"""Read saved actual K/E decisions, full NAV signatures and public transport receipts."""
import copy,gzip,json,re,sys
from decimal import Decimal as D
from fractions import Fraction as F
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));from common import sha,put,rel
rd=lambda p:json.loads(p.read_text());gz=lambda p:json.loads(gzip.decompress(p.read_bytes()));r=rd(R/'report.json');p=rd(R/'plan.json');cache={};rows=[]
def archive(path,h):
 assert sha(ROOT/path)==h
 if path not in cache:cache[path]=gz(ROOT/path)
 return cache[path]
for c in r['configs'].values():
 if c['scope']!='native':continue
 assert c['E'] in [.00625,.00875] and c['VC']==.05;ref=p['read_only_references'][c['reference_fingerprint']];a=archive(c['archive'],c['archive_sha256']);o=archive(ref['archive'],ref['archive_sha256']);pair=next(z for z in r['configs'].values() if z['scope']=='native' and z['K']==c['K'] and z['E']!=c['E']);b=archive(pair['archive'],pair['archive_sha256'])
 for k in ['1','2','3']:
  new,old,other=a['scenes'][k]['decisions'],o['scenes'][k]['decisions'],b['scenes'][k]['decisions'];assert len(new)==len(old)==len(other)==370;diff=[];paired_equal=True
  for x,y,z in zip(new,old,other):
   assert x['execution_ts_ns']==y['execution_ts_ns']==z['execution_ts_ns'] and x['signal_available_ts_ns']<x['execution_ts_ns'];xx,zz=copy.deepcopy(x),copy.deepcopy(z);xx['policy_audit'].pop('exit_buffer_fraction');zz['policy_audit'].pop('exit_buffer_fraction');paired_equal=paired_equal and xx==zz
   assert x['policy_audit']['entry_volatility_ceiling']==y['policy_audit']['entry_volatility_ceiling']==z['policy_audit']['entry_volatility_ceiling']==.05
   if x['desired_direction']!=y['desired_direction']:diff.append((x,y))
  first=None
  if diff:
   x,y=diff[0];q=D(x['state_before']['signed_units']);ret=F(x['policy_audit']['return_exact']);e=F(str(c['E']));old_e=F('.0075');assert x['state_before']==y['state_before'] and q!=0
   direction=(q>0)-(q<0)
   if e<old_e:
    assert x['desired_direction']==0 and y['desired_direction']==direction
    assert e<=ret<old_e if q>0 else -old_e<ret<=-e
   else:
    assert e>old_e and x['desired_direction']==direction and y['desired_direction']==0
    assert old_e<=ret<e if q>0 else -e<ret<=-old_e
   first={'execution_utc':datetime.fromtimestamp(x['execution_ts_ns']//10**9,timezone.utc).isoformat(),'actual_return_exact':str(ret),'old_exit_E':.0075,'new_exit_E':c['E'],'fixed_entry_VC':.05,'same_predecision_book':True,'old_desired':y['desired_direction'],'new_desired':x['desired_direction'],'strict_exit_boundary_explains_first_difference':True}
  nav_equal=c['scenes'][k]['NAV_sha256_f64le']==pair['scenes'][k]['NAV_sha256_f64le'];assert not paired_equal or nav_equal
  rows.append({'fingerprint':c['fingerprint'],'K':c['K'],'E':c['E'],'fixed_VC':.05,'cost':k,'old_E1_VC5_control_fingerprint':c['reference_fingerprint'],'different_saved_desired_direction_days':len(diff),'first_difference':first,'paired_E':pair['E'],'paired_saved_decisions_equal_except_E_field':paired_equal,'paired_full_NAV_hash_equal':nav_equal})
assert len(rows)==18
put(R/'exit_buffer_saved_path_diagnostics.json',{'passed':True,'report_sha256':sha(R/'report.json'),'rows':rows,'scope':'Savedactualdecisions/fullNAVhashes only,0policy/accountvaluations. Firstdifferencechecks samebeforebook,narrowerEexitswhilewiderEretainsactualposition,unchangedVC5. Realizedaliasesnotmathematicalequivalence/independentproof.'})
control=rd(R/'relative_control_diagnostic.json')['summary'];aliases=rd(R/'same_bank_realized_NAV_alias_diagnostic.json');cs=list(r['configs'].values());parents=[c for c in cs if c['scope']=='parent'];natives=[c for c in cs if c['scope']=='native']
put(R/'strategy_direction_conclusion.json',{'passed_evidence_validation':True,'report_sha256':sha(R/'report.json'),'new_actual_configs':12,'cost_scenes':36,'axes':['ETH_K','ETH_E'],'fixed_VC':.05,'historical_parent_passed':sum(c['status']=='passed' for c in parents),'native_rejected':sum(c['status']=='rejected' for c in natives),'prior_native_models_compared':aliases['prior_native_definitions_compared'],'prior_parent_models_compared':aliases['prior_parent_definitions_compared'],'new_configs_with_all3_saved_NAV_paths_seen_before':aliases['new_allcost_signatures_seen_in_prior_results'],'new_configs_dominated_by_oldE0p75VC5_at_all3costs':control['rows_dominated_by_oldE0p75VC5_same_K_at_allcosts'],'new_configs_dominating_oldE0p75VC5_at_all3costs':control['rows_dominating_oldE0p75VC5_same_K_at_allcosts'],'parent_3x_return_range_pct':[min(c['scenes']['3']['net_return_pct'] for c in parents),max(c['scenes']['3']['net_return_pct'] for c in parents)],'parent_3x_whole_continuous_DD_range_pct':[min(c['scenes']['3']['max_drawdown_pct'] for c in parents),max(c['scenes']['3']['max_drawdown_pct'] for c in parents)],'paired_new_E_allcost_paths_equal':all(x['paired_full_NAV_hash_equal'] for x in rows),'saved_first_exit_difference_diagnostic':rel(R/'exit_buffer_saved_path_diagnostics.json'),'interpretation':'固定VC5%下K与退出E交互，按冻结全criteria判断。收益/回撤权衡、近期门槛和路径别名全部保留，不把重复路径当独立证据。没有结果后改参数、权重或门槛；重复开发历史不是独立最终、前向或稳定实盘，不改冻结账户。','new_independent_future_validated':False,'completed_financial_or_observation_reruns':0})
li=rd(R/'l4h02_observation/input_manifest.json');qi=rd(R/'fewm_observation/input_manifest.json');attempts=rd(R/'candidate_transport_attempts.json');unique={(z['raw'],z['started_utc']):z for z in attempts+li['provenance']+qi['provenance']+rd(R/'funding16_current_preflight_receipts.json')};failed=[]
for z in unique.values():
 assert sha(ROOT/z['raw'])==z['sha256'] and len(gzip.decompress((ROOT/z['raw']).read_bytes()))==z['bytes']
 if z.get('curl_exit_code',0) or z['http_status']!=200:failed.append(z)
errors=[{'log':z['log'],'stderr':z['stderr'],'observed_curl_error_codes':re.findall(r'curl: \((\d+)\)',z['stderr'])} for z in rd(R/'forward_commands.json') if 'curl:' in z.get('stderr','')]
put(R/'transport_failure_verification.json',{'passed':True,'fresh08_public_GETs':0,'fresh16_public_GETs':len(rd(R/'funding16_current_preflight_receipts.json')),'original_prior08_public_fields_reused_with_original_retrieval_UTC':True,'deduplicated_actual_HTTP_attempts':len(unique),'failed_HTTP_attempts_preserved':failed,'SMA_transport_error_native_receipts':errors,'observed_actual_HTTP_or_transport_failures':len(failed)+sum(len(x['observed_curl_error_codes']) for x in errors),'all_actual_raw_bytes_retained':True,'FEWM_reused_public_data_not_double_counted':True,'completed_account_observation_reruns':0})
print('PASS18savedK/Eexitcomparisons,actualdirection/aliases,fixedVC5;transportfailures',len(failed)+sum(len(x['observed_curl_error_codes']) for x in errors))
