# ETH 多空非对称入场阈值验证

完整读取25562事件/12659ID、272份既往结论，排除持续观察后的历史研究定义数9445。初始16项均有实际证据，无缺失回测需要重跑。本轮6个新ETH组件+6个新BTC/ETH组合、36成本场景逐项reserve后实际计算，所有正负期间与结果完整保留。

Long and short reversal entries may prefer different hurdles. Predeclare L3/4/5 x longHL2/2.5/3percent with shortHS2.5percent fixed, positiveexitbuffer.0025,S28alwaysgate,V10cap.045,ETH15000/N4500 andBTC3750/N375. SymmetricHL2.5 actualnative/parent results readonly; longHL2/3 six ETH paths and six parent sums new. Earlier jointH grids moved both sides and differ from this exact asymmetry. Changes may raise turnover or miss profitable long pullbacks; no outcome-driven extensions, no relaxed recentgates. Whole historical period repeatedly developed, not untouchedfinal OOS.

预设两轴为快回望L=[3,4,5]与多仓入场阈值HL=[0.02,0.025,0.03]，空仓阈值HS固定0.025，原return_hurdle字段表示本批固定空侧。HL=2.5%对称的三个原生/三个父、BTC和匹配持有父/两原生共10旧定义只读；其余6原生与6父为新配置。既往共同调整多空H的网格与本批不同；完整spec指纹查重，不按family排除。

完整价格规则：fastROC=C[i−1]/C[i−1−L]−1。严格r>+HS空、r<−HL多；等号不新开。其余区间，实际多仅r<E、实际空仅r>−E保留，E=+0.0025，等号退出；绝对slow28方向始终门控，不匹配退出。V10样本logvol>0.045只过滤新开/翻向。原先更早退出及实际同向数量保留不变，普通翻向先平后开。无最长持仓、慢趋势幅度门槛、BTC残差或资金费入场信号。

经济假设为多空触发条件可能偏好不同幅度，本批固定空侧以隔离多侧变化；更小HL可能增加换手，更大HL可能错失有效回撤。这是假设而非官方盈利结论，不在结果后改阈值或宽限近期/敏感性门槛。

资金与原始权重：BTC真实银行3750/N375旧ROC31/H4%/E1%曲线只读；ETH15000/N4500按原生数量/冲击/抵押重新执行。原[1,1]是两个完整银行美元NAV相加，总本金18750，初始本金份额20%/80%仅说明资金分配，不再次相乘或自动归一化。初始名义总4875=26%本金。固定N/前完整close按LOT向下取整，下一UTC00:01原生OPEN不利tick，终止平仓计成本；无父调仓、转账、跨抵押、复利调N或线性缩放旧净值。

Walk-forward区间2025-10-19UTC00:01至2026-10-24UTC00:01连续370天，12完整30日折+10日尾折；现金/数量/费用跨折不重置，全分钟/事件NAV计算整体回撤。近期40天继承day330与8×5日折。固定规则无拟合/标签，purge0、预热30+间隔3，ADV/波动仅前20完整日。历史经过大量反复开发，多重试验数保留，不称未触碰最终留出、独立未来或DSR/PBO显著性。

1/2/3倍成本每边5bp手续费、1bp半价差、2bp滑点、0.5×past20样本logvol×sqrt(实际q×OPEN/past20完整quoteADV)冲击。真实资金费按每次settlement/rate/mark/heldq入账，支出倍增而正收入不放大。原生LOT/tick/minnotional、参与率<=0.001、费用后1倍抵押、各银行独立1%闭合小时不利mark维护代理均审核。线性永续不需现货借币，不虚构借币费；缺L2/TCA/完整历史档位/逐tick清算或容量证明。匹配本金与初始N持有及现金0%并列，非满仓或等风险持有。

预先不变的失败门槛：每成本全年净正，1倍>=9/12正完整月；每成本近期净正且>=6/8正5日折；3倍整体DD<=25%；L/HL索引半径1含中心邻域的3倍净正及严格近期支持均>=60%；>=4平仓，毛参考价格PnL加fund/执行成本>=2.5；零拒单、负抵押、小时维护代理违规，终止flat且>=180天。新原生和父各自判断，对称旧结果不改资格，仅新增当前邻域诊断。

|新配置|范围|L|多仓HL|1倍净%|2倍净%|3倍净%|3倍整体DD%|正月/12|近期正折1/2/3倍|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|asym370_ETH_L3_HL200bp_HS250_E025_V10|native|3|0.020|14.886987|13.033759|11.179670|3.975470|9|5/4/4|rejected|
|asym370_ETH_L3_HL300bp_HS250_E025_V10|native|3|0.030|11.588524|10.070981|8.552864|3.975470|9|5/4/4|rejected|
|asym370_ETH_L4_HL200bp_HS250_E025_V10|native|4|0.020|13.997903|12.376436|10.754731|4.602858|10|5/5/5|rejected|
|asym370_ETH_L4_HL300bp_HS250_E025_V10|native|4|0.030|11.984043|10.530840|9.077986|3.979750|10|5/5/5|rejected|
|asym370_ETH_L5_HL200bp_HS250_E025_V10|native|5|0.020|13.676146|12.109638|10.544002|4.899742|10|3/3/3|rejected|
|asym370_ETH_L5_HL300bp_HS250_E025_V10|native|5|0.030|9.166239|7.998060|6.830477|4.892072|10|1/1/1|rejected|
|asym370_parent_L3_HL200bp_HS250|parent|3|0.020|12.544468|10.969628|9.394103|3.305465|10|6/6/6|passed|
|asym370_parent_L3_HL300bp_HS250|parent|3|0.030|9.905698|8.599406|7.292658|3.305465|10|6/6/6|passed|
|asym370_parent_L4_HL200bp_HS250|parent|4|0.020|11.833201|10.443770|9.054152|3.813762|11|6/6/6|passed|
|asym370_parent_L4_HL300bp_HS250|parent|4|0.030|10.222113|8.967294|7.712756|3.310960|11|6/6/6|passed|
|asym370_parent_L5_HL200bp_HS250|parent|5|0.020|11.575795|10.230332|8.885569|3.846302|11|4/4/4|rejected|
|asym370_parent_L5_HL300bp_HS250|parent|5|0.030|7.967870|6.941069|5.914748|3.841414|11|3/3/3|rejected|

新父历史通过4、淘汰2，逐配置失败判据{'asym370_ETH_L3_HL200bp_HS250_E025_V10': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'asym370_ETH_L3_HL300bp_HS250_E025_V10': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'asym370_ETH_L4_HL200bp_HS250_E025_V10': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'asym370_ETH_L4_HL300bp_HS250_E025_V10': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'asym370_ETH_L5_HL200bp_HS250_E025_V10': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'asym370_ETH_L5_HL300bp_HS250_E025_V10': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'asym370_parent_L3_HL200bp_HS250': [], 'asym370_parent_L3_HL300bp_HS250': [], 'asym370_parent_L4_HL200bp_HS250': [], 'asym370_parent_L4_HL300bp_HS250': [], 'asym370_parent_L5_HL200bp_HS250': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'asym370_parent_L5_HL300bp_HS250': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct']}。年度正收益不替代近期或局部邻域门槛。

新配置与同L对称HL=HS=2.5%对照的三成本完整NAV全同0/12，逐成本收益/DD差异与匹配fingerprint见equivalent_realized_NAV_paths。参数新颖不等于新alpha，同路径别名不删除、不改旧资格。

11CSV包含36场景、逐月/尾折/近期折、每日NAV、原生/父完整9格敏感性、72相邻边、持有/现金、旧来源与原分配。两面八指标图显示收益、全曲线DD、Sharpe和近期正折；Sharpe正格比例、边界峰值与描述性2std悬崖另列，不当作显著性，不按结果扩展本批门槛。

合成TDD先证明旧代码用2.5%对称门槛会把新多侧2%策略的2.2%回撤留空；修改后检查L3/4/5×HL2/2.5/3%、固定空侧2.5%等号/严格穿越、原持仓保留/退出/翻向、slow方向门、未来bar追加不变与隐式对称参数恒等。独立Fraction重算两侧价格规则，Decimal复核真实数量/成交/费用/资金费/小时风险/完整NAV及父对齐，不调用simulate/decide/trade重新回测。

冻结账户另行续接：原SMA和singleS28从Nov2UTC02:30至04:30，已处理00资金费/日决策不重复；独立未过滤L4/H2从04:10至06:10，仅06:11参考闭合后采集。保留完整cash/q/desired/risk/上下文/NAV前缀，不注入研究非对称参数；SMA真实65日上下文继续引用20261102T015622Z。部分延迟shadow不替代十策略实时报价模拟，不取消长期计划或新建账户。

一手来源实际访问2026-11-02：[Binance市场数据API](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)。8份真实bars/mark/funding/约束文件的hash、字节与边界在plan/data_manifest；文档不证明策略盈利或历史网络发布时刻，假设和局限分别留档。

同main排他锁内逐项finish、登记/来源/导出/监控检查、提交非强制push。只读汇总不产生成交、不改冻结规则/本金/持仓、不部署网页或新建任务。不下真实订单，正回测不称稳定实盘盈利。

封存：12个新定义逐项finish，6父中4历史通过、2淘汰，6ETH组件均未通过独立近期门槛。新父3倍370日净收益5.914748%至9.394103%，整体DD3.305465%至3.846302%。12个新配置相对匹配对称基线均为不同完整NAV，不把参数变化当独立未来证据。

L3/HL2%（shortHS2.5%固定）组合1/2/3倍净收益12.544468%/10.969628%/9.394103%，对应全曲线DD3.035647%/3.169982%/3.305465%；1倍10/12正月，近期各成本6/8正折，局部严格近期支持100%。匹配对称HL=HS=2.5%的收益10.241686%/8.890985%/7.539829%，DD完全相同；逐成本收益改善2.302782/2.078643/1.854274个百分点。这只是本批同L/同实际银行/同费用假设的历史对照改善，不是全历史最优、独立最终留出或稳定实盘盈利。

其他通过的L3/HL3%收益低于对应旧对照、DD相同；L4/HL2%收益提高但3倍DD由3.310960%升至3.813762%，L4/HL3%收益下降且DD相同。L5两多侧阈值近期净收益/正折/局部支持不足而淘汰；全部6原生组件近期不足。passed_candidate_evidence逐配置与逐成本列出，未按年度收益放宽门槛。

当前9格严格近期父6/9、原生0/9，三成本Sharpe全格正，但最大值在低HL端、全域描述性悬崖仍存在。局部门槛通过不代表所有参数或市场阶段稳健；未按结果增补HL变体或重新登记旧结果，没有独立未来资格或新账户/任务。

独立审核通过：19620468完整新对齐NAV点、6660决策，核算计数{'funding': 39960, 'fills': 1650, 'rejects': 0, 'metric_checks': 756, 'margin_checks': 135582}。Fraction独立重算多/空阈值，Decimal验证实际数量、费用、冲击、资金费、小时风险及完整父来源；父不新增成交。research_evidence_counts分别统计新/旧实际funding和成交，方向决策数不当订单数。25133旧保护文件字节不变，21新ID/42条追加事件完整；无simulate/decide/trade金融重跑。

SMA65续至2026-11-02T04:30:00Z：旧NAV44822+120=44942，累计44909分钟/31完整日，0新日决策/成交，保留原Floatcash/q/desired/cost/trades；65日上下文仍在20261102T015622Z，下一日决策2026-11-03T00:01:00Z。singleS28续2026-11-02T02:30:00Z至2026-11-02T04:30:00Z，NAV9115、累计ID225，新决策0、成交0、资金费[]、小时检查6。

独立未过滤L4/H2续2026-11-02T04:10:00Z至2026-11-02T06:10:00Z，06:11闭合参考后采集，NAV1852、累计1809分钟/48ID；新决策0、成交0、资金费[]、小时检查6。二者风险0违规，00已记资金费不重复，全部cash/q/risk/上下文与NAV前缀保持，不注入非对称阈值；三份部分观察仍沿原长期计划，未获180日资格。

只读监控检查通过：9016研究行、9004旧行完整字典不变，10原报价账户/220观察，gzip4081603字节，5MB预算保持。本轮可确认HTTP/传输失败0次，真实失败尝试及原始响应/stderr按实际保存；不补造未输出的响应，不继承上轮错误，预期TDD红灯另存，无完成观察重跑。

清理20558字节可重建一次性脚本，保存原hash和复现命令；真实结果与完整账户账本删除0。轻量结果、必要代码、规则、数据hash、原始响应完整保留；main提交/非强制push、完整远端tree/blob和真实进程终态/解锁证明在.git/automation_proofs/20261102T055753Z.json。
