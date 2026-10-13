import json,pathlib
R=pathlib.Path(__file__).resolve().parents[1]
for asset in ('BTC','ETH'):
 for cap in (5000,10000):
  for phase in (0,1,2):
   for hold in (1,2,3):
    role='primary_event' if phase==0 else 'predeclared_phase_placebo_control'
    name=f'turn15_{asset.lower()}_cap{cap}_phase{phase}_hold{hold}m'
    s={'kind':'strategy','family':'utc-quarter-hour-boundary-long-only-event','market':'spot','timeframe':'1m','universe':[asset+'/USDT'],'name':name,
    'logic':{'event':'At every UTC hour quarter-hour boundary minute {0,15,30,45} plus fixed phase offset p, buy at that one-minute open and exit exactly hold_minutes later. Event windows do not overlap because hold_minutes<=3 and the next event is 15 minutes later. Repeat on the calendar only while sufficient cash and exchange filters permit.',
    'causality':'UTC event timing is fixed and known in advance; the event signal is available 60 seconds before the first executable open. No entry or holding-period bar is used to select the event.',
    'control_role':role,'sizing':f'Independent {cap} USDT unlevered long-only spot account per asset/config; use available cash at each permitted event; no transfers, leverage, shorts, interest or scale-in.'},
    'parameters':{'initial_capital_usdt':cap,'phase_offset_minutes':phase,'hold_minutes':hold,'event_minutes_utc':[0,15,30,45],
      'oos_start_utc':'2025-09-19T00:00:00Z','oos_end_exclusive_utc':'2026-09-14T00:00:00Z','walk_forward_test_days':30,'walk_forward_folds':12,'walk_forward_step_days':30,
      'cost_multipliers':[1,2,3],'fee_rate_per_side':0.001,'half_spread_estimate_per_side':0.0001,'slippage_estimate_per_side':0.0002,
      'impact_model':'0.5 * sample stdev(previous 20 complete UTC daily log returns) * sqrt(order quote budget / previous 20 complete UTC daily quote ADV)',
      'max_participation':0.001,'exchange_filters':'Frozen Binance exchange-info PRICE_FILTER, LOT_SIZE, NOTIONAL; adverse tick rounding, lot floor and 5-minute pre-execution VWAP percent-price proxy.',
      'input_history_utc':'2024-09-16T00:00:00Z/2026-09-16T00:00:00Z','sensitivity_axes':['initial_capital_usdt','hold_minutes','phase_offset_minutes']},
    'sources':[{'citation':'Shanaev et al. (2023), Turn-of-the-candle effect in bitcoin returns, Heliyon 9:e14236, DOI 10.1016/j.heliyon.2023.e14236','url':'https://doi.org/10.1016/j.heliyon.2023.e14236','accessed_utc':'2026-10-12','use':'Paper reports BTC turn-minute returns and a venue-specific fee-tier benefit near $5,000 on Bitfinex; this experiment tests Binance with fixed 10bp per-side fees, so the venue-specific zero-fee result is not assumed.'}],
    'failure_gates':{'all_1x_2x_3x_net_returns_positive':True,'min_positive_1x_folds':8,'max_3x_event_sample_drawdown_pct':25,'min_3x_neighbor_positive_fraction':0.6,'min_1x_round_trips':100,'min_1x_gross_reference_pnl_to_cost':2.5,'no_capacity_or_balance_violations':True,'terminal_flat':True,
      'phase_specificity':'For each asset, capital size and holding duration, exact phase 0 mean 1x net return must exceed both phase-1 and phase-2 control means; controls themselves are not promotion candidates.'}}
    (R/'specs'/f'{name}.json').write_text(json.dumps(s,indent=2,ensure_ascii=False)+'\n')
for asset in ('BTC','ETH'):
 for cap in (5000,10000):
  name=f'buy_hold_{asset.lower()}_cap{cap}_event_period'
  s={'kind':'strategy','family':'turn15-buy-and-hold-reference','market':'spot','timeframe':'1m','universe':[asset+'/USDT'],'name':name,
  'logic':{'entry':'Buy at OOS start 00:00 UTC one-minute open.','exit':'Terminal sell at 2026-09-14T00:00:00Z one-minute open.','sizing':f'Independent {cap} USDT unlevered buy-and-hold reference; same fees, spread, slippage, impact, lot, tick and participation model as candidates.'},
  'parameters':{'initial_capital_usdt':cap,'oos_start_utc':'2025-09-19T00:00:00Z','oos_end_exclusive_utc':'2026-09-14T00:00:00Z','cost_multipliers':[1,2,3],'fee_rate_per_side':0.001,'half_spread_estimate_per_side':0.0001,'slippage_estimate_per_side':0.0002,'impact_model':'prior 20 completed daily returns/quote ADV square-root model','max_participation':0.001}}
  (R/'specs'/f'{name}.json').write_text(json.dumps(s,indent=2,ensure_ascii=False)+'\n')
print('generated 36 strategy/control specs and 4 capital-matched buy-hold references')
