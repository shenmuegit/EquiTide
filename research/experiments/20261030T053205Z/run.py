"""Static raw BTC/ETH bank ownership; immutable native ledgers, no new orders."""
import argparse,copy,functools,gzip,hashlib,importlib.util,itertools,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
from decimal import Decimal as D
import numpy as np
import engine
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
LOOKS=[20,25,30];HURDLES=[.02,.04,.06];ALPHAS=[.25,.5,.75]
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
def anchor_configs():return {}

def grid_configs(configs):return {**anchor_configs(),**{n:c for n,c in configs.items() if c['role']=='candidate'}}
def axes(c):return {'fast_ETH_bank_units':ALPHAS,'lookback_days':LOOKS,'return_hurdle':HURDLES}
def neighbors(c,configs):return [x for x in configs.values() if x['scope']==c['scope'] and all(abs(v.index(x[p])-v.index(c[p]))<=1 for p,v in axes(c).items())]
def positive_recent(c,k):return sum(f['net_return_pct']>0 for f in c['scenes'][k]['recent40']['folds'])
def stress_fold_ok(c):return all(positive_recent(c,k)>=6 for k in ['1','2','3'])
def criteria(c,frac,recentfrac):
 s=c['scenes'];ratio=s['1']['gross_reference_PnL_to_execution_cost'];return {'positive_all_costs':all(z['net_return_pct']>0 for z in s.values()),'nine_of_twelve_positive_complete30d_1x_folds':c['positive_complete_30d_folds_1x']>=9,'recent40_positive_all_costs':all(z['recent40']['net_return_pct']>0 for z in s.values()),'recent40_six_of_eight_positive5d_1x_folds':positive_recent(c,'1')>=6,'recent40_six_of_eight_positive5d_all_costs':stress_fold_ok(c),'composite_DD3_lte25pct':s['3']['max_drawdown_pct']<=25,'local_positive3_gte60pct':frac>=.6,'local_recent6of8_allcost_gte60pct':recentfrac>=.6,'four_round_trips1':s['1']['round_trips']>=4,'gross_plus_funding_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'no_negative_collateral':all(z['cash_or_units_violations']==0 for z in s.values()),'no_order_rejections':all(z['rejected_orders']==0 for z in s.values()),'no_margin_proxy_violations':all(z['margin'].get('independent_sleeve_violations',z['margin'].get('violations'))==0 for z in s.values()),'terminal_flat':all(D(z['terminal_units'])==0 for z in s.values()),'minimum180days':engine.DAYS>=180}

def recent(v,m):
 ix=m['daily_indices'];daily=v[ix].tolist();tail=v[ix[330]:];s=engine.stats(tail,daily[330:],40);s.update(start_utc='2026-09-14T00:01:00Z',end_exclusive_utc='2026-10-24T00:01:00Z',initial_NAV_usdt=float(tail[0]),final_NAV_usdt=float(tail[-1]),NAV_points=len(tail),NAV_sha256_f64le=engine.navhash(tail),daily_equity_usdt=daily[330:],state_policy='Inherited day330predecisionstate/cash,no resetor diagnosticorders.',folds=[])
 for j in range(8):
  l,h=330+5*j,335+5*j;a,b=ix[[l,h]];s['folds'].append({'fold':j+1,'start_utc':engine.stamp(int(m['ts'][a])),'end_exclusive_utc':engine.stamp(int(m['ts'][b])),'duration_days':5,**engine.stats(v[a:b+1],daily[l:h+1],5)})
 return s

def freeze():module(R/'freeze_batch.py','ownership_freeze').main()
def attach_feature_history(m,files):
 info=next(x for x in files if x['path'].endswith('/funding_settlement.parquet'));assert sha(ROOT/info['path'])==info['sha256'];history=[{**x,'source_index':j} for j,x in enumerate(engine.pl.read_parquet(ROOT/info['path']).to_dicts())];assert len(history)==1212
 assert [x for x in history if m['start_ns']<x['settlement_ts']<=m['end_ns']]==m['funds'];m['funding_feature_history']=history

def evaluate():
 assert not(R/'report.json').exists();plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(batch)==30 and all(records[x['fingerprint']]['status']=='reserved' for x in batch);started=now();_,markets,common,vectors,ss=parent.parent.recover(plan);configs={};(R/'results').mkdir()
 for row in batch:
  sp=json.loads((ROOT/row['spec']).read_text());fps=row['source_fingerprints'];weights=row['raw_component_multipliers'];scenes={};arc={'spec':sp,'fingerprint':row['fingerprint'],'scenes':{}}
  for k in ['1','2','3']:
   v=np.zeros(len(common['keys']))
   for fp,w in zip(fps,weights):v+=w*vectors[fp,k]
   s=summarize_parent(v,owned_parts([ss[fp][k] for fp in fps],weights),common,20000);arc['scenes'][k]={'summary':s,'source_fingerprints':fps,'raw_component_multipliers':weights,'source_full_NAV_sha256':[ss[fp][k]['NAV_sha256_f64le'] for fp in fps]};scenes[k]=s
  path=R/'results'/(row['name']+'.json.gz');gzwrite(path,arc);configs[row['name']]={**row,'archive':rel(path),'archive_sha256':sha(path),'scenes':scenes,'positive_folds_1x':sum(f['net_return_pct']>0 for f in scenes['1']['folds']),'positive_complete_30d_folds_1x':sum(f['net_return_pct']>0 for f in scenes['1']['folds'][:12]),'recent40_positive_5d_folds_1x':positive_recent({'scenes':scenes},'1')};print(row['name'],scenes['3']['net_return_pct'],scenes['3']['recent40']['net_return_pct'],flush=True)
 grid=grid_configs(configs)
 for c in configs.values():
  if c['role']!='candidate':c.update(status='rejected',criteria={'reference_or_fixed_BTC_execution_component_only':False},failed_criteria=['reference_or_fixed_BTC_execution_component_only'],sensitivity={'reference_only':True});continue
  ns=neighbors(c,grid);frac=sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns);rf=sum(stress_fold_ok(x) for x in ns)/len(ns);c['sensitivity']={'neighbor_names':[x['name'] for x in ns],'neighbor_count':len(ns),'dimension_count':3,'local_3x_neighbor_positive_fraction':frac,'local_recent6of8_allcost_fraction':rf};c['criteria']=criteria(c,frac,rf);c['status']='passed' if all(c['criteria'].values()) else 'rejected';c['failed_criteria']=[x for x,y in c['criteria'].items() if not y]
 out={'round':R.name,'evaluation_started_utc':started,'frozen_plan_sha256':sha(R/'plan.json'),'time_boundaries':plan['time_boundaries'],'input_data':plan['data'],'component_sources':plan['component_sources'],'configs':configs,'summary':{'new_configs':30,'candidate_configs':27,'benchmark_configs':3,'new_native_components':0,'new_component_backtests':0,'new_passive_parents':30,'cost_scenarios':90,'read_only_native_components':14,'source_cost_curves':42,'passed':[c['name'] for c in grid.values() if c['status']=='passed'],'rejected':[c['name'] for c in grid.values() if c['status']=='rejected'],'positive_configs_by_cost':{k:sum(c['scenes'][k]['net_return_pct']>0 for c in grid.values()) for k in ['1','2','3']}},'parent_axis':{'union_points':len(common['keys']),'union_axis_sha256':common['sha256'],'daily_boundaries':371,'folds':13,'projection_policy':'last completed(ns,eventcode),no future interpolation orweightnormalization'},'read_only_anchor_references':plan['read_only_anchor_references'],'read_only_hold_references':plan['read_only_hold_references'],'scope':plan['limits']};put(R/'report.json',out);print(json.dumps(out['summary']),flush=True)
def finish():
 report=json.loads((R/'report.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(report['configs'])==30 and all(records[c['fingerprint']]['status']==c['status'] and records[c['fingerprint']]['result_available'] is True and records[c['fingerprint']]['report_sha256']==sha(R/'report.json') for c in report['configs'].values());put(R/'finish_verification.json',{'passed':True,'actual_finished_financial_IDs':30,'report_sha256':sha(R/'report.json')});print('PASS30 actual finished definitions')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['freeze','evaluate','finish']);globals()[p.parse_args().command]()
