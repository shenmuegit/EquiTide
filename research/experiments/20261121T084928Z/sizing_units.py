"""Check actual amount and funding-count axes from each existing source spec."""
from common import *
rd=lambda p:json.loads(p.read_text());p=rd(R/'plan.json');assert p['axes']=={'BTC_ENTRY_TARGET_USDT':[750,1000,1125,1250,1375],'ETH_FUNDING_SETTLEMENT_COUNT':[4,5,6]} and len(p['read_only_references'])==22
from run import neighbors
full={g['fingerprint']:g for g in p['grid']}
for row in p['grid']:
 sp=rd(ROOT/row['spec']);children=[rd(ROOT/p['read_only_references'][fp]['spec'])['parameters'] for fp in row['source_fingerprints']];b,e=children;assert [x['weight'] for x in sp['components']]==[1,1] and b['fixed_entry_notional_usdt']==row['W'] and b['initial_capital_usdt']==3750 and e['fixed_entry_notional_usdt']==4000 and e['initial_capital_usdt']==15000 and e['entry_funding_settlement_count']==row['K'] and e['entry_funding_max_age_hours']==48 and e['lookback_days']==5 and e['return_hurdle']==.02 and e['entry_volatility_window_days']==6 and e['entry_volatility_ceiling']==.05625
 ns,dims=neighbors(row,p,full);expected=[g for g in p['grid'] if abs(p['axes']['BTC_ENTRY_TARGET_USDT'].index(g['W'])-p['axes']['BTC_ENTRY_TARGET_USDT'].index(row['W']))<=1 and abs(p['axes']['ETH_FUNDING_SETTLEMENT_COUNT'].index(g['K'])-p['axes']['ETH_FUNDING_SETTLEMENT_COUNT'].index(row['K']))<=1];assert dims==2 and {g['fingerprint'] for g in ns}=={g['fingerprint'] for g in expected}
 if not row['readonly']:
  q=sp['parameters'];assert q['component_initial_entry_notionals_usdt']==[row['W'],4000] and q['initial_target_total_notional_usdt']==row['W']+4000 and q['actual_native_quantity_and_impact_reused']
put(R/'sizing_primitive_verification.json',{'passed':True,'all15_actual_source_amount_and_count_maps_checked':True,'raw_wholebank_weights_unchanged':True,'component_orders_and_costs_not_linearly_resized':True,'two_axis_neighbor_geometry_checked':True,'no_market_or_account_execution':True});print('PASS15actualsourceamount/countmaps+geometry')
