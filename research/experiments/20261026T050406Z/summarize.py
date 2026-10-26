"""Full S/L/H/ETH-exit sensitivity, with immutable ungated matched controls."""
import csv,gzip,io,itertools,json,statistics
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run import ROOT,R,SLOWS,LOOKS,HURDLES,BUFFERS,axes,grid_configs,anchor_configs,sha,put

def table(path,rows,compressed=False):
 fields=list(dict.fromkeys(k for r in rows for k in r));b=io.StringIO(newline='');w=csv.DictWriter(b,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows);raw=b.getvalue().encode();path.write_bytes(gzip.compress(raw,mtime=0) if compressed else raw)
def main():
 assert not (R/'finish.json').exists();report=json.loads((R/'report.json').read_text());grid=grid_configs(report['configs']);assert len(grid)==81;href=json.loads((R/'holds.json').read_text())['parent'];assert sha(ROOT/href['report'])==href['report_sha256'];hold=json.loads((ROOT/href['report']).read_text())['configs'][href['name']];rows=[];folds=[];recent=[];daily=[];comp=[];edges=[];cells={}
 for c in grid.values():
  old=c.get('read_only_anchor',False);meta={'name':c['name'],'read_only_anchor':old,'capital_usdt':20000,**{p:c[p] for p in axes(c)}};cells[c['name']]={**meta,'fingerprint':c['fingerprint'],'original_or_new_status':c['status'],'positive_complete30d_folds1':c['positive_complete_30d_folds_1x'],'positive_recent5d_folds1':c['recent40_positive_5d_folds_1x'],'original_or_new_sensitivity':c['sensitivity'],'scenes':{k:{p:z[p] for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','NAV_sha256_f64le']} for k,z in c['scenes'].items()},'recent40':{k:{p:z['recent40'][p] for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','NAV_sha256_f64le']} for k,z in c['scenes'].items()}}
  for k,z in c['scenes'].items():
   rows.append({**meta,'cost_multiplier':int(k),'status':c['status'],**{p:z[p] for p in ['net_return_pct','max_drawdown_pct','daily_mark_drawdown_pct','sharpe_365','calmar','cost_usdt','funding_usdt','gross_reference_PnL_to_execution_cost','executions','round_trips','NAV_sha256_f64le']},**{'recent40_'+p:z['recent40'][p] for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','NAV_sha256_f64le']},**{'cost_'+p:v for p,v in z['cost_parts_usdt'].items()}});folds.extend({**meta,'cost_multiplier':int(k),**f} for f in z['folds']);recent.extend({**meta,'cost_multiplier':int(k),**f} for f in z['recent40']['folds'])
   if old:continue
   daily.extend({**meta,'cost_multiplier':int(k),'boundary_index':j,'equity_usdt':v} for j,v in enumerate(z['daily_equity_usdt']))
   controls=[('matched_ungated',anchor_configs()[c['matched_ungated_control']])]
   for kind,y in [*controls,('hold',hold)]:
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
 counts={'cost':len(rows),'full_folds':len(folds),'recent40_folds':len(recent),'daily_NAV':len(daily),'edges':len(edges),'reference_comparisons':len(comp)};assert list(counts.values())==[243,3159,1944,90153,216,486]
 for path,data,gz in [('sensitivity.csv',rows,False),('fold_results.csv',folds,False),('recent40_fold_results.csv',recent,False),('daily_equity.csv.gz',daily,True),('joint_edges.csv',edges,False),('reference_comparisons.csv',comp,False)]:table(R/path,data,gz)
 report['joint_grid_sensitivity']={'cell_count':81,'new_cells':81,'readonly_comparison_controls_outside_grid':27,'dimension_count':4,'axes':dims,'cells':cells,'adjacent_edges':216,'old_qualification_unchanged':True,'cliff_definition':'AbsadjacentSharpedelta>2*populationSDoffiniteabsadjacentSharpedeltasoverfull81grid;descriptiveonly,Nonepreserved,nopostresultgridexpansion.'};put(R/'report.json',report)
 limits={rr:max(abs((c['scenes']['3']['recent40'] if rr else c['scenes']['3'])['net_return_pct']) for c in grid.values()) or 1 for rr in [False,True]}
 for S in SLOWS:
  fig,axs=plt.subplots(3,2,figsize=(10,12),layout='constrained')
  for i,E in enumerate(BUFFERS):
   for j,rr in enumerate([False,True]):
    mat=np.array([[(by[S,L,H,E]['scenes']['3']['recent40'] if rr else by[S,L,H,E]['scenes']['3'])['net_return_pct'] for L in LOOKS] for H in HURDLES]);im=axs[i,j].imshow(mat,cmap='RdYlGn',vmin=-limits[rr],vmax=limits[rr]);axs[i,j].set_title(f'BTC slow {S}d / ETH trend exit {E*100:g}%'+'\n'+('Inherited 40 days' if rr else '370 days'));axs[i,j].set_xticks(range(3),[str(x) for x in LOOKS]);axs[i,j].set_yticks(range(3),[f'{x*100:g}%' for x in HURDLES]);axs[i,j].set_xlabel('BTC fast reversal lookback (days)');axs[i,j].set_ylabel('BTC reversal entry hurdle')
    for a,b in itertools.product(range(3),range(3)):axs[i,j].text(b,a,f'{mat[a,b]:+.3f}%',ha='center',va='center',fontsize=9)
    fig.colorbar(im,ax=axs[i,j],label='3x net return (%)')
  fig.suptitle('BTC gated reversal + ETH trend | raw 1/1 | banks 20,000 | known history');fig.savefig(R/f'sensitivity_S{S}.png',dpi=120);plt.close(fig)
 def brief(c):return {'name':c['name'],'full_return3_pct':c['scenes']['3']['net_return_pct'],'whole_DD3_pct':c['scenes']['3']['max_drawdown_pct'],'recent_return3_pct':c['scenes']['3']['recent40']['net_return_pct'],'recent_DD3_pct':c['scenes']['3']['recent40']['max_drawdown_pct'],'positive_complete30d_folds1':c['positive_complete_30d_folds_1x'],'positive_recent5d_folds1':c['recent40_positive_5d_folds_1x'],'status':c['status'],'failed_criteria':c['failed_criteria']}
 cs=list(report['configs'].values());summ={'new_financial_configs':81,'new_native_backtests':0,'new_passive_parents':81,'readonly_native_components':30,'readonly_ungated_controls':27,'readonly_matched_hold':1,'full_grid_cells':81,'passed_candidates':len(report['summary']['passed']),'rejected_candidates':len(report['summary']['rejected']),'positive_configs_by_cost':report['summary']['positive_configs_by_cost'],'recent_positive_configs_by_cost':{k:sum(c['scenes'][k]['recent40']['net_return_pct']>0 for c in cs) for k in ['1','2','3']},'failed_criteria_counts':dict(Counter(p for c in cs for p in c['failed_criteria'])),'best_full':brief(max(cs,key=lambda c:c['scenes']['3']['net_return_pct'])),'best_recent':brief(max(cs,key=lambda c:c['scenes']['3']['recent40']['net_return_pct'])),'rows':counts,'groups':{}}
 for S in SLOWS:
  group=[c for c in cs if c['BTC_trend_lookback_days']==S];summ['groups'][f'S{S}']={'configs':len(group),'passed':sum(c['status']=='passed' for c in group),'full_positive3':sum(c['scenes']['3']['net_return_pct']>0 for c in group),'recent_positive3':sum(c['scenes']['3']['recent40']['net_return_pct']>0 for c in group),'full3_range_pct':[min(c['scenes']['3']['net_return_pct'] for c in group),max(c['scenes']['3']['net_return_pct'] for c in group)],'recent3_range_pct':[min(c['scenes']['3']['recent40']['net_return_pct'] for c in group),max(c['scenes']['3']['recent40']['net_return_pct'] for c in group)],'positive_complete30d_folds1_counts':dict(Counter(c['positive_complete_30d_folds_1x'] for c in group)),'positive_recent5d_folds1_counts':dict(Counter(c['recent40_positive_5d_folds_1x'] for c in group)),'failed_criteria_counts':dict(Counter(p for c in group for p in c['failed_criteria']))}
 put(R/'summary.json',summ);ctx=json.loads((R/'context.json').read_text());fwd=json.loads((R/'forward_report.json').read_text());fv=json.loads((R/'forward_verification.json').read_text())
 lines=[f'# {R.name} BTC慢趋势约束反转＋ETH顺趋势',
 f'真实评估81个新组合、243个1/2/3倍成本场景，{summ["passed_candidates"]}通过/{summ["rejected_candidates"]}淘汰。全部先成功reserve，计算及独立核验后逐项finish；所有负收益、零收益和淘汰保留。全文读取{ctx["registry_events"]}事件/{ctx["registry_ids"]}ID和{len(ctx["prior_conclusions_read"])}份旧结论；初始16项均有真实历史证据，无缺实际结果项。30个原生组件/90原成本NAV只读恢复并核对原SHA，组件信号/撮合/资金费模型重跑0。',
 '预设BTC慢ROC S7/14/28日、短ROC L1/2/3日、入场H2/4/6%；ETH顺趋势ROC28日、入场2%，退出E0.5/1/2%。S×L×H×E完整81格四维网格，216相邻边，资产角色固定，不根据未来表现切换。本轮把ETH从反转换成顺趋势，检验其活动与BTC回撤折的组合效果，不预设负相关或改善。27个旧无BTC慢门槛组合只作同L/H/ETH_E匹配对照，原资格/登记/报告字节不变，不加入新网格重新评级。',
 'BTC完整规则：以前一完整close计算短ROC，>H空、<-H多；带内实际已有多头仅ROC<0保持、空头仅ROC>0保持，过零退出；反向极端先平后开。慢ROC>0仅允许多、<0仅空、=0全平；不兼容立即平实际仓位，不保留隐藏desired，现金重入须新严格极端。ETH以前一完整close算28日ROC，>2%多、<-2%空；带内实际多头仅ROC>-E保持，空头仅ROC<E保持；跨反向严格入场带先平后开；精确入场等号不新开、精确退出等号平仓。两币次日UTC00:01 OPEN执行，数量按前一close/lot向下取整，同向保持实际q。每个源spec/报告/完整账本SHA固定，不以过滤旧NAV代替门槛造成的真实持仓变化。',
 '原值权重1/1代表两个各10000USDT完整独立银行相加，父本金20000，每币固定2000入场预算、总4000占初始本金20%。不自动归一化、按收益缩放手数、复利、转账、交叉保证金、现金生息或父再平衡，没有额外父成交。同档绝对NAV按共同纳秒/事件轴相加，只携带已完成源样本、不插值或平均单币收益率/Sharpe。',
 '真实Binance8合并Parquet及16年度/近期原输入留忽略data，保存路径/版本/字节/SHA。连续OOS2025-10-19 UTC00:01至2026-10-24 UTC00:01共370日、33日上下文，12完整30日折＋10日尾折。完整月正折至少9/12，尾折保留但不计入门槛。近期Sep14-Oct24从日330决策前现金/仓位续接，8个连续5日折，要求至少6/8净正且所有成本总净正。无模型或未来标签拟合，purge不适用；3日初始embargo/因果执行保留，状态跨全部折不重开。历史均反复使用，不能称未触碰最终测试集。',
 '原生永续每侧5bp手续费＋1bp半价差＋2bp滑点，冲击0.5×滞后20日对数波动×sqrt(订单参考金额/滞后20日ADV)，参与率≤0.1%；原真实lot/不利tick/最小金额和独立现金约束保持。实际资金费按真实结算时点及mark对当时持仓入账，流出×成本倍数、流入不放大。永续空头以现金保证金，不虚构现货借贷。缺历史L2/排队/TCA/完整阶梯；1%维持保证金及小时不利mark高低价只作代理，分钟交易代理＋小时mark＋结算的整体DD不等于tick级清算保证。',
 '三项验证实际执行：13时间折/8近期折及完整连续OOS回撤；81格四维敏感性、216相邻边和Sharpe陡变；243新成本场景含手续费/价差/滑点/成交量冲击/资金费。其他资格门槛为3x整体DD≤25%、局部邻域3x净正≥60%、至少4往返、(参考价毛利＋资金费)/执行成本≥2.5、源现金/拒单/保证金代理违规0、各源终点空仓。原生旧报告ETH近期字段extension40按相同Sep14-Oct24区间只读识别，不改原报告。',
 f'全期1/2/3倍成本净正数量{summ["positive_configs_by_cost"]}，近期对应{summ["recent_positive_configs_by_cost"]}；失败门槛{summ["failed_criteria_counts"]}。全期最佳{summ["best_full"]}；近期最佳{summ["best_recent"]}。']
 for label,z in summ['groups'].items():lines.append(f'{label}：{z}')
 lines += ['每个新组合对照同L/H/ETH_E无BTC慢门槛旧组合及相同本金/预算恒多，486个逐成本对照完整保留；30原生＋27旧组合＋1恒多共58个旧唯一结果原状态/资格/报告字节/登记SHA不变。不同组件配对是真新配置，不因family相同排除；仅改名、组件顺序或等价数字格式不是新配置。',
 f'原冻结SMA65/对称1%、BTC1500/ETH500从上轮UTC02:30续至{fwd["cutoff_utc"]}，仅追加{fv["new_closed_marks_per_asset"]}闭合分钟mark、无新日决策/参考/成交。Oct26UTC00:01的BTC卖出已经完成，不重复执行。逐币逐成本cash/units/desired/历史费用/成交与旧{fv["original_NAV_prefix"]}点严格继承，新总{fv["NAV_points_per_scene"]}点；下一日决策2026-10-27 UTC00:01、终点2027-03-31不变。两币现金续接不从2000本金重开；现金期间NAV不变不代表新alpha。',
 '原SMA沿用历史Float手数、10bp手续费模型，不套新永续5bp/lot/tick。24日初期延迟shadow不足180日/六折，不冒充paper10真实报价模拟；partial rejected不取消冻结计划。最近65日日线上下文仍指010010/forward_inputs.json.gz及原SHA，下一日从该字典续接；当前mark-only输入仅分钟数组。',
 '本轮读取AQR官方[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)（2012-05-01）与[交易成本研究](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)（2012-12-05），访问2026-10-26。传统期货12个月趋势和股票反转成本仅作背景；BTC短期反转加慢趋势门槛与ETH28日顺趋势的组合是本轮推断，非论文复现或利润/容量移植。81相关试验基于已见历史，不称未触碰留出、DSR/PBO校正或稳定实盘盈利，不据此改变冻结账户。',
 '复现工作目录/home/desktop/Documents/Codex/EquiTide；audit.py/check_sources.py/check_alignment.py只读已finish证据；forward.py --reproduce及audit_forward.py不HTTP取数或写登记。不要重新reserve/evaluate/summarize已finish配置。真实失败留read_failures，必要门禁以实际exit为准；行情忽略data，只清本轮可重建缓存/checkpoint。普通SSH非强推main，经freshfetch/全heads/完整tree与必要blob/data/reportSHA核验后释放本轮broker；发布/释放回执留.git。']
 (R/'result.md').write_text('\n\n'.join(lines)+'\n');print(json.dumps(summ),flush=True)
if __name__=='__main__':main()
