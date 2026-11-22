# 20261122T112219Z BTC实际入场金额与ETH资金费预算波动窗口组合验证

事前固定BTC实际原生目标N1000旧/1125/1375 × ETH VW7/8/10。ETH固定S16、H=.02、M4、最大年龄36小时、趋势斜率K=.0075；六个新被动父组合分别reserve、计算一次及finish，十个原生银行和六个旧父/持有对照只读；历史通过6/6。预设N1125/VW8，不按结果改选。

完整读取40840事件/20281ID和509份结论；初始16项实际结果缺口0。规范研究定义11913→11919，不能将相关路径和历史选择视为独立试验。

改变ETH新入场资金费预算所用的已闭合日波动样本窗口VW，可能改变carry预算与BTC金额之间的互补。事前固定BTC实际目标N1000旧/1125/1375 × ETH VW7/8/10日；固定ETH C15000/N4000、L5/H.02/E.0075、有限EWMS16beta15/17、D3/斜率.0075、V6cap.05625、成熟结算M4/年龄1..36h、R.0075。六个新被动组合，十个旧实际原生银行及六个旧父/持有只读；另事前绑定同BTC金额VW9两份旧报告。预设N1125/VW8，不按结果改选扩网格。原银行乘数[1,1]，C3750+15000=18750、资本20/80，初始目标5125/5375；完整共同轴美元NAV相加，保持原LOT/q/非线性冲击/费用/实际资金费/保证金，不缩放、不归一化、不转账再平衡或跨保证金。

All component signals are read-only actually completed rules:BTC L29H.03E.005,V10cap.0275,strictpositiveROC5>.0025;ETH L5contrarianH.02,E.0075,finiteEWMS16beta15/17,D3K.0075,V6cap.05625,M4,age1..36h,R.0075,VW7/8/10. No new native execution or signal fitting.

原始银行乘数[1,1]不归一化，C3750+15000=18750，资本20/80；本轮目标BTC1125或1375+ETH4000=5125或5375。每个原生组件均已按实际金额计算过LOT数量、非线性成交量冲击、费用、资金费及保证金，直接复用完整净值；父组合对齐共同时间轴相加美元NAV，无新增父订单、转账、再平衡或跨保证金，不线性缩放NAV。

391日为反复使用的开发历史2025-10-19 00:01→2026-11-14 00:01，不能称未触碰最终测试。无拟合标签，实际33闭合上下文日、embargo0；13个完整30日折+1日尾段，近期40日8×5、扩展21日5/5/5/6。折间继承现金/q，全期终点平仓计成本；整体回撤从连续完整NAV计算。

每边手续费5bp、半价差1bp、滑点2bp、0.5×过去20日样本logvol×sqrt(实际订单额/过去20日quoteADV)冲击；不利tick、LOT/最低金额、参与率≤.001。执行成本及实际资金费支出按1/2/3倍，收入不放大。线性永续无现货借币；1倍入场抵押及小时不利价1%维持保证金代理。对比等目标金额的实际持有组合和零息现金。缺L2/TCA、完整tiers、tick清算与容量实证。

|范围|BTC目标USDT|ETH预算波动窗口VW|状态|净收益1/2/3倍%|整体DD3%|Sharpe3|Calmar3|正30日折1倍|近40日正5日折1/2/3|
|---|---|---|---|---|---|---|---|---|---|
|parent|1125|7|passed|8.889919 / 8.415244 / 7.940729|1.365560|2.239931|5.414381|12/13|6/6/6（各/8）|
|parent|1125|8|passed|9.588637 / 9.072561 / 8.556645|1.365560|2.366137|5.833211|12/13|6/6/6（各/8）|
|parent|1125|10|passed|9.757824 / 9.181560 / 8.605456|1.365560|2.345147|5.866396|12/13|6/6/6（各/8）|
|parent|1375|7|passed|9.755997 / 9.216876 / 8.677934|1.437336|2.211870|5.620261|12/13|6/6/6（各/8）|
|parent|1375|8|passed|10.454715 / 9.874193 / 9.293850|1.437336|2.328477|6.017996|12/13|6/6/6（各/8）|
|parent|1375|10|passed|10.623902 / 9.983192 / 9.342661|1.437336|2.311040|6.049511|12/13|6/6/6（各/8）|

事前失败判据：全期、近期和扩展各成本为正；1倍≥10/13正月；近期各成本≥6/8正5日折；扩展各成本≥3/4正折；DD3≤25%；邻域正及近期合格均≥60%；≥4次底层平仓；1倍毛损益加资金费/执行成本≥2.5；无拒单/负抵押/保证金代理违规；终点flat。

parent_BTCN1125_ETHlongonlyH200M4D3Age36hSlopeK0075VW7_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1125_ETHlongonlyH200M4D3Age36hSlopeK0075VW8_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1125_ETHlongonlyH200M4D3Age36hSlopeK0075VW10_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1375_ETHlongonlyH200M4D3Age36hSlopeK0075VW7_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1375_ETHlongonlyH200M4D3Age36hSlopeK0075VW8_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1375_ETHlongonlyH200M4D3Age36hSlopeK0075VW10_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。

相同预算波动窗口和本金，对旧BTC1000中心四指标严格改善父组合0/6。实际损益、资金费和执行成本差见sizing_effect_decomposition.json；全部变体/成本/逐折及连续每日净值见exports/。
完整三成本路径共6种；旧路径重复按NAV_alias_inventory保留披露，不能把相关路径算独立alpha。正Sharpe比例={"parent": {"1": 1.0, "2": 1.0, "3": 1.0}}；相邻敏感性边12，启发式警示3条，边界表现仅诊断，不扩网格或改选。
BTC金额轴为1000/1125/1375，间距不均；邻域按事前索引半径1定义。这是有限局部诊断，不代表完整响应面或参数显著性。Sharpe变化警示保持披露，未据此扩网格。

本轮四账户续接120闭合分钟；原日决策{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、资金费{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}。已知Nov21_08三永续此前均已记账，本轮不重复；其他实际事件依freshGET与各自窗口处理。下一SMA/candidate['2026-11-21T18:30:00Z', '2026-11-21T20:30:00Z']、L4/FEWM['2026-11-21T20:10:00Z', '2026-11-21T22:10:00Z']须freshGET、去重并先reserve，不提前记账、不重置、不强平、不采用研究规则；SMA73日背景只读。

原SMA三倍成本累计-7.468958%，仍为延迟shadow；原10bp与Float核算不变，未采用研究规则，不冒充十策略实盘报价模拟。所有账户尚未达到180日/六折资格。
监控成功=True，展示11478项，旧11472行完整字典保持。实际GET25，传输失败4；工程/读取失败原回执与恢复见read_failures.json。

实际复现命令（已完成模型和账户窗口不得重复计算）：

```sh
cd /home/desktop/Documents/Codex/EquiTide
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T112219Z/commands.py prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T112219Z/commands.py freeze
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T112219Z/commands.py units
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T112219Z/commands.py bind
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T112219Z/commands.py reserve_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T112219Z/commands.py evaluate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T112219Z/commands.py audit
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T112219Z/commands.py exports
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T112219Z/commands.py finish_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T112219Z/commands.py research_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T112219Z/commands.py l4h02
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T112219Z/commands.py fewm
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T112219Z/commands.py candidate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T112219Z/commands.py forward
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T112219Z/commands.py accounts_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T112219Z/commands.py journal
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T112219Z/commands.py sources_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T112219Z/commands.py gates
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T112219Z/commands.py feed
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T112219Z/commands.py midnight_prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T112219Z/commands.py collect
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T112219Z/commands.py final_checks
```

官方来源和访问UTC见primary_source_access.json：[Binance市场数据文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)。正收益回测不代表稳定实盘盈利。

原Nov21日决策与已知00/08资金费均此前处理，本轮按各自实际窗口核验，未重复、未提前记账。下一原日决策Nov22_00:01，当前与下一窗口仍在其之前，原SMA73日背景只读。

Nov20_16三永续此前均已各记一次，本轮各0条；三永续唯一计数均6。首捕获UTC=2026-11-21T05:15:47.350340Z及原始毫秒/mark/rate保持。下一SMA/candidateNov21 18:30→20:30、L4/FEWM20:10→22:10（四原账户均已处理原Nov21日决策/资金费），须新鲜查询实际事件，不重复已记16，不提前记账。

与同金额、M4、H.02、年龄36小时、S16及预算波动窗口VW9的已完成结果比较：
BTC N1125/VW7：收益差-0.664727pp、整体DD差0.000000pp、Sharpe差-0.105216、Calmar差-0.452016；完整NAV同路径=False。
BTC N1125/VW8：收益差-0.048811pp、整体DD差0.000000pp、Sharpe差0.020990、Calmar差-0.033186；完整NAV同路径=False。
BTC N1125/VW10：收益差0.000000pp、整体DD差0.000000pp、Sharpe差0.000000、Calmar差0.000000；完整NAV同路径=True。
BTC N1375/VW7：收益差-0.664727pp、整体DD差0.000000pp、Sharpe差-0.099170、Calmar差-0.429250；完整NAV同路径=False。
BTC N1375/VW8：收益差-0.048811pp、整体DD差0.000000pp、Sharpe差0.017437、Calmar差-0.031514；完整NAV同路径=False。
BTC N1375/VW10：收益差0.000000pp、整体DD差0.000000pp、Sharpe差0.000000、Calmar差0.000000；完整NAV同路径=True。
全部18个逐成本比较见exports/previous_VW9_comparisons.csv；仅比较已完成报告，不重跑旧组件或旧组合。

与同金额VW9的18个逐成本比较：四指标同时改善0项，旧VW9支配8项，完整NAV同路径6项；全成本同旧VW9路径的新图2个。见comparison_scope_review.json。历史门槛状态与比较优劣分别保留；维持事前1125/VW8，不据结果换候选，不修改原冻结账户。相关配置和重复历史不构成独立前向或实盘盈利证据。

下轮准备提示：即刻下一窗口仍无原日决策；再后一个L4/FEWM窗口将覆盖冻结的Nov22_00:01日决策。跨日时必须恢复原日核算器并读取真实已闭合日背景，不能沿用只做mark的假设；资金费实际时间/字段仍须新鲜完整查询后按各自窗口去重、先reserve，不按名义日界预记账。此处仅留日历提示，无提前计算或记账。

增量判定：VW10两图在三成本下与同金额旧VW9全路径一致；VW8在三倍成本下Sharpe小幅提高，但净收益与Calmar下降、整体回撤相同；VW7较弱。故保留全部真实结果及原历史门槛状态，不升级新候选，不改变事前1125/VW8代表，不把复用历史解释为独立前向盈利证据。

已知Nov21_08:00:00.003三永续此前均已记账一次，本轮不重复；当前资金费记录={"SMA": 0, "candidate": 0, "l4h02": 0, "fewm": 0}。08全链唯一计数各6，首次捕获UTC和原始来源SHA保持；下一窗口继续freshGET与按账户去重，不提前记账。

实际Nov21_16:00:00.000此前三永续均已按各自q/rate/mark/成本记账一次，全链唯一计数各6，本轮各新增0；十八个原账本不重置、不重复记资金费。首次来源UTC及SHA保持。下一SMA/candidate18:30→20:30、L4/FEWM20:10→22:10仍排除已知16结算；须刷新实际来源、按各自窗口去重并先reserve，不提前入账。

本轮只读复核命令（不得重跑已完成金融模型或账户窗口）：

```sh
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T112219Z/component_reuse_review.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T112219Z/funding_availability_review.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T112219Z/compare_previous_H.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T112219Z/review_economic_identity.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T112219Z/reconcile_actual08.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T112219Z/reconcile_actual16.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T112219Z/review_next_handoff.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T112219Z/final_notes.py
```
