"""Compare saved original ETH bank decisions and cashflows; execute no model or account."""
from common import *
rd=lambda p:json.loads(p.read_text());plan=rd(R/'plan.json');reporthash=sha(R/'report.json');refs=plan['read_only_references'];banks={}
for z in refs.values():
 if z['scope']=='native' and z['asset']=='ETH' and z['role']=='component':
  sp=rd(ROOT/z['spec']);q=sp['parameters'];lag=q['trend_slope_lag_days'];assert lag in [2,3,4] and q['entry_funding_budget_volatility_window_days']==9 and q['trend_slope_hurdle_fraction']==.0075
  arc=json.loads(gzip.decompress((ROOT/z['archive']).read_bytes()));assert sha(ROOT/z['archive'])==z['archive_sha256'] and arc['spec']==sp;banks[lag]=(z,arc)
assert set(banks)=={2,3,4};rows=[];keys=['gross_reference_price_PnL_usdt','funding_usdt','cost_usdt','final_NAV_usdt','round_trips','executions']
for lag,(ref,arc) in sorted(banks.items()):
 for cost,z in arc['scenes'].items():
  old=banks[3][1]['scenes'][cost];a,b=z['decisions'],old['decisions'];assert len(a)==len(b)==391 and [x['signal_available_ts_ns'] for x in a]==[x['signal_available_ts_ns'] for x in b];v=z['summary'];o=old['summary'];delta={k:v[k]-o[k] for k in keys};assert abs(delta['gross_reference_price_PnL_usdt']+delta['funding_usdt']-delta['cost_usdt']-delta['final_NAV_usdt'])<1e-8
  rows.append({'ETH_trend_lag_days':lag,'cost_multiplier':int(cost),'fingerprint':ref['fingerprint'],'fixed_funding_budget_volatility_window_days':9,'different_saved_slowgate_directions_to_D3':sum(x['policy_audit']['slowgate_direction']!=y['policy_audit']['slowgate_direction'] for x,y in zip(a,b)),'different_saved_final_desired_days_to_D3':sum(x['desired_direction']!=y['desired_direction'] for x,y in zip(a,b)),'actual_summary':{k:v[k] for k in keys},'delta_to_old_D3':delta,'NAV_sha256':v['NAV_sha256_f64le']})
assert len(rows)==9 and sha(R/'report.json')==reporthash;put(R/'trend_lag_economic_review.json',{'passed':True,'recorded_utc':now(),'completed_financial_report_sha256_unchanged':reporthash,'source_bank_capital_usdt':15000,'source_actual_entry_target_usdt':4000,'rows':rows,'cashflow_difference_identity_verified':True,'actual_saved_results_only':True,'new_model_or_account_executions':0,'parent_bank_multiplier_literal_one':True});print(json.dumps({'passed':True,'rows':9,'cost1_nonbaseline':[z for z in rows if z['cost_multiplier']==1 and z['ETH_trend_lag_days']!=3]}))
