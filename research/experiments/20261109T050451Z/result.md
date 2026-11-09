本轮6新ETH退出缓冲配置＋6新组合，36场景实际回测；组合历史通过6/6、淘汰0/6，旧E1%三K列只读。

上轮延长S18/20有6组合历史通过，但12新定义中10个被同K旧S16在1/2/3倍成本下收益和整体DD支配，ETH近期仅1或2/8正折。本轮转向退出持仓缓冲：固定有限EWM S16/beta15/17、D3、ROC5/H2%、entry-only V10cap4.5%；事先冻结K0.5%/0.75%/1% × E1%/1.25%/1.5%。更宽E使原long在ROC<E、原short在ROC>-E时继续持有，可能减少过早退出和成本，也可能延长逆势风险；entry H严格优先，E<H，不根据OOS改门槛。旧E1%三K列只读，六个新ETH E1.25/1.5%组件及六新组合先逐项reserve再计算。代表预定K0.5%/E1.25%/S16，不据结果替换。BTC29/H3/E1银行C3750/N1000只读，ETHC15000/N4500，raw1/1表示两个完整独立银行NAV相加18750不归一化/缩放。370日连续12×30+10尾段、继承日330的近期8×5折、两轴K/E敏感性及1/2/3实际执行成本和资金费压力；反复开发及多重选择非未触碰最终、独立未来或稳定实盘。原四冻结账户不采用研究参数，本轮四窗均仅闭合mark。

完整读取30956登记事件/15356ID、355份既往结论。初始16项真实历史证据齐全，缺0；此前规范研究定义10405，标实际10192、未标实际213；不称全部登记均有结果。

固定BTC signedROC29/H3%/E1%、C3750/N1000只读；ETH C15000/N4500，反向ROC5/H2%、退出E1/1.25/1.5%、斜率间隔D3，有限归一EWM窗口S16、beta=(S-1)/(S+1)，严格斜率门槛K0.5/0.75/1%。entry H优先，保留原long当ROC<E、原short当ROC>-E，边界相等退出。慢趋势和V10样本logvol上限4.5%只过滤新开/反手，保留同向实际q，反手先平后开，无日再平衡。所有新E的数量、LOT、冲击、费用、资金费、风险和NAV实际计算。

Raw[1,1]相加两个独立完整银行NAV，总本金18750，资金占比20/80%不重复乘，不归一化或缩放旧q/NAV/成本。BTC初始名义为本银行26.666667%/总本5.333333%，ETH为本银行30%/总本24%；无父订单、转账、再平衡或交叉保证金。

连续370日开发OOS：2025-10-19UTC00:01至2026-10-24UTC00:01，12×30日完整折和10日尾；近期40日继承day330状态分8×5日，折间不重开。ETH信号最大19、成本需21个过去收盘（合需21），BTC需30，统一初始真实33日。只用完整过去数据，下一UTC00:01 OPEN执行，终点计成本平仓。固定规则无fit/labels，purge/embargo0。逐折及完整连续DD留档；反复开发历史和多重选择不是未触碰最终、独立未来或稳定实盘盈利。

每边5bp手续费+1bp半价差+2bp滑点；冲击0.5×过去20完整日样本logvol×sqrt(实际q×OPEN/过去20日quoteADV)。1/2/3倍执行成本及资金费支出，收入不放大；实际fundingTime/rate/mark/当时q。线性永续无现货借币，核对LOT/tick/minnotional、参与率≤0.1%、费后1倍入场抵押、1%闭合小时不利mark风险代理。缺L2/TCA、历史完整保证金层级/逐tick强平和真实容量证据。

K/E原生和父组合各九格，旧E1%列只读，索引半径1含中心；全变体收益/整体DD/Sharpe/Calmar、72邻接边、边界和跳变留档。未定义统计留None/N/A、不填0，保留全部格。门槛不变：全期及近期各成本净正、1x≥9/12正30日、各成本近期≥6/8正5日、3xDD≤25%、局部3x净正及严格近期合格率≥60%、至少4原生平仓、毛PnL+资金费/1x成本≥2.5、无抵押/订单/风险违规、终点flat、≥180日。匹配同C/N实际常持有与现金0%，不据结果改门槛。

|新配置|类别|固定D|S|E|K|1x净%|2x净%|3x净%|3x整体DD%|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
|strength370_ETH_D3_K5000ppm_S16_L5_H200bp_E12500ppm|native|3|16|0.0125|0.005|12.042508|11.179507|10.316711|4.537987|2/2/2|rejected|
|strength370_ETH_D3_K5000ppm_S16_L5_H200bp_E15000ppm|native|3|16|0.015|0.005|11.280344|10.402085|9.524029|4.537987|2/2/2|rejected|
|strength370_ETH_D3_K7500ppm_S16_L5_H200bp_E12500ppm|native|3|16|0.0125|0.0075|14.411651|13.670822|12.930199|2.050018|2/2/2|rejected|
|strength370_ETH_D3_K7500ppm_S16_L5_H200bp_E15000ppm|native|3|16|0.015|0.0075|13.649487|12.893399|12.137517|3.340466|2/2/2|rejected|
|strength370_ETH_D3_K10000ppm_S16_L5_H200bp_E12500ppm|native|3|16|0.0125|0.01|12.972875|12.331305|11.689903|2.050018|1/1/1|rejected|
|strength370_ETH_D3_K10000ppm_S16_L5_H200bp_E15000ppm|native|3|16|0.015|0.01|12.210711|11.553882|10.897220|3.340466|1/1/1|rejected|
|strength370_parent_BTC29H3_D3_K5000ppm_S16_L5_H200bp_E12500ppm|parent|3|16|0.0125|0.005|12.033907|11.047546|10.061352|4.180988|6/6/6|passed|
|strength370_parent_BTC29H3_D3_K5000ppm_S16_L5_H200bp_E15000ppm|parent|3|16|0.015|0.005|11.424176|10.425608|9.427206|4.180988|6/6/6|passed|
|strength370_parent_BTC29H3_D3_K7500ppm_S16_L5_H200bp_E12500ppm|parent|3|16|0.0125|0.0075|13.929221|13.040598|12.152142|2.214788|6/6/6|passed|
|strength370_parent_BTC29H3_D3_K7500ppm_S16_L5_H200bp_E15000ppm|parent|3|16|0.015|0.0075|13.319490|12.418659|11.517996|3.434330|6/6/6|passed|
|strength370_parent_BTC29H3_D3_K10000ppm_S16_L5_H200bp_E12500ppm|parent|3|16|0.0125|0.01|12.778201|11.968984|11.159905|2.214788|6/6/6|passed|
|strength370_parent_BTC29H3_D3_K10000ppm_S16_L5_H200bp_E15000ppm|parent|3|16|0.015|0.01|12.168470|11.347046|10.525759|3.434330|6/6/6|passed|

逐项失败判据：{'strength370_ETH_D3_K5000ppm_S16_L5_H200bp_E12500ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'strength370_ETH_D3_K5000ppm_S16_L5_H200bp_E15000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'strength370_ETH_D3_K7500ppm_S16_L5_H200bp_E12500ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'strength370_ETH_D3_K7500ppm_S16_L5_H200bp_E15000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'strength370_ETH_D3_K10000ppm_S16_L5_H200bp_E12500ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'strength370_ETH_D3_K10000ppm_S16_L5_H200bp_E15000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'strength370_parent_BTC29H3_D3_K5000ppm_S16_L5_H200bp_E12500ppm': [], 'strength370_parent_BTC29H3_D3_K5000ppm_S16_L5_H200bp_E15000ppm': [], 'strength370_parent_BTC29H3_D3_K7500ppm_S16_L5_H200bp_E12500ppm': [], 'strength370_parent_BTC29H3_D3_K7500ppm_S16_L5_H200bp_E15000ppm': [], 'strength370_parent_BTC29H3_D3_K10000ppm_S16_L5_H200bp_E12500ppm': [], 'strength370_parent_BTC29H3_D3_K10000ppm_S16_L5_H200bp_E15000ppm': []}。

四个原冻结账户延续原现金/q/desired/成本、风险和完整NAV，不采用本轮研究参数。SMA/single Nov9_00:30→02:30，L4/FEWM Nov9_02:10→04:10均只增加闭合分钟mark与适用闭合小时风险核验；原Nov9午夜资金费/日决策已各自完成，不重复结算，不增加新成交。SMA保留上轮真实65日输入及完整自身NAV，核对旧字典1d/1m与新分钟数组重叠；当前交接来源从真实report推导纠正陈旧字段，旧报告/状态原字节保留。皆partial延迟shadow，不是十策略实时报价模拟或180日资格。

完成finish和必要检查后，在同main排他锁内运行只读monitor及原生检查。保留全部正负/失败、冻结规则、完整账本、登记和必要真实输入，清理可重建中间物。无真实订单、页面重部署或新定时任务。实际main push、完整远端tree/blob与解锁终态见.git/automation_proofs/20261109T050451Z.json。

历史spec中的warmup_days30/embargo_days3和persistence旧E.005文字为未被执行器读取的继承描述；本轮实际前置33个完整收盘，无fit/labels和折间purge/embargo，当前每个spec数值E及完整规则为执行依据，详见冻结rules.legacy_parameter_fields。

方向结论：6个E1.25%定义的三成本完整净值路径已在既往结果中出现；它们仍是不同数值参数的实际新配置，但不是6份独立行情证据。6个E1.5%定义在全部1/2/3倍成本下被同K旧E1%严格支配（收益不低、整体DD不高且每成本至少一项严格优）；0个新定义全面优于旧对照。因此本轮退出缓冲扩展未发现稳健改善，不采用到冻结账户。六组合虽通过原历史门槛，六ETH组件仍因近期仅1或2/8正折及局部近期门槛失败淘汰；K1%的两项另未达9/12正30日折。

四账户本轮均仅补闭合mark：SMA NAV54789→54909，single19182→19304，L4 11919→12041，FEWM6027→6149；现金、q、desired、费用及完整NAV前缀不变，0资金费/日事件/成交。SMA仍为38日partial，1/2/3倍累计-6.982980%/-7.226287%/-7.468958%，负收益完整保存。三永续Nov9午夜各自6笔资金费及6笔日决策在完整自身链中仅一次，SMA原日决策两资产各一次。已核对并纠正本轮交接中的SMA65日来源为上轮实际报告指向的20261109T030420Z/forward_inputs.json.gz；旧状态、报告和原始数据均不修改。两次实际TLS35访问失败经有限重试恢复，原响应、stderr和真实退出码留档，无账户重跑。

监控本轮生成/原生校验成功：True；本轮新增研究展示12条、待恢复后展示0条。若失败，原生非零退出/生成快照/旧有效文件哈希留档，保留上次有效汇总，未修改检查门槛、账户或规则。
同K、同C/N的旧E1%/S16/D3/H2%对照在1/2/3倍成本下收益不低且整体DD不高、每个成本至少一项严格改善的当前配置数：6/12。本轮组合历史通过6项；各成本收益不低且整体回撤不高、至少一项严格改善的当前配置数0/12。逐项比较留档，不替换冻结账户，不建立新前向账户。
封存：6新ETH退出缓冲组件＋6新组合/36场景，组合通过6、淘汰0；24ID/48事件全部finish，51122旧文件保持。18旧原生路径只读，18新ETH原生路径/6660实际决策及18新组合路径独立核验。
原SMA NAV54789→54909，single 19182→19304，L4 11919→12041，FEWM 6027→6149。single/L4/FEWM实际新资金费0/0/0，日事件0/0/0，成交0/0/0；各自实际资金费时间戳/rate/mark/结算前q与本窗闭合mark独立核验，旧00/00:01仅保留已验证历史证明，原现金/q/风险/fullNAV连续，不复制现金流或重复16/00。FEWM累计6009分钟/153ID，所有账户partial非180日资格。
只读监控9976行，原9964行不变，10报价账户/303观察，gzip4580795字节。HTTP/传输失败2次原证据保留，所有正负/淘汰结果、完整账本/冻结规则/登记/必要输入保留。真实main push、完整远端tree/blob与解锁终态见.git/automation_proofs/20261109T050451Z.json。
