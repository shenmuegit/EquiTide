"""Export all recorded costs/folds,2D/3D neighborhoods and matched immutable references."""
import csv,itertools,json
from datetime import datetime,timedelta,timezone
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run import ROOT,R,sha,put,grid_configs,axes,positive_recent,stress_fold_ok,WEIGHTS,EXITS,SLOWS
report=json.loads((R/'report.json').read_text());assert json.loads((R/'verification.json').read_text())['passed'];configs=report['configs'];grid=grid_configs(configs);holds={}
for name,x in json.loads((R/'holds.json').read_text()).items():
 c=json.loads((ROOT/x['report']).read_text())['configs'][name];q=json.loads((ROOT/x['spec']).read_text())['parameters'];holds[q['raw_component_multipliers'][0]]={**c,'read_only_anchor':True}
x=next(x for x in report['component_sources'].values() if x['asset']=='ETH' and x['role']=='benchmark');ethhold=json.loads((ROOT/x['report']).read_text())['configs'][x['name']];ethhold={**ethhold,'read_only_anchor':True,'scope':'native','role':'benchmark'}
allc={**grid,**{c['name']:c for c in holds.values()},ethhold['name']:ethhold};assert len(allc)==52
cols=['net_return_pct','max_drawdown_pct','sharpe_365','calmar'];cost=[];full=[];recent=[];daily=[];comparisons=[];edges=[]
for c in allc.values():
 for k,z in c['scenes'].items():
  t=z.get('recent40',z.get('extension40'));cost.append({'name':c['name'],'scope':c['scope'],'role':c['role'],'old_readonly':bool(c.get('read_only_anchor')),'status':c['status'],'cost_multiplier':int(k),**{f:z[f] for f in cols},'recent_return_pct':t['net_return_pct'],'recent_DD_pct':t['max_drawdown_pct'],'recent_positive_folds':sum(f['net_return_pct']>0 for f in t['folds']),'positive_complete30d_folds':sum(f['net_return_pct']>0 for f in z['folds'][:12]),'executions':z['executions'],'round_trips':z['round_trips'],'cost_usdt':z['cost_usdt'],'funding_usdt':z['funding_usdt'],'NAV_sha256_f64le':z['NAV_sha256_f64le']})
  for dest,folds in [(full,z['folds']),(recent,t['folds'])]:
   for f in folds:
    start=f.get('start_utc') or (datetime(2026,9,14,0,1,tzinfo=timezone.utc)+timedelta(days=5*(f['fold']-1))).isoformat().replace('+00:00','Z');end=f.get('end_exclusive_utc') or (datetime(2026,9,14,0,1,tzinfo=timezone.utc)+timedelta(days=5*f['fold'])).isoformat().replace('+00:00','Z');dest.append({'name':c['name'],'cost_multiplier':int(k),'fold':f['fold'],'duration_days':f['duration_days'],'start_utc':start,'end_exclusive_utc':end,**{a:f[a] for a in cols}})
  if c['name'] in configs:
   for i,v in enumerate(z['daily_equity_usdt']):daily.append({'name':c['name'],'cost_multiplier':int(k),'day_boundary_index':i,'NAV_usdt':v})
for c in configs.values():
 if c['scope']=='native':
  control=next(x for x in grid.values() if x['scope']=='native' and x['trend_lookback_days']==29 and x['exit_buffer_fraction']==c['exit_buffer_fraction']);hold=ethhold
 else:
  control=next(x for x in grid.values() if x['scope']=='parent' and x['BTC_bank_units']==c['BTC_bank_units'] and x['ETH_exit_buffer_fraction']==c['ETH_exit_buffer_fraction'] and x['ETH_trend_lookback_days']==29);hold=holds[c['BTC_bank_units']]
 for typ,ref in [('same_E_and_weight_S29',control),('same_scale_constant_long',hold)]:
  for k in ['1','2','3']:
   a,b=c['scenes'][k],ref['scenes'][k];ta,tb=a.get('recent40',a.get('extension40')),b.get('recent40',b.get('extension40'));comparisons.append({'name':c['name'],'reference_type':typ,'reference_name':ref['name'],'cost_multiplier':int(k),'return_pct':a['net_return_pct'],'reference_return_pct':b['net_return_pct'],'delta_return_pp':a['net_return_pct']-b['net_return_pct'],'DD_pct':a['max_drawdown_pct'],'reference_DD_pct':b['max_drawdown_pct'],'recent_return_pct':ta['net_return_pct'],'reference_recent_return_pct':tb['net_return_pct'],'recent_delta_pp':ta['net_return_pct']-tb['net_return_pct'],'positive_recent_folds':sum(f['net_return_pct']>0 for f in ta['folds']),'reference_positive_recent_folds':sum(f['net_return_pct']>0 for f in tb['folds'])})
for scope in ['native','parent']:
 sub={n:c for n,c in grid.items() if c['scope']==scope};ax=axes(next(iter(sub.values())));index={tuple(c[k] for k in ax):c for c in sub.values()}
 for c in sub.values():
  pt=[c[k] for k in ax]
  for j,(key,vals) in enumerate(ax.items()):
   i=vals.index(pt[j])
   if i+1==len(vals):continue
   nxt=pt.copy();nxt[j]=vals[i+1];b=index[tuple(nxt)];a0,b0=c['scenes']['3'],b['scenes']['3'];edges.append({'scope':scope,'axis':key,'left':c['name'],'right':b['name'],'full_return_delta_pp':b0['net_return_pct']-a0['net_return_pct'],'DD_delta_pp':b0['max_drawdown_pct']-a0['max_drawdown_pct'],'Sharpe_delta':None if a0['sharpe_365'] is None or b0['sharpe_365'] is None else b0['sharpe_365']-a0['sharpe_365'],'Calmar_delta':None if a0['calmar'] is None or b0['calmar'] is None else b0['calmar']-a0['calmar'],'recent_return_delta_pp':b0['recent40']['net_return_pct']-a0['recent40']['net_return_pct'],'left_min_positive_recent_folds':min(positive_recent(c,k) for k in ['1','2','3']),'right_min_positive_recent_folds':min(positive_recent(b,k) for k in ['1','2','3'])})
assert [len(x) for x in [cost,full,recent,daily,edges,comparisons]]==[156,2028,1248,26712,92,144]
exports={}
for name,rows in [('cost_results',cost),('walk_forward_folds',full),('recent40_folds',recent),('daily_NAV',daily),('sensitivity_edges',edges),('reference_comparisons',comparisons)]:
 path=R/(name+'.csv')
 with path.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
 exports[name]={'path':str(path.relative_to(ROOT)),'rows':len(rows),'sha256':sha(path)}
frag={'report_sha256':sha(R/'report.json'),'new_financial_evaluations':0,'old24statuses_unchanged':True,'rows':[]}
for c in configs.values():frag['rows'].append({'name':c['name'],'fingerprint':c['fingerprint'],'scope':c['scope'],'status':c['status'],'positive_recent_folds_by_cost':{k:positive_recent(c,k) for k in ['1','2','3']},'minimum_positive_recent_fold_pct_by_cost':{k:min((f['net_return_pct'] for f in c['scenes'][k]['recent40']['folds'] if f['net_return_pct']>0),default=None) for k in ['1','2','3']},'local_recent6of8_allcost_fraction':c['sensitivity']['local_recent6of8_allcost_fraction'],'independent_future_qualified':False})
put(R/'qualification_fragility.json',frag)
items=[('3x full net %',lambda c:c['scenes']['3']['net_return_pct']),('3x continuous max DD %',lambda c:c['scenes']['3']['max_drawdown_pct']),('3x daily Sharpe',lambda c:c['scenes']['3']['sharpe_365']),('3x Calmar',lambda c:c['scenes']['3']['calmar']),('3x recent40 net %',lambda c:c['scenes']['3']['recent40']['net_return_pct']),('Minimum positive5d folds 1/2/3x',lambda c:min(positive_recent(c,k) for k in ['1','2','3']))];figures=[]
for scope,E in [('native',None),*[('parent',E) for E in EXITS]]:
 sub={tuple(c[k] for k in axes(c)):c for c in grid.values() if c['scope']==scope};xs=EXITS if scope=='native' else WEIGHTS;fig,axs=plt.subplots(2,3,figsize=(17,9))
 for ax,(title,fn) in zip(axs.flat,items):
  a=np.array([[fn(sub[x,S] if scope=='native' else sub[x,E,S]) for x in xs] for S in SLOWS]);im=ax.imshow(a,aspect='auto',cmap='viridis');ax.set_xticks(range(3),[str(x) for x in xs]);ax.set_yticks(range(4),[str(S) for S in SLOWS]);ax.set_xlabel('Exit E' if scope=='native' else 'Raw BTC bank units w');ax.set_ylabel('Slow S (old28/29,new30/31)');ax.set_title(title);fig.colorbar(im,ax=ax)
  for j,i in itertools.product(range(4),range(3)):ax.text(i,j,f'{a[j,i]:.2f}',ha='center',va='center',color='white',fontsize=10)
 fig.suptitle(f'{scope}: S30/31 boundary extension; E={E}; repeated history, no future qualification');fig.tight_layout();path=R/(f'sensitivity_{scope}'+('' if E is None else f'_{round(E*10000)}')+'.png');fig.savefig(path,dpi=125);plt.close(fig);figures.append({'path':str(path.relative_to(ROOT)),'sha256':sha(path),'panels':6})
summary={'report_sha256':sha(R/'report.json'),'exports':exports,'figures':figures,'grid_cells':{'native':12,'parent':36},'edges':92,'status_counts':dict(Counter(c['status'] for c in configs.values())),'failed_criterion_counts':dict(Counter(k for c in configs.values() for k in c['failed_criteria'])),'strict_individual_costfold_passes':sum(stress_fold_ok(c) for c in configs.values())};put(R/'sensitivity_summary.json',summary)
passed=[c for c in configs.values() if c['status']=='passed'];best=max(passed or list(configs.values()),key=lambda c:c['scenes']['3']['net_return_pct']);put(R/'representative.json',{'name':best['name'],'fingerprint':best['fingerprint'],'status':best['status'],'scope':best['scope'],'raw_units':best.get('raw_component_multipliers'),'E':best.get('exit_buffer_fraction',best.get('ETH_exit_buffer_fraction')),'S':best.get('trend_lookback_days',best.get('ETH_trend_lookback_days')),'return3_pct':best['scenes']['3']['net_return_pct'],'whole_DD3_pct':best['scenes']['3']['max_drawdown_pct'],'recent_return3_pct':best['scenes']['3']['recent40']['net_return_pct'],'positive_recent_folds_by_cost':{k:positive_recent(best,k) for k in ['1','2','3']},'sensitivity':best['sensitivity'],'failed_criteria':best['failed_criteria'],'independent_future_qualified':False})
with (R/'result.md').open('w') as f:
 f.write('# BTC/ETH S30、S31边界扩展实际回测\n\n24项新配置：6原生ETH、18静态原值所有权组合，72成本场景。原生L3/H2.5%、E−1.5/−1/−0.5%、S30/31，N3000/10000；固定BTC31/H4/E1、N1000/10000。组合原值[w,2−w]，w0.375/0.5/0.625，本金20000，固定所有权占比18.75/25/31.25% BTC与其余ETH；不自动归一化。新规模订单执行仅在原生固定规模内成立，组合为银行净值所有权。\n\n')
 f.write('370日按时间连续OOS，12×30日+10日尾折，近期40日继承第330日状态、8×5日；历史被多轮研究使用，属于开发数据。33个完整上下文收盘支持最大32日ROC，无未来价/资金费用于信号或规模。逐折及连续完整净值回撤已独立核验。\n\n')
 f.write('预先固定的原生二维12格、组合三维36格，共24旧只读+24新；92条邻边。每项均实际执行1/2/3倍手续费、价差、滑点、成交量相关冲击和资金费压力，实际lot/tick/参与率/全额抵押及闭合小时风险代理。各成本均需近期至少6/8正折，局部满足该条件比例至少60%，无放宽门槛。\n\n')
 f.write('历史门槛通过'+str(len(passed))+'项；淘汰'+str(24-len(passed))+'项。独立各成本近期6/8通过'+str(summary['strict_individual_costfold_passes'])+'项。失败条件汇总：`'+json.dumps(summary['failed_criterion_counts'],ensure_ascii=False)+'`。\n\n')
 f.write('|配置|状态|3倍370日净收益%|整体最大回撤%|近期净收益%|1/2/3倍近期正折|局部严格通过率|\n|---|---|---:|---:|---:|---|---:|\n')
 for c in configs.values():f.write('|'+c['name']+'|'+c['status']+'|'+f"{c['scenes']['3']['net_return_pct']:.6f}|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['scenes']['3']['recent40']['net_return_pct']:.6f}|"+'/'.join(str(positive_recent(c,k)) for k in ['1','2','3'])+'|'+f"{c['sensitivity']['local_recent6of8_allcost_fraction']:.6f}"+'|\n')
 f.write('\n完整spec、成交/资金费/状态段、每成本/逐折/全NAV哈希和全部正负结果在本目录。旧S28/S29通过或拒绝历史状态不改；S31仍新上边界，不能以开发网格通过称稳定实盘盈利、独立未来资格或真实重配规模可执行容量。\n\n来源：[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)、[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)；本轮已读取原始研究页。慢门控与成本试验是加密数据上的研究推断，不能移植论文收益结论。\n')
print(json.dumps(summary),flush=True)
