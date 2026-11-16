本轮完成6个新金融配置：BTC严格短周期方向确认A0.25%/0.50%两个组件，固定风险窗口V10与上限2.75%、L29/H3%/E0.5%，与已有ETH预算R=.00875/.01组成四父组合，18条1/2/3倍成本场景。历史通过6个：4父+2BTC；淘汰0个。8旧实际配置/24场景只读；12项原账户窗口各自reserve/finish，partial rejected表示尚未成熟180日，不取消原长期计划。

假设与预设：固定5日近期方向确认，要求最小同向完成ROC超过0/0.25%/0.50%，可能避开微弱噪声入场，但也可能错过早期趋势。A=[0,.0025,.005]×ETH R=[.00875,.01]，A0对应已有5日确认银行，只读、位于下边界；事前代表A.0025/R.01，不事后换格或扩批。完整读取22个固定BTC既往定义与全部登记/结论；六新具体参数指纹先查重再预登记。

BTC规则：本金3750/名义1000，L29完成ROC严格>3%多、<−3%空；入场优先，带内实际多仅ROC>−0.5%、空仅ROC<0.5%保留，相等退出。仅新或反手先核对过去V10无偏样本logvol≤2.75%，再要求d×(C[i-1]/C[i-6]−1)>A，固定5完成日，A=.0025/.005；等于门槛也阻新仓。已有同向q与正常退出保持，旧A0已实际结果只读。两个新银行均从原3750本金按新规则完整计算391日。下一00:01OPEN、LOT/tick、费用/冲击/实际资金费/抵押/保证金规则保持，所有特征只读完成前缀。

ETH只读：本金15000/名义4000，long-only L5/H2%/退出E0.75%，有限归一化EWMS16 beta15/17、D3严格K0.75%、V6 cap5.625%；最近4笔实际已实现有符号资金费中位数，信号前1–36小时且available≤signal合格，缺4笔阻新仓。预算min(.0002,R×过去V8样本logvol×最新合格过去实际结算间隔小时/24)。R原值.00875/.01，仅新入场过滤，原同向q/退出不变。旧ETH文字E.005过期而机器E.0075，旧spec/报告/status原字节保持。

父组合本金18750/raw[1,1]直接相加BTC3750与ETH15000两个原规模银行的美元NAV，20/80仅初始本金占比，权重不归一化。无缩放、转账、再平衡、父订单或跨保证金；对齐完整事件时间轴后重算组合NAV与整体DD，不平均收益/Sharpe/回撤。

完整读取36696登记事件/18209ID、441份结论、去除观察后的11365个规范化研究定义（不等于独立试验）、task/README/三技能、checks/*oos.py及freqtrade原ZIP。初始16条均有实际证据，缺实际结果0，旧legacy/false及负结果保留；旧paper失败观察不补单重跑。保护82419旧文件，main上原报价、账本和缺口保持。

Walk-forward已执行：2025-10-19T00:01Z→2026-11-14T00:01Z，391日/33日背景。每币610562分钟bar、10176小时mark、1273实际资金费，8份Parquet SHA、单位、闭合/可得时间及连续性核验。固定规则无训练/标签，仅使用完成前缀；13完整30日折+1日尾折，现金/持仓跨折连续，全期终止才按成本平仓，整体DD用完整事件NAV。近40日8×5及扩展21日5+5+5+6逐折保存，尾折Sharpe=None不计完整正月；无标签故无标签purge用途，背景/下一OPEN/资金费成熟另核验。OOS字样沿用机器字段，实际是复用开发历史。

Sensitivity已执行：BTC固定5日确认最低收益A三档×ETH R两档六格；BTC组件只沿最低同向收益A轴，ETH只沿R。全部净收益、整体DD、Sharpe、Calmar、近期正折、10相邻变化和并列最优边界保留。局部3倍净正与严格近期合格比例各≥60%；小邻域/两档ETH不能证明宽平台，不事后扩批/换代表。相同NAV若出现须披露，参数不同仍分别登记，不能当独立样本。

Costs已执行：每边费5bp+半价差1bp+滑点2bp+0.5×过去20日样本logvol×sqrt(abs(q)×真实OPEN/过去20完整日quoteADV)，不利tick与实际LOT/minnotional；参与率≤0.1%，费后1倍抵押，闭合小时high/low的1%维持保证金代理。执行成本与负资金费1/2/3倍，收入不放大；线性永续无需借现货，不编借币费。含逐项费用、交易数/成本占比、持有与现金0比较；冻结费率/盘口为估计，缺历史L2/TCA、完整档位、tick强平和真实容量证明。

冻结门槛：三成本全期/近期净正；1倍≥10/13正完整月；近期各成本≥6/8正5日折；扩展21日三成本净正且≥3/4正折；3倍DD≤25%；两项适用局部比例≥60%；至少4底层平仓；1倍(毛价格PnL+净资金费)/执行成本≥2.5；无拒单、负抵押或保证金代理违规，期末平仓且≥180日。任一失败即rejected，结果仍保留。

|BTC最小同向5日ROC A（小数）|ETH R|来源/状态|1x净%|2x净%|3x净%|3x整体DD%|正月/13|近期正折1/2/3|
|---:|---:|---|---:|---:|---:|---:|---:|---|
|0|0.00875|旧只读/passed|9.329762905|8.778151221|8.226725725|1.358487577|12|6/6/6|
|0|0.01|旧只读/passed|9.268167095|8.712717061|8.157453216|1.358487577|12|6/6/6|
|0.0025|0.00875|新/passed|9.350602745|8.807892662|8.265363973|1.357833669|12|6/6/6|
|0.0025|0.01|新/passed|9.289006934|8.742458502|8.196091464|1.357833669|12|6/6/6|
|0.005|0.00875|新/passed|9.350602745|8.807892662|8.265363973|1.357833669|12|6/6/6|
|0.005|0.01|新/passed|9.289006934|8.742458502|8.196091464|1.357833669|12|6/6/6|


事前代表A.0025/L29/H3%/E0.5%/V10/R.01（f0f50c44f08cb28f92147b31b07af0c1f2551d43e449949dbad8398d40046e25）：三成本净9.289006934%/8.742458502%/8.196091464%，3倍DD1.357833669%，Sharpe2.342950470、Calmar5.619846128，passed，失败项[]。

BTC最小5日ROC门槛A=0.0025（收益率小数）/L29/H3%/E0.5%/V10组件passed：三成本净18.230203542%/17.001556610%/15.772976398%，3倍DD5.775982000%，Sharpe1.561251005、Calmar2.536525438，正月10/13、近期{'1': 6, '2': 6, '3': 6}，失败项[]。

BTC最小5日ROC门槛A=0.005（收益率小数）/L29/H3%/E0.5%/V10组件passed：三成本净18.230203542%/17.001556610%/15.772976398%，3倍DD5.775982000%，Sharpe1.561251005、Calmar2.536525438，正月10/13、近期{'1': 6, '2': 6, '3': 6}，失败项[]。

各新组件与父组合的真实通过状态、完整正月、近期正折和失败项按上表/逐项结果保存。组合资格不能替代组件资格；ETH扩展21日PnL若为0，该段父利润仅来自BTC，旧ETH状态不改。代表始终A.0025/R.01，不事后换成其他格。

配对旧A0（5日）：新A0.0025/R0.00875，3倍净变化+0.038638248个百分点、整体DD变化-0.000653908个百分点、Sharpe+0.014808349、Calmar+0.029139205。

配对旧A0（5日）：新A0.0025/R0.01，3倍净变化+0.038638248个百分点、整体DD变化-0.000653908个百分点、Sharpe+0.014775337、Calmar+0.029117526。

配对旧A0（5日）：新A0.005/R0.00875，3倍净变化+0.038638248个百分点、整体DD变化-0.000653908个百分点、Sharpe+0.014808349、Calmar+0.029139205。

配对旧A0（5日）：新A0.005/R0.01，3倍净变化+0.038638248个百分点、整体DD变化-0.000653908个百分点、Sharpe+0.014775337、Calmar+0.029117526。

相对匹配ETH预算的旧A0，四项指标同时严格改善（净收益增、整体DD降、Sharpe增、Calmar增）的新父数量4/4。所有收益/回撤代价按上述原数值披露，不能只选单一最好格；各指标及并列最优的边界信息另存sensitivity_metric_boundaries.json。小3×2邻域、两档ETH及重复历史不能证明宽平台，全部启发标记保留，待独立未来。

六新配置全成本NAV签名3组，匹配8旧参考0组，匹配上轮实际新/只读路径0/6；原始abs(deltaSharpe)>2×sampleSTD(absdeltas)标记2/10，绝对变化范围[0.0, 0.026429821723476854]、STD0.010392959，不是显著性或过拟合概率。三倍净正/正Sharpe/严格近期比例1.0/1.0/1.0。

本轮0.25%与0.50%门槛的BTC全成本资金路径相同，其391日目标、前后持仓状态、全部成交和资金费逐项相等；同ETH预算父组合相同。因此六个新配置只有三组不同资金路径，不增加独立市场样本。各参数指纹仍分别保存真实登记，事前代表A.0025/R.01不换格。匹配旧零门槛组合的净收益改善约0.038638个百分点、整体回撤下降约0.000654个百分点，幅度很小，无显著性或宽平台结论。逐项核验见new_variant_alias_state_verification.json和NAV_alias_inventory.json。

微小改进分解（保存结果只读）：BTC每个成本场景减少2次执行，3倍毛价格PnL变化+2.831100000USDT、净资金费变化-0.391668131、执行费用变化-4.805239650，净改善+7.244671519USDT。ETH路径不变，因此在18750父本金中仅约0.038638个百分点；成本节省是主要部分，不能把约7.24USDT历史差异解释为显著或稳定收益。

另只读9个同规模旧BTC总波动率上限组件和18个对应父组合；本轮0/6匹配该集合的全成本路径，比较范围与8个预声明参考/上一批分开。新参数/路径也不是独立市场样本或未来证据；全部失败项保留，本轮所有通过/淘汰状态仅针对复用历史，不能把邻域改善称宽平台或独立未来，不事后改网格或原账户。

匹配持有3倍净-14.782911083%、DD18.454766592%，现金0；18父成本场景BTC/ETH利润守恒。独立审计新原生6/新父12、旧原生15/旧父9条，新决策2346、旧只读5865；42场景、588逐折、336近期折、168扩展折、16464日NAV、18持有对照、10邻边/图均保存。资金核算核心与上轮原字节一致；策略引擎保持固定5日同向确认与原总波动门控，唯一策略改动是要求同向ROC严格超过预声明25/50bp；simulate、货币/资金费辅助函数AST、ETH分支与核算核心保持；确认过滤及BTC分支只增加最小门槛，ETH分支、全部其他策略/货币/资金费辅助函数与simulate AST保持。合成检查独立计算近期ROC方向、严格零边界、已有仓位、旧A0等价、真实入口及未来后缀。显式生成本轮规则说明，reserve前逐个核对标量/轴/描述并保存signal_scalar_consistency_before_reservation.json；171个严格阈值/真实持仓/未来后缀合成检查通过后绑定、预登记。本轮所有新配置先成功reserve再完整评估一次，未重跑已完成配置；上轮H2.5/H3.5说明勘误和全部原记录保留，文案修正不算新配置。

原账户SMA/singleNov16_02:30→04:30、L4/FEWM04:10→06:10。新日事件{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、新资金费记录{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、原核算成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}。本轮公共完整窗口实际返回BTC/ETH结算均空，所有账户只追加已闭合分钟；不重复已记Nov16_00结算及00:01原日决策。独立核对自身现金/数量/费用/保证金、旧NAV前缀和全链唯一键。

原SMA沿用上轮68日完整SPOT权威research/experiments/20261116T080637Z/forward_inputs.json.gz，67/66/65前缀逐条相等；指标仍65日、对称1%、本金1500:500/raw75:25与Float核算。原现货手续费10bp+半价差1bp+滑点2bp及过去20日ADV冲击保持，未追溯添加新研究LOT/tick。追加120闭合分钟，新增资产日决策0、参考点0、成交0；累计65069分钟/65116点。原冻结计划和2027-03-31终止日不改，不强制平仓。三倍累计净-7.468957812%，负收益完整保留；未成熟180日，延迟真实历史重建不冒充十策略同时实盘报价成交。

本轮SMA/singleNov16_02:30→04:30，L4/FEWM04:10→06:10；新完整窗口实际BTC/ETH结算均空，全部仅续接标记，不重复Nov16_00与原00:01决策。SMA65/对称1%/Float及完整68日SPOT权威、67/66/65前缀保持。下轮SMA/single04:30→06:30、06:31后闭合，L4/FEWM06:10→08:10、08:11后闭合；后者须新查完整实际结算边界，不假定名义08时刻或零，不用本轮空结果代替下轮查询。全部下一日决策Nov17_00:01，不采用新研究参数，不重置账户，旧延迟shadow与十策略实时报价模拟分开。

旧Nov16_00公开源首次捕获UTC2026-11-16T06:10:18.547191Z和原字节不改；本轮新完整窗口查询捕获UTC2026-11-16T12:11:56.527673Z返回空，查询边界02:30→06:10。保留旧Nov13–15_00/08/16和Nov16_00公共原包及各自UTC，不重标时间，不复制其他账户现金流。

有包公共GET 18次，均保存URL/捕获时界/body/gzipSHA；上述行情/结算捕获观察到传输失败0次，本轮两项官方文档读取成功，所有真实失败/恢复（如有）见read_failures.json。FEWM与cached metadata/time精确去重，SMA内部未分包重试数0仅按原stderr/命令时界披露，失败体、资产/URL和精确尝试UTC若原执行器未记录则不编造。

复现与实际执行顺序：cwd=/home/desktop/Documents/Codex/EquiTide，使用既有/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B。review/launch.py bootstrap.py review/preflight.py；configure_hurdle.py准备后，排版定位错误按原失败回执保留，仅configure_hurdle_finish.py恢复尚未执行的只读部分；setup_confirmation.py prepare_confirmation.py configure_report.py；review/execute.py freeze units bind reserve_0 evaluate audit exports finish_0 research_check；diagnostics/historical_aliases/totalrisk_history_aliases与hurdle_effect，实际view_image后visual_review；原账户midnight_archive l4h02 fewm candidate forward accounts_check；account_continuity/complete_transport_audit/validate_sources；journal sources_check gates feed collect final_checks，staged_whitespace，既有venv运行封存/发布助手。命令UTC/退出码/失败原日志均保留，不能在已完成目录重复reserve/evaluate或重放已完成账户窗口；只读复核保存的report/archive/raw包，forward --reproduce只用原包核验。

391日历史与多重选择偏差未消除，无DSR/PBO显著性结论，正收益不代表稳定实盘盈利。本轮已读[Binance官方市场/资金费文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)和[官方公共数据README](https://github.com/binance/binance-public-data/blob/master/README.md)，实际原包/输入SHA是复现依据。

实际失败/阻碍：{"facts": [{"command": ["/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python", "-B", "/home/desktop/Documents/Codex/EquiTide/research/experiments/20261116T120809Z/review/configure_hurdle.py"], "cwd": "/home/desktop/Documents/Codex/EquiTide", "started_utc": "2026-11-16T12:13:36.380029Z", "finished_utc": "2026-11-16T12:13:36.690119Z", "exit_code": 1, "log": "research/experiments/20261116T120809Z/review/native_configure_hurdle.py_receipt.log", "type": "prebinding_configuration_formatter_search", "resolved": true, "root_cause": "Whitespace-specific search expected two spaces beforekey;actual formatter hasone. Model edits were already completed and were not reapplied.", "successful_resume_receipt": "research/experiments/20261116T120809Z/review/native_configure_hurdle_finish.py_receipt.json", "financial_or_account_calculations": 0, "reserved_configurations_at_failure": 0}]}。保留所有正/负/淘汰/失败、原账户完整账本/冻结规则/登记、原包、哈希和下轮状态；只清理可重建缓存，大行情忽略。锁内snapshot只读已有账户/报告，不新回测或产生模拟成交，不部署或创建定时任务。真实commit/push、完整远端树/blob和解锁后检查见.git/automation_proofs回执。
