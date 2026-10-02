"""Freeze hybrid SMA/EMA portfolios, reusing size-matched net components."""
import copy,gzip,hashlib,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ledger=ROOT/'research/automation/registry.jsonl';records=registry.read_records(ledger);canonical={registry.fingerprint(v['spec']) for v in records.values()}
assert len(canonical)==338 and all(v.get('result_available') and v['status']!='reserved' for v in records.values())
rounds={'2025':{'SMA':'20261001T173606Z','EMA':'20261001T234032Z'},'2026':{'SMA':'20261001T133655Z','EMA':'20261001T234032Z'}}
reports={rid:json.loads((ROOT/'research/experiments'/rid/'report.json').read_text()) for rid in {s for d in rounds.values() for s in d.values()}}
old=json.loads((ROOT/'research/experiments/20261001T213902Z/spec.json').read_text())
plan={'round':ROUND.name,'trigger_utc':'2026-10-02T01:41:32.255Z','actual_first_tool_utc':'2026-10-02T01:41:57Z','frozen_at_utc':datetime.now(timezone.utc).isoformat(),
 'hypothesis':'SMA and EMA have different trend response/state paths; combine one on each asset to test whether asynchronous exposure improves fold diversification. Freeze both directions and full lookback/span grid before derived results.',
 'grid':{'SMA_lookback_days':[60,65,70],'EMA_span_days':[50,65,80],'SMA_band':.01,'EMA_band':.015,'directions':['BTC_SMA_ETH_EMA','BTC_EMA_ETH_SMA'],'raw_weights':[.75,.25],'capital_usdt':2000,'component_capitals_usdt':[1500,500]},
 'new_configs':36,'new_cost_scenes':108,'prior_canonical_trials':338,
 'walk_forward':old['walk_forward'],'execution':old['execution'],'costs':old['costs'],'gates':old['gates'],
 'SMA_rules':old['rules'],'EMA_definition':reports['20261001T234032Z']['plan']['EMA_definition'],
 'allocation':'Raw BTC/ETH75/25 specifies initial1500/500USDT. Each independently computed actual-capital costed minute NAV is added; no second weighting, transfers, maintained weights or rebalancing. All components already have real results; no new component backtests.',
 'sensitivity':'For each period and direction, complete3x3 SMA lookback x EMA span grid,9 new distinct configurations. Bands fixed atSMA1%/EMA1.5%, weights fixed75/25. Publish all cost/fold/risk metrics and adjacent descriptive2sd differences; no OOS retuning.',
 'periods':old['periods'],'component_report_rounds':rounds,
 'development_history_reused':True,'interpretation':'Both histories already observed; previous SMA/EMA findings motivated this grid. EMA1.5% is selected from prior development results, not unobserved validation. Daily causal execution does not remove retrospective selection and multiple-trial bias. No pristine final holdout, statistical significance or stable live profit claim.',
 'cross_period_confirmation':'Identical direction/lookback/span/rawweights must pass all gates in EACH separately reported sixfold period. Do not combine/multiply separate period returns into a new unregistered strategy.',
 'forward_plan':{'path':old['forward_plan']['path'],'sha256':old['forward_plan']['sha256'],'status_at_freeze':'ScheduledOct2UTC00:01 start has elapsed;attempt fresh public data retrieval before shadow observation,keep original rules unchanged. No forward result yet at grid freeze.'},
 'data_status':'Fresh-data probe is an operational read only; collect/validate source records first. Any actual forward strategy computation must have its own distinct reserved spec; no fabricated bars, current quote substitution or reused historical forward result.'}
(ROUND/'spec.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
snap={'ledger_sha256':sha(ledger),'lines':len(ledger.read_text().splitlines()),'canonical':338,'records':records,'prior_conclusions':{str(p.relative_to(ROOT)):{'sha256':sha(p),'text':p.read_text()} for p in sorted((ROOT/'research/experiments').glob('*/result.md'))}}
with (ROUND/'prior_summary.json.gz').open('wb') as f:
 with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as z:z.write(json.dumps(snap,ensure_ascii=False,separators=(',',':')).encode())
batch=[]
for year in ('2025','2026'):
 sma=reports[rounds[year]['SMA']];ema=reports[rounds[year]['EMA']]
 def lookup(kind,asset,n):
  report=sma if kind=='SMA' else ema
  if kind=='SMA':matches=[(name,row) for name,row in report['configs'].items() if row['role']=='component' and row['asset']==asset and row['parameters']['lookback_days']==n and row['parameters']['initial_capital_usdt']==(1500 if asset=='BTC' else 500)]
  else:matches=[(name,row) for name,row in report['configs'].items() if row['role']=='component' and row['asset']==asset and row['year']==year and row['span_days']==n and row['band']==.015]
  assert len(matches)==1;name,row=matches[0];assert records[row['fingerprint']]['result_available'];rid=rounds[year][kind]
  return {'kind':kind,'name':name,'report':f'research/experiments/{rid}/report.json','report_sha256':sha(ROOT/'research/experiments'/rid/'report.json'),'source_round':rid,'fingerprint':row['fingerprint'],'archive':row['archive'],'archive_sha256':row['archive_sha256'],'spec':row.get('spec_path',row.get('spec')),'capital_usdt':1500 if asset=='BTC' else 500,'asset':asset}
 template=next(r for r in sma['configs'].values() if r['role']=='combination')
 for direction in plan['grid']['directions']:
  for lookback in plan['grid']['SMA_lookback_days']:
   for span in plan['grid']['EMA_span_days']:
    kinds=('SMA','EMA') if direction=='BTC_SMA_ETH_EMA' else ('EMA','SMA')
    refs=[lookup(kind,asset,lookback if kind=='SMA' else span) for kind,asset in zip(kinds,('BTC','ETH'))]
    name=f'hybrid_{year}_{direction}_n{lookback}_s{span}';sp=copy.deepcopy(json.loads((ROOT/template['spec_path']).read_text()))
    sp.update(name=name,validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['components']=[{'fingerprint':ref['fingerprint'],'weight':w} for ref,w in zip(refs,(.75,.25))]
    fp=registry.fingerprint(sp);assert fp not in canonical
    path=ROUND/'specs'/f'{name}.json';path.parent.mkdir(exist_ok=True);path.write_text(json.dumps(sp,indent=2)+'\n')
    result=subprocess.run(['python3','research/automation/registry.py','reserve',str(path)],cwd=ROOT,capture_output=True,text=True)
    print(name,result.returncode,result.stdout.strip(),flush=True)
    if result.returncode:raise RuntimeError('STOP before calculation:'+result.stdout+result.stderr)
    batch.append({'name':name,'year':year,'direction':direction,'SMA_lookback_days':lookback,'EMA_span_days':span,'raw_weights':[.75,.25],'fingerprint':fp,'spec':str(path.relative_to(ROOT)),'component_refs':refs})
assert len(batch)==36 and len({b['fingerprint'] for b in batch})==36
(ROUND/'batch.json').write_text(json.dumps(batch,indent=2)+'\n')
print('PASS:36 genuinely new hybrid configurations reserved before portfolio calculations;24 finished size-matched components reused.')
