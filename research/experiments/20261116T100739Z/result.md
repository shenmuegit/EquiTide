本轮完成6个新金融配置：BTC严格短周期方向确认W4/6两个组件，固定风险窗口V10与上限2.75%、L29/H3%/E0.5%，与已有ETH预算R=.00875/.01组成四父组合，18条1/2/3倍成本场景。历史通过6个：4父+2BTC；淘汰0个。8旧实际配置/24场景只读；12项原账户窗口各自reserve/finish，partial rejected表示尚未成熟180日，不取消原长期计划。

假设与预设：固定29日ROC信号下，4/6完成日近期走势严格同向确认可能避开近期反转，但也可能延迟趋势入场。固定W=[4,5,6]×ETH R=[.00875,.01]，旧W5已确认银行只读、位于中心，事前代表W4/R.01；不事后换成其他格或扩批。完整读取20个固定BTC既往定义、全部登记与结论，未见当前4/6日严格同向定义，六新指纹逐个查重和预登记。

BTC规则：本金3750/名义1000；完成L29 ROC严格>3%多、<−3%空，带内实际多仅ROC>−0.5%、空仅ROC<0.5%保留，相等退出，原入场优先。仅新或反手先检查过去V10日无偏样本logvol≤2.75%，再要求d×(C[i-1]/C[i-1-W]−1)>0，W为4或6完成日；近期收益等于0也阻新仓，同向已有q及正常退出不变。W5为原实际确认银行，只读；新两档完整重算391日。下一00:01 OPEN、不利tick/LOT、原费用/滑点/过去20日冲击/实际资金费/保证金核算不改；不使用未来后缀。

ETH只读：本金15000/名义4000，long-only L5/H2%/退出E0.75%，有限归一化EWMS16 beta15/17、D3严格K0.75%、V6 cap5.625%；最近4笔实际已实现有符号资金费中位数，信号前1–36小时且available≤signal合格，缺4笔阻新仓。预算min(.0002,R×过去V8样本logvol×最新合格过去实际结算间隔小时/24)。R原值.00875/.01，仅新入场过滤，原同向q/退出不变。旧ETH文字E.005过期而机器E.0075，旧spec/报告/status原字节保持。

父组合本金18750/raw[1,1]直接相加BTC3750与ETH15000两个原规模银行的美元NAV，20/80仅初始本金占比，权重不归一化。无缩放、转账、再平衡、父订单或跨保证金；对齐完整事件时间轴后重算组合NAV与整体DD，不平均收益/Sharpe/回撤。

完整读取36640登记事件/18181ID、440份结论、去除观察后的11359个规范化研究定义（不等于独立试验）、task/README/三技能、checks/*oos.py及freqtrade原ZIP。初始16条均有实际证据，缺实际结果0，旧legacy/false及负结果保留；旧paper失败观察不补单重跑。保护82057旧文件，main上原报价、账本和缺口保持。

Walk-forward已执行：2025-10-19T00:01Z→2026-11-14T00:01Z，391日/33日背景。每币610562分钟bar、10176小时mark、1273实际资金费，8份Parquet SHA、单位、闭合/可得时间及连续性核验。固定规则无训练/标签，仅使用完成前缀；13完整30日折+1日尾折，现金/持仓跨折连续，全期终止才按成本平仓，整体DD用完整事件NAV。近40日8×5及扩展21日5+5+5+6逐折保存，尾折Sharpe=None不计完整正月；无标签故无标签purge用途，背景/下一OPEN/资金费成熟另核验。OOS字样沿用机器字段，实际是复用开发历史。

Sensitivity已执行：BTC近期方向确认W三档×ETH R两档六格；BTC组件只沿W轴，ETH只沿R。全部净收益、整体DD、Sharpe、Calmar、近期正折、10相邻变化和并列最优边界保留。局部3倍净正与严格近期合格比例各≥60%；小邻域/两档ETH不能证明宽平台，不事后扩批/换代表。相同NAV若出现须披露，参数不同仍分别登记，不能当独立样本。

Costs已执行：每边费5bp+半价差1bp+滑点2bp+0.5×过去20日样本logvol×sqrt(abs(q)×真实OPEN/过去20完整日quoteADV)，不利tick与实际LOT/minnotional；参与率≤0.1%，费后1倍抵押，闭合小时high/low的1%维持保证金代理。执行成本与负资金费1/2/3倍，收入不放大；线性永续无需借现货，不编借币费。含逐项费用、交易数/成本占比、持有与现金0比较；冻结费率/盘口为估计，缺历史L2/TCA、完整档位、tick强平和真实容量证明。

冻结门槛：三成本全期/近期净正；1倍≥10/13正完整月；近期各成本≥6/8正5日折；扩展21日三成本净正且≥3/4正折；3倍DD≤25%；两项适用局部比例≥60%；至少4底层平仓；1倍(毛价格PnL+净资金费)/执行成本≥2.5；无拒单、负抵押或保证金代理违规，期末平仓且≥180日。任一失败即rejected，结果仍保留。

|BTC近期确认W日|ETH R|来源/状态|1x净%|2x净%|3x净%|3x整体DD%|正月/13|近期正折1/2/3|
|---:|---:|---|---:|---:|---:|---:|---:|---|
|4|0.00875|新/passed|9.258691640|8.698444289|8.138401254|1.357571952|12|6/6/6|
|4|0.01|新/passed|9.197095829|8.633010129|8.069128745|1.357571952|12|6/6/6|
|5|0.00875|旧只读/passed|9.329762905|8.778151221|8.226725725|1.358487577|12|6/6/6|
|5|0.01|旧只读/passed|9.268167095|8.712717061|8.157453216|1.358487577|12|6/6/6|
|6|0.00875|新/passed|9.187705615|8.627439659|8.067376914|1.358487577|12|6/6/6|
|6|0.01|新/passed|9.126109804|8.562005499|7.998104405|1.358487577|12|6/6/6|


事前代表W4/L29/H3%/E0.5%/V10/R.01（3ae9b18479ab314ff967e3856f5a6b3e86ed21f0d39fe5287dbdf782be6f7ec9）：三成本净9.197095829%/8.633010129%/8.069128745%，3倍DD1.357571952%，Sharpe2.295081820、Calmar5.534079207，passed，失败项[]。

BTC近期确认W4日/L29/H3%/E0.5%/V10组件passed：三成本净17.770648016%/16.454314743%/15.138162804%，3倍DD5.680706071%，Sharpe1.480171085、Calmar2.475741634，正月10/13、近期{'1': 6, '2': 6, '3': 6}，失败项[]。

BTC近期确认W6日/L29/H3%/E0.5%/V10组件passed：三成本净17.415717893%/16.099291592%/14.783041105%，3倍DD5.789755227%，Sharpe1.449594373、Calmar2.372382194，正月10/13、近期{'1': 6, '2': 6, '3': 6}，失败项[]。

各新组件与父组合的真实通过状态、完整正月、近期正折和失败项按上表/逐项结果保存。组合资格不能替代组件资格；ETH扩展21日PnL若为0，该段父利润仅来自BTC，旧ETH状态不改。代表始终W4/R.01，不事后换成其他格。

配对旧W5：新W4/R0.00875，3倍净变化-0.088324471个百分点、整体DD变化-0.000915625个百分点、Sharpe-0.033163978、Calmar-0.056614884。

配对旧W5：新W4/R0.01，3倍净变化-0.088324471个百分点、整体DD变化-0.000915625个百分点、Sharpe-0.033093313、Calmar-0.056649395。

配对旧W5：新W6/R0.00875，3倍净变化-0.159348811个百分点、整体DD变化+0.000000000个百分点、Sharpe-0.051216830、Calmar-0.108929979。

配对旧W5：新W6/R0.01，3倍净变化-0.159348811个百分点、整体DD变化+0.000000000个百分点、Sharpe-0.051164401、Calmar-0.108934620。

相对匹配ETH预算的旧W5，四项指标同时严格改善（净收益增、整体DD降、Sharpe增、Calmar增）的新父数量0/4。所有收益/回撤代价按上述原数值披露，不能只选单一最好格；各指标及并列最优的边界信息另存sensitivity_metric_boundaries.json。小3×2邻域、两档ETH及重复历史不能证明宽平台，全部启发标记保留，待独立未来。

六新配置全成本NAV签名6组，匹配8旧参考0组，匹配上轮实际新/只读路径0/6；原始abs(deltaSharpe)>2×sampleSTD(absdeltas)标记4/10，绝对变化范围[0.019213255649568328, 0.08522681017553979]、STD0.021311566，不是显著性或过拟合概率。三倍净正/正Sharpe/严格近期比例1.0/1.0/1.0。

另只读9个同规模旧BTC总波动率上限组件和18个对应父组合；本轮0/6匹配该集合的全成本路径，比较范围与8个预声明参考/上一批分开。新参数/路径也不是独立市场样本或未来证据；全部失败项保留，本轮所有通过/淘汰状态仅针对复用历史，不能把邻域改善称宽平台或独立未来，不事后改网格或原账户。

匹配持有3倍净-14.782911083%、DD18.454766592%，现金0；18父成本场景BTC/ETH利润守恒。独立审计新原生6/新父12、旧原生15/旧父9条，新决策2346、旧只读5865；42场景、588逐折、336近期折、168扩展折、16464日NAV、18持有对照、10邻边/图均保存。资金核算核心与上轮原字节一致；策略引擎保持上轮严格近期同向ROC与总波动门控，唯一改动是允许预声明4/6日参数；simulate、货币/资金费辅助函数AST、ETH分支与核算核心保持；全部辅助公式保持，AST仅允许参数白名单差异。合成检查独立计算近期ROC方向、严格零边界、已有仓位、W0等价、真实入口及未来后缀。显式生成本轮规则说明，reserve前逐个核对标量/轴/描述并保存signal_scalar_consistency_before_reservation.json；36个严格阈值/真实持仓/未来后缀合成检查通过后绑定、预登记。本轮所有新配置先成功reserve再完整评估一次，未重跑已完成配置；上轮H2.5/H3.5说明勘误和全部原记录保留，文案修正不算新配置。

原账户SMA/singleNov16_00:30→02:30、L4/FEWM02:10→04:10。新日事件{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、新资金费记录{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、原核算成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}。本轮公共完整窗口实际返回BTC/ETH结算均空，所有账户只追加已闭合分钟；不重复已记Nov16_00结算及00:01原日决策。独立核对自身现金/数量/费用/保证金、旧NAV前缀和全链唯一键。

原SMA沿用上轮68日完整SPOT权威research/experiments/20261116T080637Z/forward_inputs.json.gz，67/66/65前缀逐条相等；指标仍65日、对称1%、本金1500:500/raw75:25与Float核算。原现货手续费10bp+半价差1bp+滑点2bp及过去20日ADV冲击保持，未追溯添加新研究LOT/tick。追加120闭合分钟，新增资产日决策0、参考点0、成交0；累计64949分钟/64996点。原冻结计划和2027-03-31终止日不改，不强制平仓。三倍累计净-7.468957812%，负收益完整保留；未成熟180日，延迟真实历史重建不冒充十策略同时实盘报价成交。

本轮SMA/singleNov16_00:30→02:30，L4/FEWM02:10→04:10；实际新查询BTC/ETH结算均空，全部仅续接标记，不重复已记Nov16_00资金费与00:01决策。SMA使用上轮完整68日现货权威并保留67/66/65前缀，仍SMA65/对称1%/Float。下轮SMA/single02:30→04:30、04:31后闭合；L4/FEWM04:10→06:10、06:11后闭合，仍须新查完整实际结算，不按名义8小时或本轮空结果推断。下一日决策均Nov17_00:01；保持全部原现金/持仓/desired/成本/冻结计划，与十策略实时报价模拟分开。

旧Nov16_00公开源首次捕获UTC2026-11-16T06:10:18.547191Z和原字节不改；本轮新完整窗口查询捕获UTC2026-11-16T10:14:31.403822Z返回空，查询边界00:30→04:10。保留旧Nov13–15_00/08/16和Nov16_00公共原包及各自UTC，不重标时间，不复制其他账户现金流。

有包公共GET 18次，均保存URL/捕获时界/body/gzipSHA；上述行情/结算捕获观察到传输失败0次，本轮两项官方文档读取成功，所有真实失败/恢复（如有）见read_failures.json。FEWM与cached metadata/time精确去重，SMA内部未分包重试数0仅按原stderr/命令时界披露，失败体、资产/URL和精确尝试UTC若原执行器未记录则不编造。

复现与实际执行顺序：cwd=/home/desktop/Documents/Codex/EquiTide，解释器/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B。review/launch.py bootstrap.py review/preflight.py；review/configure_neighbors.py review/setup_confirmation.py review/prepare_confirmation.py；review/configure_report.py；review/execute.py freeze units bind reserve_0 evaluate。原audit遇独立检查错误后，review/repair_audit.py保留原检查并绑定只读补充audit_retry1.py，执行audit_retry1；原exports同一错误修正为适用轴后执行exports_retry1 finish_0 research_check。diagnostics/historical_aliases/totalrisk_history_aliases，实际view_image后visual_review；原账户midnight_archive l4h02 fewm candidate forward accounts_check；account_continuity/complete_transport_audit/validate_sources；journal sources_check gates feed collect final_checks、staged_whitespace、seal/publish。全部实际命令、UTC、退出码、失败及修复回执均保留。以上是原执行记录，不能在已完成目录重复reserve/evaluate或重放账户窗口；复核使用保存的report/archive/raw包及只读审计，forward --reproduce仅使用原包核验。

391日历史与多重选择偏差未消除，无DSR/PBO显著性结论，正收益不代表稳定实盘盈利。本轮已读[Binance官方市场/资金费文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)和[官方公共数据README](https://github.com/binance/binance-public-data/blob/master/README.md)，实际原包/输入SHA是复现依据。

实际失败/阻碍：{"facts": [{"command": ["/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python", "-B", "/home/desktop/Documents/Codex/EquiTide/research/experiments/20261116T100739Z/audit.py"], "cwd": "/home/desktop/Documents/Codex/EquiTide", "started_utc": "2026-11-16T10:17:50.021301Z", "finished_utc": "2026-11-16T10:18:01.561919Z", "exit_code": 1, "log": "research/experiments/20261116T100739Z/audit.log", "stderr": "Traceback (most recent call last):\n  File \"/home/desktop/Documents/Codex/EquiTide/research/experiments/20261116T100739Z/audit.py\", line 103, in <module>\n    rows=plan['grid'] if c['scope']=='parent' else plan['native_grid'];ns=[full[g['fingerprint']] for g in rows if abs(plan['axes']['BTC_RECENT_CONFIRM_DAYS'].index(g['W'])-plan['axes']['BTC_RECENT_CONFIRM_DAYS'].index(c['W']))<=1 and abs(plan['axes']['ETH_FUND_R'].index(g['K'])-plan['axes']['ETH_FUND_R'].index(c['K']))<=1];dims=2\n                                                                                                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nValueError: 0 is not in list\n", "resolved": true, "root_cause": "Independent readonly neighbor/export traversal evaluated unrelated ETH W0 on BTC4/5/6axis before asset filtering", "effective_successful_receipt": "research/experiments/20261116T100739Z/audit_retry1_commands.json", "effective_successful_receipt_sha256": "04417457b45174a8394a8762f47cbc05fdefa2ad19d2de9961768ad336187278", "financial_report_sha256_unchanged": "9d01e5df354dd784a92600e7d98a4476b3bbd233047b420f26b8c645de53b006", "strategy_or_account_reruns": 0}, {"command": ["/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python", "-B", "/home/desktop/Documents/Codex/EquiTide/research/experiments/20261116T100739Z/exports.py"], "cwd": "/home/desktop/Documents/Codex/EquiTide", "started_utc": "2026-11-16T10:20:13.347599Z", "finished_utc": "2026-11-16T10:20:14.504246Z", "exit_code": 1, "log": "research/experiments/20261116T100739Z/exports.log", "stderr": "Traceback (most recent call last):\n  File \"/home/desktop/Documents/Codex/EquiTide/research/experiments/20261116T100739Z/exports.py\", line 29, in <module>\n    if abs(p['axes']['BTC_RECENT_CONFIRM_DAYS'].index(a['W'])-p['axes']['BTC_RECENT_CONFIRM_DAYS'].index(b['W']))+abs(p['axes']['ETH_FUND_R'].index(a['K'])-p['axes']['ETH_FUND_R'].index(b['K']))!=1:continue\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nValueError: 0 is not in list\n", "resolved": true, "root_cause": "Independent readonly neighbor/export traversal evaluated unrelated ETH W0 on BTC4/5/6axis before asset filtering", "effective_successful_receipt": "research/experiments/20261116T100739Z/exports_retry1_commands.json", "effective_successful_receipt_sha256": "ccf933a2ddf061c5ea734a7ec9bcfe085a6fa4c4efa3289296546a3982dbd23d", "financial_report_sha256_unchanged": "9d01e5df354dd784a92600e7d98a4476b3bbd233047b420f26b8c645de53b006", "strategy_or_account_reruns": 0}, {"command": ["/usr/bin/python3", "-B", "/home/desktop/Documents/Codex/EquiTide/research/experiments/20261116T100739Z/finalize.py"], "cwd": "/home/desktop/Documents/Codex/EquiTide", "started_utc": "2026-11-16T10:35:13.145537Z", "finished_utc": "2026-11-16T10:35:13.219053Z", "exit_code": 1, "log": ".git/automation_proofs/20261116T100739Z_seal.log", "type": "private_seal_launcher_wrong_system_python", "resolved": true, "native_completion_chunk": "818bae", "preserved_failure_log": "research/experiments/20261116T100739Z/review/first_native_seal.log", "root_cause": "Private launcher inherited system python3; numpy absent there. All actual research/account executions already used existing venv.", "resolution": "Explicit existing research venv dependency import succeeded; launcher now always selects that interpreter. Full seal remains pending separate native receipt.", "successful_dependency_probe": "research/experiments/20261116T100739Z/review/seal_venv_dependency_probe.json", "financial_or_account_valuations": 0}]}。保留所有正/负/淘汰/失败、原账户完整账本/冻结规则/登记、原包、哈希和下轮状态；只清理可重建缓存，大行情忽略。锁内snapshot只读已有账户/报告，不新回测或产生模拟成交，不部署或创建定时任务。真实commit/push、完整远端树/blob和解锁后检查见.git/automation_proofs回执。
