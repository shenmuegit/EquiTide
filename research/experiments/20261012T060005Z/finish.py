#!/usr/bin/env python3
"""Finish each already reserved candidate and comparator from actual evidence."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ROUND = Path(__file__).resolve().parent
report = json.loads((ROUND / "report.json").read_text(encoding="utf-8"))
batch = json.loads((ROUND / "batch.json").read_text(encoding="utf-8"))
audit = json.loads((ROUND / "audit.json").read_text(encoding="utf-8"))
assert audit["passed"] and len(batch) == 26
assert report["summary"]["candidate_configs"] == 24
with (ROUND / "finish.log").open("w", encoding="utf-8") as log:
    for row in batch:
        status = "rejected" if row["is_comparator"] else report["configs"][row["name"]]["status"]
        assert status in ("passed", "rejected")
        command = [sys.executable, str(ROOT / "research/automation/registry.py"), "finish",
                   str(ROOT / row["spec"]), status,
                   str((ROUND / "report.json").relative_to(ROOT))]
        proc = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        line = json.dumps({"name": row["name"], "status": status, "returncode": proc.returncode,
                           "stdout": proc.stdout.strip(), "stderr": proc.stderr.strip()}, ensure_ascii=False)
        log.write(line + "\n")
        log.flush()
        if proc.returncode != 0:
            raise SystemExit(f"finish failed for {row['name']}: {line}")
print(json.dumps({"finished": len(batch), "candidate_passed": 0,
                  "candidate_rejected": 24, "comparator_rejected_reference_only": 2,
                  "report": str((ROUND / "report.json").relative_to(ROOT))}))
