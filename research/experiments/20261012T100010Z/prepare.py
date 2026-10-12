#!/usr/bin/env python3
"""Freeze and reserve the predeclared BTC/ETH 4h volume-confirmed momentum grid."""
import hashlib, json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]; ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation')); import registry

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
source=ROOT/'research/experiments/20261012T035429Z/report.json'
r=json.loads(source.read_text()); filters=r['plan']['execution']['filters']
files={}
for asset in ('BTC','ETH'):
  files[asset]=[]
  for suffix in (f'{asset}_20240916T000000Z_20250916T000000Z_transfer_20261001',f'{asset}_20250916T000000Z_20260916T000000Z_archive_20260929'):
    p=ROOT/f'data/normalized/binance/{asset}/binance_{suffix}/spot_bars.parquet'
    files[asset].append({'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size})

common={
 'source_literature':{'citation':'Shen, D., Urquhart, A., & Wang, P. (2022). Bitcoin intraday time-series momentum. Financial Review, 57(2), 319–344. DOI:10.1111/fire.12290.','url':'https://onlinelibrary.wiley.com/doi/10.1111/fire.12290','accessed_utc':'2026-10-12','use':'Motivates testing a predeclared intraday momentum and volume confirmation rule; this 4h rule is an adaptation, not a replication.'},
 'data':{'source':'Binance spot 1m OHLCV, normalized closed bars','files':files,'history_utc':'2024-09-16T00:00:00Z/2026-09-16T00:00:00Z','reuse_disclosure':'The full period is repeatedly used development/validation history and is not an untouched final holdout.'},
 'walk_forward':{'window_type':'rolling','train_bars':2190,'train_days':365,'test_bars':180,'test_days':30,'step_bars':180,'embargo_bars':18,'embargo_days':3,'folds':12,'continuous_oos':True,'first_test_bar_index':2208,'end_exclusive_bar_index':4368,'first_oos_bar_utc':'2025-09-19T00:00:00Z','first_execution_utc':'2025-09-19T00:01:00Z','terminal_execution_utc':'2026-09-14T00:01:00Z','parameter_fit':'None; all rule parameters frozen before evaluation. Each fold uses only already completed bars for signal and lagged cost inputs. OOS account starts flat and carries state continuously across adjacent test folds.'},
 'execution':{'reference':'Next UTC 4h block first one-minute open, at block_start+60s; prior 4h close is available at block_start. Decimal fill reuses research/experiments/20261001T133655Z/kernel.py and existing market filter snapshot. Historical L2 is unavailable; fill costs and 5m VWAP are estimated. No real orders.' ,'filters_source':'research/experiments/20261012T035429Z/report.json','filters_sha256':sha(source),'filters_by_symbol':filters},
 'costs':{'fee_per_side':0.001,'half_spread_estimate_per_side':0.0001,'slippage_estimate_per_side':0.0002,'impact_coefficient':0.5,'impact_formula':'0.5 * sample_std(previous 20 complete UTC daily log returns) * sqrt(order_budget / mean_quote_volume(previous 20 complete UTC days))','max_prior_ADV_participation':0.001,'scenarios':[1,2,3],'spread_counted_once':True,'funding_borrow':'Not applicable: unlevered long-only spot.'},
 'selection_bias':'Registry currently has zero spot 4h volume-confirmed momentum entries. This batch is 20 preregistered definitions; no result-based specification edits. All history reused.'
}
plan={'round':ROUND.name,'frozen_at_utc':'2026-10-12T10:00:10Z','direction':'4h UTC long-only spot time-series momentum with same-slot relative quote-volume confirmation','hypothesis':'An intermediate 4h close-to-close momentum signal confirmed by elevated same-slot quote turnover may avoid low-liquidity false entries; compare 6/12/24-bar momentum and volume ratios 1.00/1.25/1.50 on BTC and ETH.','grid':{'assets':['BTC','ETH'],'lookback_4h_bars':[6,12,24],'same_slot_quote_volume_ratio_min':[1.0,1.25,1.5],'same_slot_reference_days':20,'capital_usdt_each':2000},'sensitivity_axes':['lookback_4h_bars','same_slot_quote_volume_ratio_min'], 'rule':'For completed UTC 4h bar i, define momentum as close[i-1]/close[i-1-lookback]-1. Compute relative volume as quote_volume[i-1] divided by the arithmetic mean of quote_volume from the prior 20 observations of the same UTC 4h slot (i-7, i-13, ..., i-121); current bar is excluded. Flat enters when momentum>0 and relative volume>=threshold. Long exits when momentum<=0, regardless of volume. Otherwise retain desired state. Signals use closed bars only; execution at the next block start+1 minute open. No leverage, shorting, scale-in, rebalance, cross-asset transfer, or pre-OOS trades. Each asset/config has independent 2000 USDT initial cash.', 'accounting':'Independent $2,000 account per asset/config. Preserve cash and units, maximum affordable buy, whole sale, no yield/rebalance. Terminal liquidation is costed.', 'gates':{'all_1x_2x_3x_net_returns_positive':True,'minimum_positive_1x_folds':7,'max_3x_minute_close_sample_drawdown_pct':25,'min_3x_neighborhood_positive_fraction_per_asset':0.60,'min_1x_round_trips':2,'min_1x_gross_pnl_to_cost':2.5,'no_balance_violations':True,'terminal_flat':True,'interpretation':'A pass is a repeated-history screen only; no independent/forward profitability claim.'},**common}
(ROUND/'spec.json').write_text(json.dumps(plan,indent=2,ensure_ascii=False)+'\n')
rows=[]
for asset in ('BTC','ETH'):
 for look in (6,12,24):
  for ratio in (1.0,1.25,1.5):
   name=f'mom{look}_slotvol{int(ratio*100):03d}_{asset}'
   spec={'kind':'strategy','family':'spot-4h-volume-confirmed-momentum','market':'spot','timeframe':'4h','universe':[asset+'/USDT'],'name':name,
    'logic':{'momentum_entry':'At newly closed 4h bar i, enter only if close[i-1] > close[i-1-lookback_4h_bars], strictly positive momentum.', 'relative_volume_entry':'On same decision, quote_volume[i-1] / arithmetic_mean(quote_volume at same UTC 4h slot from prior 20 days, indices i-7 through i-121 step -6) >= configured threshold. Current bar excluded.', 'exit':'If long, set desired cash whenever close[i-1] <= close[i-1-lookback_4h_bars], regardless of volume. Exit has priority; otherwise enter on both entry conditions; all other cases preserve desired state.', 'timing':'Signals only use completed UTC 4h bars. Execute on the next UTC 4h block first one-minute open, block_start+60 seconds.', 'sizing':'Independent $2,000 unlevered spot account; max affordable LOT_SIZE entry, exit all valid units; preserve cash; no rebalance, add-on, leverage, short, yield, or pre-OOS fills.'},
    'parameters':{'lookback_4h_bars':look,'same_slot_quote_volume_ratio_min':ratio,'same_slot_reference_days':20,'initial_capital_usdt':2000,'walk_forward_train_bars':2190,'walk_forward_test_bars':180,'walk_forward_step_bars':180,'embargo_bars':18,'folds':12,'oos_start_bar_index':2208,'oos_end_exclusive_bar_index':4368,'cost_multipliers':[1,2,3]}}
   p=ROUND/'specs'/f'{name}.json'; p.write_text(json.dumps(spec,indent=2)+'\n'); rows.append({'name':name,'asset':asset,'spec':str(p.relative_to(ROOT)),'fingerprint':registry.fingerprint(spec),'is_comparator':False})
for asset in ('BTC','ETH'):
 name=f'hold_360d_{asset}'
 spec={'kind':'strategy','family':'spot-4h-hold-reference','market':'spot','timeframe':'4h','universe':[asset+'/USDT'],'name':name,'logic':{'entry':'Buy at first OOS execution time, without a signal.','exit':'Hold until the common terminal execution time, then liquidate; reference only.','timing':'Same OOS start and end as candidate grid.','sizing':'Independent $2,000 unlevered spot reference.'},'parameters':{'initial_capital_usdt':2000,'oos_start_bar_index':2208,'oos_end_exclusive_bar_index':4368,'cost_multipliers':[1,2,3]}}
 p=ROUND/'specs'/f'{name}.json'; p.write_text(json.dumps(spec,indent=2)+'\n'); rows.append({'name':name,'asset':asset,'spec':str(p.relative_to(ROOT)),'fingerprint':registry.fingerprint(spec),'is_comparator':True})
(ROUND/'batch.json').write_text(json.dumps(rows,indent=2)+'\n')
with (ROUND/'reserve.log').open('w') as log:
 for row in rows:
  cp=subprocess.run([sys.executable,str(ROOT/'research/automation/registry.py'),'reserve',str(ROOT/row['spec'])],cwd=ROOT,text=True,capture_output=True)
  log.write(json.dumps({'name':row['name'],'returncode':cp.returncode,'stdout':cp.stdout.strip(),'stderr':cp.stderr.strip()})+'\n'); log.flush()
  if cp.returncode: raise SystemExit(f"reserve failed: {row['name']} rc={cp.returncode} {cp.stderr}")
print(f'reserved {len(rows)}; fingerprints={len(set(x["fingerprint"] for x in rows))}')
