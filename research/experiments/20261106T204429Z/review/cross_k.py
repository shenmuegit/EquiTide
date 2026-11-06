"""Compare already registered D/K/VC report metrics; no valuation or regrading."""
import csv,hashlib,itertools,json,statistics,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));from common import reg,sha,put,rel
rd=lambda p:json.loads(p.read_text());p=rd(R/'plan.json');decl=p['predeclared_cross_K_readonly_diagnostic'];assert decl['D']==[6,7,8] and decl['K']==[.01,.02,.03] and decl['VC']==[.04,.045,.05] and decl['new_strategy_evaluations']==0
rs=reg.read_records(ROOT/'research/automation/registry.jsonl');before={};cells={};rows=[];sources=[];cache={}
for path,k in zip(decl['source_reports'],decl['K']):
 f=ROOT/path;doc=rd(f);sources.append({'path':path,'sha256':sha(f),'fixed_K':k})
 for scope,key in [('parent','all_current_grid'),('native','all_current_native_grid')]:
  assert len(doc[key])==9
  for c in doc[key].values():
   assert c['K']==k and c['D'] in decl['D'] and c['VC'] in decl['VC'];fp=c['fingerprint'];z=rs[fp];assert z['result_available'] is True and z['status']==c['status'] and sha(ROOT/z['report'])==z['report_sha256'];before[fp]=(z['status'],z['report_sha256'])
   if z['report'] not in cache:cache[z['report']]=rd(ROOT/z['report'])
   canonical=next(a for a in cache[z['report']]['configs'].values() if a['fingerprint']==fp);assert c['scenes']==canonical['scenes'] and c['criteria']==canonical['criteria'] and c['sensitivity']==canonical['sensitivity'];assert sha(ROOT/c['archive'])==c['archive_sha256'];spec=rd(ROOT/c['spec']);q=spec['parameters'];assert q['initial_capital_usdt']==(18750 if scope=='parent' else 15000)
   if scope=='parent':assert [x['weight'] for x in spec['components']]==[1,1] and q['component_capitals_usdt']==[3750,15000] and q['component_initial_entry_notionals_usdt']==[1000,4500]
   cells[scope,c['D'],k,c['VC']]=c
   for cost,s in c['scenes'].items():rows.append({'scope':scope,'D':c['D'],'K':k,'VC':c['VC'],'cost_multiplier':int(cost),'fingerprint':fp,'canonical_status':z['status'],'canonical_report':z['report'],'canonical_report_sha256':z['report_sha256'],'container_report':path,'new_current_round':not c['readonly'] and k==.03,'net_return_pct':s['net_return_pct'],'whole_DD_pct':s['max_drawdown_pct'],'Sharpe365':s['sharpe_365'],'Calmar':s['calmar'],'recent40_net_return_pct':s['recent40']['net_return_pct'],'positive5d_folds':sum(a['net_return_pct']>0 for a in s['recent40']['folds']),'NAV_sha256_f64le':s['NAV_sha256_f64le']})
assert len(cells)==54 and len(rows)==162 and len(before)==54
edges=[];flags=[]
for scope,cost,axis in itertools.product(['parent','native'],[1,2,3],['D','K','VC']):
 vals=decl[axis];xs=[]
 for d,k,v in itertools.product(decl['D'],decl['K'],decl['VC']):
  point={'D':d,'K':k,'VC':v};i=vals.index(point[axis])
  if i==2:continue
  after={**point,axis:vals[i+1]};a,b=cells[scope,d,k,v],cells[scope,after['D'],after['K'],after['VC']];aa,bb=a['scenes'][str(cost)],b['scenes'][str(cost)];delta=abs(aa['sharpe_365']-bb['sharpe_365']);xs.append(delta);edges.append({'scope':scope,'cost_multiplier':cost,'axis':axis,'from_D':d,'from_K':k,'from_VC':v,'to_D':after['D'],'to_K':after['K'],'to_VC':after['VC'],'from_fingerprint':a['fingerprint'],'to_fingerprint':b['fingerprint'],'absolute_Sharpe_change':delta,'absolute_return_change_pp':abs(aa['net_return_pct']-bb['net_return_pct']),'absolute_DD_change_pp':abs(aa['max_drawdown_pct']-bb['max_drawdown_pct'])})
 assert len(xs)==18;threshold=2*statistics.stdev(xs);flags.append({'scope':scope,'cost_multiplier':cost,'axis':axis,'edges':18,'max_absolute_Sharpe_change':max(xs),'two_std_threshold':threshold,'descriptive_cliff_flag':max(xs)>threshold})
assert len(edges)==324
by_k=[]
for scope,k in itertools.product(['parent','native'],decl['K']):
 cs=[c for (s,d,kk,v),c in cells.items() if s==scope and kk==k];strict=sum(all(c['scenes'][str(cost)]['recent40']['net_return_pct']>0 and sum(a['net_return_pct']>0 for a in c['scenes'][str(cost)]['recent40']['folds'])>=6 for cost in [1,2,3]) for c in cs);ss=[c['scenes']['3'] for c in cs];by_k.append({'scope':scope,'K':k,'cells':9,'strict_recent_allcost_cells':strict,'positive_whole3_cells':sum(s['net_return_pct']>0 for s in ss),'whole3_return_range_pct':[min(s['net_return_pct'] for s in ss),max(s['net_return_pct'] for s in ss)],'whole3_DD_range_pct':[min(s['max_drawdown_pct'] for s in ss),max(s['max_drawdown_pct'] for s in ss)]})
for name,items in [('readonly_cross_K_cells.csv',rows),('readonly_cross_K_edges.csv',edges)]:
 with (R/name).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(items[0]),lineterminator='\n');w.writeheader();w.writerows(items)
for fp,(status,h) in before.items():assert rs[fp]['status']==status and rs[fp]['report_sha256']==h
result={'passed':True,'recorded_utc':datetime.now(timezone.utc).isoformat(),'predeclared_in_plan_sha256':sha(R/'plan.json'),'current_report_sha256':sha(R/'report.json'),'source_reports':sources,'registered_unique_cells':54,'cells_per_scope':27,'cost_metric_rows':162,'adjacent_edges':324,'by_K':by_k,'edge_flags':flags,'all_canonical_scenes_and_qualifications_preserved':True,'new_strategy_configurations':0,'new_strategy_valuation_calls':0,'new_orders':0,'new_NAV_computations':0,'canonical_results':{fp:{'status':status,'report_sha256':h} for fp,(status,h) in before.items()},'interpretation':'Dependent existing-metric diagnostic across previously used development history, not new independent trials, not a regrade, not future validation; component and parent share ETH and all parents share BTC.'};put(R/'readonly_cross_K_diagnostic.json',result);print(json.dumps({'passed':True,'cells':54,'cost_rows':162,'edges':324,'new_valuations':0,'by_K':by_k}),flush=True)
