"""Check both BTC axes, full source parameters and native/parent neighborhood before reserve."""
from common import *
from run import neighbors
rd=lambda p:json.loads(p.read_text());p=rd(R/'plan.json');base=rd(ROOT/p['read_only_references'][p['baseline_native_fingerprint']]['spec'])['parameters'];native={x['fingerprint']:x for x in p['native_grid']};allrows={**native,**{x['fingerprint']:x for x in p['grid']}}
for g in p['native_grid']:
 q=rd(ROOT/g['spec'])['parameters'];assert q['lookback_days']==g['W'] and q['return_hurdle']==g['K'] and q['initial_capital_usdt']==3750 and q['fixed_entry_notional_usdt']==1000
 diff={k for k in set(q)|set(base) if q.get(k)!=base.get(k) and k not in {'persistence','prior_370day_source_fingerprint'}};expected=set()
 if g['W']!=29:expected.add('lookback_days')
 if g['K']!=.03:expected.add('return_hurdle')
 assert diff==expected,(g['name'],diff,expected)
 assert q['entry_volatility_window_days']==10 and q['entry_volatility_ceiling']==.0275 and q['entry_directional_confirmation_hurdle']==.0025 and q['entry_directional_confirmation_lookback_days']==5 and q['exit_buffer_fraction']==.005 and q['warmup_days']==33
for g in p['grid']:
 q=rd(ROOT/g['spec'])['parameters'];assert q['initial_capital_usdt']==18750 and q['component_capitals_usdt']==[3750,15000] and q['component_initial_entry_notionals_usdt']==[1000,4000] and [z['weight'] for z in rd(ROOT/g['spec'])['components']]==[1,1]
for g in [*p['native_grid'],*p['grid']]:
 ns,dims=neighbors(g,p,allrows);rows=p['native_grid'] if g['scope']=='native' else p['grid'];expected=[x for x in rows if abs(p['axes']['BTC_MAIN_LOOKBACK_DAYS'].index(x['W'])-p['axes']['BTC_MAIN_LOOKBACK_DAYS'].index(g['W']))<=1 and abs(p['axes']['BTC_ENTRY_RETURN_HURDLE'].index(x['K'])-p['axes']['BTC_ENTRY_RETURN_HURDLE'].index(g['K']))<=1];assert dims==2 and {z['fingerprint'] for z in ns}=={z['fingerprint'] for z in expected}
put(R/'sizing_primitive_verification.json',{'passed':True,'both9cell_native_parent_grids_and_geometry_checked':True,'new_native_amounts_1000_capital3750_actual_recalculation_required':True,'raw_bank_weights_1_1_not_normalized':True,'parent_capital18750_notional5000':True,'no_market_or_account_execution':True});print('PASSnative2axes/parent2axes/sizing/common-neighborhood')
