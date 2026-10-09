"""Read complete prior evidence and select exact funded sources without evaluating portfolios."""
from pathlib import Path
from datetime import datetime, timezone
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
assert not subprocess.check_output(['git', 'diff', '--name-only'], cwd=R, text=True).strip()
conclusions = [{'path': str(p.relative_to(R)), 'sha256': sha(p), 'text': p.read_text()}
               for p in sorted((R / 'research/experiments').glob('*/result.md')) if p.parent != T]
oos = {str(p.relative_to(R)): {'sha256': sha(p), 'text': p.read_text()}
       for p in sorted((R / 'checks').glob('*oos.py'))}
assert len(conclusions) == 78 and len(oos) == 4
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



sys.path.insert(0,str(T));from design import source_spec,AXES
components={}
for fp,v in canonical.items():
 sp=v['spec'];p=sp.get('parameters',{});asset=sp.get('universe',[''])[0].split('/')[0]
 if sp['family']=='daily-close-range-breakout' and asset in('BTC','ETH')and p.get('initial_capital_usdt')==(1500 if asset=='BTC'else 500)and p.get('entry_lookback_days')==15 and p.get('exit_lookback_days')==30 and p.get('start_utc','')[:4]in('2025','2026')and p.get('end_utc','').endswith('-09-14T00:01:00Z'):
  rp=R/v['report'];assert v['result_available']and sha(rp)==v['report_sha256'];row=next(c for c in json.loads(rp.read_text())['configs'].values()if c['fingerprint']==fp);components[p['start_utc'][:4],asset]=(fp,sp,row)
assert len(components)==4
fixed={}
for fp,v in canonical.items():
 sp=v['spec'];p=sp.get('parameters',{})
 if sp['family']=='daily-close-range-relative-quote-volume' and sp.get('universe')==['BTC/USDT'] and p.get('initial_capital_usdt')==1500 and p.get('volume_lookback_days')==30 and p.get('minimum_volume_ratio')==1 and p.get('entry_lookback_days')==15 and p.get('exit_lookback_days')==30 and p.get('start_utc','')[:4]in('2025','2026') and p.get('end_utc','').endswith('-09-14T00:01:00Z'):
  assert v['result_available'];fixed[p['start_utc'][:4]]=fp
assert len(fixed)==2
novelty={k:[]for k in('new_component_coordinates','reused_component_coordinates','new_grid_coordinates','reused_grid_coordinates','equivalent_parent_collisions')};equivalent={}
for fp,v in canonical.items():
 if v['spec']['kind']=='combination':equivalent.setdefault(tuple(sorted((c['fingerprint'],str(c['weight']))for c in v['spec']['components'])),[]).append(fp)
template=json.loads((R/'research/experiments/20261009T091020Z/specs/volratio_channel_2026_n30_r1_btc0.75.json').read_text())
for year in('2025','2026'):
 for n in AXES['volume_lookback_days']:
  for ratio in AXES['minimum_volume_ratio']:
   sp=source_spec(components[year,'ETH'][1],n,ratio);fp=registry.fingerprint(sp);known=fp in canonical
   if known:assert n==20 and ratio in (.75,1) and canonical[fp]['result_available'] and sha(R/canonical[fp]['report'])==canonical[fp]['report_sha256']
   novelty['reused_component_coordinates'if known else'new_component_coordinates'].append([year,n,ratio,fp]);co=copy.deepcopy(template)
   co['parameters']['start_utc']=sp['parameters']['start_utc'];co['parameters']['end_utc']=sp['parameters']['end_utc'];co['components']=[{'fingerprint':fixed[year],'weight':.75},{'fingerprint':fp,'weight':.25}];parent=registry.fingerprint(co);known=parent in canonical
   if known:assert n==20 and ratio in (.75,1) and canonical[parent]['result_available'] and sha(R/canonical[parent]['report'])==canonical[parent]['report_sha256']
   novelty['reused_grid_coordinates'if known else'new_grid_coordinates'].append([year,n,ratio,parent]);same=equivalent.get(tuple(sorted((c['fingerprint'],str(c['weight']))for c in co['components'])),[])
   if not known and same:novelty['equivalent_parent_collisions'].append(same)
assert len(novelty['new_component_coordinates'])==len(novelty['new_grid_coordinates'])==14 and len(novelty['reused_component_coordinates'])==len(novelty['reused_grid_coordinates'])==4 and not novelty['equivalent_parent_collisions']
skill_paths=[R/'.agents/skills'/s/'SKILL.md'for s in('walk-forward-validation','ml4t-sensitivity-analysis','ml4t-transaction-costs')]
summary={'base_head':head,'canonical':len(canonical),'preserved_ids':len(records),'lines':len(rows),'ledger_sha256':sha(L),'records':records,'conclusions':conclusions,'oos_checks':oos,'freqtrade_results':freqtrade,'initial16_actual_evidence_complete':True,'pending_reservations':[],'paper10_plan_sha256':sha(R/'research/paper10/plan.json'),'paper10_state_sha256':sha(R/'research/paper10/state.json'),'novelty_preflight':novelty,'read_task_sha256':sha(R/'research/automation/task.md'),'read_task_text':(R/'research/automation/task.md').read_text(),'read_automation_README':{'sha256':sha(R/'research/automation/README.md'),'text':(R/'research/automation/README.md').read_text()},'read_monitor_README':{'sha256':sha(R/'research/monitor/README.md'),'text':(R/'research/monitor/README.md').read_text()},'skills':{str(p.relative_to(R)):{'sha256':sha(p),'text':p.read_text()}for p in skill_paths}}
with(T/'prior_summary.json.gz').open('wb')as f:
 with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0)as z:z.write(json.dumps(summary,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
notes={'before_new_calculation':True,'new_results_computed':0,'direction':'RefineETHclose-channel15/30 turnover entry gate with preceding15/20/25day mean and minimum ratio0.75/0.875/1;BTC existingvolume30/r1 exact1500USDT fixed,ETH500USDT;raw75/25 initialfunds. Centre/focusETH20/r0.875. PriorETH20/r1 improved2025 returns but worsened2026;old20/r0.75 matched reference paths. Test an intermediate gate without choosing new outcomes. ExactoldETH20/r0.75 and20/r1 and their portfolios acrossbothyears remain read-only (8old definitions),14newETH+14newportfolios/84cost scenes. Full9cell grids peryear,all source parameters/rules/costs remain fixed before reserve. No new NAV before reservations.','initial16_selection':'Original first16 ledger rows/aliases actual evidence complete;no missing initial16.','legacy_shadow':'AppendOct9UTC17:00 to19:00 closed minute marks only,nextdailyOct10UTC00:01;paper10 observation25 unchanged.','old_gate_policy':'Never overwrite existingETH20/r0.75 or20/r1 criteria/status with new-neighbourhood statistics.'}
(T/'preflight_notes.json').write_text(json.dumps(notes,indent=2)+'\n');print(json.dumps({k:v for k,v in summary.items()if k in('base_head','canonical','preserved_ids','lines','initial16_actual_evidence_complete','pending_reservations')}))
