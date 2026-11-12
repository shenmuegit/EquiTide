本轮完成后续时间区间的22个真实配置、66个成本场景：BTC固定组件1、ETH预设窗口组件9、匹配持有组件2、候选组合9、匹配持有父项1。所有22项先独立reserve，随后一次实际evaluate、独立审计及finish，全部以rejected/result_available=true保存；正收益不满足资格，负收益对照与负折完整保留。无实际结果的前置数据失败不伪装回测淘汰。

新证据：九个组合三倍成本净收益均0.471978%，完整连续18日最大回撤0.336860%；同期间匹配持有为-3.799329%。ETH九组全部零开仓、15000现金，收益/费用/资金费完全来自同一固定BTC组件。不是九项独立获利策略，不能据此认定ETH窗口稳健或稳定实盘盈利。

完整读取33316事件/16536ID、388份既往结论与任务/三技能/README/初始16具体配置。初始16已有11正式补测与5原始freqtradeZIP真实证据，旧false字段及全部历史保留。完整规则/参数/市场/时间/原值权重父图查重，只有本轮新时间边界构成新配置；同族不排除，不按别名或数字格式伪造新配置。31个金融/数据/账户根源首reserve前绑定，旧源函数体与四账户保持；旧年度6项只读不重算、不改状态。

输入2026-09-21 UTC00:00起，33完整日预热；OOS为2026-10-24 UTC00:01到2026-11-11 UTC00:01，共18连续日，6个顺序3日折，折间保留真实q/cash，无训练/标签/拟合，purge/embargo不适用。Nov11仅2个闭合终点分钟，不使用未完整当日日线作信号/成本。这个后续历史已被其他原账户部分观察，不是未触碰最终测试集或独立前向。18日年化Sharpe/Calmar非常不稳定，不能替代180日门槛。

真实数据：每币73442闭合分钟、1224闭合mark小时、154笔全输入资金费，其中OOS54笔，数量取自官方实际响应，不硬假定8小时。Oct25之前复用原真实缓存，之后核验190个既有候选原包、1582个原HTTP gzip SHA（185个包用于合成），保留原检索UTC。发现每币47小时mark和5笔资金费缺口后，分别2次官方GET取得47个闭合小时和完整54笔OOS真实fundingTime/rate/mark；不生成或插值行情、不跨缺口估值。两次实际dataset退出1及源版本/覆盖诊断/重试0均保存，均发生于首reserve及收益计算前。cohort_inputs.json保存完整来源及数据哈希，4个新增公共原始响应轻量压缩保留。

固定规则：BTC L29/H3%/E1%带缓冲有符号动量；ETH L5/H2%反转/E0.75%，有限归一化EWM S16 beta15/17、同宽3日前斜率严格K0.75%，只门控新开/反手，同向留实际q。预设价格样本logvol V={5,6,7}日、阈值5.625%；资金费预算样本logvol VW={8,10,12}日，最近4笔signed成熟真实费率中位数（偶数中间两项平均），结算年龄1–36h、available≤signal，budget=min(.0002,.00875*pastVWvol*latesteligible实际间隔小时/24)。保守1小时可用是建模假设，不是历史到达证明。代表V6/VW10事前固定，结果后不换代表/不增格/不弱化门控。

新实验银行BTC3750/N1000、ETH15000/N4000，总本金18750 USDT。raw[1,1]加完整银行，20/80只是本金描述，权重不归一化、不二次缩放NAV、不转账/父订单/再平衡/共享保证金。独立冷启动只属于本轮研究cohort，不触碰四个原账户；q=floor(N/前完整日close/LOT)*LOT，下一UTC00:01原生OPEN不利tick成交，反手先平，终点成本平仓。父项按共同因果事件时间轴合计NAV，直接算全路径DD，不平均子Sharpe。

1/2/3倍成本已实际计算：每边fee5bp+halfspread1bp+slip2bp+impact=.5*过去20完整日样本logvol*sqrt(真实absq*OPEN/过去20完整日quoteADV)。执行成本与资金费支出随压力倍增，正资金费收入不放大。线性永续含真实资金费，无现货借币；LOT/tick/minnotional、参与率≤0.1%、费后1倍抵押、闭合mark小时不利high/low的1%保证金代理逐曲线核验。缺L2/TCA、完整历史风险档位和tick强平证据，不能证明容量。

冻结失败标准：控制项不可晋级；各成本全期净正、各成本至少4/6盈利3日折、3倍整体DD≤25%、局部3倍正收益与4/6折条件比例各≥60%、底层至少4次平仓、毛价格PnL加净资金费/1倍执行成本≥2.5、无抵押/拒单/保证金代理违规、终点flat、至少180日及真正独立前向。18日及已观察回溯必然不满足末两项；候选仅1次底层平仓也失败。局部条件通过不等于ETH参数敏感性已可识别。

|配置|范围|V/VW|1x净%|2x净%|3x净%|3x完整DD%|3x正折/6|3x成交/平仓|状态及失败|
|---|---|---|---:|---:|---:|---:|---:|---|---|
|later18_BTC_momentum|component|None/None|2.439390|2.399639|2.359890|1.661332|4|2/1|rejected:four_underlying_native_closes1,minimum180days,genuine_independent_prospective_validation|
|later18_ETH_V5_VW8|component|5/8|0.000000|0.000000|0.000000|0.000000|0|0/0|rejected:positive_all_costs,four_of_six_positive3d_folds_allcost,local_positive3_gte60pct,local_four_of_six_allcost_gte60pct,four_underlying_native_closes1,gross_plus_funding_to_cost1_gte2_5,minimum180days,genuine_independent_prospective_validation|
|later18_ETH_V5_VW10|component|5/10|0.000000|0.000000|0.000000|0.000000|0|0/0|rejected:positive_all_costs,four_of_six_positive3d_folds_allcost,local_positive3_gte60pct,local_four_of_six_allcost_gte60pct,four_underlying_native_closes1,gross_plus_funding_to_cost1_gte2_5,minimum180days,genuine_independent_prospective_validation|
|later18_ETH_V5_VW12|component|5/12|0.000000|0.000000|0.000000|0.000000|0|0/0|rejected:positive_all_costs,four_of_six_positive3d_folds_allcost,local_positive3_gte60pct,local_four_of_six_allcost_gte60pct,four_underlying_native_closes1,gross_plus_funding_to_cost1_gte2_5,minimum180days,genuine_independent_prospective_validation|
|later18_ETH_V6_VW8|component|6/8|0.000000|0.000000|0.000000|0.000000|0|0/0|rejected:positive_all_costs,four_of_six_positive3d_folds_allcost,local_positive3_gte60pct,local_four_of_six_allcost_gte60pct,four_underlying_native_closes1,gross_plus_funding_to_cost1_gte2_5,minimum180days,genuine_independent_prospective_validation|
|later18_ETH_V6_VW10|component|6/10|0.000000|0.000000|0.000000|0.000000|0|0/0|rejected:positive_all_costs,four_of_six_positive3d_folds_allcost,local_positive3_gte60pct,local_four_of_six_allcost_gte60pct,four_underlying_native_closes1,gross_plus_funding_to_cost1_gte2_5,minimum180days,genuine_independent_prospective_validation|
|later18_ETH_V6_VW12|component|6/12|0.000000|0.000000|0.000000|0.000000|0|0/0|rejected:positive_all_costs,four_of_six_positive3d_folds_allcost,local_positive3_gte60pct,local_four_of_six_allcost_gte60pct,four_underlying_native_closes1,gross_plus_funding_to_cost1_gte2_5,minimum180days,genuine_independent_prospective_validation|
|later18_ETH_V7_VW8|component|7/8|0.000000|0.000000|0.000000|0.000000|0|0/0|rejected:positive_all_costs,four_of_six_positive3d_folds_allcost,local_positive3_gte60pct,local_four_of_six_allcost_gte60pct,four_underlying_native_closes1,gross_plus_funding_to_cost1_gte2_5,minimum180days,genuine_independent_prospective_validation|
|later18_ETH_V7_VW10|component|7/10|0.000000|0.000000|0.000000|0.000000|0|0/0|rejected:positive_all_costs,four_of_six_positive3d_folds_allcost,local_positive3_gte60pct,local_four_of_six_allcost_gte60pct,four_underlying_native_closes1,gross_plus_funding_to_cost1_gte2_5,minimum180days,genuine_independent_prospective_validation|
|later18_ETH_V7_VW12|component|7/12|0.000000|0.000000|0.000000|0.000000|0|0/0|rejected:positive_all_costs,four_of_six_positive3d_folds_allcost,local_positive3_gte60pct,local_four_of_six_allcost_gte60pct,four_underlying_native_closes1,gross_plus_funding_to_cost1_gte2_5,minimum180days,genuine_independent_prospective_validation|
|later18_BTC_hold|benchmark_component|None/None|-2.519021|-2.663482|-2.807944|3.135809|2|2/1|rejected:not_a_benchmark_control,positive_all_costs,four_of_six_positive3d_folds_allcost,four_underlying_native_closes1,gross_plus_funding_to_cost1_gte2_5,minimum180days,genuine_independent_prospective_validation|
|later18_ETH_hold|benchmark_component|None/None|-3.833469|-3.940377|-4.047176|4.894883|2|2/1|rejected:not_a_benchmark_control,positive_all_costs,four_of_six_positive3d_folds_allcost,four_underlying_native_closes1,gross_plus_funding_to_cost1_gte2_5,minimum180days,genuine_independent_prospective_validation|
|later18_parent_V5_VW8|candidate|5/8|0.487878|0.479928|0.471978|0.336860|4|2/1|rejected:four_underlying_native_closes1,minimum180days,genuine_independent_prospective_validation|
|later18_parent_V5_VW10|candidate|5/10|0.487878|0.479928|0.471978|0.336860|4|2/1|rejected:four_underlying_native_closes1,minimum180days,genuine_independent_prospective_validation|
|later18_parent_V5_VW12|candidate|5/12|0.487878|0.479928|0.471978|0.336860|4|2/1|rejected:four_underlying_native_closes1,minimum180days,genuine_independent_prospective_validation|
|later18_parent_V6_VW8|candidate|6/8|0.487878|0.479928|0.471978|0.336860|4|2/1|rejected:four_underlying_native_closes1,minimum180days,genuine_independent_prospective_validation|
|later18_parent_V6_VW10|candidate|6/10|0.487878|0.479928|0.471978|0.336860|4|2/1|rejected:four_underlying_native_closes1,minimum180days,genuine_independent_prospective_validation|
|later18_parent_V6_VW12|candidate|6/12|0.487878|0.479928|0.471978|0.336860|4|2/1|rejected:four_underlying_native_closes1,minimum180days,genuine_independent_prospective_validation|
|later18_parent_V7_VW8|candidate|7/8|0.487878|0.479928|0.471978|0.336860|4|2/1|rejected:four_underlying_native_closes1,minimum180days,genuine_independent_prospective_validation|
|later18_parent_V7_VW10|candidate|7/10|0.487878|0.479928|0.471978|0.336860|4|2/1|rejected:four_underlying_native_closes1,minimum180days,genuine_independent_prospective_validation|
|later18_parent_V7_VW12|candidate|7/12|0.487878|0.479928|0.471978|0.336860|4|2/1|rejected:four_underlying_native_closes1,minimum180days,genuine_independent_prospective_validation|
|later18_matched_hold_parent|benchmark|None/None|-3.570579|-3.684998|-3.799329|4.446533|2|4/2|rejected:not_a_benchmark_control,positive_all_costs,four_of_six_positive3d_folds_allcost,four_underlying_native_closes1,gross_plus_funding_to_cost1_gte2_5,minimum180days,genuine_independent_prospective_validation|


预设代表 00e3500ae4809154c6213b9e7c20082c1bc66e15f37d6e9d71452887a08f0e2d，三成本净收益分别 0.487877953%/0.479927870%/0.471977928%；三成本各4/6正折。三倍6折依次 0.055503627%/0.150274601%/-0.031965229%/-0.133467281%/0.305267333%/0.126021341%，完整回撤按连续事件NAV核算，保留跨折峰值。逐配置/逐成本/逐折见cost_scenes.csv、walk_forward_folds.csv及results完整NAV。

敏感性实际执行9个ETH及9个父项×三成本，保存27+27网格行、72相邻边。独立政策审计显示每个ETH有11个未门控非零目标，但固定趋势门控后全零；价格与资金费入场筛选各0次触发，故这18日不能区分V/VW，更无稳健平台或独立alpha证据。完整三成本父路径仅1条。inactivity_attribution.json与NAV_alias_inventory.json分别保存归因/同时间完整路径比对；旧年度不同日历不拿来冒充同路径匹配。

匹配持有同C/N/原权重/新日历/成本真实执行，1/2/3倍净收益-3.570579005%/-3.684998307%/-3.799329302%，3倍DD4.446533%；现金0%。27项匹配比较完整保存。未将旧370日持有收益与本18日称匹配，控制项不因正负收益改变其不可晋级含义。

独立审计36新原生曲线与30新父项，648政策决策、1944资金费行、18成交、462指标和4356保证金代理检查，0拒单；Fraction/Horner政策、Decimal/LOT/成本/资金费/cash、完整时间轴/6折/全路径DD独立重建，不调用simulate/decide/trade。36数量成本合成例、27完整ETH政策例（18个活跃筛选）、18日6折/跨折DD25%已知合成例均通过；9个刻意错误合成变体实际退出1，检出未来信号/预算/价格、总体方差、固定N、线性冲击、重复权重、折重置及错误天数，均早于绑定/reserve。无虚构真实市场RED。报告SHA256=2b7473d11bc91075611cc08508297934128774d88c15d4f0ab7f8ac2b2a6d134。

原四账户本轮固定窗口：SMA/single Nov11_18:30→20:30，L4/FEWM20:10→22:10，全部只闭合分钟mark/小时风险、0新资金费/日决策/成交。18个永续book的cash/q/entry完全保持，Nov11_16各资产/成本三条完整链各只结算一次。原Nov11_16字段检索UTC 2026-11-11T17:33:47.232608Z，不当成本轮新结算或新GET，不提前跨Nov12_00入账，不采用本轮cohort或参数。

SMA完整NAV前缀58751→58871，各9成本场景独立核验。

single完整NAV前缀23230→23352，各9成本场景独立核验。

L4完整NAV前缀15967→16089，各9成本场景独立核验。

FEWM完整NAV前缀10075→10197，各9成本场景独立核验。

SMA原Float、1500/500本金及冻结规则保持，三倍累计−7.468958%、cashflat；权威65个SPOT闭合日仍032206到Nov11 UTC00:00，当前分钟数组不得替代。全部是延迟闭合数据shadow，独立于paper10真实公开报价模拟；partial观察淘汰不取消原180日计划。

下轮SMA/single 2026-11-11T20:30:00Z→2026-11-11T22:30:00Z只mark/risk；L4/FEWM 2026-11-11T22:10:00Z→2026-11-12T00:10:00Z真正跨UTC00资金费及00:01日决策，参考分钟必须在Nov12_00:11后闭合。先取真实新BTC/ETH fundingTime/rate/mark及实际毫秒和原检索UTC，再按各自原q/cash/context独立登记/计算；不可拿Nov11_16或Nov11_00替代。当前墙钟到Nov12不授权跳过本账户固定窗口或提前多观察一窗。SMA仅当其自有窗口跨日才取真实新65闭合日并用原daily适配器。

下轮研究未执行提案：UNEXECUTED: keep the predeclared V/VW grid and all22 new18day outcomes. Nine ETH paths have zero entries because fixed trend gate blocked all11 fast nonzero days; price and funding horizon sensitivity is not identified. Do not densify V/VW or weaken gate after seeing this cohort. Next research may inspect one genuinely different predeclared direction after full registry/default/numeric/parentgraph lookup, or collect sufficiently long later real data; reuse existing fullbankNAV for exact matching combinations. Preserve six older annual references and all four original accounts, never adopt/reset/forceclose. No next configuration/reserve/evaluation this round.

监控生成并原生检查通过，10430研究配置、旧10408完整字典保持，paper10=10账户/336观察；只读已有报告，无新回测/成交/部署/任务。原账户公共传输实际失败2次，原始响应/失败/stderr保存；本轮另4次真实数据缺口GET均200。失败数据准备未启动收益计算，全部失败原生证据保持。

本轮保留实际结果/spec/完整账户/冻结规则/登记、数据代码哈希、必要原始响应、原生argv/cwd/UTC/退出码、复现和下轮状态；无可重建npy/tmp/pycache。main提交push后核对ref/全tree/必要blob及三条完整账户链再释放锁；真实终态保存在.git/automation_proofs/20261111T232947Z.json。

格式检查原生失败已留档：首reserve前冻结的period_summary.py末尾多一个空行，完整默认检查只有该唯一诊断。保持金融源哈希，不改已执行代码；精确核验原诊断后仅关闭blank-at-eof格式规则，其余默认空白检查继续执行。原失败gzip、实际退出码和例外SHA均保存，不涉及估值或账户重跑。
