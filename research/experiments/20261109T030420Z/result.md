本轮6新ETH平滑窗口配置＋6新组合，36场景实际回测；组合历史通过6/6、淘汰0/6，旧S16三K列只读。

上轮K0.5%/0.75%×S12/14/16的六组合历史通过，K0.5%/S16整体DD达4.18%；ETH组件近期仅1或2/8正折。本轮事先固定D3、K0.5%/0.75%/1%×S16/18/20，检验更长有限EWM平滑窗口能否减少低K噪音，也可能增加滞后并削弱收益/近期一致性。S16三K列已有真实结果仅只读；六新ETH窗口组件及六新父组合先独立reserve再实际计算。预定代表K0.5%/S18，不按结果扩网格或改门槛。固定BTC29/H3/E1银行C3750/N1000；ETHL5/H2/E1、entry-onlyV10cap4.5%银行C15000/N4500，raw1/1表示完整独立银行相加18750、不归一化。370日连续历史12×30+10尾段，最近40日继承日330状态8×5；两轴敏感性及1/2/3手续费/价差/滑点/量冲击/实际资金费压力。所有历史已重复开发、多重选择，不是未触碰最终测试或稳定实盘盈利。原四冻结账户不采用研究参数，SMA/单策略本轮各自跨Nov9午夜，L4/FEWM已完成午夜只续闭合mark。

完整读取30888登记事件/15322ID、354份既往结论。初始16项真实历史证据齐全，缺0；此前规范研究定义10393，标实际10180、未标实际213；不称全部登记均有结果。

固定BTC signedROC29/H3%/E1%、C3750/N1000只读；ETH C15000/N4500，反向ROC5/H2%、退出E1%、斜率间隔D3，有限归一EWM窗口S16/18/20、beta=(S-1)/(S+1)，严格斜率门槛K0.5/0.75/1%。entry H优先，保留原long当ROC<E、原short当ROC>-E，边界相等退出。慢趋势和V10样本logvol上限4.5%只过滤新开/反手，保留同向实际q，反手先平后开，无日再平衡。所有新S的数量、LOT、冲击、费用、资金费、风险和NAV实际计算。

Raw[1,1]相加两个独立完整银行NAV，总本金18750，资金占比20/80%不重复乘，不归一化或缩放旧q/NAV/成本。BTC初始名义为本银行26.666667%/总本5.333333%，ETH为本银行30%/总本24%；无父订单、转账、再平衡或交叉保证金。

连续370日开发OOS：2025-10-19UTC00:01至2026-10-24UTC00:01，12×30日完整折和10日尾；近期40日继承day330状态分8×5日，折间不重开。ETH信号最大23、成本需21个过去收盘（合需23），BTC需30，统一初始真实33日。只用完整过去数据，下一UTC00:01 OPEN执行，终点计成本平仓。固定规则无fit/labels，purge/embargo0。逐折及完整连续DD留档；反复开发历史和多重选择不是未触碰最终、独立未来或稳定实盘盈利。

每边5bp手续费+1bp半价差+2bp滑点；冲击0.5×过去20完整日样本logvol×sqrt(实际q×OPEN/过去20日quoteADV)。1/2/3倍执行成本及资金费支出，收入不放大；实际fundingTime/rate/mark/当时q。线性永续无现货借币，核对LOT/tick/minnotional、参与率≤0.1%、费后1倍入场抵押、1%闭合小时不利mark风险代理。缺L2/TCA、历史完整保证金层级/逐tick强平和真实容量证据。

K/S原生和父组合各九格，旧S16列只读，索引半径1含中心；全变体收益/整体DD/Sharpe/Calmar、72邻接边、边界和跳变留档。未定义统计留None/N/A、不填0，保留全部格。门槛不变：全期及近期各成本净正、1x≥9/12正30日、各成本近期≥6/8正5日、3xDD≤25%、局部3x净正及严格近期合格率≥60%、至少4原生平仓、毛PnL+资金费/1x成本≥2.5、无抵押/订单/风险违规、终点flat、≥180日。匹配同C/N实际常持有与现金0%，不据结果改门槛。

|新配置|类别|固定D|S|固定E|K|1x净%|2x净%|3x净%|3x整体DD%|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
|strength370_ETH_D3_K5000ppm_S18_L5_H200bp_E10000ppm|native|3|18|0.01|0.005|11.077521|10.111587|9.145589|5.756840|2/2/2|rejected|
|strength370_ETH_D3_K7500ppm_S18_L5_H200bp_E10000ppm|native|3|18|0.01|0.0075|12.812518|11.998787|11.185261|4.537987|2/2/2|rejected|
|strength370_ETH_D3_K10000ppm_S18_L5_H200bp_E10000ppm|native|3|18|0.01|0.01|9.475861|9.005241|8.534642|2.050018|1/1/1|rejected|
|strength370_ETH_D3_K5000ppm_S20_L5_H200bp_E10000ppm|native|3|20|0.01|0.005|11.253175|10.229975|9.206711|5.756840|2/2/2|rejected|
|strength370_ETH_D3_K7500ppm_S20_L5_H200bp_E10000ppm|native|3|20|0.01|0.0075|11.986542|11.240576|10.494646|4.597594|2/2/2|rejected|
|strength370_ETH_D3_K10000ppm_S20_L5_H200bp_E10000ppm|native|3|20|0.01|0.01|12.146900|11.573094|10.999288|2.100310|1/1/1|rejected|
|strength370_parent_BTC29H3_D3_K5000ppm_S18_L5_H200bp_E10000ppm|parent|3|18|0.01|0.005|11.261917|10.193210|9.124454|5.159513|6/6/6|passed|
|strength370_parent_BTC29H3_D3_K7500ppm_S18_L5_H200bp_E10000ppm|parent|3|18|0.01|0.0075|12.649915|11.702970|10.756192|4.180988|6/6/6|passed|
|strength370_parent_BTC29H3_D3_K10000ppm_S18_L5_H200bp_E10000ppm|parent|3|18|0.01|0.01|9.980589|9.308133|8.635696|1.943908|6/6/6|passed|
|strength370_parent_BTC29H3_D3_K5000ppm_S20_L5_H200bp_E10000ppm|parent|3|20|0.01|0.005|11.402440|10.287920|9.173351|5.159513|6/6/6|passed|
|strength370_parent_BTC29H3_D3_K7500ppm_S20_L5_H200bp_E10000ppm|parent|3|20|0.01|0.0075|11.989135|11.096401|10.203700|4.691495|6/6/6|passed|
|strength370_parent_BTC29H3_D3_K10000ppm_S20_L5_H200bp_E10000ppm|parent|3|20|0.01|0.01|12.117421|11.362415|10.607413|1.943908|6/6/6|passed|

逐项失败判据：{'strength370_ETH_D3_K5000ppm_S18_L5_H200bp_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'strength370_ETH_D3_K7500ppm_S18_L5_H200bp_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'strength370_ETH_D3_K10000ppm_S18_L5_H200bp_E10000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'strength370_ETH_D3_K5000ppm_S20_L5_H200bp_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'strength370_ETH_D3_K7500ppm_S20_L5_H200bp_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'strength370_ETH_D3_K10000ppm_S20_L5_H200bp_E10000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'strength370_parent_BTC29H3_D3_K5000ppm_S18_L5_H200bp_E10000ppm': [], 'strength370_parent_BTC29H3_D3_K7500ppm_S18_L5_H200bp_E10000ppm': [], 'strength370_parent_BTC29H3_D3_K10000ppm_S18_L5_H200bp_E10000ppm': [], 'strength370_parent_BTC29H3_D3_K5000ppm_S20_L5_H200bp_E10000ppm': [], 'strength370_parent_BTC29H3_D3_K7500ppm_S20_L5_H200bp_E10000ppm': [], 'strength370_parent_BTC29H3_D3_K10000ppm_S20_L5_H200bp_E10000ppm': []}。

四个原冻结账户延续原现金/q/desired/成本、风险和完整NAV，不采用研究参数。本轮SMA及single Nov8_22:30→Nov9_00:30各自处理原00:01决策；single用真实Nov9_00 fundingTime/rate/mark和自身结算前q记账，SMA现货无资金费。L4/FEWM Nov9_00:10→02:10只增加闭合mark，其00资金费与00:01日决策已在上一轮各自完成，禁止重记。SMA抓取完整65日真实上下文，核对64日重叠及分钟/日线收盘；single续接自身1440分钟完整Nov8日close/volume。成交由原规则确定，不复制现金流、不重启或强制截止平仓。皆为partial延迟shadow，不是十策略实时报价模拟或180日资格。

完成finish和必要检查后，在同main排他锁内运行只读monitor及原生检查。保留全部正负/失败、冻结规则、完整账本、登记和必要真实输入，清理可重建中间物。无真实订单、页面重部署或新定时任务。实际main push、完整远端tree/blob与解锁终态见.git/automation_proofs/20261109T030420Z.json。

历史spec中的warmup_days30/embargo_days3和persistence旧E.005文字为未被执行器读取的继承描述；本轮实际前置33个完整收盘，无fit/labels和折间purge/embargo，当前数值E=.01及完整规则为执行依据，详见冻结rules.legacy_parameter_fields。

文字勘误（已绑定 spec/plan/report 与实际结果原字节保留）：rules.benchmark 继承的 primaryD3K1S16 文字不准确；本轮预先指定实际 primary_control 为 K0.5%/S16。全部逐项对照为同 K 的旧 S16，按 reference_fingerprint、reference_S=16 和完整数字参数核验。不是同 S、旧 K1% 对照；无重算、重新评级或门槛修改。详见 control_description_clarification.json。

本轮方向结论：延长 S 没有建立比旧 S16 更稳健的收益平台。12 个新定义中，10 个在全部 1/2/3 倍成本下同时被同 K 的旧 S16 收益与整体回撤支配，0 个全面优于旧对照。六个新组合符合预设历史门槛，只保留为历史通过证据；六个 ETH 组件因近期仅 1–2/8 正折及局部近期门槛失败而淘汰，其中 K1%/S18、S20 还不足 9/12 正30日折。各组合近期为6/8，未重写旧资格或冻结账户参数。三倍成本组合连续整体回撤为1.943908%–5.159513%，并非逐折回撤平均；全部参数/逐折/逐场景与负收益原SMA均保存。

跨午夜核验：SMA 延续原资金与持仓新增120分钟及1个日参考，NAV54668→54789，累计38完整日，成本1/2/3净收益仍为-6.982980%/-7.226287%/-7.468958%。single 自身 NAV19055→19182，完成Nov9_00资金费6条和00:01决策6条、0成交；BTC每成本情景收入0.05323605816182454 USDT，收入不放大，ETH零持仓金额由公式推导为零。L4 NAV11797→11919、FEWM5905→6027仅新增闭合mark，当前无资金费/日决策/成交。三永续账户完整链各自Nov9午夜6条，均只出现一次；下一次四账户日决策为Nov10_00:01。所有前向结果仍partial延迟shadow，不是180日资格或十策略实时报价收益。

监控本轮生成/原生校验成功：True；本轮新增研究展示12条、待恢复后展示0条。若失败，原生非零退出/生成快照/旧有效文件哈希留档，保留上次有效汇总，未修改检查门槛、账户或规则。
同K、同C/N的旧S16/D3/H2%对照在1/2/3倍成本下收益不低且整体DD不高的当前配置数：10/12。本轮组合历史通过6项；各成本收益不低且整体回撤不高、至少一项严格改善的当前配置数0/12。逐项比较留档，不替换冻结账户，不建立新前向账户。
封存：6新ETH平滑窗口组件＋6新组合/36场景，组合通过6、淘汰0；24ID/48事件全部finish，50731旧文件保持。18旧原生路径只读，18新ETH原生路径/6660实际决策及18新组合路径独立核验。
原SMA NAV54668→54789，single 19055→19182，L4 11797→11919，FEWM 5905→6027。single/L4/FEWM实际新资金费6/0/0，日事件1/0/0，成交0/0/0；各自实际资金费时间戳/rate/mark/结算前q与本窗闭合mark独立核验，旧00/00:01仅保留已验证历史证明，原现金/q/风险/fullNAV连续，不复制现金流或重复16/00。FEWM累计5889分钟/150ID，所有账户partial非180日资格。
只读监控9964行，原9952行不变，10报价账户/302观察，gzip4575430字节。HTTP/传输失败0次原证据保留，所有正负/淘汰结果、完整账本/冻结规则/登记/必要输入保留。真实main push、完整远端tree/blob与解锁终态见.git/automation_proofs/20261109T030420Z.json。
