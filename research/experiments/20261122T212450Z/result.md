# 20261122T212450Z BTC实际入场金额与ETH快速ROC回看期组合验证

事前固定BTC实际原生目标N1000旧/1125/1375 × ETH L4/5旧/6。ETH固定S16、H=.02、M4、预算VW9/R=.0075、最大年龄36小时、趋势斜率门槛=.0075；四个新被动父组合分别reserve、计算一次及finish，十个原生银行和八个旧父/持有对照只读；历史通过4/4。预设N1125/L4，不按结果改选。

完整读取41116事件/20419ID和514份结论；初始16项实际结果缺口0。规范研究定义11941→11945，不能将相关路径和历史选择视为独立试验。

固定BTC原生目标1000旧/1125/1375 × ETH快速ROC回看L4/5旧/6日，检验入场与退出信号的回看期变化及其与中等BTC银行的互补。ETH固定C15000/N4000、H.02/E.0075、有限EWM S16 beta15/17/D3、斜率门槛.0075、V6cap.05625、成熟M4/年龄1..36h、预算VW9/R.0075；BTC固定C3750、L29/H.03/E.005、V10cap.0275、strictpositiveROC5>.0025。四个新被动父组合，十个实际旧原生银行与八个旧父/持有只读；预设1125/L4，不按结果改选。原银行乘数[1,1]，本金3750+15000=18750、20/80，目标5125/5375；全共同轴相加美元NAV，保留原LOT/q/手续费/非线性冲击/实际资金费/保证金，无归一化、父订单、转账、再平衡或跨保证金。

All component signals are read-only actually completed rules:BTC L29H.03E.005,V10cap.0275,strictpositiveROC5>.0025;ETH L4/5/6contrarianH.02,E.0075,finiteEWMS16beta15/17,D3K.0075,E.0075,V6cap.05625,M4,age1..36h,R.0075,VW9. No new native execution or signal fitting.

原始银行乘数[1,1]不归一化，C3750+15000=18750，资本20/80；本轮目标BTC1125或1375+ETH4000=5125或5375。每个原生组件均已按实际金额计算过LOT数量、非线性成交量冲击、费用、资金费及保证金，直接复用完整净值；父组合对齐共同时间轴相加美元NAV，无新增父订单、转账、再平衡或跨保证金，不线性缩放NAV。

391日为反复使用的开发历史2025-10-19 00:01→2026-11-14 00:01，不能称未触碰最终测试。无拟合标签，实际33闭合上下文日、embargo0；13个完整30日折+1日尾段，近期40日8×5、扩展21日5/5/5/6。折间继承现金/q，全期终点平仓计成本；整体回撤从连续完整NAV计算。

每边手续费5bp、半价差1bp、滑点2bp、0.5×过去20日样本logvol×sqrt(实际订单额/过去20日quoteADV)冲击；不利tick、LOT/最低金额、参与率≤.001。执行成本及实际资金费支出按1/2/3倍，收入不放大。线性永续无现货借币；1倍入场抵押及小时不利价1%维持保证金代理。对比等目标金额的实际持有组合和零息现金。缺L2/TCA、完整tiers、tick清算与容量实证。

|范围|BTC目标USDT|ETH快速ROC回看期L（日）|状态|净收益1/2/3倍%|整体DD3%|Sharpe3|Calmar3|正30日折1倍|近40日正5日折1/2/3|
|---|---|---|---|---|---|---|---|---|---|
|parent|1125|4|passed|7.404403 / 6.720304 / 6.036004|4.463557|1.426210|1.259883|10/13|6/6/6（各/8）|
|parent|1125|6|passed|6.607276 / 6.121696 / 5.636114|1.337279|1.950688|3.927128|10/13|6/6/6（各/8）|
|parent|1375|4|passed|8.270481 / 7.521936 / 6.773210|4.782512|1.466205|1.319162|10/13|6/6/6（各/8）|
|parent|1375|6|passed|7.473354 / 6.923327 / 6.373319|1.664786|1.895719|3.566337|10/13|6/6/6（各/8）|

事前失败判据：全期、近期和扩展各成本为正；1倍≥10/13正月；近期各成本≥6/8正5日折；扩展各成本≥3/4正折；DD3≤25%；邻域正及近期合格均≥60%；≥4次底层平仓；1倍毛损益加资金费/执行成本≥2.5；无拒单/负抵押/保证金代理违规；终点flat。

parent_BTCN1125_ETHlongonlyL4H200M4D3Age36hSlopeK0075E0075_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1125_ETHlongonlyL6H200M4D3Age36hSlopeK0075E0075_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1375_ETHlongonlyL4H200M4D3Age36hSlopeK0075E0075_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1375_ETHlongonlyL6H200M4D3Age36hSlopeK0075E0075_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。

相同ETH回看期和本金，对旧BTC1000中心四指标严格改善父组合0/4。实际损益、资金费和执行成本差见sizing_effect_decomposition.json；全部变体/成本/逐折及连续每日净值见exports/。
完整三成本路径共4种；旧路径重复按NAV_alias_inventory保留披露，不能把相关路径算独立alpha。正Sharpe比例={"parent": {"1": 1.0, "2": 1.0, "3": 1.0}}；相邻敏感性边12，启发式警示3条，边界表现仅诊断，不扩网格或改选。
BTC金额轴为1000/1125/1375，间距不均；邻域按事前索引半径1定义。这是有限局部诊断，不代表完整响应面或参数显著性。Sharpe变化警示保持披露，未据此扩网格。

本轮四账户续接120闭合分钟；原日决策{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、资金费{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}。已知Nov21_08三永续此前均已记账，本轮不重复；其他实际事件依freshGET与各自窗口处理。下一SMA/candidate['2026-11-22T04:30:00Z', '2026-11-22T06:30:00Z']、L4/FEWM['2026-11-22T06:10:00Z', '2026-11-22T08:10:00Z']须freshGET、去重并先reserve，不提前记账、不重置、不强平、不采用研究规则；SMA74日背景/原日决策完整核验。

原SMA三倍成本累计-7.468958%，仍为延迟shadow；原10bp与Float核算不变，未采用研究规则，不冒充十策略实盘报价模拟。所有账户尚未达到180日/六折资格。
监控成功=True，展示11504项，旧11500行完整字典保持。实际GET21，传输失败1；工程/读取失败原回执与恢复见read_failures.json。

实际复现命令（已完成模型和账户窗口不得重复计算）：

```sh
cd /home/desktop/Documents/Codex/EquiTide
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T212450Z/commands.py prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T212450Z/commands.py freeze
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T212450Z/commands.py units
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T212450Z/commands.py bind
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T212450Z/commands.py reserve_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T212450Z/commands.py evaluate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T212450Z/commands.py audit
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T212450Z/commands.py exports
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T212450Z/commands.py finish_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T212450Z/commands.py research_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/.git/automation_proofs/20261122T212450Z_pipeline.py l4h02 fewm candidate forward accounts_check journal sources_check gates feed midnight_prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T212450Z/commands.py l4h02_retry1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T212450Z/commands.py fewm
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T212450Z/commands.py candidate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T212450Z/commands.py forward
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T212450Z/commands.py accounts_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T212450Z/commands.py journal
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T212450Z/commands.py sources_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T212450Z/commands.py gates
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T212450Z/commands.py feed
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T212450Z/commands.py midnight_prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T212450Z/commands.py collect
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T212450Z/commands.py final_checks
```

官方来源和访问UTC见primary_source_access.json：[Binance市场数据文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)。正收益回测不代表稳定实盘盈利。

与同金额、H.02、年龄36小时、S16、成熟M4、预算VW9且快速ROC回看L5、退出E.0075的已完成结果比较：
BTC N1125/L4：收益差-2.569451pp、整体DD差3.097997pp、Sharpe差-0.918937、Calmar差-4.606513；完整NAV同路径=False。
BTC N1125/L6：收益差-2.969342pp、整体DD差-0.028281pp、Sharpe差-0.394459、Calmar差-1.939268；完整NAV同路径=False。
BTC N1375/L4：收益差-2.569451pp、整体DD差3.345176pp、Sharpe差-0.844835、Calmar差-4.730348；完整NAV同路径=False。
BTC N1375/L6：收益差-2.969342pp、整体DD差0.227450pp、Sharpe差-0.415321、Calmar差-2.483173；完整NAV同路径=False。
全部12个逐成本比较见exports/previous_L5_comparisons.csv；仅比较已完成报告，不重跑旧组件或旧组合。

与同金额L5的12个逐成本比较：四指标同时改善0项，旧L5支配9项，完整NAV同路径0项；全成本同旧L5路径的新图0个。见comparison_scope_review.json。历史门槛状态与比较优劣分别保留；维持事前1125/L4，不据结果换候选，不修改原冻结账户。相关配置和重复历史不构成独立前向或实盘盈利证据。

下一原冻结账户窗口的历史真实结算留证：fundingTime毫秒=[1795334400003]，各自下一窗口待处理记录={"SMA": 0, "candidate": 0, "l4h02": 6, "fewm": 6}。首次捕获UTC=2026-11-22T21:50:17.299563Z及来源SHA保持；本轮未提前入账。下一轮须刷新实际来源、按自身窗口去重并先reserve，再以自身q/成本核算，不复用其他账户金额。详见next_preparation_contract.new_actual_settlement_handoff。

本轮四个原冻结账户仅续接120分钟mark，原日决策、资金费和成交各0；Nov22日决策及三个永续实际00:00:00.001资金费均已按自身窗口完成，只读保留各6唯一键，不重复。SMA full74真实现货背景只读、现金/数量/desired/成本不重置。下一四窗口均无日决策；L4/FEWM资金费以只读实际查询的独立窗口待处理字段为准，未提前入账。下一原日决策UTC Nov23_00:01。

已知Nov21_08:00:00.003三永续此前均已记账一次，本轮不重复；当前资金费记录={"SMA": 0, "candidate": 0, "l4h02": 0, "fewm": 0}。08全链唯一计数各6，首次捕获UTC和原始来源SHA保持；下一窗口继续freshGET与按账户去重，不提前记账。

旧Nov21_16事件三个永续各6个唯一键，本轮旧事件0新增；本轮其他资金费与原日决策成交按自身q/mark/rate/成本逐项重核，十八本现金完整对账。详见actual16_nov21_reconciliation.json，未重跑模型或账户窗口。

本轮只读复核命令（不得重跑已完成金融模型或账户窗口）：

```sh
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T212450Z/component_reuse_review.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T212450Z/funding_availability_review.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T212450Z/compare_previous_H.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T212450Z/review_economic_identity.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T212450Z/review_sensitivity_axes.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T212450Z/review_reservation_metadata.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T212450Z/review_interruption_resume.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T212450Z/review_lookback_economics.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T212450Z/reconcile_actual08.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T212450Z/reconcile_actual16.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T212450Z/complete_midnight_handoff.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T212450Z/review_next_handoff.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T212450Z/review_next_settlement_split.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T212450Z/final_notes.py
```

实际机制复核：ETH L4/L5/L6原银行三倍成本分别执行18/14/10次，完整平仓9/7/5次；1倍正30日折6/7/3（各/13）。L4增加周转及费用，L6减少费用同时错失更多毛价格损益。全部12个同BTC金额逐成本收益差均从实际ETH银行NAV差核对；组件旧状态不重分类。4个父组合通过历史门槛不代表ETH单腿稳健。详见lookback_economic_review.json。

三条敏感性启发式警示都来自ETH回看4到5日，在三个BTC金额下的相关表现，不是三份独立新样本。新L4/L6组合三倍成本比同金额旧L5收益分别低约2.569451/2.969342个百分点，均未改善收益、Sharpe与Calmar三项；不升级新候选，不修改冻结账户，不按结果扩网格。正收益开发回测不能称稳定实盘盈利。

本轮原L4观察器实际成功后，外层续接会话返回143；无已完成审计回执，终止来源无法确定。原观察器不重跑，只读审计和登记投影恢复成功，保存状态及报告哈希不变。恢复准备后误调用不存在路径的127也保留为工程失败；两项均未重算金融模型或已完成账户窗口。

下一各自窗口实际资金费待处理记录（3成本合计）={"SMA": 0, "candidate": 0, "l4h02": 6, "fewm": 6}；无日决策不等于无资金费。只读保存首次实际毫秒/mark/rate/UTC，下轮仍须刷新来源、按自身窗口去重并reserve；当前未提前入账。详见next_settlement_split_review.json。
