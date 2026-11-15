本轮真实完成6个新金融配置：BTC入场H2.5%/3.5%两个原生组件，与已有ETH预算R=.00875/.01组成四父组合，共18条1/2/3倍成本场景。历史通过5个：4父组合+1个BTC组件；淘汰1个BTC组件。8个旧实际配置/24场景只读复用。12项原冻结账户窗口各自reserve/finish，partial rejected只表示未成熟180日，不取消原长期计划。

事前假设：固定BTC L29、退出E0.5%、过去V10 samplelogvol上限3%，改变严格ROC入场阈值H为2.5%/3.5%，检验较早弱趋势入场和较强确认的费用后时序稳健性。H=[.025,.03,.035]×已有ETH R=[.00875,.01]为3×2面，代表H2.5%/R.01在结果前冻结，旧H3%中心只读。完整规则/参数/币种/资本/边界查重，不依赖名称/family/continuous_days标记；新两阈值均无实际结果，未在结果后扩批或换代表。

BTC本金3750/固定名义1000；完成29日ROC严格>H多、<−H空，入场优先；带内实际多头仅ROC>−.005、空头仅ROC<.005保留，相等退出。仅新/反手检查过去V10样本日log波动率≤3%，同向实际q保持。LOT向下、信号后下一00:01真实OPEN不利tick。每个新H从原现金计算完整391日原生数量、费用、冲击、资金费及保证金，prior370指纹仅谱系，不复用新参数的货币前缀。

ETH银行只读：本金15000/固定名义4000，long-only L5/H2%/退出E.75%，有限归一化EWMS16 beta15/17、D3严格K.75%、V6 cap5.625%。最近4笔实际已实现有符号资金费中位数，信号前1–36小时且available≤signal合格，缺4笔阻止新仓；预算min(.0002,R×过去V8样本logvol×最新合格实际过去结算间隔小时/24)。R原值.00875/.01，仅新入场过滤，原同向q与退出不变。旧E.005文字过期而机器一直E.0075，旧spec/报告/status原字节不改。

父组合本金18750/raw[1,1]直接相加BTC3750和ETH15000两个原规模完整独立银行的美元NAV，20/80仅初始本金占比。权重不归一化，不缩放、不转账/再平衡/父订单/跨保证金；完整事件轴对齐后重算整体NAV与DD，不平均收益、Sharpe或回撤。

完整读取35956登记事件/17845ID、428份结论、三技能/task/README/OOS及freqtrade原ZIP。初始16条均有真实归档，缺实际结果0，保留旧legacy/false与负结果。基于最新main及真实模拟盘报价/采样缺口提交；上轮推送与解锁后证明核对，无旧reserved，本轮未重复上轮锁恢复。保护77972份旧文件，paper10冻结计划/账本/缺口保持原字节。

Walk-forward已执行：2025-10-19T00:01Z→2026-11-14T00:01Z，391日和33日背景；每币610562分钟bar、10176小时mark、1273实际资金费，8份Parquet的SHA、单位、闭合/可得时间与连续性核验。固定规则无拟合或标签，只用当时完成前缀；13完整30日折+1日尾折，现金/持仓跨折连续，仅全期末计成本平仓，整体DD来自全事件NAV。近40日8×5及扩展21日5+5+5+6逐折保存，尾折Sharpe=None且不计完整正月。无标签时purge/embargo无标签用途，实际背景/下一可执行OPEN/资金费成熟界限另行核验。研究历史反复开发，非未触碰最终留出或独立未来。

Sensitivity已执行：BTC H三档×ETH R两档六格，BTC原生只沿H、ETH原生只沿R；净收益、整体DD、Sharpe、Calmar、近期正折及所有并列最佳边界/10条相邻变化保留。局部3倍净正与严格近期比例各≥60%。旧H3全期收益/Sharpe/Calmar是内部峰，ETH仅两档，不能证明宽平台；六新路径不同仍不等于独立市场样本，不事后扩网格/重选代表。

Costs已执行：每边手续费5bp+半价差1bp+滑点2bp+0.5×过去20日samplelogvol×sqrt(abs(q)×真实OPEN/过去20日quoteADV)，不利tick；执行成本及负资金费1/2/3倍，收入不放大。含实际LOT/tick/minnotional、参与率≤0.1%、费后1倍抵押及闭合小时high/low的1%维持保证金代理。线性永续不借现货，不编借币费。冻结费率/价差仍是估计，缺历史L2/TCA、完整档位、tick强平及真实容量证明；交易数、分项成本/占比和匹配持有/现金0对照逐场景保存。

预设门槛：三成本全期/近期净正；1倍≥10/13正完整月；近期各成本≥6/8正5日折；扩展21日净正且≥3/4正折；3倍DD≤25%；适用局部两比例≥60%；至少4底层平仓；1倍(毛价格PnL+净资金费)/执行成本≥2.5；无拒单/负抵押/保证金代理违规、期末平仓且≥180日。失败即rejected，完整结果仍保留。

|BTC入场H|ETH预算R|来源/状态|1x净%|2x净%|3x净%|3x整体DD%|正月/13|近期正折1/2/3|
|---:|---:|---|---:|---:|---:|---:|---:|---|
|2.5%|0.00875|新/passed|8.519970808|7.923754915|7.327724993|1.362398031|12|6/6/6|
|2.5%|0.01|新/passed|8.458374998|7.858320756|7.258452484|1.362398031|12|6/6/6|
|3.0%|0.00875|旧只读/passed|9.000028418|8.422242505|7.844642170|1.362719676|12|6/6/6|
|3.0%|0.01|旧只读/passed|8.938432608|8.356808345|7.775369660|1.362719676|12|6/6/6|
|3.5%|0.00875|新/passed|8.579370198|8.004592441|7.429979329|1.364318836|12|6/6/6|
|3.5%|0.01|新/passed|8.517774388|7.939158281|7.360706819|1.364318836|12|6/6/6|


事前代表H2.5%/ETH R.01（d16b89652c1e99bd3ceeab1dada1eaccd6e1d8eeb8500b9329d9e61007a610c2）：三成本净8.458374998%/7.858320756%/7.258452484%，3倍DD1.362398031%，Sharpe2.038362399、Calmar4.961727689，passed、失败项[]。

BTC H2.5%组件rejected：三成本净14.077043858%/12.580867877%/11.084781498%，3倍DD6.194437414%，Sharpe1.060927001，正月9/13、近期正折{'1': 6, '2': 6, '3': 6}，失败项['ten_of_thirteen_positive_complete30d_1x_folds']。

BTC H3.5%组件passed：三成本净14.374040809%/12.985055504%/11.596053176%，3倍DD5.953464158%，Sharpe1.136097167，正月10/13、近期正折{'1': 6, '2': 6, '3': 6}，失败项[]。

BTC H3.5%达到10/13正月、三成本近期6/8及全部历史门槛，保留为待独立未来验证的历史合格候选；BTC H2.5%仅9/13正月而淘汰。四父组合各12/13正月、近期6/8，历史通过，但全期收益/Sharpe/Calmar低于相同ETH预算的旧H3。H2.5父DD比旧H3低约0.000322个百分点，H3.5高约0.001599个百分点，差异很小，热图自动缩放不应夸大。没有综合优于旧中心，不修改冻结规则。ETH扩展21日PnL为0，父组合该段利润由BTC贡献，组合通过不替代各自组件资格。

六新配置三成本NAV签名6组，匹配八个预登记旧参考0组，上轮实际新/只读配置匹配0/6；新父3倍净收益低于对应H3为4个、相同0个。实际目标/状态/成交/资金费/NAV差异只读核验，未重算市场策略。

原始abs(deltaSharpe)>2×sampleSTD(absdeltas)启发式标记2/10，绝对变化范围[0.01895510468173578, 0.25433372181504676]、样本STD0.082980416，全部保存，不是统计显著性或过拟合概率。全部指标及并列最优边界见sensitivity_metric_boundaries。父网格3倍净正/正Sharpe/严格近期比例1.000000/1.000000/1.000000。

匹配持有3倍净-14.782911083%、DD18.454766592%，现金0；18父成本场景BTC/ETH全期及扩展PnL加总守恒核对。独立审计新原生6条/新父12条、旧原生15条/旧父9条曲线，新决策2346、旧只读5865；42成本场景、588逐折、336近期折、168扩展折、16464日NAV、18持有对照、10边及3×2图保留。引擎函数AST与核算核心字节未变，每个新配置先reserve再计算并finish，完整金融评估一次。

原冻结账户窗口：SMA/single Nov15_00:30→02:30，L4/FEWM02:10→04:10；本轮日事件{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、新成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、资金费记录{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}全0。完整实际结算窗口公开查询为空，18本永续账簿cash/q/entry等原样；完整NAV前缀、历史资金费/日事件唯一键、Nov15午夜各自一次核对，不按名义八小时补造，也不重复已完成的原00:01日决策。

SMA原65/对称1%/Float/本金1500:500/raw75:25保持，只增加120闭合分钟估值，累计63509分钟/63555点。完整67日权威research/experiments/20261115T075947Z/forward_inputs.json.gz只读复用，旧66/65数组前缀完全一致，本轮没有新日线捕获/指标计算；当前输入是minute数组。原组合3倍累计净-7.468957812%，负收益完整保存。所有原账户未成熟180日，旧延迟shadow不冒充十策略真实报价模拟。

本轮SMA/single Nov15_00:30→02:30，L4/FEWM02:10→04:10，仅闭合分钟估值/风险，日事件/资金费/成交全0，cash/q/entry/desired/已计成本保持原样。三永续与SMA已完成Nov15午夜/原00:01日事件，本轮不重复。下轮SMA/single02:30→04:30，04:31后参考闭合；L4/FEWM04:10→06:10，06:11后闭合，均在下一Nov16_00:01前。先查实际完整窗口fundingTime，不按名义八小时编造；只续接原账簿与完整NAV，不能重开/强平/转账或采纳研究H2.5/H3.5参数。当前SMA输入是每资产minute数组，完整67日权威仍075947/forward_inputs的1d/1m字典，保留旧66/65前缀；下一日事件到来前使用mark-only流程，不误用要求一个日事件的daily-only执行器。旧延迟shadow与十策略真实报价模拟分开，保留全部纸面缺口/旧blocked记录。

旧Nov15午夜公开字段原捕获UTC2026-11-15T08:17:46.618283Z保留；本轮查询UTC2026-11-15T10:04:59.247467Z字段为空，未把旧字段重标为新响应。下一原日事件所有账户均为Nov16_00:01。

保存唯一公共GET 21次、实际传输失败3次，URL/UTC/raw/body/gzipSHA及失败回执保留；FEWM仅复用同窗公开数据、candidate仅复用metadata/time，账户cashflow不复制。SMA原curl没有单独保存体/精确UTC的内部重试仅按stderr披露，不补造。

391日开发历史与多重选择偏差未消除，无DSR/PBO显著性结论；历史合格或正收益不代表稳定实盘盈利。[Binance官方市场/资金费文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)及[官方公共数据README](https://github.com/binance/binance-public-data/blob/master/README.md)本轮已读取，实际响应/数据哈希是复现依据。

实际命令cwd=/home/desktop/Documents/Codex/EquiTide，解释器/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B。review/launch.py依次bootstrap.py、review/preflight.py、review/prepare.py、review/setup.py；review/execute.py依次freeze units bind reserve_0 evaluate audit exports finish_0 research_check；diagnostics/historical_aliases；原账户midnight_archive l4h02 fewm candidate forward accounts_check；实际view_image后visual_review/account_continuity/complete_transport_audit/validate_sources；journal sources_check gates feed collect final_checks、staged_whitespace、seal/publish。实际命令/UTC/退出码/log保留；prepare/setup为首次源变换，不在已变换源上重复。已有实际ID禁止精确回测或覆盖归档，forward --reproduce只读核验不新增窗口。

实际阻碍/失败：{"round": "20261115T095944Z", "facts": [{"type": "transient_public_GET_failure", "url": "https://fapi.binance.com/fapi/v1/fundingRate?symbol=BTCUSDT&startTime=1794702600001&endTime=1794715800000&limit=1000", "raw": "research/experiments/20261115T095944Z/window_funding_preflight/BTC_0.json.gz", "sha256": "f61f27bd17de546264aa58f40f3aafaac7021e0ef69c17f6b1b4cd7664a037ec", "original_capture_utc": "2026-11-15T10:04:43.800408Z", "http_status": 0, "curl_exit_code": 35, "stderr": "curl: (35) TLS connect error: error:0A000126:SSL routines::unexpected eof while reading\n", "resolved": true, "recovery": "Subsequent bounded verified-TLS GET for same URL succeeded; original failure retained, account/model window executed once."}, {"type": "transient_public_GET_failure", "url": "https://fapi.binance.com/fapi/v1/fundingRate?symbol=ETHUSDT&startTime=1794702600001&endTime=1794715800000&limit=1000", "raw": "research/experiments/20261115T095944Z/window_funding_preflight/ETH_0.json.gz", "sha256": "f61f27bd17de546264aa58f40f3aafaac7021e0ef69c17f6b1b4cd7664a037ec", "original_capture_utc": "2026-11-15T10:04:50.896647Z", "http_status": 0, "curl_exit_code": 35, "stderr": "curl: (35) TLS connect error: error:0A000126:SSL routines::unexpected eof while reading\n", "resolved": true, "recovery": "Subsequent bounded verified-TLS GET for same URL succeeded; original failure retained, account/model window executed once."}, {"type": "transient_public_GET_failure", "url": "https://fapi.binance.com/fapi/v1/fundingRate?symbol=ETHUSDT&startTime=1794700800002&endTime=1794715800000&limit=1000", "raw": "data/raw/binance/l4h02_forward/20261115T095944Z/http_0007.gz", "sha256": "f61f27bd17de546264aa58f40f3aafaac7021e0ef69c17f6b1b4cd7664a037ec", "original_capture_utc": "2026-11-15T10:10:40.823555+00:00", "http_status": 0, "curl_exit_code": 35, "stderr": "curl: (35) TLS connect error: error:0A000126:SSL routines::unexpected eof while reading\n", "resolved": true, "recovery": "Subsequent bounded verified-TLS GET for same URL succeeded; original failure retained, account/model window executed once."}, {"type": "diagnostic_read_path_failure", "recorded_utc": "2026-11-15T10:23:04.488117+00:00", "command": "cat research/experiments/20261115T095944Z/complete_transport_audit.json research/experiments/20261115T095944Z/read_failures.json", "cwd": "/home/desktop/Documents/Codex/EquiTide", "native_chunk_id": "ee3494", "exit_code": 1, "stderr": "cat: research/experiments/20261115T095944Z/complete_transport_audit.json: No such file or directory", "resolved": true, "recovery": "Read the actual complete_transport_verification.json; financial/account calculations unaffected."}]}。保留全部正/负/淘汰/失败、原账户账本、冻结规则、登记、必要原包/哈希和下轮状态，清理可重建缓存，大行情忽略。6金融+12实际观察/36事件独立归档；锁内snapshot只读汇总既有账户/报告，不新回测/成交/部署/定时任务。最终commit/push、完整远端树/blob与解锁后检查见.git/automation_proofs实际回执。
