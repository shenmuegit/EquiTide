"""Complete Chinese report for frozen mixed-channel horizon portfolios."""
import hashlib,json
from pathlib import Path
from collections import Counter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
T=Path(__file__).resolve().parent;R=T.parents[2]
r=json.loads((T/'report.json').read_text());f=json.loads((T/'forward_report.json').read_text());h=json.loads((T/'history_paths.json').read_text());recovery=json.loads((T/'cache_recovery.json').read_text());s=r['summary'];g=r['plan']['grid']
label=lambda c:f"BTC收盘通道20/{c['BTC_exit_days']}；ETH收盘通道{c['ETH_entry_days']}/30"
lookup={(c['year'],c['BTC_exit_days'],c['ETH_entry_days']):c for c in r['configs'].values()};qualified=[c for c in r['configs'].values() if c['year']=='2026' and c['both_periods_meet_full_gates']];fail=Counter(k for c in r['configs'].values() if c['is_new'] for k in c['failed_criteria'])
comparison=[]
for c in r['configs'].values():
 if not c['is_new']:continue
 anchor=lookup[c['year'],30,20];a,b=c['scenes']['3'],anchor['scenes']['3']
 comparison.append({'name':c['name'],'year':c['year'],'anchor_name':anchor['name'],'return_difference_3x_pct_points':a['net_return_pct']-b['net_return_pct'],'DD_difference_3x_pct_points':a['max_drawdown_pct']-b['max_drawdown_pct'],'first_five_difference_3x_pct_points':a['first_five_fold_return_pct']-b['first_five_fold_return_pct']})
notes={'report_sha256':hashlib.sha256((T/'report.json').read_bytes()).hexdigest(),'matched_anchor_comparisons':comparison,'new_both_periods_qualified':len(s['new_both_periods_passed_combination_pairs']),'full_grid_both_periods_qualified':len(qualified),'cross_period_grid_fraction':len(qualified)/9,'predeclared_center_status':{y:lookup[y,20,15]['status'] for y in ('2025','2026')},'decision':'Retain new historical candidates with lower drawdown and improved earlier2026 returns;center fails2025 and qualifying cells lie at BTC-exit boundaries. No parameter changes or additions to frozen paper10 accounts;no stable live profit claim.'}
(T/'comparison.json').write_text(json.dumps(notes,indent=2)+'\n')
lines=[f'# BTC/ETH不同通道周期组合：{T.name}','',f"16个新历史组合/48成本场景，1x净正{s['positive_1x']}、3x净正{s['positive_3x']}；{len(s['passed'])}个单年度通过、{len(s['rejected'])}个淘汰。新增跨2025/2026分别通过的设置{len(s['new_both_periods_passed_combination_pairs'])}组，旧双20/30组合2个年度配置/6场景只读，12个同预算组件/36场景只读复用。",'', '## 事前假设、规则、权重和去重','', '旧BTC通道20/10在2026较快退场、前五折较好，却缺盈利折；ETH通道15/30的第四折与BTC快退场不同。本轮预设BTC入场20日/退出10、20、30日×ETH入场10、15、20日/退出30日，检验不同持有周期能否缓和负收益折与回撤。中心BTC退出20日、ETH入场15日；双20/30是已存在只读锚。完整3×3网格、两个年份、成本和八门槛在结果之前冻结，16个新组合与3个原账户截止配置均先reserve成功后计算。','', '技术指标仅为已闭合UTC日收盘价最高/最低通道。决策i比较C[i-1]与C[i-L-1:i-1]极值，参照区间止于i-2并排除被比较收盘；严格上破设多头，严格下破设现金，其余及等号保持desired。下一UTC00:01真实分钟open为历史执行参考；OOS起点空仓，跨折不重置，末端计成本退出。没有EMA、SMA过滤、杠杆、止损或事后调参。','', '原BTC/ETH75%/25%表示2000USDT初始1500/500独立分仓，不自动归一化、维持比例、跨币转账或再平衡。原组件在恰好1500/500资金上实际计算预算相关冲击和LOT/PRICE取整；新组合只把同时间轴、已计各自成本的绝对NAV相加一次，不二次乘权重或平均Sharpe。','', '读取完整4771行登记、2336规范定义/2338保留ID、58轮全文结论、既有Freqtrade结果与640行OOS检查；初始16均有实际证据，无缺结果补测项。前期硬编码读取174933下不存在的20/30spec，确认该锚已只读复用154903原spec/archive后按report中的显式路径恢复；无计算前产出或重复回测，说明保存在preflight_notes.json。既有paper失败观察归owner单独保留，未伪补成历史结果。','', '## 三项验证和固定门槛','', 'Walk-forward完成：2025、2026分别UTC03-18 00:01至09-14 00:01，各180天/6个连续30天折；180日滚动历史、3日gap、purge0，无模型/标签或OOS/逐折拟合。每场259382个分钟/执行参考点计算逐折与连续OOS整体回撤；两年独立初始资金，不拼为跨年复利。两段反复用于开发，不是未触碰的最终测试集。','', 'Sensitivity完成：每年份完整3×3，同时变化BTC退出周期与ETH入场周期，其他窗口/权重固定。保存全部1/2/3成本的净收益、分钟/日回撤、Sharpe365、Calmar、六折、盈利比例、12条邻接边及描述性2sd cliff。不同完整NAV不等于独立市场样本，边界较好不代表已找到普适最优。','', 'Costs完成：手续费10bp/侧、估计半价差1bp、滑点2bp，加0.5×前20日样本sigma×sqrt(实际预算/前20日quoteADV)冲击，全部项乘1/2/3；最大ADV参与率.001。Decimal28、PRICE/LOT、最低名义额、此前5闭合分钟VWAP代理及Oct1静态交易过滤保持。全额立即LIMIT IOC成交是假设，剩余现金保留；现货仅做多，借币/资金费不适用。缺历史盘口与TCA校准，未证明真实容量。','', '固定八门槛：所有成本净正、1x至少4/6盈利折、3x整体分钟回撤≤25%、3x邻域净正≥60%、至少2个组件往返、1x毛参考PnL/执行成本≥2.5、无负余额、末端空仓。旧精确锚原状态/criteria保持，扩展表面不覆写旧登记。', '', f"失败原因计数（可重叠）：{dict(fail)}。全段正收益且失败的配置也完整保留，不能把盈利折不足隐去。",'', '## 新跨期合格候选与参数局限','', f"完整9格中{len(qualified)}/9在两段均通过，其中3组新配置、1组旧锚。事前中心BTC20/20＋ETH15/30在2025未过盈利折门槛；合格设置位于BTC退出10或30日边界，因此不能宣称整个邻域稳健。",'', 'BTC20/10＋ETH15/30在2026三倍成本下收益16.723031%、分钟整体回撤9.115551%、前五折复合+5.775442%、末折+10.349840%；2025收益41.975119%、回撤10.668964%。相对旧双20/30，2026收益25.110363%、回撤11.951882%、前五折+1.000161%，新快退场降低回撤、改善前期收益并牺牲全段收益。BTC20/10＋ETH20/30也双期通过；这些是保留的历史候选，仍受重复研究与选择偏差影响。','', '## 2026收益倒序（180天累计，非年化；原权重75%/25%）','', '|技术指标/参数|新配置|1x收益%|2x收益%|3x收益%|3x分钟整体回撤%|1x盈利折|3x前五折累计%|2025年3x收益%|跨两段门槛|','|---|---|---|---|---|---|---|---|---|---|']
for c in sorted((c for c in r['configs'].values() if c['year']=='2026'),key=lambda c:-c['scenes']['3']['net_return_pct']):
 a=c['scenes'];other=r['configs'][c['other_period_config']]
 lines.append(f"|{label(c)}|{c['is_new']}|{a['1']['net_return_pct']:.6f}|{a['2']['net_return_pct']:.6f}|{a['3']['net_return_pct']:.6f}|{a['3']['max_drawdown_pct']:.6f}|{c['positive_folds_1x']}/6|{a['3']['first_five_fold_return_pct']:.6f}|{other['scenes']['3']['net_return_pct']:.6f}|{c['both_periods_meet_full_gates']}|")
lines+=['','## 全部配置、成本与逐折结果','', '|配置|新测|状态|成本倍数|收益%|整体分钟回撤%|Sharpe365|Calmar|成本占初始%|六折净收益%|失败判据|','|---|---|---|---|---|---|---|---|---|---|---|']
for n,c in r['configs'].items():
 for k,a in c['scenes'].items():
  folds=','.join(f"{x['net_return_pct']:.5f}" for x in a['folds']);lines.append(f"|{n}|{c['is_new']}|{c['status']}|{k}|{a['net_return_pct']:.6f}|{a['max_drawdown_pct']:.6f}|{a['sharpe_365']:.6f}|{a['calmar']:.6f}|{a['cost_pct_initial']:.6f}|{folds}|{','.join(c['failed_criteria'])}|")
lines+=['', '## 路径新颖性与比较对象','', f"核对全部{len(h['all_prior_report_sha256'])}份历史report及SHA；48新成本场景中{h['new_scenes_already_in_any_prior_report']}条NAV此前出现、{h['new_scenes_not_in_any_prior_report']}条未见；2026新组合3x共{h['new_2026_combo_3x_paths_not_in_any_prior_report']}条未见路径，合格跨年全成本配对{h['qualified_cross_period_pairs_not_in_any_prior_report']}种未见。全时段金额NAV哈希不同仍不是独立市场证据，多重选择偏差未消除。",'', '现金收益0、同期持有、SMA65、双15/30和双20/30只读比较保存在report，资金敞口与风险不同，不能把持有差额直接当alpha。', '', '## 原SMA冻结账户：延迟shadow连续估值','', '从Oct8 UTC00:50延续至02:50，8697个旧NAV点完整保留，追加120个闭合分钟至8817点，累计8809分钟/6个完整日。Oct8UTC00:01决策已经处理，本轮没有新日决策、参考点、成交或费用；原现金/币数量/desired及历史交易保留，下一日决策Oct9UTC00:01、终点2027Mar31均不变。', '', '|原账户|成本倍数|累计收益%|分钟整体回撤%|','|---|---|---|---|']
for name,c in f['configs'].items():
 for k,a in c['scenes'].items():lines.append(f"|{name}|{k}|{a['net_return_pct']:.6f}|{a['max_drawdown_pct']:.6f}|")
lines+=['', '上述是原SMA规则依据实际分钟行情的延迟shadow重建，采用原冻结浮点数量模型；不计入P01–P10的Decimal真实报价前向账本。本轮paper10 plan/state哈希保持原值，不新增、替换或重启固定10组账户。3个partial观察rejected仅表示没有180天/六折资格，原长期计划继续。', '', '## 审计、缓存、复现与留档','', f"生产计算前重建{len(recovery['missing_cache_files_restored'])}个缺失只读缓存，36个来源组件场景＋6个旧组合场景全部NAV哈希吻合；没有重跑旧信号或交易。独立审计重建36个来源成本场景、54个组合场景/14006628分钟NAV点，核对资金恒等式、费用、逐折复利与整体回撤；9个原账户估值场景核对真实HTTP200原始响应、重叠bar、8697点旧前缀和账户连续性。",'', '16个新历史组合与3个原观察截止定义实际完成，经审计后finish；成功、淘汰、亏损折、原账户负收益和零交易均留档。Git保存spec、report、压缩成交、输入/数据哈希、CSV、图、stdout和验证记录；大行情及完整NAV缓存留在忽略data目录。', '', f"复现：`bash research/experiments/{T.name}/reproduce.sh`。使用同SHA真实缓存和本轮真实已保存输入，不HTTP、写登记或生成开始之前的纸盘订单。",'', '保留新的不同周期历史候选，继续检验独立时期；固定10组真实报价模拟盘仍按原计划积累180天。正收益回测与历史门槛通过不能称稳定实盘盈利。']
(T/'result.md').write_text('\n'.join(lines)+'\n')
fig,axes=plt.subplots(1,2,figsize=(11,4.7),constrained_layout=True)
for ax,y in zip(axes,('2025','2026')):
 vals=np.array([[lookup[y,x,e]['scenes']['3']['net_return_pct'] for x in g['BTC_exit_days']] for e in g['ETH_entry_days']]);im=ax.imshow(vals,cmap='YlGnBu',aspect='auto')
 ax.set_xticks(range(3),g['BTC_exit_days']);ax.set_yticks(range(3),g['ETH_entry_days']);ax.set_xlabel('BTC exit days; BTC entry20 fixed');ax.set_ylabel('ETH entry days; ETH exit30 fixed');ax.set_title(y+' mixed close-channel horizons\n3x cost net return,180days; P/R=gates')
 for i,e in enumerate(g['ETH_entry_days']):
  for j,x in enumerate(g['BTC_exit_days']):
   c=lookup[y,x,e];tag=('P' if c['status']=='passed' else 'R')+(' old' if not c['is_new'] else '');ax.text(j,i,f'{vals[i,j]:.2f}%\n{tag}',ha='center',va='center',color='white' if vals[i,j]>np.mean(vals) else 'black')
 fig.colorbar(im,ax=ax,label='Cumulative net return (%)')
fig.savefig(T/'sensitivity.png',dpi=150);plt.close(fig)
print(json.dumps({'new_configs':16,'passed':len(s['passed']),'rejected':len(s['rejected']),'new_cross_period_qualified':len(s['new_both_periods_passed_combination_pairs']),'grid_both_periods_fraction':len(qualified)/9,'center2025':lookup['2025',20,15]['status'],'full_scene_rows':54}))
