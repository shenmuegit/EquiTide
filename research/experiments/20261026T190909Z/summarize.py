"""Export every actual cell/fold/cost and ETHslow4D native/parent predeclared surfaces."""
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
 assert not(R/'finish.json').exists();report=json.loads((R/'report.json').read_text());grid=grid_configs(report['configs']);assert len(grid)==270
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
   for kind,y in [('matched_old_S28',grid[c['matched_old_S28']]),('matched_old_S14',grid[c['matched_old_S14']]),('matched_hold',holds[href['fingerprint']])]:
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
  for S in [7,14,21,28,31]:
   fig,axs=plt.subplots(3,2,figsize=(11,12),layout='constrained')
   for i,N in enumerate(NOTIONALS):
    for j,rr in enumerate([False,True]):
     mat=np.array([[(by[N,S,L,H]['scenes']['3']['recent40'] if rr else by[N,S,L,H]['scenes']['3'])['net_return_pct'] for L in LOOKS] for H in HURDLES]);im=axs[i,j].imshow(mat,cmap='RdYlGn',vmin=-limits[rr],vmax=limits[rr]);old=S in [7,14,28];bank=f'ETH N{N}/bank10,000' if scope=='native' else f'BTC N{4000-N}+ETH N{N}/banks20,000';axs[i,j].set_title(bank+(' / old*' if old else ' / new')+'\n'+('Inherited40days' if rr else '370days'));axs[i,j].set_xticks(range(3),LOOKS);axs[i,j].set_yticks(range(3),[f'{x*100:g}%' for x in HURDLES]);axs[i,j].set_xlabel('ETH reversal lookback(days)');axs[i,j].set_ylabel('ETH reversal entry hurdle')
     for x,y in itertools.product(range(3),range(3)):axs[i,j].text(y,x,f'{mat[x,y]:+.3f}%'+('*' if old else ''),ha='center',va='center',fontsize=9)
     fig.colorbar(im,ax=axs[i,j],label='3x net return (%)')
   fig.suptitle(f'{scope}: ETH slow trend {S}days | known history/raw1/1 parent');fig.savefig(R/f'sensitivity_{scope}_S{S}.png',dpi=120);plt.close(fig)
 counts={'cost':len(rows),'full_folds':len(folds),'recent40_folds':len(recent),'daily_NAV':len(daily),'edges':len(edges),'reference_comparisons':len(comp)};assert list(counts.values())==[810,10530,6480,120204,756,972]
 for path,data,gz in [('sensitivity.csv',rows,False),('fold_results.csv',folds,False),('recent40_fold_results.csv',recent,False),('daily_equity.csv.gz',daily,True),('joint_edges.csv',edges,False),('reference_comparisons.csv',comp,False)]:table(R/path,data,gz)
 report['joint_grid_sensitivity']={'surfaces':surfaces,'total_cells':270,'new_cells':108,'readonly_old_cells':162,'cells':cells,'cliff_definition':'Per-scope absadjacentSharpedelta >2*populationSDoffiniteabsadjacentSharpedeltas; descriptive only, oldqualificationunchanged, no postresultexpansion.'};put(R/'report.json',report)
 def brief(c):return {'name':c['name'],'scope':c['scope'],'full_return3_pct':c['scenes']['3']['net_return_pct'],'whole_DD3_pct':c['scenes']['3']['max_drawdown_pct'],'recent_return3_pct':c['scenes']['3']['recent40']['net_return_pct'],'recent_DD3_pct':c['scenes']['3']['recent40']['max_drawdown_pct'],'positive_complete30d_folds1':c['positive_complete_30d_folds_1x'],'positive_recent5d_folds1':c['recent40_positive_5d_folds_1x'],'status':c['status'],'failed_criteria':c['failed_criteria']}
 cs=list(report['configs'].values());summ={'new_financial_configs':108,'new_native_backtests':54,'new_passive_parents':54,'readonly_native_components':84,'readonly_parent_cells':81,'readonly_native_cells':81,'readonly_matched_holds':6,'full_grid_cells':270,'passed_candidates':len(report['summary']['passed']),'rejected_candidates':len(report['summary']['rejected']),'positive_configs_by_cost':report['summary']['positive_configs_by_cost'],'recent_positive_configs_by_cost':{k:sum(c['scenes'][k]['recent40']['net_return_pct']>0 for c in cs) for k in ['1','2','3']},'failed_criteria_counts':dict(Counter(p for c in cs for p in c['failed_criteria'])),'best_full':brief(max(cs,key=lambda c:c['scenes']['3']['net_return_pct'])),'best_recent':brief(max(cs,key=lambda c:c['scenes']['3']['recent40']['net_return_pct'])),'rows':counts,'groups':{}}
 for scope in ['native','parent']:
  z=[c for c in cs if c['scope']==scope];summ['groups'][scope]={'configs':len(z),'passed':sum(c['status']=='passed' for c in z),'positive3':sum(c['scenes']['3']['net_return_pct']>0 for c in z),'recent_positive3':sum(c['scenes']['3']['recent40']['net_return_pct']>0 for c in z),'full3_range_pct':[min(c['scenes']['3']['net_return_pct'] for c in z),max(c['scenes']['3']['net_return_pct'] for c in z)],'recent3_range_pct':[min(c['scenes']['3']['recent40']['net_return_pct'] for c in z),max(c['scenes']['3']['recent40']['net_return_pct'] for c in z)],'failed_criteria_counts':dict(Counter(p for c in z for p in c['failed_criteria']))}
 put(R/'summary.json',summ);ctx=json.loads((R/'context.json').read_text());fwd=json.loads((R/'forward_report.json').read_text());fv=json.loads((R/'forward_verification.json').read_text())
 lines=[f'# {R.name} ETH慢趋势21/31日门控敏感性',f'实际评估54个ETH新原生参数/数量配置＋54组合，共108项、324个1/2/3倍成本场景：{summ["passed_candidates"]}历史通过/{summ["rejected_candidates"]}淘汰。所有实际定义逐项先reserve，计算/独立核验后finish，正、负收益和门槛失败均保存。全文读取{ctx["registry_events"]}事件/{ctx["registry_ids"]}ID、{len(ctx["prior_conclusions_read"])}份旧结论；初始16已有真实历史证据。',
 '原ETH慢趋势28日在旧网格边界，不能只看该点。预先固定新增21日（三周）和31日（略越过28）门控，配合N1000/2000/3000、短L1/2/3、H2/4/6%，并保留旧S7/14/28只读控制。更短/更长门控可能减少反向仓位，也可能误过滤反转或错过趋势；原BTC31日/H4%/退出1%固定，不追逐上一轮联合格收益。仍是已见历史开发试验，不是独立新数据确认。',
 '每scope原生/父N3×S5×L3×H3=135格四维，各81旧＋54新、378相邻边；合计270格/756边。slow轴7/14/21/28/31的间隔不均匀（7/7/7/3日），邻域是预定相邻索引，不能解释为等距离。只对108新项按预定资格评级，162旧格的原资格/报告/登记不变。',
 '原值1/1为两各10000 USDT完整独立银行，父本金20000。ETH_N1000/2000/3000，BTC_N=4000-ETH_N，总固定入场4000占初始父本金20%；N非归一化资本权重，不按NAV复利。每次新q=floor(N/此前完整close/真实lot)×lot，同向保留实际q。54个新ETH参数/手数路径真实核算费用、tick/lot、资金费和保证金，不能线性缩放NAV；父无转账/交叉保证金/再平衡/额外成交。',
 'ETH短ROC>H反转空、<-H反转多，带内实际多仅ROC<0、实际空仅ROC>0保持，过零退出；慢ROC正只许多、负只许空、零全平，不兼容平实际仓位，无隐藏desired，现金重入须新严格极端。BTC31日ROC严格>4%多、<-4%空，带内多仅ROC>-1%、空仅ROC<1%保持，反向极端先平后开。00:01 OPEN执行，信号/手数仅用此前完整close；00:00或毫秒偏移资金费先计旧q。',
 '本轮engine相对冻结185633代码只扩展slow允许域7/14/28至7/14/21/28/31；数学/成本/账本逻辑未改。预计算675个人工向量目标检查、405个旧域精确一致性比较、未来值毒化和负索引拒绝已实际执行；这些工程夹具不是策略回测、账户或未来收益。原生/父的两个慢周期字段须同时一致，检查器会拒绝矛盾定义。',
 '预计算检查发现54个原始父spec的ETH_trend_lookback_days已为21/31而重复别名trend_filter_lookback_days仍为28；尚未进行任何实际回测。原始spec/plan/batch/reserve及失败exit1留档，54错误父定义finish abandoned/false，不算负收益或已完成回测；54原生定义有效保留。修正别名后另存specs_corrected和plan_corrected，54正确父定义逐项reserve成功才计算；不改数据、规则、费用或失败门槛。invalid_spec_report、correction_commands和alias_preflight_recovery完整证明，禁止把无结果错误项冒充rejected或删去。',
 '数据为真实8合并Parquet＋16年度/近期源文件，路径/版本/字节/SHA固定并留忽略data。连续OOS2025-10-19 UTC00:01至2026-10-24 UTC00:01共370日，33日完整上下文支持最大S31，初始3日embargo保持，无负索引/未来warmup。12完整30日折＋10日尾折，至少9/12完整月1x净正；近期Sep14-Oct24继承日330决策前cash/q，8×5日折至少6/8净正且三档近期净正，不重开本金或制造诊断成交。无拟合/未来标签，purge不适用；历史反复使用，不称未触碰最终留出。',
 '每侧5bp手续费＋1bp半价差＋2bp滑点，冲击0.5×此前20日日对数波动×sqrt(参考金额/此前20日ADV)，参与率≤0.1%；真实lot/不利tick/最小金额、独立现金与100%抵押入场上限。资金费=-q×结算mark×realizedrate，流出乘成本k、流入不放大，费率事后记账不入信号/手数；永续空头无虚构现货借币费用。缺L2/队列/TCA/完整阶梯，闭合小时不利mark＋1%维持保证金仅代理，分钟价/小时mark/结算前后抽样DD不是tick级清算保证。',
 '三项验证已执行：13时间折/8近期折及连续整条NAV回撤；两scope四维完整邻域、Sharpe/Calmar/陡变/边界图；324新成本场景。其他固定门槛3x整体DD≤25%、局部3x净正≥60%、1x至少4往返、(参考毛利＋资金费)/执行成本≥2.5、现金/拒单/保证金代理违规0和终点空仓。810成本行、10530全期折、6480近期折、120204新日边界、756边、972逐成本对照保留。每新项匹配相同N/L/H的旧S14、S28和同预算恒多/解析现金。',
 f'全期1/2/3倍净正{summ["positive_configs_by_cost"]}，近期{summ["recent_positive_configs_by_cost"]}；失败门槛{summ["failed_criteria_counts"]}。全期最佳（scope区分单币10000/父20000）{summ["best_full"]}；近期最佳{summ["best_recent"]}；分组{summ["groups"]}。',
 '84旧原生/252成本NAV由真实cash/q/entry分段和价格恢复并逐条核对原SHA；不重跑旧信号/撮合/资金费模型。只54新ETH原生运行162成本路径，再逐点加已保存BTC净值得54父/162场景。独立整数因果信号、q/Decimal费用/结算/完整NAV/小时风险与父逐点相加核验，不平均Sharpe/收益率；171旧唯一结果（含6同预算恒多）原状态/报告保持。',
 f'旧SMA65/对称1%、BTC1500/ETH500，从UTC16:30逐成本现金状态续至{fwd["cutoff_utc"]}；新增{fv["new_closed_marks_per_asset"]}闭合分钟mark，0日决策/参考/成交，旧{fv["original_NAV_prefix"]}点严格继承至{fv["NAV_points_per_scene"]}点。Oct26退出不重复，下一日Oct27UTC00:01、终点2027-03-31不变。24日延迟shadow不是paper10或候选的新数据前向。',
 '原070542候选BTC31日/H4/E1、N1000＋ETH S28/L3/H2、N3000保持spec/资格/报告SHA。09轮180日新数据计划、11轮已核验观察器只读，当前status仍等待2026-10-27UTC00:01；未建候选账户/未来窗口/成交/收益，不依新slow结果切换。未来真实窗口逐项reserve后增量续接两10000银行及2027-04-25终点；既有SMA/paper10不重置/替换。',
 '一手背景：[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)（2012-05-01）、[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)（2012-12-05），访问2026-10-26。传统期货自收益趋势/股票反转费用只作背景，加密慢门控周期与预算为本轮假设，不是论文复现或利润/容量移植。108相关实际试验仍受历史多重选择偏差影响，无DSR/PBO校正或稳定实盘盈利证明。',
 '复现目录/home/desktop/Documents/Codex/EquiTide；audit.py/check_sources.py/check_spec_aliases.py/check_alignment.py及forward.py --reproduce/audit_forward.py读取已finish实际证据，不重新reserve/evaluate/summarize精确配置。保留失败定义和完整账本/冻结规则/登记/核验证据，只清本轮可重建缓存。仅main、同一branch.lock内提交非强推，freshfetch/独立全heads/完整tree与必要blob/data/report验证后释放本轮锁；不新建定时器、网页部署、分支或真实订单。']
 (R/'result.md').write_text('\n\n'.join(lines)+'\n');print(json.dumps(summ),flush=True)
if __name__=='__main__':main()
