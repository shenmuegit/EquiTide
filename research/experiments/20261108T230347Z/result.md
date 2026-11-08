本轮6新ETH斜率门槛配置＋6新组合，36场景实际回测；组合历史通过6/6、淘汰0/6，旧K1.5%三S行只读。

上轮D2/3配合1.5%严格斜率门槛过度过滤：两ETH配置零成交，六组合虽全期净正但近期或邻域失败。本轮固定D3、L5/H2/E1%、entry-only V10cap4.5%及原银行，事前预设K=1%/1.25%/1.5%×S12/14/16，beta=(S-1)/(S+1)。检验降低斜率门槛能否恢复反转交易覆盖和近期一致性，同时在手续费、价差、滑点、成交量冲击和资金费后保留余量；可能增加噪音和换手损失。旧K1.5%三S行仅只读；六新ETH和六新父组合逐一reserve后实际执行。代表D3/K1%/S12事前固定，不据结果扩网格或改门槛。ETH信号需19、成本需21个过去收盘，BTC需30，统一保留33日真实前置和370日连续开发历史。复用与多重选择不是未触碰最终、独立未来或稳定实盘盈利。

完整读取30752登记事件/15254ID、352份既往结论。初始16项真实历史证据齐全，缺0；此前规范研究定义10369，标实际10156、未标实际213；不称全部登记均有结果。

固定BTC signedROC29/H3%/E1%、C3750/N1000只读；ETH C15000/N4500，反向ROC5/H2%、退出E1%、斜率间隔D3，有限归一EWM窗口S12/14/16、beta=(S-1)/(S+1)，严格斜率门槛K1/1.25/1.5%。entry H优先，保留原long当ROC<E、原short当ROC>-E，边界相等退出。慢趋势和V10样本logvol上限4.5%只过滤新开/反手，保留同向实际q，反手先平后开，无日再平衡。所有新K的数量、LOT、冲击、费用、资金费、风险和NAV实际计算。

Raw[1,1]相加两个独立完整银行NAV，总本金18750，资金占比20/80%不重复乘，不归一化或缩放旧q/NAV/成本。BTC初始名义为本银行26.666667%/总本5.333333%，ETH为本银行30%/总本24%；无父订单、转账、再平衡或交叉保证金。

连续370日开发OOS：2025-10-19UTC00:01至2026-10-24UTC00:01，12×30日完整折和10日尾；近期40日继承day330状态分8×5日，折间不重开。ETH信号最大19、成本需21个过去收盘，BTC需30，统一初始真实33日。只用完整过去数据，下一UTC00:01 OPEN执行，终点计成本平仓。固定规则无fit/labels，purge/embargo0。逐折及完整连续DD留档；反复开发历史和多重选择不是未触碰最终、独立未来或稳定实盘盈利。

每边5bp手续费+1bp半价差+2bp滑点；冲击0.5×过去20完整日样本logvol×sqrt(实际q×OPEN/过去20日quoteADV)。1/2/3倍执行成本及资金费支出，收入不放大；实际fundingTime/rate/mark/当时q。线性永续无现货借币，核对LOT/tick/minnotional、参与率≤0.1%、费后1倍入场抵押、1%闭合小时不利mark风险代理。缺L2/TCA、历史完整保证金层级/逐tick强平和真实容量证据。

K/S原生和父组合各九格，旧K1.5%行只读，索引半径1含中心；全变体收益/整体DD/Sharpe/Calmar、72邻接边、边界和跳变留档。未定义统计留None/N/A、不填0，保留全部格。门槛不变：全期及近期各成本净正、1x≥9/12正30日、各成本近期≥6/8正5日、3xDD≤25%、局部3x净正及严格近期合格率≥60%、至少4原生平仓、毛PnL+资金费/1x成本≥2.5、无抵押/订单/风险违规、终点flat、≥180日。匹配同C/N实际常持有与现金0%，不据结果改门槛。

|新配置|类别|固定D|S|固定E|K|1x净%|2x净%|3x净%|3x整体DD%|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
|strength370_ETH_D3_K10000ppm_S12_L5_H200bp_E10000ppm|native|3|12|0.01|0.01|8.368584|7.900736|7.432908|2.050018|1/1/1|rejected|
|strength370_ETH_D3_K12500ppm_S12_L5_H200bp_E10000ppm|native|3|12|0.01|0.0125|7.876010|7.523420|7.170700|2.050018|1/1/1|rejected|
|strength370_ETH_D3_K10000ppm_S14_L5_H200bp_E10000ppm|native|3|14|0.01|0.01|12.972875|12.331305|11.689903|2.050018|1/1/1|rejected|
|strength370_ETH_D3_K12500ppm_S14_L5_H200bp_E10000ppm|native|3|14|0.01|0.0125|9.363536|8.831980|8.300444|2.050018|1/1/1|rejected|
|strength370_ETH_D3_K10000ppm_S16_L5_H200bp_E10000ppm|native|3|16|0.01|0.01|12.972875|12.331305|11.689903|2.050018|1/1/1|rejected|
|strength370_ETH_D3_K12500ppm_S16_L5_H200bp_E10000ppm|native|3|16|0.01|0.0125|12.102866|11.580439|11.058178|2.105140|1/1/1|rejected|
|strength370_parent_BTC29H3_D3_K10000ppm_S12_L5_H200bp_E10000ppm|parent|3|12|0.01|0.01|9.094768|8.424529|7.754309|2.132977|6/6/6|passed|
|strength370_parent_BTC29H3_D3_K12500ppm_S12_L5_H200bp_E10000ppm|parent|3|12|0.01|0.0125|8.700708|8.122676|7.544543|1.943908|6/6/6|passed|
|strength370_parent_BTC29H3_D3_K10000ppm_S14_L5_H200bp_E10000ppm|parent|3|14|0.01|0.01|12.778201|11.968984|11.159905|2.214788|6/6/6|passed|
|strength370_parent_BTC29H3_D3_K12500ppm_S14_L5_H200bp_E10000ppm|parent|3|14|0.01|0.0125|9.890729|9.169524|8.448338|2.132977|6/6/6|passed|
|strength370_parent_BTC29H3_D3_K10000ppm_S16_L5_H200bp_E10000ppm|parent|3|16|0.01|0.01|12.778201|11.968984|11.159905|2.214788|6/6/6|passed|
|strength370_parent_BTC29H3_D3_K12500ppm_S16_L5_H200bp_E10000ppm|parent|3|16|0.01|0.0125|12.082194|11.368291|10.654525|1.943908|6/6/6|passed|

逐项失败判据：{'strength370_ETH_D3_K10000ppm_S12_L5_H200bp_E10000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'strength370_ETH_D3_K12500ppm_S12_L5_H200bp_E10000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'strength370_ETH_D3_K10000ppm_S14_L5_H200bp_E10000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'strength370_ETH_D3_K12500ppm_S14_L5_H200bp_E10000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'strength370_ETH_D3_K10000ppm_S16_L5_H200bp_E10000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'strength370_ETH_D3_K12500ppm_S16_L5_H200bp_E10000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'strength370_parent_BTC29H3_D3_K10000ppm_S12_L5_H200bp_E10000ppm': [], 'strength370_parent_BTC29H3_D3_K12500ppm_S12_L5_H200bp_E10000ppm': [], 'strength370_parent_BTC29H3_D3_K10000ppm_S14_L5_H200bp_E10000ppm': [], 'strength370_parent_BTC29H3_D3_K12500ppm_S14_L5_H200bp_E10000ppm': [], 'strength370_parent_BTC29H3_D3_K10000ppm_S16_L5_H200bp_E10000ppm': [], 'strength370_parent_BTC29H3_D3_K12500ppm_S16_L5_H200bp_E10000ppm': []}。

原四冻结账户独立延续现金/q/desired/成本/风险/fullNAV，不采用研究K。本轮SMA/single Nov8_18:30→20:30、L4/FEWM Nov8_20:10→22:10，均仅闭合mark，原00/08.001/16资金费不重复，无新日决策、资金费或成交。SMA完整65日上下文保留R025309的1d/1m字典，现分钟数组核对重叠；保持原规则/本金/持仓及完整NAV前缀。下一L4FEWM22:10→Nov9_00:10跨午夜，需新实际资金费时间戳/rate/mark和完整Nov8日close/volume，以自身结算前q与冻结策略独立执行00:01；不能复制旧字段或其他现金流。SMA/single下一20:30→22:30仍仅mark。账户皆partial延迟shadow，非十策略实时报价模拟或180日资格。

finish和必要检查后，在同main排他锁内生成/原生检查只读monitor。保留全部正负/失败/冻结规则/完整账本/登记/必要真实输入，只清理可重建中间物。无真实订单、页面重部署或新任务。实际main push/完整远端tree/blob和解锁终态见.git/automation_proofs/20261108T230347Z.json。

历史spec中的warmup_days30/embargo_days3和persistence旧E.005文字为未被执行器读取的继承描述；本轮实际前置33个完整收盘，无fit/labels和折间purge/embargo，当前数值E=.01及完整规则为执行依据，详见冻结rules.legacy_parameter_fields。

结果解释：六个父组合历史通过，六个ETH组件仍未达到≥9/12正月折、近期≥6/8正5日和局部近期≥60%门槛；所有新ETH组件近期仅1/8正折。不能把组合近期合格解释为ETH组件本身近期稳定。三个K1.25%父组合在全部成本下相对同S旧K1.5%提高净收益、整体回撤完全相同；K1%三组合提高净收益同时回撤变大。新组合3倍净收益7.544543%–11.159905%，整体DD1.943908%–2.214788%。K1%/S14与S16在原生和父组合均形成相同完整三成本净值路径，只是不同真实参数在本数据上路径重合，不能算两份独立收益证据。事前代表D3/K1%/S12保留；边界及跳变仍存在，未建立平坦平台。

图表核验发现继承标题中的旧固定K1.5%标签，已只读改为固定D3并重新生成；全部11个CSV字节和财务报告SHA保持，未重算策略或改资格。旧标签观察和成功重试回执留档。未定义统计通用N/A处理已在首个reserve前绑定，不填造零值。

原报告execution_scope.explanation保留了继承的fixedK1.5percent/threeD说明文字；这是不参与执行的旧描述。本轮执行参数始终是冻结D3及K/S两轴，六新ETH的K为1%/1.25%、旧只读K1.5%，每个spec、完整决策及显式varied_axes均正确。以execution_scope_description_clarification.json逐项数字核验和纠正说明为准；已finish财务报告与登记哈希原字节保留，不改规则、状态、收益或重算。

监控本轮生成/原生校验成功：True；本轮新增研究展示12条、待恢复后展示0条。若失败，原生非零退出/生成快照/旧有效文件哈希留档，保留上次有效汇总，未修改检查门槛、账户或规则。
同S、同C/N的旧K1.5%/D3/H2%对照在1/2/3倍成本下收益不低且整体DD不高的当前配置数：0/12。本轮组合历史通过6项；各成本收益不低且整体回撤不高、至少一项严格改善的当前配置数9/12。逐项比较留档，不替换冻结账户，不建立新前向账户。
封存：6新ETH斜率门槛组件＋6新组合/36场景，组合通过6、淘汰0；24ID/48事件全部finish，49970旧文件保持。18旧原生路径只读，18新ETH原生路径/6660实际决策及18新组合路径独立核验。
原SMA NAV54428→54548，single 18811→18933，L4 11548→11670，FEWM 5656→5778。single/L4/FEWM实际新资金费0/0/0，日事件0/0/0，成交0/0/0；各自实际资金费时间戳/rate/mark/结算前q与本窗闭合mark独立核验，旧00/00:01仅保留已验证历史证明，原现金/q/风险/fullNAV连续，不复制现金流或重复16/00。FEWM累计5649分钟/144ID，所有账户partial非180日资格。
只读监控9940行，原9928行不变，10报价账户/300观察，gzip4564191字节。HTTP/传输失败0次原证据保留，所有正负/淘汰结果、完整账本/冻结规则/登记/必要输入保留。真实main push、完整远端tree/blob与解锁终态见.git/automation_proofs/20261108T230347Z.json。
