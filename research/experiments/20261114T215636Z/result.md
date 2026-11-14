本轮完成6个新金融配置：2个BTC组件、4个BTC/ETH父组合，共18条1/2/3倍成本场景；6个通过预设历史门槛，0个淘汰。8个既有真实配置/24场景只读复用。恢复上轮受阻的原账户窗口，12个真实短期观察留档；partial rejected仅表示未达到完整180日资格，不取消冻结计划。

事前假设：固定BTC ROC L29、入场H3%、退出E0.5%和入场波动率cap3%，检查更短波动率样本记忆V6/V10能否减少滞后并保持经成本稳健性。预先固定V=[6,10,14]×既有ETH预算R=[0.00875,0.01]，代表V10/R0.01；V14银行、两档ETH银行、两项V14父组合和三项匹配持有均只读。没有事后扩网格或换代表。完整登记扫描确认仅V14已有实算，V6/V10不存在真实结果；初次错误地查找parameters.asset的过滤已在计算前改为spec.universe，原筛查及更正保留。

BTC本金3750/固定入场名义1000USDT。严格完成ROC>3%做多、<-3%做空，入场优先；入场带内实际多头仅ROC>-0.005保留、空头仅ROC<0.005保留，否则退出，相等退出。仅新仓或反手检查过去V个完整日samplelogvol≤3%；同向实际q不变。数量按1000/前日close向下LOT取整，下一00:01真实OPEN成交。新窗口完整391日从原本金实算，prior370指纹仅谱系，不冒充新参数的旧净值前缀。引擎所有函数AST及核算核心字节与前轮完全相同，未改公式或资金规则。

ETH复用本金15000/名义4000的两个真实long-only银行：L5/H2%/E0.75%，有限EWMS16 beta15/17、D3严格K0.75%、V6cap5.625%。M4取距信号1–36小时且available≤信号的最近4笔已成熟真实有符号费率中位数；预算min(.0002,R×过去V8日samplelogvol×最新合格记录真实过去结算间隔小时/24)。保守1小时可得延迟是假设，旧文字E.005不执行，机器E.0075及独立审计为准，旧spec/报告/status原字节保留。

父组合本金18750，raw[1,1]直接相加原规模的3750/15000独立完整银行美元NAV，20/80仅初始本金占比。权重不归一化、不二次加权、不缩放旧银行假冒新名义，不转账、再平衡、产生父订单或跨保证金。BTC真实q、费用、成交量冲击、资金费和保证金逐成本重算；ETH只读投影到共同真实时间轴。

完整读取35676登记事件/17705ID、423份既往结论、三技能/task/README、OOS检查及freqtrade原ZIP。初始16项都已找到真实归档证据，缺实际结果数量0；保留legacy/false原行与历史负结果，不把paper失败当缺历史策略。保护76361份旧文件，最新main已含21UTC paper10观察。上轮main推送、完整远端与解锁后回执已核对，无遗留reserved。

仍使用反复开发的391日：2025-10-19T00:01Z→2026-11-14T00:01Z，另33日背景；每币610562分钟bar、10176小时mark、1273真实资金费，8份Parquet的SHA、单位、连续性、闭合与可得时间已核对。本轮没有新增完整研究日；当日16:00资金费仅用于原冻结账户，不放进截止00:01的研究。

Walk-forward已完成：固定规则、无拟合与前瞻标签，特征只读当时已完成前缀；13个完整30日折+1日尾折，折间cash/q连续，只有全期末计成本平仓。尾折不算正月门槛，单日Sharpe=None；近40日8×5折、扩展21日5+5+5+6折均保存。整体最大回撤由连续全部事件净值计算，不平均折回撤、组件收益率或Sharpe。

Sensitivity已完成：3档BTC波动率窗口×2档ETH预算的全部六格，原生BTC只沿V、ETH只沿R，父组合沿两轴。净收益、整体DD、Sharpe、Calmar、10条邻接变化及所有并列最佳/边界保存。适用局部3倍净正与严格近期合格比例门槛均60%，旧资格不随本次邻域重分类。最佳值在V6/V14端点并列，ETH只有两档，不能据此证明内点宽平台。

Costs已完成：每边5bp手续费+1bp半价差+2bp滑点+0.5×过去20日samplelogvol×sqrt(abs(q)×真实OPEN/过去20日quoteADV)冲击，按不利tick。执行成本和负资金费1/2/3倍、收入不放大；含LOT/tick/minnotional、参与率≤0.1%、费后1倍抵押及闭合小时不利high/low的1%维持保证金代理。线性永续无现货借币，不编借币费；缺历史L2/TCA、完整风险档位、tick强平与真实容量证明，成本是冻结估计而非成交保证。

预设条件：各成本全期/近期净正；1倍≥10/13正完整月；近期各成本≥6/8正5日折；扩展21日各成本净正且≥3/4正折；3倍DD≤25%；两局部比例各≥60%；至少4次底层平仓；1倍(毛价格PnL+净资金费)/执行成本≥2.5；无拒单、负抵押或保证金代理违规；期末平仓且≥180日。任一失败即rejected，本轮六项全部达到这些历史条件，但没有新增收益改善。

|BTC波动率窗口V|ETH R|来源/状态|1x净%|2x净%|3x净%|3x整体DD%|正月/13|近期正折1/2/3|
|---:|---:|---|---:|---:|---:|---:|---:|---|
|6|0.00875|新/passed|9.056276762|8.478305852|7.900520536|1.361994711|12|6/6/6|
|6|0.01|新/passed|8.994680951|8.412871692|7.831248026|1.361994711|12|6/6/6|
|10|0.00875|新/passed|9.000028418|8.422242505|7.844642170|1.362719676|12|6/6/6|
|10|0.01|新/passed|8.938432608|8.356808345|7.775369660|1.362719676|12|6/6/6|
|14|0.00875|旧只读/passed|9.056276762|8.478305852|7.900520536|1.361994711|12|6/6/6|
|14|0.01|旧只读/passed|8.994680951|8.412871692|7.831248026|1.361994711|12|6/6/6|


预设V10/R0.01代表41f377ade77f1c2630d40b9816bec506a9a8bb26bbb143d89534c555e942bdf7：三成本净8.938432608%/8.356808345%/7.775369660%；3倍整体DD1.362719676%，Sharpe2.196913497，Calmar5.312957853。passed，失败项[]。

BTC V6组件：passed，三成本净16.758573627%/15.353622560%/13.948759211%；3倍DD5.737272243%，正月10/13，近期正折{'1': 6, '2': 6, '3': 6}，失败项[]。

BTC V10组件：passed，三成本净16.477331910%/15.073305823%/13.669367381%；3倍DD5.737272243%，正月10/13，近期正折{'1': 6, '2': 6, '3': 6}，失败项[]。

V6与已有V14在全部3成本场景中的391个目标/现金/q状态、全部成交、资金费和完整NAV逐项完全相同；它和两个V6父组合是三条已见路径，不代表新alpha。V10只改变2个日目标，原始ROC目标不变，执行数相同而具体时点/资金费与成本不同；相对V14，两个父组合3倍净收益各低0.055878366个百分点、整体DD各高0.000724966个百分点，Sharpe约低0.015756，没有收益改善。原生与组合均为历史门槛通过，只保留比较，不采纳为新冻结规则。

本批六定义内部三成本路径有6条不同签名，其中3条与本批只读旧参考相同，父组合旧路径别名2条；上轮实际新/只读批次匹配3/6。相对原V14中心，新父组合严格更低收益2项，相同2项。新参数定义、不同路径均不等于独立市场样本。ETH扩展21日PnL全零=True，不能把组合近期盈利归因于ETH。逐银行完整/扩展PnL对账见component_attribution。

原始敏感性启发式abs(deltaSharpe)>2×sampleSTD(absdeltas)标记10/10条，全部保留。绝对变化范围[0.015755692059394644, 0.025996189177534212]，样本STD=0.004371710；约0.008743阈值只是未中心化绝对量与很小离散度比较，不是显著性检验或经济上悬崖的证据。V6/V14完整路径相等、V10仅小幅退化，不能把10个标记机械称为严重过拟合，也不把它们抹去。图中DD色条有+1.362偏移并自动缩放，绝对差约0.000725个百分点，不能凭色彩夸大。

匹配持有3倍净-14.782911083%、DD18.454766592%，现金0%。六父格3倍净正、正Sharpe、严格近期比例分别1.000000/1.000000/1.000000。所有指标并列最佳与边界：[{"metric": "net_return_pct", "sense": "maximize", "fingerprint": "9382afa74973e907db672ae5ee7a2b5465e2d7bdd9d9d8fd6ca17dac8478f9a7", "W": 6, "K": 0.00875, "value": 7.9005205355693775, "all_tied_best_points": [{"W": 6, "K": 0.00875, "fingerprint": "9382afa74973e907db672ae5ee7a2b5465e2d7bdd9d9d8fd6ca17dac8478f9a7", "readonly": false}, {"W": 14, "K": 0.00875, "fingerprint": "a6095f34ce5ba20456c593e855262fd5f1e71863eba86a01b45d339cbdf0e311", "readonly": true}], "BTC_volatility_window_axis_boundary": true, "ETH_ratio_two_values_both_boundaries": true, "readonly": false}, {"metric": "max_drawdown_pct", "sense": "minimize", "fingerprint": "9382afa74973e907db672ae5ee7a2b5465e2d7bdd9d9d8fd6ca17dac8478f9a7", "W": 6, "K": 0.00875, "value": 1.361994710725134, "all_tied_best_points": [{"W": 6, "K": 0.00875, "fingerprint": "9382afa74973e907db672ae5ee7a2b5465e2d7bdd9d9d8fd6ca17dac8478f9a7", "readonly": false}, {"W": 6, "K": 0.01, "fingerprint": "44905e70da93445fa640463e5831e7ca874881599db551d3713bf12473987e18", "readonly": false}, {"W": 14, "K": 0.00875, "fingerprint": "a6095f34ce5ba20456c593e855262fd5f1e71863eba86a01b45d339cbdf0e311", "readonly": true}, {"W": 14, "K": 0.01, "fingerprint": "5f647294c1af82ab332231c4c4d1901cb73a608f72981b771d1dfb561c188c86", "readonly": true}], "BTC_volatility_window_axis_boundary": true, "ETH_ratio_two_values_both_boundaries": true, "readonly": false}, {"metric": "sharpe_365", "sense": "maximize", "fingerprint": "9382afa74973e907db672ae5ee7a2b5465e2d7bdd9d9d8fd6ca17dac8478f9a7", "W": 6, "K": 0.00875, "value": 2.2317508940493043, "all_tied_best_points": [{"W": 6, "K": 0.00875, "fingerprint": "9382afa74973e907db672ae5ee7a2b5465e2d7bdd9d9d8fd6ca17dac8478f9a7", "readonly": false}, {"W": 14, "K": 0.00875, "fingerprint": "a6095f34ce5ba20456c593e855262fd5f1e71863eba86a01b45d339cbdf0e311", "readonly": true}], "BTC_volatility_window_axis_boundary": true, "ETH_ratio_two_values_both_boundaries": true, "readonly": false}, {"metric": "calmar", "sense": "maximize", "fingerprint": "9382afa74973e907db672ae5ee7a2b5465e2d7bdd9d9d8fd6ca17dac8478f9a7", "W": 6, "K": 0.00875, "value": 5.4011342472906465, "all_tied_best_points": [{"W": 6, "K": 0.00875, "fingerprint": "9382afa74973e907db672ae5ee7a2b5465e2d7bdd9d9d8fd6ca17dac8478f9a7", "readonly": false}, {"W": 14, "K": 0.00875, "fingerprint": "a6095f34ce5ba20456c593e855262fd5f1e71863eba86a01b45d339cbdf0e311", "readonly": true}], "BTC_volatility_window_axis_boundary": true, "ETH_ratio_two_values_both_boundaries": true, "readonly": false}]

独立审计新原生6/新父12/旧原生15/旧父9条成本曲线，新因果决策2346、旧只读决策5865；42成本场景、588逐折、336近期折、168扩展折、16464日NAV、18匹配持有、10相邻边及3×2图留档。每个新配置完整spec、先reserve再计算、各自finish；完整金融评估只执行一次。

本轮从最后真实175537账户状态恢复195634受阻窗口：SMA/single14:30→16:30Z，L4/FEWM16:10→18:10Z。日事件{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、新成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、资金费记录{'SMA': 0, 'candidate': 6, 'l4h02': 0, 'fewm': 0}。single用自身BTC空头q=-0.012，在真实fundingTime1794672000000按rate0.00003872/mark65713.9补记，每成本场景收入0.030533306496USDT；收入不按2/3倍放大。ETH空仓零金额三条保留；L4/FEWM之前已记16，本轮不重复。

本轮实际自身现金流：[{"account": "candidate", "asset": "BTC", "cost": "1", "actual_settlement_ns": 1794672000000000000, "held_units": "-0.012000000000000000", "own_amount_usdt": "0.03053330649600000000000000000", "original_public_capture_UTC": "2026-11-14T21:59:55.229143Z"}, {"account": "candidate", "asset": "BTC", "cost": "2", "actual_settlement_ns": 1794672000000000000, "held_units": "-0.012000000000000000", "own_amount_usdt": "0.03053330649600000000000000000", "original_public_capture_UTC": "2026-11-14T21:59:55.229143Z"}, {"account": "candidate", "asset": "BTC", "cost": "3", "actual_settlement_ns": 1794672000000000000, "held_units": "-0.012000000000000000", "own_amount_usdt": "0.03053330649600000000000000000", "original_public_capture_UTC": "2026-11-14T21:59:55.229143Z"}, {"account": "candidate", "asset": "ETH", "cost": "1", "actual_settlement_ns": 1794672000000000000, "held_units": "0", "own_amount_usdt": "0E-16", "original_public_capture_UTC": "2026-11-14T21:59:55.229143Z"}, {"account": "candidate", "asset": "ETH", "cost": "2", "actual_settlement_ns": 1794672000000000000, "held_units": "0", "own_amount_usdt": "0E-16", "original_public_capture_UTC": "2026-11-14T21:59:55.229143Z"}, {"account": "candidate", "asset": "ETH", "cost": "3", "actual_settlement_ns": 1794672000000000000, "held_units": "0", "own_amount_usdt": "0E-16", "original_public_capture_UTC": "2026-11-14T21:59:55.229143Z"}]。18本永续账簿、完整NAV前缀、所有资产×成本×真实时点唯一键已独立核对；三账户历史08/16各一次。旧blocked三定义/失败报告仍原字节保留无结果，新的真实输入窗口以新观察ID完成，不把旧失败报告改成结果；不复制现金流、不重开本金、不重复首单、不窗口强平、不采纳研究参数。

SMA累计62909分钟、62954点，完整66日权威research/experiments/20261114T035058Z/forward_inputs.json.gz保留旧65日数组前缀；原SMA65/对称1%/Float/raw75:25/本金1500:500不变，当前输入仅分钟。SMA原冻结组合3倍累计净-7.468957812%也完整保存，不因负收益删除。四原账户均未成熟180日，延迟shadow重建不冒充实时成交或paper10十策略真实报价模拟。

已恢复195634受阻的待续窗口：SMA/single14:30→16:30Z，L4/FEWM16:10→18:10Z，本轮12个真实观察逐项reserve/finish、保留完整原NAV前缀。single已按自身q/cash补记16:00真实资金费6条，L4/FEWM本轮0、之前已各记一次；三账户历史16各一次。下轮SMA/single16:30→18:30Z，18:31后参考闭合；L4/FEWM18:10→20:10Z，20:11后参考闭合，不提前运行，重新查询实际完整结算窗口，不重复旧资金费、不复制现金流、不重开本金。下一日事件Nov15_00:01。SMA完整66日权威035058/forward_inputs，当前包仅分钟；原65/对称1%/Float/本金1500:500/raw75:25不变。旧blocked三定义仍保留无结果，当前实际窗口有真实输入的新观察ID不冒充旧失败结果。冻结账户不采纳本轮研究参数，不窗口强平。旧shadow与paper10真实报价模拟分开。

原08捕获UTC2026-11-14T09:56:41.855564Z与原16捕获UTC2026-11-14T17:58:56.177141Z保持；本轮重查UTC2026-11-14T21:59:55.229143Z只重核对同一公开字段，不将旧捕获重标为新UTC。

当前保存的独立公共GET 21次，真实传输失败3次；URL/UTC/raw/body/gzipSHA核对。原source自带有界重试成功后才登记和推进；失败原包保留。FEWM只复用同窗公开行情、candidate只复用metadata/time，均独立现金流；SMA内部curl未单独保存失败体/精确UTC的重试按原stderr披露，不补造。

历史391日被反复开发和筛选，非未触碰最终测试集或独立未来。多重选择偏差未消除，没有DSR/PBO统计显著性结论；小条件邻域不能证明广泛平台，正收益回测不能称稳定实盘盈利。

[Binance官方资金费及市场数据](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)与[官方公共数据README](https://github.com/binance/binance-public-data/blob/master/README.md)本轮UTC核对；真实fundingTime、实际过去间隔、闭合/单位/可得时间与SHA见plan/context/data_manifest/primary_source_reads_current。

复现cwd=/home/desktop/Documents/Codex/EquiTide，解释器/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B。bootstrap/review预检、prepare/setup后，review/execute.py依次freeze units bind reserve_0 evaluate audit exports finish_0 research_check；账户midnight_archive l4h02 fewm candidate forward accounts_check；只读diagnostics/historical_aliases/view_image/visual_review/recovered_accounts/complete_transport_audit/validate_sources；再journal sources_check gates feed collect final_checks/staged_whitespace/seal/publish。具体命令/cwd/UTC/退出码/log全留档；已有实际配置禁止重复金融回测，forward --reproduce只读复核不新增模拟窗口。

真实工程处理：{"facts": [{"action": "Initial mutex launcher used script stdin and immediately released before any research mutation", "resolved": true, "native_chunk": "7b6250", "first_broker_pid": 1857024, "actual_held_broker_pid": 1857068, "actual_held_session": 11955, "actual_held_start_chunk": "b003d1", "research_mutations_before_held_lock": 0, "resolution": "Started persistent python -c stdin broker before remote fetch and all research writes"}, {"action": "Precalculation registry screen used nonexistent parameters.asset filter", "resolved": true, "resolution": "Retained original screen and reran fullregistry using spec.universe;confirmed V14actual source and V6/V10 absent before spec/reserve/calculation", "actual_model_or_account_calculations": 0, "initial_native_chunk": "b7f033", "corrected_native_chunk": "96f507"}]}。正/负/失败全部保存，清理可重建缓存，完整账户账本/冻结规则/登记/原包/哈希与下轮状态保留，大行情留忽略data。6金融+12实际观察/36事件独立片段；锁内snapshot只汇总已有账户/报告，不新增回测/成交/部署/定时任务。最终提交/push、完整远端树/blob及解锁后核验见.git/automation_proofs原生回执。
