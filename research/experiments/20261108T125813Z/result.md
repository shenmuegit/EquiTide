本轮6新ETH慢趋势窗口配置＋6新组合，共36成本场景实际回测；组合历史通过6/6、淘汰0/6。旧S24三格原生和父组合只读。

上轮H1.75/2.25%×D6/7/8的6新组合历史通过，但全部新配置在各成本下均被同D旧H2%对照收益/回撤支配，未形成更优替代。本轮固定L5/H2/E1/K1.5%，预设慢窗口S20/22/24×斜率间隔D6/7/8，finiteEWM beta=(S-1)/(S+1)，检验更短平滑窗口响应趋势与噪音的权衡。保持原33日前置共同市场轴，最大S24+D8=32，不计算需要额外前置的S26；旧S24列只读。6新ETH/6新组合各自reserve后计算；事前代表D6/S20，不据结果扩网格、改代表或改门槛，保留正负及失败、同路径。重复开发历史不是独立最终/未来或稳定实盘盈利。

完整读取30392登记事件/15074ID、347份既往结论。初始16项真实历史证据齐全，缺0；此前研究定义10309、标实际10096、未标实际213，不称全部登记均有结果。

固定BTC signedROC29日/H3%/E1%，只读C3750/N1000。ETH C15000/N4500、反向ROC5日/H2%、finiteEWM S20/22/24 beta=(S-1)/(S+1)、固定严格斜率K1.5%，D6/7/8日×慢窗口S20/22/24，退出E1%固定。入场strictH优先；阈值内原long在ROC<E保留、原short在ROC>-E保留，等于退出边界平仓。慢趋势与V10样本logvol上限4.5%只过滤新开/反手；同向留实际q、反手先平后开，无日再平衡。新参数均实际核算数量、LOT、成交量冲击、费用、资金费、风险和完整NAV。

Raw[1,1]直接相加两个独立完整银行NAV，总本金18750，资金占比20/80%不重复乘、不归一化、不缩放旧q/NAV/成本。BTC初始名义为本银行26.666667%/总本5.333333%，ETH为本银行30%/总本24%；无父订单、转账、再平衡或交叉保证金。

370日连续开发OOS：2025-10-19UTC00:01至2026-10-24UTC00:01，12×30完整折＋10日尾。近期40日继承day330现金/q，划8×5日，不折间重开。BTC需30、ETH最大32过去完整收盘，来源33日；仅完整过去收盘发信号，下一UTC00:01 OPEN执行，终点计成本平仓。固定规则无fit/labels，purge/embargo0；逐折及连续整体DD留档。重复开发历史和多轮参数选择不是未触碰最终留出、独立未来或稳定实盘收益。

每边5bp手续费＋1bp半价差＋2bp滑点；冲击0.5×过去20完整日样本logvol×sqrt(实际q×OPEN/过去20日quoteADV)。1/2/3倍执行成本与资金费支出压力，收入不放大；真实fundingTime/rate/mark/当时q。线性永续无现货借币，核对LOT/tick/minnotional、参与率≤0.1%、费后1倍入场抵押和1%闭合小时不利mark风险代理；缺L2/TCA/历史完整层级/逐tick强平与真实容量证据。

原生和父组合D/S各9格、旧S24列只读；索引半径1含中心，全部变体收益/整体DD/Sharpe/Calmar及72邻接边、边界/跳变留档。门槛原样：全期和近期各成本净正、1倍≥9/12正30日折、各成本近期≥6/8正5日、3倍DD≤25%、局部三倍净正与严格近期合格率≥60%、至少4原生平仓、毛PnL＋资金费/1倍成本≥2.5、无抵押/订单/风险违规、终点flat、≥180日。与同C/N真实常持有及现金0%只读比较，不据结果改变门槛。

|新配置|类别|ETH D|S|固定E|固定K|1x净%|2x净%|3x净%|3x整体DD%|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
|slowwindow370_ETH_D6_S20_L5_H200bp_E10000ppm|native|6|20|0.01|0.015|19.069815|17.813147|16.556565|3.846782|2/2/2|rejected|
|slowwindow370_ETH_D6_S22_L5_H200bp_E10000ppm|native|6|22|0.01|0.015|16.930280|15.608447|14.286395|3.908477|2/2/2|rejected|
|slowwindow370_ETH_D7_S20_L5_H200bp_E10000ppm|native|7|20|0.01|0.015|17.574204|16.146621|14.718718|4.436388|2/2/2|rejected|
|slowwindow370_ETH_D7_S22_L5_H200bp_E10000ppm|native|7|22|0.01|0.015|16.343131|14.923517|13.503583|5.256798|2/2/2|rejected|
|slowwindow370_ETH_D8_S20_L5_H200bp_E10000ppm|native|8|20|0.01|0.015|16.343131|14.923517|13.503583|5.256798|2/2/2|rejected|
|slowwindow370_ETH_D8_S22_L5_H200bp_E10000ppm|native|8|22|0.01|0.015|15.656025|14.245364|12.834381|5.256798|2/2/2|rejected|
|slowwindow370_parent_BTC29H3_D6_S20_L5_H200bp_E10000ppm|parent|6|20|0.01|0.015|17.655753|16.354457|15.053234|3.615595|6/6/6|passed|
|slowwindow370_parent_BTC29H3_D6_S22_L5_H200bp_E10000ppm|parent|6|22|0.01|0.015|15.944124|14.590698|13.237098|3.662329|6/6/6|passed|
|slowwindow370_parent_BTC29H3_D7_S20_L5_H200bp_E10000ppm|parent|7|20|0.01|0.015|16.459264|15.021237|13.582957|3.949625|6/6/6|passed|
|slowwindow370_parent_BTC29H3_D7_S22_L5_H200bp_E10000ppm|parent|7|22|0.01|0.015|15.474405|14.042754|12.610849|4.697440|6/6/6|passed|
|slowwindow370_parent_BTC29H3_D8_S20_L5_H200bp_E10000ppm|parent|8|20|0.01|0.015|15.474405|14.042754|12.610849|4.697440|6/6/6|passed|
|slowwindow370_parent_BTC29H3_D8_S22_L5_H200bp_E10000ppm|parent|8|22|0.01|0.015|14.924721|13.500231|12.075488|4.697440|6/6/6|passed|

逐项失败判据：{'slowwindow370_ETH_D6_S20_L5_H200bp_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'slowwindow370_ETH_D6_S22_L5_H200bp_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'slowwindow370_ETH_D7_S20_L5_H200bp_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'slowwindow370_ETH_D7_S22_L5_H200bp_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'slowwindow370_ETH_D8_S20_L5_H200bp_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'slowwindow370_ETH_D8_S22_L5_H200bp_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'slowwindow370_parent_BTC29H3_D6_S20_L5_H200bp_E10000ppm': [], 'slowwindow370_parent_BTC29H3_D6_S22_L5_H200bp_E10000ppm': [], 'slowwindow370_parent_BTC29H3_D7_S20_L5_H200bp_E10000ppm': [], 'slowwindow370_parent_BTC29H3_D7_S22_L5_H200bp_E10000ppm': [], 'slowwindow370_parent_BTC29H3_D8_S20_L5_H200bp_E10000ppm': [], 'slowwindow370_parent_BTC29H3_D8_S22_L5_H200bp_E10000ppm': []}。

原四冻结账户独立延续原现金/q/desired/成本/风险/fullNAV，不采用研究慢窗口S。本轮SMA/single Nov8_08:30→10:30及L4/FEWM Nov8_10:10→12:10均仅mark，所有账户旧08资金费已按各自q/rate/mark计入，本轮不重复，均无新日决策/成交，不重复已完成的Nov8_00/00:01或旧16。SMA完整65日spot上下文保留R025309的1d/1m字典，本轮输入minute数组需核对重叠，所有原规则/本金/持仓与完整NAV前缀不变。所有账户partial延迟shadow，非十策略实时报价收益或180日资格。

finish和必要检查后，在同main排他锁内生成只读monitor并检查。保留全部正负、失败、冻结规则、完整账本、登记及必要真实输入，仅清理可重建中间物。无真实订单、页面重部署或新定时任务。真实main push/完整远端tree/blob核验及解锁终态见.git/automation_proofs/20261108T125813Z.json。

历史spec中的warmup_days30/embargo_days3和persistence旧E.005文字为未被执行器读取的继承描述；本轮实际前置33个完整收盘，无fit/labels和折间purge/embargo，当前数值E=.01及完整规则为执行依据，详见冻结rules.legacy_parameter_fields。

同D、同C/N的旧S24/H2%对照在1/2/3倍成本下收益不低且整体DD不高的当前配置数：9/12。本轮组合历史通过6项；各成本同时改善旧S24收益/回撤的当前配置数2/12。逐项比较留档，不替换冻结账户，不建立新前向账户。
封存：6新ETH慢趋势窗口组件＋6新组合/36场景，组合通过6、淘汰0；24ID/48事件全部finish，48080旧文件保持。18旧原生路径只读，18新ETH原生路径/6660实际决策及18新组合路径独立核验。
原SMA NAV53828→53948，single 18199→18321，L4 10936→11058，FEWM 5044→5166。single/L4/FEWM实际新资金费0/0/0，日事件0/0/0，成交0/0/0；各自实际资金费时间戳/rate/mark/结算前q与本窗闭合mark独立核验，旧00/00:01仅保留已验证历史证明，原现金/q/风险/fullNAV连续，不复制现金流或重复16/00。FEWM累计5049分钟/129ID，所有账户partial非180日资格。
只读监控9880行，原9868行不变，10报价账户/295观察，gzip4538933字节。HTTP/传输失败1次原证据保留，所有正负/淘汰结果、完整账本/冻结规则/登记/必要输入保留。真实main push、完整远端tree/blob与解锁终态见.git/automation_proofs/20261108T125813Z.json。
