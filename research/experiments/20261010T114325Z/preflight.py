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
assert len(conclusions) == 84 and len(oos) == 4
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

assert len(rows)==6395 and len(records)==3150 and len(canonical)==3148
sys.path.insert(0,str(T));from design import source_spec,AXES
fixed={};templates={};pure={};equivalent={}
for fp,v in canonical.items():
 sp=v['spec'];p=sp.get('parameters',{});year=p.get('start_utc','')[:4]
 if sp['kind']=='combination':equivalent.setdefault(tuple(sorted((c['fingerprint'],str(c['weight']))for c in sp['components'])),[]).append(fp)
 if year not in ('2025','2026')or not p.get('end_utc','').endswith('-09-14T00:01:00Z'):continue
 if sp.get('universe')==['BTC/USDT'] and sp['family']=='daily-close-range-relative-quote-volume' and p.get('initial_capital_usdt')==1500 and (p.get('entry_lookback_days'),p.get('exit_lookback_days'),p.get('volume_lookback_days'),p.get('minimum_volume_ratio'))==(15,30,30,1):fixed[year]=(fp,v)
 if sp.get('universe')==['ETH/USDT']and p.get('initial_capital_usdt')==500 and(p.get('entry_lookback_days'),p.get('exit_lookback_days'))==(15,30):
  if sp['family']=='daily-channel-ema-confirmation'and(p.get('EMA_span_days'),p.get('EMA_symmetric_band'))==(50,.015):templates[year]=(fp,v)
  if sp['family']=='daily-close-range-breakout':pure[year]=(fp,v)
assert len(fixed)==len(templates)==len(pure)==2
parent_template=json.loads((R/'research/experiments/20261010T011651Z/specs/vol_filter_2026_btcN30r1_ethEma50_btc0.75.json').read_text())
novelty={'new_components':[],'old_components':[],'new_parents':[],'old_parents':[],'equivalent_parent_collisions':[]}
for year in ('2025','2026'):
 for span in AXES['EMA_span_days']:
  for band in AXES['EMA_symmetric_band']:
   cs=source_spec(templates[year][1]['spec'],span,band);cfp=registry.fingerprint(cs);novelty['old_components'if cfp in canonical else'new_components'].append([year,span,band,cfp])
   sp=copy.deepcopy(parent_template);sp['parameters']['start_utc']=cs['parameters']['start_utc'];sp['parameters']['end_utc']=cs['parameters']['end_utc'];sp['components']=[{'fingerprint':fixed[year][0],'weight':.75},{'fingerprint':cfp,'weight':.25}];fp=registry.fingerprint(sp)
   novelty['old_parents'if fp in canonical else'new_parents'].append([year,span,band,fp])
   eq=equivalent.get(tuple(sorted((c['fingerprint'],str(c['weight']))for c in sp['components'])),[])
   if fp not in canonical and eq:novelty['equivalent_parent_collisions'].append([year,span,band,eq])
assert (len(novelty['new_components']),len(novelty['old_components']),len(novelty['new_parents']),len(novelty['old_parents']))==(12,6,12,6)and not novelty['equivalent_parent_collisions']
def parent_ref(year):
 key=tuple(sorted(((fixed[year][0],str(.75)),(pure[year][0],str(.25)))))
 fps=[fp for fp in equivalent[key]if canonical[fp]['spec']['parameters']['initial_capital_usdt']==2000];assert len(fps)==1
 fp=fps[0];rec=canonical[fp];rp=R/rec['report'];assert rec['result_available']and sha(rp)==rec['report_sha256'];c=next(c for c in json.loads(rp.read_text())['configs'].values()if c['fingerprint']==fp)
 assert sha(R/c['archive'])==c['archive_sha256'];return {'year':year,'kind':'MATCHED_BTC_VOLUME_PURE_ETH_CHANNEL','name':c['name'],'fingerprint':fp,'report':rec['report'],'report_sha256':rec['report_sha256'],'archive':c['archive'],'archive_sha256':c['archive_sha256'],'spec':c['spec'],'spec_sha256':sha(R/c['spec']),'source_round':Path(c['archive']).parts[2]}
skill_paths=[R/'.agents/skills'/s/'SKILL.md'for s in('walk-forward-validation','ml4t-sensitivity-analysis','ml4t-transaction-costs')]
paper=json.loads((R/'research/paper10/state.json').read_text());assert paper['observations']==32 and paper['last_observation_id']=='20261010T113144508501Z'
P=R/'research/paper10/observations'/paper['last_observation_id'];pp=json.loads((P/'preflight.json').read_text());protected={**pp['protected_sha256'],**{str(p.relative_to(R)):sha(p)for p in P.rglob('*')if p.is_file()and'__pycache__'not in p.parts},'research/paper10/state.json':sha(R/'research/paper10/state.json')}
summary={'base_head':head,'base_tree':subprocess.check_output(['git','rev-parse','HEAD^{tree}'],cwd=R,text=True).strip(),'canonical':len(canonical),'preserved_ids':len(records),'lines':len(rows),'ledger_sha256':sha(L),'records':records,'conclusions':conclusions,'oos_checks':oos,'freqtrade_results':freqtrade,'initial16_actual_evidence_complete':True,'pending_reservations':[],'paper10_plan_sha256':sha(R/'research/paper10/plan.json'),'paper10_state_sha256':sha(R/'research/paper10/state.json'),'paper_observation':paper['last_observation_id'],'paper_observations':32,'protected_sha256':protected,'monitor_counts_before':json.loads((R/'research/monitor/latest.json').read_text())['research']['counts'],'novelty_preflight':novelty,'matched_comparator_refs':[parent_ref(y)for y in('2025','2026')],'read_task_sha256':sha(R/'research/automation/task.md'),'read_task_text':(R/'research/automation/task.md').read_text(),'read_automation_README':{'sha256':sha(R/'research/automation/README.md'),'text':(R/'research/automation/README.md').read_text()},'read_monitor_README':{'sha256':sha(R/'research/monitor/README.md'),'text':(R/'research/monitor/README.md').read_text()},'skills':{str(p.relative_to(R)):{'sha256':sha(p),'text':p.read_text()}for p in skill_paths}}
with(T/'prior_summary.json.gz').open('wb')as f:
 with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0)as z:z.write(json.dumps(summary,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
notes={'before_new_calculation':True,'new_results_computed':0,'direction':'After prior25day EMA lost2025 fold/risk consistency while35day kept a plateau,predeclare localETH30/35/40 x symmetric1/1.25/1.5percent around35/1.25percent oldcenter. Newfocus30/1.25percent;all old35day cells read-only. BTCfixed15/30closechannel pluspreceding30dayUSDTturnover ratio1,raw75/25initial1500/500USDT.12newETH+12newparents/72scenes;12oldgrid definitions plus2BTCsources/42scenes read-only. Smaller EMA-speed perturbation may improve2026without the2025 cliff;measure every cell,negative fold,and matched/oldcenter tradeoff.No OOS optimization or paper replacement.','initial16_selection':'First16 raw ledger records/aliases have actual evidence;none missing.','legacy_shadow':'Continue originalSMA65/1percent75/25 from07:00 to11:00UTC with240closedminute marks;11949oldNAVpoints and unchanged positions/trades/costs. NextdailyOct11UTC00:01. Laterretrieval is delayedshadow,not paper10 actualquotes. Paper32 and its two gaps/94.556949percent coverage risk preserved.'}
(T/'preflight_notes.json').write_text(json.dumps(notes,indent=2)+'\n')
print(json.dumps({'base':head,'registry_rows':len(rows),'canonical':len(canonical),'conclusions_read':len(conclusions),'initial16_missing':0,'new_historical_configs':24,'old_grid_configs':12,'protected_files':len(protected)}))
