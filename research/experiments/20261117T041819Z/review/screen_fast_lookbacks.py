"""Full-registry semantic screen for genuine fast-window changes before any calculation."""
import json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import *
rs=reg.read_records(ROOT/'research/automation/registry.jsonl');broad=[];fixed={'return_hurdle':.02,'exit_buffer_fraction':.0075,'trend_lookback_days':16,'trend_slope_lag_days':3,'trend_slope_hurdle_fraction':.0075,'entry_volatility_window_days':6,'entry_volatility_ceiling':.05625,'entry_funding_settlement_count':4,'entry_funding_budget_volatility_window_days':8,'entry_direction_mode':'long_only','continuous_oos_days':391,'initial_capital_usdt':15000,'fixed_entry_notional_usdt':4000}
for fp,z in rs.items():
 sp=z.get('spec',{});q=sp.get('parameters',{})
 if sp.get('kind')=='strategy' and sp.get('universe')==['ETH/USDT'] and all(q.get(k)==v for k,v in fixed.items()):
  if z['result_available']:assert sha(ROOT/z['report'])==z['report_sha256']
  broad.append({'fingerprint':fp,'L':q['lookback_days'],'M':q['entry_funding_settlement_count'],'R':q['entry_funding_volatility_ratio'],'parameters':q,'status':z['status'],'result_available':z['result_available'],'report':z.get('report'),'report_sha256':z.get('report_sha256'),'spec':sp})
rows=[z for z in broad if z['R']==.0075];assert not any(z['L'] in [4,6] and (z['result_available'] or z['status']=='reserved') for z in rows);assert any(z['L']==5 and z['result_available'] for z in rows)
put(R/'fast_lookback_semantic_screen.json',{'passed':True,'recorded_utc':now(),'full_logical_registry_ids_read':len(rs),'matching_fixed_ETH_definitions':rows,'all_same_other_parameter_L_R':broad,'new_L':[4,6],'old_L':5,'fixed_R':.0075,'fixed_M':4,'fixed_VW':8,'no_model_account_or_registry_mutation':True});print('PASS genuineL4/L6atM4R.0075VW8absent;oldactualL/R',[(z['L'],z['R'],z['status']) for z in broad])
