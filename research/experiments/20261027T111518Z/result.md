# 20261027T111518Z ETH较短趋势过滤与反转速度验证

实际计算6个ETH原生策略＋6个组合，共12配置/36成本场景，历史通过0、淘汰12。完整读取20116事件/9954ID、203份结论，初始16项已有真实历史证据，无缺结果项可补。

预设ETH慢22/25/28/31日×反转3/4/5日，阈值2%、零交叉退出、原生银行10000、固定入场3000。慢22/25日6原生＋6组合逐项先reserve再计算；慢28/31日12旧单元只读，保留旧资格。BTC固定此前完整31日ROC严格>4%多/<-4%空，带内多仅ROC>-1%、空仅ROC<1%保留；完整反向极端先平后开，银行10000/入场1000。

ETH此前完整L日ROC严格>2%反转空/<-2%反转多，带内多仅ROC<0、空仅ROC>0保留，零退出；慢S日ROC正仅许多、负仅许空，零/不兼容平实际仓位，现金重入须新极端，无隐藏desired。UTC00:01真实OPEN执行，数量floor(N/此前完整close/lot)，不用未来OPEN/未闭合价格/资金费决定信号或手数。引擎仅允许22/25慢周期，信号/成交/资金费/风险/指标函数其余字节不变。

原值1/1指两个完整10000USDT独立银行，父本金20000，入场合计4000=初始本金20%；不归一化、不复利调仓、不转账/交叉保证金/再平衡。8个旧原生/24成本NAV只读恢复并核对原SHA，不重跑旧信号/撮合。组合按共同(ns,eventcode)时钟承接上一完成点后逐点相加并重算整体指标，不平均收益率/Sharpe，不缩放旧N净值。每新项与相同L/金额的旧慢28日、同金额恒多及解析现金0逐档比较。

真实8合并Parquet及16年度/近期源文件SHA/字节固定。370日连续OOS2025-10-19UTC00:01至2026-10-24UTC00:01，33日先验上下文、3日初始embargo，覆盖最大慢31日。静态规则无拟合/未来标签，purge不适用；12完整30日折＋10日尾折连续carry现金/数量/entry/成本，近期40日从day330继承状态并分8×5日，不重开本金或诊断平仓，仅预定终点计费平仓。反复使用的开发历史不称最终未触碰留出或独立市场证据。

每侧5bp费＋1bp半价差＋2bp滑点＋0.5×此前20日日log波动×sqrt(成交金额/此前20日ADV)冲击，参与率≤0.1%；真实不利tick/lot/最小金额、100%抵押入场上限。资金费=-q×实际结算mark×rate，流出乘1/2/3，收入不放大；永续空头无虚构现货借币。价差/滑点/冲击为估计，缺L2/TCA/历史完整margin阶梯，1%维持保证金＋闭合小时不利mark仅风险代理，不保证tick清算安全或实盘容量。

预设门槛不变：全期/近期三档净正，1倍完整月正折≥9/12且近期≥6/8，3倍完整连续NAV最大DD≤25%，二维排序相邻索引半径1含自身邻域净正率≥60%，≥4往返、(参考毛利＋资金费)/执行成本≥2.5，现金/拒单/风险代理违规0、终点空仓及≥180日。两个作用域各12格、17边；完整收益/回撤/Sharpe/Calmar/陡变/边界、逐折/逐变体留档，2图12面板。旧单元资格不按新邻域重评级。

结果：{"new_financial_configs": 12, "new_native_components": 6, "new_passive_parents": 6, "passed_candidates": 0, "rejected_candidates": 12, "positive_configs_by_cost": {"1": 12, "2": 12, "3": 12}, "failed_criteria_counts": {"nine_of_twelve_positive_complete30d_1x_folds": 6, "recent40_six_of_eight_positive5d_1x_folds": 12, "recent40_positive_all_costs": 7}, "by_scope": {"native": {"new": 6, "passed": 0, "best_full3": {"name": "shortgate370_ETH_N3000_S22_L5_H02", "return3_pct": 10.066909668283586, "whole_DD3_pct": 5.703511339890643, "recent_return3_pct": -0.2593756397313518, "positive_months1": 10, "positive_recent1": 2, "failed_criteria": ["recent40_positive_all_costs", "recent40_six_of_eight_positive5d_1x_folds"]}}, "parent": {"new": 6, "passed": 0, "best_full3": {"name": "shortgate370_parent_B1000_E3000_S22_L5_H02", "return3_pct": 6.033902074542374, "whole_DD3_pct": 3.680563075393828, "recent_return3_pct": 0.060162641196925826, "positive_months1": 9, "positive_recent1": 5, "failed_criteria": ["recent40_six_of_eight_positive5d_1x_folds"]}}}, "rows": {"cost": 78, "full_folds": 1014, "recent40_folds": 624, "daily_NAV": 13356, "edges": 34, "reference_comparisons": 72}}

原H4/ETH慢28日反转3日冻结候选与旧SMA只续接至Oct27UTC10:30，承接08:30完整现金/数量/entry/成本/资金费/风险段和NAV链，不重复08:00.001已记资金费，不改长期规则或强制平仓。两者为延迟闭合行情重建，不能当paper10真实报价账户或成熟前向资格。paper10账本只读，部分观察rejected不取消原长期计划。

一手背景复用此前2026-10-27已实际访问的[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)（2012-05-01）和[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)（2012-12-05）。加密22/25日过滤与3/4/5日反转为本研究推论，非论文复现或传统市场利润/容量移植。12新相关试验有多重选择偏差，未证明DSR/PBO或稳定实盘盈利。

复现工作目录/home/desktop/Documents/Codex/EquiTide；audit.py调用独立audit_native.verify核验整数信号、Decimal费用/资金费/状态/NAV；check_sources.py、audit_candidate.py、audit_forward.py、forward.py --reproduce只读已有真实证据，不重复reserve/evaluate/summarize已完成配置。普通main非强推及完整远端tree/blob/行情SHA证明后释放自己锁，不建分支、任务、重部署或真实下单。

历史通过项目只读冻结检查：0项。完整spec/来源/报告/账本SHA见candidate_validation.json；不改原冻结L3未来账户。

逐配置结果（收益/回撤单位%，三倍全期回撤使用完整连续OOS）：

|配置|1x收益|2x收益|3x收益|3x最大回撤|近期3x收益|1x月正折|1x近期正折|结论|
|---|---:|---:|---:|---:|---:|---:|---:|---|
|shortgate370_ETH_N3000_S22_L5_H02|13.799113|11.933008|10.066910|5.703511|-0.259376|10/12|2/8|rejected|
|shortgate370_ETH_N3000_S25_L5_H02|10.727866|8.820624|6.913899|6.236247|-1.349650|9/12|1/8|rejected|
|shortgate370_parent_B1000_E3000_S22_L5_H02|8.396628|7.215264|6.033902|3.680563|0.060163|9/12|5/8|rejected|
|shortgate370_ETH_N3000_S22_L4_H02|10.037040|7.997451|5.956796|5.622891|-0.218977|7/12|2/8|rejected|
|shortgate370_parent_B1000_E3000_S25_L5_H02|6.861004|5.659071|4.457397|4.054756|-0.499594|9/12|4/8|rejected|
|shortgate370_ETH_N3000_S25_L3_H02|9.037289|6.520301|4.001678|8.974026|-0.228491|7/12|3/8|rejected|
|shortgate370_parent_B1000_E3000_S22_L4_H02|6.515591|5.247485|3.978845|3.703160|0.087213|8/12|5/8|rejected|
|shortgate370_ETH_N3000_S22_L3_H02|7.402107|5.348851|3.294051|8.043485|0.764293|7/12|3/8|rejected|
|shortgate370_ETH_N3000_S25_L4_H02|7.302615|5.199320|3.095722|8.237013|-1.348270|8/12|1/8|rejected|
|shortgate370_parent_B1000_E3000_S25_L3_H02|6.015716|4.508910|3.001286|5.391809|0.085295|9/12|5/8|rejected|
|shortgate370_parent_B1000_E3000_S22_L3_H02|5.198125|3.923185|2.647473|4.856538|0.586591|9/12|5/8|rejected|
|shortgate370_parent_B1000_E3000_S25_L4_H02|5.148379|3.848419|2.548308|4.059427|-0.482924|8/12|4/8|rejected|

12/12近期正折不足6/8；7/12近期未能三档全正；6/12完整月正折不足9/12。全部12全期三档净正并不足以通过历史门槛。每项具体失败理由、逐折及成本/资金费/成交分项保存在report.json和78成本行、1014全期折、624近期折、13356新日边界、34敏感性边、72匹配对照中；2图12面板已实际打开。
独立核验1410新成交、19980资金费记录、6660因果决策、45741状态小时风险检查；36新成本场景共19620468完整NAV点、504全期/逐折与324近期/逐折指标。8旧原生/24成本路径与15旧唯一结果SHA/资格保持，未重跑旧模型。8180受保护文件不变。18新实际ID各自finish，36事件仅追加。
只读监控实际检查exit0：7484研究项，151既有paper观察/10账户；7472旧展示行完整字典不变。原候选累计645点/场景、629分钟，0新增日决策/成交/资金费，08:00.001旧收入未重复；旧SMA累计36656点，同为0新日决策/成交。两者均非十策略实时报价执行或长期盈利证据。
真实非零命令退出2项，均见read_failures.json；初次heredoc锁探测即时释放，未在其下写登记或账户，实际工作由持续stdin排他锁保护。所有真实负收益近期/分折、成功/失败及完整账户账本保留。行情与HTTPpacket留ignoreddata并绑定SHA，不提交大行情或凭据；main普通非强推，freshfetch/独立allheads/完整tree/blob/数据核验通过后释放自己锁。
