本轮完成6个新金融配置（2个BTC组件、4个BTC/ETH父组合），18个1/2/3倍成本场景：5个历史通过、1个淘汰。另8个已有真实配置/24场景只读复用。12个原账户观察partial rejected表示未成熟，不取消冻结长期计划。全部真实结果、负收益折、失败和淘汰均保留。

事前假设：BTC更早退出的缓冲E=0.5%或更晚退出的E=1.5%，能否在原E=1%附近改善扣成本收益或风险？最终预设E=[0.005,0.01,0.015]×既有ETH资金费预算系数R=[0.00875,0.01]，3×2面。BTC L29/H3%/V14cap3%固定；ETH两银行、BTC E1%中心、两个旧中心组合及匹配持有全部只读。代表E0.5%/R0.01在计算前固定，未事后换代表或扩网格。准备时提过的0.75%/1.25%未冻结、未登记、未计算；最终取值复用原引擎白名单，策略及金额函数AST不改。

BTC本金3750/固定入场名义1000USDT：29日严格ROC>3%做多、<-3%做空，入场优先；在入场带内，实际多头仅ROC>-E时保留、空头仅ROC<E时保留，否则退出；相等退出。新仓/反手才检查过去14完成日无偏samplelogvol≤3%，同向q不变。LOT数量用N/前日close向下取整，下一00:01真实OPEN执行。E是退出滞后缓冲，绝不是入场H、成本或仓位大小。新BTC spec继承的prior_370day_source_fingerprint仅记录原银行谱系，不主张新E参数的370日资金/持仓前缀相同；两个新BTC银行均从本期首日完整实算391日，未套用原E1%的策略净值前缀。

ETH原本金15000/名义4000、L5/H2%/E0.75%反转、有限归一化EWMS16 beta15/17、D3严格K0.75%、入场V6cap5.625%，long-only。最近4笔距信号1–36小时且available<=信号的真实有符号资金费取中位数；偶数平均中间两数。预算min(.0002,R×V8日samplelogvol×最新合格记录实际过去结算间隔小时/24)。两档R均是已有真实银行，不重算、不从现金重新开。1小时资金费可得延迟为保守假设，不是实测网络延迟。旧persistence文字E.005不执行，机器参数exit_buffer_fraction=.0075及独立审计为准，旧spec/报告原字节保留。

父组合本金18750，raw[1,1]表示两个原规模完整独立银行美元NAV直接相加；初始本金占比20/80。权重不归一化、不二次加权、不线性缩放旧银行为新名义，不转账、再平衡、产生父订单或跨保证金。新BTC逐成本真实核算数量、费用、成交量相关冲击、资金费和风险；ETH净值只读投影到公共时间轴后相加。

完整读取35526条登记事件/17630个ID、420份结论及三技能、task/README、OOS脚本、freqtrade原ZIP。排除观察的规范研究定义11239个，不能当独立样本数。初始16项均有实际归档证据，保留legacy/false和负结果原记录；无缺实际结果项可优先补测。保护75437份旧文件；同步最新main及15UTC paper10结果，上轮已推送，无遗留reserved。

研究数据仍为2025-10-19T00:01Z→2026-11-14T00:01Z的391日重复开发历史，33日背景；每币610562分钟、10176小时mark、1273真实资金费，8份Parquet SHA/时间单位/闭合/连续/可得时间逐一核对。本轮无新完整研究日或研究行情GET；原账户当日08及16时的数据不进入截止00:01的研究。UTC轮次不随本地上海日期跨日改变。

Walk-forward完成：固定规则无拟合、无前瞻标签；13个完整30日折+1日尾折，逐折继承cash/q，只在全期末带成本平仓。滚动信号和成本估计只读当时完成前缀；1倍须至少10/13正完整月，尾折不进月门槛、单日Sharpe=None。近期40日8×5折和扩展21日5+5+5+6折均保留原持仓。整体DD用连续全部事件NAV，不能平均折DD或组件Sharpe。

Sensitivity完成：BTC退出E三档×ETH预算R两档，全部六组合及适用原生邻域的收益、整体DD、Sharpe、Calmar和相邻变化均导出。BTC只沿退出E，ETH只沿预算R；新组合沿两轴。旧资格不重新分类，当前邻域另作诊断。正收益和严格近期合格邻居比例门槛各60%；三档邻域不能证明广泛平台，最佳边界只披露、不事后扩网格。

Costs完成：每边5bp手续费+1bp半价差+2bp滑点+0.5×过去20日samplelogvol×sqrt(abs(q)×真实OPEN/过去20日quoteADV)冲击，不利tick；执行成本与负资金费按1/2/3倍，资金费收入不放大。核对LOT/tick/minnotional、参与率≤0.1%、费后1倍抵押及闭合小时不利high/low的1%维持保证金代理。线性永续无现货借币；没有历史L2/TCA、完整风险档位或tick强平证明，费用/价差/滑点/容量均按冻结估计假设，不能保证实际成交。

预定门槛：全期及近期各成本净正，1倍完整月≥10/13正、近期各成本≥6/8正5日折，扩展21日净正且≥3/4正折，3倍整体DD≤25%，局部正收益/严格近期合格比例≥60%，至少4次底层平仓，1倍(毛价格PnL+净资金费)/执行成本≥2.5，无拒单、负抵押或保证金代理违规，期末平仓且至少180日。任何一项未过即rejected，完整实际结果仍永久保留。

|BTC退出E|ETH R|来源/状态|1x净%|2x净%|3x净%|3x整体DD%|正月/13|近期正折1/2/3|
|---:|---:|---|---:|---:|---:|---:|---:|---|
|0.5%|0.00875|新/passed|9.056277|8.478306|7.900521|1.361995|12|6/6/6|
|0.5%|0.01|新/passed|8.994681|8.412872|7.831248|1.361995|12|6/6/6|
|1.0%|0.00875|旧只读/passed|9.242102|8.668938|8.095959|1.483420|12|6/6/6|
|1.0%|0.01|旧只读/passed|9.180507|8.603503|8.026687|1.483420|12|6/6/6|
|1.5%|0.00875|新/passed|8.811733|8.232774|7.653973|1.488053|12|6/6/6|
|1.5%|0.01|新/passed|8.750137|8.167339|7.584700|1.488053|12|6/6/6|


预设代表BTC E0.5%/ETH R0.01，指纹5f647294c1af82ab332231c4c4d1901cb73a608f72981b771d1dfb561c188c86：1/2/3倍净收益8.994680951%/8.412871692%/7.831248026%，3倍整体DD1.361994711%，Sharpe2.212669189、Calmar5.353893698；状态passed，失败项[]。

BTC E0.5%：passed，三成本净16.758573627%/15.353622560%/13.948759211%；3倍整体DD5.737272243%，正完整月10/13，近期正折{'1': 6, '2': 6, '3': 6}，各成本执行38/38/38；失败项[]。

BTC E1.5%：rejected，三成本净15.535856115%/14.125961000%/12.716020005%；3倍整体DD7.030197559%，正完整月9/13，近期正折{'1': 6, '2': 6, '3': 6}，各成本执行36/36/36；失败项['ten_of_thirteen_positive_complete30d_1x_folds']。

预设E0.5%相对同R0.01旧E1%：3倍净收益差-0.195438837个百分点、整体DD差-0.121425653个百分点、Sharpe差0.055859543。这是更低收益换更小回撤/更高风险调整指标的历史权衡，不能说净收益提高或稳定实盘盈利；不改变原冻结前向账户。E1.5%组件虽然净正，但9/13正月不够10/13而淘汰，四父组合历史通过不掩盖单组件失败。

BTC相对E1%中心逐成本真实差异（391日desired、raw目标、完整现金/持仓、成交、资金费、NAV、成本）：[{"BTC_exit_buffer": 0.005, "cost": 1, "different_daily_desired_count_vs_old_E0p01": 7, "different_raw_pre_entry_filter_targets": 7, "same_allcost_scene_NAV": false, "all391_desired_and_book_states_equal": false, "all_trades_equal": false, "all_funding_equal": false, "executions": 38, "execution_difference_to_center": 2, "execution_cost_difference_usdt": 1.541258850000002, "report_status": "passed", "failed_criteria": []}, {"BTC_exit_buffer": 0.005, "cost": 2, "different_daily_desired_count_vs_old_E0p01": 7, "different_raw_pre_entry_filter_targets": 7, "same_allcost_scene_NAV": false, "all391_desired_and_book_states_equal": false, "all_trades_equal": false, "all_funding_equal": false, "executions": 38, "execution_difference_to_center": 2, "execution_cost_difference_usdt": 3.0813270999999958, "report_status": "passed", "failed_criteria": []}, {"BTC_exit_buffer": 0.005, "cost": 3, "different_daily_desired_count_vs_old_E0p01": 7, "different_raw_pre_entry_filter_targets": 7, "same_allcost_scene_NAV": false, "all391_desired_and_book_states_equal": false, "all_trades_equal": false, "all_funding_equal": false, "executions": 38, "execution_difference_to_center": 2, "execution_cost_difference_usdt": 4.6216083500000025, "report_status": "passed", "failed_criteria": []}, {"BTC_exit_buffer": 0.015, "cost": 1, "different_daily_desired_count_vs_old_E0p01": 9, "different_raw_pre_entry_filter_targets": 9, "same_allcost_scene_NAV": false, "all391_desired_and_book_states_equal": false, "all_trades_equal": false, "all_funding_equal": false, "executions": 36, "execution_difference_to_center": 0, "execution_cost_difference_usdt": -0.047463100000001646, "report_status": "rejected", "failed_criteria": ["ten_of_thirteen_positive_complete30d_1x_folds"]}, {"BTC_exit_buffer": 0.015, "cost": 2, "different_daily_desired_count_vs_old_E0p01": 9, "different_raw_pre_entry_filter_targets": 9, "same_allcost_scene_NAV": false, "all391_desired_and_book_states_equal": false, "all_trades_equal": false, "all_funding_equal": false, "executions": 36, "execution_difference_to_center": 0, "execution_cost_difference_usdt": -0.09670209999999457, "report_status": "rejected", "failed_criteria": ["ten_of_thirteen_positive_complete30d_1x_folds"]}, {"BTC_exit_buffer": 0.015, "cost": 3, "different_daily_desired_count_vs_old_E0p01": 9, "different_raw_pre_entry_filter_targets": 9, "same_allcost_scene_NAV": false, "all391_desired_and_book_states_equal": false, "all_trades_equal": false, "all_funding_equal": false, "executions": 36, "execution_difference_to_center": 0, "execution_cost_difference_usdt": -0.14071820000000912, "report_status": "rejected", "failed_criteria": ["ten_of_thirteen_positive_complete30d_1x_folds"]}]

6新定义有6条不同三成本签名，在本批8个只读网格对照中重复签名0条；额外只读比较上轮全部新/只读结果，本轮匹配旧路径0/6个，其中父组合0/4。该诊断不重写资格；新路径仍不是独立市场样本。新父组合3倍净收益低于各自E1%中心4个、相等0个。ETH扩展21日PnL全部0：True，逐银行归因和18个父场景PnL对账见component_attribution。

匹配持有3倍净-14.782911083%、整体DD18.454766592%，现金0%。六父格3倍净正比例1.000000、正Sharpe比例1.000000、严格近期合格比例1.000000；启发式abs(deltaSharpe)>2×sampleSTD(absdeltas)标记1/10条边，绝对变化范围[0.017989575686620185, 0.22182927964877086]，全部边/标记留档，不当统计显著性。退出轴净收益最佳是否边界：False。

逐指标边界补充：[{"metric": "net_return_pct", "sense": "maximize", "fingerprint": "bf81331e1132b6fc12306dcc263fc28cfcf5d535abf4f459128a5a5110b738f2", "W": 0.01, "K": 0.00875, "value": 8.09595937225367, "BTC_exit_axis_boundary": false, "ETH_ratio_axis_two_values_both_boundaries": true, "readonly": true}, {"metric": "max_drawdown_pct", "sense": "minimize", "fingerprint": "a6095f34ce5ba20456c593e855262fd5f1e71863eba86a01b45d339cbdf0e311", "W": 0.005, "K": 0.00875, "value": 1.361994710725134, "BTC_exit_axis_boundary": true, "ETH_ratio_axis_two_values_both_boundaries": true, "readonly": false}, {"metric": "sharpe_365", "sense": "maximize", "fingerprint": "a6095f34ce5ba20456c593e855262fd5f1e71863eba86a01b45d339cbdf0e311", "W": 0.005, "K": 0.00875, "value": 2.2317508940493043, "BTC_exit_axis_boundary": true, "ETH_ratio_axis_two_values_both_boundaries": true, "readonly": false}, {"metric": "calmar", "sense": "maximize", "fingerprint": "a6095f34ce5ba20456c593e855262fd5f1e71863eba86a01b45d339cbdf0e311", "W": 0.005, "K": 0.00875, "value": 5.4011342472906465, "BTC_exit_axis_boundary": true, "ETH_ratio_axis_two_values_both_boundaries": true, "readonly": false}]。净收益最佳在原E1%中间值；最小DD及最大Sharpe/Calmar在E0.5%下边界。ETH只有两档，不能凭两个端点声称内点平台；全部指标边界披露而不扩本轮网格、不换预设代表。

独立审计新BTC原生6条/父12条、旧原生15条/旧父9条曲线；新因果决策2346、旧只读决策5865。导出42成本场景、588逐折、336近期折、168扩展折、16464日NAV、18匹配持有对照、10邻接边及3×2图。所有实际变体独立spec、先reserve后算、各自finish；旧真实组件仅复用已存完整银行净值。

原账户SMA/single Nov14_10:30→12:30Z，L4/FEWM12:10→14:10Z：日事件{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、新成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、资金费{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}。本轮官方10:30→14:10完整窗口BTC/ETH结算查询均为空；旧08:00:00.001三永续各计一次，全部历史asset/cost/timestamp唯一。18本永续账簿及完整NAV前缀核对，不现金重开、不重复首单、不窗口强平、不采用新研究参数。各入口在绑定前统一为本轮真实锁PID1758091，无需上轮临时CLI适配器；冻结策略/金额内核不变。

SMA累计62669分钟/62714点；完整66日权威research/experiments/20261114T035058Z/forward_inputs.json.gz，旧65日背景前缀一致，原SMA65日/对称1%/Float/raw75:25规则与本金不变。本轮仅分钟包，不能当日背景。账户尚未成熟180日，是延迟shadow重建，不是实时成交，也不是paper10十策略真实报价模拟。

下轮SMA/single Nov14_12:30→14:30Z，14:31后参考闭合；L4/FEWM14:10→16:10Z，16:11后参考闭合，不能提前运行。三永续账户08:00:00.001已各计一次，本轮四账户仅mark、无日事件/成交/新资金费；下轮仍查询完整实际结算窗口，不能假定8小时。保留原09:56:41.855564Z的funding08公共捕获；本轮新查询10:30→14:10返回空，不把空响应替代旧08记录或重标旧UTC。下次原日决策Nov15_00:01；SMA完整66日权威035058/forward_inputs，本轮155436包仅分钟数组，原均线65日/对称1%/Float数量/1500:500本金/raw75:25不变。仅mark可复用本轮forward.py并改PREV/窗口，日交叉需原dailyadapter增补闭合日。不重置、强平或采用研究参数；旧shadow与十策略实时公开报价模拟分开。

L4/FEWM nextwindow reaches16:10 and may contain real16UTCsettlement. Query actualfundingTime/rate/markPrice before dependent evaluation; current14:10cursor has notbooked it. Single nextcut14:30doesnotnominallycross16,stillqueryrealwindow. No copied08cashflows.

本轮保存公共行情GET 18次、真实传输失败2次；成功及可独立保存的请求，其URL/UTC/状态/raw及body/gzip SHA已核对。SMA内置curl重试如失败，只留原stderr，原命令未逐次保存失败响应体和精确UTC，明确披露且不补造；见complete_transport_verification中的SMA_internal_retry_stderr与SMA_failed_attempt_body_not_separately_persisted_by_original_curl。FEWM只复用同窗公开行情，single仅复用metadata/time，独立账簿现金流不复制。原08字段捕获UTC2026-11-14T09:56:41.855564Z保持；新空窗口预检UTC2026-11-14T15:57:59.277790Z，两者不混淆或重标UTC。

391日历史和此前参数选择被反复使用，非未触碰最终测试集或独立未来；多重选择偏差未消除，未完成支持显著性结论的DSR/PBO，不能宣称稳定实盘盈利。四个原冻结前向账户不采纳本轮参数；paper10规则、资金、持仓、账本完整原字节保留。

[Binance官方USD-M市场数据及资金费说明](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)本轮2026-11-14 UTC核对，[官方公共数据README](https://github.com/binance/binance-public-data/blob/master/README.md)同UTC日上轮已核对。真实fundingTime/实际过去间隔决定结算，不硬编码名义8小时；来源版本、数据SHA和真实包见plan/context/data_manifest/primary_source_reads_current及窗口预检。

复现工作目录/home/desktop/Documents/Codex/EquiTide，解释器/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B。bootstrap、review/preflight、review/prepare、review/setup后，review/execute.py依次freeze units bind reserve_0 evaluate audit exports finish_0 research_check；账户midnight_archive l4h02 fewm candidate forward accounts_check；diagnostics、historical_aliases、view_image/visual_review、complete_transport_audit、validate_sources，再journal sources_check gates feed collect final_checks、staged_whitespace、seal/publish。各原生命令/cwd/UTC/退出码/stdout见*_commands.json和review/native_*；已有登记会阻止精确重算。

本轮真实工程失败：{"facts": [{"action": "functions.exec orchestration parse before nested calls", "error": "SyntaxError: Invalid or unexpected token; stray quote after yield_time_ms property", "nested_tools_executed": 0, "resolved": true, "resolution": "Corrected JS property syntax and retried source preparation; ongoing independently launched financial process was not interrupted or rerun."}]}。所有实际正/负/淘汰、完整账本、冻结规则、登记、必要源码、原响应和下轮状态保留，清理可重建缓存，大行情只留忽略data。6金融+12观察新ID、36事件独立片段留档。只读snapshot汇总已有报告和账户，不新增回测/成交/部署/定时任务；最终commit/push、完整远端树/blob及解锁后核验以.git/automation_proofs原生回执为准。
