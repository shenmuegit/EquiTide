完成 L×价格波动窗口批次：16项独立登记配置、48个1/2/3倍成本场景，2/8个父组合历史通过，6个父组合及8个ETH组件淘汰。16项全期均净正，仍按原判据淘汰不合格者；全期三档均净负的配置数为0，逐折负收益及全部结果均保留。事前代表L5/V8三倍收益13.921519%、连续整体回撤2.429298%，历史门槛通过。不是稳定实盘盈利证明。

固定资金费M4/BUDGET_VW8/R0.00875及有限EWM S16/D3/K0.75%、H2%/E0.75%/VC5%，联合检验快ROC L4/5/6与价格波动窗口V8/10/12。旧L5/V10只读，8新组件+8组合先reserve再算48场景。事前代表L5/V8。资金费预算VW8独立于价格V。固定成本、日历、资本、名义金额、raw[1,1]、失败判据。原SMA/single12:30至14:30只mark；L4/FEWM14:10至16:10用新抓取实际Nov10_16字段和各自q/cash入账一次，无新日决策或成交，不采用研究规则。

本轮完整读取32252事件/16004ID和373份既往结论。初始16项均有实际结果证据（11正式+5原ZIP实际回测），不因5个legacy标志为false重复测试或改写旧登记。此前规范研究定义10647，其中标记有实际结果10434，未标实际213；不把代码检查称回测。全部16份spec与数值组件图先查重、成功reserve，随后实际计算并finish。10个旧源结果与旧L5/V10中心只读。另12项原账户真实观察，共28ID/56事件。

本轮只变快ROC L=[4,5,6]和价格波动窗口PRICE_V=[8,10,12]。固定有限归一化EWM S16、beta15/17、趋势斜率滞后D3及严格门槛±K0.75%，固定反转入场H2%/保留退出E0.75%、价格波动上限VC5%。r=最近完成日收盘/前L日收盘−1；r>H做空、r<−H做多，区间内仅按严格E规则保留同向实际仓位。趋势及波动门槛只约束新开/反手，同向实际数量不重置，反手先平，下一UTC00:01 OPEN执行。

资金费预算BUDGET_VW固定8日，与价格PRICE_V独立。UTC00:00信号只用结算年龄1–36小时、available_ts不晚于信号的最新4笔SIGNED真实费率，偶数median取中间两项均值；expected_out=max(拟开方向×median,0)，仅当其≤min(0.0002,0.00875×过去8日样本logvol×最新成熟真实结算间隔小时/24)才允许新开。实际间隔为最新合格fundingTime减直接上一笔实际时间，保留毫秒抖动且两笔已可用；归一化名义8小时不是实测间隔。缺必要记录/间隔只阻止新开。每资产1212笔真实费率、370次来源选择及1小时保守可用延迟核验；该延迟是建模假设，非网络到达证明，过去费率不等于未来费率。

351组独立Fraction ROC、Horner EWM、样本PRICE波动、H/E边界、持仓/反手、未来数据隔离检查及360次预算窗口分离检查通过。5项预期RED分别拦截未扩展的域、重复资金加权、强行旧L5、未来资金费、强行旧价格V10。仅decide的L/PRICE_V可接受域变化，其余函数及simulate/现金/成本/资金费/预算逻辑AST不变。最大ETH信号上下文19日，成本21日；价格最多需13个收盘、资金费预算9个收盘；33日源上下文覆盖ETH21和BTC30，无未来初始化。

Walk-forward已执行：2025-10-19 UTC00:01至2026-10-24 UTC00:01连续370日，12个完整30日折+10日尾。近期40日继承day330实际现金、仓位和风险，分8个5日折，折间不重新开仓。624个逐折、384个近期折、17808个日净值行及连续OOS全路径整体DD保存。不存在拟合/标签窗口，purge/embargo不适用；该历史反复用于开发，不称未触碰最终测试集、独立最终检验或未来收益证明。8份真实归一化源文件及必要原始来源、完整哈希留档。

敏感性已执行：原生与父组合各9格（8新+1旧L5/V10中心）、72条邻接边，收益、连续整体DD、Sharpe、Calmar及三档成本完整保留。原生与父组合各9/9格全期Sharpe为正，但ETH近期仅1–2/8正5日折，局部严格近期比例为0，全部8项淘汰。父组合近期各档均6/8；L4/L6只有8/12正完整月折，故6项淘汰，L5的两项新配置有10/12正月并通过。L从5改为4或6仍出现明显跳变；Sharpe最大格在V8边界。不能把条件于L5的价格V邻域解释为跨参数稳定平台。旧中心canonical资格与旧敏感性不重评，本轮诊断单列。

成本1/2/3倍已执行：每边手续费5bp+半价差1bp+滑点2bp；冲击=0.5×过去20日样本logvol×sqrt(实际abs(q)×原生OPEN/过去20日quoteADV)。执行成本及资金费支出随倍数放大，正资金费收入不放大。线性永续不借现货；按实际结算time/rate/mark和自身真实持仓核算，检查LOT/tick/minnotional、≤0.1%参与率、费后1倍抵押及1%已闭合小时不利mark维护保证金代理。无真实L2/TCA、完整历史风险档位、逐tick强平或实盘容量证明。

父组合raw[1,1]直接相加独立完整银行：旧BTC29/H3%/E1%，资本3750、固定开仓N1000；新ETH资本15000、N4500逐项实际模拟。总初始资本18750，20%/80%为资本份额，不再次加权、不归一化、不缩放源NAV、不转移资金、不再平衡、无父订单或交叉抵押。旧中心、旧预算、同C/N无过滤、同期常持有和现金0%比较均保留；多参数不同的旧对照仅作描述，不把全部差异归因于资金费过滤。

原门槛不改：各成本全期/近期净正，1x≥9/12正完整月折，近期各档≥6/8正5日折，3x整体DD≤25%，局部3x净正及严格近期比例≥60%，≥4次原生平仓，毛价格PnL加净资金费/1x执行成本≥2.5，无现金/订单/风险代理违规，终点flat且≥180日。正收益不免除失败判据。

|范围|L|价格V|1x净%|2x净%|3x净%|3x整体DD%|月正/12|近期正折1/2/3|状态|
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|native|4|8|11.094932|10.006669|8.918171|5.734212|8|2/2/2|rejected|
|native|4|10|8.377935|7.296606|6.214890|5.804207|8|2/2/2|rejected|
|native|4|12|8.180438|7.155442|6.130283|5.827127|8|2/2/2|rejected|
|native|5|8|16.800007|15.970774|15.141921|3.288415|10|2/2/2|rejected|
|native|5|12|17.105268|16.224062|15.343085|4.082937|10|2/2/2|rejected|
|native|6|8|4.823570|4.158422|3.493980|7.144008|7|1/1/1|rejected|
|native|6|10|4.966033|4.298000|3.630762|8.060596|7|1/1/1|rejected|
|native|6|12|4.502856|3.886948|3.271712|7.955449|7|1/1/1|rejected|
|parent|4|8|11.275846|10.109276|8.942520|5.507383|8|6/6/6|rejected|
|parent|4|10|9.102248|7.941225|6.779894|5.507383|8|6/6/6|rejected|
|parent|4|12|8.944251|7.828293|6.712209|5.557528|8|6/6/6|rejected|
|parent|5|8|15.839906|14.880559|13.921519|2.429298|10|6/6/6|passed|
|parent|5|12|16.084115|15.083189|14.082451|3.083936|10|6/6/6|passed|
|parent|6|8|6.258757|5.430677|4.603166|5.803465|8|6/6/6|rejected|
|parent|6|10|6.372727|5.542340|4.712592|6.151700|8|6/6/6|rejected|
|parent|6|12|6.002185|5.213498|4.425352|6.066747|8|6/6/6|rejected|
|native旧中心|5|10|17.187991|16.305532|15.423452|4.080065|10|2/2/2|rejected|
|parent旧中心|5|10|16.150293|15.148365|14.146745|3.082168|10|6/6/6|passed|


逐项失败判据：{'fastvolcarry_370_ETH_L4_PV8': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fastvolcarry_370_ETH_L4_PV10': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fastvolcarry_370_ETH_L4_PV12': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fastvolcarry_370_ETH_L5_PV8': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fastvolcarry_370_ETH_L5_PV12': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fastvolcarry_370_ETH_L6_PV8': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fastvolcarry_370_ETH_L6_PV10': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fastvolcarry_370_ETH_L6_PV12': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fastvolcarry_370_parent_BTC29H3_ETH_L4_PV8': ['nine_of_twelve_positive_complete30d_1x_folds'], 'fastvolcarry_370_parent_BTC29H3_ETH_L4_PV10': ['nine_of_twelve_positive_complete30d_1x_folds'], 'fastvolcarry_370_parent_BTC29H3_ETH_L4_PV12': ['nine_of_twelve_positive_complete30d_1x_folds'], 'fastvolcarry_370_parent_BTC29H3_ETH_L6_PV8': ['nine_of_twelve_positive_complete30d_1x_folds'], 'fastvolcarry_370_parent_BTC29H3_ETH_L6_PV10': ['nine_of_twelve_positive_complete30d_1x_folds'], 'fastvolcarry_370_parent_BTC29H3_ETH_L6_PV12': ['nine_of_twelve_positive_complete30d_1x_folds']}。所有成本、逐折/逐变体回撤与负收益留存。

独立审计通过：24新原生+24新父组合+18旧成本曲线，8880次新决策、46620条资金费、1152笔新旧成交、924项全期/逐月指标、141540项风险检查，0订单拒绝。独立Fraction/Horner、数量/LOT/价差/冲击/资金费现金流与完整NAV重建，不调用新simulate/decide/trade。

同C/N全路径比较534个旧原生定义及244个旧父组合，发现2项（L4/V10组件及父组合）三档保存路径与旧结果一致。实参不同仍各自登记，已执行一次并保留；路径别名不构成独立盈利样本，旧资格不改。

预设代表L5/V8的三倍收益13.921519%低于旧L5/V10中心14.146745%，同时整体DD2.429298%低于旧中心3.082168%。这是收益与回撤权衡，非严格收益/DD双改善。L5/V12三倍收益14.082451%、整体DD3.083936%，也不支配旧中心。未按事后峰值更换预设代表或修改门槛。

原四账户独立续接：SMA/single本窗Nov10 UTC12:30–14:30仅闭合mark/risk；L4/FEWM14:10–16:10按新抓取的真实16:00:00.002结算。BTC fundingRate=0.00005925、mark=73187.13633333；ETH fundingRate=−0.00002117、mark=2022.42103101。L4原BTC q=−0.006，FEWM原BTC q=−0.009，各自现金流按−q×mark×rate计算；正收入在2/3倍不放大，ETH零持仓现金流为零。每账户6条资金费分别入账，未复制他人现金流。single本窗尚未跨16，保持自身08结算为最新，未提前入账。

SMA完整NAV前缀56950→57070，累计57029分钟；实际资金费、各自现金/q/entry/risk/日上下文及完整前缀独立核验，0新日决策/成交。

single完整NAV前缀21389→21511，累计21029分钟；实际资金费、各自现金/q/entry/risk/日上下文及完整前缀独立核验，0新日决策/成交。

L4完整NAV前缀14126→14250，累计13929分钟；实际资金费、各自现金/q/entry/risk/日上下文及完整前缀独立核验，0新日决策/成交。

FEWM完整NAV前缀8234→8358，累计8169分钟；实际资金费、各自现金/q/entry/risk/日上下文及完整前缀独立核验，0新日决策/成交。

本窗逐笔资金费见current_actual_nov10_16_funding_verification.json，当前记录数{'candidate': 0, 'l4h02': 6, 'fewm': 6}。Nov10_00、08及当日日决策在三条完整账链中各自恰好一次，Nov9旧16也不重复。SMA本轮3倍累计仍为−7.468958%，负结果及全部partial淘汰保留，继续原180日计划；这些是未成熟延迟闭合行情shadow，不等于paper10十策略真实报价模拟。SMA日上下文继续031055轮65个完整SPOT日、截至Nov10 UTC00:00，minute数组不替换日上下文。

下轮SMA/single UTC14:30–16:30：single需用本轮已验证的真实Nov10_16.002公共字段和自己原持仓/现金结算一次；SMA只mark。L4/FEWM16:10–18:10只mark/risk，不重复16结算。所有账户下一日事件为Nov11 UTC00:01，非上海本地午夜；届时SMA从当前Float现金/q/desired继续，日模板PREV/DAILY/日期须在reserve前更新并刷新65个已完成SPOT日。保持冻结规则/本金/仓位/账本，不采用本轮研究策略。

下一批仅提案、未执行：固定L5、S16/D3/K0.75%、H2%/E0.75%和资金费M4/BUDGET_VW8/R0.00875，向下检验PRICE_V6/7/8 × VC4.5%/5%/5.5%，观察V8边界及低回撤是否形成邻域。旧V8/VC5%本轮实际结果必须只读，其他实参先全账本/数值图查重，再冻结代码/spec与代表V7/VC5%、独立样本波动/因果检查和reserve。两窗口分离，资本/名义金额/raw权重/成本/时间/门槛保持；不预认改善，不新建冻结账户。

只读网页：原生snapshot及monitor_snapshot检查均通过；研究10222行，旧10206行完整保持，paper10共10账户/321观察，gzip4677569字节，当前新结果待展示0项。使用同一main锁执行原生脚本，快照只读已存账户/报告，没有新回测、模拟成交、重新部署或新定时任务。

真实失败留档：本轮共7条事实；源匹配、修补语法、原账户cutoff字段、误复制旧helper回执、缺公共复用元数据均在金融/账户计算前发现并修复；封存前staging曾与只读Git检查争用index.lock，git add真实退出128，等待原检查结束后按同一范围重试，不删除锁或改金融结果。原native失败与源码/日志保留。HTTP/传输实际失败0次，失败响应/stderr若有则完整保留，TLS验证未关闭。5项预期合成RED另列。策略回测与已完成账户窗口均未重跑，实际报告原字节和已finish收益不改。

少量继承打印文本/键名含旧S/D、K/VC、H/E、预算或matchedF75标签，统一以derived_label_correction.json、完整L/PRICE_V spec、绑定代码与实际独立审计为准，不改写历史证据。全部逐折/逐变体结果、负收益、真实失败、冻结账户全账本及核验必需数据保留；可重建中间文件已清理。复现命令、cwd/UTC/退出码、真实源哈希见reproduction_history.json及commands/receipts。

main排他锁内完成登记、核验、快照及封存；随后普通非force提交推送并独立核对远端ref、完整tree/必需blob及三条永续链，再释放锁。本文不单独作为push成功证明，实际终态保存于.git/automation_proofs/20261110T171502Z.json。
