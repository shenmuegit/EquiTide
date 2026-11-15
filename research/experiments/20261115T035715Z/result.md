本轮真实完成6个新金融配置：BTC V10入场波动率上限4%/5%两个原生组件，与已有ETH资金费预算R=.00875/.01组成四个父组合，共18条1/2/3倍成本场景。父组合历史通过4个，BTC原生组件通过0个、淘汰2个；8个旧实际配置/24场景只读复用。另12项原冻结账户窗口实际观察各自reserve/finish，未成熟180日的partial rejected不取消长期计划。

事前假设：固定BTC ROC L29/H3%/退出E0.5%与过去V10样本日log波动率，放宽入场上限4%/5%能否保留有用趋势入场，改善经成本时序稳健性；旧3%中心只读。BTC cap=[.03,.04,.05]×已有ETH R=[.00875,.01]组成3×2面，代表cap4%/R.01在结果前指定，取适度放宽而非不限制入场。完整核心参数/币种/边界查重不依赖名称/family/continuous_days标记，确认新4%/5%配置无实际结果；没有事后扩网格或换代表。

BTC本金3750/固定入场名义1000。只读已完成日收盘ROC，严格r>3%多、r<−3%空；带内已持多头仅r>−.005保留、空头仅r<.005保留，相等退出。仅新/反手检查过去V10日samplelogvol≤cap，等于上限允许；实际同向q保留，不因门强制退出。LOT向下，信号后下一00:01真实OPEN不利tick。每个新cap按完整391日从原现金计算数量、费用、成交量冲击、资金费和保证金，不复用新参数的货币前缀。

ETH银行完全只读：本金15000/固定名义4000，long-only L5/H2%/退出E.75%，有限归一化EWMS16 beta15/17、D3严格K.75%、V6 cap5.625%。最近4笔实际已结算有符号资金费取中位数，合格年龄1–36小时且source_available≤signal，缺4笔阻止新仓；预算min(.0002,R×过去V8日samplelogvol×最新合格实际过去结算间隔小时/24)。R原值.00875/.01；仅新入场检查，收入不放大，原同向q及退出保持。旧文字E.005过期而机器一直E.0075，旧spec/status/报告字节保留，不将文字修正算新定义。

父组合本金18750，raw[1,1]相加BTC3750和ETH15000两个完整独立原规模银行的美元NAV，20/80仅初始本金占比；保留权重原值，不归一化、不缩放、不转账/再平衡/父订单/跨保证金。对齐全部事件时间轴重算连续NAV及整体DD，不平均收益、Sharpe或回撤。

完整读取35844登记事件/17789ID、426份既往结论、task/README/三技能/OOS与freqtrade原ZIP；初始16条缺实际历史结果为0，保留legacy/false原行及所有原负收益。基于03UTC paper10的最新main；上轮push、远端及解锁后证明已核对，无旧reserved。保护77319份旧文件，paper10冻结计划、完整账本和已有报价观察保持原字节。

Walk-forward已执行：2025-10-19T00:01Z→2026-11-14T00:01Z，391日加33日背景；每币610562分钟bar、10176小时mark、1273实际资金费，8份Parquet的SHA、单位、可得/闭合与连续性检查。固定规则、无拟合或标签，特征只读当时前缀；13完整30日折+1日尾折，现金/持仓跨折连续，仅全期末计成本平仓，整体DD来自全事件NAV。近40日8×5及扩展21日5+5+5+6逐折保留，尾折Sharpe=None且不计完整正月门槛。无标签时purge/embargo无标签用途，实际33日特征背景/下一可执行OPEN和资金费成熟边界独立检查。历史已反复开发，本轮未加入新完整研究日，不能称未触碰最终留出或独立未来。

Sensitivity已执行：3档BTC cap×2档ETH R全部六格，BTC原生只沿cap、ETH原生只沿R；净收益/整体DD/Sharpe/Calmar、近期正折、所有并列最佳边界及10条相邻变化留档。局部3倍净正与严格近期比例门槛各60%。4%/5%参数虽不同，实际资金路径相同：六新定义只有三组三成本路径；原生391个目标/前后账簿、全部成交及资金费的相等性另行核验。不能将平坦图形解释为独立收益证据或广泛稳健平台。

Costs已执行：每边手续费5bp+半价差1bp+滑点2bp+0.5×过去20日samplelogvol×sqrt(abs(q)×真实OPEN/过去20日quoteADV)，不利tick；执行成本与负资金费1/2/3倍，收入不放大。含实际LOT/tick/minnotional、参与率≤0.1%、费后1倍抵押、闭合小时high/low的1%维持保证金代理。线性永续不借现货，不编借币费。费率/价差仍是估计，缺历史L2/TCA、完整档位、tick强平及真实容量证明；逐场景成交数、成本分项/占比和匹配持有/现金0对照均保存。

预设门槛：三成本全期/近期净正；1倍≥10/13正完整月；各成本近期≥6/8正5日折；扩展21日净正且≥3/4正折；3倍DD≤25%；适用局部两比例≥60%；至少4底层平仓；1倍(毛价格PnL+净资金费)/执行成本≥2.5；无拒单/负抵押/保证金代理违规，期末平仓且≥180日。任何失败即rejected，仍保存真实完整结果。

|BTC入场波动上限|ETH预算R|来源/状态|1x净%|2x净%|3x净%|3x整体DD%|正月/13|近期正折1/2/3|
|---:|---:|---|---:|---:|---:|---:|---:|---|
|3%|0.00875|旧只读/passed|9.000028418|8.422242505|7.844642170|1.362719676|12|6/6/6|
|3%|0.01|旧只读/passed|8.938432608|8.356808345|7.775369660|1.362719676|12|6/6/6|
|4%|0.00875|新/passed|8.758831040|8.161735167|7.564809887|1.418018270|11|6/6/6|
|4%|0.01|新/passed|8.697235230|8.096301007|7.495537377|1.418018270|11|6/6/6|
|5%|0.00875|新/passed|8.758831040|8.161735167|7.564809887|1.418018270|11|6/6/6|
|5%|0.01|新/passed|8.697235230|8.096301007|7.495537377|1.418018270|11|6/6/6|


事前代表cap4%/ETH R.01（1170a77a66bcdc72a8aabd0bf610d3af7e158b07cb8473aa2e0f8ae94a3f94e5）：三成本净8.697235230%/8.096301007%/7.495537377%，3倍DD1.418018270%，Sharpe2.110509787、Calmar4.922449047，passed、失败项[]。

BTC cap4%组件rejected：三成本净15.271345018%/13.770769134%/12.270205967%，3倍DD6.811607873%，正月9/13、近期正折{'1': 6, '2': 6, '3': 6}，失败项['ten_of_thirteen_positive_complete30d_1x_folds']。

BTC cap5%组件rejected：三成本净15.271345018%/13.770769134%/12.270205967%，3倍DD6.811607873%，正月9/13、近期正折{'1': 6, '2': 6, '3': 6}，失败项['ten_of_thirteen_positive_complete30d_1x_folds']。

两个BTC组件全期与近期虽正，只有9/13正完整月，未达到10/13门槛而淘汰；四父组合各11/13正月、近期6/8，达到历史门槛。四新父相对相同ETH预算的旧cap3，全期净收益/Sharpe/Calmar均降低、整体DD由约1.362720%升至1.418018%，绝对增加约0.0553个百分点，自动缩放色彩不代表巨大绝对风险变化。未发现放宽上限的改进，不采纳新冻结规则。只读ETH近期仍不合格，其扩展21日PnL为0；父组合该段利润由BTC贡献，父通过不能替代组件资格。

六新定义的三成本NAV签名3组，匹配八个旧预登记参考0组，上轮实际新/只读配置匹配0/6。新父3倍净收益低于对应cap3为4个、相同0个。4%与5%在本历史样本全部实际目标/状态/成交/资金费/NAV相同不代表所有市场未来等价；参数不同因此均独立登记finish，未重复计作独立alpha。

原始abs(deltaSharpe)>2×sampleSTD(absdeltas)启发式标记1/10，绝对变化范围[0.0, 0.13910276025466217]、样本STD0.047664469，全部保存，不是统计显著性或过拟合概率。最佳旧cap3在边界、ETH只有两档，不能证明宽平台；所有指标并列最优见sensitivity_metric_boundaries。父网格3倍净正/正Sharpe/严格近期比例1.000000/1.000000/1.000000。

匹配持有3倍净-14.782911083%、DD18.454766592%，现金0；18个父成本场景的BTC/ETH全期及扩展PnL加总守恒独立核对。新原生6条/新父12条、旧原生15条/旧父9条场景审计；新决策2346、旧只读5865；42成本场景、588逐折、336近期折、168扩展折、16464日NAV、18持有对照、10相邻边和3×2热图保留。引擎所有函数AST和核算核心字节与前轮相同，每个新配置先reserve后计算并finish，完整金融评估只执行一次。

原冻结账户本轮SMA/single Nov14_20:30→22:30，L4/FEWM Nov14_22:10→Nov15_00:10；日事件{'SMA': 0, 'candidate': 0, 'l4h02': 1, 'fewm': 1}，实际成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}，资金费记录{'SMA': 0, 'candidate': 0, 'l4h02': 6, 'fewm': 6}。真实结算fundingTime=1794700800002毫秒（Nov15_00:00:00.002）早于原00:01日决策。L4/FEWM各6条BTC/ETH×三成本资金费按自己当时q计算，收入不放大/支出乘成本倍数，未复制另账户现金流；随后各6个原因果日决策及任何原规则实际模拟成交、现金/数量/费用逐项核对。合并各自partial为完整Nov14日收盘/成交量，完整NAV前缀与所有历史资金费/日事件唯一键通过。

原SMA仍仅闭合分钟估值，完整66日权威research/experiments/20261114T035058Z/forward_inputs.json.gz与旧65前缀一致，当前包只有分钟。累计63269分钟/63314点，原65/对称1%/Float/本金1500:500/raw75:25不变；组合3倍累计净-7.468957812%，负收益完整保留，不以研究组合覆盖。原账户未成熟180日，延迟shadow不冒充十策略真实报价模拟。

本轮SMA/single Nov14_20:30→22:30仅闭合分钟估值；L4/FEWM Nov14_22:10→Nov15_00:10已完成真实午夜结算与Nov15_00:01原日决策，合并各自partial为完整Nov14日量/收盘，账簿现金/数量只按各自原核算核变化，不采用研究cap4/5。下轮SMA/single22:30→Nov15_00:30，00:31后参考闭合，实际跨Nov15_00:01，SMA必须取得完整67日背景并与旧66逐项前缀一致，使用原65/对称1%/Float/本金1500:500/raw75:25日适配器，不能继续mark-only或把当前minute包当全日背景；single真实午夜结算需按自己的既有q计费，不能复制L4/FEWM现金流。L4/FEWM下轮00:10→02:10，02:11后闭合，下一原日事件Nov16_00:01；Nov15午夜和日决策已各记一次，不重复。重新核对实际fundingTime，不硬编码名义八小时。不重开、强平、转账或改冻结本金/规则/持仓，保留全部旧blocked与paper10账本。

新午夜公开字段原捕获UTC2026-11-15T04:00:17.177433Z保留；旧Nov14_08捕获UTC2026-11-14T09:56:41.855564Z、16捕获UTC2026-11-14T17:58:56.177141Z不重标。本轮L4/FEWM已记Nov15午夜与日决策，single尚未记，明确留待下一实际窗口。

独立保存公共GET 20次、真实传输失败2次，URL/UTC/raw/body/gzipSHA及真实失败回执保留；FEWM只复用同窗公开数据，candidate只复用metadata/time，账户现金流独立。SMA内部curl没有单独保存体/精确UTC的重试仅按stderr披露，不补造。

391日历史反复用于开发，多重选择偏差未消除，无DSR/PBO显著性结论；正收益回测不是稳定实盘盈利。[Binance官方市场/资金费文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)及[官方公共数据README](https://github.com/binance/binance-public-data/blob/master/README.md)本轮已读取，实际原响应/输入哈希是复现依据。

实际命令cwd=/home/desktop/Documents/Codex/EquiTide，解释器/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B。review/launch.py依次bootstrap.py、review/preflight.py、review/prepare.py、review/setup.py；review/execute.py依次freeze units bind reserve_0 evaluate audit exports finish_0 research_check；只读diagnostics/historical_aliases；原账户midnight_archive l4h02 fewm candidate forward accounts_check；实际view_image后visual_review/account_continuity/complete_transport_audit/validate_sources；再journal sources_check gates feed collect final_checks、staged_whitespace、seal/publish。真实命令/UTC/退出码/log保留；prepare/setup为从上轮模板生成冻结源的一次预处理，不可在已变换源上重复；已有实际ID禁止精确回测或覆盖归档，forward --reproduce只读核验不新增窗口。

实际阻碍/失败：{"round": "20261115T035715Z", "facts": [{"type": "transient_public_GET_failure", "url": "https://fapi.binance.com/fapi/v1/klines?symbol=ETHUSDT&interval=1m&startTime=1794694140000&endTime=1794701400000&limit=1500", "raw": "data/raw/binance/l4h02_forward/20261115T035715Z/http_0005.gz", "sha256": "f61f27bd17de546264aa58f40f3aafaac7021e0ef69c17f6b1b4cd7664a037ec", "original_capture_utc": "2026-11-15T04:06:16.497281+00:00", "http_status": 0, "curl_exit_code": 35, "stderr": "curl: (35) TLS connect error: error:0A000126:SSL routines::unexpected eof while reading\n", "resolved": true, "recovery": "Subsequent bounded verified-TLS GET for same URL succeeded; original failure retained, account/model window executed once."}, {"type": "transient_public_GET_failure", "url": "https://fapi.binance.com/fapi/v1/fundingRate?symbol=BTCUSDT&startTime=1794672000000&endTime=1794695400000&limit=1000", "raw": "data/raw/binance/candidate_forward/20261115T035715Z/http_attempt_0002.gz", "sha256": "f61f27bd17de546264aa58f40f3aafaac7021e0ef69c17f6b1b4cd7664a037ec", "original_capture_utc": "2026-11-15T04:08:14.749014+00:00", "http_status": 0, "curl_exit_code": 35, "stderr": "curl: (35) TLS connect error: error:0A000126:SSL routines::unexpected eof while reading\n", "resolved": true, "recovery": "Subsequent bounded verified-TLS GET for same URL succeeded; original failure retained, account/model window executed once."}]}。保留全部正/负/淘汰/失败、账本、冻结规则、登记、原包/哈希/下轮状态，清理本轮可重建缓存，大行情忽略。6金融+12实际观察/36事件独立归档。锁内snapshot仅只读汇总已有账户和报告，不新增回测、成交、部署或任务；commit/push/完整远端树/blob/实际解锁与解锁后检查见.git/automation_proofs回执。
