本轮完成6个新金融配置：BTC动量ROC回看期L28/L30两个组件，固定风险窗口V10与波动率上限2.75%，与已有ETH预算R=.00875/.01组成四父组合，18条1/2/3倍成本场景。历史通过4个：4父+0BTC；淘汰2个。8旧实际配置/24场景只读；12项原账户窗口各自reserve/finish，partial rejected表示尚未成熟180日，不取消原长期计划。

假设与预设：固定H3%/退出E0.5%/风险V10/cap2.75%，预声明BTC ROC L=[28,29,30]×ETH R=[.00875,.01]，短ROC响应更早但可能多交易，长ROC平滑噪音但可能延迟出场；旧L29中心只读，事前代表L28/R.01固定。所有新完整定义先reserve再计算；不看结果后扩批或换代表，历史仍为复用开发样本。

BTC规则：本金3750/固定名义1000；完成L=28/29/30日ROC严格>3%多、<−3%空，入场优先；带内实际多仅ROC>−0.5%、空仅ROC<0.5%保留，相等退出。仅新/反手检查过去10个完成日无偏样本log(close/prevclose)波动率≤固定2.75%，同向实际q保持。信号可得后的下一00:01 OPEN、不利tick、LOT向下；新L28/L30从原现金完整计算391日数量、费用、冲击、资金费和保证金，不缩放旧NAV。

ETH只读：本金15000/名义4000，long-only L5/H2%/退出E0.75%，有限归一化EWMS16 beta15/17、D3严格K0.75%、V6 cap5.625%；最近4笔实际已实现有符号资金费中位数，信号前1–36小时且available≤signal合格，缺4笔阻新仓。预算min(.0002,R×过去V8样本logvol×最新合格过去实际结算间隔小时/24)。R原值.00875/.01，仅新入场过滤，原同向q/退出不变。旧ETH文字E.005过期而机器E.0075，旧spec/报告/status原字节保持。

父组合本金18750/raw[1,1]直接相加BTC3750与ETH15000两个原规模银行的美元NAV，20/80仅初始本金占比，权重不归一化。无缩放、转账、再平衡、父订单或跨保证金；对齐完整事件时间轴后重算组合NAV与整体DD，不平均收益/Sharpe/回撤。

完整读取36180登记事件/17957ID、432份结论、task/README/三技能、checks/*oos.py及freqtrade原ZIP。初始16条均有实际证据，缺实际结果0，旧legacy/false及负结果保留；旧paper失败观察不补单重跑。保护79266旧文件，main上原报价、账本和缺口保持。

Walk-forward已执行：2025-10-19T00:01Z→2026-11-14T00:01Z，391日/33日背景。每币610562分钟bar、10176小时mark、1273实际资金费，8份Parquet SHA、单位、闭合/可得时间及连续性核验。固定规则无训练/标签，仅使用完成前缀；13完整30日折+1日尾折，现金/持仓跨折连续，全期终止才按成本平仓，整体DD用完整事件NAV。近40日8×5及扩展21日5+5+5+6逐折保存，尾折Sharpe=None不计完整正月；无标签故无标签purge用途，背景/下一OPEN/资金费成熟另核验。OOS字样沿用机器字段，实际是复用开发历史。

Sensitivity已执行：BTC ROC回看期L三档×ETH R两档六格；BTC组件只沿L，ETH只沿R。全部净收益、整体DD、Sharpe、Calmar、近期正折、10相邻变化和并列最优边界保留。局部3倍净正与严格近期合格比例各≥60%；小邻域/两档ETH不能证明宽平台，不事后扩批/换代表。相同NAV若出现须披露，参数不同仍分别登记，不能当独立样本。

Costs已执行：每边费5bp+半价差1bp+滑点2bp+0.5×过去20日样本logvol×sqrt(abs(q)×真实OPEN/过去20完整日quoteADV)，不利tick与实际LOT/minnotional；参与率≤0.1%，费后1倍抵押，闭合小时high/low的1%维持保证金代理。执行成本与负资金费1/2/3倍，收入不放大；线性永续无需借现货，不编借币费。含逐项费用、交易数/成本占比、持有与现金0比较；冻结费率/盘口为估计，缺历史L2/TCA、完整档位、tick强平和真实容量证明。

冻结门槛：三成本全期/近期净正；1倍≥10/13正完整月；近期各成本≥6/8正5日折；扩展21日三成本净正且≥3/4正折；3倍DD≤25%；两项适用局部比例≥60%；至少4底层平仓；1倍(毛价格PnL+净资金费)/执行成本≥2.5；无拒单、负抵押或保证金代理违规，期末平仓且≥180日。任一失败即rejected，结果仍保留。

|BTC ROC L|ETH R|来源/状态|1x净%|2x净%|3x净%|3x整体DD%|正月/13|近期正折1/2/3|
|---:|---:|---|---:|---:|---:|---:|---:|---|
|28日|0.00875|新/passed|8.698275789|8.130309253|7.562485500|1.359650425|10|6/6/6|
|28日|0.01|新/passed|8.636679978|8.064875094|7.493212990|1.359650425|10|6/6/6|
|29日|0.00875|旧只读/passed|9.158860698|8.581388838|8.004112196|1.360652752|12|6/6/6|
|29日|0.01|旧只读/passed|9.097264887|8.515954679|7.934839687|1.360652752|12|6/6/6|
|30日|0.00875|新/passed|8.326902610|7.741915479|7.157091864|1.468861903|12|6/6/6|
|30日|0.01|新/passed|8.265306799|7.676481319|7.087819354|1.468861903|12|6/6/6|


事前代表L28/V10/cap2.75%/R.01（96b56d9114a22136e5b10504f647df6403dc6188cb92610aa87ee52a92485f1b）：三成本净8.636679978%/8.064875094%/7.493212990%，3倍DD1.359650425%，Sharpe2.144501447、Calmar5.132174514，passed，失败项[]。

BTC L28日/cap2.75%组件rejected：三成本净14.968568761%/13.613639567%/12.258584031%，3倍DD6.262454704%，Sharpe1.219096717、Calmar1.820166055，正月9/13、近期{'1': 6, '2': 6, '3': 6}，失败项['ten_of_thirteen_positive_complete30d_1x_folds']。

BTC L30日/cap2.75%组件rejected：三成本净13.111702867%/11.671670696%/10.231615851%，3倍DD6.331433300%，Sharpe1.002139299、Calmar1.503590675，正月9/13、近期{'1': 6, '2': 6, '3': 6}，失败项['ten_of_thirteen_positive_complete30d_1x_folds']。

两个新BTC组件均仅9/13正完整月而淘汰，尽管三成本总净正且近期各6/8；L28两父10/13、L30两父12/13，四父历史通过。组合通过不替代组件资格。ETH扩展21日PnL为0，该段父利润来自BTC；旧ETH状态不改，代表始终L28/R.01，不事后改为旧中心或更高格。

配对旧L29：新L28日/R0.00875，3倍净变化-0.441626697个百分点、整体DD变化-0.001002326个百分点、Sharpe-0.101069857、Calmar-0.297665266。

配对旧L29：新L28日/R0.01，3倍净变化-0.441626697个百分点、整体DD变化-0.001002326个百分点、Sharpe-0.101290209、Calmar-0.297713022。

配对旧L29：新L30日/R0.00875，3倍净变化-0.847020333个百分点、整体DD变化+0.108209151个百分点、Sharpe-0.316273492、Calmar-0.939192705。

配对旧L29：新L30日/R0.01，3倍净变化-0.847020333个百分点、整体DD变化+0.108209151个百分点、Sharpe-0.315506640、Calmar-0.935732290。

四个新父的净收益/Sharpe/Calmar均低于匹配ETH预算的旧L29。L28三倍成本净收益少约0.441627个百分点、整体DD仅少约0.001002个百分点，是微小回撤改善伴随收益代价；L30净收益少约0.847020个百分点、DD高约0.108209个百分点。没有收益与回撤的联合改善。小3×2条件邻域、两档ETH和两组件正月失败，不能证明宽平台；原始启发标记与全部数值保留，不改门槛、不换代表，待独立未来。

六新配置全成本NAV签名6组，匹配8旧参考0组，匹配上轮实际新/只读路径0/6；原始abs(deltaSharpe)>2×sampleSTD(absdeltas)标记3/10，绝对变化范围[0.018350428073167002, 0.3955739648742551]、STD0.144466542，不是显著性或过拟合概率。三倍净正/正Sharpe/严格近期比例1.0/1.0/1.0。

匹配持有3倍净-14.782911083%、DD18.454766592%，现金0；18父成本场景BTC/ETH利润守恒。独立审计新原生6/新父12、旧原生15/旧父9条，新决策2346、旧只读5865；42场景、588逐折、336近期折、168扩展折、16464日NAV、18持有对照、10邻边/图均保存。策略引擎与资金核算源码和上轮原字节一致，81个严格ROC阈值/实际持仓/未来后缀合成检查通过后绑定、预登记，金融完整评估一次，未重跑已完成配置。freeze stdout沿用volcaps旧标签，accounts_check stdout沿用0/6/0/0旧标签；实际plan/spec/轴与图为BTC_ROC_LOOKBACK，账户检查断言及JSON均为全0，两处旧文字与真实字段对照见stdout_label_notes.json，不把stdout标签当结果证据。

原账户：SMA/single08:30→10:30、L4/FEWM10:10→12:10；日事件{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、新成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、资金费记录{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}，新鲜完整窗口查询BTC/ETH均为空。原现金/数量/入场价/desired/本金/规则保持；全部历史资金费、日事件唯一键与NAV前缀核验，三永续先前08各记一次而本窗不重复，SMA现货无资金费。

SMA65/对称1%/Float/本金1500:500/raw75:25原样，追加120闭合分钟，累计63989分钟/64035点；完整67日权威research/experiments/20261115T075947Z/forward_inputs.json.gz、旧66/65前缀只读，本轮输入为minute数组，无新日线捕获或指标决策。原组合3倍累计净-7.468957812%，负收益完整保留；各账户未成熟180日，旧延迟shadow不冒充十策略真实报价模拟。

本轮SMA/single08:30→10:30、L4/FEWM10:10→12:10，完整窗口实际资金费查询均为空；日决策、成交、资金费记录全0，各自现金/持仓/入场价/desired/本金/冻结规则保持，原NAV完整前缀逐点核验。三永续Nov15_08此前已各记一次，本窗不重复。下轮SMA/single10:30→12:30、12:31后闭合；L4/FEWM12:10→14:10、14:11后闭合，需新查实际结算。下一原日事件仍Nov16_00:01；67日权威仍075947/forward_inputs，当前minute数组不冒充日线，保留旧66/65前缀；新L28/L30研究不采纳到原账户，旧延迟shadow与十策略真实报价分开。

午夜源原捕获UTC2026-11-15T08:17:46.618283Z、08源原捕获UTC2026-11-15T14:06:10.992989Z与原包哈希保持；本轮新完整窗口查询UTC2026-11-15T18:05:17.246840Z返回空列表，独立回执保留，不把旧捕获UTC重标或旧08再入账。

有包公共GET 18次，均保存URL/捕获时界/body/gzipSHA；上述行情/结算捕获观察到传输失败0次，本轮官方文档两次读取成功，实际工程读错路径/元数据脚本语法错误及修复另见失败事实。FEWM与cached metadata/time精确去重，SMA内部未分包重试数0仅按原stderr/命令时界披露，失败体、资产/URL和精确尝试UTC若原执行器未记录则不编造。

复现：cwd=/home/desktop/Documents/Codex/EquiTide，解释器/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B。review/launch.py bootstrap.py review/preflight.py；review/prepare.py review/setup.py；review/execute.py freeze units bind reserve_0 evaluate audit exports finish_0 research_check；diagnostics/historical_aliases、实际view_image后visual_review；原账户midnight_archive l4h02 fewm candidate forward accounts_check；account_continuity/complete_transport_audit/validate_sources；journal sources_check gates feed collect final_checks、staged_whitespace、seal/publish。真实命令/UTC/退出码/stdout保留；不重复运行源变换、已完成金融或账户窗口。forward --reproduce仅只读核验。

391日历史与多重选择偏差未消除，无DSR/PBO显著性结论，正收益不代表稳定实盘盈利。本轮已读[Binance官方市场/资金费文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)和[官方公共数据README](https://github.com/binance/binance-public-data/blob/master/README.md)，实际原包/输入SHA是复现依据。

实际失败/阻碍：{"round": "20261115T180155Z", "facts": [{"type": "context_read_wrong_bootstrap_path", "native_chunks": ["217977", "573bb8"], "attempted_path": "research/experiments/20261115T160124Z/review/bootstrap.py", "actual_path": "research/experiments/20261115T160124Z/bootstrap.py", "resolved": true, "recovery": "Actual root bootstrap source fully read in native chunk e9d15e; no model/account computation or reserve involved."}, {"type": "completion_metadata_writer_syntax_error_before_execution", "native_start_chunk": "840b4b", "error": "SyntaxError: unterminated string literal", "resolved": true, "recovery": "Re-executed corrected metadata-only writer before binding or market evaluation; first Python block parsed nothing and made no writes. Independent prepare/setup stages in that shell did complete exit0 and were not repeated.", "market_or_account_reruns": 0}]}。保留所有正/负/淘汰/失败、原账户完整账本/冻结规则/登记、原包、哈希和下轮状态；只清理可重建缓存，大行情忽略。锁内snapshot只读已有账户/报告，不新回测或产生模拟成交，不部署或创建定时任务。真实commit/push、完整远端树/blob和解锁后检查见.git/automation_proofs回执。
