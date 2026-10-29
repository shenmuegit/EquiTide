# 20261029T092426Z 门控方式与快周期交叉分散

实际54个新组合/162成本场景；历史通过0、淘汰54。完整读取22338登记事件/11065ID和226份结论；初始16项均有实际证据。

All54same-fast gateownership mixtures failed recent6of8 despite positive total returns. Test one predeclared different timing pairing:full-gate L3 withentry-onlyL4 andfull-gateL4 withentry-onlyL3,atfixed a/H/S grid. The assignment axis swaps both fastperiods together;not an isolated single-source lookback sensitivity. Compare each new portfolio with the exact prior same-fast portfolio holding BTC/full-gate source,a,H,S fixed and changing only entry-only fastperiod. No source model rerun,gate relaxation or post-result grid extension. Positive source parent returns already imply positive convex fullperiod totals,not independent new alpha.

Raw[1,a,1-a],a.25/.5/.75,not normalized. Owned initialcapital[10000,10000*a,10000*(1-a)]sum20000. Native entryN1000/3000/3000;owned nominal entrybudget1000+3000*a+3000*(1-a)=4000=20percent initialparent. Static claims on existing complete bank outcomes;no native resizing,transfers,rebalance,crossmargin or cash yield.

Fixed BTC ROC31/H4/E1,N1000/10000bank plus ETH_A entries-and-retention slow-majority bank and ETH_B entry-only slow-majority bank,N3000/10000each. ETH share entry H2/2.5/3percent and slowcenterS27/28/29 but have opposite fast assignments:(LA,LB)=(3,4) or(4,3). LA=3/4,LB=7-LA. Full three original parameter dictionaries and fingerprints bind every spec. A gates entries and retention;B gates only entries/reversals and retains actual fast-compatible positions.

ParentNAV=BTC_NAV+a*ETH_full_gate_NAV+(1-a)*ETH_entry_only_NAV on common causal union(ns,eventcode). Monetary PnL/cost/funding/cushion weighted by bank ownership;source action counts unweighted. Source full-bank nonlinear order impact/lot/collateral retained. No new parent fills,recosting,netting or source resizing.

Every native bank retains original full-collateral and closed-hour1percentmaintenance proxy. Fractional ownership scales economic cushion but does not permit cross-bank rescue or net simultaneousETHlong/short obligations. L2/TCA/exacttiers/tick-liquidation unavailable.

预设4D54格为a0.25/0.5/0.75、共享H2/2.5/3%、共享S27/28/29和配对(完整门控LA,仅入场门控LB)=(3,4)/(4,3)。135相邻边；最后一个轴同时交换两源快周期，属于离散配对敏感性，不称独立只改一个源周期。权重原值[1,a,1−a]不归一化；本金20000、入场预算4000=20%；是完整银行账本的静态所有权，非ETH750/1500/2250小订单重估。

39个已有原生/117成本NAV仅从已保存现金、数量、entry、成交和资金费事件回放，核对每条完整NAV SHA；无原生信号/成交/资金费模型重跑，无父层新增成交或净额抵消。纳秒/事件码并集时轴只取最后完成值，整体收益/回撤/Sharpe/Calmar及逐折指标由逐点组合净值重算。两个ETH账本不假定统计独立、市场中性或等风险。

8真实合并Parquet及16年度/近期源SHA/字节固定。370日OOS2025-10-19UTC00:01至2026-10-24UTC00:01，33日上下文含30预热及3日初始embargo。静态规则无拟合/未来标签，purge不适用；12完整30日折加10日尾折连续承接所有状态；近期40由day330继承分8×5日，不重开本金/诊断平仓，仅原终点计费退出。已有重复历史属于开发验证，非未触碰最终测试。

成本沿用实际原生订单：每侧5bp费+1bp半价差+2bp滑点+0.5×滞后20日日log波动×sqrt(实际原生成交金额/滞后20日quoteADV)冲击，参与率≤0.1%，不利tick/lot/最小金额/全额抵押约束。资金费=−有符号q×实际结算mark×rate，流出按1/2/3倍放大、收入不放大；永续不虚构现货借币。闭合小时不利mark与独立银行1%维持保证金是风险代理，缺L2/TCA、完整历史tier/tick清算和聚合容量证明。

固定门槛：全期/近期三成本净正、1x月正折≥9/12、近期≥6/8、3x完整连续整体DD≤25%、4D相邻索引半径1含自身全期3x净正≥60%、≥4往返、(参考毛利+资金费)/成本≥2.5、现金/拒单/风险违规0、终点空仓及≥180日。36单ETH父组合、54上轮相同快周期组合及恒多只读且资格不变。每个新组合与匹配相同a/H/S/完整门控周期的上轮组合比较，仅改变仅入场源的快周期。源父组合正收益已数学上保证全期正的凸组合，不据此宣称独立alpha。

{"new_financial_configs": 54, "new_native_components": 0, "new_passive_parents": 54, "candidate_configs": 54, "benchmark_configs": 0, "passed_candidates": 0, "rejected_candidates": 54, "positive_configs_by_cost": {"1": 54, "2": 54, "3": 54}, "failed_criteria_counts": {"recent40_six_of_eight_positive5d_1x_folds": 54, "nine_of_twelve_positive_complete30d_1x_folds": 1}, "rows": {"cost": 435, "full_folds": 5655, "recent40_folds": 3480, "daily_NAV": 60102, "edges": 135, "reference_comparisons": 648}, "by_slow_center": {"27": {"candidates": 18, "passed": 0, "recent6of8": 0, "full3x_positive_Sharpe_fraction": 1.0}, "28": {"candidates": 18, "passed": 0, "recent6of8": 0, "full3x_positive_Sharpe_fraction": 1.0}, "29": {"candidates": 18, "passed": 0, "recent6of8": 0, "full3x_positive_Sharpe_fraction": 1.0}}}

原冻结单S28候选与SMA65从UTC06:30续接至08:30。候选使用实际08资金费精确纳秒、mark、rate和有符号持仓逐条入账一次，流出压力/收入不放大独立核验；保留08小时前后现金/风险栈、35日候选/65日SMA上下文及3个候选日NAV边界，完整净值前缀承接。无新日决策或成交；下一日决策Oct30UTC00:01。下一10:30窗口应消化08/09小时风险栈，排除零时长而保留任何真实正时长前后状态。原账户不替换为本轮组合，与paper10十策略实时报价观察分开。

一手背景：[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)与[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)。本轮快周期交叉所有权组合是研究推论，并非原论文复现。54相关新试验及所有既往试验存在多重选择偏差，无DSR/PBO、独立未来资格或稳定实盘盈利证明。

复现目录/home/desktop/Documents/Codex/EquiTide。audit.py独立Decimal源事件播放及逐点/逐折核验；check_exports.py/check_sources.py/check_feed.py只读数值/SHA/登记；audit_candidate.py/audit_forward.py独立核验原账户，forward.py --reproduce离线复现。不得重新reserve/evaluate已完成精确配置。全部正负结果、冻结规则、登记、完整账户账本及失败留档；行情/原始HTTPpacket留ignoreddata绑定SHA。仅main普通非强推，完整远端tree/blob/数据核验及发布实际exit0后释放自身锁。

已完成配置的只读配对诊断（不改变资格或门槛）：{"new_financial_evaluations": 0, "source": "Already completed report.json and verified reference_comparisons.csv only", "financial_report_sha256": "12b09208af66ed9e96b4be1c76c9bf094d6c40d35df035640a22f953b08a29c7", "highest_full3_cell": {"name": "crossgate370_A25_H025_S27_LA3_LB4", "ETH_A_ownership_fraction": 0.25, "reversal_return_hurdle": 0.025, "trend_filter_lookback_days": 27, "ETH_A_lookback_days": 3, "ETH_B_lookback_days": 4, "positive_complete_30d_folds_1x": 11, "recent40_positive_5d_folds_1x": 5, "failed_criteria": ["recent40_six_of_eight_positive5d_1x_folds"], "scenes": {"1": {"net_return_pct": 9.969515964429586, "max_drawdown_pct": 2.8064943975424583, "sharpe_365": 2.1091750130596365, "calmar": 3.502013214554113, "cost_usdt": 174.03763358875}, "2": {"net_return_pct": 8.8825647491094, "max_drawdown_pct": 2.8461494114567, "sharpe_365": 1.8824386777602127, "calmar": 3.0769369083098344, "cost_usdt": 347.5795168175}, "3": {"net_return_pct": 7.7952332703892235, "max_drawdown_pct": 2.8861870642041487, "sharpe_365": 1.6549789366721677, "calmar": 2.6630098715444452, "cost_usdt": 521.19745272625}}, "recent40_3_return_pct": 1.1834550211824446}, "recent_positive_fold_histogram": {"5": 44, "4": 10}, "controls": {"matched_single_full_gate": {"pairs": 54, "full3_net_improved": 39, "recent40_3_net_improved": 45, "full3_return_delta_range_pp": [-0.7981866264603177, 2.8567322247381233]}, "matched_single_entry_only": {"pairs": 54, "full3_net_improved": 15, "recent40_3_net_improved": 9, "full3_return_delta_range_pp": [-2.856732224738102, 0.7981866264602733]}, "matched_same_fast_mix": {"pairs": 54, "full3_net_improved": 27, "recent40_3_net_improved": 27, "full3_return_delta_range_pp": [-1.5967477647208295, 1.5967477647208295]}}}。本轮实际访问的一手发布页、日期及推论边界见literature_access.json。

历史通过项目只读冻结检查：0项。完整spec/来源/报告/账本SHA见candidate_validation.json；不改原冻结L3未来账户。

逐配置结果（收益/回撤单位%，三倍全期回撤使用完整连续OOS）：

|配置|1x收益|2x收益|3x收益|3x最大回撤|近期3x收益|1x月正折|1x近期正折|结论|
|---|---:|---:|---:|---:|---:|---:|---:|---|
|crossgate370_A25_H025_S27_LA3_LB4|9.969516|8.882565|7.795233|2.886187|1.183455|11/12|5/8|rejected|
|crossgate370_A25_H025_S28_LA3_LB4|9.934736|8.781363|7.627589|2.879822|1.246250|11/12|5/8|rejected|
|crossgate370_A25_H025_S27_LA4_LB3|9.785511|8.677682|7.569348|2.801790|1.373421|9/12|5/8|rejected|
|crossgate370_A25_H025_S28_LA4_LB3|9.776051|8.613798|7.450849|2.795789|1.436215|9/12|5/8|rejected|
|crossgate370_A25_H020_S27_LA3_LB4|9.741786|8.504586|7.266847|2.897575|1.189354|11/12|5/8|rejected|
|crossgate370_A50_H025_S28_LA4_LB3|9.553337|8.398218|7.242519|2.840375|1.355450|11/12|5/8|rejected|
|crossgate370_A50_H025_S27_LA3_LB4|9.448433|8.330877|7.212912|2.848424|1.176127|10/12|5/8|rejected|
|crossgate370_A25_H020_S28_LA3_LB4|9.715654|8.447407|7.178625|2.891160|1.251536|11/12|5/8|rejected|
|crossgate370_A50_H025_S27_LA4_LB3|9.377319|8.273490|7.169238|2.844284|1.282377|9/12|5/8|rejected|
|crossgate370_A50_H025_S28_LA3_LB4|9.415485|8.247044|7.078126|2.844170|1.251547|11/12|5/8|rejected|
|crossgate370_A25_H030_S28_LA3_LB4|9.153625|8.105577|7.057342|2.022361|0.819671|11/12|5/8|rejected|
|crossgate370_A75_H025_S28_LA4_LB3|9.330623|8.182637|7.034189|2.885039|1.274500|11/12|5/8|rejected|
|crossgate370_A50_H020_S27_LA3_LB4|9.451648|8.164094|6.875899|2.862077|1.179879|10/12|5/8|rejected|
|crossgate370_A25_H020_S28_LA4_LB3|9.479664|8.144653|6.808838|2.958184|1.444973|9/12|5/8|rejected|
|crossgate370_A50_H020_S28_LA3_LB4|9.436299|8.120324|6.803692|2.857783|1.254803|11/12|5/8|rejected|
|crossgate370_A75_H025_S27_LA4_LB3|8.969128|7.869297|6.769128|2.886787|1.190816|10/12|5/8|rejected|
|crossgate370_A25_H020_S27_LA4_LB3|9.275586|7.989428|6.702503|2.961765|1.384733|9/12|5/8|rejected|
|crossgate370_A75_H025_S27_LA3_LB4|8.927350|7.779189|6.630590|2.810543|1.168720|9/12|5/8|rejected|
|crossgate370_A25_H025_S29_LA4_LB3|8.839410|7.707611|6.575186|2.803431|1.443291|9/12|5/8|rejected|
|crossgate370_A75_H025_S28_LA3_LB4|8.896234|7.712725|6.528663|2.808356|1.256900|10/12|5/8|rejected|
|crossgate370_A25_H030_S27_LA3_LB4|8.462861|7.493968|6.524961|2.097112|0.762753|11/12|4/8|rejected|
|crossgate370_A50_H020_S28_LA4_LB3|9.137213|7.831372|6.524881|2.866377|1.364706|11/12|5/8|rejected|
|crossgate370_A75_H030_S28_LA4_LB3|8.585148|7.542384|6.499426|2.084702|0.845180|11/12|4/8|rejected|
|crossgate370_A75_H020_S27_LA3_LB4|9.161511|7.823603|6.484951|2.826410|1.170337|9/12|5/8|rejected|
|crossgate370_A75_H020_S28_LA3_LB4|9.156943|7.793242|6.428759|2.824198|1.258095|10/12|5/8|rejected|
|crossgate370_A25_H020_S29_LA4_LB3|9.031623|7.728515|6.424692|2.933494|1.445361|8/12|5/8|rejected|
|crossgate370_A50_H025_S29_LA4_LB3|8.653859|7.529580|6.404814|2.854204|1.356476|10/12|5/8|rejected|
|crossgate370_A50_H020_S27_LA4_LB3|8.945912|7.671681|6.396794|2.866422|1.291807|9/12|5/8|rejected|
|crossgate370_A75_H030_S27_LA4_LB3|8.295395|7.312103|6.328683|2.085600|0.760042|10/12|4/8|rejected|
|crossgate370_A25_H030_S29_LA3_LB4|8.335091|7.329953|6.324654|2.434728|0.820518|10/12|5/8|rejected|
|crossgate370_A50_H030_S27_LA4_LB3|8.310942|7.309709|6.308167|2.045648|0.856214|9/12|4/8|rejected|
|crossgate370_A50_H030_S28_LA4_LB3|8.395276|7.344426|6.293147|2.043571|0.930332|11/12|5/8|rejected|
|crossgate370_A25_H030_S27_LA4_LB3|8.326489|7.307315|6.287651|2.416144|0.952607|9/12|4/8|rejected|
|crossgate370_A75_H025_S29_LA3_LB4|8.614493|7.440940|6.266813|2.813425|1.245362|10/12|5/8|rejected|
|crossgate370_A50_H025_S29_LA3_LB4|8.552345|7.402749|6.252679|2.857456|1.251608|10/12|5/8|rejected|
|crossgate370_A75_H020_S28_LA4_LB3|8.794761|7.518092|6.240924|2.906027|1.284139|11/12|5/8|rejected|
|crossgate370_A25_H025_S29_LA3_LB4|8.490197|7.364559|6.238546|2.901540|1.257857|9/12|5/8|rejected|
|crossgate370_A75_H025_S29_LA4_LB3|8.468308|7.351550|6.234441|2.905284|1.269533|10/12|5/8|rejected|
|crossgate370_A75_H020_S29_LA3_LB4|8.812079|7.475353|6.137867|3.123319|1.246894|9/12|5/8|rejected|
|crossgate370_A50_H030_S28_LA3_LB4|8.233668|7.169563|6.105098|2.046317|0.825909|11/12|5/8|rejected|
|crossgate370_A75_H020_S27_LA4_LB3|8.616237|7.353934|6.091085|2.905810|1.198518|10/12|5/8|rejected|
|crossgate370_A25_H030_S28_LA4_LB3|8.205405|7.146467|6.086868|2.412258|1.015960|9/12|5/8|rejected|
|crossgate370_A50_H020_S29_LA4_LB3|8.560135|7.286099|6.011515|2.967371|1.361577|9/12|5/8|rejected|
|crossgate370_A50_H020_S29_LA3_LB4|8.531076|7.245294|5.958884|2.969467|1.255122|10/12|5/8|rejected|
|crossgate370_A75_H030_S29_LA4_LB3|7.841636|6.841597|5.841423|2.622227|0.835866|10/12|4/8|rejected|
|crossgate370_A50_H030_S27_LA3_LB4|7.826774|6.812828|5.798623|2.338044|0.754129|10/12|4/8|rejected|
|crossgate370_A25_H020_S29_LA3_LB4|8.250074|7.015236|5.779902|2.912540|1.263379|9/12|5/8|rejected|
|crossgate370_A50_H030_S29_LA3_LB4|7.831719|6.787361|5.742643|2.526865|0.819015|10/12|5/8|rejected|
|crossgate370_A75_H020_S29_LA4_LB3|8.088647|6.843682|5.598337|3.005274|1.277278|9/12|5/8|rejected|
|crossgate370_A50_H030_S29_LA4_LB3|7.618855|6.597294|5.575360|2.524467|0.926932|10/12|5/8|rejected|
|crossgate370_A25_H030_S29_LA4_LB3|7.396075|6.352991|5.309298|2.430493|1.018625|9/12|5/8|rejected|
|crossgate370_A75_H030_S29_LA3_LB4|7.328347|6.244768|5.160633|2.619207|0.817496|9/12|4/8|rejected|
|crossgate370_A75_H030_S28_LA3_LB4|7.313710|6.233550|5.152854|2.423193|0.832261|10/12|4/8|rejected|
|crossgate370_A75_H030_S27_LA3_LB4|7.190687|6.131688|5.072284|2.581004|0.745388|9/12|4/8|rejected|

全网格Sharpe正值比例、收益正值比例及最高观测单元边界诊断（只读已有结果，不改变资格）：{"parent": {"dimension_count": 4, "cells": 54, "full3x_positive_Sharpe_fraction": 1.0, "recent40_3x_positive_Sharpe_fraction": 1.0, "full3x_positive_net_fraction": 1.0, "recent40_3x_positive_net_fraction": 1.0, "highest_observed_full3x_net_cell": "crossgate370_A25_H025_S27_LA3_LB4", "highest_observed_is_on_axis_boundary": {"ETH_A_ownership_fraction": true, "reversal_return_hurdle": false, "trend_filter_lookback_days": true, "ETH_A_lookback_days": true}, "descriptive_full_Sharpe_cliff_edges": 33, "old_qualifications_preserved": true, "recent6of8_by_slow_center": {"27": 0, "28": 0, "29": 0}, "not_untouched_test_or_global_optimum": true}}。最高观测单元的预设网格边界标记已保存，不称全局最优；全期平台不能消除近期正折不足。

实际失败门槛计数：{"recent40_six_of_eight_positive5d_1x_folds": 54, "nine_of_twelve_positive_complete30d_1x_folds": 1}。逐项真实结论见上表和report.json，不因全期收益正而放宽门槛。435成本行、5655全期折、3480近期折、60102新日边界、135敏感性边、648匹配对照完整留档；6图36面板已实际打开。
独立只读核验39旧原生/117成本曲线、7332条已保存成交与129870条已保存资金费记录，原完整NAV SHA保持；没有旧原生模型重跑或父层新增成交；无新原生模型执行，39个已有原生账本经独立Decimal事件播放与原NAV SHA核验，父层按原值份额组合。54新配置162成本场景共88292106完整NAV点、2268全期/逐折和1458近期/逐折指标通过；130旧唯一结果SHA/资格保持，13720受保护文件不变。60新实际ID各自finish，120事件仅追加；54实际金融配置加6实际partial，全部完整spec在reserve前核对三个原生参数字典，无本轮失配定义。
只读监控实际检查exit0：8245研究项，174既有paper观察/10账户；8191旧展示行完整字典不变。原候选累计3469点/场景、3389分钟，0新日决策/成交，新增资金费记录6条；现金与资金费独立核验，收入不随成本放大，00旧结算未重复、实际08资金费逐条入账一次、06/07小时风险已承接且08小时前后栈完整保留。旧SMA累计39418点，0新日决策/成交。两者均非十策略实时报价执行或长期盈利证据。
真实命令/传输异常记录0项，见read_failures.json。本轮登记、账户续接及提交由持续stdin排他锁保护。所有真实负收益分折/近期、成功/失败和完整账户账本保留；行情与HTTPpacket留ignoreddata并绑定SHA，不提交大行情或凭据。main普通非强推，freshfetch/独立allheads/完整tree/blob/行情核验通过后释放自己锁。
