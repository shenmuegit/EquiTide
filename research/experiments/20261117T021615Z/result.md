本轮完成6个新金融配置：固定R=.0075/VW8，ETH过去实际资金费中位数笔数M2/M3两个原生组件，交叉已有BTC H3%/3.25%银行形成四父；M4R.0075只读。18条新1/2/3倍成本场景，8旧网格/持有配置24场景只读。历史通过4（父4、组件0），淘汰2，全部失败项保留。12原账户观察独立reserve/finish，partial rejected不取消长期计划。

事前假设：较少笔数的中位数更快响应已实现carry，可能减少陈旧门槛，也可能增加估计噪声。M=[2,3,4]×只读BTCH=[.03,.0325]，预算R=.0075/VW8固定；代表M2/BTCH.03在结果前固定，不事后扩批、换代表或改失败门槛。W为ETH统计笔数，K为BTC主阈值，单币只沿自身适用轴。

完整读取37088登记事件/18405ID、448份结论、11407个排除观察的规范研究定义（非独立试验数），task/README/三技能、checks/*oos.py与freqtrade原ZIP。初始16项缺实际结果0，legacy/false与全部负结果保持；保护84912旧文件及paper10账本/报价。语义查重已找到R.01/.00875的M2/M3真实结果，均只读不重测；本轮R.0075下M2/M3不存在已测/运行中精确配置，逐项reserve成功后才计算。查询完整表见tight_budget_median_prior_lookup.json。

ETH本金15000/固定名义4000，long-only L5/H.02/E.0075、有限归一化EWMS16 beta15/17、D3严格K.0075，V6已完成样本logvol上限.05625。仅新/反手要求最近M笔实际已实现有符号资金费中位数，年龄1–36h含端点且available≤signal。偶数笔取中间两率均值、奇数笔取中值；允许支出min(.0002,.0075×过去8个已完成日无偏样本logvol×最近合格已知实际结算间隔小时/24)。预算相等通过，缺失阻新仓，已有q及正常退出不改。预算VW8、入场风险V6、执行冲击V20分开；仅M2/M3新参数，不靠文案修正制造新颖性，旧spec/report/状态原字节保持。

BTC两银行只读：本金3750/名义1000，L29主ROC严格>.03或.0325多、低于其负值空；入场优先，带内多仅ROC>−.005、空仅ROC<.005持有，相等退出。新/反手再要求V10 samplelogvol≤.0275及5日同向ROC严格>.0025，同向旧q保留。新父直接复用这些原规模净值，无新BTC策略计算。

父本金18750/raw[1,1]相加BTC3750和ETH15000原银行美元NAV，20/80只是初始本金占比，权重不归一化。无缩放、转账、再平衡、父订单或跨保证金；完整事件轴对齐后重算组合净值与整体DD，不平均单策略收益、Sharpe或DD。

Walk-forward已执行：2025-10-19T00:01Z→2026-11-14T00:01Z，共391日、33日背景；每币610562分钟bar、10176小时mark、1273实际资金费，8个Parquet SHA/单位/闭合可得时间核验。13完整30日折+1日尾，跨折继承现金/q，全期终止才按成本平仓，整体DD来自全事件NAV。近40日8×5与扩展21日5+5+5+6逐折保留，1日尾Sharpe=None。固定规则不拟合/无标签，只用完成前缀；OOS字段指复用开发历史，不是未触碰最终集或独立未来。

敏感性已执行：M2/3/4×BTC H3%/3.25%六父格，ETH组件仅沿M，BTC仅沿H。保存全部净收益、整体DD、Sharpe、Calmar、近期折、10邻边、启发跳变标记与并列最优边界。局部3倍净正和严格近期合格比例各≥60%；小3×2条件邻域不证明宽平台或全局最优；旧参考状态不被当前邻域改写。

成本已执行：每边费5bp+半价差1bp+滑点2bp+0.5×过去20完整日samplelogvol×sqrt(abs(q)×真实OPEN/过去20日quoteADV)，不利tick、实际LOT/minnotional，参与率≤.1%、费后1倍抵押、闭合小时high/low的1%维持保证金代理。执行成本和负资金费1/2/3倍，收入不放大。线性永续无现货借币需求；费/盘口为估计，缺历史L2/TCA、完整保证金档位、tick强平和容量证明。

冻结门槛：全期/近期三成本净正，1倍≥10/13正完整月，近期各成本≥6/8正5日折，扩展21日各成本净正且≥3/4正折；3倍DD≤25%，两项局部比例各≥60%，至少4底层平仓，1倍(毛价PnL+净资金费)/执行成本≥2.5；无拒单/负抵押/保证金代理违规、期末平仓且≥180日。任一失败即淘汰，结果保持。

|ETH资金费中位数M（笔）|BTC主H|来源/状态|1x净%|2x净%|3x净%|3x整体DD%|正月/13|近期正折1/2/3|
|---:|---:|---|---:|---:|---:|---:|---:|---|
|2|0.03|新/passed|8.849490734|8.359313754|7.869317996|1.357833669|12|6/6/6|
|2|0.0325|新/passed|8.741891094|8.252410442|7.763110980|1.357833669|12|6/6/6|
|3|0.03|新/passed|7.844248169|7.436034629|7.028001709|1.357833669|11|6/6/6|
|3|0.0325|新/passed|7.736648528|7.329131317|6.921794692|1.357833669|11|6/6/6|
|4|0.03|旧只读/passed|9.119819920|8.633459365|8.147280124|1.357833669|12|6/6/6|
|4|0.0325|旧只读/passed|9.012220280|8.526556052|8.041073107|1.357833669|12|6/6/6|


事前代表M2/BTCH.03（992382b415832a9c06d95c570f1101c09d5b045073913f91a2d59075f2e48b1b）三成本净8.849490734%/8.359313754%/7.869317996%，3倍整体DD 1.357833669%，Sharpe 2.265095712，Calmar 5.396342263，passed；失败项[]。

ETH M=2组件rejected，三成本净6.504312532%/6.198753040%/5.893403396%，3倍DD 1.528984097%，正月6/13，近期正折{'1': 0, '2': 0, '3': 0}，失败项['ten_of_thirteen_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct', 'extension21_positive_all_costs', 'extension21_three_of_four_positive_folds_all_costs']。

ETH M=3组件rejected，三成本净5.247759325%/5.044654134%/4.841758036%，3倍DD 1.528984097%，正月4/13，近期正折{'1': 0, '2': 0, '3': 0}，失败项['ten_of_thirteen_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct', 'extension21_positive_all_costs', 'extension21_three_of_four_positive_folds_all_costs']。

配对旧M4R.0075、相同BTCH0.03：新M2的3倍净变化-0.277962127个百分点，整体DD变化+0.000000000个百分点，Sharpe -0.100060119，Calmar -0.190121135。

配对旧M4R.0075、相同BTCH0.0325：新M2的3倍净变化-0.277962127个百分点，整体DD变化+0.000000000个百分点，Sharpe -0.099853908，Calmar -0.190133573。

配对旧M4R.0075、相同BTCH0.03：新M3的3倍净变化-1.119278415个百分点，整体DD变化+0.000000000个百分点，Sharpe -0.169343939，Calmar -0.765765374。

配对旧M4R.0075、相同BTCH0.0325：新M3的3倍净变化-1.119278415个百分点，整体DD变化+0.000000000个百分点，Sharpe -0.171389441，Calmar -0.765815668。

本轮新父相对同BTC旧M4的净收益、整体DD、Sharpe、Calmar四项严格联合改善0组；保存全部配对变化和取舍，不单择一个指标宣布改进。历史通过父4个、组件0个，所有淘汰原因按上表/逐组件清单保留。组合通过不覆盖组件失败，原账户不采用本轮新参数；全部仍待独立未来验证。

6新配置全成本NAV签名6组，匹配8网格/持有参考0组，匹配上轮新/只读路径0/6。启发abs(deltaSharpe)>2×sampleSTD(absdeltas)标记1/10，绝对变化范围[0.029497055865038924, 0.29703637472415356]、STD 0.089517517；不是显著性或过拟合概率。父格净正/正Sharpe/严格近期比例1.0/1.0/1.0。相同终值与相同完整路径分别核验，391日目标/持仓/成交/资金费对照见bank_path_alias_verification.json。

再只读更早同参数组的10个ETH M/R银行及12个同BTC父，匹配本轮1/6（组件1，父0）；完整NAV/391日原生目标、持仓、成交、资金费一致性见older_median_path_alias_verification.json。此有限集合不是全库独立样本检验。

只读分解ETH M2对旧M4：毛价格PnL变化-49.987890000USDT，资金费变化-2.252635585，执行费变化-0.122626730，净差-52.117898855，执行数差0；同BTC父净差-0.277962127个百分点。

只读分解ETH M3对旧M4：毛价格PnL变化-253.714650000USDT，资金费变化+4.215680689，执行费变化-39.634266490，净差-209.864702821，执行数差-4；同BTC父净差-1.119278415个百分点。

另只读旧BTC总波动上限组件9个/对应父18个，匹配新路径0/6；范围与8网格参考和上轮对照分开。两个新ETH完整391日实际计算一次，不线性缩放旧NAV，也不重跑已完成配置。

独立核对新原生6/父12、旧原生15/父9成本曲线，新决策2346、旧决策5865；42场景、588逐折、336近期折、168扩展折、16464日NAV、18持有对照、10邻边/六图留档。匹配持有3倍净-14.782911083%、整体DD 18.454766592%，现金0。引擎与货币核心源字节均与上轮一致，仅预声明M参数变化。294个奇偶中位数/成熟性/缺失/等号/未来后缀合成检查及资产轴检查先于reserve；所有实际配置先登记再计算并finish。

原账户SMA/single16:30→18:30、L4/FEWM18:10→20:10；新日事件{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、资金费{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}。完整新资金费查询为空，旧实际1794844800004ms即16:00:00.004及00/08/原日决策全链各一次；三个永续各自现金、q、entry和日背景保持，不能复制现金流或重复记16。

SMA完整68日SPOT权威research/experiments/20261116T080637Z/forward_inputs.json.gz及67/66/65前缀相等，仍65日/对称1%/Float、本金1500:500/raw75:25；费10bp+半价差1bp+滑点2bp+过去20日ADV冲击，不追溯新LOT/tick。追加120闭合分钟，无新日决策/参考/成交；累计65909分钟/65956点，三倍净-7.468957812%，负结果完整保留。原2027-03-31终止计划不改、不强平，延迟shadow不冒充十策略真实报价成交。

本轮SMA/single16:30→18:30、L4/FEWM18:10→20:10；完整新查实际资金费为空，均无新资金费、日决策或成交。旧16:00:00.004、00/08及原日决策全链各一次。下轮SMA/single18:30→20:30（20:31闭合）、L4/FEWM20:10→22:10（22:11闭合），仍完整新查，不重记16、不预设名义8小时时刻。原SMA65/对称1%/Float/full68SPOT与67/66/65前缀、下一日决策Nov17_00:01保持，不采用新研究。

实际16源首次捕获UTC 2026-11-16T22:20:02.088970Z 原字节保持，本轮完整新查询16:30→20:10的UTC 2026-11-17T02:19:47.672820Z、BTC/ETH均空。全部旧Nov13–16源/捕获UTC/哈希保持，不把旧首捕获重标为本轮时间，不编造新的名义资金费时刻。

有包公共GET 18次、实际传输失败0次；URL/捕获时界/body/gzipSHA保留，FEWM/cached metadata/time精确去重。SMA内部未分包重试0按实际stderr披露，不编未知UTC/失败体。

复现cwd=/home/desktop/Documents/Codex/EquiTide，既有venv python -B。launch bootstrap/preflight/screen_tight_medians/configure_median/configure_accounts/setup_confirmation/prepare_confirmation/prepare_diagnostics/configure_report；实际freeze后units首次失败，保留原源码后launch units_neighborhood_repair、execute units_retry1通过，再bind reserve_0 evaluate audit exports finish_0 research_check；diagnostics/historical_aliases/totalrisk_history_aliases/budget_effect/older_median_aliases，实际view_image后visual_review，再diagnostic_review；midnight_archive l4h02 fewm candidate forward accounts_check；account_continuity/complete_transport_audit/validate_sources；journal sources_check gates feed collect final_checks/staged_whitespace；封存/发布助手。精确UTC/命令/退出码/stdout见回执；已完成目录不重复reserve/evaluate或重放账户，forward --reproduce只核验原包。

391日复用开发历史与多重选择偏差未消除，无DSR/PBO显著性结论，历史正收益不代表稳定实盘盈利。本轮读取[Binance官方市场/资金费文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)与[官方公共数据README](https://github.com/binance/binance-public-data/blob/master/README.md)；真实原包与输入SHA是复现依据。

预登记前的合成邻域检查曾错误地把旧M4参考当中间行，真实中间行是M3；只修正两项检查断言后独立重试通过。原失败源码、日志、退出码和修复前guard均保留，计划、参数、规则、引擎和资金核心SHA未变；此工程检查失败发生在任何reserve/市场/账户计算前，实际金融配置和原账户窗口未重复运行。

实际失败/阻碍：{"round": "20261117T021615Z", "facts": [{"command": ["/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python", "-B", "/home/desktop/Documents/Codex/EquiTide/research/experiments/20261117T021615Z/parent_units.py"], "cwd": "/home/desktop/Documents/Codex/EquiTide", "started_utc": "2026-11-17T02:35:33.730879Z", "finished_utc": "2026-11-17T02:35:34.033360Z", "exit_code": 1, "log": "research/experiments/20261117T021615Z/parent_units.log", "stderr": "Traceback (most recent call last):\n  File \"/home/desktop/Documents/Codex/EquiTide/research/experiments/20261117T021615Z/parent_units.py\", line 23, in <module>\n    ns,dims=neighbors(g,p,full);assert dims==2 and len(ns)==(6 if g['W']==4 else 4)\n                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nAssertionError\n", "resolved": true, "resolution_utc": "2026-11-17T02:41:14.861629+00:00", "resolution": "Only copied synthetic middle-row neighbor-count expectations changed M4 to M3 before first reservation; strategy neighbors/plan/specs/engine/money unchanged. Successful primitive retry retained separately; no market or account calculation occurred.", "successful_retry_receipt": "research/experiments/20261117T021615Z/units_retry1_commands.json", "successful_retry_native_completion_chunk": "2f3625", "failed_source": "research/experiments/20261117T021615Z/review/failures/parent_units_before_middle_row_fix.py", "failed_source_sha256": "c80b0b74981f64b88ce1802e55638927fccbfbf3d7f77bdd2eacbde24b609b8e", "corrected_source": "research/experiments/20261117T021615Z/parent_units.py", "corrected_source_sha256": "60ffbe9bfc59b0d0ab2ac18d21f039a41406f978e28e195e8de6abd14c9613c2"}], "no_completed_model_or_account_window_replays": true}。保留全部正负、淘汰/失败、原账本/冻结规则/登记/哈希/原包及下轮必要状态，仅清理可重建缓存。锁内monitor只读汇总，不新增回测、模拟成交、部署或定时任务。真实commit/push/远端树及解锁后回执见.git/automation_proofs。
