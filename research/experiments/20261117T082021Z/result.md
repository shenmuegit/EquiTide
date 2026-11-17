本轮完成ETH退出缓冲E=.00625/.00875两个原生组件，以及交叉已有BTC H.03/.0325银行的四个新父组合，共6项/18条新成本场景。E.0075旧基准及BTC/持有共8配置/24场景只读。历史通过4（父4、组件0），淘汰2，所有结果均finish。12个原冻结账户观察独立reserve/finish，partial rejected不取消长期计划。

事前假设：更早或更晚退出反弹，可能改变利润捕获与持仓风险。固定L5/H.02、EWMS16 beta15/17、D3严格K.0075、V6样本logvol上限.05625、M4/R.0075/VW8；仅退出E=[.00625,.0075,.00875]，交叉只读BTCH=[.03,.0325]。代表E.00625/BTCH.03在结果前固定，不事后改代表、扩批或调门槛。

完整读取37256条登记事件/18489ID、451份结论及11425个排除观察的规范研究定义（非独立试验数）；读取task/README/三技能、checks/*oos.py及Freqtrade原ZIP，初始16项缺实际结果0，legacy/false及旧失败保留。语义查重确认两个新E不存在已测/运行中的精确配置，保护86073旧文件和paper10账本/报价；逐项reserve成功才计算。

ETH long-only本金15000/固定名义4000。快ROC r=最后完成日close/5日前完成日close−1：r>H先给−1、r<−H先给+1；带内actual+1仅r<E保留、actual−1仅r>−E保留，否则0，等号退出。有限归一化EWMS16斜率D3严格K.0075筛新/反手方向；V6风险与M4已实现有符号资金费中位数仅筛新/反手，已持q与正常退出保留，最终max(desired,0)。资金费年龄1–36h含端点、available≤signal，偶数取中间两率均值；允许支出min(.0002,.0075×过去8完整日无偏样本logvol×最近合格已知真实结算间隔小时/24)，相等通过，缺失阻新仓。预算VW8/风险V6/冲击V20分开；H及long/short_entry_return_hurdle始终.02，仅exit_buffer_fraction为新E。

BTC旧银行本金3750/固定名义1000，L29主ROC严格H.03/.0325入场、E.005带内退出，V10 cap.0275、最近5日同向ROC严格>.0025仅筛新/反手，已有q保留；本轮不重新计算BTC。父本金18750/raw[1,1]直接相加两原银行美元NAV，20/80只是初始本金占比，权重不归一化，无缩放/转账/再平衡/父订单/跨保证金；组合对齐完整事件轴后重算整体DD，不能平均收益或Sharpe。

Walk-forward：2025-10-19T00:01Z→2026-11-14T00:01Z，共391日/33日背景，每币610562分钟bar、10176小时mark、1273实际资金费，8个Parquet SHA/UTC单位/闭合/可得时间核验。13完整30日折+1日尾，跨折继承现金/q，仅全期终止按成本平仓；整体DD来自连续完整事件NAV。近期40日8×5与扩展21日5+5+5+6逐折保留，1日尾Sharpe=None。固定规则无拟合/标签，仅完成前缀，OOS指复用开发历史，不是未触碰最终集或独立未来；多重选择偏差未消除，无DSR/PBO显著性结论。

敏感性：事前固定ETH退出E×BTC主H的3×2父格，ETH组件仅沿自身E、BTC仅沿自身H；保存净收益、全路径DD、Sharpe、Calmar、近期折及全部并列最优边界。局部3倍净正与严格近期合格比例各≥60%。10邻边的abs(deltaSharpe)>2×sampleSTD(absdeltas)仅为描述性启发，不是显著性或过拟合概率；小邻域不证明宽平台或全局最优。

成本：每边手续费5bp+半价差1bp+滑点2bp+0.5×过去20完整日samplelogvol×sqrt(abs(q)×真实OPEN/过去20日quoteADV)，不利tick、实际LOT/minnotional；参与率≤.1%、费后1倍抵押、闭合小时high/low的1%维持保证金代理。执行成本和负资金费1/2/3倍，收入不放大；线性永续不用现货借币。费/盘口为估计，缺历史L2/TCA、完整保证金档位、tick强平及容量证明。

冻结通过门槛：全期/近期三成本净正、1倍≥10/13正完整月、近期各成本≥6/8正5日折、扩展21日各成本净正且≥3/4正折；3倍DD≤25%，两项局部比例各≥60%，至少4底层平仓，1倍(毛价PnL+净资金费)/执行成本≥2.5；无拒单/负抵押/保证金代理违规、期末平仓且≥180日。任一失败即淘汰，全部原因保留。

|ETH退出E|BTC主H|来源/状态|1x净%|2x净%|3x净%|3x整体DD%|正月/13|近期正折1/2/3|
|---:|---:|---|---:|---:|---:|---:|---:|---|
|0.00625|0.03|新/passed|9.119819920|8.633459365|8.147280124|1.357833669|12|6/6/6|
|0.00625|0.0325|新/passed|9.012220280|8.526556052|8.041073107|1.357833669|12|6/6/6|
|0.0075|0.03|旧只读/passed|9.119819920|8.633459365|8.147280124|1.357833669|12|6/6/6|
|0.0075|0.0325|旧只读/passed|9.012220280|8.526556052|8.041073107|1.357833669|12|6/6/6|
|0.00875|0.03|新/passed|9.119819920|8.633459365|8.147280124|1.357833669|12|6/6/6|
|0.00875|0.0325|新/passed|9.012220280|8.526556052|8.041073107|1.357833669|12|6/6/6|


事前代表E.00625/BTCH.03（0c3270a363f7858d166dd793e8eec76515d6ca9fd4e124ba369abce0135cbb1b）三成本净9.119819920%/8.633459365%/8.147280124%；3倍DD 1.357833669%，Sharpe 2.365155831，Calmar 5.586463398，passed，失败项[]。

ETH E=0.00625组件rejected，三成本净6.842224015%/6.541435053%/6.240856055%，3倍DD 1.528984097%，正月6/13，近期正折{'1': 0, '2': 0, '3': 0}，失败项['ten_of_thirteen_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct', 'extension21_positive_all_costs', 'extension21_three_of_four_positive_folds_all_costs']。

ETH E=0.00875组件rejected，三成本净6.842224015%/6.541435053%/6.240856055%，3倍DD 1.528984097%，正月6/13，近期正折{'1': 0, '2': 0, '3': 0}，失败项['ten_of_thirteen_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct', 'extension21_positive_all_costs', 'extension21_three_of_four_positive_folds_all_costs']。

对旧E.0075/同BTCH0.03：新E0.00625的3倍净变化+0.000000000个百分点、整体DD变化+0.000000000个百分点、Sharpe +0.000000000、Calmar +0.000000000。

对旧E.0075/同BTCH0.0325：新E0.00625的3倍净变化+0.000000000个百分点、整体DD变化+0.000000000个百分点、Sharpe +0.000000000、Calmar +0.000000000。

对旧E.0075/同BTCH0.03：新E0.00875的3倍净变化+0.000000000个百分点、整体DD变化+0.000000000个百分点、Sharpe +0.000000000、Calmar +0.000000000。

对旧E.0075/同BTCH0.0325：新E0.00875的3倍净变化+0.000000000个百分点、整体DD变化+0.000000000个百分点、Sharpe +0.000000000、Calmar +0.000000000。

同BTC旧基准的四项严格联合改善0/4组；全差异与取舍保留，组合通过不覆盖组件失败，原账户不采用新E。

6新配置全成本NAV签名3组，匹配8网格/持有参考3组、上轮实际路径6/6、更早同其他参数E/R的6组件/12父中匹配6/6。另旧BTC总波动上限9组件/18父匹配0/6。完整391日目标/持仓/成交/资金费与相同完整NAV的核对见bank_path_alias_verification.json，精确不同配置不等于独立市场样本。启发跳变1/10，绝对Sharpe变化[0.0, 0.04858481063530795]、STD 0.018593175；父格净正/正Sharpe/严格近期比例1.0/1.0/1.0。

本轮两个退出E的新组件及对应父路径均与旧E.0075相同：本批仅3条不同全成本路径，6个新配置全部匹配既往真实路径，没有新增独立alpha或收益改善；退出缓冲在本条件邻域没有改变任何最终目标、持仓、成交或资金费。ETH扩展21日PnL全为零：True，近期组合通过不能当作ETH组件稳健性通过。

只读分解E0.00625对旧E.0075：毛价格PnL变化+0.000000000USDT、资金费变化+0.000000000、执行费变化+0.000000000、净差+0.000000000、执行数差0；同BTC父净差+0.000000000个百分点。

只读分解E0.00875对旧E.0075：毛价格PnL变化+0.000000000USDT、资金费变化+0.000000000、执行费变化+0.000000000、净差+0.000000000、执行数差0；同BTC父净差+0.000000000个百分点。

独立核对新原生6/父12、旧原生15/父9成本曲线，新决策2346、旧决策5865；42场景、588逐折、336近期折、168扩展折、16464日NAV、18持有对照、10邻边/六面板留档。匹配持有3倍净-14.782911083%、整体DD 18.454766592%，现金0。引擎/货币核心源字节不改，354个严格H/E/等号/成熟性/缺失/预算/未来后缀合成检查及资产轴检查先于reserve；实际两个ETH各计算一次完整391日，不线性缩放旧NAV、不精确重跑旧配置。

原账户SMA/single22:30→Nov17_00:30，L4/FEWM00:10→02:10；新日事件{'SMA': 1, 'candidate': 1, 'l4h02': 0, 'fewm': 0}、资金费记录{'SMA': 0, 'candidate': 6, 'l4h02': 0, 'fewm': 0}、成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}。single用自己的结算前q记真实1794873600000ms资金费并执行原日内核，L4/FEWM不重记已完成午夜；三个永续全链Nov17_00及原00:01日决策现各一次，旧Nov13–16也保持各一次。不得复制其他账户现金流。

SMA真实69日SPOT权威research/experiments/20261117T082021Z/forward_inputs.json.gz、SHA cfc1d7777fe9ae133c9b67fb254c4188d1f3dbcbb7a38b1c83ac5e69ac16a94b，原68/67/66/65前缀全相等。原SMA65/对称1%/Float、本金1500:500/raw75:25及10bp手续费+1bp半价差+2bp滑点+过去20日ADV冲击不改，不追溯新LOT/tick。原daily simulate函数AST与20261116T080637Z完全相同。新增120闭合分钟及1个原日参考，每币1次日决策、成本场景订单总数0，累计66269分钟/66317点；三倍净-7.468957812%，负结果保留。延迟shadow不是十策略真实报价成交；原2027-03-31终止计划不改、不强平。

本轮SMA/single从Nov16_22:30接续至Nov17_00:30：SMA已补真实69日SPOT背景并核对原68/67/66/65前缀，用原SMA65/对称1%/Float/10bp费用执行00:01日决策；single按自己的结算前q记真实午夜资金费，再执行原冻结日内核。L4/FEWM本轮00:10→02:10只追加闭合数据，不重复上轮已记的00资金费和00:01日决策。现三个永续的Nov17午夜及四账户原日决策均各一次；下一日决策全部为Nov18_00:01。下轮SMA/single00:30→02:30（02:31闭合）、L4/FEWM02:10→04:10（04:11闭合）均mark-only，仍完整新查真实结算，不预设名义8小时时刻，不重记已知午夜。SMA必须保留本轮full69权威与68/67/66/65前缀，使用保留的mark-only模板，不能把本轮仅用于跨日的daily wrapper直接用于非跨日窗口；未来Nov18跨日再沿用原日计算函数并补新闭合日。各账户本金、规则、持仓及各自冻结终止日保持；原SMA终止日仍为2027-03-31，不采用本轮研究退出E、不重启或强平。

Nov17午夜源仍是首捕获UTC 2026-11-17T06:24:46.678539Z、SHA 0580bfb3e40a5cd47ca809993996edccb69519db61e13c04f5b3caaf9cc0a778；本轮22:30→02:10新查询UTC 2026-11-17T08:24:27.087420Z仅确认同一条BTC/ETH真实结算，原源与捕获UTC原字节保持，不重标时间。SMA69四个SPOT原包及所有公开原响应/单位/重叠均留档。

有包公共GET 25次、实际传输失败4次；FEWM/cached metadata/time按原路径+URL精确去重，prefetch与实际SMA调用复用同一原包，不重复下载；失败若有保留URL/原始body/SHA/真实退出码，不编造缺失失败体。

原L4捕获曾在三次公开时间GET的TLS协商中失败，且发生在任何观察reserve/账户advance之前。失败窗口、全部原始响应和真实日志保留；仅改为验证证书的TLS>=1.2协商并使用独立retry原包目录，成功后原账户首次推进一次；重试另有一次exchangeInfo TLS失败后恢复，均计入完整公开GET审计。金融回测未重跑。

复现cwd=/home/desktop/Documents/Codex/EquiTide，既有venv python -B。launch bootstrap/preflight/prefetch_sma69/screen_exit_buffers/configure_exit_buffers/configure_accounts/setup_confirmation/prepare_confirmation/prepare_diagnostics/configure_report；freeze units bind reserve_0 evaluate audit exports finish_0 research_check；diagnostics/historical_aliases/totalrisk_history_aliases/budget_effect/older_exit_aliases；实际view_image后visual_review/diagnostic_review；midnight_archive；首次l4h02捕获失败后prepare_l4h02_transport_recovery；l4h02_retry1；finish_l4h02_transport_recovery；fewm candidate forward accounts_check；account_continuity/complete_transport_audit/validate_sources；journal sources_check gates feed collect；verify_midnight_handoff/final_checks/staged_whitespace；封存/发布助手。精确命令/UTC/退出码/stdout见真实回执，完成目录不重复reserve/evaluate或重放账户；forward --reproduce只核验原包和全净值，不发HTTP或写账本。

391日复用开发历史、多重选择偏差与有限参数邻域仍不足独立未来证明，正收益回测不称稳定实盘盈利。本轮读取[Binance官方市场/资金费文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)及[官方公共数据README](https://github.com/binance/binance-public-data/blob/master/README.md)，真实输入及原包SHA是复现依据。

实际失败/阻碍：{"round": "20261117T082021Z", "facts": [{"command": ["/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python", "-B", "/home/desktop/Documents/Codex/EquiTide/research/experiments/20261117T082021Z/observe_l4h02.py"], "cwd": "/home/desktop/Documents/Codex/EquiTide", "started_utc": "2026-11-17T08:54:15.841582Z", "finished_utc": "2026-11-17T08:54:32.691723Z", "exit_code": 1, "log": "research/experiments/20261117T082021Z/l4h02_observe.log", "stderr": "Traceback (most recent call last):\n  File \"/home/desktop/Documents/Codex/EquiTide/research/experiments/20261117T082021Z/observe_l4h02.py\", line 19, in <module>\n    obs.request=request;sys.argv=[str(SOURCE/'observer.py'),'run','--round',R.name,'--cutoff',plan['cutoff_utc'],'--lock-pid',str(plan['branch_lock_broker_pid'])];obs.main()\n                                                                                                                                                                   ^^^^^^^^^^\n  File \"/home/desktop/Documents/Codex/EquiTide/research/experiments/20261031T174613Z/prospective_l4/observer.py\", line 128, in main\n    packet=capture(cut,previous,binding,rawdir,receipts);packetpath=rawdir/'packet.json.gz';gzput(packetpath,packet);put(window/'input_manifest.json',{'packet':rel(packetpath),'sha256':c.sha(packetpath),'provenance':receipts,'plan_sha256':binding['plan_sha256']})\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/desktop/Documents/Codex/EquiTide/research/experiments/20261031T174613Z/prospective_l4/observer.py\", line 46, in capture\n    info=request('/fapi/v1/exchangeInfo',{},rawdir,receipts);server=request('/fapi/v1/time',{},rawdir,receipts);retrieved=min(now(),int(server['serverTime'])*c.MS)\n                                                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/desktop/Documents/Codex/EquiTide/research/experiments/20261117T082021Z/observe_l4h02.py\", line 18, in request\n    raise RuntimeError('Three bounded public GET attempts failed;preserve account and capture failure')\nRuntimeError: Three bounded public GET attempts failed;preserve account and capture failure\n", "resolved": true, "recovery": "Before-reservation TLS capture failure archived. Verified >=TLS1.2 negotiation and a separate retry HTTP directory succeeded; original account advanced once after its first successful reserve; no completed financial/account rerun.", "effective_successful_commands": "research/experiments/20261117T082021Z/l4h02_retry1_commands.json", "effective_successful_commands_sha256": "7df67d772a3ca403d21d0706ca3d47353fc012ff01bd96e5ad5b4c0eac272000"}, {"type": "transient_public_GET_failure", "url": "https://fapi.binance.com/fapi/v1/exchangeInfo", "raw": "data/raw/binance/l4h02_forward/20261117T082021Z_retry1/http_0000.gz", "sha256": "f61f27bd17de546264aa58f40f3aafaac7021e0ef69c17f6b1b4cd7664a037ec", "original_capture_utc": "2026-11-17T09:04:31.994036+00:00", "http_status": 0, "curl_exit_code": 35, "stderr": "curl: (35) TLS connect error: error:0A000126:SSL routines::unexpected eof while reading\n", "resolved": true, "recovery": "Subsequent bounded verified-TLS GET for same URL succeeded; original failure retained, account/model window executed once."}, {"type": "transient_public_GET_failure", "url": "https://fapi.binance.com/fapi/v1/time", "raw": "data/raw/binance/l4h02_forward/20261117T082021Z/http_0001.gz", "sha256": "f61f27bd17de546264aa58f40f3aafaac7021e0ef69c17f6b1b4cd7664a037ec", "original_capture_utc": "2026-11-17T08:54:17.596181+00:00", "http_status": 0, "curl_exit_code": 35, "stderr": "curl: (35) TLS connect error: error:0A000126:SSL routines::unexpected eof while reading\n", "resolved": true, "recovery": "Subsequent bounded verified-TLS GET for same URL succeeded; original failure retained, account/model window executed once."}, {"type": "transient_public_GET_failure", "url": "https://fapi.binance.com/fapi/v1/time", "raw": "data/raw/binance/l4h02_forward/20261117T082021Z/http_0002.gz", "sha256": "f61f27bd17de546264aa58f40f3aafaac7021e0ef69c17f6b1b4cd7664a037ec", "original_capture_utc": "2026-11-17T08:54:22.610156+00:00", "http_status": 0, "curl_exit_code": 35, "stderr": "curl: (35) TLS connect error: error:0A000126:SSL routines::unexpected eof while reading\n", "resolved": true, "recovery": "Subsequent bounded verified-TLS GET for same URL succeeded; original failure retained, account/model window executed once."}, {"type": "transient_public_GET_failure", "url": "https://fapi.binance.com/fapi/v1/time", "raw": "data/raw/binance/l4h02_forward/20261117T082021Z/http_0003.gz", "sha256": "f61f27bd17de546264aa58f40f3aafaac7021e0ef69c17f6b1b4cd7664a037ec", "original_capture_utc": "2026-11-17T08:54:27.622501+00:00", "http_status": 0, "curl_exit_code": 35, "stderr": "curl: (35) TLS connect error: error:0A000126:SSL routines::unexpected eof while reading\n", "resolved": true, "recovery": "Subsequent bounded verified-TLS GET for same URL succeeded; original failure retained, account/model window executed once."}], "no_completed_model_or_account_window_replays": true}。所有正负、淘汰、失败、完整原账本/冻结规则/登记记录和下轮必要状态保留，仅清理可重建缓存。监控仅只读汇总，不新回测、生成新模拟成交、改冻结规则或重部署网页；实际commit/push/远端树和解锁后核验存.git/automation_proofs。
