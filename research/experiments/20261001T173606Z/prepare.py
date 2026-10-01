"""Freeze the same execution/rule grid on an earlier, nonoverlapping OOS period."""
import gzip
import hashlib
import importlib.util
import json
import subprocess
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent;OLD=ROOT/'research/experiments/20261001T133655Z'
s=importlib.util.spec_from_file_location('registry',ROOT/'research/automation/registry.py');reg=importlib.util.module_from_spec(s);s.loader.exec_module(reg)
ledger=ROOT/'research/automation/registry.jsonl';records=reg.read_records(ledger)
assert len({reg.fingerprint(v['spec']) for v in records.values()})==218 and all(v.get('result_available') and v['status']!='reserved' for v in records.values())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
oldreport=json.loads((OLD/'report.json').read_text());plan=json.loads((OLD/'spec.json').read_text())
for k in ('delayed_execution','actual_first_tool_utc'):plan.pop(k,None)
plan.update(round=ROUND.name,trigger_utc='2026-10-01T17:36:06.903Z',actual_first_tool_utc='2026-10-01T17:37:02Z',frozen_at_utc=datetime.now(timezone.utc).isoformat(),
 hypothesis='Keep the entire already-used SMA60/65/70 and65/75/85%BTC grid unchanged and test economic transfer to March-September2025. Newly downloaded earlier history adds market-stage evidence but is not forward or a pristine holdout; no retuning permitted after transfer outcomes.',
 data_start_utc='2024-09-16T00:00:00Z',data_end_exclusive_utc='2025-09-16T00:00:00Z',oos_start_utc='2025-03-18T00:01:00Z',terminal_exit_utc='2025-09-14T00:01:00Z',
 previous_period_reference={'report':str((OLD/'report.json').relative_to(ROOT)),'sha256':sha(OLD/'report.json'),'OOS_start':'2026-03-18T00:01:00Z','OOS_end':'2026-09-14T00:01:00Z','prior_passed':oldreport['summary']['passed'],'comparison':'Read previously completed results; no recomputation of2026strategies and no unregistered concatenated-period portfolio calculation.'},
 transfer_confirmation='A combination confirms the prior historical candidate only if the same mathematical/execution rule meets frozen gates in BOTH separately reported periods; new passed status here refers to2025period gates. No stable live/forward profitability inference.',
 development_history_reused=False,history_note='Newly acquired earlier calendar history, retrospectively chosen after2026results. Not a prospective untouched final test. Public history/unknown trials and repeated selection prevent significance claims.',
 forward_plan='Keep original113625 future plan and parameters unchanged; itsOctober2UTC start has not happened at this run. No forward results.')
plan['execution']['limitations']+=' Applied to2025 prices as a declared stress assumption; not claimed2025 historical exchange rules.'
(ROUND/'spec.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
snapshot={'ledger_sha256':sha(ledger),'lines':len(ledger.read_text().splitlines()),'records':len(records),'canonical':218,'initial16_available':all(v.get('result_available') for v in list(records.values())[:16]),'pending':[],
 'records':records,'prior_reports':{str(p.relative_to(ROOT)):sha(p) for p in sorted((ROOT/'research/experiments').glob('*/result.md'))}}
with (ROUND/'prior_summary.json.gz').open('wb') as f:
 with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as z:z.write(json.dumps(snapshot,ensure_ascii=False,separators=(',',':')).encode())
batch=[];newfp={}
for b in json.loads((OLD/'batch.json').read_text()):
 sp=json.loads((ROOT/b['spec']).read_text());name='transfer2025_'+b['name'];sp['name']=name;sp['validation_plan']=str((ROUND/'spec.json').relative_to(ROOT))
 sp['parameters'].update(start_utc=plan['oos_start_utc'],end_utc=plan['terminal_exit_utc'])
 if sp['kind']=='combination':
  for c in sp['components']:c['fingerprint']=newfp[c['fingerprint']]
 else:sp['parameters']['execution']=plan['execution']
 p=ROUND/'specs'/f'{name}.json';p.parent.mkdir(exist_ok=True);p.write_text(json.dumps(sp,ensure_ascii=False,indent=2)+'\n')
 r=subprocess.run(['python3',str(ROOT/'research/automation/registry.py'),'reserve',str(p)],cwd=ROOT,capture_output=True,text=True)
 print(name,r.returncode,r.stdout.strip(),flush=True)
 if r.returncode:raise RuntimeError('Do not evaluate: '+r.stdout+r.stderr)
 fp=reg.fingerprint(sp);newfp[b['fingerprint']]=fp;batch.append({'name':name,'spec':str(p.relative_to(ROOT)),'fingerprint':fp,'role':b['role'],'previous_name':b['name'],'previous_fingerprint':b['fingerprint']})
assert len(batch)==30
(ROUND/'batch.json').write_text(json.dumps(batch,indent=2)+'\n')
print('PASS:30 transfer configurations reserved before new data/backtests;unchanged rule/grid/cost/gates,new2025dates')
