"""Render actual registered outcomes, full folds and transparent evidence."""
from pathlib import Path
import json,gzip,collections
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
T=Path(__file__).resolve().parent
r=json.loads((T/'report.json').read_text());f=json.loads((T/'forward_report.json').read_text());s=r['summary'];d=json.loads((T/'diagnostic.json').read_text());p=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()))
lines=['# BTC/ETH策略研究：20261005T053510Z','',f"本轮36个新历史配置、108成本场景；18个旧配置54场景只读。1倍成本正收益{s['positive_1x']}个，3倍成本正收益{s['positive_3x']}个；通过{len(s['passed'])}、淘汰{len(s['rejected'])}。新增跨2025/2026同时合格组合0个。",'', '## 冻结规则与验证','', '事前固定entry10/15/20 × exit15/25/30双轴，EMA50、±1.5%；中心entry15/exit30为旧只读。BTC/ETH原始资金比例67.5%/32.5%，总2000USDT，对应1350/650独立资金账户，无归一化、再平衡、资金转移或恒定敞口。', '仅用已完成日收盘；00:01真实分钟开盘执行。收盘低于此前exit日最小收盘或EMA×.985优先退出；高于此前entry日最大收盘且高于EMA×1.015入场，否则维持。EMA从原始首日递推不重置。OOS起点空仓，期末成本平仓。', '2025及2026分别Mar18 00:01至Sep14 00:01 UTC，180天6个连续30日折；180日历史、3日gap。无拟合标签，无同次测试集选择参数。这些历史反复使用，是开发数据，不是未触碰最终测试集。', '手续费10bp、半价差1bp、滑点2bp、依赖实际成交金额/前20日quoteADV及收益波动的冲击；四层均施加1/2/3倍压力。最大参与率.001，Decimal28、tick/LOT舍入、最低名义金额及参考价格过滤；假定IOC完整成交，无真实盘口/TCA校准。现货仅多头，不涉及资金费与借币。', '八门槛：所有成本正收益、1倍至少4/6正收益折、3倍逐分钟全期回撤≤25%、邻域3倍正收益占比≥60%、至少2轮交易、毛参考收益/成本≥2.5、无账户违规、期末平仓。参数敏感性完整3×3及邻接cliff统计；不同配置不等于独立市场证据。', '', '## 筛选结论','', '新4个通过项为2026年exit25组合entry10/15/20及exit15组合entry20；2025对应项均因正收益折不足淘汰，因此不列为跨年度合格方法。', 'entry15组合：2025 exit15三倍成本收益12.34838%，分钟回撤21.20713%，前五折累计19.88406%(rejected)；2025 exit25三倍成本收益26.53475%，分钟回撤21.96605%，前五折累计29.39456%(rejected)；2025 exit30三倍成本收益42.75414%，分钟回撤13.32909%，前五折累计45.78983%(passed)；2026 exit15三倍成本收益14.98914%，分钟回撤10.63987%，前五折累计-0.93568%(rejected)；2026 exit25三倍成本收益14.94184%，分钟回撤13.21912%，前五折累计-1.49708%(passed)；2026 exit30三倍成本收益14.94184%，分钟回撤13.21912%，前五折累计-1.49708%(passed)。中间退出窗口仍未提供跨年度合格改进；完整结果及每折收益见下表。', f"淘汰门槛计数（可重叠）：{d['failure_counts']}。新108场景与旧exit30相同的完整NAV数量见diagnostic.json；2026组合三倍成本有{d['combo_2026_unique_3x_NAVs']}条不同NAV。", '', '## 全配置、成本与逐折结果','', '|配置|新测|状态|成本|净收益%|分钟回撤%|六折净收益%|失败门槛|','|---|---|---|---|---|---|---|---|']
for n,c in r['configs'].items():
 for k,z in c['scenes'].items():lines.append(f"|{n}|{c['is_new']}|{c['status']}|{k}|{z['net_return_pct']:.6f}|{z['max_drawdown_pct']:.6f}|{','.join(format(x['net_return_pct'],'.5f') for x in z['folds'])}|{','.join(c['failed_criteria'])}|")
lines+=['','## 原冻结模拟观察','', '续接033410原state/report，从Oct5 03:10至05:10UTC，保留4514点完整NAV前缀，仅追加120闭合分钟，累计4629分钟（77小时9分、3完整日），4634点。无新日决策、无新成交，现金/持币/交易/成本全部保持。仍是原SMA65±1%、BTC75%/ETH25%浮点模型，禁止将本轮参数替换进去。下一次日决策Oct6UTC00:01。', '|配置|成本|累计净收益%|全期回撤%|','|---|---|---|---|']
for n,c in f['configs'].items():
 for k,z in c['scenes'].items():lines.append(f"|{n}|{k}|{z['net_return_pct']:.6f}|{z['max_drawdown_pct']:.6f}|")
lines+=['', '3个partial快照均rejected仅表示不足180日/六折，不终止长期观察。延迟真实数据模拟，无实盘订单，无实时成交证据，不称稳定盈利。', '', '## 登记、证据和复现','', f"完整读取登记簿{p['lines']}行、{p['canonical']}规范定义、{len(p['records'])}保留ID、{len(p['prior_conclusions'])}轮历史结论，初始16均已有结果。全部39新定义先reserve，审计通过后finish，负收益永久保留。", '本轮历史独立审计全部162场景、42019884逐分钟NAV点、19440因果决策、72未来/当前收盘扰动探针、660成交，其中480新成交。观察审计9场景原账户连续性及HTTP200原始响应/hash/时间轴。', '代码、spec、report、压缩逐配置结果、数据哈希、中文结果和必要日志均保存。大行情/NAV缓存留忽略data目录。spec.json/data_manifest.json记录具体SHA及数据范围；report.json/source_hashes绑定代码和原验证文件。', '复现命令：`bash research/experiments/20261005T053510Z/reproduce.sh`；无HTTP或登记写入，108新历史+54只读+9观察精确重放。', '下轮可预登记EMA退出阈值或新策略方向，关注跨年度折一致性，不因本轮排名追认合格。']
(T/'result.md').write_text('\n'.join(lines)+'\n')
fig,axes=plt.subplots(2,3,figsize=(13,7))
for i,y in enumerate(('2025','2026')):
 for j,a in enumerate(('BTC','ETH','combination')):
  cells={(c['exit_days'],c['entry_days']):c for c in r['configs'].values() if c['year']==y and c.get('asset','combination')==a};v=np.array([[cells[x,e]['scenes']['3']['net_return_pct'] for e in (10,15,20)] for x in (15,25,30)]);ax=axes[i,j];im=ax.imshow(v,cmap='RdYlGn',vmin=-20,vmax=60)
  for ii,x in enumerate((15,25,30)):
   for jj,e in enumerate((10,15,20)):ax.text(jj,ii,f'{v[ii,jj]:.2f}%',ha='center',va='center')
  ax.set_xticks(range(3),[10,15,20]);ax.set_yticks(range(3),[5,10,30]);ax.set_xlabel('Entry days');ax.set_ylabel('Exit days');ax.set_title(f'{y} {a}, 3x costs')
fig.tight_layout();fig.savefig(T/'sensitivity.png',dpi=130);plt.close(fig)
