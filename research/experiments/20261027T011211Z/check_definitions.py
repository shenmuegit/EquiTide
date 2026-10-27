"""Reject wrong N/exit/ETH aliases or source fingerprints before reserve/evaluation."""
import json
from run import ROOT,R,reg,sha,put
plan=json.loads((R/'plan.json').read_text());rows=json.loads((R/'batch.json').read_text());assert len(rows)==90
for row in rows:
 sp=json.loads((ROOT/row['spec']).read_text());p=sp['parameters'];fps=row['source_fingerprints'];assert reg.fingerprint(sp)==row['fingerprint'] and sp['validation_plan']==str((R/'plan.json').relative_to(ROOT));assert [x['fingerprint'] for x in sp['components']]==fps and [x['weight'] for x in sp['components']]==p['raw_component_multipliers']==[1,1] and p['component_capitals_usdt']==[10000,10000] and p['initial_capital_usdt']==20000
 B,E=row['BTC_fixed_entry_notional_usdt'],row['ETH_fixed_entry_notional_usdt'];assert B in [1000,2000,3000] and E in [1000,2000,3000] and p['component_initial_entry_notionals_usdt']==[B,E] and p['BTC_fixed_entry_notional_usdt']==B and p['ETH_fixed_entry_notional_usdt']==E
 a,b=[plan['component_sources'][fp] for fp in fps];assert [a['asset'],b['asset']]==['BTC','ETH'] and [a['fixed_entry_notional_usdt'],b['fixed_entry_notional_usdt']]==[B,E] and all(sha(ROOT/x['spec'])==x['spec_sha256'] and sha(ROOT/x['archive'])==x['archive_sha256'] for x in [a,b])
 assert p['trend_filter_lookback_days']==p['ETH_trend_lookback_days']==row['trend_filter_lookback_days']==b['trend_lookback_days'] and p['ETH_lookback_days']==p['reversal_lookback_days']==row['reversal_lookback_days']==b['lookback_days']==3 and p['ETH_return_hurdle']==p['reversal_return_hurdle']==row['reversal_return_hurdle']==b['return_hurdle'];assert a['lookback_days']==p['BTC_lookback_days']==31 and a['return_hurdle']==p['BTC_return_hurdle']==row['BTC_return_hurdle'] in [.02,.06] and a['exit_buffer_fraction']==p['BTC_exit_buffer_fraction']==p['trend_exit_buffer_fraction']==row['trend_exit_buffer_fraction']==.01 and b['exit_buffer_fraction']==p['ETH_exit_buffer_fraction']==0
proof={'passed':True,'checked_configs':90,'candidate_configs':90,'benchmark_configs':0,'both_budget_aliases_BTC_exit_aliases_and_both_ETH_signal_aliases_match_exact_sources':True,'no_financial_evaluation':True,'plan_sha256':sha(R/'plan.json')}
if (R/'definition_check.json').exists():assert json.loads((R/'definition_check.json').read_text())==proof
else:put(R/'definition_check.json',proof)
print('PASS:90 exact source pairs,all entrybudget/entryhurdle/exit/signal aliases and raw1/1 bank parameters consistent before reserve/evaluation.')
