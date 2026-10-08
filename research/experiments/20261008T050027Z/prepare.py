"""Freeze mixed BTC/ETH close-channel horizons, reusing exact funded components."""
import copy,gzip,hashlib,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
R=Path(__file__).resolve().parents[3];T=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ledger=R/'research/automation/registry.jsonl';records=registry.read_records(ledger);canonical={registry.fingerprint(v['spec']):v for v in records.values()}
prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));assert sha(ledger)==prior['ledger_sha256'] and len(canonical)==prior['canonical']
latest=R/'research/experiments/20261008T025926Z';base=json.loads((latest/'spec.json').read_text());brp=R/'research/experiments/20261002T154903Z/report.json';erp=R/'research/experiments/20261002T174933Z/report.json';btc=json.loads(brp.read_text());eth=json.loads(erp.read_text())
example=next(c for c in btc['configs'].values() if c['role']=='component');csp=json.loads((R/example['spec']).read_text())
plan={k:copy.deepcopy(base[k]) for k in ('periods','execution','costs','gates','walk_forward','forward_plan')}
plan.update(round=T.name,trigger_utc='2026-10-08T05:00:27.065Z',actual_first_tool_utc=None,frozen_at_utc=datetime.now(timezone.utc).isoformat(),
 hypothesis='The previous different-horizon grid varied the dominant BTC exit and minority ETH entry. Test the economically different reverse assignment: dominant BTC retains exit30 while its entry varies10/15/20,minority ETH fixes entry20 with exit10/20/30. Faster ETH exits may reduce choppy minority exposure while preserving slower BTC trends,or reduce useful diversification. Freeze the complete two-year grid before calculating portfolio results. Exact1500/500USDT already-costed sleeves only;no capital scaling,new source signals or test-set retuning.',
 grid={'BTC_entry_days':[10,15,20],'BTC_exit_days':30,'ETH_entry_days':20,'ETH_exit_days':[10,20,30],'directions':['BTC_SLOW_CHANNEL_ETH_FAST_CHANNEL'],'raw_weights':[.75,.25],'capital_usdt':2000,'component_capitals_usdt':[1500,500],'predeclared_center':{'BTC_entry_days':15,'ETH_exit_days':20},'read_only_anchor':{'BTC_entry_days':20,'ETH_exit_days':30}},
 rules=csp['logic'],channel_definition=csp['parameters']['channel_definition'],
 allocation='Raw BTC/ETH75/25 denotes initial1500/500USDT independent sleeves of2000. Sum exact-size costed absolute NAVs once;no second weighting,normalization,transfers,maintained ratio or rebalance. BTC and ETH entry/exit horizons are independent as declared.',
 sensitivity='Two historical-year3x3 surfaces vary BTC entry10/15/20 and ETH exit10/20/30 simultaneously. BTC exit30 and ETH entry20 fixed.16new exact portfolios reserved before evaluation;2existing both20/30 anchors read-only. All costs,folds,return,minute/daily drawdown,Sharpe,Calmar and adjacent differences retained.',
 new_configs=16,new_cost_scenes=48,reused_grid_configs=2,reused_cost_scenes=6,full_grid_configs=18,reused_component_configs=12,prior_canonical_trials=prior['canonical'],development_history_reused=True,
 cross_period_confirmation='Identical BTCentry,ETHexit,fixedBTCexit30/ETHentry20 and75/25funding must pass EACH reused180day/sixfold period separately;no pooled-year account or untouched final test.',
 qualification_scope='Original eight gates unchanged. Exact prior anchors preserve their original records/status/criteria. All trials and repeated historical selection disclosed.',
 interpretation='Both years repeatedly used for development. New mixed horizons are not independent market evidence,untouched final holdout,statistical significance or stable live profit.',
 component_report_rounds={'BTC':'20261002T174933Z','ETH':'20261002T154903Z'},
 knowledge_sources=[{'url':'https://github.com/binance/binance-public-data','scope':'Same-SHA cached official spot archive;all four normalized data files rechecked'},{'url':'https://data-api.binance.vision/api/v3/klines','scope':'Actual completed-minute public HTTP responses for legacy shadow only;not paper10 actual-quote fills'}])
plan['walk_forward']['fit']='Fixed causal asset-specific close-channel rules,no fit/labels/per-fold or OOS tuning;180day rolling history,3gap,purge0,six continuous30day diagnostics. OOS starts cash;balances and desired cross fold boundaries.'
plan['forward_plan']['status_at_freeze']='Original SMA65/1percent75/25 shadow collecting;Oct8UTC00:01 processed,positions continue,next Oct9UTC00:01. Independent actual-quote paper10 accounts untouched.'
plan['forward_resume']={'source_state':str((latest/'forward_state.json').relative_to(R)),'state_sha256':sha(latest/'forward_state.json'),'source_report':str((latest/'forward_report.json').relative_to(R)),'report_sha256':sha(latest/'forward_report.json'),'resume_utc':'2026-10-08T02:50:00Z','cutoff_utc':'2026-10-08T04:50:00Z','new_minutes':120,'cumulative_minutes':8929,'prior_NAV_points':8817,'new_reference_points':0,'total_NAV_points':8937,'action':'Append120closed-minute legacy marks only,no new daily reference/decision/fill,cost or forced exit. Keep exact original positions and prior NAV prefix;paper10 real-quote state remains separate.','new_configs':3,'new_cost_scenes':9,'qualification':'Legacy8929minute delayed shadow,6complete days,not180day/sixfold or paper10 forward performance.'}
plan['read_only_comparator_refs']=[x for x in base['read_only_comparator_refs'] if x['kind'] in ('SMA_or_hold','CHANNEL15_30')]
for y in plan['periods']:
 c=next(c for c in btc['configs'].values() if c['year']==y and c['role']=='combination' and c['entry_days']==20 and c['exit_days']==30)
 plan['read_only_comparator_refs'].append({'name':c['name'],'year':y,'kind':'CHANNEL20_30','report':str(brp.relative_to(R)),'report_sha256':sha(brp)})
plan['reused_code_sha256']={str(p.relative_to(R)):sha(p) for p in [R/'research/experiments/20261002T154903Z/evaluate.py',R/'research/experiments/20261002T174933Z/evaluate.py',R/'research/experiments/20261002T154903Z/signals.py',R/'research/experiments/20261001T133655Z/evaluate.py',R/'research/experiments/20261001T133655Z/kernel.py',R/'research/experiments/20261001T213902Z/audit.py',R/'research/experiments/20261001T213902Z/evaluate.py']}
(T/'spec.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
batch=[];grid=[]
def save(sp,fields,target):
 fp=registry.fingerprint(sp);assert fp not in canonical
 path=T/'specs'/f'{sp["name"]}.json';path.parent.mkdir(exist_ok=True);path.write_text(json.dumps(sp,indent=2)+'\n')
 x=subprocess.run([sys.executable,'research/automation/registry.py','reserve',str(path.relative_to(R))],cwd=R,capture_output=True,text=True);print(sp['name'],x.returncode,x.stdout.strip(),flush=True)
 if x.returncode:raise RuntimeError('STOP before calculation:'+x.stdout+x.stderr)
 b={'name':sp['name'],'fingerprint':fp,'spec':str(path.relative_to(R)),**fields};target.append(b);return b
for y in plan['periods']:
 template=next(c for c in btc['configs'].values() if c['year']==y and c['role']=='combination' and c['entry_days']==20 and c['exit_days']==30)
 def lookup(asset,entry,exit):
  report,rp=(eth,erp) if asset=='BTC' else (btc,brp)
  m=[c for c in report['configs'].values() if c['year']==y and c['role']=='component' and c['asset']==asset and c['entry_days']==entry and c['exit_days']==exit];assert len(m)==1;c=m[0];path=c.get('spec_path',c.get('spec'));capital=1500 if asset=='BTC' else 500
  assert records[c['fingerprint']]['result_available'] and json.loads((R/path).read_text())['parameters']['initial_capital_usdt']==capital
  return {'kind':'CHANNEL','name':c['name'],'report':str(rp.relative_to(R)),'report_sha256':sha(rp),'source_round':Path(c['archive']).parts[2],'fingerprint':c['fingerprint'],'archive':c['archive'],'archive_sha256':c['archive_sha256'],'spec':path,'capital_usdt':capital,'asset':asset}
 for x in plan['grid']['ETH_exit_days']:
  for e in plan['grid']['BTC_entry_days']:
   refs=[lookup('BTC',e,30),lookup('ETH',20,x)];sp=copy.deepcopy(json.loads((R/template['spec']).read_text()));sp.update(name=f'mixed_channel_reverse_{y}_btc{e}_x30_eth20_x{x}',family='close-channel-mixed-horizons-initial-capital',validation_plan=str((T/'spec.json').relative_to(R)));sp['components']=[{'fingerprint':r['fingerprint'],'weight':w} for r,w in zip(refs,(.75,.25))]
   fields={'year':y,'role':'combination','direction':'BTC_SLOW_CHANNEL_ETH_FAST_CHANNEL','ETH_exit_days':x,'BTC_entry_days':e,'raw_weights':[.75,.25],'component_refs':refs};fp=registry.fingerprint(sp)
   if fp in canonical:
    assert (x,e)==(30,20);rec=canonical[fp];rp=R/rec['report'];assert rec['result_available'] and sha(rp)==rec['report_sha256'];prev=next(c for c in json.loads(rp.read_text())['configs'].values() if c['fingerprint']==fp)
    b={**{k:prev[k] for k in ('name','fingerprint','spec')},**fields,'is_new':False,'source_ref':{'report':rec['report'],'report_sha256':sha(rp),'archive':prev['archive'],'archive_sha256':prev['archive_sha256'],'source_round':Path(prev['archive']).parts[2],'spec_sha256':sha(R/prev['spec'])}};print('READ_ONLY_EXACT',b['name'],flush=True)
   else:b=save(sp,{**fields,'is_new':True},batch)
   grid.append(b)
assert len(batch)==16 and len(grid)==18 and len({r['fingerprint'] for b in grid for r in b['component_refs']})==12
(T/'batch.json').write_text(json.dumps(batch,indent=2)+'\n');(T/'grid_batch.json').write_text(json.dumps(grid,indent=2)+'\n')
forward=[];oldfb=json.loads((latest/'forward_batch.json').read_text());fps={}
for asset,capital in [('BTC',1500),('ETH',500)]:
 b=next(b for b in oldfb if b.get('asset')==asset);sp=json.loads((R/b['spec']).read_text());sp.update(name='forward_snapshot_'+asset,validation_plan=str((T/'spec.json').relative_to(R)));sp['parameters']['end_utc']=plan['forward_resume']['cutoff_utc'];fps[asset]=save(sp,{'asset':asset,'capital_usdt':capital},forward)['fingerprint']
sp=json.loads((R/oldfb[-1]['spec']).read_text());sp.update(name='forward_snapshot_combo',validation_plan=str((T/'spec.json').relative_to(R)));sp['parameters']['end_utc']=plan['forward_resume']['cutoff_utc'];sp['components']=[{'fingerprint':fps[a],'weight':w} for a,w in zip(('BTC','ETH'),(.75,.25))];save(sp,{'capital_usdt':2000},forward)
(T/'forward_batch.json').write_text(json.dumps(forward,indent=2)+'\n');print('PASS:16new mixed-channel portfolios+3legacy cutoffs reserved;2exact anchors and12size-matched sleeves read-only.')
