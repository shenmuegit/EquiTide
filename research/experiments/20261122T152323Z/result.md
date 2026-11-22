# 20261122T152323Z BTC实际入场金额与ETH资金费预算比率组合验证

事前固定BTC实际原生目标N1000旧/1125/1375 × ETH R.00625/.00875/.01。ETH固定S16、H=.02、M4、预算VW9、最大年龄36小时、趋势斜率K=.0075；六个新被动父组合分别reserve、计算一次及finish，十个原生银行和六个旧父/持有对照只读；历史通过6/6。预设N1125/R.00875，不按结果改选。

完整读取40952事件/20337ID和511份结论；初始16项实际结果缺口0。规范研究定义11925→11931，不能将相关路径和历史选择视为独立试验。

改变ETH新入场资金费预算相对已闭合日波动的容忍比率R，可能改变carry约束与中等BTC银行的互补。事前固定BTC目标N1000旧/1125/1375 × ETH R.00625/.00875/.01，固定ETH C15000/N4000、L5/H.02/E.0075、S16beta15/17/D3/斜率.0075、V6cap.05625、成熟M4/年龄1..36h、预算VW9。六个新被动组合，十个旧原生银行和六个旧父/持有只读，另绑定同BTC金额R.0075两份旧报告。预设1125/R.00875不按结果改选。原银行乘数[1,1]，资本C3750+15000=18750、20/80，目标5125/5375；完整共同轴美元NAV相加，保留原LOT/q/费用/非线性冲击/实际资金费/保证金，不缩放、不归一化，无父订单/转账/再平衡/跨保证金。

All component signals are read-only actually completed rules:BTC L29H.03E.005,V10cap.0275,strictpositiveROC5>.0025;ETH L5contrarianH.02,E.0075,finiteEWMS16beta15/17,D3K.0075,V6cap.05625,M4,age1..36h,R.00625/.00875/.01,VW9. No new native execution or signal fitting.

原始银行乘数[1,1]不归一化，C3750+15000=18750，资本20/80；本轮目标BTC1125或1375+ETH4000=5125或5375。每个原生组件均已按实际金额计算过LOT数量、非线性成交量冲击、费用、资金费及保证金，直接复用完整净值；父组合对齐共同时间轴相加美元NAV，无新增父订单、转账、再平衡或跨保证金，不线性缩放NAV。

391日为反复使用的开发历史2025-10-19 00:01→2026-11-14 00:01，不能称未触碰最终测试。无拟合标签，实际33闭合上下文日、embargo0；13个完整30日折+1日尾段，近期40日8×5、扩展21日5/5/5/6。折间继承现金/q，全期终点平仓计成本；整体回撤从连续完整NAV计算。

每边手续费5bp、半价差1bp、滑点2bp、0.5×过去20日样本logvol×sqrt(实际订单额/过去20日quoteADV)冲击；不利tick、LOT/最低金额、参与率≤.001。执行成本及实际资金费支出按1/2/3倍，收入不放大。线性永续无现货借币；1倍入场抵押及小时不利价1%维持保证金代理。对比等目标金额的实际持有组合和零息现金。缺L2/TCA、完整tiers、tick清算与容量实证。

|范围|BTC目标USDT|ETH资金费预算比率R|状态|净收益1/2/3倍%|整体DD3%|Sharpe3|Calmar3|正30日折1倍|近40日正5日折1/2/3|
|---|---|---|---|---|---|---|---|---|---|
|parent|1125|0.00625|passed|8.592192 / 8.154183 / 7.716333|1.365560|2.185310|5.261749|11/13|6/6/6（各/8）|
|parent|1125|0.00875|passed|9.757824 / 9.181560 / 8.605456|1.365560|2.345147|5.866396|12/13|6/6/6（各/8）|
|parent|1125|0.01|passed|9.757824 / 9.181560 / 8.605456|1.365560|2.345147|5.866396|12/13|6/6/6（各/8）|
|parent|1375|0.00625|passed|9.458270 / 8.955815 / 8.453538|1.437336|2.162026|5.475317|11/13|6/6/6（各/8）|
|parent|1375|0.00875|passed|10.623902 / 9.983192 / 9.342661|1.437336|2.311040|6.049511|12/13|6/6/6（各/8）|
|parent|1375|0.01|passed|10.623902 / 9.983192 / 9.342661|1.437336|2.311040|6.049511|12/13|6/6/6（各/8）|

事前失败判据：全期、近期和扩展各成本为正；1倍≥10/13正月；近期各成本≥6/8正5日折；扩展各成本≥3/4正折；DD3≤25%；邻域正及近期合格均≥60%；≥4次底层平仓；1倍毛损益加资金费/执行成本≥2.5；无拒单/负抵押/保证金代理违规；终点flat。

parent_BTCN1125_ETHlongonlyH200M4D3Age36hSlopeK0075VW9R0.00625_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1125_ETHlongonlyH200M4D3Age36hSlopeK0075VW9R0.00875_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1125_ETHlongonlyH200M4D3Age36hSlopeK0075VW9R0.01_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1375_ETHlongonlyH200M4D3Age36hSlopeK0075VW9R0.00625_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1375_ETHlongonlyH200M4D3Age36hSlopeK0075VW9R0.00875_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1375_ETHlongonlyH200M4D3Age36hSlopeK0075VW9R0.01_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。

相同预算比率和本金，对旧BTC1000中心四指标严格改善父组合0/6。实际损益、资金费和执行成本差见sizing_effect_decomposition.json；全部变体/成本/逐折及连续每日净值见exports/。
完整三成本路径共4种；旧路径重复按NAV_alias_inventory保留披露，不能把相关路径算独立alpha。正Sharpe比例={"parent": {"1": 1.0, "2": 1.0, "3": 1.0}}；相邻敏感性边12，启发式警示3条，边界表现仅诊断，不扩网格或改选。
BTC金额轴为1000/1125/1375，间距不均；邻域按事前索引半径1定义。这是有限局部诊断，不代表完整响应面或参数显著性。Sharpe变化警示保持披露，未据此扩网格。

本轮四账户续接120闭合分钟；原日决策{'SMA': 0, 'candidate': 0, 'l4h02': 1, 'fewm': 1}、成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、资金费{'SMA': 0, 'candidate': 0, 'l4h02': 6, 'fewm': 6}。已知Nov21_08三永续此前均已记账，本轮不重复；其他实际事件依freshGET与各自窗口处理。下一SMA/candidate['2026-11-21T22:30:00Z', '2026-11-22T00:30:00Z']、L4/FEWM['2026-11-22T00:10:00Z', '2026-11-22T02:10:00Z']须freshGET、去重并先reserve，不提前记账、不重置、不强平、不采用研究规则；SMA73日背景只读。

原SMA三倍成本累计-7.468958%，仍为延迟shadow；原10bp与Float核算不变，未采用研究规则，不冒充十策略实盘报价模拟。所有账户尚未达到180日/六折资格。
监控成功=True，展示11490项，旧11484行完整字典保持。实际GET22，传输失败0；工程/读取失败原回执与恢复见read_failures.json。

实际复现命令（已完成模型和账户窗口不得重复计算）：

```sh
cd /home/desktop/Documents/Codex/EquiTide
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T152323Z/commands.py prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T152323Z/commands.py freeze
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T152323Z/commands.py units
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T152323Z/commands.py bind
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T152323Z/commands.py reserve_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T152323Z/commands.py evaluate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T152323Z/commands.py audit
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T152323Z/commands.py exports
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T152323Z/commands.py finish_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T152323Z/commands.py research_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T152323Z/commands.py l4h02
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T152323Z/commands.py fewm
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T152323Z/commands.py candidate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T152323Z/commands.py forward
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T152323Z/commands.py accounts_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T152323Z/commands.py journal
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T152323Z/commands.py sources_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T152323Z/commands.py gates
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T152323Z/commands.py feed
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T152323Z/commands.py midnight_prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T152323Z/commands.py collect
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T152323Z/commands.py final_checks
```

官方来源和访问UTC见primary_source_access.json：[Binance市场数据文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)。正收益回测不代表稳定实盘盈利。

与同金额、H.02、年龄36小时、S16、成熟M4、预算VW9且比率R.0075的已完成结果比较：
BTC N1125/R0.00625：收益差-0.889123pp、整体DD差0.000000pp、Sharpe差-0.159837、Calmar差-0.604647；完整NAV同路径=False。
BTC N1125/R0.00875：收益差0.000000pp、整体DD差0.000000pp、Sharpe差0.000000、Calmar差0.000000；完整NAV同路径=True。
BTC N1125/R0.01：收益差0.000000pp、整体DD差0.000000pp、Sharpe差0.000000、Calmar差0.000000；完整NAV同路径=True。
BTC N1375/R0.00625：收益差-0.889123pp、整体DD差0.000000pp、Sharpe差-0.149014、Calmar差-0.574193；完整NAV同路径=False。
BTC N1375/R0.00875：收益差0.000000pp、整体DD差0.000000pp、Sharpe差0.000000、Calmar差0.000000；完整NAV同路径=True。
BTC N1375/R0.01：收益差0.000000pp、整体DD差0.000000pp、Sharpe差0.000000、Calmar差0.000000；完整NAV同路径=True。
全部18个逐成本比较见exports/previous_R0075_comparisons.csv；仅比较已完成报告，不重跑旧组件或旧组合。

与同金额R.0075的18个逐成本比较：四指标同时改善0项，旧R.0075支配6项，完整NAV同路径12项；全成本同旧R.0075路径的新图4个。见comparison_scope_review.json。历史门槛状态与比较优劣分别保留；维持事前1125/R.00875，不据结果换候选，不修改原冻结账户。相关配置和重复历史不构成独立前向或实盘盈利证据。

下一原冻结账户窗口的历史真实结算留证：fundingTime毫秒=[1795305600001]，各自下一窗口待处理记录={"SMA": 0, "candidate": 6, "l4h02": 0, "fewm": 0}。首次捕获UTC=2026-11-22T13:55:24.752610Z及来源SHA保持；本轮未提前入账。下一轮须刷新实际来源、按自身窗口去重并先reserve，再以自身q/成本核算，不复用其他账户金额。详见next_preparation_contract.new_actual_settlement_handoff。

本轮L4/FEWM按原冻结日内核执行Nov22日决策及实际00:00:00.001资金费，各自现金/q/成交见独立账本；SMA/candidate本轮仍仅mark。下一SMA/candidate跨Nov22_00:01，必须使用真实full74日背景与原日适配器，先刷新来源并reserve；L4/FEWM下一窗口不重复已记00事件。研究增量见funding_ratio_tradeoff_review.json，保留事前1125/R.00875代表及全部门槛状态，无独立未来资格。

已知Nov21_08:00:00.003三永续此前均已记账一次，本轮不重复；当前资金费记录={"SMA": 0, "candidate": 0, "l4h02": 6, "fewm": 6}。08全链唯一计数各6，首次捕获UTC和原始来源SHA保持；下一窗口继续freshGET与按账户去重，不提前记账。

旧Nov21_16事件三个永续各6个唯一键，本轮旧事件0新增；当前Nov22资金费独立按各自q/mark/rate/成本重核，candidate0、L4/FEWM各6记录，十八本现金与原内核成交完整对账。原只读复核把全部当前资金费假定为零的断言失败及源码原样保留，使用reconcile_actual16_daily.py校验；没有重跑金融或账户窗口，也未覆盖下一SMAfull74日决策准备。

本轮只读复核命令（不得重跑已完成金融模型或账户窗口）：

```sh
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T152323Z/component_reuse_review.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T152323Z/funding_availability_review.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T152323Z/compare_previous_H.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T152323Z/review_economic_identity.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T152323Z/reconcile_actual08.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T152323Z/reconcile_actual16_daily.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T152323Z/review_next_handoff.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T152323Z/final_notes.py
```
