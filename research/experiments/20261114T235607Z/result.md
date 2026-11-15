本轮真实完成6个新金融配置：2个ETH原生组件、4个BTC/ETH父组合，共18条1/2/3倍成本场景。4个父组合通过预设历史门槛，两个ETH组件淘汰；8个已有真实配置/24场景只读复用。12项原冻结账户窗口实际观察保留，partial rejected仅表示尚未成熟180日，不取消长期计划。所有正/负收益、失败及完整折证据保留。

事前假设：固定更严格的ETH资金费预算R=0.00875，比较已成熟资金费中位数样本数M=[2,3,4]，检验更短样本能否减少滞后而保持经成本稳健性；与只读BTC波动率窗口V=[10,14]银行组成3×2面。代表M3/BTCV14在新结果前指定，未扩网格或换代表。完整登记查重确认R0.01的M2/M3已真实淘汰，不再重跑；本轮新定义是M2/M3与R0.00875的具体参数组合，旧M4及BTC银行/两个对应父组合/持有基准只读。

ETH本金15000/固定名义4000，long-only：完成ROC L5/H2%、退出E0.75%，有限EWMS16 beta15/17、D3严格K0.75%趋势门、入场V6 samplelogvol≤5.625%。只在新仓/反手检查门槛，同向实际q保留。M取信号前距今1–36小时且available≤信号的最近M笔真实已结算有符号资金费，中位数偶数取中间两数平均，奇数取中间值，缺M笔阻止新仓。预算min(.0002,0.00875×过去V8日samplelogvol×最新合格记录真实过去结算间隔小时/24)，比较max(desired×median,0)，等于预算可过，资金费不强迫持仓退出。最终负desired归零，正常退出/同向q不变。保守1小时可得延迟是假设。

新ETH按完整391日从原本金独立计算真实数量、费用、成交量冲击、资金费与保证金；prior370指纹仅谱系，不复用新参数的旧货币前缀。原spec persistence的E.005是历史文字错误，机器参数一直E.0075；本轮新spec文字同步修正，旧spec/报告/status原字节不改，文字修正本身不计新定义。引擎全部函数AST及核算核心字节与前轮完全相同。

BTC完全复用既有实际银行：本金3750/固定名义1000，ROC L29、入场H3%、退出E0.5%，入场波动率V10或14、cap3%；严格ROC>3%做多、<-3%做空，带内实际多头仅ROC>-0.005/空头仅ROC<0.005保留，相等退出。只在新/反手入场过滤，保留实际q；LOT向下取整、下一00:01真实OPEN不利tick执行。未重新计算BTC策略，也不缩放旧净值假冒新名义。

父组合本金18750、raw[1,1]直接相加BTC3750和ETH15000两个原规模独立完整银行的美元NAV；20/80仅初始本金占比，权重保留原值，不归一化、不二次加权、不转账/再平衡/父订单/跨保证金。对齐完整事件时间轴重算组合净值和整体回撤，不平均组件收益、Sharpe或回撤。

完整读取35732登记事件/17733ID、424份结论、三技能/task/README、OOS脚本及freqtrade原ZIP。初始16项都已找到真实归档，缺实际结果0；保留legacy/false原行与旧负结果，不把paper失败当缺历史策略。保护76685份旧文件；基于最新main与23UTC paper10结果，上轮已推送并完成远端及解锁后核验，无遗留reserved。

研究仍为复用的391日开发历史：2025-10-19T00:01Z→2026-11-14T00:01Z，另33日背景；每币610562分钟bar、10176小时mark、1273真实资金费，8份Parquet的SHA、单位、连续性、闭合与可得时间核对。虽然本轮跨到Nov15 UTC，研究没有加入新的完整日，不能称为新最终留出或独立未来。原账户使用各自固定待续窗口，与研究样本截止分开。

Walk-forward已执行：固定规则、无拟合或前瞻标签，所有特征只读当时已完成前缀；13完整30日折+1日尾折，现金/持仓跨折连续，仅全期末带成本平仓。尾折不算正月门槛、单日Sharpe=None；近40日8×5折和扩展21日5+5+5+6折保存，整体DD来自连续全部事件NAV。无训练标签，purge/embargo没有标签泄漏用途；实际33日背景、信号后下一可执行OPEN和资金费成熟界限独立检查。

Sensitivity已执行：ETH M三档×BTC V两档全部六格、ETH只沿M/BTC只沿V的原生邻域，净收益/整体DD/Sharpe/Calmar、所有并列最佳边界与10条相邻变化保存。局部3倍净正与严格近期比例门槛各60%；原生ETH近期不合格，不能用父组合的邻域通过掩盖。最佳为旧M4边界且BTC仅两档，没有宽平台证明；不事后扩批或重选代表。

Costs已执行：每边5bp手续费+1bp半价差+2bp滑点+0.5×过去20日samplelogvol×sqrt(abs(q)×真实OPEN/过去20日quoteADV)冲击，不利tick；执行成本及负资金费1/2/3倍，收入不放大。含LOT/tick/minnotional、参与率≤0.1%、费后1倍抵押及闭合小时high/low的1%维持保证金代理。线性永续不借现货，不编借币费用；缺历史L2/TCA、完整风险档位、tick强平与真实容量证明，成本仍是冻结估计。

预设通过条件：各成本全期/近期净正；1倍≥10/13正完整月；近期各成本≥6/8正5日折；扩展21日各成本净正且≥3/4正折；3倍DD≤25%；适用两局部比例≥60%；至少4底层平仓；1倍(毛价格PnL+净资金费)/执行成本≥2.5；无拒单、负抵押或保证金代理违规；期末平仓且≥180日。任何失败即rejected，仍保存完整真实结果。

|ETH中位数M|BTC波动率V|来源/状态|1x净%|2x净%|3x净%|3x整体DD%|正月/13|近期正折1/2/3|
|---:|---:|---|---:|---:|---:|---:|---:|---|
|2|10|新/passed|8.498916408|7.973663597|7.448596193|1.362719676|12|6/6/6|
|2|14|新/passed|8.555164751|8.029726944|7.504474559|1.361994711|12|6/6/6|
|3|10|新/passed|8.431971497|7.887035106|7.342283864|1.362719676|11|6/6/6|
|3|14|新/passed|8.488219840|7.943098454|7.398162230|1.361994711|11|6/6/6|
|4|10|旧只读/passed|9.000028418|8.422242505|7.844642170|1.362719676|12|6/6/6|
|4|14|旧只读/passed|9.056276762|8.478305852|7.900520536|1.361994711|12|6/6/6|


事前代表M3/BTCV14，指纹a921f9e57b9d087be1223b7097a32a62db8c0f9d221eb28df286cba831b5676c：三成本净8.488219840%/7.943098454%/7.398162230%；3倍DD1.361994711%，Sharpe2.081131758，Calmar5.058504026。passed，失败项[]。

ETH M2/R0.00875组件：rejected，三成本全期净6.504312532%/6.198753040%/5.893403396%；3倍DD1.528984097%，正月6/13，近期正折{'1': 0, '2': 0, '3': 0}，三成本近期40日净0.000000000%/0.000000000%/0.000000000%；失败项['ten_of_thirteen_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct', 'extension21_positive_all_costs', 'extension21_three_of_four_positive_folds_all_costs']。全期正收益不能覆盖月度、近期和扩展失败。

ETH M3/R0.00875组件：rejected，三成本全期净6.420631393%/6.090467427%/5.760512985%；3倍DD1.528984097%，正月6/13，近期正折{'1': 0, '2': 0, '3': 0}，三成本近期40日净-0.020516561%/-0.041144478%/-0.061884606%；失败项['ten_of_thirteen_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct', 'extension21_positive_all_costs', 'extension21_three_of_four_positive_folds_all_costs']。全期正收益不能覆盖月度、近期和扩展失败。

两ETH组件都仅6/13正完整月、近期0/8正5日折；M2近期40日净0，M3近期各成本为负，扩展21日两者均0。原生近期与扩展门槛失败，明确淘汰。四父组合依靠BTC近期正贡献通过历史门槛，不能将组合资格当成ETH过滤改动成功；相对同BTC银行的旧M4，四新父组合收益/Sharpe/Calmar均低而整体DD没有下降，没有新增收益改善，不采用为新冻结规则。

六定义内部有6条不同三成本签名，其中旧参考匹配0；上轮实际新/只读配置匹配0/6。新父组合收益低于各自M4中心4个、相同0个；新路径不等于独立市场样本。ETH扩展21日PnL全零=True，该段父盈利由BTC贡献。逐银行完整/扩展PnL与各成本守恒见component_attribution。

原始abs(deltaSharpe)>2×sampleSTD(absdeltas)启发式标记3/10，全部保存；绝对变化范围[0.01566902852499652, 0.19387297733101172]，样本STD=0.066426698，不作统计显著性或过拟合概率结论。图中DD色条有+1.362偏移并自动缩放，BTC V10/14绝对差约0.000725个百分点，不凭色彩夸大。ETH M2/M3/M4各行的DD相同，不称风险改善。

匹配持有3倍净-14.782911083%、DD18.454766592%，现金0%。父网格3倍净正/正Sharpe/严格近期比例1.000000/1.000000/1.000000；所有指标最佳及并列边界：[{"metric": "net_return_pct", "sense": "maximize", "fingerprint": "a6095f34ce5ba20456c593e855262fd5f1e71863eba86a01b45d339cbdf0e311", "W": 4, "K": 14, "value": 7.9005205355693775, "all_tied_best_points": [{"W": 4, "K": 14, "fingerprint": "a6095f34ce5ba20456c593e855262fd5f1e71863eba86a01b45d339cbdf0e311", "readonly": true}], "ETH_median_axis_boundary": true, "BTC_vol_two_values_both_boundaries": true, "readonly": true}, {"metric": "max_drawdown_pct", "sense": "minimize", "fingerprint": "363f5715cb22c9a0389de1a98e1887658eb6b275384d7e9a4f2e8ad3ea26f780", "W": 2, "K": 14, "value": 1.361994710725134, "all_tied_best_points": [{"W": 2, "K": 14, "fingerprint": "363f5715cb22c9a0389de1a98e1887658eb6b275384d7e9a4f2e8ad3ea26f780", "readonly": false}, {"W": 3, "K": 14, "fingerprint": "a921f9e57b9d087be1223b7097a32a62db8c0f9d221eb28df286cba831b5676c", "readonly": false}, {"W": 4, "K": 14, "fingerprint": "a6095f34ce5ba20456c593e855262fd5f1e71863eba86a01b45d339cbdf0e311", "readonly": true}], "ETH_median_axis_boundary": true, "BTC_vol_two_values_both_boundaries": true, "readonly": false}, {"metric": "sharpe_365", "sense": "maximize", "fingerprint": "a6095f34ce5ba20456c593e855262fd5f1e71863eba86a01b45d339cbdf0e311", "W": 4, "K": 14, "value": 2.2317508940493043, "all_tied_best_points": [{"W": 4, "K": 14, "fingerprint": "a6095f34ce5ba20456c593e855262fd5f1e71863eba86a01b45d339cbdf0e311", "readonly": true}], "ETH_median_axis_boundary": true, "BTC_vol_two_values_both_boundaries": true, "readonly": true}, {"metric": "calmar", "sense": "maximize", "fingerprint": "a6095f34ce5ba20456c593e855262fd5f1e71863eba86a01b45d339cbdf0e311", "W": 4, "K": 14, "value": 5.4011342472906465, "all_tied_best_points": [{"W": 4, "K": 14, "fingerprint": "a6095f34ce5ba20456c593e855262fd5f1e71863eba86a01b45d339cbdf0e311", "readonly": true}], "ETH_median_axis_boundary": true, "BTC_vol_two_values_both_boundaries": true, "readonly": true}]

审计新ETH原生6条/新父12条、旧原生15条/旧父9条成本曲线；新独立重算的决策2346、旧只读核验决策5865。42成本场景、588逐折、336近期折、168扩展折、16464日NAV、18持有对照、10相邻边与3×2图留档。全体实际变体各自完整spec、先reserve后计算、各自finish；完整金融评估只执行一次。R0.01的M2/M3旧淘汰结果只读比较见existing_R001_results_readonly_comparison，未重算。

原冻结账户SMA/single16:30→18:30Z，L4/FEWM18:10→20:10Z，均为Nov14 UTC；本轮日事件{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、资金费记录{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}，全部0。完整实际结算窗口查询为空，不按名义8小时编资金费，也不重复上轮已记的16:00。18本永续账簿现金/数量/entry等字段原样，完整NAV前缀与所有历史资金费/日事件唯一键核对；仅增加闭合分钟估值与风险点。

SMA累计63029分钟、63074点，原65/对称1%/Float/raw75:25/本金1500:500不变。完整66日权威research/experiments/20261114T035058Z/forward_inputs.json.gz保留旧65日原数组前缀，当前包仅分钟；原SMA组合3倍累计净-7.468957812%也完整保存。所有原账户仍未成熟180日，延迟shadow不冒充实时成交或paper10十策略真实报价模拟。旧blocked与全部paper10冻结计划/本金/持仓/账本保持原字节。

本轮SMA/single Nov14_16:30→18:30Z，L4/FEWM18:10→20:10Z，仅增加已闭合分钟估值/风险点。实际完整结算窗口公开字段为空，四账户0资金费/0日事件/0成交，原cash/q/desired/已计成本不变。三永续账户过去Nov14_16:00已各记一次，不重复。下轮SMA/single18:30→20:30Z，20:31后参考闭合；L4/FEWM20:10→22:10Z，22:11后闭合，重新查询实际结算窗口、不硬编码8小时。下一原日事件Nov15_00:01；仅在实际续接窗口覆盖该时点时使用原日决策与新增闭合日背景，当前下一窗口仍未覆盖它。SMA完整66日权威035058/forward_inputs，当前包仅分钟；原65/对称1%/Float/本金1500:500/raw75:25不改，禁止拿本轮minute包冒充完整日背景。原冻结策略/本金/持仓不采纳研究M2/M3，不窗口强平、不重开账户。旧blocked失败和paper10原账本保留；旧shadow与十策略真实报价模拟分开。

原08捕获UTC2026-11-14T09:56:41.855564Z与16捕获UTC2026-11-14T17:58:56.177141Z保持；本轮查询UTC2026-11-15T00:02:58.387558Z字段为空，与旧16记录不同，不将旧捕获重标为新UTC。

保存独立公共GET 18次，实际传输失败0次；URL/UTC/raw/body/gzipSHA均留档。FEWM只复用同窗公开行情、candidate只复用metadata/time，账户cashflow不复制；SMA内部curl未另存失败体/精确UTC的重试按原stderr披露，不补造。

391日已反复用于开发与筛选，非未触碰最终测试集或独立未来，多重选择偏差未消除；没有DSR/PBO统计显著性结论，小邻域不证明广泛平台。正收益回测不能称稳定实盘盈利，当前研究不修改冻结账户。

[Binance官方资金费及市场数据](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)与[官方公共数据README](https://github.com/binance/binance-public-data/blob/master/README.md)本轮UTC核对；实际fundingTime/间隔、单位、闭合、可得时间与SHA见plan/context/data_manifest/primary_source_reads_current。

复现cwd=/home/desktop/Documents/Codex/EquiTide，解释器/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B。bootstrap/review预检、prepare/setup后，review/execute.py依次freeze units bind reserve_0 evaluate audit exports finish_0 research_check；账户midnight_archive l4h02 fewm candidate forward accounts_check；diagnostics/historical_aliases/view_image/visual_review/account_continuity/complete_transport_audit/validate_sources；再journal sources_check gates feed collect final_checks/staged_whitespace/seal/publish。具体命令/cwd/UTC/退出码/log保留；已有实际配置禁止精确重复回测，forward --reproduce仅只读复核不新增窗口。

真实工程/访问阻碍：{"facts": []}。全部实际正/负/失败、账本、冻结规则、登记、原包/哈希与下轮状态保存，可重建缓存清理、大行情保持忽略。6金融+12实际观察/36事件独立片段；锁内snapshot只汇总已有账户/报告，不新增回测/成交/部署/任务。最终commit/push、完整远端树/blob及解锁后核验见.git/automation_proofs原生回执。
