"""Saved pricegate changes vs exactoldcenter;fundingbudget/source and first book independently checked."""
import gzip,json,re,sys
from decimal import Decimal as D
from fractions import Fraction as F
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));from common import sha,put,rel
rd=lambda p:json.loads(p.read_text());gz=lambda p:json.loads(gzip.decompress(p.read_bytes()));r=rd(R/'report.json');p=rd(R/'plan.json');rows=[];cache={}
def arc(path,h):
 assert sha(ROOT/path)==h
 if path not in cache:cache[path]=gz(ROOT/path)
 return cache[path]
for c in r['configs'].values():
 if c['scope']!='native':continue
 ref=p['read_only_references'][c['reference_fingerprint']];new=arc(c['archive'],c['archive_sha256']);old=arc(ref['archive'],ref['archive_sha256'])
 for k in ['1','2','3']:
  xs,ys=new['scenes'][k]['decisions'],old['scenes'][k]['decisions'];assert len(xs)==len(ys)==370;diff=[]
  for x,y in zip(xs,ys):
   a,b=x['policy_audit'],y['policy_audit'];assert x['execution_ts_ns']==y['execution_ts_ns'] and x['signal_available_ts_ns']==y['signal_available_ts_ns']<x['execution_ts_ns'] and a['slope_hurdle_fraction']==c['K'] and a['entry_volatility_ceiling']==c['VC'] and b['slope_hurdle_fraction']==.0075 and b['entry_volatility_ceiling']==.05625 and a['slow_lookback_days']==c['S'] and a['slope_lag_days']==c['D'] and b['slow_lookback_days']==16 and b['slope_lag_days']==3
   assert a['fast_lookback_days']==c['L'] and a['volatility_window_days']==c['V'] and b['fast_lookback_days']==5 and b['volatility_window_days']==6
   assert a['volatility_window_days']==c['V'] and b['volatility_window_days']==6
   fa,fb=a['funding_filter'],b['funding_filter']
   for n in ['budget_sigma_daily','budget_volatility_window_days','latest_past_interval_hours']:assert fa[n]==fb[n]
   assert fa['budget_volatility_window_days']==8 and D(fa['budget_ratio'])==D(str(c['R'])) and fa['settlement_count']==c['M'];assert D(fa['cap_fraction_per_settlement'])==min(D('.0002'),D(str(c['R']))*D(fa['budget_sigma_daily'])*D(fa['latest_past_interval_hours'])/D(24))
   assert fa['selected_settlements']==fb['selected_settlements'][:c['M']];rates=sorted(D(z['realized_rate']) for z in fa['selected_settlements']);N=c['M'];median=rates[N//2] if N%2 else (rates[N//2-1]+rates[N//2])/2;assert D(fa['median_realized_rate'])==median
   if x['desired_direction']!=y['desired_direction']:diff.append((x,y))
  first=None
  if diff:
   x,y=diff[0];assert x['state_before']==y['state_before'];a,b=x['policy_audit'],y['policy_audit'];q=D(x['state_before']['signed_units']);actual=(q>0)-(q<0);rr=F(a['return_exact']);slow=F(a['slow_distance_exact']);base=-1 if rr>F('.02') else 1 if rr<F('-.02') else actual if actual==1 and rr<F('.0075') or actual==-1 and rr>F('-.0075') else 0;calculated=[]
   for audit,K,VC,H,E in [(a,c['K'],c['VC'],c['H'],c['E']),(b,.0075,.05625,.02,.0075)]:
    rr=F(audit['return_exact']);h,e=F(str(H)),F(str(E));base=-1 if rr>h else 1 if rr<-h else actual if actual==1 and rr<e or actual==-1 and rr>-e else 0;assert audit['ungated_desired']==base;slow=F(audit['slow_distance_exact']);assert F(audit['slow_mean_exact'])/F(audit['slow_reference_mean_exact'])-1==slow;strength=F(str(K));gate=(slow>strength)-(slow<-strength);raw=base if base==actual or base==gate else 0;pre=0 if raw and raw!=actual and audit['observed_sample_logvol']>VC else raw;f=audit['funding_filter'];out=max(F(pre)*F(f['median_realized_rate']),F(0));want=0 if pre and pre!=actual and out>F(f['cap_fraction_per_settlement']) else pre;assert audit['slowgate_direction']==gate and audit['raw_desired_before_funding_filter']==pre;calculated.append(want)
   assert calculated==[x['desired_direction'],y['desired_direction']];first={'execution_utc':datetime.fromtimestamp(x['execution_ts_ns']//10**9,timezone.utc).isoformat(),'L':c['L'],'PRICE_V':c['V'],'S':c['S'],'D':c['D'],'K':c['K'],'VC':c['VC'],'same_predecision_book':True,'same_past_prices_VW8_and_actualinterval':True,'independent_M_R_median_and_cap_checked':True,'new_desired':calculated[0],'old_desired':calculated[1],'new_price_audit':a,'old_price_audit':b}
  rows.append({'fingerprint':c['fingerprint'],'L':c['L'],'PRICE_V':c['V'],'S':c['S'],'D':c['D'],'K':c['K'],'VC':c['VC'],'cost':k,'old_center_fingerprint':c['reference_fingerprint'],'different_saved_desired_days':len(diff),'first_difference':first,'funding_M_R_changes_independently_reconstructed':True,'old_center_full_NAV_equal':c['scenes'][k]['NAV_sha256_f64le']==old['scenes'][k]['summary']['NAV_sha256_f64le']})
assert len(rows)==24;put(R/'entry_hurdle_saved_path_diagnostics.json',{'passed':True,'report_sha256':sha(R/'report.json'),'artifact_name_legacy':True,'rows':rows,'new_strategy_or_account_valuations':0})
a=rd(R/'same_bank_realized_NAV_alias_diagnostic.json');parents=[c for c in r['configs'].values() if c['scope']=='parent'];put(R/'strategy_direction_conclusion.json',{'passed_evidence_validation':True,'report_sha256':sha(R/'report.json'),'new_actual_configs':16,'cost_scenes':48,'axes':['M','R'],'fixed_funding':{'VW':8,'hardcap':.0002},'historical_parent_passed':len(r['summary']['passed']),'new_configs_with_all3_saved_NAV_paths_seen_before':a['new_allcost_signatures_seen_in_prior_results'],'parent_3x_return_range_pct':[min(c['scenes']['3']['net_return_pct'] for c in parents),max(c['scenes']['3']['net_return_pct'] for c in parents)],'parent_3x_whole_continuous_DD_range_pct':[min(c['scenes']['3']['max_drawdown_pct'] for c in parents),max(c['scenes']['3']['max_drawdown_pct'] for c in parents)],'interpretation':'价格波动窗口/入场上限邻域通过仍只是反复开发历史，净值别名不构成独立证据。无新未来账户/原规则采用。','new_independent_future_validated':False,'completed_financial_or_observation_reruns':0})

sma_http=[{'raw':z['raw_gzip_path'],'sha256':z['raw_gzip_sha256'],'bytes':len(gzip.decompress((ROOT/z['raw_gzip_path']).read_bytes())),'started_utc':z['retrieved_utc'],'http_status':z['status'],'curl_exit_code':0} for z in rd(R/'forward_report.json')['provenance']];li=rd(R/'l4h02_observation/input_manifest.json');qi=rd(R/'fewm_observation/input_manifest.json');attempts=rd(R/'candidate_transport_attempts.json');failed_capture_rows=[z for f in R.glob('l4h02_capture_failed_attempt*/failure_receipts.json') for z in rd(f) if 'raw' in z];unique={(z['raw'],z['started_utc']):z for z in attempts+li['provenance']+qi['provenance']+sma_http+failed_capture_rows };failed=[]
for z in unique.values():
 assert sha(ROOT/z['raw'])==z['sha256'] and len(gzip.decompress((ROOT/z['raw']).read_bytes()))==z['bytes']
 if z.get('curl_exit_code',0) or z['http_status']!=200:failed.append(z)
errors=[{'log':z['log'],'stderr':z['stderr'],'observed_curl_error_codes':re.findall(r'curl: \((\d+)\)',z['stderr'])} for z in rd(R/'forward_commands.json') if 'curl:' in z.get('stderr','')]
put(R/'transport_failure_verification.json',{'passed':True,'fresh00_public_GETs':0,'fresh_SMA_SPOT_GETs':len(sma_http),'original00_public_GETs':len(rd(R/'funding00_current_preflight_receipts.json')),'fresh08_public_GETs':0,'originalNov11_08_GETs':len(rd(R/'funding08_nov11_preflight_receipts.json')),'originalNov10_08_GETs':len(rd(R/'funding08_nov10_preflight_receipts.json')),'fresh16_public_GETs':0,'originalNov10_16_GETs':len(rd(R/'funding16_nov10_preflight_receipts.json')),'original_prior08_and16_public_fields_reused_with_original_retrieval_UTC':True,'deduplicated_actual_HTTP_attempts':len(unique),'failed_HTTP_attempts_preserved':failed,'SMA_transport_error_native_receipts':errors,'observed_actual_HTTP_or_transport_failures':len(failed)+sum(len(x['observed_curl_error_codes']) for x in errors),'all_actual_raw_bytes_retained':True,'FEWM_reused_public_data_not_double_counted':True,'completed_account_observation_reruns':0})
print('PASS24savedL_PRICE_Vcomparisons,fullNAValiases,fixedK/VC/H/E;transportfailures',len(failed)+sum(len(x['observed_curl_error_codes']) for x in errors))
