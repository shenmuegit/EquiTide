"""Evaluate only preregistered definitions; --reproduce is an audit, not research."""
import argparse,csv,gzip,hashlib,json,platform,sys
from pathlib import Path
from ridge import *
registry=module('registry_m1',ROOT/'research/automation/registry.py')
dump=prev.dump

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--reproduce',action='store_true');args=parser.parse_args()
 batch=json.loads((ROUND/'batch.json').read_text());plan=json.loads((ROUND/'spec.json').read_text());records=registry.read_records(ROOT/'research/automation/registry.jsonl')
 for row in batch:
  spec=json.loads((ROOT/row['spec']).read_text());assert registry.fingerprint(spec)==row['fingerprint'];assert records[row['fingerprint']]['status'] in ('passed','rejected') if args.reproduce else records[row['fingerprint']]['status']=='reserved'
 folds=old.folds_for('pairs');datasets={};frames={};predictions={};native_predictions={};model_entries=[]
 for asset in ('BTC','ETH'):
  data=load(asset);datasets[asset]=data;ndata=native_data(data);decisions=data['times']
  features=factor_frame(ndata,decisions);assert features.filter(pl.col('input_max_available_ts')>pl.col('decision_ts')).height==0
  labels=continuous_labels(data);frame=features.join(labels,on='decision_ts',how='left');frames[asset]=frame
  native_labels=label_frame(native_config(data,whole_history=True),ndata,decisions).filter(pl.col('horizon')=='24h');nframe=features.join(native_labels,on='decision_ts',how='left')
  evidence={'features':features.to_dicts(),'continuous_labels':labels.to_dicts(),'native_labels_24h':native_labels.to_dicts()};path=ROUND/'results'/f'features_labels_{asset}.json.gz'
  if args.reproduce:assert json.loads(gzip.decompress(path.read_bytes()))==evidence
  else:dump(path,evidence)
  data['derived_evidence_path']=str(path.relative_to(ROOT));data['derived_evidence_sha256']=sha(path)
  for alpha in plan['alphas']:
   preds,audits=fitted_predictions(frame,folds,alpha);predictions[(asset,alpha)]=preds;path=ROUND/'results'/f'models_{asset}_a{alpha}.json.gz'
   if args.reproduce:assert json.loads(gzip.decompress(path.read_bytes()))==audits
   else:dump(path,audits)
   model_entries.append({'asset':asset,'alpha':alpha,'role':'continuous','path':str(path.relative_to(ROOT)),'sha256':sha(path),'folds':[{k:v for k,v in a.items() if k not in ('training_row_indices','predictions')} for a in audits]})
   print('MODEL',asset,alpha,'rows',[a['training_rows'] for a in audits],'positive_hours',[a['predicted_positive_hours'] for a in audits],flush=True)
  nf=[dict(folds[0])];nf[0]['test_end_signal_ns']=ns(plan['native']['end'])
  preds,audits=fitted_predictions(nframe,nf,1,native=True);native_predictions[asset]=preds;path=ROUND/'results'/f'models_native_{asset}.json.gz'
  if args.reproduce:assert json.loads(gzip.decompress(path.read_bytes()))==audits
  else:dump(path,audits)
  model_entries.append({'asset':asset,'alpha':1,'role':'native','path':str(path.relative_to(ROOT)),'sha256':sha(path),'folds':[{k:v for k,v in a.items() if k not in ('training_row_indices','predictions')} for a in audits]})
  print('NATIVE MODEL',asset,'positive_hours',audits[0]['predicted_positive_hours'],flush=True)
 report={'round':plan['round'],'plan_sha256':sha(ROUND/'spec.json'),'parent_commit':plan['parent_commit'],'folds':folds,'models':model_entries,'data':{a:{'hashes':x['hashes'],'metadata':x['meta'],'hourly_quotes':len(x['rows']),'funding_count':len(x['events']),'derived_evidence_path':x['derived_evidence_path'],'derived_evidence_sha256':x['derived_evidence_sha256']} for a,x in datasets.items()},'trials':[],'native_recovery':[],'legacy_recovery':[],'environment':{'python':platform.python_version(),'numpy':np.__version__,'polars':pl.__version__,'nautilus_trader':__import__('nautilus_trader').__version__,'sklearn':__import__('sklearn').__version__},'method':plan['validation'],'limits':plan['limits']}
 for row in batch:
  if row['role']=='legacy_aggregate':continue
  spec=json.loads((ROOT/row['spec']).read_text());p=spec['parameters'];asset=spec['universe'][0].split('/')[0];role=row['role'];results={}
  for m in (1,2,3):
   result=native_run(datasets[asset],p,m,native_predictions[asset]) if role=='native' else simulate(datasets[asset],p,m,folds,predictions[(asset,p['ridge_alpha'])]);results[str(m)]=result
   s=prev.summarize(result,role);print(json.dumps({'name':row['name'],'cost':m,**{k:v for k,v in s.items() if k in ('net_return_pct','max_drawdown_pct','round_trips','executions','status')}}),flush=True)
  path=ROUND/'results'/(row['name']+'.json.gz')
  if args.reproduce:assert results==json.loads(gzip.decompress(path.read_bytes())),'scenario mismatch '+row['name']
  else:dump(path,results)
  entry={**row,'parameters':p,'full_result_path':str(path.relative_to(ROOT)),'full_result_sha256':sha(path),'scenarios':{str(m):prev.summarize(results[str(m)],role) for m in (1,2,3)}}
  report['native_recovery' if role=='native' else 'trials'].append(entry)
 for asset in ('BTC','ETH'):
  group=[x for x in report['trials'] if asset in x['name']];share=sum(int(x['scenarios']['3']['net_return_pct']>0) for x in group)/len(group)
  for x in group:
   s=x['scenarios'];reasons=[]
   if not all(s[str(m)]['net_return_pct']>0 for m in (1,2,3)):reasons.append('cost_pressure_nonpositive')
   if s['1']['positive_folds_1x']<4:reasons.append('fewer_than_4_positive_folds')
   if s['3']['max_drawdown_pct']>25:reasons.append('drawdown_above_25_pct')
   if share<.6:reasons.append('parameter_neighborhood_below_60_pct_positive')
   if s['1']['round_trips']<4:reasons.append('fewer_than_4_round_trips')
   if any(s[str(m)]['cash_margin_violations'] for m in (1,2,3)):reasons.append('cash_or_margin_violation')
   if s['1']['gross_to_execution_cost'] is None or s['1']['gross_to_execution_cost']<2.5:reasons.append('gross_cost_safety_ratio_below_2_5')
   x.update(qualification='rejected' if reasons else 'passed',failure_reasons=reasons,neighborhood_positive_fraction_3x=share)
 for x in batch:
  if x['role']=='legacy_aggregate':report['legacy_recovery'].append({**x,'concrete_children':[t['fingerprint'] for t in report['native_recovery']],'actual_backtest_available':True,'qualification':'rejected','scope_note':'two true24h native cases restore actual evidence to abbreviated original scope; eight-hour examples not evaluated this round; no long-run acceptance from72h'})
 prior=json.loads((ROOT/'research/experiments/20261001T053425Z/report.json').read_text());report['reused_benchmarks']=[{'fingerprint':x['fingerprint'],'name':x['name'],'original_report':'research/experiments/20261001T053425Z/report.json','report_sha256':sha(ROOT/'research/experiments/20261001T053425Z/report.json'),'full_result_path':x['full_result_path'],'full_result_sha256':x['full_result_sha256'],'scenarios':x['scenarios']} for x in prior['benchmarks']]
 report['benchmark_note']='Prior45% initial-spot comparator reused without recalculation, cash0. Directional/gross exposure differs from25% matched carry. Sharpe is not averaged.'
 report['qualified']=sum(int(x['qualification']=='passed') for x in report['trials']);report['actual_scenarios']=60
 if args.reproduce:print('PASS: frozen features, labels, all38 actual model fits and all60 complete scenario outputs exactly reproduced');return
 dump(ROUND/'report.json',report)
 fields=['name','asset','ridge_alpha','buffer_usdt','cost_multiplier','net_return_pct','max_drawdown_pct','sharpe_annualized','calmar','round_trips','execution_cost_usdt','funding_usdt','positive_folds','qualification']
 with (ROUND/'sensitivity.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader()
  for x in report['trials']:
   for m,s in x['scenarios'].items():w.writerow({'name':x['name'],'asset':x['name'].split('_')[1],'ridge_alpha':x['parameters']['ridge_alpha'],'buffer_usdt':x['parameters']['buffer_usdt'],'cost_multiplier':m,**{k:s[k] for k in ('net_return_pct','max_drawdown_pct','sharpe_annualized','calmar','round_trips','execution_cost_usdt','funding_usdt')},'positive_folds':s['positive_folds_1x'],'qualification':x['qualification']})
 print('COMPLETED',len(report['trials']),'candidates',len(report['native_recovery']),'native, qualified',report['qualified'],flush=True)
if __name__=='__main__':main()
