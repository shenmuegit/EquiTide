# 20261029T152659Z 固定规模BTC/ETH银行所有权联合敏感性

实际36个新组合＋4个同权重恒多对照，共40定义/120成本场景；新候选历史通过0、淘汰36。复用12个原生银行/36条真实成本曲线，未重跑原生模型。

经济假设：上轮原值[1,1]的6个合格组合近期1倍6/8，但2/3倍仅5/8，正折边际很小。本轮在看结果前固定w0.5/0.75/1.25/1.5、ETH=2−w，联合E−1.5/−1/−0.5%及S27/28/29，L3/H2.5%固定。9个旧w1/E/S对照保留原资格，只读实际数字，不把旧资格按新门槛重写。L3与本轮方向来自反复开发历史，不称独立测试。

原值权重是现有各10000银行的静态所有权单位，故父本金始终20000，不自动归一化。BTC_owned_capital=10000w，ETH_owned_capital=10000(2−w)，初始拥有的入场预算1000w+3000(2−w)，分别占25/22.5/17.5/15%。底层固定N1000/N3000数量与非线性冲击成本保持原规模；金额/成本/资金费按所有权归属，底层动作次数不加权且不是新父层订单。没有再平衡、转账、合并净额或交叉保证金。该指数所有权结果不是新规模直接成交或合并容量证明。

BTC原ROC31/H4/退出1%；ETH快L3、严格H2.5%，E负阈值在快ROC到零前退出而非入场PnL止损。慢ROC(S−1,S,S+1)严格多数仅约束新入场/反向，已有快方向一致数量保留。每份spec含两个完整底层参数字典、实际来源指纹、时间、资本、成本和所有权含义。

8个真实合并Parquet及16个年度/近期源SHA固定。370日2025-10-19UTC00:01至2026-10-24UTC00:01；33日上下文含30预热与3初始embargo。静态规则不拟合、无未来标签、purge不适用。12个连续30日折＋10日尾折，近期40从day330继承状态分8×5日；不重开本金、不插入诊断交易，仅原始终点计费平仓。完整事件并集逐点重算整体最大回撤，非平均组件回撤/收益/Sharpe。

原成本每侧5bp手续费＋1bp半价差＋2bp滑点＋0.5×滞后20日样本日log波动×sqrt(实际原生订单金额/滞后20日quoteADV)，参与率≤0.1%，原lot/tick/最小金额/全额抵押约束。实际永续资金费−signedq×结算mark×rate，流出按1/2/3放大、收入不放大；无虚构现货借币。1%维持保证金/闭合小时不利mark为风险代理，缺真实L2/TCA/历史tier/tick清算/聚合容量证据。

事前门槛保留全期及近期三档净正、1倍月正≥9/12、1倍近期≥6/8、三倍整体DD≤25%、全期净正邻域≥60%、≥4往返、(毛利＋资金费)/成本≥2.5、现金/拒单/风险违规0、终点空仓及≥180日。新配置在看结果前额外要求近期每一档成本均≥6/8正折，以及同作用域w/E/S索引半径1含自身的该条件邻域比例≥60%；旧9资格不变，4恒多仅参考不申请alpha资格。

真实结果：{"actual_configs": 40, "actual_candidates": 36, "actual_reference_only": 4, "new_native_models": 0, "cost_scenes": 120, "passed": 0, "rejected_candidates": 36, "failed_criteria_counts": {"recent40_six_of_eight_positive5d_1x_folds": 24, "recent40_six_of_eight_positive5d_all_costs": 30, "local_recent6of8_allcost_gte60pct": 36}, "positive_candidate_configs_by_cost": {"1": 36, "2": 36, "3": 36}, "candidate_eachcost_recent6of8_count": 6, "complete_sensitivity_cells": 45, "old_read_only_cells": 9, "edges": 96, "full3_positive_Sharpe_fraction": 1.0, "full3_positive_net_fraction": 1.0, "recent3_positive_net_fraction": 1.0, "descriptive_Sharpe_cliff_edges": 7, "descriptive_cliff_threshold_2sd": 0.25112923100663026, "highest_observed_cell": "bankweight370_W050_E-100_S28_L3_H025", "highest_observed_boundary": {"BTC_bank_units": true, "ETH_exit_buffer_fraction": false, "ETH_trend_lookback_days": false}, "best_new": {"name": "bankweight370_W050_E-100_S28_L3_H025", "net_return3_pct": 10.902816733683341, "whole_DD3_pct": 3.1907499632710667, "recent_return3_pct": 2.0225254534662174, "recent_positive_folds_by_cost": {"1": 6, "2": 6, "3": 6}, "status": "rejected", "failed_criteria": ["local_recent6of8_allcost_gte60pct"]}, "by_BTC_units": {"0.5": {"candidates": 9, "passed": 0, "eachcost_recent6of8": 6}, "0.75": {"candidates": 9, "passed": 0, "eachcost_recent6of8": 0}, "1.25": {"candidates": 9, "passed": 0, "eachcost_recent6of8": 0}, "1.5": {"candidates": 9, "passed": 0, "eachcost_recent6of8": 0}}, "report_sha256": "e7faaea78bae9fd272561fcc0621ec8ac712e3531fa0bf3e1250876010552e85", "strict_gates_predeclared": true, "old_statuses_unchanged": true, "independent_future_qualification": false}

|配置|用途|1x收益%|2x收益%|3x收益%|3x整体DD%|近期3x收益%|近期正折1/2/3x|结论|
|---|---|---:|---:|---:|---:|---:|---|---|
|bankweight370_W050_E-100_S28_L3_H025|candidate|13.921354|12.412592|10.902817|3.190750|2.022525|6/6/6|rejected|
|bankweight370_W050_E-50_S27_L3_H025|candidate|13.586386|12.171413|10.755741|3.507385|1.960724|5/5/5|rejected|
|bankweight370_W050_E-150_S28_L3_H025|candidate|13.379394|11.870382|10.360225|3.190750|2.032671|6/6/6|rejected|
|bankweight370_W050_E-50_S28_L3_H025|candidate|13.254439|11.769190|10.282908|3.492343|2.034125|6/6/6|rejected|
|bankweight370_W050_E-100_S27_L3_H025|candidate|12.727355|11.328152|9.928376|3.637251|1.975773|5/5/5|rejected|
|bankweight370_W050_E-100_S29_L3_H025|candidate|12.437961|10.974282|9.509662|3.787402|2.048783|6/6/6|rejected|
|bankweight370_W075_E-100_S28_L3_H025|candidate|12.100152|10.760079|9.419163|2.927510|1.768167|6/6/5|rejected|
|bankweight370_W050_E-150_S27_L3_H025|candidate|12.185394|10.785943|9.385784|3.637251|1.985768|5/5/5|rejected|
|bankweight370_W075_E-50_S27_L3_H025|candidate|11.821012|10.559097|9.296600|3.136970|1.715949|5/5/5|rejected|
|bankweight370_W075_E-150_S28_L3_H025|candidate|11.648518|10.308238|8.967003|2.927510|1.775634|6/6/5|rejected|
|bankweight370_W050_E-50_S29_L3_H025|candidate|11.793732|10.353586|8.912476|4.572212|2.060248|6/6/6|rejected|
|bankweight370_W075_E-50_S28_L3_H025|candidate|11.544390|10.223912|8.902572|3.125662|1.776703|6/6/5|rejected|
|bankweight370_W075_E-100_S27_L3_H025|candidate|11.105153|9.856380|8.607129|3.301825|1.727030|5/5/5|rejected|
|bankweight370_W050_E-150_S29_L3_H025|candidate|11.193614|9.730820|8.266950|3.787402|2.072786|6/6/6|rejected|
|bankweight370_W075_E-100_S29_L3_H025|candidate|10.863992|9.561488|8.258200|3.108009|1.787468|6/6/5|rejected|
|bankweight370_W075_E-150_S27_L3_H025|candidate|10.653519|9.404539|8.154969|3.301825|1.734376|5/5/5|rejected|
|bankweight370_W075_E-50_S29_L3_H025|candidate|10.327134|9.044241|7.760546|3.770322|1.795871|6/6/5|rejected|
|bankweight370_W075_E-150_S29_L3_H025|candidate|9.827036|8.525270|7.222608|3.108009|1.805043|6/6/5|rejected|
|bankweight370_W125_E-100_S28_L3_H025|candidate|8.457748|7.455055|6.451856|2.391448|1.242233|5/5/5|rejected|
|bankweight370_W125_E-50_S27_L3_H025|candidate|8.290264|7.334466|6.378318|2.408889|1.210007|5/5/5|rejected|
|bankweight370_W125_E-150_S28_L3_H025|candidate|8.186768|7.183950|6.180560|2.391448|1.245446|5/5/5|rejected|
|bankweight370_W125_E-50_S28_L3_H025|candidate|8.124291|7.133355|6.141901|2.372789|1.245906|5/5/5|rejected|
|bankweight370_W125_E-100_S27_L3_H025|candidate|7.860749|6.912835|5.964635|2.618762|1.214788|5/5/5|rejected|
|bankweight370_W125_E-100_S29_L3_H025|candidate|7.716052|6.735900|5.755278|2.572462|1.250517|5/5/5|rejected|
|bankweight370_W125_E-150_S27_L3_H025|candidate|7.589768|6.641731|5.693339|2.618762|1.217944|5/5/5|rejected|
|bankweight370_W125_E-50_S29_L3_H025|candidate|7.393937|6.425552|5.456685|2.373886|1.254103|5/5/5|rejected|
|bankweight370_W125_E-150_S29_L3_H025|candidate|7.093878|6.114169|5.133922|2.572462|1.258001|5/5/5|rejected|
|bankweight370_W150_E-100_S28_L3_H025|candidate|6.636546|5.802543|4.968202|2.449967|0.970265|5/5/5|rejected|
|bankweight370_W150_E-50_S27_L3_H025|candidate|6.524890|5.722150|4.919177|2.499816|0.948470|5/5/5|rejected|
|bankweight370_W150_E-150_S28_L3_H025|candidate|6.455893|5.621807|4.787338|2.449967|0.971956|5/5/5|rejected|
|bankweight370_W150_E-50_S28_L3_H025|candidate|6.414241|5.588076|4.761566|2.350840|0.972197|5/5/5|rejected|
|bankweight370_W150_E-100_S27_L3_H025|candidate|6.238547|5.441063|4.643388|2.602120|0.950993|5/5/5|rejected|
|bankweight370_W150_E-100_S29_L3_H025|candidate|6.142082|5.323106|4.503817|2.528090|0.974618|5/5/5|rejected|
|bankweight370_W150_E-150_S27_L3_H025|candidate|6.057893|5.260327|4.462524|2.602120|0.952655|5/5/5|rejected|
|bankweight370_W150_E-50_S29_L3_H025|candidate|5.927339|5.116208|4.304755|2.383242|0.976496|5/5/5|rejected|
|bankweight370_W150_E-150_S29_L3_H025|candidate|5.727300|4.908619|4.089580|2.528090|0.978535|5/5/5|rejected|
|bankweight370_W150_hold|benchmark|-4.996751|-5.439680|-5.882618|9.696689|-0.067810|4/4/4|rejected|
|bankweight370_W125_hold|benchmark|-6.193300|-6.696940|-7.200588|11.717005|-0.243523|4/4/4|rejected|
|bankweight370_W075_hold|benchmark|-8.586399|-9.211461|-9.836529|15.744773|-0.608377|4/4/4|rejected|
|bankweight370_W050_hold|benchmark|-9.782948|-10.468721|-11.154500|17.750896|-0.797863|4/3/3|rejected|

完整147成本行、1911全期逐折、1176近期逐折、44520新日净值、96敏感性边与216匹配对照留档；原w1与同权重恒多均同本金20000，现金参考0。全期平台及最高格边界、Sharpe突变边只描述已执行网格，不称全局最优或独立证据。预设新门槛不得因结果而放宽。

背景为一手[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)与[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)，本轮实际访问记录literature_access.json。静态所有权研究是假设推论，非论文复现或收益迁移证明。相关多重试验存在选择偏差，无DSR/PBO或新组合独立前向资格，不称稳定实盘盈利。

原单S28候选及旧SMA65按原规则从12:30延续到14:30，不采用本轮权重、退出阈值或新账户；只追加真实闭合mark并核对12/13小时风险承接，08资金费保持只计一次。下一资金费16UTC、下一日决策Oct30UTC00:01。原账户延迟shadow与十策略真实公开报价模拟分开。后续实际账户续接和monitor检查以最终保存审计为准。

复现命令见reproduce.md，目录/home/desktop/Documents/Codex/EquiTide。精确已完成配置不得再次reserve/evaluate；原生已保存订单/资金费回放＋因果加权/指标重算只读核验。保存所有成功/淘汰及负收益折、完整账户和冻结规则；仅main非强推，不下真实订单。

最终实际核验：40金融定义/120成本场景全部finish，36候选淘汰、4恒多参考；46实际ID/92事件仅追加。独立回放12原生/36曲线、1920成交与39960资金费账本，65401560完整NAV点、1680全期/逐折及1080近期/逐折指标通过；22旧来源资格/哈希与14546保护文件保持。
只有BTC原值0.5/ETH1.5、S28或29的6格达到每档近期6/8；邻列w0.75均5/8，全36不满足事前严格邻域60%门槛，未放宽或事后扩网格。最佳3倍370日净收益10.9028167337%、整体DD3.1907499633%，仅边界观测而非合格/最优/稳定实盘收益。
原候选累计96观察ID、3835点/场景、3749分钟；本窗122新NAV动作、0决策/成交/资金费，12/13闭合小时6个BTC成本风险检查且0违规，当前14小时状态承接。旧SMA累计39778点、39749分钟、0新日决策/成交；原SMA65与候选单S28规则、资金、数量、费用前缀保留。下一16:30候选窗口须计实际16时资金费一次并保留精确纳秒前后现金/风险状态。
登记门禁与最终只读监控实际exit0：8357研究行、177既有观察/10账户；8317旧展示行完整字典相同。3图18面板已实际打开，数据与导出逐项核验。
实际异常均留档：rg缺失；独审旧模块导入接口失败；旧对照计数硬编码少1；finish进程exit143原因未知，保留31完成只续9未完成；SMA2行TLS重试与候选1次TLS失败后成功；finalizer源码初次嵌套字符串生成失败。均已在真实证据基础上恢复，金融计算未重跑。全部原始日志/退出/失败与恢复见read_failures.json、review_resolution.json。
仅移除可重建的审计导入修复前副本，SHA及重建关系留cleanup_intermediates.json；完整账本、规则、结果、登记及必要核验代码保留。实际发布状态和commit SHA以.git/automation_proofs/20261029T152659Z.json为准，本说明不预先声称push成功。

提交前Git格式门禁曾因CSV默认CRLF退出2，publisher实际退出1且未创建提交。仅将6个CSV的48072行改LF，逐行所有单元格完全相同；完整金融/账户报告、spec、结果账本、旧资格与净值哈希均未改。CSV生产器显式LF，导出、monitor及旧行一致性已实际重新检查exit0；原始失败全文、旧manifest及诊断SHA留publication_newline_recovery.json所引位置，不绕过格式门禁或重跑金融模型。

第一结果提交9fb39fb423ea20da2397cb5e567a5bbfd56b888b已真实push，远端树/文件核验后在只读来源status别名处KeyError停止。修复manifest生产器，为22个original_status增加相同status字段；不改实际资格、报告、数据或账本。后续元数据修复提交和最终完整核验/实际退出证明见.git/automation_proofs/20261029T152659Z.json及post_push_verification_recovery.json。
