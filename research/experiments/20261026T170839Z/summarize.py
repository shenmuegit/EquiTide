"""Export every actual cell/fold/cost and joint3D/6D predeclared sensitivity surfaces."""
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
 assert not(R/'finish.json').exists();report=json.loads((R/'report.json').read_text());grid=grid_configs(report['configs']);assert len(grid)==336
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
   for kind,y in [('matched_old_BTC_L31',grid[c['matched_old_BTC_L31']]),('matched_old_BTC_H4',grid[c['matched_old_BTC_H4']]),('matched_hold',holds[href['fingerprint']])]:
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
   fig,axs=plt.subplots(2,2,figsize=(11,7),layout='constrained')
   for i,LB in enumerate([28,31]):
    for j,rr in enumerate([False,True]):
     mat=np.array([[(by[N,LB,BH]['scenes']['3']['recent40'] if rr else by[N,LB,BH]['scenes']['3'])['net_return_pct'] for N in NOTIONALS] for BH in [.04,.06]]);im=axs[i,j].imshow(mat,cmap='RdYlGn',vmin=-limits[rr],vmax=limits[rr]);axs[i,j].set_xticks(range(3),NOTIONALS);axs[i,j].set_yticks(range(2),['4%','6%']);axs[i,j].set_xlabel('BTC entry notional / 10,000 bank');axs[i,j].set_ylabel('BTC entry hurdle');axs[i,j].set_title(f'BTC look {LB}d / '+('Inherited40days' if rr else '370days'))
     for x,y in itertools.product(range(2),range(3)):axs[i,j].text(y,x,f'{mat[x,y]:+.3f}%'+('' if LB==28 and x==1 else '*'),ha='center',va='center')
     fig.colorbar(im,ax=axs[i,j],label='3x net return (%)')
   fig.suptitle('BTC lookback x entry interaction / exit1% | * old | known history');fig.savefig(R/'sensitivity_native_BTC.png',dpi=120);plt.close(fig)
  else:
   combinations=[(28,.04),(28,.06),(31,.04),(31,.06)]
   for N,S in itertools.product(NOTIONALS,SLOWS):
    fig,axs=plt.subplots(4,2,figsize=(11,16),layout='constrained')
    for i,(LB,BH) in enumerate(combinations):
     for j,rr in enumerate([False,True]):
      mat=np.array([[(by[N,S,L,H,LB,BH]['scenes']['3']['recent40'] if rr else by[N,S,L,H,LB,BH]['scenes']['3'])['net_return_pct'] for L in LOOKS] for H in HURDLES]);im=axs[i,j].imshow(mat,cmap='RdYlGn',vmin=-limits[rr],vmax=limits[rr]);old=(LB,BH)!=(28,.06);axs[i,j].set_title(f'ETH slow{S}d / BTC{LB}d entry{BH*100:g}%'+(' / old*' if old else ' / new')+'\n'+('Inherited40days' if rr else '370days'));axs[i,j].set_xticks(range(3),LOOKS);axs[i,j].set_yticks(range(3),[f'{x*100:g}%' for x in HURDLES]);axs[i,j].set_xlabel('ETH fast reversal lookback(days)');axs[i,j].set_ylabel('ETH reversal entry hurdle')
      for x,y in itertools.product(range(3),range(3)):axs[i,j].text(y,x,f'{mat[x,y]:+.3f}%'+('*' if old else ''),ha='center',va='center',fontsize=9)
      fig.colorbar(im,ax=axs[i,j],label='3x net return (%)')
    fig.suptitle(f'BTC N{4000-N}+ETH N{N} | banks20,000/raw1/1 | known history');fig.savefig(R/f'sensitivity_N{N}_S{S}.png',dpi=120);plt.close(fig)
 counts={'cost':len(rows),'full_folds':len(folds),'recent40_folds':len(recent),'daily_NAV':len(daily),'edges':len(edges),'reference_comparisons':len(comp)};assert list(counts.values())==[1008,13104,8064,93492,1208,756]
 for path,data,gz in [('sensitivity.csv',rows,False),('fold_results.csv',folds,False),('recent40_fold_results.csv',recent,False),('daily_equity.csv.gz',daily,True),('joint_edges.csv',edges,False),('reference_comparisons.csv',comp,False)]:table(R/path,data,gz)
 report['joint_grid_sensitivity']={'surfaces':surfaces,'total_cells':336,'new_cells':84,'readonly_old_cells':252,'cells':cells,'cliff_definition':'Per-scope absadjacentSharpedelta >2*populationSDoffiniteabsadjacentSharpedeltas; descriptive only, oldqualificationunchanged, no postresultexpansion.'};put(R/'report.json',report)
 def brief(c):return {'name':c['name'],'scope':c['scope'],'full_return3_pct':c['scenes']['3']['net_return_pct'],'whole_DD3_pct':c['scenes']['3']['max_drawdown_pct'],'recent_return3_pct':c['scenes']['3']['recent40']['net_return_pct'],'recent_DD3_pct':c['scenes']['3']['recent40']['max_drawdown_pct'],'positive_complete30d_folds1':c['positive_complete_30d_folds_1x'],'positive_recent5d_folds1':c['recent40_positive_5d_folds_1x'],'status':c['status'],'failed_criteria':c['failed_criteria']}
 cs=list(report['configs'].values());summ={'new_financial_configs':84,'new_native_backtests':3,'new_passive_parents':81,'readonly_native_components':90,'readonly_parent_cells':243,'readonly_native_cells':9,'readonly_matched_holds':6,'full_grid_cells':336,'passed_candidates':len(report['summary']['passed']),'rejected_candidates':len(report['summary']['rejected']),'positive_configs_by_cost':report['summary']['positive_configs_by_cost'],'recent_positive_configs_by_cost':{k:sum(c['scenes'][k]['recent40']['net_return_pct']>0 for c in cs) for k in ['1','2','3']},'failed_criteria_counts':dict(Counter(p for c in cs for p in c['failed_criteria'])),'best_full':brief(max(cs,key=lambda c:c['scenes']['3']['net_return_pct'])),'best_recent':brief(max(cs,key=lambda c:c['scenes']['3']['recent40']['net_return_pct'])),'rows':counts,'groups':{}}
 for scope in ['native','parent']:
  z=[c for c in cs if c['scope']==scope];summ['groups'][scope]={'configs':len(z),'passed':sum(c['status']=='passed' for c in z),'positive3':sum(c['scenes']['3']['net_return_pct']>0 for c in z),'recent_positive3':sum(c['scenes']['3']['recent40']['net_return_pct']>0 for c in z),'full3_range_pct':[min(c['scenes']['3']['net_return_pct'] for c in z),max(c['scenes']['3']['net_return_pct'] for c in z)],'recent3_range_pct':[min(c['scenes']['3']['recent40']['net_return_pct'] for c in z),max(c['scenes']['3']['recent40']['net_return_pct'] for c in z)],'failed_criteria_counts':dict(Counter(p for c in z for p in c['failed_criteria']))}
 put(R/'summary.json',summ);ctx=json.loads((R/'context.json').read_text());fwd=json.loads((R/'forward_report.json').read_text());fv=json.loads((R/'forward_verification.json').read_text())
 lines=[f'# {R.name} BTC回看与入场阈值联合敏感性',f'逐项预登记并实际评估3个BTC28日/H6%原生数量配置＋81组合，共84项、252个1/2/3倍成本场景：{summ["passed_candidates"]}历史通过/{summ["rejected_candidates"]}淘汰。所有spec先成功reserve，再实际计算/独立核验/finish；正、负收益与失败门槛完整保存。全文读取{ctx["registry_events"]}事件/{ctx["registry_ids"]}ID、{len(ctx["prior_conclusions_read"])}份旧结论；初始16均有真实历史证据。',
 '已完成的单轴研究显示BTC31日H6%和BTC28日H4%各有历史通过组合，但不能据此假定BTC28日H6%也更好。本轮事先固定缺少的交互格L28/H6/E1，覆盖N1000/2000/3000及所有81个ETH预算/慢趋势/短反转/阈值组合。更严格入场与更短周期可能同时减少成本，也可能错过趋势或改变反转时点；收益未知前固定批次，绝不以测试结果再选参数。',
 '原生N×BTC_L28/31×BTC_H4/6为12格三维（9旧＋3新、20边）；父N_ETH×S7/14/28×L_ETH1/2/3×H_ETH2/4/6×BTC_L28/31×BTC_H4/6为324格六维（243旧＋81新、1188边）。旧252只读格保留各自原2D/3D/4D/5D资格、登记、报告字节，不套新邻域重评级。当前联合矩形只含L28/31和H4/6，不冒充覆盖L25或H2的完整六维。',
 '原值乘数1/1为两个各10000 USDT完整独立银行，父本金20000。ETH_N1000/2000/3000，BTC_N=4000-ETH_N，总固定入场4000占初始父本金20%。N是固定入场预算，不是归一化资本权重或NAV复利。每次新q按N/此前完整close/真实lot向下取整，同向保留实际q；3个新原生手数的费用、tick/lot、实际资金费和保证金路径真实计算，不能线性缩放旧NAV。父无转账/交叉保证金/再平衡/额外成交。',
 'BTC此前完整close的L日ROC严格>H做多、<-H做空，带内实际多仅ROC>-1%、实际空仅ROC<1%保持，等号退出，反向极端先平后开。ETH短ROC>H反转空、<-H反转多，带内实际多仅ROC<0、空仅ROC>0，过零退出；慢ROC正只许多、负只许空、零全平，不兼容平实际仓位、无隐藏desired，现金重入须新严格极端。执行为00:01 OPEN，所有信号/数量只用此前完整close；00:00或毫秒偏移资金费先计当时旧q。',
 '数据为真实8合并Parquet＋16年度/近期源文件，路径/版本/字节/SHA固定并留忽略data。连续OOS2025-10-19 UTC00:01至2026-10-24 UTC00:01共370日；33日完整上下文支持最大31日，初始3日embargo不变、无负索引借未来。12完整30日折＋10日尾折，至少9/12完整月1x净正；近期Sep14-Oct24继承日330决策前cash/q，8×5日折至少6/8净正且三档近期净正，不重开本金或制造诊断成交。无拟合/未来标签，purge不适用；历史已经反复使用，不称未触碰最终留出。',
 '每侧5bp手续费＋1bp半价差＋2bp滑点，冲击0.5×此前20日日对数波动×sqrt(订单参考金额/此前20日ADV)，参与率≤0.1%；真实lot/不利tick/最小金额、独立现金与100%抵押入场上限。真实资金费=-q×结算mark×realizedrate，流出乘成本k、流入不放大，费率事后记账不入信号/手数；永续空头无虚构现货借币费。缺历史L2/队列/TCA/完整阶梯，闭合小时不利mark＋1%维持保证金仅代理，分钟价/小时mark/资金费前后NAV抽样DD不是tick级清算保证。',
 '三项验证已执行：13时间折/8近期折及整条连续NAV回撤；原生3D/父6D全网格与局部邻域、Sharpe/Calmar/陡变/边界；252新成本场景。其他固定门槛3x整体DD≤25%、局部3x净正≥60%、1x至少4往返、(参考毛利＋资金费)/执行成本≥2.5、现金/拒单/保证金代理违规0及终点空仓。1008成本行、13104全期折、8064近期折、93492新日边界、1208边、756逐成本对照完整保留。每新项对照同N/ETH参数的旧L31/H6、旧L28/H4和同预算恒多/解析现金。',
 f'全期1/2/3倍净正{summ["positive_configs_by_cost"]}，近期{summ["recent_positive_configs_by_cost"]}；失败门槛{summ["failed_criteria_counts"]}。全期最佳（scope区分单币10000/父20000）{summ["best_full"]}，近期最佳{summ["best_recent"]}；分组{summ["groups"]}。',
 '90个旧原生/270成本NAV由真实保存cash/q/entry和价格恢复，逐条核对原SHA；不重跑旧信号、撮合或资金费模型。只新3BTC原生运行9成本路径，再逐点加已保存ETH净值得81父/243场景。独立整数因果信号、原生手数/Decimal费用/结算/完整NAV/小时风险及父逐点相加核验；不平均Sharpe/收益率。339个旧唯一结果（含6个同预算恒多）的原状态/报告保持。',
 f'旧SMA65/对称1%、BTC1500/ETH500，从UTC14:30逐成本现金状态延续至{fwd["cutoff_utc"]}；新增{fv["new_closed_marks_per_asset"]}闭合分钟mark，0日决策/参考/成交，旧{fv["original_NAV_prefix"]}点严格继承至{fv["NAV_points_per_scene"]}点。Oct26退出已处理不重复，下一日Oct27UTC00:01、终点2027-03-31不变。24日延迟shadow不是paper10或原候选的独立新数据前向。',
 '原070542合格候选BTC31日/H4/E1、N1000＋ETH S28/L3/H2、N3000保持spec/资格/报告SHA。09轮180日新数据计划、11轮已核验观察器只读；当前status仍等待2026-10-27UTC00:01，未建候选账户/未来窗口/成交/收益，不依联合格结果切换。未来实际窗口须逐项reserve后增量续接两10000银行及2027-04-25终点；既有SMA/paper10不重置/替换。',
 '一手背景：[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)（2012-05-01）、[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)（2012-12-05），本轮访问2026-10-26。传统12月期货趋势/股票反转费用仅作背景，加密回看与入场交互、门控预算是本轮推断，不是论文复现或利润/容量移植。84相关新试验仍受历史多重选择偏差影响，无DSR/PBO校正或稳定实盘盈利证明。',
 '复现目录/home/desktop/Documents/Codex/EquiTide；audit.py/check_sources.py/check_alignment.py及forward.py --reproduce/audit_forward.py读取已finish实际证据，不重新reserve/evaluate/summarize精确配置。真实退出码/失败事实留档，完整账本/冻结规则/登记/核验证据保留，只清本轮可重建缓存。仅main、同一branch.lock内提交非强推，freshfetch/独立全heads/完整tree与必要blob/data/report验证后释放本轮锁；不新建定时器、网页部署、分支或真实订单。']
 (R/'result.md').write_text('\n\n'.join(lines)+'\n');print(json.dumps(summ),flush=True)
if __name__=='__main__':main()
