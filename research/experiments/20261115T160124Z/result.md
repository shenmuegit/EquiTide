本轮完成6个新金融配置：BTC入场风险估计窗口V8/V12两个组件，固定波动率上限2.75%，与已有ETH预算R=.00875/.01组成四父组合，18条1/2/3倍成本场景。历史通过5个：4父+1BTC；淘汰1个。8旧实际配置/24场景只读；12项原账户窗口各自reserve/finish，partial rejected表示尚未成熟180日，不取消原长期计划。

假设与预设：固定旧cap2.75%与ROC L29/H3%/退出E0.5%，本轮预声明BTC风险估计窗口V=[8,10,12]×ETH R=[.00875,.01]，检验短窗口响应风险变化与长窗口平滑噪音的机会成本；旧V10中心只读，事前代表V8/R.01固定。查完整参数、币种、资本、时间与组件，新V8/V12均无实际结果，所有新配置先reserve再计算；不在结果后扩批/换代表，历史仍为复用开发样本。

BTC规则：本金3750/固定名义1000；完成29日ROC严格>3%多、<−3%空，入场优先；带内实际多仅ROC>−0.5%、空仅ROC<0.5%保留，相等退出。仅新/反手检查过去V个完成日（8/10/12）无偏样本log(close/prevclose)波动率≤固定2.75%，同向实际q保持。真实信号可得后的下一00:01 OPEN、不利tick、LOT向下；新cap从原现金完整计算391日数量、费用、冲击、资金费和保证金，不缩放旧NAV。

ETH只读：本金15000/名义4000，long-only L5/H2%/退出E0.75%，有限归一化EWMS16 beta15/17、D3严格K0.75%、V6 cap5.625%；最近4笔实际已实现有符号资金费中位数，信号前1–36小时且available≤signal合格，缺4笔阻新仓。预算min(.0002,R×过去V8样本logvol×最新合格过去实际结算间隔小时/24)。R原值.00875/.01，仅新入场过滤，原同向q/退出不变。旧ETH文字E.005过期而机器E.0075，旧spec/报告/status原字节保持。

父组合本金18750/raw[1,1]直接相加BTC3750与ETH15000两个原规模银行的美元NAV，20/80仅初始本金占比，权重不归一化。无缩放、转账、再平衡、父订单或跨保证金；对齐完整事件时间轴后重算组合NAV与整体DD，不平均收益/Sharpe/回撤。

完整读取36124登记事件/17929ID、431份结论、task/README/三技能、checks/*oos.py及freqtrade原ZIP。初始16条均有实际证据，缺实际结果0，旧legacy/false及负结果保留；旧paper失败观察不补单重跑。保护78939旧文件，main上原报价、账本和缺口保持。

Walk-forward已执行：2025-10-19T00:01Z→2026-11-14T00:01Z，391日/33日背景。每币610562分钟bar、10176小时mark、1273实际资金费，8份Parquet SHA、单位、闭合/可得时间及连续性核验。固定规则无训练/标签，仅使用完成前缀；13完整30日折+1日尾折，现金/持仓跨折连续，全期终止才按成本平仓，整体DD用完整事件NAV。近40日8×5及扩展21日5+5+5+6逐折保存，尾折Sharpe=None不计完整正月；无标签故无标签purge用途，背景/下一OPEN/资金费成熟另核验。OOS字样沿用机器字段，实际是复用开发历史。

Sensitivity已执行：BTC波动率窗口V三档×ETH R两档六格；BTC组件只沿V，ETH只沿R。全部净收益、整体DD、Sharpe、Calmar、近期正折、10相邻变化和并列最优边界保留。局部3倍净正与严格近期合格比例各≥60%；小邻域/两档ETH不能证明宽平台，不事后扩批/换代表。相同NAV若出现须披露，参数不同仍分别登记，不能当独立样本。

Costs已执行：每边费5bp+半价差1bp+滑点2bp+0.5×过去20日样本logvol×sqrt(abs(q)×真实OPEN/过去20完整日quoteADV)，不利tick与实际LOT/minnotional；参与率≤0.1%，费后1倍抵押，闭合小时high/low的1%维持保证金代理。执行成本与负资金费1/2/3倍，收入不放大；线性永续无需借现货，不编借币费。含逐项费用、交易数/成本占比、持有与现金0比较；冻结费率/盘口为估计，缺历史L2/TCA、完整档位、tick强平和真实容量证明。

冻结门槛：三成本全期/近期净正；1倍≥10/13正完整月；近期各成本≥6/8正5日折；扩展21日三成本净正且≥3/4正折；3倍DD≤25%；两项适用局部比例≥60%；至少4底层平仓；1倍(毛价格PnL+净资金费)/执行成本≥2.5；无拒单、负抵押或保证金代理违规，期末平仓且≥180日。任一失败即rejected，结果仍保留。

|BTC风险窗口V|ETH R|来源/状态|1x净%|2x净%|3x净%|3x整体DD%|正月/13|近期正折1/2/3|
|---:|---:|---|---:|---:|---:|---:|---:|---|
|8日|0.00875|新/passed|9.056276762|8.478305852|7.900520536|1.361994711|12|6/6/6|
|8日|0.01|新/passed|8.994680951|8.412871692|7.831248026|1.361994711|12|6/6/6|
|10日|0.00875|旧只读/passed|9.158860698|8.581388838|8.004112196|1.360652752|12|6/6/6|
|10日|0.01|旧只读/passed|9.097264887|8.515954679|7.934839687|1.360652752|12|6/6/6|
|12日|0.00875|新/passed|8.802678844|8.226990021|7.651498451|1.365231477|11|6/6/6|
|12日|0.01|新/passed|8.741083033|8.161555862|7.582225941|1.365231477|11|6/6/6|


事前代表V8/cap2.75%/R.01（4708b8c74f5f70d2bfc638612889c4ab5022734b630dea687e5209764923fceb）：三成本净8.994680951%/8.412871692%/7.831248026%，3倍DD1.361994711%，Sharpe2.212669189、Calmar5.353893698，passed，失败项[]。

BTC V8日/cap2.75%组件passed：三成本净16.758573627%/15.353622560%/13.948759211%，3倍DD5.737272243%，Sharpe1.340834719、Calmar2.259545450，正月10/13、近期{'1': 6, '2': 6, '3': 6}，失败项[]。

BTC V12日/cap2.75%组件rejected：三成本净15.490584036%/14.097043406%/12.703648786%，3倍DD6.487258585%，Sharpe1.236773281、Calmar1.820636606，正月9/13、近期{'1': 6, '2': 6, '3': 6}，失败项['ten_of_thirteen_positive_complete30d_1x_folds']。

BTC V8为10/13正完整月、近期三成本各6/8且全部历史门槛通过；V12总净正但仅9/13正月而淘汰。V8两个父为12/13、V12两个父为11/13，近期各成本均6/8，四父历史通过。组合通过不替代组件资格；ETH扩展21日PnL为0，该段父利润来自BTC，旧ETH状态不改。代表始终V8/R.01，不换为旧中心或事后更高格。

配对旧V10：新V8日/R0.00875，3倍净变化-0.103591661个百分点、整体DD变化+0.001341959个百分点、Sharpe-0.033158041、Calmar-0.076037411。

配对旧V10：新V8日/R0.01，3倍净变化-0.103591661个百分点、整体DD变化+0.001341959个百分点、Sharpe-0.033122467、Calmar-0.075993838。

配对旧V10：新V12日/R0.00875，3倍净变化-0.352613746个百分点、整体DD变化+0.004578725个百分点、Sharpe-0.096939253、Calmar-0.258270681。

配对旧V10：新V12日/R0.01，3倍净变化-0.352613746个百分点、整体DD变化+0.004578725个百分点、Sharpe-0.096962591、Calmar-0.258122351。

四个新父全期净收益/Sharpe/Calmar均低于匹配ETH预算的旧V10，整体DD均更高，没有综合改善。V8三倍净少约0.103592个百分点、DD高约0.001342个百分点；V12净少约0.352614个百分点、DD高约0.004579个百分点。DD绝对差很小，色阶不应夸大；旧V10是本网格四指标内部最优，但小3×2条件邻域和V12组件资格失败不能证明广泛稳健平台。所有原始启发标记保留，不扩批/改门槛/换代表，历史候选仍待独立未来。

六新配置全成本NAV签名6组，匹配8旧参考0组，匹配上轮实际新/只读路径0/6；原始abs(deltaSharpe)>2×sampleSTD(absdeltas)标记3/10，绝对变化范围[0.019081704998775706, 0.16093998343305782]、STD0.047602783，不是显著性或过拟合概率。三倍净正/正Sharpe/严格近期比例1.0/1.0/1.0。

匹配持有3倍净-14.782911083%、DD18.454766592%，现金0；18父成本场景BTC/ETH利润守恒。独立审计新原生6/新父12、旧原生15/旧父9条，新决策2346、旧只读5865；42场景、588逐折、336近期折、168扩展折、16464日NAV、18持有对照、10邻边/图均保存。预登记前只扩展策略及辅助函数的窗口校验允许值，归一化两处列表后策略完整AST一致、simulate/货币核算和核心字节不变。首次合成准备检查发现辅助函数旧允许列表，失败脚本/回执/当时源码均保留；当时尚无plan/batch/reserve/市场回测，补齐后5个合成窗口与未来后缀检查通过，再绑定/预登记，金融完整评估一次，未重跑已完成配置。

原账户：SMA/single06:30→08:30、L4/FEWM08:10→10:10；日事件{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、新成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}，资金费记录{'SMA': 0, 'candidate': 6, 'l4h02': 0, 'fewm': 0}。实际08UTC fundingTime=1794729600000，BTC/ETH各一笔；本窗仅single按自己的原q/现金及1/2/3成本规则入账6条，收入不放大，零持仓资产的零金额结算保留。此前L4/FEWM已各自记过08，本窗不重复。数量/入场价/本金/规则保持，现金只按各自结算变化；完整NAV前缀、所有历史资金费/日事件唯一键及午夜各一次核验，现三永续08均各记一次，SMA现货无资金费。

SMA65/对称1%/Float/本金1500:500/raw75:25原样，追加120闭合分钟，累计63869分钟/63915点；完整67日权威research/experiments/20261115T075947Z/forward_inputs.json.gz、旧66/65前缀只读，本轮输入为minute数组，无新日线捕获或指标决策。原组合3倍累计净-7.468957812%，负收益完整保留；各账户未成熟180日，旧延迟shadow不冒充十策略真实报价模拟。

本轮SMA/single06:30→08:30，L4/FEWM08:10→10:10；仅single按自己的持仓/现金与原成本规则计实际Nov15_08资金费6条，SMA现货与L4/FEWM为0。L4/FEWM此前已记08，不重复；三永续现均已按自己持仓各记08一次。日决策与新成交全0，q/入场价/本金/冻结规则不变，仅single现金按自己的资金费变化。新研究BTC风险窗口V8/V12不采纳到原账户。下轮SMA/single08:30→10:30，10:31后闭合；L4/FEWM10:10→12:10，12:11后闭合，先查各自完整窗口实际结算，不假定名义八小时。下一原日事件仍Nov16_00:01，完整67日权威仍075947/forward_inputs，当前分钟数组不冒充日线；保持旧66/65前缀，不重开/强平/转账，十策略真实报价与旧shadow分开。

午夜源原捕获UTC2026-11-15T08:17:46.618283Z不重标；已存08源原捕获UTC2026-11-15T14:06:10.992989Z与原包哈希保持；本轮新查询UTC2026-11-15T16:06:47.935006Z同值且有独立回执，不把旧捕获UTC重标。只复用公开字段，资金费按自己持仓计算。

有包公共GET 20次，均保存URL/捕获时界/body/gzipSHA；上述行情/结算捕获观察到传输失败2次，文档访问超时另见失败事实。FEWM与cached metadata/time精确去重，SMA内部未分包重试数0仅按原stderr/命令时界披露，失败体、资产/URL和精确尝试UTC若原执行器未记录则不编造。

复现：cwd=/home/desktop/Documents/Codex/EquiTide，解释器/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B。review/launch.py bootstrap.py；review/preflight.py；prepare.py合成检查失败，setup.py完成实际结算预绑定；prepare_complete.py补齐两处允许列表并验证；review/execute.py freeze units bind reserve_0 evaluate audit exports finish_0 research_check；diagnostics/historical_aliases、实际view_image后visual_review；原账户midnight_archive l4h02 fewm candidate forward accounts_check；account_continuity/complete_transport_audit/validate_sources；journal sources_check gates feed collect final_checks、staged_whitespace、seal/publish。每条真实命令/UTC/退出码/stdout保留；prepare/setup是首次源变换，不重复运行或重算已有ID。forward --reproduce仅只读核验。

391日历史与多重选择偏差未消除，无DSR/PBO显著性结论，正收益不代表稳定实盘盈利。本轮已读[Binance官方市场/资金费文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)和[官方公共数据README](https://github.com/binance/binance-public-data/blob/master/README.md)，实际原包/输入SHA是复现依据。

实际失败/阻碍：{"round": "20261115T160124Z", "facts": [{"type": "official_document_web_fetch_timeout", "attempt": "first", "observed_tool_result_utc": "2026-11-15T16:06:00Z", "url": "https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data", "tool": "web.run open via functions.exec", "tool_error": "Internal Error; (400) Timeout fetching", "origin_HTTP_status_or_response_body_not_available": true, "resolved": true, "resolved_utc": "2026-11-15T16:11:18.616907+00:00", "recovery": "Official specific funding-history URL redirected to canonical market-data page and fetched successfully; official Binance connector source and public-data README also read. Both original tool timeout results retained; no model/account rerun."}, {"type": "official_document_web_fetch_timeout", "attempt": "bounded_retry", "observed_tool_result_utc": "2026-11-15T16:06:53Z", "url": "https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data", "tool": "web.run open via functions.exec", "tool_error": "Internal Error; (400) Timeout fetching", "origin_HTTP_status_or_response_body_not_available": true, "resolved": true, "resolved_utc": "2026-11-15T16:11:18.616936+00:00", "recovery": "Official specific funding-history URL redirected to canonical market-data page and fetched successfully; official Binance connector source and public-data README also read. Both original tool timeout results retained; no model/account rerun."}, {"command": ["/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python", "-B", "/home/desktop/Documents/Codex/EquiTide/research/experiments/20261115T160124Z/review/prepare.py"], "cwd": "/home/desktop/Documents/Codex/EquiTide", "started_utc": "2026-11-15T16:09:48.729467Z", "finished_utc": "2026-11-15T16:09:51.197957Z", "exit_code": 1, "log": "research/experiments/20261115T160124Z/review/native_prepare.py_receipt.log", "type": "synthetic_preparation_window_helper_guard_failure", "resolved": true, "recovery": "Both policy/helper window allowlists completed and five synthetic base/helper/future-prefix cases passed before first reserve/model calculation. Original failed script, partial engine and actual native receipt retained. No spec,capital,gates or completed result changed."}, {"type": "transient_public_GET_failure", "url": "https://fapi.binance.com/fapi/v1/exchangeInfo", "raw": "data/raw/binance/l4h02_forward/20261115T160124Z/http_0000.gz", "sha256": "f61f27bd17de546264aa58f40f3aafaac7021e0ef69c17f6b1b4cd7664a037ec", "original_capture_utc": "2026-11-15T16:17:51.071252+00:00", "http_status": 0, "curl_exit_code": 35, "stderr": "curl: (35) TLS connect error: error:0A000126:SSL routines::unexpected eof while reading\n", "resolved": true, "recovery": "Subsequent bounded verified-TLS GET for same URL succeeded; original failure retained, account/model window executed once."}, {"type": "transient_public_GET_failure", "url": "https://fapi.binance.com/fapi/v1/fundingRate?symbol=ETHUSDT&startTime=1794700800002&endTime=1794731400000&limit=1000", "raw": "data/raw/binance/candidate_forward/20261115T160124Z/http_attempt_0005.gz", "sha256": "f61f27bd17de546264aa58f40f3aafaac7021e0ef69c17f6b1b4cd7664a037ec", "original_capture_utc": "2026-11-15T16:20:22.746269+00:00", "http_status": 0, "curl_exit_code": 35, "stderr": "curl: (35) TLS connect error: error:0A000126:SSL routines::unexpected eof while reading\n", "resolved": true, "recovery": "Subsequent bounded verified-TLS GET for same URL succeeded; original failure retained, account/model window executed once."}]}。保留所有正/负/淘汰/失败、原账户完整账本/冻结规则/登记、原包、哈希和下轮状态；只清理可重建缓存，大行情忽略。锁内snapshot只读已有账户/报告，不新回测或产生模拟成交，不部署或创建定时任务。真实commit/push、完整远端树/blob和解锁后检查见.git/automation_proofs回执。
