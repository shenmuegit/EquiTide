# 20261028T092048Z BTC入场时机与ETH一日慢周期扰动的组合验证

实际计算12个新组合/36成本场景，历史通过0、淘汰12。完整读取20924事件/10358ID、214份结论，初始16项已有真实历史证据。

事前固定BTC ROC31/H2/4/6%/退出1% × ETH反转阈值2/2.5% × 慢27/28/29日 × 反转3/4日，完整四维36格：24旧格只读、12缺失组件对先分别成功reserve再计算、84相邻边。15个旧原生/45成本NAV从已存现金/数量/entry分段恢复核对原SHA，不重跑旧信号/成交/费用/资金费模型。BTC1000/ETH3000均复用实际金额专属路径，不缩放其他金额结果。检验不同BTC时机能否改善上一轮S27/29近期资格脆弱性，不据新结果放宽门槛。

原值1/1为两个完整10000USDT独立银行，父本金20000；入场预算4000=初始本金20%，不是目标权重或恒定风险比例。不归一化、不复利调仓、不转账/交叉保证金/再平衡/现金利息。共同(ns,eventcode)时轴上仅承接上一完成源NAV，逐点相加后重算整体收益、Sharpe、Calmar和回撤，不平均指标。逐项与同ETH阈值/周期/资金的旧BTC_H4组合、同资金恒多及解析现金0对照。

BTC此前完整31日ROC严格>H多/<-H空，带内多仅ROC>-1%、空仅ROC<1%保留，反向完整极端先平后开。ETH此前完整L日ROC严格>H反转空/<-H反转多，带内多仅ROC<0、空仅ROC>0保留，零退出；慢S日ROC正仅许多、负仅许空，零或不兼容平实际仓位，现金重入须新严格极端。00:01真实OPEN执行，q=floor(N/此前完整close/lot)*lot，不用未来OPEN/NAV/资金费或未闭合数据生成信号和手数；本轮父层无新增成交。

8真实合并Parquet与16年度/近期源SHA/字节固定。370日连续OOS为2025-10-19UTC00:01至2026-10-24UTC00:01；33日上下文、3日初始embargo，静态规则无拟合/未来标签，purge不适用。12完整30日折＋10日尾折连续承接原现金/数量/entry/费用，近期40日从day330继承状态并分8×5日，不重开本金或诊断平仓，只有原终点计费平仓。该历史反复研究，只是开发验证，不是未触碰最终测试或独立未来市场。

每侧5bp手续费＋1bp半价差＋2bp滑点＋0.5×此前20日日log波动×sqrt(成交金额/此前20日ADV)冲击，参与率≤0.1%，实际不利tick/lot/最小金额及100%抵押入场上限。真实资金费=-q×结算mark×rate，流出乘1/2/3、收入不放大；永续空头无虚构现货借币。报告逐档执行数、成本占比、分项成本与资金费。缺L2/TCA/历史完整保证金阶梯，1%维持保证金＋闭合小时不利mark仅风险代理，不保证tick清算安全或实盘容量。

门槛保持：全期/近期三档净正、1倍月正折≥9/12且近期≥6/8、3倍完整OOS最大DD≤25%、四维排序索引半径1含自身邻域3倍净正≥60%、至少4往返、(参考毛利＋资金费)/执行费用≥2.5、现金/拒单/独立银行风险违规0、终点空仓且≥180日。24旧格不重评级；6图36面板、111成本行、1443全期折、888近期折、13356新日边界、84敏感性边和72匹配对照完整留档。

结果：{"new_financial_configs": 12, "new_native_components": 0, "new_passive_parents": 12, "passed_candidates": 0, "rejected_candidates": 12, "positive_configs_by_cost": {"1": 12, "2": 12, "3": 12}, "failed_criteria_counts": {"recent40_six_of_eight_positive5d_1x_folds": 12, "nine_of_twelve_positive_complete30d_1x_folds": 7}, "best_full3": {"name": "nearcyclepair370_BH06_EH025_S29_L4_B1000_E3000", "return3_pct": 6.8101533003215975, "whole_DD3_pct": 2.9763215383092345, "recent_return3_pct": 1.1857150452372567, "positive_months1": 11, "positive_recent1": 5, "failed_criteria": ["recent40_six_of_eight_positive5d_1x_folds"]}, "rows": {"cost": 111, "full_folds": 1443, "recent40_folds": 888, "daily_NAV": 13356, "edges": 84, "reference_comparisons": 72}}

原冻结候选与旧SMA从Oct28UTC06:30续接至08:30，逐档承接现金、数量、entry、成本、既有资金费、日决策、上下文及净值链；不重开本金/持仓、不重复已处理事件、不强制截止平仓。本轮跨越08:00，按实际结算mark/rate独立核对-q×mark×rate，流出按成本压力放大、收入不放大，并保留资金费前后现金及当前小时风险栈。下一日决策Oct29UTC00:01，下一资金费16:00。延迟闭合数据重建，独立于paper10实时报价账户；partial的rejected不取消长期计划。

背景沿用此前2026-10-27实际访问的[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)及[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)。本加密联合阈值组合为研究推论，不是论文复现或利润/容量移植。12个相关新组合及所有既往试验有多重选择偏差，无DSR/PBO、独立长期未来资格或稳定实盘盈利证明。

复现工作目录/home/desktop/Documents/Codex/EquiTide；audit.py独立恢复原生已存现金/数量账本，核验共同纳秒时轴和完整组合净值；check_sources.py、audit_candidate.py、audit_forward.py及forward.py --reproduce只读已存证据，不重新reserve/evaluate/summarize已完成配置。main普通非强推，完整远端tree/blob/行情SHA验证后释放自己锁；不建分支、定时任务、重部署或真实订单。

本轮工程预检曾有两次真实失败，均发生在任何reserve/回测前：先前漏计4个已测组合，后因宽泛文本替换使校验器误把ETH3000断言写成2000。冻结spec/本金/金额/规则始终未改。失败代码与stderr、完整SHA绑定及恢复命令见engineering_recovery.json；修正校验器并通过完整定义预检后，12项全部成功reserve才执行本轮唯一一次组合评估。未重算那4个已测组合，未把工程失败当作策略收益。

本轮原冻结候选实际08:00资金费：BTC维持-0.012000000000000000，每档收到0.07673887374160546800000000000 USDT，收入未随成本档放大；ETH空仓资金费0。6条结算、完整新增净值与风险状态独立核验通过；BTC当前08小时结算前/后两份现金风险状态均保留至下轮09:00闭合小时检查，未重计以前结算。两次curl35握手失败均由独立有界验证TLS重试恢复，原失败stderr/响应哈希保存，未关闭证书校验。详见candidate_funding_continuity.json。

历史通过项目只读冻结检查：0项。完整spec/来源/报告/账本SHA见candidate_validation.json；不改原冻结L3未来账户。

同BTC阈值、同ETH阈值及反转L的完整慢周期匹配诊断（只读已登记指标）：12个S28中心中12格达到近期6/8；24个S27/S29邻格中0格达到。中心正折分布{"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 12, "7": 0, "8": 0}，邻格分布{"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 24, "6": 0, "7": 0, "8": 0}。全36格三倍成本全期收益均正，但近期6/8资格未形成相邻慢周期平台，不能将全期收益平台称为稳健实盘方法。详见paired_cycle_diagnostics.json；旧状态保持。

逐配置结果（收益/回撤单位%，三倍全期回撤使用完整连续OOS）：

|配置|1x收益|2x收益|3x收益|3x最大回撤|近期3x收益|1x月正折|1x近期正折|结论|
|---|---:|---:|---:|---:|---:|---:|---:|---|
|nearcyclepair370_BH06_EH025_S29_L4_B1000_E3000|9.071436|7.940877|6.810153|2.976322|1.185715|11/12|5/8|rejected|
|nearcyclepair370_BH06_EH025_S29_L3_B1000_E3000|8.684612|7.497058|6.308878|2.818280|1.250471|9/12|5/8|rejected|
|nearcyclepair370_BH02_EH025_S29_L4_B1000_E3000|8.019444|6.745646|5.471671|2.939388|1.189180|10/12|5/8|rejected|
|nearcyclepair370_BH02_EH025_S29_L3_B1000_E3000|7.632620|6.301828|4.970396|3.083455|1.254783|9/12|5/8|rejected|
|nearcyclepair370_BH06_EH025_S27_L4_B1000_E3000|6.667968|5.593657|4.519177|3.401572|0.028117|8/12|5/8|rejected|
|nearcyclepair370_BH06_EH020_S27_L3_B1000_E3000|7.154760|5.787714|4.419968|3.709116|0.305338|8/12|5/8|rejected|
|nearcyclepair370_BH06_EH025_S27_L3_B1000_E3000|6.689653|5.532104|4.374233|3.390584|0.305472|8/12|5/8|rejected|
|nearcyclepair370_BH06_EH020_S27_L4_B1000_E3000|6.088253|4.907302|3.726001|3.415980|0.028332|7/12|5/8|rejected|
|nearcyclepair370_BH02_EH025_S27_L4_B1000_E3000|5.615976|4.398426|3.180696|3.318281|0.016734|8/12|5/8|rejected|
|nearcyclepair370_BH02_EH020_S27_L3_B1000_E3000|6.102768|4.592483|3.081487|4.227134|0.297490|9/12|5/8|rejected|
|nearcyclepair370_BH02_EH025_S27_L3_B1000_E3000|5.637661|4.336874|3.035751|3.581338|0.297622|8/12|5/8|rejected|
|nearcyclepair370_BH02_EH020_S27_L4_B1000_E3000|5.036261|3.712071|2.387519|3.332410|0.016864|8/12|5/8|rejected|

全网格Sharpe正值比例、收益正值比例及最高观测单元边界诊断（只读已有结果，不改变资格）：{"parent": {"dimension_count": 4, "cells": 36, "full3x_positive_Sharpe_fraction": 1.0, "recent40_3x_positive_Sharpe_fraction": 1.0, "full3x_positive_net_fraction": 1.0, "recent40_3x_positive_net_fraction": 1.0, "highest_observed_full3x_net_cell": "nearcyclepair370_BH06_EH025_S29_L4_B1000_E3000", "highest_observed_is_on_axis_boundary": {"BTC_return_hurdle": true, "reversal_return_hurdle": true, "trend_filter_lookback_days": true, "reversal_lookback_days": true}, "descriptive_full_Sharpe_cliff_edges": 32, "old_qualifications_preserved": true, "not_untouched_test_or_global_optimum": true}}。最高观测单元的预设网格边界标记已保存，不称全局最优；全期平台不能消除近期正折不足。

实际失败门槛计数：{"recent40_six_of_eight_positive5d_1x_folds": 12, "nine_of_twelve_positive_complete30d_1x_folds": 7}。逐项真实结论见上表和report.json，不因全期收益正而放宽门槛。111成本行、1443全期折、888近期折、13356新日边界、84敏感性边、72匹配对照完整留档；6图36面板已实际打开。
独立只读核验15旧原生/45成本曲线、3060条已保存成交与49950条已保存资金费记录，原完整NAV SHA保持；没有原生模型重跑或父层新增成交。12新组合36成本场景共19620468完整NAV点、504全期/逐折和324近期/逐折指标通过；40旧唯一结果SHA/资格保持，10440受保护文件不变。18新实际ID各自finish，36事件仅追加。
只读监控实际检查exit0：7712研究项，162既有paper观察/10账户；7700旧展示行完整字典不变。原候选累计1996点/场景、1949分钟，0新增日决策/成交，实际新增资金费记录6条；现金与资金费逐条独立核验，收入不随成本放大，过去已计入结算未重复，本轮08新结算按实际记录核验；旧SMA累计37977点，0新增日决策/成交；最新65日上下文仍为012050已核验文件。两者均非十策略实时报价执行或长期盈利证据。
真实命令/传输异常记录4项，见read_failures.json。本轮登记、账户续接及提交由持续stdin排他锁保护。所有真实负收益分折/近期、成功/失败和完整账户账本保留；行情与HTTPpacket留ignoreddata并绑定SHA，不提交大行情或凭据。main普通非强推，freshfetch/独立allheads/完整tree/blob/行情核验通过后释放自己锁。

提交前另有一次真实中止：git diff --cached --check 对原始 reserve.log 的终末空行返回2，未产生commit/push。日志来自先前真实失败的stdout/stderr，保持原字节，不通过删日志或修改财务结果消除错误。改用排除原始*.log的代码/spec/报告空白检查后续接普通提交；全部日志仍逐文件SHA/完整远端tree核验。上文4项为首次封存时记录，本次计入第5项；详细原命令/输出和恢复边界见publication_preflight_recovery.json。
