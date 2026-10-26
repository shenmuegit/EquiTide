"""Independent BTC/ETH entry budgets using immutable quantity-specific source ledgers."""
import argparse,copy,functools,gzip,hashlib,importlib.util,itertools,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
from decimal import Decimal as D
import numpy as np
import engine
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
EXITS=[0] # Required by immutable ledger auditor import; not a grid axis or new evaluation.
NOTIONALS=[1000,2000,3000];SLOWS=[28,31];LOOKS=[1,2,3];HURDLES=[.02,.04,.06]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rel=lambda p:str(p.relative_to(ROOT))
now=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def module(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
parent=module(ROOT/'research/experiments/20261025T145537Z/run.py','native370_parent_helpers')
keys,align=parent.keys,parent.align
def gzwrite(p,x):p.write_bytes(gzip.compress(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode(),mtime=0))
def call(command,row,*args):
 p=subprocess.run([sys.executable,'research/automation/registry.py',command,row['spec'],*args],cwd=ROOT,capture_output=True,text=True);out={'name':row['name'],'fingerprint':row['fingerprint'],'command':command,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr};print(json.dumps(out),flush=True);assert p.returncode==0 and p.stdout.strip()==row['fingerprint'];return out
@functools.lru_cache(maxsize=1)
def anchor_configs():
 refs=json.loads((R/'anchors.json').read_text());docs={};out={}
 for name,ref in refs.items():
  assert sha(ROOT/ref['report'])==ref['report_sha256']
  if ref['report'] not in docs:docs[ref['report']]=json.loads((ROOT/ref['report']).read_text())
  c=copy.deepcopy(docs[ref['report']]['configs'][name]);assert c['fingerprint']==ref['fingerprint'] and c['status']==ref['original_status'];c.update(read_only_anchor=True,scope='parent',asset='COMBO',capital_usdt=20000)
  c.setdefault('BTC_return_hurdle',.04);c.setdefault('BTC_fixed_entry_notional_usdt',2000);c.setdefault('ETH_fixed_entry_notional_usdt',2000)
  for z in c['scenes'].values():
   if 'recent40' not in z:z['recent40']=copy.deepcopy(z['extension40'])
  c.setdefault('recent40_positive_5d_folds_1x',sum(f['net_return_pct']>0 for f in c['scenes']['1']['recent40']['folds']));out[name]=c
 assert len(out)==54;return out
def grid_configs(configs):return {**anchor_configs(),**{n:c for n,c in configs.items() if c['role']=='candidate'}}
def axes(c):return {'BTC_fixed_entry_notional_usdt':NOTIONALS,'ETH_fixed_entry_notional_usdt':NOTIONALS,'trend_filter_lookback_days':SLOWS,'reversal_lookback_days':LOOKS,'reversal_return_hurdle':HURDLES}
def neighbors(c,configs):return [x for x in configs.values() if x['role']=='candidate' and all(abs(v.index(x[p])-v.index(c[p]))<=1 for p,v in axes(c).items())]
def criteria(c,frac):
 s=c['scenes'];ratio=s['1']['gross_reference_PnL_to_execution_cost'];return {'positive_all_costs':all(z['net_return_pct']>0 for z in s.values()),'nine_of_twelve_positive_complete30d_1x_folds':c['positive_complete_30d_folds_1x']>=9,'recent40_positive_all_costs':all(z['recent40']['net_return_pct']>0 for z in s.values()),'recent40_six_of_eight_positive5d_1x_folds':c['recent40_positive_5d_folds_1x']>=6,'composite_DD3_lte25pct':s['3']['max_drawdown_pct']<=25,'local_positive3_gte60pct':frac>=.6,'four_round_trips1':s['1']['round_trips']>=4,'gross_plus_funding_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'no_negative_collateral':all(z['cash_or_units_violations']==0 for z in s.values()),'no_order_rejections':all(z['rejected_orders']==0 for z in s.values()),'no_margin_proxy_violations':all(z['margin']['independent_sleeve_violations']==0 for z in s.values()),'terminal_flat':all(D(z['terminal_units'])==0 for z in s.values()),'minimum180days':engine.DAYS>=180}
def freeze():module(R/'freeze_batch.py','independent_budget_freeze').main()
def evaluate():
 assert not(R/'report.json').exists();plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(batch)==114 and all(records[x['fingerprint']]['status']=='reserved' for x in batch) and sha(R/'engine.py')==plan['source_engine']['sha256'];started=now();_,markets,common,vectors,ss=parent.recover(plan);configs={};(R/'results').mkdir()
 for row in batch:
  spec=json.loads((ROOT/row['spec']).read_text());fps=row['source_fingerprints'];scenes={};arc={'spec':spec,'fingerprint':row['fingerprint'],'source_fingerprints':fps,'scenes':{}}
  for k in ['1','2','3']:
   v=vectors[fps[0],k]+vectors[fps[1],k];z=parent.summarize_parent(v,[ss[fp][k] for fp in fps],common);scenes[k]=z;arc['scenes'][k]={'summary':z,'source_fingerprints':fps,'source_full_NAV_sha256':[ss[fp][k]['NAV_sha256_f64le'] for fp in fps]}
  dest=R/'results'/(row['name']+'.json.gz');gzwrite(dest,arc);configs[row['name']]={**row,'archive':rel(dest),'archive_sha256':sha(dest),'scenes':scenes,'positive_folds_1x':sum(f['net_return_pct']>0 for f in scenes['1']['folds']),'positive_complete_30d_folds_1x':sum(f['net_return_pct']>0 for f in scenes['1']['folds'][:12]),'recent40_positive_5d_folds_1x':sum(f['net_return_pct']>0 for f in scenes['1']['recent40']['folds'])};print(row['name'],scenes['1']['net_return_pct'],scenes['3']['net_return_pct'],scenes['3']['recent40']['net_return_pct'],flush=True)
 grid=grid_configs(configs);assert len(grid)==162
 for c in configs.values():
  if c['role']=='benchmark':c.update(status='rejected',criteria={'reference_only_no_alpha_qualification':False},failed_criteria=['reference_only_no_alpha_qualification'],sensitivity={'reference_only':True});continue
  ns=neighbors(c,grid);frac=sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns);c['sensitivity']={'neighbor_names':[x['name'] for x in ns],'neighbor_count':len(ns),'dimension_count':5,'local_3x_neighbor_positive_fraction':frac};c['criteria']=criteria(c,frac);c['status']='passed' if all(c['criteria'].values()) else 'rejected';c['failed_criteria']=[k for k,v in c['criteria'].items() if not v]
 cs=[c for c in configs.values() if c['role']=='candidate'];report={'round':R.name,'evaluation_started_utc':started,'frozen_plan_sha256':sha(R/'plan.json'),'time_boundaries':plan['time_boundaries'],'input_data':plan['data'],'component_sources':plan['component_sources'],'configs':configs,'summary':{'new_configs':114,'candidate_configs':108,'benchmark_configs':6,'new_native_components':0,'new_passive_parents':114,'cost_scenarios':342,'read_only_native_components':63,'read_only_parent_cells':54,'read_only_matched_hold_parents':3,'full_parent_grid':162,'passed':[c['name'] for c in cs if c['status']=='passed'],'rejected':[c['name'] for c in cs if c['status']=='rejected'],'positive_configs_by_cost':{k:sum(c['scenes'][k]['net_return_pct']>0 for c in cs) for k in ['1','2','3']}},'axis':{a:{'points':len(m['ts']),'axis_sha256':m['axis_sha256'],'axis_prices_sha256_f64le':m['axis_price_sha256_f64le'],'daily_boundary_count':len(m['daily_indices']),'folds':len(m['fold_indices'])-1} for a,m in markets.items()},'parent_axis':{'union_points':len(common['keys']),'union_axis_sha256':common['sha256'],'daily_boundaries':len(common['daily_indices']),'folds':len(common['fold_indices'])-1,'projection_policy':'Last completed actual(ns,eventcode),relative-ns packing,no interpolation,NAV rescaling or normalization.'},'read_only_anchor_references':plan['read_only_anchor_references'],'read_only_hold_references':plan['read_only_hold_references'],'scope':plan['limits']};put(R/'report.json',report);print(json.dumps(report['summary']),flush=True)
def finish():
 report=json.loads((R/'report.json').read_text());done=[]
 for row in json.loads((R/'batch.json').read_text()):done.append(call('finish',row,report['configs'][row['name']]['status'],rel(R/'report.json')));put(R/'finish.json',done)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['freeze','evaluate','finish']);globals()[p.parse_args().command]()
