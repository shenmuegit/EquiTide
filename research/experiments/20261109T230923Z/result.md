结论：本轮6个新ETH历史资金费过滤组件及6个父组合全部rejected，真实36场景/370日验证已留档。父组合3倍成本净收益8.515882%–13.701254%，完整连续OOS最大回撤1.901154%–4.048789%。6个父组合近期各成本均只有5/8正五日折，未达6/8；H2.25%/F0.5bp另月折8/12未达9/12。H/F表面有描述性跳变，未形成稳定平台。全期三成本净正不能替代近期一致性或前向证明。

关闭过滤的同H旧路径在全部36个新旧成本对比中收益更高；0.5bp的6项新配置被对照在收益/回撤共同支配，0上限组降低部分回撤但牺牲收益，未共同支配对照。逐项价格PnL、净资金费和执行成本差额满足现金平衡，见funding_filter_attribution.json，不能把所有收益变化归因于资金费预测。

本轮6个历史资金费过滤ETH组件与6个父组合完成36个成本场景；父组合历史通过0/6、淘汰6/6。

上轮降低H的历史父组合部分通过，但12项均被同E旧H2路径支配。本轮新增已知历史资金费入场过滤：固定ETH L5/E0.75%/K0.75%/S16/D3/V10/VC5%，H1.75/2/2.25%×F0/0.5bp/关闭。用最近合格已实现费率预测单次付费，检验是否降低不利carry；它只是过去代理，不能预知下一结算。使用settlement1–12h且available<=signal；00结算尚不可用，暖启动实际完整。关闭列复用精确旧组件/父组合；6+6新配置独立reserve后算36场景。代表预定H2%/F0.5bp，不事后挑选。BTC银行3750/N1000只读，ETH15000/N4500，两整银行raw[1,1]。既有门槛/边界/成本不变。当前四账户仅闭合mark/risk、无新fund/daily/fill，不采用本轮过滤。

完整读取31568事件/15662ID、364份结论；初始16项实际证据齐全。此前规范研究定义10513，未标实际213；本轮不重复旧filterOff结果。

H1.75/2/2.25%×F0/0.5bp/关闭，E0.75%、L5、K0.75%、S16/beta15/17、D3、V10样本logvol上限5%固定。只用signal时刻前已可用且结算年龄1–12小时的最近真实费率，以max(入场方向×费率,0)为单次付费代理；等于上限通过，缺失/过期阻止新开仓；同向实际q保留，反手先平后开。available_ts=settlement+1h为既有数据的保守假设，不是历史网络到达证明；过去费率不是未来实际费率。暖启动与所有370个决策的真实来源在funding_signal_preflight.json。

BTC3750/N1000只读，ETH15000/N4500新算LOT、数量、费用、量冲击、真实资金费、保证金风险与完整NAV。Raw[1,1]相加两整个独立银行，总本金18750；20/80%不再乘，不归一化/缩放/转账/再平衡/交叉保证金，无父订单。

Walk-forward：2025-10-19UTC00:01至2026-10-24UTC00:01连续370日、12×30日完整折+10日尾段；近期40日继承day330分8×5日，折间不重开。33日真实源上下文；ETH信号19、成本21、BTC30。固定规则无fit/labels/purge/embargo，仅完整过去数据、下一00:01 OPEN，终点平仓计成本。重复开发历史及多重选择，不是未触碰最终或独立未来测试。

成本：每边5bp手续费+1bp半价差+2bp滑点；冲击0.5×过去20日样本logvol×sqrt(q×OPEN/过去20日quoteADV)。1/2/3倍执行成本和资金费支出，收入不放大。核对LOT/tick/minnotional、≤0.1%参与率、费后1倍入场抵押、1%闭合小时不利mark风险代理。线性永续无现货借币。缺L2/TCA、历史完整保证金层级、逐tick强平与真实容量证据。

Sensitivity：H与F同时变化，两9格含3旧控制；F按[0,0.5bp,关闭]逐渐放宽，局部索引半径1含中心。全部收益/DD/Sharpe/Calmar和72邻接边、边界与跳变保留。关闭为分类边界，不能据此宣称广泛连续参数平台。未定义统计留空/N/A。

失败门槛事前不变：全期与近期全成本净正、1x≥9/12正30日、近期各成本≥6/8正5日、3x整体DD≤25%、局部净正及严格近期合格率≥60%、至少4平仓、毛PnL+资金费/1x成本≥2.5、无订单/抵押/风险违规、终点flat和≥180日。匹配同本金/名义常持有与现金0%。

|新配置|范围|H|F|1x净%|2x净%|3x净%|3x整体DD%|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---|---|
|pastfund_370_ETH_L5_H175bp_E7500ppm_F0ppm|native|0.0175|0|9.879035|9.469339|9.059724|5.025357|1/1/1|rejected|
|pastfund_370_ETH_L5_H175bp_E7500ppm_F50ppm|native|0.0175|5e-05|13.945645|13.086447|12.227815|5.677468|1/1/1|rejected|
|pastfund_370_ETH_L5_H200bp_E7500ppm_F0ppm|native|0.02|0|12.416794|12.057698|11.698498|1.995010|1/1/1|rejected|
|pastfund_370_ETH_L5_H200bp_E7500ppm_F50ppm|native|0.02|5e-05|16.483403|15.674806|14.866589|4.080065|1/1/1|rejected|
|pastfund_370_ETH_L5_H225bp_E7500ppm_F0ppm|native|0.0225|0|8.896557|8.640708|8.384875|1.995010|0/0/0|rejected|
|pastfund_370_ETH_L5_H225bp_E7500ppm_F50ppm|native|0.0225|5e-05|9.860999|9.382875|8.905092|4.222543|0/0/0|rejected|
|pastfund_370_parent_BTC29H3_ETHL5_H175bp_F0ppm|parent|0.0175|0|10.303129|9.679411|9.055762|3.495767|5/5/5|rejected|
|pastfund_370_parent_BTC29H3_ETHL5_H175bp_F50ppm|parent|0.0175|5e-05|13.556416|12.573098|11.590234|4.048789|5/5/5|rejected|
|pastfund_370_parent_BTC29H3_ETHL5_H200bp_F0ppm|parent|0.02|0|12.333336|11.750098|11.166781|1.901154|5/5/5|rejected|
|pastfund_370_parent_BTC29H3_ETHL5_H200bp_F50ppm|parent|0.02|5e-05|15.586623|14.643785|13.701254|3.082168|5/5/5|rejected|
|pastfund_370_parent_BTC29H3_ETHL5_H225bp_F0ppm|parent|0.0225|0|9.517147|9.016506|8.515882|1.901154|5/5/5|rejected|
|pastfund_370_parent_BTC29H3_ETHL5_H225bp_F50ppm|parent|0.0225|5e-05|10.288700|9.610240|8.932056|3.169346|5/5/5|rejected|

逐项未通过：{'pastfund_370_ETH_L5_H175bp_E7500ppm_F0ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'pastfund_370_ETH_L5_H175bp_E7500ppm_F50ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'pastfund_370_ETH_L5_H200bp_E7500ppm_F0ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'pastfund_370_ETH_L5_H200bp_E7500ppm_F50ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'pastfund_370_ETH_L5_H225bp_E7500ppm_F0ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'pastfund_370_ETH_L5_H225bp_E7500ppm_F50ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'pastfund_370_parent_BTC29H3_ETHL5_H175bp_F0ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'pastfund_370_parent_BTC29H3_ETHL5_H175bp_F50ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'pastfund_370_parent_BTC29H3_ETHL5_H200bp_F0ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'pastfund_370_parent_BTC29H3_ETHL5_H200bp_F50ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'pastfund_370_parent_BTC29H3_ETHL5_H225bp_F0ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'pastfund_370_parent_BTC29H3_ETHL5_H225bp_F50ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct']}。

四原账户延续各自cash/q/desired/风险/完整NAV，本窗SMA和single18:30–20:30、L4和FEWM20:10–22:10仅闭合mark/risk，0资金费/日决策/成交。不采用新过滤，不重置。下一L4/FEWM窗22:10–Nov10 00:10将跨新00资金费及00:01日决策，须新实际公共字段/完整闭合日/参考分钟闭合后按自己的持仓续记；旧Nov9午夜字段不得替代。SMA完整65日源R030420保留，新日决策需刷新。全部仍为partial延迟shadow，无180日前向资格，不等同十策略实时报价。

全部真实结果、负收益、失败、完整账本、登记及核验必需证据保留。main同锁下原生registry/monitor检查后提交push，独立tree/blob/账户链证明与真实推送SHA在.git/automation_proofs/20261109T230923Z.json。无真实订单、重部署或新定时任务。

旧spec warmup_days30/embargo_days3等未读描述保留；实际上下文33、固定规则无fit/labels/purge/embargo，本轮完整数值和rules为依据。

监控本轮生成/原生校验成功：True；本轮新增研究展示12条、待恢复后展示0条。若失败，原生非零退出/生成快照/旧有效文件哈希留档，保留上次有效汇总，未修改检查门槛、账户或规则。
同K、同C/N的同H旧关闭资金费过滤/L5/K0.75%/VC5%/S16/D3对照在1/2/3倍成本下收益不低且整体DD不高、每个成本至少一项严格改善的当前配置数：6/12。本轮组合历史通过0项；各成本收益不低且整体回撤不高、至少一项严格改善的当前配置数0/12。逐项比较留档，不替换冻结账户，不建立新前向账户。
封存：6新ETH历史资金费入场过滤组件＋6新组合/36场景，组合通过0、淘汰6；24ID/48事件全部finish，54724旧文件保持。18旧原生路径只读，18新ETH原生路径/6660实际决策及18新组合路径独立核验。
原SMA NAV55869→55989，single 20284→20406，L4 13021→13143，FEWM 7129→7251。single/L4/FEWM实际新资金费0/0/0，日事件0/0/0，成交0/0/0；各自实际资金费时间戳/rate/mark/结算前q与本窗闭合mark独立核验，旧00/00:01仅保留已验证历史证明，原现金/q/风险/fullNAV连续，不复制现金流或重复16/00。FEWM累计7089分钟/180ID，所有账户partial非180日资格。
只读监控10084行，原10072行不变，10报价账户/312观察，gzip4623586字节。HTTP/传输失败0次原证据保留，所有正负/淘汰结果、完整账本/冻结规则/登记/必要输入保留。真实main push、完整远端tree/blob与解锁终态见.git/automation_proofs/20261109T230923Z.json。
