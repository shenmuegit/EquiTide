本轮完成6个新金融配置：BTC退出缓冲E1%/E1.5%两个组件，固定风险窗口V10与波动率上限2.75%，与已有ETH预算R=.00875/.01组成四父组合，18条1/2/3倍成本场景。历史通过5个：4父+1BTC；淘汰1个。8旧实际配置/24场景只读；12项原账户窗口各自reserve/finish，partial rejected表示尚未成熟180日，不取消原长期计划。

假设与预设：固定ROC L29/入场H3%/风险V10/cap2.75%，预声明BTC退出缓冲E=[0.5%,1%,1.5%]×ETH R=[.00875,.01]。更宽滞回可能减少过早退出和换手，但会容忍更多不利波动；旧E0.5%只读且位于边界，不能据此宣称其双侧邻域或全局最优。事前代表E1%/R.01固定；完整新定义先reserve再计算，不事后扩批或换代表，仍为复用开发历史。

BTC规则：本金3750/固定名义1000；完成29日ROC严格>3%多、<−3%空，入场优先；带内实际多仅ROC>−E、空仅ROC<E保留，E为0.5%/1%/1.5%，相等退出。仅新/反手检查过去10个完成日无偏样本log(close/prevclose)波动率≤2.75%，同向q保持。信号可得后的下一00:01 OPEN、不利tick、LOT向下；新E1/E1.5从原现金完整计算391日数量、费用、冲击、资金费和保证金，不缩放旧NAV。

ETH只读：本金15000/名义4000，long-only L5/H2%/退出E0.75%，有限归一化EWMS16 beta15/17、D3严格K0.75%、V6 cap5.625%；最近4笔实际已实现有符号资金费中位数，信号前1–36小时且available≤signal合格，缺4笔阻新仓。预算min(.0002,R×过去V8样本logvol×最新合格过去实际结算间隔小时/24)。R原值.00875/.01，仅新入场过滤，原同向q/退出不变。旧ETH文字E.005过期而机器E.0075，旧spec/报告/status原字节保持。

父组合本金18750/raw[1,1]直接相加BTC3750与ETH15000两个原规模银行的美元NAV，20/80仅初始本金占比，权重不归一化。无缩放、转账、再平衡、父订单或跨保证金；对齐完整事件时间轴后重算组合NAV与整体DD，不平均收益/Sharpe/回撤。

完整读取36292登记事件/18013ID、434份结论、task/README/三技能、checks/*oos.py及freqtrade原ZIP。初始16条均有实际证据，缺实际结果0，旧legacy/false及负结果保留；旧paper失败观察不补单重跑。保护79933旧文件，main上原报价、账本和缺口保持。

Walk-forward已执行：2025-10-19T00:01Z→2026-11-14T00:01Z，391日/33日背景。每币610562分钟bar、10176小时mark、1273实际资金费，8份Parquet SHA、单位、闭合/可得时间及连续性核验。固定规则无训练/标签，仅使用完成前缀；13完整30日折+1日尾折，现金/持仓跨折连续，全期终止才按成本平仓，整体DD用完整事件NAV。近40日8×5及扩展21日5+5+5+6逐折保存，尾折Sharpe=None不计完整正月；无标签故无标签purge用途，背景/下一OPEN/资金费成熟另核验。OOS字样沿用机器字段，实际是复用开发历史。

Sensitivity已执行：BTC退出缓冲E三档×ETH R两档六格；BTC组件只沿E，ETH只沿R。全部净收益、整体DD、Sharpe、Calmar、近期正折、10相邻变化和并列最优边界保留。局部3倍净正与严格近期合格比例各≥60%；小邻域/两档ETH不能证明宽平台，不事后扩批/换代表。相同NAV若出现须披露，参数不同仍分别登记，不能当独立样本。

Costs已执行：每边费5bp+半价差1bp+滑点2bp+0.5×过去20日样本logvol×sqrt(abs(q)×真实OPEN/过去20完整日quoteADV)，不利tick与实际LOT/minnotional；参与率≤0.1%，费后1倍抵押，闭合小时high/low的1%维持保证金代理。执行成本与负资金费1/2/3倍，收入不放大；线性永续无需借现货，不编借币费。含逐项费用、交易数/成本占比、持有与现金0比较；冻结费率/盘口为估计，缺历史L2/TCA、完整档位、tick强平和真实容量证明。

冻结门槛：三成本全期/近期净正；1倍≥10/13正完整月；近期各成本≥6/8正5日折；扩展21日三成本净正且≥3/4正折；3倍DD≤25%；两项适用局部比例≥60%；至少4底层平仓；1倍(毛价格PnL+净资金费)/执行成本≥2.5；无拒单、负抵押或保证金代理违规，期末平仓且≥180日。任一失败即rejected，结果仍保留。

|BTC退出E|ETH R|来源/状态|1x净%|2x净%|3x净%|3x整体DD%|正月/13|近期正折1/2/3|
|---:|---:|---|---:|---:|---:|---:|---:|---|
|0.5%|0.00875|旧只读/passed|9.158860698|8.581388838|8.004112196|1.360652752|12|6/6/6|
|0.5%|0.01|旧只读/passed|9.097264887|8.515954679|7.934839687|1.360652752|12|6/6/6|
|1%|0.00875|新/passed|9.344686389|8.772020534|8.199551033|1.481963764|12|6/6/6|
|1%|0.01|新/passed|9.283090578|8.706586374|8.130278523|1.481963764|12|6/6/6|
|1.5%|0.00875|新/passed|8.914317195|8.335856526|7.757564355|1.486586875|12|6/6/6|
|1.5%|0.01|新/passed|8.852721385|8.270422367|7.688291846|1.486586875|12|6/6/6|


事前代表E1%/L29/H3%/V10/cap2.75%/R.01（47d5114240862b910c8fb25e596fdbfb1d84021aef6887cf37ea17c8f2668863）：三成本净9.283090578%/8.706586374%/8.130278523%，3倍DD1.481963764%，Sharpe2.188125822、Calmar5.107884269，passed，失败项[]。

BTC E1%/cap2.75%组件passed：三成本净18.200621761%/16.822195971%/15.443911697%，3倍DD5.789820696%，Sharpe1.463203429、Calmar2.477916200，正月10/13、近期{'1': 6, '2': 6, '3': 6}，失败项[]。

BTC E1.5%/cap2.75%组件rejected：三成本净16.048775794%/14.641375932%/13.233978308%，3倍DD6.977185534%，Sharpe1.238826174、Calmar1.763176140，正月9/13、近期{'1': 6, '2': 6, '3': 6}，失败项['ten_of_thirteen_positive_complete30d_1x_folds']。

BTC E1%组件10/13正完整月且全部历史门槛通过；E1.5%仅9/13正完整月而淘汰，两组件近期三成本均6/8。四父均12/13正月并历史通过，组合通过不替代组件资格；ETH扩展21日PnL为0，该段父利润来自BTC，旧ETH状态不改。代表始终E1%/R.01，不事后换成收益最高的其他预算格。

配对旧E0.5%：新E1%/R0.00875，3倍净变化+0.195438837个百分点、整体DD变化+0.121311012个百分点、Sharpe-0.058652264、Calmar-0.325879085。

配对旧E0.5%：新E1%/R0.01，3倍净变化+0.195438837个百分点、整体DD变化+0.121311012个百分点、Sharpe-0.057665834、Calmar-0.322003267。

配对旧E0.5%：新E1.5%/R0.00875，3倍净变化-0.246547841个百分点、整体DD变化+0.125934123个百分点、Sharpe-0.189637388、Calmar-0.618031926。

配对旧E0.5%：新E1.5%/R0.01，3倍净变化-0.246547841个百分点、整体DD变化+0.125934123个百分点、Sharpe-0.188539397、Calmar-0.614032898。

E1%两个新父三倍净收益较匹配ETH预算的旧E0.5%提高约0.195439个百分点，但整体DD升高约0.121311个百分点，Sharpe与Calmar均下降，是收益与风险代价，不是联合改善。E1.5%两父净收益少约0.246548个百分点、DD高约0.125934个百分点，Sharpe/Calmar同样下降。最高净收益位于E1%内部，最小DD和较高Sharpe/Calmar仍为旧E0.5%边界；多指标不能只读单一最优格。小3×2邻域、两档ETH与旧参考处于边界不能证明宽平台，全部启发标记保留，不改门槛/代表，待独立未来。

六新配置全成本NAV签名6组，匹配8旧参考0组，匹配上轮实际新/只读路径0/6；原始abs(deltaSharpe)>2×sampleSTD(absdeltas)标记1/10，绝对变化范围[0.018019288266744482, 0.224377255204262]、STD0.067686383，不是显著性或过拟合概率。三倍净正/正Sharpe/严格近期比例1.0/1.0/1.0。

匹配持有3倍净-14.782911083%、DD18.454766592%，现金0；18父成本场景BTC/ETH利润守恒。独立审计新原生6/新父12、旧原生15/旧父9条，新决策2346、旧只读5865；42场景、588逐折、336近期折、168扩展折、16464日NAV、18持有对照、10邻边/图均保存。策略引擎与资金核算源码和上轮原字节一致。显式生成本轮规则说明，reserve前逐个核对标量/轴/描述并保存signal_scalar_consistency_before_reservation.json；81个严格阈值/真实持仓/未来后缀合成检查通过后绑定、预登记。金融完整评估一次，未重跑已完成配置；上轮H2.5/H3.5说明勘误和全部原记录保留，文案修正不算新配置。

原账户：SMA/single12:30→14:30、L4/FEWM14:10→16:10；日事件{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、新成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、资金费记录{'SMA': 0, 'candidate': 0, 'l4h02': 6, 'fewm': 6}。真实Nov15_16 fundingTime=1794758400000，BTC/ETH各一笔；仅L4/FEWM在本窗各计6条，single截止仍14:30而未记16。BTC负费率空仓支付按原1/2/3成本压力，ETH零仓位零金额行保留；各自q/入场价/本金/规则不变，现金按自己的结算改变。所有旧资金费/日事件唯一键及完整NAV前缀核验。

l4h02 BTC原持仓-0.006000000000000000，本次16UTC三成本自身资金费USDT：-0.0009591489180000000000000000000/-0.001918297836000000000000000000/-0.002877446754000000000000000000；ETH零仓位三条零金额结算原样保留。

fewm BTC原持仓-0.009000000000000000，本次16UTC三成本自身资金费USDT：-0.001438723377000000000000000000/-0.002877446754000000000000000000/-0.004316170131000000000000000000；ETH零仓位三条零金额结算原样保留。

SMA65/对称1%/Float/本金1500:500/raw75:25原样，追加120闭合分钟，累计64229分钟/64275点；完整67日权威research/experiments/20261115T075947Z/forward_inputs.json.gz、旧66/65前缀只读，本轮输入为minute数组，无新日线捕获或指标决策。原组合3倍累计净-7.468957812%，负收益完整保留；各账户未成熟180日，旧延迟shadow不冒充十策略真实报价模拟。

本轮SMA/single12:30→14:30无资金费，L4/FEWM14:10→16:10各按自身原持仓计入Nov15_16真实资金费6条（含ETH零仓位），BTC空仓遇负费率为支付，支出按原1/2/3倍压力。日决策与新成交全0，原q/入场价/desired/本金/冻结规则保持，现金只按自己的结算变化，完整NAV前缀核验。下轮SMA/single14:30→16:30、16:31后闭合，single尚未记16，须新查实际结算、可核对本轮原公开字段但只用自己的q/现金计算；L4/FEWM16:10→18:10、18:11后闭合，已记16不得重复。所有窗口仍需完整实际结算查询，不假定八小时或零。日事件仍Nov16_00:01，原67日权威/66与65前缀保持，新E1/E1.5研究不采用到原账户，旧shadow与十策略真实报价分开。

旧午夜源捕获UTC2026-11-15T08:17:46.618283Z、08源捕获UTC2026-11-15T14:06:10.992989Z及哈希保持；本轮16源首次捕获UTC2026-11-15T22:09:23.048575Z，原公开负费率/标记价及全部HTTP回执保存。下轮可复用/比较该原公开字段，不重标捕获UTC，不复制别的账户现金流，也不提前给single入账。

有包公共GET 18次，均保存URL/捕获时界/body/gzipSHA；上述行情/结算捕获观察到传输失败0次，本轮官方文档两次读取成功，初始未应用的patch格式错误和所有真实失败/恢复见read_failures.json。FEWM与cached metadata/time精确去重，SMA内部未分包重试数0仅按原stderr/命令时界披露，失败体、资产/URL和精确尝试UTC若原执行器未记录则不编造。

复现：cwd=/home/desktop/Documents/Codex/EquiTide，解释器/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B。review/launch.py bootstrap.py review/preflight.py；review/configure.py review/prepare.py review/setup.py；review/execute.py freeze units bind reserve_0 evaluate audit exports finish_0 research_check；diagnostics/historical_aliases、实际view_image后visual_review；原账户midnight_archive l4h02 fewm candidate forward accounts_check；account_continuity/complete_transport_audit/validate_sources；journal sources_check gates feed collect final_checks、staged_whitespace、seal/publish。真实命令/UTC/退出码/stdout保留；不重复运行源变换、已完成金融或账户窗口。forward --reproduce仅只读核验。

391日历史与多重选择偏差未消除，无DSR/PBO显著性结论，正收益不代表稳定实盘盈利。本轮已读[Binance官方市场/资金费文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)和[官方公共数据README](https://github.com/binance/binance-public-data/blob/master/README.md)，实际原包/输入SHA是复现依据。

实际失败/阻碍：{"round": "20261115T220354Z", "facts": [{"type": "initial_freeze_patch_format_error", "tool": "tools.apply_patch via functions.exec", "error": "multiple operations target the same freeze.py path", "no_files_changed_by_failed_patch": true, "resolved": true, "resolution": "Wrote and AST-checked the explicit scalar-consistent freeze source before any plan/spec/reserve or market/account evaluation.", "financial_or_account_reruns": 0}, {"type": "visual_axes_tail_label_stale", "original_text": "H3/E0.5 fixed", "resolved": true, "resolution": "Axes label now derives from actual predeclared plan; original metadata/review source retained and all financial/plot bytes plus numeric diagnostics verified unchanged.", "financial_or_account_reruns": 0}, {"type": "seal_daily_expected_count_error", "original_native_receipt": "research/experiments/20261115T220354Z/review/seal_failed_before_fix_receipt.json", "original_native_exit_code": 1, "original_log": "research/experiments/20261115T220354Z/review/seal_failed_before_fix.log", "resolved": true, "resolution": "Only daily-event sealing expectation changed to actual all0;funding remains0/0/6/6. Original failed source/receipt/log retained;future replacement is field-specific;all bound financial artifacts unchanged.", "financial_or_account_reruns": 0}]}。保留所有正/负/淘汰/失败、原账户完整账本/冻结规则/登记、原包、哈希和下轮状态；只清理可重建缓存，大行情忽略。锁内snapshot只读已有账户/报告，不新回测或产生模拟成交，不部署或创建定时任务。真实commit/push、完整远端树/blob和解锁后检查见.git/automation_proofs回执。
