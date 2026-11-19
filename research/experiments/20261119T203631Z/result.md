# 20261119T203631Z 复用真实银行净值的BTC/ETH独立目标组合

事前固定BTC目标1000/1250/1500与ETH目标3250/3750/4250完整3×3网格，ETH V6波动上限固定0.05625。旧BTC1250金额的3个策略组合和3个持有组合只读；6个真正新策略交叉组合、6个匹配持有基准全部先reserve后计算一次并finish。新组合通过历史门槛6/6、持有基准淘汰6/6，负收益不删除。事前代表1000/3750不随结果改变。严格同时改善收益、整体回撤、Sharpe、Calmar为0/6；没有独立未来或稳定实盘盈利资格。

完整读取38932条事件、19327个ID、478份既往结论及29份附加材料。初始16项真实回测缺口0。规范研究定义11629→11641，正式有结果11428；定义数、相关路径数均不是独立试验次数，没有DSR/PBO显著性证明。

经济含义：BTC本金3750、ETH本金15000、总18750和原始银行权重[1,1]保持；20/80是初始本金占比，不自动归一化，不转移资金。两轴是独立的原银行入场目标金额，目标总额4250–5750随格点变化，不再固定5000，更不固定实际动态敞口。较高收益可能只是目标金额/风险增加；同初始目标持有基准也不匹配动态风险。

底层12个已完成银行（6个策略、6个持有）全部只读复用：从原状态片段与原价格还原完整NAV后核对原全路径哈希，再在共同事件轴逐点相加美元净值；不缩放收益、平均Sharpe、不重跑策略或产生新底层订单。父组合无订单、再平衡、抵押转移或跨保证金净额。原ETH组件的一致性淘汰状态保留。

完整规则：All underlying BTC L29/H.03/E.005/V10cap.0275/strictdirection*ROC5>.0025 and ETHlongonly L5/H.02/E.0075/finiteEWMS16beta15/17/D3K.0075/V6cap.05625/M4R.0075VW9 native rules,quantities,funding,costs and margin are exactly the saved completed source banks. No source strategy or order is recomputed. New candidates only change which independently funded existingBTC/ETH banks are jointly held.

按时间验证：391日反复开发历史，2025-10-19 00:01→2026-11-14 00:01，33个闭合上下文日；固定规则无拟合、训练或标签，purge不适用、标签embargo为0。13个完整30日折+1日尾段，近40日8×5日、扩展21日5/5/5/6；跨折继承实际源银行现金/q，原终点计费平仓，整体回撤由连续完整NAV计算。不能称未触碰最终留出。

成本1/2/3倍沿用源银行实际数量核算：每边手续费5bp、半价差1bp、滑点2bp、0.5×过去20日样本对数波动×sqrt(实际订单额/过去20日quoteADV)，不利tick/LOT/最低金额/参与率≤0.001；完全抵押1倍入场与小时不利价1%维持保证金代理。真实永续资金费支出随倍数增加、收入不放大；线性永续无现货借币。原费用/资金费逐项相加并独立复核；父组合没有新成交成本。估计费用缺真实L2/TCA、完整阶梯、tick清算与容量实证。

|BTC/ETH目标USDT|初始总目标|类型|状态|净收益1x/2x/3x %|整体DD3 %|Sharpe3|Calmar3|正30日折1x|近40日正5日折1/2/3|
|---|---|---|---|---|---|---|---|---|---|
|1000/3250|4250|benchmark|rejected|-11.090702 / -11.775008 / -12.459367|15.595789|-1.377440|-0.749005|6/13|1/1/1（各/8）|
|1000/3750|4750|benchmark|rejected|-12.479858 / -13.240066 / -14.000385|17.494092|-1.367225|-0.750740|6/13|1/1/1（各/8）|
|1000/4250|5250|benchmark|rejected|-13.879866 / -14.716686 / -15.553398|19.398497|-1.356868|-0.752572|6/13|1/1/1（各/8）|
|1500/3250|4750|benchmark|rejected|-12.211705 / -13.000781 / -13.789913|17.203365|-1.372881|-0.751892|6/13|1/1/1（各/8）|
|1500/3750|5250|benchmark|rejected|-13.600861 / -14.465839 / -15.330931|19.089380|-1.362695|-0.753757|6/13|1/1/1（各/8）|
|1500/4250|5750|benchmark|rejected|-15.000869 / -15.942459 / -16.883943|20.981683|-1.352216|-0.755684|6/13|1/1/1（各/8）|
|1000/3250|4250|candidate|passed|8.230913 / 7.741184 / 7.251448|1.143046|2.339463|5.908197|12/13|6/6/6（各/8）|
|1000/3750|4750|candidate|passed|8.935942 / 8.408236 / 7.880873|1.284300|2.344206|5.713673|12/13|6/6/6（各/8）|
|1000/4250|5250|candidate|passed|9.641997 / 9.076531 / 8.511220|1.430302|2.339876|5.539685|12/13|6/6/6（各/8）|
|1500/3250|4750|candidate|passed|9.994210 / 9.381665 / 8.769090|1.537844|2.257023|5.307966|12/13|6/6/6（各/8）|
|1500/3750|5250|candidate|passed|10.699239 / 10.048717 / 9.398515|1.535583|2.290843|5.696211|12/13|6/6/6（各/8）|
|1500/4250|5750|candidate|passed|11.405294 / 10.717012 / 10.028861|1.533330|2.312809|6.085984|12/13|6/6/6（各/8）|

预设失败判据：全期/近期各成本正、1x≥10/13正月、近40日各成本≥6/8正5日折、扩展各成本≥3/4正折、DD3≤25%、邻域正收益与近期合格比例≥60%、至少4次底层平仓、1x(毛价差收益+资金费)/费用≥2.5，无拒单/负抵押/保证金代理违规、原终点flat。持有基准无可调alpha参数，不强行构造邻域。

parent_independentEntry_matched_hold_BTCN1000_ETHN3250_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_independentEntry_matched_hold_BTCN1000_ETHN3750_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_independentEntry_matched_hold_BTCN1000_ETHN4250_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_independentEntry_matched_hold_BTCN1500_ETHN3250_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_independentEntry_matched_hold_BTCN1500_ETHN3750_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_independentEntry_matched_hold_BTCN1500_ETHN4250_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_independentEntry_BTCN1000_ETHN3250_Cap0p05625_C3750_15000_391d：通过预设历史门槛，待独立未来验证。
parent_independentEntry_BTCN1000_ETHN3750_Cap0p05625_C3750_15000_391d：通过预设历史门槛，待独立未来验证。
parent_independentEntry_BTCN1000_ETHN4250_Cap0p05625_C3750_15000_391d：通过预设历史门槛，待独立未来验证。
parent_independentEntry_BTCN1500_ETHN3250_Cap0p05625_C3750_15000_391d：通过预设历史门槛，待独立未来验证。
parent_independentEntry_BTCN1500_ETHN3750_Cap0p05625_C3750_15000_391d：通过预设历史门槛，待独立未来验证。
parent_independentEntry_BTCN1500_ETHN4250_Cap0p05625_C3750_15000_391d：通过预设历史门槛，待独立未来验证。

相对旧1250/3750中心的三倍成本变化：
BTC/ETH=1000/3250，目标总额4250：收益-1.395737个百分点，整体DD-0.189494个百分点，Sharpe0.022060，Calmar-0.132638；敞口不同，不解释为独立alpha提升。
BTC/ETH=1000/3750，目标总额4750：收益-0.766312个百分点，整体DD-0.048241个百分点，Sharpe0.026803，Calmar-0.327162；敞口不同，不解释为独立alpha提升。
BTC/ETH=1000/4250，目标总额5250：收益-0.135965个百分点，整体DD0.097762个百分点，Sharpe0.022473，Calmar-0.501150；敞口不同，不解释为独立alpha提升。
BTC/ETH=1500/3250，目标总额4750：收益0.121905个百分点，整体DD0.205304个百分点，Sharpe-0.060380，Calmar-0.732869；敞口不同，不解释为独立alpha提升。
BTC/ETH=1500/3750，目标总额5250：收益0.751330个百分点，整体DD0.203043个百分点，Sharpe-0.026560，Calmar-0.344624；敞口不同，不解释为独立alpha提升。
BTC/ETH=1500/4250，目标总额5750：收益1.381676个百分点，整体DD0.200790个百分点，Sharpe-0.004594，Calmar0.045149；敞口不同，不解释为独立alpha提升。

敏感性全部保存：90个成本场景、1260逐折、720近期折、360扩展折、35280日NAV行、27个匹配持有对比及12条相邻边；新12配置有12条不同完整成本路径。启发式跳变边=[{"scope": "parent", "from": "parent_independentEntry_BTCN1000_ETHN3250_Cap0p05625_C3750_15000_391d", "to": "parent_independentEntry_BTCN1250_ETHN3250_Cap0p05625_C3750_15000_391d", "delta_net_pp": 0.7663115280573285, "delta_sharpe": -0.04449357190750325, "delta_DD_pp": 0.1826533287500931, "delta_Calmar": -0.277052469242939}, {"scope": "parent", "from": "parent_independentEntry_BTCN1000_ETHN3750_Cap0p05625_C3750_15000_391d", "to": "parent_fixedGross5000_BTCN1250_ETHN3750_Cap0p05625_C3750_15000_391d", "delta_net_pp": 0.7663115280573276, "delta_sharpe": -0.02680288200403691, "delta_DD_pp": 0.04824054494538821, "delta_Calmar": 0.32716241367639753}, {"scope": "parent", "from": "parent_independentEntry_BTCN1250_ETHN3250_Cap0p05625_C3750_15000_391d", "to": "parent_independentEntry_BTCN1500_ETHN3250_Cap0p05625_C3750_15000_391d", "delta_net_pp": 0.7513297919299546, "delta_sharpe": -0.03794644374984735, "delta_DD_pp": 0.21214499737931547, "delta_Calmar": -0.3231788877870194}, {"scope": "parent", "from": "parent_fixedGross5000_BTCN1250_ETHN3750_Cap0p05625_C3750_15000_391d", "to": "parent_independentEntry_BTCN1500_ETHN3750_Cap0p05625_C3750_15000_391d", "delta_net_pp": 0.7513297919299795, "delta_sharpe": -0.02655978040966067, "delta_DD_pp": 0.20304325587561234, "delta_Calmar": -0.3446240191938905}, {"scope": "parent", "from": "parent_independentEntry_BTCN1500_ETHN3250_Cap0p05625_C3750_15000_391d", "to": "parent_independentEntry_BTCN1500_ETHN3750_Cap0p05625_C3750_15000_391d", "delta_net_pp": 0.6294250947818121, "delta_sharpe": 0.03381986415606297, "delta_DD_pp": -0.002260656633590319, "delta_Calmar": 0.3882452643242358}]
收益最优若在金额网格边缘，仅作敞口诊断；不根据结果扩网格或替换代表。小网格不证明全域稳健。
独立核验只读源银行36条完整曲线、14076个原政策决策、42228条资金费、原成交/费用/小时风险，并核验新组合36条连续NAV、逐折和全部门槛；新增native策略决策/执行次数为0。父组合相对旧中心的货币现金流桥接见sizing_effect_decomposition.json。

本轮四账户各续接120个闭合分钟，日决策{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}；实际资金费记录{'SMA': 0, 'candidate': 0, 'l4h02': 6, 'fewm': 6}。L4/FEWM各自在08:00:00.002按原持仓计入资金费，现金变化逐笔核对，持仓/desired/入场价/累计执行费用保持；candidate本次截止06:30，08资金费尚未入账，ETH继续为0。完整71日SPOT权威及原70精确前缀只读，分钟包不是日线权威。首08来源UTC保持2026-11-19T20:40:54.314631Z，实际fundingTime1795075200002不替换为名义整点。下一SMA/candidate['2026-11-19T06:30:00Z', '2026-11-19T08:30:00Z']，candidate须复用该首来源并重新查询后按自己数量记账；下一L4/FEWM['2026-11-19T08:10:00Z', '2026-11-19T10:10:00Z']不得重复08。所有账户下一日决策Nov20_00:01，不重置本金、不强制平仓、不采用新研究配置。

原SMA三倍成本累计-7.468958%；原账户为延迟shadow，180日/六折资格未成熟。十策略仅只读汇总，未改冻结规则/本金/持仓或产生新成交。
保存18份唯一公共GET回执，本轮18、旧复用0、已保存运输失败0；旧首资金费来源UTC/SHA保留，完整71日SPOT权威只读。其他实际失败事实：[{"command": ["/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python", "-B", "/home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T203631Z/prepare.py"], "cwd": "/home/desktop/Documents/Codex/EquiTide", "started_utc": "2026-11-19T20:40:46.289283Z", "finished_utc": "2026-11-19T20:40:54.323745Z", "exit_code": 1, "log": "research/experiments/20261119T203631Z/prepare.log", "stderr": "Traceback (most recent call last):\n  File \"/home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T203631Z/prepare.py\", line 42, in <module>\n    assert all(len(v)==1 for v in actual08.values()),actual08\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nAssertionError: {'BTC': [], 'ETH': []}\n", "resolved": true, "reason": "Exact returned fundingTime1795075200002 retained instead of nominal08:00:00.000;prepare_retry1 completed0 from first saved successful HTTP responses without newHTTP;no reserve or financial/account calculation had occurred.", "failed_source": "research/experiments/20261119T203631Z/pre_exact_funding_ms_fix/prepare.py", "failed_source_sha256": "1de0ad867df39564ef661ef39fceb892e0a21408219b24da0b6ef73c09c328b0", "successful_recovery_receipt": "research/experiments/20261119T203631Z/prepare_retry1_commands.json", "native_recovery_completion": {"session_id": 53202, "exit_code": 0, "chunk_id": "9b6c89"}}, {"type": "native_coordinator_termination_after_saved_financial_children", "recorded_utc": "2026-11-19T20:49:46.373842+00:00", "native_session_id": 33243, "native_exit_code": 143, "native_completion_chunk": "6f9a4f", "cause": "Unknown;do not infer a cause from exit143", "underlying_research_check_native_receipt": "research/experiments/20261119T203631Z/research_check_commands.json", "underlying_native_check": {"command": ["/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python", "-B", "/home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T203631Z/checks.py", "research"], "cwd": "/home/desktop/Documents/Codex/EquiTide", "started_utc": "2026-11-19T20:46:02.957688Z", "finished_utc": "2026-11-19T20:47:17.108308Z", "exit_code": 0, "log": "research/experiments/20261119T203631Z/research_check.log", "stderr": ""}, "financial_report_sha256": "1ccaa9cd7771a7842879a9172fb7cc4095e662a1396412b6c6b7e24344d3a83b", "all_financial_evaluation_finish_and_research_check_receipts_exit_zero": true, "models_evaluated_once": true, "resolved": true, "resolution": "Preserve coordinator143;accept only actual saved child0 receipt/report after readonly verification. Original wrapper is not claimed successful;no model/window rerun."}]
监控生成成功=True，11200研究配置，11188旧行完整字典不变。

实际完成阶段命令（完成目录不得重跑市场/账户，仅保留核验和数据哈希）：

```sh
cd /home/desktop/Documents/Codex/EquiTide
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T203631Z/commands.py prepare # 首次准备在精确毫秒检查处停止；retry复用原成功响应，未重算账户或模型
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T203631Z/commands.py prepare_retry1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T203631Z/commands.py freeze
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T203631Z/commands.py units
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T203631Z/commands.py bind
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T203631Z/commands.py reserve_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T203631Z/commands.py reserve_1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T203631Z/commands.py evaluate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T203631Z/commands.py audit
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T203631Z/commands.py exports
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T203631Z/commands.py finish_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T203631Z/commands.py finish_1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T203631Z/checks.py research
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T203631Z/commands.py l4h02
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T203631Z/commands.py fewm
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T203631Z/commands.py candidate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T203631Z/commands.py forward
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T203631Z/commands.py accounts_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T203631Z/commands.py journal
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T203631Z/commands.py sources_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T203631Z/commands.py gates
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T203631Z/commands.py feed
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T203631Z/commands.py collect
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T203631Z/commands.py final_checks
```

字段格式与版本见primary_source_access.json的[Binance官方REST文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)及[公共数据README](https://github.com/binance/binance-public-data/blob/master/README.md)。所有负收益、失败、来源和冻结规则均保留；成本系数是研究假设。

控制台摘要更正：collect.log末行资金费分配为旧零值标签；逐笔账本、account_window_verification与本轮交接状态均为SMA0、candidate0、L4 6、FEWM6。原日志保留，详见collector_stdout_erratum.json。
