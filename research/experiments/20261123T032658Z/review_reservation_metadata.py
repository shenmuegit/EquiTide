"""Read actual reserve receipts and verify previously frozen coordinates and child scalars."""
from common import *
rd=lambda p:json.loads(p.read_text());p=rd(R/'plan.json');batch=rd(R/'batch.json');binding=rd(R/'code_binding_before_evaluation.json');rs=[z for f in sorted((R/'reserve_batches').glob('*.json')) for z in rd(f)['actual_command_receipts']];assert len(rs)==4 and all(z['exit_code']==0 for z in rs);first=min(z['started_utc'] for z in rs);assert binding['recorded_utc']<first and p['frozen_at_utc']<first;rows=[]
for z in batch:
 sp=rd(ROOT/z['spec']);q=sp['parameters'];assert sha(ROOT/z['spec'])==binding['immutable_source_sha256'][z['spec']] and q['ETH_entry_volatility_window_days']==6 and q['ETH_trend_slope_hurdle_fraction']==z['K'] in [.00625,.00875] and q['ETH_lookback_days']==5 and q['ETH_exit_buffer_fraction']==.0075 and q['ETH_trend_slope_lag_days']==3
 for asset,fp in zip(['BTC','ETH'],z['source_fingerprints']):
  child=rd(ROOT/p['read_only_references'][fp]['spec'])['parameters']
  for k,v in child.items():
   if asset+'_'+k in q:assert q[asset+'_'+k]==v,(asset,k)
 rows.append({'fingerprint':z['fingerprint'],'BTC_N':z['W'],'ETH_slope_K':z['K'],'ETH_V_fixed':6,'ETH_L_fixed':5,'ETH_E_fixed':.0075,'ETH_D_fixed':3,'raw_weights':[x['weight'] for x in sp['components']]})
put(R/'reservation_metadata_review.json',{'passed':True,'review_recorded_utc':now(),'review_is_after_reserve_not_relabelled_as_pre_reservation':True,'actual_frozen_plan_utc':p['frozen_at_utc'],'actual_code_binding_utc':binding['recorded_utc'],'actual_first_reserve_started_utc':first,'rows':rows,'previously_frozen_actual_child_specs_and_scalar_fields_consistent':True,'no_financial_or_account_execution':True});print('PASS4previouslyfrozenmetadata/actualreserveUTCs;slopeK.00625/.00875,V6,L5,E.0075,D3consistent')
