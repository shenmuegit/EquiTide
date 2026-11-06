"""Describe 27 saved H/D/K results; never value or regrade an old configuration."""
import csv,itertools,json,statistics,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R))
from common import reg,sha,put,rel,now
H=[.03,.04,.05];D=[6,7,8];K=[.01,.02,.03];coords=list(itertools.product(H,D,K))
def adjacent():
 out=[]
 for c in coords:
  for axis,values in enumerate([H,D,K]):
   i=values.index(c[axis])
   if i+1<len(values):
    z=list(c);z[axis]=values[i+1];out.append((axis,c,tuple(z)))
 return out
def neighbors(c):return [z for z in coords if all(abs(v.index(c[j])-v.index(z[j]))<=1 for j,v in enumerate([H,D,K]))]
if '--self-test' in sys.argv:
 assert len(coords)==len(set(coords))==27 and len(adjacent())==54 and len(neighbors((.03,6,.01)))==8 and len(neighbors((.04,7,.02)))==27
 print('PASS synthetic27coordinates,54uniqueadjacentpairs,clipped8corner/27center neighborhood;0marketvaluation');raise SystemExit(0)
rd=lambda p:json.loads(p.read_text());pre=rd(R/'joint_grid_before_evaluation.json');p=rd(R/'plan.json');rep=rd(R/'report.json');binding=rd(R/'code_binding_before_evaluation.json');assert pre['helper_sha256']==sha(Path(__file__))==binding['immutable_source_sha256'][rel(Path(__file__))] and pre['frozen_utc']<rep['evaluation_started_utc']
assert pre['axes']==p['supplemental_joint_sensitivity']['axes'] and len(pre['cells'])==27 and pre['new_cells']==8 and pre['old_cells']==19
rs=reg.read_records(ROOT/'research/automation/registry.jsonl');cells={};csvrows=[]
for z in pre['cells']:
 c=(z['BTC_H'],z['D'],z['K']);assert c in coords and c not in cells;fp=z['fingerprint'];sp=rd(ROOT/z['spec']);q=sp['parameters'];rec=rs[fp];assert sha(ROOT/z['spec'])==z['spec_sha256'] and reg.fingerprint(sp)==fp and rec['result_available']
 assert q['BTC_lookback_days']==29 and q['BTC_return_hurdle']==c[0] and q['component_capitals_usdt']==[3750,15000] and q['component_initial_entry_notionals_usdt']==[1000,4500] and [x['weight'] for x in sp['components']]==[1,1]
 bp,ep=[rs[x['fingerprint']]['spec']['parameters'] for x in sp['components']];assert bp['lookback_days']==29 and bp['return_hurdle']==c[0] and ep['trend_slope_lag_days']==c[1] and ep['trend_slope_hurdle_fraction']==c[2]
 if z['new']:
  path=R/'report.json';cfg=next(x for x in rep['configs'].values() if x['fingerprint']==fp);assert rec['report_sha256']==sha(path) and len(rep['configs'])==8
 else:
  path=ROOT/z['report'];assert sha(path)==z['report_sha256']==rec['report_sha256'] and sha(ROOT/z['archive'])==z['archive_sha256'] and rec['status']==z['status'];cfg=next(x for x in rd(path)['configs'].values() if x['fingerprint']==fp)
 assert cfg['status']==rec['status'];metrics={}
 for k,s in cfg['scenes'].items():
  assert s['initial_capital_usdt']==18750 and len(s['folds'])==13 and len(s['recent40']['folds'])==8
  m={key:s[key] for key in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','cost_usdt','funding_usdt','executions','round_trips']};m.update(recent40_net_return_pct=s['recent40']['net_return_pct'],positive5d=sum(f['net_return_pct']>0 for f in s['recent40']['folds']));metrics[k]=m;csvrows.append([*c,fp,z['new'],cfg['status'],k,*m.values()])
 strict=all(m['recent40_net_return_pct']>0 and m['positive5d']>=6 for m in metrics.values());cells[c]={'BTC_H':c[0],'ETH_D':c[1],'ETH_K':c[2],'fingerprint':fp,'new_this_round':z['new'],'canonical_status':cfg['status'],'source_report':rel(path),'source_report_sha256':sha(path),'original_criteria':cfg['criteria'],'strict_recent_allcost':strict,'metrics':metrics}
assert set(cells)==set(coords) and sum(z['new_this_round'] for z in cells.values())==8
for c,z in cells.items():
 ns=neighbors(c);z['descriptive_3D_neighborhood']={'cells':len(ns),'positive3_fraction':sum(cells[t]['metrics']['3']['net_return_pct']>0 for t in ns)/len(ns),'strict_recent_allcost_fraction':sum(cells[t]['strict_recent_allcost'] for t in ns)/len(ns),'not_used_to_regrade_canonical_status':True}
with (R/'joint_H_D_K_metrics.csv').open('w',newline='') as f:
 w=csv.writer(f,lineterminator='\n');w.writerow(['BTC_H','ETH_D','ETH_K','fingerprint','new_this_round','canonical_status','cost_multiplier',*next(iter(cells.values()))['metrics']['1']]);w.writerows(csvrows)
edges=[];cliffs={}
for axis,a,b in adjacent():
 for k in ['1','2','3']:
  x,y=cells[a]['metrics'][k],cells[b]['metrics'][k];edges.append({'axis':['BTC_H','ETH_D','ETH_K'][axis],'cost_multiplier':k,'from':list(a),'to':list(b),'from_fingerprint':cells[a]['fingerprint'],'to_fingerprint':cells[b]['fingerprint'],'absolute_Sharpe_change':abs(x['sharpe_365']-y['sharpe_365']),'absolute_return_change_pp':abs(x['net_return_pct']-y['net_return_pct']),'absolute_whole_DD_change_pp':abs(x['max_drawdown_pct']-y['max_drawdown_pct'])})
for axis in ['BTC_H','ETH_D','ETH_K']:
 cliffs[axis]={}
 for k in ['1','2','3']:
  xs=[x['absolute_Sharpe_change'] for x in edges if x['axis']==axis and x['cost_multiplier']==k];threshold=2*statistics.stdev(xs);cliffs[axis][k]={'edge_count':len(xs),'max_Sharpe_change':max(xs),'two_std_threshold':threshold,'descriptive_cliff_flag':max(xs)>threshold}
assert len(csvrows)==81 and len(edges)==162
uniform=[]
for h in [.03,.05]:
 for k in ['1','2','3']:
  ds=[cells[h,d,kk]['metrics'][k]['net_return_pct']-cells[.04,d,kk]['metrics'][k]['net_return_pct'] for d,kk in itertools.product(D,K)];assert max(ds)-min(ds)<1e-10;uniform.append({'BTC_H':h,'reference_H':.04,'cost_multiplier':k,'nine_same_ETH_cells':9,'min_return_delta_pp':min(ds),'max_return_delta_pp':max(ds),'uniform_shift_verified':True,'interpretation':'Shared independent BTC bank changes add the same full-period NAV difference; dependent combinations do not supply nine independent alpha tests.'})
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
fig,axs=plt.subplots(3,3,figsize=(12,10),layout='constrained')
columns=[('3x continuous370 return %',lambda z:z['metrics']['3']['net_return_pct']),('3x wholecurve DD %',lambda z:z['metrics']['3']['max_drawdown_pct']),('3x recent positive5d /8',lambda z:z['metrics']['3']['positive5d'])]
for j,(label,fn) in enumerate(columns):
 vals=[fn(z) for z in cells.values()];lo,hi=(0,8) if j==2 else (min(vals),max(vals))
 for i,h in enumerate(H):
  arr=np.array([[fn(cells[h,d,k]) for k in K] for d in D]);ax=axs[i,j];im=ax.imshow(arr,cmap='RdYlGn_r' if j==1 else 'RdYlGn',vmin=lo,vmax=hi,aspect='auto');ax.set_title('BTC29/H'+str(round(h*100))+'% | '+label);ax.set_xticks(range(3),['K1%','K2%','K3%']);ax.set_yticks(range(3),['D6','D7','D8']);ax.set_xlabel('ETH strict finiteEWM slope K');ax.set_ylabel('ETH slope lag D')
  for di,d in enumerate(D):
   for ki,k in enumerate(K):ax.text(ki,di,str(round(float(arr[di,ki]),3))+(' N' if cells[h,d,k]['new_this_round'] else ' O'),ha='center',va='center',fontsize=10)
  fig.colorbar(im,ax=ax,shrink=.7)
fig.suptitle('Predeclared BTC H3/4/5% x ETH D6/7/8 x K1/2/3% | native C3750/N1000 + C15000/N4500\nraw[1,1],total18750 | 8 new N + 19 readonly O | reused dependent development history');fig.savefig(R/'joint_H_D_K.png',dpi=140);plt.close(fig)
summary={'passed':True,'predeclared_inventory_sha256':sha(R/'joint_grid_before_evaluation.json'),'new_report_sha256':sha(R/'report.json'),'helper_sha256':sha(Path(__file__)),'cells':27,'new_cells':8,'old_cells':19,'cost_metric_rows':81,'adjacent_cost_edges':162,'positive3_cells':sum(z['metrics']['3']['net_return_pct']>0 for z in cells.values()),'strict_recent_allcost_cells':sum(z['strict_recent_allcost'] for z in cells.values()),'by_BTC_H':{str(h):{'cells':9,'strict_recent_allcost':sum(cells[h,d,k]['strict_recent_allcost'] for d,k in itertools.product(D,K)),'same_recent_pattern_as_H4':all(cells[h,d,k]['strict_recent_allcost']==cells[.04,d,k]['strict_recent_allcost'] for d,k in itertools.product(D,K))} for h in H},'uniform_return_shifts':uniform,'descriptive_cliffs':cliffs,'nodes':[cells[c] for c in coords],'edges':edges,'all_canonical_statuses_criteria_and_old_report_hashes_preserved':True,'no_new_financial_valuation_or_reservation':True,'not_independent_final_future_or_live_evidence':True,'image':rel(R/'joint_H_D_K.png'),'image_sha256':sha(R/'joint_H_D_K.png')};put(R/'joint_sensitivity.json',summary);print(json.dumps({key:summary[key] for key in ['passed','cells','new_cells','old_cells','cost_metric_rows','adjacent_cost_edges','positive3_cells','strict_recent_allcost_cells','by_BTC_H']}),flush=True)
