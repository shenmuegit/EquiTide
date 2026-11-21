# 20261121T185301Z BTC实际入场金额与ETH 60小时成熟资金费组合验证

事前固定BTC实际原生目标N1000旧/1500/1750 × ETH M4/5/6。ETH固定H=.02、最大年龄60小时；六个新被动父组合分别reserve、计算一次及finish，十个原生银行和六个旧父/持有对照只读；历史通过6/6。预设N1500/M5，不按结果改选。

完整读取40392事件/20057ID和501份结论；初始16项实际结果缺口0。规范研究定义11865→11871，不能将相关路径和历史选择视为独立试验。

放宽ETH成熟资金费历史最大年龄至60小时，可能增加可用历史、改变与较大BTC银行的风险互补。事前固定BTC N1000旧/1500/1750 × ETH M4/5/6，ETH H.02、L5/E.0075/S16/D3/K.0075/V6cap.05625、年龄1..60h、R.0075/VW9固定；六个新被动组合，十个原生银行和六个旧父/持有对照只读。预设N1500/M5。原始银行乘数[1,1]，C3750+15000=18750、资本20/80，目标5500/5750USDT；不缩放NAV或数量、不归一化、不转账、不再平衡、不跨保证金。与已完成相同金额H.02/age48结果只读对比，不按结果改选。

All component signals are read-only actually completed rules:BTC L29H.03E.005,V10cap.0275,strictpositiveROC5>.0025;ETH L5contrarianH.02,E.0075,finiteEWMS16beta15/17,D3K.0075,V6cap.05625,M4/5/6,age1..60h,R.0075,VW9. No new native execution or signal fitting.

原始银行乘数[1,1]不归一化，C3750+15000=18750，资本20/80；本轮目标BTC1500或1750+ETH4000=5500或5750。每个原生组件均已按实际金额计算过LOT数量、非线性成交量冲击、费用、资金费及保证金，直接复用完整净值；父组合对齐共同时间轴相加美元NAV，无新增父订单、转账、再平衡或跨保证金，不线性缩放NAV。

391日为反复使用的开发历史2025-10-19 00:01→2026-11-14 00:01，不能称未触碰最终测试。无拟合标签，实际33闭合上下文日、embargo0；13个完整30日折+1日尾段，近期40日8×5、扩展21日5/5/5/6。折间继承现金/q，全期终点平仓计成本；整体回撤从连续完整NAV计算。

每边手续费5bp、半价差1bp、滑点2bp、0.5×过去20日样本logvol×sqrt(实际订单额/过去20日quoteADV)冲击；不利tick、LOT/最低金额、参与率≤.001。执行成本及实际资金费支出按1/2/3倍，收入不放大。线性永续无现货借币；1倍入场抵押及小时不利价1%维持保证金代理。对比等目标金额的实际持有组合和零息现金。缺L2/TCA、完整tiers、tick清算与容量实证。

|范围|BTC目标USDT|ETH成熟M|状态|净收益1/2/3倍%|整体DD3%|Sharpe3|Calmar3|正30日折1倍|近40日正5日折1/2/3|
|---|---|---|---|---|---|---|---|---|---|
|parent|1500|4|passed|11.052304 / 10.382940 / 9.713733|1.534455|2.303143|5.891008|12/13|6/6/6（各/8）|
|parent|1500|5|passed|10.074460 / 9.446577 / 8.818851|1.534455|2.206086|5.349794|12/13|6/6/6（各/8）|
|parent|1500|6|passed|10.781975 / 10.108794 / 9.435771|1.534455|2.224055|5.722931|12/13|6/6/6（各/8）|
|parent|1750|4|passed|12.030701 / 11.293292 / 10.556054|1.820303|2.267057|5.395126|12/13|6/6/6（各/8）|
|parent|1750|5|passed|11.052857 / 10.356929 / 9.661172|1.820303|2.176365|4.939133|12/13|6/6/6（各/8）|
|parent|1750|6|passed|11.760372 / 11.019146 / 10.278092|1.820303|2.196570|5.253515|12/13|6/6/6（各/8）|

事前失败判据：全期、近期和扩展各成本为正；1倍≥10/13正月；近期各成本≥6/8正5日折；扩展各成本≥3/4正折；DD3≤25%；邻域正及近期合格均≥60%；≥4次底层平仓；1倍毛损益加资金费/执行成本≥2.5；无拒单/负抵押/保证金代理违规；终点flat。

parent_BTCN1500_ETHlongonlyH200M4Age60h_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1500_ETHlongonlyH200M5Age60h_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1500_ETHlongonlyH200M6Age60h_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1750_ETHlongonlyH200M4Age60h_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1750_ETHlongonlyH200M5Age60h_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1750_ETHlongonlyH200M6Age60h_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。

相同M和本金，对旧BTC1000中心四指标严格改善父组合0/6。实际损益、资金费和执行成本差见sizing_effect_decomposition.json；全部变体/成本/逐折及连续每日净值见exports/。
完整三成本路径共6种；旧路径重复按NAV_alias_inventory保留披露，不能把相关路径算独立alpha。正Sharpe比例={"parent": {"1": 1.0, "2": 1.0, "3": 1.0}}；相邻敏感性边12，启发式警示3条，边界表现仅诊断，不扩网格或改选。
BTC金额轴为1000/1500/1750，间距不均；邻域按事前索引半径1定义。这是有限局部诊断，不代表完整响应面或参数显著性。Sharpe变化警示保持披露，未据此扩网格。

本轮四账户各续接120闭合分钟；原日决策数{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、成交数{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、实际资金费记录{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}，按各自现金/数量/费用和完整NAV核对。四账户的Nov21原日决策及三永续实际00:00:00.002资金费均已在此前完成，本轮不重复；SMA完整73日真实SPOT背景只读，按原Float估值延续现金与数量，不运行日决策或新增成交。三永续资金费各恰好一次，四原账户日决策均已完成。下一SMA/candidate['2026-11-21T02:30:00Z', '2026-11-21T04:30:00Z']、L4/FEWM['2026-11-21T04:10:00Z', '2026-11-21T06:10:00Z']只续估值并新鲜查询实际特殊资金费，下一原日决策Nov22_00:01。保留各自现金/q/desired/成本，不重置、不强制平仓、不采用研究配置。

原SMA三倍成本累计-7.468958%，仍为延迟shadow；原10bp与Float核算不变，未采用研究规则，不冒充十策略实盘报价模拟。所有账户尚未达到180日/六折资格。
监控成功=True，展示11430项，旧11424行完整字典保持。实际GET20，传输失败0；工程/读取失败原回执与恢复见read_failures.json。

实际复现命令（已完成模型和账户窗口不得重复计算）：

```sh
cd /home/desktop/Documents/Codex/EquiTide
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T185301Z/commands.py prepare # actual native phase prepare exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T185301Z/commands.py freeze # actual native phase freeze exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T185301Z/commands.py units # actual native phase units exit=1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T185301Z/commands.py units_retry1 # actual native phase units_retry1 exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T185301Z/commands.py bind # actual native phase bind exit=1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T185301Z/commands.py bind_retry1 # actual native phase bind_retry1 exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T185301Z/commands.py reserve_0 # actual native phase reserve_0 exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T185301Z/commands.py evaluate # actual native phase evaluate exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T185301Z/commands.py audit # actual native phase audit exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T185301Z/commands.py exports # actual native phase exports exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T185301Z/commands.py finish_0 # actual native phase finish_0 exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T185301Z/commands.py research_check # actual native phase research_check exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T185301Z/commands.py l4h02 # actual native phase l4h02 exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T185301Z/commands.py fewm # actual native phase fewm exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T185301Z/commands.py candidate # actual native phase candidate exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T185301Z/commands.py forward # actual native phase forward exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T185301Z/commands.py accounts_check # actual native phase accounts_check exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T185301Z/commands.py journal # actual native phase journal exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T185301Z/commands.py sources_check # actual native phase sources_check exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T185301Z/commands.py gates # actual native phase gates exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T185301Z/commands.py feed # actual native phase feed exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T185301Z/commands.py midnight_prepare # actual native phase midnight_prepare exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T185301Z/commands.py collect # actual native phase collect exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T185301Z/commands.py final_checks # actual native phase final_checks exit=0
```

官方来源和访问UTC见primary_source_access.json：[Binance市场数据文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)。正收益回测不代表稳定实盘盈利。

Nov21跨日上轮已完成：本轮四原账户仅续接估值，日决策均0次；既有73日真实SPOT上下文只读，保留原Float/10bp规则。三永续资金费唯一计数均6，四原账户Nov21日决策均已完成。首捕获UTC=2026-11-21T13:20:15.157839Z保持。下一SMA/candidate02:30→04:30、L4/FEWM04:10→06:10仅估值并新鲜查询实际特殊资金费；下一原日决策为Nov22_00:01，不提前入账。

Nov20_16三永续此前均已各记一次，本轮各0条；三永续唯一计数均6。首捕获UTC=2026-11-21T05:15:47.350340Z及原始毫秒/mark/rate保持。下一SMA/candidateNov21 02:30→04:30、L4/FEWM04:10→06:10（四原账户均已处理原Nov21日决策/资金费），须新鲜查询实际事件，不重复已记16，不提前记账。

与同金额、同M、H.02且年龄48小时的已完成结果比较：
BTC N1500/M4：收益差0.000000pp、整体DD差0.000000pp、Sharpe差0.000000、Calmar差0.000000；完整NAV同路径=True。
BTC N1500/M5：收益差0.000000pp、整体DD差0.000000pp、Sharpe差0.000000、Calmar差0.000000；完整NAV同路径=True。
BTC N1500/M6：收益差0.000000pp、整体DD差0.000000pp、Sharpe差0.000000、Calmar差0.000000；完整NAV同路径=True。
BTC N1750/M4：收益差0.000000pp、整体DD差0.000000pp、Sharpe差0.000000、Calmar差0.000000；完整NAV同路径=True。
BTC N1750/M5：收益差0.000000pp、整体DD差0.000000pp、Sharpe差0.000000、Calmar差0.000000；完整NAV同路径=True。
BTC N1750/M6：收益差0.000000pp、整体DD差0.000000pp、Sharpe差0.000000、Calmar差0.000000；完整NAV同路径=True。
全部18个逐成本比较见exports/previous_H002_comparisons.csv；仅比较已完成报告，不重跑旧组件或旧组合。

本轮六个新定义的18条逐成本完整NAV均与同金额age48旧结果完全相同；未产生独立alpha或策略提升，不替换已有候选及冻结账户。NAV_alias_inventory仅比较本轮选定的16个只读源，previous_H_comparison和age60_incremental_evidence另给出与age48相同金额的跨批次精确同路径证据。

同路径原因核验：对比3519条旧组件已保存决策，M4/5/6选中资金费集合、median、方向均相同；最大选中年龄分别32/40/48小时，48小时上限在本样本已足够，60小时未增加选中历史。仅为实际样本证据，不断言未来普遍等价。见age60_selected_history_identity.json。

本轮只读复核命令（不得重跑已完成金融模型或账户窗口）：

```sh
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T185301Z/bootstrap.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T185301Z/component_reuse_review.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T185301Z/funding_availability_review.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T185301Z/compare_previous_H.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T185301Z/review_economic_identity.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T185301Z/complete_midnight_handoff.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T185301Z/review_next_handoff.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T185301Z/final_notes.py
```
