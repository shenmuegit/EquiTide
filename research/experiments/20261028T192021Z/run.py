"""Coupled BTC/ETH entry-threshold portfolios from immutable quantity-specific native ledgers."""
import argparse,copy,functools,gzip,hashlib,importlib.util,itertools,json,subprocess,sys,math
from datetime import datetime,timezone,timedelta
from pathlib import Path
from decimal import Decimal as D
import numpy as np
import engine
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
EXITS=[.01];WEIGHTS=[.25,.5,.75];HURDLES=[.02,.025,.03];SLOWS=[27,28,29];LOOKS=[3,4]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rel=lambda p:str(p.relative_to(ROOT))
now=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def module(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
parent=module(ROOT/'research/experiments/20261025T145537Z/run.py','native370_parent_helpers')
keys,align,metric=parent.keys,parent.align,parent.metric
def gzwrite(p,x):p.write_bytes(gzip.compress(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode(),mtime=0))
def call(command,row,*args):
 p=subprocess.run([sys.executable,'research/automation/registry.py',command,row['spec'],*args],cwd=ROOT,capture_output=True,text=True);out={'name':row['name'],'fingerprint':row['fingerprint'],'command':command,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr};print(json.dumps(out),flush=True);assert p.returncode==0 and p.stdout.strip()==row['fingerprint'];return out

def summarize_parent(v,parts,common,capital):
 daily=v[common['daily_indices']].tolist();s=metric(v,daily,370);s['folds']=[];start=datetime.fromisoformat('2025-10-19T00:01:00+00:00');bounds=[*range(0,370,30),370]
 assert len(daily)==371 and len(common['fold_indices'])==14
 for j,(a,b) in enumerate(zip(common['fold_indices'],common['fold_indices'][1:])):
  lo,hi=bounds[j:j+2];s['folds'].append({'fold':j+1,'start_utc':(start+timedelta(days=lo)).isoformat().replace('+00:00','Z'),'end_exclusive_utc':(start+timedelta(days=hi)).isoformat().replace('+00:00','Z'),'duration_days':hi-lo,**metric(v[a:b+1],daily[lo:hi+1],hi-lo)})
 assert abs(math.prod(1+f['net_return_pct']/100 for f in s['folds'])-v[-1]/v[0])<1e-12
 fields=['cost_usdt','funding_usdt','base_funding_same_exposure_usdt','funding_stress_increment_usdt','funding_income_usdt','funding_outflow_usdt','gross_reference_price_PnL_usdt','executions','round_trips','rejected_orders','cash_or_units_violations','funding_settlements','nonzero_funding_settlements'];s.update({f:sum(x[f] for x in parts) for f in fields});cost=s['cost_usdt'];gross=s['gross_reference_price_PnL_usdt'];fund=s['funding_usdt'];assert abs(gross+fund-cost-(v[-1]-capital))<1e-8
 assert all(D(x['terminal_units'])==0 for x in parts)
 s.update(initial_capital_usdt=capital,final_NAV_usdt=float(v[-1]),cost_pct_initial=cost/capital*100,cost_parts_usdt={p:sum(x['cost_parts_usdt'][p] for x in parts) for p in ['fee','half_spread','slippage','impact','tick_rounding']},gross_reference_PnL_to_execution_cost=(gross+fund)/cost if cost else None,terminal_units='0',daily_equity_usdt=daily,NAV_points=len(v),NAV_sha256_f64le=hashlib.sha256(v.astype('<f8',copy=False).tobytes()).hexdigest(),axis_sha256=common['sha256'],margin={'independent_sleeve_violations':sum(x['margin']['violations'] for x in parts),'minimum_individual_sleeve_cushion_usdt':min((x['margin']['minimum_equity_minus_maintenance_usdt'] for x in parts if x['margin']['minimum_equity_minus_maintenance_usdt'] is not None),default=None),'no_cross_margin_netting':True})
 lo=330;a=int(common['daily_indices'][lo]);tail=v[a:];t={**metric(tail,daily[lo:],40),'start_utc':'2026-09-14T00:01:00Z','end_exclusive_utc':'2026-10-24T00:01:00Z','initial_NAV_usdt':float(tail[0]),'final_NAV_usdt':float(tail[-1]),'NAV_points':len(tail),'NAV_sha256_f64le':hashlib.sha256(tail.astype('<f8').tobytes()).hexdigest(),'daily_equity_usdt':daily[lo:],'folds':[],'state_policy':'Inherited predecision state/cash at day330; no cash restart, extra exit or rebalance.'}
 for j in range(8):
  l,h=330+j*5,335+j*5;aa,bb=common['daily_indices'][[l,h]];t['folds'].append({'fold':j+1,'start_utc':(start+timedelta(days=l)).isoformat().replace('+00:00','Z'),'end_exclusive_utc':(start+timedelta(days=h)).isoformat().replace('+00:00','Z'),'duration_days':5,**metric(v[aa:bb+1],daily[l:h+1],5)})
 assert abs(math.prod(1+f['net_return_pct']/100 for f in t['folds'])-tail[-1]/tail[0])<1e-12;s['recent40']=t;return s

def owned_parts(parts,weights):
 money=['cost_usdt','funding_usdt','base_funding_same_exposure_usdt','funding_stress_increment_usdt','funding_income_usdt','funding_outflow_usdt','gross_reference_price_PnL_usdt']
 out=[]
 for original,w in zip(parts,weights):
  x=copy.deepcopy(original)
  for f in money:x[f]*=w
  x['cost_parts_usdt']={k:v*w for k,v in x['cost_parts_usdt'].items()}
  f='minimum_equity_minus_maintenance_usdt'
  if x['margin'][f] is not None:x['margin'][f]*=w
  out.append(x)
 return out

FAST_LOOKS=[3,4]

@functools.lru_cache(maxsize=1)
def anchor_configs():
 out={}
 for name,ref in json.loads((R/'anchors.json').read_text()).items():
  assert sha(ROOT/ref['report'])==ref['report_sha256'];c=copy.deepcopy(json.loads((ROOT/ref['report']).read_text())['configs'][name]);p=json.loads((ROOT/ref['spec']).read_text())['parameters'];c.update(read_only_anchor=True,scope='parent',asset='COMBO',capital_usdt=20000,reversal_return_hurdle=p['ETH_return_hurdle'],trend_filter_lookback_days=p['ETH_trend_lookback_days'],reversal_lookback_days=p['ETH_lookback_days']);out[name]=c
 assert len(out)==18;return out
def grid_configs(configs):return {n:c for n,c in configs.items() if c['role']=='candidate'}
def axes(c):return {'ETH_A_ownership_fraction':WEIGHTS,'ETH_A_return_hurdle':HURDLES,'ETH_B_return_hurdle':HURDLES,'trend_filter_lookback_days':SLOWS}
def neighbors(c,configs):return [x for x in configs.values() if all(abs(v.index(x[p])-v.index(c[p]))<=1 for p,v in axes(c).items())]
def criteria(c,frac):
 s=c['scenes'];ratio=s['1']['gross_reference_PnL_to_execution_cost'];return {'positive_all_costs':all(z['net_return_pct']>0 for z in s.values()),'nine_of_twelve_positive_complete30d_1x_folds':c['positive_complete_30d_folds_1x']>=9,'recent40_positive_all_costs':all(z['recent40']['net_return_pct']>0 for z in s.values()),'recent40_six_of_eight_positive5d_1x_folds':c['recent40_positive_5d_folds_1x']>=6,'composite_DD3_lte25pct':s['3']['max_drawdown_pct']<=25,'local_positive3_gte60pct':frac>=.6,'four_round_trips1':s['1']['round_trips']>=4,'gross_plus_funding_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'no_negative_collateral':all(z['cash_or_units_violations']==0 for z in s.values()),'no_order_rejections':all(z['rejected_orders']==0 for z in s.values()),'no_margin_proxy_violations':all(z['margin']['independent_sleeve_violations']==0 for z in s.values()),'terminal_flat':all(D(z['terminal_units'])==0 for z in s.values()),'minimum180days':engine.DAYS>=180}
def freeze():module(R/'freeze_batch.py','split_eth_freeze').main()
def evaluate():
 assert not(R/'report.json').exists();plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(batch)==81 and all(records[x['fingerprint']]['status']=='reserved' for x in batch);started=now();_,markets,common,vectors,ss=parent.recover(plan);configs={};destdir=R/'results';assert not destdir.exists() or not any(destdir.iterdir());destdir.mkdir(exist_ok=True)
 for row in batch:
  spec=json.loads((ROOT/row['spec']).read_text());fps=row['source_fingerprints'];weights=row['raw_component_multipliers'];arc={'spec':spec,'fingerprint':row['fingerprint'],'source_fingerprints':fps,'raw_component_multipliers':weights,'scenes':{}};scenes={}
  for k in ['1','2','3']:
   v=weights[0]*vectors[fps[0],k]+weights[1]*vectors[fps[1],k]+weights[2]*vectors[fps[2],k];z=summarize_parent(v,owned_parts([ss[fp][k] for fp in fps],weights),common,20000);z['ownership_accounting']='Raw [1,a,1-a] ownership of three existing full banks; money weighted,source action counts unweighted,no order resizing or cross-bank netting; capital20000,entrybudget4000.';scenes[k]=z;arc['scenes'][k]={'summary':z,'source_fingerprints':fps,'source_full_NAV_sha256':[ss[fp][k]['NAV_sha256_f64le'] for fp in fps]}
  dest=R/'results'/(row['name']+'.json.gz');gzwrite(dest,arc);configs[row['name']]={**row,'archive':rel(dest),'archive_sha256':sha(dest),'scenes':scenes,'positive_folds_1x':sum(f['net_return_pct']>0 for f in scenes['1']['folds']),'positive_complete_30d_folds_1x':sum(f['net_return_pct']>0 for f in scenes['1']['folds'][:12]),'recent40_positive_5d_folds_1x':sum(f['net_return_pct']>0 for f in scenes['1']['recent40']['folds'])};print(row['name'],scenes['3']['net_return_pct'],scenes['3']['recent40']['net_return_pct'],flush=True)
 for c in configs.values():
  ns=neighbors(c,configs);frac=sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns);c['sensitivity']={'neighbor_names':[x['name'] for x in ns],'neighbor_count':len(ns),'dimension_count':4,'local_3x_neighbor_positive_fraction':frac};c['criteria']=criteria(c,frac);c['status']='passed' if all(c['criteria'].values()) else 'rejected';c['failed_criteria']=[k for k,v in c['criteria'].items() if not v]
 report={'round':R.name,'evaluation_started_utc':started,'frozen_plan_sha256':sha(R/'plan.json'),'time_boundaries':plan['time_boundaries'],'input_data':plan['data'],'component_sources':plan['component_sources'],'configs':configs,'summary':{'new_configs':81,'candidate_configs':81,'benchmark_configs':0,'new_native_components':0,'new_passive_parents':81,'cost_scenarios':243,'read_only_native_components':21,'read_only_parent_cells':18,'full_parent_grid':81,'passed':[c['name'] for c in configs.values() if c['status']=='passed'],'rejected':[c['name'] for c in configs.values() if c['status']=='rejected'],'positive_configs_by_cost':{k:sum(c['scenes'][k]['net_return_pct']>0 for c in configs.values()) for k in ['1','2','3']}},'parent_axis':{'union_points':len(common['keys']),'union_axis_sha256':common['sha256'],'daily_boundaries':371,'folds':13,'projection_policy':'Lastcompleted(ns,eventcode),relative-ns packing,no interpolation/normalization.'},'read_only_anchor_references':plan['read_only_anchor_references'],'read_only_hold_references':plan['read_only_hold_references'],'scope':plan['limits']};put(R/'report.json',report);print(json.dumps(report['summary']),flush=True)
def finish():
 report=json.loads((R/'report.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');assert all(records[c['fingerprint']]['status']==c['status'] and records[c['fingerprint']]['result_available'] is True and records[c['fingerprint']]['report_sha256']==sha(R/'report.json') for c in report['configs'].values());put(R/'finish_verification.json',{'passed':True,'actual_finished_financial_IDs':81,'report_sha256':sha(R/'report.json'),'policy':'Read-only completion verification after bounded real registry finish batches;no repeated finish or financial evaluation.'});print('PASS:all81 actual configurations finished in bounded batches')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['freeze','evaluate','finish']);globals()[p.parse_args().command]()
