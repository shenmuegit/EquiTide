"""Non-market parent quantity/capital invariants; no native accounting execution."""
import json,numpy as np
from common import *
from portfolio import sum_aligned_full_banks
p=json.loads((R/'plan.json').read_text());assert p['axes']=={'BTC_ENTRY_N':[750,1000,1500],'ETH_ENTRY_N':[3625,3750,3875]};assert len(p['grid'])==9 and len(p['read_only_references'])==18
x=np.array([3750.,4000.,3900.]);y=np.array([15000.,14800.,15100.]);t=np.array([1,2,3]);assert sum_aligned_full_banks([x,y],[t,t]).tolist()==[18750.,18800.,19000.]
for bad in [np.array([1,3,4]),np.array([0,2,3])]:
 try:sum_aligned_full_banks([x,y],[t,bad]);raise RuntimeError('misaligned axes accepted')
 except AssertionError:pass
for B in p['axes']['BTC_ENTRY_N']:
 for E in p['axes']['ETH_ENTRY_N']:
  row=next(z for z in p['grid'] if z['W']==B and z['K']==E);sp=json.loads((ROOT/row['spec']).read_text());assert [z['weight'] for z in sp['components']]==[1,1];assert 4375<=B+E<=5375
put(R/'sizing_primitive_verification.json',{'passed':True,'synthetic_aligned_dollarNAV_and_2mismatched_axes_cases':3,'all9componentgraphs_and_raw_weights_preserved':True,'no_normalization_return_scaling_or_margin_netting':True,'no_market_or_original_account_evaluations':True});print('PASS aligneddollarNAVsum,mismatchedaxestrap,9rawwholebankcapital/targetmaps;0marketmodels')
