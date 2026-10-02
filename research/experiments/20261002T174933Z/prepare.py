"""Freeze channel boundary extension;reuse exact prior20/30 definitions without reserving again."""
import copy,gzip,hashlib,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ledger=ROOT/'research/automation/registry.jsonl';records=registry.read_records(ledger);canonical={registry.fingerprint(v['spec']) for v in records.values()}
assert len(canonical)==644 and all(v.get('result_available') and v['status']!='reserved' for v in records.values())
source=ROOT/'research/experiments/20261002T154903Z';base=json.loads((source/'spec.json').read_text());old=json.loads((source/'report.json').read_text());oldbatch=json.loads((source/'batch.json').read_text())
plan=copy.deepcopy(base)
plan.update(round=ROUND.name,trigger_utc='2026-10-02T17:49:33.356Z',actual_first_tool_utc='2026-10-02T17:49:48Z',frozen_at_utc=datetime.now(timezone.utc).isoformat(),
 hypothesis='Previous20/30close-channel combination passed both reused historical periods only at grid boundary.Extend toward faster entry and longer exit to test whether nearby rules form a qualification plateau;faster entry may add whipsaws and longer exits increase giveback.Freeze all cells first;no unseen-data or optimality claim.',
 grid={'entry_lookback_days':[10,15,20],'exit_lookback_days':[30,40,50],'raw_weight_pair':[.75,.25],'capital_usdt':2000,'component_capitals_usdt':{'BTC':1500,'ETH':500},'predeclared_center':[15,40]},
 sensitivity='Full3x3 entry10/15/20 x exit30/40/50 for each year and BTC/ETH/combination;48 new exact definitions reserve first.6 existing20/30 cells and18 cost scenes read-only,with source report/spec/archive/NAV hashes.No repeat strategy computation,registration or finish of those six.',
 new_configs=48,new_cost_scenes=144,reused_grid_configs=6,reused_cost_scenes=18,full_grid_configs=54,prior_canonical_trials=644,development_history_reused=True,
 interpretation='Grid extension is chosen after seeing prior20/30boundary results in these SAME reused historical periods.Not an independent holdout,statistical significance or forward validation.Mathematical signal/rule identity remains unchanged;only entry/exit lengths change.Per-day data availability remains causal.',
 reuse_source={'round':source.name,'report':str((source/'report.json').relative_to(ROOT)),'report_sha256':sha(source/'report.json')},
 qualification_scope='Fresh configurations use fixed gates and expanded9-cell positivity.Used existing archives may be compared against the expanded neighbourhood;their original ledger status/source criteria remain explicitly saved and untouched.',
 forward_resume={'source_state':str((source/'forward_state.json').relative_to(ROOT)),'state_sha256':sha(source/'forward_state.json'),'source_report':str((source/'forward_report.json').relative_to(ROOT)),'report_sha256':sha(source/'forward_report.json'),'resume_utc':'2026-10-02T15:40:00Z','cutoff_utc':'2026-10-02T17:40:00Z','new_minutes':120,'cumulative_minutes':1059,'action':'Append closed marks only;preserve original positions,desired,trades and costs.Next daily decisionOct3UTC00:01.','new_configs':3,'new_cost_scenes':9,'qualification':'Partial1059minutes insufficient for180days/sixfold;keep original long-run plan collecting.'})
plan['forward_plan']['status_at_freeze']='Collecting fromOct2UTC00:01;resume154903 exact per-cost positions.Original symmetricSMA65/1% rule unchanged;do not apply extended channel to observer.'
(ROUND/'spec.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
snap={'ledger_sha256':sha(ledger),'lines':len(ledger.read_text().splitlines()),'canonical':len(canonical),'records':records,'prior_conclusions':{str(p.relative_to(ROOT)):{'sha256':sha(p),'text':p.read_text()} for p in sorted((ROOT/'research/experiments').glob('*/result.md'))},'legacy_results':{str(p.relative_to(ROOT)):json.loads(p.read_text()) for p in (ROOT/'freqtrade_trial/results').glob('walk_forward*.json')},'checks_read':{str(p.relative_to(ROOT)):{'sha256':sha(p),'text':p.read_text()} for p in (ROOT/'checks').glob('*oos.py')}}
with (ROUND/'prior_summary.json.gz').open('wb') as f:
 with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as z:z.write(json.dumps(snap,ensure_ascii=False,separators=(',',':')).encode())
batch=[];allgrid=[];fps={}
def save(sp,fields,target):
 fp=registry.fingerprint(sp);assert fp not in canonical
 path=ROUND/'specs'/f'{sp["name"]}.json';path.parent.mkdir(exist_ok=True);path.write_text(json.dumps(sp,indent=2)+'\n')
 run=subprocess.run([sys.executable,'research/automation/registry.py','reserve',str(path)],cwd=ROOT,capture_output=True,text=True);print(sp['name'],run.returncode,run.stdout.strip(),flush=True)
 if run.returncode:raise RuntimeError('STOP before calculation:'+run.stdout+run.stderr)
 row={'name':sp['name'],'fingerprint':fp,'spec':str(path.relative_to(ROOT)),**fields};target.append(row);return row
def grid_cell(sp,fields):
 fp=registry.fingerprint(sp)
 if fp in canonical:
  assert fields['entry_days']==20 and fields['exit_days']==30
  prev=next(b for b in oldbatch if b['fingerprint']==fp);row=old['configs'][prev['name']]
  assert registry.fingerprint(records[fp]['spec'])==fp and records[fp]['result_available'] and records[fp]['status']!='reserved'
  b={**prev,'is_new':False,'source_ref':{'source_round':source.name,'report':plan['reuse_source']['report'],'report_sha256':plan['reuse_source']['report_sha256'],'archive':row['archive'],'archive_sha256':row['archive_sha256'],'spec_sha256':sha(ROOT/prev['spec'])}}
  print('READ_ONLY_EXACT',prev['name'],fp,flush=True)
 else:b=save(sp,{**fields,'is_new':True},batch)
 allgrid.append(b);return fp
for y in plan['periods']:
 for asset in ('BTC','ETH'):
  template=next(c for c in old['configs'].values() if c['year']==y and c.get('asset')==asset and c['entry_days']==20 and c['exit_days']==30)
  for entry in plan['grid']['entry_lookback_days']:
   for exit in plan['grid']['exit_lookback_days']:
    sp=copy.deepcopy(json.loads((ROOT/template['spec']).read_text()));sp.update(name=f'channel_{y}_{asset}_e{entry}_x{exit}',validation_plan=str((ROUND/'spec.json').relative_to(ROOT)))
    sp['parameters'].update(entry_lookback_days=entry,exit_lookback_days=exit)
    fps[(y,asset,entry,exit)]=grid_cell(sp,{'year':y,'role':'component','asset':asset,'entry_days':entry,'exit_days':exit})
 template=next(c for c in old['configs'].values() if c['year']==y and c['role']=='combination' and c['entry_days']==20 and c['exit_days']==30)
 for entry in plan['grid']['entry_lookback_days']:
  for exit in plan['grid']['exit_lookback_days']:
   sp=copy.deepcopy(json.loads((ROOT/template['spec']).read_text()));sp.update(name=f'channel_{y}_combo_e{entry}_x{exit}_btc0.75',validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['components']=[{'fingerprint':fps[(y,a,entry,exit)],'weight':w} for a,w in zip(('BTC','ETH'),(.75,.25))]
   grid_cell(sp,{'year':y,'role':'combination','entry_days':entry,'exit_days':exit,'raw_weights':[.75,.25]})
assert len(batch)==48 and len(allgrid)==54 and len({b['fingerprint'] for b in allgrid})==54 and sum(not b['is_new'] for b in allgrid)==6
(ROUND/'batch.json').write_text(json.dumps(batch,indent=2)+'\n');(ROUND/'grid_batch.json').write_text(json.dumps(allgrid,indent=2)+'\n')
forward=[];prior=json.loads((source/'forward_batch.json').read_text())
for asset,capital in [('BTC',1500),('ETH',500)]:
 b=next(b for b in prior if b.get('asset')==asset);sp=json.loads((ROOT/b['spec']).read_text());sp.update(name='forward_snapshot_'+asset,validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['parameters']['end_utc']=plan['forward_resume']['cutoff_utc'];fps[asset]=save(sp,{'asset':asset,'capital_usdt':capital},forward)['fingerprint']
b=next(b for b in prior if b['name']=='forward_snapshot_combo');sp=json.loads((ROOT/b['spec']).read_text());sp.update(name='forward_snapshot_combo',validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['parameters']['end_utc']=plan['forward_resume']['cutoff_utc'];sp['components']=[{'fingerprint':fps[a],'weight':w} for a,w in zip(('BTC','ETH'),(.75,.25))];save(sp,{'capital_usdt':2000},forward);(ROUND/'forward_batch.json').write_text(json.dumps(forward,indent=2)+'\n')
print('PASS:48 NEW channel definitions and3 cumulative cutoffs reserved;6 EXACT completed cells read-only;rules and source records unchanged.')
