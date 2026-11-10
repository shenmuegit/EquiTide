本轮完成9个新ETH组件和9个新父组合的54个成本场景；6/9父组合历史通过，3/9父组合及9/9ETH组件淘汰。M4、R=0.0075/0.01两项三倍成本净收益14.068797%、连续整体回撤3.082168%，较同资本旧无过滤对照收益高0.312647个百分点、回撤相同；两项是同一实际路径，属于看完网格后的描述性发现。尚无独立未来或稳定实盘盈利证据。

检验资金费入场预算相对于过去价格风险的比例，能否优于固定cap及旧无过滤路径。M2/3/4×R0.005/0.0075/0.01，9组件+9父组合，全部先reserve。预算min(2bp,R×过去10日样本日logvol×最新成熟实际结算间隔/24)，缺数据仅阻止新开/反手，同向q保留。固定所有价格规则/资本/权重/门槛与连续370日窗口，不假设改善。四原账户仅续闭合marks，无资金费/日决策/成交。

本轮完整读取31772事件/15764ID、367份既往结论。初始16项：11项正式结果及5项旧ZIP实际证据齐全，缺实际结果为0；5项legacy的登记标志仍保持历史原值，不将旧实际回测重跑。此前规范研究定义10549，其中登记标实际10336、未标实际213；不能据此声称全部登记均已验证。每个新完整参数配置与数值组件图已查重；18项先成功reserve再计算、均已finish，保留全部通过/淘汰结果。另有12项原账户真实闭合行情观测，合计30ID/60事件。

经济假设：允许的历史资金费流出应与当时价格风险成比例，避免固定cap在波动率变化时过松或过严。固定ETH H2%/E0.75%/L5/K0.75%/有限归一化EWM S16、beta15/17、D3、价格入场V10样本日logvol上限5%；仅改变资金费预算。M=[2,3,4]×R=[0.005,0.0075,0.01]九格全部新算。预算=min(0.0002,R×过去10个已闭合日收益的样本logvol×最新合格已结算间隔小时/24)，Decimal28，以sigma十进制字符串转换；R为风险预算比例，0.0002为每次结算费率硬上限2bp。

按signal UTC00:00之前已可用、结算年龄1–36小时的最新M笔SIGNED实际费率取中位数：奇数中间项、偶数中间二项平均；max(原入场方向×median,0)<=动态预算才允许新开/反手。缺M笔、缺过去间隔、间隔非正或大于36小时则阻止新开/反手；同向实际q保留，反手先平旧仓。交易在下一UTC00:01 OPEN。来源available_ts=结算后1小时是保守可得性假设，不是历史网络到达证据；历史中位数不是未来费率。

实际间隔：归一化actual_interval_hours全部为名义8小时，不能当成测量值。新门槛使用最新合格fundingTime与其直接上一笔真实fundingTime的纳秒差/3600000000000，两笔都在signal时可得；保留毫秒抖动。BTC/ETH各1212条来源，全370次决策都至少有4条成熟合格记录，完整选择索引/实际率/年龄/间隔已保存。数据文件和原始公共响应及SHA256保留在plan、funding_signal_preflight、data_manifest和raw_evidence_index。官方公开字段依据[Binance资金费历史文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)，访问UTC2026-11-10。相对风险预算公式为本轮自行预设研究假设。

父组合：旧BTC29/H3%/E1%银行3750、N1000整条实际净值只读复用；新ETH银行15000、N4500逐笔重算实际数量/LOT/成本/资金费/保证金与完整净值。raw权重[1,1]相加两个完整独立银行，本金18750，20%/80%资金占比不再乘第二次。无归一化、净值缩放、转账、再平衡、父订单或跨组件交叉保证金。10项旧结果含同M固定75ppm对照、共同BTC及同资本/名义金额常持有基准；现金0%。

Walk-forward已实际完成：2025-10-19 UTC00:01至2026-10-24 UTC00:01连续370日，12×30日完整折+10日尾；近期40日由day330继承仓位/现金分成8×5日，不在折间重开。源上下文33日，ETH信号19日/成本21日、BTC30日；无模型拟合、标签、purge或embargo。过去已闭合信号、下一可执行OPEN和终点平仓成本均检查；整体回撤由完整连续净值计算。逐折、逐场景、近期折及完整日净值在CSV和压缩结果中。历史反复使用，不能称未触碰最终留出。

成本压力已完成：每边手续费5bp+半价差1bp+滑点2bp；冲击=0.5×过去20日样本logvol×sqrt(实际abs(q)×原生OPEN/过去20日quoteADV)。1/2/3倍执行成本及实际资金费支出，收入不放大。每笔实际fundingTime/rate/mark与结算时q核算；线性永续无现货借币。检查LOT/tick/minnotional、≤0.1%成交参与率、费后1倍入场抵押及1%已闭合小时不利mark维护保证金代理。缺真实L2/TCA、完整历史风险档位/逐tick强平及实盘容量证据。18项在三档成本下全期净收益均正，资格仍需满足完整门槛。

Sensitivity已完成两轴九格、原生及父组合的净收益/整体回撤/Sharpe/Calmar、72条邻接边和静态图。所有格Sharpe为正；R=0.005的父组合近期仅5/8正折且局部严格近期合格率0.5，被淘汰。其余6项父组合近期6/8、局部严格近期合格率2/3或1。所有ETH组件近期仅1–2/8，均淘汰。各成本两张网格均有描述性邻接跳变，最大值在M4边界，未建立稳定平台；不能将依赖网格或相同净值别名当独立证据。

门槛保持：全期/近期各成本净正，1x至少9/12完整30日折为正，近期各成本至少6/8正5日折，3x整体DD≤25%，局部3x净正及严格近期合格率≥60%，至少4次原生平仓，毛价格PnL加净资金费/1x成本≥2.5，无抵押/订单/保证金代理违规，终点flat，至少180日。不因结果调整门槛。

|范围|M|R|1x净%|2x净%|3x净%|3x整体DD%|月正折/12|近期正折1/2/3|状态|
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|native|2|0.005|15.069639|14.376486|13.683555|4.080065|7|1/1/1|rejected|
|native|2|0.0075|15.726299|14.896796|14.067673|4.080065|9|2/2/2|rejected|
|native|2|0.01|16.721251|15.828040|14.935209|4.080065|10|2/2/2|rejected|
|native|3|0.005|14.087305|13.452359|12.817633|4.080065|7|1/1/1|rejected|
|native|3|0.0075|15.307487|14.529721|13.752175|4.080065|8|2/2/2|rejected|
|native|3|0.01|16.302439|15.460965|14.619711|4.080065|9|2/2/2|rejected|
|native|4|0.005|14.004582|13.370889|12.737266|4.082937|7|1/1/1|rejected|
|native|4|0.0075|17.101301|16.213469|15.326017|4.080065|10|2/2/2|rejected|
|native|4|0.01|17.101301|16.213469|15.326017|4.080065|10|2/2/2|rejected|
|parent|2|0.005|14.455612|13.605129|12.754826|3.082168|9|5/5/5|rejected|
|parent|2|0.0075|14.980940|14.021377|13.062121|3.082168|10|6/6/6|passed|
|parent|2|0.01|15.776902|14.766372|13.756150|3.082168|10|6/6/6|passed|
|parent|3|0.005|13.669745|12.865827|12.062089|3.082168|9|5/5/5|rejected|
|parent|3|0.0075|14.645890|13.727716|12.809723|3.082168|9|6/6/6|passed|
|parent|3|0.01|15.441852|14.472712|13.503752|3.082168|9|6/6/6|passed|
|parent|4|0.005|13.603567|12.800651|11.997795|3.083936|9|5/5/5|rejected|
|parent|4|0.0075|16.080941|15.074715|14.068797|3.082168|10|6/6/6|passed|
|parent|4|0.01|16.080941|15.074715|14.068797|3.082168|10|6/6/6|passed|

全部失败判据：{'volcarry_370_ETH_M2_R5000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volcarry_370_ETH_M2_R7500ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volcarry_370_ETH_M2_R10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volcarry_370_ETH_M3_R5000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volcarry_370_ETH_M3_R7500ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volcarry_370_ETH_M3_R10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volcarry_370_ETH_M4_R5000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volcarry_370_ETH_M4_R7500ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volcarry_370_ETH_M4_R10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volcarry_370_parent_BTC29H3_ETH_M2_R5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volcarry_370_parent_BTC29H3_ETH_M2_R7500ppm': [], 'volcarry_370_parent_BTC29H3_ETH_M2_R10000ppm': [], 'volcarry_370_parent_BTC29H3_ETH_M3_R5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volcarry_370_parent_BTC29H3_ETH_M3_R7500ppm': [], 'volcarry_370_parent_BTC29H3_ETH_M3_R10000ppm': [], 'volcarry_370_parent_BTC29H3_ETH_M4_R5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volcarry_370_parent_BTC29H3_ETH_M4_R7500ppm': [], 'volcarry_370_parent_BTC29H3_ETH_M4_R10000ppm': []}。

独立审计：27新原生+27新父组合+18旧原生成本曲线；9990次新策略决策，49950条资金费、1188笔成交，1008项整体/逐月指标、134145项风险检查。独立Fraction信号/Horner趋势、Decimal预算/实际数量/冲击/资金费及完整净值重构通过；未调用新engine.simulate/decide/trade。

旧路径查重：比较485个同C/N旧ETH定义和195个旧父组合，18项中6项三档完整净值均已出现；其中与无过滤对照完全相同的有2项，历史通过父组合中1项。另12项在各成本收益/回撤上均被无过滤对照严格支配。M4两档R互为同一新路径，最多是一条新增历史路径；M4发现为网格后描述，事前代表仍为M3/R0.0075，不改为最优点。

逐项同M固定75ppm与旧无过滤对照的收益、成本、资金费、净值哈希及价差PnL归因留档；过滤改变的是持仓路径，收益变化不能全归为资金费预测能力。旧报告、资格与规则原字节保留。

四原账户本窗仅延续：SMA/single Nov10 00:30–02:30，L4/FEWM 02:10–04:10，全部闭合分钟mark/小时风险，无新资金费、日决策、成交或重开。SMA完整65个SPOT日上下文继续使用031055轮、结束Nov10 UTC00:00；当前minute数组不能替换日上下文。所有现金/q/desired/成本及完整历史净值前缀独立核对，不采用本轮研究预算。

原SMA NAV 56230→56350，累计56309分钟；仍为partial延迟shadow，不等同paper10实时行情模拟或180日前向资格。
原single NAV 20655→20777，累计20309分钟；仍为partial延迟shadow，不等同paper10实时行情模拟或180日前向资格。
L4 NAV 13392→13514，累计13209分钟；仍为partial延迟shadow，不等同paper10实时行情模拟或180日前向资格。
FEWM NAV 7500→7622，累计7449分钟；仍为partial延迟shadow，不等同paper10实时行情模拟或180日前向资格。

下轮四账户仅续已闭合mark：SMA/single02:30–04:30、L4/FEWM04:10–06:10；下一日决策Nov11 UTC00:01。三个永续账户最近真实资金费均为Nov10_00且各自已结算一次；下一08必须等各自窗口跨越后读取真实新时间戳/rate/mark，以各自当时q核算，不复用旧00/08/16现金流。下一研究预案为固定M4，对资金费预算单独VW=[8,10,12]×R=[0.00625,0.0075,0.00875]；价格入场V10规则不改。VW10/R0.0075是本轮已执行中心必须只读，不能仅添加显式默认字段冒充新配置。下一批尚未执行，仍须完整查重、代码/来源/边界检查、冻结和reserve。

只读监控本轮生成与原生检查True，10126研究行，其中旧10108行不变、新18行；paper10为10账户/315观察。gzip4636596字节。未重部署或新建任务，未改变冻结规则/本金/持仓。

准备/只读检查发生的真实失败及修复、4项预期合成RED全部保留；无真实回测或账户窗口重跑、无真实订单。部分继承输出字符串及旧派生字段仍写12/36、H/F或F50，独立订正见derived_label_correction.json；权威结果为冻结spec/plan、每配置M/R、真实源数据、压缩逐笔/净值及独立核验。不得修改已finish报告来掩盖标签遗留。

复现：见reproduction.md与各*_commands.json的真实argv/cwd/原生退出码。大行情与完整原始数据仍保留在忽略data目录；Git保存全部正负结果、逐折/成本/敏感性、完整账户账本、原始公共响应压缩副本与必要SHA证据。可重建中间文件清理记录见cleanup_verification.json。

发布步骤：本轮锁内完成登记/检查/只读快照后封存，直接提交并非force push main，独立核对远端main ref、完整tree、必需blob和三个永续账户完整链，然后释放锁。真实commit/push与解锁终态见.git/automation_proofs/20261110T051156Z.json，不能仅据本文宣称push成功。
