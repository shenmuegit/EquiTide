"""Pre-register,backtest and finish a fixed two-parameter exit-buffer experiment."""
import argparse,copy,functools,gzip,hashlib,importlib.util,itertools,json,subprocess,sys
from pathlib import Path
from datetime import datetime,timezone
import engine
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
LOOKS,HURDLES,EXITS=[28,31],[.02,.04],[.005,.01,.02]
NOTIONALS=[1000,2000,3000]
LOOKS_BY_ASSET={'BTC':[31],'ETH':[28]}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rel=lambda p:str(p.relative_to(ROOT))
now=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def module(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
def gzwrite(p,x):p.write_bytes(gzip.compress(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode(),mtime=0))
def call(command,row,*args):
 p=subprocess.run([sys.executable,'research/automation/registry.py',command,row['spec'],*args],cwd=ROOT,capture_output=True,text=True);x={'name':row['name'],'fingerprint':row['fingerprint'],'command':command,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr};print(json.dumps(x),flush=True);assert p.returncode==0 and p.stdout.strip()==row['fingerprint'];return x
def validate_lookback(L):assert L in LOOKS and engine.START-1-L>=0

def anchor_configs():return {}

def grid_configs(configs):return {**anchor_configs(),**{n:c for n,c in configs.items() if c['role']=='candidate'}}

def neighbors(c,configs):
 return [x for x in configs.values() if x['asset']==c['asset'] and x['lookback_days']==c['lookback_days'] and abs(NOTIONALS.index(x['fixed_entry_notional_usdt'])-NOTIONALS.index(c['fixed_entry_notional_usdt']))<=1 and abs(EXITS.index(x['exit_buffer_fraction'])-EXITS.index(c['exit_buffer_fraction']))<=1 and abs(HURDLES.index(x['return_hurdle'])-HURDLES.index(c['return_hurdle']))<=1]

def freeze():module(R/'freeze_batch.py','current_buffer_freeze').main()

def evaluate():
 assert not (R/'report.json').exists();plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');assert all(records[x['fingerprint']]['status']=='reserved' for x in batch);started=now();markets={a:engine.load_market(a,x) for a,x in plan['data']['assets'].items()};configs={};(R/'results').mkdir()
 for row in batch:
  assert row['role']=='benchmark' or row['lookback_days'] in LOOKS;spec=json.loads((ROOT/row['spec']).read_text());arc={'spec':spec,'fingerprint':row['fingerprint'],'scenes':{}};scenes={}
  for k in ['1','2','3']:
   m=markets[row['asset']];v,z=engine.simulate(spec,m,int(k));indices=m['daily_indices'][330:];tail=v[indices[0]:];daily=v[indices].tolist();extension=engine.stats(tail,daily,40);extension.update(start_utc='2026-09-14T00:01:00Z',end_exclusive_utc='2026-10-24T00:01:00Z',start_NAV_usdt=float(tail[0]),end_NAV_usdt=float(tail[-1]),NAV_points=len(tail),NAV_sha256_f64le=engine.navhash(tail),daily_equity_usdt=daily,interpretation='Existingcontinuouspath segment,inheritedpreterminalstate;no separate reset or oldterminalfee,no new trades for diagnostic.');extension['folds']=[]
   for j in range(8):
    a,b=indices[j*5],indices[(j+1)*5];extension['folds'].append({'fold':j+1,'duration_days':5,**engine.stats(v[a:b+1],daily[j*5:(j+1)*5+1],5)})
   z['summary']['extension40']=extension;arc['scenes'][k]=z;scenes[k]=z['summary']
  path=R/'results'/(row['name']+'.json.gz');gzwrite(path,arc);configs[row['name']]={**row,'archive':rel(path),'archive_sha256':sha(path),'scenes':scenes,'positive_folds_1x':sum(x['net_return_pct']>0 for x in scenes['1']['folds']),'positive_complete_30d_folds_1x':sum(x['net_return_pct']>0 for x in scenes['1']['folds'][:12])};print(row['name'],scenes['1']['net_return_pct'],scenes['3']['net_return_pct'],flush=True)
 grid=grid_configs(configs)
 for c in configs.values():
  if c['role']=='benchmark':c.update(status='rejected',criteria={'reference_only_no_alpha_qualification':False},failed_criteria=['reference_only_no_alpha_qualification']);continue
  ns=neighbors(c,grid);frac=sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns);c['sensitivity']={'neighbor_names':[x['name'] for x in ns],'neighbor_count':len(ns),'local_3x_neighbor_positive_fraction':frac};s=c['scenes'];ratio=s['1']['gross_reference_PnL_to_execution_cost'];c['criteria']={'positive_all_costs':all(x['net_return_pct']>0 for x in s.values()),'nine_positive_complete30d_folds':c['positive_complete_30d_folds_1x']>=9,'minimum180days_evidence':engine.DAYS>=180,'composite_DD3_lte25pct':s['3']['max_drawdown_pct']<=25,'neighbourhood_positive3_gte60pct':frac>=.6,'four_round_trips1':s['1']['round_trips']>=4,'gross_plus_funding_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'no_negative_collateral':all(x['cash_or_units_violations']==0 for x in s.values()),'no_order_rejections':all(x['rejected_orders']==0 for x in s.values()),'no_margin_proxy_violations':all(x['margin']['violations']==0 for x in s.values()),'terminal_flat':all(float(x['terminal_units'])==0 for x in s.values())};c['status']='passed' if all(c['criteria'].values()) else 'rejected';c['failed_criteria']=[k for k,v in c['criteria'].items() if not v]
 cs=list(configs.values());report={'round':R.name,'evaluation_started_utc':started,'frozen_plan_sha256':sha(R/'plan.json'),'anchor_sources':plan['anchor_sources'],'time_boundaries':plan['time_boundaries'],'input_data':plan['data'],'configs':configs,'summary':{'new_configs':42,'candidate_configs':36,'benchmark_configs':6,'cost_scenarios':126,'read_only_anchor_configs':0,'read_only_anchor_cost_scenes':0,'full_grid_configs':36,'passed':[c['name'] for c in cs if c['status']=='passed'],'rejected':[c['name'] for c in cs if c['status']=='rejected'],'positive_configs_by_cost':{k:sum(c['scenes'][k]['net_return_pct']>0 for c in cs) for k in ['1','2','3']}},'scope':plan['limits'],'axis':{a:{'points':len(m['ts']),'axis_sha256':m['axis_sha256'],'axis_prices_sha256_f64le':m['axis_price_sha256_f64le'],'daily_boundary_count':len(m['daily_indices']),'folds':len(m['fold_indices'])-1} for a,m in markets.items()},'read_only_anchor_references':json.loads((R/'anchors.json').read_text()),'anchor_original_statuses_unchanged':True};put(R/'report.json',report);print(json.dumps(report['summary']),flush=True)
def finish():
 report=json.loads((R/'report.json').read_text());done=[]
 for row in json.loads((R/'batch.json').read_text()):done.append(call('finish',row,report['configs'][row['name']]['status'],rel(R/'report.json')));put(R/'finish.json',done)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['freeze','evaluate','finish']);globals()[p.parse_args().command]()
