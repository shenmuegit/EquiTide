本轮真实完成6个新金融配置：ETH有限EWM记忆S12/S20两个原生组件、与只读BTC V10/V14银行组成四个父组合，共18条1/2/3倍成本场景。父组合历史通过4个，原生组件通过0个、淘汰2个；8个既有实际配置/24成本场景只读复用。12项原冻结账户窗口实际观察各自预登记和finish；partial rejected仅表示尚未成熟180日，长期计划继续。

事前假设：相同ETH反转信号的趋势入场门改用更短S12或更长S20的有限归一化EWM，能否改善费用后收益与时序稳健性。固定资金费中位数M4、预算R=.00875；与BTC实际银行入场波动率V10/V14组成3×2面，S16中心为旧结果。S20/BTCV14代表在结果前指定，较长记忆可能保留短回撤中的正斜率；S12作为较短滞后对照。未事后扩网格或换代表。完整核心参数查重不依赖名称、family或continuous_days标记，确认本轮S12/S20尚无实际结果。

ETH本金15000、固定入场名义4000、long-only。用已完成收盘计算ROC L5，严格r>2%产生空目标、r<−2%产生多目标；带内实际多头仅r<0.75%保留、空头仅r>−0.75%保留，否则0。趋势均值level=Σ(beta^j×close[t−j])/Σbeta^j，j=0…S−1，beta=(S−1)/(S+1)；与向前回溯D3的同权均值比值减1，严格斜率>K=.0075给多门、<−K给空门。仅新/反手入场要求目标与趋势门一致；V6样本日log波动率≤.05625，最后负目标归零。已持同向实际q保持，正常快退出不变。S12/16/20分别beta11/13、15/17、19/21，四个S/window/decay字段一致更新。

资金费门固定为最近4笔实际已结算有符号费率中位数，信号前1–36小时且source_available≤signal才合格；偶数取中间两数平均，缺4笔阻止新入场。上限min(.0002,.00875×过去V8日samplelogvol×最新合格记录与其前笔实际结算间隔小时/24)，比较max(desired×median,0)，相等可过，持有同向不因门而退出；1小时延迟为保守可得性假设。只用过去闭合前缀，执行是信号后下一00:01真实OPEN。新参数从原现金完整计算391日，prior370指纹仅谱系，不复用新参数的货币前缀。旧E.005描述错误只在新spec文字同步为机器一直使用的E.0075，不算新颖性，旧字节保留。

BTC原生银行只读：本金3750/固定名义1000，ROC L29/H3%/退出E0.5%，入场samplelogvol窗口V10或14、cap3%。严格ROC>3%多、<−3%空；带内实际多头仅ROC>−.005、空头仅ROC<.005保留，相等退出。入场过滤只适用新/反手，保持原q。父组合本金18750/raw[1,1]相加两个原规模完整银行的美元NAV；20/80仅初始本金占比，不归一化、不缩放、不转账/再平衡/父订单/跨保证金；对齐全部事件时间轴重算连续NAV和整体DD。

完整读取登记35788事件/17761ID、425份结论、三技能/task/README/OOS与freqtrade原ZIP。初始16项缺实际历史结果为0，旧false/legacy行与原负结果保留。基于最新main及01UTC paper10提交；上轮真实push/远端/解锁后证明已核对，当前无旧reserved。保护77003份旧文件，paper10冻结计划、账本和已有报价观察原字节不改。

Walk-forward：研究区间2025-10-19T00:01Z→2026-11-14T00:01Z，391日加33日背景；每币610562分钟bar、10176小时mark、1273实际资金费，8份Parquet数据SHA、闭合/单位/可得时间与连续性实际检查。13完整30日折+1日尾折，近40日8×5与扩展21日5+5+5+6逐折保存；现金/持仓跨折连续，仅全期末计成本平仓，整体DD由全事件NAV计算。固定规则无拟合或标签，purge/embargo无标签用途；33日特征背景和未来后缀/资金费成熟边界独立核验。尾日Sharpe=None，不计完整正月门槛。该391日反复用于开发，虽然当前已Nov15，本轮未加新完整日，不能称未触碰最终留出或独立未来。

Sensitivity：预定ETH S=[12,16,20]×BTC V=[10,14]六格全部列出；ETH原生只沿S、BTC原生只沿V计算适用邻域。净收益、整体DD、Sharpe、Calmar、近期正折、所有并列最佳边界与10条相邻变化保留。局部3倍净正与严格近期比例各≥60%。小条件邻域和仅两档BTC参数不证明广泛平台；边界值只作诊断，不依据本轮OOS追加参数。

Costs：手续费5bp+半价差1bp+滑点2bp+0.5×过去20日samplelogvol×sqrt(abs(q)×真实OPEN/过去20日quoteADV)，不利tick；执行成本和负资金费1/2/3倍，收入不放大。实际LOT/tick/minnotional、参与率≤0.1%、费后1倍抵押及闭合小时high/low的1%维持保证金代理检查。线性永续不借现货，不编造借币费。冻结费率/价差为估计，缺历史L2/TCA、完整档位、tick强平和真实容量证明。逐场景成交数、各成本分项/占比与同期匹配持有、现金0对照见exports。

预设通过条件：三成本全期/近期净正；1倍至少10/13正完整月；各成本近期至少6/8正5日折；扩展21日净正且至少3/4正折；3倍DD≤25%；适用局部正收益与严格近期比例≥60%；至少4底层平仓；1倍(毛价格PnL+净资金费)/执行成本≥2.5；无拒单、负抵押或保证金代理违规，期末平仓且≥180日。失败即rejected，保留全部真实结果。

|ETH记忆S|BTC波动V|来源/状态|1x净%|2x净%|3x净%|3x整体DD%|正月/13|近期正折1/2/3|
|---:|---:|---|---:|---:|---:|---:|---:|---|
|12|10|新/passed|7.724456667|7.224817769|6.725363754|1.362719676|11|6/6/6|
|12|14|新/passed|7.780705010|7.280881116|6.781242121|1.361994711|11|6/6/6|
|16|10|旧只读/passed|9.000028418|8.422242505|7.844642170|1.362719676|12|6/6/6|
|16|14|旧只读/passed|9.056276762|8.478305852|7.900520536|1.361994711|12|6/6/6|
|20|10|新/passed|6.573509054|5.983960545|5.394595347|3.906288211|11|6/6/6|
|20|14|新/passed|6.629757398|6.040023892|5.450473713|3.906288211|11|6/6/6|


事前代表S20/BTCV14（20bce9b4c82e9dc7d45f6399769d9471d950f9aa1ad3725724c7e7a3a19dc71f）三成本净6.629757398%/6.040023892%/5.450473713%，3倍整体DD3.906288211%，Sharpe1.297364050，Calmar1.300209100，状态passed、失败项[]。

ETH S12组件rejected：三成本全期净5.536237856%/5.262695755%/4.989362848%，3倍DD1.528984097%，正月5/13、近期正折{'1': 0, '2': 0, '3': 0}，近期40日净-0.020688454%/-0.041467898%/-0.062338867%；扩展21日三成本净均0，失败项['ten_of_thirteen_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct', 'extension21_positive_all_costs', 'extension21_three_of_four_positive_folds_all_costs']。

ETH S20组件rejected：三成本全期净4.097553341%/3.711624225%/3.325902339%，3倍DD3.470060169%，正月6/13、近期正折{'1': 0, '2': 0, '3': 0}，近期40日净-0.020974320%/-0.042087815%/-0.063341835%；扩展21日三成本净均0，失败项['ten_of_thirteen_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct', 'extension21_positive_all_costs', 'extension21_three_of_four_positive_folds_all_costs']。

两个ETH组件全期虽为正收益，但S12仅5/13、S20仅6/13正完整月，近期都是0/8正折且40日各成本为负，扩展21日零PnL，均淘汰。四父组合达到历史门槛，各11/13正月和近期6/8；全期净收益/Sharpe/Calmar均低于相同BTC银行的旧S16。S12整体DD与旧S16相同；S20父组合DD约3.906288%，高于S16约1.362%，风险恶化。S20近期组合收益略高，不能抵销全期收益和回撤劣化。父近期及扩展利润仍由BTC贡献，不能用父通过掩盖ETH组件失败，本轮不提供新规则采纳理由。

六新定义内部不同三成本NAV签名6条，匹配八个旧预登记参考0条；上轮实际新/只读配置匹配0/6。新父3倍收益低于对应S16为4个、相同0个。ETH扩展21日PnL全零=True，18个父成本场景的BTC/ETH全期及扩展PnL加总守恒独立核验。不同路径仍非独立市场样本。

abs(deltaSharpe)>2×sampleSTD(absdeltas)原始启发式标记3/10，全部保存，绝对相邻Sharpe变化范围[0.013016987655993129, 1.076809801948646]、样本STD0.435785125。这不是显著性或过拟合概率。S16为本邻域全期净收益/Sharpe/Calmar内部峰，S20整体DD明显升高，不能称三个ETH参数组成宽稳健平台；各指标所有并列最优见sensitivity_metric_boundaries。

匹配持有3倍净-14.782911083%、DD18.454766592%；父网格3倍净正、正Sharpe、严格近期比例分别1.000000/1.000000/1.000000。旧配置原status不因当前邻域诊断而改写。

独立审计新原生6条/新父12条、旧原生15条/旧父9条场景，新策略决策2346、旧只读决策5865；42成本场景、588逐折、336近期折、168扩展折、16464日NAV、18持有对照、10相邻边和3×2热图留档。引擎函数AST与核算核心字节未变，合成严格边界/未来后缀/资金费成熟、真实时间线和完整货币核算均实际通过。每一实际参数配置先reserve后计算并独立finish，完整金融评估只运行一次。

原账户窗口：SMA/single Nov14_18:30→20:30Z，L4/FEWM20:10→22:10Z，日事件{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、资金费记录{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}全为0。18本永续账簿cash/q/entry等原样，全部NAV前缀、历史资金费/日事件唯一键及Nov14_16各账户只记一次核验。只增加闭合分钟估值/风险点，SMA累计63149分钟/63194点，原65/对称1%/Float/raw75:25/本金1500:500不变。延迟shadow不冒充十策略实时行情模拟，所有原账户未成熟180日。

原SMA组合3倍累计净收益-7.468957812%，负收益完整保留，不用当前研究组合的历史正收益覆盖原账户表现。

本轮SMA/single为Nov14_18:30→20:30Z，L4/FEWM为20:10→22:10Z，仅闭合分钟估值与风险点，0资金费/0日事件/0成交，18账簿原cash/q/entry保持。下轮SMA/single20:30→22:30，22:31后参考闭合；L4/FEWM22:10→Nov15_00:10，00:11后参考闭合，已跨Nov15_00:01原日决策，须使用原冻结日决策核心与实际新增闭合日背景，先查询完整窗口真实资金费，不能继续假设全部mark-only。SMA下一窗口尚未跨日，完整66日权威仍035058/forward_inputs；当SMA后续实际窗口覆盖Nov15_00:01，才补充完整67日背景并用原日适配器，禁止以当前minute包冒充完整日背景。三永续Nov14_16各已记一次，不重复；不硬编码名义八小时，不采纳研究S12/S20，不强平或重开账户。旧blocked记录和paper10冻结账户/本金/持仓/账本保留。

旧08捕获UTC2026-11-14T09:56:41.855564Z、旧16捕获UTC2026-11-14T17:58:56.177141Z保持，本轮窗口查询UTC2026-11-15T02:06:00.919277Z字段为空，不重标旧捕获为新响应。SMA完整66日权威research/experiments/20261114T035058Z/forward_inputs.json.gz原65日数组前缀一致，当前输入仅分钟，后续跨原日决策才补实际闭合日。

公共GET独立保存18次，真实传输失败0次，URL/UTC/raw/body/gzipSHA与真实失败回执保留。FEWM同窗只复用公开行情、candidate仅复用metadata/time，cashflow按各自q独立；原SMA内部curl未另存体/精确UTC的重试仅按stderr披露，不补造。

研究391日反复开发和多重选择偏差未消除，无DSR/PBO显著性结论；新路径或正收益回测不代表稳定实盘盈利，当前研究不改任何冻结账户。[Binance官方市场/资金费文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)和[官方公共数据README](https://github.com/binance/binance-public-data/blob/master/README.md)本轮已核对，原响应与data_manifest/hash是复现依据。

复现cwd=/home/desktop/Documents/Codex/EquiTide；解释器/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B。review/launch.py依次bootstrap.py、review/preflight.py、review/prepare.py和review/setup.py；review/execute.py依次freeze units bind reserve_0 evaluate audit exports finish_0 research_check；只读diagnostics/historical_aliases；原账户midnight_archive l4h02 fewm candidate forward accounts_check；实际view_image后visual_review/account_continuity/complete_transport_audit/validate_sources；再journal sources_check gates feed collect final_checks、staged_whitespace、seal/publish。这些是本轮真实命令顺序，完整命令/cwd/UTC/退出码/log留档；prepare/setup为从上轮模板生成当前冻结源的首次预处理，已变换源不可再次原地执行。已有实际ID禁止精确重跑或覆盖归档；forward --reproduce仅本轮首次完成后只读核验，不新增窗口。

实际阻碍与失败：{"round": "20261115T015614Z", "facts": []}。全部正/负/淘汰/失败结果、账户账本、冻结规则、完整登记、必要原包与哈希/下轮状态保留，可重建中间缓存清理，大行情忽略。6金融+12实际观察/36事件独立归档；锁内snapshot只读汇总已有账户/报告，不新增回测、成交、部署或定时任务。最终commit/push与完整远端树/blob/解锁后证明见.git/automation_proofs实际回执。
