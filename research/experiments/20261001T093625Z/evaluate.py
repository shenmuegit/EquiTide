"""Run22 reserved new configurations, retaining each success/zero/negative path."""
import argparse,csv,gzip,json,platform
from pathlib import Path
from long_carry import *
reg=module('registry0936_eval',ROOT/'research/automation/registry.py');dump=prev.dump

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--reproduce',action='store_true');args=parser.parse_args();batch=json.loads((ROUND/'batch.json').read_text());plan=json.loads((ROUND/'spec.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl')
 for b in batch:
  s=json.loads((ROOT/b['spec']).read_text());assert reg.fingerprint(s)==b['fingerprint'];assert records[b['fingerprint']]['status'] in ('passed','rejected') if args.reproduce else records[b['fingerprint']]['status']=='reserved'
 folds=make_folds();datasets={};predictions={};native_predictions={};models=[]
 for asset in ('BTC','ETH'):
  data=load(asset);datasets[asset]=data;features,reference=reused_features(data);data['feature_reference']=reference;label_evidence={}
  for h in plan['holding_hours']:
   labels=continuous_labels(data,h);label_evidence[str(h)]=labels.to_dicts();frame=features.join(labels,on='decision_ts',how='left')
   for alpha in plan['alphas']:
    prediction,audit=fitted_predictions(frame,folds,alpha);predictions[(asset,h,alpha)]=prediction;path=ROUND/'results'/f'models_{asset}_h{h}_a{alpha}.json.gz'
    if args.reproduce:assert json.loads(gzip.decompress(path.read_bytes()))==audit,'model audit mismatch '+path.name
    else:dump(path,audit)
    models.append({'asset':asset,'holding_hours':h,'alpha':alpha,'role':'continuous','path':str(path.relative_to(ROOT)),'sha256':sha(path),'folds':[{k:v for k,v in a.items() if k not in ('training_row_indices','predictions')} for a in audit]})
    print('MODEL',asset,'H',h,'alpha',alpha,'training',[a['training_rows'] for a in audit],'positive_hours',[a['predicted_positive_hours'] for a in audit],flush=True)
  nlabels=native_labels(native_config(data,whole_history=True),native_data(data),data['times']);label_evidence['native8']=nlabels.to_dicts();nf=[dict(old.folds_for('pairs')[0])];nf[0]['test_end_signal_ns']=ns(plan['native']['end']);nframe=features.join(nlabels,on='decision_ts',how='left');prediction,audit=fitted_predictions(nframe,nf,1,native=True);native_predictions[asset]=prediction;path=ROUND/'results'/f'models_native8_{asset}.json.gz'
  if args.reproduce:assert json.loads(gzip.decompress(path.read_bytes()))==audit
  else:dump(path,audit)
  models.append({'asset':asset,'holding_hours':8,'alpha':1,'role':'native','path':str(path.relative_to(ROOT)),'sha256':sha(path),'folds':[{k:v for k,v in a.items() if k not in ('training_row_indices','predictions')} for a in audit]});print('NATIVE8 MODEL',asset,'positive_hours',audit[0]['predicted_positive_hours'],flush=True)
  path=ROUND/'results'/f'labels_{asset}.json.gz'
  if args.reproduce:assert json.loads(gzip.decompress(path.read_bytes()))==label_evidence
  else:dump(path,label_evidence)
  data['derived_evidence_path']=str(path.relative_to(ROOT));data['derived_evidence_sha256']=sha(path)
 r={'round':plan['round'],'plan_sha256':sha(ROUND/'spec.json'),'parent_commit':plan['parent_commit'],'folds':folds,'models':models,'method':plan['validation'],'limits':plan['limits'],'data':{a:{'hashes':x['hashes'],'metadata':x['meta'],'hourly_quotes':len(x['rows']),'funding_count':len(x['events']),'feature_reference':x['feature_reference'],'derived_evidence_path':x['derived_evidence_path'],'derived_evidence_sha256':x['derived_evidence_sha256']} for a,x in datasets.items()},'trials':[],'native_recovery':[],'benchmarks':[],'environment':{'python':platform.python_version(),'numpy':np.__version__,'polars':pl.__version__,'nautilus_trader':__import__('nautilus_trader').__version__,'sklearn':__import__('sklearn').__version__}}
 for b in batch:
  spec=json.loads((ROOT/b['spec']).read_text());p=spec['parameters'];asset=spec['universe'][0].split('/')[0];role=b['role'];result={}
  for m in (1,2,3):
   s=native_run(datasets[asset],m,native_predictions[asset]) if role=='native' else (benchmark(datasets[asset],m,folds) if role=='benchmark' else simulate(datasets[asset],p,m,folds,predictions[(asset,p['holding_hours'],p['ridge_alpha'])]));result[str(m)]=s;summary=prev.summarize(s,role)
   print(json.dumps({'name':b['name'],'cost':m,**{k:v for k,v in summary.items() if k in ('net_return_pct','max_drawdown_pct','round_trips','executions','status')}}),flush=True)
  path=ROUND/'results'/(b['name']+'.json.gz')
  if args.reproduce:assert json.loads(gzip.decompress(path.read_bytes()))==result,'scenario mismatch '+b['name']
  else:dump(path,result)
  r[{'candidate':'trials','native':'native_recovery','benchmark':'benchmarks'}[role]].append({**b,'parameters':p,'full_result_path':str(path.relative_to(ROOT)),'full_result_sha256':sha(path),'scenarios':{str(m):prev.summarize(result[str(m)],role) for m in (1,2,3)}})
 for asset in ('BTC','ETH'):
  group=[x for x in r['trials'] if asset in x['name']];share=sum(x['scenarios']['3']['net_return_pct']>0 for x in group)/len(group)
  for x in group:
   s=x['scenarios'];reasons=[]
   if not all(s[str(m)]['net_return_pct']>0 for m in (1,2,3)):reasons.append('cost_pressure_nonpositive')
   if s['1']['positive_folds_1x']<3:reasons.append('fewer_than3_of4_positive_folds')
   if s['3']['max_drawdown_pct']>25:reasons.append('drawdown_above25pct')
   if share<.6:reasons.append('positive_parameter_neighborhood_below60pct')
   if s['1']['round_trips']<2:reasons.append('fewer_than2_round_trips')
   if s['1']['gross_to_execution_cost'] is None or s['1']['gross_to_execution_cost']<2.5:reasons.append('gross_execution_cost_safety_below2_5')
   if any(s[str(m)]['cash_margin_violations'] for m in (1,2,3)):reasons.append('cash_margin_violations')
   x.update(qualification='rejected' if reasons else 'passed',failure_reasons=reasons,neighborhood_positive_fraction_3x=share)
 r['qualified']=sum(x['qualification']=='passed' for x in r['trials']);r['actual_scenarios']=66
 if args.reproduce:print('PASS: new long/native8 labels, all74 model fits/predictions and all66 full scenario outputs exactly match frozen archives');return
 dump(ROUND/'report.json',r)
 fields=['name','asset','holding_hours','ridge_alpha','cost_multiplier','net_return_pct','max_drawdown_pct','sharpe_annualized','calmar','round_trips','execution_cost_usdt','funding_usdt','positive_folds','qualification']
 with (ROUND/'sensitivity.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader()
  for x in r['trials']:
   for m,s in x['scenarios'].items():w.writerow({'name':x['name'],'asset':x['name'].split('_')[1],'holding_hours':x['parameters']['holding_hours'],'ridge_alpha':x['parameters']['ridge_alpha'],'cost_multiplier':m,**{k:s[k] for k in ('net_return_pct','max_drawdown_pct','sharpe_annualized','calmar','round_trips','execution_cost_usdt','funding_usdt')},'positive_folds':s['positive_folds_1x'],'qualification':x['qualification']})
 print('COMPLETED',len(r['trials']),'candidates,',len(r['native_recovery']),'native8,',len(r['benchmarks']),'benchmarks, qualified',r['qualified'],flush=True)
if __name__=='__main__':main()
