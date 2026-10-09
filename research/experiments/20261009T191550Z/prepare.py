"""Freeze a narrower ETHvolume grid;reuse exact prior cells without re-reserving them."""
from pathlib import Path
from datetime import datetime,timezone
import copy,gzip,hashlib,json,subprocess,sys
R=Path(__file__).resolve().parents[3];T=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'research/automation'));import registry
sys.path.insert(0,str(T));from design import source_spec,VOLUME_LOGIC,AXES
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));assert sha(R/'research/automation/registry.jsonl')==prior['ledger_sha256']
canonical={registry.fingerprint(v['spec']):v for v in prior['records'].values()};pure={};fixed={}
for fp,rec in canonical.items():
 sp=rec['spec'];p=sp.get('parameters',{});year=p.get('start_utc','')[:4]
 if year not in('2025','2026')or not p.get('end_utc','').endswith('-09-14T00:01:00Z'):continue
 if sp['family']=='daily-close-range-breakout'and sp.get('universe')==['ETH/USDT']and p.get('initial_capital_usdt')==500 and p.get('entry_lookback_days')==15 and p.get('exit_lookback_days')==30:pure[year]=(fp,rec)
 if sp['family']=='daily-close-range-relative-quote-volume'and sp.get('universe')==['BTC/USDT']and p.get('initial_capital_usdt')==1500 and p.get('volume_lookback_days')==30 and p.get('minimum_volume_ratio')==1 and p.get('entry_lookback_days')==15 and p.get('exit_lookback_days')==30:fixed[year]=(fp,rec)
assert len(pure)==len(fixed)==2
latest=R/'research/experiments/20261009T171550Z';base=json.loads((latest/'spec.json').read_text());oldf=json.loads((latest/'forward_report.json').read_text());state=json.loads((latest/'forward_state.json').read_text());dt=lambda x:datetime.fromisoformat(x.replace('Z','+00:00'))
resume=oldf['cutoff_utc'];cutoff='2026-10-09T19:00:00Z';newminutes=int((dt(cutoff)-dt(resume)).total_seconds()/60);scene=oldf['configs']['forward_snapshot_combo']['scenes']['1'];oldpoints=len(scene['equity_usdt']);totalminutes=scene['elapsed_minutes']+newminutes
assert newminutes==120 and dt(resume)<dt(cutoff)<dt(state['next_daily_decision_utc'])and dt(cutoff)<datetime.now(timezone.utc)
plan={k:copy.deepcopy(base[k])for k in('periods','execution','costs','gates','walk_forward','forward_plan')}
plan.update(round=T.name,trigger_utc='2026-10-09T19:15:50.783Z',actual_first_tool_utc='2026-10-09T19:15:57Z',frozen_at_utc=datetime.now(timezone.utc).isoformat(),hypothesis=json.loads((T/'preflight_notes.json').read_text())['direction'],
 grid={**AXES,'BTC_entry_lookback_days':15,'BTC_exit_lookback_days':30,'ETH_entry_lookback_days':15,'ETH_exit_lookback_days':30,'raw_weights':[.75,.25],'capital_usdt':2000,'component_capitals_usdt':[1500,500],'BTC_fixed_volume_lookback_days':30,'BTC_fixed_minimum_volume_ratio':1,'predeclared_center':{'volume_lookback_days':20,'minimum_volume_ratio':.875},'predeclared_focus':{'volume_lookback_days':20,'minimum_volume_ratio':.875}},
 rules_by_asset={'BTC':fixed['2026'][1]['spec']['logic'],'ETH':VOLUME_LOGIC},allocation='Raw75/25 initial1500/500USDT independent sleeves of2000. Sum same-funded already-costed absolute NAV once on common minute/execution axis;no normalization,second weighting,rescaling,transfers,maintained ratio or rebalance.',
 sensitivity='ETH mean15/20/25days jointly crossed with minimum ratio0.75/0.875/1. New14ETH+14portfolios;exact old20/r0.75 and20/r1 annualETH+parents (8definitions) read-only. Full9cells peryear forETH/portfolios;all costs,folds,Sharpe/Calmar/whole risk retained. Existing statuses/criteria never overwritten by new-neighbourhood stats.',
 new_component_configs=14,new_combination_configs=14,new_configs=28,new_cost_scenes=84,reused_component_configs=6,reused_combination_configs=4,reused_grid_configs=8,reused_cost_scenes=30,full_grid_configs=38,prior_canonical_trials=prior['canonical'],development_history_reused=True,
 cross_period_confirmation='SameETHN/ratio and fixedBTC30/r1,raw75/25 must pass both reused180day/sixfold histories;no pooled years or untouched final holdout.',qualification_scope='Original eight gates retained;new7cells peryear independently evaluated and registered. Old20/r0.75 and20/r1 retain original source gates/status,not newly evaluated results.',interpretation='Narrower neighbourhood chosen after previous reused-history study;selection bias remains. No stable-live-profit claim;fixedP01-P10 unchanged.',knowledge_sources=copy.deepcopy(base['knowledge_sources']))
plan['walk_forward']['fit']='Fixed causal disjoint completed-close/quote-turnover ranges;no model,labels,perfold/OOS fitting. Original180day rolling history,3daygap,purge0,six continuous30day diagnostic folds. Previously reused history not an independent final test.'
plan['forward_plan']['status_at_freeze']='Continue originalSMA65/1percent75/25 delayed shadow17:00 to19:00 marks only,nextdailyOct10UTC00:01;paper10 observation25 unchanged.'
plan['forward_resume']={'source_state':str((latest/'forward_state.json').relative_to(R)),'state_sha256':sha(latest/'forward_state.json'),'source_report':str((latest/'forward_report.json').relative_to(R)),'report_sha256':sha(latest/'forward_report.json'),'resume_utc':resume,'cutoff_utc':cutoff,'next_daily_decision_utc':state['next_daily_decision_utc'],'new_minutes':newminutes,'cumulative_minutes':totalminutes,'prior_NAV_points':oldpoints,'new_reference_points':0,'total_NAV_points':oldpoints+newminutes,'action':'Append120closed marks only;all old cash/units/desired/trades/costs retained. Zero new daily decision/reference/fill;delayed shadow disclosed,not paper10 actual quotes.','new_configs':3,'new_cost_scenes':9}
def ref_for(fp):
 rec=canonical[fp];assert rec['result_available']and sha(R/rec['report'])==rec['report_sha256'];row=next(c for c in json.loads((R/rec['report']).read_text())['configs'].values()if c['fingerprint']==fp);sp=rec['spec'];asset=sp['universe'][0].split('/')[0]if sp['kind']=='strategy'else None
 assert json.loads((R/row['spec']).read_text())==sp and sha(R/row['archive'])==row['archive_sha256']
 return {'kind':'VOLUME_COMPONENT'if asset else'PORTFOLIO','name':row['name'],'year':sp['parameters']['start_utc'][:4],'asset':asset,'capital_usdt':sp['parameters']['initial_capital_usdt'],'fingerprint':fp,'spec':row['spec'],'spec_sha256':sha(R/row['spec']),'report':rec['report'],'report_sha256':rec['report_sha256'],'archive':row['archive'],'archive_sha256':row['archive_sha256'],'source_round':Path(row['archive']).parts[2],'is_new_component':False}
plan['read_only_component_refs']=[ref_for(fixed[y][0])for y in('2025','2026')];plan['read_only_grid_refs']=[]
plan['read_only_comparator_refs']=copy.deepcopy(base['read_only_comparator_refs']);plan['comparator_scope']=base['comparator_scope']
template=json.loads((R/'research/experiments/20261009T171550Z/specs/dualvol_channel_2026_btcN30r1_ethN10_r0.75_btc0.75.json').read_text())
potential=[];allfp={}
for year in('2025','2026'):
 for n in AXES['volume_lookback_days']:
  for ratio in AXES['minimum_volume_ratio']:
   sp=source_spec(pure[year][1]['spec'],n,ratio);sp.update(name=f'volratio_{year}_ETH_n{n}_r{ratio:g}_e15_x30_c500',validation_plan=str((T/'spec.json').relative_to(R)));fp=registry.fingerprint(sp);allfp[year,n,ratio]=fp
   fields={'year':year,'role':'component','asset':'ETH','capital_usdt':500,'volume_lookback_days':n,'minimum_volume_ratio':ratio}
   if fp in canonical:
    assert n==20 and ratio in(.75,1);ref=ref_for(fp);plan['read_only_component_refs'].append(ref);potential.append((None,{**fields,'name':ref['name'],'fingerprint':fp,'spec':ref['spec'],'is_new':False,'source_ref':ref}))
   else:potential.append((sp,{**fields,'is_new':True}))
for ref in plan['read_only_component_refs'][:2]:potential.append((None,{'name':ref['name'],'fingerprint':ref['fingerprint'],'spec':ref['spec'],'year':ref['year'],'role':'component','asset':'BTC','capital_usdt':1500,'is_new':False,'source_ref':ref}))
for year in('2025','2026'):
 for n in AXES['volume_lookback_days']:
  for ratio in AXES['minimum_volume_ratio']:
   sp=copy.deepcopy(template);sp.update(name=f'dualvol_channel_{year}_btcN30r1_ethN{n}_r{ratio:g}_btc0.75',validation_plan=str((T/'spec.json').relative_to(R)));sp['parameters']['start_utc']=pure[year][1]['spec']['parameters']['start_utc'];sp['parameters']['end_utc']=pure[year][1]['spec']['parameters']['end_utc'];sp['components']=[{'fingerprint':fixed[year][0],'weight':.75},{'fingerprint':allfp[year,n,ratio],'weight':.25}];fp=registry.fingerprint(sp)
   fields={'year':year,'role':'combination','volume_lookback_days':n,'minimum_volume_ratio':ratio,'raw_weights':[.75,.25]}
   if fp in canonical:
    assert n==20 and ratio in(.75,1);ref=ref_for(fp);plan['read_only_grid_refs'].append(ref);potential.append((None,{**fields,'name':ref['name'],'fingerprint':fp,'spec':ref['spec'],'is_new':False,'source_ref':ref}))
   else:potential.append((sp,{**fields,'is_new':True}))
assert len(potential)==38 and sum(sp is not None for sp,b in potential)==28 and len(plan['read_only_component_refs'])==6 and len(plan['read_only_grid_refs'])==4
paths=[R/'research/experiments/20261002T174933Z/evaluate.py',R/'research/experiments/20261002T174933Z/signals.py',R/'research/experiments/20261001T133655Z/evaluate.py',R/'research/experiments/20261001T133655Z/kernel.py',R/'research/experiments/20261001T213902Z/audit.py',R/'research/experiments/20261001T213902Z/evaluate.py',R/'research/experiments/20261001T013355Z/evaluate.py',R/'.agents/skills/walk-forward-validation/scripts/walk_forward.py',R/'research/automation/registry.py',T/'design.py',T/'signals.py',T/'check_signals.py'];plan['reused_code_sha256']={str(p.relative_to(R)):sha(p)for p in paths};plan['preflight_sha256']=sha(T/'preflight.py')
assert not(T/'spec.json').exists();(T/'spec.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n');(T/'specs').mkdir(exist_ok=True);(T/'results').mkdir(exist_ok=True)
batch=[];grid=[]
def save(sp,fields,target):
 fp=registry.fingerprint(sp);assert fp not in canonical;path=T/'specs'/f'{sp["name"]}.json';assert not path.exists();path.write_text(json.dumps(sp,indent=2)+'\n')
 p=subprocess.run([sys.executable,'research/automation/registry.py','reserve',str(path.relative_to(R))],cwd=R,capture_output=True,text=True);print(sp['name'],p.returncode,p.stdout.strip(),flush=True)
 if p.returncode:raise RuntimeError('STOP before calculation:'+p.stdout+p.stderr)
 row={'name':sp['name'],'fingerprint':fp,'spec':str(path.relative_to(R)),**fields};target.append(row);return row
for sp,fields in potential:grid.append(save(sp,fields,batch)if sp is not None else fields)
assert len(batch)==28 and len(grid)==38;(T/'batch.json').write_text(json.dumps(batch,indent=2)+'\n');(T/'grid_batch.json').write_text(json.dumps(grid,indent=2)+'\n')
forward=[];oldfb=json.loads((latest/'forward_batch.json').read_text());fps={}
for asset,capital in [('BTC',1500),('ETH',500)]:
 b=next(b for b in oldfb if b.get('asset')==asset);sp=json.loads((R/b['spec']).read_text());sp.update(name='forward_snapshot_'+asset,validation_plan=str((T/'spec.json').relative_to(R)));sp['parameters']['end_utc']=cutoff;fps[asset]=save(sp,{'asset':asset,'capital_usdt':capital},forward)['fingerprint']
sp=json.loads((R/oldfb[-1]['spec']).read_text());sp.update(name='forward_snapshot_combo',validation_plan=str((T/'spec.json').relative_to(R)));sp['parameters']['end_utc']=cutoff;sp['components']=[{'fingerprint':fps[a],'weight':w}for a,w in zip(('BTC','ETH'),(.75,.25))];save(sp,{'capital_usdt':2000},forward)
(T/'forward_batch.json').write_text(json.dumps(forward,indent=2)+'\n');print('PASS:28new histories+3legacy cutoffs reserved;8exact old grid cells and2BTC sources read-only.')
