本轮6新ETH入场波动率上限配置＋6新组合，36场景实际回测；组合历史通过6/6、淘汰0/6，旧VC4.5%三K列只读。

既往放宽/收紧退出E测试多为重合或劣化，K0.5/E0.75的组合三倍收益仅微增0.0129个百分点，近期与DD未改善。本轮改测入场波动率过滤：固定有限EWM S16/beta15/17、D3、ROC5/H2%/E1%、V10样本logvol，预设K0.5%/0.75%/1% × VC3.5%/4%/4.5%。更低上限可能阻止高波动下的逆势新入场，也可能错过盈利反弹；只过滤新开/反手，同向实际q不因高波动而强平，阻止反手时先平旧后保持空仓，sigma等于上限允许入场。旧VC4.5%三K列只读，新VC3.5%/4%六ETH组件与六新组合逐项reserve后实际计算。代表预定K0.5%/VC4%/E1%/S16，不按结果调网格/权重/门槛。BTC29/H3/E1银行C3750/N1000只读，ETHC15000/N4500，raw1/1为两完整独立银行NAV相加18750、不归一化或缩放旧曲线。370日连续12×30+10尾段、继承day330近期8×5折、两轴K/VC与1/2/3实际交易成本和资金费压力；反复开发历史/多重选择不是未触碰最终、独立未来或稳定实盘。原冻结四账户不采用研究参数；本轮L4/FEWM各自08资金费按新实际fundingTime/rate/mark与自身原q核算，single/SMA当前窗口未跨08。

完整读取31092登记事件/15424ID、357份既往结论。初始16项真实历史证据齐全，缺0；此前规范研究定义10429，标实际10216、未标实际213；不称全部登记均有结果。

固定BTC signedROC29/H3%/E1%、C3750/N1000只读；ETH C15000/N4500，反向ROC5/H2%、退出E1%、斜率间隔D3，有限归一EWM窗口S16、beta=(S-1)/(S+1)，严格斜率门槛K0.5/0.75/1%。entry H优先，保留原long当ROC<E、原short当ROC>-E，边界相等退出。慢趋势和V10样本logvol上限VC3.5/4/4.5%只过滤新开/反手，保留同向实际q，反手先平后开，无日再平衡。所有新VC的数量、LOT、冲击、费用、资金费、风险和NAV实际计算。

Raw[1,1]相加两个独立完整银行NAV，总本金18750，资金占比20/80%不重复乘，不归一化或缩放旧q/NAV/成本。BTC初始名义为本银行26.666667%/总本5.333333%，ETH为本银行30%/总本24%；无父订单、转账、再平衡或交叉保证金。

连续370日开发OOS：2025-10-19UTC00:01至2026-10-24UTC00:01，12×30日完整折和10日尾；近期40日继承day330状态分8×5日，折间不重开。ETH信号最大19、成本需21个过去收盘（合需21），BTC需30，统一初始真实33日。只用完整过去数据，下一UTC00:01 OPEN执行，终点计成本平仓。固定规则无fit/labels，purge/embargo0。逐折及完整连续DD留档；反复开发历史和多重选择不是未触碰最终、独立未来或稳定实盘盈利。

每边5bp手续费+1bp半价差+2bp滑点；冲击0.5×过去20完整日样本logvol×sqrt(实际q×OPEN/过去20日quoteADV)。1/2/3倍执行成本及资金费支出，收入不放大；实际fundingTime/rate/mark/当时q。线性永续无现货借币，核对LOT/tick/minnotional、参与率≤0.1%、费后1倍入场抵押、1%闭合小时不利mark风险代理。缺L2/TCA、历史完整保证金层级/逐tick强平和真实容量证据。

K/VC原生和父组合各九格，旧VC4.5%列只读，索引半径1含中心；全变体收益/整体DD/Sharpe/Calmar、72邻接边、边界和跳变留档。未定义统计留None/N/A、不填0，保留全部格。门槛不变：全期及近期各成本净正、1x≥9/12正30日、各成本近期≥6/8正5日、3xDD≤25%、局部3x净正及严格近期合格率≥60%、至少4原生平仓、毛PnL+资金费/1x成本≥2.5、无抵押/订单/风险违规、终点flat、≥180日。匹配同C/N实际常持有与现金0%，不据结果改门槛。

|新配置|类别|固定D|S|固定E|VC|K|1x净%|2x净%|3x净%|3x整体DD%|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
|volcap370_ETH_D3_K5000ppm_S16_L5_H200bp_E10000ppm_VC35000ppm|native|3|16|0.01|0.035|0.005|5.878882|5.231465|4.584237|4.597594|2/2/2|rejected|
|volcap370_ETH_D3_K5000ppm_S16_L5_H200bp_E10000ppm_VC40000ppm|native|3|16|0.01|0.04|0.005|8.433169|7.680182|6.927253|4.597594|2/2/2|rejected|
|volcap370_ETH_D3_K7500ppm_S16_L5_H200bp_E10000ppm_VC35000ppm|native|3|16|0.01|0.035|0.0075|8.248025|7.722780|7.197725|2.079751|2/2/2|rejected|
|volcap370_ETH_D3_K7500ppm_S16_L5_H200bp_E10000ppm_VC40000ppm|native|3|16|0.01|0.04|0.0075|10.802311|10.171497|9.540741|2.050018|2/2/2|rejected|
|volcap370_ETH_D3_K10000ppm_S16_L5_H200bp_E10000ppm_VC35000ppm|native|3|16|0.01|0.035|0.01|6.809249|6.383263|5.957429|2.079751|1/1/1|rejected|
|volcap370_ETH_D3_K10000ppm_S16_L5_H200bp_E10000ppm_VC40000ppm|native|3|16|0.01|0.04|0.01|9.363536|8.831980|8.300444|2.050018|1/1/1|rejected|
|volcap370_parent_BTC29H3_D3_K5000ppm_S16_L5_H200bp_E10000ppm_VC35000ppm|parent|3|16|0.01|0.035|0.005|7.103007|6.289112|5.475373|4.691495|6/6/6|passed|
|volcap370_parent_BTC29H3_D3_K5000ppm_S16_L5_H200bp_E10000ppm_VC40000ppm|parent|3|16|0.01|0.04|0.005|9.146436|8.248086|7.349785|4.691495|6/6/6|passed|
|volcap370_parent_BTC29H3_D3_K7500ppm_S16_L5_H200bp_E10000ppm_VC35000ppm|parent|3|16|0.01|0.035|0.0075|8.998320|8.282164|7.566163|2.163648|6/6/6|passed|
|volcap370_parent_BTC29H3_D3_K7500ppm_S16_L5_H200bp_E10000ppm_VC40000ppm|parent|3|16|0.01|0.04|0.0075|11.041750|10.241137|9.440575|2.132977|6/6/6|passed|
|volcap370_parent_BTC29H3_D3_K10000ppm_S16_L5_H200bp_E10000ppm_VC35000ppm|parent|3|16|0.01|0.035|0.01|7.847300|7.210550|6.573926|2.163648|6/6/6|passed|
|volcap370_parent_BTC29H3_D3_K10000ppm_S16_L5_H200bp_E10000ppm_VC40000ppm|parent|3|16|0.01|0.04|0.01|9.890729|9.169524|8.448338|2.132977|6/6/6|passed|

逐项失败判据：{'volcap370_ETH_D3_K5000ppm_S16_L5_H200bp_E10000ppm_VC35000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volcap370_ETH_D3_K5000ppm_S16_L5_H200bp_E10000ppm_VC40000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volcap370_ETH_D3_K7500ppm_S16_L5_H200bp_E10000ppm_VC35000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volcap370_ETH_D3_K7500ppm_S16_L5_H200bp_E10000ppm_VC40000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volcap370_ETH_D3_K10000ppm_S16_L5_H200bp_E10000ppm_VC35000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volcap370_ETH_D3_K10000ppm_S16_L5_H200bp_E10000ppm_VC40000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volcap370_parent_BTC29H3_D3_K5000ppm_S16_L5_H200bp_E10000ppm_VC35000ppm': [], 'volcap370_parent_BTC29H3_D3_K5000ppm_S16_L5_H200bp_E10000ppm_VC40000ppm': [], 'volcap370_parent_BTC29H3_D3_K7500ppm_S16_L5_H200bp_E10000ppm_VC35000ppm': [], 'volcap370_parent_BTC29H3_D3_K7500ppm_S16_L5_H200bp_E10000ppm_VC40000ppm': [], 'volcap370_parent_BTC29H3_D3_K10000ppm_S16_L5_H200bp_E10000ppm_VC35000ppm': [], 'volcap370_parent_BTC29H3_D3_K10000ppm_S16_L5_H200bp_E10000ppm_VC40000ppm': []}。

四个原冻结账户延续原现金/q/desired/费用、风险与完整NAV，不采用本轮VC参数。SMA/single Nov9_04:30→06:30仅补闭合mark；L4/FEWM Nov9_06:10→08:10各自使用新真实08资金费字段和自身结算前q记账，收入不放大、支出才按成本压力，并补闭合mark/适用小时风险。原午夜和旧Nov8资金费不重复结算；本轮无新日决策/策略交易。Single自身08仍在后续06:30→08:30窗口，不能复制其他账户金额，公开字段仅允许保留原检索UTC和hash只读复用。SMA完整65日上下文仍来自验证的R030420输入，账本不重开；均为partial延迟shadow，非十策略实时报价或180日资格。

完成finish和必要检查后，在同main排他锁内运行只读monitor及原生检查。保留全部正负/失败、冻结规则、完整账本、登记和必要真实输入，清理可重建中间物。无真实订单、页面重部署或新定时任务。实际main push、完整远端tree/blob与解锁终态见.git/automation_proofs/20261109T090618Z.json。

历史spec中的warmup_days30/embargo_days3和persistence旧E.005文字为未被执行器读取的继承描述；本轮实际前置33个完整收盘，无fit/labels和折间purge/embargo，当前每个spec数值E及完整规则为执行依据，详见冻结rules.legacy_parameter_fields。

本轮方向结论：8个新定义在全部1/2/3倍成本下被同K旧VC4.5%严格支配，0个新定义同时改善收益与整体DD。部分组合整体DD较低但收益也降低，属于风险收益取舍；完整历史净值比对还发现2个新定义复现既往三成本路径，此计数可能与前述分类重叠，不作为独立行情证据。6组合按原门槛历史通过，三倍净收益5.475373%–9.440575%、连续整体DD2.132977%–4.691495%；6ETH组件近期仍仅1或2/8正折、局部近期门槛失败，部分另有月折不足，均淘汰。降低入场VC没有建立稳健改善，不采用到冻结账户。全部正收益、负收益、淘汰和重合结果保存。

原账户续接：SMA NAV55029→55149、single19426→19548仅补120分钟；L4 12163→12287、FEWM6271→6395在补mark外各自结算6笔真实08资金费。实际fundingTime为2026-11-09T08:00:00.001Z（1794211200001000000ns），BTC rate0.00010000/mark73839.40000000；L4各成本自身BTC q=-0.006、收入0.04430364 USDT，FEWM q=-0.009、收入0.06645546，收入不放大。ETH rate-0.00004676/mark2092.96000000，各自q=0金额按公式推导为0，字段完整保存。无新成交或日决策，原规则/资本/持仓/完整NAV前缀保持；SMA仍38日partial、1/2/3累计-6.982980%/-7.226287%/-7.468958%，负收益保留。

后续交接：L4/FEWM下一08:10→10:10只补mark，不能再次结算08；single自己当前只到06:30，下一06:30→08:30必须按自身原q/cash处理08。本轮新公开Time/rate/mark/raw可保留原检索UTC/hash只读复用，不能复制其他账户现金流或旧Nov8字段。SMA现货无资金费，下一同窗仍只mark。四账户下一日决策Nov10_00:01，完整65日SMA上下文R030420保留；不重启或采用研究VC。本轮原始公共GET无失败；敏感性图仅缩短拥挤标签重绘，原图/源/日志保留，11份CSV及report原字节核对不变，无金融或账户重算。

监控本轮生成/原生校验成功：True；本轮新增研究展示12条、待恢复后展示0条。若失败，原生非零退出/生成快照/旧有效文件哈希留档，保留上次有效汇总，未修改检查门槛、账户或规则。
同K、同C/N的旧VC4.5%/S16/D3/H2%对照在1/2/3倍成本下收益不低且整体DD不高、每个成本至少一项严格改善的当前配置数：8/12。本轮组合历史通过6项；各成本收益不低且整体回撤不高、至少一项严格改善的当前配置数0/12。逐项比较留档，不替换冻结账户，不建立新前向账户。
封存：6新ETH入场波动率上限组件＋6新组合/36场景，组合通过6、淘汰0；24ID/48事件全部finish，51881旧文件保持。18旧原生路径只读，18新ETH原生路径/6660实际决策及18新组合路径独立核验。
原SMA NAV55029→55149，single 19426→19548，L4 12163→12287，FEWM 6271→6395。single/L4/FEWM实际新资金费0/6/6，日事件0/0/0，成交0/0/0；各自实际资金费时间戳/rate/mark/结算前q与本窗闭合mark独立核验，旧00/00:01仅保留已验证历史证明，原现金/q/风险/fullNAV连续，不复制现金流或重复16/00。FEWM累计6249分钟/159ID，所有账户partial非180日资格。
只读监控10000行，原9988行不变，10报价账户/305观察，gzip4591254字节。HTTP/传输失败0次原证据保留，所有正负/淘汰结果、完整账本/冻结规则/登记/必要输入保留。真实main push、完整远端tree/blob与解锁终态见.git/automation_proofs/20261109T090618Z.json。
