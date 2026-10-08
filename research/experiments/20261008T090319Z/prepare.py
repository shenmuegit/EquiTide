"""Freeze independent BTC/ETH entry windows; reuse exact funded source evidence."""
import copy,gzip,hashlib,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
R=Path(__file__).resolve().parents[3];T=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
records=registry.read_records(R/'research/automation/registry.jsonl');canonical={registry.fingerprint(v['spec']):v for v in records.values()}
prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()))
assert sha(R/'research/automation/registry.jsonl')==prior['ledger_sha256'] and len(canonical)==prior['canonical']
latest=R/'research/experiments/20261008T070227Z';base=json.loads((latest/'spec.json').read_text())
rp=R/'research/experiments/20261002T174933Z/report.json';source=json.loads(rp.read_text())
example=next(c for c in source['configs'].values() if c['role']=='component');csp=json.loads((R/example['spec']).read_text())
oldforward=json.loads((latest/'forward_report.json').read_text());oldstate=json.loads((latest/'forward_state.json').read_text())
cutoff='2026-10-08T09:00:00Z';parse=lambda t:datetime.fromisoformat(t.replace('Z','+00:00'))
resume=oldforward['cutoff_utc'];newminutes=int((parse(cutoff)-parse(resume)).total_seconds()/60)
assert newminutes==120 and parse(cutoff)<parse(oldstate['next_daily_decision_utc']) and parse(cutoff)<datetime.now(timezone.utc)
oldscene=oldforward['configs']['forward_snapshot_combo']['scenes']['1'];oldpoints=len(oldscene['equity_usdt']);totalminutes=oldscene['elapsed_minutes']+newminutes
plan={k:copy.deepcopy(base[k]) for k in ('periods','execution','costs','gates','walk_forward','forward_plan')}
plan.update(round=T.name,trigger_utc='2026-10-08T09:03:19.466Z',actual_first_tool_utc='2026-10-08T09:03:27Z',frozen_at_utc=datetime.now(timezone.utc).isoformat(),
 hypothesis='The previous independent-fast-exit grid failed cross-period gates. Freeze both exit windows30 and independently vary BTC/ETH entry10/15/20. Earlier minority ETH entry may capture trends before slower dominant BTC while asynchronous entry timing may diversify whipsaw risk,or increase churn. Focus BTCentry15/ETHentry10 is declared before calculating new portfolios. Only4off-diagonal annual portfolios are new;14exact historical cells and12funded components remain read-only.',
 grid={'BTC_entry_days':[10,15,20],'BTC_exit_days':30,'ETH_entry_days':[10,15,20],'ETH_exit_days':30,'directions':['BTC_EARLY_CHANNEL_ETH_EARLY_CHANNEL'],'raw_weights':[.75,.25],'capital_usdt':2000,'component_capitals_usdt':[1500,500],'predeclared_center':{'BTC_entry_days':15,'ETH_entry_days':10},'read_only_anchor':{'BTC_entry_days':15,'ETH_entry_days':15}},
 rules=csp['logic'],channel_definition=csp['parameters']['channel_definition'],
 allocation='Raw BTC/ETH75/25 denotes initial1500/500USDT independent sleeves of2000. Sum same-size costed absolute NAV once;no normalization,second weighting,transfers,maintained ratio or rebalance. Exit30 fixed in both;entry windows10/15/20 independent.',
 sensitivity='Two reused-year3x3 surfaces vary BTCentry and ETHentry10/15/20 simultaneously with exit30 fixed.4new exact portfolios reserved before calculation;14existing cells read-only. All1/2/3costs,folds,return,minute/daily drawdown,Sharpe,Calmar and12adjacent edges per surface retained.',
 new_configs=4,new_cost_scenes=12,reused_grid_configs=14,reused_cost_scenes=42,full_grid_configs=18,reused_component_configs=12,prior_canonical_trials=prior['canonical'],development_history_reused=True,
 cross_period_confirmation='Identical BTCentry/ETHentry,exit30 and75/25funding must pass EACH reused180day/sixfold period independently. No pooling,final holdout or new market data.',
 qualification_scope='Original eight gates unchanged. All exact historical cells preserve original records/status/criteria. All4new variants plus3legacy cutoffs independently registered.',
 interpretation='Repeated development history and many trials;new entry assignments are not independent market evidence,statistical significance or stable live profit. No fixed-paper portfolio replacement.',
 component_report_rounds={'BTC':'20261002T174933Z','ETH':'20261002T174933Z'},
 knowledge_sources=[{'url':'https://github.com/binance/binance-public-data','access_date_utc':'2026-10-08','scope':'Official archive format,spot timestamps microseconds since2025,checksums and archive revision warning. Same-SHA four cached normalized minute data files used,not redownloaded.'},{'url':'https://data-api.binance.vision/api/v3/klines','scope':'Completed-minute public GET for separate legacy delayed shadow only,not paper10 fills'}])
plan['walk_forward']['fit']='Fixed causal close-channel rules,no labels/model fit/perfold or OOS retuning;180day rolling history,3day gap,purge0,six30day diagnostic folds. Continuous balances and desired across folds;costed final exit.'
plan['forward_plan']['status_at_freeze']='Original SMA65/1percent75/25 delayed shadow collecting. Next decision Oct9UTC00:01. Original positions/trades/costs and actual-quote paper10 accounts remain separate and unchanged.'
plan['forward_resume']={'source_state':str((latest/'forward_state.json').relative_to(R)),'state_sha256':sha(latest/'forward_state.json'),'source_report':str((latest/'forward_report.json').relative_to(R)),'report_sha256':sha(latest/'forward_report.json'),'resume_utc':resume,'cutoff_utc':cutoff,'new_minutes':newminutes,'cumulative_minutes':totalminutes,'prior_NAV_points':oldpoints,'new_reference_points':0,'total_NAV_points':oldpoints+newminutes,'action':f'Append{newminutes}closed-minute legacy marks only;no daily reference,decision,fill,cost or forced exit. Exact original positions and NAV prefix preserved;paper10 remains separate.','new_configs':3,'new_cost_scenes':9,'qualification':f'Only{totalminutes}minutes/{totalminutes//1440}complete days of delayed shadow;not180days/sixfold or paper10 contemporaneous performance.'}
plan['read_only_comparator_refs']=base['read_only_comparator_refs']
plan['reused_code_sha256']={str(p.relative_to(R)):sha(p) for p in [R/'research/experiments/20261002T174933Z/evaluate.py',R/'research/experiments/20261002T174933Z/signals.py',R/'research/experiments/20261001T133655Z/evaluate.py',R/'research/experiments/20261001T133655Z/kernel.py',R/'research/experiments/20261001T213902Z/audit.py',R/'research/experiments/20261001T213902Z/evaluate.py']}
(T/'spec.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
batch=[];grid=[]
def save(sp,fields,target):
 fp=registry.fingerprint(sp);assert fp not in canonical
 path=T/'specs'/f'{sp["name"]}.json';path.parent.mkdir(exist_ok=True);path.write_text(json.dumps(sp,indent=2)+'\n')
 x=subprocess.run([sys.executable,'research/automation/registry.py','reserve',str(path.relative_to(R))],cwd=R,capture_output=True,text=True)
 print(sp['name'],x.returncode,x.stdout.strip(),flush=True)
 if x.returncode:raise RuntimeError('STOP before calculation:'+x.stdout+x.stderr)
 b={'name':sp['name'],'fingerprint':fp,'spec':str(path.relative_to(R)),**fields};target.append(b);return b
for y in plan['periods']:
 template=next(c for c in source['configs'].values() if c['year']==y and c['role']=='combination' and c['entry_days']==20 and c['exit_days']==30)
 def lookup(asset,entry):
  matches=[c for c in source['configs'].values() if c['year']==y and c['role']=='component' and c['asset']==asset and c['entry_days']==entry and c['exit_days']==30];assert len(matches)==1;c=matches[0];path=c.get('spec_path',c.get('spec'));capital=1500 if asset=='BTC' else 500
  assert records[c['fingerprint']]['result_available'] and json.loads((R/path).read_text())['parameters']['initial_capital_usdt']==capital
  return {'kind':'CHANNEL','name':c['name'],'report':str(rp.relative_to(R)),'report_sha256':sha(rp),'source_round':Path(c['archive']).parts[2],'fingerprint':c['fingerprint'],'archive':c['archive'],'archive_sha256':c['archive_sha256'],'spec':path,'capital_usdt':capital,'asset':asset}
 for bx in plan['grid']['BTC_entry_days']:
  for ex in plan['grid']['ETH_entry_days']:
   refs=[lookup('BTC',bx),lookup('ETH',ex)];sp=copy.deepcopy(json.loads((R/template['spec']).read_text()));sp.update(name=f'mixed_entry_channel_{y}_btc{bx}_x30_eth{ex}_x30',family='close-channel-mixed-horizons-initial-capital',validation_plan=str((T/'spec.json').relative_to(R)));sp['components']=[{'fingerprint':ref['fingerprint'],'weight':w} for ref,w in zip(refs,(.75,.25))]
   fields={'year':y,'role':'combination','direction':'BTC_EARLY_CHANNEL_ETH_EARLY_CHANNEL','BTC_exit_days':30,'BTC_entry_days':bx,'ETH_exit_days':30,'ETH_entry_days':ex,'raw_weights':[.75,.25],'component_refs':refs};fp=registry.fingerprint(sp)
   if fp in canonical:
    rec=canonical[fp];oldrp=R/rec['report'];assert rec['result_available'] and sha(oldrp)==rec['report_sha256'];prev=next(c for c in json.loads(oldrp.read_text())['configs'].values() if c['fingerprint']==fp)
    b={**{k:prev[k] for k in ('name','fingerprint','spec')},**fields,'is_new':False,'source_ref':{'report':rec['report'],'report_sha256':sha(oldrp),'archive':prev['archive'],'archive_sha256':prev['archive_sha256'],'source_round':Path(prev['archive']).parts[2],'spec_sha256':sha(R/prev['spec'])}};print('READ_ONLY_EXACT',b['name'],flush=True)
   else:
    assert (bx,ex) in ((10,15),(15,10));b=save(sp,{**fields,'is_new':True},batch)
   grid.append(b)
assert len(batch)==4 and len(grid)==18 and len({r['fingerprint'] for b in grid for r in b['component_refs']})==12
(T/'batch.json').write_text(json.dumps(batch,indent=2)+'\n');(T/'grid_batch.json').write_text(json.dumps(grid,indent=2)+'\n')
forward=[];oldfb=json.loads((latest/'forward_batch.json').read_text());fps={}
for asset,capital in [('BTC',1500),('ETH',500)]:
 b=next(b for b in oldfb if b.get('asset')==asset);sp=json.loads((R/b['spec']).read_text());sp.update(name='forward_snapshot_'+asset,validation_plan=str((T/'spec.json').relative_to(R)));sp['parameters']['end_utc']=cutoff;fps[asset]=save(sp,{'asset':asset,'capital_usdt':capital},forward)['fingerprint']
sp=json.loads((R/oldfb[-1]['spec']).read_text());sp.update(name='forward_snapshot_combo',validation_plan=str((T/'spec.json').relative_to(R)));sp['parameters']['end_utc']=cutoff;sp['components']=[{'fingerprint':fps[a],'weight':w} for a,w in zip(('BTC','ETH'),(.75,.25))];save(sp,{'capital_usdt':2000},forward)
(T/'forward_batch.json').write_text(json.dumps(forward,indent=2)+'\n');print('PASS:4new portfolios+3legacy cutoffs reserved;14exact grid cells and12funded components read-only.')
