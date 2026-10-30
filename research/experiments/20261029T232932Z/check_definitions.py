"""Exact capital/quantity/weights/funding/price rules before any new market simulation."""
import json
from run import ROOT,R,reg,sha,put
plan=json.loads((R/'plan.json').read_text());rows=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');specs={x['fingerprint']:json.loads((ROOT/x['spec']).read_text()) for x in rows};assert len(rows)==len(specs)==42 and sha(R/'engine.py')==plan['new_engine_sha256'] and sha(R/'btc_engine.py')==plan['new_BTC_engine_sha256']
for row in rows:
 s=specs[row['fingerprint']];p=s['parameters'];w=row['BTC_capital_fraction'];assert reg.fingerprint(s)==row['fingerprint'] and s['validation_plan']==str((R/'plan.json').relative_to(ROOT)) and w in [.1875,.25,.3125]
 if row['scope']=='native':
  capital=20000*(w if row['asset']=='BTC' else 1-w);frac=.1 if row['asset']=='BTC' else .3;assert p['initial_capital_usdt']==row['capital_usdt']==capital and p['fixed_entry_notional_usdt']==row['fixed_entry_notional_usdt']==capital*frac and p['raw_entry_notional_fraction_of_initial_capital']==frac
  if row['mode']=='candidate':assert p['lookback_days']==3 and p['return_hurdle']==.025 and p['exit_buffer_fraction']==-.01 and p['trend_lookback_days']==28 and p['trend_gate_application']=='entries_only' and p['entry_funding_lookback_settlements']==6 and p['entry_funding_cost_cap_per_settlement']==row['entry_funding_cost_cap_per_settlement'] in [0,.00005,.0001]
  elif row['mode']=='momentum':assert row['asset']=='BTC' and p['lookback_days']==31 and p['return_hurdle']==.04 and p['exit_buffer_fraction']==.01 and row['role']=='component'
  elif row['mode']=='hold':assert p['signal_mode']=='constant_long_reference'
  else:assert row['asset']=='ETH' and row['mode']=='ungated' and not any(k.startswith('entry_funding_') for k in p)
 else:
  fps=row['source_fingerprints'];source=[specs.get(fp,records.get(fp,{}).get('spec')) for fp in fps];assert p['source_component_parameters']==[x['parameters'] for x in source] and [x['fingerprint'] for x in s['components']]==fps and p['raw_component_multipliers']==row['raw_component_multipliers']==[x['weight'] for x in s['components']]
  if row['mode']=='ownership':assert p['component_capitals_usdt']==[10000,10000] and p['raw_component_multipliers']==[2*w,2*(1-w)]
  else:assert p['component_capitals_usdt']==[20000*w,20000*(1-w)] and p['raw_component_multipliers']==[1,1] and [x['parameters']['initial_capital_usdt'] for x in source]==p['component_capitals_usdt']
  assert sum(a*b for a,b in zip(p['component_capitals_usdt'],p['raw_component_multipliers']))==20000 and p['initial_capital_usdt']==20000 and p['owned_component_capitals_usdt']==[20000*w,20000*(1-w)]
 assert p['start_utc']=='2025-10-19T00:01:00Z' and p['end_utc']=='2026-10-24T00:01:00Z'
assert sum(x['role']=='candidate' for x in rows)==18 and sum(x['scope']=='native' for x in rows)==21 and sum(x['mode']=='ownership' for x in rows)==6 and plan['gates']['recent40_positive5d_each_cost_min']==6
put(R/'definition_check.json',{'passed':True,'financial_evaluations':0,'complete_new_definitions':42,'native_cashbanks':21,'true_cashbank_parents':15,'new_ownership_comparison_parents':6,'candidate_2D_cells':18,'strict_gates_unchanged':True,'no_old_NAV_scaling_used_for_new_native_execution':True,'raw_multipliers_not_renormalized':True});print('PASS42 nativecapital/fullspec/source/cost/gate bindings')
