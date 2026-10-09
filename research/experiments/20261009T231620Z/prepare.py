"""Predeclare BTC/ETH turnover-threshold interaction;only genuinely new parents are reserved."""
from pathlib import Path
from datetime import datetime,timezone
import copy,gzip,hashlib,json,subprocess,sys
R=Path(__file__).resolve().parents[3];T=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));assert sha(R/'research/automation/registry.jsonl')==prior['ledger_sha256']
canonical={registry.fingerprint(v['spec']):v for v in prior['records'].values()};components={}
for fp,rec in canonical.items():
 sp=rec['spec'];p=sp.get('parameters',{});a=sp.get('universe',[''])[0].split('/')[0];year=p.get('start_utc','')[:4]
 if sp['family']!='daily-close-range-relative-quote-volume'or year not in('2025','2026')or not p.get('end_utc','').endswith('-09-14T00:01:00Z')or p.get('entry_lookback_days')!=15 or p.get('exit_lookback_days')!=30:continue
 use=a=='BTC'and p.get('initial_capital_usdt')==1500 and p.get('volume_lookback_days')==30 and p.get('minimum_volume_ratio')in(.9,1,1.1)
 use=use or(a=='ETH'and p.get('initial_capital_usdt')==500 and p.get('volume_lookback_days')==20 and p.get('minimum_volume_ratio')in(.75,.875,1))
 if use:components[year,a,p['minimum_volume_ratio']]=(fp,rec)
assert len(components)==12
latest=R/'research/experiments/20261009T211520Z';base=json.loads((latest/'spec.json').read_text());oldf=json.loads((latest/'forward_report.json').read_text());state=json.loads((latest/'forward_state.json').read_text());dt=lambda x:datetime.fromisoformat(x.replace('Z','+00:00'))
resume=oldf['cutoff_utc'];cutoff='2026-10-09T23:00:00Z';newminutes=int((dt(cutoff)-dt(resume)).total_seconds()/60);oldscene=oldf['configs']['forward_snapshot_combo']['scenes']['1'];oldpoints=len(oldscene['equity_usdt']);totalminutes=oldscene['elapsed_minutes']+newminutes
assert newminutes==120 and dt(resume)<dt(cutoff)<dt(state['next_daily_decision_utc'])and dt(cutoff)<datetime.now(timezone.utc)
plan={k:copy.deepcopy(base[k])for k in('periods','execution','costs','gates','walk_forward','forward_plan')}
plan.update(round=T.name,trigger_utc='2026-10-09T23:16:20.968Z',actual_first_tool_utc='2026-10-09T23:16:28Z',frozen_at_utc=datetime.now(timezone.utc).isoformat(),hypothesis=json.loads((T/'preflight_notes.json').read_text())['direction'],
 grid={'directions':['BTC_ETH_VOLUME_THRESHOLD_INTERACTION'],'BTC_minimum_volume_ratio':[.9,1,1.1],'ETH_minimum_volume_ratio':[.75,.875,1],'BTC_volume_lookback_days':30,'ETH_volume_lookback_days':20,'channel_entry_days':15,'channel_exit_days':30,'raw_weights':[.75,.25],'capital_usdt':2000,'component_capitals_usdt':[1500,500],'predeclared_center':{'BTC_minimum_volume_ratio':1,'ETH_minimum_volume_ratio':.875},'predeclared_focus':{'BTC_minimum_volume_ratio':1,'ETH_minimum_volume_ratio':.875}},
 rules_by_asset={a:copy.deepcopy(components['2026',a,n][1]['spec']['logic'])for a,n in [('BTC',1),('ETH',.875)]},allocation='Raw75/25 initial1500/500USDT independent sleeves of2000. Sum same-funded already-costed absolute NAV once;no normalization,capital scaling,second weighting,transfers,maintained ratio or rebalance.',
 sensitivity='Two independent entry-turnover-ratio axes:BTC0.9/1/1.1 at30days andETH0.75/0.875/1 at20days. Full9cells peryear. OldBTCratio1row6annualparents read-only;12newparents/36costscenes. All12fundedcomponents read-only. Oldcriteria/status preserved;newneighbourhood does not overwrite oldgates.',
 new_configs=12,new_cost_scenes=36,reused_grid_configs=6,reused_cost_scenes=18,full_grid_configs=18,reused_component_configs=12,prior_canonical_trials=prior['canonical'],development_history_reused=True,
 cross_period_confirmation='SameBTC/ETHthresholds,fixedwindows30/20 and raw75/25 must pass each reused180day/sixfold history;no independent final holdout or pooled years.',qualification_scope='Original eight gates retained. Existing centre andBTCratio1row remain old results,not newly retested confirmations.',interpretation='Positive repeated-history net returns do not establish stable live profit. New paired-path candidate in prior round remains development evidence;fixedP01-P10 unchanged.')
plan['walk_forward']['fit']='Fixed causal prior-close channel and disjoint priorUSDTturnover mean on bothassets. No new source signal/trade replay,labels/model/perfold/OOS fitting. Original180day rolling history,3daygap,purge0,six continuous30day folds.'
plan['forward_plan']['status_at_freeze']='OriginalSMA65/1percent75/25 delayed shadow21:00 to23:00 marks only,nextdailyOct10UTC00:01;paper10 observation27 unchanged.'
plan['forward_resume']={'source_state':str((latest/'forward_state.json').relative_to(R)),'state_sha256':sha(latest/'forward_state.json'),'source_report':str((latest/'forward_report.json').relative_to(R)),'report_sha256':sha(latest/'forward_report.json'),'resume_utc':resume,'cutoff_utc':cutoff,'daily_decision_utc':state['next_daily_decision_utc'],'new_minutes':newminutes,'cumulative_minutes':totalminutes,'prior_NAV_points':oldpoints,'new_reference_points':0,'total_NAV_points':oldpoints+newminutes,'action':'Append120closed marks only;preserve original positions,desired,trades andcosts. No new decision/reference/fill;delayed shadow,not paper10 real quotes.','new_configs':3,'new_cost_scenes':9}
template=json.loads((R/'research/experiments/20261009T191550Z/specs/dualvol_channel_2026_btcN30r1_ethN20_r0.875_btc0.75.json').read_text())
def parent(year,bn,en):
 sp=copy.deepcopy(template);sp['parameters']['start_utc']=components[year,'BTC',bn][1]['spec']['parameters']['start_utc'];sp['parameters']['end_utc']=components[year,'BTC',bn][1]['spec']['parameters']['end_utc'];sp['components']=[{'fingerprint':components[year,'BTC',bn][0],'weight':.75},{'fingerprint':components[year,'ETH',en][0],'weight':.25}];return sp
def ref_for(fp):
 rec=canonical[fp];rp=R/rec['report'];assert rec['result_available']and sha(rp)==rec['report_sha256'];row=next(c for c in json.loads(rp.read_text())['configs'].values()if c['fingerprint']==fp);sp=rec['spec'];asset=sp['universe'][0].split('/')[0]if sp['kind']=='strategy'else None
 assert json.loads((R/row['spec']).read_text())==sp and sha(R/row['archive'])==row['archive_sha256']
 return {'kind':'VOLUME_COMPONENT'if asset else'PORTFOLIO','name':row['name'],'year':sp['parameters']['start_utc'][:4],'asset':asset,'capital_usdt':sp['parameters']['initial_capital_usdt'],'fingerprint':fp,'spec':row['spec'],'spec_sha256':sha(R/row['spec']),'report':rec['report'],'report_sha256':rec['report_sha256'],'archive':row['archive'],'archive_sha256':row['archive_sha256'],'source_round':Path(row['archive']).parts[2]}
def source_ref(year,asset,n):return ref_for(components[year,asset,n][0])
plan['read_only_comparator_refs']=[copy.deepcopy(x)for x in base['read_only_comparator_refs']if x['kind']=='SMA_or_hold']
for year in('2025','2026'):
 for en in(.75,.875,1):
  fp=registry.fingerprint(parent(year,1,en));ref=ref_for(fp);plan['read_only_comparator_refs'].append({'kind':'MATCHED_BTC_R1_SAME_ETH','name':ref['name'],'year':year,'ETH_minimum_volume_ratio':en,'fingerprint':fp,'report':ref['report'],'report_sha256':ref['report_sha256']})
plan['comparator_scope']='Compare each newBTCratio0.9/1.1cell to existingBTCratio1 with sameETHratio,fixedmeans30/20 and1500/500funding. Existing centre1/0.875 and fullBTCratio1row are read-only,not reselected from current outcomes.'
potential=[]
for year in('2025','2026'):
 for bn in(.9,1,1.1):
  for en in(.75,.875,1):
   sp=parent(year,bn,en);fp=registry.fingerprint(sp);refs=[source_ref(year,'BTC',bn),source_ref(year,'ETH',en)];fields={'year':year,'role':'combination','direction':'BTC_ETH_VOLUME_THRESHOLD_INTERACTION','BTC_minimum_volume_ratio':bn,'ETH_minimum_volume_ratio':en,'raw_weights':[.75,.25],'component_refs':refs}
   if fp in canonical:
    assert bn==1;ref=ref_for(fp);potential.append((None,{'name':ref['name'],'fingerprint':fp,'spec':ref['spec'],**fields,'is_new':False,'source_ref':ref}))
   else:
    sp.update(name=f'dualratio_{year}_btcN30r{bn:g}_ethN20r{en:g}_btc0.75',validation_plan=str((T/'spec.json').relative_to(R)));potential.append((sp,{**fields,'is_new':True}))
assert len(potential)==18 and sum(sp is not None for sp,b in potential)==12
paths=[R/'research/experiments/20261001T133655Z/evaluate.py',R/'research/experiments/20261001T133655Z/kernel.py',R/'research/experiments/20261001T213902Z/evaluate.py',R/'research/experiments/20261001T213902Z/audit.py',R/'research/experiments/20261001T013355Z/evaluate.py',R/'research/experiments/20261001T113625Z/signals.py',R/'research/experiments/20261009T091020Z/signals.py',R/'research/automation/registry.py'];plan['reused_code_sha256']={str(p.relative_to(R)):sha(p)for p in paths};plan['preflight_sha256']=sha(T/'preflight.py')
assert not(T/'spec.json').exists();(T/'spec.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n');batch=[];grid=[]
def save(sp,fields,target):
 fp=registry.fingerprint(sp);assert fp not in canonical;path=T/'specs'/f'{sp["name"]}.json';path.parent.mkdir(exist_ok=True);assert not path.exists();path.write_text(json.dumps(sp,indent=2)+'\n')
 p=subprocess.run([sys.executable,'research/automation/registry.py','reserve',str(path.relative_to(R))],cwd=R,capture_output=True,text=True);print(sp['name'],p.returncode,p.stdout.strip(),flush=True)
 if p.returncode:raise RuntimeError('STOP before calculation:'+p.stdout+p.stderr)
 row={'name':sp['name'],'fingerprint':fp,'spec':str(path.relative_to(R)),**fields};target.append(row);return row
for sp,fields in potential:grid.append(save(sp,fields,batch)if sp is not None else fields)
assert len(batch)==12 and len(grid)==18;(T/'batch.json').write_text(json.dumps(batch,indent=2)+'\n');(T/'grid_batch.json').write_text(json.dumps(grid,indent=2)+'\n')
forward=[];oldfb=json.loads((latest/'forward_batch.json').read_text());fps={}
for asset,capital in [('BTC',1500),('ETH',500)]:
 b=next(b for b in oldfb if b.get('asset')==asset);sp=json.loads((R/b['spec']).read_text());sp.update(name='forward_snapshot_'+asset,validation_plan=str((T/'spec.json').relative_to(R)));sp['parameters']['end_utc']=cutoff;fps[asset]=save(sp,{'asset':asset,'capital_usdt':capital},forward)['fingerprint']
sp=json.loads((R/oldfb[-1]['spec']).read_text());sp.update(name='forward_snapshot_combo',validation_plan=str((T/'spec.json').relative_to(R)));sp['parameters']['end_utc']=cutoff;sp['components']=[{'fingerprint':fps[a],'weight':w}for a,w in zip(('BTC','ETH'),(.75,.25))];save(sp,{'capital_usdt':2000},forward)
(T/'forward_batch.json').write_text(json.dumps(forward,indent=2)+'\n');print('PASS:12new annualportfolios+3legacycutoffs reserved;6oldparents and12funded components read-only.')
