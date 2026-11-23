# 20261123T032658Z BTC实际入场金额与ETH趋势斜率门槛组合验证

事前固定BTC实际原生目标N1000旧/1125/1375 × ETH K.00625/.0075旧/.00875。ETH固定S16、H=.02、V6cap.05625、M4、预算VW9/R=.0075、最大年龄36小时，趋势门槛按K轴变化；四个新被动父组合分别reserve、计算一次及finish，十个原生银行和八个旧父/持有对照只读；历史通过4/4。预设N1125/K.00625，不按结果改选。

完整读取41240事件/20481ID和516份结论；初始16项实际结果缺口0。规范研究定义11949→11953，不能将相关路径和历史选择视为独立试验。

固定BTC原生目标1000旧/1125/1375 × ETH有限EWM趋势斜率门槛K.00625/.0075旧/.00875，检验趋势确认强度变化与中等BTC银行的互补。ETH固定C15000/N4000、ROC L5/H.02/E.0075、有限EWM S16 beta15/17/D3、入场波动率V6cap.05625、成熟M4/年龄1..36h、预算VW9/R.0075；BTC固定C3750、L29/H.03/E.005、V10cap.0275、strictpositiveROC5>.0025。四个新被动父组合，十个实际旧原生银行与八个旧父/持有只读；预设1125/K.00625，不按结果改选。原银行乘数[1,1]，本金3750+15000=18750，资本20/80，初始目标5125/5375；完整共同轴相加美元NAV，保留原LOT/q/手续费/非线性冲击/资金费/保证金，无归一化、父订单、转账、再平衡或跨保证金。

All component signals are read-only actually completed rules:BTC L29H.03E.005,V10cap.0275,strictpositiveROC5>.0025;ETH L5contrarianH.02,E.0075,finiteEWMS16beta15/17,D3K.00625/.0075old/.00875,E.0075,V6cap.05625,M4,age1..36h,R.0075,VW9. No new native execution or signal fitting.

原始银行乘数[1,1]不归一化，C3750+15000=18750，资本20/80；本轮目标BTC1125或1375+ETH4000=5125或5375。每个原生组件均已按实际金额计算过LOT数量、非线性成交量冲击、费用、资金费及保证金，直接复用完整净值；父组合对齐共同时间轴相加美元NAV，无新增父订单、转账、再平衡或跨保证金，不线性缩放NAV。

391日为反复使用的开发历史2025-10-19 00:01→2026-11-14 00:01，不能称未触碰最终测试。无拟合标签，实际33闭合上下文日、embargo0；13个完整30日折+1日尾段，近期40日8×5、扩展21日5/5/5/6。折间继承现金/q，全期终点平仓计成本；整体回撤从连续完整NAV计算。

每边手续费5bp、半价差1bp、滑点2bp、0.5×过去20日样本logvol×sqrt(实际订单额/过去20日quoteADV)冲击；不利tick、LOT/最低金额、参与率≤.001。执行成本及实际资金费支出按1/2/3倍，收入不放大。线性永续无现货借币；1倍入场抵押及小时不利价1%维持保证金代理。对比等目标金额的实际持有组合和零息现金。缺L2/TCA、完整tiers、tick清算与容量实证。

|范围|BTC目标USDT|ETH趋势斜率门槛K（比例）|状态|净收益1/2/3倍%|整体DD3%|Sharpe3|Calmar3|正30日折1倍|近40日正5日折1/2/3|
|---|---|---|---|---|---|---|---|---|---|
|parent|1125|0.00625|passed|8.620865 / 7.992768 / 7.364898|3.868757|1.644961|1.772856|11/13|6/6/6（各/8）|
|parent|1125|0.00875|passed|9.757824 / 9.181560 / 8.605456|1.365560|2.345147|5.866396|12/13|6/6/6（各/8）|
|parent|1375|0.00625|passed|9.486943 / 8.794400 / 8.102103|4.090831|1.678545|1.844010|11/13|6/6/6（各/8）|
|parent|1375|0.00875|passed|10.623902 / 9.983192 / 9.342661|1.437336|2.311040|6.049511|12/13|6/6/6（各/8）|

事前失败判据：全期、近期和扩展各成本为正；1倍≥10/13正月；近期各成本≥6/8正5日折；扩展各成本≥3/4正折；DD3≤25%；邻域正及近期合格均≥60%；≥4次底层平仓；1倍毛损益加资金费/执行成本≥2.5；无拒单/负抵押/保证金代理违规；终点flat。

parent_BTCN1125_ETHlongonlyL5H200M4D3Age36hSlopeK0.00625E0075V6Cap05625_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1125_ETHlongonlyL5H200M4D3Age36hSlopeK0.00875E0075V6Cap05625_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1375_ETHlongonlyL5H200M4D3Age36hSlopeK0.00625E0075V6Cap05625_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1375_ETHlongonlyL5H200M4D3Age36hSlopeK0.00875E0075V6Cap05625_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。

相同ETH趋势斜率门槛和本金，对旧BTC1000中心四指标严格改善父组合0/4。实际损益、资金费和执行成本差见sizing_effect_decomposition.json；全部变体/成本/逐折及连续每日净值见exports/。
完整三成本路径共4种；旧路径重复按NAV_alias_inventory保留披露，不能把相关路径算独立alpha。正Sharpe比例={"parent": {"1": 1.0, "2": 1.0, "3": 1.0}}；相邻敏感性边12，启发式警示3条，边界表现仅诊断，不扩网格或改选。
BTC金额轴为1000/1125/1375，间距不均；邻域按事前索引半径1定义。这是有限局部诊断，不代表完整响应面或参数显著性。Sharpe变化警示保持披露，未据此扩网格。

本轮四账户续接120闭合分钟；原日决策{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、资金费{'SMA': 0, 'candidate': 6, 'l4h02': 0, 'fewm': 0}。已知Nov21_08三永续此前均已记账，本轮不重复；其他实际事件依freshGET与各自窗口处理。下一SMA/candidate['2026-11-22T08:30:00Z', '2026-11-22T10:30:00Z']、L4/FEWM['2026-11-22T10:10:00Z', '2026-11-22T12:10:00Z']须freshGET、去重并先reserve，不提前记账、不重置、不强平、不采用研究规则；SMA74日背景/原日决策完整核验。

原SMA三倍成本累计-7.468958%，仍为延迟shadow；原10bp与Float核算不变，未采用研究规则，不冒充十策略实盘报价模拟。所有账户尚未达到180日/六折资格。
监控成功=True，展示11512项，旧11508行完整字典保持。实际GET23，传输失败3；工程/读取失败原回执与恢复见read_failures.json。

实际复现命令（已完成模型和账户窗口不得重复计算）：

```sh
cd /home/desktop/Documents/Codex/EquiTide
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T032658Z/commands.py prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T032658Z/commands.py freeze
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T032658Z/commands.py units
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T032658Z/commands.py bind
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T032658Z/commands.py reserve_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T032658Z/commands.py evaluate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T032658Z/commands.py audit
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T032658Z/commands.py exports
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T032658Z/commands.py finish_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T032658Z/commands.py research_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T032658Z/commands.py l4h02
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T032658Z/commands.py fewm
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T032658Z/commands.py candidate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T032658Z/commands.py forward
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T032658Z/commands.py accounts_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T032658Z/commands.py journal
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T032658Z/commands.py sources_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T032658Z/commands.py gates
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T032658Z/commands.py feed
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T032658Z/commands.py midnight_prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T032658Z/commands.py collect
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T032658Z/commands.py final_checks
```

官方来源、访问UTC和版本内容SHA见primary_source_access.json。本轮衍生品文档页面两次超时，已改读[Binance官方只读接口源代码](https://raw.githubusercontent.com/binance/binance-futures-connector-python/main/binance/um_futures/market.py)，并保留原始页面失败回执；行情及资金费以实际公共GET字节和哈希为准。正收益回测不代表稳定实盘盈利。

与同金额、H.02、年龄36小时、S16、成熟M4、预算VW9且趋势斜率门槛K.0075、波动率V6、ROC L5、退出E.0075的已完成结果比较：
BTC N1125/K0.00625：收益差-1.240558pp、整体DD差2.503198pp、Sharpe差-0.700186、Calmar差-4.093540；完整NAV同路径=False。
BTC N1125/K0.00875：收益差0.000000pp、整体DD差0.000000pp、Sharpe差0.000000、Calmar差0.000000；完整NAV同路径=True。
BTC N1375/K0.00625：收益差-1.240558pp、整体DD差2.653495pp、Sharpe差-0.632495、Calmar差-4.205500；完整NAV同路径=False。
BTC N1375/K0.00875：收益差0.000000pp、整体DD差0.000000pp、Sharpe差0.000000、Calmar差0.000000；完整NAV同路径=True。
全部12个逐成本比较见exports/previous_K0075_comparisons.csv；仅比较已完成报告，不重跑旧组件或旧组合。

与同金额K.0075的12个逐成本比较：四指标同时改善0项，旧K.0075支配6项，完整NAV同路径6项；全成本同旧K.0075路径的新图2个。见comparison_scope_review.json。历史门槛状态与比较优劣分别保留；维持事前1125/K.00625，不据结果换候选，不修改原冻结账户。相关配置和重复历史不构成独立前向或实盘盈利证据。

本轮原冻结账户各续接120分钟，无原日决策及成交；candidate按自身持仓处理实际08:00:00.003资金费6条；L4/FEWM已在各自上个窗口处理，当前不重复；SMA无永续资金费。Nov22日决策及三个永续实际00:00:00.001资金费均已按自身窗口完成，只读保留各6唯一键，不重复。SMA full74真实现货背景只读、现金/数量/desired/成本不重置。下一四窗口均无日决策；各永续账户资金费以只读实际查询的独立窗口待处理字段为准，未提前入账。下一原日决策UTC Nov23_00:01。

已知Nov21_08:00:00.003三永续此前均已记账一次，本轮不重复；当前资金费记录={"SMA": 0, "candidate": 6, "l4h02": 0, "fewm": 0}。08全链唯一计数各6，首次捕获UTC和原始来源SHA保持；下一窗口继续freshGET与按账户去重，不提前记账。

旧Nov21_16事件三个永续各6个唯一键，本轮旧事件0新增；本轮其他资金费与原日决策成交按自身q/mark/rate/成本逐项重核，十八本现金完整对账。详见actual16_nov21_reconciliation.json，未重跑模型或账户窗口。

本轮只读复核命令（不得重跑已完成金融模型或账户窗口）：

```sh
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T032658Z/component_reuse_review.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T032658Z/funding_availability_review.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T032658Z/compare_previous_H.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T032658Z/review_economic_identity.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T032658Z/review_sensitivity_axes.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T032658Z/review_reservation_metadata.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T032658Z/review_trend_strength_economics.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T032658Z/reconcile_actual08.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T032658Z/reconcile_actual16.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T032658Z/complete_midnight_handoff.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T032658Z/review_next_handoff.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T032658Z/review_next_settlement_split.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T032658Z/final_notes.py
```

实际机制复核：趋势门槛K.00625/.0075/.00875的ETH原银行三倍成本执行16/14/14次，完整平仓8/7/7次。较低K多一次完整交易，期末NAV比旧K.0075少232.604608 USDT，来自实际毛价格损益、资金费与执行成本差；全部12个同BTC金额逐成本差与ETH原银行NAV差核对。较高K与旧中心完整三成本路径相同。见trend_strength_economic_review.json。

三条Sharpe启发式警示来自趋势门槛.00625到.0075步长在三个BTC金额下的相关比较，不是三个独立新样本。新图历史门槛通过，但未改善旧中心；维持预设1125/K.00625，不升级新候选、不按结果扩网格。正收益开发回测不代表独立前向或稳定实盘盈利。

真实08:00:00.003结算当前已按自身窗口在三个原永续账户完成各6唯一键；本轮仅candidate新增6条，L4/FEWM不重复。首次捕获UTC及源SHA保持，现金流按自身q/实际mark/rate核算，收入不放大、支出按1/2/3压力。下一窗口待处理记录={"SMA": 0, "candidate": 0, "l4h02": 0, "fewm": 0}，未提前入账；下轮仍须刷新实际来源并按自身窗口reserve。
