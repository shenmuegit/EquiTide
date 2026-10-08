"""Freeze asset-specific EMA filter spans using exact already-funded components."""
from pathlib import Path
from datetime import datetime,timezone
import copy,gzip,hashlib,json,subprocess,sys
R=Path(__file__).resolve().parents[3];T=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
records=registry.read_records(R/'research/automation/registry.jsonl');canonical={registry.fingerprint(v['spec']):v for v in records.values()};prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()))
assert sha(R/'research/automation/registry.jsonl')==prior['ledger_sha256'] and len(canonical)==prior['canonical']
latest=R/'research/experiments/20261008T090319Z';base=json.loads((latest/'spec.json').read_text());reference=R/'research/experiments/20261005T214041Z/report.json';source=json.loads(reference.read_text())
components={}
for fp,v in records.items():
 sp=v['spec'];p=sp.get('parameters',{})
 if p.get('initial_capital_usdt') in (1350,650) and p.get('entry_lookback_days')==15 and p.get('exit_lookback_days')==30 and p.get('EMA_symmetric_band')==.03 and p.get('EMA_span_days') in (25,27,29):
  y=p['start_utc'][:4];asset=sp['universe'][0].split('/')[0];components[y,asset,p['EMA_span_days']]={'fingerprint':fp,'record':v}
assert len(components)==12
csp=components['2026','BTC',25]['record']['spec']
oldforward=json.loads((latest/'forward_report.json').read_text());state=json.loads((latest/'forward_state.json').read_text());resume=oldforward['cutoff_utc'];cutoff='2026-10-08T11:00:00Z';parse=lambda t:datetime.fromisoformat(t.replace('Z','+00:00'))
minutes=int((parse(cutoff)-parse(resume)).total_seconds()/60);oldscene=oldforward['configs']['forward_snapshot_combo']['scenes']['1'];oldpoints=len(oldscene['equity_usdt']);totalminutes=oldscene['elapsed_minutes']+minutes
assert minutes==120 and parse(cutoff)<datetime.now(timezone.utc) and parse(cutoff)<parse(state['next_daily_decision_utc'])
plan={k:copy.deepcopy(base[k]) for k in ('periods','execution','costs','gates','walk_forward','forward_plan')}
plan.update(round=T.name,trigger_utc='2026-10-08T11:04:49.525Z',actual_first_tool_utc='2026-10-08T11:04:57Z',frozen_at_utc=datetime.now(timezone.utc).isoformat(),
 hypothesis='Independent pure-channel entry/exit changes did not add cross-period qualified settings. Test independent BTC/ETH EMA confirmation speeds25/27/29 while fixing close-channel entry15/exit30 and symmetric3percent EMA band. Asset-specific response speeds may diversify threshold timing,or merely reproduce existing fills. Predeclare BTC29/ETH25 focus;EMA27/27 is an old center. All off-diagonal portfolios across both years are new configurations;no old component or diagonal backtests repeated.',
 grid={'BTC_EMA_span_days':[25,27,29],'ETH_EMA_span_days':[25,27,29],'entry_lookback_days':15,'exit_lookback_days':30,'EMA_symmetric_band':.03,'directions':['ASSET_SPECIFIC_EMA_CHANNEL_CONFIRMATION'],'raw_weights':[.675,.325],'capital_usdt':2000,'component_capitals_usdt':[1350,650],'predeclared_center':{'BTC_EMA_span_days':27,'ETH_EMA_span_days':27},'predeclared_focus':{'BTC_EMA_span_days':29,'ETH_EMA_span_days':25},'read_only_diagonals':[25,27,29]},
 rules=copy.deepcopy(csp['logic']),channel_definition=csp['parameters']['channel_definition'],EMA_definition=csp['logic']['EMA'],
 allocation='Original BTC/ETH67.5/32.5 means initial1350/650USDT independent sleeves of2000. Sum exact-capital already-costed absolute NAVs once;no normalization,second weighting,maintained ratio,transfer or rebalance.',
 sensitivity='BTC EMA span25/27/29 crossed with ETH span25/27/29,channel15/30 and symmetric3percent band fixed.12new annual off-diagonal portfolios,6exact old diagonals read-only,12existing actual-funded components;all1/2/3costs,sixfolds,minute/daily drawdown,Sharpe,Calmar and12adjacent edges per surface retained.',
 new_configs=12,new_cost_scenes=36,reused_grid_configs=6,reused_cost_scenes=18,full_grid_configs=18,reused_component_configs=12,prior_canonical_trials=prior['canonical'],development_history_reused=True,
 cross_period_confirmation='Identical BTCspan/ETHspan and fixed channel15/30,band3percent,67.5/32.5funding must pass EACH reused180day/sixfold period. No pooled years,untouched final holdout or independent market evidence.',
 qualification_scope='Original eight gates unchanged. All12new parameter pairs independently reserve/finish;6old diagonals retain their original status/criteria. Whole-NAV equality measured explicitly and never called independent evidence.',
 interpretation='Repeated development history and many trials;parameter novelty or positive historical net returns do not establish stable live profit. FixedP01-P10 real-quote paper parameters/accounts remain unchanged.',
 knowledge_sources=[{'url':'https://github.com/binance/binance-public-data','access_date_utc':'2026-10-08','scope':'Official spot archive timestamps/checksums/revisions. Same-SHA cached minute data reused;no archive version changed.'},{'url':'https://data-api.binance.vision/api/v3/klines','scope':'Only completed-minute publicGET for separate original delayed shadow;not paper10 actual-quote fills.'}])
plan['walk_forward']['fit']='Fixed causal close-channel and EMA rules;Python float EMA alpha2/(span+1),adjustFalse,seed datasetday0,never reset per fold. No model/labels/perfold or OOS fitting.180day rolling history,3day gap,purge0,six continuous30day diagnostic folds.'
plan['forward_plan']['status_at_freeze']='Original SMA65/1percent75/25 delayed shadow continues exact per-cost positions;next daily decision2026-10-09UTC00:01. Actual-quote paper10 accounts are separate.'
plan['forward_resume']={'source_state':str((latest/'forward_state.json').relative_to(R)),'state_sha256':sha(latest/'forward_state.json'),'source_report':str((latest/'forward_report.json').relative_to(R)),'report_sha256':sha(latest/'forward_report.json'),'resume_utc':resume,'cutoff_utc':cutoff,'new_minutes':minutes,'cumulative_minutes':totalminutes,'prior_NAV_points':oldpoints,'new_reference_points':0,'total_NAV_points':oldpoints+minutes,'action':f'Append{minutes}closed marks to{oldpoints}old points;no daily reference,decision,fill,cost,restart or forced exit. Paper10 remains unchanged.','new_configs':3,'new_cost_scenes':9,'qualification':f'Only{totalminutes}minutes/{totalminutes//1440}complete days of delayed shadow;not180day/sixfold or contemporaneous paper10 performance.'}
plan['read_only_comparator_refs']=[v for v in base['read_only_comparator_refs'] if v['kind'] in ('SMA_or_hold','CHANNEL15_30')]
plan['comparator_scope']='Primary controls are same-funded EMA25/25,27/27,29/29 diagonals. Cash has0return. Older hold/SMA/pure-channel references keep original allocations and funding;not exposure/capital-matched alpha controls for this67.5/32.5batch.'
plan['reused_code_sha256']={str(p.relative_to(R)):sha(p) for p in [R/'research/experiments/20261005T214041Z/evaluate.py',R/'research/experiments/20261005T214041Z/signals.py',R/'research/experiments/20261007T083620Z/signals.py',R/'research/experiments/20261007T123850Z/signals.py',R/'research/experiments/20261001T133655Z/evaluate.py',R/'research/experiments/20261001T133655Z/kernel.py',R/'research/experiments/20261001T213902Z/audit.py',R/'research/experiments/20261001T213902Z/evaluate.py']}
(T/'spec.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
batch=[];grid=[]
def save(sp,fields,target):
 fp=registry.fingerprint(sp);assert fp not in canonical
 path=T/'specs'/f'{sp["name"]}.json';path.parent.mkdir(exist_ok=True);path.write_text(json.dumps(sp,indent=2)+'\n')
 x=subprocess.run([sys.executable,'research/automation/registry.py','reserve',str(path.relative_to(R))],cwd=R,capture_output=True,text=True);print(sp['name'],x.returncode,x.stdout.strip(),flush=True)
 if x.returncode:raise RuntimeError('STOP before calculation:'+x.stdout+x.stderr)
 b={'name':sp['name'],'fingerprint':fp,'spec':str(path.relative_to(R)),**fields};target.append(b);return b
def lookup(year,asset,span):
 x=components[year,asset,span];rec=x['record'];rp=R/rec['report'];assert rec['result_available'] and sha(rp)==rec['report_sha256'];row=next(c for c in json.loads(rp.read_text())['configs'].values() if c['fingerprint']==x['fingerprint']);capital=1350 if asset=='BTC' else 650
 assert json.loads((R/row['spec']).read_text())['parameters']['initial_capital_usdt']==capital
 return {'kind':'CHANNEL_EMA','name':row['name'],'report':str(rp.relative_to(R)),'report_sha256':sha(rp),'source_round':Path(row['archive']).parts[2],'fingerprint':x['fingerprint'],'archive':row['archive'],'archive_sha256':row['archive_sha256'],'spec':row['spec'],'capital_usdt':capital,'asset':asset}
for y in plan['periods']:
 template=next(c for c in source['configs'].values() if c.get('year')==y and c.get('role')=='combination' and c.get('span_days')==25 and c.get('entry_days')==15)
 for bs in plan['grid']['BTC_EMA_span_days']:
  for es in plan['grid']['ETH_EMA_span_days']:
   refs=[lookup(y,'BTC',bs),lookup(y,'ETH',es)];sp=copy.deepcopy(json.loads((R/template['spec']).read_text()));sp.update(name=f'mixed_ema_spans_{y}_btc{bs}_eth{es}_e15_x30_b0.03_btc0.675',family='channel-asset-specific-ema-confirmation',validation_plan=str((T/'spec.json').relative_to(R)));sp['components']=[{'fingerprint':ref['fingerprint'],'weight':w} for ref,w in zip(refs,(.675,.325))]
   fields={'year':y,'role':'combination','direction':'ASSET_SPECIFIC_EMA_CHANNEL_CONFIRMATION','BTC_EMA_span_days':bs,'ETH_EMA_span_days':es,'entry_days':15,'exit_days':30,'EMA_band':.03,'raw_weights':[.675,.325],'component_refs':refs};fp=registry.fingerprint(sp)
   if fp in canonical:
    assert bs==es;rec=canonical[fp];rp=R/rec['report'];assert rec['result_available'] and sha(rp)==rec['report_sha256'];old=next(c for c in json.loads(rp.read_text())['configs'].values() if c['fingerprint']==fp)
    b={**{k:old[k] for k in ('name','fingerprint','spec')},**fields,'is_new':False,'source_ref':{'report':rec['report'],'report_sha256':sha(rp),'archive':old['archive'],'archive_sha256':old['archive_sha256'],'source_round':Path(old['archive']).parts[2],'spec_sha256':sha(R/old['spec'])}};print('READ_ONLY_EXACT',b['name'],flush=True)
   else:assert bs!=es;b=save(sp,{**fields,'is_new':True},batch)
   grid.append(b)
assert len(batch)==12 and len(grid)==18 and len({r['fingerprint'] for b in grid for r in b['component_refs']})==12
(T/'batch.json').write_text(json.dumps(batch,indent=2)+'\n');(T/'grid_batch.json').write_text(json.dumps(grid,indent=2)+'\n')
forward=[];oldfb=json.loads((latest/'forward_batch.json').read_text());fps={}
for asset,capital in [('BTC',1500),('ETH',500)]:
 b=next(b for b in oldfb if b.get('asset')==asset);sp=json.loads((R/b['spec']).read_text());sp.update(name='forward_snapshot_'+asset,validation_plan=str((T/'spec.json').relative_to(R)));sp['parameters']['end_utc']=cutoff;fps[asset]=save(sp,{'asset':asset,'capital_usdt':capital},forward)['fingerprint']
sp=json.loads((R/oldfb[-1]['spec']).read_text());sp.update(name='forward_snapshot_combo',validation_plan=str((T/'spec.json').relative_to(R)));sp['parameters']['end_utc']=cutoff;sp['components']=[{'fingerprint':fps[a],'weight':w} for a,w in zip(('BTC','ETH'),(.75,.25))];save(sp,{'capital_usdt':2000},forward)
(T/'forward_batch.json').write_text(json.dumps(forward,indent=2)+'\n');print('PASS:12new portfolios+3legacy cutoffs reserved;6old diagonals and12funded components read-only.')
