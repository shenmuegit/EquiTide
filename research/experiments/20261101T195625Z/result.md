# BTC控制的ETH反向信号验证

完整读取25252登记事件/12504ID、267份历史结论；初始16项真实结果证据齐全。预设L3/4/5×A0/0.5/1，A0三格原生和三格父及匹配持有父/来源共10个旧定义只读。A0.5/A1新增6个ETH组件和6个BTC/ETH组合、36个成本场景，每个配置先reserve成功后计算并独立finish。

经济假设：用BTC同期已实现收益控制ETH短窗收益中的共同市场成分，可能改善反向信号，也可能移除有用反转信息。固定系数不拟合，不在本轮结果上再选择网格。上一轮连续确认不注入本机制。

Predeclared BTC return control x=rETH_L-A*rBTC_L may remove common crypto movement from ETH reversal signals, while potentially removing useful market reversal information. Fixed A0/.5/1 crossed with L3/4/5; A0 raw-return sources readonly, A.5/A1 produce six fresh ETH native models and six unchanged-bank parents. No fitted beta or market-neutral hedge claim; all costs and quantities remain actual native. Historical 370d data reused after prior confirmation weakness, not untouched final OOS. No outcome-driven extra tests.

完整规则：两币L日简单收益r=C[i-1]/C[i-1-L]−1，x=rETH−A*rBTC，L=3/4/5、A=0/0.5/1；x>2.5%空、x<−2.5%多。带内实际多仅x<0.25%、实际空仅x>−0.25%保留，等号退出；ETH绝对28日slow方向不匹配始终退出，当前ETH10日样本logvol>4.5%只阻止新入场/翻向。同向保留不重置q，反向先平再开。A只控制信号，不改变资金权重或数量，不创建BTC对冲订单，不声称市场中性。

两币完整分钟open时间轴和日close索引对齐；信号可得时间取两币真实available最大值，只使用此前已完成日线，之后下一UTC00:01原生OPEN执行。ETH按原生LOT从固定名义预算4500/前日ETHclose向下取整，费用和funding均使用实际ETHq；BTC独立组件原ROC31/H4%/E1%原生3750本金/375名义路径只读复用。ETH本金15000，原权重[1,1]代表两份完整银行，美元净值相加，总本金18750，资金份额20%/80%不再次乘权重、不归一化。无父调仓、转账、线性NAV缩放或跨抵押。

真实边界2025-10-19UTC00:01至2026-10-24UTC00:01，连续370天、12完整30天折加10天尾段；状态/现金/q/成本跨折不重置，day330继承近期40天/8×5天。固定无训练标签，purge0、30日预热加3日间隔；所有价格/quoteADV/logvol当时已可得。反复开发历史及全部试验数量在context，不能称未触碰最终测试；局部比例没有消除多重选择偏差，未声称DSR/PBO显著性。

失败判据预固定：每档全年净正、1倍>=9/12正完整月；每档近期净正且>=6/8正5日折；3倍整体DD<=25%；L/A索引半径1含中心局部3倍净正和严格近期支持均>=60%；>=4平仓、毛参考PnL加fund/执行成本>=2.5，零拒单/负抵押/维护代理违规，终止flat、至少180天。原生与父分别判定；旧A0的canonical资格/原敏感性/报告不改，仅另列当前邻域诊断。

费用每边5bp、半价差1bp、滑点2bp、冲击0.5×过去20日样本logvol×sqrt(实际q×OPEN/过去20完整日quoteADV)，1/2/3倍压力；真实funding纳秒/rate/mark/当时q，支出倍增、正收入不放大。原生LOT/tick/minnotional、参与率<=0.001、费用后1倍入场抵押、独立银行1%闭合小时不利mark维护代理。线性永续不需要现货借币，不虚构借币费；无TCA/L2、完整历史档位/逐tick清算或容量证明。匹配本金/初始N持有与现金0%为对照，非满仓或同风险持有。

|新配置|范围|L|A|1倍净%|2倍净%|3倍净%|3倍整体DD%|正月/12|近期正折1/2/3倍|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|btccontrol370_ETH_L3_A50_H250_E025_V10|native|3|0.5|8.076955|6.961069|5.844859|3.562196|8|3/3/3|rejected|
|btccontrol370_ETH_L3_A100_H250_E025_V10|native|3|1|6.763157|5.840634|4.917776|3.828647|9|2/2/1|rejected|
|btccontrol370_ETH_L4_A50_H250_E025_V10|native|4|0.5|5.774327|4.631900|3.489770|5.934659|9|3/3/3|rejected|
|btccontrol370_ETH_L4_A100_H250_E025_V10|native|4|1|13.434526|12.471529|11.508817|3.825853|7|2/2/2|rejected|
|btccontrol370_ETH_L5_A50_H250_E025_V10|native|5|0.5|5.926615|4.801977|3.677579|4.958376|8|1/1/1|rejected|
|btccontrol370_ETH_L5_A100_H250_E025_V10|native|5|1|10.664090|9.736477|8.809206|4.841131|7|2/2/2|rejected|
|btccontrol370_parent_L3_A50_H250|parent|3|0.5|7.096443|6.111477|5.126254|2.966074|10|5/5/5|rejected|
|btccontrol370_parent_L3_A100_H250|parent|3|1|6.045405|5.215128|4.384588|3.067892|9|4/4/4|rejected|
|btccontrol370_parent_L4_A50_H250|parent|4|0.5|5.254340|4.248141|3.242183|5.089343|10|5/5/5|rejected|
|btccontrol370_parent_L4_A100_H250|parent|4|1|11.382500|10.519844|9.657420|3.208895|8|4/4/4|rejected|
|btccontrol370_parent_L5_A50_H250|parent|5|0.5|5.376171|4.384203|3.392430|3.878925|10|3/3/3|rejected|
|btccontrol370_parent_L5_A100_H250|parent|5|1|9.166151|8.331803|7.497732|3.952692|9|3/3/3|rejected|

新父候选：0历史通过、6淘汰。所有新配置失败原因：{'btccontrol370_ETH_L3_A50_H250_E025_V10': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btccontrol370_ETH_L3_A100_H250_E025_V10': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btccontrol370_ETH_L4_A50_H250_E025_V10': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btccontrol370_ETH_L4_A100_H250_E025_V10': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btccontrol370_ETH_L5_A50_H250_E025_V10': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btccontrol370_ETH_L5_A100_H250_E025_V10': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btccontrol370_parent_L3_A50_H250': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btccontrol370_parent_L3_A100_H250': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btccontrol370_parent_L4_A50_H250': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btccontrol370_parent_L4_A100_H250': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btccontrol370_parent_L5_A50_H250': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btccontrol370_parent_L5_A100_H250': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct']}。所有负收益/负期间保存，不放宽门槛或按新结果增加其他系数。

11CSV保存全部36成本场景、逐完整月和尾段、近期5日折、每日NAV、原生/父完整9格敏感性、72相邻边、匹配持有/现金、旧来源与原资金分配。完整NAV SHA及必要逐笔/资金费/状态段/父来源哈希支持独立重建。多指标与描述性2std悬崖不等于统计显著性；最大值在边界如实标明，不自动扩展本批。

合成TDD旧代码不能在A1抵消两币共同变化，预期红灯留档；新实现验证残差Fraction、两方向/等号/slow门控/保留/退出/A0恒等和两币未来扰动。实际独审直接读取BTC原数据独立计算信号和两币可得时间最大值，不借用策略decide。

冻结原SMA/singleS28按原cash/q/desired/risk/全NAV续16:30至18:30，独立未过滤L4/H2续18:10至20:10且20:11参考分钟闭合后采集；16资金费已实际计入，不能重记。原规则/本金/终止计划不改，本轮A不注入原账户；部分观察rejected不取消长期计划，延迟shadow不作十策略实盘报价成交。

一手来源于2026-11-01复查：[Binance官方市场数据文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)；接口版本/字段见primary_sources，文档样例不作行情证据，实际Parquet/API字节和SHA单独核验。

全程同main排他锁；监控只读既有报告和账户，不产生成交，不改冻结规则/本金/持仓，不重部署网页或建定时任务，不下真实订单。

资金与权重：BTC实际本金3750USDT、固定入场名义375，ETH本金15000、固定名义4500；原权重[1,1]代表两份完整独立银行，总本金18750。20%/80%只是资金份额，不再次乘权重；初始名义预算合计4875即26%本金。控制系数A只作用于信号，原生ETH波动成本、数量、资金费和抵押约束均未按A缩小。按同一真实时间轴美元净值相加，不归一化、不线性缩放旧净值、不设父调仓、资金转移或跨账户抵押。

封存：12个新配置已逐一finish，其中新父历史通过0，淘汰6。新父3倍370日净收益3.242183%至9.657420%，整体DD2.966074%至5.089343%。实际逐配置失败原因见上表及report；全年正收益不能替代近期和邻域门槛。本轮严格近期父2/9、原生0/9；旧A0原资格保留，不称当前全域稳健。

独立审计通过：19620468完整新NAV点、6660决策；核算计数{'funding': 39960, 'fills': 1308, 'rejects': 0, 'metric_checks': 756, 'margin_checks': 132900}。计数范围包含只读旧来源及新原生；research_evidence_counts.json分别统计新/旧资金费和成交，父只引用同源交易不新增成交。不调用simulate/decide/trade做金融重跑。23796个旧保护文件字节相同，21新ID/42条追加事件完整。

原SMA65续至2026-11-01T18:30:00Z：44221旧NAV+120=44341，累计44309分钟；无新日决策/成交。原singleS28续2026-11-01T16:30:00Z至2026-11-01T18:30:00Z，NAV8500，累计观察ID210；本窗真实funding[]，6正时长小时风险检查、零违规。

独立未过滤L4/H2续2026-11-01T18:10:00Z至2026-11-01T20:10:00Z，仅参考分钟闭合后采集；NAV1237，累计1209分钟/33ID。本窗funding[]、6正时长风险检查、零违规；16资金费现金不重复，完整原cash/q/desired/risk/NAV前缀保持，研究BTC控制信号不注入原账户。三份部分观察均继续长期冻结计划。

监控只读汇总通过：8956研究行，8944旧行完整字典相同，10固定报价账户/215既有观察；gzip4047740字节，现有5MB预算保持。可确认HTTP/传输失败1次，候选/L4逐次原始响应与SMA真实stderr均按本轮实际保留；未被原传输器逐次输出的失败响应体不补造，具体失败来源见failure_receipts。本轮预期TDD红灯及其余真实工具/传输失败回执分别保留；不继承上轮失败为本轮事实，无金融/完成观察重跑。

清理3083字节可重建语义查重材料，原哈希和复现命令留档；金融结果/完整账户账本删除0。全部轻量证据、必要代码、状态、真实响应及数据哈希保留。main提交/非强制push及完整远端核验、真实进程终态和解锁证明在.git/automation_proofs/20261101T195625Z.json。
