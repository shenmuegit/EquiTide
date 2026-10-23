"""Reserve, evaluate and individually finish the fixed perpetual directional batch."""
import argparse,gzip,hashlib,importlib.util,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
import engine
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
LOOKS,HURDLES=[20,25,30],[.01,.02,.04]
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

def anchor_configs():
 plan=json.loads((R/'plan.json').read_text());source=plan['anchor_source'];assert sha(ROOT/source['report'])==source['report_sha256'];old=json.loads((ROOT/source['report']).read_text());refs=json.loads((R/'anchors.json').read_text());out={}
 for name,ref in refs.items():
  c=old['configs'][name];assert c['fingerprint']==ref['fingerprint'] and c['status']==ref['original_status'] and c['lookback_days']==20;out[name]=c
 assert len(out)==6;return out

def grid_configs(configs):return {**anchor_configs(),**configs}

def freeze():
 import copy
 assert not (R/'plan.json').exists();ctx=json.loads((R/'context.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');source=ROOT/'research/experiments/20261023T164355Z';plan=copy.deepcopy(json.loads((source/'plan.json').read_text()));old=json.loads((source/'report.json').read_text());assert sha(source/'engine.py')==sha(R/'engine.py')
 plan.update(round=R.name,frozen_at_utc=now(),trigger_utc='2026-10-23T18:44:00.920Z',hypothesis='The previous20day boundary waspositive undercosts but lacked foldbreadth. Predeclare longer25/30daylookbacks tocheck whether that boundary extends into a robust plateau. This followsseenhistory and is not independentconfirmation.')
 plan['grid']={'lookback_days':LOOKS,'return_hurdle':HURDLES,'assets':['BTC','ETH'],'new_financial_candidates':12,'read_only_anchor_configs':6,'all_grid_configs':18,'fixed_exit_ROC':0,'preset_center':{'lookback_days':25,'return_hurdle':.02}}
 plan['anchor_source']={'report':rel(source/'report.json'),'report_sha256':sha(source/'report.json'),'plan':rel(source/'plan.json'),'plan_sha256':sha(source/'plan.json'),'engine':rel(source/'engine.py'),'engine_sha256':sha(source/'engine.py'),'policy':'Only6existingL20configs are read-only grid anchors. No oldNAV/signals/trades or qualifications recomputed. Original status and reportSHA retained.'}
 plan['hold_reference_source']=plan.pop('source_comparison');plan['sensitivity']='Perasset20/25/30lookback x1/2/4percent entry;6old20dayanchors read-only,12new25/30configs. Full3x3neighborgrid;onlynewconfigqualificationcomputed. No retroactive rerating of anchors,no gridextensionafteroutcomes.'
 plan['novelty']={'initial16_missing_actual_results':0,'prior_registry_events':ctx['registry_events'],'prior_registry_ids':ctx['registry_ids'],'prior_canonical_research_definitions':ctx['canonical_research_definitions_excluding_observations'],'all_prior_conclusions_read':len(ctx['prior_conclusions_read']),'multiple_testing':'Adaptive direction chosen between rounds fromseenhistory;no untouchedfinalholdout,noDSR/PBO.'}
 plan['lookback_availability']={'first_decision_day_index':engine.START,'maximum_lookback':max(LOOKS),'earliest_completed_close_index':engine.START-1-max(LOOKS),'rule':'Nonnegative priorcloseindex and fixed30warmup+3initialgap;do not extendlookbacks beyond dataavailability or change originalOOS.'};assert engine.START-1-max(LOOKS)>=0
 for files in plan['data']['assets'].values():
  for f in files:assert sha(ROOT/f['path'])==f['sha256'] and (ROOT/f['path']).stat().st_size==f['bytes']
 refs={}
 for name,c in old['configs'].items():
  if c['lookback_days']!=20:continue
  rec=records[c['fingerprint']];assert rec['result_available'] and rec['report_sha256']==sha(source/'report.json') and rec['status']==c['status']
  refs[name]={'name':name,'fingerprint':c['fingerprint'],'asset':c['asset'],'lookback_days':20,'return_hurdle':c['return_hurdle'],'original_status':c['status'],'source_report':rel(source/'report.json'),'source_report_sha256':sha(source/'report.json'),'source_spec':c['spec'],'source_spec_sha256':sha(ROOT/c['spec']),'source_archive':c['archive'],'source_archive_sha256':c['archive_sha256'],'NAV_sha256_by_cost':{k:z['NAV_sha256_f64le'] for k,z in c['scenes'].items()}}
 assert len(refs)==6;put(R/'plan.json',plan);put(R/'anchors.json',refs);(R/'specs').mkdir();batch=[]
 for asset in ['BTC','ETH']:
  for L in [25,30]:
   for H in HURDLES:
    template=old['configs'][f'perp_zeroexit_{asset}_L20_H{int(H*100):02d}'];spec=copy.deepcopy(json.loads((ROOT/template['spec']).read_text()));name=f'perp_zeroexit_{asset}_L{L}_H{int(H*100):02d}';spec['name']=name;spec['parameters']['lookback_days']=L;spec['validation_plan']=rel(R/'plan.json');path=R/'specs'/(name+'.json');put(path,spec);fp=reg.fingerprint(spec);assert fp not in records or records[fp].get('result_available') is not True and records[fp]['status'] in ['blocked','abandoned'];batch.append({'name':name,'role':'candidate','spec':rel(path),'fingerprint':fp,'asset':asset,'lookback_days':L,'return_hurdle':H,'capital_usdt':10000})
 assert len(batch)==len({x['fingerprint'] for x in batch})==12;assert not ({x['fingerprint'] for x in batch}&{x['fingerprint'] for x in refs.values()});put(R/'batch.json',batch);put(R/'spec.json',json.loads((R/'specs/perp_zeroexit_BTC_L25_H02.json').read_text()));done=[]
 for row in batch:done.append(call('reserve',row));put(R/'reserve.json',done)
 print('FROZEN_AND_RESERVED12_NEW_PLUS6READONLY',sha(R/'plan.json'),flush=True)

def evaluate():
 assert not (R/'report.json').exists();plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');assert all(records[x['fingerprint']]['status']=='reserved' for x in batch);started=now();markets={a:engine.load_market(a,files) for a,files in plan['data']['assets'].items()};configs={};(R/'results').mkdir()
 for row in batch:
  spec=json.loads((ROOT/row['spec']).read_text());arc={'spec':spec,'fingerprint':row['fingerprint'],'scenes':{}};scenes={}
  for k in ['1','2','3']:v,z=engine.simulate(spec,markets[row['asset']],int(k));arc['scenes'][k]=z;scenes[k]=z['summary']
  path=R/'results'/(row['name']+'.json.gz');gzwrite(path,arc);configs[row['name']]={**row,'archive':rel(path),'archive_sha256':sha(path),'scenes':scenes,'positive_folds_1x':sum(x['net_return_pct']>0 for x in scenes['1']['folds'])};print(row['name'],scenes['1']['net_return_pct'],scenes['3']['net_return_pct'],flush=True)
 for c in configs.values():
  if c.get('role')=='benchmark':c.update(status='rejected',criteria={'reference_only_no_alpha_qualification':False},sensitivity={'reference_only':True});continue
  neighbors=[x for x in grid_configs(configs).values() if x.get('role')!='benchmark' and x['asset']==c['asset'] and abs(LOOKS.index(x['lookback_days'])-LOOKS.index(c['lookback_days']))<=1 and abs(HURDLES.index(x['return_hurdle'])-HURDLES.index(c['return_hurdle']))<=1];frac=sum(x['scenes']['3']['net_return_pct']>0 for x in neighbors)/len(neighbors);c['sensitivity']={'neighbor_names':[x['name'] for x in neighbors],'neighbor_count':len(neighbors),'local_3x_neighbor_positive_fraction':frac};s=c['scenes'];ratio=s['1']['gross_reference_PnL_to_execution_cost'];c['criteria']={'positive_all_costs':all(x['net_return_pct']>0 for x in s.values()),'eight_positive_1x_folds':c['positive_folds_1x']>=8,'composite_DD3_lte25pct':s['3']['max_drawdown_pct']<=25,'neighbourhood_positive3_gte60pct':frac>=.6,'four_round_trips1':s['1']['round_trips']>=4,'gross_plus_funding_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'no_negative_collateral':all(x['cash_or_units_violations']==0 for x in s.values()),'no_order_rejections':all(x['rejected_orders']==0 for x in s.values()),'no_margin_proxy_violations':all(x['margin']['violations']==0 for x in s.values()),'terminal_flat':all(float(x['terminal_units'])==0 for x in s.values())};c['status']='passed' if all(c['criteria'].values()) else 'rejected';c['failed_criteria']=[k for k,v in c['criteria'].items() if not v]
 candidates=[x for x in configs.values() if x.get('role')!='benchmark'];report={'round':R.name,'evaluation_started_utc':started,'frozen_plan_sha256':sha(R/'plan.json'),'anchor_source_report_sha256':plan['anchor_source']['report_sha256'],'time_boundaries':plan['time_boundaries'],'input_data':plan['data'],'configs':configs,'summary':{'new_configs':len(batch),'candidate_configs':len(batch),'benchmark_configs':0,'cost_scenarios':3*len(batch),'read_only_anchor_configs':6,'read_only_anchor_cost_scenes':18,'full_grid_configs':18,'passed':[x['name'] for x in candidates if x['status']=='passed'],'rejected':[x['name'] for x in candidates if x['status']=='rejected'],'positive_configs_by_cost':{k:sum(x['scenes'][k]['net_return_pct']>0 for x in candidates) for k in ['1','2','3']}},'scope':plan['limits'],'axis':{a:{'points':len(m['ts']),'axis_sha256':m['axis_sha256'],'axis_prices_sha256_f64le':m['axis_price_sha256_f64le'],'daily_boundary_count':len(m['daily_indices']),'folds':len(m['fold_indices'])-1} for a,m in markets.items()}}
 report['read_only_anchor_references']=json.loads((R/'anchors.json').read_text());report['anchor_original_statuses_unchanged']=True
 put(R/'report.json',report);print('SUMMARY',json.dumps(report['summary']),flush=True)

def finish():
 report=json.loads((R/'report.json').read_text());done=[]
 for row in json.loads((R/'batch.json').read_text()):done.append(call('finish',row,report['configs'][row['name']]['status'],rel(R/'report.json')));put(R/'finish.json',done)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['freeze','evaluate','finish']);globals()[p.parse_args().command]()
