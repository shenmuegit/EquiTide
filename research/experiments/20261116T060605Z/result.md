本轮完成6个新金融配置：BTC完成价格路径效率floor.125/.25两个组件，固定风险窗口V10与上限2.75%、L29/H3%/E0.5%，与已有ETH预算R=.00875/.01组成四父组合，18条1/2/3倍成本场景。历史通过3个：2父+1BTC；淘汰3个。8旧实际配置/24场景只读；12项原账户窗口各自reserve/finish，partial rejected表示尚未成熟180日，不取消原长期计划。

假设与预设：同样29日ROC门槛下，较高净位移/总路径长度可能减少震荡入场，但可能错过趋势早段或反转，也减少分散化。固定BTC路径效率floor=[0,.125,.25]×ETH R=[.00875,.01]，旧0为只读下边界，事前代表.125/R.01；不在结果后改批次或换代表。旧36个相关KAMA/ETH路径实验不是当前BTC完整定义，全部保留，六新完整指纹逐个查重/预登记。

BTC规则：本金3750/名义1000；完成L29 ROC严格>3%多、<−3%空，带内实际多仅ROC>−0.5%、空仅ROC<0.5%保留，相等退出；原入场优先/同向q保持。仅新或反手先检查过去V10日无偏样本logvol≤2.75%，再检查ER≥floor。ER=abs(C[i-1]-C[i-30])/sum(abs(C[j]-C[j-1]),j=i-29..i-1)，分母0时0，全程Fraction精确比值，严格低于门槛才阻挡，相等通过，未来后缀排除。0与旧总波动规则等价只读，新.125/.25完整重算391日。下一00:01 OPEN、不利tick、LOT向下；费用/滑点/过去20日冲击/资金费/保证金原核算不改。

ETH只读：本金15000/名义4000，long-only L5/H2%/退出E0.75%，有限归一化EWMS16 beta15/17、D3严格K0.75%、V6 cap5.625%；最近4笔实际已实现有符号资金费中位数，信号前1–36小时且available≤signal合格，缺4笔阻新仓。预算min(.0002,R×过去V8样本logvol×最新合格过去实际结算间隔小时/24)。R原值.00875/.01，仅新入场过滤，原同向q/退出不变。旧ETH文字E.005过期而机器E.0075，旧spec/报告/status原字节保持。

父组合本金18750/raw[1,1]直接相加BTC3750与ETH15000两个原规模银行的美元NAV，20/80仅初始本金占比，权重不归一化。无缩放、转账、再平衡、父订单或跨保证金；对齐完整事件时间轴后重算组合NAV与整体DD，不平均收益/Sharpe/回撤。

完整读取36528登记事件/18125ID、438份结论、去除观察后的11347个规范化研究定义（不等于独立试验）、task/README/三技能、checks/*oos.py及freqtrade原ZIP。初始16条均有实际证据，缺实际结果0，旧legacy/false及负结果保留；旧paper失败观察不补单重跑。保护81345旧文件，main上原报价、账本和缺口保持。

Walk-forward已执行：2025-10-19T00:01Z→2026-11-14T00:01Z，391日/33日背景。每币610562分钟bar、10176小时mark、1273实际资金费，8份Parquet SHA、单位、闭合/可得时间及连续性核验。固定规则无训练/标签，仅使用完成前缀；13完整30日折+1日尾折，现金/持仓跨折连续，全期终止才按成本平仓，整体DD用完整事件NAV。近40日8×5及扩展21日5+5+5+6逐折保存，尾折Sharpe=None不计完整正月；无标签故无标签purge用途，背景/下一OPEN/资金费成熟另核验。OOS字样沿用机器字段，实际是复用开发历史。

Sensitivity已执行：BTC路径效率floor三档×ETH R两档六格；BTC组件只沿floor轴，ETH只沿R。全部净收益、整体DD、Sharpe、Calmar、近期正折、10相邻变化和并列最优边界保留。局部3倍净正与严格近期合格比例各≥60%；小邻域/两档ETH不能证明宽平台，不事后扩批/换代表。相同NAV若出现须披露，参数不同仍分别登记，不能当独立样本。

Costs已执行：每边费5bp+半价差1bp+滑点2bp+0.5×过去20日样本logvol×sqrt(abs(q)×真实OPEN/过去20完整日quoteADV)，不利tick与实际LOT/minnotional；参与率≤0.1%，费后1倍抵押，闭合小时high/low的1%维持保证金代理。执行成本与负资金费1/2/3倍，收入不放大；线性永续无需借现货，不编借币费。含逐项费用、交易数/成本占比、持有与现金0比较；冻结费率/盘口为估计，缺历史L2/TCA、完整档位、tick强平和真实容量证明。

冻结门槛：三成本全期/近期净正；1倍≥10/13正完整月；近期各成本≥6/8正5日折；扩展21日三成本净正且≥3/4正折；3倍DD≤25%；两项适用局部比例≥60%；至少4底层平仓；1倍(毛价格PnL+净资金费)/执行成本≥2.5；无拒单、负抵押或保证金代理违规，期末平仓且≥180日。任一失败即rejected，结果仍保留。

|BTC路径效率floor|ETH R|来源/状态|1x净%|2x净%|3x净%|3x整体DD%|正月/13|近期正折1/2/3|
|---:|---:|---|---:|---:|---:|---:|---:|---|
|0|0.00875|旧只读/passed|9.158860698|8.581388838|8.004112196|1.360652752|12|6/6/6|
|0|0.01|旧只读/passed|9.097264887|8.515954679|7.934839687|1.360652752|12|6/6/6|
|0.125|0.00875|新/passed|8.803111301|8.302502993|7.802079139|1.403998340|12|6/6/6|
|0.125|0.01|新/passed|8.741515490|8.237068833|7.732806630|1.403998340|12|6/6/6|
|0.25|0.00875|新/rejected|7.998014510|7.569336783|7.140835270|1.231295949|11|4/4/4|
|0.25|0.01|新/rejected|7.936418700|7.503902623|7.071562761|1.231295949|11|4/4/4|


事前代表floor.125/L29/H3%/E0.5%/V10/R.01（1bca2a5cf8ac343467c3b8666de63ce836c20ee28f220a3519e9428d523a9d24）：三成本净8.741515490%/8.237068833%/7.732806630%，3倍DD1.403998340%，Sharpe2.228819090、Calmar5.128593156，passed，失败项[]。

BTC路径效率floor0.125/L29/H3%/E0.5%/V10组件passed：三成本净15.492746322%/14.474608266%/13.456552229%，3倍DD6.899368369%，Sharpe1.368496946、Calmar1.812927859，正月10/13、近期{'1': 6, '2': 6, '3': 6}，失败项[]。

BTC路径效率floor0.25/L29/H3%/E0.5%/V10组件rejected：三成本净11.467262369%/10.808777212%/10.150332883%，3倍DD6.000387652%，Sharpe1.285441325、Calmar1.573980670，正月9/13、近期{'1': 4, '2': 4, '3': 4}，失败项['ten_of_thirteen_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct']。

各新组件与父组合的真实通过状态、完整正月、近期正折和失败项按上表/逐项结果保存。组合资格不能替代组件资格；ETH扩展21日PnL若为0，该段父利润仅来自BTC，旧ETH状态不改。代表始终floor.125/R.01，不事后换成其他格。

配对旧floor0：新floor0.125/R0.00875，3倍净变化-0.202033057个百分点、整体DD变化+0.043345588个百分点、Sharpe-0.016604216、Calmar-0.302748473。

配对旧floor0：新floor0.125/R0.01，3倍净变化-0.202033057个百分点、整体DD变化+0.043345588个百分点、Sharpe-0.016972566、Calmar-0.301294380。

配对旧floor0：新floor0.25/R0.00875，3倍净变化-0.863276926个百分点、整体DD变化-0.129356803个百分点、Sharpe-0.036117705、Calmar-0.075904534。

配对旧floor0：新floor0.25/R0.01，3倍净变化-0.863276926个百分点、整体DD变化-0.129356803个百分点、Sharpe-0.038232418、Calmar-0.080899983。

相对匹配ETH预算的旧floor0，四项指标同时严格改善（净收益增、整体DD降、Sharpe增、Calmar增）的新父数量0/4。所有收益/回撤代价按上述原数值披露，不能只选单一最好格；各指标及并列最优的边界信息另存sensitivity_metric_boundaries.json。小3×2邻域、两档ETH及重复历史不能证明宽平台，全部启发标记保留，待独立未来。

六新配置全成本NAV签名6组，匹配8旧参考0组，匹配上轮实际新/只读路径0/6；原始abs(deltaSharpe)>2×sampleSTD(absdeltas)标记1/10，绝对变化范围[0.01660421629028752, 0.08305562001529299]、STD0.019991782，不是显著性或过拟合概率。三倍净正/正Sharpe/严格近期比例1.0/1.0/0.6666666666666666。

另只读9个同规模旧BTC总波动率上限组件和18个对应父组合；本轮0/6匹配该集合的全成本路径，比较范围与8个预声明参考/上一批分开。新参数/路径也不是独立市场样本或未来证据；全部失败项保留，较低DD不能抵消近期正折或局部稳健门槛失败，不事后改网格或原账户。

匹配持有3倍净-14.782911083%、DD18.454766592%，现金0；18父成本场景BTC/ETH利润守恒。独立审计新原生6/新父12、旧原生15/旧父9条，新决策2346、旧只读5865；42场景、588逐折、336近期折、168扩展折、16464日NAV、18持有对照、10邻边/图均保存。资金核算核心与上轮原字节一致；策略引擎有意采用原总波动门控叠加精确BTC价格路径效率入场过滤，并增加审计字段；simulate及其他既有辅助函数AST、ETH分支与资金核算核心保持。合成检查独立计算路径首尾/总长度、零分母、严格阈值、floor0等价、真实入口及未来后缀。显式生成本轮规则说明，reserve前逐个核对标量/轴/描述并保存signal_scalar_consistency_before_reservation.json；21个严格阈值/真实持仓/未来后缀合成检查通过后绑定、预登记。本轮所有新配置先成功reserve再完整评估一次，未重跑已完成配置；上轮H2.5/H3.5说明勘误和全部原记录保留，文案修正不算新配置。

原账户SMA/singleNov15_20:30→22:30、L4/FEWM22:10→Nov16_00:10。新日事件{'SMA': 0, 'candidate': 0, 'l4h02': 1, 'fewm': 1}、真实资金费记录{'SMA': 0, 'candidate': 0, 'l4h02': 6, 'fewm': 6}、原核算成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}。L4/FEWM各自00资金费/日决策只入账一次，single尚未跨00；完整日线partial+新分钟的1440条/成交量/收盘价、旧背景前缀、现金/数量/费用/保证金、全部NAV与唯一键独立核验。

l4h02 BTC结算时原持仓-0.006000000000000000，Nov16_00三成本自身资金费USDT：-0.004957457552299824000000000000/-0.009914915104599648000000000000/-0.01487237265689947200000000000；ETH零仓位的零金额结算也逐条保留，不借用其他账户现金流。

fewm BTC结算时原持仓-0.009000000000000000，Nov16_00三成本自身资金费USDT：-0.007436186328449736000000000000/-0.01487237265689947200000000000/-0.02230855898534920800000000000；ETH零仓位的零金额结算也逐条保留，不借用其他账户现金流。

SMA65/对称1%/Float/本金1500:500/raw75:25原样，追加120闭合分钟，累计64709分钟/64755点；完整67日权威research/experiments/20261115T075947Z/forward_inputs.json.gz、旧66/65前缀只读，本轮输入为minute数组，无新日线捕获或指标决策。原组合3倍累计净-7.468957812%，负收益完整保留；各账户未成熟180日，旧延迟shadow不冒充十策略真实报价模拟。

本轮SMA/singleNov15_20:30→22:30未跨午夜；L4/FEWM22:10→Nov16_00:10，按各自原持仓入账真实00结算并执行原00:01日决策，日线partial+新闭合分钟严格组成1440条；成交按原核算，不采用新研究。下轮SMA/single22:30→00:30、00:31后闭合，须single自身00结算一次和原SMA新68日现货背景/日决策；L4/FEWM00:10→02:10、02:11后闭合，不重复00资金费或日决策，下一日决策Nov17_00:01。仍新查完整实际结算，不假定名义八小时或零。旧SMA延迟shadow与十策略真实报价模拟分开。

旧午夜源捕获UTC2026-11-15T08:17:46.618283Z、08源捕获UTC2026-11-15T14:06:10.992989Z及哈希保持；原16源首次捕获UTC2026-11-15T22:09:23.048575Z原字节不改，本轮新查询捕获UTC2026-11-16T06:10:18.547191Z，本轮捕获真实Nov16_00结算，BTC/ETH时刻均1794787200000ms；旧Nov15_16原字段和首次捕获UTC保持，新00源单独存funding00_nov16_preflight.json，不复制现金流。两次捕获分别留档，不重标原UTC，不复制其他账户现金流。

有包公共GET 19次，均保存URL/捕获时界/body/gzipSHA；上述行情/结算捕获观察到传输失败1次，本轮两项官方文档读取成功，所有真实失败/恢复（如有）见read_failures.json。FEWM与cached metadata/time精确去重，SMA内部未分包重试数0仅按原stderr/命令时界披露，失败体、资产/URL和精确尝试UTC若原执行器未记录则不编造。

复现：cwd=/home/desktop/Documents/Codex/EquiTide，解释器/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B。review/launch.py bootstrap.py review/preflight.py；review/configure_efficiency.py review/prepare_efficiency.py review/setup_efficiency.py；review/configure_report.py；冻结stdout旧标题另存澄清，不作等价重跑；review/execute.py freeze units bind reserve_0 evaluate audit exports finish_0 research_check；diagnostics/historical_aliases/totalrisk_history_aliases、实际view_image后visual_review；原账户midnight_archive l4h02 fewm candidate forward accounts_check；account_continuity/complete_transport_audit/validate_sources；journal sources_check gates feed collect final_checks、staged_whitespace、seal/publish。原始命令/UTC/退出码/stdout完整保留；不重复运行源变换、已完成金融或账户窗口。forward --reproduce仅只读核验。

391日历史与多重选择偏差未消除，无DSR/PBO显著性结论，正收益不代表稳定实盘盈利。本轮已读[Binance官方市场/资金费文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)和[官方公共数据README](https://github.com/binance/binance-public-data/blob/master/README.md)，实际原包/输入SHA是复现依据。

实际失败/阻碍：{"round": "20261116T060605Z", "facts": [{"type": "transient_public_GET_failure", "url": "https://fapi.binance.com/fapi/v1/klines?symbol=BTCUSDT&interval=1m&startTime=1794780540000&endTime=1794787800000&limit=1500", "raw": "data/raw/binance/l4h02_forward/20261116T060605Z/http_0002.gz", "sha256": "f61f27bd17de546264aa58f40f3aafaac7021e0ef69c17f6b1b4cd7664a037ec", "original_capture_utc": "2026-11-16T06:21:42.304005+00:00", "http_status": 0, "curl_exit_code": 35, "stderr": "curl: (35) TLS connect error: error:0A000126:SSL routines::unexpected eof while reading\n", "resolved": true, "recovery": "Subsequent bounded verified-TLS GET for same URL succeeded; original failure retained, account/model window executed once."}]}。保留所有正/负/淘汰/失败、原账户完整账本/冻结规则/登记、原包、哈希和下轮状态；只清理可重建缓存，大行情忽略。锁内snapshot只读已有账户/报告，不新回测或产生模拟成交，不部署或创建定时任务。真实commit/push、完整远端树/blob和解锁后检查见.git/automation_proofs回执。
