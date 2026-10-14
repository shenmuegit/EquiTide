#!/usr/bin/env python3
"""Freeze daily time-series momentum parameter batch before evaluating returns."""
import hashlib,json
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
OOS_START='2025-09-19T00:01:00Z';OOS_END='2026-09-14T00:01:00Z'
DATA={
 'BTC':[
  {'path':'data/normalized/binance/BTC/binance_BTC_20240916T000000Z_20250916T000000Z_transfer_20261001/spot_bars.parquet','bytes':30555668,'sha256':'9a5bc556eb277db34831457d22c53f50f5b4f2c0f04f6aefe80f941e51405ba6'},
  {'path':'data/normalized/binance/BTC/binance_BTC_20250916T000000Z_20260916T000000Z_archive_20260929/spot_bars.parquet','bytes':30415140,'sha256':'50983b6865dc5873afa9c4e2abb2cf73d846ec5ed98b31453fee24afef1a0d16'}],
 'ETH':[
  {'path':'data/normalized/binance/ETH/binance_ETH_20240916T000000Z_20250916T000000Z_transfer_20261001/spot_bars.parquet','bytes':27110682,'sha256':'aaebd29868abe2ed3af3a6f3479b495e4d788385c1fb0988d5d2372a9be89d57'},
  {'path':'data/normalized/binance/ETH/binance_ETH_20250916T000000Z_20260916T000000Z_archive_20260929/spot_bars.parquet','bytes':26332430,'sha256':'437545ee866153d6bf31a17a021b9249e5a97cb688cf60a42a58fc8515e83584'}]}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def main():
 exfile=R/'exchange_info_raw.json';ex=json.loads(exfile.read_text());filters={}
 for s in ex['symbols']:
  a='BTC' if s['symbol']=='BTCUSDT' else 'ETH' if s['symbol']=='ETHUSDT' else None
  if not a:continue
  d={f['filterType']:f for f in s['filters']}
  price=d['PRICE_FILTER'];lot=d['LOT_SIZE'];notional=d.get('NOTIONAL',d.get('MIN_NOTIONAL'));assert notional
  percent=d.get('PERCENT_PRICE_BY_SIDE',d.get('PERCENT_PRICE'))
  filters[a]={k:v for k,v in [('PRICE_FILTER',price),('LOT_SIZE',lot),('NOTIONAL',notional)]}
  if percent:filters[a]['PERCENT_PRICE_BY_SIDE']=percent
 assert set(filters)=={'BTC','ETH'}
 exch={'source_url':'https://data-api.binance.vision/api/v3/exchangeInfo?symbols=%5B%22BTCUSDT%22%2C%22ETHUSDT%22%5D','method':'GET','captured_at_utc':datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),'server_time_ms':ex['serverTime'],'raw_sha256':sha(exfile),'filters':filters}
 put(R/'exchange_filters.json',exch)
 for a,files in DATA.items():
  for item in files:
   p=ROOT/item['path'];assert p.exists() and p.stat().st_size==item['bytes'] and sha(p)==item['sha256']
 plan={'round':R.name,'frozen_at_utc':datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),'direction':'Daily time-series momentum with a fixed positive entry hurdle and zero-return exit; separate unlevered BTC and ETH cash accounts.','hypothesis':'Published work reports daily/weekly cryptocurrency time-series momentum. Test a simple long-only, absolute return-threshold adaptation on Binance BTC/ETH; this is not a paper replication and does not assume the reported effect survives contemporary trading costs.',
  'sources':[{'citation':'Liu, Tsyvinski and Wu, Risks and Returns of Cryptocurrency (NBER Working Paper 24877 / Review of Financial Studies, 2021).','url':'https://www.nber.org/papers/w24877','accessed_utc':'2026-10-14','scope':'Motivation only; their universe and sampling differ, and the current rule is not a replication.'}],
  'rule':{'signal':'On each newly closed UTC daily candle j, calculate ROC_L=close[j]/close[j-L]-1 using only that candle and the close L complete daily bars earlier.','entry':'If cash and ROC_L is strictly greater than the frozen entry hurdle, target long.','exit':'If long and ROC_L is less than or equal to zero, target cash. Between thresholds, keep the previous target. Equality at entry does not enter; equality at exit exits.','execution':'Signal becomes available at the signal candle close; if target changes, simulate an order at the next UTC day 00:01 one-minute open (60-second delay). Rejected orders are not backfilled; the same desired state may be tried on a later new daily decision. At the frozen OOS terminal timestamp, liquidate any open lot with costs.','account':'Independent 2,000 USDT single-asset cash account for every asset×parameter combination; all initial capital assigned to the specified asset sleeve, no leverage, borrowing, shorting, transfer or cash interest.'},
  'grid':{'assets':['BTC','ETH'],'lookback_days':[7,14,28],'entry_hurdle_pct':[0,2.5,5.0],'exit_hurdle_pct':0,'candidate_configurations':18,'cost_multipliers':[1,2,3]},
  'time_boundaries':{'input_history_utc':'2024-09-16T00:00:00Z/2026-09-16T00:00:00Z','oos_start_utc':OOS_START,'oos_end_exclusive_utc':OOS_END,'oos_days':360,'warmup_days':365,'embargo_days':3,'walk_forward':'12 consecutive, non-overlapping 30-day evaluation windows; account remains continuous across windows; no fitting, parameter selection or fold reset.','history_note':'The 2025–2026 OOS window has been reused extensively in this repository and is not an untouched final holdout.'},
  'validation':{'parameter_sensitivity_axes':['lookback_days','entry_hurdle_pct'],'neighborhood':'Same asset, adjacent lookback index and adjacent hurdle index in the frozen 3×3 grid; 3×3 neighborhood including center.','round_trip_minimum':8,'positive_1x_folds_minimum':8,'all_cost_scenarios_positive':True,'max_3x_minute_sample_drawdown_pct':25,'minimum_3x_positive_neighborhood_fraction':0.6,'gross_reference_pnl_to_cost_minimum':2.5,'capacity_or_filter_rejections':0,'terminal_flat':True,'multiple_testing':'No DSR/PBO claim: repeated reused-OOS history and many prior strategy trials create material selection bias.'},
  'costs':{'per_side_fee':0.001,'estimated_half_spread_per_side':0.0001,'estimated_slippage_per_side':0.0002,'impact':'0.5 × sample stdev of previous 20 complete UTC daily log returns × sqrt(order quote budget / previous 20 complete daily quote ADV)','maximum_participation':0.001,'cost_multipliers':[1,2,3],'filters_source':'Fresh public Binance exchangeInfo GET body and derived current PRICE_FILTER/LOT_SIZE/NOTIONAL/PERCENT_PRICE rules; adverse tick rounding and lot floor; 5-minute pre-execution VWAP proxy. Historical L2 and historical exchange filters are unavailable.'},
  'data':{'format':'Archived Binance spot 1m OHLCV; daily closes and quote ADV are aggregated from fully closed UTC days.','assets':DATA},
  'prior_results':{'initial_16_missing_actual_results':0,'same_family_context':['Daily EMA 5/10/20×40/80/160 crossover grid completed 2026-10-14 and rejected.','4h time-series momentum and volume-confirmed 4h momentum grids completed/rejected.','Long-horizon relative-strength, daily weekday calendar and multiple channel/MA grids are already in the registry.'],'distinction':'This rule uses daily cumulative simple close-to-close return with an absolute entry hurdle and zero ROC exit; it is a different full rule/timeframe from 4h momentum, cross-sectional relative strength and moving-average crosses.'}}
 put(R/'plan.json',plan)
 import sys
 sys.path.insert(0,str(ROOT/'research/automation'));import registry
 batch=[]
 for asset in plan['grid']['assets']:
  for L in plan['grid']['lookback_days']:
   for hurdle in plan['grid']['entry_hurdle_pct']:
    name=f'daily_roc_momentum_{asset}_L{L}_H{str(hurdle).replace(".","p")}'
    spec={'kind':'strategy','family':'spot-daily-time-series-momentum-hurdle','market':'spot','timeframe':'1d','universe':[f'{asset}/USDT'],'name':name,'logic':{'entry':'At a newly closed daily bar j, compute ROC_L=close[j]/close[j-L]-1. If flat, enter long only if ROC_L > entry_hurdle_fraction, strict inequality.','exit':'If long, exit when ROC_L <= 0. Otherwise preserve prior target state. Exit takes precedence if state is long; entry can only start from flat.','sizing':'Independent 2,000 USDT cash account; all original capital allocated to this asset; long-only, no leverage, no borrowing, no cross-asset transfer or add-on.','timing':'Close-based signal only from a closed UTC daily bar, next day 00:01 UTC one-minute open (60-second delay); no historical fill before OOS.'},'parameters':{'asset':asset,'lookback_days':L,'entry_hurdle_fraction':hurdle/100,'exit_hurdle_fraction':0.0,'initial_capital_usdt':2000,'oos_start_utc':OOS_START,'oos_end_exclusive_utc':OOS_END,'warmup_days':365,'embargo_days':3,'walk_forward_test_days':30,'walk_forward_folds':12,'walk_forward_step_days':30,'fee_rate_per_side':0.001,'half_spread_estimate_per_side':0.0001,'slippage_estimate_per_side':0.0002,'impact_model':'0.5 * sample_stdev(previous 20 complete UTC daily log returns) * sqrt(order quote budget / previous 20 complete daily quote-volume ADV)','max_participation':0.001,'cost_multipliers':[1,2,3],'exchange_filters_sha256':sha(R/'exchange_filters.json'),'sensitivity_axes':['lookback_days','entry_hurdle_fraction']},'sources':plan['sources']}
    path=R/'specs'/f'{name}.json';put(path,spec);batch.append({'name':name,'asset':asset,'lookback_days':L,'entry_hurdle_pct':hurdle,'spec':str(path.relative_to(ROOT)),'fingerprint':registry.fingerprint(spec)})
 put(R/'batch.json',batch)
 print('freeze complete',len(batch),'configurations','plan_sha256='+sha(R/'plan.json'))
if __name__=='__main__':main()
