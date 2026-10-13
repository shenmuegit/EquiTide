#!/usr/bin/env python3
"""Freeze and reserve the UTC-hour half-hour continuation study."""
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
(ROUND/"specs").mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/"research/automation"));import registry
FILTER_SOURCE=ROOT/"research/experiments/20261012T035429Z/report.json"
filters=json.load(open(FILTER_SOURCE))["plan"]["execution"]["filters"]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

source_files={}
for asset in ("BTC","ETH"):
 source_files[asset]=[]
 for suffix in (f"{asset}_20240916T000000Z_20250916T000000Z_transfer_20261001",f"{asset}_20250916T000000Z_20260916T000000Z_archive_20260929"):
  p=ROOT/f"data/normalized/binance/{asset}/binance_{suffix}/spot_bars.parquet"
  source_files[asset].append({"path":str(p.relative_to(ROOT)),"bytes":p.stat().st_size,"sha256":sha(p)})
paper={"citation":"Shen, D., Urquhart, A., & Wang, P. (2022). Bitcoin intraday time-series momentum. Financial Review, 57(2), 319–344. DOI:10.1111/fire.12290.",
       "url":"https://doi.org/10.1111/fire.12290","accessed_utc":"2026-10-13",
       "reported_finding":"The authors report that the first half-hour positively predicts the last half-hour return and that high-volume/high-volatility first sessions show stronger predictability. This BTC study motivates, but does not validate, our fixed UTC-hour BTC/ETH spot adaptation."}
grid={"first_half_return_threshold":[0.0,0.0005,0.001],"same_slot_quote_volume_ratio_min":[0.75,1.0,1.25]}
common={"first_half_minutes":30,"second_half_hold_minutes":30,"same_slot_reference_days":20,
        "initial_capital_usdt":2000,"oos_start_utc":"2025-09-19T00:00:00Z","oos_end_exclusive_utc":"2026-09-14T00:00:00Z",
        "oos_terminal_execution_utc":"2026-09-14T00:01:00Z","oos_start_day_index":368,"oos_end_day_index":728,
        "walk_forward_train_days":365,"walk_forward_test_days":30,"walk_forward_step_days":30,"walk_forward_folds":12,"embargo_days":3,
        "cost_multipliers":[1,2,3],"fee_rate_per_side":0.001,"half_spread_estimate_per_side":0.0001,"slippage_estimate_per_side":0.0002,
        "impact_model":"0.5 * sample_stdev(previous 20 complete UTC daily log returns) * sqrt(order quote budget / previous 20 complete UTC daily quote-volume ADV)",
        "maximum_participation":0.001,"exchange_filters":"Frozen Binance PRICE_FILTER, LOT_SIZE, NOTIONAL, PERCENT_PRICE_BY_SIDE; adverse tick, lot floor, previous closed 5-minute VWAP proxy."}
plan={"round":ROUND.name,"frozen_at_utc":"2026-10-13T05:29:46Z",
 "direction":"Intrahour half-hour time-series continuation, long-only Binance spot, with a same-UTC-hour first-half quote-volume gate.",
 "hypothesis":"Primary Bitcoin research reports first-half-hour return predictiveness for the last half-hour and stronger effects in high-volume/high-volatility sessions. Test a causal next-minute-open adaptation with a predeclared same-slot quote-volume filter on BTC and ETH; the rule is not a paper replication.",
 "source_paper":paper,"grid":{"assets":["BTC","ETH"],**grid,"candidate_configs":18,"benchmarks":2,"total_registry_definitions":20},
 "rule":"For each completed UTC hour h, calculate first-half return close(minute h+29)/open(minute h)-1 and first-half quote volume as the sum of quote_volume over the 30 closed one-minute bars h through h+29. Calculate the quote-volume ratio against the arithmetic mean of the previous 20 fully completed UTC days' first-half quote volume at the same UTC hour h; current day is excluded. If first-half return is strictly greater than the configured threshold and volume ratio is at least the configured minimum, enter long at the next one-minute open h+31 (signal availability h+30, fixed 60-second delay). Schedule full exit at the next hour's first-minute open h+61, giving a 30-minute holding window. If exit execution is rejected, retry at each next one-minute open until filled; while still holding, ignore a later entry signal rather than backfill it. No leverage, shorting, add-on or inter-asset transfer. Common OOS terminal liquidation is costed.",
 "time_boundaries":{"history_utc":"2024-09-16T00:00:00Z/2026-09-16T00:00:00Z","warmup_days":365,"embargo_days":3,"oos_start_utc":common["oos_start_utc"],"oos_end_exclusive_utc":common["oos_end_exclusive_utc"],"oos_days":360,"walk_forward":"12 continuous non-overlapping 30-day folds; no fitted parameters; events are scheduled from completed first-half bars only.","history_disclosure":"Repeatedly used repository development/validation history; not an untouched final holdout."},
 "sensitivity_axes":["first_half_return_threshold","same_slot_quote_volume_ratio_min"],
 "execution":{"signal_data":"Binance spot closed 1m OHLCV aggregated into rolling UTC-hour first/second half sessions; price reference uses minute opens after signal availability.","filters_source":"research/experiments/20261012T035429Z/report.json","filters_sha256":sha(FILTER_SOURCE),"source_files":source_files,"accounting":"Separate 2,000 USDT account per asset/config, cash compounds after each scheduled window; no interest/rebalance."},
 "costs":{"fee_each_side":"10bp","half_spread_estimate_each_side":"1bp","slippage_each_side":"2bp","impact":"0.5 × prior 20 complete UTC day return stdev × sqrt(order quote budget / prior 20-day quote ADV)","maximum_participation":"0.1% of lagged ADV","multipliers":[1,2,3],"spread_counted_once":True,"market_depth":"No historical L2; spread and impact are estimates.","funding_borrow":"Not applicable: long-only spot."},
 "failure_gates":{"all_1x_2x_3x_returns_positive":True,"minimum_positive_1x_folds":8,"maximum_3x_minute_close_sample_drawdown_pct":25,"minimum_3x_adjacent_neighbor_positive_fraction":0.60,"minimum_1x_round_trips":250,"minimum_1x_gross_pnl_to_cost":2.5,"no_capacity_balance_or_rejected_orders":True,"terminal_flat":True,"interpretation":"Positive backtest results are historical screens only and do not establish future or live profitability."},
 "prior_research":"The repository has tested 15m quarter-hour scheduled windows, 4h volume-confirmed momentum, and 4h/daily reversal variants. This distinct half-hour response is fixed before result calculation; all cost/volume filters and the 20-config reserve history are preserved."}
(ROUND/"plan.json").write_text(json.dumps(plan,indent=2,ensure_ascii=False)+"\n")
batch=[]
for asset in ("BTC","ETH"):
 for ret in grid["first_half_return_threshold"]:
  for vol in grid["same_slot_quote_volume_ratio_min"]:
   name=f"hhr_{asset.lower()}_ret{int(ret*10000):02d}_vol{int(vol*100):03d}"
   spec={"kind":"strategy","family":"spot-intrahour-halfhour-momentum","market":"spot","timeframe":"1h","universe":[f"{asset}/USDT"],"name":name,
    "logic":{"entry":"Using a newly completed UTC first-half-hour, compute close(minute h+29)/open(minute h)-1; enter only if return > first_half_return_threshold AND first-half quote_volume / mean(first-half quote_volume at the same UTC hour over the previous 20 fully closed UTC days) >= same_slot_quote_volume_ratio_min.",
             "timing":"Current first-half data is closed and available at h+30. Entry reference is h+31 one-minute open (60 seconds after signal availability). Exit is scheduled at h+61 open, 30 minutes after entry; no price from the traded interval influences its entry.",
             "exit":"Sell full position at scheduled h+61 open. If rejected by frozen exchange filters, retry next one-minute opens until filled, with no missed entry retroactively inserted; ignore any next scheduled entry while inventory remains.",
             "sizing":"Independent 2,000 USDT long-only spot account per asset and parameter set; use currently available cash, no leverage/add-on/borrow/yield/transfers."},
    "parameters":{**common,"first_half_return_threshold":ret,"same_slot_quote_volume_ratio_min":vol,"sensitivity_axes":["first_half_return_threshold","same_slot_quote_volume_ratio_min"]},
    "sources":[paper],"failure_gates":plan["failure_gates"]}
   p=ROUND/"specs"/(name+".json");p.write_text(json.dumps(spec,indent=2,ensure_ascii=False)+"\n")
   batch.append({"name":name,"asset":asset,"spec":str(p.relative_to(ROOT)),"fingerprint":registry.fingerprint(spec),"is_comparator":False})
for asset in ("BTC","ETH"):
 name=f"hold_360d_{asset}_halfhour_period"
 spec={"kind":"strategy","family":"spot-hourly-halfhour-hold-reference","market":"spot","timeframe":"1h","universe":[f"{asset}/USDT"],"name":name,
       "logic":{"entry":"Buy at the same OOS start executable minute open irrespective of signal.","exit":"Hold to common OOS terminal execution and liquidate with the same costs.","sizing":"Independent 2,000 USDT unlevered long-only spot benchmark."},
       "parameters":{"initial_capital_usdt":2000,"oos_start_utc":common["oos_start_utc"],"oos_terminal_execution_utc":common["oos_terminal_execution_utc"],"oos_days":360,"cost_multipliers":[1,2,3]},"sources":[paper]}
 p=ROUND/"specs"/(name+".json");p.write_text(json.dumps(spec,indent=2,ensure_ascii=False)+"\n")
 batch.append({"name":name,"asset":asset,"spec":str(p.relative_to(ROOT)),"fingerprint":registry.fingerprint(spec),"is_comparator":True})
(ROUND/"batch.json").write_text(json.dumps(batch,indent=2)+"\n")
reserved=[]
for x in batch:
 p=subprocess.run([sys.executable,str(ROOT/"research/automation/registry.py"),"reserve",str(ROOT/x["spec"])],cwd=ROOT,capture_output=True,text=True)
 row={**x,"exit_code":p.returncode,"output":p.stdout.strip(),"stderr":p.stderr.strip()};reserved.append(row)
 if p.returncode:
  (ROUND/"reserve_partial.json").write_text(json.dumps(reserved,indent=2)+"\n")
  raise SystemExit(f"reserve failed before calculation {x['name']} rc={p.returncode}: {p.stdout} {p.stderr}")
(ROUND/"reserve_all.json").write_text(json.dumps(reserved,indent=2)+"\n")
(ROUND/"reserve.json").write_text(json.dumps([x for x in reserved if not x["is_comparator"]],indent=2)+"\n")
(ROUND/"benchmark_reserve.json").write_text(json.dumps([x for x in reserved if x["is_comparator"]],indent=2)+"\n")
print(json.dumps({"reservations":len(reserved),"unique":len({x['fingerprint'] for x in reserved}),"candidates":18,"benchmarks":2,"scenes":60},indent=2))
