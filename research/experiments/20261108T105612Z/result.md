本轮6新ETH入场门槛配置＋6新组合，共36成本场景实际回测；组合历史通过6/6、淘汰0/6。旧H2%三格原生和父组合只读。

上轮宽快周期L3/5/7批次12个配置全部淘汰，尽管全期净正，近期折和局部合格率不足。本轮固定L5，预设对称入场H1.75/2/2.25%×慢间隔D6/7/8，退出E1%、finiteEWM24/K1.5%、entry-only V10cap4.5%和原银行不变，检验门槛过滤噪音与错过反转的权衡。旧H2%三组件/三组合只读；6新ETH和6新组合逐个reserve后计算。事前代表D6/H1.75/L5，不因结果改代表、扩网格或门槛；正负、失败、同路径均保留。重复开发历史不是未触碰最终/独立未来或稳定实盘盈利。

完整读取30324登记事件/15040ID、346份既往结论。初始16项真实历史证据齐全，缺0；此前研究定义10297、标实际10084、未标实际213，不称全部登记均有结果。

固定BTC signedROC29日/H3%/E1%，只读C3750/N1000。ETH C15000/N4500、反向ROC5日/H1.75/2/2.25%、finiteEWM24 beta23/25、固定严格斜率K1.5%，D6/7/8日×对称入场H1.75/2/2.25%，退出E1%固定。入场strictH优先；阈值内原long在ROC<E保留、原short在ROC>-E保留，等于退出边界平仓。慢趋势与V10样本logvol上限4.5%只过滤新开/反手；同向留实际q、反手先平后开，无日再平衡。新参数均实际核算数量、LOT、成交量冲击、费用、资金费、风险和完整NAV。

Raw[1,1]直接相加两个独立完整银行NAV，总本金18750，资金占比20/80%不重复乘、不归一化、不缩放旧q/NAV/成本。BTC初始名义为本银行26.666667%/总本5.333333%，ETH为本银行30%/总本24%；无父订单、转账、再平衡或交叉保证金。

370日连续开发OOS：2025-10-19UTC00:01至2026-10-24UTC00:01，12×30完整折＋10日尾。近期40日继承day330现金/q，划8×5日，不折间重开。BTC需30、ETH最大32过去完整收盘，来源33日；仅完整过去收盘发信号，下一UTC00:01 OPEN执行，终点计成本平仓。固定规则无fit/labels，purge/embargo0；逐折及连续整体DD留档。重复开发历史和多轮参数选择不是未触碰最终留出、独立未来或稳定实盘收益。

每边5bp手续费＋1bp半价差＋2bp滑点；冲击0.5×过去20完整日样本logvol×sqrt(实际q×OPEN/过去20日quoteADV)。1/2/3倍执行成本与资金费支出压力，收入不放大；真实fundingTime/rate/mark/当时q。线性永续无现货借币，核对LOT/tick/minnotional、参与率≤0.1%、费后1倍入场抵押和1%闭合小时不利mark风险代理；缺L2/TCA/历史完整层级/逐tick强平与真实容量证据。

原生和父组合D/H各9格、旧H2%列只读；索引半径1含中心，全部变体收益/整体DD/Sharpe/Calmar及72邻接边、边界/跳变留档。门槛原样：全期和近期各成本净正、1倍≥9/12正30日折、各成本近期≥6/8正5日、3倍DD≤25%、局部三倍净正与严格近期合格率≥60%、至少4原生平仓、毛PnL＋资金费/1倍成本≥2.5、无抵押/订单/风险违规、终点flat、≥180日。与同C/N真实常持有及现金0%只读比较，不据结果改变门槛。

|新配置|类别|ETH D|H|固定E|固定K|1x净%|2x净%|3x净%|3x整体DD%|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
|entryhurdle370_ETH_D6_L5_H17500ppm_E10000ppm|native|6|0.0175|0.01|0.015|15.118016|13.787348|12.456645|4.714389|2/2/2|rejected|
|entryhurdle370_ETH_D6_L5_H22500ppm_E10000ppm|native|6|0.0225|0.01|0.015|12.121223|11.073515|10.025549|3.908477|1/1/1|rejected|
|entryhurdle370_ETH_D7_L5_H17500ppm_E10000ppm|native|7|0.0175|0.01|0.015|15.812615|14.494505|13.176360|4.684481|2/2/2|rejected|
|entryhurdle370_ETH_D7_L5_H22500ppm_E10000ppm|native|7|0.0225|0.01|0.015|12.703497|11.607411|10.511067|4.446996|1/1/1|rejected|
|entryhurdle370_ETH_D8_L5_H17500ppm_E10000ppm|native|8|0.0175|0.01|0.015|15.013185|13.643090|12.272961|4.722083|2/2/2|rejected|
|entryhurdle370_ETH_D8_L5_H22500ppm_E10000ppm|native|8|0.0225|0.01|0.015|11.904067|10.755997|9.607668|4.446996|1/1/1|rejected|
|entryhurdle370_parent_BTC29H3_D6_L5_H17500ppm_E10000ppm|parent|6|0.0175|0.01|0.015|14.494313|13.133818|11.773299|3.776722|6/6/6|passed|
|entryhurdle370_parent_BTC29H3_D6_L5_H22500ppm_E10000ppm|parent|6|0.0225|0.01|0.015|12.096879|10.962752|9.828422|3.662329|6/6/6|passed|
|entryhurdle370_parent_BTC29H3_D7_L5_H17500ppm_E10000ppm|parent|7|0.0175|0.01|0.015|15.049993|13.699544|12.349070|3.769884|6/6/6|passed|
|entryhurdle370_parent_BTC29H3_D7_L5_H22500ppm_E10000ppm|parent|7|0.0225|0.01|0.015|12.562698|11.389869|10.216836|3.737890|6/6/6|passed|
|entryhurdle370_parent_BTC29H3_D8_L5_H17500ppm_E10000ppm|parent|8|0.0175|0.01|0.015|14.410449|13.018412|11.626351|3.781705|6/6/6|passed|
|entryhurdle370_parent_BTC29H3_D8_L5_H22500ppm_E10000ppm|parent|8|0.0225|0.01|0.015|11.923154|10.708737|9.494117|3.737890|6/6/6|passed|

逐项失败判据：{'entryhurdle370_ETH_D6_L5_H17500ppm_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'entryhurdle370_ETH_D6_L5_H22500ppm_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'entryhurdle370_ETH_D7_L5_H17500ppm_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'entryhurdle370_ETH_D7_L5_H22500ppm_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'entryhurdle370_ETH_D8_L5_H17500ppm_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'entryhurdle370_ETH_D8_L5_H22500ppm_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'entryhurdle370_parent_BTC29H3_D6_L5_H17500ppm_E10000ppm': [], 'entryhurdle370_parent_BTC29H3_D6_L5_H22500ppm_E10000ppm': [], 'entryhurdle370_parent_BTC29H3_D7_L5_H17500ppm_E10000ppm': [], 'entryhurdle370_parent_BTC29H3_D7_L5_H22500ppm_E10000ppm': [], 'entryhurdle370_parent_BTC29H3_D8_L5_H17500ppm_E10000ppm': [], 'entryhurdle370_parent_BTC29H3_D8_L5_H22500ppm_E10000ppm': []}。

原四冻结账户独立延续原现金/q/desired/成本/风险/fullNAV，不采用研究入场门槛H。本轮SMA/single Nov8_06:30→08:30（SMA仅mark，single计真实08:00:00.001资金费），L4/FEWM Nov8_08:10→10:10仅mark，旧08资金费不重复，按各自结算前q/rate/mark记账，均无新日决策/成交，不重复已完成的Nov8_00/00:01或旧16。SMA完整65日spot上下文保留R025309的1d/1m字典，本轮输入minute数组需核对重叠，所有原规则/本金/持仓与完整NAV前缀不变。所有账户partial延迟shadow，非十策略实时报价收益或180日资格。

finish和必要检查后，在同main排他锁内生成只读monitor并检查。保留全部正负、失败、冻结规则、完整账本、登记及必要真实输入，仅清理可重建中间物。无真实订单、页面重部署或新定时任务。真实main push/完整远端tree/blob核验及解锁终态见.git/automation_proofs/20261108T105612Z.json。

同D、同C/N的旧H2%对照在1/2/3倍成本下收益不低且整体DD不高的当前配置数：12/12。六个新父组合历史门槛通过，但未优于旧中心，不替换冻结账户，不建立新前向账户。
封存：6新ETH入场门槛组件＋6新组合/36场景，组合通过6、淘汰0；24ID/48事件全部finish，47719旧文件保持。18旧原生路径只读，18新ETH原生路径/6660实际决策及18新组合路径独立核验。
原SMA NAV53708→53828，single 18075→18199，L4 10814→10936，FEWM 4922→5044。single/L4/FEWM实际新资金费6/0/0，日事件0/0/0，成交0/0/0；各自实际资金费时间戳/rate/mark/结算前q与本窗闭合mark独立核验，旧00/00:01仅保留已验证历史证明，原现金/q/风险/fullNAV连续，不复制现金流或重复16/00。FEWM累计4929分钟/126ID，所有账户partial非180日资格。
只读监控9868行，原9856行不变，10报价账户/294观察，gzip4533115字节。HTTP/传输失败0次原证据保留，所有正负/淘汰结果、完整账本/冻结规则/登记/必要输入保留。真实main push、完整远端tree/blob与解锁终态见.git/automation_proofs/20261108T105612Z.json。
