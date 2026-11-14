完成6个新金融配置：2个ETH组件、4个BTC/ETH父组合，18个1/2/3倍成本场景；历史门槛通过4个，淘汰2个。8个已有真实配置/24场景只读复用。12个原账户观察partial rejected只表示未成熟，不取消冻结长期计划。所有真实结果、负折及失败证据均保留。

事前假设：ETH最近2/3笔已成熟实际结算的有符号资金费中位数，相比4笔，能否更快响应且避免孤立峰？参数M=[2,3,4]，资金费预算波动窗口V8、系数R=0.01固定；与已完成BTC入场阈值H=[3%,3.5%]交叉为2×3面。只新增ETH M2/M3；BTC两银行、ETH M4、两个M4组合、匹配持有只读。代表H3%/M3在任何结果前固定，没有看完OOS再改代表或扩批。

BTC本金3750/固定入场名义1000USDT，L29、退出E1%、入场V14cap3%；严格ROC>H做多、<-H做空。ETH本金15000/名义4000，L5/H2%/E0.75%反转、有限归一化EWMS16 beta15/17、D3严格K0.75%、入场V6cap5.625%，最后long-only。资金费记录须距信号1–36小时、available<=信号；先按实际结算时间选最近M笔再取有符号中位数，偶数取中间两数平均。不足M笔只阻止新仓/反手，同向持仓不改q。预算min(.0002,.01×V8日samplelogvol×最新合格记录的实际过去结算间隔小时/24)。LOT数量由N/前日close向下取整，次日00:01真实OPEN成交。资金费1小时可得延迟是保守假设，不是实测网络延迟。

旧ETH parameters.persistence描述仍有E.005；机器参数exit_buffer_fraction=.0075与冻结可执行引擎/独立逐日审计为准，logic明确旧描述不执行。旧spec、状态、报告原字节保留。warmup30/embargo3历史字段不改，实际33日背景、无拟合/标签；逐折cash/q连续。

父组合本金18750，raw[1,1]表示两个完整原规模银行美元NAV直接相加；20/80仅为初始本金占比。权重不归一化，不二次加权、缩放旧NAV冒充新名义、转账、再平衡、父订单或跨保证金。新ETH数量/手续费/冲击/资金费/风险逐成本实算一次；BTC净值只读复用。

完整读取35470条登记事件/17602个ID、419份既往结论，三技能、task、README、OOS脚本及freqtrade原ZIP。排除观察后的规范研究定义11233个，不是独立市场样本数。初始16项均已有实际结果证据，保留legacy/false原记录，没有无真实结果项可优先补测。保护75127份旧文件；基于最新main和13UTC paper10记录，上轮补充发布核验回执完整读取，无遗留reserved或未推送结果。

数据仍是反复开发的391日：2025-10-19T00:01Z→2026-11-14T00:01Z，33日背景；每币610562分钟、10176小时mark、1273实际资金费。8份Parquet SHA/单位/闭合/连续/可得时间核对；本轮无新完整研究日、无新研究行情GET，账户本日08时资金费不加入截止00:01的研究。

Walk-forward已执行：13个完整30日折+1日尾折；特征只读已完成前缀，固定规则、无拟合/标签，折间继承cash/q，仅全期末带成本退出。1倍至少10/13正完整月，尾折不参与月门槛、单日Sharpe=None。近40日8×5折及扩展21日5+5+5+6折保留源持仓；连续OOS全部事件净值计算整体DD，不平均折DD或单策略Sharpe。

Sensitivity已执行：BTC H两档×ETH M三档，逐配置/场景报告净收益、整体DD、Sharpe、Calmar及邻接差异。BTC仅沿H邻域、ETH仅沿M邻域，组合沿两轴；旧资格状态不重新分类。预定正收益/严格近期邻居占比各至少60%。局部小网格只是条件诊断，不能证明广泛参数平台或消除历史选择偏差。

Costs已执行：每边5bp手续费+1bp半价差+2bp滑点+0.5×过去20日samplelogvol×sqrt(abs(q)×真实OPEN/过去20日quoteADV)冲击，不利tick。执行成本、负资金费按1/2/3倍，资金费收入不放大。原生LOT/tick/minnotional、参与率≤0.1%、费后1倍抵押及闭合小时不利high/low的1%维持保证金代理均核对。线性永续无需现货借币；缺历史L2/TCA、完整风险档位和tick强平数据，容量/价差/冲击是估计。

预先失败门槛：所有成本全期及近期净正，近期各成本至少6/8正5日折；扩展21日净正且至少3/4正折，3倍整体DD≤25%，至少4次底层平仓，1倍(毛价格PnL+净资金费)/执行成本≥2.5，无拒单、负抵押、保证金代理违规；期末平仓、至少180日。任何一项失败即rejected，仍保留完整真实结果。

|BTC H|ETH M|来源/状态|1x净%|2x净%|3x净%|3x整体DD%|正月/13|近期正折1/2/3|
|---:|---:|---|---:|---:|---:|---:|---:|---|
|3.0%|2|新/passed|8.910177|8.329358|7.748725|1.483420|12|6/6/6|
|3.0%|3|新/passed|8.910177|8.329358|7.748725|1.483420|12|6/6/6|
|3.0%|4|旧只读/passed|9.180507|8.603503|8.026687|1.483420|12|6/6/6|
|3.5%|2|新/passed|8.586315|8.007572|7.429002|1.371605|12|6/6/6|
|3.5%|3|新/passed|8.586315|8.007572|7.429002|1.371605|12|6/6/6|
|3.5%|4|旧只读/passed|8.856644|8.281718|7.706964|1.371605|12|6/6/6|


事前代表H3%/M3，指纹4e5bdbc9906fd034b9d607a214e21c4f06437fa636984f9c02ca87e54eb47d82：1/2/3倍净收益8.910177457%/8.329357778%/7.748724736%；3倍整体DD1.483420364%，Sharpe2.067378652，Calmar4.863976912。状态passed，失败项[]。

ETH M2：rejected，三成本净6.715796300%/6.335001962%/5.954417571%，3倍整体DD1.528984097%，正月7/13，近期正折{'1': 0, '2': 0, '3': 0}，扩展21日净0.000000000%/0.000000000%/0.000000000%，各成本执行14/14/14；失败项['ten_of_thirteen_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct', 'extension21_positive_all_costs', 'extension21_three_of_four_positive_folds_all_costs']。

ETH M3：rejected，三成本净6.715796300%/6.335001962%/5.954417571%，3倍整体DD1.528984097%，正月7/13，近期正折{'1': 0, '2': 0, '3': 0}，扩展21日净0.000000000%/0.000000000%/0.000000000%，各成本执行14/14/14；失败项['ten_of_thirteen_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct', 'extension21_positive_all_costs', 'extension21_three_of_four_positive_folds_all_costs']。

M2/M3相对旧M4逐成本真实差异（391日desired、完整cash/q、成交、资金费、NAV、资金费median和预算门槛）：[{"ETH_funding_median_count": 2, "cost": 1, "different_daily_desired_count_vs_old_M4": 1, "different_daily_median_values": 333, "different_selected_settlement_counts": 391, "different_daily_budget_values": 0, "different_funding_block_count": 1, "same_allcost_scene_NAV": false, "all391_desired_and_book_states_equal": false, "all_trades_equal": false, "all_funding_equal": false, "executions": 14, "execution_difference_to_center": 0, "execution_cost_difference_usdt": -0.052046210000000315, "report_status": "rejected", "failed_criteria": ["ten_of_thirteen_positive_complete30d_1x_folds", "recent40_positive_all_costs", "recent40_six_of_eight_positive5d_all_costs", "local_recent6of8_allcost_gte60pct", "extension21_positive_all_costs", "extension21_three_of_four_positive_folds_all_costs"]}, {"ETH_funding_median_count": 2, "cost": 2, "different_daily_desired_count_vs_old_M4": 1, "different_daily_median_values": 333, "different_selected_settlement_counts": 391, "different_daily_budget_values": 0, "different_funding_block_count": 1, "same_allcost_scene_NAV": false, "all391_desired_and_book_states_equal": false, "all_trades_equal": false, "all_funding_equal": false, "executions": 14, "execution_difference_to_center": 0, "execution_cost_difference_usdt": -0.08734511999999484, "report_status": "rejected", "failed_criteria": ["ten_of_thirteen_positive_complete30d_1x_folds", "recent40_positive_all_costs", "recent40_six_of_eight_positive5d_all_costs", "local_recent6of8_allcost_gte60pct", "extension21_positive_all_costs", "extension21_three_of_four_positive_folds_all_costs"]}, {"ETH_funding_median_count": 2, "cost": 3, "different_daily_desired_count_vs_old_M4": 1, "different_daily_median_values": 333, "different_selected_settlement_counts": 391, "different_daily_budget_values": 0, "different_funding_block_count": 1, "same_allcost_scene_NAV": false, "all391_desired_and_book_states_equal": false, "all_trades_equal": false, "all_funding_equal": false, "executions": 14, "execution_difference_to_center": 0, "execution_cost_difference_usdt": -0.12262672999997903, "report_status": "rejected", "failed_criteria": ["ten_of_thirteen_positive_complete30d_1x_folds", "recent40_positive_all_costs", "recent40_six_of_eight_positive5d_all_costs", "local_recent6of8_allcost_gte60pct", "extension21_positive_all_costs", "extension21_three_of_four_positive_folds_all_costs"]}, {"ETH_funding_median_count": 3, "cost": 1, "different_daily_desired_count_vs_old_M4": 1, "different_daily_median_values": 381, "different_selected_settlement_counts": 391, "different_daily_budget_values": 0, "different_funding_block_count": 1, "same_allcost_scene_NAV": false, "all391_desired_and_book_states_equal": false, "all_trades_equal": false, "all_funding_equal": false, "executions": 14, "execution_difference_to_center": 0, "execution_cost_difference_usdt": -0.052046210000000315, "report_status": "rejected", "failed_criteria": ["ten_of_thirteen_positive_complete30d_1x_folds", "recent40_positive_all_costs", "recent40_six_of_eight_positive5d_all_costs", "local_recent6of8_allcost_gte60pct", "extension21_positive_all_costs", "extension21_three_of_four_positive_folds_all_costs"]}, {"ETH_funding_median_count": 3, "cost": 2, "different_daily_desired_count_vs_old_M4": 1, "different_daily_median_values": 381, "different_selected_settlement_counts": 391, "different_daily_budget_values": 0, "different_funding_block_count": 1, "same_allcost_scene_NAV": false, "all391_desired_and_book_states_equal": false, "all_trades_equal": false, "all_funding_equal": false, "executions": 14, "execution_difference_to_center": 0, "execution_cost_difference_usdt": -0.08734511999999484, "report_status": "rejected", "failed_criteria": ["ten_of_thirteen_positive_complete30d_1x_folds", "recent40_positive_all_costs", "recent40_six_of_eight_positive5d_all_costs", "local_recent6of8_allcost_gte60pct", "extension21_positive_all_costs", "extension21_three_of_four_positive_folds_all_costs"]}, {"ETH_funding_median_count": 3, "cost": 3, "different_daily_desired_count_vs_old_M4": 1, "different_daily_median_values": 381, "different_selected_settlement_counts": 391, "different_daily_budget_values": 0, "different_funding_block_count": 1, "same_allcost_scene_NAV": false, "all391_desired_and_book_states_equal": false, "all_trades_equal": false, "all_funding_equal": false, "executions": 14, "execution_difference_to_center": 0, "execution_cost_difference_usdt": -0.12262672999997903, "report_status": "rejected", "failed_criteria": ["ten_of_thirteen_positive_complete30d_1x_folds", "recent40_positive_all_costs", "recent40_six_of_eight_positive5d_all_costs", "local_recent6of8_allcost_gte60pct", "extension21_positive_all_costs", "extension21_three_of_four_positive_folds_all_costs"]}]

6新定义有3条不同三成本净值签名，其中0条签名已在本批8个只读网格对照出现，父组合旧路径别名0组。新父组合3倍净收益与各自M4中心相等0个、更低4个。ETH扩展21日PnL全部为0：True。各银行归因见component_attribution，正组合不得掩盖单组件门槛失败，参数ID或路径别名不算独立alpha。

额外只读核对上轮115333真实结果：本轮6/6新定义的三成本完整净值均有上轮匹配，其中父组合4/4。新ETH M2/M3与上轮ETH M4/VW12完整391日desired、cash/q、交易、资金费与NAV均同；不同信号参数在这段历史产生相同可执行交易，未增加独立路径证据。该对照为看完后的路径重复诊断，不加入预先邻域或重写资格。

匹配持有3倍净-14.782911083%、整体DD18.454766592%，现金0%。相邻Sharpe描述启发式abs(delta)>2×sampleSTD(absdeltas)保留2/10条标记；绝对变化范围[0.0, 0.13673028245565333]，全部边/标记留档，不当统计显著性。

独立审计新ETH原生6条/父12条、旧原生15条/旧父9条曲线；新因果决策2346、旧只读决策5865。导出42成本场景、588逐折、336近期折、168扩展折、16464日NAV、18匹配持有对照、10邻接边和2×3图。每个实际变体独立spec、先reserve后算、各自finish，完成的精确配置只读复用。

原账户SMA/single08:30→10:30Z，L4/FEWM10:10→12:10Z：日事件{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、资金费{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}。官方本轮08:30→12:10结算查询BTC/ETH都空，当前没有资金费现金流；旧08:00:00.001三账户各一次，全链asset/cost/timestamp唯一。18本永续账簿与完整NAV前缀独立核对，现金/持仓/desired/费用不变，不从现金重开或强平。

SMA累计62549分钟/62594点，原均线65日、Float数量、raw75:25和冻结本金不变；完整66日权威research/experiments/20261114T035058Z/forward_inputs.json.gz，本轮分钟包不能当日背景。所有账户仍未成熟180日，是延迟shadow重建，不是实时成交或paper10的真实报价模拟。

启动前检查发现single观察入口继承上轮锁PID1698571；单独CLI适配器在owner检查前供应本轮真实PID1726860，原绑定源码保持、策略/金额/窗口不变，未重复计算或写入旧账户。核验见candidate_lock_adapter_binding；下轮必须绑定自己的实际锁PID。

下轮SMA/single Nov14_10:30→12:30Z，12:31后参考闭合；L4/FEWM12:10→14:10Z，14:11后参考闭合，不能提前运行。三永续账户08:00:00.001已各计一次，本轮四账户仅mark、无日事件/成交/新资金费；下轮仍查询完整实际结算窗口，不能假定8小时。保留原09:56:41.855564Z的funding08公共捕获；本轮新查询08:30→12:10返回空，不把空响应替代旧08记录或重标旧UTC。下次原日决策Nov15_00:01；SMA完整66日权威035058/forward_inputs，本轮135434包仅分钟数组，原均线65日/对称1%/Float数量/1500:500本金/raw75:25不变。仅mark可复用本轮forward.py并改PREV/窗口，日交叉需原dailyadapter增补闭合日。不重置、强平或采用研究参数；旧shadow与十策略实时公开报价模拟分开。

保存的公共行情GET 19次，真实传输失败1次，原raw/body和gzip SHA、URL/UTC/状态均留档。FEWM复用同窗公开数据、single只复用metadata/time，现金流始终独立。旧08捕获UTC2026-11-14T09:56:41.855564Z保留，本轮新空窗口查询UTC2026-11-14T14:02:52.478487Z，两者明确分开。

391日历史已反复开发、多次选参，不能叫未触碰最终测试集、独立未来或稳定实盘盈利；未完成支持显著性声明的DSR/PBO。冻结前向账户不采纳本轮研究参数，paper10十策略全部冻结规则、资金、账本和持仓保持原字节。

[Binance官方USD-M市场数据及资金费说明](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)与[官方公共数据README](https://github.com/binance/binance-public-data/blob/master/README.md)，2026-11-14核对。实际结算时间与过去间隔取公共真实记录，不硬编码8小时；来源和哈希见plan/context/data_manifest/primary_source_reads_current及原始包。

复现工作目录/home/desktop/Documents/Codex/EquiTide，解释器/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B。先bootstrap、review/preflight、review/prepare、review/setup，再review/execute.py依次freeze units bind reserve_0 evaluate audit exports finish_0 research_check；账户midnight_archive l4h02 fewm candidate forward accounts_check；diagnostics、view_image/visual_review、complete_transport_audit、validate_sources，再journal sources_check gates feed collect final_checks、staged_whitespace、seal/publish。原生命令/cwd/UTC/退出码/stdout详见各*_commands.json和review/native_*。准确复现须使用匹配原SHA数据；已有登记禁止精确重算。

本轮真实工程失败：{"facts": [{"action": "Read engine source by searching nonexistent def mature prefix", "actual_error": "ValueError: substring not found", "actual_process_exit_code": 1, "resolved": true, "resolution": "Read actual function names with AST and bounded source lines; no code/model/account evaluation occurred."}]}。6金融+12观察新ID，36事件单独片段登记；全部负收益和淘汰保留。监控只读汇总已存在报告/账户，不新回测、模拟成交、网页部署或定时任务。最终提交/push与完整远端树/blob及解锁后核验以.git/automation_proofs原生回执为准。
