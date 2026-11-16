本轮完成6个新金融配置：BTC入场波动率上限2.625%/2.875%两个组件，固定风险窗口V10、L29/H3%/E0.5%，与已有ETH预算R=.00875/.01组成四父组合，18条1/2/3倍成本场景。历史通过6个：4父+2BTC；淘汰0个。8旧实际配置/24场景只读；12项原账户窗口各自reserve/finish，partial rejected表示尚未成熟180日，不取消原长期计划。

假设与预设：固定ROC L29/严格入场H3%/退出E0.5%/过去10完成日样本logvol，预声明BTC新/反手入场波动率上限=[2.625%,2.75%,2.875%]×ETH资金费预算R=[.00875,.01]。更紧门槛可能减少高波动不利入场但错过趋势，更松可能增加机会及风险；旧2.75%中心只读。代表2.625%/R.01在看结果前固定，完整新定义先reserve再计算，不事后扩批或换代表，仍为复用开发历史。

BTC规则：本金3750/固定名义1000；完成29日ROC严格>3%多、<−3%空，入场优先；带内实际多仅ROC>−0.5%、空仅ROC<0.5%保留，相等退出。仅新/反手检查过去10个完成日无偏样本log(close/prevclose)波动率≤2.625%/2.75%/2.875%，同向q保持。信号可得后的下一00:01 OPEN、不利tick、LOT向下；两新上限从原现金完整计算391日数量、费用、冲击、资金费和保证金，不缩放旧NAV。

ETH只读：本金15000/名义4000，long-only L5/H2%/退出E0.75%，有限归一化EWMS16 beta15/17、D3严格K0.75%、V6 cap5.625%；最近4笔实际已实现有符号资金费中位数，信号前1–36小时且available≤signal合格，缺4笔阻新仓。预算min(.0002,R×过去V8样本logvol×最新合格过去实际结算间隔小时/24)。R原值.00875/.01，仅新入场过滤，原同向q/退出不变。旧ETH文字E.005过期而机器E.0075，旧spec/报告/status原字节保持。

父组合本金18750/raw[1,1]直接相加BTC3750与ETH15000两个原规模银行的美元NAV，20/80仅初始本金占比，权重不归一化。无缩放、转账、再平衡、父订单或跨保证金；对齐完整事件时间轴后重算组合NAV与整体DD，不平均收益/Sharpe/回撤。

完整读取36416登记事件/18069ID、436份结论、去除观察后的11335个规范化研究定义（不等于独立试验）、task/README/三技能、checks/*oos.py及freqtrade原ZIP。初始16条均有实际证据，缺实际结果0，旧legacy/false及负结果保留；旧paper失败观察不补单重跑。保护80666旧文件，main上原报价、账本和缺口保持。

Walk-forward已执行：2025-10-19T00:01Z→2026-11-14T00:01Z，391日/33日背景。每币610562分钟bar、10176小时mark、1273实际资金费，8份Parquet SHA、单位、闭合/可得时间及连续性核验。固定规则无训练/标签，仅使用完成前缀；13完整30日折+1日尾折，现金/持仓跨折连续，全期终止才按成本平仓，整体DD用完整事件NAV。近40日8×5及扩展21日5+5+5+6逐折保存，尾折Sharpe=None不计完整正月；无标签故无标签purge用途，背景/下一OPEN/资金费成熟另核验。OOS字样沿用机器字段，实际是复用开发历史。

Sensitivity已执行：BTC入场波动率上限三档×ETH R两档六格；BTC组件只沿上限轴，ETH只沿R。全部净收益、整体DD、Sharpe、Calmar、近期正折、10相邻变化和并列最优边界保留。局部3倍净正与严格近期合格比例各≥60%；小邻域/两档ETH不能证明宽平台，不事后扩批/换代表。相同NAV若出现须披露，参数不同仍分别登记，不能当独立样本。

Costs已执行：每边费5bp+半价差1bp+滑点2bp+0.5×过去20日样本logvol×sqrt(abs(q)×真实OPEN/过去20完整日quoteADV)，不利tick与实际LOT/minnotional；参与率≤0.1%，费后1倍抵押，闭合小时high/low的1%维持保证金代理。执行成本与负资金费1/2/3倍，收入不放大；线性永续无需借现货，不编借币费。含逐项费用、交易数/成本占比、持有与现金0比较；冻结费率/盘口为估计，缺历史L2/TCA、完整档位、tick强平和真实容量证明。

冻结门槛：三成本全期/近期净正；1倍≥10/13正完整月；近期各成本≥6/8正5日折；扩展21日三成本净正且≥3/4正折；3倍DD≤25%；两项适用局部比例≥60%；至少4底层平仓；1倍(毛价格PnL+净资金费)/执行成本≥2.5；无拒单、负抵押或保证金代理违规，期末平仓且≥180日。任一失败即rejected，结果仍保留。

|BTC入场波动率上限|ETH R|来源/状态|1x净%|2x净%|3x净%|3x整体DD%|正月/13|近期正折1/2/3|
|---:|---:|---|---:|---:|---:|---:|---:|---|
|2.625%|0.00875|新/passed|9.158860698|8.581388838|8.004112196|1.360652752|12|6/6/6|
|2.625%|0.01|新/passed|9.097264887|8.515954679|7.934839687|1.360652752|12|6/6/6|
|2.75%|0.00875|旧只读/passed|9.158860698|8.581388838|8.004112196|1.360652752|12|6/6/6|
|2.75%|0.01|旧只读/passed|9.097264887|8.515954679|7.934839687|1.360652752|12|6/6/6|
|2.875%|0.00875|新/passed|9.000028418|8.422242505|7.844642170|1.362719676|12|6/6/6|
|2.875%|0.01|新/passed|8.938432608|8.356808345|7.775369660|1.362719676|12|6/6/6|


事前代表cap2.625%/L29/H3%/E0.5%/V10/R.01（368a7a51c0326f787842c26af7036c95b440234c76967a5fd29c8b7645dae9f8）：三成本净9.097264887%/8.515954679%/7.934839687%，3倍DD1.360652752%，Sharpe2.245791656、Calmar5.429887536，passed，失败项[]。

BTC入场cap2.625%/L29/H3%/E0.5%/V10组件passed：三成本净17.271493306%/15.869037492%/14.466717514%，3倍DD5.694252106%，Sharpe1.397713264、Calmar2.360782539，正月10/13、近期{'1': 6, '2': 6, '3': 6}，失败项[]。

BTC入场cap2.875%/L29/H3%/E0.5%/V10组件passed：三成本净16.477331910%/15.073305823%/13.669367381%，3倍DD5.737272243%，Sharpe1.315260722、Calmar2.214475320，正月10/13、近期{'1': 6, '2': 6, '3': 6}，失败项[]。

各新组件与父组合的真实通过状态、完整正月、近期正折和失败项按上表/逐项结果保存。组合资格不能替代组件资格；ETH扩展21日PnL若为0，该段父利润仅来自BTC，旧ETH状态不改。代表始终cap2.625%/R.01，不事后换成其他格。

配对旧cap2.75%：新cap2.625%/R0.00875，3倍净变化+0.000000000个百分点、整体DD变化+0.000000000个百分点、Sharpe+0.000000000、Calmar+0.000000000。

配对旧cap2.75%：新cap2.625%/R0.01，3倍净变化+0.000000000个百分点、整体DD变化+0.000000000个百分点、Sharpe+0.000000000、Calmar+0.000000000。

配对旧cap2.75%：新cap2.875%/R0.00875，3倍净变化-0.159470027个百分点、整体DD变化+0.002066924个百分点、Sharpe-0.048913951、Calmar-0.116996762。

配对旧cap2.75%：新cap2.875%/R0.01，3倍净变化-0.159470027个百分点、整体DD变化+0.002066924个百分点、Sharpe-0.048878159、Calmar-0.116929683。

相对匹配ETH预算的旧cap2.75%，四项指标同时严格改善（净收益增、整体DD降、Sharpe增、Calmar增）的新父数量0/4。所有收益/回撤代价按上述原数值披露，不能只选单一最好格；各指标及并列最优的边界信息另存sensitivity_metric_boundaries.json。小3×2邻域、两档ETH及重复历史不能证明宽平台，全部启发标记保留，待独立未来。

六新配置全成本NAV签名6组，匹配8旧参考3组，匹配上轮实际新/只读路径3/6；原始abs(deltaSharpe)>2×sampleSTD(absdeltas)标记1/10，绝对变化范围[0.0, 0.08245254155610171]、STD0.026676442，不是显著性或过拟合概率。三倍净正/正Sharpe/严格近期比例1.0/1.0/1.0。

额外只读既往固定规则的7个BTC上限组件及14个真实父组合完整三成本净值，本轮6/6新配置已匹配该旧路径集合。该结论覆盖更宽的已测上限集合，与上述8预声明参考/上一批的比较范围分开；不扩展本轮网格、不重分类旧状态、不新增计算或事后换代表，不把新参数指纹当独立样本。证据见known_cap_path_alias_verification.json。

匹配持有3倍净-14.782911083%、DD18.454766592%，现金0；18父成本场景BTC/ETH利润守恒。独立审计新原生6/新父12、旧原生15/旧父9条，新决策2346、旧只读5865；42场景、588逐折、336近期折、168扩展折、16464日NAV、18持有对照、10邻边/图均保存。资金核算核心与上轮原字节一致；策略引擎仅扩展预声明入场波动率上限的参数白名单，归一化该白名单后完整AST相同。显式生成本轮规则说明，reserve前逐个核对标量/轴/描述并保存signal_scalar_consistency_before_reservation.json；36个严格阈值/真实持仓/未来后缀合成检查通过后绑定、预登记。本轮所有新配置先成功reserve再完整评估一次，未重跑已完成配置；上轮H2.5/H3.5说明勘误和全部原记录保留，文案修正不算新配置。

原账户：SMA/single16:30→18:30、L4/FEWM18:10→20:10；新日事件{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、新成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、资金费记录{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}。完整窗口真实查询为空，三账户此前Nov15_16各6条全链记录已计一次，本窗不重复；各自现金/数量/入场价/desired/本金/规则保持。所有资金费/日事件唯一键及完整NAV前缀核验。

SMA65/对称1%/Float/本金1500:500/raw75:25原样，追加120闭合分钟，累计64469分钟/64515点；完整67日权威research/experiments/20261115T075947Z/forward_inputs.json.gz、旧66/65前缀只读，本轮输入为minute数组，无新日线捕获或指标决策。原组合3倍累计净-7.468957812%，负收益完整保留；各账户未成熟180日，旧延迟shadow不冒充十策略真实报价模拟。

本轮SMA/single16:30→18:30、L4/FEWM18:10→20:10，已新查完整窗口实际资金费为空；日决策、成交、资金费全0。三永续此前真实Nov15_16各入账一次，本窗不重复；各自现金/数量/入场价/desired/本金/冻结规则保持，完整NAV前缀核验。下轮SMA/single18:30→20:30、20:31后闭合；L4/FEWM20:10→22:10、22:11后闭合，仍须新查完整实际结算，不假定名义八小时或零。下一日事件Nov16_00:01，原67日权威/66与65前缀保留，新研究cap不采纳到原账户；旧SMA shadow与十策略报价模拟分开。

旧午夜源捕获UTC2026-11-15T08:17:46.618283Z、08源捕获UTC2026-11-15T14:06:10.992989Z及哈希保持；原16源首次捕获UTC2026-11-15T22:09:23.048575Z原字节不改，本轮新查询捕获UTC2026-11-16T02:08:55.285501Z，本轮为不同的稍后窗口且公开字段为空，不把旧16结算改成零，也不重标其首次捕获UTC。两次捕获分别留档，不重标原UTC，不复制其他账户现金流。

有包公共GET 20次，均保存URL/捕获时界/body/gzipSHA；上述行情/结算捕获观察到传输失败4次，本轮两项官方文档读取成功，所有真实失败/恢复（如有）见read_failures.json。FEWM与cached metadata/time精确去重，SMA内部未分包重试数2仅按原stderr/命令时界披露，失败体、资产/URL和精确尝试UTC若原执行器未记录则不编造。

复现：cwd=/home/desktop/Documents/Codex/EquiTide，解释器/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B。review/launch.py bootstrap.py review/preflight.py；review/configure_caps.py review/prepare_caps.py review/setup_caps.py；review/execute.py freeze units bind reserve_0 evaluate audit exports finish_0 research_check；diagnostics/historical_aliases、实际view_image后visual_review；原账户midnight_archive l4h02 fewm candidate forward accounts_check；account_continuity/complete_transport_audit/validate_sources；journal sources_check gates feed collect final_checks、staged_whitespace、seal/publish。原始命令/UTC/退出码/stdout完整保留；不重复运行源变换、已完成金融或账户窗口。forward --reproduce仅只读核验。

391日历史与多重选择偏差未消除，无DSR/PBO显著性结论，正收益不代表稳定实盘盈利。本轮已读[Binance官方市场/资金费文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)和[官方公共数据README](https://github.com/binance/binance-public-data/blob/master/README.md)，实际原包/输入SHA是复现依据。

实际失败/阻碍：{"round": "20261116T020401Z", "facts": [{"type": "transient_public_GET_failure", "url": "https://fapi.binance.com/fapi/v1/fundingRate?symbol=ETHUSDT&startTime=1794758400000&endTime=1794773400000&limit=1000", "raw": "data/raw/binance/l4h02_forward/20261116T020401Z/http_0007.gz", "sha256": "f61f27bd17de546264aa58f40f3aafaac7021e0ef69c17f6b1b4cd7664a037ec", "original_capture_utc": "2026-11-16T02:29:18.614953+00:00", "http_status": 0, "curl_exit_code": 35, "stderr": "curl: (35) TLS connect error: error:0A000126:SSL routines::unexpected eof while reading\n", "resolved": true, "recovery": "Subsequent bounded verified-TLS GET for same URL succeeded; original failure retained, account/model window executed once."}, {"type": "transient_public_GET_failure", "url": "https://fapi.binance.com/fapi/v1/fundingRate?symbol=ETHUSDT&startTime=1794758400000&endTime=1794773400000&limit=1000", "raw": "data/raw/binance/l4h02_forward/20261116T020401Z/http_0008.gz", "sha256": "f61f27bd17de546264aa58f40f3aafaac7021e0ef69c17f6b1b4cd7664a037ec", "original_capture_utc": "2026-11-16T02:29:23.627669+00:00", "http_status": 0, "curl_exit_code": 35, "stderr": "curl: (35) TLS connect error: error:0A000126:SSL routines::unexpected eof while reading\n", "resolved": true, "recovery": "Subsequent bounded verified-TLS GET for same URL succeeded; original failure retained, account/model window executed once."}, {"type": "SMA_original_curl_internal_retry_stderr", "log": "research/experiments/20261116T020401Z/forward.log", "stderr": "curl: (35) TLS connect error: error:0A000126:SSL routines::unexpected eof while reading\ncurl: (35) TLS connect error: error:0A000126:SSL routines::unexpected eof while reading\n", "command_receipt": "research/experiments/20261116T020401Z/forward_commands.json", "command_receipt_sha256": "e80499ef9786f88c7a2ee95a3cb8097fe74557b1ed5d0ce866f96fbfdafcff4a", "command_start_utc": "2026-11-16T02:32:41.736807Z", "command_finished_utc": "2026-11-16T02:33:05.885052Z", "native_phase_exit_code": 0, "curl_error_codes": ["35", "35"], "exact_failed_attempt_UTC_asset_URL_and_body_not_separately_saved": true, "resolved": true, "recovery": "Original bounded curl completed successfully; final raw responses and exact forward replay verified. Failed body,asset/URL,and exact attempt UTC unavailable and not fabricated."}]}。保留所有正/负/淘汰/失败、原账户完整账本/冻结规则/登记、原包、哈希和下轮状态；只清理可重建缓存，大行情忽略。锁内snapshot只读已有账户/报告，不新回测或产生模拟成交，不部署或创建定时任务。真实commit/push、完整远端树/blob和解锁后检查见.git/automation_proofs回执。
