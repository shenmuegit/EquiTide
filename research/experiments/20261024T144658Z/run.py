"""Passive BTC L31 / ETH L28 buffered-exit portfolios from immutable NAV."""
import argparse,copy,gzip,hashlib,importlib.util,itertools,json,subprocess,sys
from datetime import datetime,timezone
from decimal import Decimal as D
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
HURDLES,BUFFERS=[.01,.02,.04],[0,.0025,.005,.01]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rel=lambda p:str(p.relative_to(ROOT))
now=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
readgz=lambda p:json.loads(gzip.decompress(p.read_bytes()))
def module(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
base=module(ROOT/'research/experiments/20261023T204326Z/run.py','immutable_parent_helpers')
keys,align,metric,summarize,recover=base.keys,base.align,base.metric,base.summarize,base.recover
def gzwrite(p,x):p.write_bytes(gzip.compress(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode(),mtime=0))
def call(command,row,*args):
 p=subprocess.run([sys.executable,'research/automation/registry.py',command,row['spec'],*args],cwd=ROOT,capture_output=True,text=True);x={'name':row['name'],'fingerprint':row['fingerprint'],'command':command,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr};print(json.dumps(x),flush=True);assert p.returncode==0 and p.stdout.strip()==row['fingerprint'];return x
def anchor_configs():
 refs=json.loads((R/'anchors.json').read_text());docs={};out={}
 for name,ref in refs.items():
  path=ref['report'];assert sha(ROOT/path)==ref['report_sha256']
  if path not in docs:docs[path]=json.loads((ROOT/path).read_text())
  c=docs[path]['configs'][name];assert c['fingerprint']==ref['fingerprint'] and c['status']==ref['original_status'];out[name]={**c,'BTC_exit_buffer_fraction':c.get('BTC_exit_buffer_fraction',0),'ETH_exit_buffer_fraction':c.get('ETH_exit_buffer_fraction',0),'read_only_anchor':True}
 assert len(out)==9;return out
def grid_configs(configs):return {**anchor_configs(),**configs}
def neighbors(c,configs):
 axes={'BTC_return_hurdle':HURDLES,'BTC_exit_buffer_fraction':BUFFERS,'ETH_return_hurdle':HURDLES,'ETH_exit_buffer_fraction':BUFFERS}
 return [x for x in configs.values() if all(abs(a.index(x[p])-a.index(c[p]))<=1 for p,a in axes.items())]
def freeze():module(R/'freeze_batch.py','current_fullgrid_freeze').main()
def evaluate():
 assert not (R/'report.json').exists();plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');assert all(records[x['fingerprint']]['status']=='reserved' for x in batch);started=now();oldengine,markets,common,vectors,ss=recover(plan);(R/'results').mkdir();configs={}
 for row in batch:
  spec=json.loads((ROOT/row['spec']).read_text());fps=row['source_fingerprints'];scenes={};arc={'spec':spec,'fingerprint':row['fingerprint'],'source_fingerprints':fps,'scenes':{}}
  for k in ['1','2','3']:
   v=vectors[fps[0],k]+vectors[fps[1],k];s=summarize(v,[ss[fp][k] for fp in fps],common);scenes[k]=s;arc['scenes'][k]={'summary':s,'source_full_NAV_sha256':[plan['component_sources'][fp]['NAV_sha256_by_cost'][k] for fp in fps]}
  p=R/'results'/(row['name']+'.json.gz');gzwrite(p,arc);configs[row['name']]={**row,'archive':rel(p),'archive_sha256':sha(p),'scenes':scenes,'positive_folds_1x':sum(f['net_return_pct']>0 for f in scenes['1']['folds'])};print(row['name'],scenes['1']['net_return_pct'],scenes['3']['net_return_pct'],flush=True)
 grid=grid_configs(configs)
 for c in configs.values():
  ns=neighbors(c,grid);frac=sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns);c['sensitivity']={'neighbor_names':[x['name'] for x in ns],'neighbor_count':len(ns),'four_dimensional_local_3x_positive_fraction':frac};s=c['scenes'];ratio=s['1']['gross_reference_PnL_to_execution_cost'];c['criteria']={'positive_all_costs':all(x['net_return_pct']>0 for x in s.values()),'eight_positive_1x_folds':c['positive_folds_1x']>=8,'composite_DD3_lte25pct':s['3']['max_drawdown_pct']<=25,'full4D_neighbourhood_positive3_gte60pct':frac>=.6,'four_round_trips1':s['1']['round_trips']>=4,'gross_plus_funding_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'no_negative_sleeve_collateral':all(x['cash_or_units_violations']==0 for x in s.values()),'no_source_order_rejections':all(x['rejected_orders']==0 for x in s.values()),'no_either_sleeve_margin_violations':all(x['margin']['independent_sleeve_violations']==0 for x in s.values()),'terminal_flat':all(D(x['terminal_units'])==0 for x in s.values())};c['status']='passed' if all(c['criteria'].values()) else 'rejected';c['failed_criteria']=[k for k,v in c['criteria'].items() if not v]
 cs=list(configs.values());report={'round':R.name,'evaluation_started_utc':started,'frozen_plan_sha256':sha(R/'plan.json'),'time_boundaries':plan['time_boundaries'],'component_sources':plan['component_sources'],'input_data':plan['data'],'configs':configs,'read_only_anchor_references':json.loads((R/'anchors.json').read_text()),'summary':{'new_configs':135,'candidate_configs':135,'benchmark_configs':0,'new_component_backtests':0,'source_configs_reused_read_only':24,'source_cost_scenes_hash_verified':72,'cost_scenarios':405,'read_only_anchor_configs':9,'full_grid_configs':144,'passed':[c['name'] for c in cs if c['status']=='passed'],'rejected':[c['name'] for c in cs if c['status']=='rejected'],'positive_configs_by_cost':{k:sum(c['scenes'][k]['net_return_pct']>0 for c in cs) for k in ['1','2','3']}},'axis':{'source_points':{a:len(m['ts']) for a,m in markets.items()},'union_points':len(common['keys']),'union_axis_sha256':common['sha256'],'projection_policy':'Last completed(ts,eventcode)sourceNAV,not interpolation or normalization.','daily_boundaries':len(common['daily_indices']),'folds':len(common['fold_indices'])-1},'scope':plan['limits']};put(R/'report.json',report);print(json.dumps(report['summary']),flush=True)
def finish():
 report=json.loads((R/'report.json').read_text());done=[]
 for row in json.loads((R/'batch.json').read_text()):done.append(call('finish',row,report['configs'][row['name']]['status'],rel(R/'report.json')));put(R/'finish.json',done)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['freeze','evaluate','finish']);globals()[p.parse_args().command]()
