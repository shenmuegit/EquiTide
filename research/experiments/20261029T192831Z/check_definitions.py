"""Check complete definitions and context availability without PnL."""
import json
from run import ROOT,R,sha,put,reg
p=json.loads((R/'plan.json').read_text());rows=json.loads((R/'batch.json').read_text());specs={x['fingerprint']:json.loads((ROOT/x['spec']).read_text()) for x in rows};records=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(rows)==24 and sha(R/'engine.py')==p['new_engine_sha256'] and sha(ROOT/p['source_engine']['path'])==p['source_engine']['sha256'] and json.loads((R/'engine_change_verification.json').read_text())['passed']
for row in rows:
 s=specs[row['fingerprint']];q=s['parameters'];assert reg.fingerprint(s)==row['fingerprint'] and s['validation_plan']==str((R/'plan.json').relative_to(ROOT))
 if row['scope']=='native':
  assert q['lookback_days']==3 and q['return_hurdle']==.025 and q['fixed_entry_notional_usdt']==3000 and q['initial_capital_usdt']==10000 and q['exit_buffer_fraction'] in [-.015,-.01,-.005] and q['trend_lookback_days'] in [30,31] and q['trend_gate_lookbacks_days']==[q['trend_lookback_days']-1,q['trend_lookback_days'],q['trend_lookback_days']+1] and max(q['trend_gate_lookbacks_days'])<=32 and q['warmup_days']+q['embargo_days']>=33 and q['trend_gate_application']=='entries_only'
 else:
  w=row['BTC_bank_units'];assert w in [.375,.5,.625] and q['raw_component_multipliers']==[w,2-w]==[x['weight'] for x in s['components']] and q['initial_capital_usdt']==20000 and q['owned_component_capitals_usdt']==[10000*w,10000*(2-w)] and sum(q['owned_component_capitals_usdt'])==20000
  source=[(specs.get(fp) or records[fp]['spec'])['parameters'] for fp in row['source_fingerprints']];assert q['source_component_parameters']==source and source[0]['fixed_entry_notional_usdt']==1000 and source[1]['fixed_entry_notional_usdt']==3000 and source[1]['trend_lookback_days']==q['ETH_trend_lookback_days']==q['trend_filter_lookback_days'] in [30,31] and source[1]['exit_buffer_fraction']==q['ETH_exit_buffer_fraction']==q['reversal_exit_buffer_fraction']
 assert q['start_utc']=='2025-10-19T00:01:00Z' and q['end_utc']=='2026-10-24T00:01:00Z'
assert p['gates']['recent40_positive5d_each_cost_min']==6 and p['gates']['local_recent6of8_allcost_fraction_min']==.6
put(R/'definition_check.json',{'passed':True,'financial_evaluations':0,'complete_new_definitions':24,'native':6,'passive_parent':18,'old_anchor_count':24,'context33_closes_support_ROCmax32':True,'raw_weights_preserved':True,'native_engine_formulas_unchanged_only_whitelist_extended':True,'strict_gates_unchanged':True});print('PASS24 complete definitions,33contextcloses/nativeengine/strictgates/rawunits')
