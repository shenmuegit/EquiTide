#!/usr/bin/env python3
"""Freeze weekly weekday-window experiment and independently fingerprint variants."""
import hashlib, json
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
R=Path(__file__).resolve().parent
ROUND=R.name
OOS_START='2025-09-19T00:01:00Z'
OOS_END='2026-09-14T00:01:00Z'
DATA={
 'BTC':[
  {'path':'data/normalized/binance/BTC/binance_BTC_20240916T000000Z_20250916T000000Z_transfer_20261001/spot_bars.parquet','bytes':30555668,'sha256':'9a5bc556eb277db34831457d22c53f50f5b4f2c0f04f6aefe80f941e51405ba6'},
  {'path':'data/normalized/binance/BTC/binance_BTC_20250916T000000Z_20260916T000000Z_archive_20260929/spot_bars.parquet','bytes':30415140,'sha256':'50983b6865dc5873afa9c4e2abb2cf73d846ec5ed98b31453fee24afef1a0d16'}],
 'ETH':[
  {'path':'data/normalized/binance/ETH/binance_ETH_20240916T000000Z_20250916T000000Z_transfer_20261001/spot_bars.parquet','bytes':27110682,'sha256':'aaebd29868abe2ed3af3a6f3479b495e4d788385c1fb0988d5d2372a9be89d57'},
  {'path':'data/normalized/binance/ETH/binance_ETH_20250916T000000Z_20260916T000000Z_archive_20260929/spot_bars.parquet','bytes':26332430,'sha256':'437545ee866153d6bf31a17a021b9249e5a97cb688cf60a42a58fc8515e83584'}]
}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,obj): p.write_text(json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def main():
 R.joinpath('specs').mkdir(parents=True,exist_ok=True)
 src=R/'exchange_info_raw.json'
 if not src.exists(): raise SystemExit('missing public Binance exchangeInfo GET snapshot')
 ex=json.loads(src.read_text())
 filter_map={}
 for sym in ex['symbols']:
  a='BTC' if sym['symbol']=='BTCUSDT' else 'ETH' if sym['symbol']=='ETHUSDT' else None
  if not a: continue
  f={x['filterType']:x for x in sym['filters']}
  required=('PRICE_FILTER','LOT_SIZE','NOTIONAL','PERCENT_PRICE_BY_SIDE')
  if any(k not in f for k in required): raise SystemExit(f'{a} missing required filter')
  filter_map[a]={k:f[k] for k in required}
 if set(filter_map)!={'BTC','ETH'}: raise SystemExit('fresh public snapshot must contain both BTCUSDT and ETHUSDT')
 raw_sha=sha(src)
 ex_snapshot={'source_url':'https://data-api.binance.vision/api/v3/exchangeInfo?symbols=%5B%22BTCUSDT%22%2C%22ETHUSDT%22%5D','method':'GET','captured_at_utc':datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),'server_time_ms':ex.get('serverTime'),'raw_sha256':raw_sha,'filters':filter_map}
 put(R/'exchange_filters.json',ex_snapshot)
 plan={
  'round':ROUND,'frozen_at_utc':datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),
  'direction':'UTC weekday scheduled long-only spot windows, BTC/ETH tested separately.',
  'hypothesis':'Published crypto day-of-week return studies report weekday-dependent returns, including a Monday BTC effect in older samples. Test whether a fixed weekday schedule supports an executable net edge in Binance BTC/ETH under current estimated spot costs; the weekday is a categorical parameter, not selected using this OOS.',
  'source_paper':[{'citation':'The day of the week effect in the cryptocurrency market (Finance Research Letters, 2019)','url':'https://doi.org/10.1016/j.frl.2018.12.005','accessed_utc':'2026-10-14','use':'Motivation only. This experiment is not a replication; older findings do not establish a current edge.'},{'citation':'Bitcoin time-of-day, day-of-week and month-of-year effects in returns and trading volume (2019)','url':'https://www.sciencedirect.com/science/article/pii/S1544612319301710','accessed_utc':'2026-10-14','use':'Motivation only; prior sample/exchange differs.'}],
  'universe':['BTC/USDT','ETH/USDT'],'assets_are_independent_accounts':True,'initial_capital_usdt_per_configuration':2000,'raw_asset_allocation':1.0,'leverage':1,'shorting':False,'cross_asset_transfer':False,'rebalancing':False,
  'grid':{'assets':['BTC','ETH'],'weekday_utc':[0,1,2,3,4,5,6],'weekday_names':['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'],'holding_days':[1,3],'candidate_configurations':28,'cost_multipliers':[1,2,3]},
  'rule':{'entry':'Each UTC calendar week, at most once on the predeclared weekday, schedule a buy at that date 00:01 UTC one-minute open. The deterministic schedule is known before the signal time 00:00 UTC; no price bar after that time selects the entry. Use all available account cash.', 'exit':'Schedule a full sell at 00:01 UTC exactly holding_days later. With holding_days in {1,3}, the weekly windows cannot overlap. If an entry is rejected, skip that week; if a scheduled exit is rejected by a filter, retry on each following one-minute open until filled or the fixed OOS end. No re-entry is allowed while inventory is nonzero.', 'account':'Independent 2,000 USDT account per asset × weekday × holding horizon; cash earns zero; no leverage, borrowing, shorting, add-ons, transfer, or reinvestment outside scheduled windows.', 'signal_to_execution':'60 seconds from scheduled event availability at 00:00 UTC to the 00:01 UTC minute open. This is a historical execution reference, not a contemporaneous quote or an exchange fill guarantee.'},
  'time_boundaries':{'input_history_utc':'2024-09-16T00:00:00Z/2026-09-16T00:00:00Z','oos_start_utc':OOS_START,'oos_end_exclusive_utc':OOS_END,'oos_days':360,'walk_forward':'12 consecutive non-overlapping 30-day evaluation folds; positions remain continuous across fold boundaries, no parameter fitting or fold resets.','warmup_days':365,'embargo_days':3,'history_note':'This OOS interval is repeatedly used in repository research and is not an untouched final holdout.'},
  'costs':{'fee_rate_per_side':0.001,'estimated_half_spread_per_side':0.0001,'estimated_slippage_per_side':0.0002,'impact':'0.5 × sample standard deviation of previous 20 complete UTC daily log returns × sqrt(order quote budget / previous 20 complete daily quote ADV)','maximum_participation':0.001,'multipliers':[1,2,3],'filters_source':'Fresh public Binance exchangeInfo GET response frozen in exchange_info_raw.json and exchange_filters.json; adverse tick rounding, LOT_SIZE floor, NOTIONAL and PERCENT_PRICE_BY_SIDE checked using 5-minute pre-execution VWAP proxy. Historical L2 and historical exchange filters are unavailable.'},
  'sensitivity':{'axes':['entry_weekday_utc (7 cyclic categorical values)','holding_days (1,3)'],'local_neighborhood':'same asset, weekday at cyclic distance ≤1, both predeclared holding horizons; report 3× positive fraction without selecting an OOS winner.'},
  'failure_gates':{'all_1x_2x_3x_net_returns_positive':True,'minimum_positive_1x_folds':8,'maximum_3x_minute_sampled_drawdown_pct':25,'minimum_3x_neighbor_positive_fraction':0.6,'minimum_1x_round_trips':40,'minimum_1x_gross_reference_pnl_to_cost':2.5,'no_capacity_or_balance_violations':True,'terminal_flat':True,'interpretation':'Exploratory historical screen only; no stable/live profitability claim. Sample size is approximately 50 weekly entries per configuration and is insufficient for strong statistical claims.'},
  'data':{'assets':DATA,'source_format':'Archived Binance spot 1-minute OHLCV parquet; all bars must be closed, UTC aligned and continuous.'},
  'prior_evidence':{'initial_16_missing_actual_backtests':0,'latest_round':'research/experiments/20261014T084051Z/result.md','older weekday rules': 'No weekday/DOW rule fingerprint was found in the complete main registry or committed experiment result summaries; parameters differ from earlier quarter-hour schedule tests.'}
 }
 # Verify frozen inputs before writing their hashes.
 for a,items in DATA.items():
  for it in items:
   p=ROOT/it['path']
   if not p.is_file() or p.stat().st_size!=it['bytes'] or sha(p)!=it['sha256']: raise SystemExit(f'data integrity error: {p}')
 put(R/'plan.json',plan)
 import sys
 sys.path.insert(0,str(ROOT/'research/automation'));import registry
 batch=[]
 for asset in plan['grid']['assets']:
  for day in plan['grid']['weekday_utc']:
   for hold in plan['grid']['holding_days']:
    name=f'weekday_window_{asset}_dow{day}_hold{hold}d'
    spec={'kind':'strategy','family':'utc-weekday-scheduled-long-window','market':'spot','timeframe':'1m','universe':[f'{asset}/USDT'],'name':name,'logic':{'entry':'Once per UTC week on the specified weekday, deterministic schedule known at least 60 seconds beforehand; buy at 00:01 UTC minute open.','exit':'Sell at 00:01 UTC after fixed holding_days; retry each minute after a rejected exit; no overlapping/re-entry before exit.','sizing':'Independent 2,000 USDT cash account; use available cash; long-only unlevered spot; no transfers or interest.','time_availability':'Calendar event is known before its scheduled minute; all price-driven cost inputs are lagged completed-day observations.'},'parameters':{'asset':asset,'entry_weekday_utc':day,'holding_days':hold,'initial_capital_usdt':2000,'oos_start_utc':OOS_START,'oos_end_exclusive_utc':OOS_END,'walk_forward_test_days':30,'walk_forward_folds':12,'walk_forward_step_days':30,'warmup_days':365,'embargo_days':3,'cost_multipliers':[1,2,3],'fee_rate_per_side':0.001,'half_spread_estimate_per_side':0.0001,'slippage_estimate_per_side':0.0002,'impact_model':'0.5 * sample_stdev(previous 20 complete UTC daily log returns) * sqrt(order quote budget / previous 20 complete daily quote-volume ADV)','maximum_participation':0.001,'exchange_filters_sha256':sha(R/'exchange_filters.json'),'sensitivity_axes':['entry_weekday_utc','holding_days']},'sources':plan['source_paper']}
    path=R/'specs'/f'{name}.json';put(path,spec)
    batch.append({'name':name,'asset':asset,'weekday_utc':day,'holding_days':hold,'spec':str(path.relative_to(ROOT)),'fingerprint':registry.fingerprint(spec)})
 put(R/'batch.json',batch)
 print(f'freeze complete: {len(batch)} specs; plan sha256={sha(R/"plan.json")}')
if __name__=='__main__':main()
