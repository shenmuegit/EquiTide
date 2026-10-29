# 20261029T052355Z 慢多数门控仅约束入场

实际18个ETH原生＋18个固定BTC/ETH组合，共36配置、108成本场景；历史通过0、淘汰36。读取22094事件/10943ID及224份既往结论，初始16项已有实际证据。

事前固定H2/2.5/3% × S27/28/29 × L3/4，18格每作用域；新规则只对现金新开或反向开仓检查S−1/S/S+1至少两票同号慢ROC。已有实际持仓只要快ROC仍支持同方向即保留，不因慢票变化平仓。快ROC零/反向仍退出；现金重新入场仍需新严格极端，无隐藏desired。旧相同H/S/L的完整慢门控36个结果只读作对照，不混入新参数邻域，不重新评级。

ETH独立10000银行固定N3000；BTC旧ROC31/H4/退出1%固定N1000、10000银行。组合原值[1,1]持有两整银行，本金20000、入场预算4000=20%；不归一化、净值缩放、转账、交叉保证金或再平衡。21个旧原生/63条成本曲线从真实已保存账本回放并核对原SHA；18个新原生实际独立计算成交、费用、资金费、风险，再与旧BTC完整因果时轴对齐相加。

下一UTC00:01真实OPEN执行；q=floor(N/此前完整close/lot)*lot。33日上下文含30预热及3日初始embargo；静态规则无拟合、未来标签，purge不适用。370日OOS为2025-10-19UTC00:01至2026-10-24UTC00:01，12完整30日折＋10日尾折连续承接现金/数量/entry/费用；近期40由day330继承状态分8×5日，不重开本金或诊断平仓，仅原终点计费退出。反复研究的历史属于开发验证，非未触碰最终测试。

每侧5bp费＋1bp半价差＋2bp滑点＋0.5×滞后20日日log波动×sqrt(实际成交金额/滞后20日quoteADV)冲击，参与率≤0.1%，tick/lot/最小金额/100%抵押约束。资金费=−有符号q×实际结算mark×rate，流出按1/2/3倍成本放大、收入不放大；永续无虚构现货借币。闭合小时不利mark高低和正时长状态重叠检查独立银行1%维持保证金代理；缺L2/TCA/历史完整tier/tick清算/容量证明。

固定门槛：全期及近期三成本净正、1x月正折≥9/12、近期≥6/8、全连续OOS的3x整体回撤≤25%、同机制三维相邻索引半径1含自身全期3x净正≥60%、≥4往返、(参考毛利＋资金费)/成本≥2.5、现金/拒单/风险违规0、终点平仓、≥180日。预设36配置和全部既往试验存在多重选择偏差，无DSR/PBO或稳定实盘盈利证明。

{"new_financial_configs": 36, "new_native_components": 18, "new_passive_parents": 18, "passed_candidates": 0, "rejected_candidates": 36, "positive_configs_by_cost": {"1": 36, "2": 36, "3": 36}, "failed_criteria_counts": {"recent40_six_of_eight_positive5d_1x_folds": 36, "nine_of_twelve_positive_complete30d_1x_folds": 1}, "by_scope": {"native": {"new": 18, "passed": 0, "best_full3": {"name": "entrygate370_ETH_H025_S27_L4_N3000", "return3_pct": 14.754215588976693, "whole_DD3_pct": 4.54129594861662, "recent_return3_pct": 1.8974042756431553, "positive_months1": 11, "positive_recent1": 3, "failed_criteria": ["recent40_six_of_eight_positive5d_1x_folds"]}}, "parent": {"new": 18, "passed": 0, "best_full3": {"name": "entrygate370_parent_B1000_E3000_H025_S27_L4", "return3_pct": 8.377555034888928, "whole_DD3_pct": 2.92383413288525, "recent_return3_pct": 1.1907055112805542, "positive_months1": 11, "positive_recent1": 5, "failed_criteria": ["recent40_six_of_eight_positive5d_1x_folds"]}}}, "rows": {"cost": 222, "full_folds": 2886, "recent40_folds": 1776, "daily_NAV": 40068, "edges": 66, "reference_comparisons": 216}}

新规则合成测试先RED后GREEN，2970组严格边界/实际持仓状态/未来不变性及旧默认规则回归；仅majority_target和simulate改变，数据、数量、执行成本、资金费和风险函数原字节保持。实际回测由独立整数信号、Decimal成交/资金费、逐点净值及整体/逐折指标审计。

6图36面板及全部收益/Sharpe/Calmar/回撤/相邻边/匹配旧规则和恒多对照留档。原冻结单S28候选与SMA65独立续接02:30至04:30，仅已闭合mark，规则/本金/持仓/成本完整承接；这两个延迟shadow账户与十策略实时报价账户分开。下一日决策Oct30UTC00:01，下一资金费Oct29UTC08:00。

背景沿用2026-10-27实际访问的一手[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)及[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)。门控仅用于入场是本轮研究假设，非原论文复现或盈利迁移结论。

复现工作目录/home/desktop/Documents/Codex/EquiTide，audit.py/audit_native.py/check_sources.py/check_exports.py/check_feed.py只读核验；原账户audit_candidate.py/audit_forward.py和forward.py --reproduce复现。已完成精确配置不得再次reserve/evaluate。所有正负结果与失败事实保留，行情及原始HTTPpacket位于ignoreddata并绑定SHA。main普通非强推及完整远端tree/blob/行情核验后释放自身排他锁。

与相同H/S/L/本金/预算的旧完整慢门控逐项配对：18个原生及18个组合的三倍成本全期收益、近期总收益全部改善，实际成交次数各减少2至8次；但近期正折数量只在8个原生、2个组合改善，仍无配置达到6/8。详见matched_gate_comparison.json及216条逐成本对照；提升全期收益未解决预设的近期折覆盖要求。
本轮2026-10-29再次实际访问两份一手论文发布页，日期、用途及推论边界存literature_access.json。

历史通过项目只读冻结检查：0项。完整spec/来源/报告/账本SHA见candidate_validation.json；不改原冻结L3未来账户。

逐配置结果（收益/回撤单位%，三倍全期回撤使用完整连续OOS）：

|配置|1x收益|2x收益|3x收益|3x最大回撤|近期3x收益|1x月正折|1x近期正折|结论|
|---|---:|---:|---:|---:|---:|---:|---:|---|
|entrygate370_ETH_H025_S27_L4_N3000|17.987056|16.370986|14.754216|4.541296|1.897404|11/12|3/8|rejected|
|entrygate370_ETH_H025_S28_L4_N3000|17.913831|16.133844|14.353210|4.515773|1.996451|11/12|3/8|rejected|
|entrygate370_ETH_H030_S28_L4_N3000|17.153024|15.585662|14.018278|3.656438|1.179788|11/12|3/8|rejected|
|entrygate370_ETH_H025_S27_L3_N3000|17.393263|15.666230|13.938020|4.227071|2.428970|10/12|4/8|rejected|
|entrygate370_ETH_H025_S28_L3_N3000|17.003388|15.161238|13.317465|4.203331|2.536694|10/12|4/8|rejected|
|entrygate370_ETH_H020_S27_L4_N3000|17.069705|15.192637|13.314694|5.033628|1.921972|10/12|3/8|rejected|
|entrygate370_ETH_H020_S28_L4_N3000|16.995877|15.051460|13.106222|5.047793|2.018906|10/12|3/8|rejected|
|entrygate370_ETH_H030_S27_L4_N3000|15.203753|13.852696|12.501706|3.656438|1.103564|11/12|2/8|rejected|
|entrygate370_ETH_H020_S28_L3_N3000|16.650090|14.418347|12.184694|5.865757|2.562965|9/12|4/8|rejected|
|entrygate370_ETH_H020_S27_L3_N3000|16.216379|14.116830|12.015531|5.904343|2.471688|9/12|4/8|rejected|
|entrygate370_ETH_H030_S29_L4_N3000|14.682784|13.247572|11.812434|3.470798|1.203343|11/12|3/8|rejected|
|entrygate370_ETH_H020_S29_L3_N3000|16.012080|13.844343|11.674843|6.198433|2.574967|8/12|4/8|rejected|
|entrygate370_ETH_H025_S29_L3_N3000|15.055779|13.273765|11.490223|6.130409|2.579341|10/12|4/8|rejected|
|entrygate370_ETH_H030_S27_L3_N3000|13.689930|12.112323|10.533375|4.314581|1.648940|10/12|3/8|rejected|
|entrygate370_ETH_H025_S29_L4_N3000|13.861955|12.155219|10.447931|6.494677|2.068503|10/12|3/8|rejected|
|entrygate370_ETH_H030_S28_L3_N3000|13.036925|11.399498|9.760284|4.296020|1.756419|10/12|4/8|rejected|
|entrygate370_ETH_H020_S29_L4_N3000|12.944000|11.072836|9.200943|6.534321|2.092618|9/12|3/8|rejected|
|entrygate370_parent_B1000_E3000_H025_S27_L4|10.490599|9.434253|8.377555|2.923834|1.190706|11/12|5/8|rejected|
|entrygate370_parent_B1000_E3000_H025_S28_L4|10.453987|9.315681|8.177052|2.915314|1.241007|11/12|5/8|rejected|
|entrygate370_ETH_H030_S29_L3_N3000|11.352446|9.719858|8.085578|6.256747|1.784119|10/12|4/8|rejected|
|entrygate370_parent_B1000_E3000_H030_S28_L4|10.073583|9.041590|8.009586|2.045355|0.813543|10/12|5/8|rejected|
|entrygate370_parent_B1000_E3000_H025_S27_L3|10.193702|9.081874|7.969457|2.759307|1.463952|9/12|5/8|rejected|
|entrygate370_parent_B1000_E3000_H025_S28_L3|9.998765|8.829378|7.659180|2.751283|1.516796|9/12|5/8|rejected|
|entrygate370_parent_B1000_E3000_H020_S27_L4|10.031923|8.845078|7.657794|2.932903|1.198762|11/12|5/8|rejected|
|entrygate370_parent_B1000_E3000_H020_S28_L4|9.995010|8.774490|7.553558|2.924330|1.248291|11/12|5/8|rejected|
|entrygate370_parent_B1000_E3000_H030_S27_L4|9.098948|8.175108|7.251300|2.051306|0.771262|10/12|4/8|rejected|
|entrygate370_parent_B1000_E3000_H020_S28_L3|9.822116|8.457933|7.092794|3.693537|1.524940|9/12|5/8|rejected|
|entrygate370_parent_B1000_E3000_H020_S27_L3|9.605260|8.307174|7.008213|3.713343|1.477297|9/12|5/8|rejected|
|entrygate370_parent_B1000_E3000_H030_S29_L4|8.838463|7.872545|6.906664|2.480402|0.822005|9/12|5/8|rejected|
|entrygate370_parent_B1000_E3000_H020_S29_L3|9.503111|8.170931|6.837869|3.044057|1.528634|10/12|5/8|rejected|
|entrygate370_parent_B1000_E3000_H025_S29_L3|9.024961|7.885642|6.745559|2.953227|1.529976|9/12|5/8|rejected|
|entrygate370_parent_B1000_E3000_H030_S27_L3|8.342036|7.304921|6.267135|2.788513|1.049221|9/12|4/8|rejected|
|entrygate370_parent_B1000_E3000_H025_S29_L4|8.428048|7.326369|6.224413|3.113637|1.264108|9/12|5/8|rejected|
|entrygate370_parent_B1000_E3000_H030_S28_L3|8.015534|6.948508|5.880589|2.782367|1.102067|9/12|5/8|rejected|
|entrygate370_parent_B1000_E3000_H020_S29_L4|7.969071|6.785177|5.600919|3.123367|1.271666|9/12|5/8|rejected|
|entrygate370_parent_B1000_E3000_H030_S29_L3|7.173294|6.108688|5.043236|2.984413|1.110950|9/12|5/8|rejected|

全网格Sharpe正值比例、收益正值比例及最高观测单元边界诊断（只读已有结果，不改变资格）：{"native": {"dimension_count": 3, "cells": 18, "new_cells": 18, "old_readonly_cells": 0, "full3x_positive_Sharpe_fraction": 1.0, "recent40_3x_positive_Sharpe_fraction": 1.0, "full3x_positive_net_fraction": 1.0, "recent40_3x_positive_net_fraction": 1.0, "highest_observed_full3x_net_cell": "entrygate370_ETH_H025_S27_L4_N3000", "highest_observed_cell_original_or_new_status": "rejected", "highest_observed_is_on_axis_boundary": {"return_hurdle": false, "trend_lookback_days": true, "lookback_days": true}, "descriptive_full_Sharpe_cliff_edges": 10, "old_qualifications_preserved": true, "recent6of8_by_fast_lookback": {"3": 0, "4": 0}, "new_recent6of8_by_slow_center": {"27": 0, "28": 0, "29": 0}, "not_untouched_test_or_global_optimum": true}, "parent": {"dimension_count": 3, "cells": 18, "new_cells": 18, "old_readonly_cells": 0, "full3x_positive_Sharpe_fraction": 1.0, "recent40_3x_positive_Sharpe_fraction": 1.0, "full3x_positive_net_fraction": 1.0, "recent40_3x_positive_net_fraction": 1.0, "highest_observed_full3x_net_cell": "entrygate370_parent_B1000_E3000_H025_S27_L4", "highest_observed_cell_original_or_new_status": "rejected", "highest_observed_is_on_axis_boundary": {"reversal_return_hurdle": false, "trend_filter_lookback_days": true, "reversal_lookback_days": true}, "descriptive_full_Sharpe_cliff_edges": 5, "old_qualifications_preserved": true, "recent6of8_by_fast_lookback": {"3": 0, "4": 0}, "new_recent6of8_by_slow_center": {"27": 0, "28": 0, "29": 0}, "not_untouched_test_or_global_optimum": true}}。最高观测单元的预设网格边界标记已保存，不称全局最优；全期平台不能消除近期正折不足。

实际失败门槛计数：{"recent40_six_of_eight_positive5d_1x_folds": 36, "nine_of_twelve_positive_complete30d_1x_folds": 1}。逐项真实结论见上表和report.json，不因全期收益正而放宽门槛。222成本行、2886全期折、1776近期折、40068新日边界、66敏感性边、216匹配对照完整留档；6图36面板已实际打开。
独立只读核验21旧原生/63成本曲线、3846条已保存成交与69930条已保存资金费记录，原完整NAV SHA保持；旧原生模型未重跑，父层未新增成交；18个新原生按实际订单/资金费/成本/风险计算并经独立整数信号与Decimal逐点审计，21个旧原生仅回放保存账本核对SHA。36新配置108成本场景共58861404完整NAV点、1512全期/逐折和972近期/逐折指标通过；40旧唯一结果SHA/资格保持，13161受保护文件不变。42新实际ID各自finish，84事件仅追加；36实际金融配置加6实际partial，全部完整spec在reserve前核对原生参数、父层两组件完整参数及周期别名，无本轮失配定义。
只读监控实际检查exit0：8137研究项，172既有paper观察/10账户；8101旧展示行完整字典不变。原候选累计3223点/场景、3149分钟，0新增日决策/成交，实际新增资金费记录0条；现金与资金费逐条独立核验，收入不随成本放大，00旧结算未重复、02/03小时风险已承接；旧SMA累计39178点，0新日决策/成交。两者均非十策略实时报价执行或长期盈利证据。
真实命令/传输异常记录2项，见read_failures.json。本轮登记、账户续接及提交由持续stdin排他锁保护。所有真实负收益分折/近期、成功/失败和完整账户账本保留；行情与HTTPpacket留ignoreddata并绑定SHA，不提交大行情或凭据。main普通非强推，freshfetch/独立allheads/完整tree/blob/行情核验通过后释放自己锁。
