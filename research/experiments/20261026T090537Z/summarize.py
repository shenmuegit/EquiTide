"""Full five-axis BTC-exit/budget surface, preserving all old qualifications."""
import csv,gzip,io,itertools,json,statistics
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run import ROOT,R,SLOWS,LOOKS,HURDLES,BUFFERS,NOTIONALS,axes,grid_configs,sha,put

def table(path,rows,compressed=False):
 fields=list(dict.fromkeys(k for r in rows for k in r));b=io.StringIO(newline='');w=csv.DictWriter(b,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows);raw=b.getvalue().encode();path.write_bytes(gzip.compress(raw,mtime=0) if compressed else raw)
def main():
 assert not (R/'finish.json').exists();report=json.loads((R/'report.json').read_text());grid=grid_configs(report['configs']);assert len(grid)==243;holds={}
 for key,href in json.loads((R/'holds.json').read_text()).items():
  assert sha(ROOT/href['report'])==href['report_sha256'];holds[key]=json.loads((ROOT/href['report']).read_text())['configs'][href['name']]
 rows=[];folds=[];recent=[];daily=[];comp=[];edges=[];cells={}
 for c in grid.values():
  old=c.get('read_only_anchor',False);meta={'name':c['name'],'read_only_anchor':old,'capital_usdt':20000,**{p:c[p] for p in axes(c)}};cells[c['name']]={**meta,'fingerprint':c['fingerprint'],'original_or_new_status':c['status'],'positive_complete30d_folds1':c['positive_complete_30d_folds_1x'],'positive_recent5d_folds1':c['recent40_positive_5d_folds_1x'],'original_or_new_sensitivity':c['sensitivity'],'scenes':{k:{p:z[p] for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','NAV_sha256_f64le']} for k,z in c['scenes'].items()},'recent40':{k:{p:z['recent40'][p] for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','NAV_sha256_f64le']} for k,z in c['scenes'].items()}}
  for k,z in c['scenes'].items():
   rows.append({**meta,'cost_multiplier':int(k),'status':c['status'],**{p:z[p] for p in ['net_return_pct','max_drawdown_pct','daily_mark_drawdown_pct','sharpe_365','calmar','cost_usdt','funding_usdt','gross_reference_PnL_to_execution_cost','executions','round_trips','NAV_sha256_f64le']},**{'recent40_'+p:z['recent40'][p] for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','NAV_sha256_f64le']},**{'cost_'+p:v for p,v in z['cost_parts_usdt'].items()}});folds.extend({**meta,'cost_multiplier':int(k),**f} for f in z['folds']);recent.extend({**meta,'cost_multiplier':int(k),**f} for f in z['recent40']['folds'])
   if old:continue
   daily.extend({**meta,'cost_multiplier':int(k),'boundary_index':j,'equity_usdt':v} for j,v in enumerate(z['daily_equity_usdt']))
   reference=grid[c['matched_old_exit1pct']];hold=holds['B'+str(c['BTC_fixed_entry_notional_usdt'])+'_E'+str(c['ETH_fixed_entry_notional_usdt'])]
   for kind,y in [('matched_old_exit1pct',reference),('matched_hold',hold)]:
    a=y['scenes'][k];comp.append({**meta,'cost_multiplier':int(k),'reference_kind':kind,'reference_name':y['name'],'reference_fingerprint':y['fingerprint'],'reference_original_status':y['status'],'new_return_pct':z['net_return_pct'],'reference_return_pct':a['net_return_pct'],'return_delta_pp':z['net_return_pct']-a['net_return_pct'],'DD_delta_pp':z['max_drawdown_pct']-a['max_drawdown_pct'],'recent40_return_delta_pp':z['recent40']['net_return_pct']-a['recent40']['net_return_pct'],'execution_count_delta':z['executions']-a['executions'],'cost_delta_usdt':z['cost_usdt']-a['cost_usdt'],'new_NAV_sha256':z['NAV_sha256_f64le'],'reference_NAV_sha256':a['NAV_sha256_f64le'],'cash_analytic_return_pct':0})
 dims=axes(next(iter(grid.values())));fields=list(dims);by={tuple(c[p] for p in fields):c for c in grid.values()};assert set(by)==set(itertools.product(*dims.values()))
 for key,c in by.items():
  for i,(field,axis) in enumerate(dims.items()):
   j=axis.index(key[i])
   if j+1==len(axis):continue
   other=list(key);other[i]=axis[j+1];y=by[tuple(other)];a,b=c['scenes']['3'],y['scenes']['3'];edges.append({'axis':field,'from':c['name'],'to':y['name'],'return3_delta_pp':b['net_return_pct']-a['net_return_pct'],'DD3_delta_pp':b['max_drawdown_pct']-a['max_drawdown_pct'],'sharpe3_delta':b['sharpe_365']-a['sharpe_365'] if a['sharpe_365'] is not None and b['sharpe_365'] is not None else None,'recent40_return3_delta_pp':b['recent40']['net_return_pct']-a['recent40']['net_return_pct'],'recent40_sharpe3_delta':b['recent40']['sharpe_365']-a['recent40']['sharpe_365'] if a['recent40']['sharpe_365'] is not None and b['recent40']['sharpe_365'] is not None else None})
 for field,flag in [('sharpe3_delta','full_sharpe_cliff'),('recent40_sharpe3_delta','recent40_sharpe_cliff')]:
  vals=[abs(e[field]) for e in edges if e[field] is not None];cut=2*statistics.pstdev(vals) if vals else None
  for e in edges:e[flag]=e[field] is not None and abs(e[field])>cut;e[flag+'_threshold_abs_delta']=cut
 counts={'cost':len(rows),'full_folds':len(folds),'recent40_folds':len(recent),'daily_NAV':len(daily),'edges':len(edges),'reference_comparisons':len(comp)};assert list(counts.values())==[729,9477,5832,120204,810,648]
 for path,data,gz in [('sensitivity.csv',rows,False),('fold_results.csv',folds,False),('recent40_fold_results.csv',recent,False),('daily_equity.csv.gz',daily,True),('joint_edges.csv',edges,False),('reference_comparisons.csv',comp,False)]:table(R/path,data,gz)
 report['joint_grid_sensitivity']={'cell_count':243,'new_cells':108,'readonly_old_parent_cells':135,'dimension_count':5,'axes':dims,'cells':cells,'adjacent_edges':810,'old_original_qualification_unchanged':True,'cliff_definition':'AbsadjacentSharpedelta>2*populationSDoffiniteabsadjacentSharpedeltasoverfull243grid;descriptiveonly,Nonepreserved,nopostresultgridexpansion.'};put(R/'report.json',report)
 limits={rr:max(abs((c['scenes']['3']['recent40'] if rr else c['scenes']['3'])['net_return_pct']) for c in grid.values()) or 1 for rr in [False,True]}
 for N,S in itertools.product(NOTIONALS,SLOWS):
  fig,axs=plt.subplots(3,2,figsize=(10,12),layout='constrained')
  for i,E in enumerate(BUFFERS):
   for j,rr in enumerate([False,True]):
    mat=np.array([[(by[N,S,L,H,E]['scenes']['3']['recent40'] if rr else by[N,S,L,H,E]['scenes']['3'])['net_return_pct'] for L in LOOKS] for H in HURDLES]);im=axs[i,j].imshow(mat,cmap='RdYlGn',vmin=-limits[rr],vmax=limits[rr]);old=N==2000 or E==.01;axs[i,j].set_title(f'ETH slow {S}d / BTC exit {E*100:g}%'+(' / old*' if old else '')+'\n'+('Inherited 40 days' if rr else '370 days'));axs[i,j].set_xticks(range(3),[str(x) for x in LOOKS]);axs[i,j].set_yticks(range(3),[f'{x*100:g}%' for x in HURDLES]);axs[i,j].set_xlabel('ETH fast reversal lookback (days)');axs[i,j].set_ylabel('ETH reversal entry hurdle')
    for a,b in itertools.product(range(3),range(3)):axs[i,j].text(b,a,f'{mat[a,b]:+.3f}%'+('*' if old else ''),ha='center',va='center',fontsize=9)
    fig.colorbar(im,ax=axs[i,j],label='3x net return (%)')
  fig.suptitle(f'BTC trend N{4000-N} + ETH gate N{N} | banks 20,000 | raw 1/1 | known history');fig.savefig(R/f'sensitivity_N{N}_S{S}.png',dpi=120);plt.close(fig)
 def brief(c):return {'name':c['name'],'full_return3_pct':c['scenes']['3']['net_return_pct'],'whole_DD3_pct':c['scenes']['3']['max_drawdown_pct'],'recent_return3_pct':c['scenes']['3']['recent40']['net_return_pct'],'recent_DD3_pct':c['scenes']['3']['recent40']['max_drawdown_pct'],'positive_complete30d_folds1':c['positive_complete_30d_folds_1x'],'positive_recent5d_folds1':c['recent40_positive_5d_folds_1x'],'status':c['status'],'failed_criteria':c['failed_criteria']}
 cs=list(report['configs'].values());summ={'new_financial_configs':108,'new_native_backtests':0,'new_passive_parents':108,'readonly_native_components':90,'readonly_parent_cells':135,'readonly_matched_holds':3,'full_grid_cells':243,'passed_candidates':len(report['summary']['passed']),'rejected_candidates':len(report['summary']['rejected']),'positive_configs_by_cost':report['summary']['positive_configs_by_cost'],'recent_positive_configs_by_cost':{k:sum(c['scenes'][k]['recent40']['net_return_pct']>0 for c in cs) for k in ['1','2','3']},'failed_criteria_counts':dict(Counter(p for c in cs for p in c['failed_criteria'])),'best_full':brief(max(cs,key=lambda c:c['scenes']['3']['net_return_pct'])),'best_recent':brief(max(cs,key=lambda c:c['scenes']['3']['recent40']['net_return_pct'])),'rows':counts,'groups':{}}
 for N in [1000,3000]:
  group=[c for c in cs if c['ETH_fixed_entry_notional_usdt']==N];summ['groups'][f'ETH_N{N}']={'configs':len(group),'passed':sum(c['status']=='passed' for c in group),'full_positive3':sum(c['scenes']['3']['net_return_pct']>0 for c in group),'recent_positive3':sum(c['scenes']['3']['recent40']['net_return_pct']>0 for c in group),'full3_range_pct':[min(c['scenes']['3']['net_return_pct'] for c in group),max(c['scenes']['3']['net_return_pct'] for c in group)],'recent3_range_pct':[min(c['scenes']['3']['recent40']['net_return_pct'] for c in group),max(c['scenes']['3']['recent40']['net_return_pct'] for c in group)],'positive_complete30d_folds1_counts':dict(Counter(c['positive_complete_30d_folds_1x'] for c in group)),'positive_recent5d_folds1_counts':dict(Counter(c['recent40_positive_5d_folds_1x'] for c in group)),'failed_criteria_counts':dict(Counter(p for c in group for p in c['failed_criteria']))}
 put(R/'summary.json',summ);ctx=json.loads((R/'context.json').read_text());fwd=json.loads((R/'forward_report.json').read_text());fv=json.loads((R/'forward_verification.json').read_text())
 lines=[f'# {R.name} BTC退出带宽与门槛反转预算的五维敏感性',f'真实新评估108组合/324个1/2/3倍成本场景：{summ["passed_candidates"]}通过/{summ["rejected_candidates"]}淘汰。全部逐项先reserve，计算、独立核验后finish；负收益/零收益/失败门槛完整保存。全文读取{ctx["registry_events"]}事件/{ctx["registry_ids"]}ID与{len(ctx["prior_conclusions_read"])}份旧结论，初始16均有真实历史证据。复用90完整原生账本/270成本NAV原SHA，源信号/撮合/资金费模型重跑0。',
 '预设BTC顺趋势ROC31日、入场4%、退出E0.5/1/2%；ETH慢趋势约束反转S7/14/28日、短L1/2/3日、H2/4/6%，ETH_N1000/2000/3000且BTC_N=4000-ETH_N。N×S×L×H×E完整243格五维网格，810相邻边；旧N2000三退出81项及旧非对称预算E1%54项共135控制只读，108缺格（N≠2000且E≠1%）才是新配置。原070542历史合格候选完整spec/参数/资格/报告SHA不变；本轮是BTC退出敏感性，不是其独立前向验证，不根据结果切换旧候选。',
 '原值权重1/1代表两个各10000USDT完整独立银行，父本金20000，总固定入场预算4000占初始本金20%。1000/3000为风险预算，不自动归一化资本或按NAV复利。各源新入场按N/此前完整close/lot向下取整，同向保留实际q；不缩放旧NAV替代新手数。本轮所用每种N的真实源路径均已有实际结果，按保存cash/q/entry与真实价格恢复后核对每条原NAV SHA。无转账、交叉保证金、现金生息、父再平衡或额外父成交。',
 'BTC前一完整close的31日ROC>4%多、<-4%空，带内实际多头仅ROC>-E保持，空头仅ROC<E保持；退出等号平仓，入场等号不新开，反向极端先平后开。ETH短ROC>H空、<-H多；带内实际多头仅ROC<0保持、空头仅ROC>0保持，过零退出；慢ROC>0仅许多、<0仅许空、=0全平，不兼容平实际仓位，无隐藏desired，现金重入须新严格极端。均只用此前完整close，次日UTC00:01 OPEN执行。完整规则、实际数量、费用和风险路径由源spec/账本/报告指纹固定。',
 '真实Binance8合并Parquet＋16年度/近期源文件留忽略data并固定路径/字节/版本/SHA。连续OOS2025-10-19 UTC00:01至2026-10-24 UTC00:01共370日、33日上下文；12完整30日折＋10日尾折，至少9/12完整月净正，尾折保留但不计门槛。近期Sep14-Oct24继承日330决策前状态，8个连续5日折至少6/8净正且各成本净正，无本金/仓位重开或诊断成交。无拟合模型/未来标签、purge不适用，因果执行及初始3日embargo保持。全部历史已反复使用，不称未触碰最终测试。',
 '每原生每侧5bp手续费＋1bp半价差＋2bp滑点，冲击0.5×滞后20日对数波动×sqrt(订单参考金额/滞后20日ADV)，参与率≤0.1%；真实lot/不利tick/最小金额与各源独立现金约束。真实资金费按结算时点/mark及当时q入账，流出×k、流入不放大，未来公开费率不用于信号/数量。永续空头以现金保证金，不虚构现货借贷。缺历史L2/队列/TCA/完整阶梯，1%维持保证金＋小时不利mark高低价仅代理；完整分钟交易代理/小时mark/结算NAV回撤不称tick级清算保证。复用不等于零费用。',
 '三项验证已执行：13时间折、8近期折、连续OOS整体DD；243格五维敏感性及810边、Sharpe/Calmar/边界诊断；324新1/2/3倍成本场景。其他预设门槛3x整体DD≤25%、局部五维3x净正≥60%、至少4往返、(参考价毛利＋资金费)/执行成本≥2.5、各源现金/拒单/保证金代理违规0、终点空仓。旧135资格维持原三维/四维定义，只将原指标用于新邻域，不重评级。',
 f'全期1/2/3倍成本净正数量{summ["positive_configs_by_cost"]}，近期{summ["recent_positive_configs_by_cost"]}；失败门槛{summ["failed_criteria_counts"]}。全期最佳{summ["best_full"]}；近期最佳{summ["best_recent"]}。']
 for label,z in summ['groups'].items():lines.append(f'{label}：{z}')
 lines += ['每个新组合对照同N/S/L/H的旧BTC退出1%和相同预算恒多/现金，648个逐成本对照完整保留。90原生＋135旧父＋3恒多共228旧唯一结果原状态/资格/报告字节/登记SHA不变。不同BTC退出源组件为真实新组合，不因family相同排除；仅改名、顺序、数字格式不算新配置。',
 f'原SMA65/对称1%、BTC1500/ETH500从UTC06:30现金状态续至{fwd["cutoff_utc"]}，新增{fv["new_closed_marks_per_asset"]}闭合分钟mark，零日决策/参考/成交，旧{fv["original_NAV_prefix"]}点严格继承、新总{fv["NAV_points_per_scene"]}点。Oct26UTC00:01BTC退出已完成不重复；下一日2026-10-27UTC00:01、终点2027-03-31不变。逐币逐成本cash/units/desired/费用/成交完整延续，不从2000本金重开。',
 '旧SMA继续历史Float手数/10bp模型，不套新永续5bp/lot/tick；24日延迟shadow不足180日/六折，非paper10实盘报价模拟，也非070542候选的独立前向。最近65日日线上下文仍010010/forward_inputs.json.gz及原SHA，当前mark-only输入仅分钟数组，下一日不得误作日线。所有既有冻结账户/本金/持仓保持。',
 '本轮读AQR官方[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)（2012-05-01）和[交易成本研究](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)（2012-12-05），访问2026-10-26。传统12月期货趋势与股票反转成本只作背景；加密双币S/L/H/预算/BTC退出研究为本轮推断，不是论文复现或利润/容量移植。108相关新组合依赖已见历史，不能称独立确认、DSR/PBO校正或稳定实盘盈利。旧候选需单独预定的新数据前向验证，尚无该候选的独立前向收益。',
 '复现目录/home/desktop/Documents/Codex/EquiTide；audit.py/check_sources.py/check_alignment.py读取已finish证据，forward.py --reproduce及audit_forward.py不HTTP/写登记。不要重新reserve/evaluate/summarize已finish精确配置；本轮计算/审计/汇总/finish分阶段记录实际退出，避免长会话结束丢失回执。行情留忽略data，保留完整账本与核验必要证据，只清本轮可重建缓存。普通SSH非强推main，freshfetch/全heads/完整tree及必要blob/data/report核验后释放本轮broker；发布回执留.git。']
 (R/'result.md').write_text('\n\n'.join(lines)+'\n');print(json.dumps(summ),flush=True)
if __name__=='__main__':main()
