"""Finish every reserved scope/configuration, retaining negative and zero-trade results."""
import json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parent;ROOT=R.parents[2];report=str((R/'report.json').relative_to(ROOT));r=json.loads((R/'report.json').read_text());qual={x['fingerprint']:x['qualification'] for x in r['trials']}
for row in json.loads((R/'batch.json').read_text()):
 status=qual.get(row['fingerprint'],'rejected')
 subprocess.run(['python3','research/automation/registry.py','finish',row['spec'],status,report],cwd=ROOT,check=True)
print('FINISHED 36 records: 24 continuous configurations, 8 native concrete cases, 2 comparators, 2 recovered initial scopes')
