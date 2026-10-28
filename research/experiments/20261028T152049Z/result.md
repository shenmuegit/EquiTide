# 20261028T152049Z 固定银行份额与多数门控参数联合验证

实际38项：36候选＋2同权重恒多对照；历史通过4、候选淘汰32。完整读取21116事件/10454ID、217份结论，初始16项实际证据齐全。

Preset raw ownership grid tests whether BTC/ETH capital allocation broadens the S28-only recent qualification seen in prior majority-hurdle study. Change weights jointly with H/S/L; no component amount resimulation, no result-driven extension or original future-account replacement.

Raw BTC ownership w=0.5/1/1.5 and ETH ownership1, never normalized. Initial capital=10000*w+10000=15000/20000/25000. Effective inherited entry budget1000*w+3000=3500/4000/4500. Ownership multiplies original full-bank NAV/cash/position/economic cost/funding, not per-order size; original nonlinear impact,lot constraints and margin paths retained. Source execution/event counts are unweighted counts of underlying bank actions. No transfers,additional leverage,cross-margin,rebalance,cash yield or fund-unit transactions.

Static ownership of existing fully funded independent source banks. BTC ROC31/H4/E1 N1000, ETH adjacent S-1/S/S+1 majority gated reversal L3/4 H2/2.5/3 E0 N3000. No new native signals/orders/funding simulations.

事前固定 BTC原值份额0.5/1/1.5、ETH份额1，与ETH阈值2/2.5/3%、慢中心27/28/29和快反转3/4日联合形成四维54格、135相邻边；18个raw1/1旧格只读，36新候选和2新恒多对照均先成功reserve，再实际计算。父本金15000/20000/25000，继承入场预算3500/4000/4500，占比23.333%/20%/18%；不归一化。相同组件及原值权重进行语义查重，未按名称或顺序伪创新。

21个旧原生/63成本NAV由已保存现金、数量与entry片段重建并校验原SHA；不重跑信号、下单或资金费模型。源账本的非线性成交量冲击及tick/lot/抵押、资金费和风险完整保留。份额缩放的是经济所有权；成本/损益/资金费按份额乘，源成交及事件计数不乘；不能把本研究当BTC N500/N1500的新订单回测或按缩放后数量重新估成本。实际模拟银行之间不净额成交、不交叉救助。

370日连续OOS为2025-10-19UTC00:01至2026-10-24UTC00:01。33日上下文含30日预热与3日初始embargo，静态规则无训练/未来标签、purge不适用；日信号只用此前完成close、数量由此前close取lot，UTC00:01实际OPEN执行。12个完整30日折及10日尾折承接现金/仓位；近期40日从day330继承，8×5日折不重置或额外平仓，终点原定平仓计费。所有组合沿共同(ns,eventcode)时轴因果承接源NAV，整体回撤及Sharpe从实际加权连续净值重新计算。

每侧5bp费、1bp半价差、2bp滑点加0.5×此前20日样本日log波动×sqrt(实际源订单金额/此前20日quoteADV)冲击；参与率≤0.1%，全额抵押入场。资金费=-有符号数量×实际结算mark×rate，流出乘成本倍数，收入不放大；永续无需虚构现货借币。1%维持保证金与已闭合小时不利mark仅风险代理，缺盘口/TCA/历史完整阶梯和tick清算证据。

门槛保持全期及近期三档净正、月正折≥9/12、近期正折≥6/8、三倍连续整体DD≤25%、四维邻域三倍净正≥60%、≥4往返、参考毛利＋资金费/成本≥2.5、现金/拒单/独立银行风险违规0、终点空仓且≥180日。恒多仅对照，以reference_only原因rejected，不冒称alpha资格。

与同权重恒多及现金0比较；旧1/1对照资本/风险不同，报告金额与收益率，不作等风险比较。全历史多次使用，属于开发验证；38个新相关试验加所有先前试验存在多重选择偏差，无DSR/PBO或未触碰最终测试资格。

{"new_financial_configs": 38, "new_native_components": 0, "new_passive_parents": 38, "candidate_configs": 36, "benchmark_configs": 2, "passed_candidates": 4, "rejected_candidates": 32, "positive_configs_by_cost": {"1": 36, "2": 36, "3": 36}, "failed_criteria_counts": {"recent40_six_of_eight_positive5d_1x_folds": 32, "nine_of_twelve_positive_complete30d_1x_folds": 4}, "rows": {"cost": 171, "full_folds": 2223, "recent40_folds": 1368, "daily_NAV": 42294, "edges": 135, "reference_comparisons": 216}, "by_BTC_raw_ownership": {"0.5": {"candidates": 18, "passed": 4, "recent6of8": 4}, "1.5": {"candidates": 18, "passed": 0, "recent6of8": 0}}}

原单S28冻结候选与SMA65从UTC12:30续接至14:30，持仓/现金/成本/资金费/风险栈/完整净值前缀承接，不换新权重，不重复08资金费或日决策，不截止强平。下一16:30窗口含16:00实际资金费、下一日决策Oct29UTC00:01。延迟真实闭合行情重建，不是十策略同期报价执行或真实订单。

背景沿用以前实际访问的一手AQR Time Series Momentum与Trading Costs of Asset Pricing Anomalies；本权重/多数门控为研究推论，不是论文复制或收益移植。新历史通过也不代表稳定实盘盈利。

复现工作目录/home/desktop/Documents/Codex/EquiTide；audit.py独立播放记录事件并核对每个加权NAV、折、资金费和原资格。check_sources.py/audit_forward.py/audit_candidate.py/check_feed.py只读证据，forward.py --reproduce离线复现；不重新reserve/evaluate/summarize已完成配置。main普通非强推，远端完整tree/blob/SHA核验后释放本轮锁。

本轮工程失败与完整定义修正均真实留档：审计源码预检出现一次语法错误，首次评估缺少metric别名，恢复时因空结果目录存在而停止，随后只读审计缺少兼容EXITS导入。前三次未生成完整配置结果；恢复保留原日志/源码/退出码，不改规则、权重、成本或失败门槛。
全spec复核发现24项继承的ETH_trend_gate_lookbacks_days为[26,27,28]，与S28/29的实际组件不符。原矛盾定义各自finish abandoned、result_available=false，原spec及临时实际组件计算报告/账本仍保留；不能把它们作为精确声明规则的有效回测。24份正确列表重新reserve成功后才计算，14个已完成且定义完全一致的结果逐字复用。最终38个有效实际配置、24个无有效精确结果的退休定义分别登记，未新增24个独立市场试验；源组件、原值权重、参数中心、边界和门槛未改。详见alias_correction.json、invalid_spec_report.json、corrected_evaluation.json及read_failures.json。
原始临时报告只作失配证据，最终有效收益与资格以report.json及其登记指纹为准；监控仅读取真实finish结果，不展示abandoned为通过。下一轮须在reserve前比较全部冗余周期别名与所选源spec，不能只核对中心S。
一手背景：[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)、[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)，沿用2026-10-27实际访问记录，本轮未声称新访问或复制论文策略。

登记进程中断亦保留真实证据：首次finish外层进程实际退出143，原因未明；检查时37项已完成、1项仍reserved，已有36份逐命令回执。恢复只读核对37项已完成状态及报告SHA，并仅对剩余1项执行finish，未伪造丢失的命令输出或重算结果。详见finish_interruption.json、finish_partial_receipts_before_interrupt.json和finish_resume_verification.json。

历史通过项目只读冻结检查：4项。完整spec/来源/报告/账本SHA见candidate_validation.json；不改原冻结L3未来账户。
voteweight370_B050_E100_H020_S28_L3：1/2/3倍370日收益[10.83873645790785, 9.122372382194488, 7.404803446647801]%，整体3倍回撤4.00689290333629%，近期3倍收益1.5348325255682083%；完整月正折10/12、近期6/8，邻域全期3倍净正24/24、原始近期6/8仅8/24。仅通过预设历史门槛，尚无该新配置独立未来证据。
voteweight370_B050_E100_H020_S28_L4：1/2/3倍370日收益[10.271697778899558, 8.773908550950305, 7.275658360501058]%，整体3倍回撤3.5093072675317916%，近期3倍收益1.4581937838218373%；完整月正折10/12、近期6/8，邻域全期3倍净正24/24、原始近期6/8仅8/24。仅通过预设历史门槛，尚无该新配置独立未来证据。
voteweight370_B050_E100_H025_S28_L3：1/2/3倍370日收益[10.17126366281258, 8.738702169913148, 7.305302409613734]%，整体3倍回撤3.2795347702281763%，近期3倍收益1.5362775948063012%；完整月正折9/12、近期6/8，邻域全期3倍净正36/36、原始近期6/8仅8/36。仅通过预设历史门槛，尚无该新配置独立未来证据。
voteweight370_B050_E100_H025_S28_L4：1/2/3倍370日收益[11.14583167602088, 9.790236063434365, 8.434179882514536]%，整体3倍回撤3.484446379627315%，近期3倍收益1.4423895800557807%；完整月正折11/12、近期6/8，邻域全期3倍净正36/36、原始近期6/8仅8/36。仅通过预设历史门槛，尚无该新配置独立未来证据。

逐配置结果（收益/回撤单位%，三倍全期回撤使用完整连续OOS）：

|配置|1x收益|2x收益|3x收益|3x最大回撤|近期3x收益|1x月正折|1x近期正折|结论|
|---|---:|---:|---:|---:|---:|---:|---:|---|
|voteweight370_B050_E100_H025_S28_L4|11.145832|9.790236|8.434180|3.484446|1.442390|11/12|6/8|passed|
|voteweight370_B050_E100_H030_S28_L4|10.701978|9.487951|8.273975|2.632277|0.871935|11/12|5/8|rejected|
|voteweight370_B050_E100_H025_S27_L4|10.416534|9.120967|7.825059|3.768477|1.318749|10/12|5/8|rejected|
|voteweight370_B050_E100_H030_S27_L4|10.041749|8.920156|7.798633|2.631518|0.745364|11/12|4/8|rejected|
|voteweight370_B050_E100_H020_S29_L3|11.126061|9.441375|7.755502|3.838237|1.503900|8/12|5/8|rejected|
|voteweight370_B050_E100_H025_S29_L3|10.570807|9.139667|7.707629|3.274953|1.504578|9/12|5/8|rejected|
|voteweight370_B050_E100_H030_S29_L4|9.754508|8.615360|7.476348|3.067990|0.852866|10/12|4/8|rejected|
|voteweight370_B050_E100_H020_S27_L3|10.830450|9.144975|7.458373|4.014869|1.401482|9/12|5/8|rejected|
|voteweight370_B050_E100_H025_S29_L4|10.045629|8.732186|7.418460|3.526761|1.430322|10/12|5/8|rejected|
|voteweight370_B050_E100_H020_S28_L3|10.838736|9.122372|7.404803|4.006893|1.534833|10/12|6/8|passed|
|voteweight370_B050_E100_H025_S27_L3|10.210308|8.804162|7.397392|3.580063|1.402289|8/12|5/8|rejected|
|voteweight370_B050_E100_H025_S28_L3|10.171264|8.738702|7.305302|3.279535|1.536278|9/12|6/8|passed|
|voteweight370_B050_E100_H020_S28_L4|10.271698|8.773909|7.275658|3.509307|1.458194|10/12|6/8|passed|
|voteweight370_B050_E100_H020_S27_L4|10.050703|8.549078|7.046869|3.795359|1.328464|9/12|5/8|rejected|
|voteweight370_B050_E100_H020_S29_L4|9.158165|7.702515|6.246582|3.552232|1.446327|8/12|5/8|rejected|
|voteweight370_B150_E100_H025_S28_L4|7.885156|6.873149|5.860866|2.591237|1.040923|11/12|5/8|rejected|
|voteweight370_B150_E100_H030_S28_L4|7.618844|6.691778|5.764743|2.022648|0.692176|10/12|4/8|rejected|
|voteweight370_B150_E100_H025_S27_L4|7.447577|6.471588|5.495393|2.590893|0.964281|10/12|5/8|rejected|
|voteweight370_B150_E100_H030_S27_L4|7.222707|6.351101|5.479538|2.022375|0.614318|9/12|4/8|rejected|
|voteweight370_B150_E100_H020_S29_L3|7.873294|6.663833|5.453659|3.116412|1.076783|9/12|5/8|rejected|
|voteweight370_B050_E100_H030_S29_L3|8.101919|6.770395|5.437866|3.321052|0.948458|9/12|4/8|rejected|
|voteweight370_B150_E100_H025_S29_L3|7.540141|6.482808|5.424935|2.639519|1.077079|10/12|5/8|rejected|
|voteweight370_B150_E100_H030_S29_L4|7.050362|6.168224|5.286167|2.669040|0.679722|9/12|4/8|rejected|
|voteweight370_B150_E100_H020_S27_L3|7.695927|6.485992|5.275382|3.138860|1.013841|10/12|5/8|rejected|
|voteweight370_B150_E100_H025_S29_L4|7.225034|6.238319|5.251434|2.669040|1.031277|10/12|5/8|rejected|
|voteweight370_B150_E100_H020_S28_L3|7.700899|6.472431|5.243240|3.134015|1.094711|10/12|5/8|rejected|
|voteweight370_B150_E100_H025_S27_L3|7.323842|6.281505|5.238793|2.604959|1.014197|10/12|5/8|rejected|
|voteweight370_B150_E100_H025_S28_L3|7.300415|6.242229|5.183539|2.600113|1.095340|11/12|5/8|rejected|
|voteweight370_B150_E100_H020_S28_L4|7.360676|6.263353|5.165753|2.602490|1.047875|11/12|5/8|rejected|
|voteweight370_B050_E100_H030_S27_L3|7.741419|6.434891|5.127629|3.630533|0.843475|8/12|4/8|rejected|
|voteweight370_B150_E100_H020_S27_L4|7.228079|6.128454|5.028479|2.602143|0.968609|10/12|5/8|rejected|
|voteweight370_B050_E100_H030_S28_L3|7.526955|6.230876|4.933848|3.329038|0.979326|9/12|5/8|rejected|
|voteweight370_B150_E100_H020_S29_L4|6.692556|5.620517|4.548307|2.928220|1.038284|9/12|5/8|rejected|
|voteweight370_B150_E100_H030_S29_L3|6.058808|5.061245|4.063077|2.662195|0.735580|10/12|4/8|rejected|
|voteweight370_B150_E100_H030_S27_L3|5.842508|4.859942|3.876935|2.627366|0.671694|10/12|4/8|rejected|
|voteweight370_B150_E100_H030_S28_L3|5.713830|4.737533|3.760667|2.682486|0.753610|11/12|4/8|rejected|
|voteweight370_hold_B150_E100|-6.432610|-6.948392|-7.464182|12.120002|-0.279191|6/12|4/8|rejected|
|voteweight370_hold_B050_E100|-8.985248|-9.630548|-10.275853|16.414524|-0.671000|6/12|4/8|rejected|

全网格Sharpe正值比例、收益正值比例及最高观测单元边界诊断（只读已有结果，不改变资格）：{"parent": {"dimension_count": 4, "cells": 54, "full3x_positive_Sharpe_fraction": 1.0, "recent40_3x_positive_Sharpe_fraction": 1.0, "full3x_positive_net_fraction": 1.0, "recent40_3x_positive_net_fraction": 1.0, "highest_observed_full3x_net_cell": "voteweight370_B050_E100_H025_S28_L4", "highest_observed_is_on_axis_boundary": {"BTC_ownership_multiplier": true, "reversal_return_hurdle": false, "trend_filter_lookback_days": false, "reversal_lookback_days": true}, "descriptive_full_Sharpe_cliff_edges": 20, "old_qualifications_preserved": true, "recent6of8_by_raw_weight_and_S": {"0.5": {"27": 0, "28": 4, "29": 0}, "1": {"27": 0, "28": 4, "29": 0}, "1.5": {"27": 0, "28": 0, "29": 0}}, "not_untouched_test_or_global_optimum": true}}。最高观测单元的预设网格边界标记已保存，不称全局最优；全期平台不能消除近期正折不足。

实际失败门槛计数：{"recent40_six_of_eight_positive5d_1x_folds": 32, "nine_of_twelve_positive_complete30d_1x_folds": 4}。逐项真实结论见上表和report.json，不因全期收益正而放宽门槛。171成本行、2223全期折、1368近期折、42294新日边界、135敏感性边、216匹配对照完整留档；6图36面板已实际打开。
独立只读核验21旧原生/63成本曲线、3846条已保存成交与69930条已保存资金费记录，原完整NAV SHA保持；没有旧原生模型重跑或父层新增成交；无新原生模型执行，21个已有原生账本经独立Decimal事件播放与原NAV SHA核验，父层按原值份额组合。38新配置114成本场景共62131482完整NAV点、1596全期/逐折和1026近期/逐折指标通过；40旧唯一结果SHA/资格保持，11057受保护文件不变。68新ID各自finish，136事件仅追加；38实际金融配置加6实际partial，24别名失配定义abandoned无有效精确结果。
只读监控实际检查exit0：7786研究项，165既有paper观察/10账户；7748旧展示行完整字典不变。原候选累计2362点/场景、2309分钟，0新增日决策/成交，实际新增资金费记录0条；现金与资金费逐条独立核验，收入不随成本放大，08旧结算未重复；旧SMA累计38337点，0新日决策/成交。两者均非十策略实时报价执行或长期盈利证据。
真实命令/传输异常记录6项，见read_failures.json。本轮登记、账户续接及提交由持续stdin排他锁保护。所有真实负收益分折/近期、成功/失败和完整账户账本保留；行情与HTTPpacket留ignoreddata并绑定SHA，不提交大行情或凭据。main普通非强推，freshfetch/独立allheads/完整tree/blob/行情核验通过后释放自己锁。
