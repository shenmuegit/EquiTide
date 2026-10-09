"""Freeze BTC asymmetric-SMA / ETH filtered-channel configurations before calculation."""
from pathlib import Path
from datetime import datetime,timezone
import copy,gzip,hashlib,json,subprocess,sys
R=Path(__file__).resolve().parents[3];T=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
records=registry.read_records(R/'research/automation/registry.jsonl');canonical={registry.fingerprint(v['spec']):v for v in records.values()}
prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));assert sha(R/'research/automation/registry.jsonl')==prior['ledger_sha256']
latest=R/'research/experiments/20261009T010850Z';base=json.loads((latest/'spec.json').read_text());components={}
for fp,rec in canonical.items():
 sp=rec['spec'];p=sp.get('parameters',{});asset=sp.get('universe',[''])[0].split('/')[0]
 filtered=asset=='ETH' and sp['family']=='daily-channel-ema-confirmation' and p.get('initial_capital_usdt')==500 and p.get('entry_lookback_days')==15 and p.get('exit_lookback_days')==30 and p.get('EMA_symmetric_band')==.015 and p.get('EMA_span_days') in (50,65,80)
 asym=asset=='BTC' and sp['family']=='daily-sma-asymmetric-hysteresis' and p.get('initial_capital_usdt')==1500 and p.get('lookback_days')==65 and p.get('entry_band_fraction') in (.0125,.015,.02) and p.get('exit_band_fraction')==.005
 if (filtered or asym) and p.get('start_utc','')[:4] in ('2025','2026') and p.get('end_utc','').endswith('-09-14T00:01:00Z'):
  axis=p['EMA_span_days'] if filtered else p['entry_band_fraction'];components[p['start_utc'][:4],asset,axis]=(fp,rec)
assert len(components)==12
oldforward=json.loads((latest/'forward_report.json').read_text());state=json.loads((latest/'forward_state.json').read_text());resume=oldforward['cutoff_utc'];cutoff='2026-10-09T03:00:00Z';event=state['next_daily_decision_utc'];parse=lambda s:datetime.fromisoformat(s.replace('Z','+00:00'))
minutes=int((parse(cutoff)-parse(resume)).total_seconds()/60);oldscene=oldforward['configs']['forward_snapshot_combo']['scenes']['1'];oldpoints=len(oldscene['equity_usdt']);totalminutes=oldscene['elapsed_minutes']+minutes
assert minutes==120 and parse(resume)<parse(cutoff)<parse(event) and parse(cutoff)<datetime.now(timezone.utc)
plan={k:copy.deepcopy(base[k]) for k in ('periods','execution','costs','gates','walk_forward','forward_plan')}
plan.update(round=T.name,trigger_utc='2026-10-09T03:09:20.186Z',actual_first_tool_utc='2026-10-09T03:09:26Z',frozen_at_utc=datetime.now(timezone.utc).isoformat(),hypothesis=json.loads((T/'preflight_notes.json').read_text())['direction'],
 grid={'directions':['BTC_ASMA_ETH_FILTERED'],'ETH_EMA_span_days':[50,65,80],'BTC_SMA_entry_band':[.0125,.015,.02],'ETH_channel_entry_days':15,'ETH_channel_exit_days':30,'ETH_EMA_symmetric_band':.015,'BTC_SMA_days':65,'BTC_SMA_exit_band':.005,'raw_weights':[.75,.25],'capital_usdt':2000,'component_capitals_usdt':[1500,500],'predeclared_center':{'ETH_EMA_span_days':65,'BTC_SMA_entry_band':.015},'predeclared_focus':{'ETH_EMA_span_days':65,'BTC_SMA_entry_band':.015}},
 rules_by_asset={a:copy.deepcopy(components['2026',a,axis][1]['spec']['logic']) for a,axis in [('BTC',.015),('ETH',65)]},
 allocation='Original BTC/ETH75/25 means initial1500/500USDT independent sleeves of2000. Sum exact-capital already-costed absolute NAVs once;no normalization,second weighting,maintained ratio,transfers or rebalance.',
 sensitivity='ETH filtered-channel EMA span50/65/80 and BTC asymmetricSMA65 entry1.25/1.5/2percent,exit0.5percent. Full3x3 each2025/2026,all18annual configurations are new;12exact funded components read-only. Preserve full cost scenes,folds,minute/daily drawdowns,Sharpe/Calmar and12adjacent edges.',
 new_configs=18,new_cost_scenes=54,reused_grid_configs=0,reused_cost_scenes=0,full_grid_configs=18,reused_component_configs=12,prior_canonical_trials=prior['canonical'],development_history_reused=True,
 cross_period_confirmation='Identical ETH EMAspan/BTC entrythreshold and original75/25 must pass each reused180day/sixfold period. No pooled years or untouched holdout;any new path is not an independent market sample.',
 qualification_scope='Original eight gates unchanged;all18annual configurations independently reserved/finished. Existing source and comparator statuses/criteria preserved.',
 interpretation='Repeated history and many trials;positive historical net returns do not establish stable live profit. FrozenP01-P10 actual-quote accounts remain unchanged.',
 knowledge_sources=[{'url':'https://github.com/binance/binance-public-data','access_date_utc':'2026-10-09','scope':'Official spot archive timestamps/checksums/revisions;reuse same-SHA cached real minute data,no archive version change.'},{'url':'https://data-api.binance.vision/api/v3/klines','scope':'Only publicGET closed-minute/daily inputs for separate original delayed shadow;not paper10 actual-quote fills.'}])
plan['walk_forward']['fit']='Fixed causal rules;ETH EMA Pythonfloat adjustFalse seeded at datasetday0 and continuous across folds;BTC Decimal28 SMA65 includes tested completed close. No model,labels,per-fold/OOS fitting.180day rolling history,3day gap,purge0,six continuous30day diagnostic folds.'
plan['forward_plan']['status_at_freeze']='OriginalSMA65/1percent75/25 delayed shadow appends marks before nextdailyOct10UTC00:01;paper10 actual-quote accounts are separate.'
plan['forward_resume']={'source_state':str((latest/'forward_state.json').relative_to(R)),'state_sha256':sha(latest/'forward_state.json'),'source_report':str((latest/'forward_report.json').relative_to(R)),'report_sha256':sha(latest/'forward_report.json'),'resume_utc':resume,'cutoff_utc':cutoff,'next_daily_decision_utc':event,'new_minutes':minutes,'cumulative_minutes':totalminutes,'prior_NAV_points':oldpoints,'new_reference_points':0,'total_NAV_points':oldpoints+minutes,'action':'Carry all original positions,costs,desired/trades;append120closed marks only,no new daily reference,decision,fill,cost,restart or forced exit. Delayed shadow disclosed;paper10 unchanged.','new_configs':3,'new_cost_scenes':9,'qualification':f'Only{totalminutes}minutes/{totalminutes//1440}complete days of delayed shadow;not180day/sixfold or paper10 performance.'}
template=json.loads((R/'research/experiments/20261002T195003Z/specs/channel_asma_2026_BTC_ASMA_ETH_CHANNEL_e0.015_d15.json').read_text())
def source_ref(year,asset,axis):
 fp,rec=components[year,asset,axis];rp=R/rec['report'];assert rec['result_available'] and sha(rp)==rec['report_sha256']
 row=next(c for c in json.loads(rp.read_text())['configs'].values() if c['fingerprint']==fp);capital=1500 if asset=='BTC' else 500
 assert json.loads((R/row['spec']).read_text())==rec['spec'] and rec['spec']['parameters']['initial_capital_usdt']==capital
 return {'kind':'ASMA' if asset=='BTC' else 'FILTERED_CHANNEL','name':row['name'],'report':rec['report'],'report_sha256':sha(rp),'source_round':Path(row['archive']).parts[2],'fingerprint':fp,'archive':row['archive'],'archive_sha256':row['archive_sha256'],'spec':row['spec'],'capital_usdt':capital,'asset':asset}
plan['read_only_comparator_refs']=[copy.deepcopy(v) for v in base['read_only_comparator_refs'] if v['kind'] in ('SMA_or_hold','CHANNEL15_30')]
for year in ('2025','2026'):
 pure=next((fp,v) for fp,v in canonical.items() if v['spec']['family']=='daily-close-range-breakout' and v['spec'].get('universe')==['ETH/USDT'] and v['spec'].get('parameters',{}).get('initial_capital_usdt')==500 and v['spec'].get('parameters',{}).get('entry_lookback_days')==15 and v['spec'].get('parameters',{}).get('exit_lookback_days')==30 and v['spec'].get('parameters',{}).get('start_utc','').startswith(year))
 for entry in plan['grid']['BTC_SMA_entry_band']:
  control=copy.deepcopy(template);control['components']=[{'fingerprint':components[year,'BTC',entry][0],'weight':.75},{'fingerprint':pure[0],'weight':.25}]
  control['parameters']['start_utc']=components[year,'BTC',entry][1]['spec']['parameters']['start_utc'];control['parameters']['end_utc']=components[year,'BTC',entry][1]['spec']['parameters']['end_utc'];fp=registry.fingerprint(control)
  rec=canonical[fp];rp=R/rec['report'];assert rec['result_available'] and sha(rp)==rec['report_sha256'];row=next(c for c in json.loads(rp.read_text())['configs'].values() if c['fingerprint']==fp)
  plan['read_only_comparator_refs'].append({'name':row['name'],'fingerprint':fp,'year':year,'kind':'MATCHED_ASMA_CHANNEL','BTC_SMA_entry_band':entry,'report':rec['report'],'report_sha256':sha(rp)})
plan['comparator_scope']='Primary controls are same-funded pureETHchannel15/30 with identicalBTC SMA65 entry threshold/exit0.5percent;all original criteria/status retained. Existing same-funded hold/SMA/channel and cash0 are historical context,not independent evidence.'
paths=[R/'research/experiments/20261001T133655Z/evaluate.py',R/'research/experiments/20261001T133655Z/kernel.py',R/'research/experiments/20261001T213902Z/audit.py',R/'research/experiments/20261001T213902Z/evaluate.py',R/'research/experiments/20261001T013355Z/evaluate.py',R/'research/experiments/20261001T113625Z/signals.py',R/'research/experiments/20261002T094655Z/signals.py',R/'research/experiments/20261007T123850Z/signals.py',R/'research/automation/registry.py']
plan['reused_code_sha256']={str(p.relative_to(R)):sha(p) for p in paths};plan['preflight_sha256']=sha(T/'preflight.py')
assert not (T/'spec.json').exists();(T/'spec.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
batch=[];grid=[]
def save(sp,fields,target):
 fp=registry.fingerprint(sp);assert fp not in canonical
 path=T/'specs'/f'{sp["name"]}.json';path.parent.mkdir(exist_ok=True);assert not path.exists();path.write_text(json.dumps(sp,indent=2)+'\n')
 x=subprocess.run([sys.executable,'research/automation/registry.py','reserve',str(path.relative_to(R))],cwd=R,capture_output=True,text=True);print(sp['name'],x.returncode,x.stdout.strip(),flush=True)
 if x.returncode:raise RuntimeError('STOP before any calculation:'+x.stdout+x.stderr)
 row={'name':sp['name'],'fingerprint':fp,'spec':str(path.relative_to(R)),**fields};target.append(row);return row
for year in plan['periods']:
 for span in plan['grid']['ETH_EMA_span_days']:
  for entry in plan['grid']['BTC_SMA_entry_band']:
   refs=[source_ref(year,'BTC',entry),source_ref(year,'ETH',span)];sp=copy.deepcopy(template)
   sp.update(name=f'asma_filtered_{year}_btc_e{entry}_eth_s{span}_x0.005_btc0.75',family='asymmetric-sma-filtered-channel-initial-capital',validation_plan=str((T/'spec.json').relative_to(R)))
   sp['parameters']['start_utc']=components[year,'ETH',span][1]['spec']['parameters']['start_utc'];sp['parameters']['end_utc']=components[year,'ETH',span][1]['spec']['parameters']['end_utc'];sp['components']=[{'fingerprint':r['fingerprint'],'weight':w} for r,w in zip(refs,(.75,.25))]
   row=save(sp,{'year':year,'role':'combination','direction':'BTC_ASMA_ETH_FILTERED','ETH_EMA_span_days':span,'BTC_SMA_entry_band':entry,'raw_weights':[.75,.25],'component_refs':refs,'is_new':True},batch);grid.append(row)
assert len(batch)==len(grid)==18 and len({r['fingerprint'] for b in grid for r in b['component_refs']})==12
(T/'batch.json').write_text(json.dumps(batch,indent=2)+'\n');(T/'grid_batch.json').write_text(json.dumps(grid,indent=2)+'\n')
forward=[];oldfb=json.loads((latest/'forward_batch.json').read_text());fps={}
for asset,capital in [('BTC',1500),('ETH',500)]:
 b=next(b for b in oldfb if b.get('asset')==asset);sp=json.loads((R/b['spec']).read_text());sp.update(name='forward_snapshot_'+asset,validation_plan=str((T/'spec.json').relative_to(R)));sp['parameters']['end_utc']=cutoff
 fps[asset]=save(sp,{'asset':asset,'capital_usdt':capital},forward)['fingerprint']
sp=json.loads((R/oldfb[-1]['spec']).read_text());sp.update(name='forward_snapshot_combo',validation_plan=str((T/'spec.json').relative_to(R)));sp['parameters']['end_utc']=cutoff;sp['components']=[{'fingerprint':fps[a],'weight':w} for a,w in zip(('BTC','ETH'),(.75,.25))];save(sp,{'capital_usdt':2000},forward)
(T/'forward_batch.json').write_text(json.dumps(forward,indent=2)+'\n');print('PASS:18new portfolios+3legacy cutoffs reserved;12exact-funded components and matched old controls read-only.')
