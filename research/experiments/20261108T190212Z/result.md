本轮6新ETH斜率间隔配置＋6新组合，共36成本场景实际回测；组合历史通过6/6、淘汰0/6。旧D6三格原生和父组合只读。

上轮缩短S至12/14的六个组合虽历史通过，但均未优于同D旧S16对照，且边界与净值路径重合仍在。本轮固定L5/H2/E1/K1.5%、entry-only V10cap4.5%和原独立银行，预设D4/5/6×S12/14/16及beta=(S-1)/(S+1)，检验较短斜率间隔在相同严格斜率门槛下能否筛选更强近期趋势、降低滞后或噪音损失。旧D6各S行只读；6新ETH和6新组合各自reserve后实际计算。事前代表D4/S12，不据结果扩网格、改门槛或代表。最大ETH22、BTC30过去收盘，保留共同初始33日及370日完整轴。重复开发历史和多重选择不是独立最终、未来或稳定实盘盈利。监控真实失败才按要求保留旧有效汇总并留档，不削弱检查或改变账户。

完整读取30616登记事件/15186ID、350份既往结论。初始16项真实历史证据齐全，缺0；此前研究定义10345、标实际10132、未标实际213，不称全部登记均有结果。

固定BTC signedROC29日/H3%/E1%，只读C3750/N1000。ETH C15000/N4500、反向ROC5日/H2%、finiteEWM S12/14/16 beta=(S-1)/(S+1)、固定严格斜率K1.5%，D4/5/6日×慢窗口S12/14/16，退出E1%固定。入场strictH优先；阈值内原long在ROC<E保留、原short在ROC>-E保留，等于退出边界平仓。慢趋势与V10样本logvol上限4.5%只过滤新开/反手；同向留实际q、反手先平后开，无日再平衡。新参数均实际核算数量、LOT、成交量冲击、费用、资金费、风险和完整NAV。

Raw[1,1]直接相加两个独立完整银行NAV，总本金18750，资金占比20/80%不重复乘、不归一化、不缩放旧q/NAV/成本。BTC初始名义为本银行26.666667%/总本5.333333%，ETH为本银行30%/总本24%；无父订单、转账、再平衡或交叉保证金。

370日连续开发OOS：2025-10-19UTC00:01至2026-10-24UTC00:01，12×30完整折＋10日尾。近期40日继承day330现金/q，划8×5日，不折间重开。BTC需30、ETH最大22、BTC最大30过去完整收盘，来源33日；仅完整过去收盘发信号，下一UTC00:01 OPEN执行，终点计成本平仓。固定规则无fit/labels，purge/embargo0；逐折及连续整体DD留档。重复开发历史和多轮参数选择不是未触碰最终留出、独立未来或稳定实盘收益。

每边5bp手续费＋1bp半价差＋2bp滑点；冲击0.5×过去20完整日样本logvol×sqrt(实际q×OPEN/过去20日quoteADV)。1/2/3倍执行成本与资金费支出压力，收入不放大；真实fundingTime/rate/mark/当时q。线性永续无现货借币，核对LOT/tick/minnotional、参与率≤0.1%、费后1倍入场抵押和1%闭合小时不利mark风险代理；缺L2/TCA/历史完整层级/逐tick强平与真实容量证据。

原生和父组合D/S各9格、旧D6行只读；索引半径1含中心，全部变体收益/整体DD/Sharpe/Calmar及72邻接边、边界/跳变留档。门槛原样：全期和近期各成本净正、1倍≥9/12正30日折、各成本近期≥6/8正5日、3倍DD≤25%、局部三倍净正与严格近期合格率≥60%、至少4原生平仓、毛PnL＋资金费/1倍成本≥2.5、无抵押/订单/风险违规、终点flat、≥180日。与同C/N真实常持有及现金0%只读比较，不据结果改变门槛。

|新配置|类别|ETH D|S|固定E|固定K|1x净%|2x净%|3x净%|3x整体DD%|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
|shortlag370_ETH_D4_S12_L5_H200bp_E10000ppm|native|4|12|0.01|0.015|8.975977|8.505200|8.034446|2.050018|1/1/1|rejected|
|shortlag370_ETH_D4_S14_L5_H200bp_E10000ppm|native|4|14|0.01|0.015|10.575829|9.987021|9.398387|2.050018|1/1/1|rejected|
|shortlag370_ETH_D4_S16_L5_H200bp_E10000ppm|native|4|16|0.01|0.015|11.159528|10.574306|9.989251|2.050018|1/1/1|rejected|
|shortlag370_ETH_D5_S12_L5_H200bp_E10000ppm|native|5|12|0.01|0.015|14.194733|13.313270|12.432373|4.831807|1/1/1|rejected|
|shortlag370_ETH_D5_S14_L5_H200bp_E10000ppm|native|5|14|0.01|0.015|17.868731|16.778301|15.687952|3.904400|2/2/2|rejected|
|shortlag370_ETH_D5_S16_L5_H200bp_E10000ppm|native|5|16|0.01|0.015|16.656438|15.623260|14.590009|3.904400|2/2/2|rejected|
|shortlag370_parent_BTC29H3_D4_S12_L5_H200bp_E10000ppm|parent|4|12|0.01|0.015|9.580683|8.908100|8.235539|1.943908|6/6/6|passed|
|shortlag370_parent_BTC29H3_D4_S14_L5_H200bp_E10000ppm|parent|4|14|0.01|0.015|10.860564|10.093557|9.326693|1.943908|6/6/6|passed|
|shortlag370_parent_BTC29H3_D4_S16_L5_H200bp_E10000ppm|parent|4|16|0.01|0.015|11.327523|10.563385|9.799383|2.243223|6/6/6|passed|
|shortlag370_parent_BTC29H3_D5_S12_L5_H200bp_E10000ppm|parent|5|12|0.01|0.015|13.755687|12.754556|11.753881|3.151605|6/6/6|passed|
|shortlag370_parent_BTC29H3_D5_S14_L5_H200bp_E10000ppm|parent|5|14|0.01|0.015|16.694885|15.526581|14.358344|3.659249|6/6/6|passed|
|shortlag370_parent_BTC29H3_D5_S16_L5_H200bp_E10000ppm|parent|5|16|0.01|0.015|15.725051|14.602548|13.479990|3.659249|6/6/6|passed|

逐项失败判据：{'shortlag370_ETH_D4_S12_L5_H200bp_E10000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'shortlag370_ETH_D4_S14_L5_H200bp_E10000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'shortlag370_ETH_D4_S16_L5_H200bp_E10000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'shortlag370_ETH_D5_S12_L5_H200bp_E10000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'shortlag370_ETH_D5_S14_L5_H200bp_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'shortlag370_ETH_D5_S16_L5_H200bp_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'shortlag370_parent_BTC29H3_D4_S12_L5_H200bp_E10000ppm': [], 'shortlag370_parent_BTC29H3_D4_S14_L5_H200bp_E10000ppm': [], 'shortlag370_parent_BTC29H3_D4_S16_L5_H200bp_E10000ppm': [], 'shortlag370_parent_BTC29H3_D5_S12_L5_H200bp_E10000ppm': [], 'shortlag370_parent_BTC29H3_D5_S14_L5_H200bp_E10000ppm': [], 'shortlag370_parent_BTC29H3_D5_S16_L5_H200bp_E10000ppm': []}。

原四冻结账户独立延续原现金/q/desired/成本/风险/fullNAV，不采用研究慢窗口S。本轮SMA/single Nov8_14:30→16:30，SMA仅mark、single跨实际16:00:00.000资金费按自身结算前q/rate/mark独立记账；L4/FEWM Nov8_16:10→18:10仅mark、各自16已入账不重复，旧08不重复，均无新日决策/成交，不重复已完成的Nov8_00/00:01或旧16。SMA完整65日spot上下文保留R025309的1d/1m字典，本轮输入minute数组需核对重叠，所有原规则/本金/持仓与完整NAV前缀不变。所有账户partial延迟shadow，非十策略实时报价收益或180日资格。

finish和必要检查后，在同main排他锁内生成只读monitor并检查。保留全部正负、失败、冻结规则、完整账本、登记及必要真实输入，仅清理可重建中间物。无真实订单、页面重部署或新定时任务。真实main push/完整远端tree/blob核验及解锁终态见.git/automation_proofs/20261108T190212Z.json。

历史spec中的warmup_days30/embargo_days3和persistence旧E.005文字为未被执行器读取的继承描述；本轮实际前置33个完整收盘，无fit/labels和折间purge/embargo，当前数值E=.01及完整规则为执行依据，详见冻结rules.legacy_parameter_fields。

同窗口旧D6对照：仅D5/S14父组合在1/2/3倍成本下均实现净收益更高且整体回撤更低。3倍成本净收益14.358344%（旧11.994124%，增加2.364220个百分点），整体DD 3.659249%（旧4.172415%）。D4三组合以降低收益换取较低回撤；D5/S12仅3倍收益略高，1/2倍收益较低；D5/S16被同S旧D6对照占优。旧D6/S16仍为本9格收益与Sharpe最高点；不能据此宣称新全局最优或稳定平台。原生ETH近期只有1或2/8正折，父组合受既有BTC路径影响达到6/8，未证明ETH组件独立近期稳定。事前代表D4/S12保留。

监控本轮生成/原生校验成功：True；本轮新增研究展示12条、待恢复后展示0条。若失败，原生非零退出/生成快照/旧有效文件哈希留档，保留上次有效汇总，未修改检查门槛、账户或规则。
同S、同C/N的旧D6/H2%对照在1/2/3倍成本下收益不低且整体DD不高的当前配置数：2/12。本轮组合历史通过6项；各成本收益不低且整体回撤不高、至少一项严格改善的当前配置数2/12。逐项比较留档，不替换冻结账户，不建立新前向账户。
封存：6新ETH斜率间隔组件＋6新组合/36场景，组合通过6、淘汰0；24ID/48事件全部finish，49213旧文件保持。18旧原生路径只读，18新ETH原生路径/6660实际决策及18新组合路径独立核验。
原SMA NAV54188→54308，single 18565→18689，L4 11304→11426，FEWM 5412→5534。single/L4/FEWM实际新资金费6/0/0，日事件0/0/0，成交0/0/0；各自实际资金费时间戳/rate/mark/结算前q与本窗闭合mark独立核验，旧00/00:01仅保留已验证历史证明，原现金/q/风险/fullNAV连续，不复制现金流或重复16/00。FEWM累计5409分钟/138ID，所有账户partial非180日资格。
只读监控9916行，原9904行不变，10报价账户/298观察，gzip4555200字节。HTTP/传输失败1次原证据保留，所有正负/淘汰结果、完整账本/冻结规则/登记/必要输入保留。真实main push、完整远端tree/blob与解锁终态见.git/automation_proofs/20261108T190212Z.json。
