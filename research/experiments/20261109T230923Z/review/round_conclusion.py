"""Read saved funding-filter causality, matched off paths, and actual transport receipts."""
import gzip,json,re,sys
from decimal import Decimal as D
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
 assert c['L']==5 and c['H'] in [.0175,.02,.0225] and c['F'] in [0,.00005] and c['E']==.0075 and c['K']==.0075 and c['VC']==.05;ref=p['read_only_references'][c['reference_fingerprint']];a=archive(c['archive'],c['archive_sha256']);o=archive(ref['archive'],ref['archive_sha256'])
 for k in ['1','2','3']:
  new,old=a['scenes'][k]['decisions'],o['scenes'][k]['decisions'];assert len(new)==len(old)==370;diff=[];blocked=applied=0
  for x,y in zip(new,old):
   assert x['execution_ts_ns']==y['execution_ts_ns'] and x['signal_available_ts_ns']<x['execution_ts_ns'];xx,yy=x['policy_audit'],y['policy_audit'];assert xx['fast_lookback_days']==yy['fast_lookback_days']==5 and xx['exit_buffer_fraction']==yy['exit_buffer_fraction']==.0075 and xx['long_entry_return_hurdle']==xx['short_entry_return_hurdle']==yy['long_entry_return_hurdle']==yy['short_entry_return_hurdle']==c['H']
   for key in ['return_exact','slow_mean_exact','slow_reference_mean_exact','slow_distance_exact','observed_sample_logvol','entry_volatility_ceiling','slope_hurdle_fraction']:assert xx[key]==yy[key]
   f=xx['funding_filter'];sn=x['signal_available_ts_ns'];assert 3600*10**9<=sn-f['selected_settlement_ts_ns']<=12*3600*10**9 and f['selected_available_ts_ns']<=sn and f['signal_available_ts_ns']==sn and D(f['cap_fraction_per_settlement'])==D(str(c['F']))
   applied+=f['applied'];blocked+=f['blocked']
   if f['blocked']:assert f['applied'] and x['desired_direction']==0 and xx['raw_desired_before_funding_filter']!=0 and D(f['expected_outflow_fraction'])>D(str(c['F']))
   if x['desired_direction']!=y['desired_direction']:diff.append((x,y))
  first=None
  if diff:
   x,y=diff[0];fa=x['policy_audit']['funding_filter'];assert x['state_before']==y['state_before'] and fa['blocked'] and x['desired_direction']==0 and y['desired_direction']==x['policy_audit']['raw_desired_before_funding_filter']
   first={'execution_utc':datetime.fromtimestamp(x['execution_ts_ns']//10**9,timezone.utc).isoformat(),'fixed_H':c['H'],'new_F':c['F'],'old_F':'Off','same_predecision_book':True,'same_past_price_features':True,'causal_funding_gate_is_first_divergence':True,'funding_audit':fa,'old_desired':y['desired_direction'],'new_desired':x['desired_direction']}
  pairs=[z for z in r['configs'].values() if z['scope']=='native' and z['H']==c['H'] and z['F']!=c['F']];assert len(pairs)==1;rows.append({'fingerprint':c['fingerprint'],'L':5,'H':c['H'],'F':c['F'],'E':.0075,'cost':k,'filterOff_same_H_control_fingerprint':c['reference_fingerprint'],'filter_applied_days':applied,'filter_blocked_days':blocked,'different_saved_desired_direction_days':len(diff),'first_difference':first,'old_control_full_NAV_hash_equal':c['scenes'][k]['NAV_sha256_f64le']==o['scenes'][k]['summary']['NAV_sha256_f64le'],'other_F_same_H_full_NAV_hash_equal':c['scenes'][k]['NAV_sha256_f64le']==pairs[0]['scenes'][k]['NAV_sha256_f64le']})
assert len(rows)==18
put(R/'entry_hurdle_saved_path_diagnostics.json',{'passed':True,'report_sha256':sha(R/'report.json'),'rows':rows,'artifact_name_legacy':True,'scope':'Saved actual H/F decisions/fullNAV;0newvaluations. SameH/E/pricefeatures/firstbook,firstdivergencefrompasteligiblefundinggate. Allselectedrateavailability/age/thresholdschecked;noactualfutureorunmaturedcurrentrate. Aliasesnotindependentproof.'})
control=rd(R/'relative_control_diagnostic.json')['summary'];aliases=rd(R/'same_bank_realized_NAV_alias_diagnostic.json');cs=list(r['configs'].values());parents=[c for c in cs if c['scope']=='parent'];natives=[c for c in cs if c['scope']=='native']
put(R/'strategy_direction_conclusion.json',{'passed_evidence_validation':True,'report_sha256':sha(R/'report.json'),'new_actual_configs':12,'cost_scenes':36,'axes':['ETH_H','ETH_F'],'fixed_E':.0075,'fixed_K':.0075,'fixed_VC':.05,'historical_parent_passed':sum(c['status']=='passed' for c in parents),'native_rejected':sum(c['status']=='rejected' for c in natives),'prior_native_models_compared':aliases['prior_native_definitions_compared'],'prior_parent_models_compared':aliases['prior_parent_definitions_compared'],'new_configs_with_all3_saved_NAV_paths_seen_before':aliases['new_allcost_signatures_seen_in_prior_results'],'new_configs_dominated_by_filterOff_at_all3costs':control['rows_dominated_by_filterOff_same_H_at_allcosts'],'new_configs_dominating_filterOff_at_all3costs':control['rows_dominating_filterOff_same_H_at_allcosts'],'parent_3x_return_range_pct':[min(c['scenes']['3']['net_return_pct'] for c in parents),max(c['scenes']['3']['net_return_pct'] for c in parents)],'parent_3x_whole_continuous_DD_range_pct':[min(c['scenes']['3']['max_drawdown_pct'] for c in parents),max(c['scenes']['3']['max_drawdown_pct'] for c in parents)],'saved_entry_funding_difference_diagnostic':rel(R/'entry_hurdle_saved_path_diagnostics.json'),'interpretation':'资金费过滤H/F全部按预设门槛判断，净正或减少carry不等于近期/逐月稳定；全失败/路径别名保留。既有保守1h可用时延非历史到达证明。重复开发历史非独立未来/稳定实盘，不改冻结账户/权重/门槛。','new_independent_future_validated':False,'completed_financial_or_observation_reruns':0})
li=rd(R/'l4h02_observation/input_manifest.json');qi=rd(R/'fewm_observation/input_manifest.json');attempts=rd(R/'candidate_transport_attempts.json');unique={(z['raw'],z['started_utc']):z for z in attempts+li['provenance']+qi['provenance']};failed=[]
for z in unique.values():
 assert sha(ROOT/z['raw'])==z['sha256'] and len(gzip.decompress((ROOT/z['raw']).read_bytes()))==z['bytes']
 if z.get('curl_exit_code',0) or z['http_status']!=200:failed.append(z)
errors=[{'log':z['log'],'stderr':z['stderr'],'observed_curl_error_codes':re.findall(r'curl: \((\d+)\)',z['stderr'])} for z in rd(R/'forward_commands.json') if 'curl:' in z.get('stderr','')]
put(R/'transport_failure_verification.json',{'passed':True,'fresh08_public_GETs':0,'fresh16_public_GETs':0,'original_prior08_and16_public_fields_reused_with_original_retrieval_UTC':True,'deduplicated_actual_HTTP_attempts':len(unique),'failed_HTTP_attempts_preserved':failed,'SMA_transport_error_native_receipts':errors,'observed_actual_HTTP_or_transport_failures':len(failed)+sum(len(x['observed_curl_error_codes']) for x in errors),'all_actual_raw_bytes_retained':True,'FEWM_reused_public_data_not_double_counted':True,'completed_account_observation_reruns':0})
print('PASS18savedH/Ffundingcomparisons,fullNAValiases,fixedK/VC;transportfailures',len(failed)+sum(len(x['observed_curl_error_codes']) for x in errors))
