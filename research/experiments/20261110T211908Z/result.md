完成快ROC L×有限EWM S批次16配置、48个成本场景：2/8个父组合历史通过（L5/S12、L5/S20），6个父组合因盈利月数不足、8个ETH组件因近期折和局部近期一致性不足淘汰。三档全期均净负配置数0，全期正收益不免除失败判据；全部逐折负收益和淘汰结果保留。预设L5/S12三倍净收益12.795231%、连续整体DD2.434735%。旧L5/S16只读中心为14.794144%/2.434735%；新代表收益下降，DD按六位小数相同，没有新增收益改善。

固定PRICE_V6/VC5.5%、资金费M4/BUDGET_VW8/R0.00875、D3/K0.75%、H2%/E0.75%，联合检验快ROC L4/5/6与有限归一化EWM S12/16/20，挑战上轮描述性角点的快窗口脆弱性。旧L5/S16只读，其余8组件+8组合先reserve后算48场景。事前代表L5/S12。沿用完全相同执行器，不虚构缺参数域或改核算；资本/N/raw[1,1]/成本/日历/门槛不变。原SMA/single16:30至18:30和L4/FEWM18:10至20:10只mark/risk，不重复已各自一次的Nov10_16.002，无新日决策、成交或研究规则采用。

完整读取32404事件/16080ID、375份既往结论、指定技能/README/OOS检查和原ZIP实际结果。初始16项证据齐全（11正式+5原ZIP），5个legacy false标志和旧记录保持，不重复已经实际测试的具体定义。此前规范研究定义10679、标实际10466、未标实际213，不把代码检查称回测或断言全部登记有结果。全部16份spec及数值父组件图先查重并reserve成功后才计算，全部finish。10个旧结果、6个旧原生银行/18成本路径只读；另12项原账户实际观察，共28ID/56事件。

假设是原价格波动角点的收益可能依赖快ROC或EWM窗口，联合变L4/5/6和S12/16/20检验这种脆弱性。固定PRICE_V6/VC5.5%、趋势斜率滞后D3、严格±K0.75%、入场H2%/保留退出E0.75%。r=最近完成日收盘/前L日收盘−1，r>H空、r<−H多，区间内仅按严格E保留实际仓位。有限S归一化均值的beta=(S−1)/(S+1)，当前完成窗口与D日前同窗口相比。趋势/价格波动门槛仅约束新开或反手，同向实际数量不重置，反手先平，信号后下一UTC00:01 OPEN成交。

整个执行器与上一轮逐字节和全部函数AST完全相同，复用已有动态L/S参数化，没有修改策略核算或虚构缺参数域故障。351组独立Fraction ROC、Horner有限归一化EWM、衰减/窗口宽度、样本波动、严格H/E、持仓反手和未来隔离检查通过；另33组价格/斜率边界和360次资金费预算分离检查通过。5项RED均为明确的合成内存故障注入，分别强行S宽16、重复资金加权、强行旧价格上限5%、采用未来资金费、强行旧价格窗口8；真实基线一直支持所用域且通过检查，没有实际回测重跑。

资金费预算BUDGET_VW仍为8日，独立于PRICE_V6。UTC00:00信号仅使用available_ts≤信号、结算年龄1–36小时的最新4笔SIGNED真实费率，偶数median取中间两项均值。max(拟开方向×median,0)≤min(0.0002,0.00875×过去8日样本logvol×最新成熟真实结算间隔小时/24)才允许新开。间隔取最新合格fundingTime减直接上一笔真实时间，保留毫秒抖动且两笔均已可用；名义8小时不是实测间隔。缺必要记录/间隔只阻新开。每资产1212笔实际资金费和370次来源选择核验；结算后1小时可用是建模假设，非历史网络到达证明，过去费率不等于未来费率。

最大ETH信号上下文23日（S20+D3），成本21日，PRICE需7个收盘、预算9个收盘；33日源上下文覆盖ETH23和BTC30。Walk-forward实际执行2025-10-19 UTC00:01至2026-10-24 UTC00:01连续370日，12个完整30日折+10日尾；近期40日继承day330实际现金/持仓，分8个5日折，折间不重开。624条逐折、384条近期折、17808条日净值及完整路径整体DD保存，终点flat含成本。不拟合/不产生标签，purge/embargo不适用；历史反复用于开发，不能称未触碰最终测试集、独立确认或未来证明。8份真实归一化源的版本、SHA256和必要原始数据留存。

敏感性完成：原生/父组合各9格（8新+1旧L5/S16中心）、72邻接边，三档净收益、整体DD、Sharpe、Calmar和近期折完整保存。两类各9/9格全期Sharpe为正，仍存在显著描述性邻接跳变，峰值在只读旧中心而非新格。父组合近期均6/8正折，6个L4/L6组合仅7或8/12正完整月，淘汰；L5/S12为9/12、L5/S20为10/12，满足原门槛。ETH近期仅1–2/8、局部严格近期比例0，全8项淘汰。快L一日变化仍明显恶化收益/回撤，不能把全期正Sharpe解释为稳定跨参数平台。旧canonical资格和敏感性不改，本轮诊断另存。

原失败判据保持：各成本全期/近期净正，1x≥9/12正完整月折，近期各档≥6/8正5日折，3x整体DD≤25%，局部3x净正及严格近期比例≥60%，≥4次原生平仓，毛价格PnL加净资金费/1x执行成本≥2.5，无现金/订单/保证金代理违规，终点flat且≥180日。不能因为正收益而放宽门槛，也不能把不合格ETH组件称单独合格策略。

1/2/3倍成本完成：每边手续费5bp+半价差1bp+滑点2bp，成交量冲击=0.5×过去20日样本logvol×sqrt(实际abs(q)×原生OPEN/过去20日quoteADV)。执行成本及资金费支出随倍数放大，正资金费收入不放大。线性永续不借现货，按实际time/rate/mark和自身持仓入账；检查LOT/tick/minnotional、≤0.1%参与率、费后1倍抵押及1%已闭合小时不利mark保证金代理。缺真实L2/TCA、完整历史风险档位、逐tick强平及实盘容量证明。

组合raw[1,1]直接相加两个独立完整银行：旧BTC29/H3%/E1%、本金3750/N1000；新ETH本金15000/N4500，逐项实际模拟数量、LOT、成本、冲击、资金费与完整NAV。总本金18750，20%/80%是资本份额，不再加权、不归一化、不缩放源NAV、不转移资金、不再平衡、无父订单或交叉抵押。同期常持有、现金0%、旧中心、旧价格控制和同C/N无过滤控制完整保存；多参数不同的控制仅作描述，不把全部差异归因于资金费。previous_budget_center和matchedF75等是继承键名，本轮secondary为旧V8/VC5%价格控制，资金费预算不变；以勘误及完整spec为准。

|范围|L|S|1x净%|2x净%|3x净%|3x整体DD%|月正/12|近期正折1/2/3|状态|
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|native|4|12|10.358157|9.367613|8.377284|5.675105|8|1/1/1|rejected|
|native|4|16|13.139389|11.994388|10.849235|5.661577|8|2/2/2|rejected|
|native|4|20|11.753937|10.542779|9.331609|6.870964|9|2/2/2|rejected|
|native|5|12|15.178691|14.456163|13.734061|3.286613|8|1/1/1|rejected|
|native|5|20|14.692313|13.856580|13.021309|4.477367|10|2/2/2|rejected|
|native|6|12|1.600224|1.136281|0.673076|7.824811|6|1/1/1|rejected|
|native|6|16|4.989637|4.371238|3.753479|7.954863|7|1/1/1|rejected|
|native|6|20|3.390504|2.699203|2.008541|8.084186|7|1/1/1|rejected|
|parent|4|12|10.686426|9.598030|8.509810|5.461921|8|6/6/6|rejected|
|parent|4|16|12.911412|11.699450|10.487370|5.451489|8|6/6/6|rejected|
|parent|4|20|11.803050|10.538163|9.273270|6.420464|8|6/6/6|rejected|
|parent|5|12|14.542854|13.668870|12.795231|2.434735|9|6/6/6|passed|
|parent|5|20|14.153751|13.189204|12.225030|4.593283|10|6/6/6|passed|
|parent|6|12|3.680080|3.012965|2.346444|6.149379|8|6/6/6|rejected|
|parent|6|16|6.391610|5.600930|4.810765|6.066386|8|6/6/6|rejected|
|parent|6|20|5.112304|4.263302|3.414815|6.145821|7|6/6/6|rejected|
|native旧中心|5|16|17.992468|17.112353|16.232701|3.286613|10|2/2/2|rejected|
|parent旧中心|5|16|16.793876|15.793822|14.794144|2.434735|10|6/6/6|passed|


逐项淘汰理由：{'lsvolcarry_370_ETH_L4_S12': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lsvolcarry_370_ETH_L4_S16': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lsvolcarry_370_ETH_L4_S20': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lsvolcarry_370_ETH_L5_S12': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lsvolcarry_370_ETH_L5_S20': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lsvolcarry_370_ETH_L6_S12': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lsvolcarry_370_ETH_L6_S16': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lsvolcarry_370_ETH_L6_S20': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lsvolcarry_370_parent_BTC29H3_ETH_L4_S12': ['nine_of_twelve_positive_complete30d_1x_folds'], 'lsvolcarry_370_parent_BTC29H3_ETH_L4_S16': ['nine_of_twelve_positive_complete30d_1x_folds'], 'lsvolcarry_370_parent_BTC29H3_ETH_L4_S20': ['nine_of_twelve_positive_complete30d_1x_folds'], 'lsvolcarry_370_parent_BTC29H3_ETH_L6_S12': ['nine_of_twelve_positive_complete30d_1x_folds'], 'lsvolcarry_370_parent_BTC29H3_ETH_L6_S16': ['nine_of_twelve_positive_complete30d_1x_folds'], 'lsvolcarry_370_parent_BTC29H3_ETH_L6_S20': ['nine_of_twelve_positive_complete30d_1x_folds']}。独立审计24新原生+24新父组合+18旧成本曲线，8880次新决策、46620条资金费、1116笔新旧成交、924项全期/逐月指标、141609项风险检查通过，0订单拒绝。独立Fraction/Horner、真实数量/现金/价差/冲击/资金费和全NAV重建，不调用新simulate/decide/trade。

同C/N旧路径比对550个原生、260个组合，本轮0个新定义复现既往三档完整NAV，内部别名组0。路径新颖也不构成独立市场数据，完整源/哈希与比较留档。预设L5/S12的整体DD六位小数与旧中心相同、收益降低；L5/S20三倍收益12.225030%、整体DD4.593283%，也未改善旧中心。没有按事后峰值更换预设代表或调整门槛。

原四账户按各自原规则、本金和持仓延续：SMA/single UTC16:30–18:30，L4/FEWM18:10–20:10，均仅闭合mark/risk。本窗0新资金费、0日决策、0成交。三条完整永续链确认Nov10_00、08、16:00:00.002及当日日决策各自一次，旧资金费未重复。仅复用原实际公共字段和来源哈希，不复制他人现金流；当前没有新公共资金费抓取或未来费率预测。

SMA完整NAV前缀57190→57310，累计57269分钟；各自cash/q/entry/desired/成本/风险/上下文及完整前缀独立核验，冻结规则未采用研究新参数。

single完整NAV前缀21635→21757，累计21269分钟；各自cash/q/entry/desired/成本/风险/上下文及完整前缀独立核验，冻结规则未采用研究新参数。

L4完整NAV前缀14372→14494，累计14169分钟；各自cash/q/entry/desired/成本/风险/上下文及完整前缀独立核验，冻结规则未采用研究新参数。

FEWM完整NAV前缀8480→8602，累计8409分钟；各自cash/q/entry/desired/成本/风险/上下文及完整前缀独立核验，冻结规则未采用研究新参数。

SMA3倍累计仍−7.468958%，负结果及全部partial淘汰保留，继续原长期计划；未成熟延迟闭合行情shadow不等于paper10十策略真实报价模拟或180日资格。SMA日上下文保留031055轮65个完整SPOT日、截至Nov10 UTC00:00，当前minute数组不替换日上下文。

下轮SMA/single UTC18:30–20:30、L4/FEWM20:10–22:10只mark/risk，不重复资金费。所有账户下一日决策Nov11 UTC00:01，非上海午夜；后续跨Nov11_00时，须等真实参考闭合取得新实际资金费字段，并在reserve前更新PREV/DAILY/日期及原现金/q、完整日量/日收盘上下文，SMA刷新65个已完成SPOT日。不得用Nov10字段代替Nov11，或提前评估尚未闭合的窗口。

下一批仅提案、未执行：固定L5/S16/D3/K0.75%、PRICE_V6/VC5.5%、资金费M4/BUDGET_VW8/R0.00875，联合检验入场H1.75%/2%/2.25%和保留退出E0.625%/0.75%/0.875%，挑战滞回/换手敏感性。旧H2%/E0.75%只读，其他完整实参先查重；预设H2%/E0.625%，保存spec并reserve后算。已有动态执行器支持这些域，复用且做明确故障注入/独立边界、保留、反手及因果检查，不虚构缺参数域。信号19日/成本21日，33日源覆盖BTC30；资本/N/raw权重、成本、日历、门槛不改，不预认改善、不建新账户。

只读监控：原生snapshot及monitor_snapshot检查通过。研究10254行、旧10238行逐字典保持，paper10为10账户/323观察，gzip4695172字节，本轮待展示0项。仅在同一main锁内汇总已有账户/报告，没有新增回测/模拟成交、冻结变更、网页重部署或新定时任务。

真实非预期失败事实0条，HTTP/传输失败1次；若有，原响应/stderr/有界重试完整保留，TLS验证未关闭。5项RED为刻意合成内存故障，和真实运行失败分开。所有金融配置和已完成账户窗口仅实际执行一次，未删除负收益或改写已finish报告。部分继承stdout/键名仍有旧PRICE_V/VC、S/D、K/VC、matchedF75等字样，以完整L/S spec、绑定代码和derived_label_correction.json为准。

复现argv、cwd、UTC和退出码见reproduction_history.json及commands/receipts；真实数据哈希、完整结果/账本、冻结规则与核验必需证据保留，可重建中间文件清理。main锁内封存后普通非force提交push，独立核对远端ref、完整tree/必需blob及三条账户链，再释放锁。实际终态保存在.git/automation_proofs/20261110T211908Z.json；本文不单独作为push成功证明。
