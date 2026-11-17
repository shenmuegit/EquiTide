"""Complete registry semantic screen before selecting any new median-count configuration."""
import json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import *
rs=reg.read_records(ROOT/'research/automation/registry.jsonl');rows=[]
fixed={'lookback_days':5,'return_hurdle':.02,'exit_buffer_fraction':.0075,'trend_lookback_days':16,'trend_slope_lag_days':3,'trend_slope_hurdle_fraction':.0075,'entry_volatility_window_days':6,'entry_volatility_ceiling':.05625,'entry_funding_budget_volatility_window_days':8,'entry_direction_mode':'long_only','continuous_oos_days':391,'initial_capital_usdt':15000,'fixed_entry_notional_usdt':4000}
for fp,z in rs.items():
 sp=z.get('spec',{});q=sp.get('parameters',{})
 if sp.get('kind')=='strategy' and sp.get('universe')==['ETH/USDT'] and all(q.get(k)==v for k,v in fixed.items()):
  if z['result_available']:assert sha(ROOT/z['report'])==z['report_sha256']
  rows.append({'fingerprint':fp,'M':q['entry_funding_settlement_count'],'R':q['entry_funding_volatility_ratio'],'parameters':q,'status':z['status'],'result_available':z['result_available'],'report':z.get('report'),'report_sha256':z.get('report_sha256'),'spec':sp})
assert not any(z['M'] in [2,3] and z['R']==.0075 and (z['result_available'] or z['status']=='reserved') for z in rows)
assert any(z['M']==4 and z['R']==.0075 and z['result_available'] for z in rows)
put(R/'tight_budget_median_prior_lookup.json',{'passed':True,'recorded_utc':now(),'full_logical_registry_ids_read':len(rs),'matching_fixed_ETH_definitions':rows,'new_M':[2,3],'fixed_R':.0075,'fixed_VW':8,'old_M4_center_and_looser_R001_counts_kept_readonly':True,'no_model_account_or_registry_mutation':True})
print('PASS genuineM2/M3atR.0075absent;knownactualM/R',[(z['M'],z['R'],z['status']) for z in rows])
