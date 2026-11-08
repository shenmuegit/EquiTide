本轮6新ETH斜率间隔配置＋6新组合，共36成本场景实际回测；组合历史通过0/6、淘汰6/6。旧D4三格原生和父组合只读。

上轮D4组合降低回撤但收益低于较长间隔，D5/S14相对同S旧D6在全部成本下同时提高收益和降低回撤；旧D6/S16仍为上轮格内最高收益/Sharpe，且边界及参数跳变未消失。本轮固定L5/H2/E1/K1.5%、entry-only V10cap4.5%及BTC29/H3/E1原独立银行，预设D2/3/4×S12/14/16、beta=(S-1)/(S+1)。检验更短斜率间隔在同1.5%严格门槛下要求更强短期速度，能否延续D4低回撤而保留足够交易和成本余量；也可能过度过滤、近期失效。旧D4三S行只读；六新ETH与六新组合各自reserve后真实计算。事前代表D2/S12，不据结果扩网格、改门槛或代表。ETH信号最多20日、成本20个日收益需21个收盘、BTC最多30日过去完整收盘，保留共同初始33日及370日连续轴。重复开发历史和多重选择不是独立最终、未来或稳定实盘盈利。

完整读取30684登记事件/15220ID、351份既往结论。初始16项真实历史证据齐全，缺0；此前研究定义10357、标实际10144、未标实际213，不称全部登记均有结果。

固定BTC signedROC29日/H3%/E1%，只读C3750/N1000。ETH C15000/N4500、反向ROC5日/H2%、finiteEWM S12/14/16 beta=(S-1)/(S+1)、固定严格斜率K1.5%，D2/3/4日×慢窗口S12/14/16，退出E1%固定。入场strictH优先；阈值内原long在ROC<E保留、原short在ROC>-E保留，等于退出边界平仓。慢趋势与V10样本logvol上限4.5%只过滤新开/反手；同向留实际q、反手先平后开，无日再平衡。新参数均实际核算数量、LOT、成交量冲击、费用、资金费、风险和完整NAV。

Raw[1,1]直接相加两个独立完整银行NAV，总本金18750，资金占比20/80%不重复乘、不归一化、不缩放旧q/NAV/成本。BTC初始名义为本银行26.666667%/总本5.333333%，ETH为本银行30%/总本24%；无父订单、转账、再平衡或交叉保证金。

370日连续开发OOS：2025-10-19UTC00:01至2026-10-24UTC00:01，12×30完整折＋10日尾。近期40日继承day330现金/q，划8×5日，不折间重开。BTC需30、ETH信号20/成本21、BTC最大30过去完整收盘，来源33日；仅完整过去收盘发信号，下一UTC00:01 OPEN执行，终点计成本平仓。固定规则无fit/labels，purge/embargo0；逐折及连续整体DD留档。重复开发历史和多轮参数选择不是未触碰最终留出、独立未来或稳定实盘收益。

每边5bp手续费＋1bp半价差＋2bp滑点；冲击0.5×过去20完整日样本logvol×sqrt(实际q×OPEN/过去20日quoteADV)。1/2/3倍执行成本与资金费支出压力，收入不放大；真实fundingTime/rate/mark/当时q。线性永续无现货借币，核对LOT/tick/minnotional、参与率≤0.1%、费后1倍入场抵押和1%闭合小时不利mark风险代理；缺L2/TCA/历史完整层级/逐tick强平与真实容量证据。

原生和父组合D/S各9格、旧D4行只读；索引半径1含中心，全部变体收益/整体DD/Sharpe/Calmar及72邻接边、边界/跳变留档。门槛原样：全期和近期各成本净正、1倍≥9/12正30日折、各成本近期≥6/8正5日、3倍DD≤25%、局部三倍净正与严格近期合格率≥60%、至少4原生平仓、毛PnL＋资金费/1倍成本≥2.5、无抵押/订单/风险违规、终点flat、≥180日。与同C/N真实常持有及现金0%只读比较，不据结果改变门槛。

|新配置|类别|ETH D|S|固定E|固定K|1x净%|2x净%|3x净%|3x整体DD%|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
|shortlag370_ETH_D2_S12_L5_H200bp_E10000ppm|native|2|12|0.01|0.015|0.000000|0.000000|0.000000|0.000000|0/0/0|rejected|
|shortlag370_ETH_D2_S14_L5_H200bp_E10000ppm|native|2|14|0.01|0.015|0.000000|0.000000|0.000000|0.000000|0/0/0|rejected|
|shortlag370_ETH_D2_S16_L5_H200bp_E10000ppm|native|2|16|0.01|0.015|0.604899|0.550577|0.496405|1.378558|0/0/0|rejected|
|shortlag370_ETH_D3_S12_L5_H200bp_E10000ppm|native|3|12|0.01|0.015|7.029792|6.820040|6.610291|2.050018|0/0/0|rejected|
|shortlag370_ETH_D3_S14_L5_H200bp_E10000ppm|native|3|14|0.01|0.015|9.125688|8.678746|8.231824|2.050018|0/0/0|rejected|
|shortlag370_ETH_D3_S16_L5_H200bp_E10000ppm|native|3|16|0.01|0.015|8.493527|8.081113|7.668720|2.171053|1/1/1|rejected|
|shortlag370_parent_BTC29H3_D2_S12_L5_H200bp_E10000ppm|parent|2|12|0.01|0.015|2.399901|2.103940|1.807983|1.435228|5/5/5|rejected|
|shortlag370_parent_BTC29H3_D2_S14_L5_H200bp_E10000ppm|parent|2|14|0.01|0.015|2.399901|2.103940|1.807983|1.435228|5/5/5|rejected|
|shortlag370_parent_BTC29H3_D2_S16_L5_H200bp_E10000ppm|parent|2|16|0.01|0.015|2.883820|2.544401|2.205107|1.488365|5/5/5|rejected|
|shortlag370_parent_BTC29H3_D3_S12_L5_H200bp_E10000ppm|parent|3|12|0.01|0.015|8.023734|7.559972|7.096216|1.943908|5/5/5|rejected|
|shortlag370_parent_BTC29H3_D3_S14_L5_H200bp_E10000ppm|parent|3|14|0.01|0.015|9.700451|9.046936|8.393442|2.132977|5/5/5|rejected|
|shortlag370_parent_BTC29H3_D3_S16_L5_H200bp_E10000ppm|parent|3|16|0.01|0.015|9.194722|8.568831|7.942959|1.943908|6/6/6|rejected|

逐项失败判据：{'shortlag370_ETH_D2_S12_L5_H200bp_E10000ppm': ['positive_all_costs', 'nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_positive3_gte60pct', 'local_recent6of8_allcost_gte60pct', 'four_underlying_native_closes1', 'gross_plus_funding_to_cost1_gte2_5'], 'shortlag370_ETH_D2_S14_L5_H200bp_E10000ppm': ['positive_all_costs', 'nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct', 'four_underlying_native_closes1', 'gross_plus_funding_to_cost1_gte2_5'], 'shortlag370_ETH_D2_S16_L5_H200bp_E10000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct', 'four_underlying_native_closes1'], 'shortlag370_ETH_D3_S12_L5_H200bp_E10000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'shortlag370_ETH_D3_S14_L5_H200bp_E10000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'shortlag370_ETH_D3_S16_L5_H200bp_E10000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'shortlag370_parent_BTC29H3_D2_S12_L5_H200bp_E10000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'shortlag370_parent_BTC29H3_D2_S14_L5_H200bp_E10000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'shortlag370_parent_BTC29H3_D2_S16_L5_H200bp_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'shortlag370_parent_BTC29H3_D3_S12_L5_H200bp_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'shortlag370_parent_BTC29H3_D3_S14_L5_H200bp_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'shortlag370_parent_BTC29H3_D3_S16_L5_H200bp_E10000ppm': ['local_recent6of8_allcost_gte60pct']}。

原四冻结账户独立延续原现金/q/desired/成本/风险/fullNAV，不采用研究斜率间隔D。本轮SMA/single Nov8_16:30→18:30、L4/FEWM Nov8_18:10→20:10均仅增加闭合mark，各套永续账户自己的16点资金费此前已独立入账，不再记账，旧08不重复，均无新日决策/成交，不重复已完成的Nov8_00/00:01或旧16。SMA完整65日spot上下文保留R025309的1d/1m字典，本轮输入minute数组需核对重叠，所有原规则/本金/持仓与完整NAV前缀不变。所有账户partial延迟shadow，非十策略实时报价收益或180日资格。

finish和必要检查后，在同main排他锁内生成只读monitor并检查。保留全部正负、失败、冻结规则、完整账本、登记及必要真实输入，仅清理可重建中间物。无真实订单、页面重部署或新定时任务。真实main push/完整远端tree/blob核验及解锁终态见.git/automation_proofs/20261108T210242Z.json。

历史spec中的warmup_days30/embargo_days3和persistence旧E.005文字为未被执行器读取的继承描述；本轮实际前置33个完整收盘，无fit/labels和折间purge/embargo，当前数值E=.01及完整规则为执行依据，详见冻结rules.legacy_parameter_fields。

本轮解释：12项均实际完成后淘汰；六个组合3倍成本净收益范围1.807983%–8.393442%，整体最大回撤1.435228%–2.132977%。D2/S12、D2/S14原生ETH在完整370日均无成交，净值保持15000，收益和回撤为0，Sharpe/Calmar未定义；这是实际执行结果，不是缺数据，也不填造Sharpe=0。对应两个父组合路径相同，仅为旧BTC银行加ETH现金，不是两份独立收益证据。D3/S16近期各成本6/8正折，但预设邻域严格近期通过率3/6=50%低于60%；其余五个组合近期只有5/8正折。旧D4同S对照维持原资格。本轮没有合格新候选，不能因全期成本后净正而保留通过。

只读导出修复：初次汇总因未定义Sharpe相减报错，原非零退出、源码快照和日志均保留。成功重试仅修复派生导出及配套只读网格校验；报告/计划/36绑定源文件、收益、资格门槛不变，无金融或账户重算。图表空值显示N/A；全部九格和72邻接边保留，原生Sharpe正值占7/9，4条未定义邻接差不参与可定义Sharpe跳变统计但仍在表中。另一次回执字典附加字段判断失败亦如实留档并修正核对方式。

监控本轮生成/原生校验成功：True；本轮新增研究展示12条、待恢复后展示0条。若失败，原生非零退出/生成快照/旧有效文件哈希留档，保留上次有效汇总，未修改检查门槛、账户或规则。
同S、同C/N的旧D4/H2%对照在1/2/3倍成本下收益不低且整体DD不高的当前配置数：5/12。本轮组合历史通过0项；各成本收益不低且整体回撤不高、至少一项严格改善的当前配置数0/12。逐项比较留档，不替换冻结账户，不建立新前向账户。
封存：6新ETH斜率间隔组件＋6新组合/36场景，组合通过0、淘汰6；24ID/48事件全部finish，49586旧文件保持。18旧原生路径只读，18新ETH原生路径/6660实际决策及18新组合路径独立核验。
原SMA NAV54308→54428，single 18689→18811，L4 11426→11548，FEWM 5534→5656。single/L4/FEWM实际新资金费0/0/0，日事件0/0/0，成交0/0/0；各自实际资金费时间戳/rate/mark/结算前q与本窗闭合mark独立核验，旧00/00:01仅保留已验证历史证明，原现金/q/风险/fullNAV连续，不复制现金流或重复16/00。FEWM累计5529分钟/141ID，所有账户partial非180日资格。
只读监控9928行，原9916行不变，10报价账户/299观察，gzip4559951字节。HTTP/传输失败2次原证据保留，所有正负/淘汰结果、完整账本/冻结规则/登记/必要输入保留。真实main push、完整远端tree/blob与解锁终态见.git/automation_proofs/20261108T210242Z.json。
