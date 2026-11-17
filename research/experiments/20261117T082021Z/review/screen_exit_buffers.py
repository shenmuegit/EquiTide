"""Read full logical definitions for genuine exit-buffer changes, without financial calculation."""
import json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import *
rs=reg.read_records(ROOT/'research/automation/registry.jsonl');rows=[];fixed={'lookback_days':5,'return_hurdle':.02,'trend_lookback_days':16,'trend_slope_lag_days':3,'trend_slope_hurdle_fraction':.0075,'entry_volatility_window_days':6,'entry_volatility_ceiling':.05625,'entry_funding_settlement_count':4,'entry_funding_budget_volatility_window_days':8,'entry_direction_mode':'long_only','continuous_oos_days':391,'initial_capital_usdt':15000,'fixed_entry_notional_usdt':4000}
for fp,z in rs.items():
 sp=z.get('spec',{});q=sp.get('parameters',{})
 if sp.get('kind')=='strategy' and sp.get('universe')==['ETH/USDT'] and all(q.get(k)==v for k,v in fixed.items()):
  if z['result_available']:assert sha(ROOT/z['report'])==z['report_sha256']
  rows.append({'fingerprint':fp,'E':q['exit_buffer_fraction'],'R':q['entry_funding_volatility_ratio'],'parameters':q,'spec':sp,'status':z['status'],'result_available':z['result_available'],'report':z.get('report'),'report_sha256':z.get('report_sha256')})
exact=[z for z in rows if z['R']==.0075];assert not any(z['E'] in [.00625,.00875] and (z['result_available'] or z['status']=='reserved') for z in exact);assert any(z['E']==.0075 and z['result_available'] for z in exact)
put(R/'exit_buffer_semantic_screen.json',{'passed':True,'recorded_utc':now(),'logical_registry_ids_read':len(rs),'matching_fixed_ETH_definitions':exact,'all_same_other_parameter_E_R':rows,'new_E':[.00625,.00875],'old_E':.0075,'fixed_L':5,'fixed_H':.02,'fixed_M':4,'fixed_R':.0075,'fixed_VW':8,'no_model_account_or_registry_mutation':True});print('PASS newE.00625/.00875 absent at L5H.02M4/R.0075/VW8;oldE/R',[(z['E'],z['R'],z['status']) for z in rows])
