本轮6新ETH斜率门槛配置＋6新组合，36场景实际回测；组合历史通过6/6、淘汰0/6，旧K1%三S行只读。

上轮固定D3、K1%/1.25%×S12/14/16的六组合历史通过，但所有ETH组件近期仅1/8正折，窗口存在路径重合与边界/跳变。本轮预设D3不变，K0.5%/0.75%/1%×S12/14/16、beta=(S-1)/(S+1)，检验继续放松斜率门槛能否改善ETH交易覆盖和近期一致性；也可能放大噪音、换手与成本损失。旧K1%三S行只读，六新ETH与六父组合各自reserve后实际执行；预定代表D3/K0.5%/S12，不据结果扩网格或改门槛。固定BTC29/H3/E1银行C3750/N1000、ETHL5/H2/E1银行C15000/N4500、entry-only V10cap4.5%，raw1/1。成本含手续费/价差/滑点/量冲击/实际资金费，1/2/3压力。真实前置33日、370日连续开发历史；重复开发与多重选择不是未触碰最终、独立未来或稳定实盘盈利。原四前向账户不采用研究参数，本轮L4/FEWM午夜事件按各自冻结规则与新真实数据推进。

完整读取30820登记事件/15288ID、353份既往结论。初始16项真实历史证据齐全，缺0；此前规范研究定义10381，标实际10168、未标实际213；不称全部登记均有结果。

固定BTC signedROC29/H3%/E1%、C3750/N1000只读；ETH C15000/N4500，反向ROC5/H2%、退出E1%、斜率间隔D3，有限归一EWM窗口S12/14/16、beta=(S-1)/(S+1)，严格斜率门槛K0.5/0.75/1%。entry H优先，保留原long当ROC<E、原short当ROC>-E，边界相等退出。慢趋势和V10样本logvol上限4.5%只过滤新开/反手，保留同向实际q，反手先平后开，无日再平衡。所有新K的数量、LOT、冲击、费用、资金费、风险和NAV实际计算。

Raw[1,1]相加两个独立完整银行NAV，总本金18750，资金占比20/80%不重复乘，不归一化或缩放旧q/NAV/成本。BTC初始名义为本银行26.666667%/总本5.333333%，ETH为本银行30%/总本24%；无父订单、转账、再平衡或交叉保证金。

连续370日开发OOS：2025-10-19UTC00:01至2026-10-24UTC00:01，12×30日完整折和10日尾；近期40日继承day330状态分8×5日，折间不重开。ETH信号最大19、成本需21个过去收盘，BTC需30，统一初始真实33日。只用完整过去数据，下一UTC00:01 OPEN执行，终点计成本平仓。固定规则无fit/labels，purge/embargo0。逐折及完整连续DD留档；反复开发历史和多重选择不是未触碰最终、独立未来或稳定实盘盈利。

每边5bp手续费+1bp半价差+2bp滑点；冲击0.5×过去20完整日样本logvol×sqrt(实际q×OPEN/过去20日quoteADV)。1/2/3倍执行成本及资金费支出，收入不放大；实际fundingTime/rate/mark/当时q。线性永续无现货借币，核对LOT/tick/minnotional、参与率≤0.1%、费后1倍入场抵押、1%闭合小时不利mark风险代理。缺L2/TCA、历史完整保证金层级/逐tick强平和真实容量证据。

K/S原生和父组合各九格，旧K1%行只读，索引半径1含中心；全变体收益/整体DD/Sharpe/Calmar、72邻接边、边界和跳变留档。未定义统计留None/N/A、不填0，保留全部格。门槛不变：全期及近期各成本净正、1x≥9/12正30日、各成本近期≥6/8正5日、3xDD≤25%、局部3x净正及严格近期合格率≥60%、至少4原生平仓、毛PnL+资金费/1x成本≥2.5、无抵押/订单/风险违规、终点flat、≥180日。匹配同C/N实际常持有与现金0%，不据结果改门槛。

|新配置|类别|固定D|S|固定E|K|1x净%|2x净%|3x净%|3x整体DD%|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
|strength370_ETH_D3_K5000ppm_S12_L5_H200bp_E10000ppm|native|3|12|0.01|0.005|11.533375|10.802515|10.071980|2.954384|1/1/1|rejected|
|strength370_ETH_D3_K7500ppm_S12_L5_H200bp_E10000ppm|native|3|12|0.01|0.0075|11.977923|11.400061|10.822366|2.050018|1/1/1|rejected|
|strength370_ETH_D3_K5000ppm_S14_L5_H200bp_E10000ppm|native|3|14|0.01|0.005|12.971030|12.176921|11.383016|2.967564|2/2/2|rejected|
|strength370_ETH_D3_K7500ppm_S14_L5_H200bp_E10000ppm|native|3|14|0.01|0.0075|13.391687|12.698381|12.005400|2.050018|1/1/1|rejected|
|strength370_ETH_D3_K5000ppm_S16_L5_H200bp_E10000ppm|native|3|16|0.01|0.005|12.042508|11.179507|10.316711|4.537987|2/2/2|rejected|
|strength370_ETH_D3_K7500ppm_S16_L5_H200bp_E10000ppm|native|3|16|0.01|0.0075|14.411651|13.670822|12.930199|2.050018|2/2/2|rejected|
|strength370_parent_BTC29H3_D3_K5000ppm_S12_L5_H200bp_E10000ppm|parent|3|12|0.01|0.005|11.626600|10.745952|9.865566|3.355934|6/6/6|passed|
|strength370_parent_BTC29H3_D3_K7500ppm_S12_L5_H200bp_E10000ppm|parent|3|12|0.01|0.0075|11.982239|11.223989|10.465876|2.214788|6/6/6|passed|
|strength370_parent_BTC29H3_D3_K5000ppm_S14_L5_H200bp_E10000ppm|parent|3|14|0.01|0.005|12.776725|11.845477|10.914396|3.367973|6/6/6|passed|
|strength370_parent_BTC29H3_D3_K7500ppm_S14_L5_H200bp_E10000ppm|parent|3|14|0.01|0.0075|13.113250|12.262644|11.412303|2.214788|6/6/6|passed|
|strength370_parent_BTC29H3_D3_K5000ppm_S16_L5_H200bp_E10000ppm|parent|3|16|0.01|0.005|12.033907|11.047546|10.061352|4.180988|6/6/6|passed|
|strength370_parent_BTC29H3_D3_K7500ppm_S16_L5_H200bp_E10000ppm|parent|3|16|0.01|0.0075|13.929221|13.040598|12.152142|2.214788|6/6/6|passed|

逐项失败判据：{'strength370_ETH_D3_K5000ppm_S12_L5_H200bp_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'strength370_ETH_D3_K7500ppm_S12_L5_H200bp_E10000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'strength370_ETH_D3_K5000ppm_S14_L5_H200bp_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'strength370_ETH_D3_K7500ppm_S14_L5_H200bp_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'strength370_ETH_D3_K5000ppm_S16_L5_H200bp_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'strength370_ETH_D3_K7500ppm_S16_L5_H200bp_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'strength370_parent_BTC29H3_D3_K5000ppm_S12_L5_H200bp_E10000ppm': [], 'strength370_parent_BTC29H3_D3_K7500ppm_S12_L5_H200bp_E10000ppm': [], 'strength370_parent_BTC29H3_D3_K5000ppm_S14_L5_H200bp_E10000ppm': [], 'strength370_parent_BTC29H3_D3_K7500ppm_S14_L5_H200bp_E10000ppm': [], 'strength370_parent_BTC29H3_D3_K5000ppm_S16_L5_H200bp_E10000ppm': [], 'strength370_parent_BTC29H3_D3_K7500ppm_S16_L5_H200bp_E10000ppm': []}。

四个原冻结账户延续原现金/q/desired/已计费用、风险与完整NAV，不采用研究K。本轮SMA/single Nov8_20:30→22:30仅闭合mark，自己的Nov9午夜仍待后续窗口；L4/FEWM Nov8_22:10→Nov9_00:10跨新真实资金费及原00:01日决策。以各自结算前持仓和新fundingTime/rate/mark记账，再用完整Nov8日close/volume执行原策略，成交数由冻结规则实际确定，不假定零，不复制其他账户现金流。SMA完整65日上下文保留R025309，输入字典/分钟数组核对重叠；旧午夜证明不重写，新增Nov9核验另存。所有账户皆partial延迟shadow，非十策略实时报价模拟或180日资格。

完成finish和必要检查后，在同main排他锁内运行只读monitor及原生检查。保留全部正负/失败、冻结规则、完整账本、登记和必要真实输入，清理可重建中间物。无真实订单、页面重部署或新定时任务。实际main push、完整远端tree/blob与解锁终态见.git/automation_proofs/20261109T010349Z.json。

历史spec中的warmup_days30/embargo_days3和persistence旧E.005文字为未被执行器读取的继承描述；本轮实际前置33个完整收盘，无fit/labels和折间purge/embargo，当前数值E=.01及完整规则为执行依据，详见冻结rules.legacy_parameter_fields。

本轮六组合按预设绝对历史门槛通过，六ETH组件近期仅1/8或2/8正5日折，仍不达近期/局部稳健性门槛；通过组合不证明ETH独立近期稳定。三倍组合净收益9.865566%–12.152142%，整体DD2.214788%–4.180988%。K0.5%的一些配置提高换手与回撤且收益不优于旧K1%对照，全部保留原通过/淘汰标准和逐项比较，不因相对表现事后改门槛。K0.75%/S16的三倍组合净收益12.152142%、DD2.214788%，为本格最高，但仍在S边界并有邻接跳变，不是全局最优或稳定实盘证明。事前代表D3/K0.5%/S12保留。

午夜真实续接：L4和FEWM分别各记6条Nov9_00资金费及6次原00:01日决策；BTC各成本收入分别0.02661802908091227和0.039927043621368405USDT，ETH结算前零持仓即使费率负也现金流为零。各自完整Nov8日1440分钟close/quotevolume、过去20日ADV/sigma、现金流先于日决策和全NAV前缀独立核验；本窗实际零新成交。原Nov8证明与冻结内核未改写，没有采用研究K，SMA/single本轮还未到自己的Nov9午夜。

监控本轮生成/原生校验成功：True；本轮新增研究展示12条、待恢复后展示0条。若失败，原生非零退出/生成快照/旧有效文件哈希留档，保留上次有效汇总，未修改检查门槛、账户或规则。
同S、同C/N的旧K1%/D3/H2%对照在1/2/3倍成本下收益不低且整体DD不高的当前配置数：4/12。本轮组合历史通过6项；各成本收益不低且整体回撤不高、至少一项严格改善的当前配置数5/12。逐项比较留档，不替换冻结账户，不建立新前向账户。
封存：6新ETH斜率门槛组件＋6新组合/36场景，组合通过6、淘汰0；24ID/48事件全部finish，50353旧文件保持。18旧原生路径只读，18新ETH原生路径/6660实际决策及18新组合路径独立核验。
原SMA NAV54548→54668，single 18933→19055，L4 11670→11797，FEWM 5778→5905。single/L4/FEWM实际新资金费0/6/6，日事件0/1/1，成交0/0/0；各自实际资金费时间戳/rate/mark/结算前q与本窗闭合mark独立核验，旧00/00:01仅保留已验证历史证明，原现金/q/风险/fullNAV连续，不复制现金流或重复16/00。FEWM累计5769分钟/147ID，所有账户partial非180日资格。
只读监控9952行，原9940行不变，10报价账户/301观察，gzip4569442字节。HTTP/传输失败0次原证据保留，所有正负/淘汰结果、完整账本/冻结规则/登记/必要输入保留。真实main push、完整远端tree/blob与解锁终态见.git/automation_proofs/20261109T010349Z.json。
