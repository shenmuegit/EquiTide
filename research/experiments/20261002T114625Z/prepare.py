"""Freeze new asymmetric-SMA/EMA combinations and the next cumulative shadow cutoff."""
import copy,gzip,hashlib,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ledger=ROOT/'research/automation/registry.jsonl';records=registry.read_records(ledger)
canonical={registry.fingerprint(v['spec']) for v in records.values()}
assert len(canonical)==491 and all(v.get('result_available') and v['status']!='reserved' for v in records.values())
source=ROOT/'research/experiments/20261002T094655Z'
asym=json.loads((source/'report.json').read_text());ema_path=ROOT/'research/experiments/20261001T234032Z/report.json';ema=json.loads(ema_path.read_text())
base=json.loads((source/'spec.json').read_text())
rounds={y:{'ASMA':'20261002T094655Z','EMA':'20261001T234032Z'} for y in ('2025','2026')}
plan={'round':ROUND.name,'trigger_utc':'2026-10-02T11:46:25.514Z','actual_first_tool_utc':'2026-10-02T11:47:04Z','frozen_at_utc':datetime.now(timezone.utc).isoformat(),
 'hypothesis':'Asymmetric SMA65 and EMA trend responses differ. Freeze both asset directions and full entry-buffer x EMA-span grid to test whether asynchronous exposure improves fold diversification; may delay gains or reinforce correlated drawdowns.',
 'grid':{'ASMA_lookback_days':65,'ASMA_entry_band':[.0125,.015,.02],'ASMA_exit_band':.005,'EMA_span_days':[50,65,80],'EMA_band':.015,'directions':['BTC_ASMA_ETH_EMA','BTC_EMA_ETH_ASMA'],'raw_weights':[.75,.25],'capital_usdt':2000,'component_capitals_usdt':[1500,500]},
 'new_configs':36,'new_cost_scenes':108,'prior_canonical_trials':491,
 'walk_forward':copy.deepcopy(base['walk_forward']),'execution':base['execution'],'costs':base['costs'],'gates':base['gates'],
 'ASMA_rules':base['rules'],'ASMA_initialization':base['signal_initialization'],'EMA_definition':ema['plan']['EMA_definition'],
 'allocation':'Raw BTC/ETH75/25 specifies initial1500/500USDT. Add size-matched fully costed absolute minute NAV;no second weighting,transfers,maintained weights or rebalancing.All24 component configurations have actual results;no new component backtests.',
 'sensitivity':'Each year and direction has complete3x3 ASMA entry-band x EMA-span grid.Exits fixedASMA0.5%,lookback65;EMA symmetric1.5%.All36 reserve first;all cost/fold/risk metrics and descriptive adjacent2sd flags retained.No OOS rule or weight choice.',
 'periods':base['periods'],'component_report_rounds':rounds,'development_history_reused':True,
 'interpretation':'Both histories repeatedly reused;previous asymmetricSMA/EMA results motivated this grid.Causal component decisions do not remove retrospective selection or multiple-trial bias.Not pristine final holdout,statistical significance,or stable live profit.',
 'cross_period_confirmation':'Same direction/entry-buffer/span/rawweights must meet gates in EACH separately reported sixfold period.No unregistered cross-period compounded curve.',
 'reference':base['reference'],'forward_plan':copy.deepcopy(base['forward_plan']),
 'forward_resume':{'source_state':str((source/'forward_state.json').relative_to(ROOT)),'state_sha256':sha(source/'forward_state.json'),'source_report':str((source/'forward_report.json').relative_to(ROOT)),'report_sha256':sha(source/'forward_report.json'),'resume_utc':'2026-10-02T09:40:00Z','cutoff_utc':'2026-10-02T11:40:00Z','new_minutes':120,'cumulative_minutes':699,'action':'Append closed-minute marks only;retain original positions,desired state,trades and cumulative costs.Next daily decisionOct3UTC00:01.','new_configs':3,'new_cost_scenes':9,'qualification':'Partial699minutes insufficient for180days/sixfold;original long-run plan collecting.'}}
plan['walk_forward']['fit']='No fit or labels. Reuse causal ASMA65 and recursiveEMA component states;180train/3gap/6x30 chronological diagnostics,purge0.No per-fold resets;EMA seed from source firstclose before rolling train start.'
plan['forward_plan']['status_at_freeze']='Collecting fromOct2UTC00:01;resume094655 exact positions;original symmetricSMA65/1% rule unchanged.'
comparator_refs=[]
for y,period in base['periods'].items():
 old=json.loads((ROOT/period['report']).read_text())
 for name,row in old['configs'].items():
  if row['role']=='comparator_combination' or (row['role']=='combination' and row['lookback_days']==65 and row['raw_weights']==[.75,.25]):comparator_refs.append({'name':name,'year':y,'kind':'hold50/50' if row['role']=='comparator_combination' else 'symmetricSMA65','report':period['report'],'report_sha256':sha(ROOT/period['report'])})
 for report,refpath,kind in [(asym,source/'report.json','ASMA_center'),(ema,ema_path,'EMA50')]:
  for name,row in report['configs'].items():
   if row['role']!='combination' or row['year']!=y:continue
   matches=(kind=='ASMA_center' and row['entry_band']==.015 and row['exit_band']==.005) or (kind=='EMA50' and row['span_days']==50 and row['band']==.015)
   if matches:comparator_refs.append({'name':name,'year':y,'kind':kind,'report':str(refpath.relative_to(ROOT)),'report_sha256':sha(refpath)})
assert len(comparator_refs)==8;plan['read_only_comparator_refs']=comparator_refs
(ROUND/'spec.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
snapshot={'ledger_sha256':sha(ledger),'lines':len(ledger.read_text().splitlines()),'canonical':len(canonical),'records':records,'prior_conclusions':{str(p.relative_to(ROOT)):{'sha256':sha(p),'text':p.read_text()} for p in sorted((ROOT/'research/experiments').glob('*/result.md'))},'legacy_results':{str(p.relative_to(ROOT)):json.loads(p.read_text()) for p in (ROOT/'freqtrade_trial/results').glob('walk_forward*.json')},'checks_read':{str(p.relative_to(ROOT)):{'sha256':sha(p),'text':p.read_text()} for p in (ROOT/'checks').glob('*oos.py')}}
with (ROUND/'prior_summary.json.gz').open('wb') as f:
 with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as z:z.write(json.dumps(snapshot,ensure_ascii=False,separators=(',',':')).encode())
batch=[]
def save(sp,fields,target):
 fp=registry.fingerprint(sp);assert fp not in canonical
 path=ROUND/'specs'/f'{sp["name"]}.json';path.parent.mkdir(exist_ok=True);path.write_text(json.dumps(sp,indent=2)+'\n')
 run=subprocess.run([sys.executable,'research/automation/registry.py','reserve',str(path)],cwd=ROOT,capture_output=True,text=True);print(sp['name'],run.returncode,run.stdout.strip(),flush=True)
 if run.returncode:raise RuntimeError('STOP before evaluation:'+run.stdout+run.stderr)
 target.append({'name':sp['name'],'fingerprint':fp,'spec':str(path.relative_to(ROOT)),**fields});return fp
for y in ('2025','2026'):
 old=json.loads((ROOT/base['periods'][y]['report']).read_text());template=next(row for row in old['configs'].values() if row['role']=='combination')
 def lookup(kind,asset,value):
  report=asym if kind=='ASMA' else ema
  matches=[]
  for name,row in report['configs'].items():
   if row['role']!='component' or row['asset']!=asset or row['year']!=y:continue
   keep=(kind=='ASMA' and row['lookback_days']==65 and row['entry_band']==value and row['exit_band']==.005) or (kind=='EMA' and row['span_days']==value and row['band']==.015)
   if keep:matches.append((name,row))
  assert len(matches)==1;name,row=matches[0];rid=rounds[y][kind];assert records[row['fingerprint']]['result_available']
  sp=row.get('spec_path',row.get('spec'));assert json.loads((ROOT/sp).read_text())['parameters']['initial_capital_usdt']==(1500 if asset=='BTC' else 500)
  return {'kind':kind,'name':name,'report':f'research/experiments/{rid}/report.json','report_sha256':sha(ROOT/'research/experiments'/rid/'report.json'),'source_round':rid,'fingerprint':row['fingerprint'],'archive':row['archive'],'archive_sha256':row['archive_sha256'],'spec':sp,'capital_usdt':1500 if asset=='BTC' else 500,'asset':asset}
 for direction in plan['grid']['directions']:
  for entry in plan['grid']['ASMA_entry_band']:
   for span in plan['grid']['EMA_span_days']:
    kinds=('ASMA','EMA') if direction=='BTC_ASMA_ETH_EMA' else ('EMA','ASMA')
    refs=[lookup(kind,asset,entry if kind=='ASMA' else span) for kind,asset in zip(kinds,('BTC','ETH'))]
    name=f'asymhybrid_{y}_{direction}_e{entry}_s{span}';sp=copy.deepcopy(json.loads((ROOT/template['spec_path']).read_text()))
    sp.update(name=name,family='asymmetric-sma-ema-initial-capital',validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['components']=[{'fingerprint':ref['fingerprint'],'weight':w} for ref,w in zip(refs,(.75,.25))]
    save(sp,{'year':y,'direction':direction,'ASMA_entry_band':entry,'EMA_span_days':span,'raw_weights':[.75,.25],'component_refs':refs},batch)
assert len(batch)==36 and len({b['fingerprint'] for b in batch})==36
(ROUND/'batch.json').write_text(json.dumps(batch,indent=2)+'\n')
forward=[];prior=json.loads((source/'forward_batch.json').read_text());fps={}
for asset,capital in [('BTC',1500),('ETH',500)]:
 b=next(b for b in prior if b.get('asset')==asset);sp=json.loads((ROOT/b['spec']).read_text());sp.update(name='forward_snapshot_'+asset,validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['parameters']['end_utc']=plan['forward_resume']['cutoff_utc'];fps[asset]=save(sp,{'asset':asset,'capital_usdt':capital},forward)
b=next(b for b in prior if b['name']=='forward_snapshot_combo');sp=json.loads((ROOT/b['spec']).read_text());sp.update(name='forward_snapshot_combo',validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['parameters']['end_utc']=plan['forward_resume']['cutoff_utc'];sp['components']=[{'fingerprint':fps[a],'weight':w} for a,w in zip(('BTC','ETH'),(.75,.25))];save(sp,{'capital_usdt':2000},forward)
(ROUND/'forward_batch.json').write_text(json.dumps(forward,indent=2)+'\n')
print('PASS:36 new size-matched combinations and3 new cumulative cutoff configurations reserved before calculation;24 actual-result components reused.')
