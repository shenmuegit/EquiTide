本轮局部K×E扰动的12个新定义全部复现既往同本金/同名义、同时间边界的三成本完整净值路径，没有增加独立路径或收益优势。E0.625%的6项与同K旧E0.75%路径完全相同；E0.875%的6项被同K旧E0.75%在三成本下严格支配，并匹配既往较宽E的实际路径。6组合达到冻结历史门槛、6ETH单组件因近期及局部一致性不足淘汰。相邻Sharpe跳变仍在，不能把局部别名或历史通过称为平坦平台、独立前向或实盘盈利。

本轮6新ETH退出缓冲配置＋6新组合，36场景实际回测；组合历史通过6/6、淘汰0/6，旧E0.75%/VC5%三K列只读。

上一轮固定VC5%的较宽K/E网格中E0.75%相对同K的E1%改善；本轮检验该点附近是否为稳定区而非退出边界。固定ETH S16/beta15/17、D3、ROC5/H2%、V10样本logvol上限VC5%，预设K0.5%/0.75%/1% × E0.625%/0.75%/0.875%。旧E0.75%同K三列只读，6个新ETH组件与6个父组合逐项reserve后实际计算。更窄或更宽E可改变持有天数/换手与费用，完整保留别名、负折和失败；代表预定K0.5%/E0.625%，不在看结果后改变规则、权重、门槛或时间。BTC29H3E1 C3750/N1000只读、ETH C15000/N4500，raw1/1相加两个完整独立银行18750，不归一化或缩放。连续370日12×30+10尾段，近期40继承day330分8×5；三成本含费用、量冲击及实际资金费。重复开发历史不称未触碰最终、独立前向或稳定实盘。本轮SMA/single12:30→14:30仅mark；L4/FEWM14:10→16:10使用新实际Nov9_16.001字段及自身q/cash结算，不复制现金流或采用研究参数。

完整读取31364登记事件/15560ID、361份既往结论。初始16项真实历史证据齐全，缺0；此前规范研究定义10477，标实际10264、未标实际213；不称全部登记均有结果。

固定BTC signedROC29/H3%/E1%、C3750/N1000只读；ETH C15000/N4500，反向ROC5/H2%、退出E0.625%/0.75%/0.875%、斜率间隔D3，有限归一EWM窗口S16、beta=(S-1)/(S+1)，严格斜率门槛K0.5/0.75/1%。entry H优先，保留原long当ROC<E、原short当ROC>-E，边界相等退出。慢趋势和V10样本logvol上限固定VC5%只过滤新开/反手，保留同向实际q，反手先平后开，无日再平衡。所有新E的数量、LOT、冲击、费用、资金费、风险和NAV实际计算。

Raw[1,1]相加两个独立完整银行NAV，总本金18750，资金占比20/80%不重复乘，不归一化或缩放旧q/NAV/成本。BTC初始名义为本银行26.666667%/总本5.333333%，ETH为本银行30%/总本24%；无父订单、转账、再平衡或交叉保证金。

连续370日开发OOS：2025-10-19UTC00:01至2026-10-24UTC00:01，12×30日完整折和10日尾；近期40日继承day330状态分8×5日，折间不重开。ETH信号最大19、成本需21个过去收盘（合需21），BTC需30，统一初始真实33日。只用完整过去数据，下一UTC00:01 OPEN执行，终点计成本平仓。固定规则无fit/labels，purge/embargo0。逐折及完整连续DD留档；反复开发历史和多重选择不是未触碰最终、独立未来或稳定实盘盈利。

每边5bp手续费+1bp半价差+2bp滑点；冲击0.5×过去20完整日样本logvol×sqrt(实际q×OPEN/过去20日quoteADV)。1/2/3倍执行成本及资金费支出，收入不放大；实际fundingTime/rate/mark/当时q。线性永续无现货借币，核对LOT/tick/minnotional、参与率≤0.1%、费后1倍入场抵押、1%闭合小时不利mark风险代理。缺L2/TCA、历史完整保证金层级/逐tick强平和真实容量证据。

K/E原生和父组合各九格，旧E0.75%/VC5%列只读，索引半径1含中心；全变体收益/整体DD/Sharpe/Calmar、72邻接边、边界和跳变留档。未定义统计留None/N/A、不填0，保留全部格。门槛不变：全期及近期各成本净正、1x≥9/12正30日、各成本近期≥6/8正5日、3xDD≤25%、局部3x净正及严格近期合格率≥60%、至少4原生平仓、毛PnL+资金费/1x成本≥2.5、无抵押/订单/风险违规、终点flat、≥180日。匹配同C/N实际常持有与现金0%，不据结果改门槛。

|新配置|类别|固定D|S|E|固定VC|K|1x净%|2x净%|3x净%|3x整体DD%|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
|exitlocalvc5_370_ETH_D3_K5000ppm_S16_L5_H200bp_E6250ppm_VC50000ppm|native|3|16|0.00625|0.05|0.005|14.368230|13.352857|12.337862|4.417065|2/2/2|rejected|
|exitlocalvc5_370_ETH_D3_K5000ppm_S16_L5_H200bp_E8750ppm_VC50000ppm|native|3|16|0.00875|0.05|0.005|13.874262|12.858465|11.843046|4.532974|2/2/2|rejected|
|exitlocalvc5_370_ETH_D3_K7500ppm_S16_L5_H200bp_E6250ppm_VC50000ppm|native|3|16|0.00625|0.05|0.0075|16.721251|15.828040|14.935209|4.080065|2/2/2|rejected|
|exitlocalvc5_370_ETH_D3_K7500ppm_S16_L5_H200bp_E8750ppm_VC50000ppm|native|3|16|0.00875|0.05|0.0075|16.243405|15.349779|14.456534|4.080065|2/2/2|rejected|
|exitlocalvc5_370_ETH_D3_K10000ppm_S16_L5_H200bp_E6250ppm_VC50000ppm|native|3|16|0.00625|0.05|0.01|15.282476|14.488523|13.694913|4.080065|1/1/1|rejected|
|exitlocalvc5_370_ETH_D3_K10000ppm_S16_L5_H200bp_E8750ppm_VC50000ppm|native|3|16|0.00875|0.05|0.01|14.804629|14.010262|13.216238|4.080065|1/1/1|rejected|
|exitlocalvc5_370_parent_BTC29H3_D3_K5000ppm_S16_L5_H200bp_E6250ppm_VC50000ppm|parent|3|16|0.00625|0.05|0.005|13.894485|12.786225|11.678273|4.091074|6/6/6|passed|
|exitlocalvc5_370_parent_BTC29H3_D3_K5000ppm_S16_L5_H200bp_E8750ppm_VC50000ppm|parent|3|16|0.00875|0.05|0.005|13.499311|12.390712|11.282420|4.091074|6/6/6|passed|
|exitlocalvc5_370_parent_BTC29H3_D3_K7500ppm_S16_L5_H200bp_E6250ppm_VC50000ppm|parent|3|16|0.00625|0.05|0.0075|15.776902|14.766372|13.756150|3.082168|6/6/6|passed|
|exitlocalvc5_370_parent_BTC29H3_D3_K7500ppm_S16_L5_H200bp_E8750ppm_VC50000ppm|parent|3|16|0.00875|0.05|0.0075|15.394624|14.383763|13.373210|3.082168|6/6/6|passed|
|exitlocalvc5_370_parent_BTC29H3_D3_K10000ppm_S16_L5_H200bp_E6250ppm_VC50000ppm|parent|3|16|0.00625|0.05|0.01|14.625881|13.694758|12.763913|3.082168|6/6/6|passed|
|exitlocalvc5_370_parent_BTC29H3_D3_K10000ppm_S16_L5_H200bp_E8750ppm_VC50000ppm|parent|3|16|0.00875|0.05|0.01|14.243604|13.312150|12.380973|3.082168|6/6/6|passed|

逐项失败判据：{'exitlocalvc5_370_ETH_D3_K5000ppm_S16_L5_H200bp_E6250ppm_VC50000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'exitlocalvc5_370_ETH_D3_K5000ppm_S16_L5_H200bp_E8750ppm_VC50000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'exitlocalvc5_370_ETH_D3_K7500ppm_S16_L5_H200bp_E6250ppm_VC50000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'exitlocalvc5_370_ETH_D3_K7500ppm_S16_L5_H200bp_E8750ppm_VC50000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'exitlocalvc5_370_ETH_D3_K10000ppm_S16_L5_H200bp_E6250ppm_VC50000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'exitlocalvc5_370_ETH_D3_K10000ppm_S16_L5_H200bp_E8750ppm_VC50000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'exitlocalvc5_370_parent_BTC29H3_D3_K5000ppm_S16_L5_H200bp_E6250ppm_VC50000ppm': [], 'exitlocalvc5_370_parent_BTC29H3_D3_K5000ppm_S16_L5_H200bp_E8750ppm_VC50000ppm': [], 'exitlocalvc5_370_parent_BTC29H3_D3_K7500ppm_S16_L5_H200bp_E6250ppm_VC50000ppm': [], 'exitlocalvc5_370_parent_BTC29H3_D3_K7500ppm_S16_L5_H200bp_E8750ppm_VC50000ppm': [], 'exitlocalvc5_370_parent_BTC29H3_D3_K10000ppm_S16_L5_H200bp_E6250ppm_VC50000ppm': [], 'exitlocalvc5_370_parent_BTC29H3_D3_K10000ppm_S16_L5_H200bp_E8750ppm_VC50000ppm': []}。

四个原冻结账户延续各自现金/q/desired/费用、风险和完整NAV，不采用本轮研究E/K。本窗SMA/single12:30→14:30仅闭合mark；L4/FEWM14:10→16:10跨Nov9_16:00:00.001，以本次真实官方fundingTime/rate/mark和各自结算前q/cash独立核算，收入不放大。历史08各一次、无新日决策/成交，不提前给single结算16。下一窗single14:30→16:30才跨16；L4/FEWM16:10→18:10仅mark；下一日决策Nov10，SMA完整65上下文R030420保留。均为partial延迟shadow，非十策略实时报价或180日资格。

完成finish和必要检查后，在同main排他锁内运行只读monitor及原生检查。保留全部正负/失败、冻结规则、完整账本、登记和必要真实输入，清理可重建中间物。无真实订单、页面重部署或新定时任务。实际main push、完整远端tree/blob与解锁终态见.git/automation_proofs/20261109T170751Z.json。

历史spec中的warmup_days30/embargo_days3和persistence旧E.005文字为未被执行器读取的继承描述；本轮实际前置33个完整收盘，无fit/labels和折间purge/embargo，当前每个spec数值E及完整规则为执行依据，详见冻结rules.legacy_parameter_fields。

本轮两次真实辅助检查失败均完整留档：源核验在登记片段整理前运行，原检查在完成既有整理后退出0；审计辅助脚本的输出字段在绑定后改动，被哈希门禁捕获，已恢复绑定字节、保存当时执行版本并另存准确范围的只读检查，原账户窗口检查重新退出0。36根执行源、全部金融/账户报告及规则/门槛保持原字节，没有金融或账户重跑。

监控本轮生成/原生校验成功：True；本轮新增研究展示12条、待恢复后展示0条。若失败，原生非零退出/生成快照/旧有效文件哈希留档，保留上次有效汇总，未修改检查门槛、账户或规则。
同K、同C/N的旧E0.75%/VC5%/S16/D3/H2%对照在1/2/3倍成本下收益不低且整体DD不高、每个成本至少一项严格改善的当前配置数：6/12。本轮组合历史通过6项；各成本收益不低且整体回撤不高、至少一项严格改善的当前配置数0/12。逐项比较留档，不替换冻结账户，不建立新前向账户。
封存：6新ETH退出缓冲组件＋6新组合/36场景，组合通过6、淘汰0；24ID/48事件全部finish，53479旧文件保持。18旧原生路径只读，18新ETH原生路径/6660实际决策及18新组合路径独立核验。
原SMA NAV55509→55629，single 19916→20038，L4 12653→12777，FEWM 6761→6885。single/L4/FEWM实际新资金费0/6/6，日事件0/0/0，成交0/0/0；各自实际资金费时间戳/rate/mark/结算前q与本窗闭合mark独立核验，旧00/00:01仅保留已验证历史证明，原现金/q/风险/fullNAV连续，不复制现金流或重复16/00。FEWM累计6729分钟/171ID，所有账户partial非180日资格。
只读监控10048行，原10036行不变，10报价账户/309观察，gzip4609130字节。HTTP/传输失败0次原证据保留，所有正负/淘汰结果、完整账本/冻结规则/登记/必要输入保留。真实main push、完整远端tree/blob与解锁终态见.git/automation_proofs/20261109T170751Z.json。
