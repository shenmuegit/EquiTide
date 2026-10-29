# 20261029T032224Z 多数慢趋势最小幅度G验证

实际18新ETH原生＋18新BTC/ETH组合，36配置/108成本场景；历史通过0、淘汰36。完整读取21990事件/10891ID及223份结论；初始16项已有实际证据。

本轮事前固定快反转阈值H2.5%、快周期L3/4、慢中心S27/28/29；新慢趋势最小幅度G0.5/1/2%，旧G0六原生＋六组合只读。全3D G0/0.5/1/2% × S27/28/29 × L3/4，每作用域24格/46相邻边，合计48格/92边；36新配置逐个先reserve再计算，旧资格保持。假设是忽略接近零的弱慢趋势，能否改善S28附近的近期集中，计算前固定全部参数、边界和门槛。

ETH前一完整L日ROC严格>2.5%反转空/<-2.5%反转多，带内只保留ROC<0的实际多、ROC>0的实际空，零退出。S-1/S/S+1三个完整慢ROC至少两票严格>G允许多、至少两票严格<-G允许空，否则平仓；等号与中性带不允许开仓或保留不兼容持仓。快方向须匹配慢允许方向，现金重入需新严格快极端，无隐藏desired。UTC00:01实际OPEN执行，q=floor(N/此前完整close/lot)*lot；不读未来OPEN/资金费/未闭合数据决定信号或数量。396项合成边界、投票、持仓/现金与未来不变性和G0回归检查已通过，不计作真实回测。

新引擎只修改majority_target与simulate的G传递/投票日志，其余数据、成交、资金费、数量、成本与风险函数原字节保持。ETH独立银行10000，固定N3000；BTC旧ROC31/H4%/退出1%、银行10000、N1000。父层原值[1,1]持有两完整银行，初始20000、入场预算4000=20%，不归一化、NAV缩放、转账、交叉保证金或再平衡。9旧原生/27成本NAV从已保存账本恢复核对原SHA；18新ETH实际计算专属成交/资金费/成本/风险；18组合沿共同纳秒/事件时轴因果相加，整体指标从完整净值重算。

8真实合并Parquet及16年度/近期源SHA固定。370日OOS2025-10-19UTC00:01至2026-10-24UTC00:01；33日上下文含30预热与3日初始embargo。静态规则无拟合/未来标签，purge不适用；12完整30日折加10日尾折连续承接现金/q/entry/费用，近期40从day330继承分8×5日，不重开本金或诊断平仓，仅原终点计费退出。反复使用历史属于开发验证，不是未触碰最终测试。

每侧5bp费+1bp半价差+2bp滑点+0.5×滞后20日日log波动×sqrt(实际订单金额/滞后20日quoteADV)冲击，参与率≤0.1%，不利tick/lot/最小金额/全额抵押约束。资金费=-有符号q×实际mark×rate，流出随1/2/3放大、收入不放大；永续不虚构现货借币。独立银行闭合小时1%维持保证金代理，缺L2/TCA/完整历史tier/tick清算及聚合容量证明。

门槛保持全期/近期三成本净正、1x完整月≥9/12正折且近期≥6/8、3x完整连续整体DD≤25%、3D相邻索引半径1含自身全期3x净正≥60%、≥4往返、(参考毛利+资金费)/成本≥2.5、现金/拒单/风险违规0、终点空仓且≥180日。匹配同H/S/L/N的G0旧规则、同本金恒多及现金0；旧资格不按扩展邻域重评。

{"new_financial_configs": 36, "new_native_components": 18, "new_passive_parents": 18, "passed_candidates": 0, "rejected_candidates": 36, "positive_configs_by_cost": {"1": 36, "2": 36, "3": 36}, "failed_criteria_counts": {"nine_of_twelve_positive_complete30d_1x_folds": 9, "recent40_six_of_eight_positive5d_1x_folds": 36, "recent40_positive_all_costs": 2}, "by_scope": {"native": {"new": 18, "passed": 0, "best_full3": {"name": "slowbuffer370_ETH_G200_S29_L3_H025_N3000", "return3_pct": 12.820121865638123, "whole_DD3_pct": 4.224177075880653, "recent_return3_pct": 1.8239511904310612, "positive_months1": 10, "positive_recent1": 3, "failed_criteria": ["recent40_six_of_eight_positive5d_1x_folds"]}}, "parent": {"new": 18, "passed": 0, "best_full3": {"name": "slowbuffer370_parent_B1000_E3000_G200_S29_L3_H025", "return3_pct": 7.410508173219643, "whole_DD3_pct": 2.7583315686161236, "recent_return3_pct": 1.146336044200491, "positive_months1": 10, "positive_recent1": 5, "failed_criteria": ["recent40_six_of_eight_positive5d_1x_folds"]}}}, "rows": {"cost": 150, "full_folds": 1950, "recent40_folds": 1200, "daily_NAV": 40068, "edges": 92, "reference_comparisons": 216}}

原单S28候选及SMA65按原规则从UTC00:30续接至02:30，35日候选/65日SMA上下文、第三个日净值点与完整净值前缀承接；00:00资金费已在上轮入账，不重复。BTC00小时风险栈两条状态同为00:00，第一条持续时长为零，01close只检查有正重叠的资金费后状态，再检查01小时到02close；不丢失风险栈、不重开本金、不切换新G规则。下一资金费08:00、下一日决策Oct30UTC00:01。延迟闭合行情重建与paper10实时报价模拟分开。

背景沿用2026-10-27实际访问的一手[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)及[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)。新G假设是研究推论。36个相关新试验加全部既往试验存在多重选择偏差，无DSR/PBO、独立未来或稳定实盘盈利证明。

复现工作目录/home/desktop/Documents/Codex/EquiTide。audit.py/audit_native.py独立整数信号、Decimal成交/资金费、逐点NAV/风险核验，check_exports.py/check_sources.py/check_feed.py只读验证；audit_candidate.py/audit_forward.py、forward.py --reproduce复现原账户。不得重reserve/evaluate已完成精确配置；所有正负结果/账户账本/规则/失败保留，行情/HTTPpacket留ignoreddata绑定SHA；main非强推并验证完整远端tree/blob/行情后释放本轮锁。

历史通过项目只读冻结检查：0项。完整spec/来源/报告/账本SHA见candidate_validation.json；不改原冻结L3未来账户。

逐配置结果（收益/回撤单位%，三倍全期回撤使用完整连续OOS）：

|配置|1x收益|2x收益|3x收益|3x最大回撤|近期3x收益|1x月正折|1x近期正折|结论|
|---|---:|---:|---:|---:|---:|---:|---:|---|
|slowbuffer370_ETH_G200_S29_L3_H025_N3000|15.998092|14.409713|12.820122|4.224177|1.823951|10/12|3/8|rejected|
|slowbuffer370_ETH_G050_S29_L3_H025_N3000|14.284162|12.447788|10.609880|4.251980|1.939127|9/12|4/8|rejected|
|slowbuffer370_ETH_G050_S28_L3_H025_N3000|13.707343|11.970621|10.232545|4.246837|1.867566|9/12|3/8|rejected|
|slowbuffer370_ETH_G050_S27_L4_H025_N3000|13.589453|11.905987|10.222160|5.597016|1.752414|9/12|2/8|rejected|
|slowbuffer370_ETH_G100_S29_L3_H025_N3000|13.313931|11.628513|9.941441|4.289550|1.872603|10/12|3/8|rejected|
|slowbuffer370_ETH_G200_S29_L4_H025_N3000|12.852375|11.394237|9.935373|4.675096|1.757066|9/12|2/8|rejected|
|slowbuffer370_ETH_G050_S28_L4_H025_N3000|13.109751|11.501530|9.892522|4.625820|1.757763|10/12|2/8|rejected|
|slowbuffer370_ETH_G100_S29_L4_H025_N3000|12.720411|11.262487|9.803686|4.675096|1.759210|9/12|2/8|rejected|
|slowbuffer370_ETH_G050_S29_L4_H025_N3000|13.147637|11.387072|9.625896|4.641557|1.459439|10/12|3/8|rejected|
|slowbuffer370_ETH_G050_S27_L3_H025_N3000|13.267413|11.416094|9.563985|5.009684|1.879176|7/12|3/8|rejected|
|slowbuffer370_ETH_G200_S28_L3_H025_N3000|11.986087|10.451740|8.916329|4.929006|1.890561|8/12|3/8|rejected|
|slowbuffer370_ETH_G100_S27_L3_H025_N3000|11.771838|10.031825|8.290925|5.386647|1.901687|7/12|3/8|rejected|
|slowbuffer370_parent_B1000_E3000_G200_S29_L3_H025|9.496117|8.453616|7.410508|2.758332|1.146336|10/12|5/8|rejected|
|slowbuffer370_ETH_G100_S27_L4_H025_N3000|10.034434|8.475326|6.915760|5.774140|1.807587|9/12|2/8|rejected|
|slowbuffer370_ETH_G200_S27_L3_H025_N3000|10.216131|8.537709|6.858379|4.946582|-0.009962|7/12|3/8|rejected|
|slowbuffer370_ETH_G100_S28_L3_H025_N3000|9.719985|8.083501|6.445811|5.312690|1.935289|7/12|3/8|rejected|
|slowbuffer370_parent_B1000_E3000_G050_S29_L3_H025|8.639152|7.472653|6.305387|2.767680|1.198424|9/12|5/8|rejected|
|slowbuffer370_ETH_G100_S28_L4_H025_N3000|9.132184|7.674920|6.217019|5.505304|1.819695|8/12|2/8|rejected|
|slowbuffer370_parent_B1000_E3000_G050_S28_L3_H025|8.350743|7.234070|6.116720|2.765955|1.160475|10/12|5/8|rejected|
|slowbuffer370_parent_B1000_E3000_G050_S27_L4_H025|8.291798|7.201753|6.111527|2.990760|1.101429|10/12|5/8|rejected|
|slowbuffer370_parent_B1000_E3000_G100_S29_L3_H025|8.154036|7.063016|5.971168|2.780219|1.162087|9/12|5/8|rejected|
|slowbuffer370_parent_B1000_E3000_G200_S29_L4_H025|7.923258|6.945878|5.968134|2.967752|1.102936|10/12|5/8|rejected|
|slowbuffer370_parent_B1000_E3000_G050_S28_L4_H025|8.051946|6.999524|5.946708|2.951722|1.103161|11/12|5/8|rejected|
|slowbuffer370_parent_B1000_E3000_G100_S29_L4_H025|7.857277|6.880003|5.902290|2.967752|1.103629|10/12|5/8|rejected|
|slowbuffer370_parent_B1000_E3000_G050_S29_L4_H025|8.070890|6.942296|5.813395|2.956859|0.949572|10/12|5/8|rejected|
|slowbuffer370_parent_B1000_E3000_G050_S27_L3_H025|8.130778|6.956806|5.782440|2.910709|1.164184|9/12|5/8|rejected|
|slowbuffer370_ETH_G200_S27_L4_H025_N3000|8.482804|6.985285|5.487282|5.630945|-0.126194|9/12|2/8|rejected|
|slowbuffer370_parent_B1000_E3000_G200_S28_L3_H025|7.490115|6.474630|5.458612|3.022079|1.167801|9/12|5/8|rejected|
|slowbuffer370_parent_B1000_E3000_G100_S27_L3_H025|7.382990|6.264672|5.145910|3.333011|1.171315|8/12|5/8|rejected|
|slowbuffer370_ETH_G200_S28_L4_H025_N3000|7.692736|6.290374|4.887374|5.861476|1.843188|7/12|2/8|rejected|
|slowbuffer370_parent_B1000_E3000_G100_S27_L4_H025|6.514288|5.486422|4.458327|3.038894|1.119056|9/12|5/8|rejected|
|slowbuffer370_parent_B1000_E3000_G200_S27_L3_H025|6.605137|5.517614|4.429637|3.099792|0.193370|8/12|5/8|rejected|
|slowbuffer370_parent_B1000_E3000_G100_S28_L3_H025|6.357063|5.290510|4.223353|3.281197|1.181805|9/12|5/8|rejected|
|slowbuffer370_parent_B1000_E3000_G100_S28_L4_H025|6.063163|5.086219|4.108957|3.058468|1.122853|10/12|5/8|rejected|
|slowbuffer370_parent_B1000_E3000_G200_S27_L4_H025|5.738473|4.741402|3.744088|3.031802|0.135348|9/12|5/8|rejected|
|slowbuffer370_parent_B1000_E3000_G200_S28_L4_H025|5.343439|4.393946|3.444134|3.051284|1.130151|9/12|5/8|rejected|

全网格Sharpe正值比例、收益正值比例及最高观测单元边界诊断（只读已有结果，不改变资格）：{"native": {"dimension_count": 3, "cells": 24, "new_cells": 18, "old_readonly_cells": 6, "full3x_positive_Sharpe_fraction": 1.0, "recent40_3x_positive_Sharpe_fraction": 0.9583333333333334, "full3x_positive_net_fraction": 1.0, "recent40_3x_positive_net_fraction": 0.9166666666666666, "highest_observed_full3x_net_cell": "slowbuffer370_ETH_G200_S29_L3_H025_N3000", "highest_observed_cell_original_or_new_status": "rejected", "highest_observed_is_on_axis_boundary": {"slow_return_hurdle_fraction": true, "trend_lookback_days": true, "lookback_days": true}, "descriptive_full_Sharpe_cliff_edges": 11, "old_qualifications_preserved": true, "recent6of8_by_fast_lookback": {"3": 0, "4": 0}, "new_recent6of8_by_slow_center": {"27": 0, "28": 0, "29": 0}, "not_untouched_test_or_global_optimum": true}, "parent": {"dimension_count": 3, "cells": 24, "new_cells": 18, "old_readonly_cells": 6, "full3x_positive_Sharpe_fraction": 1.0, "recent40_3x_positive_Sharpe_fraction": 1.0, "full3x_positive_net_fraction": 1.0, "recent40_3x_positive_net_fraction": 1.0, "highest_observed_full3x_net_cell": "slowbuffer370_parent_B1000_E3000_G200_S29_L3_H025", "highest_observed_cell_original_or_new_status": "rejected", "highest_observed_is_on_axis_boundary": {"reversal_slow_return_hurdle_fraction": true, "trend_filter_lookback_days": true, "reversal_lookback_days": true}, "descriptive_full_Sharpe_cliff_edges": 9, "old_qualifications_preserved": true, "recent6of8_by_fast_lookback": {"3": 1, "4": 1}, "new_recent6of8_by_slow_center": {"27": 0, "28": 0, "29": 0}, "not_untouched_test_or_global_optimum": true}}。最高观测单元的预设网格边界标记已保存，不称全局最优；全期平台不能消除近期正折不足。

实际失败门槛计数：{"nine_of_twelve_positive_complete30d_1x_folds": 9, "recent40_six_of_eight_positive5d_1x_folds": 36, "recent40_positive_all_costs": 2}。逐项真实结论见上表和report.json，不因全期收益正而放宽门槛。150成本行、1950全期折、1200近期折、40068新日边界、92敏感性边、216匹配对照完整留档；6图36面板已实际打开。
独立只读核验9旧原生/27成本曲线、1332条已保存成交与29970条已保存资金费记录，原完整NAV SHA保持；旧原生模型未重跑，父层未新增成交；18个新原生按实际订单/资金费/成本/风险计算并经独立整数信号与Decimal逐点审计，9个旧原生仅回放保存账本核对SHA。36新配置108成本场景共58861404完整NAV点、1512全期/逐折和972近期/逐折指标通过；16旧唯一结果SHA/资格保持，12899受保护文件不变。42新实际ID各自finish，84事件仅追加；36实际金融配置加6实际partial，全部完整spec在reserve前核对原生参数、父层两组件完整参数及周期别名，无本轮失配定义。
只读监控实际检查exit0：8101研究项，171既有paper观察/10账户；8065旧展示行完整字典不变。原候选累计3101点/场景、3029分钟，0新增日决策/成交，实际新增资金费记录0条；现金与资金费逐条独立核验，收入不随成本放大，00旧结算未重复；旧SMA累计39058点，0新日决策/成交。两者均非十策略实时报价执行或长期盈利证据。
真实命令/传输异常记录2项，见read_failures.json。本轮登记、账户续接及提交由持续stdin排他锁保护。所有真实负收益分折/近期、成功/失败和完整账户账本保留；行情与HTTPpacket留ignoreddata并绑定SHA，不提交大行情或凭据。main普通非强推，freshfetch/独立allheads/完整tree/blob/行情核验通过后释放自己锁。
