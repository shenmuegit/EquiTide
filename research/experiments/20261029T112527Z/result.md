# 20261029T112527Z 仅入场门控下的快ROC退出缓冲

实际18新ETH原生＋18固定BTC/ETH组合，共36配置/108成本场景；历史通过0、淘汰36。完整读取22478事件/11135ID和227份结论；初始16项均有实际证据。

Same-fast and cross-fast gateownership mixtures failed recent6of8. Test distinct native exit persistence:hold contrarian actual position modestly beyond fast ROC zero,with strict Eexit < Hentry. Hypothesis is reduced premature exit/churn may improve chronological foldbreadth after costs;hold longer can also worsen losses/funding. E/S/L batch fixed before new PnL,qualification unchanged.

事前固定E0.5/1/1.5% × S27/28/29 × L3/4，严格入场H2.5%固定，E<H。快ROC>H提议空、<-H提议多；否则已有多仓仅在ROC<E时保留，已有空仓仅在ROC>−E时保留，边界相等退出。E是快ROC越零后的退出阈值，不是按入场盈亏计算的止损。现金新入场仍需新的严格极端；慢多数S−1/S/S+1只约束现金/反向开仓，已有快方向一致持仓忽略慢票变化；无隐藏desired。

ETH独立10000银行固定N3000；BTC旧ROC31/H4/退出1%固定N1000、10000银行。原值[1,1]持有两整银行，父本金20000、入场预算4000=20%；不归一化/NAV缩放/转账/交叉保证金/再平衡。9旧原生/27成本NAV只从实际保存账本回放核对原SHA，不重跑源模型；18个新ETH原生实际计算自己的成交、资金费、成本与风险。18个父组合对齐因果纳秒/事件并集逐点相加，整体/逐折指标由完整净值重算，不平均Sharpe或收益率。

完整三维24格每作用域含6个旧E0真实数字邻居，合计92相邻边；旧12个结果保持原资格。匹配同H/S/L/N/仅入场门控的E0、同本金恒多及现金0对照。source E0 spec的persistence说明沿用了更早base文案；保留原字节，以原明确entries_only参数、实际执行代码及独立核验的实际决策绑定行为。新spec完整修正文案，E0全部旧行为回归通过；见spec_binding_review.json，历史未改写。

8真实合并Parquet及16年度/近期源SHA/字节固定。370日OOS2025-10-19UTC00:01至2026-10-24UTC00:01；33日上下文含30预热及3日初始embargo。静态规则不拟合，无未来标签，purge不适用；12完整30日折加10日尾折连续承接现金/数量/entry/成本/资金费。近期40从day330继承分8×5日，不重开本金或诊断平仓；仅原终点计费退出。重复历史属于开发验证，非未触碰最终测试。

每侧5bp费＋1bp半价差＋2bp滑点＋0.5×滞后20日日log波动×sqrt(实际原生成交金额/滞后20日quoteADV)冲击，参与率≤0.1%，不利tick/lot/最小金额/全额抵押约束。资金费=−有符号q×实际结算mark×rate，流出按1/2/3成本放大、收入不放大；永续不虚构现货借币。独立银行闭合小时不利mark和1%维持保证金为风险代理，缺L2/TCA/完整历史tier/tick清算/聚合容量证明。

固定门槛：全期/近期三档净正、1x月正折≥9/12及近期≥6/8、3x完整连续OOS整体DD≤25%、同作用域三维相邻索引半径1含自身全期3x净正≥60%、≥4往返、(参考毛利＋资金费)/成本≥2.5、现金/拒单/风险违规0、终点空仓及≥180日。资格未放宽。

{"new_financial_configs": 36, "new_native_components": 18, "new_passive_parents": 18, "passed_candidates": 0, "rejected_candidates": 36, "positive_configs_by_cost": {"1": 36, "2": 36, "3": 36}, "failed_criteria_counts": {"recent40_six_of_eight_positive5d_1x_folds": 36, "nine_of_twelve_positive_complete30d_1x_folds": 3}, "by_scope": {"native": {"new": 18, "passed": 0, "best_full3": {"name": "exitbuffer370_ETH_E150_S27_L3_H025_N3000", "return3_pct": 19.392533105253417, "whole_DD3_pct": 4.088286312944545, "recent_return3_pct": 2.3729066973719126, "positive_months1": 11, "positive_recent1": 3, "failed_criteria": ["recent40_six_of_eight_positive5d_1x_folds"]}}, "parent": {"new": 18, "passed": 0, "best_full3": {"name": "exitbuffer370_parent_B1000_E3000_X150_S27_L3_H025", "return3_pct": 10.696713793027278, "whole_DD3_pct": 2.711770248079093, "recent_return3_pct": 1.4578205425860302, "positive_months1": 10, "positive_recent1": 5, "failed_criteria": ["recent40_six_of_eight_positive5d_1x_folds"]}}}, "rows": {"cost": 150, "full_folds": 1950, "recent40_folds": 1200, "daily_NAV": 40068, "edges": 92, "reference_comparisons": 216}}

合成测试先RED后GREEN：9360组严格边界、持仓状态、未来不变性和4680项旧E0行为回归。新引擎只修改majority_target，simulate及数据、数量、成本、资金费、风险函数字节不变。独立整数信号/Decimal成交资金费/风险、每个NAV点及整体/逐折指标均实际核验。

原冻结单S28候选及SMA65从UTC08:30续接至10:30，只增加已闭合mark，不重计08资金费、不换本轮E缓冲策略。BTC08小时前后风险状态同一精确08:00时间戳，前状态零时长，09close应排除零时长前缀并核验后状态；09小时在10close核验。保留完整现金/数量/entry/费用/NAV前缀、35日候选/65日SMA上下文和3个候选日NAV边界。下一资金费16UTC、下一日决策Oct30UTC00:01。两类延迟shadow与paper10十策略实时报价观察分开。

研究背景为一手[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)与[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)。本轮退出缓冲假设为研究推论，非原论文复现。36个相关新试验及全部历史存在多重选择偏差，无DSR/PBO、独立未来资格或稳定实盘盈利证明。

复现目录/home/desktop/Documents/Codex/EquiTide。audit.py/audit_native.py独立核验真实原生成交、资金费、风险及组合逐点净值；check_sources.py/check_exports.py/check_feed.py只读核验；audit_candidate.py/audit_forward.py及forward.py --reproduce复现原账户。已完成精确配置不得重新reserve/evaluate。全部正负结果和完整账户账本/冻结规则/登记/失败保留；行情及原始HTTPpacket留ignoreddata并绑定SHA。仅main普通非强推，完整远端tree/blob/数据核验及发布实际exit0后释放自己锁。

已完成结果的只读E0匹配诊断（不改变资格或门槛）：{"new_financial_evaluations": 0, "source": "Finished report.json and verified reference_comparisons.csv only", "report_sha256": "e925def2f7c8310a8395ed33a9b6d2f86d2bbc09032ad1c2f053cf02da72c638", "by_scope": {"native": {"pairs": 18, "full3_net_improved": 14, "recent40_3_net_improved": 2, "full3_execution_delta_range": [-6, 0], "full3_return_delta_range_pp": [-2.4210927835685023, 5.935815269529554], "recent_positive_fold_histogram": {"4": 6, "3": 12}}, "parent": {"pairs": 18, "full3_net_improved": 14, "recent40_3_net_improved": 7, "full3_execution_delta_range": [-6, 0], "full3_return_delta_range_pp": [-1.2105463917842618, 2.967907634764755], "recent_positive_fold_histogram": {"5": 18}}}}。一手发布页本轮已实际访问，日期/用途见literature_access.json。

历史通过项目只读冻结检查：0项。完整spec/来源/报告/账本SHA见candidate_validation.json；不改原冻结L3未来账户。

逐配置结果（收益/回撤单位%，三倍全期回撤使用完整连续OOS）：

|配置|1x收益|2x收益|3x收益|3x最大回撤|近期3x收益|1x月正折|1x近期正折|结论|
|---|---:|---:|---:|---:|---:|---:|---:|---|
|exitbuffer370_ETH_E150_S27_L3_H025_N3000|22.952987|21.173591|19.392533|4.088286|2.372907|11/12|3/8|rejected|
|exitbuffer370_ETH_E150_S28_L3_H025_N3000|23.043615|21.149325|19.253280|4.066000|2.465036|11/12|3/8|rejected|
|exitbuffer370_ETH_E150_S28_L4_H025_N3000|20.483300|18.769929|17.056165|5.316885|1.805556|10/12|3/8|rejected|
|exitbuffer370_ETH_E150_S27_L4_H025_N3000|20.056536|18.384091|16.711200|5.332769|1.810989|10/12|3/8|rejected|
|exitbuffer370_ETH_E100_S27_L3_H025_N3000|20.108085|18.350141|16.590477|4.161733|2.431322|10/12|3/8|rejected|
|exitbuffer370_ETH_E100_S28_L3_H025_N3000|20.198712|18.325875|16.451224|4.138640|2.525848|10/12|3/8|rejected|
|exitbuffer370_ETH_E150_S29_L3_H025_N3000|19.055605|17.235827|15.414390|5.930669|2.549118|10/12|3/8|rejected|
|exitbuffer370_ETH_E050_S27_L3_H025_N3000|18.836073|17.077135|15.316563|4.209125|2.421531|10/12|4/8|rejected|
|exitbuffer370_ETH_E100_S28_L4_H025_N3000|18.532177|16.791815|15.051133|5.346357|1.581850|10/12|3/8|rejected|
|exitbuffer370_ETH_E100_S27_L4_H025_N3000|18.101171|16.401730|14.701916|5.362838|1.586742|10/12|3/8|rejected|
|exitbuffer370_ETH_E050_S28_L3_H025_N3000|18.446199|16.572143|14.696008|4.185586|2.527903|10/12|4/8|rejected|
|exitbuffer370_ETH_E150_S29_L4_H025_N3000|16.197973|14.560717|12.923067|6.197454|1.872879|9/12|3/8|rejected|
|exitbuffer370_ETH_E050_S29_L3_H025_N3000|16.498590|14.684670|12.868766|5.995595|2.569879|10/12|4/8|rejected|
|exitbuffer370_ETH_E050_S28_L4_H025_N3000|16.127047|14.404800|12.682340|5.416634|1.426645|10/12|4/8|rejected|
|exitbuffer370_ETH_E100_S29_L3_H025_N3000|16.210702|14.412377|12.612333|6.038722|2.614204|10/12|3/8|rejected|
|exitbuffer370_ETH_E050_S27_L4_H025_N3000|15.696040|14.014714|12.333123|5.433662|1.431144|10/12|4/8|rejected|
|exitbuffer370_ETH_E100_S29_L4_H025_N3000|14.236241|12.571984|10.907405|6.351554|1.641921|9/12|3/8|rejected|
|exitbuffer370_parent_B1000_E3000_X150_S27_L3_H025|12.973565|11.835555|10.696714|2.711770|1.457821|10/12|5/8|rejected|
|exitbuffer370_parent_B1000_E3000_X150_S28_L3_H025|13.018879|11.823422|10.627087|2.703993|1.506002|10/12|5/8|rejected|
|exitbuffer370_parent_B1000_E3000_X150_S28_L4_H025|11.738721|10.633724|9.528530|2.985453|1.149651|10/12|5/8|rejected|
|exitbuffer370_parent_B1000_E3000_X150_S27_L4_H025|11.525339|10.440805|9.356047|2.990189|1.151486|10/12|5/8|rejected|
|exitbuffer370_parent_B1000_E3000_X100_S27_L3_H025|11.551113|10.423830|9.295686|2.737117|1.476784|9/12|5/8|rejected|
|exitbuffer370_parent_B1000_E3000_X100_S28_L3_H025|11.596427|10.411697|9.226059|2.729194|1.525614|9/12|5/8|rejected|
|exitbuffer370_ETH_E050_S29_L4_H025_N3000|12.075171|10.426175|8.777061|6.456838|1.478621|9/12|4/8|rejected|
|exitbuffer370_parent_B1000_E3000_X150_S29_L3_H025|11.024873|9.866673|8.707642|2.887761|1.533001|9/12|5/8|rejected|
|exitbuffer370_parent_B1000_E3000_X050_S27_L3_H025|10.915108|9.787327|8.658729|2.753246|1.466142|9/12|5/8|rejected|
|exitbuffer370_parent_B1000_E3000_X100_S28_L4_H025|10.763160|9.644667|8.526014|3.007822|1.026468|10/12|5/8|rejected|
|exitbuffer370_parent_B1000_E3000_X100_S27_L4_H025|10.547656|9.449624|8.351405|3.012700|1.028140|10/12|5/8|rejected|
|exitbuffer370_parent_B1000_E3000_X050_S28_L3_H025|10.720170|9.534831|8.348451|2.745257|1.518658|9/12|5/8|rejected|
|exitbuffer370_parent_B1000_E3000_X150_S29_L4_H025|9.596057|8.529118|7.461981|3.043202|1.172019|8/12|5/8|rejected|
|exitbuffer370_parent_B1000_E3000_X050_S29_L3_H025|9.746366|8.591095|7.434830|2.890281|1.531770|9/12|5/8|rejected|
|exitbuffer370_parent_B1000_E3000_X050_S28_L4_H025|9.560595|8.451159|7.341617|3.020388|0.939750|10/12|5/8|rejected|
|exitbuffer370_parent_B1000_E3000_X100_S29_L3_H025|9.602422|8.454948|7.306614|2.915372|1.553327|9/12|5/8|rejected|
|exitbuffer370_parent_B1000_E3000_X050_S27_L4_H025|9.345091|8.256117|7.167009|3.025337|0.941296|10/12|5/8|rejected|
|exitbuffer370_parent_B1000_E3000_X100_S29_L4_H025|8.615192|7.534752|6.454150|3.078024|1.046655|8/12|5/8|rejected|
|exitbuffer370_parent_B1000_E3000_X050_S29_L4_H025|7.534656|6.461847|5.388978|3.104296|0.957328|8/12|5/8|rejected|

全网格Sharpe正值比例、收益正值比例及最高观测单元边界诊断（只读已有结果，不改变资格）：{"native": {"dimension_count": 3, "cells": 24, "new_cells": 18, "old_readonly_cells": 6, "full3x_positive_Sharpe_fraction": 1.0, "recent40_3x_positive_Sharpe_fraction": 1.0, "full3x_positive_net_fraction": 1.0, "recent40_3x_positive_net_fraction": 1.0, "highest_observed_full3x_net_cell": "exitbuffer370_ETH_E150_S27_L3_H025_N3000", "highest_observed_cell_original_or_new_status": "rejected", "highest_observed_is_on_axis_boundary": {"exit_buffer_fraction": true, "trend_lookback_days": true, "lookback_days": true}, "descriptive_full_Sharpe_cliff_edges": 13, "old_qualifications_preserved": true, "recent6of8_by_fast_lookback": {"3": 0, "4": 0}, "new_recent6of8_by_slow_center": {"27": 0, "28": 0, "29": 0}, "not_untouched_test_or_global_optimum": true}, "parent": {"dimension_count": 3, "cells": 24, "new_cells": 18, "old_readonly_cells": 6, "full3x_positive_Sharpe_fraction": 1.0, "recent40_3x_positive_Sharpe_fraction": 1.0, "full3x_positive_net_fraction": 1.0, "recent40_3x_positive_net_fraction": 1.0, "highest_observed_full3x_net_cell": "exitbuffer370_parent_B1000_E3000_X150_S27_L3_H025", "highest_observed_cell_original_or_new_status": "rejected", "highest_observed_is_on_axis_boundary": {"reversal_exit_buffer_fraction": true, "trend_filter_lookback_days": true, "reversal_lookback_days": true}, "descriptive_full_Sharpe_cliff_edges": 10, "old_qualifications_preserved": true, "recent6of8_by_fast_lookback": {"3": 0, "4": 0}, "new_recent6of8_by_slow_center": {"27": 0, "28": 0, "29": 0}, "not_untouched_test_or_global_optimum": true}}。最高观测单元的预设网格边界标记已保存，不称全局最优；全期平台不能消除近期正折不足。

实际失败门槛计数：{"recent40_six_of_eight_positive5d_1x_folds": 36, "nine_of_twelve_positive_complete30d_1x_folds": 3}。逐项真实结论见上表和report.json，不因全期收益正而放宽门槛。150成本行、1950全期折、1200近期折、40068新日边界、92敏感性边、216匹配对照完整留档；6图36面板已实际打开。
独立只读核验9旧原生/27成本曲线、1260条已保存成交与29970条已保存资金费记录，原完整NAV SHA保持；旧原生模型未重跑，父层未新增成交；18个新原生按实际订单/资金费/成本/风险计算并经独立整数信号与Decimal逐点审计，9个旧原生仅回放保存账本核对SHA。36新配置108成本场景共58861404完整NAV点、1512全期/逐折和972近期/逐折指标通过；16旧唯一结果SHA/资格保持，14016受保护文件不变。42新实际ID各自finish，84事件仅追加；36实际金融配置加6实际partial，全部完整spec在reserve前核对原生参数、父层两组件完整参数及周期别名，无本轮失配定义。
只读监控实际检查exit0：8281研究项，175既有paper观察/10账户；8245旧展示行完整字典不变。原候选累计3591点/场景、3509分钟，0新增日决策/成交，实际新增资金费记录0条；现金与资金费逐条独立核验，收入不随成本放大，08旧结算未重复、零时长前缀排除及08/09小时风险承接；旧SMA累计39538点，0新日决策/成交。两者均非十策略实时报价执行或长期盈利证据。
真实命令/传输异常记录0项，见read_failures.json。本轮登记、账户续接及提交由持续stdin排他锁保护。所有真实负收益分折/近期、成功/失败和完整账户账本保留；行情与HTTPpacket留ignoreddata并绑定SHA，不提交大行情或凭据。main普通非强推，freshfetch/独立allheads/完整tree/blob/行情核验通过后释放自己锁。
