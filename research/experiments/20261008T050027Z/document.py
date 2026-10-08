"""Report every reverse-horizon variant, cost scene, fold and uncertainty."""
import hashlib,json
from collections import Counter
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
T=Path(__file__).resolve().parent;R=T.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((T/'report.json').read_text());f=json.loads((T/'forward_report.json').read_text());h=json.loads((T/'history_paths.json').read_text());p=json.loads(__import__('gzip').decompress((T/'prior_summary.json.gz').read_bytes()));recovery=json.loads((T/'cache_recovery.json').read_text());s=r['summary'];g=r['plan']['grid']
label=lambda c:f"BTC收盘通道{c['BTC_entry_days']}/30；ETH收盘通道20/{c['ETH_exit_days']}"
lookup={(c['year'],c['BTC_entry_days'],c['ETH_exit_days']):c for c in r['configs'].values()}
qualified=[c for c in r['configs'].values() if c['year']=='2026' and c['both_periods_meet_full_gates']]
fail=Counter(k for c in r['configs'].values() if c['is_new'] for k in c['failed_criteria'])
comparison=[]
for c in r['configs'].values():
 if not c['is_new']:continue
 anchor=lookup[c['year'],20,30];a,b=c['scenes']['3'],anchor['scenes']['3']
 comparison.append({'name':c['name'],'year':c['year'],'anchor_name':anchor['name'],'return_difference_3x_pct_points':a['net_return_pct']-b['net_return_pct'],'DD_difference_3x_pct_points':a['max_drawdown_pct']-b['max_drawdown_pct'],'first_five_difference_3x_pct_points':a['first_five_fold_return_pct']-b['first_five_fold_return_pct']})
center={y:lookup[y,15,20]['status'] for y in ('2025','2026')}
notes={'report_sha256':sha(T/'report.json'),'matched_anchor_comparisons':comparison,'new_both_periods_qualified':len(s['new_both_periods_passed_combination_pairs']),'full_grid_both_periods_qualified':len(qualified),'cross_period_grid_fraction':len(qualified)/9,'predeclared_center_status':center,'decision':'Keep actual historical evidence and compare dominant BTC entry/minority ETH exit. Exact gates and all failed folds retained;boundary results,identical paths and reused history prevent an independent/stable-profit claim. Fixed paper10 accounts unchanged.'}
(T/'comparison.json').write_text(json.dumps(notes,indent=2)+'\n')
lines=[f'# BTC慢退出／ETH快退出的收盘通道组合：{T.name}','',f"16个新历史组合/48成本场景，1x净正{s['positive_1x']}、3x净正{s['positive_3x']}；{len(s['passed'])}个单年度通过、{len(s['rejected'])}个淘汰。新增跨2025/2026分别通过的设置{len(s['new_both_periods_passed_combination_pairs'])}组。两个旧双20/30年度配置及12个同预算组件只读复用。",'',
'## 事前假设与原始权重','',
'上一轮改变BTC退出与ETH入场，本轮预设相反的资产时序：BTC保持30日退出，入场10/15/20日；ETH保持20日入场，退出10/20/30日。假设占初始资金75%的BTC保留较慢退出，25%的ETH用更快退出可能减少反复波动，也可能损失分散效果。中心BTC入场15日、ETH退出20日；双20/30为已存在只读锚。完整3×3、两年份、失败门槛和截止时间在任何新组合结果之前冻结，16个新组合与3个旧SMA观察截止分别reserve成功后计算。','',
'技术指标仅为闭合UTC日收盘通道。决策i比较C[i-1]与C[i-L-1:i-1]极值，参考窗口止于i-2并排除正在比较的收盘；严格上破设多头，严格下破设现金，等号及死区保持desired。历史成交参考下一UTC00:01分钟开盘，OOS从现金开始、跨折不重置、期末计成本平仓。源组件完整规则、指纹、数据与归档哈希均保留。','',
'原BTC/ETH75%/25%表示2000USDT初始1500/500独立分仓，不自动归一化、维持比例、转账或再平衡。组件实际使用相同1500/500预算核算非线性冲击和取整；组合只将同时间轴成本后绝对NAV相加一次，不二次乘权重，不平均Sharpe或单币收益。','',
f"读取完整{p['lines']}行登记、{p['canonical']}规范定义/{len(p['records'])}保留ID、{len(p['prior_conclusions'])}轮全文结论及Freqtrade归档和640行OOS代码。初始16条均有真实结果，缺结果补测项0。首次工程预读把部分旧条目的直接report指针误当result_evidence列表，已在无新增计算/登记时恢复并保留preflight_notes.json。owner=btc-eth-2的无结果观察保留原记录，不当缺历史策略重测。",'',
'## 三项验证','',
'Walk-forward完成：2025及2026分别UTC03-18 00:01至09-14 00:01，各180天/6个连续30天诊断折；180日滚动历史、3日gap、purge0，固定规则无模型或标签拟合，无逐折/OOS调参。每场259382个分钟/执行参考点计算逐折和连续OOS整体回撤。两年独立初始资金，不跨年拼接复利；两段已反复研究，不能称未触碰最终测试集。','',
'Sensitivity完成：每年份完整3×3同时改变BTC入场与ETH退出，其他窗口/权重冻结。保留全部1/2/3成本、净收益、分钟/日回撤、Sharpe365、Calmar、六折、正收益比例、12条邻接边和描述性2sd cliff。正收益比例不等于整个邻域都通过折一致性或跨期门槛。','',
'Costs完成：手续费10bp/侧、估计半价差1bp、滑点2bp，加0.5×前20日样本波动率×sqrt(实际预算/前20日quoteADV)冲击，四项一起乘1/2/3；最大参与率0.001。Decimal28、PRICE/LOT、最低名义额、前5个闭合分钟VWAP百分价格代理及Oct1静态交易过滤均沿用。立即全额LIMIT IOC是假设，残余现金保留；现货只做多，资金费/借币不适用。缺历史盘口与TCA校准，未证明真实成交容量。','',
'固定八门槛：所有成本净正、1x至少4/6盈利折、3x分钟整体回撤≤25%、3x邻域净正≥60%、至少2次组件往返、1x毛参考PnL/执行成本≥2.5、无负余额、期末空仓。旧精确锚保持原始criteria/status，扩展表面不覆写旧登记。','',
f"失败原因计数（可重叠）：{dict(fail)}。盈利但未通过的配置、所有亏损折及成本场景均完整留档。",'',
'## 跨期合格候选和参数局限','',
f"完整9格中{len(qualified)}/9在两段均通过，其中{len(s['new_both_periods_passed_combination_pairs'])}组新设置。事前中心的状态：{center}。以下候选只保留为重复开发历史上的证据，不更换冻结10组前向账户。",'']
for c in sorted((c for c in qualified if c['is_new']),key=lambda c:-c['scenes']['3']['net_return_pct']):
 a=c['scenes']['3'];other=r['configs'][c['other_period_config']]['scenes']['3'];lines.append(f"- {label(c)}：2026三倍成本累计{a['net_return_pct']:.6f}%、分钟整体回撤{a['max_drawdown_pct']:.6f}%、前五折{a['first_five_fold_return_pct']:.6f}%；2025收益{other['net_return_pct']:.6f}%、回撤{other['max_drawdown_pct']:.6f}%。")
if not any(c['is_new'] for c in qualified):lines.append('没有新增双期合格候选；保留全部实际结果供后续比较。')
lines+=['','## 2026收益倒序（180天累计，非年化）','', '|技术指标/参数|新配置|1x收益%|2x收益%|3x收益%|3x整体分钟回撤%|1x盈利折|3x前五折累计%|2025年3x收益%|双期通过|','|---|---|---|---|---|---|---|---|---|---|']
for c in sorted((c for c in r['configs'].values() if c['year']=='2026'),key=lambda c:-c['scenes']['3']['net_return_pct']):
 a=c['scenes'];other=r['configs'][c['other_period_config']];lines.append(f"|{label(c)}|{c['is_new']}|{a['1']['net_return_pct']:.6f}|{a['2']['net_return_pct']:.6f}|{a['3']['net_return_pct']:.6f}|{a['3']['max_drawdown_pct']:.6f}|{c['positive_folds_1x']}/6|{a['3']['first_five_fold_return_pct']:.6f}|{other['scenes']['3']['net_return_pct']:.6f}|{c['both_periods_meet_full_gates']}|")
lines+=['','## 全部配置、成本与逐折结果','', '|配置|新测|状态|成本倍数|收益%|整体分钟回撤%|Sharpe365|Calmar|成本占初始%|六折净收益%|失败判据|','|---|---|---|---|---|---|---|---|---|---|---|']
for name,c in r['configs'].items():
 for k,a in c['scenes'].items():
  folds=','.join(f"{z['net_return_pct']:.5f}" for z in a['folds']);lines.append(f"|{name}|{c['is_new']}|{c['status']}|{k}|{a['net_return_pct']:.6f}|{a['max_drawdown_pct']:.6f}|{a['sharpe_365']:.6f}|{a['calmar']:.6f}|{a['cost_pct_initial']:.6f}|{folds}|{','.join(c['failed_criteria'])}|")
lines+=['','## 路径新颖性、对照与选择偏差','',f"核对全部{len(h['all_prior_report_sha256'])}份历史report及SHA；48个新场景中{h['new_scenes_already_in_any_prior_report']}条完整NAV以前出现、{h['new_scenes_not_in_any_prior_report']}条未见；2026新组合3x有{h['new_2026_combo_3x_paths_not_in_any_prior_report']}条未见路径，合格跨年全成本配对有{h['qualified_cross_period_pairs_not_in_any_prior_report']}种未见。参数或NAV哈希不同都不等于独立市场样本，多重选择偏差没有消除。",'',
'现金0收益、同期持有、SMA65、双15/30及双20/30只读比较保存在report和comparison.json。资金敞口与风险不同，不把持有差额直接当alpha。','',
'## 原SMA冻结账户：延迟shadow连续估值','',
'从Oct8 UTC02:50延续至04:50，8817个旧NAV点完整保留，追加120个闭合分钟至8937点，累计8929分钟/6个完整日。Oct8UTC00:01已处理，本轮无新日决策、参考点、成交、费用或强制平仓；现金、币数量、desired及交易历史连续，下一日决策Oct9UTC00:01，终点2027Mar31。该结果是延迟历史分钟shadow重建，采用原浮点数量模型，不计入P01–P10的真实报价Decimal模拟资金账本。','',
'|原账户|成本倍数|累计收益%|分钟整体回撤%|','|---|---|---|---|']
for name,c in f['configs'].items():
 for k,a in c['scenes'].items():lines.append(f"|{name}|{k}|{a['net_return_pct']:.6f}|{a['max_drawdown_pct']:.6f}|")
lines+=['', 'paper10 plan/state哈希保持本轮开始值，不新增、替换、重置或回填固定10组账户。3个partial旧观察rejected只表示未成熟，原计划继续。','',
'## 审计、来源、复现与留档','',
f"计算前重建{len(recovery['missing_cache_files_restored'])}个缺失只读缓存，36个源组件场景＋6个旧组合场景完整NAV哈希全部吻合，无旧信号或交易重跑。独立审计核对36个来源、54个组合成本场景及14006628个分钟NAV点，检查资金、全部费用、折复利与整体回撤；9个原SMA估值场景核对真实HTTP200响应、重叠bar、8817点旧前缀和账户连续性。",'',
'原始数据依据[Binance官方公开数据说明](https://github.com/binance/binance-public-data)（访问日2026-10-08）；2025年后的原始现货归档时间戳为微秒，冻结规范化缓存以纳秒检查，API分钟输入以毫秒检查。四个规范化行情文件的同SHA内容、时间轴与闭合状态重新核对，数据版本及哈希见data_manifest.json。','',
'16个新历史组合与3个旧截止定义实际完成，经独立审计后逐一finish。成功、淘汰、亏损折、负收益shadow和零交易均保留；Git保存轻量spec/report/成交归档、来源/哈希、CSV/图与stdout，大行情和完整NAV留忽略data缓存。','',f"复现：`bash research/experiments/{T.name}/reproduce.sh`，只使用同SHA缓存和本轮已保存输入，不HTTP或写登记。",'',
'历史门槛通过不能称稳定实盘盈利；需要独立时期和完整前向样本继续验证。']
(T/'result.md').write_text('\n'.join(lines)+'\n')
fig,axes=plt.subplots(1,2,figsize=(11,4.7),constrained_layout=True)
for ax,y in zip(axes,('2025','2026')):
 vals=np.array([[lookup[y,be,ex]['scenes']['3']['net_return_pct'] for ex in g['ETH_exit_days']] for be in g['BTC_entry_days']]);im=ax.imshow(vals,cmap='YlGnBu',aspect='auto')
 ax.set_xticks(range(3),g['ETH_exit_days']);ax.set_yticks(range(3),g['BTC_entry_days']);ax.set_xlabel('ETH exit days; ETH entry20 fixed');ax.set_ylabel('BTC entry days; BTC exit30 fixed');ax.set_title(y+' reverse channel horizons\n3x cost net return,180days; P/R=gates')
 for i,be in enumerate(g['BTC_entry_days']):
  for j,ex in enumerate(g['ETH_exit_days']):
   c=lookup[y,be,ex];tag=('P' if c['status']=='passed' else 'R')+(' old' if not c['is_new'] else '');ax.text(j,i,f'{vals[i,j]:.2f}%\n{tag}',ha='center',va='center',color='white' if vals[i,j]>np.mean(vals) else 'black')
 fig.colorbar(im,ax=ax,label='Cumulative net return (%)')
fig.savefig(T/'sensitivity.png',dpi=150);plt.close(fig)
print(json.dumps({'new_configs':16,'passed':len(s['passed']),'rejected':len(s['rejected']),'new_cross_period_qualified':len(s['new_both_periods_passed_combination_pairs']),'grid_both_periods_fraction':len(qualified)/9,'center_status':center,'full_scene_rows':54}))
