本轮完成16个真实配置、48成本场景：4个变名义金额的策略银行、1个新匹配持有银行、8个策略父组合、3个新匹配持有父组合。逐项先reserve后计算并finish，4个新策略组合通过历史门槛、12个真实配置淘汰（含4个策略组合）；全部正收益、负收益持有及负折保留。另有14个精确旧结果、21条原生成本净值只读复用，未缩放旧NAV。

新发现：名义金额提高并非统一改善。最高收益格NB1250/NE4500三倍净14.546291%、整体DD2.414406%，仍因近期三倍仅5/8盈利折及局部覆盖50%被淘汰。NB750与NE3500/4000/4500、NB1000与NE4500通过历史门槛，仍待独立前向；这是已反复使用的开发历史，不代表稳定实盘盈利。

完整读取33464事件/16610ID、10879研究定义、390份既往结论，以及任务/三技能/README/OOS检查/原始freqtradeZIP。初始16项已有11正式补测和5原始ZIP实际证据，旧false及历史保持，不将paper失败窗口当历史缺测。按完整参数/市场/日历/父图原权重查重，本轮8个新策略组合之外，精确旧银行/持有组合优先复用；未因同族排除，也未用名称/等价数字伪造新配置。27个金融/账户根源首reserve前绑定，真实新N执行器、独立政策/钱账审计及原SMA日线适配器保持哈希。

预设两轴NB={750,1000,1250}×NE={3500,4000,4500} USDT，代表1000/4000事前指定且已有真实结果，本轮只读。BTC固定L29、严格H2.75%带E1%缓冲动量；ETH固定L5/H2%反转/E0.75%、有限归一化EWM S16 beta15/17、D3斜率严格K0.75%，新开/反手门控，价格V6样本logvol≤5.625%；资金费M4 signed成熟真实费率中位数、年龄1–36h、available≤signal，预算min(.0002,.00875*过去VW10样本logvol*最新成熟真实结算间隔小时/24)，偶数取中间均值。同向保留实际q，缺字段阻新开，保守1h可用是建模假设而非历史到达证明。

资金与敞口：银行本金BTC3750/ETH15000、总18750固定，raw[1,1]加完整独立银行；20/80只是本金份额，不归一化、不二次加权、不转账/再平衡/父订单/跨保证金。NB/NE是实际入场名义预算，总4250–5750约总本金22.67%–30.67%，不是资本权重。改变N必须重新执行q=floor(N/前完整日close/LOT)*LOT、次日UTC00:01原生OPEN不利tick、真实费用/平方根冲击/资金费/抵押；不线性拉伸旧曲线。每个格都对应同C、同N、同日历、同原权重和成本的实际常量做多银行控制；同初始预算不等于全程方向与风险暴露相同。

真实输入来自固定版本Binance线性永续分钟、闭合mark小时、实际资金费及LOT/tick元数据，文件SHA与源报告/档案哈希见plan.json和data_manifest.json。33完整日预热，连续OOS2025-10-19 UTC00:01→2026-10-24 UTC00:01共370日；12×30完整日折加10日尾，近期40日继承day330真实cash/q分8×5日折，折间不重开。没有模型训练、标签或预处理拟合，purge/embargo不适用。该历史已多次研究，参数选择/多重试验偏差存在，不是未触碰最终测试集或独立未来。

1/2/3倍成本实际执行：每边fee5bp、半价差1bp、滑点2bp，impact=.5*过去20完整日样本logvol*sqrt(absq*真实OPEN/过去20完整日quoteADV)，不利tick；执行费用和真实资金费支出压力倍增，正资金费收入不放大。费用/价差是冻结估计，不是历史盘口或实际用户费率证明。线性永续无现货借币，不虚构借币费；原生LOT/tick/minnotional、≤0.1%参与率、费后1倍抵押和闭合小时不利high/low的1%维护代理逐曲线核验，无L2/TCA/完整历史风险档位/tick强平或容量证明。

冻结历史门槛：各成本全期/近期净正、1倍≥9/12盈利完整月、近期各成本≥6/8盈利5日折、3倍完整DD≤25%、局部3倍净正和严格近期比例≥60%、底层≥4平仓、(毛价格PnL+净资金费)/1倍执行成本≥2.5，无订单/现金/保证金代理违规、终点成本平仓、≥180日。持有控制不可作为候选晋级。新银行只变化自己的N（1个适用轴），父项联合NB/NE两轴；既定信号政策不搜索。

|NB|NE|新/旧|1x净%|2x净%|3x净%|3x整体DD%|Sharpe3|Calmar3|近期正折1/2/3|局部严格近期|状态/失败|
|---:|---:|---|---:|---:|---:|---:|---:|---:|---|---:|---|
|750|3500|新实际|12.398819|11.625613|10.852228|1.968794|2.587453519574476|5.433781460144587|6/6/6|0.75|passed:|
|750|4000|新实际|13.998694|13.146465|12.294218|2.248083|2.6267172858183305|5.390548239677426|6/6/6|0.8333333333333334|passed:|
|750|4500|新实际|15.599624|14.668241|13.737166|2.521183|2.6558024841439387|5.3702942867550485|6/6/6|1.0|passed:|
|1000|3500|新实际|13.079357|12.224796|11.370063|1.933859|2.507477087124386|5.795720827998622|6/6/5|0.5|rejected:recent40_six_of_eight_positive5d_all_costs,local_recent6of8_allcost_gte60pct|
|1000|4000|旧只读|14.679231|13.745648|12.812053|2.159682|2.562285366706179|5.847353193055244|6/6/6|0.5555555555555556|passed:|
|1000|4500|新实际|16.280162|15.267424|14.255001|2.432986|2.6036401058964143|5.774561893232626|6/6/6|0.6666666666666666|passed:|
|1250|3500|新实际|13.535577|12.598574|11.661353|2.184360|2.3868188689319405|5.262429779297029|5/5/5|0.25|rejected:recent40_six_of_eight_positive5d_all_costs,local_recent6of8_allcost_gte60pct|
|1250|4000|新实际|15.135452|14.119426|13.103343|2.300377|2.457881628375042|5.614429158423133|5/5/5|0.3333333333333333|rejected:recent40_six_of_eight_positive5d_all_costs,local_recent6of8_allcost_gte60pct|
|1250|4500|新实际|16.736382|15.641201|14.546291|2.414406|2.5130741646060013|5.937800285787616|6/6/5|0.5|rejected:recent40_six_of_eight_positive5d_all_costs,local_recent6of8_allcost_gte60pct|


|其余新配置|范围|1x净%|2x净%|3x净%|3x整体DD%|Sharpe3|Calmar3|状态/失败|
|---|---|---:|---:|---:|---:|---:|---:|---|
|sizingrisk370_BTC_N750|component|5.973247|4.857728|3.742230|5.186764|0.5371919139032706|0.7115684311910211|rejected:nine_of_twelve_positive_complete30d_1x_folds,recent40_six_of_eight_positive5d_all_costs,local_recent6of8_allcost_gte60pct|
|sizingrisk370_BTC_N1250|component|11.657038|9.722530|7.787856|8.500783|0.6549003081382984|0.9032901970615153|rejected:nine_of_twelve_positive_complete30d_1x_folds,recent40_six_of_eight_positive5d_all_costs,local_recent6of8_allcost_gte60pct|
|sizingrisk370_ETH_N3500|component|14.005212|13.317585|12.629727|2.626306|2.7933181987594122|4.740060836652798|rejected:recent40_six_of_eight_positive5d_all_costs,local_recent6of8_allcost_gte60pct|
|sizingrisk370_ETH_N4500|component|18.006219|17.120869|16.235900|3.283719|2.7950542874286497|4.87246902883481|rejected:recent40_six_of_eight_positive5d_all_costs,local_recent6of8_allcost_gte60pct|
|sizingrisk370_hold_ETH_N3500|benchmark_component|-9.475582|-10.103750|-10.731921|17.011033|-1.1032592093815834|-0.6228232204062163|rejected:not_a_benchmark_control,positive_all_costs,nine_of_twelve_positive_complete30d_1x_folds,recent40_positive_all_costs,recent40_six_of_eight_positive5d_all_costs,local_positive3_gte60pct,local_recent6of8_allcost_gte60pct,four_underlying_native_closes1,gross_plus_funding_to_cost1_gte2_5|
|sizingrisk370_hold_parent_BTC750_ETH3500|benchmark|-8.660496|-9.296396|-9.932299|15.907331|-1.1056266712989724|-0.616375342854223|rejected:not_a_benchmark_control,positive_all_costs,nine_of_twelve_positive_complete30d_1x_folds,recent40_positive_all_costs,recent40_six_of_eight_positive5d_all_costs,local_positive3_gte60pct,local_recent6of8_allcost_gte60pct,four_underlying_native_closes1,gross_plus_funding_to_cost1_gte2_5|
|sizingrisk370_hold_parent_BTC1000_ETH3500|benchmark|-8.969081|-9.643085|-10.317097|16.546018|-1.100389119864498|-0.6155579686484425|rejected:not_a_benchmark_control,positive_all_costs,nine_of_twelve_positive_complete30d_1x_folds,recent40_positive_all_costs,recent40_six_of_eight_positive5d_all_costs,local_positive3_gte60pct,local_recent6of8_allcost_gte60pct,four_underlying_native_closes1,gross_plus_funding_to_cost1_gte2_5|
|sizingrisk370_hold_parent_BTC1250_ETH3500|benchmark|-9.277662|-9.989777|-10.701895|17.184189|-1.094930506273587|-0.6148209944972128|rejected:not_a_benchmark_control,positive_all_costs,nine_of_twelve_positive_complete30d_1x_folds,recent40_positive_all_costs,recent40_six_of_eight_positive5d_all_costs,local_positive3_gte60pct,local_recent6of8_allcost_gte60pct,four_underlying_native_closes1,gross_plus_funding_to_cost1_gte2_5|


旧代表1000/4000（9db66bc2d8a80a105afc874329b8dd8c3ae29fede855047413348c6c4560568d）三倍净12.812053352%、DD2.159681661%，本轮不重跑或重登记。其旧canonical passed保持；本轮N邻域严格近期覆盖率为5/9=0.555555556，低于60%，不能声称通过本轮局部鲁棒性复核。新诊断与旧状态分开见representative_current_grid_diagnostic.json，不能回写旧报告或将旧状态当本轮全网格平台。

敏感性：全9格三倍净收益/Sharpe均正，但严格近期条件只5/9满足，整体低于60%目标；新8个策略父项只有4个通过全部门槛。NB750一带局部严格近期覆盖75%–100%，较高BTC敞口部分近期折在3倍成本翻负。描述性最高收益在边界且被淘汰，不事后换代表、加格或改变失败标准。所有变体的净收益/DD/Sharpe/Calmar、原生1轴和父项2轴邻域、36个相邻成本变化、624逐折及384近期折均保存，负折不删；2std断崖仅描述诊断。

同C/N匹配持有每格全3成本合计27项比较保留，现金0%；9个控制全套来源、复用或新算状态见all_current_benchmark_grid。新增3个NE3500持有父项三倍净收益分别−9.932299%、−10.317097%、−10.701895%，全部真实负收益留档；旧NE4000/4500等精确控制只读。不能以固定一条不同N持有曲线冒充全网格匹配对照。

独立审计新原生15条、新父项33条及复用原生21条成本曲线，5550个新因果政策决策、39960条资金费、702笔底层历史成交、966指标及274356保证金代理检查，0拒单。Fraction/Horner政策、Decimal真实N/LOT/成本/资金费/cash、全NAV/逐折/近期独立重建，不调用策略simulate/decide/trade。36个实际执行器合成N/LOT/成本例通过；4个刻意固定错N、未来OPEN定仓、线性冲击、重复资本加权变体实际退出1，均早于绑定/reserve，无真实市场RED。报告SHA256=3535a86e2a352afb3c6be79840575ae5de48b8acdc9ccc73529d3a5f432ee1b5。

完整三成本NAV别名比对：同期间/同本金/同币种或父项口径下，16新定义命中旧完整路径1项，其中候选父项0项。参数/金额不同不保证经济路径独立，未匹配格式不足以证明绝对唯一；与试验计数一起保留，不称独立显著性。

原账户：SMA现货与single各续Nov11_22:30→Nov12_00:30；L4/FEWM续Nov12_00:10→02:10只mark/risk。SMA实际新取截至Nov12_00的65个闭合SPOT日与121分钟（含1重叠），64个旧日线完整字段逐一相等；首reserve前已预取并绑定，保留真实请求UTC/四个原始响应，新上下文不是分钟数组替代品。按原Float持仓/1%对称规则计算BTC/ETH各1个日决策（成本分场景共6），0新成交；原现货fee10bp/价差/滑点/volumeimpact保持，不套用研究永续fee5bp或LOT/tick。新全65日权威为本轮forward_inputs.json.gz（每资产1d/1m字典），不得继续把032206旧截止作为最新。

single以自己的原q/cash记Nov12_00真实资金费6行并做原冻结日决策6个，0新成交；L4/FEWM本窗0资金费/0日决策/0成交，不重复已记入的午夜事件。三条完整永续链全部Nov12_00及00:01日决策每资产/成本恰好一次，18个book独立精确对账。公共资金费源原检索UTC 2026-11-12T01:36:58.569286Z、actual fundingTime(ms)=1794441600000 保持，BTC/ETH费率与mark不从别的账户现金流借用。本轮没有新取该旧公共字段的GET，不称新的资金费来源。

SMA完整NAV前缀58991→59112，各9成本场景独立核验。

single完整NAV前缀23474→23601，各9成本场景独立核验。

L4完整NAV前缀16216→16338，各9成本场景独立核验。

FEWM完整NAV前缀10324→10446，各9成本场景独立核验。

SMA三倍累计−7.468958%、cashflat，原1500/500本金及2027-03-31终止计划保持；新日决策不取消长期计划。只生成一个新观察结果；原daily适配器的finish和verify另执行2次只读精确重放，用同一保存输入、不再HTTP或生成新登记/观察结果。全部原账户仍为延迟shadow、非paper10实时公开报价模拟，180日/六完整折尚未成熟，不采用本轮N或任何研究passed策略。

字段定义本轮核对[Binance现货市场数据](https://developers.binance.com/en/docs/catalog/core-trading-spot-trading/api/rest-api/market)与[线性永续市场数据](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)官方文档，访问UTC Nov12；实际获取晚于参考执行时刻，明确延迟历史重建，不证明实时成交或历史到达时延。

下一窗SMA/single2026-11-12T00:30:00Z→2026-11-12T02:30:00Z，L4/FEWM2026-11-12T02:10:00Z→2026-11-12T04:10:00Z全部只mark/risk。SMA需改用既有mark-only模板012923（同时更新PREV），不能原样重用本轮要求1次日事件的daily脚本；保留本轮新65日字典上下文及Float状态。下一日决策Nov13_00:01、下一资金费名义时点Nov12_08:00，均不可提前或重复午夜；L4/FEWM下一04:10参考必须等04:11闭合后才算，预算内等待或如实blocked。

下轮研究仅未执行提案：UNEXECUTED: Saveall16N/holdresultsandall9strategycells. 4of8newparentshistoricallypass;highestreturn1250/4500rejectedonrecent5of8andlocal.5. NB750bandmorelocallyrobust butthis isdescriptiveknownhistory,notposthoc optimum. Old1000/4000canonicalstatuspreserved;currentnewN-neighborhood5/9below.6isadifferentdiagnostic,notrecertification. Do not densifyNaxesafterseeingOOSoradoptNintononeof4originalaccounts. Nextonebatchrequiresfreshfullregistry/semanticqueryandpredeclarednewhypothesis/laterdata;independentfuturestillunproven. No extraconfig/reserve/calculationthisround.

监控生成并原生检查通过，10454研究行、旧10438完整字典保持，paper10=10账户/338观察；只读已有报告，无新回测/模拟成交/部署/任务。账户公共HTTP实际失败1次后有限重试恢复，失败原始响应与stderr保存；SPOT预取4次GET均成功，金融/观察结果没有重复创建。

保留所有实际成功/淘汰/负收益、完整账本/冻结规则/登记、数据/代码哈希、原始响应、原生argv/cwd/UTC/退出码、复现及下轮状态；本轮无可重建npy/tmp/pycache残留。main提交push后另核验ref、全tree、必要blob SHA和完整三账户链，再原生释放锁；实际终态保存在.git/automation_proofs/20261112T033054Z.json。
