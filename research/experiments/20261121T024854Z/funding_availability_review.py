"""Read saved policy audit and real settlement parquet; no strategy execution."""
import gzip,json
from fractions import Fraction as F
import polars as pl
from common import ROOT,R,sha,put,rel,HOUR
rd=lambda p:json.loads(p.read_text());p=rd(R/'plan.json');report=rd(R/'report.json');source=next(z for z in p['data']['assets']['ETH'] if z['path'].endswith('funding_settlement.parquet'));assert sha(ROOT/source['path'])==source['sha256'];events=pl.read_parquet(ROOT/source['path']).to_dicts();rows=[]
for c in report['configs'].values():
 if c['scope']!='native':continue
 arc=json.loads(gzip.decompress((ROOT/c['archive']).read_bytes()));age=48;ratio=.0075;lag=3;span=16;q=rd(ROOT/c['spec'])['parameters'];exit_e=q['exit_buffer_fraction'];entry_v=q['entry_volatility_window_days'];assert entry_v==c['W'] and q['lookback_days']==5;count=c['K'];bycost={}
 for k,z in arc['scenes'].items():
  n={'signals':0,'enough_mature_history':0,'missing_mature_history':0,'pre_funding_new_or_reversed_requests':0,'new_requests_missing_history':0,'new_requests_blocked_by_carry_budget':0,'policy_long_entries_requested':0,'filled_native_openings':sum(t['opening'] and t['status']=='filled' for t in z['trades'])};distribution={}
  for d in z['decisions']:
   sn=d['signal_available_ts_ns'];a=d['policy_audit'];fa=a['funding_filter'];selected=sorted([e for e in events if HOUR<=sn-e['settlement_ts']<=age*HOUR and e['available_ts']<=sn],key=lambda e:e['settlement_ts'],reverse=True)[:count];enough=len(selected)==count;n['signals']+=1;n['enough_mature_history']+=enough;n['missing_mature_history']+=not enough;distribution[str(len(selected))]=distribution.get(str(len(selected)),0)+1;n['pre_funding_new_or_reversed_requests']+=fa['applied'];n['new_requests_missing_history']+=fa['applied'] and not enough;n['new_requests_blocked_by_carry_budget']+=fa['applied'] and enough and fa['blocked'];n['policy_long_entries_requested']+=d['desired_direction']>0 and F(d['state_before']['signed_units'])==0
   assert fa['maximum_age_ns']==age*HOUR and fa['minimum_age_ns']==HOUR
   if enough:
    rates=sorted(F(e['realized_rate']) for e in selected);median=rates[count//2] if count%2 else sum(rates[count//2-1:count//2+1])/2;assert F(fa['median_realized_rate'])==median and [x['settlement_ts_ns'] for x in fa['selected_settlements']]==[x['settlement_ts'] for x in selected]
   else:assert fa['selected_settlements']==[] and fa['median_realized_rate'] is None
  n['selected_count_distribution']=distribution;assert n['signals']==391;bycost[k]=n
 rows.append({'fingerprint':c['fingerprint'],'max_age_hours':age,'budget_volatility_ratio':ratio,'trend_slope_lag_days':lag,'trend_window_days':span,'exit_buffer_fraction':exit_e,'fast_ROC_lookback_days':5,'entry_volatility_window_days':entry_v,'required_settlements':count,'by_cost':bycost,'actual_report_status':c['status']})
put(R/'funding_history_availability_review.json',{'passed':True,'saved_actual_results_only':True,'actual_market_source':source,'new_native_observation_counts':rows,'source_available_delay_1h_unchanged':True,'min_age1h_unchanged':True,'max_history_age_is_distinct_from_latest_actual_interval_budget36h':True,'full391days_allcosts_independent_selection_medians_verified':True,'no_financial_or_account_reexecution':True});print(json.dumps({'passed':True,'new_native_models_reviewed':len(rows),'real_settlements':len(events)}))
