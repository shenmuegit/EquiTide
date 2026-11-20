# 20261120T043737Z 复用真实银行净值的BTC/ETH独立目标组合

事前固定BTC目标1125/1250/1375与ETH目标3250/3500/4250完整3×3网格，ETH V6波动上限固定0.05625。旧1125/3500、1250/3250、1250/4250的3个策略组合和3个持有组合只读；6个真正新策略交叉组合、6个匹配持有基准全部先reserve后计算一次并finish。新组合通过历史门槛6/6、持有基准淘汰6/6，负收益不删除。事前代表1250/3500不随结果改变。严格同时改善收益、整体回撤、Sharpe、Calmar为0/6；没有独立未来或稳定实盘盈利资格。

完整读取39156条事件、19439个ID、482份既往结论及29份附加材料。初始16项真实回测缺口0。规范研究定义11665→11677，正式有结果11464；定义数、相关路径数均不是独立试验次数，没有DSR/PBO显著性证明。

经济含义：BTC本金3750、ETH本金15000、总18750和原始银行权重[1,1]保持；20/80是初始本金占比，不自动归一化，不转移资金。两轴是独立的原银行入场目标金额，目标总额4375–5625随格点变化，不再固定5000，更不固定实际动态敞口。较高收益可能只是目标金额/风险增加；同初始目标持有基准也不匹配动态风险。

底层12个已完成银行（6个策略、6个持有）全部只读复用：从原状态片段与原价格还原完整NAV后核对原全路径哈希，再在共同事件轴逐点相加美元净值；不缩放收益、平均Sharpe、不重跑策略或产生新底层订单。父组合无订单、再平衡、抵押转移或跨保证金净额。原ETH组件的一致性淘汰状态保留。

完整规则：All underlying BTC L29/H.03/E.005/V10cap.0275/strictdirection*ROC5>.0025 and ETHlongonly L5/H.02/E.0075/finiteEWMS16beta15/17/D3K.0075/V6cap.05625/M4R.0075VW9 native rules,quantities,funding,costs and margin are exactly the saved completed source banks. No source strategy or order is recomputed. New candidates only change which independently funded existingBTC/ETH banks are jointly held.

按时间验证：391日反复开发历史，2025-10-19 00:01→2026-11-14 00:01，33个闭合上下文日；固定规则无拟合、训练或标签，purge不适用、标签embargo为0。13个完整30日折+1日尾段，近40日8×5日、扩展21日5/5/5/6；跨折继承实际源银行现金/q，原终点计费平仓，整体回撤由连续完整NAV计算。不能称未触碰最终留出。

成本1/2/3倍沿用源银行实际数量核算：每边手续费5bp、半价差1bp、滑点2bp、0.5×过去20日样本对数波动×sqrt(实际订单额/过去20日quoteADV)，不利tick/LOT/最低金额/参与率≤0.001；完全抵押1倍入场与小时不利价1%维持保证金代理。真实永续资金费支出随倍数增加、收入不放大；线性永续无现货借币。原费用/资金费逐项相加并独立复核；父组合没有新成交成本。估计费用缺真实L2/TCA、完整阶梯、tick清算与容量实证。

|BTC/ETH目标USDT|初始总目标|类型|状态|净收益1x/2x/3x %|整体DD3 %|Sharpe3|Calmar3|正30日折1x|近40日正5日折1/2/3|
|---|---|---|---|---|---|---|---|---|---|
|1125/3250|4375|benchmark|rejected|-11.314905 / -12.020169 / -12.725476|15.915493|-1.376779|-0.749708|6/13|1/1/1（各/8）|
|1125/4250|5375|benchmark|rejected|-14.104069 / -14.961847 / -15.819506|19.715170|-1.356134|-0.753227|6/13|1/1/1（各/8）|
|1250/3500|4750|benchmark|rejected|-12.233681 / -12.997849 / -13.762069|17.184189|-1.370870|-0.751204|6/13|1/1/1（各/8）|
|1375/3250|4625|benchmark|rejected|-11.763301 / -12.510471 / -13.257689|16.559939|-1.375058|-0.750813|6/13|1/1/1（各/8）|
|1375/3500|4875|benchmark|rejected|-12.457879 / -13.243000 / -14.028173|17.505553|-1.369955|-0.751745|6/13|1/1/1（各/8）|
|1375/4250|5625|benchmark|rejected|-14.552465 / -15.452149 / -16.351720|20.347733|-1.354357|-0.754514|6/13|1/1/1（各/8）|
|1125/3250|4375|candidate|passed|8.699731 / 8.180286 / 7.660813|1.164147|2.328797|6.127801|12/13|6/6/6（各/8）|
|1125/4250|5375|candidate|passed|10.110815 / 9.515633 / 8.920584|1.437873|2.345627|5.774816|12/13|6/6/6（各/8）|
|1250/3500|4750|candidate|passed|9.481385 / 8.906830 / 8.332188|1.324722|2.307813|5.855713|12/13|6/6/6（各/8）|
|1375/3250|4625|candidate|passed|9.565809 / 8.981918 / 8.398018|1.427968|2.271710|5.475137|12/13|6/6/6（各/8）|
|1375/3500|4875|candidate|passed|9.918153 / 9.315324 / 8.712446|1.426917|2.288016|5.683752|12/13|6/6/6（各/8）|
|1375/4250|5625|candidate|passed|10.976893 / 10.317265 / 9.657789|1.497113|2.318474|6.003275|12/13|6/6/6（各/8）|

预设失败判据：全期/近期各成本正、1x≥10/13正月、近40日各成本≥6/8正5日折、扩展各成本≥3/4正折、DD3≤25%、邻域正收益与近期合格比例≥60%、至少4次底层平仓、1x(毛价差收益+资金费)/费用≥2.5，无拒单/负抵押/保证金代理违规、原终点flat。持有基准无可调alpha参数，不强行构造邻域。

parent_independentEntry_matched_hold_BTCN1125_ETHN3250_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_independentEntry_matched_hold_BTCN1125_ETHN4250_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_independentEntry_matched_hold_BTCN1250_ETHN3500_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_independentEntry_matched_hold_BTCN1375_ETHN3250_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_independentEntry_matched_hold_BTCN1375_ETHN3500_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_independentEntry_matched_hold_BTCN1375_ETHN4250_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_independentEntry_BTCN1125_ETHN3250_Cap0p05625_C3750_15000_391d：通过预设历史门槛，待独立未来验证。
parent_independentEntry_BTCN1125_ETHN4250_Cap0p05625_C3750_15000_391d：通过预设历史门槛，待独立未来验证。
parent_independentEntry_BTCN1250_ETHN3500_Cap0p05625_C3750_15000_391d：通过预设历史门槛，待独立未来验证。
parent_independentEntry_BTCN1375_ETHN3250_Cap0p05625_C3750_15000_391d：通过预设历史门槛，待独立未来验证。
parent_independentEntry_BTCN1375_ETHN3500_Cap0p05625_C3750_15000_391d：通过预设历史门槛，待独立未来验证。
parent_independentEntry_BTCN1375_ETHN4250_Cap0p05625_C3750_15000_391d：通过预设历史门槛，待独立未来验证。

相对旧1125/3500对照的三倍成本变化：
BTC/ETH=1125/3250，目标总额4375：收益-0.314428个百分点，整体DD-0.061633个百分点，Sharpe-0.008376，Calmar0.069848；敞口不同，不解释为独立alpha提升。
BTC/ETH=1125/4250，目标总额5375：收益0.945343个百分点，整体DD0.212093个百分点，Sharpe0.008454，Calmar-0.283137；敞口不同，不解释为独立alpha提升。
BTC/ETH=1250/3500，目标总额4750：收益0.356947个百分点，整体DD0.098943个百分点，Sharpe-0.029360，Calmar-0.202239；敞口不同，不解释为独立alpha提升。
BTC/ETH=1375/3250，目标总额4625：收益0.422777个百分点，整体DD0.202188个百分点，Sharpe-0.065463，Calmar-0.582815；敞口不同，不解释为独立alpha提升。
BTC/ETH=1375/3500，目标总额4875：收益0.737205个百分点，整体DD0.201137个百分点，Sharpe-0.049157，Calmar-0.374200；敞口不同，不解释为独立alpha提升。
BTC/ETH=1375/4250，目标总额5625：收益1.682548个百分点，整体DD0.271333个百分点，Sharpe-0.018699，Calmar-0.054677；敞口不同，不解释为独立alpha提升。

敏感性全部保存：90个成本场景、1260逐折、720近期折、360扩展折、35280日NAV行、27个匹配持有对比及12条相邻边；新12配置有12条不同完整成本路径。启发式跳变边=[{"scope": "parent", "from": "parent_independentEntry_BTCN1125_ETHN3250_Cap0p05625_C3750_15000_391d", "to": "parent_independentEntry_BTCN1250_ETHN3250_Cap0p05625_C3750_15000_391d", "delta_net_pp": 0.3569471506753574, "delta_sharpe": -0.033827441627674926, "delta_DD_pp": 0.16155215959161584, "delta_Calmar": -0.49665563509904764}, {"scope": "parent", "from": "parent_independentEntry_BTCN1125_ETHN3500_Cap0p05625_C3750_15000_391d", "to": "parent_independentEntry_BTCN1250_ETHN3500_Cap0p05625_C3750_15000_391d", "delta_net_pp": 0.35694715067535654, "delta_sharpe": -0.029360305781005902, "delta_DD_pp": 0.09894271612633787, "delta_Calmar": -0.2022393083084948}, {"scope": "parent", "from": "parent_independentEntry_BTCN1250_ETHN3250_Cap0p05625_C3750_15000_391d", "to": "parent_independentEntry_BTCN1375_ETHN3250_Cap0p05625_C3750_15000_391d", "delta_net_pp": 0.3802582765679787, "delta_sharpe": -0.0232591294717861, "delta_DD_pp": 0.10226865822485776, "delta_Calmar": -0.1560078565991594}, {"scope": "parent", "from": "parent_independentEntry_BTCN1250_ETHN3500_Cap0p05625_C3750_15000_391d", "to": "parent_independentEntry_BTCN1250_ETHN4250_Cap0p05625_C3750_15000_391d", "delta_net_pp": 0.9453428648805282, "delta_sharpe": 0.020596202574926448, "delta_DD_pp": 0.13334677226257696, "delta_Calmar": 0.06632260414286506}, {"scope": "parent", "from": "parent_independentEntry_BTCN1250_ETHN3500_Cap0p05625_C3750_15000_391d", "to": "parent_independentEntry_BTCN1375_ETHN3500_Cap0p05625_C3750_15000_391d", "delta_net_pp": 0.3802582765679574, "delta_sharpe": -0.019796491613850442, "delta_DD_pp": 0.10219448302252188, "delta_Calmar": -0.1719611248570425}, {"scope": "parent", "from": "parent_independentEntry_BTCN1375_ETHN3500_Cap0p05625_C3750_15000_391d", "to": "parent_independentEntry_BTCN1375_ETHN4250_Cap0p05625_C3750_15000_391d", "delta_net_pp": 0.9453428648805282, "delta_sharpe": 0.030458222152509595, "delta_DD_pp": 0.0701960505436694, "delta_Calmar": 0.31952357127477793}]
收益最优若在金额网格边缘，仅作敞口诊断；不根据结果扩网格或替换代表。小网格不证明全域稳健。
独立核验只读源银行36条完整曲线、14076个原政策决策、42228条资金费、原成交/费用/小时风险，并核验新组合36条连续NAV、逐折和全部门槛；新增native策略决策/执行次数为0。父组合相对旧中心的货币现金流桥接见sizing_effect_decomposition.json。

本轮四账户各续接120个闭合分钟，日决策{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}；实际资金费记录{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}。本轮各永续只处理当前各自窗口实际新增结算，不重复旧08:00:00.002资金费。各账户现金变化逐笔核对，持仓/desired/入场价/累计执行费用保持。完整71日SPOT权威及原70精确前缀只读，分钟包不是日线权威。首08来源UTC保持2026-11-19T20:40:54.314631Z，实际fundingTime1795075200002不替换为名义整点；目前三永续均恰好记08一次。下一SMA/candidate['2026-11-19T12:30:00Z', '2026-11-19T14:30:00Z']，L4/FEWM['2026-11-19T14:10:00Z', '2026-11-19T16:10:00Z']，均不重复08，先查询实际特殊资金费；下一日决策Nov20_00:01。不重置本金、不强制平仓、不采用新研究配置。

原SMA三倍成本累计-7.468958%；原账户为延迟shadow，180日/六折资格未成熟。十策略仅只读汇总，未改冻结规则/本金/持仓或产生新成交。
保存19份唯一公共GET回执，本轮19、旧复用0、已记录运输错误1（内置重试的失败子请求URL/时间/HTTP响应未独立采集，保留stderr，不补造缺失细节）；旧首资金费来源UTC/SHA保留，完整71日SPOT权威只读。其他实际失败事实：[{"type": "unused_template_file_read_failure", "native_chunk": "22fd2f", "native_exit_code": 1, "path": "research/experiments/20261120T043737Z/check_midnight_archive.py", "reason": "Inspection tried an obsolete unused command label; template has no such file. No phase invoked, no reservation or computation. Normal23-phase workflow does not include midnight_archive.", "resolved": true}, {"url": "https://fapi.binance.com/fapi/v1/klines?symbol=ETHUSDT&interval=1m&startTime=1795090140000&endTime=1795097400000&limit=1500", "started_utc": "2026-11-20T04:52:05.318590+00:00", "http_status": 0, "curl_exit_code": 35, "raw": "data/raw/binance/l4h02_forward/20261120T043737Z/http_0005.gz", "sha256": "f61f27bd17de546264aa58f40f3aafaac7021e0ef69c17f6b1b4cd7664a037ec", "bytes": 0, "stderr": "curl: (35) TLS connect error: error:0A000126:SSL routines::unexpected eof while reading\n", "transport": "verifiedTLSmin1.2HTTP1.1 publicGET,bounded3attempts", "resolved": true, "resolution": "Same exact URL has validated successful saved public bytes; original capture time retained, including earlier source reuse documented before first reserve. Successful original account packet and audit retained."}]
监控生成成功=True，11236研究配置，11224旧行完整字典不变。

实际完成阶段命令（完成目录不得重跑市场/账户，仅保留核验和数据哈希）：

```sh
cd /home/desktop/Documents/Codex/EquiTide
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T043737Z/commands.py prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T043737Z/commands.py freeze
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T043737Z/commands.py units
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T043737Z/commands.py bind
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T043737Z/commands.py reserve_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T043737Z/commands.py reserve_1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T043737Z/commands.py evaluate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T043737Z/commands.py audit
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T043737Z/commands.py exports
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T043737Z/commands.py finish_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T043737Z/commands.py finish_1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T043737Z/commands.py research_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T043737Z/commands.py l4h02
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T043737Z/commands.py fewm
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T043737Z/commands.py candidate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T043737Z/commands.py forward
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T043737Z/commands.py accounts_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T043737Z/commands.py journal
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T043737Z/commands.py sources_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T043737Z/commands.py gates
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T043737Z/commands.py feed
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T043737Z/commands.py collect
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T043737Z/commands.py final_checks
```

字段格式与版本见primary_source_access.json的[Binance官方REST文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)及[公共数据README](https://github.com/binance/binance-public-data/blob/master/README.md)。所有负收益、失败、来源和冻结规则均保留；成本系数是研究假设。

ETH金额步长为250及750 USDT，邻域按格点索引；启发式Sharpe跳变是诊断，未加入事前冻结的淘汰门槛。passed仅代表报告列出的历史门槛通过，不代表跳变已消除或全域稳健。旧顶层fixed_entry_notionals_usdt是继承的1000/4000基准元数据，不是本轮执行金额；实际轴、每配置parameters和原组件SHA为准，详见legacy_plan_metadata_resolution_before_reserve.json。

下一L4/FEWM14:10→16:10跨名义16点；必须先查询真实结算，保存新事件首次公共字段、原始毫秒时间和捕获UTC并在任何reserve前绑定，按各自继承持仓及成本记账。不得预记资金费或重复旧结算。下一SMA/candidate12:30→14:30，下一日决策仍为Nov20 00:01。下轮仅供查重的4个新图提案见next_bank_graph_availability.json，本轮未reserve或计算。
