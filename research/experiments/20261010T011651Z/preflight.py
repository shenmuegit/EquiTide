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
assert len(conclusions) == 81 and len(oos) == 4
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

components={};extras={}
for fp,v in canonical.items():
 sp=v['spec'];p=sp.get('parameters',{});asset=sp.get('universe',[''])[0].split('/')[0];year=p.get('start_utc','')[:4]
 if year not in('2025','2026')or not p.get('end_utc','').endswith('-09-14T00:01:00Z'):continue
 btc=asset=='BTC'and sp['family']=='daily-close-range-relative-quote-volume'and p.get('initial_capital_usdt')==1500 and p.get('entry_lookback_days')==15 and p.get('exit_lookback_days')==30 and p.get('volume_lookback_days')==30 and p.get('minimum_volume_ratio')in(.9,1,1.1)
 eth=asset=='ETH'and sp['family']=='daily-channel-ema-confirmation'and p.get('initial_capital_usdt')==500 and p.get('entry_lookback_days')==15 and p.get('exit_lookback_days')==30 and p.get('EMA_symmetric_band')==.015 and p.get('EMA_span_days')in(50,65,80)
 if btc or eth:
  rp=R/v['report'];assert v['result_available']and sha(rp)==v['report_sha256'];row=next(c for c in json.loads(rp.read_text())['configs'].values()if c['fingerprint']==fp)
  components[year,asset,p['minimum_volume_ratio']if btc else p['EMA_span_days']]=(fp,sp,row)
 if asset=='ETH'and p.get('initial_capital_usdt')==500:
  if sp['family']=='daily-close-range-breakout'and p.get('entry_lookback_days')==15 and p.get('exit_lookback_days')==30:extras[year,'channel']=fp
  if sp['family']=='daily-ema-hysteresis'and p.get('span_days')in(50,65,80)and p.get('symmetric_band_fraction')==.015:extras[year,p['span_days']]=fp
assert len(components)==12 and len(extras)==8
base_spec=json.loads((R/'research/experiments/20261009T191550Z/specs/dualvol_channel_2026_btcN30r1_ethN20_r0.875_btc0.75.json').read_text())
equivalent={}
for fp,v in canonical.items():
 sp=v['spec']
 if sp['kind']=='combination':equivalent.setdefault(tuple(sorted((c['fingerprint'],str(c['weight']))for c in sp['components'])),[]).append(fp)
novelty={'new_grid_coordinates':[],'read_only_coordinates':[],'equivalent_parent_collisions':[]}
for year in('2025','2026'):
 for ratio in(.9,1,1.1):
  for span in(50,65,80):
   sp=copy.deepcopy(base_spec);sp['parameters']['start_utc']=components[year,'BTC',ratio][1]['parameters']['start_utc'];sp['parameters']['end_utc']=components[year,'BTC',ratio][1]['parameters']['end_utc'];sp['components']=[{'fingerprint':components[year,'BTC',ratio][0],'weight':.75},{'fingerprint':components[year,'ETH',span][0],'weight':.25}]
   fp=registry.fingerprint(sp);key='read_only_coordinates'if fp in canonical else'new_grid_coordinates';novelty[key].append([year,ratio,span,fp]);same=equivalent.get(tuple(sorted((c['fingerprint'],str(c['weight']))for c in sp['components'])),[])
   if fp not in canonical and same:novelty['equivalent_parent_collisions'].append({'coordinates':[year,ratio,span],'existing':same})
assert len(novelty['new_grid_coordinates'])==18 and not novelty['read_only_coordinates']and not novelty['equivalent_parent_collisions']
def component_ref(fp):
 rec=canonical[fp];rp=R/rec['report'];assert rec['result_available']and sha(rp)==rec['report_sha256'];row=next(c for c in json.loads(rp.read_text())['configs'].values()if c['fingerprint']==fp)
 assert sha(R/row['archive'])==row['archive_sha256'];return {'name':row['name'],'fingerprint':fp,'report':rec['report'],'report_sha256':rec['report_sha256'],'archive':row['archive'],'archive_sha256':row['archive_sha256'],'spec':row['spec'],'spec_sha256':sha(R/row['spec']),'source_round':Path(row['archive']).parts[2]}
def parent_ref(btc,eth):
 matches=equivalent.get(tuple(sorted(((btc,str(.75)),(eth,str(.25))))),[]);assert matches
 valid=[fp for fp in matches if canonical[fp]['spec']['parameters']['initial_capital_usdt']==2000];assert len(valid)==1
 return component_ref(valid[0])
comparators=[]
for year in('2025','2026'):
 for ratio in(.9,1,1.1):comparators.append({**parent_ref(components[year,'BTC',ratio][0],extras[year,'channel']),'year':year,'kind':'MATCHED_BTC_VOLUME_PURE_ETH_CHANNEL','BTC_minimum_volume_ratio':ratio})
 for span in(50,65,80):comparators.append({**parent_ref(components[year,'BTC',1][0],extras[year,span]),'year':year,'kind':'BTC_R1_PURE_ETH_EMA_SAME_SPAN','ETH_EMA_span_days':span})
signatures={year+'_'+asset:len({tuple(components[year,asset,x][2]['scenes'][str(k)]['NAV_sha256_f64le']for k in(1,2,3))for x in values})for year in('2025','2026')for asset,values in [('BTC',(.9,1,1.1)),('ETH',(50,65,80))]}
skill_paths=[R/'.agents/skills'/s/'SKILL.md'for s in('walk-forward-validation','ml4t-sensitivity-analysis','ml4t-transaction-costs')]
summary={'base_head':head,'canonical':len(canonical),'preserved_ids':len(records),'lines':len(rows),'ledger_sha256':sha(L),'records':records,'conclusions':conclusions,'oos_checks':oos,'freqtrade_results':freqtrade,'initial16_actual_evidence_complete':True,'pending_reservations':[],'paper10_plan_sha256':sha(R/'research/paper10/plan.json'),'paper10_state_sha256':sha(R/'research/paper10/state.json'),'monitor_counts_before':json.loads((R/'research/monitor/latest.json').read_text())['research']['counts'],'novelty_preflight':novelty,'existing_component_path_signature_counts':signatures,'matched_comparator_refs':comparators,'read_task_sha256':sha(R/'research/automation/task.md'),'read_task_text':(R/'research/automation/task.md').read_text(),'read_automation_README':{'sha256':sha(R/'research/automation/README.md'),'text':(R/'research/automation/README.md').read_text()},'read_monitor_README':{'sha256':sha(R/'research/monitor/README.md'),'text':(R/'research/monitor/README.md').read_text()},'skills':{str(p.relative_to(R)):{'sha256':sha(p),'text':p.read_text()}for p in skill_paths}}
with(T/'prior_summary.json.gz').open('wb')as f:
 with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0)as z:z.write(json.dumps(summary,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
notes={'before_new_calculation':True,'new_results_computed':0,'direction':'BTCclosechannel15/30 with preceding30day USDTturnover entry ratio0.9/1/1.1 crossed with ETHclosechannel15/30 jointly confirmed by EMA50/65/80 symmetric1.5percent. Raw75/25 initial1500/500USDT. Full3x3 per2025/2026,18genuinely newannualparents/54costscenes. All12funded components and12matched oldparentcontrols read-only;no oldsignals/trades reevaluated. Predeterminedfocus BTCratio1/ETHEMA65. Hypothesis: different activity/trend confirmations across assets may lower drawdown without surrendering too much growth;report alltradeoffs vs sameBTC pureETHchannel and BTC1 pureETHEMA controls. NoOOS retuning,capital scaling or fixedpaper replacement.','initial16_selection':'Original first16rawledgerrows/aliases all have actual evidence;none to backfill.','legacy_shadow':'Resume originalSMA65/band1percent75/25 atOct9UTC23:00 throughOct10UTC01:00;process exactlyOct10UTC00:01 originaldaily decision from65closed dailybars and append120minute marks+1reference. Laterretrieval isdelayedshadow reconstruction,never paper10 actualquotes. Preserve prior11468points/cash/units/costs/trades. Paper10observation28 stays untouched.'}
(T/'preflight_notes.json').write_text(json.dumps(notes,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items()if k in('base_head','canonical','preserved_ids','lines','initial16_actual_evidence_complete','existing_component_path_signature_counts')}))
