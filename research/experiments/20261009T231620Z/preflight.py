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
assert len(conclusions) == 80 and len(oos) == 4
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

components = {}
for fp,v in canonical.items():
    sp=v['spec'];p=sp.get('parameters',{});asset=sp.get('universe',[''])[0].split('/')[0]
    filtered=asset=='BTC' and sp['family']=='daily-close-range-relative-quote-volume' and p.get('initial_capital_usdt')==1500 and p.get('entry_lookback_days')==15 and p.get('exit_lookback_days')==30 and p.get('volume_lookback_days')==30 and p.get('minimum_volume_ratio') in (.9,1,1.1)
    asymmetric=asset=='ETH' and sp['family']=='daily-close-range-relative-quote-volume' and p.get('initial_capital_usdt')==500 and p.get('entry_lookback_days')==15 and p.get('exit_lookback_days')==30 and p.get('volume_lookback_days')==20 and p.get('minimum_volume_ratio') in (.75,.875,1)
    if (filtered or asymmetric) and p.get('start_utc','')[:4] in ('2025','2026') and p.get('end_utc','').endswith('-09-14T00:01:00Z'):
        rp=R/v['report'];assert sha(rp)==v['report_sha256'] and v['result_available']
        row=next(c for c in json.loads(rp.read_text())['configs'].values() if c['fingerprint']==fp)
        axis=p['minimum_volume_ratio']
        components[p['start_utc'][:4],asset,axis]=(fp,sp,row)
assert len(components)==12
base_spec=json.loads((R/'research/experiments/20261009T191550Z/specs/dualvol_channel_2026_btcN30r1_ethN20_r0.875_btc0.75.json').read_text())
novelty={'new_grid_coordinates':[],'read_only_coordinates':[],'equivalent_parent_collisions':[]};equivalent={}
for fp,v in canonical.items():
    sp=v['spec']
    if sp['kind']=='combination':equivalent.setdefault(tuple(sorted((c['fingerprint'],str(c['weight'])) for c in sp['components'])),[]).append(fp)
for year in ('2025','2026'):
    for span in (.9,1,1.1):
        for entry in (.75,.875,1):
            sp=copy.deepcopy(base_spec);sp['parameters']['start_utc']=components[year,'BTC',span][1]['parameters']['start_utc'];sp['parameters']['end_utc']=components[year,'BTC',span][1]['parameters']['end_utc']
            sp['components']=[{'fingerprint':components[year,'BTC',span][0],'weight':.75},{'fingerprint':components[year,'ETH',entry][0],'weight':.25}]
            fp=registry.fingerprint(sp);key='read_only_coordinates' if fp in canonical else 'new_grid_coordinates';novelty[key].append([year,span,entry,fp])
            same=equivalent.get(tuple(sorted((c['fingerprint'],str(c['weight'])) for c in sp['components'])),[])
            if fp not in canonical and same:novelty['equivalent_parent_collisions'].append({'coordinates':[year,span,entry],'existing':same})
assert len(novelty['new_grid_coordinates'])==12 and len(novelty['read_only_coordinates'])==6 and not novelty['equivalent_parent_collisions']
signatures={}
for year in ('2025','2026'):
    for asset,values in [('BTC',(.9,1,1.1)),('ETH',(.75,.875,1))]:
        signatures[year+'_'+asset]=len({tuple(components[year,asset,x][2]['scenes'][str(k)]['NAV_sha256_f64le'] for k in (1,2,3)) for x in values})
skill_paths = [R / '.agents/skills' / s / 'SKILL.md' for s in ('walk-forward-validation', 'ml4t-sensitivity-analysis', 'ml4t-transaction-costs')]
summary = {'base_head': head, 'canonical': len(canonical), 'preserved_ids': len(records), 'lines': len(rows),
           'ledger_sha256': sha(L), 'records': records, 'conclusions': conclusions, 'oos_checks': oos,
           'freqtrade_results': freqtrade, 'initial16_actual_evidence_complete': True, 'pending_reservations': [],
           'paper10_plan_sha256': sha(R / 'research/paper10/plan.json'), 'paper10_state_sha256': sha(R / 'research/paper10/state.json'),
           'monitor_counts_before': json.loads((R/'research/monitor/latest.json').read_text())['research']['counts'],
           'novelty_preflight': novelty, 'existing_component_path_signature_counts': signatures,
           'read_task_sha256': sha(R / 'research/automation/task.md'),
           'read_task_text': (R / 'research/automation/task.md').read_text(),
           'read_automation_README': {'sha256': sha(R / 'research/automation/README.md'), 'text': (R / 'research/automation/README.md').read_text()},
           'read_monitor_README': {'sha256': sha(R / 'research/monitor/README.md'), 'text': (R / 'research/monitor/README.md').read_text()},
           'skills': {str(p.relative_to(R)): {'sha256': sha(p), 'text': p.read_text()} for p in skill_paths}}
with (T / 'prior_summary.json.gz').open('wb') as f:
    with gzip.GzipFile(filename='', mode='wb', fileobj=f, mtime=0) as z:
        z.write(json.dumps(summary, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())
notes={'before_new_calculation':True,'new_results_computed':0,'direction':'Cross BTC entry-turnover ratios0.9/1/1.1 using fixed30day mean with ETHratios0.75/0.875/1 using fixed20day mean,bothclosechannels15/30. Original75/25 initial1500/500USDT. Full3x3 per2025/2026;12exact-funded components and6exact BTCratio1-row annualparents read-only. Twelve new annualparents/36costscenes. Centre/focusBTCratio1/ETH0.875 is prior candidate and never retested. Test whether independent two-asset entry-turnover thresholds preserve its return/risk or reveal a parameter cliff;no source signal/trade reevaluation and no newNAV/return before reserve.','initial16_selection':'Original first16 rows/aliases actual evidence complete;no missing initial16 to retest.','legacy_shadow':'AppendOct9UTC21:00 to23:00 closed minute marks only,nextdailyOct10UTC00:01. Fixedpaper10 observation27 remains unchanged.'}
(T/'preflight_notes.json').write_text(json.dumps(notes,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items()if k in('base_head','canonical','preserved_ids','lines','initial16_actual_evidence_complete','pending_reservations','existing_component_path_signature_counts')}))
