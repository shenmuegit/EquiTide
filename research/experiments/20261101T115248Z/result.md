# BTC原生资金临界区间与ETH入场门槛验证

本轮12个新金融定义：BTC3125/N312.5和4375/N437.5各自的动量组件及常多参考共4个原生路径，交叉ETH H2%/2.5%/3%共6个新父候选，两个同资金/同初始入场预算常多父参考；36个1/2/3倍成本场景全部先独立reserve再计算。旧BTC3750的3个组合候选、1个持有父及6个原生来源只读复用，共10个唯一旧定义。完整读取25004事件、12380ID、263份结论；初始16项均有真实原始证据，不精确重复。

假设见结果前固定：上轮BTC2500近期失败，旧3750/H2.5成为宽网格内部Sharpe峰值，但宽网格严格近期仅4/9。预先选3750两侧等距625的3125/4375实际银行，保留H2/2.5/3%邻域，检验更近的真实数量取整/成本临界区域。BTC N固定为自身初始资金10%，资金与入场预算绑定，不能声称两个独立参数。新的4原生路径从真实行情计算q/LOT、tick、规模冲击、现金和资金费，不线性缩放旧NAV。此选择已使用过往结果，只是开发研究，不是独立未触碰最终测试。

组合原权重[1,1]为一份完整BTC原生银行和一份ETH15000银行。总初始资金18125/18750/19375，BTC资金占比17.241379%/20%/22.580645%；BTC初始N312.5/375/437.5，ETH N4500。美元净值直接相加，不重复乘资金份额、不平均Sharpe/收益率；无父再平衡订单、资金转账、NAVresize或跨账户抵押净额。实际N/C0各不相同，不称同风险比较。常多基准匹配银行及初始N，非满仓买持或同风险基准；另与现金0%比较。

BTC原ROC31/H4%/E1%；ETH固定L4/S28、退出缓冲绝对ROC0.0025、V10样本logvol cap0.045，仅新入场/翻向过滤。ETH priorfastROC>H空、<−H多；带内实际多仅r<E、空仅r>−E保留，等号退出，slow方向始终门控。q=floor(N/prior完整日close/LOT)×LOT，下一UTC00:01原生OPEN不利tick，翻向先平后开，同向保留实际q，370日终止计费平仓。

历史边界2025-10-19 UTC00:01至2026-10-24 UTC00:01，连续370天、12个完整30天折和10天尾折；跨折不重置现金/q/成本/funding。近期40天继承day330，8个5天折。固定规则无拟合或标签，purge0、预热30天/间隔3天，决策仅用prior完整日close；成本仅past20完整日quoteADV和样本logvol。历史多次使用与多重选择偏差明示，不把本轮正收益或局部邻域当独立未来/DSR/PBO证明。

1/2/3倍成本：每边5bp费用、1bp半价差、2bp滑点、0.5×past20logvol×sqrt(actualq×OPEN/past20quoteADV)。真实资金费结算纳秒/rate/mark/当时q，支出倍增、正收入不放大。实际LOT/tick/minnotional、参与率<=0.001、费用后1倍入场抵押和每银行1%闭合小时不利mark维护代理；线性永续无需现货借币，不虚构借币费。没有L2/TCA、完整历史抵押阶梯/逐tick清算或真实容量证明。

原门槛不放宽：每档全年净正，1倍>=9/12正完整30天折；每档近期40天净正且>=6/8正5天折；3倍完整DD<=25%；资金/H索引半径1含中心的局部3倍净正比例与严格近期达标比例各>=60%；至少4次平仓，毛价差PnL+fund/执行成本>=2.5，零拒单/负抵押/维护代理违规、终止flat、至少180天。原生动量component按资金轴一维邻域执行同样财务门槛，单列资格，不计父候选。4个持有控制（2原生、2父）按冻结非候选criterion=false保留真实结果，控制角色失败不等于未计算。

|新配置|角色|BTC银行/总C0|H%|1倍净%|2倍净%|3倍净%|3倍整体DD%|正月/12|近期正折1/2/3倍|状态|
|---|---|---|---:|---:|---:|---:|---:|---:|---|---|
|nativebudget370_BTC_C3125_N312.5_momentum|component|3125/3125|4|2.567854|2.126766|1.685682|2.460028|9|4/4/4|rejected|
|nativebudget370_BTC_C3125_N312.5_hold|benchmark_component|3125/3125|—|-1.851467|-2.080081|-2.308696|4.053890|6|4/4/4|rejected|
|nativebudget370_BTC_C4375_N437.5_momentum|component|4375/4375|4|3.171533|2.695832|2.220178|2.616215|9|4/4/4|rejected|
|nativebudget370_BTC_C4375_N437.5_hold|benchmark_component|4375/4375|—|-2.644962|-2.971554|-3.298165|5.777670|6|4/4/4|rejected|
|bankmix370_parent_B3125_H200|candidate|3125/18125|2|10.932444|9.392766|7.853056|3.956500|10|6/6/6|passed|
|bankmix370_parent_B3125_H250|candidate|3125/18125|2.5|11.394264|10.070857|8.747607|3.421886|11|6/6/6|passed|
|bankmix370_parent_B3125_H300|candidate|3125/18125|3|8.945429|7.787414|6.629633|3.421886|11|5/5/5|rejected|
|bankmix370_parent_B4375_H200|candidate|4375/19375|2|10.529107|9.052491|7.575854|3.739034|10|6/6/6|passed|
|bankmix370_parent_B4375_H250|candidate|4375/19375|2.5|10.961133|9.686834|8.412692|3.238816|11|6/6/6|passed|
|bankmix370_parent_B4375_H300|candidate|4375/19375|3|8.670288|7.550710|6.431361|3.238816|11|5/5/5|rejected|
|bankmix370_hold_B3125|benchmark|3125/18125|—|-10.400431|-11.108224|-11.816020|18.732335|6|3/3/3|rejected|
|bankmix370_hold_B4375|benchmark|4375/19375|—|-10.028061|-10.727063|-11.426072|18.164501|6|4/3/3|rejected|

6个新父候选4通过、2淘汰；两个原生动量组件状态[('nativebudget370_BTC_C3125_N312.5_momentum', 'rejected', ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct']), ('nativebudget370_BTC_C4375_N437.5_momentum', 'rejected', ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'])]；4个持有控制单列。全部配置失败判据{'nativebudget370_BTC_C3125_N312.5_momentum': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'nativebudget370_BTC_C3125_N312.5_hold': ['benchmark_control_not_strategy_candidate'], 'nativebudget370_BTC_C4375_N437.5_momentum': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'nativebudget370_BTC_C4375_N437.5_hold': ['benchmark_control_not_strategy_candidate'], 'bankmix370_parent_B3125_H200': [], 'bankmix370_parent_B3125_H250': [], 'bankmix370_parent_B3125_H300': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'bankmix370_parent_B4375_H200': [], 'bankmix370_parent_B4375_H250': [], 'bankmix370_parent_B4375_H300': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'bankmix370_hold_B3125': ['benchmark_control_not_strategy_candidate'], 'bankmix370_hold_B4375': ['benchmark_control_not_strategy_candidate']}。所有正/负收益、逐折/逐变体及控制结果保存并finish，不择优隐藏失败。

10份CSV保留36新成本场景、逐月/近期折/每日NAV、9格点、9旧父场景、36相邻边、27同资金hold/cash比较、18旧原生成本来源与12资金分配说明。每场景545013完整NAV点SHA、原生逐笔/资金费/状态段及新父源哈希保留。独立审计用Fraction信号和Decimal账务核对实际q/LOT、成本、fund、抵押、闭合小时风险、完整净值和整体/逐折DD，不调用策略simulate/decide/trade重跑。

全网格正Sharpe比例、最高点/边界、多个指标和描述性相邻悬崖均披露；旧点仅增加当前邻域诊断，原canonical status/criteria/sensitivity不重写。描述性相邻2std启发式不是统计显著性，正收益回测不能称稳定实盘盈利。

冻结延迟观察分别续接：原SMA65、原singleS28从Nov1 UTC08:30至10:30；独立未过滤L4/H2从10:10至12:10，仅在12:11参考分钟闭合后采集。08资金费已记账，不重复；真实cash/q/risk和全NAV前缀不重置。三账户原规则/本金/持仓/成本/终止计划保持，历史资金邻域不替换冻结账户；部分资格rejected保留各自180天计划。延迟shadow不充当十策略实时公开报价成交。

只读网页快照同main排他锁生成，执行登记/监控门禁；生成失败恢复上次有效快照并留档。只汇总已有报告/账户，不新建回测或模拟成交，不改规则/本金/持仓/预算、不部署网页或新增定时器、不下真实订单。

封存结论：6个新父候选4项历史门槛通过、2项淘汰。通过为BTC3125/4375银行各自交叉ETH H2%/2.5%，三倍成本370日净收益7.575854%至8.747607%，完整DD3.238816%至3.956500%。各通过项每档近期6/8正5天折、局部严格近期支持至少2/3，其余原冻结门槛均满足。H3%的两新候选近期仅5/8，局部严格近期支持50%，按原标准淘汰。

两个新BTC原生动量组件单独近期4/8和局部近期失败，不能把组合资格当单币资格；4个常多控制实际负收益单列保留，非策略候选。完整12定义/36场景、9观察/27场景均成功reserve后计算并finish，共21新ID/42追加事件。

当前更近的3×3资金/H邻域9点每档全年收益/Sharpe全正，严格近期6/9；最大Sharpe仍在旧3750/H2.5内部点，旧canonical资格/报告字节保持。所有成本档的描述性相邻悬崖仍触发，提示对ETH阈值的依赖。这是由既往研究启发的窄开发邻域，不覆盖先前BTC2500的失败区，不能称广域稳健、独立未触碰最终测试或稳定实盘盈利。

独立审计actualexit0：12新原生、24新父成本曲线，共19620468完整NAV点；18旧原生曲线和12旧父NAV哈希只读。4440次独立新原生决策、33300资金费、840成交、756整体/月指标、214764小时风险检查，无拒单/负抵押/维护代理违规。10个唯一旧来源及22766个旧保护文件字节保持。实际LOT数量、规模冲击和成本完整验证，但无真实TCA/盘口/完整清算档位或容量证明。

原SMA65续08:30至10:30：43741旧NAV+120=43861点，43829分钟/30天，0新日决策/成交；完整Float现金/q/desired/trades与所有旧NAV前缀保持。原singleS28同窗保留10000/10000,N1000/3000,ETHL3：7888旧点+122=8010点，7829分钟/198ID/66窗。本窗无新日决策/成交/资金费；9次小时风险检查包括08资金费前后正时长现金状态，0违规，08资金费不重复记账。

独立未过滤L4/H2保留5000/15000,N500/4500,S28zeroexit，10:10续12:10，仅12:11参考闭合后采集：625旧NAV+122=747点，729分钟/21ID/7窗。本窗0新日决策/成交/资金费，6次小时风险检查/0违规；独立pointer/book/risk和累计链不与原S28混用。三账户都未成熟180天，部分rejected不取消原冻结长期计划，不使用本轮参数替换规则或重开现金。

只读监控同锁registry/snapshot/monitor门禁及每个旧行完整字典核验actualexit0：8908研究行，旧8896行完全一致，10固定报价账户/211真实观察，gzip4018831字节，沿用5MB预算。未改监控代码/预算、paper计划/本金/持仓，未部署网页/新增定时器或下真实订单。

报告说明更正：执行器继承了上一轮execution_scope文字，实际36场景结果/规格/状态均正确；原始报告逐字节压缩保存为research/experiments/20261101T115248Z/report_as_executed.json.gz（解压SHA 3f44a110644c283b8df057e456da4242632f740dcf38b213c1b073145974ab72），仅更正该说明，全部其他字段完全相等。未修改已绑定金融代码、规则、判据、收益、成交、账户或归档，模型/已完成观察0重跑；更正代码/回执/前后哈希公开留档。实际HTTP失败1次，真实原始尝试/stderr/响应和回执全保留。

核验后只清理本轮可重建语义元数据清单1408203字节，原SHA/定义数/基准版本在cleanup_verification.json；金融结果/账户账本删除均0，剩余npy/pyc/tmp/checkpoint为0。保留10CSV、全部归档/状态段/必要逐笔、当前轻量HTTP/packet及下轮必要状态。main非强制push与完整远端tree/必要blob、198ID原S28链/21ID独立L4链、实际publisher终态/解锁证明在.git/automation_proofs/20261101T115248Z.json；封存不预写commit SHA。
