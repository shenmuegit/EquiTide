"""Read complete prior evidence and select exact funded sources without evaluating portfolios."""
from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal as D
import copy, gzip, hashlib, json, subprocess, sys, zipfile
T = Path(__file__).resolve().parent
R = T.parents[2]
sys.path.insert(0, str(R / 'research/automation'))
import registry
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
L = R / 'research/automation/registry.jsonl'
raw = L.read_bytes()
rows = [json.loads(x) for x in raw.splitlines()]
records = registry.read_records(L)
canonical = {registry.fingerprint(v['spec']): v for v in records.values()}
assert not [v for v in records.values() if v.get('status') == 'reserved']
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=R, text=True).strip()
assert head == subprocess.check_output(['git', 'rev-parse', 'origin/codex/strategy-research'], cwd=R, text=True).strip()
assert not subprocess.check_output(['git','diff','--name-only'],cwd=R,text=True).strip()
conclusions = [{'path': str(p.relative_to(R)), 'sha256': sha(p), 'text': p.read_text()}
               for p in sorted((R / 'research/experiments').glob('*/result.md')) if p.parent != T]
oos = {str(p.relative_to(R)): {'sha256': sha(p), 'text': p.read_text()}
       for p in sorted((R / 'checks').glob('*oos.py'))}
assert len(conclusions)==sum(1 for p in (R/"research/experiments").glob("*/result.md") if p.parent!=T) and len(oos)==4
freqtrade = []
for p in sorted((R / 'freqtrade_trial/results').iterdir()):
    if not p.is_file():
        continue
    blob = p.read_bytes()
    members = []
    if p.suffix == '.zip':
        with zipfile.ZipFile(p) as z:
            for name in z.namelist():
                b = z.read(name)
                members.append({'name': name, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()})
                if name.endswith('.json'):
                    json.loads(b)
    elif p.suffix == '.json':
        json.loads(blob)
    else:
        blob.decode('utf-8')
    freqtrade.append({'path': str(p.relative_to(R)), 'bytes': len(blob), 'sha256': sha(p), 'members': members})
assert len(freqtrade) == 7

# The original sixteen are the FIRST ledger rows, never the lexically first dictionary keys.
initial = []
for position, row in enumerate(rows[:16], 1):
    fp = row['fingerprint']
    v = records[fp]
    evidence = copy.deepcopy(v.get('result_evidence') or [])
    if not evidence and v.get('report'):
        evidence = [{'path': v['report'], 'sha256': v['report_sha256'], 'type': 'actual_report_pointer'}]
    assert v.get('result_available') and evidence, fp
    for ev in evidence:
        p = R / ev['path']
        assert sha(p) == ev['sha256']
        if ev['type'] == 'actual_report_pointer':
            doc = json.loads(p.read_text())
            assert fp in json.dumps(doc) or registry.fingerprint(v['spec']) in json.dumps(doc), fp
            for recovery in doc.get('legacy_recovery', []):
                if recovery['fingerprint'] == fp:
                    assert recovery['actual_backtest_available'] and recovery['concrete_children']
    initial.append({'original_ledger_position': position, 'fingerprint': fp, 'canonical_fingerprint': registry.fingerprint(v['spec']),
                    'family': row['spec']['family'], 'status': v['status'], 'evidence': evidence})
assert len({x['fingerprint'] for x in initial}) == 16
audit = {'selection': 'Original raw ledger rows 1 through 16 in recorded order.',
         'checked_at_utc': datetime.now(timezone.utc).isoformat(),
         'initial16_actual_results_checked': initial, 'missing_initial16': [],
         'scope': 'Actual evidence exists; legacy short carry cases and old walk-forward reports do not imply current long-run qualification.'}
(T / 'prior_evidence_audit.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n')



assert len(rows)==len(raw.splitlines()) and not[v for v in records.values()if v.get('status')=='reserved']
sys.path.insert(0,str(T));from design import definitions,AXES
fresh=[];old=[]
for sp,fields in definitions(registry.fingerprint):
 fp=registry.fingerprint(sp);(old if fp in canonical else fresh).append({'fingerprint':fp,**fields})
 if fp in canonical:assert canonical[fp]['result_available']
assert len(fresh)==28 and len(old)==14 and sum(x['role']=='component'for x in fresh)==16 and sum(x.get('asset')=='BTC'for x in fresh)==4 and sum(x.get('asset')=='ETH'for x in fresh)==12 and sum(x['role']=='combination'for x in fresh)==12
assert all(sum(D(str(q['weight'])) for q in sp.get('components',[]))==D(1) for sp,b in definitions(registry.fingerprint) if sp['kind']=='combination')
paper=json.loads((R/'research/paper10/state.json').read_text());assert paper['observations']==51 and paper['last_observation_id']=='20261012T002852636046Z'
P=R/'research/paper10/observations'/paper['last_observation_id'];pp=json.loads((P/'preflight.json').read_text());paths={R/p for p in pp['protected_sha256']}
for path,h in pp['protected_sha256'].items():assert sha(R/path)==h,path
for root in(P,R/'research/experiments/20261011T215357Z'):
 paths.update(p for p in root.rglob('*')if p.is_file()and'__pycache__'not in p.parts)
paths.add(R/'research/paper10/state.json')
summary={'base_head':head,'base_tree':subprocess.check_output(['git','rev-parse','HEAD^{tree}'],cwd=R,text=True).strip(),'canonical':len(canonical),'preserved_ids':len(records),'lines':len(rows),'ledger_sha256':sha(L),'records':records,'conclusions':conclusions,'oos_checks':oos,'freqtrade_results':freqtrade,'initial16_actual_evidence_complete':True,'pending_reservations':[],'paper10_plan_sha256':sha(R/'research/paper10/plan.json'),'paper10_state_sha256':sha(R/'research/paper10/state.json'),'paper_observation':paper['last_observation_id'],'paper_observations':51,'protected_sha256':{str(p.relative_to(R)):sha(p)for p in sorted(paths)},'monitor_counts_before':json.loads((R/'research/monitor/latest.json').read_text())['research']['counts'],'novelty_preflight':{'new':fresh,'old':old},'read_task_sha256':sha(R/'research/automation/task.md'),'read_task_text':(R/'research/automation/task.md').read_text(),'read_automation_README':{'sha256':sha(R/'research/automation/README.md'),'text':(R/'research/automation/README.md').read_text()},'read_monitor_README':{'sha256':sha(R/'research/monitor/README.md'),'text':(R/'research/monitor/README.md').read_text()},'skills':{str((R/'.agents/skills'/n/'SKILL.md').relative_to(R)):{'sha256':sha(R/'.agents/skills'/n/'SKILL.md'),'text':(R/'.agents/skills'/n/'SKILL.md').read_text()}for n in('walk-forward-validation','ml4t-sensitivity-analysis','ml4t-transaction-costs')}}
with(T/'prior_summary.json.gz').open('wb')as f:
 with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0)as z:z.write(json.dumps(summary,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
notes={'before_new_calculation':True,'new_results_computed':0,'direction':'R45EMA40/45/50allnineparentsqualifiedacrossbothhistories,butnojointreturn/drawdowngainagainst35;R44period20/25failedfoldgates. PredeclarelocalETH EMA32/34/36 x entry0.01/0.0125/0.015,exit0.005fixed,focus34/0.0125. Testwhether35ispartofalocalqualifiedplateauorasharpregimeboundary;noassumedgain. Matchedsameentry/exitETH35R44andETH40R45parentsareseparateread-onlyperiodcontrols. BTCEMA15e0.01/x0.03/channel15/30/disjointvolume40r1.1andraw55/45own1100/900unchanged.18newETHown900+18parents;exactoldBTC1100NAVreused.Eightgatesunchanged,noadaptiveOOSgrid/noindependentfinaltestclaim;multipletrialselectionandrepeatedhistoriesdisclosed,paperaccountsuntouched.','initial16_selection':'Original16actualevidencecomplete;none missing.','legacy_shadow':'Append120closedmarks21:00to23:00UTC,preserve14230oldNAVpoints,14339minutes/14350points,nextdailyOct12UTC00:01.No newdailydecision/reference/fill;oldfloatcash/units/desired/trades/costs retained. Paper50,two oldgaps and96.459783percentcount/time-gapcoverageproxy unchanged.','monitor_source_unchanged':True}
(T/'preflight_notes.json').write_text(json.dumps(notes,indent=2)+'\n')
print(json.dumps({'base':head,'registry_rows':len(rows),'canonical':len(canonical),'conclusions_read':len(conclusions),'initial16_missing':0,'new_histories':len(fresh),'new_components':16,'old_configs':len(old),'protected_files':len(paths)}))
