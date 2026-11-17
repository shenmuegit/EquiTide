本轮完成6个新金融配置：固定L5/M4/R=.0075/VW8，ETH fastROC严格对称入场H=.0175/.0225两个原生组件，交叉已有BTC H3%/3.25%银行形成四父；ETH H.02旧银行只读。18条新1/2/3倍成本场景，8旧网格/持有配置24场景只读。历史通过4（父4、组件0），淘汰2，全部结果保留。12原账户观察独立reserve/finish，partial rejected不取消长期计划。

事前假设：固定5日fastROC后，对称入场阈值1.75%/2.25%改变正慢趋势内回撤深度和触发频率；M4/R.0075/VW8及其他风险/核算规则固定。ETH H=[.0175,.02,.0225]×只读BTCH=[.03,.0325]，代表ETHH.0175/BTCH.03在结果前固定，不事后扩批、换代表或改失败门槛。W为ETH主入场阈值，K为BTC主入场阈值，单币只沿自身适用轴。

完整读取37200登记事件/18461ID、450份结论、11419个排除观察的规范研究定义（非独立试验数），task/README/三技能、checks/*oos.py与freqtrade原ZIP。初始16项缺实际结果0，legacy/false和全部负结果保持；保护85690旧文件及paper10账本/报价。完整语义查重确认固定L5/M4/R.0075/VW8的ETH H.0175/.0225不存在已测/运行中精确配置；H.02旧结果只读，六项逐项reserve成功后才计算。完整表见entry_hurdle_semantic_screen.json。

ETH本金15000/固定名义4000，long-only L5、严格H.0175/.02/.0225、E.0075：快ROC>H先给-1、低于-H先给+1，带内仅actual+1且r<E或actual-1且r>-E保留，否则0。有限归一化EWMS16 beta15/17、D3严格K.0075筛方向；V6已完成样本logvol上限.05625仅筛新/反手。最近M4笔实际有符号资金费中位数，年龄1–36h含端点、available≤signal；偶数取中间两率均值，允许支出min(.0002,.0075×过去8个已完成日无偏样本logvol×最近合格已知实际结算间隔小时/24)。预算相等通过，缺失阻新仓，已有q及正常退出不改，最终max(desired,0)。预算VW8/风险V6/冲击V20分开；仅H.0175/.0225新参数，long_entry_return_hurdle、short_entry_return_hurdle与return_hurdle标量一致，旧spec/report/状态原字节保持。

BTC两银行只读：本金3750/名义1000，L29主ROC严格>.03或.0325多、低于其负值空；入场优先，带内多仅ROC>−.005、空仅ROC<.005持有，相等退出。新/反手再要求V10 samplelogvol≤.0275及5日同向ROC严格>.0025，同向旧q保留。新父直接复用这些原规模净值，无新BTC策略计算。

父本金18750/raw[1,1]相加BTC3750和ETH15000原银行美元NAV，20/80只是初始本金占比，权重不归一化。无缩放、转账、再平衡、父订单或跨保证金；完整事件轴对齐后重算组合净值与整体DD，不平均单策略收益、Sharpe或DD。

Walk-forward已执行：2025-10-19T00:01Z→2026-11-14T00:01Z，共391日、33日背景；每币610562分钟bar、10176小时mark、1273实际资金费，8个Parquet SHA/单位/闭合可得时间核验。13完整30日折+1日尾，跨折继承现金/q，全期终止才按成本平仓，整体DD来自全事件NAV。近40日8×5与扩展21日5+5+5+6逐折保留，1日尾Sharpe=None。固定规则不拟合/无标签，只用完成前缀；OOS字段指复用开发历史，不是未触碰最终集或独立未来。

敏感性已执行：ETH H.0175/.02/.0225×BTC H3%/3.25%六父格，ETH组件仅沿H，BTC仅沿H。保存全部净收益、整体DD、Sharpe、Calmar、近期折、10邻边、启发跳变标记与并列最优边界。局部3倍净正和严格近期合格比例各≥60%；小3×2条件邻域不证明宽平台或全局最优；旧参考状态不被当前邻域改写。

成本已执行：每边费5bp+半价差1bp+滑点2bp+0.5×过去20完整日samplelogvol×sqrt(abs(q)×真实OPEN/过去20日quoteADV)，不利tick、实际LOT/minnotional，参与率≤.1%、费后1倍抵押、闭合小时high/low的1%维持保证金代理。执行成本和负资金费1/2/3倍，收入不放大。线性永续无现货借币需求；费/盘口为估计，缺历史L2/TCA、完整保证金档位、tick强平和容量证明。

冻结门槛：全期/近期三成本净正，1倍≥10/13正完整月，近期各成本≥6/8正5日折，扩展21日各成本净正且≥3/4正折；3倍DD≤25%，两项局部比例各≥60%，至少4底层平仓，1倍(毛价PnL+净资金费)/执行成本≥2.5；无拒单/负抵押/保证金代理违规、期末平仓且≥180日。任一失败即淘汰，结果保持。

|ETH fastROC主入场H（比例）|BTC主H|来源/状态|1x净%|2x净%|3x净%|3x整体DD%|正月/13|近期正折1/2/3|
|---:|---:|---|---:|---:|---:|---:|---:|---|
|0.0175|0.03|新/passed|9.119819920|8.633459365|8.147280124|1.357833669|12|6/6/6|
|0.0175|0.0325|新/passed|9.012220280|8.526556052|8.041073107|1.357833669|12|6/6/6|
|0.02|0.03|旧只读/passed|9.119819920|8.633459365|8.147280124|1.357833669|12|6/6/6|
|0.02|0.0325|旧只读/passed|9.012220280|8.526556052|8.041073107|1.357833669|12|6/6/6|
|0.0225|0.03|新/passed|4.078659188|3.791525882|3.504406110|1.396371369|10|6/6/6|
|0.0225|0.0325|新/passed|3.971059547|3.684622570|3.398199093|1.396371369|10|6/6/6|


事前代表ETHH.0175/BTCH.03（203191e6b0714e57507a25bafe8701c915d0011ef379c533f2adacc200b1259c）三成本净9.119819920%/8.633459365%/8.147280124%，3倍整体DD 1.357833669%，Sharpe 2.365155831，Calmar 5.586463398，passed；失败项[]。

ETH H=0.0175组件rejected，三成本净6.842224015%/6.541435053%/6.240856055%，3倍DD 1.528984097%，正月6/13，近期正折{'1': 0, '2': 0, '3': 0}，失败项['ten_of_thirteen_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct', 'extension21_positive_all_costs', 'extension21_three_of_four_positive_folds_all_costs']。

ETH H=0.0225组件rejected，三成本净0.540773099%/0.489018200%/0.437263537%，3倍DD 1.583579893%，正月1/13，近期正折{'1': 0, '2': 0, '3': 0}，失败项['ten_of_thirteen_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct', 'four_underlying_native_closes1', 'extension21_positive_all_costs', 'extension21_three_of_four_positive_folds_all_costs']。

配对旧ETHH.02/L5/M4R.0075、相同BTCH0.03：新H0.0175的3倍净变化+0.000000000个百分点，整体DD变化+0.000000000个百分点，Sharpe +0.000000000，Calmar +0.000000000。

配对旧ETHH.02/L5/M4R.0075、相同BTCH0.0325：新H0.0175的3倍净变化+0.000000000个百分点，整体DD变化+0.000000000个百分点，Sharpe +0.000000000，Calmar +0.000000000。

配对旧ETHH.02/L5/M4R.0075、相同BTCH0.03：新H0.0225的3倍净变化-4.642874014个百分点，整体DD变化+0.038537700个百分点，Sharpe -0.811546648，Calmar -3.246389958。

配对旧ETHH.02/L5/M4R.0075、相同BTCH0.0325：新H0.0225的3倍净变化-4.642874014个百分点，整体DD变化+0.038537700个百分点，Sharpe -0.827348233，Calmar -3.244591716。

本轮新父相对同BTC旧ETHH.02/L5/M4的净收益、整体DD、Sharpe、Calmar四项严格联合改善0组；保存全部配对变化和取舍，不单择一个指标宣布改进。历史通过父4个、组件0个，所有淘汰原因按上表/逐组件清单保留。组合通过不覆盖组件失败，原账户不采用本轮新参数；全部仍待独立未来验证。

1.75%阈值相对旧2%在每个成本场景有2日的入场风险过滤前目标不同，但最终391日目标、持仓、成交、资金费和完整NAV均相同；它是不同参数的实际测试结果，不是新增独立alpha。2.25%阈值相对旧2%有7日最终目标不同，ETH仅2次执行/1次平仓，交易数不足亦为淘汰原因。

6新配置全成本NAV签名6组，匹配8网格/持有参考3组，匹配上轮新/只读路径3/6。启发abs(deltaSharpe)>2×sampleSTD(absdeltas)标记1/10，绝对变化范围[0.0, 1.4273666866833947]、STD 0.510990374；不是显著性或过拟合概率。父格净正/正Sharpe/严格近期比例1.0/1.0/1.0。相同终值与相同完整路径分别核验，391日目标/持仓/成交/资金费对照见bank_path_alias_verification.json。

再只读更早同参数组的6个ETH H/R银行（其余参数固定）及12个同BTC父，匹配本轮3/6（组件1，父2）；完整NAV/391日原生目标、持仓、成交、资金费一致性见older_hurdle_path_alias_verification.json。此有限集合不是全库独立样本检验。

只读分解ETH H0.0175对旧H.02/L5/M4：毛价格PnL变化+0.000000000USDT，资金费变化+0.000000000，执行费变化+0.000000000，净差+0.000000000，执行数差0；同BTC父净差+0.000000000个百分点。

只读分解ETH H0.0225对旧H.02/L5/M4：毛价格PnL变化-982.465360000USDT，资金费变化+12.259951137，执行费变化-99.666531220，净差-870.538877643，执行数差-10；同BTC父净差-4.642874014个百分点。

另只读旧BTC总波动上限组件9个/对应父18个，匹配新路径0/6；范围与8网格参考和上轮对照分开。两个新ETH完整391日实际计算一次，不线性缩放旧NAV，也不重跑已完成配置。

独立核对新原生6/父12、旧原生15/父9成本曲线，新决策2346、旧决策5865；42场景、588逐折、336近期折、168扩展折、16464日NAV、18持有对照、10邻边/六图留档。匹配持有3倍净-14.782911083%、整体DD 18.454766592%，现金0。引擎与货币核心源字节均与上轮一致，仅预声明ETH主H参数变化。336个快ROC严格边界/成熟性/缺失/预算等号/未来后缀合成检查及资产轴检查先于reserve；所有实际配置先登记再计算并finish。

原账户SMA/single20:30→22:30，L4/FEWM22:10→Nov17_00:10；新日事件{'SMA': 0, 'candidate': 0, 'l4h02': 1, 'fewm': 1}、资金费{'SMA': 0, 'candidate': 0, 'l4h02': 6, 'fewm': 6}、成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}。实际资金费为1794873600000ms：BTC率−.00000569/mark64856，ETH率−.00003280/mark1819.75066159；L4/FEWM按各自结算前q独立记费，再于00:01执行各自原冻结内核，不能复制现金流。single尚未到自己的午夜窗口；旧Nov16的实际16:00:00.004及00/08/日决策全链各一次保留。逐笔cashflow、决策、成交及完整日上下文审计见original_account_continuity.json。

SMA完整68日SPOT权威research/experiments/20261116T080637Z/forward_inputs.json.gz及67/66/65前缀相等，仍65日/对称1%/Float、本金1500:500/raw75:25；费10bp+半价差1bp+滑点2bp+过去20日ADV冲击，不追溯新LOT/tick。追加120闭合分钟，无新日决策/参考/成交；累计66149分钟/66196点，三倍净-7.468957812%，负结果完整保留。原2027-03-31终止计划不改、不强平，延迟shadow不冒充十策略真实报价成交。

本轮SMA/single20:30→22:30仅闭合分钟mark；L4/FEWM22:10→Nov17_00:10已按各自结算前q在真实1794873600000ms结算，然后按各自完整闭合日背景与原冻结内核执行00:01日决策，资金费/日事件/成交均逐条保存，不复制账户现金流、不采用新研究H。下轮SMA/single22:30→Nov17_00:30（00:31闭合）才跨原午夜，必须新查完整真实结算字段，single按自己的q记费；SMA补第69个完整SPOT日并核对68/67/66/65前缀，调用保留的原SMA65/1%/Float日适配器及原成本，当前mark-only适配器不能用于跨日。下轮L4/FEWMNov17_00:10→02:10（02:11闭合）不重复本轮已记的午夜资金费和日决策，仍完整新查实际结算，不预设名义8小时；其下一原日决策Nov18_00:01。所有本金、冻结规则、2027-03-31终止计划保留，不重启或强平账户。

Nov17午夜源首次捕获UTC 2026-11-17T06:24:46.678539Z、SHA 0580bfb3e40a5cd47ca809993996edccb69519db61e13c04f5b3caaf9cc0a778；本轮完整新查询20:30→00:10覆盖BTC/ETH各一条真实结算，原始字段和准确时间保留。全部旧Nov13–16源及原捕获UTC/哈希保持，不把旧首捕获重标为本轮时间，不编造名义资金费时刻。

有包公共GET 18次、实际传输失败0次；URL/捕获时界/body/gzipSHA保留，FEWM/cached metadata/time精确去重。SMA内部未分包重试0按实际stderr披露，不编未知UTC/失败体。

复现cwd=/home/desktop/Documents/Codex/EquiTide，既有venv python -B。launch bootstrap；preflight首次因未复制core依赖退出1，保留日志，补齐原字节后preflight_retry首次发出真实HTTP；screen_entry_hurdles/configure_hurdles/configure_accounts/setup_confirmation/prepare_confirmation/prepare_diagnostics/configure_report；freeze units bind reserve_0 evaluate audit exports finish_0 research_check；diagnostics/historical_aliases/totalrisk_history_aliases/budget_effect/older_hurdle_aliases；实际view_image后visual_review/diagnostic_review；midnight_archive l4h02 fewm candidate forward accounts_check；account_continuity/complete_transport_audit/validate_sources；prepare_final_handoff；journal sources_check gates feed collect；verify_midnight_handoff/final_checks/staged_whitespace；封存/发布助手。一次apply_patch格式拒绝未改源，随后单文件写入成功；两项非金融准备问题均留档。精确UTC/命令/退出码/stdout见回执；完成目录不重复reserve/evaluate或重放账户，forward --reproduce只核验原包。

391日复用开发历史与多重选择偏差未消除，无DSR/PBO显著性结论，历史正收益不代表稳定实盘盈利。本轮读取[Binance官方市场/资金费文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)与[官方公共数据README](https://github.com/binance/binance-public-data/blob/master/README.md)；真实原包与输入SHA是复现依据。

实际失败/阻碍：{"round": "20261117T061921Z", "facts": [{"command": ["/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python", "-B", "/home/desktop/Documents/Codex/EquiTide/research/experiments/20261117T061921Z/review/preflight.py"], "cwd": "/home/desktop/Documents/Codex/EquiTide", "started_utc": "2026-11-17T06:23:26.639486Z", "finished_utc": "2026-11-17T06:23:26.690505Z", "exit_code": 1, "log": "research/experiments/20261117T061921Z/review/native_preflight.py_receipt.log", "kind": "missing_copied_local_core_dependency_before_preflight_HTTP", "resolved": true, "native_completion_chunk": "926d6c", "market_model_account_or_registry_execution": false, "resolution": "Copied original core391_tail_safe.py byte-identically before first HTTP query; original failed source/log/exit1 retained.", "restored_core_sha256": "7491cc0a55e83c7431a6fc3d66899e660a8d9daec0629af4391fc31da6d4ce6c", "retry_helper": "review/preflight_retry.py"}, {"tool": "apply_patch", "kind": "patch_format_rejected_before_mutation", "recorded_utc": "2026-11-17T06:33:26.021944+00:00", "error": "apply_patch verification failed: invalid patch: multiple operations target configure_accounts.py", "exit_code": null, "resolved": true, "resolution": "Wrote the same one-file preparation source through a quoted heredoc; no target was mutated by rejected patch.", "market_model_account_or_registry_execution": false}], "no_completed_model_or_account_window_replays": true}。保留全部正负、淘汰/失败、原账本/冻结规则/登记/哈希/原包及下轮必要状态，仅清理可重建缓存。锁内monitor只读汇总，不新增回测、模拟成交、部署或定时任务。真实commit/push/远端树及解锁后回执见.git/automation_proofs。
