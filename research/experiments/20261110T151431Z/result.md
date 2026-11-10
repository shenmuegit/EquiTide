完成宽S/D批次16项/48个成本场景：5/8个父组合历史通过，3个D1组合及8个ETH组件淘汰。2个ETH定义在三档成本下全期均净负，完整结果永久保留。预设代表S16/D1三倍收益2.349993%、连续整体回撤1.483029%，未通过月度/近期一致性。事后高收益格S20/D5三倍收益16.128155%、整体DD4.110997%；它提高收益，也扩大回撤，非稳定实盘盈利证明。

固定资金费预算M4/VW8/R0.00875及价格L5/H2%/E0.75%/K0.75%/VC5%/V10，仅联合检验归一化有限EWM窗口S12/16/20和斜率滞后D1/3/5。beta=(S-1)/(S+1)，旧S16/D3原生及组合只读；其余8组件+8组合先reserve再算48场景。事前代表S16/D1。全部成本、时间、资本/名义金额/raw[1,1]及失败门槛保持，不预认改善。原四账户本窗均只mark/risk，不重复已各自入账的Nov10_08，无新日决策/成交/研究采用。

完整读取32156事件/15956ID和372份既往结论。初始16项证据齐全（11正式+5旧ZIP实际回测），无缺实际结果项；5个legacy标志与历史文件不改。此前规范研究定义10631，标实际10418、未标实际213，不能声称所有登记都完成验证。16项完整参数/数值组件图查重、保存spec、成功reserve后才算，全部finish；10个旧源结果和旧S16/D3中心只读。另12个原账户真实观察，共28ID/56事件。

规则只变有限EWM窗口S=[12,16,20]及斜率滞后D=[1,3,5]。每个S采用beta=(S−1)/(S+1)，最近S个已完成日收盘归一化有限均值与D日前同窗口均值相比。固定ROC5/H2%/E0.75%、斜率K0.75%、价格样本logvol V10/上限5%，严格边界、同向实际数量保留、反手先平旧仓及下一UTC00:01 OPEN执行均保持。351个Fraction/Horner合成检查覆盖长度、衰减、滞后、边界、持仓/反手、未来数据隔离与固定预算不变性，4项预期RED单列。仅decide的S/D可接受域改变，其余函数AST保持。

ETH最大信号上下文25日（20+5）、成本21日、预算需9个收盘；BTC需30日。33日源上下文足够，无未来初始化。没有模型拟合/标签/purge/embargo；开发历史已经反复使用，不能称未触碰最终测试集。

资金费固定为UTC00:00信号前可用、结算年龄1–36小时的最新4笔SIGNED实际费率，取中间两项均值；max(原方向×median,0)≤min(0.0002,0.00875×过去8日样本logvol×最新成熟真实结算间隔小时/24)。间隔取最新合格fundingTime与直接上一笔真实时间之差，双方信号时可得并保留毫秒抖动；归一化名义8小时不是实测间隔。缺记录/间隔只阻止新开/反手。每资产1212笔实际资金费及370次成熟来源选择核验。available_ts=结算后1小时是保守假设，非网络到达实测，过去费率不是未来费率。

组合使用旧BTC29/H3%/E1%银行3750、N1000完整路径及新ETH银行15000、N4500逐项实际数量/LOT、成本、冲击、资金费、抵押/保证金代理和全NAV。raw[1,1]相加完整独立银行，总本金18750；20%/80%是资本份额，不再次加权、不归一化、不缩放NAV、不转移资金、不再平衡、不下父订单、无交叉抵押。旧预算、无过滤同C/N、同期常持有和现金0%对照均保存；多参数不同的对照仅作描述，不能把全部差异归因于资金费过滤。

Walk-forward完成：2025-10-19 UTC00:01至2026-10-24 UTC00:01连续370日，12个30日完整折+10日尾；近期40日继承day330现金/仓位，分8个5日折，不折间重开。8份真实归一化输入的版本、SHA256、边界和必要原始数据留档。624逐折、384近期折、17808日净值行及完整连续净值整体DD保存；终点平仓含成本。重复开发和多重选择偏差保留，不称独立未来确认。

敏感性完成：原生/父组合各9格（8新+1旧中心），72邻接边，净收益、整体DD、Sharpe、Calmar及三档成本完整保存。D1父组合只有7/7/8个盈利月、近期各档5/8正折，局部严格近期不足；其余5个新组合符合原门槛。ETH近期0–2/8正折、局部严格近期比例0，全8项淘汰，部分另有全期亏损、月数、平仓数或成本安全边际不足。原生7/9格Sharpe正、组合9/9格正，仍有明显邻接跳变；收益峰值位于S20/D5边界，不是稳定平台。旧中心canonical资格与旧敏感性不改，本轮诊断分存。

成本1/2/3倍完成：每边手续费5bp+半价差1bp+滑点2bp，冲击=0.5×过去20日样本logvol×sqrt(实际abs(q)×原生OPEN/过去20日quoteADV)。执行成本和资金费支出随倍数放大，正资金费收入不放大。线性永续不借现货，逐笔真实time/rate/mark乘各自实际持仓，检查LOT/tick/minnotional、≤0.1%参与率、费后1倍抵押及1%闭合小时不利mark维护保证金代理。缺真实L2/TCA、完整历史风险档位/逐tick强平及真实容量证据。

门槛不改：各成本全期/近期净正，1x≥9/12正完整月折，近期各档≥6/8正5日折，3x整体DD≤25%，局部3x净正及严格近期比例≥60%，≥4次原生平仓，毛价格PnL加净资金费/1x成本≥2.5，无抵押/订单/风险代理违规，终点flat且≥180日。不因正收益放宽门槛。

|范围|S|D|1x净%|2x净%|3x净%|3x整体DD%|月正/12|近期正折1/2/3|状态|
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|native|12|1|-0.837546|-0.891195|-0.944845|1.346910|0|0/0/0|rejected|
|native|12|3|14.374214|13.649342|12.924812|4.080065|8|1/1/1|rejected|
|native|12|5|11.578392|10.256632|8.935734|6.730378|9|2/2/2|rejected|
|native|16|1|0.881934|0.779724|0.677513|1.958978|1|0/0/0|rejected|
|native|16|5|19.595595|18.208069|16.821121|4.349744|11|2/2/2|rejected|
|native|20|1|-0.232647|-0.340618|-0.448440|1.849382|1|0/0/0|rejected|
|native|20|3|13.887836|13.049758|12.212060|4.473084|10|2/2/2|rejected|
|native|20|5|21.018877|19.459258|17.900216|4.330403|11|2/2/2|rejected|
|parent|12|1|1.729864|1.390984|1.052107|1.446394|7|5/5/5|rejected|
|parent|12|3|13.899272|13.023413|12.147832|3.082168|9|6/6/6|passed|
|parent|12|5|11.662614|10.309246|8.956570|4.842902|10|6/6/6|passed|
|parent|16|1|3.105448|2.727719|2.349993|1.483029|7|5/5/5|rejected|
|parent|16|5|18.076376|16.670395|15.264879|4.125832|11|6/6/6|passed|
|parent|20|1|2.213783|1.831445|1.449231|1.488365|8|5/5/5|rejected|
|parent|20|3|13.510169|12.543747|11.577631|4.589765|10|6/6/6|passed|
|parent|20|5|19.215003|17.671346|16.128155|4.110997|11|6/6/6|passed|
|native旧中心|16|3|17.187991|16.305532|15.423452|4.080065|10|2/2/2|rejected|
|parent旧中心|16|3|16.150293|15.148365|14.146745|3.082168|10|6/6/6|passed|


逐项淘汰理由：{'slopecarry_370_ETH_S12_D1': ['positive_all_costs', 'nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct', 'four_underlying_native_closes1', 'gross_plus_funding_to_cost1_gte2_5'], 'slopecarry_370_ETH_S12_D3': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'slopecarry_370_ETH_S12_D5': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'slopecarry_370_ETH_S16_D1': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct', 'four_underlying_native_closes1'], 'slopecarry_370_ETH_S16_D5': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'slopecarry_370_ETH_S20_D1': ['positive_all_costs', 'nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct', 'four_underlying_native_closes1', 'gross_plus_funding_to_cost1_gte2_5'], 'slopecarry_370_ETH_S20_D3': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'slopecarry_370_ETH_S20_D5': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'slopecarry_370_parent_BTC29H3_ETH_S12_D1': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'slopecarry_370_parent_BTC29H3_ETH_S16_D1': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'slopecarry_370_parent_BTC29H3_ETH_S20_D1': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct']}。

独立审计通过：24新原生+24新父组合+18旧成本曲线，8880次新决策、46620条资金费、1074笔成交、924项全期/逐月指标、133713项风险检查，0订单拒绝。独立Fraction/Horner、实际数量/成本/现金流、完整NAV及逐折/整体DD重建，不调用新simulate/decide/trade。

完整旧路径比较526个同C/N原生定义、236个父组合，16项中0项三档全路径此前出现。具体源与内部别名见NAV哈希诊断；不同实参各自登记，路径别名不是独立盈利样本。

事后比较S20/D5：3x收益16.128155%高于旧中心14.146745%，整体DD4.110997%也高于旧中心3.082168%，不构成收益和回撤同时改善。该描述不替换预设S16/D1及其淘汰结论，不新增试验或宣称独立最优。

原账户本窗仅闭合mark/risk：SMA/single Nov10 10:30–12:30，L4/FEWM12:10–14:10，0新资金费、日决策、成交。保持原现金、q、desired、成本、风险及完整NAV，不重开、不加本金、不采用研究规则。全链Nov10_00、08及原日决策各自一次，本窗不重复08，原公开字段/检索UTC/SHA保留。

SMA完整NAV前缀56830→56950，累计56909分钟；原账本与风险连续性独立核验。

single完整NAV前缀21267→21389，累计20909分钟；原账本与风险连续性独立核验。

L4完整NAV前缀14004→14126，累计13809分钟；原账本与风险连续性独立核验。

FEWM完整NAV前缀8112→8234，累计8049分钟；原账本与风险连续性独立核验。

原SMA负收益及全部partial淘汰结果保留，继续原长期计划；这些是未成熟延迟shadow，不等同paper10十策略真实报价模拟或180日前向资格。SMA日上下文仍为031055轮65个完整SPOT日、截至Nov10 UTC00:00，当前minute数组不能替换日上下文。

下轮SMA/single12:30–14:30只mark；L4/FEWM14:10–16:10跨16 UTC，须等16:11参考闭合、取得新的真实Nov10_16 fundingTime/rate/mark，并在绑定/reserve前核对，再按各自原q/现金结算一次。旧funding16_current_preflight是Nov9，不能替代Nov10或复制他人现金流；本轮未预抓取未来费率/时间，也未预测入账。将来single自己的14:30–16:30窗口跨16时可复用已验证公共字段，但用自己的持仓。下一日事件Nov11 UTC00:01，SMA届时从当前Float状态延续并刷新65日SPOT。

下一方向提案未执行：固定资金费M4/VW8/R0.00875及EWM S16/D3/K0.75%、H2%/E0.75%/VC5%，检验快ROC窗口L=[4,5,6]×价格波动窗口V=[8,10,12]。L5/V10旧中心只读，其余先全登记簿/数值图查重；完整代码/spec及Fraction ROC、样本logvol、持仓/反手、因果/上下文检查后reserve。PRICE_V与资金费BUDGET_VW8独立，成本21日、趋势19日、BTC30日应由33日源覆盖但须复核。资本/名义金额/raw权重/时间/门槛不改，不预认改善，不建新冻结账户。

只读监控：原生检查失败，按任务保留上次有效快照；10190研究行、旧10190行保持，paper10共10账户/319观察，gzip为4659215字节。原生回执留档，没有重部署或新建任务。十策略本轮失败由其自身留档，研究任务不重跑其窗口、不重置其账户。

真实失败保留：准备/检查记录3项，HTTP/传输失败2次。报告候选文本的一处引号错误在写文件前被compile拒绝，修正后再核验，原错误回执留档，实际回测/报告原字节保持。提交前空白门禁又发现文档末尾多余空行，首次封存与失败回执已完整归档；规范末尾空白后重新封存，金融结果不改。实际失败响应（含空响应）、stderr、原bounded重试均保存，TLS验证未关闭。4项预期合成RED分列；完整策略与已完成观察没有重跑。

继承print或派生键名中的旧K/VC、H/E、VW/R及16资金费标签见derived_label_correction，以冻结S/D完整spec、绑定代码、逐笔/全NAV与独立核验为准；已finish报告不改写。复现argv/cwd/UTC/退出码见reproduction_history及commands/receipt，必要数据哈希、全部结果与账户账本保留，可重建中间文件清理。

main排他锁内完成登记、核验、只读快照与封存；普通非force提交推送后核对远端ref、完整tree/blob及三条永续链，再释放锁。实际终态见.git/automation_proofs/20261110T151431Z.json，本文不单独作为push成功证明。
