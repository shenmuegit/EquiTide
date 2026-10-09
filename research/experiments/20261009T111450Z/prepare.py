"""Freeze the complete volume-confirmation batch and reserve every new configuration."""
from pathlib import Path
from datetime import datetime,timezone
import copy,gzip,hashlib,json,subprocess,sys
R=Path(__file__).resolve().parents[3];T=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'research/automation'));import registry
sys.path.insert(0,str(T));from design import source_spec,VOLUME_LOGIC,AXES
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));L=R/'research/automation/registry.jsonl'
assert sha(L)==prior['ledger_sha256'];records=registry.read_records(L);canonical={registry.fingerprint(v['spec']):v for v in records.values()};base=json.loads((R/'research/experiments/20261009T091020Z/spec.json').read_text());old={}
for fp,rec in canonical.items():
 sp=rec['spec'];p=sp.get('parameters',{});asset=sp.get('universe',[''])[0].split('/')[0]
 if sp['family']=='daily-close-range-breakout' and asset in ('BTC','ETH') and p.get('initial_capital_usdt')==(1500 if asset=='BTC' else 500) and p.get('entry_lookback_days')==15 and p.get('exit_lookback_days')==30 and p.get('start_utc','')[:4] in ('2025','2026') and p.get('end_utc','').endswith('-09-14T00:01:00Z'):old[p['start_utc'][:4],asset]=(fp,rec)
assert len(old)==4
latest=R/'research/experiments/20261009T091020Z';oldf=json.loads((latest/'forward_report.json').read_text());state=json.loads((latest/'forward_state.json').read_text());dt=lambda x:datetime.fromisoformat(x.replace('Z','+00:00'));resume=oldf['cutoff_utc'];cutoff='2026-10-09T11:00:00Z';newminutes=int((dt(cutoff)-dt(resume)).total_seconds()/60);scene=oldf['configs']['forward_snapshot_combo']['scenes']['1'];oldpoints=len(scene['equity_usdt']);totalminutes=scene['elapsed_minutes']+newminutes
assert newminutes==120 and dt(resume)<dt(cutoff)<dt(state['next_daily_decision_utc']) and dt(cutoff)<datetime.now(timezone.utc)
plan={k:copy.deepcopy(base[k])for k in ('periods','execution','costs','gates','walk_forward','forward_plan')}
plan.update(round=T.name,trigger_utc='2026-10-09T11:14:50.478Z',actual_first_tool_utc='2026-10-09T11:14:56Z',frozen_at_utc=datetime.now(timezone.utc).isoformat(),hypothesis=json.loads((T/'preflight_notes.json').read_text())['direction'],grid={**AXES,'BTC_entry_lookback_days':15,'BTC_exit_lookback_days':30,'ETH_entry_lookback_days':15,'ETH_exit_lookback_days':30,'raw_weights':[.75,.25],'capital_usdt':2000,'component_capitals_usdt':[1500,500],'predeclared_center':{'volume_lookback_days':40,'minimum_volume_ratio':1.},'predeclared_focus':{'volume_lookback_days':40,'minimum_volume_ratio':1.}},rules_by_asset={'BTC':VOLUME_LOGIC,'ETH':old['2026','ETH'][1]['spec']['logic']},allocation='Raw initialBTC/ETH75/25 allocates1500/500USDT of2000,independent cash and coin sleeves. Sum same-funded already-costed absolute NAV once;no normalization,second weighting,transfers,maintained weights or rebalance.',sensitivity='Two predeclared parameters jointly varied:preceding quote-volume lookback30/40/50days and minimum ratio0.9/1/1.1. Each year8new BTC leaves and8new75/25portfolios plus old30day/ratio1 read-only cells;oldcriteria/status retained,ETH15/30 fixed. All9cells/folds/costs reported.',new_component_configs=16,new_combination_configs=16,new_configs=32,new_cost_scenes=96,reused_component_configs=4,reused_combination_configs=2,reused_cost_scenes=18,full_grid_configs=38,prior_canonical_trials=prior['canonical'],development_history_reused=True,cross_period_confirmation='SameN,ratio and raw75/25 must pass both reused180day/sixfold histories;no pooled periods/untouched final holdout. Novel path/parameter counts do not imply independent samples.',qualification_scope='Original eight gates unchanged for new BTC andportfolio grids. Old BTC/ETH components and prior candidate portfolio statuses/criteria/scenes preserved. Negative/zero-trade and all failed actual configs remain tested.',interpretation='Turnover confirmation gates entry only;low volume never forces exit. This is a generated hypothesis,not established alpha. No stable-live-profit claim;P01-P10 actual-quote accounts unchanged.',knowledge_sources=[{'url':'https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints','access_date_utc':'2026-10-09','scope':'Official kline index7=quote asset volume and UTC default verified before freeze. Our generated entry rule is not sourced alpha.'},{'url':'https://github.com/binance/binance-public-data','scope':'Official archive format/checksums;actual same-SHA cached minute data,no new market data for historical batch.'},{'url':'https://data-api.binance.vision/api/v3/klines','scope':'Only publicGET completed marks for separate delayed SMA shadow,not paper10 fills.'}])
plan['walk_forward']['fit']='Fixed causal close-channel15/30 and Decimal28 quote turnover ratio;no labels/model/perfold/OOS fitting.180day rolling history,3day gap,purge0,six continuous30day diagnostic folds. Both price/volume references exclude tested prior day;all complete before next00:01 execution.'
plan['forward_plan']['status_at_freeze']='Continue originalSMA65/1percent75/25 delayed shadow09:00 to11:00 marks;nextdailyOct10UTC00:01,180day plan unchanged;paper10 independent.'
plan['forward_resume']={'source_state':str((latest/'forward_state.json').relative_to(R)),'state_sha256':sha(latest/'forward_state.json'),'source_report':str((latest/'forward_report.json').relative_to(R)),'report_sha256':sha(latest/'forward_report.json'),'resume_utc':resume,'cutoff_utc':cutoff,'next_daily_decision_utc':state['next_daily_decision_utc'],'new_minutes':newminutes,'cumulative_minutes':totalminutes,'prior_NAV_points':oldpoints,'new_reference_points':0,'total_NAV_points':oldpoints+newminutes,'action':'Append120closed marks only;preserve all cash/units/desired/trades/costs,no new reference/decision/fill/forced exit. Delayedshadow disclosure;not realquote paper10.','new_configs':3,'new_cost_scenes':9,'qualification':'Partial7complete days,not180day/sixfold.'}
def oldref(year,asset):
 fp,rec=old[year,asset];rp=R/rec['report'];assert rec['result_available'] and sha(rp)==rec['report_sha256'];row=next(c for c in json.loads(rp.read_text())['configs'].values()if c['fingerprint']==fp);assert json.loads((R/row['spec']).read_text())==rec['spec']
 return {'kind':'CHANNEL','name':row['name'],'year':year,'report':rec['report'],'report_sha256':sha(rp),'source_round':Path(row['archive']).parts[2],'fingerprint':fp,'archive':row['archive'],'archive_sha256':row['archive_sha256'],'spec':row['spec'],'spec_sha256':sha(R/row['spec']),'capital_usdt':1500 if asset=='BTC' else 500,'asset':asset,'is_new_component':False}
def knownref(fp):
 rec=canonical[fp];rp=R/rec['report'];assert rec['result_available'] and sha(rp)==rec['report_sha256'];row=next(c for c in json.loads(rp.read_text())['configs'].values()if c['fingerprint']==fp);sp=rec['spec'];asset=sp['universe'][0].split('/')[0]if sp['kind']=='strategy'else None
 assert json.loads((R/row['spec']).read_text())==sp
 return {'kind':'VOLRATIO'if asset else'PORTFOLIO','name':row['name'],'year':sp['parameters']['start_utc'][:4],'report':rec['report'],'report_sha256':sha(rp),'source_round':Path(row['archive']).parts[2],'fingerprint':fp,'archive':row['archive'],'archive_sha256':row['archive_sha256'],'spec':row['spec'],'spec_sha256':sha(R/row['spec']),'capital_usdt':sp['parameters']['initial_capital_usdt'],'asset':asset,'is_new_component':False}
plan['read_only_component_refs']=[oldref(y,'ETH')for y in('2025','2026')]+[knownref(registry.fingerprint(source_spec(old[y,'BTC'][1]['spec'],30,1.)))for y in('2025','2026')]
plan['read_only_grid_refs']=[]

plan['read_only_comparator_refs']=[copy.deepcopy(v)for v in base['read_only_comparator_refs']if v['kind'] in ('SMA_or_hold','CHANNEL15_30','MATCHED_UNFILTERED_CHANNEL')]
for ref in plan['read_only_comparator_refs']:
 if ref['kind']in('CHANNEL15_30','MATCHED_UNFILTERED_CHANNEL'):
  ref['kind']='MATCHED_UNFILTERED_CHANNEL';ref['fingerprint']=json.loads((R/ref['report']).read_text())['configs'][ref['name']]['fingerprint'];rec=canonical[ref['fingerprint']];assert sorted(rec['spec']['components'],key=lambda x:x['fingerprint'])==sorted([{'fingerprint':old[ref['year'],'BTC'][0],'weight':.75},{'fingerprint':old[ref['year'],'ETH'][0],'weight':.25}],key=lambda x:x['fingerprint'])
template=json.loads((R/'research/experiments/20261002T174933Z/specs/channel_2026_combo_e15_x30_btc0.75.json').read_text())
for year in('2025','2026'):
 co=copy.deepcopy(template);co['parameters']['start_utc']=old[year,'BTC'][1]['spec']['parameters']['start_utc'];co['parameters']['end_utc']=old[year,'BTC'][1]['spec']['parameters']['end_utc'];co['components']=[{'fingerprint':registry.fingerprint(source_spec(old[year,'BTC'][1]['spec'],30,1.)),'weight':.75},{'fingerprint':old[year,'ETH'][0],'weight':.25}];plan['read_only_grid_refs'].append(knownref(registry.fingerprint(co)))
plan['comparator_scope']='Matching pureBTC15/30 plus sameETH15/30 and same1500/500USDT budgets;onlyBTC entry quote-turnover confirmation changes. Oldhold/SMA allocations are background only.'
paths=[R/'research/experiments/20261002T174933Z/evaluate.py',R/'research/experiments/20261002T174933Z/signals.py',R/'research/experiments/20261001T133655Z/evaluate.py',R/'research/experiments/20261001T133655Z/kernel.py',R/'research/experiments/20261001T213902Z/audit.py',R/'research/experiments/20261001T213902Z/evaluate.py',R/'research/experiments/20261001T013355Z/evaluate.py',R/'.agents/skills/walk-forward-validation/scripts/walk_forward.py',R/'research/automation/registry.py',T/'design.py',T/'signals.py',T/'check_signals.py'];plan['reused_code_sha256']={str(p.relative_to(R)):sha(p)for p in paths};plan['preflight_sha256']=sha(T/'preflight.py')
assert not (T/'spec.json').exists();(T/'spec.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n');(T/'specs').mkdir(exist_ok=True);(T/'results').mkdir(exist_ok=True)
batch=[];grid=[];newrefs={}
def save(sp,fields,target=batch):
 fp=registry.fingerprint(sp);assert fp not in canonical;path=T/'specs'/f'{sp["name"]}.json';assert not path.exists();path.write_text(json.dumps(sp,indent=2)+'\n');p=subprocess.run([sys.executable,'research/automation/registry.py','reserve',str(path.relative_to(R))],cwd=R,capture_output=True,text=True);print(sp['name'],p.returncode,p.stdout.strip(),flush=True)
 if p.returncode:raise RuntimeError('STOP before calculation:'+p.stdout+p.stderr)
 row={'name':sp['name'],'fingerprint':fp,'spec':str(path.relative_to(R)),**fields};target.append(row);return row
for year in('2025','2026'):
 for n in AXES['volume_lookback_days']:
  for ratio in AXES['minimum_volume_ratio']:
   sp=source_spec(old[year,'BTC'][1]['spec'],n,ratio);fp=registry.fingerprint(sp);fields={'year':year,'role':'component','asset':'BTC','capital_usdt':1500,'volume_lookback_days':n,'minimum_volume_ratio':ratio}
   if fp in canonical:
    ref=knownref(fp);row={'name':ref['name'],'fingerprint':fp,'spec':ref['spec'],**fields,'is_new':False,'source_ref':ref}
   else:
    sp.update(name=f'volratio_{year}_BTC_n{n}_r{ratio:g}_e15_x30_c1500',validation_plan=str((T/'spec.json').relative_to(R)));row=save(sp,{**fields,'is_new':True})
   grid.append(row);newrefs[year,n,ratio]=row
for ref in plan['read_only_component_refs']:
 if ref['asset']=='ETH':grid.append({'name':ref['name'],'fingerprint':ref['fingerprint'],'spec':ref['spec'],'year':ref['year'],'role':'component','asset':'ETH','capital_usdt':500,'is_new':False,'source_ref':ref})
for year in('2025','2026'):
 for n in AXES['volume_lookback_days']:
  for ratio in AXES['minimum_volume_ratio']:
   sp=copy.deepcopy(template);sp.update(name=f'volratio_channel_{year}_n{n}_r{ratio:g}_btc0.75',family='quote-volume-channel-initial-capital',validation_plan=str((T/'spec.json').relative_to(R)));sp['parameters']['start_utc']=old[year,'BTC'][1]['spec']['parameters']['start_utc'];sp['parameters']['end_utc']=old[year,'BTC'][1]['spec']['parameters']['end_utc'];sp['components']=[{'fingerprint':newrefs[year,n,ratio]['fingerprint'],'weight':.75},{'fingerprint':old[year,'ETH'][0],'weight':.25}];fp=registry.fingerprint(sp);fields={'year':year,'role':'combination','volume_lookback_days':n,'minimum_volume_ratio':ratio,'raw_weights':[.75,.25]}
   if fp in canonical:
    ref=knownref(fp);row={'name':ref['name'],'fingerprint':fp,'spec':ref['spec'],**fields,'is_new':False,'source_ref':ref}
   else:row=save(sp,{**fields,'is_new':True})
   grid.append(row)
assert len(batch)==32 and len(grid)==38 and sum(b['is_new']for b in grid)==32
(T/'batch.json').write_text(json.dumps(batch,indent=2)+'\n');(T/'grid_batch.json').write_text(json.dumps(grid,indent=2)+'\n')
forward=[];oldfb=json.loads((latest/'forward_batch.json').read_text());fps={}
for asset,capital in [('BTC',1500),('ETH',500)]:
 b=next(b for b in oldfb if b.get('asset')==asset);sp=json.loads((R/b['spec']).read_text());sp.update(name='forward_snapshot_'+asset,validation_plan=str((T/'spec.json').relative_to(R)));sp['parameters']['end_utc']=cutoff;fps[asset]=save(sp,{'asset':asset,'capital_usdt':capital},forward)['fingerprint']
sp=json.loads((R/oldfb[-1]['spec']).read_text());sp.update(name='forward_snapshot_combo',validation_plan=str((T/'spec.json').relative_to(R)));sp['parameters']['end_utc']=cutoff;sp['components']=[{'fingerprint':fps[a],'weight':w}for a,w in zip(('BTC','ETH'),(.75,.25))];save(sp,{'capital_usdt':2000},forward)
(T/'forward_batch.json').write_text(json.dumps(forward,indent=2)+'\n');print('PASS:32new historical configs+3legacy cutoffs reserved before any calculation;4oldcomponents+2oldportfolios read-only.')
