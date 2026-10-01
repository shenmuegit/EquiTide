"""Finish the already calculated full grid against the immutable final report."""
import json
import subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
ROUND=Path(__file__).resolve().parent
report=json.loads((ROUND/'report.json').read_text())
for item in json.loads((ROUND/'batch.json').read_text()):
 row=report['configs'][item['name']]
 assert row['actual_backtest_result'] is (row['status'] in ('passed','rejected'))
 result=subprocess.run(['python3',str(ROOT/'research/automation/registry.py'),'finish',item['spec'],row['status'],str((ROUND/'report.json').relative_to(ROOT))],cwd=ROOT,capture_output=True,text=True)
 assert result.returncode==0,result.stdout+result.stderr
 print(json.dumps({'config':item['name'],'status':row['status'],'fingerprint':result.stdout.strip()}),flush=True)
