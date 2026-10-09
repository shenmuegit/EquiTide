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
assert len(conclusions) == 73 and len(oos) == 4
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
 if sp['family']=='daily-close-range-breakout' and asset in ('BTC','ETH') and p.get('initial_capital_usdt')==(1500 if asset=='BTC' else 500) and p.get('entry_lookback_days')==15 and p.get('exit_lookback_days')==30 and p.get('start_utc','')[:4] in ('2025','2026') and p.get('end_utc','').endswith('-09-14T00:01:00Z'):
  rp=R/v['report'];assert v['result_available'] and sha(rp)==v['report_sha256'];row=next(c for c in json.loads(rp.read_text())['configs'].values() if c['fingerprint']==fp);components[p['start_utc'][:4],asset]=(fp,sp,row)
assert len(components)==4
novelty={'new_component_coordinates':[],'new_grid_coordinates':[],'equivalent_parent_collisions':[]};equivalent={}
for fp,v in canonical.items():
 if v['spec']['kind']=='combination':equivalent.setdefault(tuple(sorted((c['fingerprint'],str(c['weight']))for c in v['spec']['components'])),[]).append(fp)
template=json.loads((R/'research/experiments/20261002T174933Z/specs/channel_2026_combo_e15_x30_btc0.75.json').read_text())
for year in ('2025','2026'):
 for n in AXES['volume_lookback_days']:
  for ratio in AXES['minimum_volume_ratio']:
   sp=source_spec(components[year,'BTC'][1],n,ratio);fp=registry.fingerprint(sp);assert fp not in canonical;novelty['new_component_coordinates'].append([year,n,ratio,fp])
   co=copy.deepcopy(template);co['parameters']['start_utc']=sp['parameters']['start_utc'];co['parameters']['end_utc']=sp['parameters']['end_utc'];co['components']=[{'fingerprint':fp,'weight':.75},{'fingerprint':components[year,'ETH'][0],'weight':.25}];parent=registry.fingerprint(co);assert parent not in canonical;novelty['new_grid_coordinates'].append([year,n,ratio,parent]);same=equivalent.get(tuple(sorted((c['fingerprint'],str(c['weight']))for c in co['components'])),[])
   if same:novelty['equivalent_parent_collisions'].append(same)
assert len(novelty['new_component_coordinates'])==len(novelty['new_grid_coordinates'])==18 and not novelty['equivalent_parent_collisions']
skill_paths=[R/'.agents/skills'/s/'SKILL.md' for s in ('walk-forward-validation','ml4t-sensitivity-analysis','ml4t-transaction-costs')]
summary={'base_head':head,'canonical':len(canonical),'preserved_ids':len(records),'lines':len(rows),'ledger_sha256':sha(L),'records':records,'conclusions':conclusions,'oos_checks':oos,'freqtrade_results':freqtrade,'initial16_actual_evidence_complete':True,'pending_reservations':[],'paper10_plan_sha256':sha(R/'research/paper10/plan.json'),'paper10_state_sha256':sha(R/'research/paper10/state.json'),'novelty_preflight':novelty,'read_task_sha256':sha(R/'research/automation/task.md'),'read_task_text':(R/'research/automation/task.md').read_text(),'read_automation_README':{'sha256':sha(R/'research/automation/README.md'),'text':(R/'research/automation/README.md').read_text()},'read_monitor_README':{'sha256':sha(R/'research/monitor/README.md'),'text':(R/'research/monitor/README.md').read_text()},'skills':{str(p.relative_to(R)):{'sha256':sha(p),'text':p.read_text()}for p in skill_paths}}
with (T/'prior_summary.json.gz').open('wb') as f:
 with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as z:z.write(json.dumps(summary,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
notes={'before_new_calculation':True,'new_results_computed':0,'direction':'BTC close-channel15/30 entry gated by prior-day USDT quote turnover >=0.75/1/1.25 times preceding10/20/30day mean excluding that day;exit remains unfiltered. ETH close-channel15/30 exact500USDT source reused. Raw75/25 initial1500/500 funds. Two9cell grids across2025/2026,18newBTCcomponents+18newportfolios. Focus20days/ratio1. Volume confirmation may reduce false BTC breakouts or delay/miss profitable trends;no parameter selected from current OOS outcomes. PreviousBTC annual volatility guards lost to matching unguarded controls,so test entry activity without volatility-forced exits.','initial16_selection':'First16 original ledger rows,all actual evidence checked;no missing initial historical result.','legacy_shadow':'Append Oct9UTC07:00 to09:00 completed marks only;next decisionOct10UTC00:01,freeze unchanged;paper10 observation20/state unchanged.','knowledge_source':{'url':'https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints','access_date_utc':'2026-10-09','fact':'Official kline tuple index7 is quote asset volume;UTC default. Our entry rule is a predeclared generated hypothesis,not claimed exchange/academic alpha.'}}
(T/'preflight_notes.json').write_text(json.dumps(notes,indent=2)+'\n');print(json.dumps({k:v for k,v in summary.items() if k in ('base_head','canonical','preserved_ids','lines','initial16_actual_evidence_complete','pending_reservations')}))
for c in conclusions:
 paras=[x for x in c['text'].split('\n\n')[1:]if x.strip()];print(c['path'],(paras[0]if paras else c['text'])[:300])
