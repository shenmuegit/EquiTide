import json
from run import ROOT,R,put,sha,ENTRIES,EXITS,positive_recent

def main():
 r=json.loads((R/'report.json').read_text());s=json.loads((R/'sensitivity_summary.json').read_text());rep=json.loads((R/'representative.json').read_text());ctx=json.loads((R/'context.json').read_text())
 text='''# BTC/ETH 九通道因果信号共识

本轮假设：单通道近期折间稳定性不足，检验全部九格通道信号的共识与入场/保留票数迟滞是否减少参数特有反手。固定E5/6/7入场票数×H2/3/4保留票数，中心E6/H3事前确定。BTC、ETH和匹配参数父组合各9格，共27独立新配置、81个1/2/3倍成本场景，所有完整spec先成功reserve再计算。不是按收益选择源信号、加权旧NAV或重命名旧策略。

每资产只读复用上轮N20/25/30×M5/10/15九个原通道的pre-OPEN desired_direction，来源指纹排序固定。源方向必须三成本完全一致，且根据真实已完成收盘/排除被测收盘的通道上下界独立核验。每个方向在UTC00已可知，不读取同日00:01源成交、OPEN、未来资金费或PnL作为投票特征。统计多/空/平9票；一侧≥E即新入场，该侧与反向已有仓不同则先平后开，反向新多数优先。未形成新多数时，实际多仓只在多票≥H时保留、实际空仓只在空票≥H时保留，否则退出；空仓必须新多数才入场。E≥5消除双向同时入场歧义，无隐藏目标/同向调仓。

原交易/费用/资金费/风险/数据/统计函数AST保持，新增票数边界、相等保留、反手、空仓与未来票数扰动穷举1485+1485例。源18组件仅复用已留档方向与账本证据，不重新计算旧金融结果；18个新共识组件真实逐笔执行，9个父组合复用本轮实际组件NAV。

BTC独立本金10000、固定每次名义1000（自身初始本金10%），ETH独立10000/固定2000（20%）。父组合原值[1,1]合并两个已出资账户，总20000，初始本金占比各50%，不归一化、转账、按NAV扩仓、净额抵消抵押/费用。两腿均新入场目标名义3000即总本金15%，实际LOT/价格/平仓使敞口变化。三旧同本金/固定名义常持对照只读，旧字段/时间别名仅在内存规范化，原报告/资格/账本哈希不改；现金0%为数学基准。

真实8个Parquet/404日上下文，370日连续OOS为2025-10-19 UTC00:01至2026-10-24 UTC00:01，初始33日上下文含3日embargo，覆盖最长30日通道并排除被测收盘；无拟合、未来标签或测试集择优。12完整30日折及10日尾折；近期40日继承day330现金/持仓，8×5日，不重开账户。完整545013点(ns,eventcode)NAV计算连续整体回撤，保留真实毫秒资金费，不平均单策略Sharpe或收益率。既往历史反复开发，不是未触碰最终测试集，无DSR/PBO或独立未来盈利证明。

成本单边5bp手续费、1bp半价差、2bp滑点、0.5×滞后20日样本日对数波动×sqrt(实际q×真实OPEN/滞后20日quoteADV)冲击，原生LOT/minnotional及不利tick。参与率≤0.1%、付费后完全抵押1倍进入上限、1%闭合小时mark不利极值保证金代理。真实永续资金费按结算实际纳秒/mark/旧持仓计入，负支出×1/2/3，收入不放大。线性永续无需现货借币，不虚构借币费；费率不作新信号。终止平仓计成本。缺L2/TCA、完整历史档位/过滤、逐tick清算及真实容量证明。

预设资格门槛保持：全期与近期40日各成本净正、完整月折≥9/12、近期各成本正五日折≥6/8、局部三倍净正及局部严格率各≥60%、三倍完整DD≤25%、≥4往返、毛参考PnL加资金费/执行成本≥2.5，无负现金/拒单/风险违规、终止平仓且≥180日。邻域只比较同资产/同scope的E/H轴。

'''
 text+=f"完整登记{ctx['registry_events']}事件/{ctx['registry_ids']}ID及{len(ctx['prior_conclusions_read'])}历史结论已读；初始16项均有实际证据，0缺项。27新配置通过{len(r['summary']['passed'])}、淘汰{len(r['summary']['rejected'])}；1/2/3倍全期净正配置数分别为"+'/'.join(str(r['summary']['positive_configs_by_cost'][str(k)]) for k in [1,2,3])+'。全部真实正负收益均保存并finish。\n\n'
 for asset in ['BTC','ETH','COMBO']:
  g=s['groups'][asset];text+=f"## {asset} 完整网格\n\n|E入场票|H保留票|状态|三倍净收益%|完整DD%|近期净收益%|1/2/3正五日折|局部严格率|\n|---:|---:|---|---:|---:|---:|---|---:|\n"
  for E in ENTRIES:
   for H in EXITS:
    c=next(c for c in r['configs'].values() if c['asset']==asset and c['entry_vote_threshold']==E and c['retention_vote_threshold']==H);z=c['scenes']['3'];text+=f"|{E}|{H}|{c['status']}|{z['net_return_pct']:.6f}|{z['max_drawdown_pct']:.6f}|{z['recent40']['net_return_pct']:.6f}|"+'/'.join(str(positive_recent(c,str(k))) for k in [1,2,3])+f"|{c['sensitivity']['local_recent6of8_allcost_fraction']:.6f}|\n"
  c=rep['centers'][asset];text+=f"\n事前中心E6/H3：三倍净收益{c['return3_pct']:.6f}%、完整DD{c['whole_DD3_pct']:.6f}%、近期40日{c['recent_return3_pct']:.6f}%，状态{c['status']}。本组各成本正五日折严格达标格{g['strict_individual_costfold_passes']}/9；最高年度收益边界标记{g['max_return_at_grid_edge']}，不据此称全局最优。\n\n"
 text+='6CSV及3图18面板覆盖所有参数、成本、逐折、近期40日、日NAV、36相邻边、Sharpe/Calmar、成交数、成本占比和同本金常持比较，逐数值核验另存。原冻结SMA65/singleS28观察及最终审计/提交/恢复状态在后续封存附记中说明，绝不采用新共识规则替换冻结账户。\n\n'
 text+='来源：[原作者2012时间序列动量研究](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)仅提供趋势概念，12月非加密历史不验证本轮九通道共识；该共识是本轮推论并须实际回测。[Binance官方资金费资料](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)本轮访问旧地址后重定向，真实结算响应留档。正收益回测不称稳定实盘盈利。\n'
 (R/'result.md').write_text(text)
if __name__=='__main__':main()
