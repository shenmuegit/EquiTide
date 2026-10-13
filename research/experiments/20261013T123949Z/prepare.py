#!/usr/bin/env python3
"""Freeze and reserve a long-horizon BTC/ETH relative-strength rotation grid."""
import hashlib,json,subprocess,sys,gzip,urllib.parse
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
data_files={}
for asset in ('BTC','ETH'):
 data_files[asset]=[]
 for suffix in (f'{asset}_20240916T000000Z_20250916T000000Z_transfer_20261001',f'{asset}_20250916T000000Z_20260916T000000Z_archive_20260929'):
  p=ROOT/f'data/normalized/binance/{asset}/binance_{suffix}/spot_bars.parquet'
  data_files[asset].append({'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':sha(p)})
# Use the most recent successful public exchangeInfo response already in the paper10
# archive. The immediately preceding 08:27 observation failed before exchangeInfo.
source_obs=ROOT/'research/paper10/observations/20261013T062626335409Z';exchange_path=source_obs/'exchange_info.json.gz'
raw=gzip.decompress(exchange_path.read_bytes());exchange=json.loads(raw)
exchange_inputs={'path':str(exchange_path.relative_to(ROOT)),'archive_sha256':sha(exchange_path),'raw_sha256':hashlib.sha256(raw).hexdigest(),'received_utc':next(x['received_at_utc'] for x in json.loads((source_obs/'http_provenance.json').read_text()) if urllib.parse.urlsplit(x['url']).path.endswith('/api/v3/exchangeInfo'))}
prior_registry=registry.read_records(ROOT/'research/automation/registry.jsonl')
paper={'citation':'Shi, Y., Li, X., & Zhang, J. (2021). Up or down? Short-term reversal, momentum, and liquidity effects in cryptocurrency markets. International Review of Financial Analysis, 78, 101908. DOI:10.1016/j.irfa.2021.101908.',
 'url':'https://doi.org/10.1016/j.irfa.2021.101908','accessed_utc':'2026-10-13',
 'finding_summary':'The authors study daily cross-sectional cryptocurrency returns and report that very liquid large-cap assets can show daily momentum even where the broad cross-section exhibits reversal. This motivates a low-turnover BTC/ETH relative-strength allocation screen; their broad-universe result does not validate a two-asset portfolio.'}
grid={'lookback_days':[63,126,252],'absolute_return_hurdle':[0.0,0.05,0.10]}
oos={'start_utc':'2025-09-19T00:00:00Z','end_exclusive_utc':'2026-09-14T00:00:00Z','terminal_execution_utc':'2026-09-14T00:01:00Z','start_day_index':368,'end_day_index':728,'days':360,'warmup_days':365,'fold_days':30,'folds':12,'embargo_days':3}
costs={'initial_capital_usdt':2000,'fee_per_side':0.001,'half_spread_estimate_per_side':0.0001,'slippage_per_side':0.0002,
 'impact_model':'0.5 * sample_stdev(previous 20 complete UTC daily log returns) * sqrt(order quote budget / previous 20 complete daily quote ADV)',
 'maximum_participation':0.001,'multipliers':[1,2,3],'filters_source':exchange_inputs,'note':'No historical L2; half-spread, slippage and square-root impact are estimates. No funding or borrow: spot long-only.'}
plan={'round':R.name,'frozen_at_utc':'2026-10-13T12:39:49Z','direction':'Long-horizon cross-sectional relative-strength rotation between BTC and ETH with an absolute winner-return cash hurdle.',
 'hypothesis':'Lower-frequency relative strength may reduce trading-cost drag compared with previously tested short-horizon rotations. Select the stronger of BTC and ETH over 63/126/252 fully closed UTC daily bars, but stay in USDT unless that winner is above a 0/5/10 percent cumulative-return hurdle.',
 'source_paper':paper,'grid':{**grid,'rotation_configs':9,'comparators':3,'total_registry_definitions':12},
 'complete_rule':'At each OOS UTC day boundary d after the previous daily candle is fully closed, compute BTC and ETH simple returns close[d-1]/close[d-1-L]-1 using L in {63,126,252}. BTC wins exact ties. Target 100 percent of the one 2000-USDT portfolio in the winner only if the winning return is strictly greater than the absolute hurdle {0,0.05,0.10}; otherwise target cash. Trade only when the actual holding asset differs from the target. At d 00:01 one-minute open, sell the full old position first, then if required buy the new winner from remaining USDT; failed legs leave actual holdings/cash unchanged and are retried only when the next daily target still differs. Never backfill missed signals or rebalance an unchanged holding. A switch uses two sequential fills and pays costs on both legs.',
 'allocation':'Rotation account has 2000 USDT total. Target raw exposure is {BTC:1,ETH:0,cash:0}, {BTC:0,ETH:1,cash:0}, or {BTC:0,ETH:0,cash:1}; no simultaneous asset holdings, normalization, borrow, yield, or other-account transfers. Static 50/50 hold comparator starts with two separate 1000-USDT sleeves and does not rebalance.',
 'time_boundaries':{'input_history_utc':'2024-09-16T00:00:00Z/2026-09-16T00:00:00Z','walk_forward':'12 contiguous fixed 30-day OOS folds; no fitted model/parameter; lookback is strictly trailing prior completed days.','history_disclosure':'This date range has been repeatedly used in repository research, not an untouched final holdout.' ,**oos},
 'execution':{'signal':'Only fully closed daily rows; signal becomes available at new UTC day 00:00 after previous UTC day close.','entry_exit':'Historical 1m open at 00:01 UTC (60-second availability delay), full position on target changes; terminal liquidation at end UTC 00:01. Historical minute opens are used only in this research backtest, never as current paper10 fills.','filters_source_sha256':exchange_inputs['raw_sha256'],'filters_received_utc':exchange_inputs['received_utc'],'accounting':'Existing Decimal kernel fill() and lagged daily cost input implementation.'},
 'costs':costs,'sensitivity_axes':['lookback_days','absolute_return_hurdle'],
 'failure_gates':{'all_1x_2x_3x_returns_positive':True,'minimum_positive_1x_folds':8,'maximum_3x_sample_drawdown_pct':25,'minimum_3x_adjacent_neighbor_positive_fraction':0.60,'minimum_1x_round_trips':4,'minimum_1x_gross_reference_pnl_to_cost':2.5,'no_capacity_filter_or_balance_violations':True,'terminal_flat_all_costs':True,'interpretation':'Historical validation only; does not imply live/future profit or minute-level risk bounds.'},
 'data_files':data_files,'prior_research':{'nearest_existing_family':'spot-cross-sectional-dual-momentum-rotation; previous tested lookbacks were 20/40/60 days and hurdles 0/2/4%. These new 63/126/252 day and 0/5/10% definitions are fingerprint-distinct and were selected before results. Prior short-horizon rotations were rejected.'}}
(R/'plan.json').write_text(json.dumps(plan,indent=2,ensure_ascii=False)+'\n')
(R/'exchange_filters.json').write_text(json.dumps({'snapshot':exchange_inputs,'symbols':{a:next(x for x in exchange['symbols'] if x['symbol']==a+'USDT')['filters'] for a in ('BTC','ETH')}},indent=2,ensure_ascii=False)+'\n')
batch=[]
for L in grid['lookback_days']:
 for hurdle in grid['absolute_return_hurdle']:
  name=f'relstr_L{L}_H{int(hurdle*100):02d}'
  spec={'kind':'strategy','family':'spot-long-horizon-relative-strength-cash-rotation','market':'spot','timeframe':'1d','universe':['BTC/USDT','ETH/USDT'],'name':name,
   'logic':{'signal':plan['complete_rule'],'allocation':plan['allocation'],'execution':plan['execution'],'limitations':'Two-asset cross-section only; no shorting, leverage, transfers or yield.'},
   'parameters':{'lookback_days':L,'absolute_return_hurdle':hurdle,'initial_capital_usdt':2000,**oos,'cost_multipliers':[1,2,3],'sensitivity_axes':['lookback_days','absolute_return_hurdle'],'exchange_filters_sha256':exchange_inputs['raw_sha256']},
   'sources':[paper],'failure_gates':plan['failure_gates']}
  p=R/'specs'/(name+'.json');p.write_text(json.dumps(spec,indent=2,ensure_ascii=False)+'\n');batch.append({'name':name,'role':'candidate','fingerprint':registry.fingerprint(spec),'spec':str(p.relative_to(ROOT))})
for asset in ('BTC','ETH'):
 name=f'hold_360d_{asset.lower()}_relative_strength_study';spec={'kind':'strategy','family':'spot-long-horizon-relative-strength-hold-reference','market':'spot','timeframe':'1d','universe':[asset+'/USDT'],'name':name,
  'logic':{'entry':'Buy the whole one-asset sleeve at the common first executable OOS minute open.','exit':'Hold through OOS and terminal-liquidate with the same costs.','sizing':'2000-USDT independent long-only spot comparator.'},
  'parameters':{'initial_capital_usdt':2000,**oos,'cost_multipliers':[1,2,3]},'sources':[paper]}
 p=R/'specs'/(name+'.json');p.write_text(json.dumps(spec,indent=2,ensure_ascii=False)+'\n');batch.append({'name':name,'role':'single_asset_hold','asset':asset,'fingerprint':registry.fingerprint(spec),'spec':str(p.relative_to(ROOT))})
# Static 50/50 buy-and-hold basket with independent initial sleeves, no rebalance.
name='hold_360d_btc_eth_50_50_relative_strength_study';spec={'kind':'strategy','family':'spot-long-horizon-relative-strength-hold-reference','market':'spot','timeframe':'1d','universe':['BTC/USDT','ETH/USDT'],'name':name,
 'logic':{'entry':'Buy BTC and ETH once at OOS start with fixed original 50%/50% cash sleeves.','exit':'Hold sleeves independently without rebalancing; terminal-liquidate both at the same end.','sizing':'Raw 50% BTC / 50% ETH of 2000 USDT, each sleeve starts with exactly 1000 USDT; no normalization or transfers.'},
 'parameters':{'initial_capital_usdt':2000,'raw_weights':{'BTC':0.5,'ETH':0.5},**oos,'cost_multipliers':[1,2,3]},'sources':[paper]}
p=R/'specs'/(name+'.json');p.write_text(json.dumps(spec,indent=2,ensure_ascii=False)+'\n');batch.append({'name':name,'role':'static_equal_hold','asset':'BTC+ETH','fingerprint':registry.fingerprint(spec),'spec':str(p.relative_to(ROOT))})
assert len(batch)==12 and len({x['fingerprint'] for x in batch})==12
(R/'batch.json').write_text(json.dumps(batch,indent=2,ensure_ascii=False)+'\n')
reserved=[]
for x in batch:
 q=subprocess.run([sys.executable,str(ROOT/'research/automation/registry.py'),'reserve',str(ROOT/x['spec'])],cwd=ROOT,capture_output=True,text=True)
 reserved.append({**x,'exit_code':q.returncode,'output':q.stdout.strip(),'stderr':q.stderr.strip()})
 if q.returncode:
  (R/'reserve_partial.json').write_text(json.dumps(reserved,indent=2,ensure_ascii=False)+'\n');raise SystemExit(f"reserve failed {x['name']} rc={q.returncode} {q.stdout} {q.stderr}")
(R/'reserve.json').write_text(json.dumps(reserved,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'reserved':len(reserved),'unique':len({x['fingerprint'] for x in reserved}),'candidates':9,'comparators':3},ensure_ascii=False))
