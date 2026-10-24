"""Complete new/readonly joint surface and Chinese evidence; before registry finish."""
import csv,gzip,io,json,itertools
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run import ROOT,R,BTC_LOOKS,ETH_LOOKS,HURDLES,sha,put,grid_configs
def table(path,rows,compressed=False):
 fields=list(dict.fromkeys(k for row in rows for k in row));b=io.StringIO(newline='');w=csv.DictWriter(b,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows);raw=b.getvalue().encode();path.write_bytes(gzip.compress(raw,mtime=0) if compressed else raw)
def main():
 report=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text());grid=grid_configs(report['configs']);cs=list(report['configs'].values());anchors=json.loads((R/'anchors.json').read_text());by={(c['BTC_lookback_days'],c['BTC_return_hurdle'],c['ETH_lookback_days'],c['ETH_return_hurdle']):c for c in grid.values()};rows=[];folds=[];daily=[];cells={};edges=[]
 for c in grid.values():
  readonly=c['name'] in anchors;meta={p:c[p] for p in ['name','BTC_lookback_days','BTC_return_hurdle','ETH_lookback_days','ETH_return_hurdle']};meta['read_only_anchor']=readonly
  cells[c['name']]={**meta,'fingerprint':c['fingerprint'],'qualification_status':c['status'],'qualification_scope':'original204326grid unchanged' if readonly else 'current frozen81cellgrid','original_report':plan['anchor_source']['report'] if readonly else str((R/'report.json').relative_to(ROOT)),'positive_folds_1x':c['positive_folds_1x'],'scenes':{k:{p:z[p] for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','NAV_sha256_f64le']} for k,z in c['scenes'].items()}}
  for k,z in c['scenes'].items():
   cost={'cost_multiplier':int(k)};rows.append({**meta,**cost,'status':c['status'],'positive_folds_1x':c['positive_folds_1x'],**{p:z[p] for p in ['net_return_pct','max_drawdown_pct','daily_mark_drawdown_pct','sharpe_365','calmar','cost_usdt','funding_usdt','gross_reference_PnL_to_execution_cost','executions','round_trips','NAV_sha256_f64le']},**{'cost_'+p:v for p,v in z['cost_parts_usdt'].items()},'funding_income_usdt':z['funding_income_usdt'],'funding_outflow_usdt':z['funding_outflow_usdt'],'funding_stress_increment_usdt':z['funding_stress_increment_usdt'],'margin_independent_sleeve_violations':z['margin']['independent_sleeve_violations'],'margin_minimum_sleeve_cushion_usdt':z['margin']['minimum_individual_sleeve_cushion_usdt']})
   for f in z['folds']:folds.append({**meta,**cost,**f})
   if not readonly:
    for day,equity in enumerate(z['daily_equity_usdt']):daily.append({**meta,**cost,'boundary_index':day,'equity_usdt':equity})
 axes=[BTC_LOOKS,HURDLES,ETH_LOOKS,HURDLES]
 for params,c in by.items():
  for index,axis in enumerate(axes):
   i=axis.index(params[index])
   if i+1==len(axis):continue
   other=list(params);other[index]=axis[i+1];d=by[tuple(other)];a,b=c['scenes']['3'],d['scenes']['3'];edges.append({'from':c['name'],'to':d['name'],'axis':['BTC_L','BTC_H','ETH_L','ETH_H'][index],'from_readonly':c['name'] in anchors,'to_readonly':d['name'] in anchors,'return3_delta_pp':b['net_return_pct']-a['net_return_pct'],'sharpe3_delta':b['sharpe_365']-a['sharpe_365'],'DD3_delta_pp':b['max_drawdown_pct']-a['max_drawdown_pct']})
 table(R/'sensitivity.csv',rows);table(R/'fold_results.csv',folds);table(R/'daily_equity.csv.gz',daily,True);table(R/'joint_edges.csv',edges)
 report['joint_grid_sensitivity']={'axes':plan['grid'],'cells':cells,'new_cells':54,'read_only_old_cells':27,'old_qualification_not_rerated':True,'positive3_fraction':sum(c['scenes']['3']['net_return_pct']>0 for c in grid.values())/81,'positive_sharpe3_fraction':sum(c['scenes']['3']['sharpe_365']>0 for c in grid.values())/81,'new_positive3_fraction':sum(c['scenes']['3']['net_return_pct']>0 for c in cs)/54,'adjacent_edges':len(edges),'largest_abs_adjacent_return3_change_pp':max(abs(e['return3_delta_pp']) for e in edges),'highest3_at_lookback_boundary':(lambda c:c['BTC_lookback_days'] in (BTC_LOOKS[0],BTC_LOOKS[-1]) or c['ETH_lookback_days'] in (ETH_LOOKS[0],ETH_LOOKS[-1]))(max(grid.values(),key=lambda x:x['scenes']['3']['net_return_pct'])),'selection_limit':'Seen-history extension and reused oldcomponents;no independent final holdout,DSR/PBO or live TCA.'}
 report['failure_counts']=dict(Counter(k for c in cs for k in c['failed_criteria']))
 hold=plan['read_only_hold_reference'];assert sha(ROOT/hold['report'])==hold['report_sha256'];holdcfg=json.loads((ROOT/hold['report']).read_text())['configs'][hold['name']]
 report['read_only_same_budget_hold_reference']={**hold,'returns_by_cost':{k:z['net_return_pct'] for k,z in holdcfg['scenes'].items()},'rerun':False};put(R/'report.json',report)
 fig,axs=plt.subplots(3,3,figsize=(13,10),constrained_layout=True);vmax=max(c['scenes']['3']['net_return_pct'] for c in grid.values());vmin=min(0,min(c['scenes']['3']['net_return_pct'] for c in grid.values()))
 for i,lb in enumerate(BTC_LOOKS):
  for j,le in enumerate(ETH_LOOKS):
   ax=axs[i,j];mat=np.asarray([[by[lb,hb,le,he]['scenes']['3']['net_return_pct'] for he in HURDLES] for hb in HURDLES]);im=ax.imshow(mat,cmap='RdYlGn',vmin=vmin,vmax=vmax);ax.set_xticks(range(3),['1%','2%','4%']);ax.set_yticks(range(3),['1%','2%','4%']);ax.set_title(f'BTC L{lb} / ETH L{le}'+(' (old readonly)' if le==30 else ' (new)'));ax.set_xlabel('ETH entry hurdle');ax.set_ylabel('BTC entry hurdle')
   for a,b in itertools.product(range(3),repeat=2):ax.text(b,a,f'{mat[a,b]:.2f}%',ha='center',va='center',fontsize=9)
 fig.colorbar(im,ax=axs,label='3x cost net return (%)');fig.suptitle('Fixed 1/1 funded banks: 54 new + 27 readonly parents; seen history');fig.savefig(R/'sensitivity_surface.png',dpi=130);plt.close(fig)
 fwd=json.loads((R/'forward_report.json').read_text());audit=json.loads((R/'verification.json').read_text());ctx=json.loads((R/'context.json').read_text());best=max(cs,key=lambda c:c['scenes']['3']['net_return_pct']);qualified=[c for c in cs if c['status']=='passed'];summary={'new_parents':54,'read_only_anchors':27,'new_component_backtests':0,'new_scenes':162,'new_folds':1782,'full_grid_scenes_with_old':len(rows),'fold_rows_with_old':len(folds),'new_daily_NAV_rows':len(daily),'new_passed':len(qualified),'new_rejected':54-len(qualified),'positive_new_by_cost':report['summary']['positive_configs_by_cost'],'failure_counts':report['failure_counts'],'highest_new':{'name':best['name'],'return3':best['scenes']['3']['net_return_pct'],'DD3':best['scenes']['3']['max_drawdown_pct'],'status':best['status'],'folds1':best['positive_folds_1x']}}
 if qualified:
  q=max(qualified,key=lambda c:c['scenes']['3']['net_return_pct']);summary['highest_qualified']={'name':q['name'],'return3':q['scenes']['3']['net_return_pct'],'DD3':q['scenes']['3']['max_drawdown_pct'],'folds1':q['positive_folds_1x']}
 put(R/'summary.json',summary)
 lines=['# BTC/ETH零退出永续组合：ETH30日边界延伸至31/32日','',f"预登记54个新父组合、162成本场景、1782逐折真实组合计算；{len(qualified)}项通过当前历史门槛，{54-len(qualified)}项淘汰。另27项ETH30旧组合只读，与新项构成完整四维81格；不改旧收益、邻域或资格。18源组件共54成本NAV复用，源策略回测次数0。",'',
 'BTC回看20/25/30日，ETH回看30/31/32日，两币入场阈值分别1/2/4%，过零退出。原值权重1/1是各10000USDT的完整独立抵押账本，总本金20000，源每次入场固定名义2000。直接相加绝对净值，不自动归一化、不重复乘已分配本金、不调拨、不跨保证金抵消、不再平衡。', '',
 '源信号每日只读前一完整UTC日：r=C[i−1]/C[i−1−L]−1；空仓严格r>H做多、r<−H做空，已有多仓r>0保留、已有空仓r<0保留，零点退出；越过相反入场阈值先平后开。下一00:01真实分钟OPEN参考，数量按前日收盘和实际lot取整，不用未来价格或资金费定量。完整规则、时间、资金、成本和失败判据冻结于plan/spec。', '',
 '三项验证已实际执行：330日连续OOS，2025-10-19UTC00:01至2026-09-14UTC00:01，11×30日固定因果折，30日上下文和3日初始间隔，跨折保留现金/持仓，终点计费平仓。无拟合/未来标签，purge不适用；L32首个ROC为C32/C0，L33不能用负索引绕至未来尾部。此历史已反复研究，不能称未触碰最终测试。', '',
 '完整四维敏感性同时扰动两币回看与阈值；索引相邻邻域含自身，角点16格、中心81格。新54项门槛按本轮完整81格计算，旧27项只读原资格。所有成本净收益、混合采样整体回撤、Sharpe、Calmar和逐折见CSV，热图及216相邻边保留。旧合格全在ETH30边界，本批是在已看过历史上的边界研究；新结果排序不能称独立确认。', '',
 '成本：每侧手续费5bp、半价差1bp、滑点2bp，冲击0.5×过去20完整日日log波动×sqrt(订单名义/过去20日quote ADV)，参与率≤0.1%；Decimal28不利tick、实际lot/minNotional及开仓≤扣费后抵押1倍约束继承。1/2/3倍执行成本和负资金费支出，正资金费收入不放大。线性永续空头无需现货借币，真实settlement按−带符号q×mark×rate事后核算，不作信号。', '',
 '[Binance资金费官方说明](https://www.binance.com/en/support/faq/detail/360033525031)支持按持仓名义核算；[Mark/Last及保证金说明](https://www.binance.com/en/support/faq/detail/360033525271)支持保留mark风险边界。当前是分钟成交收盘代理、真实小时/结算mark和成交前后参考的混合净值；1%维护保证金代理按完整OOS小时多头低/空头高mark逐源检查，不等于逐tick强平/历史完整风险阶梯。缺历史VIP费率、真实L2、队列延迟、完整过滤器与真实TCA。', '',
 '[AQR作者2012时序动量研究](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)只提供传统12个月多期货自身收益动量背景；本批短期加密零退出规则是独立研究假设。官方资料于2026-10-24访问，具体版本与范围在plan保存；不声称复现论文或稳定实盘盈利。', '',
 '预设通过门槛保持：三成本净正、1倍≥8/11正折、3倍完整混合采样DD≤25%、四维局部3倍净正≥60%、1倍≥4组件往返、毛参考PnL加资金费/执行成本≥2.5、无负源抵押/拒单/任一保证金代理越界、终点空仓。passed仅表示本次历史门槛通过，仍待前向，不新增或修改账户。', '',
 '新候选失败计数（可重叠）：'+json.dumps(report['failure_counts'],ensure_ascii=False),
 f"新组合事后3倍收益最高{best['name']}：{best['scenes']['3']['net_return_pct']:+.6f}%，整体DD {best['scenes']['3']['max_drawdown_pct']:.6f}%，1倍{best['positive_folds_1x']}/11正折，状态{best['status']}。",'',
 '同预算双恒多父参考只读旧报告，其1/2/3倍为'+'/'.join(f"{holdcfg['scenes'][k]['net_return_pct']:+.6f}%" for k in ['1','2','3'])+'；现金零息为解析0。没有为参考再登记或重算。','',
 f"独立审计从源实际保存的{audit['source_recorded_trades_checked']}笔成交与{audit['source_recorded_funding_checked']}条资金费恢复完整54源NAV，匹配原SHA；再用结构化时间键独立对齐、核对162新父路径共{audit['new_parent_NAV_points_audited']}点和1944整体/逐折指标。源state_segments恢复与成交/资金费事件恢复逐点一致，合成错位测试只称合成检查，不冒充真实数据缺口。",'',
 f"原冻结SMA从{fwd['resume_utc']}续至{fwd['cutoff_utc']}，追加120闭合分钟与UTC00:01日决策参考。保持原SMA65/对称1%、1500/500原资金、每成本cash/units/desired/交易/成本及完整旧NAV前缀；仍是延迟shadow，不能冒充十策略真实报价模拟。完整日决策与追加成交数见forward_result.md。180天/六折未成熟，partial rejected不取消原2027-03-31计划。",'',
 f"已完整读取{ctx['registry_events']}事件/{ctx['registry_ids']}ID和{len(ctx['prior_conclusions_read'])}份既往结论；初始16项均有原真实ZIP/WF或finish报告，5个legacy缺新版标志不重测。54新配置逐项reserve后计算并逐项finish，所有负收益/淘汰保留。read_failures.json保留本轮误读不存在manifest文件的真实exit1与纠正，不把cat日志exit0当门禁成功。",'',
 '|BTC L/H|ETH L/H|1倍|2倍|3倍|正折1|DD3|邻域正3|状态|','|---|---|---:|---:|---:|---:|---:|---:|---|']
 for c in cs:
  s=c['scenes'];lines.append(f"|{c['BTC_lookback_days']}/{c['BTC_return_hurdle']:.0%}|{c['ETH_lookback_days']}/{c['ETH_return_hurdle']:.0%}|{s['1']['net_return_pct']:+.3f}%|{s['2']['net_return_pct']:+.3f}%|{s['3']['net_return_pct']:+.3f}%|{c['positive_folds_1x']}/11|{s['3']['max_drawdown_pct']:.3f}%|{c['sensitivity']['four_dimensional_local_3x_positive_fraction']:.1%}|{c['status']}|")
 lines+=['','重放：固定工作目录，以现有金融解释器运行本轮audit.py与forward.py verify，读取原完整行情/账本、只审计不再次reserve已finish配置。源档案和8份大Parquet留原data路径及SHA；保留完整结果和下轮状态，不为体积重写已finish字节。未提供独立最终留出、DSR/PBO、实盘成交或长期盈利证明。','']
 (R/'result.md').write_text('\n'.join(lines))
 (R/'forward_result.md').write_text('\n'.join(['# 原冻结SMA延迟shadow跨日续接','',f"{fwd['resume_utc']}→{fwd['cutoff_utc']}，新增120闭合分钟与1个日决策参考。",'组合1/2/3倍累计收益'+ '/'.join(f"{fwd['configs']['forward_snapshot_combo']['scenes'][k]['net_return_pct']:+.9f}%" for k in ['1','2','3'])+'。','每日决策：'+json.dumps(fwd['daily_decisions_by_asset'],ensure_ascii=False),'全成本新增虚拟成交数：'+str(sum(s['new_executions'] for c in fwd['configs'].values() if c.get('asset') in ('BTC','ETH') for s in c['scenes'].values())),'旧完整NAV前缀、cash/units/desired、原交易与成本逐一核对；原2027-03-31终止不变，下一UTC日决策2026-10-25T00:01:00Z。仅未成熟180天/六折的partial观察，不是十策略实时盘。','']))
 print(json.dumps(summary,ensure_ascii=False),flush=True)
if __name__=='__main__':main()
