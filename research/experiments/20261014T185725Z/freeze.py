#!/usr/bin/env python3
"""Freeze a short-entry-window ATR-trailing sensitivity follow-up before new calculations."""
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
 ex=json.loads((R/'exchange_info_raw.json').read_text());filters={}
 for s in ex['symbols']:
  a='BTC' if s['symbol']=='BTCUSDT' else 'ETH' if s['symbol']=='ETHUSDT' else None
  if not a:continue
  d={x['filterType']:x for x in s['filters']};n=d.get('NOTIONAL',d.get('MIN_NOTIONAL'));assert n
  filters[a]={k:v for k,v in [('PRICE_FILTER',d['PRICE_FILTER']),('LOT_SIZE',d['LOT_SIZE']),('NOTIONAL',n)]}
  if d.get('PERCENT_PRICE_BY_SIDE'):filters[a]['PERCENT_PRICE_BY_SIDE']=d['PERCENT_PRICE_BY_SIDE']
  elif d.get('PERCENT_PRICE'):filters[a]['PERCENT_PRICE_BY_SIDE']=d['PERCENT_PRICE']
 assert set(filters)=={'BTC','ETH'}
 exchange={'source_url':'https://data-api.binance.vision/api/v3/exchangeInfo?symbols=%5B%22BTCUSDT%22%2C%22ETHUSDT%22%5D','method':'GET','captured_at_utc':datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),'server_time_ms':ex['serverTime'],'raw_sha256':sha(R/'exchange_info_raw.json'),'filters':filters};put(R/'exchange_filters.json',exchange)
 for files in DATA.values():
  for x in files:
   p=ROOT/x['path'];assert p.is_file() and p.stat().st_size==x['bytes'] and sha(p)==x['sha256']
 plan={'round':R.name,'frozen_at_utc':datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),'direction':'Follow-up parameter neighborhood for daily close-channel entries with a Wilder ATR ratcheting close-trailing exit.',
  'hypothesis':'The prior E=20/40 ATR channel grid produced low trade counts on reused OOS history. Predeclare shorter E=5/10/15-day entry channels with varied Wilder ATR periods and stop multiples to test whether the same volatility-scaled trend exit offers more repeated trades; this is an exploratory second-stage screen on the same reused OOS, not independent validation.',
  'source':{'citation':'TA-Lib official ATR implementation and documented Wilder recursion.','url':'https://github.com/TA-Lib/ta-lib/blob/main/src/ta_func/ta_ATR.c','accessed_utc':'2026-10-14','scope':'Defines the indicator only; no profitability claim.'},
  'rule':{'entry':'On closed UTC daily bar j, enter if close[j] > max(high[j-E:j]); current signal day excluded from prior channel. Next UTC day 00:01 one-minute open is the execution reference.',
   'atr':'TR=max(H-L,abs(H-prev_close),abs(L-prev_close)); seed ATR with the arithmetic mean of first N complete TR values (indices 1..N); subsequent ATR=((N-1)*prior_ATR+TR)/N. ATR is computed causally and continuously, never reset by fold.',
   'stop':'At entry signal freeze ATR_entry and peak_close=signal close; initial stop=peak_close-M*ATR_entry. For each later closed daily close, peak_close=max(previous_peak,close[j]); stop=max(previous_stop,peak_close-M*ATR_entry). Exit on close[j]<=stop, execute next UTC day 00:01. Close-confirmed only; no intraday stop guarantee.',
   'account':'Each variant uses its own 2,000 USDT single-asset spot account; all capital allocated to its specified asset; long-only, no leverage, short, borrowing, add-on, transfers or interest. Do not re-enter on the exit signal day. Terminal OOS liquidation is fixed and costed.'},
  'grid':{'assets':['BTC','ETH'],'entry_lookback_days':[5,10,15],'wilder_atr_periods':[7,14,28],'stop_multipliers':[2,3,4],'candidate_configs':54,'cost_multipliers':[1,2,3]},
  'followup_reference':{'prior_batch':'research/experiments/20261014T165749Z/result.md','reason':'Most favorable prior E=40 ATR configurations had only 2–3 completed round trips; all 36 variants were rejected by fold/robustness/round-trip gates. This batch changes E, N and includes new configurations; it reuses the same historical interval and is not a fresh holdout.'},
  'time_boundaries':{'input_history_utc':'2024-09-16T00:00:00Z/2026-09-16T00:00:00Z','oos_start_utc':OOS_START,'oos_end_exclusive_utc':OOS_END,'oos_days':360,'warmup_days':365,'embargo_days':3,'walk_forward':'12 consecutive, non-overlapping 30-day evaluation folds; continuous positions and indicator state; no fitting or fold reset.','history_note':'Repeated development/validation interval, not an untouched final test set.'},
  'costs':{'fee_per_side':0.001,'estimated_half_spread_per_side':0.0001,'slippage_per_side':0.0002,'impact':'0.5 × sample stdev of previous 20 complete UTC daily log returns × sqrt(order quote budget / previous 20 complete daily quote ADV)','max_participation':0.001,'multipliers':[1,2,3],'exchange_filters':'Fresh public GET exchangeInfo snapshot, derived PRICE_FILTER/LOT_SIZE/NOTIONAL/PERCENT_PRICE_BY_SIDE, adverse tick rounding, lot floor, 5-minute pre-execution VWAP proxy. Historical L2 and historical exchange filters unavailable.'},
  'sensitivity':{'axes':['entry lookback days 5/10/15','ATR periods 7/14/28','stop multiples 2/3/4'],'neighbor':'Same asset; adjacent grid indices on all three axes, bounded at edges; report local 3× positivity, no OOS winner selection.'},
  'failure_gates':{'all_1x_2x_3x_positive':True,'positive_1x_folds_min':8,'drawdown_3x_max_pct':25,'local_3x_positive_fraction_min':0.6,'round_trips_1x_min':8,'gross_reference_to_cost_min':2.5,'no_exchange_or_capacity_rejections':True,'terminal_flat':True,'multiple_testing':'Accumulated trial count and reused OOS invalidate untouched holdout claims; no DSR/PBO is claimed.'},
  'data':{'format':'Archived Binance spot 1m OHLCV aggregated to complete UTC daily OHLC/quote volume.','assets':DATA}}
 put(R/'plan.json',plan)
 import sys
 sys.path.insert(0,str(ROOT/'research/automation'));import registry
 batch=[]
 for a in plan['grid']['assets']:
  for E in plan['grid']['entry_lookback_days']:
   for n in plan['grid']['wilder_atr_periods']:
    for mult in plan['grid']['stop_multipliers']:
     name=f'atr_short_entry_{a}_E{E}_N{n}_M{mult}'
     spec={'kind':'strategy','family':'spot-daily-channel-wilder-atr-trailing-stop','market':'spot','timeframe':'1d','universe':[f'{a}/USDT'],'name':name,'logic':{'entry':'Daily close strict breakout above max prior E daily highs (exclude current day), execute next UTC day 00:01.','exit':'Wilder ATR with exact TR definition and SMA seed then recursive smoothing. Freeze ATR on entry; long-only close-peak trailing stop ratchets up and exits when a later closed daily close <= peak_close - M*ATR_entry; next-day 00:01 execution. Terminal liquidation at OOS end.','sizing':'Independent 2,000 USDT single-asset long-only cash account; all initial capital in that asset sleeve; no leverage, borrow, short, add-on, transfer or yield.','rule_version':'Follow-up short entry-channel neighborhood; unchanged from prior ATR family except parameters.'},'parameters':{'asset':a,'entry_lookback_days':E,'wilder_atr_period':n,'stop_multiple':mult,'initial_capital_usdt':2000,'oos_start_utc':OOS_START,'oos_end_exclusive_utc':OOS_END,'warmup_days':365,'embargo_days':3,'walk_forward_test_days':30,'walk_forward_folds':12,'walk_forward_step_days':30,'fee_per_side':0.001,'half_spread_estimate_per_side':0.0001,'slippage_per_side':0.0002,'impact_model':'0.5 * sample_stdev(previous 20 complete UTC daily log returns) * sqrt(order quote budget / previous 20 complete daily quote-volume ADV)','max_participation':0.001,'cost_multipliers':[1,2,3],'exchange_filters_sha256':sha(R/'exchange_filters.json'),'sensitivity_axes':['entry_lookback_days','wilder_atr_period','stop_multiple']},'sources':[plan['source']]}
     path=R/'specs'/f'{name}.json';put(path,spec);batch.append({'name':name,'asset':a,'entry_lookback_days':E,'atr_period':n,'stop_multiple':mult,'spec':str(path.relative_to(ROOT)),'fingerprint':registry.fingerprint(spec)})
 put(R/'batch.json',batch);print('frozen',len(batch),'specs; plan_sha256='+sha(R/'plan.json'))
if __name__=='__main__':main()
