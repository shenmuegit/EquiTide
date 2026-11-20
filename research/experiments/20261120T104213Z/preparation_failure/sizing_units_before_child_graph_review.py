"""Synthetic common-axis and exact capital/parameter semantics, no backtest."""
import json,numpy as np
from common import *
from portfolio import sum_aligned_full_banks
p=json.loads((R/'plan.json').read_text());assert p['axes']=={'BTC_ENTRY_VOL_CEILING':[.026125,.0275,.028875],'ETH_ENTRY_N':[3500,3750,4000]} and len(p['grid'])==9 and len(p['native_grid'])==3 and len(p['read_only_references'])==16
x=np.array([3750.,4000.,3900.]);y=np.array([15000.,14800.,15100.]);a=np.array([1,2,3]);assert sum_aligned_full_banks([x,y],[a,a]).tolist()==[18750.,18800.,19000.]
for b in [np.array([1,3,4]),np.array([0,2,3])]:
 try:sum_aligned_full_banks([x,y],[a,b]);raise RuntimeError('mismatched axes accepted')
 except AssertionError:pass
for row in p['grid']:
 sp=json.loads((ROOT/row['spec']).read_text());q=sp['parameters'];assert [z['weight'] for z in sp['components']]==[1,1] and q['component_capitals_usdt']==[3750,15000] and q['component_initial_entry_notionals_usdt']==[1000,row['K']] and q['BTC_entry_volatility_ceiling']==row['W'] and q['BTC_entry_volatility_window_days']==10 and q['BTC_entry_notional_usdt']==1000 and q['ETH_entry_notional_usdt']==row['K']
for row in p['native_grid']:
 q=json.loads((ROOT/row['spec']).read_text())['parameters'];assert q['fixed_entry_notional_usdt']==1000 and q['initial_capital_usdt']==3750 and q['entry_volatility_ceiling']==row['W'] and q['entry_volatility_window_days']==10
put(R/'sizing_primitive_verification.json',{'passed':True,'synthetic_aligned_dollar_NAV_and_two_mismatched_axes_cases':3,'all9_parent_and3native_cap_vs_amount_mappings_checked':True,'no_normalization_NAVresizing_or_margin_netting':True,'no_market_or_original_account_evaluations':True});print('PASSsyntheticaxes,rawcapital3750/15000,9parent+3nativeVandNmaps;0marketmodels')
