#!/usr/bin/env python3
"""Finish every successfully reserved configuration after actual evaluation."""
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ROUND = Path(__file__).resolve().parent
report = json.loads((ROUND / "report.json").read_text())
batch = json.loads((ROUND / "batch.json").read_text())
statuses = []
with (ROUND / "finish.log").open("w") as log:
    for row in batch:
        status = "rejected" if row["is_comparator"] else report["configs"][row["name"]]["status"]
        result = subprocess.run([sys.executable, str(ROOT / "research/automation/registry.py"),
                                 "finish", str(ROOT / row["spec"]), status,
                                 str(ROUND / "report.json")], cwd=ROOT,
                                capture_output=True, text=True)
        record = {"name": row["name"], "fingerprint": row["fingerprint"], "status": status,
                  "returncode": result.returncode, "stdout": result.stdout.strip(),
                  "stderr": result.stderr.strip()}
        log.write(json.dumps(record, ensure_ascii=False) + "\n"); log.flush()
        if result.returncode:
            raise SystemExit(f"registry finish failed for {row['name']}: {result.stderr}")
        statuses.append(status)
print(json.dumps({"finished": len(statuses), "candidates_rejected": sum(not x["is_comparator"] for x in batch),
                  "benchmarks_rejected_as_references": sum(x["is_comparator"] for x in batch),
                  "status_counts": {name: statuses.count(name) for name in sorted(set(statuses))}}, indent=2))
