"""Freeze faster channel20 exits x asymmetric SMA threshold combinations; reuse exact sleeves."""
import copy,gzip,hashlib,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
R=Path(__file__).resolve().parents[3];T=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ledger=R/'research/automation/registry.jsonl';records=registry.read_records(ledger);canonical={registry.fingerprint(v['spec']):v for v in records.values()}
prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));assert sha(ledger)==prior['ledger_sha256'] and len(canonical)==2299
source=R/'research/experiments/20261002T215033Z';latest=R/'research/experiments/20261007T225726Z'
base=json.loads((source/'spec.json').read_text());old=json.loads((source/'report.json').read_text());channelpath=R/'research/experiments/20261002T154903Z/report.json';emapath=R/'research/experiments/20261001T234032Z/report.json'
channel=json.loads(channelpath.read_text());ema=json.loads(emapath.read_text());plan=copy.deepcopy(base)
plan.update(round=T.name,trigger_utc='2026-10-08T00:58:26.877Z',actual_first_tool_utc='2026-10-08T00:58:37Z',frozen_at_utc=datetime.now(timezone.utc).isoformat(),
 hypothesis='Faster channel20 exits paired with asymmetric SMA did not yield any new cross-period-qualified combination. Predeclare channel20 entry with exit10/20/30days x recursive EMA50/65/80days,symmetric1.5percent,in both opposite-asset directions. EMA timing may improve earlier folds or increase whipsaws/costs. Reuse exact1500/500USDT already-costed sleeves and12old exit30 anchors;evaluate only24genuinely new portfolios. Freeze complete rules and gates before calculation.',
 grid={'CHANNEL_entry_days':20,'CHANNEL_exit_days':[10,20,30],'EMA_span_days':[50,65,80],'EMA_symmetric_band':.015,'directions':['BTC_CHANNEL_ETH_EMA','BTC_EMA_ETH_CHANNEL'],'raw_weights':[.75,.25],'capital_usdt':2000,'component_capitals_usdt':[1500,500],'predeclared_center':{'CHANNEL_entry_days':20,'CHANNEL_exit_days':20,'EMA_span_days':65},'read_only_anchor_exit_days':30},
 new_configs=24,new_cost_scenes=72,reused_grid_configs=12,reused_cost_scenes=36,full_grid_configs=36,reused_component_configs=24,prior_canonical_trials=prior['canonical'],
 sensitivity='Each year/direction full3x3 surface:channel exit10/20/30days x EMAspan50/65/80days. Channel entry20 and EMA symmetric1.5percent fixed.24new exact combinations independently reserve;12old exit30 cells read-only. Report all cost/return/Sharpe/Calmar/minute and daily DD/fold/adjacent differences. No OOS selection.',
 cross_period_confirmation='Same direction,channel20 entry,exit,EMAspan and75/25raw initial weights must pass both reused180day/sixfold periods separately. Not a pooled account or untouched final test.',
 reuse_source={'round':source.name,'report':str((source/'report.json').relative_to(R)),'report_sha256':sha(source/'report.json')},
 qualification_scope='Original eight gates unchanged. Existing exact exit30 cells retain their original status/criteria even while the expanded surface is described. All historical data repeatedly reused;new combination paths are not independent market evidence.')
plan['forward_plan']['status_at_freeze']='Original SMA65/1percent75/25 shadow resumesOct7UTC22:50 and must processOct8UTC00:01 once from completedOct7 daily bars;nextOct9UTC00:01. Independent actual-quote paper10 frozen accounts unchanged.'
plan['forward_resume']={'source_state':str((latest/'forward_state.json').relative_to(R)),'state_sha256':sha(latest/'forward_state.json'),'source_report':str((latest/'forward_report.json').relative_to(R)),'report_sha256':sha(latest/'forward_report.json'),'resume_utc':'2026-10-07T22:50:00Z','cutoff_utc':'2026-10-08T00:50:00Z','daily_decision_utc':'2026-10-08T00:01:00Z','new_minutes':120,'cumulative_minutes':8689,'prior_NAV_points':8576,'new_reference_points':1,'total_NAV_points':8697,'daily_overlap_source':{'path':'research/experiments/20261007T083620Z/forward_inputs.json.gz','sha256':sha(R/'research/experiments/20261007T083620Z/forward_inputs.json.gz')},'action':'Process exactly one frozen original daily decision from completed65daily bars with original1/2/3cost model;append120closed-minute marks plus1execution-reference point. Preserve prior positions,desired,trades,costs and NAV prefix;no forced exit. Keep paper10 actual-quote accounts separate.','new_configs':3,'new_cost_scenes':9,'qualification':'Legacy8689minute delayed shadow,6complete days;not180day/sixfold or paper10 forward performance.'}
plan['reused_code_sha256']={str(p.relative_to(R)):sha(p) for p in [source/'evaluate.py',source/'audit.py',R/'research/experiments/20261002T154903Z/signals.py',R/'research/experiments/20261001T234032Z/signals.py',R/'research/experiments/20261001T133655Z/evaluate.py',R/'research/experiments/20261001T133655Z/kernel.py',R/'research/experiments/20261001T213902Z/audit.py',R/'research/experiments/20261001T213902Z/evaluate.py']}
plan['component_report_rounds']={'CHANNEL':'20261002T154903Z','EMA':'20261001T234032Z'}
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
  report,rp=(channel,channelpath) if kind=='CHANNEL' else (ema,emapath)
  matches=[c for c in report['configs'].values() if c['role']=='component' and c['asset']==asset and c['year']==y and ((kind=='CHANNEL' and c['entry_days']==20 and c['exit_days']==value) or (kind=='EMA' and c['span_days']==value and c['band']==.015))]
  assert len(matches)==1;c=matches[0];sp=c.get('spec_path',c.get('spec'));capital=1500 if asset=='BTC' else 500
  assert records[c['fingerprint']]['result_available'] and json.loads((R/sp).read_text())['parameters']['initial_capital_usdt']==capital
  return {'kind':kind,'name':c['name'],'report':str(rp.relative_to(R)),'report_sha256':sha(rp),'source_round':Path(c['archive']).parts[2],'fingerprint':c['fingerprint'],'archive':c['archive'],'archive_sha256':c['archive_sha256'],'spec':sp,'capital_usdt':capital,'asset':asset}
 for direction in plan['grid']['directions']:
  for entry in plan['grid']['EMA_span_days']:
   for days in plan['grid']['CHANNEL_exit_days']:
    kinds=('CHANNEL','EMA') if direction=='BTC_CHANNEL_ETH_EMA' else ('EMA','CHANNEL');refs=[lookup(kind,asset,days if kind=='CHANNEL' else entry) for kind,asset in zip(kinds,('BTC','ETH'))]
    sp=copy.deepcopy(json.loads((R/template['spec']).read_text()));sp.update(name=f'channel_ema_fast20_{y}_{direction}_s{entry}_x{days}',validation_plan=str((T/'spec.json').relative_to(R)));sp['components']=[{'fingerprint':ref['fingerprint'],'weight':w} for ref,w in zip(refs,(.75,.25))]
    fields={'year':y,'role':'combination','direction':direction,'EMA_span_days':entry,'CHANNEL_entry_days':20,'CHANNEL_exit_days':days,'raw_weights':[.75,.25],'component_refs':refs}
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
