# 20261119T183629Z 复用真实银行净值的BTC/ETH独立目标组合

事前固定BTC目标1125/1250/1375与ETH目标3625/3750/3875完整3×3网格，ETH V6波动上限固定0.05625。旧5000总目标的3个策略组合和3个持有组合只读；6个真正新策略交叉组合、6个匹配持有基准全部先reserve后计算一次并finish。新组合通过历史门槛6/6、持有基准淘汰6/6，负收益不删除。事前代表1250/3625不随结果改变。严格同时改善收益、整体回撤、Sharpe、Calmar为0/6；没有独立未来或稳定实盘盈利资格。

完整读取38864条事件、19293个ID、477份既往结论及29份附加材料。初始16项真实回测缺口0。规范研究定义11617→11629，正式有结果11416；定义数、相关路径数均不是独立试验次数，没有DSR/PBO显著性证明。

经济含义：BTC本金3750、ETH本金15000、总18750和原始银行权重[1,1]保持；20/80是初始本金占比，不自动归一化，不转移资金。两轴是独立的原银行入场目标金额，目标总额4750–5250随格点变化，不再固定5000，更不固定实际动态敞口。较高收益可能只是目标金额/风险增加；同初始目标持有基准也不匹配动态风险。

底层12个已完成银行（6个策略、6个持有）全部只读复用：从原状态片段与原价格还原完整NAV后核对原全路径哈希，再在共同事件轴逐点相加美元净值；不缩放收益、平均Sharpe、不重跑策略或产生新底层订单。父组合无订单、再平衡、抵押转移或跨保证金净额。原ETH组件的一致性淘汰状态保留。

完整规则：All underlying BTC L29/H.03/E.005/V10cap.0275/strictdirection*ROC5>.0025 and ETHlongonly L5/H.02/E.0075/finiteEWMS16beta15/17/D3K.0075/V6cap.05625/M4R.0075VW9 native rules,quantities,funding,costs and margin are exactly the saved completed source banks. No source strategy or order is recomputed. New candidates only change which independently funded existingBTC/ETH banks are jointly held.

按时间验证：391日反复开发历史，2025-10-19 00:01→2026-11-14 00:01，33个闭合上下文日；固定规则无拟合、训练或标签，purge不适用、标签embargo为0。13个完整30日折+1日尾段，近40日8×5日、扩展21日5/5/5/6；跨折继承实际源银行现金/q，原终点计费平仓，整体回撤由连续完整NAV计算。不能称未触碰最终留出。

成本1/2/3倍沿用源银行实际数量核算：每边手续费5bp、半价差1bp、滑点2bp、0.5×过去20日样本对数波动×sqrt(实际订单额/过去20日quoteADV)，不利tick/LOT/最低金额/参与率≤0.001；完全抵押1倍入场与小时不利价1%维持保证金代理。真实永续资金费支出随倍数增加、收入不放大；线性永续无现货借币。原费用/资金费逐项相加并独立复核；父组合没有新成交成本。估计费用缺真实L2/TCA、完整阶梯、tick清算与容量实证。

|BTC/ETH目标USDT|初始总目标|类型|状态|净收益1x/2x/3x %|整体DD3 %|Sharpe3|Calmar3|正30日折1x|近40日正5日折1/2/3|
|---|---|---|---|---|---|---|---|---|---|
|1125/3625|4750|benchmark|rejected|-12.356772 / -13.118962 / -13.881201|17.338888|-1.369103|-0.750979|6/13|1/1/1（各/8）|
|1125/3750|4875|benchmark|rejected|-12.704061 / -13.485227 / -14.266494|17.812282|-1.366541|-0.751418|6/13|1/1/1（各/8）|
|1250/3625|4875|benchmark|rejected|-12.580970 / -13.364113 / -14.147310|17.657192|-1.368304|-0.751652|6/13|1/1/1（各/8）|
|1250/3875|5125|benchmark|rejected|-13.275548 / -14.096695 / -14.917847|18.602680|-1.363157|-0.752521|6/13|1/1/1（各/8）|
|1375/3750|5125|benchmark|rejected|-13.152457 / -13.975529 / -14.798708|18.449079|-1.364821|-0.752693|6/13|1/1/1（各/8）|
|1375/3875|5250|benchmark|rejected|-13.499746 / -14.341846 / -15.183951|18.920053|-1.362239|-0.753171|6/13|1/1/1（各/8）|
|1125/3625|4750|candidate|passed|9.228919 / 8.681021 / 8.133104|1.256190|2.340185|6.028010|12/13|6/6/6（各/8）|
|1125/3750|4875|candidate|passed|9.404759 / 8.847338 / 8.290238|1.292184|2.342478|5.973018|12/13|6/6/6（各/8）|
|1250/3625|4875|candidate|passed|9.658229 / 9.074159 / 8.490051|1.324234|2.312996|5.968561|12/13|6/6/6（各/8）|
|1250/3875|5125|candidate|passed|10.010128 / 9.407158 / 8.804500|1.362729|2.321137|6.014180|12/13|6/6/6（各/8）|
|1375/3750|5125|candidate|passed|10.270837 / 9.648970 / 9.027443|1.425866|2.301015|5.893004|12/13|6/6/6（各/8）|
|1375/3875|5250|candidate|passed|10.446896 / 9.815652 / 9.184759|1.425341|2.306410|5.997610|12/13|6/6/6（各/8）|

预设失败判据：全期/近期各成本正、1x≥10/13正月、近40日各成本≥6/8正5日折、扩展各成本≥3/4正折、DD3≤25%、邻域正收益与近期合格比例≥60%、至少4次底层平仓、1x(毛价差收益+资金费)/费用≥2.5，无拒单/负抵押/保证金代理违规、原终点flat。持有基准无可调alpha参数，不强行构造邻域。

parent_independentEntry_matched_hold_BTCN1125_ETHN3625_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_independentEntry_matched_hold_BTCN1125_ETHN3750_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_independentEntry_matched_hold_BTCN1250_ETHN3625_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_independentEntry_matched_hold_BTCN1250_ETHN3875_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_independentEntry_matched_hold_BTCN1375_ETHN3750_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_independentEntry_matched_hold_BTCN1375_ETHN3875_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_independentEntry_BTCN1125_ETHN3625_Cap0p05625_C3750_15000_391d：通过预设历史门槛，待独立未来验证。
parent_independentEntry_BTCN1125_ETHN3750_Cap0p05625_C3750_15000_391d：通过预设历史门槛，待独立未来验证。
parent_independentEntry_BTCN1250_ETHN3625_Cap0p05625_C3750_15000_391d：通过预设历史门槛，待独立未来验证。
parent_independentEntry_BTCN1250_ETHN3875_Cap0p05625_C3750_15000_391d：通过预设历史门槛，待独立未来验证。
parent_independentEntry_BTCN1375_ETHN3750_Cap0p05625_C3750_15000_391d：通过预设历史门槛，待独立未来验证。
parent_independentEntry_BTCN1375_ETHN3875_Cap0p05625_C3750_15000_391d：通过预设历史门槛，待独立未来验证。

相对旧1250/3750中心的三倍成本变化：
BTC/ETH=1125/3625，目标总额4750：收益-0.514081个百分点，整体DD-0.076350个百分点，Sharpe0.022782，Calmar-0.012826；敞口不同，不解释为独立alpha提升。
BTC/ETH=1125/3750，目标总额4875：收益-0.356947个百分点，整体DD-0.040356个百分点，Sharpe0.025076，Calmar-0.067817；敞口不同，不解释为独立alpha提升。
BTC/ETH=1250/3625，目标总额4875：收益-0.157133个百分点，整体DD-0.008306个百分点，Sharpe-0.004406，Calmar-0.072274；敞口不同，不解释为独立alpha提升。
BTC/ETH=1250/3875，目标总额5125：收益0.157316个百分点，整体DD0.030188个百分点，Sharpe0.003735，Calmar-0.026655；敞口不同，不解释为独立alpha提升。
BTC/ETH=1375/3750，目标总额5125：收益0.380258个百分点，整体DD0.093326个百分点，Sharpe-0.016388，Calmar-0.147831；敞口不同，不解释为独立alpha提升。
BTC/ETH=1375/3875，目标总额5250：收益0.537574个百分点，整体DD0.092801个百分点，Sharpe-0.010992，Calmar-0.043225；敞口不同，不解释为独立alpha提升。

敏感性全部保存：90个成本场景、1260逐折、720近期折、360扩展折、35280日NAV行、27个匹配持有对比及12条相邻边；新12配置有12条不同完整成本路径。启发式跳变边=[{"scope": "parent", "from": "parent_independentEntry_BTCN1125_ETHN3625_Cap0p05625_C3750_15000_391d", "to": "parent_independentEntry_BTCN1250_ETHN3625_Cap0p05625_C3750_15000_391d", "delta_net_pp": 0.3569471506753352, "delta_sharpe": -0.027188141849871172, "delta_DD_pp": 0.06804419542406626, "delta_Calmar": -0.05944864527742233}, {"scope": "parent", "from": "parent_independentEntry_BTCN1125_ETHN3750_Cap0p05625_C3750_15000_391d", "to": "parent_fixedGross5000_BTCN1250_ETHN3750_Cap0p05625_C3750_15000_391d", "delta_net_pp": 0.35694715067531213, "delta_sharpe": -0.025075807216704327, "delta_DD_pp": 0.040355894114763036, "delta_Calmar": 0.06781687150481996}, {"scope": "parent", "from": "parent_fixedGross5000_BTCN1125_ETHN3875_Cap0p05625_C3750_15000_391d", "to": "parent_independentEntry_BTCN1250_ETHN3875_Cap0p05625_C3750_15000_391d", "delta_net_pp": 0.35694715067535654, "delta_sharpe": -0.023022523987931365, "delta_DD_pp": 0.03415015288782408, "delta_Calmar": 0.09483676840216937}]
收益最优若在金额网格边缘，仅作敞口诊断；不根据结果扩网格或替换代表。小网格不证明全域稳健。
独立核验只读源银行36条完整曲线、14076个原政策决策、42228条资金费、原成交/费用/小时风险，并核验新组合36条连续NAV、逐折和全部门槛；新增native策略决策/执行次数为0。父组合相对旧中心的货币现金流桥接见sizing_effect_decomposition.json。

本轮四账户在Nov20_00:01之前按各自冻结计划仅续接120个闭合分钟。实际日决策{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、资金费{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}，原现金/持仓/desired/累计费用保持；candidate的ETH在既往Nov19原日规则已平仓，本轮继续为0，BTC保留原空头。完整71日SPOT权威及原70精确前缀只读复用，当前分钟包不是日线权威；首Nov19_00的UTC保持2026-11-19T12:46:38.135135Z，所有旧首来源字节不变。三永续实际00及四账户Nov19日决策均恰好一次，不重复记账。下一SMA/candidate['2026-11-19T04:30:00Z', '2026-11-19T06:30:00Z']、L4/FEWM['2026-11-19T06:10:00Z', '2026-11-19T08:10:00Z']均mark-only并查询实际特殊资金费，不预记名义时刻或未来日决策，不重置本金、不强制平仓、不采用新研究配置。

原SMA三倍成本累计-7.468958%；原账户为延迟shadow，180日/六折资格未成熟。十策略仅只读汇总，未改冻结规则/本金/持仓或产生新成交。
保存18份唯一公共GET回执，本轮18、旧复用0、已保存运输失败0；旧首资金费来源UTC/SHA保留，完整71日SPOT权威只读。其他实际失败事实：[{"passed": false, "recorded_utc": "2026-11-19T18:59:21.931471+00:00", "native_launch_chunk": "47501f", "native_session_id": 54305, "native_completion_chunk": "181dc6", "exit_code": 1, "command": ["/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python", "-B", "/home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T183629Z/review_economic_identity.py"], "original_source": "research/experiments/20261119T183629Z/pre_economic_legacy_format_fix/review_economic_identity.py", "original_source_sha256": "e855bf70fc33fe8bba216bbaa9d03ac8a5dec51d37309c39d78e5ff0fdd7b93b", "error": "KeyError: 'result_available' at readonly complete registry comparison:legacy records may omit this optional field", "corrected_source_sha256": "d2e2708dfbf0b11afc995d524e9fac71b3828b6e60b0b15ed07a5acdf918c308", "financial_and_account_calculations": 0, "resolved": true, "stderr": "Traceback (most recent call last):\n  File \"/home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T183629Z/review_economic_identity.py\", line 16, in <module>\n    matches=[fp for fp,item in rs.items() if fp not in own and (item['result_available'] or item['status']=='reserved') and signature(item.get('spec',{}))==signature(sp)]\n                                                                ~~~~^^^^^^^^^^^^^^^^^^^^\nKeyError: 'result_available'\n", "resolution": "Legacy optional field read uses get(False);new12graphs and18saved source results fully rechecked;no financial/account rerun", "corrected_native_completion": {"session_id": 81814, "exit_code": 0, "chunk_id": "fc62b0"}, "successful_verification": "economic_configuration_identity_verification.json"}]
监控生成成功=True，11188研究配置，11176旧行完整字典不变。

实际完成阶段命令（完成目录不得重跑市场/账户，仅保留核验和数据哈希）：

```sh
cd /home/desktop/Documents/Codex/EquiTide
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T183629Z/commands.py prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T183629Z/commands.py freeze
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T183629Z/commands.py units # 旧3x2测试断言失败，后续retry1通过；失败源码/回执保留
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T183629Z/commands.py bind
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T183629Z/commands.py reserve_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T183629Z/commands.py reserve_1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T183629Z/commands.py evaluate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T183629Z/commands.py audit
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T183629Z/commands.py exports
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T183629Z/commands.py finish_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T183629Z/commands.py finish_1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T183629Z/commands.py research_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T183629Z/commands.py l4h02
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T183629Z/commands.py fewm
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T183629Z/commands.py candidate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T183629Z/commands.py forward
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T183629Z/commands.py accounts_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T183629Z/commands.py journal
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T183629Z/commands.py sources_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T183629Z/commands.py gates
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T183629Z/commands.py feed
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T183629Z/commands.py collect
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T183629Z/commands.py final_checks
```

字段格式与版本见primary_source_access.json的[Binance官方REST文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)及[公共数据README](https://github.com/binance/binance-public-data/blob/master/README.md)。所有负收益、失败、来源和冻结规则均保留；成本系数是研究假设。
