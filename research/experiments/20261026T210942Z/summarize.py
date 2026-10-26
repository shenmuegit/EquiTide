"""Export all five-dimensional budget cells, folds, costs, controls and sensitivity surfaces."""
import copy,csv,gzip,io,itertools,json,statistics
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run import ROOT,R,NOTIONALS,SLOWS,LOOKS,HURDLES,axes,grid_configs,sha,put

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
   for kind,y in [('same_ETH_total4000_old',grid[c['matched_total4000_reference']]),('same_budget_constant_long',hold)]:
    a=y['scenes'][k];comp.append({**meta,'cost_multiplier':int(k),'reference_kind':kind,'reference_name':y['name'],'reference_fingerprint':y['fingerprint'],'reference_original_status':y['status'],'new_return_pct':z['net_return_pct'],'reference_return_pct':a['net_return_pct'],'return_delta_pp':z['net_return_pct']-a['net_return_pct'],'DD_delta_pp':z['max_drawdown_pct']-a['max_drawdown_pct'],'recent40_return_delta_pp':z['recent40']['net_return_pct']-a['recent40']['net_return_pct'],'execution_count_delta':z['executions']-a['executions'],'cost_delta_usdt':z['cost_usdt']-a['cost_usdt'],'new_NAV_sha256':z['NAV_sha256_f64le'],'reference_NAV_sha256':a['NAV_sha256_f64le'],'cash_analytic_return_pct':0,'comparison_limit':'same_ETH_total4000 changesBTCbudget/risk;not alpha at equal exposure' if kind=='same_ETH_total4000_old' else 'sameNandcapital independentconstantlongbooks'})
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
 for S,L in itertools.product(SLOWS,LOOKS):
  fig,axs=plt.subplots(3,2,figsize=(11,12),layout='constrained')
  for i,H in enumerate(HURDLES):
   for j,rr in enumerate([False,True]):
    mat=np.array([[(by[B,E,S,L,H]['scenes']['3']['recent40'] if rr else by[B,E,S,L,H]['scenes']['3'])['net_return_pct'] for B in NOTIONALS] for E in NOTIONALS]);im=axs[i,j].imshow(mat,cmap='RdYlGn',vmin=-limits[rr],vmax=limits[rr]);axs[i,j].set_title(f'ETH H{H*100:g}% / '+('Inherited40days' if rr else '370days'));axs[i,j].set_xticks(range(3),NOTIONALS);axs[i,j].set_yticks(range(3),NOTIONALS);axs[i,j].set_xlabel('BTC fixed entry N (USDT)');axs[i,j].set_ylabel('ETH fixed entry N (USDT)')
    for x,y in itertools.product(range(3),range(3)):axs[i,j].text(y,x,f'{mat[x,y]:+.3f}%'+('*' if NOTIONALS[x]+NOTIONALS[y]==4000 else ''),ha='center',va='center',fontsize=10)
    fig.colorbar(im,ax=axs[i,j],label='3x net return (%)')
  fig.suptitle(f'ETH slow{S}days / reversal{L}days | two10,000 banks raw1/1\n* Old total4000 cells; other budgets new; known history');fig.savefig(R/f'sensitivity_S{S}_L{L}.png',dpi=120);plt.close(fig)
 counts={'cost':len(rows),'full_folds':len(folds),'recent40_folds':len(recent),'daily_NAV':len(daily),'edges':len(edges),'reference_comparisons':len(comp)};assert list(counts.values())==[513,6669,4104,126882,513,648]
 for name,data,gz in [('sensitivity.csv',rows,False),('fold_results.csv',folds,False),('recent40_fold_results.csv',recent,False),('daily_equity.csv.gz',daily,True),('joint_edges.csv',edges,False),('reference_comparisons.csv',comp,False)]:table(R/name,data,gz)
 report['joint_grid_sensitivity']={'dimension_count':5,'axes':dims,'candidate_cells':162,'new_cells':108,'readonly_old_cells':54,'matched_hold_cells':9,'adjacent_edges':513,'cells':cells,'cliff_definition':'abs adjacentSharpe delta >2*populationSDof finiteabsadjacentdelta;descriptiveonly,no oldqualificationrewrite.'};put(R/'report.json',report)
 def brief(c):return {'name':c['name'],'full_return3_pct':c['scenes']['3']['net_return_pct'],'whole_DD3_pct':c['scenes']['3']['max_drawdown_pct'],'recent_return3_pct':c['scenes']['3']['recent40']['net_return_pct'],'recent_DD3_pct':c['scenes']['3']['recent40']['max_drawdown_pct'],'positive_complete30d_folds1':c['positive_complete_30d_folds_1x'],'positive_recent5d_folds1':c['recent40_positive_5d_folds_1x'],'status':c['status'],'failed_criteria':c['failed_criteria']}
 cs=[c for c in report['configs'].values() if c['role']=='candidate'];summary={'new_financial_configs':114,'new_candidate_configs':108,'new_benchmark_configs':6,'new_native_backtests':0,'new_passive_parents':114,'readonly_native_components':63,'readonly_old_parent_cells':54,'readonly_matched_holds':3,'full_grid_cells':162,'passed_candidates':len(report['summary']['passed']),'rejected_candidates':len(report['summary']['rejected']),'positive_configs_by_cost':report['summary']['positive_configs_by_cost'],'recent_positive_configs_by_cost':{k:sum(c['scenes'][k]['recent40']['net_return_pct']>0 for c in cs) for k in ['1','2','3']},'failed_criteria_counts':dict(Counter(p for c in cs for p in c['failed_criteria'])),'best_full':brief(max(cs,key=lambda c:c['scenes']['3']['net_return_pct'])),'best_recent':brief(max(cs,key=lambda c:c['scenes']['3']['recent40']['net_return_pct'])),'rows':counts,'by_budget':{}}
 for B,E in itertools.product(NOTIONALS,NOTIONALS):
  z=[c for c in cs if c['BTC_fixed_entry_notional_usdt']==B and c['ETH_fixed_entry_notional_usdt']==E]
  if z:summary['by_budget'][f'B{B}_E{E}']={'configs':len(z),'total_entry_budget_usdt':B+E,'entry_fraction_of_initial_parent':(B+E)/20000,'passed':sum(c['status']=='passed' for c in z),'positive3':sum(c['scenes']['3']['net_return_pct']>0 for c in z),'recent_positive3':sum(c['scenes']['3']['recent40']['net_return_pct']>0 for c in z),'full3_range_pct':[min(c['scenes']['3']['net_return_pct'] for c in z),max(c['scenes']['3']['net_return_pct'] for c in z)]}
 put(R/'summary.json',summary);ctx=json.loads((R/'context.json').read_text());lines=[f'# {R.name} BTC/ETH独立入场预算五维验证',f'真实评估108新候选组合＋6同预算恒多对照=114配置/342成本场景；{summary["passed_candidates"]}候选历史通过、{summary["rejected_candidates"]}淘汰。6对照按reference_only不参加alpha资格，实际结果均rejected留档，绝非无结果。逐项在实际计算前reserve，所有正负收益保留。全文读取{ctx["registry_events"]}事件/{ctx["registry_ids"]}ID、{len(ctx["prior_conclusions_read"])}份旧结论，初始16均有真实历史证据。',
 '本轮事先固定BTC_N与ETH_N各1000/2000/3000独立变化；BTC仍ROC31日/H4%/退出1%，ETH门控S28/31、反转L1/2/3、H2/4/6%。此前仅总入场4000的3种预算，现补另6种预算×18信号组合=108新项。完整5D候选网格162格/513邻接边，54原始格只读且原资格不改；完整同预算恒多9格，3旧＋6新。没有因一族已测而排除不同预算或先看新组合收益再选批次。',
 '权重原值1/1代表两个各10000 USDT独立银行，父本金始终20000。N为新入场固定名义金额，不是本金权重，NB+NE从2000到6000即初始父本金10%到30%；真实lot取整/开盘跳空可能改变实际敞口。每个N使用其原生实际cash/q/entry/成本/资金费路径，不线性缩放NAV、不复利调仓、不转账/交叉保证金/再平衡。提高总预算会提高风险，较高收益不称等风险alpha。',
 '只恢复63个既有原生完整账本（57信号组件＋6恒多）/189成本NAV，并逐条核对原SHA；没有重跑旧信号、模拟撮合、费用或资金费模型。所有新父在共同(ns,eventcode)时间轴逐点相加两绝对NAV，缺失键仅承接上一已完成源观察，无插值/归一化/平均Sharpe。每个源的真实费用/资金费计一次，父无额外交易。',
 '真实8合并Parquet与16年度/近期源路径、字节和SHA固定；连续OOS2025-10-19UTC00:01到2026-10-24UTC00:01共370日，33日先验上下文、3日初始embargo，无拟合/未来标签，purge不适用。12完整30日折＋10日尾折连续carry，近期40日从Sep14继承第330日决策前状态并拆8×5日，禁止重开本金/诊断平仓。全部历史反复研究，只作开发验证，不是未触碰最终留出或独立新数据。',
 '成本继承真实源各1/2/3倍路径：每侧5bp手续费、1bp半价差、2bp滑点，冲击0.5×此前20日日log波动×sqrt(金额/此前20日ADV)，参与率≤0.1%；不利tick/lot/最小金额、1x抵押入场上限，真实-q×mark×rate资金费，流出乘k、流入不放大。永续空头无虚构现货借币；缺L2/队列/TCA/完整历史阶梯，闭合小时不利mark＋1%维持保证金仅代理，抽样NAV回撤不是tick清算保证。',
 '预定资格：三档全期/近期净正；完整月1x至少9/12正、近期1x至少6/8正；3x全曲线DD≤25%、五维相邻索引邻域3x净正≥60%、1x≥4往返、(参考毛利＋资金费)/执行成本≥2.5、现金/拒单/保证金代理违规0、终点空仓。原54格及原候选资格不按新5D邻域重评级。每个新候选与相同预算恒多、现金0及相同ETH但总4000旧组合逐档比较，后者风险/总敞口不同，不能称等风险改善。',
 '三项验证已实际执行：完整13折和近期8折、连续全曲线DD；五维完整网格、Sharpe/Calmar/相邻陡变/边界与六张36面板热图；342新成本场景。全部513成本行、6669全期折、4104近期折、126882新日边界、513相邻边、648对照行留档。',
 '结果：'+json.dumps(summary,ensure_ascii=False),
 '原BTC31/H4/E1 N1000＋ETH S28/L3/H2 N3000候选与2026-10-27UTC00:01起180日前瞻计划保持冻结；本轮只status检查未建账户、未登记未来窗口，不根据新预算结果替换。旧SMA按原现金/数量/desired/费用/NAV前缀续接UTC18:30到20:30，仅真实闭合mark，不是paper10实时报价模拟或新候选前向。paper10全账本与冻结参数只读。',
 '一手背景：[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)（2012-05-01）、[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)（2012-12-05），访问2026-10-26。传统期货趋势和股票费用研究只作背景，本文加密预算为推论，不是论文复现/容量移植。114相关实际试验受多重选择偏差影响，无DSR/PBO校正、独立最终留出或稳定实盘盈利证明。',
 '复现目录/home/desktop/Documents/Codex/EquiTide；audit.py、check_sources.py、check_definitions.py、check_alignment.py与forward.py --reproduce/audit_forward.py只读已保存证据，不重新reserve/evaluate/summarize精确已完成配置。保留全部账本、冻结规则、登记及失败日志；仅main、持branch.lock提交和非强推，经freshfetch/独立allheads/完整tree与必要blob/data/report核验后释放自己锁，不建分支/定时器/新网页部署或真实订单。'];(R/'result.md').write_text('\n\n'.join(lines)+'\n');print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
