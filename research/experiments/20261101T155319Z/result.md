# ETH快慢周期门控联合验证

本轮12个新定义：快周期L3/4/5交叉慢趋势S24/32，共6个原生ETH配置和6个BTC/ETH组合，36个1/2/3倍成本场景全部实际reserve后计算。S28的3个原生与3个父格点、旧匹配持有父及来源只读，共10唯一旧定义；不因family相同排除新参数，也不精确重复旧结果。完整读取25128登记事件/12442ID、265份结论，初始16项实际证据齐全。

预冻结假设：既有L4/S28峰值与新L3局部支持仍受近期弱一致性影响。本轮将慢趋势门控从28日扰动为24/32日，交叉快周期3/4/5日，固定H=2.5%、退出缓冲绝对ROC0.0025、V10样本logvol cap0.045，检验门控时域能否改善平台，而不是继续细化资金或入场阈值。参数选择受既往研究影响，这仍是重复开发历史，不是未触碰最终测试。

BTC原ROC31/H4%/E1%不变。ETH fastROC=C[i-1]/C[i-1-L]-1、slowROC=C[i-1]/C[i-1-S]-1；fast>0.025空、<−0.025多。带内实际多仅r<0.0025、实际空仅r>−0.0025保留，等号退出，slow方向始终门控；V10波动上限只过滤新入场/翻向，不阻止退出或同向保留。原生q=floor(N/prior完整close/LOT)×LOT，下一UTC00:01原生OPEN不利tick，反向先平后开，终止计成本平仓。

固定实际银行BTC3750/N375、ETH15000/N4500，总初始资本18750；原权重[1,1]为两份完整银行，资金份额20%/80%，总初始入场预算4875/18750=26%。按真实银行美元净值相加，不归一化权重、不重复乘资金份额、不线性缩放旧净值、复制同币银行、转账、父调仓、NAVresize或跨账户抵押。旧常多参考匹配银行和初始N，不是满仓买持或同风险基准；现金0%另列。

数据边界为真实2025-10-19 UTC00:01至2026-10-24 UTC00:01连续370天，12完整30天折+10天尾折，状态/现金/q/成本/资金费跨折不重置。近期40天继承day330、8×5天折。固定规则无训练/标签，purge0、预热30天/间隔3天；33个已完整预热日使S32首决策i=33可用close[0]，不负索引或未来填充。所有信号、past20完整日quoteADV/logvol只用当时过去数据。多重选择偏差没有被局部比例或简单正Sharpe消除，未计算DSR/PBO显著性。

1/2/3倍成本包括每边5bp费用、1bp半价差、2bp滑点和0.5×past20logvol×sqrt(actualq×OPEN/past20quoteADV)。真实资金费结算纳秒/rate/mark/当时q，支出倍增、正收入不放大；原生LOT/tick/minnotional、参与率<=0.001、费用后1倍入场抵押、各银行独立1%闭合小时不利mark维护代理。线性永续无现货借币，不虚构借币费；没有L2/TCA、完整历史阶梯/逐tick清算或真实容量证明。

原门槛不放宽：每档全年净正、1倍>=9/12正完整月；每档近期净正且>=6/8正5日折；3倍完整DD<=25%；快L/慢S索引半径1含中心的局部3倍净正和严格近期比例均>=60%；至少4平仓、毛价差PnL+fund/执行成本>=2.5，零拒单/负抵押/维护代理违规、终止flat、至少180天。原生与父各在自身3×3面判定，单币与组合资格分开。旧canonical状态/判据/敏感性不重写，只增加当前诊断。

|新配置|范围/角色|L|S|1倍净%|2倍净%|3倍净%|3倍整体DD%|正月/12|近期正折1/2/3倍|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|slowgate370_ETH_L3_S24_H250_E025_V10|native/component|3|24|6.780878|5.052685|3.324044|7.643717|6|3/2/2|rejected|
|slowgate370_ETH_L3_S32_H250_E025_V10|native/component|3|32|6.977443|5.257990|3.538042|6.477615|8|4/3/3|rejected|
|slowgate370_ETH_L4_S24_H250_E025_V10|native/component|4|24|7.834185|6.157140|4.479868|6.002809|7|3/3/3|rejected|
|slowgate370_ETH_L4_S32_H250_E025_V10|native/component|4|32|7.924511|6.267306|4.610651|5.331555|7|4/3/3|rejected|
|slowgate370_ETH_L5_S24_H250_E025_V10|native/component|5|24|5.962793|4.516394|3.070639|6.139674|8|1/1/1|rejected|
|slowgate370_ETH_L5_S32_H250_E025_V10|native/component|5|32|6.259728|4.964095|3.668733|4.978415|8|2/2/2|rejected|
|slowgate370_parent_L3_S24_H250|parent/candidate|3|24|6.059581|4.584769|3.109602|6.413541|7|5/5/5|rejected|
|slowgate370_parent_L3_S32_H250|parent/candidate|3|32|6.216833|4.749013|3.280800|5.220086|9|5/5/5|rejected|
|slowgate370_parent_L4_S24_H250|parent/candidate|4|24|6.902227|5.468333|4.034261|5.094439|8|4/4/4|rejected|
|slowgate370_parent_L4_S32_H250|parent/candidate|4|32|6.974488|5.556466|4.138887|4.251110|8|5/4/4|rejected|
|slowgate370_parent_L5_S24_H250|parent/candidate|5|24|5.405113|4.155736|2.906878|5.152568|10|3/3/3|rejected|
|slowgate370_parent_L5_S32_H250|parent/candidate|5|32|5.642661|4.513897|3.385353|3.970336|9|3/3/3|rejected|

6新父候选0历史通过/6淘汰。全部原生与父失败判据{'slowgate370_ETH_L3_S24_H250_E025_V10': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'slowgate370_ETH_L3_S32_H250_E025_V10': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'slowgate370_ETH_L4_S24_H250_E025_V10': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'slowgate370_ETH_L4_S32_H250_E025_V10': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'slowgate370_ETH_L5_S24_H250_E025_V10': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'slowgate370_ETH_L5_S32_H250_E025_V10': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'slowgate370_parent_L3_S24_H250': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'slowgate370_parent_L3_S32_H250': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'slowgate370_parent_L4_S24_H250': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'slowgate370_parent_L4_S32_H250': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'slowgate370_parent_L5_S24_H250': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'slowgate370_parent_L5_S32_H250': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct']}。所有负收益/负期段与失败保留并finish，不按全年正收益放宽近期或邻域要求。

11CSV保存36新场景、逐月/近期折/每日NAV、原生与父两张完整9格点、9旧父场景、72相邻边、27同资金hold/cash比较、18旧原生成本来源及10条固定分配说明。保留完整NAV SHA、原生必要逐笔/资金费/状态段及父源哈希；独立审计用Fraction信号和Decimal账务，不调用simulate/decide/trade进行金融重跑。全格点正Sharpe比例、多指标、边界和描述性2std悬崖均报告，描述性启发式不是统计显著性或稳定实盘盈利证明。

原SMA65及原singleS28续Nov1 UTC12:30至14:30；独立未过滤L4/H2续14:10至16:10，仅16:11参考闭合后采集，必须真实核算16资金费纳秒/rate/mark/当时q并只记一次、保留前后正时长风险状态。三账户原规则/本金/q/现金/desired/risk/费用/完整NAV前缀及终止计划保持，本轮L/S/缓冲/波动参数不注入已有账户。部分rejected继续180天计划，延迟shadow不充当十策略真实报价成交。

同main排他锁完成registry/snapshot/monitor门禁，快照只读已有证据，不新回测/产生成交、不改账户/规则/资金/持仓/预算、不部署网页/建定时器/下真实订单。失败保留上一有效快照与具体证据。初始合成夹具曾因S24读取另一历史段而失败，原脚本/日志/根因/修正回执保留；只调整合成历史段，策略/规格/判据不改，且在任何reserve或真实回测前恢复通过。

封存结论：6新组合和6新原生配置全淘汰。组合在3倍成本370日净收益仍为2.906878%至4.138887%，完整DD3.970336%至6.413541%，但近期3倍正5日折只有3至5/8、局部严格近期支持25%至50%，均不足原门槛；L3/S24与L4/S24、L4/S32还有正月不足9/12，L5/S24未满足每档近期净正。六个原生配置正月只有6至8/12且近期也不足，不能把全年净正当稳健。

快L/慢S两面每档9/9正Sharpe，但严格近期原生0/9、父2/9；支持仅旧S28列的L3/L4，旧L4/S28仍是内部Sharpe峰值。S24/S32两侧净收益与Sharpe大幅低于旧S28，所有成本档描述性相邻悬崖均触发；中心本轮完整邻域严格近期只有2/9。旧canonical passed保留原批次语义，不能据此称通过当前宽L/S网格、全域稳健、独立最终测试或稳定实盘盈利。

12新定义/36成本场景全部实际reserve后计算并逐项finish；另9观察/27场景完成，共21新ID/42追加事件。6旧S28格点、旧匹配持有父及来源共10唯一旧定义只读，23274旧保护文件字节保持；无旧资格/报告改写。登记事件/ID不等于独立金融试验数，规范化非观察研究定义9361中仍可能有无结果记录，多重选择偏差未由局部比例消除。

独立审计actualexit0：18新ETH原生与18新父成本曲线，共19620468完整NAV点；18旧原生和12旧父哈希只读。6660次新决策按实际S24/S32用Fraction独立核验，39960资金费、1692成交、756整体/月指标与138438小时风险状态用独立Decimal/指标重建，无拒单/负抵押/维护代理违规。策略现金/数量/信号可得时间/费用价差滑点规模冲击/funding/完整NAV和逐折DD一致，不调用simulate/decide/trade重跑。仍无真实TCA/L2、完整历史档位/逐tick清算或容量证明。

原SMA65续Nov1UTC12:30至14:30：43981旧NAV+120=44101点、44069分钟/30天，无新日决策/成交，原Float现金/q/desired/trades与全部旧前缀保持，nextdailyNov2UTC00:01。Asia/Shanghai本地已Nov2不提前触发UTC日决策。原singleS28同窗保留10000/10000,N1000/3000,ETHL3原零缓冲规则：8132旧NAV+122=8254点，8069分钟/204ID/68窗；0新日决策/成交/资金费，6小时风险检查/0违规，08资金费不重复。下一原S28窗口14:30至16:30应实际处理16资金费，不继承L4账户现金流。

独立未过滤L4/H2保留5000/15000,N500/4500,S28zeroexit，14:10续16:10，仅16:11参考闭合后采集：869旧NAV+124=993点，969分钟/27ID/9窗；本窗0新日决策/成交，16资金费实际6记录，逐q/mark/rate/精确ns独立核验现金流[{'asset': 'BTC', 'cost': '1', 'timestamp_ns': 1793548800000000000, 'base_usdt': '0.04677055686087000000000000000', 'amount_usdt': '0.04677055686087000000000000000', 'mark': '77950.92810145', 'rate': '0.00010000'}, {'asset': 'BTC', 'cost': '2', 'timestamp_ns': 1793548800000000000, 'base_usdt': '0.04677055686087000000000000000', 'amount_usdt': '0.04677055686087000000000000000', 'mark': '77950.92810145', 'rate': '0.00010000'}, {'asset': 'BTC', 'cost': '3', 'timestamp_ns': 1793548800000000000, 'base_usdt': '0.04677055686087000000000000000', 'amount_usdt': '0.04677055686087000000000000000', 'mark': '77950.92810145', 'rate': '0.00010000'}, {'asset': 'ETH', 'cost': '1', 'timestamp_ns': 1793548800000000000, 'base_usdt': '-0E-16', 'amount_usdt': '-0E-16', 'mark': '2265.78263566', 'rate': '-0.00001034'}, {'asset': 'ETH', 'cost': '2', 'timestamp_ns': 1793548800000000000, 'base_usdt': '-0E-16', 'amount_usdt': '-0E-16', 'mark': '2265.78263566', 'rate': '-0.00001034'}, {'asset': 'ETH', 'cost': '3', 'timestamp_ns': 1793548800000000000, 'base_usdt': '-0E-16', 'amount_usdt': '-0E-16', 'mark': '2265.78263566', 'rate': '-0.00001034'}]。正收入不放大，负支出按成本倍增，ETHflat仍记录零现金流；16前后现金/risk状态保留，6小时风险检查/0违规。下一17小时应检查所有正时长的前后状态，不能压平成最终book。三账户规则/本金/持仓/费用/全NAV前缀/源代码与长期终止计划均不改，部分rejected不取消180日计划，不注入本轮L/S/缓冲/过滤规则。

同main锁registry/snapshot/monitor及全部旧行逐字典核验actualexit0：8932研究配置、旧8920行完全相等、10固定报价账户/213既有真实观察，gzip4033734字节，沿用5MB预算。只汇总已有报告/账户，不新回测/成交，不改监控/预算/规则/本金/持仓，不部署网页/新建定时器/下真实订单，不把延迟shadow当十策略真实报价成交。

真实失败与恢复：初始合成夹具把S24索引20的价格错误预期为60，实际是100，策略正确门控为flat；已保存原check_primitives_before_fixture_fix.py、初始exit1日志、fixture_root_cause与只改合成历史段的fixture_fix。初始重试通过并绑定后才有首个reserve/真实回测，策略/规格/失败门槛未改；全部模型/已完成观察0重跑。实际HTTP失败1次，真实尝试/stderr/原始响应及恢复回执全留档。

核验后只清理可重建语义元数据2820字节，原SHA/行数/基准版本保存，金融结果/账户账本删除0，npy/pyc/tmp/checkpoint残留0。保留11CSV、完整状态段/必要逐笔/资金费/父档、NAV SHA、当前轻量HTTP/packet及下轮必需状态。main非强制push、完整远端tree/必要blob、204ID原S28链/27ID独立L4链及真实publisher终态/解锁证明在.git/automation_proofs/20261101T155319Z.json，封存不预写commit SHA。
