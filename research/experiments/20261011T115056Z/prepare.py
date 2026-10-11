"""Freeze joint initial-funding/EMA span definitions, then reserve each actual new test."""
from pathlib import Path
from datetime import datetime,timezone
from copy import deepcopy
import gzip,hashlib,json,subprocess,sys
T=Path(__file__).resolve().parent;R=T.parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sys.path.insert(0,str(R/'research/automation'));import registry
sys.path.insert(0,str(T));from design import definitions,AXES,BTC_SOURCE,ETH_SOURCE
prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));assert sha(R/'research/automation/registry.jsonl')==prior['ledger_sha256'];canonical={registry.fingerprint(v['spec']):v for v in prior['records'].values()}
S=R/'research/experiments/20261011T094956Z';oldplan=json.loads((S/'spec.json').read_text());oldforward=json.loads((S/'forward_report.json').read_text());oldstate=json.loads((S/'forward_state.json').read_text());plan={k:deepcopy(oldplan[k])for k in('periods','execution','costs','gates','walk_forward','forward_plan','read_only_background_refs','cash_reference')}
plan.update(round=T.name,trigger_utc='2026-10-11T11:50:56.668Z',first_recorded_clock_utc='2026-10-11T11:51:06Z',frozen_at_utc=datetime.now(timezone.utc).isoformat(),hypothesis=json.loads((T/'preflight_notes.json').read_text())['direction'],grid={**AXES,'BTC_EMA_exit_band_fraction':.03,'BTC_volume_lookback_days':40,'BTC_minimum_volume_ratio':1.1,'ETH_EMA_span_days':30,'ETH_symmetric_band':.0125,'entry_lookback_days':15,'exit_lookback_days':30,'raw_weights':[.55,.45],'component_capitals_usdt':[1100,900],'capital_usdt':2000,'predeclared_focus':{'BTC_EMA_span_days':15,'BTC_EMA_entry_band_fraction':.01,'BTC_EMA_exit_band_fraction':.03}},allocation='Explicitraw55/45own1100/900USDT of2000. NewBTCvolumeEMA rules simulateatownfunds;ETH source900NAV reused. Already-costedabsoluteNAVsumonce,no scaling,normalization,transfers,maintainedweights or rebalance.',sensitivity='BTCEMAspan10/15/20 x entryband0.005/0.01/0.015,exit0.03 fixed,joint9cells peryear forBTCandparents. ETHfixed singleoldsource. Oldspan20asymmetricEMA cells remain in sensitivitywith originalcriteria/status;oldnoBTCEMA baselines excluded.',new_configs=24,new_component_configs=12,new_combination_configs=12,new_cost_scenes=72,reused_component_configs=10,reused_combination_configs=8,reused_cost_scenes=54,full_grid_configs=42,prior_canonical_trials=prior['canonical'],development_history_reused=True,qualification_scope='Originaleightgates foractualnewcomponents/parents;two repeatedlyused180day/sixfoldhistories,not independentfinaltest. No labels/fitting/optimizer or same-round adaptivegrid.',knowledge_sources=json.loads((T/'sources.json').read_text()),read_only_component_refs=[],read_only_grid_refs=[],read_only_comparator_refs=[])
cutoff='2026-10-11T11:00:00Z';oldscene=oldforward['configs']['forward_snapshot_combo']['scenes']['1'];dt=lambda s:datetime.fromisoformat(s.replace('Z','+00:00'));newminutes=int((dt(cutoff)-dt(oldforward['cutoff_utc'])).total_seconds()/60)
assert newminutes==120 and dt(cutoff)<datetime.now(timezone.utc) and dt(cutoff)<dt(oldstate['next_daily_decision_utc'])
plan['forward_resume']={'source_state':str((S/'forward_state.json').relative_to(R)),'state_sha256':sha(S/'forward_state.json'),'source_report':str((S/'forward_report.json').relative_to(R)),'report_sha256':sha(S/'forward_report.json'),'resume_utc':oldforward['cutoff_utc'],'cutoff_utc':cutoff,'next_daily_decision_utc':oldstate['next_daily_decision_utc'],'new_minutes':120,'cumulative_minutes':oldscene['elapsed_minutes']+120,'prior_NAV_points':len(oldscene['equity_usdt']),'total_NAV_points':len(oldscene['equity_usdt'])+120,'new_reference_points':0,'action':'Append120closedmarks only;originalfloatcash/units/desired/trades/costs preserved,no dailydecision/reference/forcedexit/reset/retrofitrounding. Delayedshadow only,not paper10actualquotes.','new_configs':3,'new_cost_scenes':9}
plan['forward_plan']['status_at_freeze']='OriginalSMA65/1percent75/25 delayedshadow09:00to11:00markonly,nextdailyOct12UTC00:01. Paper44andtwo retainedgaps/95.976332percentcoverageproxy unchanged.'
def ref_for(fp):
 rec=canonical[fp];assert rec['result_available']and sha(R/rec['report'])==rec['report_sha256'];row=next(x for x in json.loads((R/rec['report']).read_text())['configs'].values()if x['fingerprint']==fp);sp=rec['spec'];asset=sp['universe'][0].split('/')[0]if sp['kind']=='strategy'else None
 assert sha(R/row['archive'])==row['archive_sha256']and json.loads((R/row['spec']).read_text())==sp
 return {'kind':'SOURCE_COMPONENT'if asset else'PORTFOLIO','name':row['name'],'year':sp['parameters']['start_utc'][:4],'asset':asset,'capital_usdt':sp['parameters']['initial_capital_usdt'],'fingerprint':fp,'spec':row['spec'],'spec_sha256':sha(R/row['spec']),'report':rec['report'],'report_sha256':rec['report_sha256'],'archive':row['archive'],'archive_sha256':row['archive_sha256'],'source_round':Path(row['archive']).parts[2]}
potential=[]
for sp,b in definitions(registry.fingerprint):
 fp=registry.fingerprint(sp)
 if fp in canonical:
  ref=ref_for(fp);plan['read_only_component_refs'if b['role']=='component'else'read_only_grid_refs'].append(ref);potential.append((None,{**b,'name':ref['name'],'fingerprint':fp,'spec':ref['spec'],'is_new':False,'source_ref':ref}))
 else:
  if b['role']=='component':name=f'fastasym_{b["year"]}_BTC_s{b["BTC_EMA_span_days"]}_e{b["BTC_EMA_entry_band_fraction"]}_x0.03_c1100'
  else:name=f'fastasym_{b["year"]}_btcS{b["BTC_EMA_span_days"]}_E{b["BTC_EMA_entry_band_fraction"]}_X0.03_btc0.55'
  sp.update(name=name,validation_plan=str((T/'spec.json').relative_to(R)));potential.append((sp,{**b,'is_new':True}))
assert len(potential)==42 and sum(sp is not None for sp,b in potential)==24 and len(plan['read_only_component_refs'])==10 and len(plan['read_only_grid_refs'])==8
btc_rule=next(sp['logic']for sp,fields in definitions(registry.fingerprint)if fields.get('BTC_EMA_span_days')==15 and fields.get('BTC_EMA_entry_band_fraction')==.01 and fields.get('BTC_EMA_exit_band_fraction')==.03 and fields['role']=='component')
plan['complete_rules']={'BTC':btc_rule,'ETH':ETH_SOURCE['2026']['logic'],'scope':'BTCjointchannel/volume/EMA same-decision entry andprice-or-EMAexit;eachspec declares span10/15/20 andentryband0.005/0.01/0.015,exitband0.03 fixed. ETH15/30EMA30band1.25percent,own1100/900funds fixed.'}
plan['complete_rules']['BTC_by_EMA_span']={str(span):next(sp['logic']for sp,fields in definitions(registry.fingerprint)if fields.get('BTC_EMA_span_days')==span and fields['role']=='component')for span in AXES['BTC_EMA_span_days']}
# Comparison isolates declared initial allocation with identical indicator rules,2000 total funds.
plan['comparator_scope']='PrimaryoldBTCwithoutEMAatmatched1100/900funding,raw55/45,fixedchannel15/30,N40/r1.1 andETHEMA30;same-entry-bandR39EMA20asymmetric3percentexit controls isolateEMAperiod;secondaryoldN30/r1raw50/50same2000total,differentexposure. Allcontrolsread-only.'
for year in('2025','2026'):
 oldsp=json.loads((R/f'research/experiments/20261010T194428Z/specs/fundalloc_{year}_btc0.5_ethS30_b0.0125.json').read_text());ref=ref_for(registry.fingerprint(oldsp));ref['kind']='OLD_N30_R1_HALF';plan['read_only_comparator_refs'].append(ref)
for year in('2025','2026'):
 for entry in(.005,.01,.015):
  oldsp=json.loads((R/f'research/experiments/20261011T094956Z/specs/asymvol_{year}_btcE{entry}_X0.03_btc0.55.json').read_text());ref=ref_for(registry.fingerprint(oldsp));ref.update(kind='MATCHED_SPAN20_ASYMMETRIC',matched_entry_band_fraction=entry);plan['read_only_comparator_refs'].append(ref)
paths=[T/n for n in('design.py','signals.py','volume_signals.py','volume_ema_signals.py','check_signals.py','evaluate.py','audit.py','forward.py','audit_forward.py')]+[R/'research/experiments/20261001T133655Z/evaluate.py',R/'research/experiments/20261001T133655Z/kernel.py',R/'research/experiments/20261001T213902Z/evaluate.py',R/'research/experiments/20261001T213902Z/audit.py',R/'.agents/skills/walk-forward-validation/scripts/walk_forward.py',R/'research/automation/registry.py',R/'research/experiments/20261001T013355Z/evaluate.py',R/'research/experiments/20261001T113625Z/signals.py'];plan['reused_code_sha256']={str(p.relative_to(R)):sha(p)for p in paths};plan['preflight_sha256']=sha(T/'preflight.py')
assert not(T/'spec.json').exists();(T/'spec.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n');(T/'specs').mkdir();(T/'results').mkdir();batch=[];grid=[]
def save(sp,fields,target):
 fp=registry.fingerprint(sp);assert fp not in canonical;path=T/'specs'/f'{sp["name"]}.json';assert not path.exists();path.write_text(json.dumps(sp,indent=2)+'\n');p=subprocess.run([sys.executable,'research/automation/registry.py','reserve',str(path.relative_to(R))],cwd=R,capture_output=True,text=True);print(sp['name'],p.returncode,p.stdout.strip(),flush=True)
 if p.returncode:raise RuntimeError('Stop before computation:'+p.stdout+p.stderr)
 b={'name':sp['name'],'fingerprint':fp,'spec':str(path.relative_to(R)),**fields};target.append(b);return b
for sp,b in potential:grid.append(save(sp,b,batch)if sp is not None else b)
(T/'batch.json').write_text(json.dumps(batch,indent=2)+'\n');(T/'grid_batch.json').write_text(json.dumps(grid,indent=2)+'\n');forward=[];fps={};oldfb=json.loads((S/'forward_batch.json').read_text())
for asset,capital in [('BTC',1500),('ETH',500)]:
 b=next(x for x in oldfb if x.get('asset')==asset);sp=json.loads((R/b['spec']).read_text());sp.update(name='forward_snapshot_'+asset,validation_plan=str((T/'spec.json').relative_to(R)));sp['parameters']['end_utc']=cutoff;fps[asset]=save(sp,{'asset':asset,'capital_usdt':capital},forward)['fingerprint']
sp=json.loads((R/oldfb[-1]['spec']).read_text());sp.update(name='forward_snapshot_combo',validation_plan=str((T/'spec.json').relative_to(R)));sp['parameters']['end_utc']=cutoff;sp['components']=[{'fingerprint':fps[a],'weight':w}for a,w in zip(('BTC','ETH'),(.75,.25))];save(sp,{'capital_usdt':2000},forward);(T/'forward_batch.json').write_text(json.dumps(forward,indent=2)+'\n')
print('PASS:24new histories+3original shadow cutoffs reserved;18exact gridconfigs and8comparatorpointers read-only;raw funds preserved.')
