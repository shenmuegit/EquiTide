本轮6新BTC组件＋6新组合/36成本场景实算；新组合通过6/6、淘汰0/6。已有L29的H2.75/3/3.25%三格原组件和组合只读，未重跑或改资格。

前轮H2.75/3.25%与退出缓冲细化后，组合虽历史通过仍未超过旧H3%同E对照。本轮固定退出E1%、BTC C3750/N1000及ETH C15000/N4500，事前检验BTC回看28/29/30日×严格入场2.75/3/3.25%，测试29日优势对相邻周期是否稳健。旧29日三个H的真实组件及组合均只读；28/30日六个新BTC组件和六个新父组合全部先reserve再计算。ETH固定L5/H2%/E0.5%/finiteEWM24/D7/K2%/V10cap4.5%。代表点L30/H3%/E1%事前固定，原失败判据和raw1/1完整银行权重不变，不根据当前结果扩展。所有正负结果保留；反复使用的开发历史不能称独立最终、未来或稳定实盘收益。

完整读取29644事件/14700ID、336既往结论。初始16项实际证据齐全，缺0；此前研究定义10177，标实际9964、未标213，不称所有登记都有结果。

BTC固定C3750/N1000，回看L28/29/30日×H2.75/3/3.25%，退出缓冲E1%；strictH入场优先，区间内旧long在ROC>-E时持有、旧short在ROC<E时持有，等于退出边界即平仓。反手先平后开，同方向留实际数量，不日再平衡。ETH固定C15000/N4500、L5/H2%/E0.5%、finiteEWM24 beta23/25、D7/K2%、entry-only V10样本logvol上限4.5%。Raw[1,1]相加完整银行，总本金18750，20/80资本份额不重复乘、不归一化、不缩放旧NAV/数量/成本，无父订单/转账/交叉保证金。

370日连续OOS：2025-10-19UTC00:01至2026-10-24UTC00:01，12×30日完整折＋10日尾；近期40日继承day330现金/持仓8×5日，无折间重开。BTC最多需31过去完整收盘、ETH需31，源33足够；过去完整收盘发信号，下一00:01OPEN执行，终点计成本平仓。固定规则无fit/labels，purge/embargo0。报告逐折和完整OOS整体DD；重复开发历史及多重选择不能叫未触碰最终、独立未来或稳定实盘盈利。

每边5bp费＋1bp半价差＋2bp滑点；冲击0.5×过去20完整日样本logvol×sqrt(实际q×OPEN/过去20日quoteADV)。1/2/3倍执行成本与资金费支出、收入不放大；真实fundingTime/rate/mark/当时q，线性永续无现货借币。LOT/tick/minnotional、参与率<=0.1%、费后1倍入场抵押、1%闭合小时不利mark保证金代理核验；缺L2/TCA/完整层级/逐tick强平与真实容量证据。

L/H两轴原生和组合各9格，L29三格只读；索引半径1含中心。保留全部变体收益/整体DD/Sharpe/Calmar、72邻接边、平台/孤峰/边界。门槛原样：全期各成本净正、1倍>=9/12正月、近期各成本净正且>=6/8正五日、3倍DD<=25%、局部三倍净正及严格近期合格率>=60%、>=4原生平仓、毛PnL+资金费/1倍成本>=2.5、零抵押/订单/风险违规、终点flat、>=180日。与同本金/名义常持有及现金0%比较，不以本轮结果改门槛。

|新配置|类别|BTC L|H|E|1x净%|2x净%|3x净%|3x整体DD%|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|btcreaction370_BTC_N1000_L28_H275bp|native|28|0.0275|0.01|5.591021|4.034469|2.477895|9.152349|5/5/4|rejected|
|btcreaction370_BTC_N1000_L28_H300bp|native|28|0.03|0.01|9.734965|8.275500|6.815976|7.172932|5/5/4|rejected|
|btcreaction370_BTC_N1000_L28_H325bp|native|28|0.0325|0.01|9.291959|7.835100|6.378152|7.202064|5/5/4|rejected|
|btcreaction370_BTC_N1000_L30_H275bp|native|30|0.0275|0.01|6.734270|5.156011|3.577672|8.021463|5/5/5|rejected|
|btcreaction370_BTC_N1000_L30_H300bp|native|30|0.03|0.01|5.262048|3.693543|2.124957|8.021463|5/5/5|rejected|
|btcreaction370_BTC_N1000_L30_H325bp|native|30|0.0325|0.01|5.262048|3.693543|2.124957|8.021463|5/5/5|rejected|
|btcreaction370_parent_L28_H275bp|parent|28|0.0275|0.01|13.271796|12.053150|10.834833|3.685016|6/6/6|passed|
|btcreaction370_parent_L28_H300bp|parent|28|0.03|0.01|14.100584|12.901356|11.702449|3.685016|6/6/6|passed|
|btcreaction370_parent_L28_H325bp|parent|28|0.0325|0.01|14.011983|12.813276|11.614884|3.688103|6/6/6|passed|
|btcreaction370_parent_L30_H275bp|parent|30|0.0275|0.01|13.500445|12.277458|11.054788|3.692187|6/6/6|passed|
|btcreaction370_parent_L30_H300bp|parent|30|0.03|0.01|13.206001|11.984965|10.764245|3.692187|6/6/6|passed|
|btcreaction370_parent_L30_H325bp|parent|30|0.0325|0.01|13.206001|11.984965|10.764245|3.692187|6/6/6|passed|

逐项失败判据：{'btcreaction370_BTC_N1000_L28_H275bp': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcreaction370_BTC_N1000_L28_H300bp': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcreaction370_BTC_N1000_L28_H325bp': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcreaction370_BTC_N1000_L30_H275bp': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcreaction370_BTC_N1000_L30_H300bp': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcreaction370_BTC_N1000_L30_H325bp': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcreaction370_parent_L28_H275bp': [], 'btcreaction370_parent_L28_H300bp': [], 'btcreaction370_parent_L28_H325bp': [], 'btcreaction370_parent_L30_H275bp': [], 'btcreaction370_parent_L30_H300bp': [], 'btcreaction370_parent_L30_H325bp': []}。

原四冻结账户独立续自己的现金/实际q/成本/风险/fullNAV，不采用研究L/H。SMA/single Nov7_10:30→12:30，L4/FEWM12:10→14:10，均仅闭合mark/风险，无新日决策、资金费或成交。各自08已计入，不重复00/08，未来16只在实际窗口到达时独立结算。四者不复制现金流、不从现金重开。各自下一日决策Nov8_00:01。SMA最后完整65日源仍R024625，当前和上一续接输入为minute数组。所有原账户partial延迟shadow，不是十策略实时报价模拟业绩或180日资格。

同main排他锁内finish和必要检查后生成只读monitor并检查；保存全部正负折、变体、完整账户账本/冻结规则/登记/必要真实输入，仅清理可重建中间物。无真实订单、页面重部署或新定时任务。实际非强制push、完整远端tree/blob核验与解锁终态见.git/automation_proofs/20261107T144905Z.json。

三项实际验证补充：新组合全部1倍有11/12个正30日完整折、各成本近期6/8正五日，局部三倍净正和严格近期合格比例均1。6个BTC单组件只有7或8/12正月、近期3倍4或5/8，局部严格近期比例0，故按原门槛淘汰。参数L/H两轴虽完成且组合9格近期合格，72条邻接边的描述性Sharpe跳变标记均须保留；收益在旧29日附近呈高脊，不据此声称平坦、独立或稳定实盘优势。30日H3与H3.25实际路径相同，仅是本段行情下的实现路径重合，仍按不同参数完整留档。

报告一处继承的诊断scope文本及独立判据日志仍写H/E；实际预登记、邻域计算、独立复核、CSV和图均使用L/H且E固定1%。详见report_label_annotation.json，保留已finish报告与绑定代码原字节，不修改已验证结果。

与相同H/E、相同银行和ETH组件的旧L29真实对照相比，6个新父组合在1/2/3倍下收益均更低，但整体DD略低，因此是收益/回撤取舍，不能写成旧对照同时支配收益和DD。3倍收益差按匹配H为[-0.770702, -0.444787, -0.426145, -0.550747, -1.382991, -1.276784]个百分点。旧主对照L29/H3%/E1%三倍收益12.147236589%、DD3.696238788%；预设L30/H3%/E1%三倍收益10.764245459%、DD3.692187499%。同期同本金/名义常持有三倍收益-12.768930378%、DD20.340098253%，该负收益旧对照完整只读。

已保存净值路径查重：19个既有同本金/名义BTC组件及19个相同ETH父组合的三成本完整NAV哈希/点数/时间边界，无新配置匹配旧三路径；本轮L30的H3与H3.25两组各自三成本路径重合。它们仍是不同规则参数，不能把共享行情下的结果当独立样本。

封存：6新BTC组件＋6新组合/36成本场景，新组合通过6、淘汰0；24ID/48事件全部finish，44227旧保护文件保持。18旧原生成本路径只读，18新BTC原生成本路径/6660实际新决策及18新组合路径独立核验。
原SMA NAV52507→52627，single NAV16848→16970，L4 NAV9585→9707，FEWM NAV3693→3815。single/L4/FEWM实际新资金费记录0/0/0，按各自真实rate/mark/ns/q独立核验；日事件与成交均0，不重复00/08或复制现金流。FEWM累计3729分钟/96ID，全部账户partial、非180日资格。
只读监控9748行，原9736行完整不变，10报价账户/284观察，gzip4472576字节。行情HTTP/传输失败0次原证据保留；所有正负/淘汰结果、完整账本/冻结规则/登记/必要输入保留。实际push、完整远端tree/blob及解锁终态见.git/automation_proofs/20261107T144905Z.json。
