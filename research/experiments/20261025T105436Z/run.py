"""Native lagged-volatility gates followed by passive exact-NAV paired portfolios."""
import argparse,copy,gzip,hashlib,importlib.util,itertools,json,subprocess,sys
from datetime import datetime,timezone,timedelta
from pathlib import Path
from decimal import Decimal as D
import numpy as np
import engine
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
WINDOWS=[10,20,30];CAPS=[.4,.6,.8];LOOKS=[28,31];HURDLES=[.02,.04];EXITS=[.01]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rel=lambda p:str(p.relative_to(ROOT))
now=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def module(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
parent=module(ROOT/'research/experiments/20261025T085436Z/run.py','parent370_helpers')
keys,align=parent.keys,parent.align
def gzwrite(p,x):p.write_bytes(gzip.compress(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode(),mtime=0))
def call(command,row,*args):
 p=subprocess.run([sys.executable,'research/automation/registry.py',command,row['spec'],*args],cwd=ROOT,capture_output=True,text=True);x={'name':row['name'],'fingerprint':row['fingerprint'],'command':command,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr};print(json.dumps(x),flush=True);assert p.returncode==0 and p.stdout.strip()==row['fingerprint'];return x
def grid_configs(configs):return configs
def neighbors(c,configs):return [x for x in configs.values() if x['asset']==c['asset'] and x['scope']==c['scope'] and abs(WINDOWS.index(x['volatility_lookback_days'])-WINDOWS.index(c['volatility_lookback_days']))<=1 and abs(CAPS.index(x['annualized_volatility_cap'])-CAPS.index(c['annualized_volatility_cap']))<=1]
def recent(v,m):
 ix=m['daily_indices'];daily=v[ix].tolist();tail=v[ix[330]:];s=engine.stats(tail,daily[330:],40);s.update(start_utc='2026-09-14T00:01:00Z',end_exclusive_utc='2026-10-24T00:01:00Z',initial_NAV_usdt=float(tail[0]),final_NAV_usdt=float(tail[-1]),NAV_points=len(tail),NAV_sha256_f64le=engine.navhash(tail),daily_equity_usdt=daily[330:],state_policy='Inherited original day330 predecision state/cash;no reset, extra trade or rebalance.',folds=[])
 for j in range(8):
  l,h=330+5*j,335+5*j;a,b=ix[[l,h]];s['folds'].append({'fold':j+1,'start_utc':engine.stamp(int(m['ts'][a])),'end_exclusive_utc':engine.stamp(int(m['ts'][b])),'duration_days':5,**engine.stats(v[a:b+1],daily[l:h+1],5)})
 return s
def criteria(c,frac):
 ss=c['scenes'];ratio=ss['1']['gross_reference_PnL_to_execution_cost'];margin=lambda z:z['margin'].get('independent_sleeve_violations',z['margin'].get('violations'));return {'positive_all_costs':all(z['net_return_pct']>0 for z in ss.values()),'nine_of_twelve_positive_complete30d_1x_folds':c['positive_complete_30d_folds_1x']>=9,'recent40_positive_all_costs':all(z['recent40']['net_return_pct']>0 for z in ss.values()),'recent40_six_of_eight_positive5d_1x_folds':c['recent40_positive_5d_folds_1x']>=6,'composite_DD3_lte25pct':ss['3']['max_drawdown_pct']<=25,'local2D_positive3_gte60pct':frac>=.6,'four_round_trips1':ss['1']['round_trips']>=4,'gross_plus_funding_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'no_negative_collateral':all(z['cash_or_units_violations']==0 for z in ss.values()),'no_order_rejections':all(z['rejected_orders']==0 for z in ss.values()),'no_margin_proxy_violations':all(margin(z)==0 for z in ss.values()),'terminal_flat':all(D(z['terminal_units'])==0 for z in ss.values()),'minimum180days':engine.DAYS>=180}
def freeze():module(R/'freeze_batch.py','current_freeze').main()
def evaluate():
 assert not (R/'report.json').exists();plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');assert all(records[x['fingerprint']]['status']=='reserved' for x in batch);started=now();markets={a:engine.load_market(a,x) for a,x in plan['data']['assets'].items()};common=parent.align(markets);vectors={};source_scenes={};configs={};(R/'results').mkdir()
 for row in batch:
  spec=json.loads((ROOT/row['spec']).read_text());arc={'spec':spec,'fingerprint':row['fingerprint'],'scenes':{}};scenes={}
  for k in ['1','2','3']:
   if row['scope']=='native':
    m=markets[row['asset']];v,z=engine.simulate(spec,m,int(k));z['summary']['recent40']=recent(v,m);z['summary']['volatility_blocked_decisions']=sum(not d['volatility_gate_passed'] for d in z['decisions']);z['summary']['raw_directional_decisions']=sum(d['raw_desired_direction']!=0 for d in z['decisions']);vectors[row['fingerprint'],k]=v[common['projections'][row['asset']]];source_scenes[row['fingerprint'],k]=z['summary']
   else:
    fps=row['source_fingerprints'];v=vectors[fps[0],k]+vectors[fps[1],k];s=parent.summarize(v,[source_scenes[fp,k] for fp in fps],common);z={'summary':s,'source_fingerprints':fps,'source_full_NAV_sha256':[source_scenes[fp,k]['NAV_sha256_f64le'] for fp in fps]}
   arc['scenes'][k]=z;scenes[k]=z['summary']
  path=R/'results'/(row['name']+'.json.gz');gzwrite(path,arc);configs[row['name']]={**row,'archive':rel(path),'archive_sha256':sha(path),'scenes':scenes,'positive_folds_1x':sum(f['net_return_pct']>0 for f in scenes['1']['folds']),'positive_complete_30d_folds_1x':sum(f['net_return_pct']>0 for f in scenes['1']['folds'][:12]),'recent40_positive_5d_folds_1x':sum(f['net_return_pct']>0 for f in scenes['1']['recent40']['folds'])};print(row['name'],scenes['1']['net_return_pct'],scenes['3']['net_return_pct'],scenes['3']['recent40']['net_return_pct'],flush=True)
 for c in configs.values():
  ns=neighbors(c,configs);frac=sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns);c['sensitivity']={'neighbor_names':[x['name'] for x in ns],'neighbor_count':len(ns),'local_3x_neighbor_positive_fraction':frac};c['criteria']=criteria(c,frac);c['status']='passed' if all(c['criteria'].values()) else 'rejected';c['failed_criteria']=[k for k,v in c['criteria'].items() if not v]
 report={'round':R.name,'evaluation_started_utc':started,'frozen_plan_sha256':sha(R/'plan.json'),'time_boundaries':plan['time_boundaries'],'input_data':plan['data'],'configs':configs,'summary':{'new_configs':27,'new_native_components':18,'new_passive_parents':9,'candidate_configs':27,'benchmark_configs':0,'cost_scenarios':81,'passed':[c['name'] for c in configs.values() if c['status']=='passed'],'rejected':[c['name'] for c in configs.values() if c['status']=='rejected'],'positive_configs_by_cost':{k:sum(c['scenes'][k]['net_return_pct']>0 for c in configs.values()) for k in ['1','2','3']}},'axis':{a:{'points':len(m['ts']),'axis_sha256':m['axis_sha256'],'axis_prices_sha256_f64le':m['axis_price_sha256_f64le'],'daily_boundary_count':len(m['daily_indices']),'folds':len(m['fold_indices'])-1} for a,m in markets.items()},'parent_axis':{'union_points':len(common['keys']),'union_axis_sha256':common['sha256'],'daily_boundaries':len(common['daily_indices']),'folds':len(common['fold_indices'])-1,'projection_policy':'Last completed(ts,eventcode)source NAV only;relative ns packed keys prevent overflow;no interpolation or normalizedweights.'},'read_only_reference_definitions':plan['read_only_references'],'scope':plan['limits']};put(R/'report.json',report);print(json.dumps(report['summary']),flush=True)
def finish():
 report=json.loads((R/'report.json').read_text());done=[]
 for row in json.loads((R/'batch.json').read_text()):done.append(call('finish',row,report['configs'][row['name']]['status'],rel(R/'report.json')));put(R/'finish.json',done)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['freeze','evaluate','finish']);globals()[p.parse_args().command]()
