"""Static raw BTC/ETH bank ownership; immutable native ledgers, no new orders."""
import argparse,copy,functools,gzip,hashlib,importlib.util,itertools,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
from decimal import Decimal as D
import numpy as np
import engine
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
WEIGHTS=[.5,.75,1,1.25,1.5];NEW_WEIGHTS=[.5,.75,1.25,1.5];EXITS=[-.015,-.01,-.005];SLOWS=[27,28,29]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rel=lambda p:str(p.relative_to(ROOT))
now=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def module(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
parent=module(ROOT/'research/experiments/20261029T092426Z/run.py','raw_ownership_helpers')
keys,align=parent.keys,parent.align
summarize_parent,owned_parts=parent.summarize_parent,parent.owned_parts

def gzwrite(p,x):p.write_bytes(gzip.compress(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode(),mtime=0))
def call(command,row,*args):
 p=subprocess.run([sys.executable,'research/automation/registry.py',command,row['spec'],*args],cwd=ROOT,capture_output=True,text=True);x={'name':row['name'],'fingerprint':row['fingerprint'],'command':command,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr};print(json.dumps(x),flush=True);assert p.returncode==0 and p.stdout.strip()==row['fingerprint'];return x
@functools.lru_cache(maxsize=1)
def anchor_configs():
 out={};docs={}
 for name,x in json.loads((R/'anchors.json').read_text()).items():
  path=x['report'];assert sha(ROOT/path)==x['report_sha256']
  if path not in docs:docs[path]=json.loads((ROOT/path).read_text())
  c=copy.deepcopy(docs[path]['configs'][name]);p=json.loads((ROOT/x['spec']).read_text())['parameters'];c.update(read_only_anchor=True,BTC_bank_units=1,ETH_exit_buffer_fraction=p['ETH_exit_buffer_fraction'],ETH_trend_lookback_days=p['ETH_trend_lookback_days'],scope='parent',asset='COMBO');out[name]=c
 assert len(out)==9;return out

def grid_configs(configs):return {**anchor_configs(),**{n:c for n,c in configs.items() if c['role']=='candidate'}}
def axes(c):return {'BTC_bank_units':WEIGHTS,'ETH_exit_buffer_fraction':EXITS,'ETH_trend_lookback_days':SLOWS}
def neighbors(c,configs):return [x for x in configs.values() if all(abs(v.index(x[p])-v.index(c[p]))<=1 for p,v in axes(c).items())]
def positive_recent(c,k):return sum(f['net_return_pct']>0 for f in c['scenes'][k]['recent40']['folds'])
def stress_fold_ok(c):return all(positive_recent(c,k)>=6 for k in ['1','2','3'])
def criteria(c,frac,recentfrac):
 s=c['scenes'];ratio=s['1']['gross_reference_PnL_to_execution_cost'];return {'positive_all_costs':all(z['net_return_pct']>0 for z in s.values()),'nine_of_twelve_positive_complete30d_1x_folds':c['positive_complete_30d_folds_1x']>=9,'recent40_positive_all_costs':all(z['recent40']['net_return_pct']>0 for z in s.values()),'recent40_six_of_eight_positive5d_1x_folds':positive_recent(c,'1')>=6,'recent40_six_of_eight_positive5d_all_costs':stress_fold_ok(c),'composite_DD3_lte25pct':s['3']['max_drawdown_pct']<=25,'local_positive3_gte60pct':frac>=.6,'local_recent6of8_allcost_gte60pct':recentfrac>=.6,'four_round_trips1':s['1']['round_trips']>=4,'gross_plus_funding_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'no_negative_collateral':all(z['cash_or_units_violations']==0 for z in s.values()),'no_order_rejections':all(z['rejected_orders']==0 for z in s.values()),'no_margin_proxy_violations':all(z['margin']['independent_sleeve_violations']==0 for z in s.values()),'terminal_flat':all(D(z['terminal_units'])==0 for z in s.values()),'minimum180days':engine.DAYS>=180}

def freeze():module(R/'freeze_batch.py','ownership_freeze').main()
def evaluate():
 assert not(R/'report.json').exists();plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(batch)==40 and all(records[x['fingerprint']]['status']=='reserved' for x in batch);started=now();_,markets,common,vectors,ss=parent.parent.recover(plan);configs={};(R/'results').mkdir()
 for row in batch:
  sp=json.loads((ROOT/row['spec']).read_text());fps=row['source_fingerprints'];weights=row['raw_component_multipliers'];arc={'spec':sp,'fingerprint':row['fingerprint'],'source_fingerprints':fps,'raw_component_multipliers':weights,'scenes':{}};scenes={}
  for k in ['1','2','3']:
   v=weights[0]*vectors[fps[0],k]+weights[1]*vectors[fps[1],k];z=summarize_parent(v,owned_parts([ss[fp][k] for fp in fps],weights),common,20000);z['ownership_accounting']='Raw [w,2-w] static units of two original10000 banks. Money belongs proportionately;source action counts unweighted,not parent fills. No new order,normalization,quantity scaling,netting or rebalance;source nonlinear costs remain at original N1000/N3000 bank order sizes.';scenes[k]=z;arc['scenes'][k]={'summary':z,'source_fingerprints':fps,'source_full_NAV_sha256':[ss[fp][k]['NAV_sha256_f64le'] for fp in fps]}
  path=R/'results'/(row['name']+'.json.gz');gzwrite(path,arc);configs[row['name']]={**row,'archive':rel(path),'archive_sha256':sha(path),'scenes':scenes,'positive_folds_1x':sum(f['net_return_pct']>0 for f in scenes['1']['folds']),'positive_complete_30d_folds_1x':sum(f['net_return_pct']>0 for f in scenes['1']['folds'][:12]),'recent40_positive_5d_folds_1x':positive_recent({'scenes':scenes},'1')};print(row['name'],scenes['3']['net_return_pct'],scenes['3']['recent40']['net_return_pct'],flush=True)
 grid=grid_configs(configs)
 for c in configs.values():
  if c['role']=='benchmark':c.update(status='rejected',criteria={'reference_only_no_alpha_qualification':False},failed_criteria=['reference_only_no_alpha_qualification'],sensitivity={'reference_only':True});continue
  ns=neighbors(c,grid);frac=sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns);rf=sum(stress_fold_ok(x) for x in ns)/len(ns);c['sensitivity']={'neighbor_names':[x['name'] for x in ns],'neighbor_count':len(ns),'dimension_count':3,'local_3x_neighbor_positive_fraction':frac,'local_recent6of8_allcost_fraction':rf};c['criteria']=criteria(c,frac,rf);c['status']='passed' if all(c['criteria'].values()) else 'rejected';c['failed_criteria']=[k for k,v in c['criteria'].items() if not v]
 cs=[c for c in configs.values() if c['role']=='candidate'];out={'round':R.name,'evaluation_started_utc':started,'frozen_plan_sha256':sha(R/'plan.json'),'time_boundaries':plan['time_boundaries'],'input_data':plan['data'],'component_sources':plan['component_sources'],'configs':configs,'summary':{'new_configs':40,'candidate_configs':36,'benchmark_configs':4,'new_native_components':0,'new_component_backtests':0,'new_passive_parents':40,'cost_scenarios':120,'read_only_native_components':12,'read_only_parent_cells':9,'full_parent_grid':45,'passed':[c['name'] for c in cs if c['status']=='passed'],'rejected':[c['name'] for c in cs if c['status']=='rejected'],'positive_configs_by_cost':{k:sum(c['scenes'][k]['net_return_pct']>0 for c in cs) for k in ['1','2','3']}},'parent_axis':{'union_points':len(common['keys']),'union_axis_sha256':common['sha256'],'daily_boundaries':371,'folds':13,'projection_policy':'Last completed structured(ns,eventcode),no interpolation or normalization.'},'read_only_anchor_references':plan['read_only_anchor_references'],'read_only_hold_references':plan['read_only_hold_references'],'scope':plan['limits']};put(R/'report.json',out);print(json.dumps(out['summary']),flush=True)
def finish():
 report=json.loads((R/'report.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(report['configs'])==40 and all(records[c['fingerprint']]['status']==c['status'] and records[c['fingerprint']]['result_available'] is True and records[c['fingerprint']]['report_sha256']==sha(R/'report.json') for c in report['configs'].values());put(R/'finish_verification.json',{'passed':True,'actual_finished_financial_IDs':40,'report_sha256':sha(R/'report.json')});print('PASS40 actual finished definitions')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['freeze','evaluate','finish']);globals()[p.parse_args().command]()
