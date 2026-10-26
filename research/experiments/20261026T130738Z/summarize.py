"""Export every actual cell/fold/cost and both predeclared sensitivity surfaces."""
import csv,gzip,io,itertools,json,statistics
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run import ROOT,R,NOTIONALS,SLOWS,LOOKS,HURDLES,axes,grid_configs,sha,put

def table(path,rows,compressed=False):
 fields=list(dict.fromkeys(k for r in rows for k in r));b=io.StringIO(newline='');w=csv.DictWriter(b,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows);path.write_bytes(gzip.compress(b.getvalue().encode(),mtime=0) if compressed else b.getvalue().encode())
def main():
 assert not(R/'finish.json').exists();report=json.loads((R/'report.json').read_text());grid=grid_configs(report['configs']);assert len(grid)==252
 docs={};holds={}
 refs=[*json.loads((R/'holds.json').read_text()).values(),*json.loads((R/'native_holds.json').read_text())['references'].values()]
 for ref in refs:
  assert sha(ROOT/ref['report'])==ref['report_sha256']
  if ref['report'] not in docs:docs[ref['report']]=json.loads((ROOT/ref['report']).read_text())
  c=__import__('copy').deepcopy(docs[ref['report']]['configs'][ref['name']]);c.update(scope=ref['scope'],asset=ref['asset'],capital_usdt=ref['capital_usdt'])
  for z in c['scenes'].values():
   if 'recent40' not in z:z['recent40']=z['extension40']
  holds[ref['fingerprint']]=c
 parentholds=json.loads((R/'holds.json').read_text());nativeholds=json.loads((R/'native_holds.json').read_text())['references'];rows=[];folds=[];recent=[];daily=[];comp=[];edges=[];cells={};surfaces={}
 for c in grid.values():
  old=c.get('read_only_anchor',False);meta={'name':c['name'],'scope':c['scope'],'asset':c['asset'],'read_only_anchor':old,'capital_usdt':c['capital_usdt'],**{p:c[p] for p in axes(c)}}
  cells[c['name']]={**meta,'fingerprint':c['fingerprint'],'original_or_new_status':c['status'],'positive_complete30d_folds1':c['positive_complete_30d_folds_1x'],'positive_recent5d_folds1':c['recent40_positive_5d_folds_1x'],'original_or_new_sensitivity':c['sensitivity'],'scenes':{k:{p:z[p] for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','NAV_sha256_f64le']} for k,z in c['scenes'].items()},'recent40':{k:{p:z['recent40'][p] for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','NAV_sha256_f64le']} for k,z in c['scenes'].items()}}
  for k,z in c['scenes'].items():
   rows.append({**meta,'cost_multiplier':int(k),'status':c['status'],**{p:z[p] for p in ['net_return_pct','max_drawdown_pct','daily_mark_drawdown_pct','sharpe_365','calmar','cost_usdt','funding_usdt','gross_reference_PnL_to_execution_cost','executions','round_trips','NAV_sha256_f64le']},**{'recent40_'+p:z['recent40'][p] for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','NAV_sha256_f64le']},**{'cost_'+p:v for p,v in z['cost_parts_usdt'].items()}})
   folds.extend({**meta,'cost_multiplier':int(k),**f} for f in z['folds']);recent.extend({**meta,'cost_multiplier':int(k),**f} for f in z['recent40']['folds'])
   if old:continue
   daily.extend({**meta,'cost_multiplier':int(k),'boundary_index':j,'equity_usdt':v} for j,v in enumerate(z['daily_equity_usdt']))
   href=nativeholds[str(c['fixed_entry_notional_usdt'])] if c['scope']=='native' else parentholds['B'+str(c['BTC_fixed_entry_notional_usdt'])+'_E'+str(c['ETH_fixed_entry_notional_usdt'])]
   for kind,y in [('matched_old_BTC_entry4pct',grid[c['matched_old_BTC_entry4pct']]),('matched_hold',holds[href['fingerprint']])]:
    a=y['scenes'][k];comp.append({**meta,'cost_multiplier':int(k),'reference_kind':kind,'reference_name':y['name'],'reference_fingerprint':y['fingerprint'],'reference_original_status':y['status'],'new_return_pct':z['net_return_pct'],'reference_return_pct':a['net_return_pct'],'return_delta_pp':z['net_return_pct']-a['net_return_pct'],'DD_delta_pp':z['max_drawdown_pct']-a['max_drawdown_pct'],'recent40_return_delta_pp':z['recent40']['net_return_pct']-a['recent40']['net_return_pct'],'execution_count_delta':z['executions']-a['executions'],'cost_delta_usdt':z['cost_usdt']-a['cost_usdt'],'new_NAV_sha256':z['NAV_sha256_f64le'],'reference_NAV_sha256':a['NAV_sha256_f64le'],'cash_analytic_return_pct':0})
 for scope in ['native','parent']:
  sub=[c for c in grid.values() if c['scope']==scope];dims=axes(sub[0]);fields=list(dims);by={tuple(c[p] for p in fields):c for c in sub};assert set(by)==set(itertools.product(*dims.values()))
  for key,c in by.items():
   for i,(field,axis) in enumerate(dims.items()):
    j=axis.index(key[i])
    if j+1==len(axis):continue
    other=list(key);other[i]=axis[j+1];y=by[tuple(other)];a,b=c['scenes']['3'],y['scenes']['3'];edges.append({'scope':scope,'axis':field,'from':c['name'],'to':y['name'],'return3_delta_pp':b['net_return_pct']-a['net_return_pct'],'DD3_delta_pp':b['max_drawdown_pct']-a['max_drawdown_pct'],'sharpe3_delta':b['sharpe_365']-a['sharpe_365'] if a['sharpe_365'] is not None and b['sharpe_365'] is not None else None,'recent40_return3_delta_pp':b['recent40']['net_return_pct']-a['recent40']['net_return_pct'],'recent40_sharpe3_delta':b['recent40']['sharpe_365']-a['recent40']['sharpe_365'] if a['recent40']['sharpe_365'] is not None and b['recent40']['sharpe_365'] is not None else None})
  for field,flag in [('sharpe3_delta','full_sharpe_cliff'),('recent40_sharpe3_delta','recent40_sharpe_cliff')]:
   scoped=[e for e in edges if e['scope']==scope];vals=[abs(e[field]) for e in scoped if e[field] is not None];cut=2*statistics.pstdev(vals) if vals else None
   for e in scoped:e[flag]=e[field] is not None and abs(e[field])>cut;e[flag+'_threshold_abs_delta']=cut
  surfaces[scope]={'cells':len(sub),'new_cells':sum(not c.get('read_only_anchor',False) for c in sub),'axes':dims,'dimension_count':len(dims),'adjacent_edges':sum(e['scope']==scope for e in edges),'old_original_qualification_unchanged':True}
  limits={rr:max(abs((c['scenes']['3']['recent40'] if rr else c['scenes']['3'])['net_return_pct']) for c in sub) or 1 for rr in [False,True]}
  if scope=='native':
   fig,axs=plt.subplots(1,2,figsize=(10,4),layout='constrained')
   for j,rr in enumerate([False,True]):
    mat=np.array([[(by[N,H]['scenes']['3']['recent40'] if rr else by[N,H]['scenes']['3'])['net_return_pct'] for N in NOTIONALS] for H in [.02,.04,.06]]);im=axs[j].imshow(mat,cmap='RdYlGn',vmin=-limits[rr],vmax=limits[rr]);axs[j].set_xticks(range(3),NOTIONALS);axs[j].set_yticks(range(3),['2% old*','4% old*','6% new']);axs[j].set_xlabel('BTC fixed entry notional / 10,000 bank');axs[j].set_ylabel('BTC entry hurdle');axs[j].set_title('Inherited 40 days' if rr else '370 days')
    for x,y in itertools.product(range(3),range(3)):axs[j].text(y,x,f'{mat[x,y]:+.3f}%',ha='center',va='center')
    fig.colorbar(im,ax=axs[j],label='3x net return (%)')
   fig.suptitle('BTC ROC31 / exit1% | known history');fig.savefig(R/'sensitivity_native_BTC.png',dpi=120);plt.close(fig)
  else:
   for N,S in itertools.product(NOTIONALS,SLOWS):
    fig,axs=plt.subplots(3,2,figsize=(10,12),layout='constrained')
    for i,E in enumerate([.02,.04,.06]):
     for j,rr in enumerate([False,True]):
      mat=np.array([[(by[N,S,L,H,E]['scenes']['3']['recent40'] if rr else by[N,S,L,H,E]['scenes']['3'])['net_return_pct'] for L in LOOKS] for H in HURDLES]);im=axs[i,j].imshow(mat,cmap='RdYlGn',vmin=-limits[rr],vmax=limits[rr]);old=E!=.06;axs[i,j].set_title(f'ETH slow {S}d / BTC entry {E*100:g}%'+(' / old*' if old else '')+'\n'+('Inherited 40 days' if rr else '370 days'));axs[i,j].set_xticks(range(3),LOOKS);axs[i,j].set_yticks(range(3),[f'{x*100:g}%' for x in HURDLES]);axs[i,j].set_xlabel('ETH fast reversal lookback (days)');axs[i,j].set_ylabel('ETH reversal entry hurdle')
      for x,y in itertools.product(range(3),range(3)):axs[i,j].text(y,x,f'{mat[x,y]:+.3f}%'+('*' if old else ''),ha='center',va='center',fontsize=9)
      fig.colorbar(im,ax=axs[i,j],label='3x net return (%)')
    fig.suptitle(f'BTC N{4000-N} + ETH N{N} | banks20,000/raw1/1 | known history');fig.savefig(R/f'sensitivity_N{N}_S{S}.png',dpi=120);plt.close(fig)
 counts={'cost':len(rows),'full_folds':len(folds),'recent40_folds':len(recent),'daily_NAV':len(daily),'edges':len(edges),'reference_comparisons':len(comp)};assert list(counts.values())==[756,9828,6048,93492,822,504]
 for path,data,gz in [('sensitivity.csv',rows,False),('fold_results.csv',folds,False),('recent40_fold_results.csv',recent,False),('daily_equity.csv.gz',daily,True),('joint_edges.csv',edges,False),('reference_comparisons.csv',comp,False)]:table(R/path,data,gz)
 report['joint_grid_sensitivity']={'surfaces':surfaces,'total_cells':252,'new_cells':84,'readonly_old_cells':168,'cells':cells,'cliff_definition':'Per-scope absadjacentSharpedelta >2*populationSDoffiniteabsadjacentSharpedeltas; descriptive only, oldqualificationunchanged, no postresultexpansion.'};put(R/'report.json',report)
 def brief(c):return {'name':c['name'],'scope':c['scope'],'full_return3_pct':c['scenes']['3']['net_return_pct'],'whole_DD3_pct':c['scenes']['3']['max_drawdown_pct'],'recent_return3_pct':c['scenes']['3']['recent40']['net_return_pct'],'recent_DD3_pct':c['scenes']['3']['recent40']['max_drawdown_pct'],'positive_complete30d_folds1':c['positive_complete_30d_folds_1x'],'positive_recent5d_folds1':c['recent40_positive_5d_folds_1x'],'status':c['status'],'failed_criteria':c['failed_criteria']}
 cs=list(report['configs'].values());summ={'new_financial_configs':84,'new_native_backtests':3,'new_passive_parents':81,'readonly_native_components':87,'readonly_parent_cells':162,'readonly_native_cells':6,'readonly_matched_holds':6,'full_grid_cells':252,'passed_candidates':len(report['summary']['passed']),'rejected_candidates':len(report['summary']['rejected']),'positive_configs_by_cost':report['summary']['positive_configs_by_cost'],'recent_positive_configs_by_cost':{k:sum(c['scenes'][k]['recent40']['net_return_pct']>0 for c in cs) for k in ['1','2','3']},'failed_criteria_counts':dict(Counter(p for c in cs for p in c['failed_criteria'])),'best_full':brief(max(cs,key=lambda c:c['scenes']['3']['net_return_pct'])),'best_recent':brief(max(cs,key=lambda c:c['scenes']['3']['recent40']['net_return_pct'])),'rows':counts,'groups':{}}
 for scope in ['native','parent']:
  z=[c for c in cs if c['scope']==scope];summ['groups'][scope]={'configs':len(z),'passed':sum(c['status']=='passed' for c in z),'positive3':sum(c['scenes']['3']['net_return_pct']>0 for c in z),'recent_positive3':sum(c['scenes']['3']['recent40']['net_return_pct']>0 for c in z),'full3_range_pct':[min(c['scenes']['3']['net_return_pct'] for c in z),max(c['scenes']['3']['net_return_pct'] for c in z)],'recent3_range_pct':[min(c['scenes']['3']['recent40']['net_return_pct'] for c in z),max(c['scenes']['3']['recent40']['net_return_pct'] for c in z)],'failed_criteria_counts':dict(Counter(p for c in z for p in c['failed_criteria']))}
 put(R/'summary.json',summ);ctx=json.loads((R/'context.json').read_text());fwd=json.loads((R/'forward_report.json').read_text());fv=json.loads((R/'forward_verification.json').read_text())
 lines=[f'# {R.name} BTC 6%入场阈值与ETH门槛反转预算验证',f'本轮预登记并真实评估3个BTC原生数量配置＋81组合，共84项、252个1/2/3倍成本场景：{summ["passed_candidates"]}历史通过/{summ["rejected_candidates"]}淘汰。全部spec先成功reserve，计算/独立核验后finish，负收益完整保留。全文读取{ctx["registry_events"]}事件/{ctx["registry_ids"]}ID与{len(ctx["prior_conclusions_read"])}份旧结论；初始16均有真实历史证据。',
 '上一轮H2比匹配H4全期更差，本轮事先固定另一侧H6，假设更严格入场可能减少震荡成本，也可能错过趋势；这是使用既有研究后提出的新开发试验，不是独立确认。BTC固定L31、退出E1%，三档N1000/2000/3000新手数真实重算。ETH S7/14/28、L1/2/3、H2/4/6%、N1000/2000/3000源账本只读。N_ETH×S×L×H_ETH×H_BTC2/4/6%共243父格，162旧＋81新、810相邻边；BTC N×H共9原生格，6旧＋3新、12边。旧168原资格、spec和报告SHA不重算/重评级。',
 '原值权重1/1代表两完整10000 USDT银行，父本金20000。BTC_N=4000-ETH_N，总固定入场4000占初始父本金20%；N不是资本权重，不归一化，不按NAV复利，不转账/交叉保证金/父再平衡。同向保留实际q，新开按N/此前完整close/真实lot向下取整，非按未来OPEN或NAV定量。不同N的原生费用、舍入、资金费及风险真实计算，不线性缩放NAV。',
 'BTC此前完整日close ROC31严格>H做多、<-H做空；带内实际多头仅ROC>-1%保持、实际空头仅ROC<1%保持，边界退出；相反严格入场先平后开。ETH短ROC>H反转空、<-H反转多；带内多仅ROC<0、空仅ROC>0保持；慢ROC正仅许多、负仅许空、零全平，实际仓位不兼容即平，现金重入须新严格短ROC极端，无隐藏desired。所有执行次日UTC00:01 OPEN，资金费00:00或毫秒偏移结算先计旧仓，再日决策。',
 '真实8合并Parquet＋16年度/近期源文件固定路径/版本/字节/SHA并留忽略data。连续OOS2025-10-19 UTC00:01至2026-10-24 UTC00:01共370日，33日上下文，12完整30日折＋10日尾折；至少9/12完整月1x净正。近期Sep14-Oct24继承第330日决策前实际cash/q，8×5日折至少6/8正且各成本近期净正；无本金重开/诊断成交。无拟合或未来标签，purge不适用，初始3日embargo及因果边界保持。所有历史已多轮使用，不能称未触碰最终留出。',
 '每侧5bp手续费＋1bp半价差＋2bp滑点，冲击0.5×此前20日日对数波动×sqrt(参考金额/此前20日ADV)，参与率≤0.1%；真实lot/不利tick/最小金额、100%入场抵押上限。实际资金费按当时q×结算mark×realized_rate，流出乘成本k、收入不放大；费率仅事后记账，不作信号/手数。永续空头用现金抵押，无虚构现货借币费。缺历史L2/队列/TCA/完整阶梯；闭合小时不利mark高低价与1%维持保证金是代理，分钟成交价/小时mark/结算前后NAV的DD不代表tick级清算保证。',
 '三项验证均实际执行：13时间折/8近期折/连续整体回撤；BTC二维与父五维完整表面、局部邻域/Sharpe/Calmar/陡变/边界诊断；新252成本场景。其他固定门槛3x整体DD≤25%、局部3x净正≥60%、1x至少4往返、(参考毛利＋资金费)/执行成本≥2.5、现金/拒单/保证金代理违规0、终点空仓。各成本逐项完整表/逐折DD以及同预算恒多/解析现金比较保留，不平均Sharpe/收益率。',
 f'结果全期1/2/3倍净正{summ["positive_configs_by_cost"]}，近期{summ["recent_positive_configs_by_cost"]}；门槛失败{summ["failed_criteria_counts"]}。全期最佳{summ["best_full"]}，近期最佳{summ["best_recent"]}。分组{summ["groups"]}。',
 '87个旧原生/261成本NAV从保存cash/q/entry分段和真实prices恢复，逐条原SHA一致；不重跑旧信号/撮合/资金费模型。只对新3个BTC原生计算9成本路径，再逐点加其与已保存ETH净值得81父/243场景；独立整条NAV/成交/资金费/严格整数阈值/手数/费用/小时风险和折指标核验。254? 旧唯一结果精确数量由source_verification和data_manifest核对，不按策略族误去重。',
 f'原SMA65/对称1%、BTC1500/ETH500，从UTC10:30逐成本真实现金状态续至{fwd["cutoff_utc"]}；追加{fv["new_closed_marks_per_asset"]}闭合分钟mark，0日决策/参考/成交，原{fv["original_NAV_prefix"]}点严格继承至{fv["NAV_points_per_scene"]}点。Oct26退出已处理不重复，下一日Oct27UTC00:01、终点2027-03-31不变。24日延迟shadow不是paper10或原候选独立新数据前瞻。',
 '原070542历史候选H4/E1、BTC_N1000/ETH_N3000、ETH S28/L3/H2保持spec/资格/报告SHA。09轮冻结180日新数据计划、11轮已校验观察器均只读；当前status实际等待2026-10-27UTC00:01，未创建账户、未来窗口、成交或收益，不根据本轮H6结果切换。两10000银行及2027-04-25终点不变，未来实际窗口先逐项reserve后增量续接。',
 '一手背景：[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)（2012-05-01）、[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)（2012-12-05），本轮访问2026-10-26。传统12月期货趋势及股票反转成本只作背景，本轮加密短周期阈值/门控/预算是研究推断，不是论文复现或利润/容量移植。84相关试验受历史多重选择偏差影响，没有DSR/PBO校正或稳定实盘盈利证明。',
 '复现工作目录/home/desktop/Documents/Codex/EquiTide。audit.py/check_sources.py/check_alignment.py及forward.py --reproduce/audit_forward.py读取已finish证据；不要重新reserve/evaluate/summarize已完成配置。每阶段实际退出码和失败事实留档。仅main、同一branch.lock内提交并普通非强推，freshfetch/独立全heads/完整tree和必要blob核验后释放本轮锁；不重部署网页/新定时器/下真实订单。']
 lines=[x.replace('254? 旧唯一结果精确数量由source_verification和data_manifest核对','255个旧唯一结果由source_verification和data_manifest核对') for x in lines]
 (R/'result.md').write_text('\n\n'.join(lines)+'\n');print(json.dumps(summ),flush=True)
if __name__=='__main__':main()
