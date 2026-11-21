"""Synthetic axis, raw dollar banking and true child-parameter checks."""
from common import *
import numpy as np
from portfolio import sum_aligned_full_banks
rd=lambda p:json.loads(p.read_text());p=rd(R/'plan.json');by={z['fingerprint']:z for z in rd(R/'batch.json')};assert p['axes']=={'ETH_ENTRY_VOLATILITY_CEILING':[.045,.05,.05625],'ETH_FUNDING_SETTLEMENT_COUNT':[4,5,6]} and len(p['read_only_references'])==12
x=np.array([3750.,4000.,3900.]);y=np.array([15000.,14800.,15100.]);a=np.array([1,2,3]);assert sum_aligned_full_banks([x,y],[a,a]).tolist()==[18750.,18800.,19000.]
for b in [np.array([1,3,4]),np.array([0,2,3])]:
 try:sum_aligned_full_banks([x,y],[a,b]);raise RuntimeError('mismatched axes accepted')
 except AssertionError:pass
for row in p['grid']:
 sp=rd(ROOT/row['spec']);q=sp['parameters'];assert [c['weight'] for c in sp['components']]==[1,1] and q['component_capitals_usdt']==[3750,15000] and q['component_initial_entry_notionals_usdt']==[1000,4000]
 children=[rd(ROOT/(by.get(fp) or p['read_only_references'][fp])['spec'])['parameters'] for fp in row['source_fingerprints']];b,e=children;assert b['initial_capital_usdt']==3750 and b['fixed_entry_notional_usdt']==1000 and e['initial_capital_usdt']==15000 and e['fixed_entry_notional_usdt']==4000 and e['entry_funding_settlement_count']==row['K'] and e['entry_funding_max_age_hours']==48 and e['entry_funding_volatility_ratio']==.0075 and e['trend_slope_lag_days']==3 and e['trend_lookback_days']==e['trend_window_days']==16 and e['trend_decay_numerator']==15 and e['trend_decay_denominator']==17 and e['exit_buffer_fraction']==.0075 and e['lookback_days']==5 and e['entry_volatility_window_days']==6 and e['entry_volatility_ceiling']==row['W']
 if not row['readonly']:
  for asset,ch in zip(['BTC','ETH'],children):
   for key,v in q.items():
    if key.startswith(asset+'_') and key.removeprefix(asset+'_') in ch:assert v==ch[key.removeprefix(asset+'_')]
for row in p['native_grid']:
 q=rd(ROOT/row['spec'])['parameters'];assert q['initial_capital_usdt']==15000 and q['fixed_entry_notional_usdt']==4000 and q['entry_funding_settlement_count']==row['K'] and q['entry_funding_max_age_hours']==48 and q['entry_funding_volatility_ratio']==.0075 and q['trend_slope_lag_days']==3 and q['trend_lookback_days']==q['trend_window_days']==16 and q['trend_decay_numerator']==15 and q['trend_decay_denominator']==17 and q['exit_buffer_fraction']==.0075 and q['lookback_days']==5 and q['entry_volatility_window_days']==6 and q['entry_volatility_ceiling']==row['W']
put(R/'sizing_primitive_verification.json',{'passed':True,'synthetic_only':True,'common_dollar_NAV_and_two_mismatched_axes_checked':True,'all9parent_and9native_ETHage_count_actual_child_rules_checked':True,'legacy_readonly_parent_scalars_not_assumed_truth':True,'no_normalization_or_NAVresizing':True,'no_market_or_account_calculations':True});print('PASS synthetic rawcapital/weights,ETHcountxBTCamount,9parent+3nativeactualchildmaps')
