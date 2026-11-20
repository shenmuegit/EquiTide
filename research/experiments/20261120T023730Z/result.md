# 20261120T023730Z 复用真实银行净值的BTC/ETH独立目标组合

事前固定BTC目标750/1000/1500与ETH目标3625/3750/3875完整3×3网格，ETH V6波动上限固定0.05625。旧ETH3750金额的3个策略组合和3个持有组合只读；6个真正新策略交叉组合、6个匹配持有基准全部先reserve后计算一次并finish。新组合通过历史门槛6/6、持有基准淘汰6/6，负收益不删除。事前代表1000/3625不随结果改变。严格同时改善收益、整体回撤、Sharpe、Calmar为0/6；没有独立未来或稳定实盘盈利资格。

完整读取39068条事件、19395个ID、481份既往结论及32份附加材料。初始16项真实回测缺口0。规范研究定义11653→11665，正式有结果11452；定义数、相关路径数均不是独立试验次数，没有DSR/PBO显著性证明。

经济含义：BTC本金3750、ETH本金15000、总18750和原始银行权重[1,1]保持；20/80是初始本金占比，不自动归一化，不转移资金。两轴是独立的原银行入场目标金额，目标总额4375–5375随格点变化，不再固定5000，更不固定实际动态敞口。较高收益可能只是目标金额/风险增加；同初始目标持有基准也不匹配动态风险。

底层12个已完成银行（6个策略、6个持有）全部只读复用：从原状态片段与原价格还原完整NAV后核对原全路径哈希，再在共同事件轴逐点相加美元净值；不缩放收益、平均Sharpe、不重跑策略或产生新底层订单。父组合无订单、再平衡、抵押转移或跨保证金净额。原ETH组件的一致性淘汰状态保留。

完整规则：All underlying BTC L29/H.03/E.005/V10cap.0275/strictdirection*ROC5>.0025 and ETHlongonly L5/H.02/E.0075/finiteEWMS16beta15/17/D3K.0075/V6cap.05625/M4R.0075VW9 native rules,quantities,funding,costs and margin are exactly the saved completed source banks. No source strategy or order is recomputed. New candidates only change which independently funded existingBTC/ETH banks are jointly held.

按时间验证：391日反复开发历史，2025-10-19 00:01→2026-11-14 00:01，33个闭合上下文日；固定规则无拟合、训练或标签，purge不适用、标签embargo为0。13个完整30日折+1日尾段，近40日8×5日、扩展21日5/5/5/6；跨折继承实际源银行现金/q，原终点计费平仓，整体回撤由连续完整NAV计算。不能称未触碰最终留出。

成本1/2/3倍沿用源银行实际数量核算：每边手续费5bp、半价差1bp、滑点2bp、0.5×过去20日样本对数波动×sqrt(实际订单额/过去20日quoteADV)，不利tick/LOT/最低金额/参与率≤0.001；完全抵押1倍入场与小时不利价1%维持保证金代理。真实永续资金费支出随倍数增加、收入不放大；线性永续无现货借币。原费用/资金费逐项相加并独立复核；父组合没有新成交成本。估计费用缺真实L2/TCA、完整阶梯、tick清算与容量实证。

|BTC/ETH目标USDT|初始总目标|类型|状态|净收益1x/2x/3x %|整体DD3 %|Sharpe3|Calmar3|正30日折1x|近40日正5日折1/2/3|
|---|---|---|---|---|---|---|---|---|---|
|750/3625|4375|benchmark|rejected|-11.684174 / -12.383501 / -13.082882|16.382391|-1.370714|-0.748895|6/13|1/1/1（各/8）|
|750/3875|4625|benchmark|rejected|-12.378751 / -13.116083 / -13.853419|17.330900|-1.365666|-0.749814|6/13|1/1/1（各/8）|
|1000/3625|4625|benchmark|rejected|-12.132569 / -12.873801 / -13.615092|17.020321|-1.369779|-0.750296|6/13|1/1/1（各/8）|
|1000/3875|4875|benchmark|rejected|-12.827147 / -13.606383 / -14.385629|17.967317|-1.364663|-0.751187|6/13|1/1/1（各/8）|
|1500/3625|5125|benchmark|rejected|-13.253572 / -14.099574 / -14.945638|18.618653|-1.365259|-0.753284|6/13|1/1/1（各/8）|
|1500/3875|5375|benchmark|rejected|-13.948150 / -14.832156 / -15.716174|19.559576|-1.360114|-0.754231|6/13|1/1/1（各/8）|
|750/3625|4375|candidate|passed|7.688554 / 7.240129 / 6.791684|1.210196|2.313599|5.227319|12/13|6/6/6（各/8）|
|750/3875|4625|candidate|passed|8.040453 / 7.573127 / 7.106133|1.283563|2.304323|5.156202|12/13|6/6/6（各/8）|
|1000/3625|4625|candidate|passed|8.760101 / 8.241919 / 7.723740|1.247733|2.344009|5.764147|12/13|6/6/6（各/8）|
|1000/3875|4875|candidate|passed|9.112001 / 8.574918 / 8.038189|1.320773|2.343883|5.666514|12/13|6/6/6（各/8）|
|1500/3625|5125|candidate|passed|10.523398 / 9.882400 / 9.241381|1.536148|2.283607|5.599192|12/13|6/6/6（各/8）|
|1500/3875|5375|candidate|passed|10.875297 / 10.215399 / 9.555830|1.535019|2.297375|5.793401|12/13|6/6/6（各/8）|

预设失败判据：全期/近期各成本正、1x≥10/13正月、近40日各成本≥6/8正5日折、扩展各成本≥3/4正折、DD3≤25%、邻域正收益与近期合格比例≥60%、至少4次底层平仓、1x(毛价差收益+资金费)/费用≥2.5，无拒单/负抵押/保证金代理违规、原终点flat。持有基准无可调alpha参数，不强行构造邻域。

parent_independentEntry_matched_hold_BTCN750_ETHN3625_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_independentEntry_matched_hold_BTCN750_ETHN3875_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_independentEntry_matched_hold_BTCN1000_ETHN3625_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_independentEntry_matched_hold_BTCN1000_ETHN3875_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_independentEntry_matched_hold_BTCN1500_ETHN3625_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_independentEntry_matched_hold_BTCN1500_ETHN3875_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_independentEntry_BTCN750_ETHN3625_Cap0p05625_C3750_15000_391d：通过预设历史门槛，待独立未来验证。
parent_independentEntry_BTCN750_ETHN3875_Cap0p05625_C3750_15000_391d：通过预设历史门槛，待独立未来验证。
parent_independentEntry_BTCN1000_ETHN3625_Cap0p05625_C3750_15000_391d：通过预设历史门槛，待独立未来验证。
parent_independentEntry_BTCN1000_ETHN3875_Cap0p05625_C3750_15000_391d：通过预设历史门槛，待独立未来验证。
parent_independentEntry_BTCN1500_ETHN3625_Cap0p05625_C3750_15000_391d：通过预设历史门槛，待独立未来验证。
parent_independentEntry_BTCN1500_ETHN3875_Cap0p05625_C3750_15000_391d：通过预设历史门槛，待独立未来验证。

相对旧1000/3750中心的三倍成本变化：
BTC/ETH=750/3625，目标总额4375：收益-1.089189个百分点，整体DD-0.074104个百分点，Sharpe-0.030606，Calmar-0.486354；敞口不同，不解释为独立alpha提升。
BTC/ETH=750/3875，目标总额4625：收益-0.774740个百分点，整体DD-0.000736个百分点，Sharpe-0.039883，Calmar-0.557471；敞口不同，不解释为独立alpha提升。
BTC/ETH=1000/3625，目标总额4625：收益-0.157133个百分点，整体DD-0.036567个百分点，Sharpe-0.000196，Calmar0.050474；敞口不同，不解释为独立alpha提升。
BTC/ETH=1000/3875，目标总额4875：收益0.157316个百分点，整体DD0.036473个百分点，Sharpe-0.000322，Calmar-0.047159；敞口不同，不解释为独立alpha提升。
BTC/ETH=1500/3625，目标总额5125：收益1.360508个百分点，整体DD0.251849个百分点，Sharpe-0.060599，Calmar-0.114481；敞口不同，不解释为独立alpha提升。
BTC/ETH=1500/3875，目标总额5375：收益1.674957个百分点，整体DD0.250719个百分点，Sharpe-0.046830，Calmar0.079729；敞口不同，不解释为独立alpha提升。

敏感性全部保存：90个成本场景、1260逐折、720近期折、360扩展折、35280日NAV行、27个匹配持有对比及12条相邻边；新12配置有12条不同完整成本路径。启发式跳变边=[{"scope": "parent", "from": "parent_independentEntry_BTCN1000_ETHN3625_Cap0p05625_C3750_15000_391d", "to": "parent_independentEntry_BTCN1500_ETHN3625_Cap0p05625_C3750_15000_391d", "delta_net_pp": 1.5176413199873062, "delta_sharpe": -0.06040274411839741, "delta_DD_pp": 0.28841578457474704, "delta_Calmar": -0.16495522557517894}, {"scope": "parent", "from": "parent_independentEntry_BTCN1000_ETHN3750_Cap0p05625_C3750_15000_391d", "to": "parent_independentEntry_BTCN1500_ETHN3750_Cap0p05625_C3750_15000_391d", "delta_net_pp": 1.5176413199873071, "delta_sharpe": -0.05336266241369758, "delta_DD_pp": 0.25128380082100055, "delta_Calmar": -0.017461605517492984}, {"scope": "parent", "from": "parent_independentEntry_BTCN1000_ETHN3875_Cap0p05625_C3750_15000_391d", "to": "parent_independentEntry_BTCN1500_ETHN3875_Cap0p05625_C3750_15000_391d", "delta_net_pp": 1.517641319987284, "delta_sharpe": -0.04650804904974315, "delta_DD_pp": 0.21424631219686407, "delta_Calmar": 0.12688725856566574}]
收益最优若在金额网格边缘，仅作敞口诊断；不根据结果扩网格或替换代表。小网格不证明全域稳健。
独立核验只读源银行36条完整曲线、14076个原政策决策、42228条资金费、原成交/费用/小时风险，并核验新组合36条连续NAV、逐折和全部门槛；新增native策略决策/执行次数为0。父组合相对旧中心的货币现金流桥接见sizing_effect_decomposition.json。

本轮四账户各续接120个闭合分钟，日决策{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}；实际资金费记录{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}。本轮各永续只处理当前各自窗口实际新增结算，不重复旧08:00:00.002资金费。各账户现金变化逐笔核对，持仓/desired/入场价/累计执行费用保持。完整71日SPOT权威及原70精确前缀只读，分钟包不是日线权威。首08来源UTC保持2026-11-19T20:40:54.314631Z，实际fundingTime1795075200002不替换为名义整点；目前三永续均恰好记08一次。下一SMA/candidate['2026-11-19T10:30:00Z', '2026-11-19T12:30:00Z']，L4/FEWM['2026-11-19T12:10:00Z', '2026-11-19T14:10:00Z']，均不重复08，先查询实际特殊资金费；下一日决策Nov20_00:01。不重置本金、不强制平仓、不采用新研究配置。

原SMA三倍成本累计-7.468958%；原账户为延迟shadow，180日/六折资格未成熟。十策略仅只读汇总，未改冻结规则/本金/持仓或产生新成交。
保存18份唯一公共GET回执，本轮18、旧复用0、已记录运输错误0（内置重试的失败子请求URL/时间/HTTP响应未独立采集，保留stderr，不补造缺失细节）；旧首资金费来源UTC/SHA保留，完整71日SPOT权威只读。其他实际失败事实：[{"command": ["/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python", "-B", "/home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T023730Z/observe_fewm.py"], "cwd": "/home/desktop/Documents/Codex/EquiTide", "started_utc": "2026-11-20T02:49:37.835857Z", "finished_utc": "2026-11-20T02:49:38.258910Z", "exit_code": 1, "log": "research/experiments/20261120T023730Z/fewm_observe.log", "stderr": "Traceback (most recent call last):\n  File \"/home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T023730Z/observe_fewm.py\", line 15, in <module>\n    obs.capture=capture;sys.argv=[str(SOURCE/'observer.py'),'run','--round',R.name,'--cutoff',WIN['cutoff_utc'],'--lock-pid','3748537'];obs.main()\n                                                                                                                                        ^^^^^^^^^^\n  File \"/home/desktop/Documents/Codex/EquiTide/research/experiments/20261104T201939Z/prospective_fewm/observer.py\", line 125, in main\n    assert args.cutoff and args.round and args.lock_pid;owner(args.lock_pid);cut=c.ns(args.cutoff);pointer,previous=prior(binding);c.check_window(previous,cut,now())\n                                                        ^^^^^^^^^^^^^^^^^^^^\n  File \"/home/desktop/Documents/Codex/EquiTide/research/experiments/20261104T201939Z/prospective_fewm/observer.py\", line 23, in owner\n    assert any('FLOCK' in x and 'WRITE' in x and x.split()[4]==str(pid) and int(x.split()[5].split(':')[-1])==ino for x in lines),'outer branch broker must hold lock'\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nAssertionError: outer branch broker must hold lock\n", "resolved": true, "resolution": "Original guard rejected stale inherited broker PID before original main could reserve/advance;guard-only dynamically bound adapter continued this unexecuted window once;full independent NAV/books audit and exact event count passed.", "recovery_verification": "research/experiments/20261120T023730Z/observer_lock_recovery_verification.json", "recovery_verification_sha256": "77c132035cd4b93ad694f3212ee4e92ec8ed98a035b2aaa4fe66cbbb1e75c3d0", "completed_model_or_window_reruns": 0}]
监控生成成功=True，11224研究配置，11212旧行完整字典不变。

实际完成阶段命令（完成目录不得重跑市场/账户，仅保留核验和数据哈希）：

```sh
cd /home/desktop/Documents/Codex/EquiTide
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T023730Z/commands.py prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T023730Z/commands.py freeze
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T023730Z/commands.py units
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T023730Z/commands.py bind
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T023730Z/commands.py reserve_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T023730Z/commands.py reserve_1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T023730Z/commands.py evaluate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T023730Z/commands.py audit
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T023730Z/commands.py exports
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T023730Z/commands.py finish_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T023730Z/commands.py finish_1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T023730Z/commands.py research_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T023730Z/commands.py l4h02
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T023730Z/commands.py fewm
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T023730Z/commands.py fewm_retry1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T023730Z/commands.py candidate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T023730Z/commands.py forward
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T023730Z/commands.py accounts_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T023730Z/commands.py journal
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T023730Z/commands.py sources_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T023730Z/commands.py gates
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T023730Z/commands.py feed
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T023730Z/commands.py collect
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T023730Z/commands.py final_checks
```

字段格式与版本见primary_source_access.json的[Binance官方REST文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)及[公共数据README](https://github.com/binance/binance-public-data/blob/master/README.md)。所有负收益、失败、来源和冻结规则均保留；成本系数是研究假设。

FEWM首次适配器启动因遗留旧锁PID而实际退出1；此前只读取并normalize已保存L4公共数据、写执行计划，未请求新行情、未reserve/advance/记账。保留失败源文件、日志与执行计划；仅把锁PID传参改为读取真实startup后，fewm_retry1是该窗口首次成功执行。candidate在首次执行前采用同一动态锁参数修正，没有重跑L4或12个金融结果。下一轮须使用next_required_effective_observer_adapters所列有效适配器，避免复制保留的旧失败版本。

已同时补存20261120T003735Z在预算内等锁的blocked无结果事实，共4份轻量证据；该轮0个实际配置，不新增或伪造登记ID。当前轮12个实际金融配置及12个实际原账户观察各自先reserve再finish；旧轮无结果不计作回测淘汰。
