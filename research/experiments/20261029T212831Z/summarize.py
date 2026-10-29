"""All costs/folds/two-parameter cells,readonly controls and figures after actual audit."""
import csv,itertools,json
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run import ROOT,R,sha,put,grid_configs,axes,positive_recent,stress_fold_ok,WINDOWS,CAPS
from controls import load_controls
report=json.loads((R/'report.json').read_text());assert json.loads((R/'verification.json').read_text())['passed'];configs=report['configs'];grid=grid_configs(configs);controls=load_controls();allc={**configs,**{c['name']:c for c in controls.values()}};assert len(allc)==22
cols=['net_return_pct','max_drawdown_pct','sharpe_365','calmar'];cost=[];full=[];recent=[];daily=[];comparisons=[];edges=[]
for c in allc.values():
 for k,z in c['scenes'].items():
  t=z['recent40'];cost.append({'name':c['name'],'scope':c['scope'],'role':c['role'],'old_readonly':bool(c.get('read_only_anchor')),'status':c['status'],'cost_multiplier':int(k),**{f:z[f] for f in cols},'recent_return_pct':t['net_return_pct'],'recent_DD_pct':t['max_drawdown_pct'],'recent_positive_folds':sum(f['net_return_pct']>0 for f in t['folds']),'positive_complete30d_folds':sum(f['net_return_pct']>0 for f in z['folds'][:12]),'executions':z['executions'],'round_trips':z['round_trips'],'cost_usdt':z['cost_usdt'],'cost_pct_initial':z['cost_pct_initial'],'funding_usdt':z['funding_usdt'],'gross_plus_funding_to_cost':z['gross_reference_PnL_to_execution_cost'],'NAV_sha256_f64le':z['NAV_sha256_f64le']})
  for dest,folds in [(full,z['folds']),(recent,t['folds'])]:
   for f in folds:dest.append({'name':c['name'],'cost_multiplier':int(k),'fold':f['fold'],'duration_days':f['duration_days'],'start_utc':f['start_utc'],'end_exclusive_utc':f['end_exclusive_utc'],**{a:f[a] for a in cols}})
  if c['name'] in configs:
   for i,v in enumerate(z['daily_equity_usdt']):daily.append({'name':c['name'],'cost_multiplier':int(k),'day_boundary_index':i,'NAV_usdt':v})
for c in configs.values():
 control=controls['nogate_nogate_ETH' if c['scope']=='native' else 'nogate_nogate_parent'];hold=controls['hold_ETH' if c['scope']=='native' else 'hold_COMBO']
 for typ,ref in [('matched_ungated_price_rules',control),('same_scale_constant_long',hold)]:
  for k in ['1','2','3']:
   a,b=c['scenes'][k],ref['scenes'][k];ta,tb=a['recent40'],b['recent40'];comparisons.append({'name':c['name'],'reference_type':typ,'reference_name':ref['name'],'cost_multiplier':int(k),'return_pct':a['net_return_pct'],'reference_return_pct':b['net_return_pct'],'delta_return_pp':a['net_return_pct']-b['net_return_pct'],'DD_pct':a['max_drawdown_pct'],'reference_DD_pct':b['max_drawdown_pct'],'recent_return_pct':ta['net_return_pct'],'reference_recent_return_pct':tb['net_return_pct'],'recent_delta_pp':ta['net_return_pct']-tb['net_return_pct'],'positive_recent_folds':sum(f['net_return_pct']>0 for f in ta['folds']),'reference_positive_recent_folds':sum(f['net_return_pct']>0 for f in tb['folds'])})
for scope in ['native','parent']:
 sub={n:c for n,c in grid.items() if c['scope']==scope};ax=axes(next(iter(sub.values())));index={tuple(c[k] for k in ax):c for c in sub.values()}
 for c in sub.values():
  pt=[c[k] for k in ax]
  for j,(key,vals) in enumerate(ax.items()):
   i=vals.index(pt[j])
   if i+1==len(vals):continue
   nxt=pt.copy();nxt[j]=vals[i+1];b=index[tuple(nxt)];a0,b0=c['scenes']['3'],b['scenes']['3'];edges.append({'scope':scope,'axis':key,'left':c['name'],'right':b['name'],'full_return_delta_pp':b0['net_return_pct']-a0['net_return_pct'],'DD_delta_pp':b0['max_drawdown_pct']-a0['max_drawdown_pct'],'Sharpe_delta':None if a0['sharpe_365'] is None or b0['sharpe_365'] is None else b0['sharpe_365']-a0['sharpe_365'],'Calmar_delta':None if a0['calmar'] is None or b0['calmar'] is None else b0['calmar']-a0['calmar'],'recent_return_delta_pp':b0['recent40']['net_return_pct']-a0['recent40']['net_return_pct'],'left_min_positive_recent_folds':min(positive_recent(c,k) for k in ['1','2','3']),'right_min_positive_recent_folds':min(positive_recent(b,k) for k in ['1','2','3'])})
assert [len(x) for x in [cost,full,recent,daily,edges,comparisons]]==[66,858,528,20034,24,108];exports={}
for name,rows in [('cost_results',cost),('walk_forward_folds',full),('recent40_folds',recent),('daily_NAV',daily),('sensitivity_edges',edges),('reference_comparisons',comparisons)]:
 path=R/(name+'.csv')
 with path.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
 exports[name]={'path':str(path.relative_to(ROOT)),'rows':len(rows),'sha256':sha(path)}
frag={'report_sha256':sha(R/'report.json'),'new_financial_evaluations':0,'old_controls_statuses_unchanged':True,'rows':[]}
for c in configs.values():frag['rows'].append({'name':c['name'],'fingerprint':c['fingerprint'],'scope':c['scope'],'status':c['status'],'N':c['entry_funding_lookback_settlements'],'cap':c['entry_funding_cost_cap_per_settlement'],'positive_recent_folds_by_cost':{k:positive_recent(c,k) for k in ['1','2','3']},'minimum_positive_recent_fold_pct_by_cost':{k:min((f['net_return_pct'] for f in c['scenes'][k]['recent40']['folds'] if f['net_return_pct']>0),default=None) for k in ['1','2','3']},'local_recent6of8_allcost_fraction':c['sensitivity']['local_recent6of8_allcost_fraction'],'independent_future_qualified':False})
put(R/'qualification_fragility.json',frag);figures=[];items=[('3x full net %',lambda c:c['scenes']['3']['net_return_pct']),('3x continuous max DD %',lambda c:c['scenes']['3']['max_drawdown_pct']),('3x daily Sharpe',lambda c:c['scenes']['3']['sharpe_365']),('3x Calmar',lambda c:c['scenes']['3']['calmar']),('3x recent40 net %',lambda c:c['scenes']['3']['recent40']['net_return_pct']),('Minimum positive5d folds 1/2/3x',lambda c:min(positive_recent(c,k) for k in ['1','2','3']))]
for scope in ['native','parent']:
 sub={(c['entry_funding_lookback_settlements'],c['entry_funding_cost_cap_per_settlement']):c for c in grid.values() if c['scope']==scope};fig,axs=plt.subplots(2,3,figsize=(17,9))
 for ax,(title,fn) in zip(axs.flat,items):
  a=np.array([[fn(sub[n,c]) for c in CAPS] for n in WINDOWS],dtype=float);im=ax.imshow(a,aspect='auto',cmap='viridis');ax.set_xticks(range(3),[str(c*10000) for c in CAPS]);ax.set_yticks(range(3),[str(n) for n in WINDOWS]);ax.set_xlabel('Directional funding cost cap per settlement (bp)');ax.set_ylabel('Last N already-available settlements');ax.set_title(title);fig.colorbar(im,ax=ax)
  for j,i in itertools.product(range(3),range(3)):ax.text(i,j,f'{a[j,i]:.2f}',ha='center',va='center',color='white',fontsize=11)
 fig.suptitle(f'{scope}: available-funding entry-only cap; fixed price rules; repeated development history');fig.tight_layout();path=R/f'sensitivity_{scope}.png';fig.savefig(path,dpi=125);plt.close(fig);figures.append({'path':str(path.relative_to(ROOT)),'sha256':sha(path),'panels':6})
cliffs=[]
for scope,key in itertools.product(['native','parent'],list(axes(next(iter(configs.values()))))):
 es=[x for x in edges if x['scope']==scope and x['axis']==key];ds=[float(x['Sharpe_delta']) for x in es if x['Sharpe_delta'] is not None];sd=float(np.std(ds)) if ds else 0.;cliffs.extend({**x,'difference_std':sd,'flag_abs_delta_gt2std':abs(x['Sharpe_delta'])>2*sd} for x in es if x['Sharpe_delta'] is not None)
summary={'report_sha256':sha(R/'report.json'),'exports':exports,'figures':figures,'grid_cells':{'native':9,'parent':9},'edges':24,'status_counts':dict(Counter(c['status'] for c in configs.values())),'failed_criterion_counts':dict(Counter(k for c in configs.values() for k in c['failed_criteria'])),'strict_individual_costfold_passes':sum(stress_fold_ok(c) for c in configs.values()),'positive_3x_Sharpe_fraction_by_scope':{s:sum(c['scenes']['3']['sharpe_365'] is not None and c['scenes']['3']['sharpe_365']>0 for c in configs.values() if c['scope']==s)/9 for s in ['native','parent']},'cliff_diagnostics':cliffs};put(R/'sensitivity_summary.json',summary)
passed=[c for c in configs.values() if c['status']=='passed'];best=next(c for c in configs.values() if c['scope']=='parent' and c['entry_funding_lookback_settlements']==6 and c['entry_funding_cost_cap_per_settlement']==.00005);put(R/'representative.json',{'name':best['name'],'fingerprint':best['fingerprint'],'status':best['status'],'scope':best['scope'],'raw_units':best.get('raw_component_multipliers'),'N':best['entry_funding_lookback_settlements'],'cap':best['entry_funding_cost_cap_per_settlement'],'return3_pct':best['scenes']['3']['net_return_pct'],'whole_DD3_pct':best['scenes']['3']['max_drawdown_pct'],'recent_return3_pct':best['scenes']['3']['recent40']['net_return_pct'],'positive_recent_folds_by_cost':{k:positive_recent(best,k) for k in ['1','2','3']},'sensitivity':best['sensitivity'],'failed_criteria':best['failed_criteria'],'independent_future_qualified':False,'selection':'Geometric grid center N6/C0.5bp,communicationonly;not selectedhighestreturn ornew modeltest'})
with (R/'result.md').open('w') as f:
 f.write('# BTC/ETH 可得资金费开仓过滤实际回测\n\n18项新配置：9原生ETH、9固定原值[0.5,1.5]组合，54成本场景。价格规则固定L3/H2.5%/E−1%/S28多数慢门控，N3000/10000；固定BTC31/H4/E1、N1000/10000。组合本金20000，银行净值所有权5000/15000，原值权重不归一化，持有初始资本25%/75%；原生固定规模订单实际重算，组合属于被动所有权指数。\n\n')
 f.write('新假设：仅当拟新仓方向×最后N条已可得真实资金费均值≤C时开新仓，N3/6/9与C0/0.5/1bp完整二维预设；恰等上限允许。资金费需available_ts和settlement_ts均不晚于00:00已完成日收盘的信号时间，最新信息不超过16小时，00:00结算但01:00可得的当期数据排除。已有实际仓位若仍符合快线持有规则则不受资金费门控影响；快线退出照常，反向拟开仓被阻时先平旧仓后现金。资金费代理不是未来预测或无风险套利。\n\n')
 f.write('真实数据370日连续OOS、12×30日+10日尾折，近期40日继承第330日状态、8×5日；33天上下文和3天初始embargo，不训练标签，不用未来资金费或执行价决定规模。全部历史已反复研究，仅开发验证。逐折与完整连续净值整体回撤、1/2/3倍手续费/价差/滑点/成交额冲击/实际资金费/lot/tick/全额抵押/闭合小时保证金代理均已计算并独审。\n\n')
 f.write('历史门槛通过'+str(len(passed))+'项，淘汰'+str(18-len(passed))+'项。各成本近期正折均至少6/8、局部满足此条件比例至少60%、全期及近期收益全成本正、月折9/12、3倍整体DD≤25%、至少4往返、成本安全边际≥2.5等门槛未放宽。失败计数：`'+json.dumps(summary['failed_criterion_counts'],ensure_ascii=False)+'`。\n\n')
 f.write('|配置|状态|3倍370日净收益%|整体最大回撤%|近期净收益%|1/2/3倍近期正折|局部严格通过率|\n|---|---|---:|---:|---:|---|---:|\n')
 for c in configs.values():f.write('|'+c['name']+'|'+c['status']+'|'+f"{c['scenes']['3']['net_return_pct']:.6f}|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['scenes']['3']['recent40']['net_return_pct']:.6f}|"+'/'.join(str(positive_recent(c,k)) for k in ['1','2','3'])+'|'+f"{c['sensitivity']['local_recent6of8_allcost_fraction']:.6f}"+'|\n')
 f.write('\n与完全相同价格规则的旧无资金费门控、同规模常数多头和现金0%（仅定义上比较，无新现金回测）比较见reference_comparisons.csv。两参数邻域18格/24边、全收益/DD/Sharpe/Calmar与cliff诊断见sensitivity_summary；旧对照不伪装有限数值邻居、资格与字节不变。所有spec、原生决策/资金费特征/成交/资金费/状态段和负收益折永久留档。\n\n局限：normalized available_ts统一滞后1小时是数据的保守可得假设，不能证明交易所真实发布延迟。资金费可能变号，所选均值不是预测；估计价差/滑点/冲击及1%闭合小时风险代理缺L2/TCA/历史全档保证金/逐tick清算验证。组合银行所有权不证明重配规模容量，任何历史通过不代表独立未来或稳定实盘盈利。\n\n来源：[Binance资金费机制](https://www.binance.com/en/support/faq/detail/360033525031)与[官方历史资金费API](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Get-Funding-Rate-History)，本轮实际读取；本轮开仓过滤为研究推断，官方材料未声称其收益。\n')
print(json.dumps({k:v for k,v in summary.items() if k not in ['cliff_diagnostics']},ensure_ascii=False),flush=True)
