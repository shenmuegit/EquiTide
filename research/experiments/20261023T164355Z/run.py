"""Reserve, evaluate and individually finish the fixed perpetual directional batch."""
import argparse,gzip,hashlib,importlib.util,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
import engine
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
LOOKS,HURDLES=[5,10,20],[.01,.02,.04]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rel=lambda p:str(p.relative_to(ROOT))
now=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def module(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
def gzwrite(p,x):
 p.write_bytes(gzip.compress(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode(),mtime=0))
def call(command,row,*args):
 p=subprocess.run([sys.executable,'research/automation/registry.py',command,row['spec'],*args],cwd=ROOT,capture_output=True,text=True);x={'name':row['name'],'fingerprint':row['fingerprint'],'command':command,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr};print(json.dumps(x),flush=True);assert p.returncode==0 and p.stdout.strip()==row['fingerprint'];return x

def freeze():
 import copy
 assert not (R/'plan.json').exists()
 ctx=json.loads((R/'context.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');source=ROOT/'research/experiments/20261023T124125Z';base=json.loads((source/'plan.json').read_text());plan=copy.deepcopy(base);rules=copy.deepcopy(base['rules'])
 rules['signal']='At daily decision i,priorcompletedperpetualROC=C[i-1]/C[i-1-L]-1. Flat enterslong iff ROC>H,short iff ROC<-H. Existinglong persistswhile ROC>0;existingshort persistswhile ROC<0. At ROC=0 exit. OppositeROC crossingfullentryband closesoldthenentersopposite at00:01. At exact +/-H no newentry;an existing same-sign position remains. State is actualsignedquantity,no unpublishedprice/funding input.'
 plan.update(round=R.name,frozen_at_utc=now(),trigger_utc='2026-10-23T16:43:55.843Z',hypothesis='Zero-crossing exits may reduce near-entry-threshold churn relative to already-tested signed momentum cash-band. Persistence may also retain losing exposure longer. This exit change is a new research hypothesis,not a claim of the cited paper or independent validation.',rules=rules)
 plan['grid']={'lookback_days':LOOKS,'return_hurdle':HURDLES,'assets':['BTC','ETH'],'financial_candidates':18,'fixed_exit_ROC':0,'preset_center':{'lookback_days':10,'return_hurdle':.02}}
 plan['source_comparison']={'report':rel(source/'report.json'),'report_sha256':sha(source/'report.json'),'source_plan':rel(source/'plan.json'),'source_plan_sha256':sha(source/'plan.json'),'source_engine':rel(source/'engine.py'),'source_engine_sha256':sha(source/'engine.py'),'policy':'All18oldcashbandand2oldconstantlongresultsread-only. No oldstrategy/NAV recomputation or re-registration;use stored metrics only. Samecosts/budget/period,sole rule changezeroexit hysteresis.'}
 plan['sensitivity']='Per asset full lookback5/10/20 x entry1/2/4percent grid;fixed zeroexit. Inclusive adjacent-index2D neighborhoods. All18configs54costscenes594folds retained;no post-result extension or parameter choice.'
 plan['sources'][0]['scope']='Original2012multiassetfutures12monthown-returnmomentummotivation only;zeroexit hysteresis and5/10/20daycryptogrid are this experiment,not a replication or profit claim.'
 plan['novelty']={'initial16_missing_actual_results':ctx['initial_16_missing_actual_results'],'initial16_legacy_evidence_resolution':ctx['initial_16_evidence_resolution'],'prior_registry_events':ctx['registry_events'],'prior_registry_ids':ctx['registry_ids'],'prior_canonical_research_definitions':ctx['canonical_research_definitions_excluding_observations'],'all_prior_conclusions_read':len(ctx['prior_conclusions_read']),'multiple_testing':'Thousands of related trials and reused2025-26history;no untouchedfinalholdout,noDSR/PBO qualification.'}
 assert not any(x.get('spec',{}).get('family')=='perpetual-daily-signed-momentum-zero-exit-hysteresis' for x in records.values())
 for files in plan['data']['assets'].values():
  for f in files:assert sha(ROOT/f['path'])==f['sha256'] and (ROOT/f['path']).stat().st_size==f['bytes']
 put(R/'plan.json',plan);(R/'specs').mkdir();batch=[]
 for asset in ['BTC','ETH']:
  for look in LOOKS:
   for hurdle in HURDLES:
    oldname=f'perp_trend_{asset}_L{look}_H{int(hurdle*100):02d}';spec=json.loads((source/'specs'/(oldname+'.json')).read_text());name=f'perp_zeroexit_{asset}_L{look}_H{int(hurdle*100):02d}'
    spec.update(family='perpetual-daily-signed-momentum-zero-exit-hysteresis',name=name,logic=rules,validation_plan=rel(R/'plan.json'),sources=plan['sources']);spec['parameters']['exit_ROC']=0;spec['parameters']['persistence']='Keep existing direction through same-sign neutral entry band;no resizing.'
    path=R/'specs'/(name+'.json');put(path,spec);fp=reg.fingerprint(spec);assert fp not in records or records[fp].get('result_available') is not True and records[fp]['status'] in ['blocked','abandoned'];batch.append({'name':name,'role':'candidate','spec':rel(path),'fingerprint':fp,'asset':asset,'lookback_days':look,'return_hurdle':hurdle,'capital_usdt':10000,'prior_cash_band_name':oldname})
 assert len(batch)==len({x['fingerprint'] for x in batch})==18;put(R/'batch.json',batch);put(R/'spec.json',json.loads((R/'specs/perp_zeroexit_BTC_L10_H02.json').read_text()));done=[]
 for row in batch:done.append(call('reserve',row));put(R/'reserve.json',done)
 print('FROZEN_AND_RESERVED18',sha(R/'plan.json'),flush=True)

def evaluate():
 assert not (R/'report.json').exists();plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');assert all(records[x['fingerprint']]['status']=='reserved' for x in batch);started=now();markets={a:engine.load_market(a,files) for a,files in plan['data']['assets'].items()};configs={};(R/'results').mkdir()
 for row in batch:
  spec=json.loads((ROOT/row['spec']).read_text());arc={'spec':spec,'fingerprint':row['fingerprint'],'scenes':{}};scenes={}
  for k in ['1','2','3']:v,z=engine.simulate(spec,markets[row['asset']],int(k));arc['scenes'][k]=z;scenes[k]=z['summary']
  path=R/'results'/(row['name']+'.json.gz');gzwrite(path,arc);configs[row['name']]={**row,'archive':rel(path),'archive_sha256':sha(path),'scenes':scenes,'positive_folds_1x':sum(x['net_return_pct']>0 for x in scenes['1']['folds'])};print(row['name'],scenes['1']['net_return_pct'],scenes['3']['net_return_pct'],flush=True)
 for c in configs.values():
  if c.get('role')=='benchmark':c.update(status='rejected',criteria={'reference_only_no_alpha_qualification':False},sensitivity={'reference_only':True});continue
  neighbors=[x for x in configs.values() if x.get('role')!='benchmark' and x['asset']==c['asset'] and abs(LOOKS.index(x['lookback_days'])-LOOKS.index(c['lookback_days']))<=1 and abs(HURDLES.index(x['return_hurdle'])-HURDLES.index(c['return_hurdle']))<=1];frac=sum(x['scenes']['3']['net_return_pct']>0 for x in neighbors)/len(neighbors);c['sensitivity']={'neighbor_names':[x['name'] for x in neighbors],'neighbor_count':len(neighbors),'local_3x_neighbor_positive_fraction':frac};s=c['scenes'];ratio=s['1']['gross_reference_PnL_to_execution_cost'];c['criteria']={'positive_all_costs':all(x['net_return_pct']>0 for x in s.values()),'eight_positive_1x_folds':c['positive_folds_1x']>=8,'composite_DD3_lte25pct':s['3']['max_drawdown_pct']<=25,'neighbourhood_positive3_gte60pct':frac>=.6,'four_round_trips1':s['1']['round_trips']>=4,'gross_plus_funding_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'no_negative_collateral':all(x['cash_or_units_violations']==0 for x in s.values()),'no_order_rejections':all(x['rejected_orders']==0 for x in s.values()),'no_margin_proxy_violations':all(x['margin']['violations']==0 for x in s.values()),'terminal_flat':all(float(x['terminal_units'])==0 for x in s.values())};c['status']='passed' if all(c['criteria'].values()) else 'rejected';c['failed_criteria']=[k for k,v in c['criteria'].items() if not v]
 candidates=[x for x in configs.values() if x.get('role')!='benchmark'];report={'round':R.name,'evaluation_started_utc':started,'frozen_plan_sha256':sha(R/'plan.json'),'source_comparison_report_sha256':plan['source_comparison']['report_sha256'],'time_boundaries':plan['time_boundaries'],'input_data':plan['data'],'configs':configs,'summary':{'new_configs':18,'candidate_configs':18,'benchmark_configs':0,'cost_scenarios':54,'passed':[x['name'] for x in candidates if x['status']=='passed'],'rejected':[x['name'] for x in candidates if x['status']=='rejected'],'positive_configs_by_cost':{k:sum(x['scenes'][k]['net_return_pct']>0 for x in candidates) for k in ['1','2','3']}},'scope':plan['limits'],'axis':{a:{'points':len(m['ts']),'axis_sha256':m['axis_sha256'],'axis_prices_sha256_f64le':m['axis_price_sha256_f64le'],'daily_boundary_count':len(m['daily_indices']),'folds':len(m['fold_indices'])-1} for a,m in markets.items()}}
 source=plan['source_comparison'];assert sha(ROOT/source['report'])==source['report_sha256'];oldreport=json.loads((ROOT/source['report']).read_text());fields=['net_return_pct','max_drawdown_pct','sharpe_365','calmar','cost_usdt','executions','round_trips','funding_usdt']
 report['read_only_comparisons']={'source_report':source['report'],'source_report_sha256':source['report_sha256'],'matched_cash_band':{row['name']:{'source_name':row['prior_cash_band_name'],'source_fingerprint':oldreport['configs'][row['prior_cash_band_name']]['fingerprint'],'scenes':{k:{a:z[a] for a in fields} for k,z in oldreport['configs'][row['prior_cash_band_name']]['scenes'].items()}} for row in batch},'constant_long_references':{name:{'source_fingerprint':c['fingerprint'],'asset':c['asset'],'scenes':{k:{a:z[a] for a in fields} for k,z in c['scenes'].items()}} for name,c in oldreport['configs'].items() if c.get('role')=='benchmark'},'old_configs_recalculated_or_reserved':0}
 put(R/'report.json',report);print('SUMMARY',json.dumps(report['summary']),flush=True)

def finish():
 report=json.loads((R/'report.json').read_text());done=[]
 for row in json.loads((R/'batch.json').read_text()):done.append(call('finish',row,report['configs'][row['name']]['status'],rel(R/'report.json')));put(R/'finish.json',done)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['freeze','evaluate','finish']);globals()[p.parse_args().command]()
