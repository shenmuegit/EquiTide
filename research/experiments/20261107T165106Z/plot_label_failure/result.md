本轮6新BTC组件＋6新组合/36成本场景实算；新组合通过6/6、淘汰0/6。已有L29/E1%的H2.75/3/3.25%三格原组件和组合只读，未重跑或改资格。

上轮相邻回看28/30日虽组合历史通过，收益仍低于旧29日同门槛对照；较宽退出缓冲也未形成更优方法。本轮固定BTC L29/C3750/N1000，事前细测退出缓冲E0.75/1/1.25%×入场H2.75/3/3.25%，检验1%附近稳定性而非把旧高点称最终最优。已有E1%三个H的真实原组件和父组合只读；E0.75/1.25%六个新BTC组件及六新父组合先reserve再计算。ETH固定C15000/N4500、L5/H2%/E0.5%/finiteEWM24/D7/K2%/V10cap4.5%。预设代表H3%/E0.75%，raw1/1完整银行、原时间边界和失败门槛不变；保留全部正负结果。多轮复用开发历史、参数和同路径选择偏差不是独立最终、未来或稳定实盘盈利。

完整读取29712事件/14734ID、337既往结论。初始16项实际证据齐全，缺0；此前研究定义10189，标实际9976、未标213，不称所有登记都有结果。

BTC固定L29、C3750/N1000，H2.75/3/3.25%×退出缓冲E0.75/1/1.25%；strictH入场优先，区间内旧long在ROC>-E时持有、旧short在ROC<E时持有，等于退出边界即平仓。反手先平后开，同方向留实际数量，不日再平衡。ETH固定C15000/N4500、L5/H2%/E0.75%、finiteEWM24 beta23/25、D7/K2%、entry-only V10样本logvol上限4.5%。Raw[1,1]相加完整银行，总本金18750，20/80资本份额不重复乘、不归一化、不缩放旧NAV/数量/成本，无父订单/转账/交叉保证金。

370日连续OOS：2025-10-19UTC00:01至2026-10-24UTC00:01，12×30日完整折＋10日尾；近期40日继承day330现金/持仓8×5日，无折间重开。BTC需30过去完整收盘、ETH需31，源33足够；过去完整收盘发信号，下一00:01OPEN执行，终点计成本平仓。固定规则无fit/labels，purge/embargo0。报告逐折和完整OOS整体DD；重复开发历史及多重选择不能叫未触碰最终、独立未来或稳定实盘盈利。

每边5bp费＋1bp半价差＋2bp滑点；冲击0.5×过去20完整日样本logvol×sqrt(实际q×OPEN/过去20日quoteADV)。1/2/3倍执行成本与资金费支出、收入不放大；真实fundingTime/rate/mark/当时q，线性永续无现货借币。LOT/tick/minnotional、参与率<=0.1%、费后1倍入场抵押、1%闭合小时不利mark保证金代理核验；缺L2/TCA/完整层级/逐tick强平与真实容量证据。

H/E两轴原生和组合各9格，E1%三格只读；索引半径1含中心。保留全部变体收益/整体DD/Sharpe/Calmar、72邻接边、平台/孤峰/边界。门槛原样：全期各成本净正、1倍>=9/12正月、近期各成本净正且>=6/8正五日、3倍DD<=25%、局部三倍净正及严格近期合格率>=60%、>=4原生平仓、毛PnL+资金费/1倍成本>=2.5、零抵押/订单/风险违规、终点flat、>=180日。与同本金/名义常持有及现金0%比较，不以本轮结果改门槛。

|新配置|类别|BTC L|H|E|1x净%|2x净%|3x净%|3x整体DD%|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|btcHysteresis370_BTC_L29_H275bp_E7500ppm|native|29|0.0275|0.0075|9.070767|7.521937|5.973157|6.811608|5/5/5|rejected|
|btcHysteresis370_BTC_L29_H300bp_E7500ppm|native|29|0.03|0.0075|11.694336|10.187994|8.681664|6.811608|5/5/5|rejected|
|btcHysteresis370_BTC_L29_H325bp_E7500ppm|native|29|0.0325|0.0075|11.156338|9.653478|8.150629|6.811608|5/5/5|rejected|
|btcHysteresis370_BTC_L29_H275bp_E12500ppm|native|29|0.0275|0.0125|8.224960|6.695510|5.166035|6.856407|5/5/5|rejected|
|btcHysteresis370_BTC_L29_H300bp_E12500ppm|native|29|0.03|0.0125|10.848529|9.361567|7.874542|6.856407|5/5/5|rejected|
|btcHysteresis370_BTC_L29_H325bp_E12500ppm|native|29|0.0325|0.0125|10.310531|8.827051|7.343507|6.856407|5/5/5|rejected|
|btcHysteresis370_parent_L29_H275bp_E7500ppm|parent|29|0.0275|0.0075|13.967745|12.750644|11.533885|3.695519|6/6/6|passed|
|btcHysteresis370_parent_L29_H300bp_E7500ppm|parent|29|0.03|0.0075|14.492459|13.283855|12.075587|3.695519|6/6/6|passed|
|btcHysteresis370_parent_L29_H325bp_E7500ppm|parent|29|0.0325|0.0075|14.384859|13.176952|11.969380|3.695519|6/6/6|passed|
|btcHysteresis370_parent_L29_H275bp_E12500ppm|parent|29|0.0275|0.0125|13.798583|12.585358|11.372461|3.700467|6/6/6|passed|
|btcHysteresis370_parent_L29_H300bp_E12500ppm|parent|29|0.03|0.0125|14.323297|13.118570|11.914162|3.700467|6/6/6|passed|
|btcHysteresis370_parent_L29_H325bp_E12500ppm|parent|29|0.0325|0.0125|14.215698|13.011666|11.807955|3.700467|6/6/6|passed|

逐项失败判据：{'btcHysteresis370_BTC_L29_H275bp_E7500ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcHysteresis370_BTC_L29_H300bp_E7500ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcHysteresis370_BTC_L29_H325bp_E7500ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcHysteresis370_BTC_L29_H275bp_E12500ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcHysteresis370_BTC_L29_H300bp_E12500ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcHysteresis370_BTC_L29_H325bp_E12500ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcHysteresis370_parent_L29_H275bp_E7500ppm': [], 'btcHysteresis370_parent_L29_H300bp_E7500ppm': [], 'btcHysteresis370_parent_L29_H325bp_E7500ppm': [], 'btcHysteresis370_parent_L29_H275bp_E12500ppm': [], 'btcHysteresis370_parent_L29_H300bp_E12500ppm': [], 'btcHysteresis370_parent_L29_H325bp_E12500ppm': []}。

原四冻结账户独立续自己的现金/实际q/成本/风险/fullNAV，不采用研究E。SMA/single Nov7_12:30→14:30，L4/FEWM14:10→16:10。无新日决策或成交，L4/FEWM在真实16时结算各自资金费；single本窗未跨16，SMA现货无资金费。各自00/08不重复，16仅按各自真实窗口和持仓独立结算。四者不复制现金流、不从现金重开。各自下一日决策Nov8_00:01。SMA最后完整65日源仍R024625，当前和上一续接输入为minute数组。所有原账户partial延迟shadow，不是十策略实时报价模拟业绩或180日资格。

同main排他锁内finish和必要检查后生成只读monitor并检查；保存全部正负折、变体、完整账户账本/冻结规则/登记/必要真实输入，仅清理可重建中间物。无真实订单、页面重部署或新定时任务。实际非强制push、完整远端tree/blob核验与解锁终态见.git/automation_proofs/20261107T165106Z.json。
