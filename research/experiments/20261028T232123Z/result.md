# 20261028T232123Z ETH多数门控快周期边界验证

实际18新ETH原生＋18新BTC/ETH组合，共36配置/108成本场景；历史通过0、淘汰36。完整读取21746事件/10769ID及221份结论；初始16项均已有实际证据。

事前补测L2/5 × H2/2.5/3% × S27/28/29，每作用域36格含18个旧L3/4只读真实邻居。新18原生＋18父组合逐个先reserve再计算，原旧资格保持、不按扩展邻域重评级。假设是邻近快周期能否拓宽近期正折表现；不因本轮结果放宽固定门槛。

ETH快ROC严格>H反转空/<-H反转多；带内只保留ROC<0的实际多、ROC>0的实际空，零退出；慢门控S-1/S/S+1至少两票严格正允许多、至少两票严格负允许空，否则平仓。快方向须与慢多数一致；现金重新入场需新严格极端，无隐藏desired。下一UTC00:01真实OPEN执行，q=floor(N/此前完整close/lot)*lot，不读未来OPEN/资金费/未闭合数据。引擎仅将允许快周期3/4扩至2/3/4/5，其他代码字节保持；360项合成信号边界/持仓状态/未来不变性检查通过。

ETH独立10000银行、固定N3000；BTC旧ROC31/H4/退出1%、10000银行固定N1000。原值[1,1]持有完整两银行，父本金20000、入场预算4000=20%，不归一化/NAV缩放/转账/交叉保证金/再平衡。21旧原生/63成本NAV从真实已保存账本恢复核对原SHA，18新原生实际计算专属成交/资金费/成本/风险；18父组合因果对齐完整纳秒事件时轴相加，指标从整体净值重算。

8真实合并Parquet和16年度/近期源SHA固定。370日OOS2025-10-19UTC00:01至2026-10-24UTC00:01；33日上下文含30预热、3日初始embargo。静态规则不拟合、无未来标签，purge不适用；12完整30日折加10日尾折连续承接现金/q/entry/费用，近期40由day330继承分8×5日，不重开本金或诊断平仓，仅原终点计费退出。反复使用历史属于开发验证，非未触碰最终测试。

每侧5bp费＋1bp半价差＋2bp滑点＋0.5×滞后20日日log波动×sqrt(实际native成交金额/滞后20日quoteADV)冲击，参与率≤0.1%，tick/lot/最小金额/100%抵押入场约束。资金费=-有符号q×实际mark×rate，流出乘成本1/2/3、收入不放大；永续无虚构现货借币。独立银行闭合小时1%维持保证金代理，不代表历史完整tier/tick清算或L2/TCA容量证明。

固定门槛：全期/近期三成本净正、1x月正折≥9/12及近期≥6/8、3x完整连续整体DD≤25%、三维相邻索引半径1含自身全期3x净正≥60%、≥4往返、(参考毛利＋资金费)/成本≥2.5、现金/拒单/风险违规0、终点空仓且≥180日。旧L3/L4邻居只读；新L2对旧L3、新L5对旧L4，匹配H/S/本金/原生N；另对照同本金恒多及现金0。

{"new_financial_configs": 36, "new_native_components": 18, "new_passive_parents": 18, "passed_candidates": 0, "rejected_candidates": 36, "positive_configs_by_cost": {"1": 35, "2": 33, "3": 32}, "failed_criteria_counts": {"positive_all_costs": 4, "nine_of_twelve_positive_complete30d_1x_folds": 13, "recent40_positive_all_costs": 13, "recent40_six_of_eight_positive5d_1x_folds": 36, "gross_plus_funding_to_cost1_gte2_5": 3}, "by_scope": {"native": {"new": 18, "passed": 0, "best_full3": {"name": "votefast370_ETH_H020_S29_L5_N3000", "return3_pct": 11.913665131156437, "whole_DD3_pct": 4.903313442345647, "recent_return3_pct": 0.5122515689332641, "positive_months1": 10, "positive_recent1": 2, "failed_criteria": ["recent40_six_of_eight_positive5d_1x_folds"]}}, "parent": {"new": 18, "passed": 0, "best_full3": {"name": "votefast370_parent_B1000_E3000_H020_S29_L5", "return3_pct": 6.9572798059788, "whole_DD3_pct": 3.38487344845253, "recent_return3_pct": 0.4621677238869637, "positive_months1": 9, "positive_recent1": 4, "failed_criteria": ["recent40_six_of_eight_positive5d_1x_folds"]}}}, "rows": {"cost": 222, "full_folds": 2886, "recent40_folds": 1776, "daily_NAV": 40068, "edges": 150, "reference_comparisons": 216}}

原单S28冻结候选与SMA65从UTC20:30续接至22:30，保留现金/数量/entry/成本/资金费/完整净值前缀，零新增日决策/资金费/成交；21close检查旧20小时风险状态、22close检查21小时。下一窗口00:30跨Oct29UTC00:00资金费及00:01日决策，必须用实际结算和更新后的原始34/65日日线上下文，不能继续markonly跨越。延迟闭合数据重建与paper10十策略实时报价观察分开。

背景沿用2026-10-27实际访问的一手[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)及[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)。新快周期假设为研究推论。36个相关新试验及全部既往试验存在多重选择偏差，无DSR/PBO、独立未来资格或稳定实盘盈利证明。

复现工作目录/home/desktop/Documents/Codex/EquiTide。audit.py/audit_native.py独立整数信号/Decimal成交资金费/风险及逐点NAV，check_sources.py/check_exports.py/check_feed.py只读验证；原账户audit_candidate.py/audit_forward.py及forward.py --reproduce只读复现。不得重reserve/evaluate已完成精确配置。全部正负结果保存，行情/HTTPpacket留ignoreddata绑定SHA；main非强推并核验完整远端tree/blob/行情后释放本轮锁。

历史通过项目只读冻结检查：0项。完整spec/来源/报告/账本SHA见candidate_validation.json；不改原冻结L3未来账户。

逐配置结果（收益/回撤单位%，三倍全期回撤使用完整连续OOS）：

|配置|1x收益|2x收益|3x收益|3x最大回撤|近期3x收益|1x月正折|1x近期正折|结论|
|---|---:|---:|---:|---:|---:|---:|---:|---|
|votefast370_ETH_H020_S29_L5_N3000|15.550619|13.731941|11.913665|4.903313|0.512252|10/12|2/8|rejected|
|votefast370_ETH_H020_S28_L5_N3000|15.688451|13.775904|11.863436|4.507465|0.549127|10/12|3/8|rejected|
|votefast370_ETH_H025_S27_L5_N3000|13.212453|11.752050|10.291694|4.424615|0.073901|10/12|1/8|rejected|
|votefast370_ETH_H025_S28_L5_N3000|13.348424|11.746478|10.144668|4.437084|-0.269744|10/12|2/8|rejected|
|votefast370_ETH_H025_S29_L5_N3000|13.239810|11.632502|10.025695|4.472343|-0.306687|10/12|1/8|rejected|
|votefast370_ETH_H030_S29_L5_N3000|12.364511|11.037016|9.710115|4.465399|0.087606|10/12|1/8|rejected|
|votefast370_ETH_H020_S27_L5_N3000|13.052679|11.337249|9.621807|4.494597|0.911592|10/12|2/8|rejected|
|votefast370_ETH_H030_S27_L5_N3000|12.168490|10.881703|9.595056|4.424615|0.316937|10/12|1/8|rejected|
|votefast370_ETH_H030_S28_L5_N3000|12.174674|10.848758|9.523072|4.430253|-0.113757|10/12|1/8|rejected|
|votefast370_parent_B1000_E3000_H020_S29_L5|9.272381|8.114730|6.957280|3.384873|0.462168|9/12|4/8|rejected|
|votefast370_parent_B1000_E3000_H020_S28_L5|9.341297|8.136711|6.932165|2.850658|0.481422|10/12|5/8|rejected|
|votefast370_parent_B1000_E3000_H025_S27_L5|8.103298|7.124784|6.146294|2.819480|0.233801|10/12|3/8|rejected|
|votefast370_parent_B1000_E3000_H025_S28_L5|8.171283|7.121998|6.072781|2.823629|0.054627|10/12|4/8|rejected|
|votefast370_parent_B1000_E3000_H025_S29_L5|8.116976|7.065010|6.013295|2.834699|0.035511|10/12|3/8|rejected|
|votefast370_parent_B1000_E3000_H030_S29_L5|7.679327|6.767267|5.855505|2.832408|0.241365|10/12|3/8|rejected|
|votefast370_parent_B1000_E3000_H020_S27_L5|8.023411|6.917384|5.811351|2.842619|0.667883|10/12|4/8|rejected|
|votefast370_parent_B1000_E3000_H030_S27_L5|7.581316|6.689611|5.797975|2.819480|0.360464|10/12|3/8|rejected|
|votefast370_parent_B1000_E3000_H030_S28_L5|7.584408|6.673139|5.761983|2.821358|0.136817|10/12|3/8|rejected|
|votefast370_ETH_H030_S27_L2_N3000|7.664038|6.037469|4.411110|5.232366|-0.898224|8/12|1/8|rejected|
|votefast370_ETH_H030_S29_L2_N3000|7.452832|5.832708|4.212524|4.716251|-0.581607|7/12|2/8|rejected|
|votefast370_ETH_H030_S28_L2_N3000|7.346148|5.724965|4.103665|4.478176|-0.791367|8/12|2/8|rejected|
|votefast370_ETH_H020_S29_L2_N3000|8.040130|5.869479|3.698163|5.764207|-0.101480|6/12|3/8|rejected|
|votefast370_parent_B1000_E3000_H030_S27_L2|5.329090|4.267494|3.206002|2.851854|-0.257367|10/12|4/8|rejected|
|votefast370_parent_B1000_E3000_H030_S29_L2|5.223487|4.165113|3.106709|2.928949|-0.094916|9/12|4/8|rejected|
|votefast370_parent_B1000_E3000_H030_S28_L2|5.170145|4.111242|3.052280|2.674063|-0.201759|10/12|4/8|rejected|
|votefast370_parent_B1000_E3000_H020_S29_L2|5.517136|4.183499|2.849529|3.332614|0.150152|9/12|5/8|rejected|
|votefast370_parent_B1000_E3000_H025_S27_L2|3.719027|2.538168|1.357457|3.010877|0.185937|8/12|5/8|rejected|
|votefast370_parent_B1000_E3000_H025_S29_L2|3.519246|2.373015|1.226799|3.332614|0.353382|8/12|5/8|rejected|
|votefast370_parent_B1000_E3000_H025_S28_L2|3.465904|2.319144|1.172370|3.074429|0.243819|9/12|5/8|rejected|
|votefast370_ETH_H025_S27_L2_N3000|4.443911|2.578818|0.714019|6.006195|-0.037236|6/12|2/8|rejected|
|votefast370_ETH_H025_S29_L2_N3000|4.044350|2.248512|0.452704|5.764207|0.298718|5/12|3/8|rejected|
|votefast370_ETH_H025_S28_L2_N3000|3.937665|2.140769|0.343845|5.249234|0.078209|6/12|3/8|rejected|
|votefast370_parent_B1000_E3000_H020_S28_L2|2.265188|0.909324|-0.447062|4.260639|0.247795|8/12|5/8|rejected|
|votefast370_parent_B1000_E3000_H020_S27_L2|1.014236|-0.348396|-1.711163|3.896878|-0.057143|7/12|5/8|rejected|
|votefast370_ETH_H020_S28_L2_N3000|1.536234|-0.678871|-2.895019|7.183311|0.080820|6/12|3/8|rejected|
|votefast370_ETH_H020_S27_L2_N3000|-0.965671|-3.194311|-5.423220|8.079160|-0.553224|5/12|3/8|rejected|

全网格Sharpe正值比例、收益正值比例及最高观测单元边界诊断（只读已有结果，不改变资格）：{"native": {"dimension_count": 3, "cells": 36, "new_cells": 18, "old_readonly_cells": 18, "full3x_positive_Sharpe_fraction": 0.9444444444444444, "recent40_3x_positive_Sharpe_fraction": 0.75, "full3x_positive_net_fraction": 0.9444444444444444, "recent40_3x_positive_net_fraction": 0.75, "highest_observed_full3x_net_cell": "votefast370_ETH_H020_S29_L5_N3000", "highest_observed_cell_original_or_new_status": "rejected", "highest_observed_is_on_axis_boundary": {"return_hurdle": true, "trend_lookback_days": true, "lookback_days": true}, "descriptive_full_Sharpe_cliff_edges": 8, "old_qualifications_preserved": true, "recent6of8_by_fast_lookback": {"2": 0, "3": 0, "4": 0, "5": 0}, "new_recent6of8_by_slow_center": {"27": 0, "28": 0, "29": 0}, "not_untouched_test_or_global_optimum": true}, "parent": {"dimension_count": 3, "cells": 36, "new_cells": 18, "old_readonly_cells": 18, "full3x_positive_Sharpe_fraction": 0.9444444444444444, "recent40_3x_positive_Sharpe_fraction": 0.8888888888888888, "full3x_positive_net_fraction": 0.9444444444444444, "recent40_3x_positive_net_fraction": 0.8888888888888888, "highest_observed_full3x_net_cell": "votefast370_parent_B1000_E3000_H020_S29_L5", "highest_observed_cell_original_or_new_status": "rejected", "highest_observed_is_on_axis_boundary": {"reversal_return_hurdle": true, "trend_filter_lookback_days": true, "reversal_lookback_days": true}, "descriptive_full_Sharpe_cliff_edges": 5, "old_qualifications_preserved": true, "recent6of8_by_fast_lookback": {"2": 0, "3": 2, "4": 2, "5": 0}, "new_recent6of8_by_slow_center": {"27": 0, "28": 0, "29": 0}, "not_untouched_test_or_global_optimum": true}}。最高观测单元的预设网格边界标记已保存，不称全局最优；全期平台不能消除近期正折不足。

实际失败门槛计数：{"positive_all_costs": 4, "nine_of_twelve_positive_complete30d_1x_folds": 13, "recent40_positive_all_costs": 13, "recent40_six_of_eight_positive5d_1x_folds": 36, "gross_plus_funding_to_cost1_gte2_5": 3}。逐项真实结论见上表和report.json，不因全期收益正而放宽门槛。222成本行、2886全期折、1776近期折、40068新日边界、150敏感性边、216匹配对照完整留档；6图36面板已实际打开。
独立只读核验21旧原生/63成本曲线、3846条已保存成交与69930条已保存资金费记录，原完整NAV SHA保持；旧原生模型未重跑，父层未新增成交；18个新原生按实际订单/资金费/成本/风险计算并经独立整数信号与Decimal逐点审计，21个旧原生仅回放保存账本核对SHA。36新配置108成本场景共58861404完整NAV点、1512全期/逐折和972近期/逐折指标通过；40旧唯一结果SHA/资格保持，12324受保护文件不变。42新实际ID各自finish，84事件仅追加；36实际金融配置加6实际partial，全部完整spec在reserve前核对原生参数、父层两组件完整参数及周期别名，无本轮失配定义。
只读监控实际检查exit0：8011研究项，169既有paper观察/10账户；7975旧展示行完整字典不变。原候选累计2852点/场景、2789分钟，0新增日决策/成交，实际新增资金费记录0条；现金与资金费逐条独立核验，收入不随成本放大，16旧结算未重复；旧SMA累计38817点，0新日决策/成交。两者均非十策略实时报价执行或长期盈利证据。
真实命令/传输异常记录2项，见read_failures.json。本轮登记、账户续接及提交由持续stdin排他锁保护。所有真实负收益分折/近期、成功/失败和完整账户账本保留；行情与HTTPpacket留ignoreddata并绑定SHA，不提交大行情或凭据。main普通非强推，freshfetch/独立allheads/完整tree/blob/行情核验通过后释放自己锁。
