"""Read saved separate-VW budgets versus exact original VW10/R.0075 paths."""
import gzip,json,re,sys
from decimal import Decimal as D
from fractions import Fraction as F
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));from common import sha,put,rel
rd=lambda p:json.loads(p.read_text());gz=lambda p:json.loads(gzip.decompress(p.read_bytes()));r=rd(R/'report.json');p=rd(R/'plan.json');cache={};rows=[];byday={x['decision_index']:x for x in rd(R/'funding_signal_preflight.json')['assets']['ETH']['all_source_selections']}
def archive(path,h):
 assert sha(ROOT/path)==h
 if path not in cache:cache[path]=gz(ROOT/path)
 return cache[path]
for c in r['configs'].values():
 if c['scope']!='native':continue
 assert c['M']==4 and c['VW'] in [8,10,12] and c['R'] in [.00625,.0075,.00875];ref=p['read_only_references'][c['reference_fingerprint']];a=archive(c['archive'],c['archive_sha256']);o=archive(ref['archive'],ref['archive_sha256'])
 for k in ['1','2','3']:
  new,old=a['scenes'][k]['decisions'],o['scenes'][k]['decisions'];assert len(new)==len(old)==370;diff=[];blocked=applied=0;caps=[];sigma_diffs=0
  for x,y in zip(new,old):
   assert x['execution_ts_ns']==y['execution_ts_ns'] and x['signal_available_ts_ns']==y['signal_available_ts_ns']<x['execution_ts_ns'];xx,yy=x['policy_audit'],y['policy_audit']
   for key in ['return_exact','slow_mean_exact','slow_reference_mean_exact','slow_distance_exact','observed_sample_logvol','entry_volatility_ceiling','slope_hurdle_fraction']:assert xx[key]==yy[key]
   f,of=xx['funding_filter'],yy['funding_filter'];src=byday[x['decision_index']];hours=D(src['latest_actual_interval_hours']);budget=min(D('.0002'),D(str(c['R']))*D(f['budget_sigma_daily'])*hours/D(24));oldbudget=min(D('.0002'),D('.0075')*D(of['budget_sigma_daily'])*hours/D(24));assert src['latest_interval_both_sources_available'] and D(f['latest_past_interval_hours'])==D(of['latest_past_interval_hours'])==hours and D(f['cap_fraction_per_settlement'])==budget and D(of['cap_fraction_per_settlement'])==oldbudget and f['selected_settlements']==of['selected_settlements'] and f['median_realized_rate']==of['median_realized_rate'] and f['settlement_count']==of['settlement_count']==4 and f['budget_volatility_window_days']==c['VW'] and xx['volatility_window_days']==yy['volatility_window_days']==10
   if c['VW']==10:assert f['budget_sigma_daily']==of['budget_sigma_daily']
   sigma_diffs+=f['budget_sigma_daily']!=of['budget_sigma_daily'];caps.append(float(budget));applied+=f['applied'];blocked+=f['blocked']
   if f['blocked']:assert f['applied'] and x['desired_direction']==0 and F(f['expected_outflow_fraction'])>F(budget)
   if x['desired_direction']!=y['desired_direction']:diff.append((x,y))
  first=None
  if diff:
   x,y=diff[0];fa,of=x['policy_audit']['funding_filter'],y['policy_audit']['funding_filter'];assert x['state_before']==y['state_before'] and x['policy_audit']['raw_desired_before_funding_filter']==y['policy_audit']['raw_desired_before_funding_filter'] and fa['blocked']!=of['blocked'];lo,hi=sorted([F(fa['cap_fraction_per_settlement']),F(of['cap_fraction_per_settlement'])]);assert lo<F(fa['expected_outflow_fraction'])<=hi
   first={'execution_utc':datetime.fromtimestamp(x['execution_ts_ns']//10**9,timezone.utc).isoformat(),'M':4,'budget_VW':c['VW'],'R':c['R'],'same_predecision_book':True,'same_past_price_gate_features':True,'new_funding_audit':fa,'old_funding_audit':of,'old_desired':y['desired_direction'],'new_desired':x['desired_direction']}
  rows.append({'fingerprint':c['fingerprint'],'M':4,'budget_VW':c['VW'],'R':c['R'],'cost':k,'old_VW10_R0075_control':c['reference_fingerprint'],'dynamic_cap_min_max':[min(caps),max(caps)],'different_budget_sigma_days':sigma_diffs,'filter_applied_days':applied,'filter_blocked_days':blocked,'different_saved_desired_direction_days':len(diff),'first_difference':first,'control_full_NAV_hash_equal':c['scenes'][k]['NAV_sha256_f64le']==o['scenes'][k]['summary']['NAV_sha256_f64le']})
assert len(rows)==24
put(R/'entry_hurdle_saved_path_diagnostics.json',{'passed':True,'report_sha256':sha(R/'report.json'),'artifact_name_legacy':True,'rows':rows,'scope':'SavedactualbudgetVW/RvsoldVW10R.0075.IndependentDecimalcapfromaudit-verifiedhistoricalVWsamplevol/actualinterval;pricegateV10same,firstbook/strictthresholdchecked.No newvaluation.'})
control=rd(R/'relative_control_diagnostic.json')['summary'];aliases=rd(R/'same_bank_realized_NAV_alias_diagnostic.json');parents=[c for c in r['configs'].values() if c['scope']=='parent'];natives=[c for c in r['configs'].values() if c['scope']=='native']
put(R/'strategy_direction_conclusion.json',{'passed_evidence_validation':True,'report_sha256':sha(R/'report.json'),'new_actual_configs':16,'cost_scenes':48,'axes':['budget_VW','R'],'fixed_funding_M':4,'fixed_pricegate_V':10,'historical_parent_passed':sum(c['status']=='passed' for c in parents),'native_rejected':sum(c['status']=='rejected' for c in natives),'prior_native_models_compared':aliases['prior_native_definitions_compared'],'prior_parent_models_compared':aliases['prior_parent_definitions_compared'],'new_configs_with_all3_saved_NAV_paths_seen_before':aliases['new_allcost_signatures_seen_in_prior_results'],'matched_center_comparison':control,'parent_3x_return_range_pct':[min(c['scenes']['3']['net_return_pct'] for c in parents),max(c['scenes']['3']['net_return_pct'] for c in parents)],'parent_3x_whole_continuous_DD_range_pct':[min(c['scenes']['3']['max_drawdown_pct'] for c in parents),max(c['scenes']['3']['max_drawdown_pct'] for c in parents)],'interpretation':'按预设门槛判断。旧中心VW10/R.0075资格保持，本轮VW/R邻域仅另作诊断，不能因旧passed字样称新邻域通过。最佳边界/历史微小增益/别名仍属多重选择开发历史，非独立未来或稳定实盘。四原账户不采用研究参数。','new_independent_future_validated':False,'completed_financial_or_observation_reruns':0})

li=rd(R/'l4h02_observation/input_manifest.json');qi=rd(R/'fewm_observation/input_manifest.json');attempts=rd(R/'candidate_transport_attempts.json');unique={(z['raw'],z['started_utc']):z for z in attempts+li['provenance']+qi['provenance']};failed=[]
for z in unique.values():
 assert sha(ROOT/z['raw'])==z['sha256'] and len(gzip.decompress((ROOT/z['raw']).read_bytes()))==z['bytes']
 if z.get('curl_exit_code',0) or z['http_status']!=200:failed.append(z)
errors=[{'log':z['log'],'stderr':z['stderr'],'observed_curl_error_codes':re.findall(r'curl: \((\d+)\)',z['stderr'])} for z in rd(R/'forward_commands.json') if 'curl:' in z.get('stderr','')]
put(R/'transport_failure_verification.json',{'passed':True,'fresh00_public_GETs':0,'original00_public_GETs':len(rd(R/'funding00_current_preflight_receipts.json')),'fresh08_public_GETs':0,'fresh16_public_GETs':0,'original_prior08_and16_public_fields_reused_with_original_retrieval_UTC':True,'deduplicated_actual_HTTP_attempts':len(unique),'failed_HTTP_attempts_preserved':failed,'SMA_transport_error_native_receipts':errors,'observed_actual_HTTP_or_transport_failures':len(failed)+sum(len(x['observed_curl_error_codes']) for x in errors),'all_actual_raw_bytes_retained':True,'FEWM_reused_public_data_not_double_counted':True,'completed_account_observation_reruns':0})
print('PASS24savedVW/Rbudgetcomparisons,fullNAValiases,fixedK/VC;transportfailures',len(failed)+sum(len(x['observed_curl_error_codes']) for x in errors))
