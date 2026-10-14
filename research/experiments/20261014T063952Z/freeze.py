#!/usr/bin/env python3
"""Freeze a two-axis BTC/ETH lead-lag threshold sensitivity before evaluation."""
import hashlib,json,subprocess,sys,urllib.parse
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
def utc():return datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,ensure_ascii=False,allow_nan=False)+'\n')

# Obtain a fresh official public spot-rule snapshot. No private endpoints or credentials.
url='https://data-api.binance.vision/api/v3/exchangeInfo?symbols=%5B%22BTCUSDT%22%2C%22ETHUSDT%22%5D'
assert urllib.parse.urlsplit(url).netloc=='data-api.binance.vision' and urllib.parse.urlsplit(url).path=='/api/v3/exchangeInfo'
started=utc();p=subprocess.run(['curl','--fail','--silent','--show-error','--max-time','25',url],capture_output=True,check=True);received=utc()
raw=p.stdout;exchange=json.loads(raw);assert {x['symbol'] for x in exchange['symbols']}=={'BTCUSDT','ETHUSDT'}
for sym in exchange['symbols']:
 assert sym['status']=='TRADING' and sym.get('isSpotTradingAllowed',True)
 types={f['filterType'] for f in sym['filters']};assert {'PRICE_FILTER','LOT_SIZE','NOTIONAL'}<=types
meta=ROUND/'exchange_info_raw.json';meta.write_bytes(raw)
snapshot={'url':url,'method':'GET','received_started_utc':started,'received_at_utc':received,'server_time_ms':exchange.get('serverTime'),'raw_sha256':sha(meta),'filters':{a:{x['filterType']:x for x in next(s for s in exchange['symbols'] if s['symbol']==a+'USDT')['filters']} for a in ('BTC','ETH')}}
write(ROUND/'exchange_filters.json',snapshot)

old=ROOT/'research/experiments/20261013T164415Z';old_plan=json.loads((old/'plan.json').read_text())
data_files=old_plan['data_files']
for asset,files in data_files.items():
 for row in files:
  f=ROOT/row['path'];assert f.is_file() and f.stat().st_size==row['bytes'] and sha(f)==row['sha256']
paper=old_plan['source_paper']
start='2025-09-19T00:00:00Z';end='2026-09-14T00:00:00Z';terminal='2026-09-14T00:01:00Z'
directions=[{'leader':'BTC','follower':'ETH'},{'leader':'ETH','follower':'BTC'}]
leader_thresholds=[0.0025,0.005,0.01]
relative_gap_thresholds=[0.001,0.0025,0.005]
lookback=30;hold=180
source_rules={
 'decision':'At each UTC hourly boundary m use only fully closed 1m data through m-1; signal values are never computed from bar m or later.',
 'signal':'For leader X and follower Y, rX=closeX[m-1]/closeX[m-1-L]-1 and rY analogously, with L=30 minutes. If flat, enter Y long only if rX is strictly greater than threshold T and rX-rY is strictly greater than threshold G. Parameters T and G are independently swept over the predeclared full grid.',
 'execution':'Signal is available after close at boundary m. Historical reference is minute m+1 open, exactly 60 seconds later; this is a backtest price, not a live quote or exchange fill.',
 'position':'At most one position per $2,000 configuration, full affordable cash; hold 180 minutes from decision boundary, then exit at the first hourly boundary at or after expiry, executing one minute later. Do not enter at an exit boundary. Do not enter when expiry would exceed terminal boundary. Rejected exits retain units and retry next eligible hourly boundary. Force terminal liquidation at 2026-09-14 00:01.',
 'cash':'Spot long only; no shorting, leverage, borrowing, funding, transfer, yield, scale-in, or rebalancing. Each direction/threshold cell owns an independent account.'}
cost={'capital_usdt':2000,'fee_per_side':0.001,'estimated_half_spread_per_side':0.0001,'slippage_per_side':0.0002,'impact_model':'0.5 * sample stdev(previous 20 complete UTC daily log returns) * sqrt(order quote budget / previous 20 complete daily quote ADV)','maximum_participation':0.001,'multipliers':[1,2,3],'all_cost_terms_scaled_together':True,'exchange_filter_snapshot_sha256':sha(ROUND/'exchange_filters.json'),'limitations':'Historical L2 and historical exchange filter schedules are unavailable; spread/slippage are estimates. Percent price uses the preceding five 1m quote/base-volume VWAP proxy. Immediate fill is an explicit OHLCV backtest assumption.'}
gates={'all_1x_2x_3x_net_returns_positive':True,'minimum_positive_1x_folds':8,'maximum_3x_sample_drawdown_pct':25,'minimum_3x_adjacent_neighbor_positive_fraction':0.60,'minimum_1x_round_trips':4,'minimum_1x_gross_reference_pnl_to_cost':2.5,'no_rejected_or_capacity_filtered_orders':True,'terminal_flat_all_scenes':True}
registry_path=ROOT/'research/automation/registry.jsonl';records=registry.read_records(registry_path)
prior_lead=[x for x in records.values() if x.get('spec',{}).get('family')=='spot-btc-eth-hourly-leadlag-follower-fixed-hold']
prior_status={k:sum(x['status']==k for x in prior_lead) for k in ('passed','rejected','abandoned','blocked','reserved')}
plan={'round':ROUND.name,'frozen_at_utc':utc(),'status':'frozen_before_evaluation','direction':'Two-way hourly cross-asset impulse follow-through; long only in the trailing asset.','hypothesis':'A short BTC/ETH impulse may transmit to the other liquid asset, but previous research found its apparent advantage was threshold/hold fragile. This round predeclares a symmetric two-way threshold surface at fixed 30m lookback and 3h hold; the aim is to test whether a broader signal-strength/gap plateau survives full costs, not to infer stable live profitability.','source_paper':{**paper,'accessed_utc':'2026-10-14','scope':'Motivates two-way discovery only; this grid is not a paper replication and prior results found limited intraday exploitability.'},'prior_work':{'prior_hourly_leadlag':'research/experiments/20261013T164415Z/result.md completed 18 configurations: all rejected. Best BTC→ETH L15/H240 was +8.88% 1x, +3.80% 2x, -1.03% 3x, only 6/12 positive folds and 0% positive 3x neighbors. It is context, not new evidence.','superseded_no_result_drafts':'The same round retained 18 abandoned before-compute drafts with no result; not being silently counted as tested or selected. This fresh batch is a distinct threshold sensitivity surface and will be independently reserved/finished.','initial16':'Prior evidence audit verified actual backtest reports for all 16 initial rows; there is no code-only original configuration to backfill.','history':'2025-09-16 through 2026-09-16 archived data is repeatedly reused development history, not an untouched holdout. Registry count includes extensive multiple testing; no DSR/PBO claim.'},'data':{'assets':data_files,'source_round':'research/experiments/20261013T164415Z/plan.json','market':'Binance spot 1m archived OHLCV with continuous UTC timestamps; daily cost inputs are aggregated from the same source. Historical signal entries/exits use the specified next-minute open only in this historical backtest.','oos_start_utc':start,'oos_end_exclusive_utc':end,'terminal_execution_utc':terminal,'start_day_index':368,'end_day_index':728,'oos_days':360,'folds':12,'fold_days':30,'warmup_days':365,'history_reused':True},'allocation':{'initial_capital_usdt':2000,'per_config_independent_account':True,'directions_are_separate_configurations':True,'follower_long_only':True,'weight_semantics':'100% of the independent $2,000 account allocated to the follower when signaled; this is one-asset exposure, not a BTC/ETH portfolio weight. No cross-account transfers.'},'rule':source_rules,'grid':{'directions':directions,'leader_lookback_minutes_fixed':lookback,'holding_minutes_fixed':hold,'leader_return_threshold':leader_thresholds,'leader_minus_follower_gap_threshold':relative_gap_thresholds,'configuration_count':18,'sensitivity_axes':['leader_return_threshold','leader_minus_follower_gap_threshold']},'cost_model':cost,'exchange_rules':{'path':'research/experiments/'+ROUND.name+'/exchange_info_raw.json','sha256':sha(meta),'received_at_utc':received,'symbols':['BTCUSDT','ETHUSDT'],'filters':{a:list(snapshot['filters'][a]) for a in ('BTC','ETH')}},'walk_forward':{'fold_days':30,'folds':12,'continuous_account_state_across_folds':True,'signal_uses_only_closed_bars':True,'label_purge_embargo':'No fitted labels or training phase; deterministic lagged signal, so no label leakage. Warmup is prior data only.','holdout_disclosure':'Repeated historical development/OOS window, not untouched.'},'failure_gates':gates,'benchmark_read_only':{'source_report':'research/experiments/20261013T123949Z/report.json','configurations':['hold_360d_btc_relative_strength_study','hold_360d_eth_relative_strength_study'],'reuse_only':True},'prior_registry_snapshot':{'events':len(registry.read_events(registry_path)),'unique_fingerprints':len(records),'prior_leadlag_statuses':prior_status}}
write(ROUND/'plan.json',plan)
batch=[];reserve_log=[];seen=set()
for d in directions:
 for t in leader_thresholds:
  for g in relative_gap_thresholds:
   name=f"lead_{d['leader'].lower()}_follow_{d['follower'].lower()}_L{lookback}_H{hold}_T{t:g}_G{g:g}"
   parameters={'leader':d['leader'],'follower':d['follower'],'leader_lookback_minutes':lookback,'fixed_hold_minutes':hold,'leader_return_threshold':t,'leader_minus_follower_gap_threshold':g,'decision_interval_minutes':60,'initial_capital_usdt':2000,'start_utc':start,'end_exclusive_utc':end,'terminal_execution_utc':terminal,'start_day_index':368,'end_day_index':728,'days':360,'fold_days':30,'folds':12,'warmup_days':365,'embargo_days':3,'cost_multipliers':[1,2,3],'exchange_filters_sha256':sha(ROUND/'exchange_filters.json'),'sensitivity_axes':['leader_return_threshold','leader_minus_follower_gap_threshold']}
   spec={'kind':'strategy','family':'spot-btc-eth-hourly-leadlag-follower-fixed-hold','market':'spot','universe':[d['leader']+'/USDT',d['follower']+'/USDT'],'timeframe':'1m','name':name,'logic':source_rules,'parameters':parameters,'validation_plan':str((ROUND/'plan.json').relative_to(ROOT)),'sources':[paper]}
   fp=registry.fingerprint(spec);assert fp not in seen;seen.add(fp)
   path=ROUND/'specs'/(name+'.json');write(path,spec)
   run=subprocess.run([sys.executable,str(ROOT/'research/automation/registry.py'),'reserve',str(path.relative_to(ROOT))],cwd=ROOT,text=True,capture_output=True)
   reserve_log.append({'name':name,'fingerprint':fp,'returncode':run.returncode,'stdout':run.stdout.strip(),'stderr':run.stderr.strip()})
   if run.returncode:write(ROUND/'reserve_partial.json',reserve_log);raise SystemExit('reserve failed: '+name+' '+run.stdout+run.stderr)
   batch.append({'name':name,'leader':d['leader'],'follower':d['follower'],'lookback_minutes':lookback,'hold_minutes':hold,'leader_threshold':t,'relative_gap_threshold':g,'fingerprint':fp,'spec':str(path.relative_to(ROOT))})
write(ROUND/'batch.json',batch);write(ROUND/'reserve.json',reserve_log)
print(json.dumps({'frozen':True,'candidate_configs':len(batch),'directions':2,'threshold_surface':'3x3 per direction','plan_sha256':sha(ROUND/'plan.json'),'fresh_filters_sha256':sha(meta),'prior_leadlag_statuses':prior_status},ensure_ascii=False))
