# 20261029T172700Z BTC/ETH静态银行所有权的细化邻域

实际36个新候选＋4个同权重恒多参考，40配置/120成本场景；历史门槛通过6、候选淘汰30。完整读取22798登记事件/11295ID及230份结论，初始16均已有实际证据。

事前假设：上轮w0.5/ETH1.5的6个格点在1/2/3成本近期均6/8，但w0.75邻列退5/8，未形成预设≥60%邻域平台。本轮在新PnL之前固定BTC原值w0.25/0.375/0.625/0.875、ETH=2−w，联合E−1.5/−1/−0.5% × S27/28/29；L3/H2.5%固定。27个旧w0.5/0.75/1格点只读，组成等间距1/8单位w七点 × E三点 × S三点的63格、138相邻边。旧27资格不随新邻域重写；完整源spec、报告、账本SHA绑定。方向/L3来自反复使用的开发历史，不是独立测试。

原值[w,2−w]是两个原10000USDT固定规模银行的静态所有权单位，不自动归一化。父本金20000，拥有的BTC/ETH资本10000w/10000(2−w)，入场预算1000w+3000(2−w)，分别占父本金27.5/26.25/23.75/21.25%。不重新缩放原生N1000/N3000订单，原始订单数量/成交冲击/资金费/风险规则保持；金额按所有权归属，底层动作次数不加权且不是新父层成交。没有再平衡、转账、NAV目标或交叉保证金。这里验证既有银行净值指数所有权，不证明按新规模直接执行或合并容量。底层银行全期净正已知，因此正权重后的全期净正不是新独立alpha，关键是逐折与局部稳定性。

BTC保持ROC31/H4/退出1%；ETH快ROC3日严格H2.5%，E为快ROC到零前的退出阈值而非入场PnL止损。慢ROC(S−1,S,S+1)严格多数只约束新开/反向开仓，已有快方向一致持仓保留；现金无隐藏desired、重新入场仍需新的严格极端。每份spec保留两完整原生参数字典、源指纹、时间/成本/资本及原值单位含义。复用12原生/36成本曲线，独立回放已实际运行回测的成交及真实历史资金费账本，不重跑原生模型。

8个真实合并Parquet及16年度/近期源SHA固定。OOS为2025-10-19UTC00:01至2026-10-24UTC00:01共370日；33日上下文含30预热与3初始embargo。静态规则不拟合、无未来标签，purge不适用。12个完整30日折＋10日尾折连续承接账户；近期40日从day330继承状态分8×5日，不重开本金、诊断平仓或再平衡。完整(ns,eventcode)事件并集逐点计算组合及整体回撤，不能平均组件收益/Sharpe/回撤。重复开发历史不称未触碰最终测试集。

原生每侧成本5bp手续费＋1bp半价差＋2bp滑点＋0.5×滞后20日样本日log波动×sqrt(实际订单金额/滞后20日quoteADV)，参与率≤0.1%，保留lot/tick/最小金额/全额抵押。实际资金费−signedq×结算mark×rate；流出按1/2/3倍放大，收入不放大。永续不虚构现货借币。闭合小时不利mark和1%维持保证金只是风险代理，缺L2/TCA/历史tier/tick清算与合并容量证据。

门槛与上轮预设严格版本相同：全期/近期各成本净正，1倍完整月正≥9/12，近期各成本均≥6/8正折，三倍整体DD≤25%，全期净正局部比例≥60%，每档近期6/8这一条件的局部比例≥60%，≥4往返、(参考毛利＋资金费)/成本≥2.5、现金/拒单/风险违规0、终点空仓且≥180日。邻域为w/E/S索引半径1含自身；4个恒多只参考。未放宽资格或事后扩网格。

真实汇总：{"actual_configs": 40, "actual_candidates": 36, "actual_reference_only": 4, "new_native_models": 0, "cost_scenes": 120, "passed": 6, "rejected_candidates": 30, "failed_criteria_counts": {"recent40_six_of_eight_positive5d_all_costs": 24, "local_recent6of8_allcost_gte60pct": 30, "recent40_six_of_eight_positive5d_1x_folds": 9}, "positive_candidate_configs_by_cost": {"1": 36, "2": 36, "3": 36}, "candidate_eachcost_recent6of8_count": 12, "complete_sensitivity_cells": 63, "old_read_only_cells": 27, "edges": 138, "full3_positive_Sharpe_fraction": 1.0, "full3_positive_net_fraction": 1.0, "recent3_positive_net_fraction": 1.0, "descriptive_Sharpe_cliff_edges": 12, "descriptive_cliff_threshold_2sd": 0.2735421119606322, "highest_observed_cell": "bankweight370_Wm0250_E-100_S28_L3_H025", "highest_observed_boundary": {"BTC_bank_units": true, "ETH_exit_buffer_fraction": false, "ETH_trend_lookback_days": false}, "best_new": {"name": "bankweight370_Wm0250_E-100_S28_L3_H025", "net_return3_pct": 12.386470442497055, "whole_DD3_pct": 3.4556953776800903, "recent_return3_pct": 2.2713927567936665, "recent_positive_folds_by_cost": {"1": 7, "2": 6, "3": 5}, "status": "rejected", "failed_criteria": ["recent40_six_of_eight_positive5d_all_costs", "local_recent6of8_allcost_gte60pct"]}, "by_BTC_units": {"0.25": {"candidates": 9, "passed": 0, "eachcost_recent6of8": 0}, "0.375": {"candidates": 9, "passed": 3, "eachcost_recent6of8": 6}, "0.625": {"candidates": 9, "passed": 3, "eachcost_recent6of8": 6}, "0.875": {"candidates": 9, "passed": 0, "eachcost_recent6of8": 0}}, "report_sha256": "13396e9f3732af530b1e3829d16f3b6709bda8f086840285e7b19d5251b2bcf9", "strict_gates_predeclared": true, "old_statuses_unchanged": true, "independent_future_qualification": false}

|配置|用途|1x收益%|2x收益%|3x收益%|3x整体DD%|近期3x收益%|近期正折1/2/3x|结论|
|---|---|---:|---:|---:|---:|---:|---|---|
|bankweight370_Wm0250_E-100_S28_L3_H025|candidate|15.742556|14.065104|12.386470|3.455695|2.271393|7/6/5|rejected|
|bankweight370_Wm0250_E-50_S27_L3_H025|candidate|15.351760|13.783729|12.214882|3.871951|2.200269|6/5/4|rejected|
|bankweight370_Wm0250_E-150_S28_L3_H025|candidate|15.110269|13.432526|11.753446|3.455695|2.284553|7/6/5|rejected|
|bankweight370_Wm0250_E-50_S28_L3_H025|candidate|14.964488|13.314469|11.663243|3.852744|2.286441|7/6/5|rejected|
|bankweight370_Wm0375_E-100_S28_L3_H025|candidate|14.831955|13.238848|11.644644|3.321197|2.147634|6/6/6|rejected|
|bankweight370_Wm0375_E-50_S27_L3_H025|candidate|14.469073|12.977571|11.485311|3.690390|2.081140|5/5/5|rejected|
|bankweight370_Wm0250_E-100_S27_L3_H025|candidate|14.349558|12.799924|11.249623|3.973527|2.219783|6/5/4|rejected|
|bankweight370_Wm0375_E-150_S28_L3_H025|candidate|14.244831|12.651454|11.056835|3.321197|2.159247|6/6/6|rejected|
|bankweight370_Wm0375_E-50_S28_L3_H025|candidate|14.109464|12.541830|10.973076|3.673318|2.160912|6/6/6|rejected|
|bankweight370_Wm0250_E-100_S29_L3_H025|candidate|14.011931|12.387076|10.761123|4.465813|2.305492|7/6/5|rejected|
|bankweight370_Wm0250_E-150_S27_L3_H025|candidate|13.717270|12.167346|10.616599|3.973527|2.232770|6/5/4|rejected|
|bankweight370_Wm0375_E-100_S27_L3_H025|candidate|13.538456|12.064038|10.589000|3.803469|2.098361|5/5/5|rejected|
|bankweight370_Wm0625_E-100_S28_L3_H025|candidate|13.010753|11.586335|10.160990|3.059523|1.896044|6/6/6|rejected|
|bankweight370_Wm0375_E-100_S29_L3_H025|candidate|13.224946|11.680679|10.135392|4.122591|2.177706|6/6/6|passed|
|bankweight370_Wm0250_E-50_S29_L3_H025|candidate|13.260331|11.662930|10.064407|5.360593|2.320425|7/6/5|rejected|
|bankweight370_Wm0625_E-50_S27_L3_H025|candidate|12.703699|11.365255|10.026170|3.322917|1.839001|5/5/5|rejected|
|bankweight370_Wm0375_E-150_S27_L3_H025|candidate|12.951332|11.476645|10.001192|3.803469|2.109810|5/5/5|rejected|
|bankweight370_Wm0625_E-150_S28_L3_H025|candidate|12.513956|11.089310|9.663614|3.059523|1.904807|6/6/6|rejected|
|bankweight370_Wm0625_E-50_S28_L3_H025|candidate|12.399414|10.996551|9.592740|3.309798|1.906062|6/6/6|rejected|
|bankweight370_Wm0375_E-50_S29_L3_H025|candidate|12.527032|11.008258|9.488442|4.968070|2.190855|6/6/6|passed|
|bankweight370_Wm0250_E-150_S29_L3_H025|candidate|12.560193|10.936370|9.311293|4.465813|2.336785|7/6/5|rejected|
|bankweight370_Wm0625_E-100_S27_L3_H025|candidate|11.916254|10.592266|9.267753|3.470039|1.852002|5/5/5|rejected|
|bankweight370_Wm0625_E-100_S29_L3_H025|candidate|11.650977|10.267885|8.883931|3.449221|1.918709|6/6/6|passed|
|bankweight370_Wm0375_E-150_S29_L3_H025|candidate|11.876904|10.333595|8.789122|4.122591|2.205249|6/6/6|passed|
|bankweight370_Wm0625_E-150_S27_L3_H025|candidate|11.419457|10.095241|8.770377|3.470039|1.860628|5/5/5|rejected|
|bankweight370_Wm0875_E-100_S28_L3_H025|candidate|11.189551|9.933823|8.677336|2.794703|1.638871|6/6/5|rejected|
|bankweight370_Wm0875_E-50_S27_L3_H025|candidate|10.938325|9.752940|8.567029|2.949526|1.591546|5/5/5|rejected|
|bankweight370_Wm0625_E-50_S29_L3_H025|candidate|11.060433|9.698913|8.336511|4.172978|1.928591|6/6/6|passed|
|bankweight370_Wm0875_E-150_S28_L3_H025|candidate|10.783081|9.527166|8.270392|2.794703|1.645133|6/6/5|rejected|
|bankweight370_Wm0875_E-50_S28_L3_H025|candidate|10.689365|9.451272|8.212404|2.939914|1.646029|6/6/5|rejected|
|bankweight370_Wm0875_E-100_S27_L3_H025|candidate|10.294052|9.120494|7.946506|3.132599|1.600841|5/5/5|rejected|
|bankweight370_Wm0625_E-150_S29_L3_H025|candidate|10.510325|9.128045|7.744779|3.449221|1.939388|6/6/6|passed|
|bankweight370_Wm0875_E-100_S29_L3_H025|candidate|10.077007|8.855091|7.632470|2.852910|1.655044|6/6/5|rejected|
|bankweight370_Wm0875_E-150_S27_L3_H025|candidate|9.887581|8.713837|7.539562|3.132599|1.606997|5/5/5|rejected|
|bankweight370_Wm0875_E-50_S29_L3_H025|candidate|9.593835|8.389569|7.184581|3.364201|1.662075|6/6/5|rejected|
|bankweight370_Wm0875_E-150_S29_L3_H025|candidate|9.143746|7.922495|6.700436|2.852910|1.669743|6/6/5|rejected|
|bankweight370_Wm0875_hold|benchmark|-7.988124|-8.582831|-9.177544|14.738181|-0.515432|4/4/4|rejected|
|bankweight370_Wm0625_hold|benchmark|-9.184673|-9.840091|-10.495515|16.749008|-0.702513|4/4/3|rejected|
|bankweight370_Wm0375_hold|benchmark|-10.381222|-11.097351|-11.813485|18.750445|-0.894451|4/3/3|rejected|
|bankweight370_Wm0250_hold|benchmark|-10.979497|-11.725982|-12.472471|19.747662|-0.992302|3/3/3|rejected|

所有201成本行、2613全期折、1608近期折、44520新日NAV、138敏感性边及216匹配对照完整保存；匹配旧w1/E/S与同权重恒多均父本金20000，现金0为数学参考。全网格Sharpe正值比例、收益比例、边界最高观测与突变边留summary；不称全局最优或独立资格。

研究背景为一手[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)及[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)，实际访问见literature_access.json。本轮假设为研究推论，非论文复现或收益迁移证明；相关多重试验选择偏差仍在，无DSR/PBO或新组合独立前向证明。正收益回测不代表稳定实盘盈利。

原单S28候选及旧SMA65按冻结规则从UTC14:30延续至16:30；16时实际资金费须按精确ns/mark/rate/旧signedq入账一次，收入不随成本放大，保留前后现金风险栈及14/15小时风险承接。原参数、资金与持仓不换成本轮新组合。最终实际续接与监控状态以本轮审计及发布证据为准；旧延迟shadow与paper10十策略报价执行分开。

固定目录/home/desktop/Documents/Codex/EquiTide；复现命令与全输入/代码版本见reproduce.md及data_manifest.json。已完成精确配置不得再次reserve/evaluate；保存所有正负结果和完整账户账本。仅main普通非强推，不下真实订单。

历史合格新候选6项，完整规则、参数、原值权重、源/账本SHA、逐成本正折与局部比例已保存candidate_validation.json；仅通过预设历史网格门槛，未建立独立未来资格或新规模执行证明，不改原单S28前向账户。

最终实际核验：40金融配置/120成本场景全部finish，其中6新候选通过预设历史门槛、30候选淘汰、4恒多参考；46个实际ID/92事件仅追加。独立回放12原生/36曲线、1920回测成交与39960资金费记录，65401560完整NAV点、1680全期/逐折及1080近期/逐折指标通过。40旧来源、27旧格资格及14839保护文件保持。
6项新历史资格均S29慢周期边界，w0.375/0.625；代表w0.375/ETH1.625、E−1%、S29的3倍370日净收益10.13539211139356%、整体DD4.122591049711688%，各成本近期6/8；3倍最小正五日折仅0.0202941782200039%。仅验证这个预设1/8单位邻域，S30外侧、不同网格尺度、真实新规模lot/冲击与独立前向尚未验证，不称稳定实盘盈利或广泛平台。全期最高w0.25/S28/E−1%为12.38647%但成本近期7/6/5折且不合格，未按最高收益放宽门槛。
原冻结候选累计99观察ID、3959点/场景、3869分钟，本窗124新NAV动作、0日决策/成交；6条16时资金费按实际纳秒、mark/rate/旧signedq与现金独审，收入未成本放大且00/08未重计。14/15闭合小时6个BTC成本风险检查、0违规，当前16小时精确前后现金栈承接。旧SMA累计39898点、39869分钟，0新日决策或成交，完整65日上下文和账户前缀不变。
只读monitor与登记门禁实际exit0：8397研究项，178既有观察/10账户，8357旧展示行完整字典不变。3图18面板已实际打开；所有失败/重试原文及原始响应SHA见read_failures.json与候选transport记录。仅清理本人可重建准备文件，保留全部正负结果、账户账本、冻结规则与复现代码。
下一原候选窗口16:30→18:30须核验闭合16/17小时；16时pre/post状态的正持续时间必须按精确纳秒判断，同刻零时长状态不得多计，正1ms不能丢弃。下一资金费Oct30UTC00:00、下一日决策00:01；不将本轮新w/S/E切入原单S28计划。实际push状态/commit/远端全证据及锁释放见.git/automation_proofs/20261029T172700Z.json，不预先声称发布成功。
