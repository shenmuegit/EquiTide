#!/usr/bin/env python3
"""Freeze daily channel entry / Wilder ATR close-trailing exit variants before evaluation."""
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
 exch={'source_url':'https://data-api.binance.vision/api/v3/exchangeInfo?symbols=%5B%22BTCUSDT%22%2C%22ETHUSDT%22%5D','method':'GET','captured_at_utc':datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),'server_time_ms':ex['serverTime'],'raw_sha256':sha(R/'exchange_info_raw.json'),'filters':filters};put(R/'exchange_filters.json',exch)
 for items in DATA.values():
  for it in items:
   p=ROOT/it['path'];assert p.is_file() and p.stat().st_size==it['bytes'] and sha(p)==it['sha256']
 plan={'round':R.name,'frozen_at_utc':datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),'direction':'Daily close channel breakout entries with a ratcheting Wilder-ATR trailing exit; independent unlevered BTC and ETH long-only accounts.',
  'hypothesis':'Volatility-scaled trailing exits may preserve persistent trends while limiting giveback after price reversals. This is a falsification grid, not a claim that ATR rules are profitable.',
  'indicator_source':{'citation':'TA-Lib official ATR source (Wilder smoothing and true-range definition).','url':'https://github.com/TA-Lib/ta-lib/blob/main/src/ta_func/ta_ATR.c','accessed_utc':'2026-10-14','implementation':'TR=max(H-L,abs(H-prev_close),abs(L-prev_close)); ATR seed is the simple mean of the first n complete TR values; subsequent ATR=((n-1)*prior_ATR+TR)/n. Own transparent implementation is audited against these published steps.'},
  'rule':{'entry':'At a newly closed UTC daily bar j, enter if close[j] is strictly greater than max(high[j-E:j]); the entry comparison excludes signal-day high and uses only the prior E complete daily highs. Signal is available at the close; execute at next UTC day 00:01 one-minute open.',
   'initial_stop':'At the entry signal day, initialize peak_close=close[j], entry_ATR=ATR_n[j], stop=peak_close-multiple*entry_ATR. The ATR value is frozen at entry.',
   'trailing_exit':'On each later complete daily close, peak_close=max(prior_peak_close,close[j]); stop=max(prior_stop,peak_close-multiple*entry_ATR), so the stop only ratchets upward. If close[j] <= stop, signal a full exit for the next UTC day 00:01 one-minute open. Stop is close-confirmed, not intraday or guaranteed executable at stop price.',
   'state':'Independent 2,000 USDT single-asset spot account, all initial capital in that sleeve, no leverage/short/add-ons/transfers/yield. After an exit, do not re-enter on that same decision day; a later daily signal can re-enter. A rejected historical order is not backfilled; evaluate the rule on the next newly closed daily bar.',
   'terminal':'Any position still open at fixed OOS end is liquidated at the end-boundary next-minute-open reference with costs. No fill is created before OOS.'},
  'grid':{'assets':['BTC','ETH'],'entry_lookback_days':[20,40],'wilder_atr_periods':[14,28,56],'entry_close_vs_prior_high':'strictly greater; exclude current signal bar','trailing_stop_multipliers':[2,3,4],'candidate_configurations':36,'cost_multipliers':[1,2,3]},
  'time_boundaries':{'input_history_utc':'2024-09-16T00:00:00Z/2026-09-16T00:00:00Z','oos_start_utc':OOS_START,'oos_end_exclusive_utc':OOS_END,'oos_days':360,'warmup_days':365,'embargo_days':3,'walk_forward':'12 consecutive, non-overlapping 30-day evaluation folds. Account and indicator state remain continuous; no fitting or per-fold reset.','history_note':'This OOS window is reused throughout the repository and is not an untouched final holdout.'},
  'costs':{'fee_per_side':0.001,'estimated_half_spread_per_side':0.0001,'slippage_per_side':0.0002,'impact':'0.5 × sample stdev of previous 20 complete UTC daily log returns × sqrt(order quote budget / previous 20 complete daily quote ADV)','max_participation':0.001,'stress_multipliers':[1,2,3],'exchange_filters':'Fresh public Binance exchangeInfo GET response, frozen in exchange_info_raw.json/exchange_filters.json; adverse PRICE tick rounding, LOT_SIZE floor, NOTIONAL and PERCENT_PRICE_BY_SIDE checks via previous 5-minute VWAP proxy. Historical L2 and historical exchange filters are unavailable.'},
  'sensitivity':{'axes':['entry_lookback_days 20/40','Wilder ATR period 14/28/56','trailing stop multiple 2/3/4'],'local_neighbor':'Same asset; adjacent indices on all three frozen axes, with bounded neighbor cells; report 3× positive fraction.'},
  'failure_gates':{'all_1x_2x_3x_net_returns_positive':True,'positive_1x_folds_min':8,'max_3x_sampled_drawdown_pct':25,'min_3x_neighbor_positive_fraction':0.6,'min_1x_round_trips':8,'gross_reference_pnl_to_cost_min':2.5,'no_capacity_or_filter_rejections':True,'terminal_flat':True,'interpretation':'Historical reused-OOS screening only; no stable-live claim. DSR/PBO will not be asserted.'},
  'data':{'format':'Archived Binance spot 1-minute OHLCV. Aggregate complete UTC daily high, low, close, quote volume; retain source file hashes.','assets':DATA},
  'novelty_review':{'initial16_missing_actual_backtests':0,'prior_atr_or_trailing_stop_full_rule_hits':0,'related_prior_results':['Daily close channel rules use fixed-bar channel exits; no ATR/trailing stop found in complete strategy registry.','Daily EMA/ROC momentum and 4h momentum used different exit rules; this ATR trailing stop is a distinct configuration.']}}
 put(R/'plan.json',plan)
 import sys
 sys.path.insert(0,str(ROOT/'research/automation'));import registry
 batch=[]
 for a in plan['grid']['assets']:
  for E in plan['grid']['entry_lookback_days']:
   for n in plan['grid']['wilder_atr_periods']:
    for mult in plan['grid']['trailing_stop_multipliers']:
     name=f'atr_trailing_{a}_E{E}_N{n}_M{mult}'
     spec={'kind':'strategy','family':'spot-daily-channel-wilder-atr-trailing-stop','market':'spot','timeframe':'1d','universe':[f'{a}/USDT'],'name':name,
       'logic':{'entry':'On closed UTC daily candle j, close[j] > max(high[j-E:j]) with the comparison channel excluding the current signal day.','exit':'Seed Wilder ATR from the first N true ranges by arithmetic mean; update recursively ATR=((N-1)*prior_ATR+TR)/N. At entry freeze ATR_entry and peak_close=signal close. On later closed bars ratchet peak_close=max(peak_close,close); stop=max(previous_stop,peak_close-M*ATR_entry). Exit if close <= stop, next-day 00:01 minute-open reference. Stop is close-confirmed; no intraday stop fills.','sizing':'Independent 2,000 USDT single-asset long-only spot account; no leverage, short, add-on, interest or transfer.','timing':'Only complete daily bars; signal executes at next daily 00:01 one-minute open. OOS starts flat; terminal liquidation at fixed OOS end.'},
       'parameters':{'asset':a,'entry_lookback_days':E,'wilder_atr_period':n,'trailing_stop_multiple':mult,'initial_capital_usdt':2000,'oos_start_utc':OOS_START,'oos_end_exclusive_utc':OOS_END,'warmup_days':365,'embargo_days':3,'walk_forward_test_days':30,'walk_forward_folds':12,'walk_forward_step_days':30,'fee_rate_per_side':0.001,'half_spread_estimate_per_side':0.0001,'slippage_estimate_per_side':0.0002,'impact_model':'0.5 * sample_stdev(previous 20 complete UTC daily log returns) * sqrt(order quote budget / previous 20 complete daily quote-volume ADV)','max_participation':0.001,'cost_multipliers':[1,2,3],'exchange_filters_sha256':sha(R/'exchange_filters.json'),'sensitivity_axes':['entry_lookback_days','wilder_atr_period','trailing_stop_multiple']},'sources':[plan['indicator_source']]}
     path=R/'specs'/f'{name}.json';put(path,spec);batch.append({'name':name,'asset':a,'entry_lookback_days':E,'atr_period':n,'stop_multiple':mult,'spec':str(path.relative_to(ROOT)),'fingerprint':registry.fingerprint(spec)})
 put(R/'batch.json',batch);print('frozen',len(batch),'configs; plan_sha256='+sha(R/'plan.json'))
if __name__=='__main__':main()
