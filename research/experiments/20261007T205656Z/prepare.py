"""Freeze channel exit x asymmetric SMA threshold combinations; reuse exact costed sleeves."""
import copy,gzip,hashlib,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
R=Path(__file__).resolve().parents[3];T=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ledger=R/'research/automation/registry.jsonl';records=registry.read_records(ledger);canonical={registry.fingerprint(v['spec']):v for v in records.values()}
prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));assert sha(ledger)==prior['ledger_sha256'] and len(canonical)==2225
source=R/'research/experiments/20261002T195003Z';latest=R/'research/experiments/20261007T185556Z'
base=json.loads((source/'spec.json').read_text());old=json.loads((source/'report.json').read_text());channelpath=R/'research/experiments/20261002T174933Z/report.json';asmapath=R/'research/experiments/20261002T094655Z/report.json'
channel=json.loads(channelpath.read_text());asma=json.loads(asmapath.read_text());plan=copy.deepcopy(base)
plan.update(round=T.name,trigger_utc='2026-10-07T20:56:56.658Z',actual_first_tool_utc='2026-10-07T20:57:07Z',frozen_at_utc=datetime.now(timezone.utc).isoformat(),
 hypothesis='Previous channel15/30 plus SMA65 on the other asset had positive but final-fold-concentrated reused-history returns. Predeclare channel15 entry with exit30/40/50 x SMA65 entry1.25/1.5/2percent,exit0.5percent,in both opposite-asset directions. Longer channel holding may diversify earlier folds or increase drawdown. Reuse exact1500/500USDT fully costed sleeves;only genuinely new combinations are evaluated,old30day combinations read-only. No parameters or gates changed after results.',
 grid={'CHANNEL_entry_days':15,'CHANNEL_exit_days':[30,40,50],'ASMA_lookback_days':65,'ASMA_entry_band':[.0125,.015,.02],'ASMA_exit_band':.005,'directions':['BTC_CHANNEL_ETH_ASMA','BTC_ASMA_ETH_CHANNEL'],'raw_weights':[.75,.25],'capital_usdt':2000,'component_capitals_usdt':[1500,500],'predeclared_center':{'CHANNEL_entry_days':15,'CHANNEL_exit_days':40,'ASMA_entry_band':.015},'read_only_anchor_exit_days':30},
 new_configs=24,new_cost_scenes=72,reused_grid_configs=12,reused_cost_scenes=36,full_grid_configs=36,reused_component_configs=24,prior_canonical_trials=prior['canonical'],
 sensitivity='Each year/direction full3x3 surface:channel exit30/40/50days x SMA65 entry1.25/1.5/2percent. Entrychannel15 and SMAexit0.5percent fixed.24new exact combinations independently reserve;12old exit30 cells read-only. All returns,Sharpe,Calmar,minute/daily DD,folds and adjacent differences reported. No OOS selection.',
 cross_period_confirmation='Same direction,channel15 entry,exit,SMAentry and75/25raw initial weights must pass both reused180day/sixfold periods separately. No pooled account or final untouched test.',
 reuse_source={'round':source.name,'report':str((source/'report.json').relative_to(R)),'report_sha256':sha(source/'report.json')},
 qualification_scope='Original eight gates unchanged. Existing exact exit30 cells retain their original status/criteria even while the expanded surface is described. All historical data repeatedly reused;new combination paths are not independent market evidence.')
plan['forward_plan']['status_at_freeze']='Original SMA65/1percent75/25 legacy observer collecting;Oct7 daily processed,next Oct8UTC00:01. Independent actual-quote paper10 frozen accounts unchanged.'
plan['forward_resume']={'source_state':str((latest/'forward_state.json').relative_to(R)),'state_sha256':sha(latest/'forward_state.json'),'source_report':str((latest/'forward_report.json').relative_to(R)),'report_sha256':sha(latest/'forward_report.json'),'resume_utc':'2026-10-07T18:40:00Z','cutoff_utc':'2026-10-07T20:50:00Z','new_minutes':130,'cumulative_minutes':8449,'prior_NAV_points':8326,'new_reference_points':0,'total_NAV_points':8456,'action':'Append130 closed-minute legacy marks;no daily decision,fills,new costs or terminal liquidation. Keep actual-quote paper10 separate.','new_configs':3,'new_cost_scenes':9,'qualification':'Legacy8449minute delayed shadow,5complete days;not180day/sixfold or paper10 forward performance.'}
plan['reused_code_sha256']={str(p.relative_to(R)):sha(p) for p in [source/'evaluate.py',source/'audit.py',R/'research/experiments/20261002T174933Z/signals.py',R/'research/experiments/20261002T094655Z/signals.py',R/'research/experiments/20261001T133655Z/evaluate.py',R/'research/experiments/20261001T133655Z/kernel.py',R/'research/experiments/20261001T213902Z/audit.py',R/'research/experiments/20261001T213902Z/evaluate.py']}
(T/'spec.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
batch=[];grid=[]
def save(sp,fields,target):
 fp=registry.fingerprint(sp);assert fp not in canonical
 path=T/'specs'/f'{sp["name"]}.json';path.parent.mkdir(exist_ok=True);path.write_text(json.dumps(sp,indent=2)+'\n')
 result=subprocess.run([sys.executable,'research/automation/registry.py','reserve',str(path.relative_to(R))],cwd=R,capture_output=True,text=True)
 print(sp['name'],result.returncode,result.stdout.strip(),flush=True)
 if result.returncode:raise RuntimeError('STOP before calculation:'+result.stdout+result.stderr)
 b={'name':sp['name'],'fingerprint':fp,'spec':str(path.relative_to(R)),**fields};target.append(b);return b
for y in plan['periods']:
 template=next(c for c in old['configs'].values() if c['year']==y)
 def lookup(kind,asset,value):
  report,rp=(channel,channelpath) if kind=='CHANNEL' else (asma,asmapath)
  matches=[c for c in report['configs'].values() if c['role']=='component' and c['asset']==asset and c['year']==y and ((kind=='CHANNEL' and c['entry_days']==15 and c['exit_days']==value) or (kind=='ASMA' and c['lookback_days']==65 and c['entry_band']==value and c['exit_band']==.005))]
  assert len(matches)==1;c=matches[0];sp=c.get('spec_path',c.get('spec'));capital=1500 if asset=='BTC' else 500
  assert records[c['fingerprint']]['result_available'] and json.loads((R/sp).read_text())['parameters']['initial_capital_usdt']==capital
  return {'kind':kind,'name':c['name'],'report':str(rp.relative_to(R)),'report_sha256':sha(rp),'source_round':Path(c['archive']).parts[2],'fingerprint':c['fingerprint'],'archive':c['archive'],'archive_sha256':c['archive_sha256'],'spec':sp,'capital_usdt':capital,'asset':asset}
 for direction in plan['grid']['directions']:
  for entry in plan['grid']['ASMA_entry_band']:
   for days in plan['grid']['CHANNEL_exit_days']:
    kinds=('CHANNEL','ASMA') if direction=='BTC_CHANNEL_ETH_ASMA' else ('ASMA','CHANNEL');refs=[lookup(kind,asset,days if kind=='CHANNEL' else entry) for kind,asset in zip(kinds,('BTC','ETH'))]
    sp=copy.deepcopy(json.loads((R/template['spec']).read_text()));sp.update(name=f'channel_asma_exit_{y}_{direction}_e{entry}_x{days}',validation_plan=str((T/'spec.json').relative_to(R)));sp['components']=[{'fingerprint':ref['fingerprint'],'weight':w} for ref,w in zip(refs,(.75,.25))]
    fields={'year':y,'role':'combination','direction':direction,'ASMA_entry_band':entry,'CHANNEL_entry_days':15,'CHANNEL_exit_days':days,'raw_weights':[.75,.25],'component_refs':refs}
    fp=registry.fingerprint(sp)
    if fp in canonical:
     assert days==30;rec=canonical[fp];rp=R/rec['report'];assert rec['result_available'] and sha(rp)==rec['report_sha256'];prev=next(c for c in json.loads(rp.read_text())['configs'].values() if c['fingerprint']==fp)
     b={**{k:prev[k] for k in ('name','fingerprint','spec')},**fields,'is_new':False,'source_ref':{'report':rec['report'],'report_sha256':sha(rp),'archive':prev['archive'],'archive_sha256':prev['archive_sha256'],'source_round':Path(prev['archive']).parts[2],'spec_sha256':sha(R/prev['spec'])}};print('READ_ONLY_EXACT',b['name'],flush=True)
    else:b=save(sp,{**fields,'is_new':True},batch)
    grid.append(b)
assert len(batch)==24 and len(grid)==36 and len({r['fingerprint'] for b in grid for r in b['component_refs']})==24
(T/'batch.json').write_text(json.dumps(batch,indent=2)+'\n');(T/'grid_batch.json').write_text(json.dumps(grid,indent=2)+'\n')
forward=[];oldfb=json.loads((latest/'forward_batch.json').read_text());fps={}
for asset,capital in [('BTC',1500),('ETH',500)]:
 b=next(b for b in oldfb if b.get('asset')==asset);sp=json.loads((R/b['spec']).read_text());sp.update(name='forward_snapshot_'+asset,validation_plan=str((T/'spec.json').relative_to(R)));sp['parameters']['end_utc']=plan['forward_resume']['cutoff_utc'];fps[asset]=save(sp,{'asset':asset,'capital_usdt':capital},forward)['fingerprint']
sp=json.loads((R/oldfb[-1]['spec']).read_text());sp.update(name='forward_snapshot_combo',validation_plan=str((T/'spec.json').relative_to(R)));sp['parameters']['end_utc']=plan['forward_resume']['cutoff_utc'];sp['components']=[{'fingerprint':fps[a],'weight':w} for a,w in zip(('BTC','ETH'),(.75,.25))];save(sp,{'capital_usdt':2000},forward)
(T/'forward_batch.json').write_text(json.dumps(forward,indent=2)+'\n');print('PASS:24new combinations+3legacy cutoffs reserved;12exact combinations and24size-matched sleeves read-only.')
