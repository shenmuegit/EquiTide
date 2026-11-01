# 单次滞后资金费入场过滤验证

完整读取25314登记事件/12535ID、268份结论，初始16项真实证据齐全。本轮L3/4/5×资金费支付率上限F=0/1bp/OFF；OFF三个原生/三个父格点和匹配持有父及来源共10唯一旧定义只读。6个新ETH组件+6个新组合、36成本场景，均先逐个reserve成功再实际计算并finish；全部正负结果保存。

经济假设：最近已可得资金费的支付方向或反映拥挤，避免新开付费方向可能减少拖累，但也可能损失有利价格走势。历史已有六次结算均值、E−1%、多数慢门、无V10等配置；本轮最近1次、E+0.25%、始终slow28/V10与资金配置不同，精确查重后允许新测试。未把family相同视为重复。

Predeclared last-available funding payment cap may avoid entering crowded paying sides, but may miss profitable trends/reversals and does not predict next funding. L3/4/5 crossed with F0/1bp/OFF; current positive exit buffer/single28alwaysgate/V10 differ from old six-settlement-mean/negative-exit/majoritygate studies. Six fresh ETH paths and six unchanged-bank parents; OFF sources readonly. Both actual funding accounting and normalized+extra1h historical availability modeled explicitly. Reused development history, not independent final OOS; no outcome-driven extra tests.

完整价格规则：ETH快ROC=C[i−1]/C[i−1−L]−1，L3/4/5、H2.5%；严格>H空、<−H多，带内实际多仅ROC<0.25%、实际空仅ROC>−0.25%保留，等号退出。绝对slow28方向不匹配始终退出；当前V10样本logvol>4.5%只过滤新开/翻向。之后仅非零且与实际持仓方向不同的desired才检验direction×历史realized_rate<=F，F0/0.0001，按每次结算原率不是年化/本金/权重；同向保留和必须退出不受资金费门控阻止。OFF=None完全等价旧规则，不查资金费信号。无BTC收益控制或连续确认。

特征从1212条完整真实历史选最新settlement，要求settlement<=当日00且available+3600秒<=00、源年龄<=16h；空缺/过期则blocked，不补0。normalized available本来为settlement+1小时，再加固定1小时，合计保守2小时模型延迟，不是官方标准或已验证的历史网络到达；00刚结算费率不得进入00信号。历史费率不预测/保证下一结算成本。实际未来资金费依每次真实settlement/rate/mark/当时q记账，信号费率不随1/2/3成本压力放大。

BTC独立银行原ROC31/H4%/E1%真实3750本金/N375路径只读；ETH15000本金/N4500，按前完整ETHclose除以LOT向下取整，下一00:01原生OPEN不利tick，翻向先平后开，终止成本平仓。原[1,1]是两完整银行美元NAV相加，总本金18750；20%/80%只是初始份额，不再次乘权重，不归一化、父调仓、转账、跨抵押、NAV复利或线性缩放旧路径。

真实区间2025-10-19UTC00:01至2026-10-24UTC00:01连续370天、12完整30日折+10日尾段，现金/q/成本跨折保持，近期40天继承day330/8×5天。固定无训练/标签，purge0、预热30+间隔3；信号、ADV/logvol与资金费源严格遵守过去可得性。该历史已反复开发，全部试验计数见context，不称未触碰最终OOS/DSR/PBO显著性或独立未来资格。

失败门槛预先不变：每成本全年净正、1倍>=9/12正完整月；每成本近期净正且>=6/8正5日折；3倍全曲线DD<=25%；L/F索引半径1含中心的局部3倍净正与严格近期支持均>=60%；>=4平仓、毛参考PnL加fund/执行成本>=2.5、零拒单/负抵押/小时维护代理违规、终止flat且>=180天。原生和父分别判断，旧OFF原资格/报告/敏感性不改，只另列当前邻域诊断。

成本每边5bp费用、1bp半价差、2bp滑点、0.5×past20ETH原生样本logvol×sqrt(实际q×OPEN/past20完整quoteADV)冲击，不因过滤缩小成本假设；实际资金费支出1/2/3倍、正收入不放大。原生LOT/tick/minnotional、参与率<=0.001、费用后1倍入场抵押、各银行独立1%闭合小时不利mark维护代理。线性永续无现货借币，不虚构借币费；没有L2/TCA/完整历史阶梯/逐tick清算或容量/实盘证明。匹配本金/初始N持有和现金0%另列，非满仓或同风险持有。

|新配置|范围|L|F每次结算|1倍净%|2倍净%|3倍净%|3倍整体DD%|正月/12|近期正折1/2/3倍|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|fundscreen370_ETH_L3_F0bp_H250_E025_V10|native|3|0bp|10.122137|9.033938|7.945913|3.515464|7|4/4/4|rejected|
|fundscreen370_ETH_L3_F1bp_H250_E025_V10|native|3|1bp|12.008510|10.435455|8.861827|3.975470|9|5/4/4|rejected|
|fundscreen370_ETH_L4_F0bp_H250_E025_V10|native|4|0bp|13.205486|12.171032|11.136958|3.115257|9|4/4/4|rejected|
|fundscreen370_ETH_L4_F1bp_H250_E025_V10|native|4|1bp|13.233099|11.725876|10.218842|3.979750|10|5/5/5|rejected|
|fundscreen370_ETH_L5_F0bp_H250_E025_V10|native|5|0bp|7.649509|6.759373|5.869693|3.516294|8|2/2/2|rejected|
|fundscreen370_ETH_L5_F1bp_H250_E025_V10|native|5|1bp|9.907072|8.501373|7.096215|4.899742|10|3/3/3|rejected|
|fundscreen370_parent_L3_F0bp_H250|parent|3|0bp|8.732588|7.769772|6.807097|2.975883|9|6/6/6|passed|
|fundscreen370_parent_L3_F1bp_H250|parent|3|1bp|10.241686|8.890985|7.539829|3.305465|10|6/6/6|passed|
|fundscreen370_parent_L4_F0bp_H250|parent|4|0bp|11.199268|10.279447|9.359933|2.625006|11|6/6/6|passed|
|fundscreen370_parent_L4_F1bp_H250|parent|4|1bp|11.221358|9.923322|8.625440|3.310960|11|6/6/6|passed|
|fundscreen370_parent_L5_F0bp_H250|parent|5|0bp|6.754486|5.950119|5.146121|2.825673|10|5/5/5|rejected|
|fundscreen370_parent_L5_F1bp_H250|parent|5|1bp|8.560537|7.343720|6.127339|3.846302|11|4/4/4|rejected|

新父候选4历史通过、2淘汰。全新配置失败原因{'fundscreen370_ETH_L3_F0bp_H250_E025_V10': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fundscreen370_ETH_L3_F1bp_H250_E025_V10': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fundscreen370_ETH_L4_F0bp_H250_E025_V10': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fundscreen370_ETH_L4_F1bp_H250_E025_V10': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fundscreen370_ETH_L5_F0bp_H250_E025_V10': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fundscreen370_ETH_L5_F1bp_H250_E025_V10': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fundscreen370_parent_L3_F0bp_H250': [], 'fundscreen370_parent_L3_F1bp_H250': [], 'fundscreen370_parent_L4_F0bp_H250': [], 'fundscreen370_parent_L4_F1bp_H250': [], 'fundscreen370_parent_L5_F0bp_H250': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fundscreen370_parent_L5_F1bp_H250': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct']}。所有负收益/负期间同样留档，不按全年收益放宽近期或邻域门槛。

同L/同资金OFF对照：6/12个新配置三成本完整NAV哈希完全相同，详细匹配在equivalent_realized_NAV_paths.json。新参数不等于新独立alpha，不重跑旧组件或据路径相同删结果/改资格。

11CSV保存36场景、逐月/尾折/近期折、每日NAV、两张完整9格敏感性、72相邻边、持有/现金、旧来源及原分配；完整NAV哈希及必要逐笔/funding/状态段与父源哈希可独立重建。两面八指标图、Sharpe正比例/多指标/边界/描述性2std悬崖不等于统计显著性，不按结果扩展本批阈值。CSV资金费率以0、0.0001和空值None=OFF表达，图用0bp/1bp/OFF。

合成TDD旧代码不能阻止已知付费新多仓，预期红灯后验证多/空支付符号、阈值等号、available+extra1h等号、未来费率扰动、持仓保留/退出/失败翻向/OFF恒等。独立Fraction审计从原历史按时刻重新选择来源并验证信号最大可得性；Decimal重建实际现金/数量/成本/资金费/全NAV，不调用simulate/decide/trade重跑。

原SMA/singleS28冻结账户续18:30至20:30，独立未过滤L4/H2续20:10至22:10且22:11参考闭合后采集；保留完整cash/q/desired/risk/NAV前缀、16已计资金费不重记。新funding筛选不注入原账户，partial rejected继续长期原计划，延迟shadow不当十策略真实报价成交。

一手来源2026-11-01实际复查：[Binance官方资金费历史API](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)。原率/settlement/mark有真实哈希，官方文档没有证明历史网络发布延迟或本策略收益，availability模型假设单列primary_sources和funding_data_availability。

同main排他锁内登记/汇总/提交；监控只读既有账户与报告，不产生成交、不改冻结规则/本金/持仓，不部署网页/建定时任务，不下真实订单。

历史通过范围：4个新父定义达到原门槛；仅L3/F0和L4/F0改变实际净值路径。其3倍净收益6.807097%/9.359933%，整体DD2.975883%/2.625006%，正完整月9/12与11/12，各成本近期均6/8、局部严格支持100%与2/3。另2个通过F1bp父与OFF三成本全NAV完全相同；6个新原生组件及2个L5组合淘汰。

效应与局限：1bp整列6配置全成本NAV等价OFF，不能计作独立alpha。9父格点只有6个不同三成本路径元组、其中4个满足严格近期；仍不是独立市场样本。L4/F0提高2/3倍净收益并降低DD，但1倍净收益略低于OFF；L3/F0各成本净收益均低于OFF，所以两者均未在每成本同时提升收益和降低DD。边界峰值/全局描述性悬崖、重复历史和归一化资金费可得延迟模型限制保留。仅待独立前向，不采用到原账户、不创建新账户或定时任务。

工程事实：只读补充统计误将旧决策schema当成新policy_audit，实际KeyError已留档；修复为仅对新原生读取资金费特征，原报告/资格/账务不改，金融与完成观察均零重跑。恢复统计核对新19980资金费/852成交及6660特征引用，114个意图被规则过滤而非拒单；旧来源19980资金费/618成交单列。

资金与权重：BTC实际本金3750USDT、固定入场名义375，ETH本金15000、固定名义4500；原权重[1,1]代表两份完整独立银行，总本金18750。20%/80%只是资金份额，不再次乘权重；初始名义预算合计4875即26%本金。资金费上限F仅作用于新开/翻向资格，不减少任何实际ETH费用/波动冲击/数量/未来资金费或抵押约束。按同一真实时间轴美元净值相加，不归一化、不线性缩放旧净值、不设父调仓、资金转移或跨账户抵押。

封存：12个新配置已逐一finish，其中新父历史通过4，淘汰2。新父3倍370日净收益5.146121%至9.359933%，整体DD2.625006%至3.846302%。实际逐配置失败原因见上表及report；全年正收益不能替代近期和邻域门槛。本轮严格近期父6/9、原生0/9；旧OFF原资格保留，不称当前全域稳健。

独立审计通过：19620468完整新NAV点、6660决策；核算计数{'funding': 39960, 'fills': 1470, 'rejects': 0, 'metric_checks': 756, 'margin_checks': 131280}。计数范围包含只读旧来源及新原生；research_evidence_counts.json分别统计新/旧资金费和成交，父只引用同源交易不新增成交。不调用simulate/decide/trade做金融重跑。24057个旧保护文件字节相同，21新ID/42条追加事件完整。

原SMA65续至2026-11-01T20:30:00Z：44341旧NAV+120=44461，累计44429分钟；无新日决策/成交。原singleS28续2026-11-01T18:30:00Z至2026-11-01T20:30:00Z，NAV8622，累计观察ID213；本窗真实funding[]，6正时长小时风险检查、零违规。

独立未过滤L4/H2续2026-11-01T20:10:00Z至2026-11-01T22:10:00Z，仅参考分钟闭合后采集；NAV1359，累计1329分钟/36ID。本窗funding[]、6正时长风险检查、零违规；16资金费现金不重复，完整原cash/q/desired/risk/NAV前缀保持，研究资金费过滤不注入原账户。三份部分观察均继续长期冻结计划。

监控只读汇总通过：8968研究行，8956旧行完整字典相同，10固定报价账户/216既有观察；gzip4054956字节，现有5MB预算保持。可确认HTTP/传输失败0次，候选/L4逐次原始响应与SMA真实stderr均按本轮实际保留；未被原传输器逐次输出的失败响应体不补造，具体失败来源见failure_receipts。本轮预期TDD红灯及其余真实工具/传输失败回执分别保留；不继承上轮失败为本轮事实，无金融/完成观察重跑。

清理42138字节可重建语义查重材料，原哈希和复现命令留档；金融结果/完整账户账本删除0。全部轻量证据、必要代码、状态、真实响应及数据哈希保留。main提交/非强制push及完整远端核验、真实进程终态和解锁证明在.git/automation_proofs/20261101T215620Z.json。
