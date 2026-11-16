本轮完成6个新金融配置：ETH资金费预算波动窗口VW7/9两个原生组件，交叉已有BTC主入场H3%/3.25%银行形成四父组合；VW8中心只读，ETH R=.01/M4与其余规则固定。18条新1/2/3倍成本场景，8旧配置/24场景只读。历史通过4个（父4、组件0），淘汰2个，失败项全部保留。12原账户观察独立reserve/finish，partial rejected不取消长期计划。

事前假设：不同已完成日波动窗口可能改变允许支付的资金费预算，调整入场筛选时机。固定VW=[7,8,9]×只读BTCH=[.03,.0325]，VW8已有实际结果只读；代表VW7/BTCH.03在看结果前固定，不事后扩批、换代表或改门槛。W轴归ETH预算窗口，K轴归BTC主阈值；单币组件只沿自身适用轴。

完整读取36920登记事件/18321ID、445份结论、11389个排除观察的规范研究定义（非独立试验数），task/README/三技能、checks/*oos.py与freqtrade原ZIP。初始16项缺实际结果0，legacy/false与所有负结果保持；保护83814旧文件和paper10账本/报价。固定ETH查询仅找到VW8/10/12，7/9新具体参数预登记成功后才实际计算。

ETH本金15000/固定名义4000，long-only L5/H.02/E.0075、有限归一化EWMS16 beta15/17、D3严格K.0075，V6已完成样本logvol上限.05625。仅新/反手要求最近4笔实际已实现有符号资金费中位数，年龄1–36h且available≤signal；允许支出min(.0002,.01×过去VW已完成日无偏样本logvol×最近合格已知实际结算间隔小时/24)。资金费预算相等通过，缺失阻新仓，已有q与正常退出不改。VW7/9只改变预算窗口；入场风险V6与执行冲击V20均保持。新spec明确E.0075并修正旧持仓文案E.005笔误，文案修正不算新配置，旧spec/report/状态原字节保留。

BTC两银行只读：本金3750/名义1000，L29主ROC严格>.03或.0325多、低于其负值空；入场优先，带内多仅ROC>−.005、空仅ROC<.005持有，相等退出。新/反手再要求V10 samplelogvol≤.0275及5日同向ROC严格>.0025，同向旧q保留。新父直接复用这些原规模净值，未生成新BTC曲线。

父本金18750/raw[1,1]相加BTC3750和ETH15000原银行美元NAV，20/80只是初始本金占比，权重不归一化。无缩放、转账、再平衡、父订单或跨保证金，完整事件轴对齐后重算组合净值和整体DD，不能平均单策略收益/Sharpe/DD。

Walk-forward已执行：2025-10-19T00:01Z→2026-11-14T00:01Z，共391日、33日背景；每币610562分钟bar、10176小时mark、1273实际资金费，8个Parquet SHA/单位/闭合可得时间核验。13完整30日折+1日尾，跨折继承现金/q，全期终止才按成本平仓，整体DD来自全事件NAV。近40日8×5与扩展21日5+5+5+6逐折保存，1日尾Sharpe=None。固定规则不拟合/无标签，只用完成前缀；OOS机器字段指复用开发历史，不能称未触碰最终集或独立未来。

敏感性已执行：VW7/8/9×BTC H3%/3.25%六父格，ETH组件仅沿VW、BTC仅沿H。保存所有净收益、整体DD、Sharpe、Calmar、近期折、10邻边、跳变启发标记与并列最优边界。局部3倍净正与严格近期合格比例各≥60%；小3×2条件邻域和两档BTC不能证明宽平台；旧参考状态不被当前邻域改写。

成本已执行：每边费5bp+半价差1bp+滑点2bp+0.5×过去20完整日samplelogvol×sqrt(abs(q)×真实OPEN/过去20日quoteADV)，不利tick、实际LOT/minnotional，参与率≤.1%、费后1倍抵押、闭合小时high/low的1%维持保证金代理。执行成本和负资金费1/2/3倍，收入不放大。线性永续无现货借币需求，不编造借币费；费/盘口为估计，缺历史L2/TCA、完整档位、tick强平和容量证明。

冻结门槛：全期/近期三成本净正；1倍≥10/13正完整月；近期各成本≥6/8正5日折；扩展21日各成本净正且≥3/4正折；3倍DD≤25%；两项局部比例≥60%；至少4底层平仓，1倍(毛价PnL+净资金费)/执行成本≥2.5；无拒单/负抵押/保证金代理违规、期末平仓且≥180日。任一失败即淘汰，结果保持。

|ETH预算窗口VW（日）|BTC主H|来源/状态|1x净%|2x净%|3x净%|3x整体DD%|正月/13|近期正折1/2/3|
|---:|---:|---|---:|---:|---:|---:|---:|---|
|7|0.03|新/passed|9.018677749|8.468312892|7.918129337|1.357833669|12|6/6/6|
|7|0.0325|新/passed|8.911078108|8.361409579|7.811922320|1.357833669|12|6/6/6|
|8|0.03|旧只读/passed|9.289006934|8.742458502|8.196091464|1.357833669|12|6/6/6|
|8|0.0325|旧只读/passed|9.181407294|8.635555190|8.089884447|1.357833669|12|6/6/6|
|9|0.03|新/passed|9.289006934|8.742458502|8.196091464|1.357833669|12|6/6/6|
|9|0.0325|新/passed|9.181407294|8.635555190|8.089884447|1.357833669|12|6/6/6|


事前代表VW7/BTCH.03（c2db05d50a97cfce2f7b789f70bd25da9c6cff07f87339b24999b82ad1c7cbc9）三成本净9.018677749%/8.468312892%/7.918129337%，3倍整体DD 1.357833669%，Sharpe 2.244814425，Calmar 5.429730705，passed；失败项[]。

ETH VW7组件rejected，三成本净6.715796300%/6.335001962%/5.954417571%，3倍DD 1.528984097%，正月7/13，近期正折{'1': 0, '2': 0, '3': 0}，失败项['ten_of_thirteen_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct', 'extension21_positive_all_costs', 'extension21_three_of_four_positive_folds_all_costs']。

ETH VW9组件rejected，三成本净7.053707782%/6.677683975%/6.301870230%，3倍DD 1.528984097%，正月7/13，近期正折{'1': 0, '2': 0, '3': 0}，失败项['ten_of_thirteen_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct', 'extension21_positive_all_costs', 'extension21_three_of_four_positive_folds_all_costs']。

配对旧VW8、相同BTCH0.03：新VW7的3倍净变化-0.277962127个百分点，整体DD变化+0.000000000个百分点，Sharpe -0.098136045，Calmar -0.190115423。

配对旧VW8、相同BTCH0.0325：新VW7的3倍净变化-0.277962127个百分点，整体DD变化+0.000000000个百分点，Sharpe -0.097935415，Calmar -0.190127855。

配对旧VW8、相同BTCH0.03：新VW9的3倍净变化+0.000000000个百分点，整体DD变化+0.000000000个百分点，Sharpe +0.000000000，Calmar +0.000000000。

配对旧VW8、相同BTCH0.0325：新VW9的3倍净变化+0.000000000个百分点，整体DD变化+0.000000000个百分点，Sharpe +0.000000000，Calmar +0.000000000。

本轮没有更优候选。四父通过各自历史门槛，但两个ETH单组件的完整正月、近期与扩展21日门槛失败；组合通过不能替代组件资格。VW7同BTC父净收益降低约.277962个百分点，VW9父收益未提高；整体DD均无改进，原账户不采用新参数，仍待独立未来。

6新配置全成本NAV签名6组，匹配8参考3组，匹配上轮新/只读配置路径2/6。启发abs(deltaSharpe)>2×sampleSTD(absdeltas)标记3/10，绝对变化范围[0.0, 0.12206625045664166]、STD 0.045210831；不是显著性或过拟合概率。父格净正/正Sharpe/严格近期比例1.0/1.0/1.0，不据此覆盖ETH失败。相同终值与相同完整路径分开核验，具体391日目标/持仓/成交/资金费对照见bank_path_alias_verification.json。

只读分解ETH VW7对旧8：毛价格PnL变化-49.987890000USDT，资金费变化-2.252635585，执行费变化-0.122626730，净差-52.117898855，执行数差0；同BTC父净差-0.277962127个百分点。

只读分解ETH VW9对旧8：毛价格PnL变化+0.000000000USDT，资金费变化+0.000000000，执行费变化+0.000000000，净差+0.000000000，执行数差0；同BTC父净差+0.000000000个百分点。

另只读旧BTC总波动上限组件9个/对应父18个，匹配新路径0/6；范围与本轮8参考和上一批对照分开。两个新ETH完整391日实际计算一次，未线性缩放旧NAV，也未重跑已完成配置。

独立核对新原生6/父12、旧原生15/父9成本曲线，新决策2346、旧决策5865；42场景、588逐折、336近期折、168扩展折、16464日NAV、18持有对照、10邻边/六图均保存。匹配持有3倍净-14.782911083%、整体DD 18.454766592%，现金0。货币/BTC/ETH公式与核算核心不变，仅budget_sigma的VW验证白名单及独立审计白名单扩展7/9。261个预算/等号/成熟事件/未来后缀合成检查及资产轴邻域检查均先于reserve；所有实际配置预登记后完整计算并finish。

原账户SMA/single10:30→12:30、L4/FEWM12:10→14:10；新日事件{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、资金费{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}。完整查询返回BTC/ETH均空，旧book/q/entry保持，00及08资金费和原日决策全链各一次，无重复键。

SMA完整68日SPOT权威research/experiments/20261116T080637Z/forward_inputs.json.gz及67/66/65前缀相等，仍65日/对称1%/Float、本金1500:500/raw75:25；手续费10bp+半价差1bp+滑点2bp+过去20日ADV冲击，不追溯新LOT/tick。追加120闭合分钟，无新日决策/参考/成交；累计65549分钟/65596点，三倍净-7.468957812%，负结果完整保留。原2027-03-31终止计划不改、不强平；延迟shadow不冒充十策略真实报价成交。

本轮SMA/singleNov16_10:30→12:30、L4/FEWM12:10→14:10；新查10:30→14:10完整实际结算，BTC/ETH返回空，无新增资金费、日决策或成交。旧00/08资金费和原日决策各一次。下轮SMA/single12:30→14:30、14:31后闭合；L4/FEWM14:10→16:10、16:11后闭合，跨名义16时刻但须新查真实结算时刻/费率/mark，按各自旧q入账，不能预设8小时或复制现金流。原SMA65/对称1%/Float/full68SPOT与67/66/65前缀保持，下一日决策Nov17_00:01，不采用新研究。

旧08首次捕获UTC 2026-11-16T14:13:46.299467Z 原字节保持；本轮10:30→14:10查询UTC 2026-11-16T20:15:40.763364Z 独立留档，BTC/ETH均空，不重标旧源。旧真实08:00:00.001的1794816000001ms未取整，Nov13–16全部旧源/捕获UTC/哈希保留。

有包公共GET 18次、实际传输失败0次，URL/捕获时界/body/gzipSHA保留，FEWM/cached metadata/time精确去重。SMA内部未分包重试0按实际stderr披露，不编未知UTC/失败体。

复现cwd=/home/desktop/Documents/Codex/EquiTide，既有venv python -B。launch bootstrap/preflight/configure_budget/setup_confirmation/prepare_confirmation；execute freeze units bind reserve_0 evaluate audit exports finish_0 research_check；prepare_diagnostics/configure_report；diagnostics/historical_aliases/totalrisk_history_aliases/budget_effect，实际view_image后visual_review；diagnostic_review只澄清字段标签、不改数值；midnight_archive l4h02 fewm candidate forward accounts_check；account_continuity/complete_transport_audit/validate_sources；journal sources_check gates feed collect final_checks/staged_whitespace；封存/发布助手。确切UTC、命令、退出码和原stdout在回执；已完成目录不重复reserve/evaluate或重放账户，forward --reproduce只用原包核验。

391日复用开发历史和多重选择偏差未消除，无DSR/PBO显著性结论，正收益不代表稳定实盘盈利。本轮读取[Binance官方资金费/市场文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)与[官方公共数据README](https://github.com/binance/binance-public-data/blob/master/README.md)，真实原包和输入SHA是复现依据。

实际失败/阻碍：{"round": "20261116T201210Z", "facts": [], "no_completed_model_or_account_window_replays": true}。保留全部正负、淘汰/失败、完整原账本/冻结规则/登记/哈希/原包和下轮必要状态；仅清理可重建缓存。锁内monitor只读汇总，不新回测、模拟成交、部署或增定时任务。真实commit/push/远端树及解锁后回执见.git/automation_proofs。
