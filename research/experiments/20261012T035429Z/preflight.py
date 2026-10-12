"""Freeze a one-axis-at-a-time 2D allocation/ETH-entry neighborhood from complete prior evidence."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal as D
import copy,gzip,hashlib,json,subprocess,sys,zipfile
T=Path(__file__).resolve().parent;R=T.parents[2]
sys.path.insert(0,str(R/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ledger=R/'research/automation/registry.jsonl';raw=ledger.read_bytes();rows=[json.loads(x)for x in raw.splitlines()];records=registry.read_records(ledger)
assert not [x for x in records.values()if x.get('status')=='reserved']
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip();remote=subprocess.check_output(['git','rev-parse','origin/codex/strategy-research'],cwd=R,text=True).strip();assert head==remote
status=subprocess.check_output(['git','status','--porcelain','--untracked-files=all'],cwd=R,text=True).splitlines();assert all(line.endswith(T.relative_to(R).as_posix()+'/'+line.split(T.name+'/',1)[-1].strip()) if False else line.startswith('?? '+T.relative_to(R).as_posix()+'/') for line in status),status
canonical={registry.fingerprint(v['spec']):v for v in records.values()};conclusions=[]
for p in sorted((R/'research/experiments').glob('*/result.md')):
 if p.parent==T:continue
 conclusions.append({'path':str(p.relative_to(R)),'sha256':sha(p),'text':p.read_text()})
oos={str(p.relative_to(R)):{'sha256':sha(p),'text':p.read_text()}for p in sorted((R/'checks').glob('*oos.py'))};assert len(oos)==4
freqtrade=[]
for p in sorted((R/'freqtrade_trial/results').iterdir()):
 if not p.is_file():continue
 blob=p.read_bytes();members=[]
 if p.suffix=='.zip':
  with zipfile.ZipFile(p)as z:
   for name in z.namelist():
    b=z.read(name);members.append({'name':name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
    if name.endswith('.json'):json.loads(b)
 elif p.suffix=='.json':json.loads(blob)
 else:blob.decode('utf-8')
 freqtrade.append({'path':str(p.relative_to(R)),'bytes':len(blob),'sha256':sha(p),'members':members})
assert len(freqtrade)==7
initial=[]
for n,row in enumerate(rows[:16],1):
 fp=row['fingerprint'];v=records[fp];evidence=copy.deepcopy(v.get('result_evidence')or[])
 if not evidence and v.get('report'):evidence=[{'path':v['report'],'sha256':v['report_sha256'],'type':'actual_report_pointer'}]
 assert v.get('result_available') and evidence
 for ev in evidence:
  path=R/ev['path'];assert sha(path)==ev['sha256']
  if ev['type']=='actual_report_pointer':
   doc=json.loads(path.read_text());assert fp in json.dumps(doc)or registry.fingerprint(v['spec'])in json.dumps(doc)
 initial.append({'position':n,'fingerprint':fp,'canonical_fingerprint':registry.fingerprint(v['spec']),'family':row['spec']['family'],'status':v['status'],'evidence':evidence})
assert len(initial)==16
paper=json.loads((R/'research/paper10/state.json').read_text());assert paper['observations']==52 and paper['last_observation_id']=='20261012T023803425448Z'
protected={'research/paper10/plan.json':sha(R/'research/paper10/plan.json'),'research/paper10/state.json':sha(R/'research/paper10/state.json')}
for name in ('20261012T023522370176Z','20261012T023611651051Z','20261012T023803425448Z'):
 root=R/'research/paper10/observations'/name
 for p in sorted(root.rglob('*')):
  if p.is_file():protected[str(p.relative_to(R))]=sha(p)
for path,h in protected.items():assert sha(R/path)==h
summary={'checked_at_utc':datetime.now(timezone.utc).isoformat(),'base_head':head,'base_tree':subprocess.check_output(['git','rev-parse','HEAD^{tree}'],cwd=R,text=True).strip(),'registry_rows':len(rows),'canonical':len(canonical),'preserved_ids':len(records),'ledger_sha256':sha(ledger),'records':records,'conclusions':conclusions,'oos_checks':oos,'freqtrade_results':freqtrade,'initial16_actual_results_checked':initial,'initial16_missing':[],'paper10_state_sha256':protected['research/paper10/state.json'],'paper10_plan_sha256':protected['research/paper10/plan.json'],'paper10_last_observation':paper['last_observation_id'],'paper10_observations':52,'paper10_protected_sha256':protected,'read_task_sha256':sha(R/'research/automation/task.md'),'read_task_text':(R/'research/automation/task.md').read_text(),'automation_readme_sha256':sha(R/'research/automation/README.md'),'automation_readme_text':(R/'research/automation/README.md').read_text(),'monitor_readme_sha256':sha(R/'research/monitor/README.md'),'monitor_readme_text':(R/'research/monitor/README.md').read_text(),'skills':{str((R/'.agents/skills'/n/'SKILL.md').relative_to(R)):{'sha256':sha(R/'.agents/skills'/n/'SKILL.md'),'text':(R/'.agents/skills'/n/'SKILL.md').read_text()}for n in ('walk-forward-validation','ml4t-sensitivity-analysis','ml4t-transaction-costs')}}
with(T/'prior_summary.json.gz').open('wb')as f:
 with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0)as z:z.write(json.dumps(summary,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
(T/'prior_evidence_audit.json').write_text(json.dumps({'selection':'The original sixteen raw ledger rows, in order.','checked_at_utc':summary['checked_at_utc'],'initial16_actual_results_checked':initial,'missing_initial16':[]},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'base_head':head,'registry_rows':len(rows),'canonical':len(canonical),'previous_result_docs':len(conclusions),'initial16_missing':0,'paper10_state_preserved':52,'freqtrade_archives':len(freqtrade)}))
