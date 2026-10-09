"""Describe actual finished guard/channel results and old matched controls; no new strategy evaluation."""
from pathlib import Path
from collections import Counter
import csv,gzip,hashlib,json,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
T=Path(__file__).resolve().parent;R=T.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((T/'report.json').read_text());cr=json.loads((T/'components_report.json').read_text());f=json.loads((T/'forward_report.json').read_text());h=json.loads((T/'history_paths.json').read_text());prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()))
assert len(json.loads((T/'reproduction_execution.json').read_text()))==8 and all(x['exit_code']==0 for x in json.loads((T/'reproduction_execution.json').read_text()))
cs=r['configs'];grid=r['plan']['grid'];comparisons=[]
for name,c in cs.items():
 on,o=next((n,x) for n,x in r['read_only_comparators'].items() if x['kind']=='MATCHED_UNGUARDED_BTC' and x['year']==c['year'] and x['ETH_channel_entry_days']==c['ETH_channel_entry_days'])
 comparisons.append({'config':name,'year':c['year'],'comparator':on,'same_initial_funding':[1500,500],'same_ETH_channel_entry_days':c['ETH_channel_entry_days'],'return_differences_pp':{k:c['scenes'][k]['net_return_pct']-o['scenes'][k]['net_return_pct'] for k in ('1','2','3')},'minute_DD3_difference_pp':c['scenes']['3']['max_drawdown_pct']-o['scenes']['3']['max_drawdown_pct'],'all_cost_NAV_identical':all(c['scenes'][k]['NAV_sha256_f64le']==o['scenes'][k]['NAV_sha256_f64le'] for k in ('1','2','3'))})
pairchecks=[]
for pair in r['summary']['new_both_periods_passed_combination_pairs']:
 rows=[next(x for x in comparisons if x['config']==n) for n in pair];ret=[v for row in rows for v in row['return_differences_pp'].values()];dd=[row['minute_DD3_difference_pp'] for row in rows]
 pairchecks.append({'pair':pair,'all_returns_nonworse_both_years':all(v>=0 for v in ret),'DD3_nonworse_both_years':all(v<=0 for v in dd),'joint_improvement_both_years':all(v>=0 for v in ret) and all(v<=0 for v in dd) and (any(v>0 for v in ret) or any(v<0 for v in dd))})
exposure={};source_signatures={}
for name,c in cr['configs'].items():
 arc=json.loads(gzip.decompress((R/c['archive']).read_bytes()));exposure[name]={'year':c['year'],'annual_volatility_ceiling':c['volatility_ceiling'],'is_new':c['is_new'],'source_archive_sha256':sha(R/c['archive']),'cost_scenes':{}}
 for k,s in arc['scenes'].items():
  exposure[name]['cost_scenes'][k]={'daily_decisions':len(s['decisions']),'high_volatility_days':sum(not d['volatility_eligible'] for d in s['decisions']),'desired_long_days':sum(d['long'] for d in s['decisions']),'invested_days':sum(st['end_day_exclusive']-st['day_offset'] for st in s['position_segments'] if float(st['units'])>0),'executions':s['summary']['executions'],'round_trips':s['summary']['round_trips']}
for ref in r['component_sources'].values():
 arc=json.loads(gzip.decompress((R/ref['archive']).read_bytes()));sig=tuple(arc['scenes'][k]['summary']['NAV_sha256_f64le'] for k in ('1','2','3'));source_signatures.setdefault(ref['year']+'_'+ref['asset'],set()).add(sig)
surfaces={}
for year in ('2025','2026'):
 cells=[c for c in cs.values() if c['year']==year];sens=r['sensitivity'][year+'_BTC_VOLGUARD_ETH_CHANNEL'];best=max(c['scenes']['3']['net_return_pct'] for c in cells);coords=[[c['BTC_annual_volatility_ceiling'],c['ETH_channel_entry_days']] for c in cells if c['scenes']['3']['net_return_pct']==best]
 surfaces[year]={'positive3_fraction':sum(c['scenes']['3']['net_return_pct']>0 for c in cells)/9,'full_gate_pass_fraction':sum(c['status']=='passed' for c in cells)/9,'descriptive_cliff_flags':sum(e['cliff_flag_2sd'] for e in sens['adjacent_edges']),'adjacent_edges':12,'best_return3_coordinates':coords,'best_on_boundary':any(cap in (.4,.6) or entry in (10,20) for cap,entry in coords),'scope':'Reused-history descriptive sensitivity,not significance/PBO/final holdout or new OOS parameter selection.'}
comparison={'report_sha256':sha(T/'report.json'),'components_report_sha256':sha(T/'components_report.json'),'matched_comparisons':comparisons,'qualified_pairs_vs_matched_controls':pairchecks,'new_both_periods_qualified':len(pairchecks),'new_qualified_pairs_jointly_improve_matched_controls':sum(c['joint_improvement_both_years'] for c in pairchecks),'failure_counts':dict(Counter(k for c in cs.values() for k in c['failed_criteria'])),'new_component_failure_counts':dict(Counter(k for c in cr['configs'].values() if c['is_new'] for k in c['failed_criteria'])),'source_component_path_signature_counts':{k:len(v) for k,v in source_signatures.items()},'guard_exposure':exposure,'surface_diagnostics':surfaces,'scope':'All18portfolios have exact1500/500USDT funding,raw75/25. Same ETH and BTC SMA thresholds as matched old controls;only BTC annual volatility guard differs. No rescaled NAV or new comparison backtest.'}
(T/'comparison.json').write_text(json.dumps(comparison,indent=2)+'\n')
with (T/'folds.csv').open('w',newline='') as fh:
 w=csv.writer(fh,lineterminator='\n');w.writerow(['config','year','kind','is_new','cost','fold','net_return_pct','minute_DD_pct','Sharpe365','Calmar'])
 for kind,doc in [('BTC_component',cr),('portfolio',r)]:
  for name,c in doc['configs'].items():
   for k,s in c['scenes'].items():
    for ff in s['folds']:w.writerow([name,c['year'],kind,c['is_new'],k,ff['fold'],ff['net_return_pct'],ff['max_drawdown_pct'],ff['sharpe_365'],ff['calmar']])
fig,axes=plt.subplots(2,3,figsize=(15,9),layout='constrained')
for j,year in enumerate(('2025','2026')):
 cells={(c['BTC_annual_volatility_ceiling'],c['ETH_channel_entry_days']):c for c in cs.values() if c['year']==year}
 for i,(key,title) in enumerate([('net_return_pct','3x cumulative net return %'),('max_drawdown_pct','3x full minute NAV drawdown %'),('sharpe_365','3x daily Sharpe (365)')]):
  ax=axes[j,i];matrix=np.array([[cells[cap,entry]['scenes']['3'][key] for entry in grid['ETH_channel_entry_days']] for cap in grid['BTC_annual_volatility_ceiling']]);im=ax.imshow(matrix,cmap='YlGnBu' if i!=1 else 'YlOrRd',aspect='auto')
  for a,cap in enumerate(grid['BTC_annual_volatility_ceiling']):
   for b,entry in enumerate(grid['ETH_channel_entry_days']):
    flag=' P' if cells[cap,entry]['status']=='passed' else ' R';ax.text(b,a,f'{matrix[a,b]:.3f}'+flag,ha='center',va='center',fontsize=10,color='white' if matrix[a,b]>(matrix.min()+matrix.max())/2 else '#111111')
  ax.set(xticks=range(3),xticklabels=grid['ETH_channel_entry_days'],yticks=range(3),yticklabels=[f'{100*x:g}%' for x in grid['BTC_annual_volatility_ceiling']],xlabel='ETH prior-close channel entry days (exit30)',ylabel='BTC annualized20-return volatility ceiling',title=year+' | '+title);fig.colorbar(im,ax=ax,fraction=.035)
fig.suptitle('BTC SMA65 +1.25%/-0.5% with volatility guard / ETH close-channel\nFrozen75/25:1500/500USDT sleeves | P/R=annual gates | reused180-day histories',fontsize=14)
fig.savefig(T/'sensitivity.png',dpi=130);plt.close(fig)
focus=[c for c in cs.values() if c['BTC_annual_volatility_ceiling']==.5 and c['ETH_channel_entry_days']==15];passed=r['summary']['passed'];rejected=r['summary']['rejected'];newleaf=[c for c in cr['configs'].values() if c['is_new']]
intro=f"4个新BTC组件/12成本场景及18个新年度组合/54成本场景全部完成；合计22个新历史配置/66场景。新组件2通过、2淘汰，组合{len(passed)}通过、{len(rejected)}淘汰；{len(pairchecks)}组跨期参数通过两段复用历史门槛。相对同资金、同ETH通道、未加BTC波动门槛的旧对照，没有同时改善两年收益与回撤的合格新设置。固定P01–P10账户保持。"
lines=['# BTC年化波动门槛SMA65 / ETH收盘通道：新组件与组合检验','',intro,'','## 预先冻结的规则、资金与时间','',
'技术指标：BTC的SMA65非对称滞回（上方1.25%入场、下方0.5%退出）和20日对数收益样本年化波动门槛40%/50%/60%；ETH的收盘通道10/15/20日入场、30日退出。3×3完整预设网格，不在看到收益后缩减。中心和关注配置均为BTC50%门槛、ETH15日。',
'决策i使用已完成收盘C[i−1]；SMA为C[i−65:i]均值。波动窗口C[i−21:i]产生20个log收益，用Decimal28样本方差ddof=1，年化波动=sqrt(365×样本方差)。波动严格高于门槛即置现金，否则依SMA阈值更新状态；恢复时C[i−1]严格高于入场水平即允许做多，无额外连续两日交叉条件，死区与相等时保留原desired。成本冲击使用未年化的lagged20日日波动，二者不可混同。',
'ETH入场比较max(C[i−entry−1:i−1])，退出比较min(C[i−31:i−1])，均排除被比较的C[i−1]。固定规则按下一UTC00:01真实历史分钟开盘模拟，末端统一平仓；不使用未来数据。',
'原始BTC/ETH75%/25%，每组2000USDT，独立1500/500袖套。剩余现金保留；不自动归一化、不维持权重、不跨币转账或再平衡，无杠杆、做空或现金收益。所有引用组件都是同金额真实核算结果，不缩放旧NAV替代新订单资金。',
'2025及2026年3月18日00:01至9月14日00:01，各180天、六个连续30天诊断折；180日滚动历史、3日gap、purge0，无模型标签或逐折拟合。历史已多次使用，是开发期跨年度对比，不是未触碰最终测试集；全部预设设置报告，不能凭当前历史排名形成新的前向业绩。',
'8条门槛：全成本净正、1×至少4/6折严格净正、连续分钟NAV的3×回撤≤25%、3×邻域正收益≥60%、1×至少2完整往返、1×毛参考盈亏/执行成本≥2.5、无负现金/数量、末端空仓。组件邻域是40/50/60，组合邻域是完整3×3；旧60%组件保留原登记结论。','',
'## 三项验证','',f"1. 时间walk-forward已执行：新组件2/4与组合{len(passed)}/18通过全部门槛。2个新BTC2026组件分别仅2/6、3/6折净正；5个淘汰组合均未达到4/6折。逐折收益、回撤、Sharpe、Calmar完整保存在folds.csv和JSON，包含零收益及负收益折。",f"2. 参数敏感性已执行：每年9组合、12相邻边，2025/2026的3×正收益占比均100%，完整门槛通过率分别100%/{100*surfaces['2026']['full_gate_pass_fraction']:.3f}%；描述性陡峭边分别{surfaces['2025']['descriptive_cliff_flags']}/{surfaces['2026']['descriptive_cliff_flags']}，最佳3×收益点都在边界。邻域净正不等于稳健最优。",'3. 1/2/3×成本压力已执行：66个新历史场景均为正收益，费用、半点差、滑点、成交量冲击均同比放大，价格tick/数量LOT舍入单独计账。新组件与组合核算分别独立审计2160次因果决策、114次虚拟历史成交及全部分钟NAV；8阶段只读复现与登记检查均退出0。','',
'## 新BTC组件及旧60%只读参考','', '| 年份 | BTC年化上限 | 新/旧 | 1×净收益% | 2× | 3× | 3×分钟回撤% | 1×正折 | 高波动天/180 | 实际持仓天/180 | 1×成交/往返 | 结论 |','|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|']
for c in sorted(cr['configs'].values(),key=lambda x:-x['scenes']['1']['net_return_pct']):
 z=c['scenes']['1'];e=exposure[c['name']]['cost_scenes']['1'];lines.append(f"| {c['year']} | {100*c['volatility_ceiling']:g}% | {'新' if c['is_new'] else '旧只读'} | {z['net_return_pct']:.6f} | {c['scenes']['2']['net_return_pct']:.6f} | {c['scenes']['3']['net_return_pct']:.6f} | {c['scenes']['3']['max_drawdown_pct']:.6f} | {c['positive_folds_1x']}/6 | {e['high_volatility_days']} | {e['invested_days']} | {z['executions']}/{z['round_trips']} | {c['status']} |")
lines+=['','40%和50%门槛确实改变持仓和成本；2026的60%门槛没有触发，不能把与无门槛基准相同的NAV算独立经济进展。降至40%/50%使2026分别74/16天处于高波动区，仍没有改善匹配对照的全成本收益。','', '## 年度组合按1×成本后累计收益倒序','', '| 年份 | BTC波动门槛 | ETH入场/退出 | 原始BTC/ETH | 1×净收益% | 2× | 3× | 3×分钟回撤% | Sharpe3 | 正折1 | 成交/往返1 | 成本1USDT（手续费/冲击） | 结论 |','|---|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|']
for c in sorted(cs.values(),key=lambda x:-x['scenes']['1']['net_return_pct']):
 z=c['scenes']['1'];s=c['scenes']['3'];cp=z['cost_parts_usdt'];lines.append(f"| {c['year']} | {100*c['BTC_annual_volatility_ceiling']:g}% | {c['ETH_channel_entry_days']}/30 | 75/25 | {z['net_return_pct']:.6f} | {c['scenes']['2']['net_return_pct']:.6f} | {s['net_return_pct']:.6f} | {s['max_drawdown_pct']:.6f} | {s['sharpe_365']:.6f} | {c['positive_folds_1x']}/6 | {z['executions']}/{z['round_trips']} | {z['cost_usdt']:.6f}（{cp['fee']:.6f}/{cp['impact']:.6f}） | {c['status']} |")
lines+=['','所有行技术指标相同类别，具体参数按表；1/2/3倍每项成本拆分、Calmar、首5折与第6折、日采样回撤与连续分钟整体回撤均在report.json；组合完整54行敏感性表为sensitivity.csv。','', '## 预定关注点与匹配旧对照','']
for c in focus:
 z=c['scenes']['3'];d=next(x for x in comparisons if x['config']==c['name']);lines.append(f"- {c['year']}中心BTC50%/ETH15：1/2/3×净收益{c['scenes']['1']['net_return_pct']:.6f}%/{c['scenes']['2']['net_return_pct']:.6f}%/{z['net_return_pct']:.6f}%，3×分钟回撤{z['max_drawdown_pct']:.6f}%，{c['positive_folds_1x']}/6折净正；3×收益较匹配无门槛旧配置差{d['return_differences_pp']['3']:.6f}个百分点，回撤差{d['minute_DD3_difference_pp']:.6f}个百分点。")
lines+=['',f"4组两期合格参数中，同时改善匹配对照两期全成本收益与3×回撤的新设置{comparison['new_qualified_pairs_jointly_improve_matched_controls']}组。2025三种波动门槛均降低匹配收益，2026的40%/50%亦降低；60%在2026全成本NAV与旧无门槛完全相同。满足绝对正收益门槛仍不构成值得替换的改进。",f"完整分钟路径核对：54个新组合场景中{h['new_scenes_already_in_any_prior_report']}已有路径、{h['new_scenes_not_in_any_prior_report']}此前未见；合格跨期配对有{h['qualified_cross_period_pairs_not_in_any_prior_report']}种此前未见路径。指纹是新配置，路径不同也不自动构成独立样本或有效alpha。这里路径库比较历次report.json组合/组件，不将本轮components_report纳入先前证据。",'8个旧实际组件只读复用或从归档position_segments精确恢复缓存，4个新BTC组件实际执行；主报告沿用的reused_component_configs=12字段代表被组合引用的全部12个来源，准确新旧拆分以plan.total_component_configs=12、plan.reused_component_configs=8、is_new_component及4个新组件登记为准。已有对照的指纹、金额与原结论不变。','',
'## 成本、数据、证据边界','', '每侧10bp手续费、1bp估计半点差、2bp估计滑点，另含0.5×前20个完整日未年化样本log波动×sqrt(实际预算/前20日quoteADV)；最大参与率0.001。PRICE_FILTER不利方向取整，LOT向下取整，最低名义额和前5个已完成分钟VWAP价格约束检查；1/2/3×四项成本同比放大。无资金费或借币。',
'Oct1交易规则静态快照应用于历史期是估计假设；历史没有L2、真实TCA、队列、部分成交或真实IOC接单证据。真实1分钟数据仅支持价格路径与该模型的虚拟核算；正收益回测不表示稳定实盘盈利。4份525600行parquet的路径/SHA、两份双币日聚合来源及哈希、输入/代码/归档哈希均在spec.json及两份报告中；不提交大行情或NPY。','',
'## 原SMA延迟shadow与真实报价模拟盘','',f"原SMA65冻结延迟shadow仅追加05:00→07:00 UTC的120个闭合分钟mark，连续{10499}分钟、完整7天，每场景10508点；新日线决策/参考/成交均0，下次日线决策2026-10-10T00:01:00Z。未重置现金、数量、desired、成本或交易，10388点旧NAV前缀完全相同。3×累计净收益{f['configs']['forward_snapshot_combo']['scenes']['3']['net_return_pct']:.6f}%。这是延迟历史分钟shadow，不是10组真实报价前向资金表现。",'固定P01–P10真实行情账户保持第19次观察状态，最后真实报价观察2026-10-09T06:55:41.425683Z，累计36.389939小时，10个主账户合计19947.864082USDT、净亏52.135918USDT（−0.260680%），4笔累计主账户买入、0卖出。10组指标/规则/本金/仓位不变，本研究轮不产生paper10成交；180天前向评审未成熟。网页只读汇总研究及既有账户。','',
'## 复现与归档','', '```bash',f'.venv/bin/python research/experiments/{T.name}/replay_verify.py','```','', '该命令核验12个新BTC成本场景、24个旧来源缓存场景、54个新组合场景和9个原shadow场景；无HTTP，无登记写入或模拟盘账户写入。初次行情GET只用于原shadow新增2×120个闭合分钟。25个配置独立reserve在各自实际计算之前，三份报告各自finish；现有初始16条全有实际归档证据，本轮没有用代码检查冒充补测。',
'本轮不晋升替换候选；保留全部正收益、负收益/零收益折、5个被淘汰组合、2个被淘汰新BTC和3个未成熟shadow cutoff。后续可研究不同风险控制机制，但先登记完整新规则；重复历史上绝对收益高的配置不能冒充新前向验证。']
lines+=['','## 网页汇总漏项修复','', '首次快照仅按*/report.json发现报告，4个已登记且有真实结果的新BTC组件使用components_report.json，因此2330个历史配置中仅2221条进入收益榜。针对真实登记报告的回归检查先失败（monitor_nondefault_red.log），随后扩展为同时读取登记簿指向的研究目录内JSON；文件哈希匹配仍为准入条件。新组件补入后收益榜2225条，原2221条的每项指标、既有rounds及模拟盘状态均不变；补充报告不重复创建研究轮次。monitor_fix_check.json记录逐条比较证据，checks/monitor_snapshot.py再次通过。']
(T/'result.md').write_text('\n'.join(lines)+'\n');(T/'forward_result.md').write_text('# 原SMA延迟shadow续接\n\n'+lines[lines.index('## 原SMA延迟shadow与真实报价模拟盘')+2]+'\n')
readme=R/'research/automation/README.md';text=readme.read_text();heading='## 最近研究记录\n'
entry=f'- [{T.name}](../experiments/{T.name}/result.md)：BTC SMA65+年化20日波动40/50/60%与ETH收盘通道10/15/20–30日，原始75/25。4新BTC组件+18新组合/66成本场景全部实算，组件2通过2淘汰、组合13通过5淘汰，4组参数两期合格；全成本净正但均未改善匹配旧无门槛对照两期收益/回撤。关注50%/15日的3×两期收益34.725182%/19.115834%，分钟回撤12.378160%/11.465064%。25配置均登记finish；原shadow仅续120分钟、无新成交，固定10组真实报价账户未改。\n'
if entry not in text:
 if heading in text:text=text.replace(heading,heading+'\n'+entry,1)
 else:text+='\n'+heading+'\n'+entry
 readme.write_text(text)
print(json.dumps({'combination_passed':len(passed),'combination_rejected':len(rejected),'component_passed':len(cr['summary']['passed']),'component_rejected':len(cr['summary']['rejected']),'matched_improvements':comparison['new_qualified_pairs_jointly_improve_matched_controls'],'surfaces':surfaces},ensure_ascii=False))
