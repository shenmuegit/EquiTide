"""Freeze a new funded-source combination grid and reserve every evaluation first."""
from pathlib import Path
from datetime import datetime, timezone
import copy, gzip, hashlib, json, subprocess, sys
R=Path(__file__).resolve().parents[3];T=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()))
assert sha(R/'research/automation/registry.jsonl')==prior['ledger_sha256']
canonical={registry.fingerprint(v['spec']):v for v in prior['records'].values()}
latest=R/'research/experiments/20261009T111450Z';base=json.loads((latest/'spec.json').read_text())
components={};pure={};ethchannel={}
for fp,rec in canonical.items():
 sp=rec['spec'];p=sp.get('parameters',{});asset=sp.get('universe',[''])[0].split('/')[0];year=p.get('start_utc','')[:4]
 if year not in ('2025','2026') or not p.get('end_utc','').endswith('-09-14T00:01:00Z'):continue
 vol=asset=='BTC' and sp['family']=='daily-close-range-relative-quote-volume' and p.get('initial_capital_usdt')==1500 and p.get('entry_lookback_days')==15 and p.get('exit_lookback_days')==30 and p.get('volume_lookback_days') in (20,30,40) and p.get('minimum_volume_ratio')==1
 asym=asset=='ETH' and sp['family']=='daily-sma-asymmetric-hysteresis' and p.get('initial_capital_usdt')==500 and p.get('lookback_days')==65 and p.get('entry_band_fraction') in (.0125,.015,.02) and p.get('exit_band_fraction')==.005
 if vol or asym:components[year,asset,p['volume_lookback_days'] if vol else p['entry_band_fraction']]=(fp,rec)
 if sp['family']=='daily-close-range-breakout' and p.get('entry_lookback_days')==15 and p.get('exit_lookback_days')==30:
  if asset=='BTC' and p.get('initial_capital_usdt')==1500:pure[year]=(fp,rec)
  if asset=='ETH' and p.get('initial_capital_usdt')==500:ethchannel[year]=(fp,rec)
assert len(components)==12 and len(pure)==len(ethchannel)==2
oldforward=json.loads((latest/'forward_report.json').read_text());state=json.loads((latest/'forward_state.json').read_text())
resume=oldforward['cutoff_utc'];cutoff='2026-10-09T13:00:00Z';event=state['next_daily_decision_utc'];parse=lambda x:datetime.fromisoformat(x.replace('Z','+00:00'))
minutes=int((parse(cutoff)-parse(resume)).total_seconds()/60);oldscene=oldforward['configs']['forward_snapshot_combo']['scenes']['1'];oldpoints=len(oldscene['equity_usdt']);totalminutes=oldscene['elapsed_minutes']+minutes
assert minutes==120 and parse(resume)<parse(cutoff)<parse(event) and parse(cutoff)<datetime.now(timezone.utc)
plan={k:copy.deepcopy(base[k]) for k in ('periods','execution','costs','gates','walk_forward','forward_plan')}
plan.update(round=T.name,trigger_utc='2026-10-09T13:14:50.541Z',actual_first_tool_utc='2026-10-09T13:14:58Z',frozen_at_utc=datetime.now(timezone.utc).isoformat(),hypothesis=json.loads((T/'preflight_notes.json').read_text())['direction'],
 grid={'directions':['BTC_VOLRATIO_ETH_ASMA'],'BTC_volume_lookback_days':[20,30,40],'BTC_minimum_volume_ratio':1,'BTC_channel_entry_days':15,'BTC_channel_exit_days':30,'ETH_SMA_entry_band':[.0125,.015,.02],'ETH_SMA_days':65,'ETH_SMA_exit_band':.005,'raw_weights':[.75,.25],'capital_usdt':2000,'component_capitals_usdt':[1500,500],'predeclared_center':{'BTC_volume_lookback_days':30,'ETH_SMA_entry_band':.015},'predeclared_focus':{'BTC_volume_lookback_days':30,'ETH_SMA_entry_band':.015}},
 rules_by_asset={a:copy.deepcopy(components['2026',a,axis][1]['spec']['logic']) for a,axis in [('BTC',30),('ETH',.015)]},
 allocation='Raw BTC/ETH75/25 initial1500/500USDT independent sleeves of2000. Sum already-costed absolute NAVs once on identical minute/execution axis;no normalization,second weighting,capital scaling,transfers or rebalance.',
 sensitivity='Independent BTC turnover reference20/30/40days and ETHSMA65 entry1.25/1.5/2percent;BTCturnover ratio1,ETHexit0.5percent fixed. Full3x3 each2025/2026,18newannual portfolios/54cost scenes;12source components read-only. All outcomes,folds,whole-minute/daily DD,Sharpe365,Calmar,12adjacent edges retained.',
 new_configs=18,new_cost_scenes=54,reused_grid_configs=0,reused_cost_scenes=0,full_grid_configs=18,reused_component_configs=12,prior_canonical_trials=prior['canonical'],development_history_reused=True,
 cross_period_confirmation='Identical BTC turnover lookback,ETH entry and original75/25 must pass each reused180day/sixfold period. No pooled years,untouched holdout or parameter selection on independent data.',
 qualification_scope='Original eight gates unchanged. Source components and controls retain existing status/criteria even if rejected. Every actual new parameter combination independently reserved/finished.',
 interpretation='Previously researched historical data,multiple selection bias,and possibly identical paths. Positive historical net returns do not establish stable live profit. P01-P10 frozen actual quote accounts unchanged.')
plan['walk_forward']['fit']='Fixed causal BTCclose-channel15/30 with prior quote-turnover>=precedingN mean and ETHDecimal28 SMA65 hysteresis. No new component signal/trade replay,no model/labels/perfold/OOS fitting. Original180day rolling history,3day gap,purge0,six continuous30day folds.'
plan['forward_plan']['status_at_freeze']='OriginalSMA65/1percent75/25 delayed shadow11:00 to13:00 closed marks only;nextdailyOct10UTC00:01. Separate paper10 actual quote observation22 untouched.'
plan['forward_resume']={'source_state':str((latest/'forward_state.json').relative_to(R)),'state_sha256':sha(latest/'forward_state.json'),'source_report':str((latest/'forward_report.json').relative_to(R)),'report_sha256':sha(latest/'forward_report.json'),'resume_utc':resume,'cutoff_utc':cutoff,'daily_decision_utc':event,'new_minutes':minutes,'cumulative_minutes':totalminutes,'prior_NAV_points':oldpoints,'new_reference_points':0,'total_NAV_points':oldpoints+minutes,'action':'Keep original positions,desired,costs and trades;append120closed minute marks,zero daily decisions,references or fills. Delayed shadow disclosed,not actual quote paper performance.','new_configs':3,'new_cost_scenes':9}
template=json.loads((R/'research/experiments/20261002T195003Z/specs/channel_asma_2026_BTC_CHANNEL_ETH_ASMA_e0.015_d15.json').read_text())
volume_template=json.loads((R/'research/experiments/20261009T091020Z/specs/volratio_channel_2026_n30_r1_btc0.75.json').read_text())
def parent(template,year,btc,eth):
 sp=copy.deepcopy(template);sp['parameters']['start_utc']=btc[1]['spec']['parameters']['start_utc'];sp['parameters']['end_utc']=btc[1]['spec']['parameters']['end_utc'];sp['components']=[{'fingerprint':btc[0],'weight':.75},{'fingerprint':eth[0],'weight':.25}];return sp
def source_ref(year,asset,axis):
 fp,rec=components[year,asset,axis];rp=R/rec['report'];assert rec['result_available'] and sha(rp)==rec['report_sha256']
 row=next(c for c in json.loads(rp.read_text())['configs'].values() if c['fingerprint']==fp);capital=1500 if asset=='BTC' else 500
 assert json.loads((R/row['spec']).read_text())==rec['spec'] and rec['spec']['parameters']['initial_capital_usdt']==capital and sha(R/row['archive'])==row['archive_sha256']
 return {'kind':'VOLRATIO' if asset=='BTC' else 'ASMA','name':row['name'],'report':rec['report'],'report_sha256':sha(rp),'source_round':Path(row['archive']).parts[2],'fingerprint':fp,'archive':row['archive'],'archive_sha256':row['archive_sha256'],'spec':row['spec'],'capital_usdt':capital,'asset':asset}
plan['read_only_comparator_refs']=[copy.deepcopy(v) for v in base['read_only_comparator_refs'] if v['kind']=='SMA_or_hold']
for year in ('2025','2026'):
 for kind,axes in [('MATCHED_CHANNEL_ASMA',(.0125,.015,.02)),('MATCHED_VOL_CHANNEL',(20,30,40))]:
  for axis in axes:
   sp=parent(template,year,pure[year],components[year,'ETH',axis]) if kind=='MATCHED_CHANNEL_ASMA' else parent(volume_template,year,components[year,'BTC',axis],ethchannel[year])
   fp=registry.fingerprint(sp);rec=canonical[fp];rp=R/rec['report'];assert rec['result_available'] and sha(rp)==rec['report_sha256'];row=next(c for c in json.loads(rp.read_text())['configs'].values() if c['fingerprint']==fp)
   plan['read_only_comparator_refs'].append({'name':row['name'],'fingerprint':fp,'year':year,'kind':kind,'ETH_SMA_entry_band':axis if kind=='MATCHED_CHANNEL_ASMA' else None,'BTC_volume_lookback_days':axis if kind=='MATCHED_VOL_CHANNEL' else None,'report':rec['report'],'report_sha256':sha(rp)})
plan['comparator_scope']='Two matched axes:A sameETH SMAentry and funds,unfilteredBTC15/30;B sameBTC turnover lookback and funds,ETH15/30channel. Existing SMA/hold context and cash0 read-only. Compare full costs/whole DD in both years;retain all old criteria/status.'
paths=[R/'research/experiments/20261001T133655Z/evaluate.py',R/'research/experiments/20261001T133655Z/kernel.py',R/'research/experiments/20261001T213902Z/audit.py',R/'research/experiments/20261001T213902Z/evaluate.py',R/'research/experiments/20261001T013355Z/evaluate.py',R/'research/experiments/20261001T113625Z/signals.py',R/'research/experiments/20261002T094655Z/signals.py',R/'research/experiments/20261009T091020Z/signals.py',R/'research/automation/registry.py']
plan['reused_code_sha256']={str(p.relative_to(R)):sha(p) for p in paths};plan['preflight_sha256']=sha(T/'preflight.py')
assert not (T/'spec.json').exists();(T/'spec.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
batch=[];grid=[]
def save(sp,fields,target):
 fp=registry.fingerprint(sp);assert fp not in canonical
 path=T/'specs'/f'{sp["name"]}.json';path.parent.mkdir(exist_ok=True);assert not path.exists();path.write_text(json.dumps(sp,indent=2)+'\n')
 x=subprocess.run([sys.executable,'research/automation/registry.py','reserve',str(path.relative_to(R))],cwd=R,capture_output=True,text=True);print(sp['name'],x.returncode,x.stdout.strip(),flush=True)
 if x.returncode:raise RuntimeError('STOP before calculation:'+x.stdout+x.stderr)
 row={'name':sp['name'],'fingerprint':fp,'spec':str(path.relative_to(R)),**fields};target.append(row);return row
for year in plan['periods']:
 for n in plan['grid']['BTC_volume_lookback_days']:
  for entry in plan['grid']['ETH_SMA_entry_band']:
   refs=[source_ref(year,'BTC',n),source_ref(year,'ETH',entry)];sp=parent(template,year,components[year,'BTC',n],components[year,'ETH',entry])
   sp.update(name=f'volratio_asma_{year}_btc_n{n}_r1_eth_e{entry}_x0.005_btc0.75',family='volume-channel-asymmetric-sma-initial-capital',validation_plan=str((T/'spec.json').relative_to(R)))
   row=save(sp,{'year':year,'role':'combination','direction':'BTC_VOLRATIO_ETH_ASMA','BTC_volume_lookback_days':n,'ETH_SMA_entry_band':entry,'raw_weights':[.75,.25],'component_refs':refs,'is_new':True},batch);grid.append(row)
assert len(batch)==len(grid)==18 and len({r['fingerprint']for b in grid for r in b['component_refs']})==12
(T/'batch.json').write_text(json.dumps(batch,indent=2)+'\n');(T/'grid_batch.json').write_text(json.dumps(grid,indent=2)+'\n')
forward=[];oldfb=json.loads((latest/'forward_batch.json').read_text());fps={}
for asset,capital in [('BTC',1500),('ETH',500)]:
 b=next(b for b in oldfb if b.get('asset')==asset);sp=json.loads((R/b['spec']).read_text());sp.update(name='forward_snapshot_'+asset,validation_plan=str((T/'spec.json').relative_to(R)));sp['parameters']['end_utc']=cutoff;fps[asset]=save(sp,{'asset':asset,'capital_usdt':capital},forward)['fingerprint']
sp=json.loads((R/oldfb[-1]['spec']).read_text());sp.update(name='forward_snapshot_combo',validation_plan=str((T/'spec.json').relative_to(R)));sp['parameters']['end_utc']=cutoff;sp['components']=[{'fingerprint':fps[a],'weight':w}for a,w in zip(('BTC','ETH'),(.75,.25))];save(sp,{'capital_usdt':2000},forward)
(T/'forward_batch.json').write_text(json.dumps(forward,indent=2)+'\n');print('PASS:18new portfolios+3legacy cutoffs reserved;12exact-funded components and12matched controls read-only.')
