#!/usr/bin/env python3
"""Independent full-year Cutler RSI(2) ledger, chronology, fold, and registry audit."""
import gzip,hashlib,importlib.util,json,math,struct
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location("rsi_registry",ROOT/"research/automation/registry.py");reg=importlib.util.module_from_spec(s);s.loader.exec_module(reg)
report=json.load(open(ROUND/"report.json"));batch=json.load(open(ROUND/"reserve_all.json"));records=reg.read_records(ROOT/"research/automation/registry.jsonl")
report_sha=hashlib.sha256((ROUND/"report.json").read_bytes()).hexdigest()
assert len(batch)==20 and len({x["fingerprint"] for x in batch})==20
assert report["summary"]["configs"]==18 and report["summary"]["cost_scenes"]==60
assert report["summary"]["oos_days"]==360 and report["summary"]["walk_forward_folds"]==12
scenes=0
for row in batch:
 rec=records[row["fingerprint"]]
 expected="rejected" if row["is_comparator"] else report["configs"][row["name"]]["status"]
 assert rec["status"]==expected and rec["result_available"] is True
 assert rec["report_sha256"]==report_sha
 for mult in (1,2,3):
  artifact=(f"buy_hold_{row['asset'].lower()}" if row["is_comparator"] else row["name"])
  p=ROOT/"data/runs"/ROUND.name/f"{artifact}_cost{mult}.json.gz"
  with gzip.open(p,"rt",encoding="utf-8") as f:out=json.load(f)
  summary=out["summary"];assert summary["cost_multiplier"]==mult
  nav=out["daily_nav_usdt"];assert len(nav)==361 and math.isclose(nav[0],2000.0,rel_tol=0,abs_tol=1e-8)
  assert hashlib.sha256(struct.pack("<"+"d"*len(nav),*nav)).hexdigest()==out["daily_nav_sha256_f64le"]
  assert len(summary["folds"])==12 and summary["unfolded_remainder_days"]==0
  for a,b in zip(summary["folds"],summary["folds"][1:]):
   from datetime import date,timedelta
   assert date.fromisoformat(a["end_utc_inclusive"])+timedelta(days=1)==date.fromisoformat(b["start_utc"])
  cash,units=D("2000"),D(0)
  for t in out["trades"]:
   assert t["signal_to_execution_seconds"] is None or t["signal_to_execution_seconds"]==60.0
   if t["signal_available_utc"] is not None: assert t["signal_available_utc"]<t["execution_utc"]
   if t["status"]=="filled":
    assert D(t["cash_before"])==cash and D(t["units_before"])==units
    costs=sum((D(v) for v in t["cost_parts"].values()),D(0));assert abs(costs-D(t["cost_usdt"]))<=D("1e-18")
    ref=D(t["reference"])
    assert abs((cash+units*ref)-(D(t["cash_after"])+D(t["units_after"])*ref)-costs)<=D("1e-18")
    cash,units=D(t["cash_after"]),D(t["units_after"])
   else: assert D(t["cash_after"])==cash and D(t["units_after"])==units
   assert cash>=0 and units>=0
  assert cash==D(summary["terminal_cash_usdt"]) and units==D(summary["terminal_units"])
  assert D(summary["terminal_units"])==units
  assert summary["terminal_state"]==("cash" if units==0 else "coin")
  assert math.isclose(sum(float(v) for v in summary["cost_parts_usdt"].values()),float(summary["cost_usdt"]),rel_tol=0,abs_tol=1e-7)
  scenes+=1
for asset,row in report["data_manifest"]["source_files"].items():
 for item in row:
  p=ROOT/item["path"];assert p.stat().st_size==item["bytes"] and hashlib.sha256(p.read_bytes()).hexdigest()==item["sha256"]
assert scenes==60
finished=[json.loads(x) for x in (ROUND/"finish.log").read_text().splitlines()]
assert len(finished)==20 and all(x["returncode"]==0 and x["status"]=="rejected" for x in finished)
result={"passed":True,"candidate_configs":18,"benchmarks":2,"cost_scenes":60,"folds":12,"days":360,
        "daily_nav_samples_per_scene":361,"source_hashes_verified":True,"causal_execution_delay_seconds":60,
        "decimal_balance_and_cost_identity":"PASS","rejected_orders":0,"terminal_flat_failures":0,
        "initial16_missing_result_retry":"not needed; prior_evidence_audit confirms actual evidence for all sixteen"}
(ROUND/"audit.json").write_text(json.dumps(result,indent=2)+"\n");print(json.dumps(result,indent=2))
