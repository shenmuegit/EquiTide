# 20261121T165204Z BTC实际入场金额与ETH 2.25%门槛成熟资金费组合验证

事前固定BTC实际原生目标N1000旧/1500/1750 × ETH M4/5/6。ETH固定H=.0225；六个新被动父组合分别reserve、计算一次及finish，十个原生银行和六个旧父/持有对照只读；历史通过6/6。预设N1500/M5，不按结果改选。

完整读取40336事件/20029ID和500份结论；初始16项实际结果缺口0。规范研究定义11859→11865，不能将相关路径和历史选择视为独立试验。

提高ETH逆势入场门槛至已实际执行的2.25%，可能改变与较大BTC头寸的风险互补。事前固定BTC N1000旧/1500/1750 × ETH成熟资金费M4/5/6，ETH H.0225、L5/E.0075/S16/D3/K.0075/V6cap.05625、年龄1..48h、R.0075/VW9固定；六个新被动组合，十个原生银行和六个旧父/持有对照只读。预设N1500/M5。原始银行乘数[1,1]，C3750+15000=18750、资本20/80，目标5500/5750USDT；不缩放NAV或数量、不归一化、不转账、不再平衡、不跨保证金。与上一批相同金额H.02结果只读对比，不按结果改选。

All component signals are read-only actually completed rules:BTC L29H.03E.005,V10cap.0275,strictpositiveROC5>.0025;ETH L5contrarianH.0225,E.0075,finiteEWMS16beta15/17,D3K.0075,V6cap.05625,M4/5/6,age1..48h,R.0075,VW9. No new native execution or signal fitting.

原始银行乘数[1,1]不归一化，C3750+15000=18750，资本20/80；本轮目标BTC1500或1750+ETH4000=5500或5750。每个原生组件均已按实际金额计算过LOT数量、非线性成交量冲击、费用、资金费及保证金，直接复用完整净值；父组合对齐共同时间轴相加美元NAV，无新增父订单、转账、再平衡或跨保证金，不线性缩放NAV。

391日为反复使用的开发历史2025-10-19 00:01→2026-11-14 00:01，不能称未触碰最终测试。无拟合标签，实际33闭合上下文日、embargo0；13个完整30日折+1日尾段，近期40日8×5、扩展21日5/5/5/6。折间继承现金/q，全期终点平仓计成本；整体回撤从连续完整NAV计算。

每边手续费5bp、半价差1bp、滑点2bp、0.5×过去20日样本logvol×sqrt(实际订单额/过去20日quoteADV)冲击；不利tick、LOT/最低金额、参与率≤.001。执行成本及实际资金费支出按1/2/3倍，收入不放大。线性永续无现货借币；1倍入场抵押及小时不利价1%维持保证金代理。对比等目标金额的实际持有组合和零息现金。缺L2/TCA、完整tiers、tick清算与容量实证。

|范围|BTC目标USDT|ETH成熟M|状态|净收益1/2/3倍%|整体DD3%|Sharpe3|Calmar3|正30日折1倍|近40日正5日折1/2/3|
|---|---|---|---|---|---|---|---|---|---|
|parent|1500|4|passed|6.011143 / 5.541006 / 5.070859|1.793675|1.539776|2.634717|10/13|6/6/6（各/8）|
|parent|1500|5|passed|6.011143 / 5.541006 / 5.070859|1.793675|1.539776|2.634717|10/13|6/6/6（各/8）|
|parent|1500|6|passed|6.718658 / 6.203223 / 5.687779|1.793675|1.582734|2.954672|10/13|6/6/6（各/8）|
|parent|1750|4|passed|6.989541 / 6.451358 / 5.913180|2.118338|1.546019|2.600787|10/13|6/6/6（各/8）|
|parent|1750|5|passed|6.989541 / 6.451358 / 5.913180|2.118338|1.546019|2.600787|10/13|6/6/6（各/8）|
|parent|1750|6|passed|7.697055 / 7.113576 / 6.530100|2.118338|1.589817|2.871561|10/13|6/6/6（各/8）|

事前失败判据：全期、近期和扩展各成本为正；1倍≥10/13正月；近期各成本≥6/8正5日折；扩展各成本≥3/4正折；DD3≤25%；邻域正及近期合格均≥60%；≥4次底层平仓；1倍毛损益加资金费/执行成本≥2.5；无拒单/负抵押/保证金代理违规；终点flat。

parent_BTCN1500_ETHlongonlyH225M4Age48h_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1500_ETHlongonlyH225M5Age48h_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1500_ETHlongonlyH225M6Age48h_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1750_ETHlongonlyH225M4Age48h_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1750_ETHlongonlyH225M5Age48h_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1750_ETHlongonlyH225M6Age48h_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。

相同M和本金，对旧BTC1000中心四指标严格改善父组合0/6。实际损益、资金费和执行成本差见sizing_effect_decomposition.json；全部变体/成本/逐折及连续每日净值见exports/。
完整三成本路径共4种；旧路径重复按NAV_alias_inventory保留披露，不能把相关路径算独立alpha。正Sharpe比例={"parent": {"1": 1.0, "2": 1.0, "3": 1.0}}；相邻敏感性边12，启发式警示2条，边界表现仅诊断，不扩网格或改选。
BTC金额轴为1000/1500/1750，间距不均；邻域按事前索引半径1定义。这是有限局部诊断，不代表完整响应面或参数显著性。Sharpe变化警示保持披露，未据此扩网格。

本轮四账户各续接120闭合分钟；原日决策数{'SMA': 1, 'candidate': 1, 'l4h02': 0, 'fewm': 0}、成交数{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、实际资金费记录{'SMA': 0, 'candidate': 6, 'l4h02': 0, 'fewm': 0}，按各自现金/数量/费用和完整NAV核对。candidate本轮处理实际Nov21_00:00:00.002资金费及原00:01日决策；SMA使用73日真实SPOT数据按原SMA65/1%和Float10bp核算原日决策；L4/FEWM此前已处理Nov21日决策/资金费，本轮不重复。三永续资金费各恰好一次，四原账户日决策均已完成。下一SMA/candidate['2026-11-21T00:30:00Z', '2026-11-21T02:30:00Z']、L4/FEWM['2026-11-21T02:10:00Z', '2026-11-21T04:10:00Z']只续估值并新鲜查询实际特殊资金费，下一原日决策Nov22_00:01。保留各自现金/q/desired/成本，不重置、不强制平仓、不采用研究配置。

原SMA三倍成本累计-7.468958%，仍为延迟shadow；原10bp与Float核算不变，未采用研究规则，不冒充十策略实盘报价模拟。所有账户尚未达到180日/六折资格。
监控成功=True，展示11424项，旧11418行完整字典保持。实际GET23，传输失败1；工程/读取失败原回执与恢复见read_failures.json。

实际复现命令（已完成模型和账户窗口不得重复计算）：

```sh
cd /home/desktop/Documents/Codex/EquiTide
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T165204Z/commands.py prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T165204Z/commands.py freeze
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T165204Z/commands.py units
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T165204Z/commands.py bind
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T165204Z/commands.py reserve_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T165204Z/commands.py evaluate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T165204Z/commands.py audit
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T165204Z/commands.py exports
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T165204Z/commands.py finish_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T165204Z/commands.py research_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T165204Z/commands.py l4h02
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T165204Z/commands.py fewm
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T165204Z/commands.py candidate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T165204Z/commands.py forward
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T165204Z/commands.py accounts_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T165204Z/commands.py journal
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T165204Z/commands.py sources_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T165204Z/commands.py gates
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T165204Z/commands.py feed
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T165204Z/commands.py midnight_prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T165204Z/commands.py collect
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T165204Z/commands.py final_checks
```

官方来源和访问UTC见primary_source_access.json：[Binance市场数据文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)。正收益回测不代表稳定实盘盈利。

Nov21跨日全部完成：本轮candidate资金费6条及原日决策一次，SMA原日决策每资产一次，保留原Float/10bp及完整73日真实SPOT上下文；L4/FEWM已处理过Nov21，本轮不重复。三永续资金费唯一计数均6，四原账户Nov21日决策均已完成。首捕获UTC=2026-11-21T13:20:15.157839Z保持。下一SMA/candidate00:30→02:30、L4/FEWM02:10→04:10仅估值并新鲜查询实际特殊资金费；下一原日决策为Nov22_00:01，不提前入账。

Nov20_16三永续此前均已各记一次，本轮各0条；三永续唯一计数均6。首捕获UTC=2026-11-21T05:15:47.350340Z及原始毫秒/mark/rate保持。下一SMA/candidateNov21 00:30→02:30、L4/FEWM02:10→04:10（四原账户均已处理原Nov21日决策/资金费），须新鲜查询实际事件，不重复已记16，不提前记账。

与上轮相同BTC金额、相同M、相同本金的ETH H.02结果只读对照（本轮H.0225，不据此重新择参）：

|BTC目标|M|净收益差pp（3倍）|整体DD差pp|Sharpe差|Calmar差|全路径相同|
|---|---|---|---|---|---|---|
|1500|4|-4.6428740140968205|0.2592198559187797|-0.7633667708910883|-3.2562902189011114|False|
|1500|5|-3.7479917770453|0.2592198559187797|-0.666310130800138|-2.715076488647685|False|
|1500|6|-3.747991777045323|0.2592198559187797|-0.6413210920448513|-2.768259161200119|False|
|1750|4|-4.64287401409682|0.29803452611769643|-0.7210385301192233|-2.7943383491301685|False|
|1750|5|-3.747991777045322|0.29803452611769643|-0.6303461164931554|-2.3383461327576724|False|
|1750|6|-3.747991777045322|0.29803452611769643|-0.6067528950414056|-2.381953644849525|False|

全部18个逐成本比较见exports/previous_H002_comparisons.csv；均来自已完成报告，不重跑旧组件或上一批组合。

三倍成本下，相同金额旧H.02在净收益、整体回撤、Sharpe、Calmar均优于新H.0225的配置数=6/6；本轮历史门槛状态保持，作为上一批的替代方案不提升。重复路径保留，不作为独立alpha证据。

本轮只读复核命令（不得重跑已完成金融模型或账户窗口）：

```sh
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T165204Z/component_reuse_review.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T165204Z/funding_availability_review.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T165204Z/compare_previous_H.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T165204Z/review_economic_identity.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T165204Z/normalize_comparison_csv.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T165204Z/final_notes.py
```
