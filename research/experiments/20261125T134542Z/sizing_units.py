"""Check actual source parameters, original capital/notionals and both-axis neighborhood geometry."""
from common import *
from run import neighbors
rd=lambda p:json.loads(p.read_text());p=rd(R/'plan.json');assert p['axes']=={'BTC_ENTRY_VOLATILITY_CEILING':[.02625,.0275,.02875],'ETH_FUNDING_BUDGET_VOLATILITY_WINDOW_DAYS':[7,9,12]}
full={g['fingerprint']:g for g in p['grid']};baseBTC=rd(ROOT/p['read_only_references']['41de4309229b892489a07574af07a73ae93229a35c118558ed60362285e90c89']['spec'])['parameters'];baseETH=rd(ROOT/p['read_only_references'][p['baseline_native_fingerprint']]['spec'])['parameters']
for g in p['grid']:
 sp=rd(ROOT/g['spec']);b,e=[rd(ROOT/p['read_only_references'][fp]['spec'])['parameters'] for fp in g['source_fingerprints']]
 assert [x['weight'] for x in sp['components']]==[1,1] and b['initial_capital_usdt']==3750 and e['initial_capital_usdt']==15000 and b['fixed_entry_notional_usdt']==1000 and e['fixed_entry_notional_usdt']==4000
 assert b['return_hurdle']==.03 and b['entry_volatility_ceiling']==g['W'] and b['lookback_days']==29 and b['entry_volatility_window_days']==10 and b['exit_buffer_fraction']==.005 and b['entry_directional_confirmation_lookback_days']==5 and b['entry_directional_confirmation_hurdle']==.0025
 assert e['entry_volatility_ceiling']==.05625 and e['trend_slope_lag_days']==3 and e['entry_funding_budget_volatility_window_days']==g['K'] and e['entry_volatility_window_days']==6 and e['trend_slope_hurdle_fraction']==.0075 and e['entry_funding_volatility_ratio']==.0075 and e['entry_funding_max_age_hours']==36 and e['entry_funding_settlement_count']==4
 for child,base,axis,default,value in [(b,baseBTC,'entry_volatility_ceiling',.0275,g['W']),(e,baseETH,'entry_funding_budget_volatility_window_days',9,g['K'])]:
  diff={k for k in set(child)|set(base) if k not in {'persistence','prior_370day_source_fingerprint'} and child.get(k)!=base.get(k)};assert diff==({axis} if value!=default else set()),diff
 ns,dims=neighbors(g,p,full);expected=[x for x in p['grid'] if abs(p['axes']['BTC_ENTRY_VOLATILITY_CEILING'].index(x['W'])-p['axes']['BTC_ENTRY_VOLATILITY_CEILING'].index(g['W']))<=1 and abs(p['axes']['ETH_FUNDING_BUDGET_VOLATILITY_WINDOW_DAYS'].index(x['K'])-p['axes']['ETH_FUNDING_BUDGET_VOLATILITY_WINDOW_DAYS'].index(g['K']))<=1];assert dims==2 and {x['fingerprint'] for x in ns}=={x['fingerprint'] for x in expected}
put(R/'sizing_primitive_verification.json',{'passed':True,'all9_actual_parameter_maps_and_fixed1000_4000_amounts_checked':True,'only_selected_child_parameter_changes':True,'neighbor_geometry_checked':True,'no_market_or_account_execution':True});print('PASS9sourceparametercells/fixedcapitals/notionals/neighborgeometry')
