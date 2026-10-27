"""Export all five-dimensional budget cells, folds, costs, controls and sensitivity surfaces."""
import copy,csv,gzip,io,itertools,json,statistics
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run import ROOT,R,NOTIONALS,SLOWS,LOOKS,HURDLES,EXITS,axes,grid_configs,sha,put

def table(path,rows,compressed=False):
 fields=list(dict.fromkeys(k for r in rows for k in r));b=io.StringIO(newline='');w=csv.DictWriter(b,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows);path.write_bytes(gzip.compress(b.getvalue().encode(),mtime=0) if compressed else b.getvalue().encode())
def main():
 assert not(R/'finish.json').exists();report=json.loads((R/'report.json').read_text());grid=grid_configs(report['configs']);assert len(grid)==162;holds={};docs={}
 for key,ref in json.loads((R/'holds.json').read_text()).items():
  assert sha(ROOT/ref['report'])==ref['report_sha256']
  if ref['report'] not in docs:docs[ref['report']]=json.loads((ROOT/ref['report']).read_text())
  c=copy.deepcopy(docs[ref['report']]['configs'][ref['name']]);c.update(read_only_anchor=True,scope='parent',asset='COMBO',capital_usdt=20000);holds[key]=c
 for c in report['configs'].values():
  if c['role']=='benchmark':holds[f'B{c["BTC_fixed_entry_notional_usdt"]}_E{c["ETH_fixed_entry_notional_usdt"]}']=c
 assert len(holds)==9;allcells={**grid,**{c['name']:c for c in holds.values()}};rows=[];folds=[];recent=[];daily=[];comp=[];edges=[];cells={}
 for c in allcells.values():
  old=c.get('read_only_anchor',False);meta={'name':c['name'],'role':c['role'],'scope':'parent','asset':'COMBO','read_only_anchor':old,'capital_usdt':20000,'BTC_fixed_entry_notional_usdt':c['BTC_fixed_entry_notional_usdt'],'ETH_fixed_entry_notional_usdt':c['ETH_fixed_entry_notional_usdt'],'total_entry_budget_usdt':c['BTC_fixed_entry_notional_usdt']+c['ETH_fixed_entry_notional_usdt'],**({p:c[p] for p in axes(c) if p not in ['BTC_fixed_entry_notional_usdt','ETH_fixed_entry_notional_usdt']} if c['role']=='candidate' else {})}
  cells[c['name']]={**meta,'fingerprint':c['fingerprint'],'original_or_new_status':c['status'],'positive_complete30d_folds1':c['positive_complete_30d_folds_1x'],'positive_recent5d_folds1':c['recent40_positive_5d_folds_1x'],'scenes':{k:{p:z[p] for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','NAV_sha256_f64le']} for k,z in c['scenes'].items()}}
  for k,z in c['scenes'].items():
   rows.append({**meta,'cost_multiplier':int(k),'status':c['status'],**{p:z[p] for p in ['net_return_pct','max_drawdown_pct','daily_mark_drawdown_pct','sharpe_365','calmar','cost_usdt','funding_usdt','gross_reference_PnL_to_execution_cost','executions','round_trips','NAV_sha256_f64le']},**{'recent40_'+p:z['recent40'][p] for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','NAV_sha256_f64le']},**{'cost_'+p:v for p,v in z['cost_parts_usdt'].items()}});folds.extend({**meta,'cost_multiplier':int(k),**f} for f in z['folds']);recent.extend({**meta,'cost_multiplier':int(k),**f} for f in z['recent40']['folds'])
   if old:continue
   daily.extend({**meta,'cost_multiplier':int(k),'boundary_index':j,'equity_usdt':v} for j,v in enumerate(z['daily_equity_usdt']))
   if c['role']!='candidate':continue
   hold=holds[f'B{c["BTC_fixed_entry_notional_usdt"]}_E{c["ETH_fixed_entry_notional_usdt"]}']
   for kind,y in [('same_budget_BTCexit1_old',grid[c['matched_exit1_reference']]),('same_budget_constant_long',hold)]:
    a=y['scenes'][k];comp.append({**meta,'cost_multiplier':int(k),'reference_kind':kind,'reference_name':y['name'],'reference_fingerprint':y['fingerprint'],'reference_original_status':y['status'],'new_return_pct':z['net_return_pct'],'reference_return_pct':a['net_return_pct'],'return_delta_pp':z['net_return_pct']-a['net_return_pct'],'DD_delta_pp':z['max_drawdown_pct']-a['max_drawdown_pct'],'recent40_return_delta_pp':z['recent40']['net_return_pct']-a['recent40']['net_return_pct'],'execution_count_delta':z['executions']-a['executions'],'cost_delta_usdt':z['cost_usdt']-a['cost_usdt'],'new_NAV_sha256':z['NAV_sha256_f64le'],'reference_NAV_sha256':a['NAV_sha256_f64le'],'cash_analytic_return_pct':0,'comparison_limit':'SameNB/NEandcapital,differentBTCexit/timeinmarket;not independentequalriskalpha' if kind=='same_budget_BTCexit1_old' else 'sameNandcapital independentconstantlongbooks'})
 dims=axes(next(iter(grid.values())));fields=list(dims);by={tuple(c[p] for p in fields):c for c in grid.values()};assert set(by)==set(itertools.product(*dims.values()))
 for key,c in by.items():
  for i,(field,axis) in enumerate(dims.items()):
   j=axis.index(key[i])
   if j+1==len(axis):continue
   other=list(key);other[i]=axis[j+1];y=by[tuple(other)];a,b=c['scenes']['3'],y['scenes']['3'];edges.append({'axis':field,'from':c['name'],'to':y['name'],'return3_delta_pp':b['net_return_pct']-a['net_return_pct'],'DD3_delta_pp':b['max_drawdown_pct']-a['max_drawdown_pct'],'sharpe3_delta':b['sharpe_365']-a['sharpe_365'] if a['sharpe_365'] is not None and b['sharpe_365'] is not None else None,'recent40_return3_delta_pp':b['recent40']['net_return_pct']-a['recent40']['net_return_pct'],'recent40_sharpe3_delta':b['recent40']['sharpe_365']-a['recent40']['sharpe_365'] if a['recent40']['sharpe_365'] is not None and b['recent40']['sharpe_365'] is not None else None})
 for field,flag in [('sharpe3_delta','full_sharpe_cliff'),('recent40_sharpe3_delta','recent40_sharpe_cliff')]:
  vals=[abs(e[field]) for e in edges if e[field] is not None];cut=2*statistics.pstdev(vals) if vals else None
  for e in edges:e[flag]=e[field] is not None and abs(e[field])>cut;e[flag+'_threshold_abs_delta']=cut
 limits={rr:max(abs((c['scenes']['3']['recent40'] if rr else c['scenes']['3'])['net_return_pct']) for c in grid.values()) or 1 for rr in [False,True]}
 for S,X in itertools.product(SLOWS,EXITS):
  fig,axs=plt.subplots(3,2,figsize=(11,12),layout='constrained')
  for i,H in enumerate(HURDLES):
   for j,rr in enumerate([False,True]):
    mat=np.array([[(by[B,E,S,H,X]['scenes']['3']['recent40'] if rr else by[B,E,S,H,X]['scenes']['3'])['net_return_pct'] for B in NOTIONALS] for E in NOTIONALS]);im=axs[i,j].imshow(mat,cmap='RdYlGn',vmin=-limits[rr],vmax=limits[rr]);axs[i,j].set_title(f'ETH H{H*100:g}% / '+('Inherited40days' if rr else '370days'));axs[i,j].set_xticks(range(3),NOTIONALS);axs[i,j].set_yticks(range(3),NOTIONALS);axs[i,j].set_xlabel('BTC fixed entry N (USDT)');axs[i,j].set_ylabel('ETH fixed entry N (USDT)')
    for x,y in itertools.product(range(3),range(3)):axs[i,j].text(y,x,f'{mat[x,y]:+.3f}%'+('*' if by[NOTIONALS[y],NOTIONALS[x],S,H,X].get('read_only_anchor',False) else ''),ha='center',va='center',fontsize=10)
    fig.colorbar(im,ax=axs[i,j],label='3x net return (%)')
  fig.suptitle(f'ETH slow{S} / fast3days | BTC H2% exit{X*100:g}% | two10,000 banks raw1/1\n* Old actual cells; unstarred are new; known history');fig.savefig(R/f'sensitivity_S{S}_BX{int(X*1000):03d}.png',dpi=120);plt.close(fig)
 counts={'cost':len(rows),'full_folds':len(folds),'recent40_folds':len(recent),'daily_NAV':len(daily),'edges':len(edges),'reference_comparisons':len(comp)};assert list(counts.values())==[513,6669,4104,120204,513,648]
 for name,data,gz in [('sensitivity.csv',rows,False),('fold_results.csv',folds,False),('recent40_fold_results.csv',recent,False),('daily_equity.csv.gz',daily,True),('joint_edges.csv',edges,False),('reference_comparisons.csv',comp,False)]:table(R/name,data,gz)
 report['joint_grid_sensitivity']={'dimension_count':5,'axes':dims,'candidate_cells':162,'new_cells':108,'readonly_old_cells':54,'matched_hold_cells':9,'adjacent_edges':513,'cells':cells,'cliff_definition':'abs adjacentSharpe delta >2*populationSDof finiteabsadjacentdelta;descriptiveonly,no oldqualificationrewrite.'};put(R/'report.json',report)
 def brief(c):return {'name':c['name'],'full_return3_pct':c['scenes']['3']['net_return_pct'],'whole_DD3_pct':c['scenes']['3']['max_drawdown_pct'],'recent_return3_pct':c['scenes']['3']['recent40']['net_return_pct'],'recent_DD3_pct':c['scenes']['3']['recent40']['max_drawdown_pct'],'positive_complete30d_folds1':c['positive_complete_30d_folds_1x'],'positive_recent5d_folds1':c['recent40_positive_5d_folds_1x'],'status':c['status'],'failed_criteria':c['failed_criteria']}
 cs=[c for c in report['configs'].values() if c['role']=='candidate'];summary={'new_financial_configs':108,'new_candidate_configs':108,'new_benchmark_configs':0,'new_native_backtests':0,'new_passive_parents':108,'readonly_native_components':27,'readonly_old_parent_cells':54,'readonly_matched_holds':9,'full_grid_cells':162,'passed_candidates':len(report['summary']['passed']),'rejected_candidates':len(report['summary']['rejected']),'positive_configs_by_cost':report['summary']['positive_configs_by_cost'],'recent_positive_configs_by_cost':{k:sum(c['scenes'][k]['recent40']['net_return_pct']>0 for c in cs) for k in ['1','2','3']},'failed_criteria_counts':dict(Counter(p for c in cs for p in c['failed_criteria'])),'best_full':brief(max(cs,key=lambda c:c['scenes']['3']['net_return_pct'])),'best_recent':brief(max(cs,key=lambda c:c['scenes']['3']['recent40']['net_return_pct'])),'rows':counts,'by_budget':{}}
 for B,E in itertools.product(NOTIONALS,NOTIONALS):
  z=[c for c in cs if c['BTC_fixed_entry_notional_usdt']==B and c['ETH_fixed_entry_notional_usdt']==E]
  if z:summary['by_budget'][f'B{B}_E{E}']={'configs':len(z),'total_entry_budget_usdt':B+E,'entry_fraction_of_initial_parent':(B+E)/20000,'passed':sum(c['status']=='passed' for c in z),'positive3':sum(c['scenes']['3']['net_return_pct']>0 for c in z),'recent_positive3':sum(c['scenes']['3']['recent40']['net_return_pct']>0 for c in z),'full3_range_pct':[min(c['scenes']['3']['net_return_pct'] for c in z),max(c['scenes']['3']['net_return_pct'] for c in z)]}
 put(R/'summary.json',summary);ctx=json.loads((R/'context.json').read_text());lines=[f'# {R.name} BTC退出缓冲与独立预算交互验证',f'实际计算108新候选组合/324成本场景：{summary["passed_candidates"]}历史通过、{summary["rejected_candidates"]}淘汰。逐项先成功reserve才计算，正负结果全部保存。全文读取{ctx["registry_events"]}事件/{ctx["registry_ids"]}ID、{len(ctx["prior_conclusions_read"])}份结论；初始16均已有真实历史证据。',
 '上一轮独立预算在BTC退出1%下未修复近期正折不足。本轮事前固定BTC退出0.5/1/2%，联合BTC_N、ETH_N各1000/2000/3000、ETH慢周期28/31和入场阈值2/4/6%；ETH短反转回看固定3日，BTC仍ROC31日/H2%。完整NB×NE×S×ETH_H×BTC_exit五维162格，54旧只读＋108缺格、513相邻边；9同预算恒多均旧控制。仅改名称、顺序或等价数值不算新配置，按完整源组件对、原1/1和区间语义查重，不重跑旧原生模型。',
 '原值1/1为两个各10000USDT独立银行，父本金始终20000；N是新入场固定名义预算，合计2000到6000占初始父本金10%到30%，不是资金权重，不归一化、不复利调仓、不转账/交叉保证金/再平衡。直接使用实际N和BTC退出对应的完整cash/q/entry/费用/资金费/风险路径，不线性缩放NAV；新退出改变持仓时间和真实敞口，同预算并不等于等实现风险。',
 'BTC此前完整31日ROC严格>2%多/<-2%空；带内多仅ROC>-E、空仅ROC<E保持，相反完整极端先平再反开，E=0.5/1/2%。ETH此前完整3日ROC>H反转空/<-H反转多，带内多仅ROC<0/空仅ROC>0保留，过零退出；慢ROC28/31日正仅许多、负仅许空、零空仓，不兼容平实际仓位，现金重入须新极端，无隐藏desired。UTC00:01OPEN执行，q=floor(N/此前完整close/lot)，信号和手数不用未来OPEN/资金费；00:00或毫秒偏移资金费先计旧仓。',
 '27旧原生（BTC9个N×退出、ETH18个N×慢周期×阈值）/81成本NAV只读从真实状态分段恢复并核对原SHA，不重跑旧信号/撮合/费用/资金费模型。共同(ns,eventcode)轴缺点仅承接上一已完成源NAV，保留前后顺序，无插值/归一化；两绝对NAV逐点相加重算整体指标，不平均Sharpe/收益。新项与同预算BTC退出1%旧组合、同预算恒多和现金0逐档比较。',
 '真实8合并Parquet＋16年度/近期源文件路径/字节/SHA固定，连续OOS2025-10-19UTC00:01至2026-10-24UTC00:01共370日；33日先验上下文、3日初始embargo，无拟合/未来标签，purge不适用。12完整30日折＋10日尾折carry原cash/q/entry/成本，近期40日从Sep14继承第330日决策前状态并分8×5日，不重开本金或诊断平仓。历史已反复研究，只作开发验证，不称未触碰最终测试或独立新数据。',
 '继承真实1/2/3倍成本路径：每侧5bp手续费＋1bp半价差＋2bp滑点；冲击0.5×此前20日日log波动×sqrt(金额/此前20日ADV)，参与率≤0.1%；真实不利tick/lot/最小金额、100%抵押入场上限。资金费=-q×结算mark×真实rate，流出乘k、收入不放大；永续空头无虚构现货借币。缺L2/队列/TCA/完整历史margin阶梯，闭合小时不利mark＋1%维持保证金和分钟/小时/结算NAV仅代理，不是tick级清算或容量保证。',
 '预定资格：三档全期/近期净正，1x完整月至少9/12正、近期至少6/8正；3x整体DD≤25%，5D相邻索引含自身邻域净正≥60%，1x≥4往返、(参考毛利＋资金费)/执行成本≥2.5、现金/拒单/各银行风险代理违规0、终点空仓。旧54资格和原候选不按新邻域重评级。退出轴0.5/1/2%的间隔不等，邻域按预定排序索引，不解释为等距离。',
 '三项验证实际执行：13全期折、8近期折和连续完整NAV回撤；5D162格净收益/Sharpe/Calmar/陡变/边界与6图36面板；324新成本场景。含9旧恒多共171展示格、513成本行、6669全期折、4104近期折、120204新日边界、513邻接边、648逐成本对照。',
 '结果：'+json.dumps(summary,ensure_ascii=False),
 '原BTC31/H4/E1 N1000＋ETH S28/L3/H2 N3000前瞻规则保持冻结。本轮只续接已有真实账户cash/q/entry/费用/资金费/小时风险段/完整NAV链，不随新历史参数结果切换；未成熟部分观察rejected不取消原180日计划。旧SMA仅从Oct27UTC00:30续接02:30闭合分钟mark，下一日决策Oct28UTC00:01，不强制平仓。两者都是延迟闭合行情重建，不是paper10实时报价账户或真实下单。实际数字和独立核验另见本轮candidate_verification/forward_verification。paper10全部冻结账本只读。',
 '一手背景：[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)（2012-05-01）、[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)（2012-12-05），访问2026-10-27。传统期货趋势/股票费用仅作背景，加密退出和预算交互为推论，不是论文复现或利润/容量移植。108相关试验受多重选择偏差影响，无DSR/PBO校正或稳定实盘盈利证明。',
 '复现目录/home/desktop/Documents/Codex/EquiTide；audit.py、check_sources.py、check_definitions.py、check_alignment.py及forward.py --reproduce/audit_forward.py只读已保存证据，不重新reserve/evaluate/summarize精确已完成配置。保留完整结果/账户账本/冻结规则/登记/失败/复现代码，仅清可重建缓存。只在main和同一branch.lock下提交非强推，经freshfetch/独立全heads/完整tree和必要blob/data/report核验后释放自己锁；不建分支/定时任务、重部署网页或真实下单。'];(R/'result.md').write_text('\n\n'.join(lines)+'\n');print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
