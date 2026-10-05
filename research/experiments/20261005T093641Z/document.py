"""Render all actual results with axis labels derived directly from the frozen plan."""
from pathlib import Path
import json,gzip
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
T=Path(__file__).resolve().parent
r=json.loads((T/'report.json').read_text());f=json.loads((T/'forward_report.json').read_text());s=r['summary'];d=json.loads((T/'diagnostic.json').read_text());p=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));g=r['plan']['grid']
lines=['# BTC/ETH 策略研究：'+T.name,'',f"新历史配置{s['new_configs']}个、{s['new_cost_scenes']}成本场景，旧配置{s['reused_grid_configs']}个/{s['reused_cost_scenes']}场景只读。1倍成本正收益{s['positive_1x']}，三倍成本正收益{s['positive_3x']}，单年度通过{len(s['passed'])}、淘汰{len(s['rejected'])}。新增跨2025/2026合格组合参数{len(s['new_both_periods_passed_combination_pairs'])}组。",'', '## 假设及事前固定规则','', '上轮1%/2%EMA带宽产生6组跨年度合格参数，但2026仅2条新增NAV、前五折仍负。本轮扩展较窄0.5%和较宽2.5%边界，与旧1%只读锚对比，检查噪声交易、成本、回撤及折一致性。', f"固定入场窗口{g['entry_lookback_days']}日×EMA对称带宽{[100*x for x in g['EMA_symmetric_bands']]}%；EMA50、退出30日，预定中心entry15/band1%旧配置。规则、数据边界、失败门槛和整个邻域均先冻结，36新历史+3新观察各自reserve成功后才计算。", 'BTC/ETH原资金占比67.5%/32.5%，总2000USDT对应1350/650独立袖套；没有归一化、资金转移、恒定敞口或再平衡。组合只相加同轴已真实计成本的绝对NAV一次，不能平均收益或Sharpe。', '每日UTC00:01真实分钟开盘执行：仅用刚完成C[i-1]，参考通道极值截止i-2。若C[i-1]低于此前exit30日最小收盘或低于EMA[i-1]×(1-band)，优先desired现金；否则收盘高于此前entry日最大收盘且高于EMA×(1+band)才desired多头；其余/等号维持。EMA alpha2/(50+1)、首日浮点收盘初始化、adjust=False，逐折不重置。OOS起点空仓，末端成本平仓。', '', '## 三项验证与范围','', '2025/2026两段分别UTC Mar18 00:01—Sep14 00:01，180日/6×30日连续折；滚动180日历史、3日gap。无拟合标签，purge0；仅固定规则的因果历史，不在同次OOS中选参数后再宣称独立测试。两段历史反复用于开发，不是未触碰最终留出。', '参数敏感性完整3×3同时改变入场日和带宽；report.json/sensitivity含每成本收益及Sharpe正值比例、范围、12条邻接边和描述性2sd cliff。CSV保存每变体成本、Sharpe365、Calmar、整体逐分钟回撤及每日回撤。热图标签直接从冻结grid读取并核对；边界最好仅是描述，不宣称已找到最优。', '成本：手续费10bp、半价差1bp、滑点2bp、冲击0.5×过去20日样本sigma×sqrt(实际预算/过去20日quoteADV)，四层同时×1/2/3。最大ADV参与率.001；Decimal28、PRICE/LOT舍入、最低名义额、静态Oct1交易过滤和前5闭合分钟VWAP百分价格代理，IOC完整成交假设、余现金保留、拒单次日按desired重试。现货多头，无杠杆/空头，资金费与借币N/A。无真实盘口/TCA或容量实盘证明。', '八门槛保持：所有成本正收益、1倍至少4/6正收益折、3倍整体分钟回撤≤25%、3倍邻域正收益率≥60%、至少2完整轮交易、毛参考PnL/成本≥2.5、无负现金/数量违规、期末平仓。现金和同期持有等只读对照保存于report/read_only_comparators，持有不是等风险alpha基准。', '', '## 筛选结论与路径差异','',f"淘汰门槛计数（可能重叠）：{d['failure_counts']}。新108场景中{d['identical_new_scenes_to_matching_old_band1pct']}条完整NAV与匹配旧1%锚相同。新增合格参数{d['new_qualified_parameter_pairs']}组，与旧锚不同的完整跨年度NAV对{d['new_cross_period_qualified_distinct_NAV_pairs']}组。2026组合三倍成本共有{d['combo_2026_unique_3x_NAVs']}条NAV，其中不在旧锚的{d['combo_2026_new_3x_NAVs_not_in_anchor']}条。", f"2026组合在三倍成本下的前五折累计：{d['all_2026_combo_first5_3x_return_pct']}%。这些是五折复合收益，不能误写成每折全部负。规则变体不等于独立市场证据，未执行独立多重比较显著性检验。", '', '|年|entry15带宽%|三倍180日收益%|整体分钟回撤%|前五折累计%|状态|','|---|---|---|---|---|---|']
headers=lines[-2:];lines=lines[:-2]
lines += ['', '本轮较宽2.5%组合将2026前五折三倍成本累计提升至+0.99365%（旧1%为-1.10936%）。entry15对应2026三倍总净收益17.68008%、整体分钟DD10.42023%；2025为37.02250%/DD13.45021%，总收益低于旧1%。0.5%entry15两年三倍收益45.00284%/16.07451%、DD12.50296%/12.40801%，但2026前五折仍-0.56892%。全部仅为重复开发历史上的描述与固定门槛结果，不追认独立测试或稳定实盘盈利。', '']
lines += headers
for c in r['configs'].values():
 if c['role']=='combination' and c['entry_days']==15:
  z=c['scenes']['3'];lines.append(f"|{c['year']}|{100*c['EMA_band']:.1f}|{z['net_return_pct']:.6f}|{z['max_drawdown_pct']:.6f}|{z['first_five_fold_return_pct']:.6f}|{c['status']}|")
lines+=['', '## 全配置、全成本、全折结果','', '|配置|入场日|带宽%|新测|状态|成本|净收益%|分钟回撤%|六折净收益%|失败门槛|','|---|---|---|---|---|---|---|---|---|---|']
for n,c in r['configs'].items():
 for k,z in c['scenes'].items():lines.append(f"|{n}|{c['entry_days']}|{100*c['EMA_band']:.1f}|{c['is_new']}|{c['status']}|{k}|{z['net_return_pct']:.6f}|{z['max_drawdown_pct']:.6f}|{','.join(format(x['net_return_pct'],'.5f') for x in z['folds'])}|{','.join(c['failed_criteria'])}|")
lines+=['', '## 原冻结模拟续接','', '原SMA65±1%、BTC75%/ETH25%浮点模型从073610 state/report续接UTC Oct5 07:10—09:10。4754点旧NAV完整前缀保持，仅追加120闭合分钟至4874点，累计4869分钟（81小时9分、3完整日）。无新日决策或新成交，现金/数量/desired/交易/成本全保留，未将新历史参数替换进原账户，也未强平。下一日决策Oct6 UTC00:01；长期终点2027Mar31不变。', '|观察配置|成本|累计净收益%|整体回撤%|','|---|---|---|---|']
for n,c in f['configs'].items():
 for k,z in c['scenes'].items():lines.append(f"|{n}|{k}|{z['net_return_pct']:.6f}|{z['max_drawdown_pct']:.6f}|")
lines+=['', '3个部分观察定义9场景finish rejected仅表明不足180日/六折，不终止长期计划。真实闭合分钟数据延迟shadow重建，没有实盘订单、实时执行证据或稳定盈利结论。', '', '## 登记与复现','', f"完整读取{p['lines']}行、{p['canonical']}规范定义/{len(p['records'])}保留ID、{len(p['prior_conclusions'])}轮结论和既往Freqtrade/CSV/4份OOS检查；初始16均已有实际结果，没有缺结果补测项。过去试验众多，明确多重选择局限。旧锚记录、报告及归档SHA保持，原始行情4份parquet连续性与SHA核对。", f"独立审计162场景/42019884逐分钟点、19440决策、72当前/未来收盘扰动、{s['audited_component_fills']}成交（其中{s['actual_component_fills']}新成交）。观察审计核对9场景账户连续性、原始HTTP200响应、重叠bar、UTC轴和SHA。两项审计通过后39个新定义finish，所有负收益折、淘汰和短期结果永久保存。", 'spec、plan、全部report/压缩归档、数据manifest/SHA、代码、stdout、中文报告、CSV、图及验证文件均留档。大行情与分钟NAV缓存仅留忽略data目录。只提交本轮轻量研究证据，不含凭据。', f"复现命令：`bash research/experiments/{T.name}/reproduce.sh`；108新成本场景精确重放、54旧只读核验、9观察及nextstate精确重放，不HTTP或写登记。", '后续按实际折一致性和成本/回撤结果预登记更独立的退出条件或新规则；不追认排名为稳定盈利，不改变原模拟规则。']
(T/'result.md').write_text('\n'.join(lines)+'\n')
entries=g['entry_lookback_days'];bands=g['EMA_symmetric_bands'];labels=[100*b for b in bands];assert labels==[.5,1.,2.5]
fig,axes=plt.subplots(2,3,figsize=(13,7))
values=[c['scenes']['3']['net_return_pct'] for c in r['configs'].values()];lo=min(0,min(values));hi=max(values)
for i,y in enumerate(('2025','2026')):
 for j,a in enumerate(('BTC','ETH','combination')):
  cells={(c['EMA_band'],c['entry_days']):c for c in r['configs'].values() if c['year']==y and c.get('asset','combination')==a};v=np.array([[cells[b,e]['scenes']['3']['net_return_pct'] for e in entries] for b in bands]);ax=axes[i,j];ax.imshow(v,cmap=('YlGn' if lo>=0 else 'RdYlGn'),vmin=lo,vmax=hi)
  for ii,b in enumerate(bands):
   for jj,e in enumerate(entries):ax.text(jj,ii,f'{v[ii,jj]:.2f}%',ha='center',va='center')
  ax.set_xticks(range(len(entries)),entries);ax.set_yticks(range(len(bands)),labels);assert [float(x.get_text()) for x in ax.get_yticklabels()]==labels;ax.set_xlabel('Entry days');ax.set_ylabel('EMA band (%)');ax.set_title(f'{y} {a}, 3x costs')
fig.tight_layout();fig.savefig(T/'sensitivity.png',dpi=130);plt.close(fig)
