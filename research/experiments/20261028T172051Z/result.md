# 20261028T172051Z 双ETH慢周期分散组合验证

实际54个新三资金账户组合，历史通过0、淘汰54。完整读取21272事件/10532ID及218份结论；初始16项实际结果齐全。

Mix two adjacent or straddling ETH slow centers at fixed total ETHbank ownership1 and BTCbank ownership1. Prespecified54 combinations span all three slow-pair categories,a/H/L;no test-driven extension. Ask whether temporal diversification improves recent positive-fold breadth rather than simply selecting the known S28 history.

Raw source-bank ownership [1,a,1-a],a=0.25/0.5/0.75;not normalized. Every source bank initial10000,owned capitals10000/10000*a/10000*(1-a),parent20000. Source entryN1000/3000/3000,owned effective entrybudget1000+3000*a+3000*(1-a)=4000=20percentinitialparent. Static ownership,no source order resizing,fund-unit trades,transfers,rebalance,cash yield or crossmargin.

One fixed BTC ROC31/H4percent/E1percent native bank plus two ETH adjacent-horizon-majority gated reversal native banks. BothETH use common prespecified H2/2.5/3percent and fast L3/4,slow centers are the explicit increasing pair. Reuse complete original recorded native ledgers,not re-run signals or orders.

Parent NAV=BTC_NAV+a*ETH_A_NAV+(1-a)*ETH_B_NAV on common causal union(ns,eventcode). Monetary costs/PnL/funding and collateral cushion are multiplied by raw ownership;underlying native execution,roundtrip andfundingevent counts are not scaled. Source costs use actual original source-order notional/ADV/lot,tick;no recosting as smaller owned orders,no same-asset netting or new parent fills.

Every native bank retains original full-collateral and closed-hour1percentmaintenance proxy. Fractional ownership scales economic cushion but does not permit cross-bank rescue or net simultaneousETHlong/short obligations. L2/TCA/exacttiers/tick-liquidation unavailable.

事前固定三组慢周期配对27/28、28/29、27/29；每组ETH_A份额a=0.25/0.5/0.75、共同阈值H2/2.5/3%、快反转L3/4形成3D18格，合计54格、99条组内邻接边。分类配对不假定数值距离，不跨组凑邻域。所有54完整spec均包含三个原生源的全部参数字典，reserve前逐字段及周期三元组核验；不是模板继承单中心别名。相同组件和原值权重做语义查重，不因名字或组件顺序伪创新。

源BTC保持ROC31/H4%/E1%、N1000；两个ETH各用S−1/S/S+1严格符号多数门控，反转ROC L严格>H空/<−H多；带内仅实际多且ROC<0、实际空且ROC>0保留，零退出，门控不容许则平仓。日信号只用此前完成close，按此前close取lot，UTC00:01实际OPEN执行。无隐藏desired、未来OPEN/资金费或未闭合价格参与信号。完整规则/原生源FP与SHA随spec冻结。

21个旧原生/63成本NAV由保存的现金/数量/entry片段恢复并核对原SHA，不重跑源信号、成交或资金费模型。所有父层逐点相加后重新计算Sharpe、Calmar与连续整体DD，不能平均组件指标。不同参数虽可能回报接近，仍按完整具体配置分别登记。

真实8合并Parquet及16年度/近期源SHA/字节固定。370日OOS2025-10-19UTC00:01至2026-10-24UTC00:01，33日上下文含30预热和3日初始embargo；静态规则无拟合/未来标签，purge不适用。12个完整30日折与10日尾折承接账户；近期40日从day330继承分8×5日，既不重开本金也不诊断平仓，仅原终点计费退出。已反复使用的历史是开发验证，不能称未触碰最终测试。

成本保留原生实际订单：每侧5bp费＋1bp半价差＋2bp滑点＋0.5×此前20日样本日log波动×sqrt(实际源订单金额/此前20日quoteADV)冲击，参与率≤0.1%，tick/lot/最小金额与全额抵押入场约束保留。资金费=-有符号数量×实际结算mark×rate，流出乘1/2/3、收入不放大；永续不虚构现货借币。源原始N3000的成本只按银行所有权分摊，不声称已验证750/1500/2250的新订单成交或净额容量。

门槛保持：全期/近期各档净正，1倍月正折≥9/12、近期≥6/8，三倍连续整体DD≤25%，组内3D邻域三倍净正≥60%，≥4往返，(参考毛利＋资金费)/成本≥2.5，现金/拒单/独立银行风险违规0，终点空仓且≥180日。18个原单S27/28/29父组合及20k同预算恒多/现金0只读对照，原资格不变，不以新邻域重评级。

{"new_financial_configs": 54, "new_native_components": 0, "new_passive_parents": 54, "candidate_configs": 54, "benchmark_configs": 0, "passed_candidates": 0, "rejected_candidates": 54, "positive_configs_by_cost": {"1": 54, "2": 54, "3": 54}, "failed_criteria_counts": {"recent40_six_of_eight_positive5d_1x_folds": 54}, "rows": {"cost": 219, "full_folds": 2847, "recent40_folds": 1752, "daily_NAV": 60102, "edges": 99, "reference_comparisons": 648}, "by_pair_group": {"27_28": {"candidates": 18, "passed": 0, "recent6of8": 0, "full3x_positive_Sharpe_fraction": 1.0}, "28_29": {"candidates": 18, "passed": 0, "recent6of8": 0, "full3x_positive_Sharpe_fraction": 1.0}, "27_29": {"candidates": 18, "passed": 0, "recent6of8": 0, "full3x_positive_Sharpe_fraction": 1.0}}}

原单S28冻结候选与SMA65从UTC14:30续接至16:30；新窗口含16:00实际资金费，必须按实际结算时间/仓位/mark/rate逐条核验，仅计一次，收入不随成本放大，并保存16时段资金费前后风险状态供下轮17:00闭合小时检查。原策略/本金/持仓/entry/成本/完整净值前缀承接，不换新组合，不强制截止平仓。下一日决策Oct29UTC00:01。延迟真实闭合行情重建，不能冒充十策略实时公开报价执行。

背景沿用2026-10-27实际访问的一手[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)和[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)。本分散组合为研究推论，不是论文复现或收益移植。54个相关新试验加所有先前试验存在多重选择偏差；无DSR/PBO、独立未来验证或稳定实盘盈利证明。

复现工作目录/home/desktop/Documents/Codex/EquiTide；audit.py独立Decimal事件播放及全部组合NAV/折/资金费/成本检查；check_sources.py、check_exports.py、audit_candidate.py、audit_forward.py、check_feed.py只读证据，forward.py --reproduce离线复现；不重跑/预留/汇总已完成配置。只提交轻量研究证据，大行情/HTTPpacket留ignoreddata绑定SHA，原账户账本/冻结规则/登记和失败证据完整保留。main普通非强推，远端完整tree/blob/SHA核验后释放本轮锁。

历史通过项目只读冻结检查：0项。完整spec/来源/报告/账本SHA见candidate_validation.json；不改原冻结L3未来账户。

原冻结候选本轮资金费独立核验：实际结算UTC16:00:00.003，共6条逐资产/逐成本场景记录。BTC每档收入0.0771536232159660864 USDT，mark80529.41634933、rate0.00007984；三档是独立成本场景，不能合并为同一账户三份收入。ETH持仓为0，mark2334.01944266、rate0.00009213，入账0。收入不随成本倍数放大，现金精确承接且无新增日决策/成交；16小时资金费前后风险栈保留，下一17:00闭合小时须检查全部有正持续时长的状态，不只检查最新状态。完整精确Decimal和ns见candidate_verification.json/state.json。
开头同分支锁被模拟盘任务占用，真实非阻塞尝试失败后排队取得；未覆盖对方17:00提交。一次候选公开GET的TLS退出35由下一独立尝试恢复，9次请求中的8次成功页及失败原始响应/回执都保留并绑定SHA。仅发生实际锁/传输异常，没有本轮spec失配或无结果金融配置。54项实际finish分7个有界批次完成，未重复finish已完成ID或重算结果。

逐配置结果（收益/回撤单位%，三倍全期回撤使用完整连续OOS）：

|配置|1x收益|2x收益|3x收益|3x最大回撤|近期3x收益|1x月正折|1x近期正折|结论|
|---|---:|---:|---:|---:|---:|---:|---:|---|
|slowsplit370_S27_28_A25_H025_L4|8.971166|7.841569|6.711648|2.929662|1.169766|11/12|5/8|rejected|
|slowsplit370_S28_29_A75_H025_L4|8.901621|7.768672|6.635411|2.936459|1.190652|11/12|5/8|rejected|
|slowsplit370_S27_28_A25_H030_L4|8.651226|7.633881|6.616578|2.179946|0.736441|10/12|4/8|rejected|
|slowsplit370_S27_28_A50_H025_L4|8.834423|7.716081|6.597438|2.929541|1.146128|11/12|5/8|rejected|
|slowsplit370_S28_29_A75_H030_L4|8.597369|7.576732|6.556150|2.155645|0.756746|10/12|4/8|rejected|
|slowsplit370_S27_28_A50_H030_L4|8.527433|7.527420|6.527452|2.179821|0.712353|10/12|4/8|rejected|
|slowsplit370_S27_28_A75_H025_L4|8.697679|7.590593|6.483228|2.929421|1.122451|10/12|5/8|rejected|
|slowsplit370_S28_29_A50_H025_L4|8.695333|7.570288|6.444964|2.943167|1.187931|11/12|5/8|rejected|
|slowsplit370_S27_28_A75_H030_L4|8.403641|7.420958|6.438325|2.179696|0.688236|9/12|4/8|rejected|
|slowsplit370_S28_29_A50_H030_L4|8.419718|7.413121|6.406595|2.160648|0.752980|10/12|4/8|rejected|
|slowsplit370_S27_29_A75_H025_L4|8.491391|7.392208|6.292781|2.936096|1.119607|10/12|5/8|rejected|
|slowsplit370_S27_29_A75_H030_L4|8.225990|7.257348|6.288770|2.155374|0.684375|9/12|4/8|rejected|
|slowsplit370_S27_29_A25_H020_L3|9.037654|7.649836|6.261138|3.270453|1.219222|10/12|5/8|rejected|
|slowsplit370_S28_29_A25_H030_L4|8.242067|7.249511|6.257040|2.249862|0.749205|10/12|4/8|rejected|
|slowsplit370_S28_29_A25_H025_L4|8.489045|7.371903|6.254516|2.949905|1.185200|11/12|5/8|rejected|
|slowsplit370_S28_29_A25_H020_L3|9.039208|7.645598|6.251094|3.268946|1.244362|9/12|5/8|rejected|
|slowsplit370_S27_29_A50_H030_L4|8.172132|7.200198|6.228342|2.160466|0.704692|10/12|4/8|rejected|
|slowsplit370_S27_29_A25_H025_L3|8.609047|7.416223|6.222776|2.770220|1.219668|9/12|5/8|rejected|
|slowsplit370_S27_29_A50_H025_L4|8.421847|7.319312|6.216543|2.942923|1.140519|11/12|5/8|rejected|
|slowsplit370_S28_29_A25_H025_L3|8.601726|7.403949|6.205509|2.770179|1.244903|9/12|5/8|rejected|
|slowsplit370_S27_29_A50_H020_L3|8.982227|7.594261|6.205427|3.316201|1.199736|10/12|5/8|rejected|
|slowsplit370_S28_29_A50_H020_L3|8.985335|7.585785|6.185338|3.313187|1.250037|10/12|5/8|rejected|
|slowsplit370_S27_29_A25_H030_L4|8.118274|7.143049|6.167913|2.203996|0.725039|10/12|4/8|rejected|
|slowsplit370_S27_29_A50_H025_L3|8.541454|7.353316|6.164607|2.770995|1.200203|10/12|5/8|rejected|
|slowsplit370_S27_29_A75_H020_L3|8.926800|7.538686|6.149715|3.361950|1.180238|9/12|5/8|rejected|
|slowsplit370_S27_29_A25_H025_L4|8.352302|7.246415|6.140306|2.949782|1.161470|11/12|5/8|rejected|
|slowsplit370_S28_29_A50_H025_L3|8.526812|7.328768|6.130073|2.770912|1.250696|10/12|5/8|rejected|
|slowsplit370_S28_29_A75_H020_L3|8.931461|7.525972|6.119582|3.357429|1.255719|10/12|5/8|rejected|
|slowsplit370_S27_29_A75_H025_L3|8.473860|7.290408|6.106437|2.771770|1.180725|9/12|5/8|rejected|
|slowsplit370_S27_28_A75_H020_L3|8.872927|7.478873|6.083959|3.406191|1.185871|10/12|5/8|rejected|
|slowsplit370_S27_28_A50_H020_L3|8.874481|7.474635|6.073915|3.404684|1.211033|10/12|5/8|rejected|
|slowsplit370_S27_28_A25_H020_L3|8.876034|7.470397|6.063871|3.403177|1.236212|9/12|5/8|rejected|
|slowsplit370_S28_29_A75_H025_L3|8.451898|7.253587|6.054637|2.771646|1.256498|10/12|5/8|rejected|
|slowsplit370_S27_28_A75_H025_L3|8.398946|7.215228|6.031001|2.795869|1.186470|9/12|5/8|rejected|
|slowsplit370_S27_28_A50_H025_L3|8.391625|7.202954|6.013734|2.772462|1.211729|9/12|5/8|rejected|
|slowsplit370_S27_28_A25_H025_L3|8.384304|7.190680|5.996467|2.772421|1.237008|9/12|5/8|rejected|
|slowsplit370_S27_28_A25_H020_L4|8.410872|7.162655|5.914069|2.945479|1.178679|11/12|5/8|rejected|
|slowsplit370_S27_28_A50_H020_L4|8.369436|7.120499|5.871171|2.945357|1.154081|11/12|5/8|rejected|
|slowsplit370_S27_28_A75_H020_L4|8.327999|7.078344|5.828274|2.945235|1.129476|10/12|5/8|rejected|
|slowsplit370_S28_29_A75_H020_L4|8.243522|7.003925|5.764016|2.952350|1.200580|10/12|5/8|rejected|
|slowsplit370_S27_29_A75_H020_L4|8.119212|6.877457|5.635322|2.951983|1.126654|10/12|5/8|rejected|
|slowsplit370_S28_29_A50_H020_L4|8.034734|6.803039|5.571064|2.959130|1.197882|10/12|5/8|rejected|
|slowsplit370_S27_29_A50_H020_L4|7.951861|6.718727|5.485268|2.958884|1.148516|11/12|5/8|rejected|
|slowsplit370_S28_29_A25_H020_L4|7.825947|6.602152|5.378112|2.965942|1.195175|10/12|5/8|rejected|
|slowsplit370_S27_29_A25_H020_L4|7.784510|6.559996|5.335214|2.965818|1.170451|11/12|5/8|rejected|
|slowsplit370_S27_29_A25_H030_L3|6.757381|5.639269|4.520453|2.799659|0.796123|9/12|4/8|rejected|
|slowsplit370_S28_29_A25_H030_L3|6.717169|5.601016|4.484120|2.800136|0.821636|9/12|4/8|rejected|
|slowsplit370_S27_29_A50_H030_L3|6.689787|5.576362|4.462284|2.800450|0.776271|10/12|4/8|rejected|
|slowsplit370_S27_29_A75_H030_L3|6.622194|5.513455|4.404115|2.801242|0.756406|9/12|4/8|rejected|
|slowsplit370_S28_29_A50_H030_L3|6.609363|5.499856|4.389616|2.801404|0.827323|9/12|4/8|rejected|
|slowsplit370_S27_28_A75_H030_L3|6.514388|5.412295|4.309611|2.826129|0.762031|9/12|4/8|rejected|
|slowsplit370_S28_29_A75_H030_L3|6.501558|5.398696|4.295113|2.802674|0.833021|10/12|4/8|rejected|
|slowsplit370_S27_28_A50_H030_L3|6.474176|5.374042|4.273278|2.807189|0.787567|9/12|4/8|rejected|
|slowsplit370_S27_28_A25_H030_L3|6.433964|5.335789|4.236944|2.824372|0.813133|9/12|4/8|rejected|

全网格Sharpe正值比例、收益正值比例及最高观测单元边界诊断（只读已有结果，不改变资格）：{"27_28": {"dimension_count": 3, "cells": 18, "full3x_positive_Sharpe_fraction": 1.0, "recent40_3x_positive_Sharpe_fraction": 1.0, "full3x_positive_net_fraction": 1.0, "recent40_3x_positive_net_fraction": 1.0, "highest_observed_full3x_net_cell": "slowsplit370_S27_28_A25_H025_L4", "highest_observed_is_on_axis_boundary": {"ETH_A_ownership_fraction": true, "reversal_return_hurdle": false, "reversal_lookback_days": true}, "descriptive_full_Sharpe_cliff_edges": 3, "old_qualifications_preserved": true, "recent6of8_count": 0, "not_untouched_test_or_global_optimum": true}, "28_29": {"dimension_count": 3, "cells": 18, "full3x_positive_Sharpe_fraction": 1.0, "recent40_3x_positive_Sharpe_fraction": 1.0, "full3x_positive_net_fraction": 1.0, "recent40_3x_positive_net_fraction": 1.0, "highest_observed_full3x_net_cell": "slowsplit370_S28_29_A75_H025_L4", "highest_observed_is_on_axis_boundary": {"ETH_A_ownership_fraction": true, "reversal_return_hurdle": false, "reversal_lookback_days": true}, "descriptive_full_Sharpe_cliff_edges": 6, "old_qualifications_preserved": true, "recent6of8_count": 0, "not_untouched_test_or_global_optimum": true}, "27_29": {"dimension_count": 3, "cells": 18, "full3x_positive_Sharpe_fraction": 1.0, "recent40_3x_positive_Sharpe_fraction": 1.0, "full3x_positive_net_fraction": 1.0, "recent40_3x_positive_net_fraction": 1.0, "highest_observed_full3x_net_cell": "slowsplit370_S27_29_A75_H025_L4", "highest_observed_is_on_axis_boundary": {"ETH_A_ownership_fraction": true, "reversal_return_hurdle": false, "reversal_lookback_days": true}, "descriptive_full_Sharpe_cliff_edges": 6, "old_qualifications_preserved": true, "recent6of8_count": 0, "not_untouched_test_or_global_optimum": true}}。最高观测单元的预设网格边界标记已保存，不称全局最优；全期平台不能消除近期正折不足。

实际失败门槛计数：{"recent40_six_of_eight_positive5d_1x_folds": 54}。逐项真实结论见上表和report.json，不因全期收益正而放宽门槛。219成本行、2847全期折、1752近期折、60102新日边界、99敏感性边、648匹配对照完整留档；6图36面板已实际打开。
独立只读核验21旧原生/63成本曲线、3846条已保存成交与69930条已保存资金费记录，原完整NAV SHA保持；没有旧原生模型重跑或父层新增成交；无新原生模型执行，21个已有原生账本经独立Decimal事件播放与原NAV SHA核验，父层按原值份额组合。54新配置162成本场景共88292106完整NAV点、2268全期/逐折和1458近期/逐折指标通过；40旧唯一结果SHA/资格保持，11381受保护文件不变。60新实际ID各自finish，120事件仅追加；54实际金融配置加6实际partial，全部完整spec在reserve前核对三个原生参数字典，无本轮失配定义。
只读监控实际检查exit0：7840研究项，166既有paper观察/10账户；7786旧展示行完整字典不变。原候选累计2486点/场景、2429分钟，0新增日决策/成交，实际新增资金费记录6条；现金与资金费逐条独立核验，收入不随成本放大，08旧结算未重复；旧SMA累计38457点，0新日决策/成交。两者均非十策略实时报价执行或长期盈利证据。
真实命令/传输异常记录2项，见read_failures.json。本轮登记、账户续接及提交由持续stdin排他锁保护。所有真实负收益分折/近期、成功/失败和完整账户账本保留；行情与HTTPpacket留ignoreddata并绑定SHA，不提交大行情或凭据。main普通非强推，freshfetch/独立allheads/完整tree/blob/行情核验通过后释放自己锁。
