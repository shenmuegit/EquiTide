"""Freeze asset-specific SMA entry/exit bands and reserve only genuinely new configurations."""
from pathlib import Path
from datetime import datetime,timezone
import copy,gzip,hashlib,json,subprocess,sys
R=Path(__file__).resolve().parents[3];T=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
records=registry.read_records(R/'research/automation/registry.jsonl');canonical={registry.fingerprint(v['spec']):v for v in records.values()}
prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));assert sha(R/'research/automation/registry.jsonl')==prior['ledger_sha256']
latest=R/'research/experiments/20261009T030920Z';base=json.loads((latest/'spec.json').read_text());components={}
for fp,rec in canonical.items():
 sp=rec['spec'];p=sp.get('parameters',{});asset=sp.get('universe',[''])[0].split('/')[0]
 btc=asset=='BTC' and p.get('initial_capital_usdt')==1500 and p.get('entry_band_fraction') in (.0125,.015,.02) and p.get('exit_band_fraction')==.005
 eth=asset=='ETH' and p.get('initial_capital_usdt')==500 and p.get('entry_band_fraction')==.015 and p.get('exit_band_fraction') in (.0025,.005,.0075)
 if sp['family']=='daily-sma-asymmetric-hysteresis' and p.get('lookback_days')==65 and (btc or eth) and p.get('start_utc','')[:4] in ('2025','2026') and p.get('end_utc','').endswith('-09-14T00:01:00Z'):
  axis=p['entry_band_fraction'] if btc else p['exit_band_fraction'];components[p['start_utc'][:4],asset,axis]=(fp,rec)
assert len(components)==12
oldforward=json.loads((latest/'forward_report.json').read_text());state=json.loads((latest/'forward_state.json').read_text());resume=oldforward['cutoff_utc'];cutoff='2026-10-09T05:00:00Z';parse=lambda s:datetime.fromisoformat(s.replace('Z','+00:00'))
minutes=int((parse(cutoff)-parse(resume)).total_seconds()/60);oldscene=oldforward['configs']['forward_snapshot_combo']['scenes']['1'];oldpoints=len(oldscene['equity_usdt']);totalminutes=oldscene['elapsed_minutes']+minutes
assert minutes==120 and parse(resume)<parse(cutoff)<parse(state['next_daily_decision_utc']) and parse(cutoff)<datetime.now(timezone.utc)
plan={k:copy.deepcopy(base[k]) for k in ('periods','execution','costs','gates','walk_forward','forward_plan')}
plan.update(round=T.name,trigger_utc='2026-10-09T05:09:50.281Z',actual_first_tool_utc='2026-10-09T05:09:56Z',frozen_at_utc=datetime.now(timezone.utc).isoformat(),hypothesis=json.loads((T/'preflight_notes.json').read_text())['direction'],grid={'directions':['BTC_ENTRY_ETH_EXIT_SMA65'],'BTC_entry_band':[.0125,.015,.02],'ETH_exit_band':[.0025,.005,.0075],'lookback_days':65,'BTC_exit_band':.005,'ETH_entry_band':.015,'raw_weights':[.75,.25],'capital_usdt':2000,'component_capitals_usdt':[1500,500],'predeclared_center':{'BTC_entry_band':.015,'ETH_exit_band':.005},'predeclared_focus':{'BTC_entry_band':.0125,'ETH_exit_band':.005}},rules_by_asset={a:copy.deepcopy(components['2026',a,axis][1]['spec']['logic']) for a,axis in [('BTC',.015),('ETH',.005)]},allocation='Raw initialBTC/ETH75/25 means1500/500USDT of2000. Sum exact-funded already-costed absolute NAVs once;no normalization,second weighting,transfers,rebalance or maintained weights.',sensitivity='IndependentBTC SMA65 entry1.25/1.5/2percent and ETH SMA65 exit0.25/0.5/0.75percent. BTCexit0.5percent/ETHentry1.5percent fixed. Full3x3 each2025/2026;16new annual portfolios,2exact old centers and12funded source components read-only. Preserve all costs,folds,minute/daily risk,Sharpe/Calmar and12adjacent edges.',new_configs=16,new_cost_scenes=48,reused_grid_configs=2,reused_cost_scenes=6,full_grid_configs=18,reused_component_configs=12,prior_canonical_trials=prior['canonical'],development_history_reused=True,cross_period_confirmation='Same BTCentry/ETHexit and raw75/25 must pass both reused180day/sixfold histories;no pooled years,untouched final holdout or independent new sample claim.',qualification_scope='Eight gates unchanged;16new annual configurations independently reserve/finish;2old center records preserve original criteria/status.',interpretation='Repeated development history and many trials;positive net historical returns do not establish stable live profit. FrozenP01-P10 actual-quote paper accounts remain unchanged.',knowledge_sources=[{'url':'https://github.com/binance/binance-public-data','access_date_utc':'2026-10-09','scope':'Official spot archive timestamps/checksums/revisions;same-SHA real minute data retained.'},{'url':'https://data-api.binance.vision/api/v3/klines','scope':'Only publicGET completed minute marks for separate original delayed shadow;not paper10 actual-quote fills.'}])
plan['walk_forward']['fit']='Fixed causal Decimal28 SMA65 including tested prior completed close,strict asymmetric entry/exit,desired state continuous across folds;no model/labels/perfold/OOS fit.180day rolling history,3day gap,purge0,six continuous30day diagnostic folds.'
plan['forward_plan']['status_at_freeze']='OriginalSMA65/1percent75/25 delayed shadow marks only before nextdailyOct10UTC00:01;paper10 separate.'
plan['forward_resume']={'source_state':str((latest/'forward_state.json').relative_to(R)),'state_sha256':sha(latest/'forward_state.json'),'source_report':str((latest/'forward_report.json').relative_to(R)),'report_sha256':sha(latest/'forward_report.json'),'resume_utc':resume,'cutoff_utc':cutoff,'next_daily_decision_utc':state['next_daily_decision_utc'],'new_minutes':minutes,'cumulative_minutes':totalminutes,'prior_NAV_points':oldpoints,'new_reference_points':0,'total_NAV_points':oldpoints+minutes,'action':'Append120closed marks only;original cash/units/desired/trades/costs continue. No daily reference/decision/fill/restart/forced exit;delayed reconstruction disclosed,not paper10.','new_configs':3,'new_cost_scenes':9,'qualification':f'Only{totalminutes}minutes/{totalminutes//1440}complete days;not180day/sixfold qualification.'}
plan['read_only_comparator_refs']=[copy.deepcopy(v) for v in base['read_only_comparator_refs'] if v['kind'] in ('SMA_or_hold','CHANNEL15_30')]
plan['comparator_scope']='Primary control is exact old shared1.5percent entry/0.5percent exit SMA65 center with matching1500/500 funds. Also compare each registeredBTCentry row to sameBTC andETHexit0.5percent baseline;these baseline cells belong to the reserved grid. Existing hold/SMA/purechannel references are background,not independent alpha proof.'
paths=[R/'research/experiments/20261001T133655Z/evaluate.py',R/'research/experiments/20261001T133655Z/kernel.py',R/'research/experiments/20261001T213902Z/audit.py',R/'research/experiments/20261001T213902Z/evaluate.py',R/'research/experiments/20261001T013355Z/evaluate.py',R/'research/experiments/20261001T113625Z/signals.py',R/'research/experiments/20261002T094655Z/signals.py',R/'research/automation/registry.py']
plan['reused_code_sha256']={str(p.relative_to(R)):sha(p) for p in paths};plan['preflight_sha256']=sha(T/'preflight.py')
assert not (T/'spec.json').exists();(T/'spec.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
template=json.loads((R/'research/experiments/20261002T094655Z/specs/asym_2026_combo_e0.015_x0.005_btc0.75.json').read_text());batch=[];grid=[]
def save(sp,fields,target):
 fp=registry.fingerprint(sp);assert fp not in canonical;path=T/'specs'/f'{sp["name"]}.json';path.parent.mkdir(exist_ok=True);assert not path.exists();path.write_text(json.dumps(sp,indent=2)+'\n')
 x=subprocess.run([sys.executable,'research/automation/registry.py','reserve',str(path.relative_to(R))],cwd=R,capture_output=True,text=True);print(sp['name'],x.returncode,x.stdout.strip(),flush=True)
 if x.returncode:raise RuntimeError('STOP before calculation:'+x.stdout+x.stderr)
 row={'name':sp['name'],'fingerprint':fp,'spec':str(path.relative_to(R)),**fields};target.append(row);return row
def ref(year,asset,axis):
 fp,rec=components[year,asset,axis];rp=R/rec['report'];assert rec['result_available'] and sha(rp)==rec['report_sha256'];row=next(c for c in json.loads(rp.read_text())['configs'].values() if c['fingerprint']==fp);capital=1500 if asset=='BTC' else 500
 assert json.loads((R/row['spec']).read_text())==rec['spec'] and rec['spec']['parameters']['initial_capital_usdt']==capital
 return {'kind':'ASMA','name':row['name'],'report':rec['report'],'report_sha256':sha(rp),'source_round':Path(row['archive']).parts[2],'fingerprint':fp,'archive':row['archive'],'archive_sha256':row['archive_sha256'],'spec':row['spec'],'capital_usdt':capital,'asset':asset}
for year in plan['periods']:
 for entry in plan['grid']['BTC_entry_band']:
  for exit in plan['grid']['ETH_exit_band']:
   refs=[ref(year,'BTC',entry),ref(year,'ETH',exit)];sp=copy.deepcopy(template);sp.update(name=f'split_asma_{year}_btc_e{entry}_eth_x{exit}_btc0.75',family='asset-specific-asymmetric-sma-initial-capital',validation_plan=str((T/'spec.json').relative_to(R)))
   sp['parameters']['start_utc']=components[year,'BTC',entry][1]['spec']['parameters']['start_utc'];sp['parameters']['end_utc']=components[year,'BTC',entry][1]['spec']['parameters']['end_utc'];sp['components']=[{'fingerprint':r['fingerprint'],'weight':w} for r,w in zip(refs,(.75,.25))]
   fields={'year':year,'role':'combination','direction':'BTC_ENTRY_ETH_EXIT_SMA65','BTC_entry_band':entry,'ETH_exit_band':exit,'raw_weights':[.75,.25],'component_refs':refs};fp=registry.fingerprint(sp)
   if fp in canonical:
    assert (entry,exit)==(.015,.005);rec=canonical[fp];rp=R/rec['report'];assert rec['result_available'] and sha(rp)==rec['report_sha256'];old=next(c for c in json.loads(rp.read_text())['configs'].values() if c['fingerprint']==fp)
    row={**{k:old[k] for k in ('name','fingerprint','spec')},**fields,'is_new':False,'source_ref':{'report':rec['report'],'report_sha256':sha(rp),'archive':old['archive'],'archive_sha256':old['archive_sha256'],'source_round':Path(old['archive']).parts[2],'spec_sha256':sha(R/old['spec'])}};print('READ_ONLY_EXACT',old['name'],flush=True)
   else:row=save(sp,{**fields,'is_new':True},batch)
   grid.append(row)
assert len(batch)==16 and len(grid)==18 and len({r['fingerprint'] for b in grid for r in b['component_refs']})==12
(T/'batch.json').write_text(json.dumps(batch,indent=2)+'\n');(T/'grid_batch.json').write_text(json.dumps(grid,indent=2)+'\n')
forward=[];oldfb=json.loads((latest/'forward_batch.json').read_text());fps={}
for asset,capital in [('BTC',1500),('ETH',500)]:
 b=next(b for b in oldfb if b.get('asset')==asset);sp=json.loads((R/b['spec']).read_text());sp.update(name='forward_snapshot_'+asset,validation_plan=str((T/'spec.json').relative_to(R)));sp['parameters']['end_utc']=cutoff;fps[asset]=save(sp,{'asset':asset,'capital_usdt':capital},forward)['fingerprint']
sp=json.loads((R/oldfb[-1]['spec']).read_text());sp.update(name='forward_snapshot_combo',validation_plan=str((T/'spec.json').relative_to(R)));sp['parameters']['end_utc']=cutoff;sp['components']=[{'fingerprint':fps[a],'weight':w} for a,w in zip(('BTC','ETH'),(.75,.25))];save(sp,{'capital_usdt':2000},forward)
(T/'forward_batch.json').write_text(json.dumps(forward,indent=2)+'\n');print('PASS:16new portfolios+3legacy cutoffs reserved;2old centers and12exact-funded components read-only.')
