"""ETH entry-threshold and cycle sensitivity with native accounting and a fixed BTC bank."""
import argparse,copy,functools,gzip,hashlib,importlib.util,itertools,json,math,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
from decimal import Decimal as D
import numpy as np
import engine
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
LOOKS=[3,4];HURDLES=[-.015,-.01,-.005,0,.005,.01,.015];BUFFERS=[.005,.01,.015];SLOWS=[27,28,29];NOTIONALS=[3000];EXITS=[0]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rel=lambda p:str(p.relative_to(ROOT))
now=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def module(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
parent=module(ROOT/'research/experiments/20261025T145537Z/run.py','mixed370_passive_helpers')
keys,align=parent.keys,parent.align
def gzwrite(p,x):p.write_bytes(gzip.compress(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode(),mtime=0))
def call(command,row,*args):
 p=subprocess.run([sys.executable,'research/automation/registry.py',command,row['spec'],*args],cwd=ROOT,capture_output=True,text=True);x={'name':row['name'],'fingerprint':row['fingerprint'],'command':command,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr};print(json.dumps(x),flush=True);assert p.returncode==0 and p.stdout.strip()==row['fingerprint'];return x
@functools.lru_cache(maxsize=1)
def anchor_configs():
 refs=json.loads((R/'anchors.json').read_text());out={};docs={}
 for name,ref in refs.items():
  path=ref['report'];assert sha(ROOT/path)==ref['report_sha256']
  if path not in docs:docs[path]=json.loads((ROOT/path).read_text())
  c=copy.deepcopy(docs[path]['configs'][name]);assert c['fingerprint']==ref['fingerprint'] and c['status']==ref['original_status'];c.update(read_only_anchor=True,scope=ref['scope'],asset=ref['asset'],capital_usdt=ref['capital_usdt']);p=json.loads((ROOT/ref['spec']).read_text())['parameters']
  if c['scope']=='parent':c.update(BTC_fixed_entry_notional_usdt=p['BTC_fixed_entry_notional_usdt'],ETH_fixed_entry_notional_usdt=p['ETH_fixed_entry_notional_usdt'],BTC_return_hurdle=p['BTC_return_hurdle'],trend_exit_buffer_fraction=p['BTC_exit_buffer_fraction'],trend_filter_lookback_days=p['ETH_trend_lookback_days'],reversal_lookback_days=p['ETH_lookback_days'],reversal_return_hurdle=p['ETH_return_hurdle'])
  for z in c['scenes'].values():
   if 'recent40' not in z:z['recent40']=copy.deepcopy(z['extension40'])
  c['exit_buffer_fraction' if c['scope']=='native' else 'reversal_exit_buffer_fraction']=p['exit_buffer_fraction' if c['scope']=='native' else 'ETH_exit_buffer_fraction']
  c.setdefault('recent40_positive_5d_folds_1x',sum(x['net_return_pct']>0 for x in c['scenes']['1']['recent40']['folds']));out[name]=c
 assert len(out)==48;return out
def grid_configs(configs):return {**anchor_configs(),**configs}
def axes(c):return {'exit_buffer_fraction':HURDLES,'trend_lookback_days':SLOWS,'lookback_days':LOOKS} if c['scope']=='native' else {'reversal_exit_buffer_fraction':HURDLES,'trend_filter_lookback_days':SLOWS,'reversal_lookback_days':LOOKS}
def neighbors(c,configs):return [x for x in configs.values() if x['scope']==c['scope'] and x['asset']==c['asset'] and all(abs(v.index(x[p])-v.index(c[p]))<=1 for p,v in axes(c).items())]
def recent(v,m):
 ix=m['daily_indices'];daily=v[ix].tolist();tail=v[ix[330]:];s=engine.stats(tail,daily[330:],40);s.update(start_utc='2026-09-14T00:01:00Z',end_exclusive_utc='2026-10-24T00:01:00Z',initial_NAV_usdt=float(tail[0]),final_NAV_usdt=float(tail[-1]),NAV_points=len(tail),NAV_sha256_f64le=engine.navhash(tail),daily_equity_usdt=daily[330:],state_policy='Inherited day330predecisionstate/cash,no resetor diagnosticorders.',folds=[])
 for j in range(8):
  l,h=330+5*j,335+5*j;a,b=ix[[l,h]];s['folds'].append({'fold':j+1,'start_utc':engine.stamp(int(m['ts'][a])),'end_exclusive_utc':engine.stamp(int(m['ts'][b])),'duration_days':5,**engine.stats(v[a:b+1],daily[l:h+1],5)})
 return s
def criteria(c,frac):
 ss=c['scenes'];ratio=ss['1']['gross_reference_PnL_to_execution_cost'];margin=lambda z:z['margin'].get('independent_sleeve_violations',z['margin'].get('violations'));return {'positive_all_costs':all(z['net_return_pct']>0 for z in ss.values()),'nine_of_twelve_positive_complete30d_1x_folds':c['positive_complete_30d_folds_1x']>=9,'recent40_positive_all_costs':all(z['recent40']['net_return_pct']>0 for z in ss.values()),'recent40_six_of_eight_positive5d_1x_folds':c['recent40_positive_5d_folds_1x']>=6,'composite_DD3_lte25pct':ss['3']['max_drawdown_pct']<=25,'local_positive3_gte60pct':frac>=.6,'four_round_trips1':ss['1']['round_trips']>=4,'gross_plus_funding_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'no_negative_collateral':all(z['cash_or_units_violations']==0 for z in ss.values()),'no_order_rejections':all(z['rejected_orders']==0 for z in ss.values()),'no_margin_proxy_violations':all(margin(z)==0 for z in ss.values()),'terminal_flat':all(D(z['terminal_units'])==0 for z in ss.values()),'minimum180days':engine.DAYS>=180}
def freeze():module(R/'freeze_batch.py','new_notional_freeze').main()
def evaluate():
 assert not (R/'report.json').exists();planpath=R/'plan_corrected.json' if (R/'plan_corrected.json').exists() else R/'plan.json';plan=json.loads(planpath.read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(batch)==36 and all(records[x['fingerprint']]['status']=='reserved' for x in batch) and sha(R/'engine.py')==plan['new_engine_sha256'];started=now()
 for row in batch:
  pp=json.loads((ROOT/row['spec']).read_text())['parameters']
  if row['scope']=='native':assert pp['trend_lookback_days']==row['trend_lookback_days'] in [27,28,29] and pp['fixed_entry_notional_usdt']==row['fixed_entry_notional_usdt'] and pp['raw_entry_notional_fraction_of_initial_capital']==pp['fixed_entry_notional_usdt']/10000
  else:assert pp['trend_filter_lookback_days']==pp['ETH_trend_lookback_days']==row['trend_filter_lookback_days'] in [27,28,29]
 _,markets,common,vectors,oldss=parent.recover({**plan,'source_engine':plan['native_engine_base']});source_scenes={(fp,k):s for fp,sc in oldss.items() for k,s in sc.items()};configs={};(R/'results').mkdir()
 for row in batch:
  spec=json.loads((ROOT/row['spec']).read_text());arc={'spec':spec,'fingerprint':row['fingerprint'],'scenes':{}};scenes={}
  for k in ['1','2','3']:
   if row['scope']=='native':
    m=markets['ETH'];v,z=engine.simulate(spec,m,int(k));z['summary']['recent40']=recent(v,m);vectors[row['fingerprint'],k]=v[common['projections']['ETH']];source_scenes[row['fingerprint'],k]=z['summary']
   else:
    fps=row['source_fingerprints'];v=vectors[fps[0],k]+vectors[fps[1],k];summary=parent.summarize_parent(v,[source_scenes[fp,k] for fp in fps],common);z={'summary':summary,'source_fingerprints':fps,'source_full_NAV_sha256':[source_scenes[fp,k]['NAV_sha256_f64le'] for fp in fps]}
   arc['scenes'][k]=z;scenes[k]=z['summary']
  p=R/'results'/(row['name']+'.json.gz');gzwrite(p,arc);configs[row['name']]={**row,'archive':rel(p),'archive_sha256':sha(p),'scenes':scenes,'positive_folds_1x':sum(f['net_return_pct']>0 for f in scenes['1']['folds']),'positive_complete_30d_folds_1x':sum(f['net_return_pct']>0 for f in scenes['1']['folds'][:12]),'recent40_positive_5d_folds_1x':sum(f['net_return_pct']>0 for f in scenes['1']['recent40']['folds'])};print(row['name'],scenes['1']['net_return_pct'],scenes['3']['net_return_pct'],scenes['3']['recent40']['net_return_pct'],flush=True)
 grid=grid_configs(configs)
 for c in configs.values():
  ns=neighbors(c,grid);frac=sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns);c['sensitivity']={'neighbor_names':[x['name'] for x in ns],'neighbor_count':len(ns),'dimension_count':len(axes(c)),'local_3x_neighbor_positive_fraction':frac};c['criteria']=criteria(c,frac);c['status']='passed' if all(c['criteria'].values()) else 'rejected';c['failed_criteria']=[k for k,v in c['criteria'].items() if not v]
 report={'round':R.name,'evaluation_started_utc':started,'frozen_plan_sha256':sha(planpath),'time_boundaries':plan['time_boundaries'],'input_data':plan['data'],'configs':configs,'summary':{'new_configs':36,'candidate_configs':36,'benchmark_configs':0,'new_native_components':18,'new_passive_parents':18,'cost_scenarios':108,'read_only_native_components':9,'read_only_parent_cells':24,'full_parent_grid':42,'full_native_ETH_grid':42,'passed':[c['name'] for c in configs.values() if c['status']=='passed'],'rejected':[c['name'] for c in configs.values() if c['status']=='rejected'],'positive_configs_by_cost':{k:sum(c['scenes'][k]['net_return_pct']>0 for c in configs.values()) for k in ['1','2','3']}},'axis':{a:{'points':len(m['ts']),'axis_sha256':m['axis_sha256'],'axis_prices_sha256_f64le':m['axis_price_sha256_f64le'],'daily_boundary_count':len(m['daily_indices']),'folds':len(m['fold_indices'])-1} for a,m in markets.items()},'parent_axis':{'union_points':len(common['keys']),'union_axis_sha256':common['sha256'],'daily_boundaries':len(common['daily_indices']),'folds':len(common['fold_indices'])-1,'projection_policy':'Lastcompleted(ts,eventcode)sourceNAV,relative-nspacking,nointerpolation/normalization.'},'component_sources':plan['component_sources'],'read_only_anchor_references':json.loads((R/'anchors.json').read_text()),'read_only_hold_references':json.loads((R/'holds.json').read_text()),'scope':plan['limits']};put(R/'report.json',report);print(json.dumps(report['summary']),flush=True)
def finish():
 report=json.loads((R/'report.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(report['configs'])==36 and all(records[c['fingerprint']]['status']==c['status'] and records[c['fingerprint']]['result_available'] is True and records[c['fingerprint']]['report_sha256']==sha(R/'report.json') for c in report['configs'].values());put(R/'finish_verification.json',{'passed':True,'actual_finished_financial_IDs':36,'report_sha256':sha(R/'report.json'),'policy':'Read-only completion after bounded actual finish calls.'});print('PASS:all36 actual configurations finished in bounded batches')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['freeze','evaluate','finish']);globals()[p.parse_args().command]()
