结论：本轮6个新ETH历史费率中位数组件及6个父组合全部rejected，36场景/370日真实回测和核验已留档。父组合3倍成本净收益10.979423%–13.697208%，完整连续OOS最大回撤2.197302%–3.120026%；6个父组合各成本近期均仅5/8正五日折，未达6/8，严格局部近期合格率也不达标。M/F有描述性跳变，未形成稳定平台。整体净正不能替代近期一致性或独立未来验证。

同F旧最近单笔费率对照在收益/回撤上共同支配10/12项新配置，1/12项新配置局部共同改善对照，但仍未通过资格门槛。M2/F0与M4/F0的原生和父组合各有一组实际全成本净值别名；不同参数保留全部实际结果，别名不算独立证据。价格PnL、净资金费及执行成本差额核算见funding_filter_attribution.json。

本轮L4/FEWM按各自原规则完成Nov10零点资金费及00:01日决策：各6条真实资金费、各6条日决策、成交0/0。前向完整NAV分别13143→13270、7251→7378，自己的q/cash/日上下文/风险连续，无重置或median研究规则采用；仍partial，不具180日前向资格。

本轮6个ETH历史费率中位数组件与6个父组合完成36场景；父组合历史通过0/6、淘汰6/6。

上轮最近单笔费率过滤12项全失败，6组合近期只有5/8正五日折，整体虽净正但不达近期稳定性。本轮只改变过去carry代理：固定ETH H2%/L5/E0.75%/K0.75%/S16/D3/V10/VC5%，预设M=2/3/4笔历史已结算费率的有符号中位数×F=0/0.5bp。中位数可能降低单笔噪声，但也可能延迟真实carry变化；不预认改善。最新M个真实结算年龄1–36h且available<=signal，偶数M取中间二率算术均值，缺M笔阻止新开/反手。只过滤入场，同向实际q保留，反手先平后开。旧M1两F结果按原1–12h规则只读，不加median元数据制造新配置。代表事前M3/F0.5bp。BTC3750/N1000只读、ETH15000/N4500新算；raw[1,1]整银行组合18750。全部冻结验证门槛、370日/近期40边界和三成本不变。账户本窗SMA/single20:30–22:30只mark；L4/FEWM22:10–Nov10 00:10各自跨新实际00资金费及00:01原日决策，必须真实数据/自己的持仓结算，不采用研究规则。

完整读取31636事件/15696ID、365份结论；初始16项实际证据齐全。此前规范研究定义10525，未标实际213。旧M1两F和未过滤H2对照只读，不重新计算或改资格。

固定ETH H2%/E0.75%/L5/K0.75%/S16 beta15/17/D3/V10/VC5%。M=2/3/4笔最新合格历史结算率×F=0/0.5bp为新配置。结算年龄1–36小时且available<=signal，按SIGNED费率排序；奇数取中间率，偶数取中间二率算术均值。max(入场方向×median,0)<=F通过，等于阈值不拦截，缺任一必要M笔阻止新开/反手。同向实际q保留，反手先平后开。M1旧对照保持原1–12h可用规则；不把它改称36h中位数模型。既有normalized availability=settlement+1h是保守假设，不是历史网络到达证明；过去费率不等于未来实际费率。

BTC3750/N1000旧银行只读，ETH15000/N4500独立新算数量/LOT/量冲击/资金费/风险/fullNAV；raw[1,1]相加两整个银行，总本金18750、资本20/80%不再乘，无归一化/缩放/转账/再平衡/父订单/交叉保证金。

Walk-forward：2025-10-19UTC00:01至2026-10-24UTC00:01连续370日，12×30日完整折+10日尾；近期40日继承day330分8×5日，折间不重开。统一真实33日源上下文，ETH信号19/成本21、BTC30；所有决策都有4笔已成熟资金费。无fit/labels/purge/embargo，下一00:01 OPEN成交，终点平仓计成本。全部逐折及连续整体回撤留档。重复开发历史和多重选择，不是未触碰最终或独立未来证明。

成本：每边5bp手续费+1bp半价差+2bp滑点；冲击0.5×过去20日样本logvol×sqrt(q×OPEN/过去20日quoteADV)。1/2/3倍执行成本和实际资金费支出，收入不放大。实际fundingTime/rate/mark/当时q，线性永续无现货借币；LOT/tick/minnotional、≤0.1%参与率、费后1倍入场抵押及1%闭合小时不利mark风险代理。缺真实L2/TCA、历史完整保证金层级和逐tick强平/真实容量证据。

Sensitivity：M[1,2,3,4]×F[0,0.5bp]两8格，M1为精确旧只读2格，新M2–4各6格。两轴局部索引半径1含中心，保留全部净收益/整体DD/Sharpe/Calmar、60邻接边和边界/跳变。旧canonical资格不重评，未定义统计留空/N/A。两F均处网格边界，不能声称宽广稳定平台。

失败门槛事前固定：全期/近期各成本净正、1x≥9/12正30日、近期各成本≥6/8正5日、3x整体DD≤25%、局部净正及严格近期合格率≥60%、至少4平仓、毛PnL+资金费/1x成本≥2.5、无抵押/订单/风险违规、终点flat、≥180日。对比同C/N常持有与现金0%，不据结果改门槛。

|配置|范围|M|F|1x净%|2x净%|3x净%|3x整体DD%|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---|---|
|medianfund_370_ETH_M2_H200bp_E7500ppm_F0ppm|native|2|0|12.304469|11.884437|11.464301|1.995010|1/1/1|rejected|
|medianfund_370_ETH_M2_H200bp_E7500ppm_F50ppm|native|2|5e-05|14.670056|13.917807|13.165937|4.141712|1/1/1|rejected|
|medianfund_370_ETH_M3_H200bp_E7500ppm_F0ppm|native|3|0|12.826645|12.353544|11.880339|1.995010|1/1/1|rejected|
|medianfund_370_ETH_M3_H200bp_E7500ppm_F50ppm|native|3|5e-05|14.004582|13.370889|12.737266|4.082937|1/1/1|rejected|
|medianfund_370_ETH_M4_H200bp_E7500ppm_F0ppm|native|4|0|12.304469|11.884437|11.464301|1.995010|1/1/1|rejected|
|medianfund_370_ETH_M4_H200bp_E7500ppm_F50ppm|native|4|5e-05|16.361918|15.611690|14.861532|4.082937|1/1/1|rejected|
|medianfund_370_parent_BTC29H3_ETH_M2_H200bp_F0ppm|parent|2|0|12.243476|11.611489|10.979423|2.204083|5/5/5|rejected|
|medianfund_370_parent_BTC29H3_ETH_M2_H200bp_F50ppm|parent|2|5e-05|14.135945|13.238185|12.340732|3.120026|5/5/5|rejected|
|medianfund_370_parent_BTC29H3_ETH_M3_H200bp_F0ppm|parent|3|0|12.661217|11.986775|11.312254|2.197302|5/5/5|rejected|
|medianfund_370_parent_BTC29H3_ETH_M3_H200bp_F50ppm|parent|3|5e-05|13.603567|12.800651|11.997795|3.083936|5/5/5|rejected|
|medianfund_370_parent_BTC29H3_ETH_M4_H200bp_F0ppm|parent|4|0|12.243476|11.611489|10.979423|2.204083|5/5/5|rejected|
|medianfund_370_parent_BTC29H3_ETH_M4_H200bp_F50ppm|parent|4|5e-05|15.489435|14.593292|13.697208|3.083936|5/5/5|rejected|

逐项未通过：{'medianfund_370_ETH_M2_H200bp_E7500ppm_F0ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'medianfund_370_ETH_M2_H200bp_E7500ppm_F50ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'medianfund_370_ETH_M3_H200bp_E7500ppm_F0ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'medianfund_370_ETH_M3_H200bp_E7500ppm_F50ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'medianfund_370_ETH_M4_H200bp_E7500ppm_F0ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'medianfund_370_ETH_M4_H200bp_E7500ppm_F50ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'medianfund_370_parent_BTC29H3_ETH_M2_H200bp_F0ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'medianfund_370_parent_BTC29H3_ETH_M2_H200bp_F50ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'medianfund_370_parent_BTC29H3_ETH_M3_H200bp_F0ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'medianfund_370_parent_BTC29H3_ETH_M3_H200bp_F50ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'medianfund_370_parent_BTC29H3_ETH_M4_H200bp_F0ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'medianfund_370_parent_BTC29H3_ETH_M4_H200bp_F50ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct']}。

原SMA/single本窗Nov9 20:30–22:30仅闭合mark/risk；L4/FEWM本窗Nov9 22:10–Nov10 00:10各自跨新真实00资金费及00:01日决策，按各自原计划、实际持仓和现金结算，再执行原规则。不得复制现金流、重复旧16/00或采用研究median参数。下一SMA/single22:30–Nov10 00:30跨自己的新00/日决策：SMA需新完整65日上下文；L4/FEWM下一00:10–02:10仅mark，待参考闭合后才推进。仍partial延迟shadow，不等于十策略实时报价或180日前向资格。

全部真实成功/负收益/失败、账本、冻结规则、登记和核验必需数据保留。main同锁原生registry/monitor检查、封存、普通非forcepush、独立远端tree/blob与账户链核验，实际终态见.git/automation_proofs/20261110T011054Z.json。无真实订单、网页重部署或新定时任务。

继承warmup_days30/embargo_days3等未读描述保留；实际源33日、无fit/labels/purge/embargo，完整当前spec/plan数值和规则为依据。

监控本轮生成/原生校验成功：True；本轮新增研究展示12条、待恢复后展示0条。若失败，原生非零退出/生成快照/旧有效文件哈希留档，保留上次有效汇总，未修改检查门槛、账户或规则。
同K、同C/N的同F旧最近单笔费率/L5/K0.75%/VC5%/S16/D3对照在1/2/3倍成本下收益不低且整体DD不高、每个成本至少一项严格改善的当前配置数：10/12。本轮组合历史通过0项；各成本收益不低且整体回撤不高、至少一项严格改善的当前配置数1/12。逐项比较留档，不替换冻结账户，不建立新前向账户。
封存：6新ETH历史费率中位数入场过滤组件＋6新组合/36场景，组合通过0、淘汰6；24ID/48事件全部finish，55146旧文件保持。18旧原生路径只读，18新ETH原生路径/6660实际决策及18新组合路径独立核验。
原SMA NAV55989→56109，single 20406→20528，L4 13143→13270，FEWM 7251→7378。single/L4/FEWM实际新资金费0/6/6，日事件0/1/1，成交0/0/0；各自实际资金费时间戳/rate/mark/结算前q与本窗闭合mark独立核验，旧Nov9的00/00:01保留历史证明，本次Nov10的新00/00:01已独立按各自持仓和完整日数据核验，原现金/q/风险/fullNAV连续，不复制现金流或重复16/00。FEWM累计7209分钟/183ID，所有账户partial非180日资格。
只读监控10096行，原10084行不变，10报价账户/313观察，gzip4628394字节。HTTP/传输失败0次原证据保留，所有正负/淘汰结果、完整账本/冻结规则/登记/必要输入保留。真实main push、完整远端tree/blob与解锁终态见.git/automation_proofs/20261110T011054Z.json。
