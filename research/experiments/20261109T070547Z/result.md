本轮6新ETH退出缓冲配置＋6新组合，36场景实际回测；组合历史通过6/6、淘汰0/6，旧E1%三K列只读。

上轮宽退出缓冲E1.25%的6个定义重复既往三成本完整净值，E1.5%的6个定义被同K旧E1%严格支配，未产生稳健改善。本轮固定S16/beta15/17、D3、ROC5/H2%和entry-only V10cap4.5%，预设K0.5%/0.75%/1% × E0.5%/0.75%/1%。更紧E使原long仅ROC<E、原short仅ROC>-E时继续持有，可能更早退出逆势风险，也可能打断均值回复、增加换手和成本；严格entryH优先，E<H，边界相等退出。旧E1%三K列仅只读，新E0.5%/0.75%六ETH组件及六组合各自先reserve后实际计算。代表预定K0.5%/E0.75%/S16，不按结果换代表或门槛。BTC29/H3/E1银行C3750/N1000只读，ETHC15000/N4500；raw1/1为两个完整独立银行NAV相加18750不归一化。370日连续12×30+10尾段，近期40继承日330状态8×5折，K/E两轴敏感性与1/2/3手续费/价差/滑点/量冲击/实际资金费压力。历史反复开发与多重选择不是未触碰最终、独立未来或稳定实盘。四原冻结账户不采用研究参数，当前窗口仅闭合mark；后续L4/FEWM06:10→08:10遇名义08结算时需取得新实际fundingTime/rate/mark并按各自q记账，当前不计算未来字段。

完整读取31024登记事件/15390ID、356份既往结论。初始16项真实历史证据齐全，缺0；此前规范研究定义10417，标实际10204、未标实际213；不称全部登记均有结果。

固定BTC signedROC29/H3%/E1%、C3750/N1000只读；ETH C15000/N4500，反向ROC5/H2%、退出E0.5/0.75/1%、斜率间隔D3，有限归一EWM窗口S16、beta=(S-1)/(S+1)，严格斜率门槛K0.5/0.75/1%。entry H优先，保留原long当ROC<E、原short当ROC>-E，边界相等退出。慢趋势和V10样本logvol上限4.5%只过滤新开/反手，保留同向实际q，反手先平后开，无日再平衡。所有新E的数量、LOT、冲击、费用、资金费、风险和NAV实际计算。

Raw[1,1]相加两个独立完整银行NAV，总本金18750，资金占比20/80%不重复乘，不归一化或缩放旧q/NAV/成本。BTC初始名义为本银行26.666667%/总本5.333333%，ETH为本银行30%/总本24%；无父订单、转账、再平衡或交叉保证金。

连续370日开发OOS：2025-10-19UTC00:01至2026-10-24UTC00:01，12×30日完整折和10日尾；近期40日继承day330状态分8×5日，折间不重开。ETH信号最大19、成本需21个过去收盘（合需21），BTC需30，统一初始真实33日。只用完整过去数据，下一UTC00:01 OPEN执行，终点计成本平仓。固定规则无fit/labels，purge/embargo0。逐折及完整连续DD留档；反复开发历史和多重选择不是未触碰最终、独立未来或稳定实盘盈利。

每边5bp手续费+1bp半价差+2bp滑点；冲击0.5×过去20完整日样本logvol×sqrt(实际q×OPEN/过去20日quoteADV)。1/2/3倍执行成本及资金费支出，收入不放大；实际fundingTime/rate/mark/当时q。线性永续无现货借币，核对LOT/tick/minnotional、参与率≤0.1%、费后1倍入场抵押、1%闭合小时不利mark风险代理。缺L2/TCA、历史完整保证金层级/逐tick强平和真实容量证据。

K/E原生和父组合各九格，旧E1%列只读，索引半径1含中心；全变体收益/整体DD/Sharpe/Calmar、72邻接边、边界和跳变留档。未定义统计留None/N/A、不填0，保留全部格。门槛不变：全期及近期各成本净正、1x≥9/12正30日、各成本近期≥6/8正5日、3xDD≤25%、局部3x净正及严格近期合格率≥60%、至少4原生平仓、毛PnL+资金费/1x成本≥2.5、无抵押/订单/风险违规、终点flat、≥180日。匹配同C/N实际常持有与现金0%，不据结果改门槛。

|新配置|类别|固定D|S|E|K|1x净%|2x净%|3x净%|3x整体DD%|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
|strength370_ETH_D3_K5000ppm_S16_L5_H200bp_E5000ppm|native|3|16|0.005|0.005|11.909837|11.051697|10.193934|4.537987|2/2/2|rejected|
|strength370_ETH_D3_K5000ppm_S16_L5_H200bp_E7500ppm|native|3|16|0.0075|0.005|12.058630|11.195639|10.332852|4.537987|2/2/2|rejected|
|strength370_ETH_D3_K7500ppm_S16_L5_H200bp_E5000ppm|native|3|16|0.005|0.0075|14.262857|13.526881|12.791281|2.050018|2/2/2|rejected|
|strength370_ETH_D3_K7500ppm_S16_L5_H200bp_E7500ppm|native|3|16|0.0075|0.0075|14.411651|13.670822|12.930199|2.050018|2/2/2|rejected|
|strength370_ETH_D3_K10000ppm_S16_L5_H200bp_E5000ppm|native|3|16|0.005|0.01|12.840530|12.203818|11.567445|2.050018|1/1/1|rejected|
|strength370_ETH_D3_K10000ppm_S16_L5_H200bp_E7500ppm|native|3|16|0.0075|0.01|12.972875|12.331305|11.689903|2.050018|1/1/1|rejected|
|strength370_parent_BTC29H3_D3_K5000ppm_S16_L5_H200bp_E5000ppm|parent|3|16|0.005|0.005|11.927770|10.945298|9.963130|4.180988|6/6/6|passed|
|strength370_parent_BTC29H3_D3_K5000ppm_S16_L5_H200bp_E7500ppm|parent|3|16|0.0075|0.005|12.046805|11.060451|10.074264|4.180988|6/6/6|passed|
|strength370_parent_BTC29H3_D3_K7500ppm_S16_L5_H200bp_E5000ppm|parent|3|16|0.005|0.0075|13.810187|12.925445|12.041007|2.214788|6/6/6|passed|
|strength370_parent_BTC29H3_D3_K7500ppm_S16_L5_H200bp_E7500ppm|parent|3|16|0.0075|0.0075|13.929221|13.040598|12.152142|2.214788|6/6/6|passed|
|strength370_parent_BTC29H3_D3_K10000ppm_S16_L5_H200bp_E5000ppm|parent|3|16|0.005|0.01|12.672325|11.866994|11.061939|2.214788|6/6/6|passed|
|strength370_parent_BTC29H3_D3_K10000ppm_S16_L5_H200bp_E7500ppm|parent|3|16|0.0075|0.01|12.778201|11.968984|11.159905|2.214788|6/6/6|passed|

逐项失败判据：{'strength370_ETH_D3_K5000ppm_S16_L5_H200bp_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'strength370_ETH_D3_K5000ppm_S16_L5_H200bp_E7500ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'strength370_ETH_D3_K7500ppm_S16_L5_H200bp_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'strength370_ETH_D3_K7500ppm_S16_L5_H200bp_E7500ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'strength370_ETH_D3_K10000ppm_S16_L5_H200bp_E5000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'strength370_ETH_D3_K10000ppm_S16_L5_H200bp_E7500ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'strength370_parent_BTC29H3_D3_K5000ppm_S16_L5_H200bp_E5000ppm': [], 'strength370_parent_BTC29H3_D3_K5000ppm_S16_L5_H200bp_E7500ppm': [], 'strength370_parent_BTC29H3_D3_K7500ppm_S16_L5_H200bp_E5000ppm': [], 'strength370_parent_BTC29H3_D3_K7500ppm_S16_L5_H200bp_E7500ppm': [], 'strength370_parent_BTC29H3_D3_K10000ppm_S16_L5_H200bp_E5000ppm': [], 'strength370_parent_BTC29H3_D3_K10000ppm_S16_L5_H200bp_E7500ppm': []}。

四个原冻结账户延续原现金/q/desired/成本、风险和完整NAV，不采用本轮研究参数。SMA/single Nov9_02:30→04:30，L4/FEWM Nov9_04:10→06:10均仅增加闭合分钟mark及适用闭合小时风险核验；原午夜事件各自完成，不重复记账，不增加新成交。SMA保留20261109T030420Z真实65日上下文，当前及上轮分钟数组按真实bar核对重叠；原现金/规则/完整账本不重开。后续L4/FEWM06:10→08:10可能跨名义08资金费，需届时取得新实际fundingTime/rate/mark并用各自结算前q核算，不能复用旧字段或其他账户现金流；当前不计算尚未发生的结算。下一日决策仍Nov10_00:01。均为partial延迟shadow，非十策略报价账户或180日资格。

完成finish和必要检查后，在同main排他锁内运行只读monitor及原生检查。保留全部正负/失败、冻结规则、完整账本、登记和必要真实输入，清理可重建中间物。无真实订单、页面重部署或新定时任务。实际main push、完整远端tree/blob与解锁终态见.git/automation_proofs/20261109T070547Z.json。

历史spec中的warmup_days30/embargo_days3和persistence旧E.005文字为未被执行器读取的继承描述；本轮实际前置33个完整收盘，无fit/labels和折间purge/embargo，当前每个spec数值E及完整规则为执行依据，详见冻结rules.legacy_parameter_fields。

本轮方向结论：4个新定义的三成本完整净值路径已在既往出现；6个新定义在所有1/2/3成本下被同K旧E1%严格支配。另2个K0.5%/E0.75%新定义（ETH组件和组合）在各成本收益微增且整体DD相同；组合三倍净收益从10.061351505939%到10.074264283749%，仅增0.012912777809个百分点，近期合格折数和整体回撤均未改善，不能据此称稳健改善或独立未来利润。6组合仍按预设门槛历史通过；6ETH组件因近期仅1或2/8正折、局部近期门槛失败淘汰，K1%两项另不足9/12正30日折。三倍组合净收益9.963130%–12.152142%、连续整体DD2.214788%–4.180988%；所有逐折、变体、负收益和重合路径均保留。

四原账户本轮仅补120分钟闭合mark：SMA NAV54909→55029，single19304→19426，L4 12041→12163，FEWM6149→6271；原现金/q/desired/费用和完整NAV前缀保持，0新资金费、日决策、成交。SMA仍38日partial，1/2/3累计-6.982980%/-7.226287%/-7.468958%，负收益完整保留。下一SMA/single04:30→06:30仍仅mark；L4/FEWM06:10→08:10可能跨名义08点资金费，必须届时获取新真实fundingTime/rate/mark并按各自结算前q记账，不能用旧08字段或其他账户金额。当前未来08计算为0。SMA完整65日上下文仍为已验证R030420真实输入，旧证据原字节不改。一次L4公共GET TLS35失败经有限重试恢复，FEWM只复用同一公开响应而未重复下载或重复计失败；原失败、真实响应、stdout/stderr、完整账本保留。

监控本轮生成/原生校验成功：True；本轮新增研究展示12条、待恢复后展示0条。若失败，原生非零退出/生成快照/旧有效文件哈希留档，保留上次有效汇总，未修改检查门槛、账户或规则。
同K、同C/N的旧E1%/S16/D3/H2%对照在1/2/3倍成本下收益不低且整体DD不高、每个成本至少一项严格改善的当前配置数：6/12。本轮组合历史通过6项；各成本收益不低且整体回撤不高、至少一项严格改善的当前配置数2/12。逐项比较留档，不替换冻结账户，不建立新前向账户。
封存：6新ETH退出缓冲组件＋6新组合/36场景，组合通过6、淘汰0；24ID/48事件全部finish，51501旧文件保持。18旧原生路径只读，18新ETH原生路径/6660实际决策及18新组合路径独立核验。
原SMA NAV54909→55029，single 19304→19426，L4 12041→12163，FEWM 6149→6271。single/L4/FEWM实际新资金费0/0/0，日事件0/0/0，成交0/0/0；各自实际资金费时间戳/rate/mark/结算前q与本窗闭合mark独立核验，旧00/00:01仅保留已验证历史证明，原现金/q/风险/fullNAV连续，不复制现金流或重复16/00。FEWM累计6129分钟/156ID，所有账户partial非180日资格。
只读监控9988行，原9976行不变，10报价账户/304观察，gzip4585544字节。HTTP/传输失败1次原证据保留，所有正负/淘汰结果、完整账本/冻结规则/登记/必要输入保留。真实main push、完整远端tree/blob与解锁终态见.git/automation_proofs/20261109T070547Z.json。
