"""Passive mixed trend/reversal parents from immutable native NAV evidence."""
import argparse,copy,gzip,hashlib,importlib.util,itertools,json,math,subprocess,sys
from datetime import datetime,timezone,timedelta
from pathlib import Path
from decimal import Decimal as D
import numpy as np
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
BUFFERS=[.005,.01,.02];LOOKS=[1,2,3];HURDLES=[.02,.04,.06]
STYLES=['btc_trend_eth_reversal','btc_reversal_eth_trend']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rel=lambda p:str(p.relative_to(ROOT))
now=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def module(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
base=module(ROOT/'research/experiments/20261025T085436Z/run.py','passive370_helpers')
keys,align,metric,recover=base.keys,base.align,base.metric,base.recover
def gzwrite(p,x):p.write_bytes(gzip.compress(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode(),mtime=0))
def call(command,row,*args):
 p=subprocess.run([sys.executable,'research/automation/registry.py',command,row['spec'],*args],cwd=ROOT,capture_output=True,text=True);x={'name':row['name'],'fingerprint':row['fingerprint'],'command':command,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr};print(json.dumps(x),flush=True);assert p.returncode==0 and p.stdout.strip()==row['fingerprint'];return x
def neighbors(c,configs):
 axes={'trend_exit_buffer_fraction':BUFFERS,'reversal_lookback_days':LOOKS,'reversal_return_hurdle':HURDLES};return [x for x in configs.values() if x['style']==c['style'] and all(abs(vals.index(x[p])-vals.index(c[p]))<=1 for p,vals in axes.items())]
def summarize_parent(v,parts,common):
 daily=v[common['daily_indices']].tolist();s=metric(v,daily,370);s['folds']=[];start=datetime.fromisoformat('2025-10-19T00:01:00+00:00');bounds=[*range(0,370,30),370]
 assert len(daily)==371 and len(common['fold_indices'])==14
 for j,(a,b) in enumerate(zip(common['fold_indices'],common['fold_indices'][1:])):
  lo,hi=bounds[j:j+2];s['folds'].append({'fold':j+1,'start_utc':(start+timedelta(days=lo)).isoformat().replace('+00:00','Z'),'end_exclusive_utc':(start+timedelta(days=hi)).isoformat().replace('+00:00','Z'),'duration_days':hi-lo,**metric(v[a:b+1],daily[lo:hi+1],hi-lo)})
 assert abs(math.prod(1+f['net_return_pct']/100 for f in s['folds'])-v[-1]/v[0])<1e-12
 fields=['cost_usdt','funding_usdt','base_funding_same_exposure_usdt','funding_stress_increment_usdt','funding_income_usdt','funding_outflow_usdt','gross_reference_price_PnL_usdt','executions','round_trips','rejected_orders','cash_or_units_violations','funding_settlements','nonzero_funding_settlements'];s.update({f:sum(x[f] for x in parts) for f in fields});cost=s['cost_usdt'];gross=s['gross_reference_price_PnL_usdt'];fund=s['funding_usdt'];assert abs(gross+fund-cost-(v[-1]-20000))<1e-8
 assert all(D(x['terminal_units'])==0 for x in parts)
 s.update(initial_capital_usdt=20000,final_NAV_usdt=float(v[-1]),cost_pct_initial=cost/20000*100,cost_parts_usdt={p:sum(x['cost_parts_usdt'][p] for x in parts) for p in ['fee','half_spread','slippage','impact','tick_rounding']},gross_reference_PnL_to_execution_cost=(gross+fund)/cost if cost else None,terminal_units='0',daily_equity_usdt=daily,NAV_points=len(v),NAV_sha256_f64le=hashlib.sha256(v.astype('<f8',copy=False).tobytes()).hexdigest(),axis_sha256=common['sha256'],margin={'independent_sleeve_violations':sum(x['margin']['violations'] for x in parts),'minimum_individual_sleeve_cushion_usdt':min((x['margin']['minimum_equity_minus_maintenance_usdt'] for x in parts if x['margin']['minimum_equity_minus_maintenance_usdt'] is not None),default=None),'no_cross_margin_netting':True})
 lo=330;a=int(common['daily_indices'][lo]);tail=v[a:];t={**metric(tail,daily[lo:],40),'start_utc':'2026-09-14T00:01:00Z','end_exclusive_utc':'2026-10-24T00:01:00Z','initial_NAV_usdt':float(tail[0]),'final_NAV_usdt':float(tail[-1]),'NAV_points':len(tail),'NAV_sha256_f64le':hashlib.sha256(tail.astype('<f8').tobytes()).hexdigest(),'daily_equity_usdt':daily[lo:],'folds':[],'state_policy':'Inherited predecision state/cash at day330; no cash restart, extra exit or rebalance.'}
 for j in range(8):
  l,h=330+j*5,335+j*5;aa,bb=common['daily_indices'][[l,h]];t['folds'].append({'fold':j+1,'start_utc':(start+timedelta(days=l)).isoformat().replace('+00:00','Z'),'end_exclusive_utc':(start+timedelta(days=h)).isoformat().replace('+00:00','Z'),'duration_days':5,**metric(v[aa:bb+1],daily[l:h+1],5)})
 assert abs(math.prod(1+f['net_return_pct']/100 for f in t['folds'])-tail[-1]/tail[0])<1e-12;s['recent40']=t;return s

def criteria(c,frac):
 ss=c['scenes'];ratio=ss['1']['gross_reference_PnL_to_execution_cost'];return {'positive_all_costs':all(z['net_return_pct']>0 for z in ss.values()),'nine_of_twelve_positive_complete30d_1x_folds':c['positive_complete_30d_folds_1x']>=9,'recent40_positive_all_costs':all(z['recent40']['net_return_pct']>0 for z in ss.values()),'recent40_six_of_eight_positive5d_1x_folds':c['recent40_positive_5d_folds_1x']>=6,'composite_DD3_lte25pct':ss['3']['max_drawdown_pct']<=25,'local3D_positive3_gte60pct':frac>=.6,'four_round_trips1':ss['1']['round_trips']>=4,'gross_plus_funding_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'no_negative_sleeve_collateral':all(z['cash_or_units_violations']==0 for z in ss.values()),'no_source_order_rejections':all(z['rejected_orders']==0 for z in ss.values()),'no_individual_sleeve_margin_violations':all(z['margin']['independent_sleeve_violations']==0 for z in ss.values()),'terminal_flat':all(D(z['terminal_units'])==0 for z in ss.values()),'minimum180days':True}
def freeze():module(R/'freeze_batch.py','mixed_style_freeze').main()
def correlation(a,b):
 x=np.diff(a)/np.asarray(a[:-1]);y=np.diff(b)/np.asarray(b[:-1]);return float(np.corrcoef(x,y)[0,1]) if np.std(x)>0 and np.std(y)>0 else None
def evaluate():
 assert not (R/'report.json').exists();plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');assert all(records[x['fingerprint']]['status']=='reserved' for x in batch);started=now();engine,markets,common,vectors,ss=recover(plan);(R/'results').mkdir();configs={}
 for row in batch:
  spec=json.loads((ROOT/row['spec']).read_text());fps=row['source_fingerprints'];arc={'spec':spec,'fingerprint':row['fingerprint'],'source_fingerprints':fps,'scenes':{}};scenes={}
  for k in ['1','2','3']:
   va,vb=[vectors[fp,k] for fp in fps];v=va+vb;s=summarize_parent(v,[ss[fp][k] for fp in fps],common);da,db=va[common['daily_indices']],vb[common['daily_indices']];s['source_daily_return_correlation_full370']=correlation(da,db);s['source_daily_return_correlation_recent40']=correlation(da[330:],db[330:]);scenes[k]=s;arc['scenes'][k]={'summary':s,'source_full_NAV_sha256':[plan['component_sources'][fp]['NAV_sha256_by_cost'][k] for fp in fps]}
  p=R/'results'/(row['name']+'.json.gz');gzwrite(p,arc);configs[row['name']]={**row,'archive':rel(p),'archive_sha256':sha(p),'scenes':scenes,'positive_folds_1x':sum(f['net_return_pct']>0 for f in scenes['1']['folds']),'positive_complete_30d_folds_1x':sum(f['net_return_pct']>0 for f in scenes['1']['folds'][:12]),'recent40_positive_5d_folds_1x':sum(f['net_return_pct']>0 for f in scenes['1']['recent40']['folds'])};print(row['name'],scenes['1']['net_return_pct'],scenes['3']['net_return_pct'],scenes['3']['recent40']['net_return_pct'],flush=True)
 for c in configs.values():
  ns=neighbors(c,configs);frac=sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns);c['sensitivity']={'neighbor_names':[x['name'] for x in ns],'neighbor_count':len(ns),'three_dimensional_local_3x_positive_fraction':frac};c['criteria']=criteria(c,frac);c['status']='passed' if all(c['criteria'].values()) else 'rejected';c['failed_criteria']=[k for k,v in c['criteria'].items() if not v]
 report={'round':R.name,'evaluation_started_utc':started,'frozen_plan_sha256':sha(R/'plan.json'),'time_boundaries':plan['time_boundaries'],'input_data':plan['data'],'component_sources':plan['component_sources'],'configs':configs,'summary':{'new_configs':54,'candidate_configs':54,'benchmark_configs':0,'new_component_backtests':0,'source_configs_reused_read_only':24,'source_cost_scenes_hash_verified':72,'cost_scenarios':162,'passed':[c['name'] for c in configs.values() if c['status']=='passed'],'rejected':[c['name'] for c in configs.values() if c['status']=='rejected'],'positive_configs_by_cost':{k:sum(c['scenes'][k]['net_return_pct']>0 for c in configs.values()) for k in ['1','2','3']}},'axis':{'source_points':{a:len(m['ts']) for a,m in markets.items()},'union_points':len(common['keys']),'union_axis_sha256':common['sha256'],'daily_boundaries':len(common['daily_indices']),'folds':len(common['fold_indices'])-1,'projection_policy':'Lastcompleted(ts,eventcode)sourceNAV;relative-nspacking,nofutureinterpolation,nocapitalnormalization.'},'read_only_reference_definitions':plan['read_only_references'],'scope':plan['limits']};put(R/'report.json',report);print(json.dumps(report['summary']),flush=True)
def finish():
 report=json.loads((R/'report.json').read_text());done=[]
 for row in json.loads((R/'batch.json').read_text()):done.append(call('finish',row,report['configs'][row['name']]['status'],rel(R/'report.json')));put(R/'finish.json',done)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['freeze','evaluate','finish']);globals()[p.parse_args().command]()
