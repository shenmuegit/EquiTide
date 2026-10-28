# 20261028T212151Z BTC入场阈值份额分散组合验证

实际54个新三银行组合，历史通过12、淘汰42。完整读取21606事件/10699ID、220份结论；初始16项已有实际证据。

Diversify BTC entry timing using existing ROC31 H2/H6 banks with static ownership a/(1-a),while ETH ownership stays1. Prespecify54 a/H/S/L combinations. Determine whether chronological fold breadth improves beyond the prior S28 island,not infer independent alpha from positive component returns.

Raw source-bank ownership [a,1-a,1],a0.25/0.5/0.75;not normalized. Owned initial capitals[10000*a,10000*(1-a),10000],sum20000. Native entryN1000/1000/3000,owned entrybudget1000*a+1000*(1-a)+3000=4000=20percentinitialparent. Static bank ownership,no source order resizing,fund-unit trades,transfers,rebalance,cash yield or crossmargin.

BTC_A ROC31/H2percent/E1percent plus BTC_B ROC31/H6percent/E1percent,each original N1000 per10000bank. One ETH majority-gated reversal bank,fast L3/4,H2/2.5/3percent,slowcenter S27/28/29 with exact S-1/S/S+1 strict-sign majority,original N3000 per10000bank,zero exit. All three exact original parameter dictionaries and fingerprints are in every spec.

Parent NAV=a*BTC_H2_NAV+(1-a)*BTC_H6_NAV+ETH_NAV on common causal union(ns,eventcode). Monetary PnL,costs,funding and individual cushion scaled by raw ownership. Native executions,roundtrips and fundingevent counts unweighted. Original nonlinear source-order costs/lot/tick retained;no parent fills or same-asset netting.

Each native bank retains full-collateral entry and closed-hour1percentmaintenance proxy. Ownership scales economic cushion without permitting cross-bank rescue/net simultaneous BTC obligations. L2/TCA/exacttiers/tickliquidation unavailable.

事前54格：BTC_H2份额a=0.25/0.5/0.75，BTC_H6份额1-a，ETH份额1；ETH阈值2/2.5/3%、慢中心S27/28/29、快周期L3/4。4D相邻135边，全部完整spec在reserve前核对三个源参数字典。两个BTC原生均N1000/初始10000，ETH原生N3000/初始10000；银行所有权不等于BTC250/500/750的新订单回测，权重不归一化。

370日连续OOS2025-10-19UTC00:01至2026-10-24UTC00:01；33日上下文含30预热及3日初始embargo。静态规则无拟合/未来标签，purge不适用；12完整30日折加10日尾折，逐折承接现金/q/entry/费用；近期40日由day330继承、8×5日，不重开本金、不产生诊断平仓，仅原终点计费退出。反复使用历史属于开发验证，不是未触碰最终测试。

23旧原生/69成本NAV按已有现金/数量/entry事件恢复并核对原SHA，不重跑信号、成交或资金费。共同纳秒/事件时轴使用最后完成值，逐点组合后重算完整整体回撤及逐折/近期指标，不平均组件指标。两个BTC共享价格和资金费，可重叠或相反，不假定独立或允许跨银行净额。

保留实际源订单成本：每侧5bp费+1bp半价差+2bp滑点+0.5×滞后20日样本log波动×sqrt(实际源订单金额/滞后20日quoteADV)冲击；参与率≤0.1%，tick/lot/最低金额及全额抵押约束。资金费=-有符号q×实际mark×rate，流出随1/2/3倍放大，收入不放大。永续不虚构现货借币；独立银行闭合小时1%维持保证金代理，不作跨银行救助/净额。

门槛固定：全期/近期三档净正、1x完整月≥9/12正折及近期≥6/8、3x完整连续整体DD≤25%、4D邻域全期3x净正≥60%、≥4往返、(参考毛利+资金费)/成本≥2.5、现金/拒单/风险违规0、终点空仓且≥180日。18个旧BTC_H4加同ETH父组合、20k恒多及现金0只读对照；保持旧资格，不评估未登记a=0/1端点。

{"new_financial_configs": 54, "new_native_components": 0, "new_passive_parents": 54, "candidate_configs": 54, "benchmark_configs": 0, "passed_candidates": 12, "rejected_candidates": 42, "positive_configs_by_cost": {"1": 54, "2": 54, "3": 54}, "failed_criteria_counts": {"recent40_six_of_eight_positive5d_1x_folds": 42, "nine_of_twelve_positive_complete30d_1x_folds": 11}, "rows": {"cost": 219, "full_folds": 2847, "recent40_folds": 1752, "daily_NAV": 60102, "edges": 135, "reference_comparisons": 324}, "by_slow_center": {"27": {"candidates": 18, "passed": 0, "recent6of8": 0, "full3x_positive_Sharpe_fraction": 1.0}, "28": {"candidates": 18, "passed": 12, "recent6of8": 12, "full3x_positive_Sharpe_fraction": 1.0}, "29": {"candidates": 18, "passed": 0, "recent6of8": 0, "full3x_positive_Sharpe_fraction": 1.0}}}

原单S28冻结候选与SMA65从UTC18:30续接至20:30，资金费已在16:00:00.003入账，不重复。19:00闭合小时承接旧18小时风险状态，再处理20:00闭合小时；保留现金/数量/entry/净值完整前缀，不换本轮新组合。下一资金费Oct29UTC00:00、下一日决策00:01。延迟真实闭合行情重建与十策略实时报价账户分开。

背景沿用2026-10-27实际访问的一手[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)与[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)。本组合为研究推论；54个相关新试验及所有先前试验存在多重选择偏差，无DSR/PBO、独立未来验证或稳定实盘盈利证明。

复现工作目录/home/desktop/Documents/Codex/EquiTide。audit.py独立Decimal源事件播放，check_exports.py/check_sources.py核对真实结果，audit_candidate.py/audit_forward.py独立核对原账户，forward.py --reproduce离线复现。不重新reserve/evaluate已完成配置。仅提交轻量必要证据，行情/HTTPpacket留ignoreddata绑定SHA；main非强推并核验完整远端tree/blob/行情后释放本轮锁。

与同ETH/同本金/同入场预算旧BTC_H4组合的只读三倍成本对照：{"source": "research/experiments/20261028T212151Z/reference_comparisons.csv", "source_sha256": "2d1256057316897088fe9940dbcb4fb093e31be5f6b43f93fa347bcdfdfddecc", "new_financial_evaluations": 0, "qualification_changes": 0, "matched_3x_rows": 54, "new_return_exceeds_BTC_H4_same_ETH": 0, "new_DD_lower_than_BTC_H4_same_ETH": 12, "full_return_delta_pp_range": [-0.7346320853397481, -0.06539116505794862], "recent40_return_delta_pp_range": [0.007556605531866545, 0.011874907727849049], "interpretation": "Descriptive comparison of already evaluated and registered candidates with old same-ETH/capital/budget BTC_H4 controls;not new trials or old-status requalification."}。新增BTC门槛分散未扩大S27/29的近期正折通过范围。

历史通过项目只读冻结检查：12项。完整spec/来源/报告/账本SHA见candidate_validation.json；不改原冻结L3未来账户。
btcmix370_A25_H020_S28_L3：1/2/3倍370日收益[8.754734886509441, 7.372039061193791, 5.988435040128159]%，整体3倍回撤3.2013947813885%，近期3倍收益1.2709891165629594%；完整月正折10/12、近期6/8，邻域全期3倍净正24/24、原始近期6/8仅8/24。仅通过预设历史门槛，尚无该新配置独立未来证据。
btcmix370_A25_H020_S28_L4：1/2/3倍370日收益[8.329455877253245, 7.110691187760665, 5.891576225518103]%，整体3倍回撤2.978159426870497%，近期3倍收益1.2128099771156142%；完整月正折10/12、近期6/8，邻域全期3倍净正24/24、原始近期6/8仅8/24。仅通过预设历史门槛，尚无该新配置独立未来证据。
btcmix370_A25_H025_S28_L3：1/2/3倍370日收益[8.254130290187977, 7.084286401982798, 5.913809262352632]%，整体3倍回撤2.805300856502946%，近期3倍收益1.271896032544917%；完整月正折9/12、近期6/8，邻域全期3倍净正36/36、原始近期6/8仅8/36。仅通过预设历史门槛，尚无该新配置独立未来证据。
btcmix370_A25_H025_S28_L4：1/2/3倍370日收益[8.985056300094229, 7.872936822123711, 6.760467367028222]%，整体3倍回撤2.96220338558576%，近期3倍收益1.2028205569404538%；完整月正折11/12、近期6/8，邻域全期3倍净正36/36、原始近期6/8仅8/36。仅通过预设历史门槛，尚无该新配置独立未来证据。
btcmix370_A50_H020_S28_L3：1/2/3倍370日收益[8.491736807152893, 7.0732314463825885, 5.65381457998726]%，整体3倍回撤3.330681326333329%，近期3倍收益1.2721255431188627%；完整月正折9/12、近期6/8，邻域全期3倍净正36/36、原始近期6/8仅12/36。仅通过预设历史门槛，尚无该新配置独立未来证据。
btcmix370_A50_H020_S28_L4：1/2/3倍370日收益[8.066457797896698, 6.81188357294944, 5.556955765377203]%，整体3倍回撤2.9689183100438%，近期3倍收益1.2137618114771875%；完整月正折10/12、近期6/8，邻域全期3倍净正36/36、原始近期6/8仅12/36。仅通过预设历史门槛，尚无该新配置独立未来证据。
btcmix370_A50_H025_S28_L3：1/2/3倍370日收益[7.991132210831453, 6.785478787171595, 5.57918880221171]%，整体3倍回撤2.7958440675557084%，近期3倍收益1.2730361571815951%；完整月正折9/12、近期6/8，邻域全期3倍净正54/54、原始近期6/8仅12/54。仅通过预设历史门槛，尚无该新配置独立未来证据。
btcmix370_A50_H025_S28_L4：1/2/3倍370日收益[8.722058220737683, 7.574129207312508, 6.4258469068873225]%，整体3倍回撤2.952990921748244%，近期3倍收益1.2037330279714542%；完整月正折11/12、近期6/8，邻域全期3倍净正54/54、原始近期6/8仅12/54。仅通过预设历史门槛，尚无该新配置独立未来证据。
btcmix370_A75_H020_S28_L3：1/2/3倍370日收益[8.228738727796369, 6.774423831571386, 5.319194119846404]%，整体3倍回撤3.460142166692204%，近期3倍收益1.2732692167395587%；完整月正折9/12、近期6/8，邻域全期3倍净正24/24、原始近期6/8仅8/24。仅通过预设历史门槛，尚无该新配置独立未来证据。
btcmix370_A75_H020_S28_L4：1/2/3倍370日收益[7.803459718540151, 6.513075958138259, 5.2223353052363475]%，整体3倍回撤2.9596527948428153%，近期3倍收益1.2147197178223657%；完整月正折10/12、近期6/8，邻域全期3倍净正24/24、原始近期6/8仅8/24。仅通过预设历史门槛，尚无该新配置独立未来证据。
btcmix370_A75_H025_S28_L3：1/2/3倍370日收益[7.728134131474906, 6.486671172360392, 5.244568342070854]%，整体3倍回撤2.796297580341889%，近期3倍收益1.274183557687092%；完整月正折9/12、近期6/8，邻域全期3倍净正36/36、原始近期6/8仅8/36。仅通过预设历史门槛，尚无该新配置独立未来证据。
btcmix370_A75_H025_S28_L4：1/2/3倍370日收益[8.459060141381137, 7.275321592501305, 6.091226446746445]%，整体3倍回撤2.943754265841736%，近期3倍收益1.2046512716302527%；完整月正折11/12、近期6/8，邻域全期3倍净正36/36、原始近期6/8仅8/36。仅通过预设历史门槛，尚无该新配置独立未来证据。

逐配置结果（收益/回撤单位%，三倍全期回撤使用完整连续OOS）：

|配置|1x收益|2x收益|3x收益|3x最大回撤|近期3x收益|1x月正折|1x近期正折|结论|
|---|---:|---:|---:|---:|---:|---:|---:|---|
|btcmix370_A25_H025_S28_L4|8.985056|7.872937|6.760467|2.962203|1.202821|11/12|6/8|passed|
|btcmix370_A25_H030_S28_L4|8.652166|7.646223|6.640314|2.222824|0.769622|10/12|5/8|rejected|
|btcmix370_A50_H025_S28_L4|8.722058|7.574129|6.425847|2.952991|1.203733|11/12|6/8|passed|
|btcmix370_A50_H030_S28_L4|8.389168|7.347415|6.305693|2.210001|0.769170|10/12|5/8|rejected|
|btcmix370_A25_H025_S27_L4|8.438083|7.370985|6.303627|3.151335|1.108154|9/12|5/8|rejected|
|btcmix370_A25_H030_S27_L4|8.156995|7.220377|6.283807|2.222319|0.673166|9/12|4/8|rejected|
|btcmix370_A25_H020_S29_L3|8.970228|7.611291|6.251459|3.085031|1.248233|9/12|5/8|rejected|
|btcmix370_A25_H025_S29_L3|8.553788|7.385010|6.215555|2.802340|1.248660|9/12|5/8|rejected|
|btcmix370_A75_H025_S28_L4|8.459060|7.275322|6.091226|2.943754|1.204651|11/12|6/8|passed|
|btcmix370_A25_H030_S29_L4|7.941563|6.991780|6.042094|2.519639|0.754580|9/12|4/8|rejected|
|btcmix370_A25_H020_S27_L3|8.748520|7.388991|6.028612|3.207411|1.170221|9/12|5/8|rejected|
|btcmix370_A25_H025_S29_L4|8.159904|7.079399|5.998677|2.989328|1.191975|10/12|5/8|rejected|
|btcmix370_A25_H020_S28_L3|8.754735|7.372039|5.988435|3.201395|1.270989|10/12|6/8|passed|
|btcmix370_A25_H025_S27_L3|8.283413|7.133381|5.982877|3.030497|1.170732|8/12|5/8|rejected|
|btcmix370_A75_H030_S28_L4|8.126170|7.048608|5.971073|2.197124|0.768715|10/12|5/8|rejected|
|btcmix370_A50_H025_S27_L4|8.175085|7.072177|5.969007|3.155707|1.108770|9/12|5/8|rejected|
|btcmix370_A50_H030_S27_L4|7.893997|6.921569|5.949187|2.209498|0.672409|9/12|4/8|rejected|
|btcmix370_A50_H020_S29_L3|8.707230|7.312484|5.916838|3.214159|1.249294|9/12|5/8|rejected|
|btcmix370_A25_H025_S28_L3|8.254130|7.084286|5.913809|2.805301|1.271896|9/12|6/8|passed|
|btcmix370_A25_H020_S28_L4|8.329456|7.110691|5.891576|2.978159|1.212810|10/12|6/8|passed|
|btcmix370_A50_H025_S29_L3|8.290790|7.086202|5.880934|2.792889|1.249723|9/12|5/8|rejected|
|btcmix370_A25_H020_S27_L4|8.163710|6.942068|5.719984|3.168307|1.114340|8/12|5/8|rejected|
|btcmix370_A50_H030_S29_L4|7.678565|6.692972|5.707473|2.649381|0.754078|9/12|4/8|rejected|
|btcmix370_A50_H020_S27_L3|8.485522|7.090183|5.693992|3.336701|1.171036|9/12|5/8|rejected|
|btcmix370_A50_H025_S29_L4|7.896906|6.780591|5.664057|2.980067|1.192859|10/12|5/8|rejected|
|btcmix370_A50_H020_S28_L3|8.491737|7.073231|5.653815|3.330681|1.272126|9/12|6/8|passed|
|btcmix370_A50_H025_S27_L3|8.020415|6.834574|5.648256|3.013398|1.171549|8/12|5/8|rejected|
|btcmix370_A75_H025_S27_L4|7.912087|6.773370|5.634386|3.160090|1.109390|9/12|5/8|rejected|
|btcmix370_A75_H030_S27_L4|7.630999|6.622762|5.614567|2.196622|0.671647|9/12|4/8|rejected|
|btcmix370_A75_H020_S29_L3|8.444232|7.013676|5.582218|3.343460|1.250362|9/12|5/8|rejected|
|btcmix370_A50_H025_S28_L3|7.991132|6.785479|5.579189|2.795844|1.273036|9/12|6/8|passed|
|btcmix370_A50_H020_S28_L4|8.066458|6.811884|5.556956|2.968918|1.213762|10/12|6/8|passed|
|btcmix370_A75_H025_S29_L3|8.027792|6.787395|5.546314|2.783413|1.250793|9/12|5/8|rejected|
|btcmix370_A50_H020_S27_L4|7.900712|6.643260|5.385364|3.172725|1.114979|8/12|5/8|rejected|
|btcmix370_A75_H030_S29_L4|7.415567|6.394165|5.372853|2.779300|0.753572|8/12|4/8|rejected|
|btcmix370_A75_H020_S27_L3|8.222524|6.791376|5.359371|3.466166|1.171856|9/12|5/8|rejected|
|btcmix370_A75_H025_S29_L4|7.633908|6.481784|5.329437|2.970782|1.193749|10/12|5/8|rejected|
|btcmix370_A75_H020_S28_L3|8.228739|6.774424|5.319194|3.460142|1.273269|9/12|6/8|passed|
|btcmix370_A75_H025_S27_L3|7.757417|6.535766|5.313636|2.996253|1.172371|8/12|5/8|rejected|
|btcmix370_A75_H025_S28_L3|7.728134|6.486671|5.244568|2.796298|1.274184|9/12|6/8|passed|
|btcmix370_A75_H020_S28_L4|7.803460|6.513076|5.222335|2.959653|1.214720|10/12|6/8|passed|
|btcmix370_A25_H020_S29_L4|7.494307|6.307146|5.119769|3.005579|1.202061|8/12|5/8|rejected|
|btcmix370_A75_H020_S27_L4|7.637714|6.344453|5.050743|3.177154|1.115623|9/12|5/8|rejected|
|btcmix370_A50_H020_S29_L4|7.231309|6.008339|4.785149|2.996289|1.202985|8/12|5/8|rejected|
|btcmix370_A25_H030_S29_L3|6.702121|5.608056|4.513232|2.832041|0.825312|9/12|4/8|rejected|
|btcmix370_A75_H020_S29_L4|6.968310|5.709531|4.450528|3.102680|1.203915|9/12|5/8|rejected|
|btcmix370_A25_H030_S27_L3|6.431747|5.356428|4.280554|3.062653|0.745834|8/12|4/8|rejected|
|btcmix370_A50_H030_S29_L3|6.439123|5.309249|4.178611|2.822530|0.825029|9/12|4/8|rejected|
|btcmix370_A25_H030_S28_L3|6.270899|5.203416|4.135219|2.837165|0.848135|9/12|5/8|rejected|
|btcmix370_A50_H030_S27_L3|6.168749|5.057620|3.945934|3.045415|0.745296|8/12|4/8|rejected|
|btcmix370_A75_H030_S29_L3|6.176125|5.010441|3.843991|2.812993|0.824744|9/12|4/8|rejected|
|btcmix370_A50_H030_S28_L3|6.007901|4.904609|3.800598|2.827644|0.847925|9/12|5/8|rejected|
|btcmix370_A75_H030_S27_L3|5.905751|4.758813|3.611313|3.028131|0.744753|8/12|4/8|rejected|
|btcmix370_A75_H030_S28_L3|5.744903|4.605801|3.465978|2.901043|0.847713|9/12|5/8|rejected|

全网格Sharpe正值比例、收益正值比例及最高观测单元边界诊断（只读已有结果，不改变资格）：{"parent": {"dimension_count": 4, "cells": 54, "full3x_positive_Sharpe_fraction": 1.0, "recent40_3x_positive_Sharpe_fraction": 1.0, "full3x_positive_net_fraction": 1.0, "recent40_3x_positive_net_fraction": 1.0, "highest_observed_full3x_net_cell": "btcmix370_A25_H025_S28_L4", "highest_observed_is_on_axis_boundary": {"BTC_A_ownership_fraction": true, "reversal_return_hurdle": false, "trend_filter_lookback_days": false, "reversal_lookback_days": true}, "descriptive_full_Sharpe_cliff_edges": 18, "old_qualifications_preserved": true, "recent6of8_by_slow_center": {"27": 0, "28": 12, "29": 0}, "not_untouched_test_or_global_optimum": true}}。最高观测单元的预设网格边界标记已保存，不称全局最优；全期平台不能消除近期正折不足。

实际失败门槛计数：{"recent40_six_of_eight_positive5d_1x_folds": 42, "nine_of_twelve_positive_complete30d_1x_folds": 11}。逐项真实结论见上表和report.json，不因全期收益正而放宽门槛。219成本行、2847全期折、1752近期折、60102新日边界、135敏感性边、324匹配对照完整留档；6图36面板已实际打开。
独立只读核验23旧原生/69成本曲线、4062条已保存成交与76590条已保存资金费记录，原完整NAV SHA保持；没有旧原生模型重跑或父层新增成交；无新原生模型执行，23个已有原生账本经独立Decimal事件播放与原NAV SHA核验，父层按原值份额组合。54新配置162成本场景共88292106完整NAV点、2268全期/逐折和1458近期/逐折指标通过；42旧唯一结果SHA/资格保持，12027受保护文件不变。60新实际ID各自finish，120事件仅追加；54实际金融配置加6实际partial，全部完整spec在reserve前核对三个原生参数字典，无本轮失配定义。
只读监控实际检查exit0：7975研究项，168既有paper观察/10账户；7921旧展示行完整字典不变。原候选累计2730点/场景、2669分钟，0新增日决策/成交，实际新增资金费记录0条；现金与资金费逐条独立核验，收入不随成本放大，16旧结算未重复；旧SMA累计38697点，0新日决策/成交。两者均非十策略实时报价执行或长期盈利证据。
真实命令/传输异常记录2项，见read_failures.json。本轮登记、账户续接及提交由持续stdin排他锁保护。所有真实负收益分折/近期、成功/失败和完整账户账本保留；行情与HTTPpacket留ignoreddata并绑定SHA，不提交大行情或凭据。main普通非强推，freshfetch/独立allheads/完整tree/blob/行情核验通过后释放自己锁。
