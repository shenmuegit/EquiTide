#!/usr/bin/env python3
"""Freeze and reserve the 12-fold annual Cutler RSI(2) extension."""
import hashlib, json, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
ROUND=Path(__file__).resolve().parent
SOURCE=ROOT/"research/experiments/20261012T212608Z"
sys.path.insert(0,str(ROOT/"research/automation"));import registry

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

previous=json.load(open(SOURCE/"plan.json"))
previous_report=SOURCE/"report.json"
filters_report=ROOT/"research/experiments/20261012T035429Z/report.json"
bars=[]
for asset in ("BTC","ETH"):
    for suffix in (f"{asset}_20240916T000000Z_20250916T000000Z_transfer_20261001",
                   f"{asset}_20250916T000000Z_20260916T000000Z_archive_20260929"):
        p=ROOT/f"data/normalized/binance/{asset}/binance_{suffix}/spot_bars.parquet"
        bars.append({"asset":asset,"path":str(p.relative_to(ROOT)),"bytes":p.stat().st_size,"sha256":sha(p)})

plan={
 "round":ROUND.name,
 "frozen_at_utc":"2026-10-13T03:26:40Z",
 "direction":"Extend the preregistered daily Cutler RSI(2) pullback plus close-above-SMA filter to a full 360-day, twelve-fold OOS interval.",
 "reason_for_extension":"The earlier 183-day screen had positive cumulative returns in some variants but zero candidates passed its six-fold consistency gate. Before selecting any parameter from those outcomes, evaluate the same frozen 3x3 RSI threshold/SMA grid over a predeclared full-year interval that includes the earlier period and the prior six months. Changed OOS boundaries/fold count make each definition distinct; no threshold, SMA length, or signal rule is selected from the earlier result.",
 "prior_screen":{"report":"research/experiments/20261012T212608Z/report.json","sha256":sha(previous_report),"candidate_configs":18,"candidate_passed":0,"candidate_rejected":18,"oos_days":183,"folds":6},
 "rules_reused_from":"research/experiments/20261012T212608Z/specs/",
 "grid":{"assets":["BTC","ETH"],"rsi_lookback_changes":2,"entry_rsi":[5,10,15],"exit_rsi":50,"trend_sma_days":[100,150,200],"candidate_configs":18,"benchmarks":2},
 "time_boundaries":{"input_history_utc":"2024-09-16T00:00:00Z/2026-09-16T00:00:00Z","oos_start_utc":"2025-09-19T00:01:00Z","oos_terminal_utc":"2026-09-14T00:01:00Z","oos_days":360,"folds":12,"fold_days":30,"embargo_days":3,"rolling_train_days":365,"reuse_disclosure":"The full period is repeated development/validation history and is not an untouched final holdout."},
 "costs":{"fee_each_side":"10bp","half_spread_estimate_each_side":"1bp","slippage_estimate_each_side":"2bp","impact":"0.5 * sample stdev(previous 20 complete UTC daily log returns) * sqrt(order quote budget / previous 20 complete UTC daily quote-volume ADV)","maximum_participation":"0.1% of prior 20-day quote ADV","multipliers":[1,2,3],"filters_source":"research/experiments/20261012T035429Z/report.json","filters_sha256":sha(filters_report),"l2_data":"Unavailable; half-spread and impact are estimates.","market":"Unlevered long-only spot; no funding or borrow."},
 "source_files":bars,
 "failure_gates":{"all_1x_2x_3x_net_returns_positive":True,"minimum_positive_1x_folds":8,"maximum_3x_daily_sample_drawdown_pct":25,"minimum_3x_adjacent_neighborhood_positive_fraction":0.60,"minimum_1x_round_trips":2,"minimum_1x_gross_reference_pnl_to_cost":2.5,"no_balance_or_rejected_order_violations":True,"terminal_flat":True},
 "bias_note":"Repeated historical research, 4349 unique ledger fingerprints before this batch; parameter choice remains subject to substantial multiple-testing and reuse bias. A positive result would still require forward paper validation."
}
(ROUND/"plan.json").write_text(json.dumps(plan,indent=2,ensure_ascii=False)+"\n")
batch=[]
for asset in ("BTC","ETH"):
 for entry in (5,10,15):
  for sma in (100,150,200):
   source=SOURCE/"specs"/f"cutler_rsi2_{asset.lower()}_entry{entry}_sma{sma}.json"
   spec=json.load(open(source));spec["name"]=f"cutler_rsi2_annual_{asset.lower()}_entry{entry}_sma{sma}"
   params=spec["parameters"]
   params.update({"oos_start_utc":"2025-09-19T00:01:00Z","oos_terminal_utc":"2026-09-14T00:01:00Z",
                  "walk_forward_test_days":30,"walk_forward_folds":12,"walk_forward_step_days":30,
                  "walk_forward_train_days":365,"embargo_days":3,"oos_first_daily_index":368,
                  "oos_end_exclusive_daily_index":728,
                  "sensitivity_axes":["entry_rsi","trend_sma_days"],
                  "result_scope":"new full-year OOS boundary; not the prior 183-day output"})
   gates=dict(plan["failure_gates"]);spec["failure_gates"]=gates
   out=ROUND/"specs"/(spec["name"]+".json");out.write_text(json.dumps(spec,indent=2,ensure_ascii=False)+"\n")
   batch.append({"name":spec["name"],"asset":asset,"spec":str(out.relative_to(ROOT)),"fingerprint":registry.fingerprint(spec),"is_comparator":False})
for asset in ("BTC","ETH"):
 source=SOURCE/"specs"/f"buy_hold_{asset.lower()}.json";spec=json.load(open(source))
 spec["name"]=f"annual_hold_{asset.lower()}_rsi_period"
 spec["parameters"].update({"oos_start_utc":"2025-09-19T00:01:00Z","oos_terminal_utc":"2026-09-14T00:01:00Z",
                            "walk_forward_folds":12,"walk_forward_test_days":30,"oos_days":360})
 out=ROUND/"specs"/(spec["name"]+".json");out.write_text(json.dumps(spec,indent=2,ensure_ascii=False)+"\n")
 batch.append({"name":spec["name"],"asset":asset,"spec":str(out.relative_to(ROOT)),"fingerprint":registry.fingerprint(spec),"is_comparator":True})
(ROUND/"batch.json").write_text(json.dumps(batch,indent=2)+"\n")
rows=[]
for x in batch:
 p=subprocess.run([sys.executable,str(ROOT/"research/automation/registry.py"),"reserve",str(ROOT/x["spec"])],cwd=ROOT,capture_output=True,text=True)
 row={**x,"exit_code":p.returncode,"output":p.stdout.strip(),"stderr":p.stderr.strip()};rows.append(row)
 if p.returncode:
  (ROUND/"reserve.json").write_text(json.dumps(rows,indent=2)+"\n")
  raise SystemExit(f"reserve failed before calculation: {x['name']} rc={p.returncode} {p.stdout} {p.stderr}")
(ROUND/"reserve_all.json").write_text(json.dumps(rows,indent=2)+"\n")
(ROUND/"reserve.json").write_text(json.dumps([x for x in rows if not x["is_comparator"]],indent=2)+"\n")
(ROUND/"benchmark_reserve.json").write_text(json.dumps([x for x in rows if x["is_comparator"]],indent=2)+"\n")
print(json.dumps({"reserved":len(rows),"unique_fingerprints":len({x['fingerprint'] for x in rows}),"candidate_configs":18,"benchmarks":2,"cost_scenarios":60},indent=2))
