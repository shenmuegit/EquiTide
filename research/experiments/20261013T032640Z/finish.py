#!/usr/bin/env python3
"""Finish or verify the 18 full-year variants and two matched benchmarks."""
import hashlib, importlib.util, json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"research/automation"));import registry
report=json.loads((ROUND/"report.json").read_text())
batch=json.loads((ROUND/"reserve_all.json").read_text())
report_sha=hashlib.sha256((ROUND/"report.json").read_bytes()).hexdigest()
records=registry.read_records(ROOT/"research/automation/registry.jsonl")
with (ROUND/"finish.log").open("w") as log:
 for row in batch:
  status="rejected" if row["is_comparator"] else report["configs"][row["name"]]["status"]
  existing=records.get(row["fingerprint"],{})
  if existing.get("status")==status and existing.get("result_available") is True:
   rec={"name":row["name"],"fingerprint":row["fingerprint"],"status":status,"action":"verified_existing_finish","returncode":0,"stdout":row["fingerprint"],"stderr":""}
  else:
   if existing.get("status")!="reserved":
    raise SystemExit(f"cannot finish {row['name']}: current state is {existing.get('status')}")
   p=subprocess.run([sys.executable,str(ROOT/"research/automation/registry.py"),"finish",str(ROOT/row["spec"]),status,str(ROUND/"report.json")],cwd=ROOT,capture_output=True,text=True)
   rec={"name":row["name"],"fingerprint":row["fingerprint"],"status":status,"action":"finished_now","returncode":p.returncode,"stdout":p.stdout.strip(),"stderr":p.stderr.strip()}
   if p.returncode:raise SystemExit(json.dumps(rec))
   records=registry.read_records(ROOT/"research/automation/registry.jsonl")
  log.write(json.dumps(rec,ensure_ascii=False)+"\n");log.flush()
print(json.dumps({"finished":len(batch),"candidate_passed":report["summary"]["passed"],"candidate_rejected":report["summary"]["rejected"],"benchmarks":2}))
