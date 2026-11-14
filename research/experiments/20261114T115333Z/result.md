本轮完成6个新金融定义（2 ETH组件、4 BTC/ETH父组合），18个1/2/3倍成本场景；4通过、2淘汰。另8个已有真实配置/24场景只读复用。12个原账户观察仍为未成熟partial rejected，不取消冻结长期计划。全部实际结果、负折、淘汰和失败证据保存。

事前假设：ETH资金费预算用8/10/12个完成日的无偏samplelogvol估计，预算系数R固定0.01，是否能改变入场筛选且避免孤立峰？与已完成BTC入场H=[3%,3.5%]交叉为2×3面。只实算ETH VW10/VW12，BTC两银行、ETH VW8、两个VW8旧组合和匹配持有均只读；代表BTC H3%/ETH VW12在任何新结果前固定，未事后换代表或扩网格。

BTC C3750/N1000，L29、退出E1%、入场V14cap3%，严格ROC>H做多、<-H做空，原保留条件不变。ETH C15000/N4000，原L5/H2%/E0.75%反转、有限归一化EWMS16 beta15/17、D3严格K0.75%、入场V6cap5.625%，最近4笔1–36小时已成熟实际资金费有符号中位数，预算min(.0002,0.01×samplelogvol(VW)×最新合格实际结算间隔小时/24)，最后long-only。新仓/反手才用资金费和趋势/波动门槛，同向q不变。N/前日close按LOT向下取整，下一00:01真实OPEN执行。预算VW不是入场V6，也不是成本20日估计窗口。

沿用的ETH parameters.persistence历史文字仍写E.005；本轮logic明确该旧描述不执行，以机器参数exit_buffer_fraction=.0075、冻结引擎及独立逐日审计为准。旧spec/报告原字节不改。原warmup30/embargo3字段保留，实际数据33日背景、无拟合/标签，逐折继承cash/q，不靠该旧字段声称标签泄漏已被统计解决。

父组合C18750，以原始[1,1]相加对齐后的两完整独立银行美元NAV；20/80仅为两银行初始本金占比。权重不归一化，不二次加权、线性缩放银行为新N、转账、再平衡、父订单或跨保证金。新ETH真实数量/手续费/冲击/资金费/风险逐成本实算一次，BTC原规模完整净值只读复用。

完整读取35414登记事件/17574ID、418份结论，三技能/task/README、OOS脚本及原ZIP。排除观察后规范研究定义11227，不是独立市场试验数。初始16项均有实际归档证据，旧legacy/false和负记录保留，无缺实际配置可优先补测；保护74818份旧文件，基于最新main及11 UTC paper10记录，无遗留reserved或未推送结果。

研究数据仍为反复开发的同391日：2025-10-19T00:01Z→2026-11-14T00:01Z，33日背景，每币610562分钟、10176小时mark、1273实际资金费；8份Parquet及原始来源SHA逐一核对。本轮无新研究行情GET/完整研究日，原账户08时资金费绝不加入截止00:01的研究数据。资金费信号保守延迟1小时是可得性假设，非实测网络延迟。

Walk-forward完成：13个完整30日折+1日尾折，逐折cash/q连续，仅全期末带成本退出。固定规则，无拟合或前瞻标签，滚动特征只用当时已完成信息。1倍至少10/13正完整月，尾折不进月门槛；近期40日8×5折、扩展21日5+5+5+6折均继承原持仓。整体DD来自全部事件NAV，不平均逐折DD；单日尾折Sharpe=None，不用单日年化挑选参数。

Sensitivity完成：BTC H两档×ETH预算VW三档，报告全部六组合和适用原生邻域收益/整体DD/Sharpe/Calmar。BTC只沿H、ETH只沿预算VW；旧状态/门槛不改，当前邻域另作只读诊断。六父格各成本净正且近期6/8正折；两ETH单组件近期0/8，不能用组合资格掩盖组件不达标。

Costs完成：每边5bp手续费+1bp半价差+2bp滑点+0.5×过去20日samplelogvol×sqrt(abs(q)×真实OPEN/过去20日quoteADV)冲击，不利tick取整。执行成本与资金费支出按1/2/3倍，收入不放大。核对原生LOT/tick/minnotional、参与率≤0.1%、费后1倍抵押及闭合小时不利high/low的1%保证金代理。线性永续无需现货借币；无历史L2/TCA、完整风险档位、tick强平或真实容量证明。估计成本不保证成交。

其余原门槛：各成本全期/近期净正、近期各6/8正5日折、3倍整体DD≤25%，局部净正/严格近期邻居比例≥60%，至少4次底层平仓、1倍(毛价格PnL+净资金费)/执行成本≥2.5，无拒单、负抵押、保证金代理违规，期末平仓且至少180日。

|BTC H|ETH预算VW|来源/状态|1x净%|2x净%|3x净%|3x整体DD%|正月/13|近期正折1/2/3|
|---:|---:|---|---:|---:|---:|---:|---:|---|
|3.0%|8|旧只读/passed|9.180507|8.603503|8.026687|1.483420|12|6/6/6|
|3.0%|10|新/passed|9.180507|8.603503|8.026687|1.483420|12|6/6/6|
|3.0%|12|新/passed|8.910177|8.329358|7.748725|1.483420|12|6/6/6|
|3.5%|8|旧只读/passed|8.856644|8.281718|7.706964|1.371605|12|6/6/6|
|3.5%|10|新/passed|8.856644|8.281718|7.706964|1.371605|12|6/6/6|
|3.5%|12|新/passed|8.586315|8.007572|7.429002|1.371605|12|6/6/6|


事前代表BTC H3%/ETH VW12 0433acc6c301ed28e391e29a1bb7588e87d4980e22e11bcf690c26ffe7641750：1/2/3倍净8.910177457%/8.329357778%/7.748724736%，3倍整体DD1.483420364%、Sharpe2.067378652、Calmar4.863976912；12/13正月、各成本近期6/8，组合通过。

ETH VW10：rejected，三成本净7.053707782%/6.677683975%/6.301870230%，3倍整体DD1.528984097%，仅7/13正完整月、近期各0/8，扩展21日净0；执行各14次。失败项['ten_of_thirteen_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct', 'extension21_positive_all_costs', 'extension21_three_of_four_positive_folds_all_costs']。

ETH VW12：rejected，三成本净6.715796300%/6.335001962%/5.954417571%，3倍整体DD1.528984097%，仅7/13正完整月、近期各0/8，扩展21日净0；执行各14次。失败项['ten_of_thirteen_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct', 'extension21_positive_all_costs', 'extension21_three_of_four_positive_folds_all_costs']。

VW10与旧VW8在391次desired和完整cash/q状态、全部成交、资金费和三成本整条NAV完全相同，预算数值变化没有跨越实际入场边界；三个成本场景的原始差异计数/完整路径核验见bank_path_alias_verification。VW12改变了筛选，ETH3倍收益下降，未减少执行次数。四个新父组合虽通过历史门槛，其中两个VW10是旧组合的完整路径别名；两个VW12低于各自VW8中心，整体DD未改善。不增加独立alpha证据，也不更换冻结前向规则。

6新定义有6条不同三成本签名，其中3条已见于只读旧结果、父组合旧路径别名2组。当前2个新父组合净收益与匹配VW8相等、2个更低。ETH扩展21日PnL全部0：True；近期组合收益由BTC贡献，不能归因ETH的新持续收益。不同参数ID/不同路径均不是独立市场样本。

匹配持有3倍净-14.782911083%、整体DD18.454766592%，现金0%。旧ETH原rejected、持有负收益和全部旧失败折保留。相邻Sharpe启发式abs(delta)>2×sampleSTD(absdeltas)保留2/10条标记，绝对变化范围0.000000–0.136730；全部标记见conditional_parameter_robustness，不当统计显著性或灾难性悬崖证明。网格小、存在别名，不外推广泛稳健平台。

独立审计6条新ETH原生/12条新父曲线、15条旧原生/9条旧父曲线，2346条新因果决策、5865条旧只读决策。导出42成本场景、588逐折、336近期折、168扩展折、16464日NAV、18匹配持有对照、10邻接边及2×3面。每个实际金融变体均独立spec、先reserve后计算、各自finish。

原账户：SMA/single Nov14_06:30→08:30Z，L4/FEWM08:10→10:10Z。日事件{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、资金费记录{'SMA': 0, 'candidate': 6, 'l4h02': 0, 'fewm': 0}。single本窗按实际08:00:00.001及自己的q/cash入账6条资产×成本记录；L4/FEWM已在上轮计入、本轮0条不重复。三永续完整链08均各一次、每个asset/cost/timestamp唯一；ETH空仓零金额也保留。正资金费给空头的收入不按2/3倍成本放大。

single BTC08三成本各自资金费：{"1": "0.03594201930936785520000000000", "2": "0.03594201930936785520000000000", "3": "0.03594201930936785520000000000"} USDT，来自自己的-0.012持仓；L4/FEWM现金流未复制。

SMA累计62429分钟/62474点、43完整日；完整66日背景权威research/experiments/20261114T035058Z/forward_inputs.json.gz，原均线65日及Float/75:25规则不变，本轮仅分钟包。18本永续账簿及完整NAV前缀核对，无现金重开、窗口强平或研究规则采用。延迟shadow不是实时成交，原账户均未成熟180日。

下轮SMA/single Nov14_08:30→10:30Z，10:31后参考闭合；L4/FEWM10:10→12:10Z，12:11后参考闭合，不能提前运行。三永续账户08:00:00.001已各计一次，single本轮完成自己的资金费入账，L4/FEWM没有重复；下轮游标均越过08仍须查询完整实际结算窗口，不能假定8小时。保留原09:56:41.855564Z的funding08公共捕获及本轮独立新捕获，不能重标旧UTC或复制现金流。下次原日决策Nov15_00:01；SMA完整66日权威035058/forward_inputs，本轮115333包仅分钟数组，原均线65日/对称1%/Float数量/1500:500本金/raw75:25不变。仅mark可复用本轮forward.py并改PREV/窗口，日交叉需原dailyadapter增补闭合日。不重置、强平或采用研究参数；旧shadow与十策略实时公开报价模拟分开。

本轮保存公共行情GET 19次、实际传输失败1次。FEWM只复用同窗公开原包，single只复用metadata/time，现金/数量/资金费/决策始终独立。原08字段捕获UTC 2026-11-14T09:56:41.855564Z 保持；本轮完整窗口新预检UTC 2026-11-14T12:03:05.232992Z，公共字段一致验证单独留档，未把旧响应重标为新捕获。失败/原raw/body及压缩SHA/UTC如有均保留。

391日反复开发且参数参考过往结果，多重选择偏差未消除；不是未触碰最终测试集或独立未来，未做支持显著性结论的DSR/PBO，不称稳定实盘盈利。旧SMA shadow与paper10十策略实时公开报价模拟分开，不修改paper规则、本金、持仓或账本。

[Binance官方USD-M市场数据与资金费说明](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)，2026-11-14核对。实际结算间隔来自已完成fundingTime差值，不硬编码名义8小时；全部来源版本、SHA和原始响应见plan/context/data_manifest及窗口预检。

复现目录/home/desktop/Documents/Codex/EquiTide，解释器/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B。bootstrap、review/prepare/preflight/setup后，review/execute.py依次freeze units bind reserve_0 evaluate audit exports finish_0 research_check；账户midnight_archive l4h02 fewm candidate forward accounts_check；diagnostics、view_image/visual_review、complete_transport_audit，随后journal sources_check gates feed collect final_checks，再seal/publish。实际命令/cwd/UTC/stdout/退出码见*_commands.json和review/native_*_receipt.json。已完成精确配置会被登记拦截；审计不产生新金融试验或账户转移。

真实工程失败清单{"facts": [{"stage": "pre-execution report formatter AST validation", "native_chunk": "8f80d5", "resolved": true, "proof": "research/experiments/20261114T115333Z/formatter_syntax_verification.json", "no_financial_or_account_recalculation": true}, {"stage": "first formatter repair and instrumented source validation", "native_chunk": "5cb3a5", "exit_code": 1, "actual_failed_receipt": "research/experiments/20261114T115333Z/review/native_validate_sources.py_receipt.json", "resolved": true, "proof": "research/experiments/20261114T115333Z/formatter_syntax_verification.json", "no_financial_or_account_recalculation": true}]}。18个新ID/36事件含6金融和12原观察；8旧金融只读。仅保留真实正/负/失败结果、完整账本/冻结规则/登记、必要源码和原响应及下轮状态，清理可重建缓存，大行情留忽略data。只读snapshot与检查和本轮轻量证据一起推送main，不新建网页或任务。最终commit/push、完整远端树/blob和账户链核验以.git/automation_proofs原生回执为准。
