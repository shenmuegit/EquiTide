"""Render current span sensitivity and all actual fold/cost outcomes from retained reports."""
import json,gzip,collections
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
T=Path(__file__).resolve().parent
r=json.loads((T/'report.json').read_text());f=json.loads((T/'forward_report.json').read_text());s=r['summary'];d=json.loads((T/'diagnostic.json').read_text());h=json.loads((T/'history_paths.json').read_text());p=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));g=r['plan']['grid']
lines=['# BTC/ETH研究：'+T.name,'',f"新历史配置36个/108成本场景；18个EMA50旧配置/54场景只读。1x净正{s['positive_1x']}、3x净正{s['positive_3x']}；单年度通过{len(s['passed'])}、淘汰{len(s['rejected'])}；新增跨两段历史合格组合参数{len(s['new_both_periods_passed_combination_pairs'])}组。",'', '## 假设、固定规则与事前登记','', '上轮20日窗口的2025表现恶化、无跨年度合格参数；本轮预设相邻窗口查验突变，本轮测试EMA更快22日/更慢78日，旧50日只读。预设入场10/15/20日×EMA22/50/78日，固定退出30日、对称带宽3%、总资金2000USDT；规则、成本、两个年份时间边界、门槛和完整3×3邻域先冻结。36新历史和3新观察定义各自reserve成功后才计算。', 'BTC/ETH原资金占比67.5%/32.5%对应1350/650USDT独立账户，没有自动归一化、恒定敞口、资金转移或再平衡。组合仅相加同轴已计各自实际成本的绝对NAV一次，不平均收益或Sharpe。', '每日UTC00:01用真实分钟开盘执行，只使用刚完成的C[i-1]；通道极值截止i-2。若C[i-1]低于此前30日最小收盘或EMA[i-1]×0.97，优先现金；否则收盘高于此前entry日最大收盘且高于EMA×1.03才desired多头；其余与等号保持。EMA按alpha2/(span+1)、首日收盘初始化、adjust=False递推；逐折不重置。OOS起点空仓，末端成本平仓。', '', '## 三项验证','', 'Walk-forward：2025/2026各UTC Mar18 00:01—Sep14 00:01，共180日、6×30日连续折；滚动180日历史/3日gap。无拟合或标签，purge0；固定因果规则不在OOS上优化。每折以及完整逐分钟NAV整体回撤均保存，两段分别判断，不把重置的两年拼成同一账户。历史反复用于开发，不是未触碰最终留出。', 'Sensitivity：入场周期与EMA窗口同时变化，全部9格/每币种每年份每成本保存净收益、Sharpe365、Calmar、分钟/日回撤。报告包含收益/Sharpe正值比例、12条邻接边及描述性2sd cliff；图的轴标签直接来自冻结grid并断言。边界较好只是描述，没有独立最优或统计显著性结论。', 'Costs：手续费10bp、半价差1bp、滑点2bp、冲击0.5×过去20日样本sigma×sqrt(实际预算/过去20日quoteADV)，四项同时乘1/2/3；最高ADV参与率.001。Decimal28、PRICE/LOT舍入、最低名义额、Oct1静态交易过滤及此前5闭合分钟VWAP百分价格代理；IOC全成交假设，剩余现金保留，拒单保持原状态并按次日desired重试。多头现货，无永续/空头，资金费/借币N/A；没有真实盘口、TCA校准或实盘容量证明。', '八门槛保持：全成本正收益、1x至少4/6正收益折、3x完整分钟回撤≤25%、3x邻域净正比例≥60%、至少2轮完整交易、1x毛参考PnL/成本≥2.5、无负余额违规及末端平仓。现金/同期持有只读比较保留，持有不作为等风险alpha基准。', '', '## 筛选与全历史路径比对','',f"淘汰原因计数（可重叠）：{d['failure_counts']}。与匹配旧50日锚相比，108新场景中{d['identical_new_scenes_to_matching_old_band3pct']}条完整NAV相同。", f"核对全部{len(h['all_prior_report_sha256'])}份历史report及SHA，108新场景中{h['new_scenes_already_in_any_prior_report']}条NAV曾出现，{h['new_scenes_not_in_any_prior_report']}条未见于过去report。2026新组合3x净值中全历史未见路径数{h['new_2026_combo_3x_paths_not_in_any_prior_report']}；合格跨年度新完整NAV配对{h['qualified_cross_period_pairs_not_in_any_prior_report']}种。参数或净值新颖性不等于独立市场证据，多重试验选择偏差未消除。",f"2026组合3x前五折累计范围/实际值：{d['all_2026_combo_first5_3x_return_pct']}%；这是五折复合收益，不表示各折同号。",'', '|年份|entry15 EMA日数|3x180日收益%|分钟整体回撤%|前五折累计%|状态|','|---|---|---|---|---|---|']

lines.insert(lines.index('|年份|entry15 EMA日数|3x180日收益%|分钟整体回撤%|前五折累计%|状态|')-1,'entry15组合22日窗口：2026三倍收益25.16625%、回撤12.24154%、前五折+0.37492%，完整NAV与25日旧路径相同；2025收益38.53929%、回撤21.65267%，盈利折数不足淘汰。78日2026前五折-5.42337%且折一致性失败。本轮无新跨年度合格参数，窗口22至25之间仍敏感，不能把2026单年较好表现视作稳定方法。')
for c in r['configs'].values():
 if c['role']=='combination' and c['entry_days']==15:
  z=c['scenes']['3'];lines.append(f"|{c['year']}|{c['span_days']}|{z['net_return_pct']:.6f}|{z['max_drawdown_pct']:.6f}|{z['first_five_fold_return_pct']:.6f}|{c['status']}|")
lines+=['','## 全参数、成本和逐折结果','','|配置|入场日|EMA日|新测|状态|成本倍数|净收益%|整体分钟回撤%|六折收益%|失败门槛|','|---|---|---|---|---|---|---|---|---|---|']
for n,c in r['configs'].items():
 for k,z in c['scenes'].items():lines.append(f"|{n}|{c['entry_days']}|{c['span_days']}|{c['is_new']}|{c['status']}|{k}|{z['net_return_pct']:.6f}|{z['max_drawdown_pct']:.6f}|{','.join(format(x['net_return_pct'],'.5f') for x in z['folds'])}|{','.join(c['failed_criteria'])}|")
lines+=['','## 原冻结模拟续接','',f"原SMA65±1%、BTC75%/ETH25%浮点模型续接234041账户：UTC Oct5 23:10—Oct6 01:10。5714点旧NAV前缀保留，增加120闭合分钟及1日执行参考至5835点；累计5829分钟（97小时9分、4完整日）。Oct6UTC00:01使用真实65根已闭合日线及过去20日成本输入，具体动作：{f['daily_decisions_by_asset']}。各成本现金、数量、desired、成交与费用按原规则续接；未改变原冻结规则或强平。下一决策Oct7UTC00:01，长期终点2027Mar31不变。",'', '|观察配置|成本倍数|累计收益%|整体回撤%|','|---|---|---|---|']
for n,c in f['configs'].items():
 for k,z in c['scenes'].items():lines.append(f"|{n}|{k}|{z['net_return_pct']:.6f}|{z['max_drawdown_pct']:.6f}|")
lines+=['', '原观察实际结果仍只是一段延迟shadow重建，未下真实订单，没有实时执行证明。3个新截止定义9场景finish rejected因不足180日/六折，不取消长期计划，短期盈亏不能证明稳定盈利。','','## 完整证据与复现','',f"读完整{p['lines']}行登记、{p['canonical']}规范定义/{len(p['records'])}保留ID、{len(p['prior_conclusions'])}轮既往结论、Freqtrade归档/CSV及4个OOS检查；所有初始16均有真实结果，没有缺结果补测项。18旧锚原始record/report/spec/archive哈希保留。",f"独立重建162成本场景、42019884分钟净值点、19440决策、72当前/未来收盘扰动、{s['audited_component_fills']}成交（{s['actual_component_fills']}新成交）；独立Pandas EMA与Decimal交易成本重算通过。4份525600分钟parquet的SHA、闭合与UTC纳秒连续性核对。观察9场景独立核对6次日线状态判断、64根日线重叠、真实分钟参考和必要成本成交；原始HTTP200响应/URL/取得时间/SHA及账户前缀留档。",'冻结spec的资格说明沿用3完整日字样，但5829分钟实际为4完整日；以独立审计与forward_report为准，spec_initial及artifact_notes保留说明，未改变规则、截止时间或登记定义。', '39个新定义均先reserve、真实计算及两审计通过再finish。成功、负收益折和淘汰结果全保留；spec、report、压缩交易归档、数据manifest/哈希、源码、CSV、图、stdout、中文结论及verification留档，分钟行情/NAV缓存仅在忽略data目录。', f"复现命令：`bash research/experiments/{T.name}/reproduce.sh`，108新场景、54旧只读和9观察/nextstate精确重放，不HTTP或写登记。",'没有独立多重比较显著性验证；正收益回测不等于稳定实盘盈利。下一轮从实际折一致性决定预设EMA窗口或退出条件，不追认本轮排名为最优，不改变原冻结模拟。']
(T/'result.md').write_text('\n'.join(lines)+'\n')
entries=g['entry_lookback_days'];spans=g['EMA_span_days'];assert spans==[22,50,78]
values=[c['scenes']['3']['net_return_pct'] for c in r['configs'].values()];lo=min(0,min(values));hi=max(values);fig,axes=plt.subplots(2,3,figsize=(13,7))
for i,y in enumerate(('2025','2026')):
 for j,a in enumerate(('BTC','ETH','combination')):
  cells={(c['span_days'],c['entry_days']):c for c in r['configs'].values() if c['year']==y and c.get('asset','combination')==a};v=np.array([[cells[w,e]['scenes']['3']['net_return_pct'] for e in entries] for w in spans]);ax=axes[i,j];ax.imshow(v,cmap='YlGn' if lo>=0 else 'RdYlGn',vmin=lo,vmax=hi)
  for ii,w in enumerate(spans):
   for jj,e in enumerate(entries):ax.text(jj,ii,f'{v[ii,jj]:.2f}%',ha='center',va='center')
  ax.set_xticks(range(len(entries)),entries);ax.set_yticks(range(len(spans)),spans);assert [int(x.get_text()) for x in ax.get_yticklabels()]==spans;ax.set_xlabel('Entry days');ax.set_ylabel('EMA span (days)');ax.set_title(f'{y} {a}, 3x costs')
fig.tight_layout();fig.savefig(T/'sensitivity.png',dpi=130);plt.close(fig)
