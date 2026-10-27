# 20261027T091448Z 较长ETH反转周期验证

实际测试4个ETH原生策略＋4个组合，共8配置/24成本场景，历史通过1、淘汰7。全文读取20060事件/9926ID及202份结论；初始16项均有实际历史证据。

本轮事前固定ETH慢28/31日×反转3/4/5日，阈值2%、零交叉退出、原生银行10000、固定入场3000；BTC固定ROC31/H4%/退出1%、银行10000、入场1000。快3日旧2原生＋2组合只读，快4/5日4原生＋4组合逐项先reserve才计算。原值1/1为两整个10000银行、组合本金20000；入场合计4000=初始本金20%，不归一化、不复利调仓、不转账/交叉保证金/再平衡。

ETH此前完整L日ROC严格>2%反转空/<-2%反转多，带内多仅ROC<0、空仅ROC>0保留，零退出；慢ROC S正仅许多、负仅许空，零/不兼容即平仓，现金重入须新极端，无隐藏desired。UTC00:01真实OPEN执行，q=floor(N/此前完整close/lot)，先平后反开，不用未来OPEN/资金费/未闭合价格产生信号或手数。研究引擎仅放宽允许L到4/5，原信号/订单/费用/资金费/风险/指标函数其余字节保持；原冻结未来观察器代码未改。

父组合仅将固定BTC已有真实净值与新ETH净值按共同(ns,eventcode)时序承接上一完成点后逐点相加，不平均收益/Sharpe；原生N3000重新实际撮合，未缩放旧净值。4个旧原生/12成本NAV源SHA校对，旧ETH3日与同N恒多逐档比较，现金0为解析对照。原资格不因新邻域重评级。

真实8合并Parquet及16年度/近期源SHA固定；370日连续OOS2025-10-19UTC00:01..2026-10-24UTC00:01，33日上下文/3日初始embargo。静态规则无拟合/未来标签，purge不适用。12完整30日折＋10日尾折carry原现金/仓位/entry/费用，近期40日继承day330状态并分8×5日，不重置或诊断平仓；只有预定Oct24终点费用平仓。该历史反复研究，仅作开发验证，不称最终未触碰留出或独立新市场证据。

每侧5bp费＋1bp半价差＋2bp滑点＋0.5×此前20日日log波动×sqrt(成交金额/此前20日ADV)冲击，参与率≤0.1%，真实不利tick/lot/最小金额、完全抵押入场限制；实际资金费=-q×结算mark×rate，流出乘1/2/3，流入不放大。永续无虚构现货借币。无L2/TCA/完整历史阶梯与tick清算，1%小时不利mark维持保证金仅代理。

资格未放宽：全期/近期三档净正，1倍月正折≥9/12且近期≥6/8，3倍整体DD≤25%，二维相邻索引含自身净正率≥60%，≥4往返、(参考毛利＋资金费)/费用≥2.5，现金/拒单/风险代理违规0、终点空仓。两作用域分别6格、7边；全部净收益、整体回撤、Sharpe/Calmar、陡变/边界及逐折留档，2图12面板。

计算前复核发现4个旧组合草案的周期说明/源规则哈希不一致，原样保留并finish abandoned/result_available=false；4原生定义有效未改。修正完整组合定义、再次reserve及预检后才计算，金融结果未重跑。具体注册与恢复回执均保留。

结果：{"new_financial_configs": 8, "new_native_components": 4, "new_passive_parents": 4, "passed_candidates": 1, "rejected_candidates": 7, "positive_configs_by_cost": {"1": 8, "2": 8, "3": 8}, "failed_criteria_counts": {"recent40_six_of_eight_positive5d_1x_folds": 7, "nine_of_twelve_positive_complete30d_1x_folds": 2}, "by_scope": {"native": {"new": 4, "passed": 0, "best_full3": {"name": "longfast370_ETH_N3000_S31_L5_H02", "return3_pct": 11.253505585157452, "whole_DD3_pct": 4.215959168303196, "recent_return3_pct": 0.5045548848636061, "positive_months1": 10, "positive_recent1": 2, "failed_criteria": ["recent40_six_of_eight_positive5d_1x_folds"]}}, "parent": {"new": 4, "passed": 1, "best_full3": {"name": "longfast370_parent_B1000_E3000_S31_L5_H02", "return3_pct": 6.627200032979319, "whole_DD3_pct": 2.692683667730411, "recent_return3_pct": 0.4580013129647398, "positive_months1": 10, "positive_recent1": 4, "failed_criteria": ["recent40_six_of_eight_positive5d_1x_folds"]}}}, "rows": {"cost": 42, "full_folds": 546, "recent40_folds": 336, "daily_NAV": 8904, "edges": 14, "reference_comparisons": 48}}

原H4/ETH3日冻结候选只续接至Oct27UTC08:30，跨实际08:00资金费，保持真实现金/数量/entry/风险段和完整净值链；旧SMA同样续接无强制平仓。两者是延迟闭合行情/资金费重建，不是paper10实时报价账户；paper10冻结账本只读。部分观察rejected不取消180日计划，短窗年化/盈利不解释为长期资格。

一手背景复用此前2026-10-27实际访问的[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)（2012-05-01）与[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)（2012-12-05）。传统期货/股票背景到加密4/5日规则为推论，非论文复现或利润/容量移植。新8相关配置承受多重选择，未证明DSR/PBO或稳定实盘盈利。

复现工作目录/home/desktop/Documents/Codex/EquiTide；audit.py/audit_native.py、check_sources.py、check_definitions.py、audit_candidate.py、forward.py --reproduce/audit_forward.py只读保存的真实结果，不重新reserve/evaluate/summarize已完成配置。main普通非强推、freshfetch/独立allheads/完整tree/blob核验后释放自己锁；不建分支/任务、重部署或真实下单。

历史通过项目只读冻结检查：1项。完整spec/来源/报告/账本SHA见candidate_validation.json；不改原冻结L3未来账户。
longfast370_parent_B1000_E3000_S28_L4_H02：1/2/3倍370日收益[7.305519282620221, 6.068303941511988, 4.83061893635377]%，整体3倍回撤2.970454968054581%，近期3倍收益1.2163539293134296%；完整月正折10/12、近期6/8，邻域全期3倍净正6/6、原始近期6/8仅2/6。仅通过预设历史门槛，尚无该新配置独立未来证据。

根登记、监控与逐行归属检查均实际exit0：7472研究配置、150既有paper观察/10账户；7464旧展示行完整字典不变。18新ID全部finish：8真实研究＋6真实部分观察＋4无实际计算abandoned草案；36事件仅追加，7987受保护文件、7旧唯一结果/原资格SHA保持。
新12原生成本场景独立核验882成交、13320资金费、4440因果决策及28062小时风险段；连同12组合成本场景，13080312净值点、336全期/逐折和216近期指标核验通过。2图12面板实际打开，42成本行/546全期折/336近期折/8904新日边界/14边/48对照完整。
冻结候选累计523点/场景，跨08:00.001实际资金费：BTC三成本各收入0.0832415904USDT，ETH空仓结算零；收入未随压力放大，现金独立核验，q/entry/执行成本保持，无新增成交。完整风险段与NAV链保留，下一窗口不得重复计费。旧SMA至08:30、36536点、0新日决策/成交；均是延迟重建，不是paper10实时报价执行或长期盈利证据。
本轮真实非零退出3项见read_failures.json；旧接口source_engine缺键在任何原生计算前失败，适配已冻结native_engine_base路径后才实际计算，没有重跑完整结果。4个原始组合定义问题、abandoned及修正规则/reserve回执另存；所有成功/失败证据及完整账户/冻结规则/登记保留。行情与原始packet留ignoreddata并保存哈希，仅清自己的缓存。main普通非强推，freshfetch/allheads/tree/blob/data核验后释放自己锁；不部署或真实下单。
