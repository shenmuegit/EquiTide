# ETH快周期与入场门槛联合验证

本轮12个新定义：ETH快周期L3/L5各交叉H2%/2.5%/3%，共6个实际原生配置和6个BTC/ETH父组合，36个1/2/3倍成本场景全部先reserve再实际计算。旧L4的3个原生和3个父格点、匹配持有父及其来源只读，共10个唯一旧定义；不因策略族相同排除新参数，也不重测已有结果。读取完整25066事件/12411ID、264份结论，初始16项均有真实原始证据。

假设预先固定：已有L4/H2.5%和资金邻域支持仅属重复开发历史，本轮检验快周期改为相邻3或5天时能否保留支持，不进一步细化银行资本。固定BTC原ROC31/H4/E1、ETH S28、退出缓冲绝对ROC0.0025、V10样本logvol上限0.045。ETH priorfastROC>H空、<−H多，带内实际多仅r<E、空仅r>−E保留，等号退出；slow方向始终门控，波动率只过滤新入场/翻向。

实际银行固定BTC3750/N375、ETH15000/N4500，总初始资本18750。原始权重[1,1]为两份完整银行，资金占比20%/80%，总初始入场预算4875/18750=26%；不自动归一化或重复乘份额，不线性缩放旧净值、复制同币银行、转移现金、父再平衡、NAVresize或跨抵押。原生q=floor(N/prior完整日close/LOT)×LOT，下一UTC00:01原生OPEN不利tick，翻向先平后开，同向保留q，终止计费平仓。

真实2025-10-19 UTC00:01至2026-10-24 UTC00:01连续370日，12完整30日折+10日尾折，无跨折现金/持仓/成本/资金费重置；近期40日继承day330、8×5日折。固定规则无拟合/标签，purge0、预热30日/间隔3日，所有信号及past20完整日quoteADV/logvol仅用过去。参数选择已受既往研究影响，不能把这段历史称未触碰最终测试集或独立未来验证；未计算DSR/PBO显著性。

成本1/2/3倍含每边5bp费用、1bp半价差、2bp滑点及0.5×past20logvol×sqrt(actualq×OPEN/past20quoteADV)。真实资金费settlement纳秒/mark/rate/当时q，支出倍增而正收入不放大；原生LOT/tick/minnotional、参与率<=.001、费用后1倍入场抵押，各银行独立1%闭合小时不利mark维护代理。线性永续无现货借币，不虚构借币费；无L2/TCA、完整历史清算档位/逐tick清算或真实容量证明。同期旧匹配持有为同银行与初始预算的常多参考，不是满仓买持或同风险基准，现金0%另列。

预冻结门槛：每档全年净正、1倍>=9/12正完整月；每档近期净正且>=6/8正5日折；3倍完整DD<=25%；L/H索引半径1含中心的局部3倍正收益比例及严格近期比例各>=60%；至少4次平仓、毛价差PnL+fund/执行成本>=2.5，零拒单/负抵押/维护代理违规、终止flat、至少180日。原生ETH与父组合各自在自己的3×3面上独立判定；原生组件资格与父候选分开。旧canonical状态/判据/敏感性不重写，仅本轮诊断。

|新配置|范围/角色|L|H%|1倍净%|2倍净%|3倍净%|3倍整体DD%|正月/12|近期正折1/2/3倍|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|lookback370_ETH_L3_H200_E025_V10|native/component|3|2|12.408271|10.456298|8.503616|4.973181|9|5/4/4|rejected|
|lookback370_ETH_L3_H250_E025_V10|native/component|3|2.5|12.008510|10.435455|8.861827|3.975470|9|5/4/4|rejected|
|lookback370_ETH_L3_H300_E025_V10|native/component|3|3|8.305728|6.882174|5.458167|4.060460|9|4/3/3|rejected|
|lookback370_ETH_L5_H200_E025_V10|native/component|5|2|13.074835|11.410995|9.747906|4.978665|10|4/4/4|rejected|
|lookback370_ETH_L5_H250_E025_V10|native/component|5|2.5|9.907072|8.501373|7.096215|4.899742|10|3/3/3|rejected|
|lookback370_ETH_L5_H300_E025_V10|native/component|5|3|8.561340|7.447483|6.334072|4.714368|10|1/1/1|rejected|
|lookback370_parent_L3_H200|parent/candidate|3|2|10.561496|8.907660|7.253259|4.254744|9|6/6/6|passed|
|lookback370_parent_L3_H250|parent/candidate|3|2.5|10.241686|8.890985|7.539829|3.305465|10|6/6/6|passed|
|lookback370_parent_L3_H300|parent/candidate|3|3|7.279461|6.048360|4.816900|3.362275|10|5/5/5|rejected|
|lookback370_parent_L5_H200|parent/candidate|5|2|11.094747|9.671417|8.248692|3.896432|11|5/5/5|rejected|
|lookback370_parent_L5_H250|parent/candidate|5|2.5|8.560537|7.343720|6.127339|3.846302|11|4/4/4|rejected|
|lookback370_parent_L5_H300|parent/candidate|5|3|7.483951|6.500608|5.517624|3.762345|11|3/3/3|rejected|

6个新父候选2通过/4淘汰。所有原生和父配置失败判据：{'lookback370_ETH_L3_H200_E025_V10': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lookback370_ETH_L3_H250_E025_V10': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lookback370_ETH_L3_H300_E025_V10': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lookback370_ETH_L5_H200_E025_V10': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lookback370_ETH_L5_H250_E025_V10': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lookback370_ETH_L5_H300_E025_V10': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lookback370_parent_L3_H200': [], 'lookback370_parent_L3_H250': [], 'lookback370_parent_L3_H300': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lookback370_parent_L5_H200': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lookback370_parent_L5_H250': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lookback370_parent_L5_H300': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct']}。所有正负收益、失败和每个变体保留并finish，不因全年正收益放宽近期/敏感性。

11份CSV保留36个新成本场景、逐月/近期折/每日NAV、原生与父两张完整9格点、9个旧父场景、72条相邻边、27次匹配hold/cash比较、18旧原生成本来源及10条固定分配说明。完整每场景NAV哈希、原生逐笔/资金费/状态段及父源哈希留存；独立Fraction信号/Decimal账务核验不调用策略simulate/decide/trade。全网格正Sharpe比例、多指标、边界和描述性相邻2std悬崖均披露；该启发式不是统计显著性，回测盈利不代表稳定实盘盈利。

冻结观察分别续接：原SMA65与原singleS28从Nov1 UTC10:30至12:30；独立未过滤L4/H2从12:10至14:10，仅14:11参考分钟闭合后采集。保持原规则/本金/q/现金/desired/risk/费用/全部NAV前缀及终止计划，08资金费已记账不可重复；本轮历史L3/L5/缓冲/波动过滤不注入已有账户，部分rejected继续各自180日计划。延迟shadow不充当十策略真实报价成交。

只读快照同main排他锁运行registry/snapshot/monitor门禁，只汇总已有证据，不产生新回测或成交、不改账户/规则/本金/持仓/预算、不部署网页/新建定时器/下真实订单。生成失败恢复上次有效快照并留具体失败。所有命令退出码、真实HTTP尝试和必要轻量证据留档。

封存结论：6新组合候选2项历史通过/4项淘汰。通过项为ETH L3交叉H2%/2.5%，固定BTC3750/N375与ETH15000/N4500、原权重1/1；3倍成本370日净收益7.253259%至7.539829%，完整DD3.305465%至4.254744%，每档近期6/8正5日折，局部严格近期支持100%或2/3，其他原门槛也满足。L3/H3与全部L5父候选因近期折数及局部近期支持不足淘汰，L5/H2.5和H3还未满足每档近期净正。

六个新原生ETH配置全期净正但近期仅1至4个3倍正5日折，全部单币资格失败，不能把父组合资格当单币资格。原生和父各完整3×3面每档9/9正Sharpe，但严格近期原生0/9、父4/9；旧L4/H2.5仍是各成本内部Sharpe峰值，其本轮父全邻域严格近期支持只有4/9。旧canonical passed按原批次语义保持，不代表通过当前更宽L/H邻域。两面各档描述性相邻悬崖都触发；正收益/局部通过不等于广域稳健、未触碰最终测试或稳定实盘盈利。

12个新定义/36成本场景全部实际reserve后计算并逐项finish；另9观察/27场景完成，合计21新ID/42追加事件。6旧L4格点、旧匹配持有父及来源共10唯一旧定义只读，23021旧保护文件字节保持；无新持有控制计算、无旧报告或资格改写。登记事件总数/ID不是独立金融试验数，规范化非观察研究定义为9349，其中仍可能有无结果记录；多重选择偏差未由简单局部比例消除。

独立审计actualexit0：18新ETH原生成本曲线和18新父曲线，共19620468完整NAV点；18旧原生曲线与12旧父哈希只读。6660次新决策用Fraction独立重建；39960资金费、1656成交、756整体/月指标与136152小时风险状态用Decimal/独立指标核验，零拒单/负抵押/维护代理违规。核对所有新q/LOT/信号可得时间、成本和funding/全NAV/逐折DD，不调用simulate/decide/trade进行金融重跑。仍无真实TCA/L2、完整历史抵押阶梯或逐tick清算/容量证明。

原SMA65续10:30至12:30：43861旧NAV+120=43981点，43949分钟/30天，无新日决策/成交；原Float现金/q/desired/trades与所有NAV前缀保持，nextdailyNov2UTC00:01。原singleS28同窗保留10000/10000,N1000/3000,ETHL3零退出缓冲原规则：8010旧点+122=8132点，7949分钟/201ID/67窗。本窗0新日决策/成交/资金费，6小时风险检查/0违规，08资金费不重复入账。该原S28不等于本轮带退出缓冲和波动过滤的新L3研究策略。

独立未过滤L4/H2保留5000/15000,N500/4500,S28zeroexit，从12:10续14:10，在14:11参考分钟闭合后才采集：747旧NAV+122=869点，849分钟/24ID/8窗；0新日决策/成交/资金费，6小时风险检查/0违规。三账户原plan/core/observer/binding SHA、资金/q/费用/risk和长期终止计划保持，部分rejected不取消各自180日计划，不注入本轮L3/L5或过滤规则。下一L4建议14:10至16:10会跨16资金费，须16:11后按真实精确纳秒/rate/mark/当时q入账一次并保留前后风险状态；本轮未提前计算该未来窗口。

只读快照在同main锁内，registry/snapshot/monitor及所有旧行逐字典门禁实际通过：8920研究配置、旧8908行完全相等、10报价账户/212既有真实观察，gzip4026005字节，沿用5MB预算。不改监控代码/预算/冻结规则/本金/持仓，不重新部署网站或新建定时器，不下真实订单，不把延迟shadow当十策略真实报价成交。

实际HTTP失败1次，所有真实尝试/stderr/原始响应和回执完整保存；一次发布辅助只读检查因子串匹配过宽误报，AST依赖核验恢复exit0并保留原失败，无模型/报告/账户/判据改动；已完成金融模型/观察0重跑。核验后只清理可重建语义元数据2781字节，原SHA/行数/基准版本保留，金融结果/账户账本删除0，npy/pyc/tmp/checkpoint残留0。保留11CSV、全部原生逐笔/资金费/状态段与父档、完整SHA、当前轻量HTTP/packet和下轮必要状态。main非强制push、完整远端tree/必要blob、201ID原S28链/24ID独立L4链、实际publisher终态和解锁证明在.git/automation_proofs/20261101T135218Z.json；封存不预写commit SHA。
