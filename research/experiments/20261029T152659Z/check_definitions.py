"""No market calculation: exact native rules,raw units,spec/registry binding."""
import json
from run import ROOT,R,reg,sha,put,WEIGHTS,NEW_WEIGHTS,EXITS,SLOWS
plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl')
assert len(batch)==len({x['fingerprint'] for x in batch})==40 and sha(R/'engine.py')==plan['source_engine']['sha256']==sha(ROOT/plan['source_engine']['path'])
assert plan['grid']['BTC_bank_units']==WEIGHTS and plan['gates']['recent40_positive5d_each_cost_min']==6 and plan['gates']['local_recent6of8_allcost_fraction_min']==.6
for row in batch:
 sp=json.loads((ROOT/row['spec']).read_text());p=sp['parameters'];w=row['BTC_bank_units'];ww=[w,2-w];fps=row['source_fingerprints'];assert w in NEW_WEIGHTS and p['raw_component_multipliers']==row['raw_component_multipliers']==ww and p['initial_capital_usdt']==row['capital_usdt']==20000
 assert [x['weight'] for x in sp['components']]==ww and [x['fingerprint'] for x in sp['components']]==fps and p['source_component_parameters']==[records[fp]['spec']['parameters'] for fp in fps] and sp['validation_plan']==str((R/'plan.json').relative_to(ROOT)) and reg.fingerprint(sp)==row['fingerprint']
 assert p['owned_component_capitals_usdt']==[10000*w,10000*(2-w)] and sum(p['owned_component_capitals_usdt'])==20000 and p['effective_owned_entry_budgets_usdt']==[1000*w,3000*(2-w)] and p['effective_owned_entry_fraction_of_parent']==sum(p['effective_owned_entry_budgets_usdt'])/20000
 a,b=p['source_component_parameters'];assert a['initial_capital_usdt']==b['initial_capital_usdt']==10000 and a['fixed_entry_notional_usdt']==1000 and b['fixed_entry_notional_usdt']==3000
 if row['role']=='candidate':
  S=row['ETH_trend_lookback_days'];E=row['ETH_exit_buffer_fraction'];assert S in SLOWS and E in EXITS and a['lookback_days']==31 and a['return_hurdle']==.04 and a['exit_buffer_fraction']==.01 and b['lookback_days']==3 and b['return_hurdle']==.025 and b['exit_buffer_fraction']==E and b['trend_lookback_days']==S and b['trend_gate_lookbacks_days']==[S-1,S,S+1] and b['trend_gate_application']=='entries_only' and b['trend_gate_mode']=='adjacent_horizon_majority' and p['ETH_exit_buffer_fraction']==E and p['ETH_trend_lookback_days']==S and p['reversal_exit_buffer_fraction']==E
 else:assert row['role']=='benchmark' and all(plan['component_sources'][fp]['role']=='benchmark' for fp in fps)
 assert p['start_utc']=='2025-10-19T00:01:00Z' and p['end_utc']=='2026-10-24T00:01:00Z' and p['cost_multipliers']==[1,2,3]
assert sum(x['role']=='candidate' for x in batch)==36
put(R/'definition_check.json',{'passed':True,'financial_evaluations':0,'complete_new_definitions':40,'candidate_configs':36,'benchmarks':4,'raw_units_not_normalized':True,'native_order_sizes_and_source_parameters_unchanged':True,'strict_new_cost_fold_gates_predeclared':True,'old_anchor_count':9,'frozen_plan_sha256':sha(R/'plan.json')});print('PASS40 exact complete specs;raw units/funded20000/nativeN1000/N3000/strictcostgates')
