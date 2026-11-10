本轮8个新ETH组件及8个新父组合完成48个成本场景，4/8父组合历史通过，另4个父组合及8个组件淘汰。VW8/R0.00875三倍成本净收益14.146745%、连续整体回撤3.082168%，较旧VW10/R0.0075中心增加0.077948个百分点，约14.62USDT。该最优点在两轴边界，仅为复用历史后的描述性发现，不是稳定实盘或独立未来证据。

检验上轮M4相对carry预算的收益对波动率估计长度是否稳定。固定M4及价格入场V10/VC5%，单独扫描预算VW8/10/12×R0.00625/0.0075/0.00875。旧VW10/R0.0075中心真实组件/组合只读；其余8组件+8组合先reserve再算48成本场景。代表事前VW12/R0.0075。不改变价格规则、资本/名义金额、raw[1,1]权重、时间和门槛，不预认改善。四原账户本窗仅marks，无fund/daily/fill。

完整读取31852条登记事件/15804ID、368份旧结论。初始16项实际证据齐全：11项正式结果、5项旧ZIP实际回测；5个legacy标志原样保留，实际缺口为0，未重复执行旧实际配置。此前规范研究定义10567，登记标实际10354、未标实际213，不能称所有登记都已完成。

新颖性按完整参数、语义默认值和数值组件图查重。VW10/R0.0075缺省budgetVW=10与新增显式10字段、已知公式描述别名视为同一规则，直接复用原生银行及父组合指纹/压缩结果，未reserve或重算。其余八格逐项生成spec、成功reserve后才计算，16项全数finish。另12项原账户闭合行情续记，共28ID/56事件；正收益、负收益、淘汰和真实失败均保留。

经济假设：上轮相对资金费预算的历史增益可能依赖波动率估计长度，本轮单独改变预算样本日logvol窗口VW=[8,10,12]和比例R=[0.00625,0.0075,0.00875]。资金费中位数M固定4；价格入场波动率门槛仍为独立V10/VC5%。ETH价格规则固定H2%/E0.75%/L5/K0.75%、有限归一化EWM S16/beta15/17/D3。预算=min(0.0002,R×sigma_VW×最新合格过去实际结算间隔小时/24)，sigma_VW仅用i−VW至i−1的VW个已完成日收益、需要VW+1个过去close，Decimal28按sigma字符串转换；R是风险预算比例，硬上限为每次结算费率2bp。

选择UTC00:00信号前已可用、结算年龄1–36小时的最新4笔SIGNED实际费率，中位数为中间二项均值。max(原入场方向×median,0)<=预算才允许新开/反手；缺记录、缺间隔或间隔非正/大于36小时仅阻止新开/反手，同向实际q保留，反手先平旧仓。下一UTC00:01 OPEN执行。真实间隔以最新合格fundingTime减其直接上一笔真实时间戳计算，两笔都在信号时可得，保留毫秒抖动；不使用归一化字段的名义常数8小时。available_ts=结算后1小时仍是保守假设，不是历史网络到达证明；过去费率不是未来费率。

BTC/ETH各1212条实际资金费来源，全370次信号都有至少4笔成熟记录。来源/版本/SHA256、选择索引/年龄/实际间隔保存在plan、funding_signal_preflight、data_manifest与raw_evidence_index；完整33日源上下文支持ETH信号19日/成本21日、BTC30日和预算最大13日close。公开字段依据[Binance资金费历史文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)，访问UTC2026-11-10。预算/VW假设为本轮研究设计。

组合保留原银行：BTC3750/N1000的29日动量/H3%/E1%实际净值只读；ETH15000/N4500新算实际数量/LOT、成本、冲击、资金费、风险与全净值。raw权重[1,1]相加两条完整独立银行，总本金18750，20%/80%资本占比不再乘第二次，无归一化、缩放、转账、再平衡、父订单或跨银行交叉保证金。10个只读旧结果包括动态中心、M4固定75ppm对照、同价格规则无过滤对照及同C/N常持有；现金基准0%。

Walk-forward完成：2025-10-19 UTC00:01至2026-10-24 UTC00:01连续370日，12×30日完整折及10日尾；近期40日继承day330现金/仓位分8×5日，折间不重开。无拟合、标签、purge或embargo；固定规则只用过去闭合数据，下一可执行OPEN，终点平仓计成本。保留逐折及完整连续净值整体回撤。历史已反复用于研究，不能称未触碰最终留出或独立确认。

Sensitivity完成VW/R两轴、各九格（8新+1旧中心）、72条邻接边、净收益/整体DD/Sharpe/Calmar及独立图表。两张网格各成本Sharpe均为正；父组合只有5/9格满足严格近期要求，各成本存在描述性邻接跳变，最大值位于VW8/R0.00875两轴边界，没有稳定平台结论。旧中心canonical历史passed及原敏感性保持；它在本轮VW/R九格的严格近期邻域比例为5/9<60%，仅作为新诊断，不能用旧passed字样声称新邻域通过，也不反写旧资格。

成本1/2/3倍压力完成，16项全期均净正。每边5bp手续费、1bp半价差、2bp滑点；冲击=0.5×过去20日样本logvol×sqrt(实际abs(q)×原生OPEN/过去20日quoteADV)。执行成本及资金费支出随1/2/3倍放大，资金费收入不放大，按实际结算time/rate/mark和当时q核算。线性永续无现货借币；检查LOT/tick/minnotional、≤0.1%参与率、费后1倍入场抵押及1%闭合小时不利mark维护保证金代理。缺真实L2/TCA、完整历史风险档位/逐tick强平与实盘容量证据。

原门槛保持：全期/近期各成本净正，1x≥9/12正完整30日折，近期各成本≥6/8正5日折，3x整体DD≤25%，局部3x净正及严格近期比例≥60%，≥4次原生平仓，毛价格PnL加净资金费/1x成本≥2.5，无抵押/订单/风险代理违规，终点flat及≥180日。新4个父组合因近期只有5/8正折及局部一致性不足淘汰，8个ETH组件近期仅1–2/8，均淘汰。新4个父组合通过全部预设门槛。

|范围|VW|R|1x净%|2x净%|3x净%|3x整体DD%|月正折/12|近期正折1/2/3|状态|
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|native|8|0.00625|16.863453|16.060235|15.257397|4.080065|9|1/1/1|rejected|
|native|8|0.0075|16.863453|16.060235|15.257397|4.080065|9|1/1/1|rejected|
|native|8|0.00875|17.187991|16.305532|15.423452|4.080065|10|2/2/2|rejected|
|native|10|0.00625|16.444641|15.693159|14.941899|4.080065|8|1/1/1|rejected|
|native|10|0.00875|17.101301|16.213469|15.326017|4.080065|10|2/2/2|rejected|
|native|12|0.00625|15.462307|14.769032|14.075977|4.080065|8|1/1/1|rejected|
|native|12|0.0075|16.721251|15.828040|14.935209|4.080065|10|2/2/2|rejected|
|native|12|0.00875|16.721251|15.828040|14.935209|4.080065|10|2/2/2|rejected|
|parent|8|0.00625|15.890663|14.952128|14.013900|3.082168|10|5/5/5|rejected|
|parent|8|0.0075|15.890663|14.952128|14.013900|3.082168|10|5/5/5|rejected|
|parent|8|0.00875|16.150293|15.148365|14.146745|3.082168|10|6/6/6|passed|
|parent|10|0.00625|15.555613|14.658467|13.761502|3.082168|9|5/5/5|rejected|
|parent|10|0.00875|16.080941|15.074715|14.068797|3.082168|10|6/6/6|passed|
|parent|12|0.00625|14.769746|13.919165|13.068765|3.082168|9|5/5/5|rejected|
|parent|12|0.0075|15.776902|14.766372|13.756150|3.082168|10|6/6/6|passed|
|parent|12|0.00875|15.776902|14.766372|13.756150|3.082168|10|6/6/6|passed|
|native旧中心|10|0.0075|17.101301|16.213469|15.326017|4.080065|10|2/2/2|rejected|
|parent旧中心|10|0.0075|16.080941|15.074715|14.068797|3.082168|10|6/6/6|passed|

逐项失败判据：{'volwindow_370_ETH_M4_VW8_R6250ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volwindow_370_ETH_M4_VW8_R7500ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volwindow_370_ETH_M4_VW8_R8750ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volwindow_370_ETH_M4_VW10_R6250ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volwindow_370_ETH_M4_VW10_R8750ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volwindow_370_ETH_M4_VW12_R6250ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volwindow_370_ETH_M4_VW12_R7500ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volwindow_370_ETH_M4_VW12_R8750ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volwindow_370_parent_BTC29H3_ETH_M4_VW8_R6250ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volwindow_370_parent_BTC29H3_ETH_M4_VW8_R7500ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volwindow_370_parent_BTC29H3_ETH_M4_VW8_R8750ppm': [], 'volwindow_370_parent_BTC29H3_ETH_M4_VW10_R6250ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volwindow_370_parent_BTC29H3_ETH_M4_VW10_R8750ppm': [], 'volwindow_370_parent_BTC29H3_ETH_M4_VW12_R6250ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volwindow_370_parent_BTC29H3_ETH_M4_VW12_R7500ppm': [], 'volwindow_370_parent_BTC29H3_ETH_M4_VW12_R8750ppm': []}。

独立审计通过：24新原生、24新组合及18旧原生成本曲线，8880次新决策，46620条资金费、1146笔成交、924项全期/逐月指标与130242项风险检查。独立Fraction/Horner价格信号、单独VW样本波动率/Decimal预算、实际数量/冲击/现金流及全NAV均核验；未调用新引擎simulate/decide/trade。原交易/资金费/抵押/净值函数AST全部保持，只新增budget_sigma并在decide引用，价格V10原规则不变。

读取494个旧同C/N ETH定义及204个旧父组合：16项中6项完整三档净值路径以前出现。新4个历史通过父组合中2项等同无过滤旧路径、1项等同旧动态中心，只有VW8/R0.00875是此前未见路径。边界最佳为看完网格后描述，事前代表仍为VW12/R0.0075，其结果等同无过滤对照，未事后替换。新最佳较旧中心仅约0.078个百分点，不能忽略约一万次历史研究选择偏差。

保存同中心、固定75ppm及无过滤对照和常持有/现金比较；价差PnL、净资金费、执行成本变化分开核对。预算过滤改变实际持仓路径，不能把全部收益变化说成资金费预测能力。所有旧报告、规则和资格原字节保留。

四原账户本窗仅续闭合mark/小时风险：SMA/single Nov10 02:30–04:30，L4/FEWM04:10–06:10，无新资金费、日决策、成交、本金或研究规则采用。SMA继续保留031055轮的65个完整SPOT日、结束Nov10 UTC00:00；当前minute数组不替代日上下文。原Float现金/q/desired/成本和全部原账本/NAV前缀独立核对。
原SMA NAV 56350→56470，累计56429分钟；仍为partial延迟shadow，不等同paper10实时行情模拟或180日前向资格。
原single NAV 20777→20899，累计20429分钟；仍为partial延迟shadow，不等同paper10实时行情模拟或180日前向资格。
L4 NAV 13514→13636，累计13329分钟；仍为partial延迟shadow，不等同paper10实时行情模拟或180日前向资格。
FEWM NAV 7622→7744，累计7569分钟；仍为partial延迟shadow，不等同paper10实时行情模拟或180日前向资格。

下轮SMA/single04:30–06:30仅mark；L4/FEWM06:10–08:10将跨越08 UTC，须先取得新真实Nov10_08的fundingTime/rate/mark、保留毫秒精度并等08:11执行参考闭合，再按各自结算前q/现金及成本场景入账。旧funding08_current_preflight是Nov9数据，不能替代Nov10；最近真实资金费仍为Nov10_00且各自已经结算一次，不重播00或复制其他账户现金流。四账户下一日决策均为Nov11 UTC00:01，SMA届时更新新的完整65日SPOT数据并从当时真实状态续接。

下一研究预案尚未执行：固定本轮VW8/R0.00875/M4和全部银行/价格周期，扫描价格慢趋势门槛K=[0.00625,0.0075,0.00875]×入场波动率上限VC=[0.045,0.05,0.055]，价格窗口V10、预算VW8保持独立。中心K0.0075/VC0.05已实际执行，必须只读；其余八格须先全登记查重、完整新代码/spec和独立边界/预算不变性检查，再reserve计算。目标为检验微小历史增益对价格门槛的依赖，不预认改善、不采用到原冻结账户。

只读监控生成与原生检查True，研究10142行，旧10126行不变、新16行；paper10为10账户/316观察。gzip4640957字节，未重部署或新建定时任务。

真实失败全部留档：只读对照脚本计数替换误改本金断言，已修正后核验；实际spec/报告及独立银行核算本金始终18750，未重算已完成回测。SMA公共请求发生1次TLS错误，原有请求重试成功，原stderr/日志保留，未禁用TLS校验或重跑账户窗口。4项预期合成RED单独保存。

少量继承输出文字/派生字段仍带旧H/E、M/F、12/36或旧午夜活动标签，独立订正见derived_label_correction.json；以冻结spec、每配置VW/R、实际来源、逐笔/净值和独立核验为准，不修改已finish报告隐藏标签遗留。

复现argv/cwd/UTC/原生退出码见reproduction_history.json和各*_commands.json。大行情/必要原始数据保留忽略data目录，Git保存全部正负/淘汰结果、逐折/成本/敏感性、完整账户账本、公共响应压缩副本、冻结规则和数据哈希。可重建中间文件清理记录见cleanup_verification.json。

同main共享锁内完成登记、检查和只读快照后封存、普通非force push，独立核对远端main、完整tree/blob及三条完整永续账户链后解锁。真实commit/push/解锁终态见.git/automation_proofs/20261110T071157Z.json，不能仅据本文宣称push成功。
