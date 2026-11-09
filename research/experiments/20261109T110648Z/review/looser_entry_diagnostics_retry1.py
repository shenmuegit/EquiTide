"""Read only saved actual decisions, paths and transport receipts; no new valuation."""
import copy,gzip,json,re,sys
from decimal import Decimal as D
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));from common import sha,put,rel
rd=lambda p:json.loads(p.read_text());gz=lambda p:json.loads(gzip.decompress(p.read_bytes()));r=rd(R/'report.json');p=rd(R/'plan.json');rows=[];cache={}
def archive(path,h):
 assert sha(ROOT/path)==h
 if path not in cache:cache[path]=gz(ROOT/path)
 return cache[path]
for c in r['configs'].values():
 if c['scope']!='native':continue
 ref=p['read_only_references'][c['reference_fingerprint']];a=archive(c['archive'],c['archive_sha256']);o=archive(ref['archive'],ref['archive_sha256']);pair=next(z for z in r['configs'].values() if z['scope']=='native' and z['K']==c['K'] and z['VC']!=c['VC']);b=archive(pair['archive'],pair['archive_sha256'])
 for k in ['1','2','3']:
  new,old,other=a['scenes'][k]['decisions'],o['scenes'][k]['decisions'],b['scenes'][k]['decisions'];assert len(new)==len(old)==len(other)==370;diff=[]
  for x,y,z in zip(new,old,other):
   assert x['execution_ts_ns']==y['execution_ts_ns']==z['execution_ts_ns'] and x['signal_available_ts_ns']<x['execution_ts_ns']
   xx,zz=copy.deepcopy(x),copy.deepcopy(z);xx['policy_audit'].pop('entry_volatility_ceiling');zz['policy_audit'].pop('entry_volatility_ceiling');assert xx==zz
   if x['desired_direction']!=y['desired_direction']:diff.append((x,y))
  first=None
  if diff:
   x,y=diff[0];sigma=x['policy_audit']['observed_sample_logvol'];assert x['state_before']==y['state_before'] and .045<sigma<=c['VC'] and y['policy_audit']['entry_filter_applied'] and x['policy_audit']['entry_filter_applied'] and y['desired_direction']==0 and x['desired_direction']==x['policy_audit']['raw_desired_before_entry_filter']!=0;first={'execution_utc':datetime.fromtimestamp(x['execution_ts_ns']//10**9,timezone.utc).isoformat(),'actual_sample_logvol':sigma,'old_cap':.045,'new_cap':c['VC'],'same_predecision_book':True,'old_desired':y['desired_direction'],'new_desired':x['desired_direction'],'vol_filter_evaluated_for_both_entries':True,'old_vol_filter_blocked':True,'new_vol_filter_allowed':True}
  assert c['scenes'][k]['NAV_sha256_f64le']==pair['scenes'][k]['NAV_sha256_f64le']
  rows.append({'fingerprint':c['fingerprint'],'K':c['K'],'VC':c['VC'],'cost':k,'old_control_fingerprint':c['reference_fingerprint'],'different_saved_desired_direction_days':len(diff),'first_difference':first,'paired_cap':pair['VC'],'paired_all_saved_decisions_equal_except_cap_field':True,'paired_full_NAV_hash_equal':True})
assert len(rows)==18
put(R/'looser_entry_saved_path_diagnostics.json',{'passed':True,'report_sha256':sha(R/'report.json'),'rows':rows,'scope':'Read actualsaved370daydecisions/fullNAVhashes only. Firstdifferencechecksoldcap45<actualpastvol<=newcapandidenticalpriorbook. VC5/5.5actualpathidentityisobservedhistory,notmathematicalequivalence orindependentrobustness. No policy/financial/account evaluation ornewconfiguration.'})
control=rd(R/'relative_control_diagnostic.json')['summary'];aliases=rd(R/'same_bank_realized_NAV_alias_diagnostic.json');cs=list(r['configs'].values());parents=[c for c in cs if c['scope']=='parent'];natives=[c for c in cs if c['scope']=='native']
put(R/'strategy_direction_conclusion.json',{'passed_evidence_validation':True,'report_sha256':sha(R/'report.json'),'new_actual_configs':12,'cost_scenes':36,'historical_parent_passed':sum(c['status']=='passed' for c in parents),'native_rejected':sum(c['status']=='rejected' for c in natives),'same_initial_capital_native_prior_models_compared':aliases['prior_native_definitions_compared'],'same_initial_capital_parent_prior_models_compared':aliases['prior_parent_definitions_compared'],'new_configs_with_all3_saved_NAV_paths_seen_before':aliases['new_allcost_signatures_seen_in_prior_results'],'new_configs_strictly_dominated_by_matched_old_VC45_at_all3costs':control['rows_dominated_by_oldVC45_same_K_at_allcosts'],'new_configs_dominating_old_VC45_at_all3costs':control['rows_dominating_oldVC45_same_K_at_allcosts'],'parent_3x_return_range_pct':[min(c['scenes']['3']['net_return_pct'] for c in parents),max(c['scenes']['3']['net_return_pct'] for c in parents)],'parent_3x_whole_continuous_DD_range_pct':[min(c['scenes']['3']['max_drawdown_pct'] for c in parents),max(c['scenes']['3']['max_drawdown_pct'] for c in parents)],'paired_caps_allcost_NAV_paths_identical':True,'first_entry_difference_diagnostic':rel(R/'looser_entry_saved_path_diagnostics.json'),'interpretation':'较宽VC提高本次全期净收益，部分K也增加整体回撤。VC5与5.5各K下的已保存决策/实际NAV相同，不能视为独立收益证据或规则数学等价。全部ETH原生仍未达近期与局部一致性门槛，组合历史通过保留；邻接跳变提示不能声称广泛平坦平台。反复开发历史与多重试验不是独立最终/前向/稳定实盘，不修改冻结账户或门槛。','new_independent_future_validated':False,'completed_financial_or_observation_reruns':0})
li=rd(R/'l4h02_observation/input_manifest.json');qi=rd(R/'fewm_observation/input_manifest.json');attempts=rd(R/'candidate_transport_attempts.json');unique={(z['raw'],z['started_utc']):z for z in attempts+li['provenance']+qi['provenance']};failed=[]
for z in unique.values():
 assert sha(ROOT/z['raw'])==z['sha256'] and len(gzip.decompress((ROOT/z['raw']).read_bytes()))==z['bytes']
 if z.get('curl_exit_code',0) or z['http_status']!=200:failed.append(z)
errors=[{'log':z['log'],'stderr':z['stderr'],'observed_curl_error_codes':re.findall(r'curl: \((\d+)\)',z['stderr'])} for z in rd(R/'forward_commands.json') if 'curl:' in z.get('stderr','')]
put(R/'transport_failure_verification.json',{'passed':True,'fresh08_public_GETs':0,'original_prior08_public_fields_reused_with_original_retrieval_UTC':True,'deduplicated_actual_HTTP_attempts':len(unique),'failed_HTTP_attempts_preserved':failed,'SMA_transport_error_native_receipts':errors,'observed_actual_HTTP_or_transport_failures':len(failed)+sum(len(x['observed_curl_error_codes']) for x in errors),'all_actual_raw_bytes_retained':True,'FEWM_reused_public_data_not_double_counted':True,'completed_account_observation_reruns':0})
print('PASS18savedentrypathcomparisons/pairedcapsidentity;directionfromactualcriteria,transportfailurecount',len(failed)+sum(len(x['observed_curl_error_codes']) for x in errors))
