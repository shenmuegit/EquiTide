"""Export every saved 3D portfolio cell, cost/fold metric and predeclared paired comparison."""
import copy,csv,gzip,io,itertools,json,statistics
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run import ROOT,R,BTC_HURDLES,SLOWS,LOOKS,axes,grid_configs,sha,put

def table(name,rows,compress=False):
 fields=list(dict.fromkeys(k for row in rows for k in row));s=io.StringIO(newline='');w=csv.DictWriter(s,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows);raw=s.getvalue().encode();(R/name).write_bytes(gzip.compress(raw,mtime=0) if compress else raw)
def main():
 assert not(R/'finish.json').exists();r=json.loads((R/'report.json').read_text());grid=grid_configs(r['configs']);assert len(grid)==36;ref=json.loads((R/'holds.json').read_text())['COMBO'];assert sha(ROOT/ref['report'])==ref['report_sha256'];hold=copy.deepcopy(json.loads((ROOT/ref['report']).read_text())['configs'][ref['name']]);hold.update(read_only_anchor=True,scope='parent',asset='COMBO',capital_usdt=20000)
 for z in hold['scenes'].values():
  if 'recent40' not in z:z['recent40']=copy.deepcopy(z['extension40'])
 allby={**grid,hold['name']:hold};rows=[];folds=[];recent=[];daily=[];comp=[];edges=[];cells={}
 for c in allby.values():
  old=c.get('read_only_anchor',False);meta={'name':c['name'],'scope':'parent','asset':'COMBO','role':c['role'],'read_only_anchor':old,'capital_usdt':20000}
  if c['role']=='candidate':meta.update({p:c[p] for p in axes(c)})
  cells[c['name']]={**meta,'fingerprint':c['fingerprint'],'original_or_new_status':c['status'],'scenes':{k:{p:z[p] for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','NAV_sha256_f64le']} for k,z in c['scenes'].items()}}
  for k,z in c['scenes'].items():
   rows.append({**meta,'cost_multiplier':int(k),'status':c['status'],**{p:z[p] for p in ['net_return_pct','max_drawdown_pct','daily_mark_drawdown_pct','sharpe_365','calmar','cost_usdt','cost_pct_initial','funding_usdt','gross_reference_PnL_to_execution_cost','executions','round_trips','NAV_sha256_f64le']},**{'recent40_'+p:z['recent40'][p] for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','NAV_sha256_f64le']},**{'cost_'+p:v for p,v in z['cost_parts_usdt'].items()}});folds.extend({**meta,'cost_multiplier':int(k),**f} for f in z['folds']);recent.extend({**meta,'cost_multiplier':int(k),**f} for f in z['recent40']['folds'])
   if old:continue
   daily.extend({**meta,'cost_multiplier':int(k),'boundary_index':j,'equity_usdt':v} for j,v in enumerate(z['daily_equity_usdt']))
   for kind,y in [('same_bank_BTC_H4',grid[c['matched_H4_reference']]),('same_bank_constant_long',hold)]:
    a=y['scenes'][k];comp.append({**meta,'cost_multiplier':int(k),'reference_kind':kind,'reference_name':y['name'],'reference_fingerprint':y['fingerprint'],'reference_original_status':y['status'],'new_return_pct':z['net_return_pct'],'reference_return_pct':a['net_return_pct'],'return_delta_pp':z['net_return_pct']-a['net_return_pct'],'DD_delta_pp':z['max_drawdown_pct']-a['max_drawdown_pct'],'recent40_return_delta_pp':z['recent40']['net_return_pct']-a['recent40']['net_return_pct'],'execution_delta':z['executions']-a['executions'],'cost_delta_usdt':z['cost_usdt']-a['cost_usdt'],'new_NAV_sha256':z['NAV_sha256_f64le'],'reference_NAV_sha256':a['NAV_sha256_f64le'],'cash_analytic_return_pct':0,'limit':'Samebank/N/ETHsource,onlyBTCthreshold/realizedriskchanges' if kind=='same_bank_BTC_H4' else 'Samecapital/Nlongreference,differentexposure/risk'})
 dims=axes(next(iter(grid.values())));fields=list(dims);by={tuple(c[p] for p in fields):c for c in grid.values()};assert set(by)==set(itertools.product(*dims.values()))
 for key,c in by.items():
  for i,(field,axis) in enumerate(dims.items()):
   j=axis.index(key[i])
   if j+1==len(axis):continue
   other=list(key);other[i]=axis[j+1];y=by[tuple(other)];a,b=c['scenes']['3'],y['scenes']['3'];edges.append({'axis':field,'from':c['name'],'to':y['name'],'return3_delta_pp':b['net_return_pct']-a['net_return_pct'],'DD3_delta_pp':b['max_drawdown_pct']-a['max_drawdown_pct'],'sharpe3_delta':b['sharpe_365']-a['sharpe_365'] if a['sharpe_365'] is not None and b['sharpe_365'] is not None else None,'recent40_return3_delta_pp':b['recent40']['net_return_pct']-a['recent40']['net_return_pct']})
 vals=[abs(e['sharpe3_delta']) for e in edges if e['sharpe3_delta'] is not None];cut=2*statistics.pstdev(vals)
 for e in edges:e['full_sharpe_cliff']=e['sharpe3_delta'] is not None and abs(e['sharpe3_delta'])>cut;e['cliff_threshold']=cut
 for H in BTC_HURDLES:
  subset=[c for c in grid.values() if c['BTC_return_hurdle']==H];fig,axs=plt.subplots(3,2,figsize=(12,10),layout='constrained')
  for i,field in enumerate(['net_return_pct','sharpe_365','max_drawdown_pct']):
   vv=[(c['scenes']['3']['recent40'] if rr else c['scenes']['3'])[field] for c in subset for rr in [False,True]];limit=max([abs(x) for x in vv if x is not None] or [1]) or 1
   for j,rr in enumerate([False,True]):
    mat=np.asarray([[(by[H,S,L]['scenes']['3']['recent40'] if rr else by[H,S,L]['scenes']['3'])[field] for L in LOOKS] for S in SLOWS],dtype=float);im=axs[i,j].imshow(mat,aspect='auto',cmap='RdYlGn_r' if field=='max_drawdown_pct' else 'RdYlGn',vmin=0 if field=='max_drawdown_pct' else -limit,vmax=limit);axs[i,j].set_title(('Inherited40days' if rr else '370days')+' /3x '+field);axs[i,j].set_xticks(range(len(LOOKS)),LOOKS);axs[i,j].set_yticks(range(len(SLOWS)),SLOWS);axs[i,j].set_xlabel('ETH reversal L(days)');axs[i,j].set_ylabel('ETH slow S(days)')
    for y,x in itertools.product(range(len(SLOWS)),range(len(LOOKS))):axs[i,j].text(x,y,('n/a' if np.isnan(mat[y,x]) else f'{mat[y,x]:+.3f}')+('*' if by[H,SLOWS[y],LOOKS[x]].get('read_only_anchor') else ''),ha='center',va='center',fontsize=10)
    fig.colorbar(im,ax=axs[i,j])
  fig.suptitle(f'BTC31/H{int(H*100)}%/E1% + ETH H2%/zeroexit; N1000/3000\ntwo10000banks,parent20000 raw1/1; *oldactualcell;knownhistory');fig.savefig(R/f'sensitivity_BH{int(H*100):02d}.png',dpi=120);plt.close(fig)
 counts={'cost':len(rows),'full_folds':len(folds),'recent40_folds':len(recent),'daily_NAV':len(daily),'edges':len(edges),'reference_comparisons':len(comp)};assert list(counts.values())==[111,1443,888,22260,75,120]
 for name,data,zipit in [('sensitivity.csv',rows,False),('fold_results.csv',folds,False),('recent40_fold_results.csv',recent,False),('daily_equity.csv.gz',daily,True),('joint_edges.csv',edges,False),('reference_comparisons.csv',comp,False)]:table(name,data,zipit)
 r['joint_grid_sensitivity']={'dimension_count':3,'parent_cells':36,'new_cells':20,'readonly_old_cells':16,'old_hold_controls':1,'adjacent_edges':75,'cells':cells,'old_qualification_unchanged':True,'cliff_definition':'DescriptiveabsSharpeadjacentdelta>2populationSDoffiniteabsdeltas,nooldrerating'};put(R/'report.json',r);cs=list(r['configs'].values());summary={'new_financial_configs':20,'new_native_components':0,'new_passive_parents':20,'passed_candidates':len(r['summary']['passed']),'rejected_candidates':len(r['summary']['rejected']),'positive_configs_by_cost':r['summary']['positive_configs_by_cost'],'failed_criteria_counts':dict(Counter(k for c in cs for k in c['failed_criteria'])),'best_full3':max(({'name':c['name'],'return3_pct':c['scenes']['3']['net_return_pct'],'whole_DD3_pct':c['scenes']['3']['max_drawdown_pct'],'recent_return3_pct':c['scenes']['3']['recent40']['net_return_pct'],'positive_months1':c['positive_complete_30d_folds_1x'],'positive_recent1':c['recent40_positive_5d_folds_1x'],'failed_criteria':c['failed_criteria']} for c in cs),key=lambda x:x['return3_pct']),'rows':counts};put(R/'summary.json',summary)
 ctx=json.loads((R/'context.json').read_text());lines=[f'# {R.name} BTC确认阈值与ETH过滤/反转周期组合验证',f'实际计算20个新组合/60成本场景，历史通过{summary["passed_candidates"]}、淘汰{summary["rejected_candidates"]}。完整读取{ctx["registry_events"]}事件/{ctx["registry_ids"]}ID、{len(ctx["prior_conclusions_read"])}份结论，初始16项均有真实历史证据。',
 '事前预设BTC ROC31入场2/4/6%、退出1% × ETH慢28/29/30/31日 × 反转3/4/5日，ETH入场2%、零交叉退出。三维36格：16旧结果只读、20缺失组件对各自先reserve再计算，75相邻边。15旧原生/45成本NAV完整恢复并核对原SHA，不重新执行原生信号/撮合/费用/资金费模型；名称、顺序、数字格式或策略族不制造新颖性。固定原生预算BTC1000/ETH3000，不线性缩放其他金额结果。',
 '原值1/1代表两个完整10000USDT独立银行，父本金20000，入场预算合计4000=初始本金20%；不是目标权重或恒定风险比例，不归一化、不复利调仓、不转账/跨银行保证金/再平衡。每档按共同(ns,eventcode)时轴承接上一完成源净值并逐点相加，重新计算整体收益/Sharpe/Calmar/回撤，不平均单策略指标。逐项与同ETH/金额的旧BTC_H4组合及同金额恒多、解析现金0对照。',
 'BTC此前完整31日ROC严格>H多/<-H空，带内多仅ROC>-1%、空仅ROC<1%保持；反向完整极端先平再反开。ETH此前完整L日ROC严格>2%反转空/<-2%反转多，带内多仅ROC<0、空仅ROC>0保留，零退出；慢S日ROC正仅许多、负仅许空，零/不兼容平实际仓位，现金重入须新极端，无隐藏desired。00:01真实OPEN执行，q=floor(N/此前完整close/lot)，不使用未来OPEN/未闭合价格/资金费产生信号或手数。全部组件规则与实际账本保持，本轮无新父层成交。',
 '8真实合并Parquet＋16年度/近期源SHA/字节固定。370日连续OOS2025-10-19UTC00:01至2026-10-24UTC00:01，33日上下文/3日初始embargo，静态规则无拟合/未来标签，purge不适用。12完整30日折＋10日尾折连续carry原现金/数量/entry/费用，近期40日从day330继承状态并分8×5日，不重开本金或诊断平仓，只有原预定终点计费平仓。该历史反复研究，只属开发验证，不称最终未触碰测试集。',
 '原生每侧5bp手续费＋1bp半价差＋2bp滑点＋0.5×此前20日日log波动×sqrt(金额/此前20日ADV)冲击，参与率≤0.1%；真实不利tick/lot/最小金额、100%抵押入场约束。实际资金费=-q×结算mark×rate，流出乘1/2/3、收入不放大，永续无虚构现货借币。原每档成本/资金费/交易数/占本金比例直接继承并核对相加，不新增重平衡成本。缺L2/TCA/历史完整阶梯，1%维持保证金＋闭合小时不利mark仅代理，不保证容量或tick清算安全。',
 '预设门槛保持：全期/近期三档净正，1倍完整月正折≥9/12、近期≥6/8，3倍完整连续OOS最大DD≤25%，三维排序相邻索引半径1含自身邻域净正≥60%，≥4往返、(参考毛利＋资金费)/执行费用≥2.5，现金/拒单/各银行风险代理违规0、终点空仓且≥180日。16旧资格不按新邻域重评级。三图18面板、111成本行、1443全期折、888近期折、22260新日边界、75相邻边和120匹配对照保存。',
 '结果：'+json.dumps(summary,ensure_ascii=False),
 '原冻结H4/ETH28L3候选与旧SMA按完整账本续接16:30至18:30，不重复08和16资金费；保留16小时内资金费前后风险状态以核验17:00完整小时。两者是延迟闭合行情重建，不是paper10实时报价执行。paper10账户/冻结规则只读，不为新历史组合改原前向计划，不强制窗口截止平仓。',
 '一手背景复用此前2026-10-27实际访问的[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)（2012-05-01）与[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)（2012-12-05）。本加密规则与组合推论非论文复现或利润/容量移植。20个相关新组合及所有既往试验存在多重选择偏差，无DSR/PBO、独立未来资格或稳定实盘盈利证明。',
 '复现工作目录/home/desktop/Documents/Codex/EquiTide；audit.py独立回放已保存实际事件、核验共同纳秒时轴和每个组合净值/指标；check_sources.py、audit_candidate.py、audit_forward.py及forward.py --reproduce只读真实证据，不重复reserve/evaluate/summarize完成项。main普通非强推、完整远端tree/blob/行情SHA验证后释放自己锁。'];(R/'result.md').write_text('\n\n'.join(lines)+'\n');print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
