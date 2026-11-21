# 20261121T205504Z BTC实际入场金额与ETH较宽松趋势斜率组合验证

事前固定BTC实际原生目标N1000旧/1500/1750 × ETH M4/5/6。ETH固定H=.02、最大年龄48小时、趋势斜率K=.00625；六个新被动父组合分别reserve、计算一次及finish，十个原生银行和六个旧父/持有对照只读；历史通过6/6。预设N1500/M5，不按结果改选。

完整读取40448事件/20085ID和502份结论；初始16项实际结果缺口0。规范研究定义11871→11877，不能将相关路径和历史选择视为独立试验。

放宽ETH有限EWM趋势斜率门槛至已实际执行的0.00625，改变入场集合后，较大BTC趋势银行可能改善其组合风险互补。事前固定BTC N1000旧/1500/1750 × ETH M4/5/6；ETH H.02、L5/E.0075/S16/D3/K.00625/V6cap.05625、年龄1..48h、R.0075/VW9及N4000/C15000固定。六个新父组合，十个旧原生银行及六个旧父/持有对照只读。预设N1500/M5，不看结果改选或扩网格；与相同金额及M、斜率K.0075/age48的已完成结果比较。原始银行乘数[1,1]、C3750+15000=18750、资本20/80，目标5500/5750；不缩放数量/NAV，不归一化、不转账、不再平衡、不跨保证金。

All component signals are read-only actually completed rules:BTC L29H.03E.005,V10cap.0275,strictpositiveROC5>.0025;ETH L5contrarianH.02,E.0075,finiteEWMS16beta15/17,D3K.00625,V6cap.05625,M4/5/6,age1..48h,R.0075,VW9. No new native execution or signal fitting.

原始银行乘数[1,1]不归一化，C3750+15000=18750，资本20/80；本轮目标BTC1500或1750+ETH4000=5500或5750。每个原生组件均已按实际金额计算过LOT数量、非线性成交量冲击、费用、资金费及保证金，直接复用完整净值；父组合对齐共同时间轴相加美元NAV，无新增父订单、转账、再平衡或跨保证金，不线性缩放NAV。

391日为反复使用的开发历史2025-10-19 00:01→2026-11-14 00:01，不能称未触碰最终测试。无拟合标签，实际33闭合上下文日、embargo0；13个完整30日折+1日尾段，近期40日8×5、扩展21日5/5/5/6。折间继承现金/q，全期终点平仓计成本；整体回撤从连续完整NAV计算。

每边手续费5bp、半价差1bp、滑点2bp、0.5×过去20日样本logvol×sqrt(实际订单额/过去20日quoteADV)冲击；不利tick、LOT/最低金额、参与率≤.001。执行成本及实际资金费支出按1/2/3倍，收入不放大。线性永续无现货借币；1倍入场抵押及小时不利价1%维持保证金代理。对比等目标金额的实际持有组合和零息现金。缺L2/TCA、完整tiers、tick清算与容量实证。

|范围|BTC目标USDT|ETH成熟M|状态|净收益1/2/3倍%|整体DD3%|Sharpe3|Calmar3|正30日折1倍|近40日正5日折1/2/3|
|---|---|---|---|---|---|---|---|---|---|
|parent|1500|4|passed|9.915344 / 9.194147 / 8.473175|4.197205|1.698877|1.879370|11/13|6/6/6（各/8）|
|parent|1500|5|passed|8.937500 / 8.257785 / 7.578293|4.197205|1.581080|1.681358|11/13|6/6/6（各/8）|
|parent|1500|6|passed|9.645015 / 8.920002 / 8.195213|4.197205|1.637385|1.817877|11/13|6/6/6（各/8）|
|parent|1750|4|passed|10.893742 / 10.104500 / 9.315496|4.476548|1.725307|1.936753|11/13|6/6/6（各/8）|
|parent|1750|5|passed|9.915898 / 9.168137 / 8.420614|4.476548|1.618167|1.751193|11/13|6/6/6（各/8）|
|parent|1750|6|passed|10.623412 / 9.830354 / 9.037534|4.476548|1.668802|1.879127|11/13|6/6/6（各/8）|

事前失败判据：全期、近期和扩展各成本为正；1倍≥10/13正月；近期各成本≥6/8正5日折；扩展各成本≥3/4正折；DD3≤25%；邻域正及近期合格均≥60%；≥4次底层平仓；1倍毛损益加资金费/执行成本≥2.5；无拒单/负抵押/保证金代理违规；终点flat。

parent_BTCN1500_ETHlongonlyH200M4Age48hSlopeK00625_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1500_ETHlongonlyH200M5Age48hSlopeK00625_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1500_ETHlongonlyH200M6Age48hSlopeK00625_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1750_ETHlongonlyH200M4Age48hSlopeK00625_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1750_ETHlongonlyH200M5Age48hSlopeK00625_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1750_ETHlongonlyH200M6Age48hSlopeK00625_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。

相同M和本金，对旧BTC1000中心四指标严格改善父组合0/6。实际损益、资金费和执行成本差见sizing_effect_decomposition.json；全部变体/成本/逐折及连续每日净值见exports/。
完整三成本路径共6种；旧路径重复按NAV_alias_inventory保留披露，不能把相关路径算独立alpha。正Sharpe比例={"parent": {"1": 1.0, "2": 1.0, "3": 1.0}}；相邻敏感性边12，启发式警示6条，边界表现仅诊断，不扩网格或改选。
BTC金额轴为1000/1500/1750，间距不均；邻域按事前索引半径1定义。这是有限局部诊断，不代表完整响应面或参数显著性。Sharpe变化警示保持披露，未据此扩网格。

本轮四账户各续接120闭合分钟；原日决策数{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、成交数{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、实际资金费记录{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}，按各自现金/数量/费用和完整NAV核对。四账户的Nov21原日决策及三永续实际00:00:00.002资金费均已在此前完成，本轮不重复；SMA完整73日真实SPOT背景只读，按原Float估值延续现金与数量，不运行日决策或新增成交。三永续资金费各恰好一次，四原账户日决策均已完成。下一SMA/candidate['2026-11-21T04:30:00Z', '2026-11-21T06:30:00Z']、L4/FEWM['2026-11-21T06:10:00Z', '2026-11-21T08:10:00Z']无原日决策；须新鲜查询并仅在各自窗口内核算实际资金费，下一原日决策Nov22_00:01。保留各自现金/q/desired/成本，不重置、不强制平仓、不采用研究配置。

原SMA三倍成本累计-7.468958%，仍为延迟shadow；原10bp与Float核算不变，未采用研究规则，不冒充十策略实盘报价模拟。所有账户尚未达到180日/六折资格。
监控成功=True，展示11436项，旧11430行完整字典保持。实际GET23，传输失败3；工程/读取失败原回执与恢复见read_failures.json。

实际复现命令（已完成模型和账户窗口不得重复计算）：

```sh
cd /home/desktop/Documents/Codex/EquiTide
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T205504Z/commands.py prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T205504Z/commands.py freeze
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T205504Z/commands.py units
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T205504Z/commands.py bind
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T205504Z/commands.py reserve_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T205504Z/commands.py evaluate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T205504Z/commands.py audit
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T205504Z/commands.py exports
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T205504Z/commands.py finish_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T205504Z/commands.py research_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T205504Z/commands.py l4h02
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T205504Z/commands.py fewm
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T205504Z/commands.py candidate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T205504Z/commands.py forward
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T205504Z/commands.py accounts_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T205504Z/commands.py journal
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T205504Z/commands.py sources_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T205504Z/commands.py gates
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T205504Z/commands.py feed
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T205504Z/commands.py midnight_prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T205504Z/commands.py collect
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T205504Z/commands.py final_checks
```

官方来源和访问UTC见primary_source_access.json：[Binance市场数据文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)。正收益回测不代表稳定实盘盈利。

Nov21跨日上轮已完成：本轮四原账户仅续接估值，日决策均0次；既有73日真实SPOT上下文只读，保留原Float/10bp规则。三永续资金费唯一计数均6，四原账户Nov21日决策均已完成。首捕获UTC=2026-11-21T13:20:15.157839Z保持。下一SMA/candidate04:30→06:30没有已知新结算；L4/FEWM06:10→08:10覆盖实际08:00:00.003。各自须重新查询、按窗口去重并先reserve，再按原持仓和成本场景核算资金费；不新增日决策、不提前入账；下一原日决策为Nov22_00:01，不提前入账。

Nov20_16三永续此前均已各记一次，本轮各0条；三永续唯一计数均6。首捕获UTC=2026-11-21T05:15:47.350340Z及原始毫秒/mark/rate保持。下一SMA/candidateNov21 04:30→06:30、L4/FEWM06:10→08:10（四原账户均已处理原Nov21日决策/资金费），须新鲜查询实际事件，不重复已记16，不提前记账。

与同金额、同M、H.02、年龄48小时且斜率K=.0075的已完成结果比较：
BTC N1500/M4：收益差-1.240558pp、整体DD差2.662750pp、Sharpe差-0.604266、Calmar差-4.011637；完整NAV同路径=False。
BTC N1500/M5：收益差-1.240558pp、整体DD差2.662750pp、Sharpe差-0.625007、Calmar差-3.668436；完整NAV同路径=False。
BTC N1500/M6：收益差-1.240558pp、整体DD差2.662750pp、Sharpe差-0.586670、Calmar差-3.905054；完整NAV同路径=False。
BTC N1750/M4：收益差-1.240558pp、整体DD差2.656245pp、Sharpe差-0.541750、Calmar差-3.458372；完整NAV同路径=False。
BTC N1750/M5：收益差-1.240558pp、整体DD差2.656245pp、Sharpe差-0.558198、Calmar差-3.187941；完整NAV同路径=False。
BTC N1750/M6：收益差-1.240558pp、整体DD差2.656245pp、Sharpe差-0.527768、Calmar差-3.374388；完整NAV同路径=False。
全部18个逐成本比较见exports/previous_H002_comparisons.csv；仅比较已完成报告，不重跑旧组件或旧组合。

冻结计划axis_semantics有一处旧age60说明，真实冻结配置及源组件均为age48、斜率K.00625；原文件及哈希保留，文字勘误见axis_label_scope_review.json。未改参数、未重跑任何金融模型或账户窗口。

本轮六个新组合均通过历史门槛，但同金额、同M、同H和age48的旧K.0075方案在18个逐成本比较中净收益更高、整体回撤更低、Sharpe和Calmar更高；本轮不提升候选。不同完整NAV保留为真实已测结果，不能称独立前向或实盘盈利证据。见slope_comparison_review.json。

本轮只读复核命令（不得重跑已完成金融模型或账户窗口）：

```sh
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T205504Z/bootstrap.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T205504Z/component_reuse_review.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T205504Z/funding_availability_review.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T205504Z/compare_previous_H.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T205504Z/review_economic_identity.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T205504Z/review_next_handoff.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T205504Z/final_notes.py
```
