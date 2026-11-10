完成8个新ETH组件和8个新父组合的48个成本场景：8/8父组合通过全部历史门槛，8/8ETH组件淘汰。三倍成本组合净收益11.146786%–14.146745%，没有超过旧中心。事前代表K0.75%/VC4.5%净收益12.542736%、连续整体回撤2.214788%，旧中心为14.146745%/3.082168%；这是较低收益/较小回撤的历史取舍，非稳定实盘证明。

检验上轮预算M4/VW8/R0.00875微小历史增益对价格门槛的依赖。固定预算全部规则及价格V10/H2%/L5/E0.75%/S16/D3，仅联合扫描K0.625/0.75/0.875%和VC4.5/5/5.5%。旧K0.75%/VC5%组件及父组合只读；其余8组件+8组合先reserve再算48场景。代表事前K0.75%/VC4.5%。全部时间/成本/资本/名义金额/raw[1,1]/失败门槛保持，不预认改善。L4/FEWM当前按新真实Nov10_08来源各自原持仓结算，原规则不采用研究K/VC。

完整读取31928事件/15842ID和369份既往结论。初始16项实际证据齐全（11正式+5旧ZIP），缺实际结果为0；5个legacy登记标志及历史文件保持。此前规范研究定义10583，登记标实际10370、未标实际213，不能声称所有登记均已验证。每个完整参数与数值组件图查重，旧K0.75%/VC5%中心只读复用，不因名称、顺序或格式重复计算。新16项保存spec、成功reserve后计算且全数finish。另12项原账户真实续记，共28ID/56事件，成功/负收益/淘汰/真实失败均保留。

经济假设：上轮相对资金费预算的微小历史优势可能依赖价格门槛，本轮固定预算中位数M4、样本日logvol窗口VW8、比例R0.00875和2bp硬上限；仅联合扫描慢EWM斜率门槛K=[0.00625,0.0075,0.00875]与价格入场波动率上限VC=[0.045,0.05,0.055]。价格波动率窗口V10、H2%/L5/E0.75%/S16/beta15/17/D3保持。趋势严格大于+K/小于−K才通过，等于边界不触发；价格sigma>VC才阻止新开/反手，等于上限允许。实际同向q保留，反手先平旧仓。

资金费门槛保持：UTC00:00前已可用、结算年龄1–36小时的最新4笔SIGNED实际费率，取中间二项均值；max(原方向×median,0)<=min(0.0002,0.00875×过去8个已完成日收益样本logvol×最近成熟真实结算间隔小时/24)，Decimal28按sigma字符串转换。间隔使用最新合格fundingTime与直接上一笔真实时间的纳秒差，双方在信号时可得，保留毫秒抖动；归一化名义8小时不是测量值。缺记录/间隔只阻止新开/反手，不重定同向数量；下一UTC00:01 OPEN执行。历史available_ts=结算后1小时仍为保守假设，非网络到达实测；过去费率不是未来费率。

BTC/ETH各1212条资金费来源、370次信号的成熟记录选择、年龄与间隔已核验。33日源上下文支持ETH信号19日/成本21日、BTC30日和预算9日close。数据版本、SHA256、真实原始公共响应和选择索引见plan/funding_signal_preflight/data_manifest/raw_evidence_index。公开字段依据[Binance资金费历史文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)，访问UTC2026-11-10；策略预算假设为本轮研究设计。

组合资本/权重：旧BTC29/H3%/E1%银行3750、N1000完整实际路径只读；新ETH银行15000、N4500逐项重算原生数量/LOT、成本/冲击/资金费/保证金代理与完整净值。raw[1,1]相加完整独立银行，总本金18750；20%/80%资本占比不再乘第二次，无归一化、缩放、资金转移、再平衡、父订单或交叉保证金。旧中心、旧预算中心、无过滤同C/N及常持有/现金0%对照均只读。

Walk-forward完成：2025-10-19 UTC00:01至2026-10-24 UTC00:01连续370日，12×30日完整折加10日尾；近期40日继承day330现金/仓位，分8×5日，不折间重开。无拟合/标签/purge/embargo，过去闭合信号、下一可执行OPEN及终点平仓成本均核验。保存逐折指标、日净值与由完整连续净值计算的整体DD。反复使用的开发历史及约一万次研究选择偏差，不是未触碰最终留出或独立确认。

Sensitivity完成K/VC各九格（8新+1旧中心）、72邻接边及净收益/整体DD/Sharpe/Calmar图。父组合九格严格近期均达6/8、局部严格近期合格比例均为1；每档成本两张网格Sharpe全正。ETH组件近期均仅2/8、局部严格近期不合格，8项淘汰。虽8个新父组合都满足预设局部门槛，收益与回撤仍出现描述性跳变，VC4.5%会牺牲收益且部分K下回撤更大；不能据此宣称独立未来稳定。数值平台存在完整净值别名，不能当作独立样本。旧中心canonical资格及旧敏感性保持，新K/VC诊断另存。

成本1/2/3倍压力完成，16项全期均净正。每边5bp手续费+1bp半价差+2bp滑点；冲击=0.5×过去20日样本logvol×sqrt(实际abs(q)×原生OPEN/过去20日quoteADV)。执行成本及资金费支出随倍数放大，资金费收入不放大。实际结算time/rate/mark与持仓q逐笔核算，线性永续无现货借币；检查LOT/tick/minnotional、≤0.1%参与率、费后1倍抵押及1%闭合小时不利mark维护保证金代理。缺真实L2/TCA、完整历史风险档位/逐tick强平、真实容量证据。

门槛不改：全期/近期各成本净正，1x≥9/12正完整30日折，近期各成本≥6/8正5日折，3x整体DD≤25%，局部3x净正及严格近期比例≥60%，≥4次原生平仓，毛价格PnL加净资金费/1x成本≥2.5，无抵押/订单/风险代理违规，终点flat及≥180日。全部新父组合通过，ETH组件因近期一致性不足淘汰，不因全期净正而放宽门槛。

|范围|K|VC|1x净%|2x净%|3x净%|3x整体DD%|月正折/12|近期正折1/2/3|状态|
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|native|0.00625|0.045|13.279258|12.476279|11.673505|4.537987|9|2/2/2|rejected|
|native|0.00625|0.05|15.588858|14.633497|13.678515|4.417065|10|2/2/2|rejected|
|native|0.00625|0.055|15.588858|14.633497|13.678515|4.417065|10|2/2/2|rejected|
|native|0.0075|0.045|14.878391|14.148314|13.418442|2.050018|9|2/2/2|rejected|
|native|0.0075|0.055|17.187991|16.305532|15.423452|4.080065|10|2/2/2|rejected|
|native|0.00875|0.045|14.878391|14.148314|13.418442|2.050018|9|2/2/2|rejected|
|native|0.00875|0.05|17.187991|16.305532|15.423452|4.080065|10|2/2/2|rejected|
|native|0.00875|0.055|17.187991|16.305532|15.423452|4.080065|10|2/2/2|rejected|
|parent|0.00625|0.045|13.023307|12.084963|11.146786|4.180988|11|6/6/6|passed|
|parent|0.00625|0.05|14.870987|13.810737|12.750794|4.091074|10|6/6/6|passed|
|parent|0.00625|0.055|14.870987|13.810737|12.750794|4.091074|10|6/6/6|passed|
|parent|0.0075|0.045|14.302613|13.422591|12.542736|2.214788|11|6/6/6|passed|
|parent|0.0075|0.055|16.150293|15.148365|14.146745|3.082168|10|6/6/6|passed|
|parent|0.00875|0.045|14.302613|13.422591|12.542736|2.214788|11|6/6/6|passed|
|parent|0.00875|0.05|16.150293|15.148365|14.146745|3.082168|10|6/6/6|passed|
|parent|0.00875|0.055|16.150293|15.148365|14.146745|3.082168|10|6/6/6|passed|
|native旧中心|0.0075|0.05|17.187991|16.305532|15.423452|4.080065|10|2/2/2|rejected|
|parent旧中心|0.0075|0.05|16.150293|15.148365|14.146745|3.082168|10|6/6/6|passed|

逐项失败判据：{'pricegatecarry_370_ETH_K6250ppm_VC45000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'pricegatecarry_370_ETH_K6250ppm_VC50000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'pricegatecarry_370_ETH_K6250ppm_VC55000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'pricegatecarry_370_ETH_K7500ppm_VC45000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'pricegatecarry_370_ETH_K7500ppm_VC55000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'pricegatecarry_370_ETH_K8750ppm_VC45000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'pricegatecarry_370_ETH_K8750ppm_VC50000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'pricegatecarry_370_ETH_K8750ppm_VC55000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'pricegatecarry_370_parent_BTC29H3_ETH_K6250ppm_VC45000ppm': [], 'pricegatecarry_370_parent_BTC29H3_ETH_K6250ppm_VC50000ppm': [], 'pricegatecarry_370_parent_BTC29H3_ETH_K6250ppm_VC55000ppm': [], 'pricegatecarry_370_parent_BTC29H3_ETH_K7500ppm_VC45000ppm': [], 'pricegatecarry_370_parent_BTC29H3_ETH_K7500ppm_VC55000ppm': [], 'pricegatecarry_370_parent_BTC29H3_ETH_K8750ppm_VC45000ppm': [], 'pricegatecarry_370_parent_BTC29H3_ETH_K8750ppm_VC50000ppm': [], 'pricegatecarry_370_parent_BTC29H3_ETH_K8750ppm_VC55000ppm': []}。

独立审计：24新原生+24新父组合+18旧原生成本曲线，8880次新决策、46620条资金费、1152笔成交、924项全期/逐月指标和131622项风险检查通过。独立Fraction/Horner信号、K/VC门槛、固定VW8预算、原生数量/冲击/现金流及全NAV核对；未调用新simulate/decide/trade。仅decide的K/VC可接受数值域改变，其余原函数AST均保持。

旧完整路径查重比较502个同C/N原生定义及212个父组合，16项中6项三档全路径此前出现，均属旧中心别名。K≥0.75%且VC≥5%的新格没有额外历史收益。K0.75/0.875%与VC4.5%互为同一较小回撤路径；K0.625%高VC也有别名。不同实参仍各自登记，真实等路径不视为独立盈利证据。

较旧中心：K0.75%/VC4.5%（事前代表）净收益12.54%、整体DD2.21%，低于旧中心14.15%/3.08%的收益及回撤；属风险收益取舍，未支配旧中心。其他部分格在收益和DD上被旧中心严格支配；逐项常持有/现金、旧预算及无过滤对照、价格PnL/资金费/成本归因均留档。价格门槛改变持仓路径，不能将差异全归为资金费预测。

本窗原账户：SMA/single Nov10 04:30–06:30仅闭合mark/风险；L4/FEWM06:10–08:10按新真实Nov10_08结算各自账本，无新日决策/成交、无重开/新本金/研究规则采用。原Float或Decimal现金、q、desired、entry、成本、风险与完整NAV前缀独立核验。SMA日上下文仍为031055轮65个完整SPOT日、结束Nov10 UTC00:00，当前minute数组不替换日数据。

新公共来源两次GET均成功：fundingTime=1794297600000ms（08:00整秒），BTC率0.00010000、mark74812.70，ETH率0.00003035、mark2115.11。L4实际BTC q=-0.006、FEWM q=-0.009，各成本场景分别收入0.04488762、0.06733143USDT，正收入未随2/3倍放大；ETH实际q=0，金额0但保留实际资金费来源及记录。每账户各6条账目，以各自结算前q/现金核算；single窗口尚未跨08，当前不入账，不能复制他人的现金流。
原SMA NAV 56470→56590，累计56549分钟；仍为partial延迟shadow，不等同paper10真实报价模拟或180日前向资格。
原single NAV 20899→21021，累计20549分钟；仍为partial延迟shadow，不等同paper10真实报价模拟或180日前向资格。
L4 NAV 13636→13760，累计13449分钟；仍为partial延迟shadow，不等同paper10真实报价模拟或180日前向资格。
FEWM NAV 7744→7868，累计7689分钟；仍为partial延迟shadow，不等同paper10真实报价模拟或180日前向资格。

下轮：SMA/single06:30–08:30，SMA仅mark、single需在自己的新截止reserve后，复用本轮不可变Nov10_08公开字段，按它自己的当时q/现金结算一次，等08:31参考闭合；旧funding08_current_preflight是Nov9，不能替代本轮funding08_nov10。L4/FEWM当前08已各自结算一次，下一08:10–10:10仅mark/risk，不重复08。下一日决策均Nov11 UTC00:01，SMA届时更新新65日SPOT并从当前状态延续。

下一研究预案未执行：固定预算M4/VW8/R0.00875、价格K0.75%/VC5%、V10/L5/S16/D3，扫描入场H=[0.0175,0.02,0.0225]×退出E=[0.00625,0.0075,0.00875]。H2%/E0.75%中心已实际执行，必须只读；其余八格仍须全查重、完整代码/spec和Fraction边界/持仓/反手/预算不变性检查，再reserve。全部成本、时间、资金/名义金额/raw权重与门槛不改，不预认改善、不建立新冻结账户或采用新规则。

只读监控生成及原生检查True：10158研究行，旧10142行保持、新16行；paper10为10账户/317观察。gzip4646240字节，未重部署或新建任务。

真实失败保存：旧L4对照脚本残留固定K/VC断言，已更新预设域后只读复核；actual回测/账户窗口未重跑。single公共请求2次TLS35失败，原 bounded 重试成功，失败原始响应、stderr和回执保留，未禁用TLS验证。4项预期合成RED单独保存。图表仅订正旧caption固定K/VC字样并按保存指标重绘，没有策略或指标重算。

部分继承print/派生字段仍带旧VW/R、H/E、12/36或午夜活动标签，见derived_label_correction.json；以冻结spec、每项K/VC、来源、完整逐笔/净值、current_actual_nov10_08及独立核验为准，不改写已finish报告隐藏标签遗留。

复现argv/cwd/UTC/原生退出码见reproduction_history.json和*_commands.json。大行情及必要原始数据保留忽略data目录；Git保留全部正负/淘汰结果、逐折/成本/敏感性、完整账户账本、公共响应压缩副本、冻结规则和数据哈希。可重建文件清理见cleanup_verification.json。

同main共享锁内完成登记、检查、只读快照后封存，普通非force push并独立核对远端ref、完整tree/blob/三条永续账户链，完成后解锁。真实commit/push/解锁终态见.git/automation_proofs/20261110T091228Z.json，不仅据本文宣称push成功。
