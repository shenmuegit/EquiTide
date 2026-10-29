"""Chinese interpretation of executed refined ownership results;no new metrics/NAV."""
import json
from run import ROOT,R,positive_recent
r=json.loads((R/'report.json').read_text());s=json.loads((R/'summary.json').read_text());p=json.loads((R/'plan.json').read_text());ctx=json.loads((R/'context.json').read_text())
text=f"# {R.name} BTC/ETH静态银行所有权的细化邻域\n\n实际36个新候选＋4个同权重恒多参考，40配置/120成本场景；历史门槛通过{s['passed']}、候选淘汰{s['rejected_candidates']}。完整读取{ctx['registry_events']}登记事件/{ctx['registry_ids']}ID及{len(ctx['prior_conclusions_read'])}份结论，初始16均已有实际证据。\n\n"
text+='事前假设：上轮w0.5/ETH1.5的6个格点在1/2/3成本近期均6/8，但w0.75邻列退5/8，未形成预设≥60%邻域平台。本轮在新PnL之前固定BTC原值w0.25/0.375/0.625/0.875、ETH=2−w，联合E−1.5/−1/−0.5% × S27/28/29；L3/H2.5%固定。27个旧w0.5/0.75/1格点只读，组成等间距1/8单位w七点 × E三点 × S三点的63格、138相邻边。旧27资格不随新邻域重写；完整源spec、报告、账本SHA绑定。方向/L3来自反复使用的开发历史，不是独立测试。\n\n'
text+='原值[w,2−w]是两个原10000USDT固定规模银行的静态所有权单位，不自动归一化。父本金20000，拥有的BTC/ETH资本10000w/10000(2−w)，入场预算1000w+3000(2−w)，分别占父本金27.5/26.25/23.75/21.25%。不重新缩放原生N1000/N3000订单，原始订单数量/成交冲击/资金费/风险规则保持；金额按所有权归属，底层动作次数不加权且不是新父层成交。没有再平衡、转账、NAV目标或交叉保证金。这里验证既有银行净值指数所有权，不证明按新规模直接执行或合并容量。底层银行全期净正已知，因此正权重后的全期净正不是新独立alpha，关键是逐折与局部稳定性。\n\n'
text+='BTC保持ROC31/H4/退出1%；ETH快ROC3日严格H2.5%，E为快ROC到零前的退出阈值而非入场PnL止损。慢ROC(S−1,S,S+1)严格多数只约束新开/反向开仓，已有快方向一致持仓保留；现金无隐藏desired、重新入场仍需新的严格极端。每份spec保留两完整原生参数字典、源指纹、时间/成本/资本及原值单位含义。复用12原生/36成本曲线，独立回放已实际运行回测的成交及真实历史资金费账本，不重跑原生模型。\n\n'
text+='8个真实合并Parquet及16年度/近期源SHA固定。OOS为2025-10-19UTC00:01至2026-10-24UTC00:01共370日；33日上下文含30预热与3初始embargo。静态规则不拟合、无未来标签，purge不适用。12个完整30日折＋10日尾折连续承接账户；近期40日从day330继承状态分8×5日，不重开本金、诊断平仓或再平衡。完整(ns,eventcode)事件并集逐点计算组合及整体回撤，不能平均组件收益/Sharpe/回撤。重复开发历史不称未触碰最终测试集。\n\n'
text+='原生每侧成本5bp手续费＋1bp半价差＋2bp滑点＋0.5×滞后20日样本日log波动×sqrt(实际订单金额/滞后20日quoteADV)，参与率≤0.1%，保留lot/tick/最小金额/全额抵押。实际资金费−signedq×结算mark×rate；流出按1/2/3倍放大，收入不放大。永续不虚构现货借币。闭合小时不利mark和1%维持保证金只是风险代理，缺L2/TCA/历史tier/tick清算与合并容量证据。\n\n'
text+='门槛与上轮预设严格版本相同：全期/近期各成本净正，1倍完整月正≥9/12，近期各成本均≥6/8正折，三倍整体DD≤25%，全期净正局部比例≥60%，每档近期6/8这一条件的局部比例≥60%，≥4往返、(参考毛利＋资金费)/成本≥2.5、现金/拒单/风险违规0、终点空仓且≥180日。邻域为w/E/S索引半径1含自身；4个恒多只参考。未放宽资格或事后扩网格。\n\n'
text+='真实汇总：'+json.dumps({k:v for k,v in s.items() if k not in ['exports','figures']},ensure_ascii=False)+'\n\n'
text+='|配置|用途|1x收益%|2x收益%|3x收益%|3x整体DD%|近期3x收益%|近期正折1/2/3x|结论|\n|---|---|---:|---:|---:|---:|---:|---|---|\n'
for c in sorted(r['configs'].values(),key=lambda c:c['scenes']['3']['net_return_pct'],reverse=True):
 z=c['scenes'];text+=f"|{c['name']}|{c['role']}|{z['1']['net_return_pct']:.6f}|{z['2']['net_return_pct']:.6f}|{z['3']['net_return_pct']:.6f}|{z['3']['max_drawdown_pct']:.6f}|{z['3']['recent40']['net_return_pct']:.6f}|{positive_recent(c,'1')}/{positive_recent(c,'2')}/{positive_recent(c,'3')}|{c['status']}|\n"
text+='\n所有201成本行、2613全期折、1608近期折、44520新日NAV、138敏感性边及216匹配对照完整保存；匹配旧w1/E/S与同权重恒多均父本金20000，现金0为数学参考。全网格Sharpe正值比例、收益比例、边界最高观测与突变边留summary；不称全局最优或独立资格。\n\n'
text+='研究背景为一手[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)及[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)，实际访问见literature_access.json。本轮假设为研究推论，非论文复现或收益迁移证明；相关多重试验选择偏差仍在，无DSR/PBO或新组合独立前向证明。正收益回测不代表稳定实盘盈利。\n\n'
text+='原单S28候选及旧SMA65按冻结规则从UTC14:30延续至16:30；16时实际资金费须按精确ns/mark/rate/旧signedq入账一次，收入不随成本放大，保留前后现金风险栈及14/15小时风险承接。原参数、资金与持仓不换成本轮新组合。最终实际续接与监控状态以本轮审计及发布证据为准；旧延迟shadow与paper10十策略报价执行分开。\n\n'
text+='固定目录/home/desktop/Documents/Codex/EquiTide；复现命令与全输入/代码版本见reproduce.md及data_manifest.json。已完成精确配置不得再次reserve/evaluate；保存所有正负结果和完整账户账本。仅main普通非强推，不下真实订单。\n'
(R/'result.md').write_text(text)
