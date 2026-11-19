# 20261119T163557Z 复用真实银行净值的BTC/ETH独立目标组合

事前固定BTC目标750/1250/1750与ETH目标3250/3750/4250完整3×3网格，ETH V6波动上限固定0.05625。旧5000总目标的3个策略组合和3个持有组合只读；6个真正新策略交叉组合、6个匹配持有基准全部先reserve后计算一次并finish。新组合通过历史门槛6/6、持有基准淘汰6/6，负收益不删除。事前代表1250/3250不随结果改变。严格同时改善收益、整体回撤、Sharpe、Calmar为0/6；没有独立未来或稳定实盘盈利资格。

完整读取38796条事件、19259个ID、476份既往结论及29份附加材料。初始16项真实回测缺口0。规范研究定义11605→11617，正式有结果11404；定义数、相关路径数均不是独立试验次数，没有DSR/PBO显著性证明。

经济含义：BTC本金3750、ETH本金15000、总18750和原始银行权重[1,1]保持；20/80是初始本金占比，不自动归一化，不转移资金。两轴是独立的原银行入场目标金额，目标总额4000–6000随格点变化，不再固定5000，更不固定实际动态敞口。较高收益可能只是目标金额/风险增加；同初始目标持有基准也不匹配动态风险。

底层12个已完成银行（6个策略、6个持有）全部只读复用：从原状态片段与原价格还原完整NAV后核对原全路径哈希，再在共同事件轴逐点相加美元净值；不缩放收益、平均Sharpe、不重跑策略或产生新底层订单。父组合无订单、再平衡、抵押转移或跨保证金净额。原ETH组件的一致性淘汰状态保留。

完整规则：All underlying BTC L29/H.03/E.005/V10cap.0275/strictdirection*ROC5>.0025 and ETHlongonly L5/H.02/E.0075/finiteEWMS16beta15/17/D3K.0075/V6cap.05625/M4R.0075VW9 native rules,quantities,funding,costs and margin are exactly the saved completed source banks. No source strategy or order is recomputed. New candidates only change which independently funded existingBTC/ETH banks are jointly held.

按时间验证：391日反复开发历史，2025-10-19 00:01→2026-11-14 00:01，33个闭合上下文日；固定规则无拟合、训练或标签，purge不适用、标签embargo为0。13个完整30日折+1日尾段，近40日8×5日、扩展21日5/5/5/6；跨折继承实际源银行现金/q，原终点计费平仓，整体回撤由连续完整NAV计算。不能称未触碰最终留出。

成本1/2/3倍沿用源银行实际数量核算：每边手续费5bp、半价差1bp、滑点2bp、0.5×过去20日样本对数波动×sqrt(实际订单额/过去20日quoteADV)，不利tick/LOT/最低金额/参与率≤0.001；完全抵押1倍入场与小时不利价1%维持保证金代理。真实永续资金费支出随倍数增加、收入不放大；线性永续无现货借币。原费用/资金费逐项相加并独立复核；父组合没有新成交成本。估计费用缺真实L2/TCA、完整阶梯、tick清算与容量实证。

|BTC/ETH目标USDT|初始总目标|类型|状态|净收益1x/2x/3x %|整体DD3 %|Sharpe3|Calmar3|正30日折1x|近40日正5日折1/2/3|
|---|---|---|---|---|---|---|---|---|---|
|750/3250|4000|benchmark|rejected|-10.642307 / -11.284708 / -11.927157|14.955582|-1.378294|-0.747560|6/13|1/1/1（各/8）|
|750/3750|4500|benchmark|rejected|-12.031462 / -12.749766 / -13.468175|16.856920|-1.368194|-0.749354|6/13|1/1/1（各/8）|
|1250/3250|4500|benchmark|rejected|-11.539103 / -12.265320 / -12.991585|16.237791|-1.375981|-0.750267|6/13|1/1/1（各/8）|
|1250/4250|5500|benchmark|rejected|-14.328267 / -15.206998 / -16.085616|20.031583|-1.355295|-0.753875|6/13|1/1/1（各/8）|
|1750/3750|5500|benchmark|rejected|-14.049258 / -14.956150 / -15.863150|19.728531|-1.360220|-0.754806|6/13|1/1/1（各/8）|
|1750/4250|6000|benchmark|rejected|-15.449266 / -16.432770 / -17.416162|21.617715|-1.349757|-0.756723|6/13|1/1/1（各/8）|
|750/3250|4000|candidate|passed|7.159366 / 6.739394 / 6.319393|1.098737|2.325601|5.358016|12/13|6/6/6（各/8）|
|750/3750|4500|candidate|passed|7.864395 / 7.406446 / 6.948818|1.246927|2.309044|5.190455|12/13|6/6/6（各/8）|
|1250/3250|4500|candidate|passed|9.129041 / 8.573425 / 8.017760|1.325699|2.294969|5.631145|12/13|6/6/6（各/8）|
|1250/4250|5500|candidate|passed|10.540124 / 9.908771 / 9.277531|1.458069|2.328409|5.922035|12/13|6/6/6（各/8）|
|1750/3750|5500|candidate|passed|11.677636 / 10.959070 / 10.240836|1.821639|2.250244|5.230695|11/13|6/6/6（各/8）|
|1750/4250|6000|candidate|passed|12.383692 / 11.627364 / 10.871182|1.818972|2.281302|5.559708|12/13|6/6/6（各/8）|

预设失败判据：全期/近期各成本正、1x≥10/13正月、近40日各成本≥6/8正5日折、扩展各成本≥3/4正折、DD3≤25%、邻域正收益与近期合格比例≥60%、至少4次底层平仓、1x(毛价差收益+资金费)/费用≥2.5，无拒单/负抵押/保证金代理违规、原终点flat。持有基准无可调alpha参数，不强行构造邻域。

parent_independentEntry_matched_hold_BTCN750_ETHN3250_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_independentEntry_matched_hold_BTCN750_ETHN3750_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_independentEntry_matched_hold_BTCN1250_ETHN3250_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_independentEntry_matched_hold_BTCN1250_ETHN4250_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_independentEntry_matched_hold_BTCN1750_ETHN3750_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_independentEntry_matched_hold_BTCN1750_ETHN4250_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_independentEntry_BTCN750_ETHN3250_Cap0p05625_C3750_15000_391d：通过预设历史门槛，待独立未来验证。
parent_independentEntry_BTCN750_ETHN3750_Cap0p05625_C3750_15000_391d：通过预设历史门槛，待独立未来验证。
parent_independentEntry_BTCN1250_ETHN3250_Cap0p05625_C3750_15000_391d：通过预设历史门槛，待独立未来验证。
parent_independentEntry_BTCN1250_ETHN4250_Cap0p05625_C3750_15000_391d：通过预设历史门槛，待独立未来验证。
parent_independentEntry_BTCN1750_ETHN3750_Cap0p05625_C3750_15000_391d：通过预设历史门槛，待独立未来验证。
parent_independentEntry_BTCN1750_ETHN4250_Cap0p05625_C3750_15000_391d：通过预设历史门槛，待独立未来验证。

相对旧1250/3750中心的三倍成本变化：
BTC/ETH=750/3250，目标总额4000：收益-2.327792个百分点，整体DD-0.233803个百分点，Sharpe0.008198，Calmar-0.682819；敞口不同，不解释为独立alpha提升。
BTC/ETH=750/3750，目标总额4500：收益-1.698367个百分点，整体DD-0.085613个百分点，Sharpe-0.008359，Calmar-0.850380；敞口不同，不解释为独立alpha提升。
BTC/ETH=1250/3250，目标总额4500：收益-0.629425个百分点，整体DD-0.006841个百分点，Sharpe-0.022433，Calmar-0.409690；敞口不同，不解释为独立alpha提升。
BTC/ETH=1250/4250，目标总额5500：收益0.630346个百分点，整体DD0.125529个百分点，Sharpe0.011006，Calmar-0.118800；敞口不同，不解释为独立alpha提升。
BTC/ETH=1750/3750，目标总额5500：收益1.593651个百分点，整体DD0.489099个百分点，Sharpe-0.067158，Calmar-0.810141；敞口不同，不解释为独立alpha提升。
BTC/ETH=1750/4250，目标总额6000：收益2.223997个百分点，整体DD0.486432个百分点，Sharpe-0.036101，Calmar-0.481127；敞口不同，不解释为独立alpha提升。

敏感性全部保存：90个成本场景、1260逐折、720近期折、360扩展折、35280日NAV行、27个匹配持有对比及12条相邻边；新12配置有12条不同完整成本路径。启发式跳变边=[{"scope": "parent", "from": "parent_independentEntry_BTCN1250_ETHN3250_Cap0p05625_C3750_15000_391d", "to": "parent_fixedGross5000_BTCN1750_ETHN3250_Cap0p05625_C3750_15000_391d", "delta_net_pp": 1.5936512757559242, "delta_sharpe": -0.08698777469445318, "delta_DD_pp": 0.49861481470521163, "delta_Calmar": -0.7281778750343726}, {"scope": "parent", "from": "parent_fixedGross5000_BTCN1250_ETHN3750_Cap0p05625_C3750_15000_391d", "to": "parent_independentEntry_BTCN1750_ETHN3750_Cap0p05625_C3750_15000_391d", "delta_net_pp": 1.5936512757559491, "delta_sharpe": -0.06715829968097076, "delta_DD_pp": 0.48909851375714686, "delta_Calmar": -0.8101406736993582}, {"scope": "parent", "from": "parent_independentEntry_BTCN1250_ETHN4250_Cap0p05625_C3750_15000_391d", "to": "parent_independentEntry_BTCN1750_ETHN4250_Cap0p05625_C3750_15000_391d", "delta_net_pp": 1.593651275755903, "delta_sharpe": -0.04710723764938729, "delta_DD_pp": 0.36090272944443447, "delta_Calmar": -0.3623274464045245}]
收益最优若在金额网格边缘，仅作敞口诊断；不根据结果扩网格或替换代表。小网格不证明全域稳健。
独立核验只读源银行36条完整曲线、14076个原政策决策、42228条资金费、原成交/费用/小时风险，并核验新组合36条连续NAV、逐折和全部门槛；新增native策略决策/执行次数为0。父组合相对旧中心的货币现金流桥接见sizing_effect_decomposition.json。

本轮四账户在Nov20_00:01之前按各自冻结计划仅续接120个闭合分钟。实际日决策{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、资金费{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}，原现金/持仓/desired/累计费用保持；candidate的ETH在上轮Nov19原日规则已平仓，本轮继续为0，BTC保留原空头。完整71日SPOT权威及原70精确前缀只读复用，当前分钟包不是日线权威；首Nov19_00的UTC保持2026-11-19T12:46:38.135135Z，所有旧首来源字节不变。三永续实际00及四账户Nov19日决策均恰好一次，不重复记账。下一SMA/candidate['2026-11-19T02:30:00Z', '2026-11-19T04:30:00Z']、L4/FEWM['2026-11-19T04:10:00Z', '2026-11-19T06:10:00Z']均mark-only并查询实际特殊资金费，不预记名义时刻或未来日决策，不重置本金、不强制平仓、不采用新研究配置。

原SMA三倍成本累计-7.468958%；原账户为延迟shadow，180日/六折资格未成熟。十策略仅只读汇总，未改冻结规则/本金/持仓或产生新成交。
保存19份唯一公共GET回执，本轮19、旧复用0、已保存运输失败1；旧首资金费来源UTC/SHA保留，完整71日SPOT权威只读。其他实际失败事实：[{"type": "private_builder_quote_syntax", "native_exit_code": 1, "native_chunk_id": "6ffad9", "resolved": true, "failed_source": "research/experiments/20261119T163557Z/pre_builder_quote_fix/build.py.txt", "failed_source_sha256": "00b52f7faa887b2c9f738c4b104dcbb89c0814d3b0f6f808f9d1f4cc52478355", "reason": "Private builder string quote fixed before any new code was applied, reservation, financial or account evaluation."}, {"command": ["/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python", "-B", "/home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T163557Z/parent_units.py"], "cwd": "/home/desktop/Documents/Codex/EquiTide", "started_utc": "2026-11-19T16:43:35.472759Z", "finished_utc": "2026-11-19T16:43:35.763541Z", "exit_code": 1, "log": "research/experiments/20261119T163557Z/parent_units.log", "stderr": "Traceback (most recent call last):\n  File \"/home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T163557Z/parent_units.py\", line 23, in <module>\n    ns,dims=neighbors(g,p,full);assert dims==2 and len(ns)==(6 if g['W']==middle else 4)\n                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nAssertionError\n", "resolved": true, "failure_type": "legacy_3x2_neighbor_test_assumption", "failed_source": "research/experiments/20261119T163557Z/pre_neighbor_geometry_fix/parent_units.py", "failed_source_sha256": "718d1bf74b53185722fc150011206637f2f1aad14f5fdf71556e29883d4747ad", "resolution": "Both actual units_retry1 native jobs exited0 with rectangular4/6/9 neighbors and aligned-dollarNAV/misaligned-axis tests;fixed before any reservation/market result."}, {"url": "https://fapi.binance.com/fapi/v1/markPriceKlines?symbol=ETHUSDT&interval=1h&startTime=1795050000000&endTime=1795057200000&limit=1500", "started_utc": "2026-11-19T16:56:04.819572+00:00", "http_status": 0, "curl_exit_code": 35, "raw": "data/raw/binance/l4h02_forward/20261119T163557Z/http_0006.gz", "sha256": "f61f27bd17de546264aa58f40f3aafaac7021e0ef69c17f6b1b4cd7664a037ec", "bytes": 0, "stderr": "curl: (35) TLS connect error: error:0A000126:SSL routines::unexpected eof while reading\n", "transport": "verifiedTLSmin1.2HTTP1.1 publicGET,bounded3attempts", "resolved": true, "resolution": "Same exact URL has validated successful saved public bytes; original capture time retained, including earlier source reuse documented before first reserve. Successful original account packet and audit retained."}]
监控生成成功=True，11176研究配置，11164旧行完整字典不变。

实际完成阶段命令（完成目录不得重跑市场/账户，仅保留核验和数据哈希）：

```sh
cd /home/desktop/Documents/Codex/EquiTide
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T163557Z/commands.py prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T163557Z/commands.py freeze
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T163557Z/commands.py units # 旧3x2测试断言失败，后续retry1通过；失败源码/回执保留
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T163557Z/commands.py units_retry1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T163557Z/commands.py bind
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T163557Z/commands.py reserve_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T163557Z/commands.py reserve_1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T163557Z/commands.py evaluate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T163557Z/commands.py audit
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T163557Z/commands.py exports
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T163557Z/commands.py finish_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T163557Z/commands.py finish_1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T163557Z/commands.py research_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T163557Z/commands.py l4h02
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T163557Z/commands.py fewm
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T163557Z/commands.py candidate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T163557Z/commands.py forward
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T163557Z/commands.py accounts_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T163557Z/commands.py journal
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T163557Z/commands.py sources_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T163557Z/commands.py gates
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T163557Z/commands.py feed
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T163557Z/commands.py collect
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T163557Z/commands.py final_checks
```

字段格式与版本见primary_source_access.json的[Binance官方REST文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)及[公共数据README](https://github.com/binance/binance-public-data/blob/master/README.md)。所有负收益、失败、来源和冻结规则均保留；成本系数是研究假设。
