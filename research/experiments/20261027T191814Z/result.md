# 20261027T191814Z BTC确认阈值与ETH过滤/反转周期组合验证

实际计算20个新组合/60成本场景，历史通过2、淘汰18。完整读取20332事件/10062ID、207份结论，初始16项均有真实历史证据。

事前预设BTC ROC31入场2/4/6%、退出1% × ETH慢28/29/30/31日 × 反转3/4/5日，ETH入场2%、零交叉退出。三维36格：16旧结果只读、20缺失组件对各自先reserve再计算，75相邻边。15旧原生/45成本NAV完整恢复并核对原SHA，不重新执行原生信号/撮合/费用/资金费模型；名称、顺序、数字格式或策略族不制造新颖性。固定原生预算BTC1000/ETH3000，不线性缩放其他金额结果。

原值1/1代表两个完整10000USDT独立银行，父本金20000，入场预算合计4000=初始本金20%；不是目标权重或恒定风险比例，不归一化、不复利调仓、不转账/跨银行保证金/再平衡。每档按共同(ns,eventcode)时轴承接上一完成源净值并逐点相加，重新计算整体收益/Sharpe/Calmar/回撤，不平均单策略指标。逐项与同ETH/金额的旧BTC_H4组合及同金额恒多、解析现金0对照。

BTC此前完整31日ROC严格>H多/<-H空，带内多仅ROC>-1%、空仅ROC<1%保持；反向完整极端先平再反开。ETH此前完整L日ROC严格>2%反转空/<-2%反转多，带内多仅ROC<0、空仅ROC>0保留，零退出；慢S日ROC正仅许多、负仅许空，零/不兼容平实际仓位，现金重入须新极端，无隐藏desired。00:01真实OPEN执行，q=floor(N/此前完整close/lot)，不使用未来OPEN/未闭合价格/资金费产生信号或手数。全部组件规则与实际账本保持，本轮无新父层成交。

8真实合并Parquet＋16年度/近期源SHA/字节固定。370日连续OOS2025-10-19UTC00:01至2026-10-24UTC00:01，33日上下文/3日初始embargo，静态规则无拟合/未来标签，purge不适用。12完整30日折＋10日尾折连续carry原现金/数量/entry/费用，近期40日从day330继承状态并分8×5日，不重开本金或诊断平仓，只有原预定终点计费平仓。该历史反复研究，只属开发验证，不称最终未触碰测试集。

原生每侧5bp手续费＋1bp半价差＋2bp滑点＋0.5×此前20日日log波动×sqrt(金额/此前20日ADV)冲击，参与率≤0.1%；真实不利tick/lot/最小金额、100%抵押入场约束。实际资金费=-q×结算mark×rate，流出乘1/2/3、收入不放大，永续无虚构现货借币。原每档成本/资金费/交易数/占本金比例直接继承并核对相加，不新增重平衡成本。缺L2/TCA/历史完整阶梯，1%维持保证金＋闭合小时不利mark仅代理，不保证容量或tick清算安全。

预设门槛保持：全期/近期三档净正，1倍完整月正折≥9/12、近期≥6/8，3倍完整连续OOS最大DD≤25%，三维排序相邻索引半径1含自身邻域净正≥60%，≥4往返、(参考毛利＋资金费)/执行费用≥2.5，现金/拒单/各银行风险代理违规0、终点空仓且≥180日。16旧资格不按新邻域重评级。三图18面板、111成本行、1443全期折、888近期折、22260新日边界、75相邻边和120匹配对照保存。

结果：{"new_financial_configs": 20, "new_native_components": 0, "new_passive_parents": 20, "passed_candidates": 2, "rejected_candidates": 18, "positive_configs_by_cost": {"1": 20, "2": 20, "3": 20}, "failed_criteria_counts": {"recent40_six_of_eight_positive5d_1x_folds": 18, "nine_of_twelve_positive_complete30d_1x_folds": 2}, "best_full3": {"name": "confirmmix370_BH06_S29_L5_B1000_E3000", "return3_pct": 7.812246774974052, "whole_DD3_pct": 2.88241405326104, "recent_return3_pct": 0.46982809807853965, "positive_months1": 10, "positive_recent1": 4, "failed_criteria": ["recent40_six_of_eight_positive5d_1x_folds"]}, "rows": {"cost": 111, "full_folds": 1443, "recent40_folds": 888, "daily_NAV": 22260, "edges": 75, "reference_comparisons": 120}}

原冻结H4/ETH28L3候选与旧SMA按完整账本续接16:30至18:30，不重复08和16资金费；保留16小时内资金费前后风险状态以核验17:00完整小时。两者是延迟闭合行情重建，不是paper10实时报价执行。paper10账户/冻结规则只读，不为新历史组合改原前向计划，不强制窗口截止平仓。

一手背景复用此前2026-10-27实际访问的[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)（2012-05-01）与[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)（2012-12-05）。本加密规则与组合推论非论文复现或利润/容量移植。20个相关新组合及所有既往试验存在多重选择偏差，无DSR/PBO、独立未来资格或稳定实盘盈利证明。

复现工作目录/home/desktop/Documents/Codex/EquiTide；audit.py独立回放已保存实际事件、核验共同纳秒时轴和每个组合净值/指标；check_sources.py、audit_candidate.py、audit_forward.py及forward.py --reproduce只读真实证据，不重复reserve/evaluate/summarize完成项。main普通非强推、完整远端tree/blob/行情SHA验证后释放自己锁。

历史通过项目只读冻结检查：2项。完整spec/来源/报告/账本SHA见candidate_validation.json；不改原冻结L3未来账户。
confirmmix370_BH02_S28_L4_B1000_E3000：1/2/3倍370日收益[6.3936720393745095, 5.07776116789882, 3.7613663908731443]%，整体3倍回撤2.9752976779795492%，近期3倍收益1.2290424123000632%；完整月正折9/12、近期6/8，邻域全期3倍净正12/12、原始近期6/8仅4/12。仅通过预设历史门槛，尚无该新配置独立未来证据。
confirmmix370_BH06_S28_L4_B1000_E3000：1/2/3倍370日收益[7.445664356800652, 6.272991627143676, 5.099848231436677]%，整体3倍回撤3.0124900447063174%，近期3倍收益1.2250107269579313%；完整月正折9/12、近期6/8，邻域全期3倍净正12/12、原始近期6/8仅4/12。仅通过预设历史门槛，尚无该新配置独立未来证据。

逐配置结果（收益/回撤单位%，三倍全期回撤使用完整连续OOS）：

|配置|1x收益|2x收益|3x收益|3x最大回撤|近期3x收益|1x月正折|1x近期正折|结论|
|---|---:|---:|---:|---:|---:|---:|---:|---|
|confirmmix370_BH06_S29_L5_B1000_E3000|10.051582|8.931827|7.812247|2.882414|0.469828|10/12|4/8|rejected|
|confirmmix370_BH06_S31_L5_B1000_E3000|9.265155|8.080813|6.896429|2.744472|0.468282|10/12|4/8|rejected|
|confirmmix370_BH06_S30_L3_B1000_E3000|9.158378|7.862686|6.565975|2.804518|1.181782|9/12|5/8|rejected|
|confirmmix370_BH02_S29_L5_B1000_E3000|8.999589|7.736596|6.473765|2.837183|0.464276|10/12|4/8|rejected|
|confirmmix370_BH06_S28_L5_B1000_E3000|8.723690|7.588087|6.452448|2.900405|0.495094|10/12|5/8|rejected|
|confirmmix370_BH06_S29_L3_B1000_E3000|9.101053|7.723339|6.344782|3.159788|1.250043|9/12|5/8|rejected|
|confirmmix370_BH06_S29_L4_B1000_E3000|8.318616|7.057192|5.795528|2.992359|1.197223|10/12|5/8|rejected|
|confirmmix370_BH02_S31_L5_B1000_E3000|8.213163|6.885582|5.557947|2.766956|0.462662|10/12|4/8|rejected|
|confirmmix370_BH06_S30_L5_B1000_E3000|7.710212|6.576551|5.442935|3.335177|0.351665|9/12|4/8|rejected|
|confirmmix370_BH02_S30_L3_B1000_E3000|8.106386|6.667455|5.227493|2.766725|1.185204|9/12|5/8|rejected|
|confirmmix370_BH02_S28_L5_B1000_E3000|7.671697|6.392857|5.113966|3.193163|0.489790|10/12|5/8|rejected|
|confirmmix370_BH06_S28_L4_B1000_E3000|7.445664|6.272992|5.099848|3.012490|1.225011|9/12|6/8|passed|
|confirmmix370_BH02_S29_L3_B1000_E3000|8.049060|6.528109|5.006300|3.677356|1.254349|9/12|5/8|rejected|
|confirmmix370_BH06_S30_L4_B1000_E3000|7.156718|6.058159|4.959221|3.009505|0.504227|9/12|4/8|rejected|
|confirmmix370_BH02_S29_L4_B1000_E3000|7.266624|5.861962|4.457046|2.955310|1.200869|9/12|5/8|rejected|
|confirmmix370_BH02_S30_L5_B1000_E3000|6.658220|5.381321|4.104453|3.852036|0.344483|9/12|4/8|rejected|
|confirmmix370_BH02_S28_L4_B1000_E3000|6.393672|5.077761|3.761366|2.975298|1.229042|9/12|6/8|passed|
|confirmmix370_BH02_S30_L4_B1000_E3000|6.104726|4.862929|3.620739|3.160618|0.498962|9/12|4/8|rejected|
|confirmmix370_BH06_S31_L4_B1000_E3000|5.704123|4.558071|3.411618|3.030778|0.838314|7/12|4/8|rejected|
|confirmmix370_BH02_S31_L4_B1000_E3000|4.652131|3.362841|2.073136|3.091050|0.837330|7/12|4/8|rejected|

全网格Sharpe正值比例、收益正值比例及最高观测单元边界诊断（只读已有结果，不改变资格）：{"parent": {"dimension_count": 3, "cells": 36, "full3x_positive_Sharpe_fraction": 1.0, "recent40_3x_positive_Sharpe_fraction": 1.0, "full3x_positive_net_fraction": 1.0, "recent40_3x_positive_net_fraction": 1.0, "highest_observed_full3x_net_cell": "confirmmix370_BH06_S29_L5_B1000_E3000", "highest_observed_is_on_axis_boundary": {"BTC_return_hurdle": true, "trend_filter_lookback_days": false, "reversal_lookback_days": true}, "descriptive_full_Sharpe_cliff_edges": 12, "old_qualifications_preserved": true, "not_untouched_test_or_global_optimum": true}}。最高观测单元的预设网格边界标记已保存，不称全局最优；全期平台不能消除近期正折不足。

实际失败门槛计数：{"recent40_six_of_eight_positive5d_1x_folds": 18, "nine_of_twelve_positive_complete30d_1x_folds": 2}。逐项真实结论见上表和report.json，不因全期收益正而放宽门槛。111成本行、1443全期折、888近期折、22260新日边界、75敏感性边、120匹配对照完整留档；3图18面板已实际打开。
独立只读核验15旧原生/45成本曲线、3114条已保存成交与49950条已保存资金费记录，原完整NAV SHA保持；没有原生模型重跑或父层新增成交。20新组合60成本场景共32700780完整NAV点、840全期/逐折和540近期/逐折指标通过；32旧唯一结果SHA/资格保持，8916受保护文件不变。26新实际ID各自finish，52事件仅追加。
只读监控实际检查exit0：7536研究项，155既有paper观察/10账户；7516旧展示行完整字典不变。原候选累计1135点/场景、1109分钟，0新增日决策/成交，实际新增资金费记录0条；现金与资金费逐条独立核验，收入不随成本放大，08旧结算未重复；旧SMA累计37136点，0新日决策/成交。两者均非十策略实时报价执行或长期盈利证据。
真实命令/传输异常记录0项，见read_failures.json。本轮登记、账户续接及提交由持续stdin排他锁保护。所有真实负收益分折/近期、成功/失败和完整账户账本保留；行情与HTTPpacket留ignoreddata并绑定SHA，不提交大行情或凭据。main普通非强推，freshfetch/独立allheads/完整tree/blob/行情核验通过后释放自己锁。
