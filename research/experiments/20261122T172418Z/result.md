# 20261122T172418Z BTC实际入场金额与ETH趋势滞后组合验证

事前固定BTC实际原生目标N1000旧/1125/1375 × ETH D1/2/4。ETH固定S16、H=.02、M4、预算VW9/R=.0075、最大年龄36小时、趋势斜率门槛=.0075；六个新被动父组合分别reserve、计算一次及finish，十个原生银行和六个旧父/持有对照只读；历史通过6/6。预设N1125/D2，不按结果改选。

完整读取41008事件/20365ID和512份结论；初始16项实际结果缺口0。规范研究定义11931→11937，不能将相关路径和历史选择视为独立试验。

事前固定BTC实际目标N1000旧/1125/1375 × ETH趋势斜率滞后D1/2/4日，考察中等BTC银行与ETH趋势确认时标的互补。固定ETH C15000/N4000、L5/H.02/E.0075、有限EWM S16 beta15/17、斜率门槛.0075、V6cap.05625、成熟M4/年龄1..36h、资金费预算VW9/R.0075。六个新被动组合，十个旧原生银行和六个旧父/持有只读，另绑定同BTC金额D3两份旧报告。预设1125/D2，不按结果改选。原银行乘数[1,1]，C3750+15000=18750、20/80，初始目标5125/5375；完整共同轴美元NAV相加，保留原LOT/q/手续费/非线性冲击/实际资金费/保证金，不缩放、不归一化，无父订单/转账/再平衡/跨保证金。

All component signals are read-only actually completed rules:BTC L29H.03E.005,V10cap.0275,strictpositiveROC5>.0025;ETH L5contrarianH.02,E.0075,finiteEWMS16beta15/17,D1/2/4K.0075,V6cap.05625,M4,age1..36h,R.0075,VW9. No new native execution or signal fitting.

原始银行乘数[1,1]不归一化，C3750+15000=18750，资本20/80；本轮目标BTC1125或1375+ETH4000=5125或5375。每个原生组件均已按实际金额计算过LOT数量、非线性成交量冲击、费用、资金费及保证金，直接复用完整净值；父组合对齐共同时间轴相加美元NAV，无新增父订单、转账、再平衡或跨保证金，不线性缩放NAV。

391日为反复使用的开发历史2025-10-19 00:01→2026-11-14 00:01，不能称未触碰最终测试。无拟合标签，实际33闭合上下文日、embargo0；13个完整30日折+1日尾段，近期40日8×5、扩展21日5/5/5/6。折间继承现金/q，全期终点平仓计成本；整体回撤从连续完整NAV计算。

每边手续费5bp、半价差1bp、滑点2bp、0.5×过去20日样本logvol×sqrt(实际订单额/过去20日quoteADV)冲击；不利tick、LOT/最低金额、参与率≤.001。执行成本及实际资金费支出按1/2/3倍，收入不放大。线性永续无现货借币；1倍入场抵押及小时不利价1%维持保证金代理。对比等目标金额的实际持有组合和零息现金。缺L2/TCA、完整tiers、tick清算与容量实证。

|范围|BTC目标USDT|ETH趋势滞后D（日）|状态|净收益1/2/3倍%|整体DD3%|Sharpe3|Calmar3|正30日折1倍|近40日正5日折1/2/3|
|---|---|---|---|---|---|---|---|---|---|
|parent|1125|1|passed|4.114858 / 3.839413 / 3.563960|1.337279|1.542762|2.484954|10/13|6/6/6（各/8）|
|parent|1125|2|passed|7.648644 / 7.196666 / 6.744847|1.198160|2.086422|5.243497|12/13|6/6/6（各/8）|
|parent|1125|4|passed|9.482939 / 8.814239 / 8.145657|3.868757|1.783377|1.960315|11/13|6/6/6（各/8）|
|parent|1375|1|passed|4.980936 / 4.641045 / 4.301165|1.664786|1.518252|2.408417|10/13|6/6/6（各/8）|
|parent|1375|2|passed|8.514722 / 7.998298 / 7.482052|1.424817|2.068196|4.890169|12/13|6/6/6（各/8）|
|parent|1375|4|passed|10.349017 / 9.615871 / 8.882863|4.090831|1.808804|2.021212|11/13|6/6/6（各/8）|

事前失败判据：全期、近期和扩展各成本为正；1倍≥10/13正月；近期各成本≥6/8正5日折；扩展各成本≥3/4正折；DD3≤25%；邻域正及近期合格均≥60%；≥4次底层平仓；1倍毛损益加资金费/执行成本≥2.5；无拒单/负抵押/保证金代理违规；终点flat。

parent_BTCN1125_ETHlongonlyH200M4D1Age36hSlopeK0075_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1125_ETHlongonlyH200M4D2Age36hSlopeK0075_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1125_ETHlongonlyH200M4D4Age36hSlopeK0075_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1375_ETHlongonlyH200M4D1Age36hSlopeK0075_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1375_ETHlongonlyH200M4D2Age36hSlopeK0075_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1375_ETHlongonlyH200M4D4Age36hSlopeK0075_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。

相同趋势滞后和本金，对旧BTC1000中心四指标严格改善父组合0/6。实际损益、资金费和执行成本差见sizing_effect_decomposition.json；全部变体/成本/逐折及连续每日净值见exports/。
完整三成本路径共6种；旧路径重复按NAV_alias_inventory保留披露，不能把相关路径算独立alpha。正Sharpe比例={"parent": {"1": 1.0, "2": 1.0, "3": 1.0}}；相邻敏感性边12，启发式警示3条，边界表现仅诊断，不扩网格或改选。
BTC金额轴为1000/1125/1375，间距不均；邻域按事前索引半径1定义。这是有限局部诊断，不代表完整响应面或参数显著性。Sharpe变化警示保持披露，未据此扩网格。

本轮四账户续接120闭合分钟；原日决策{'SMA': 1, 'candidate': 1, 'l4h02': 0, 'fewm': 0}、成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、资金费{'SMA': 0, 'candidate': 6, 'l4h02': 0, 'fewm': 0}。已知Nov21_08三永续此前均已记账，本轮不重复；其他实际事件依freshGET与各自窗口处理。下一SMA/candidate['2026-11-22T00:30:00Z', '2026-11-22T02:30:00Z']、L4/FEWM['2026-11-22T02:10:00Z', '2026-11-22T04:10:00Z']须freshGET、去重并先reserve，不提前记账、不重置、不强平、不采用研究规则；SMA74日背景/原日决策完整核验。

原SMA三倍成本累计-7.468958%，仍为延迟shadow；原10bp与Float核算不变，未采用研究规则，不冒充十策略实盘报价模拟。所有账户尚未达到180日/六折资格。
监控成功=True，展示11496项，旧11490行完整字典保持。实际GET27，传输失败5；工程/读取失败原回执与恢复见read_failures.json。

实际复现命令（已完成模型和账户窗口不得重复计算）：

```sh
cd /home/desktop/Documents/Codex/EquiTide
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T172418Z/commands.py prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T172418Z/commands.py prepare_retry1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T172418Z/commands.py prepare_retry2
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T172418Z/commands.py freeze
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T172418Z/commands.py units
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T172418Z/commands.py bind
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T172418Z/commands.py reserve_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T172418Z/commands.py evaluate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T172418Z/commands.py audit
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T172418Z/commands.py exports
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T172418Z/commands.py finish_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T172418Z/commands.py research_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T172418Z/commands.py l4h02
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T172418Z/commands.py fewm
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T172418Z/commands.py candidate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T172418Z/commands.py forward
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T172418Z/commands.py accounts_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T172418Z/commands.py journal
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T172418Z/commands.py sources_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T172418Z/commands.py gates
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T172418Z/commands.py feed
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T172418Z/commands.py midnight_prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T172418Z/commands.py collect
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T172418Z/commands.py final_checks
```

官方来源和访问UTC见primary_source_access.json：[Binance市场数据文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)。正收益回测不代表稳定实盘盈利。

与同金额、H.02、年龄36小时、S16、成熟M4、预算VW9且滞后D3的已完成结果比较：
BTC N1125/D1：收益差-5.041496pp、整体DD差-0.028281pp、Sharpe差-0.802386、Calmar差-3.381443；完整NAV同路径=False。
BTC N1125/D2：收益差-1.860609pp、整体DD差-0.167400pp、Sharpe差-0.258725、Calmar差-0.622899；完整NAV同路径=False。
BTC N1125/D4：收益差-0.459798pp、整体DD差2.503198pp、Sharpe差-0.561770、Calmar差-3.906082；完整NAV同路径=False。
BTC N1375/D1：收益差-5.041496pp、整体DD差0.227450pp、Sharpe差-0.792788、Calmar差-3.641094；完整NAV同路径=False。
BTC N1375/D2：收益差-1.860609pp、整体DD差-0.012519pp、Sharpe差-0.242844、Calmar差-1.159342；完整NAV同路径=False。
BTC N1375/D4：收益差-0.459798pp、整体DD差2.653495pp、Sharpe差-0.502236、Calmar差-4.028299；完整NAV同路径=False。
全部18个逐成本比较见exports/previous_D3_comparisons.csv；仅比较已完成报告，不重跑旧组件或旧组合。

与同金额D3的18个逐成本比较：四指标同时改善0项，旧D3支配9项，完整NAV同路径0项；全成本同旧D3路径的新图0个。见comparison_scope_review.json。历史门槛状态与比较优劣分别保留；维持事前1125/D2，不据结果换候选，不修改原冻结账户。相关配置和重复历史不构成独立前向或实盘盈利证据。

本轮SMA/candidate按原冻结规则处理Nov22日决策，candidate实际00:00:00.001资金费按自身q/成本记账；L4/FEWM不重复先前日决策或资金费。下一四窗口均mark only，SMA保留完整真实full74，下一原日决策UTC Nov23_00:01。原账本、冻结规则和本金保持，无研究参数采纳。

原SMA日内核身份说明的planned_terminal_utc标签误写为2027-03-31 00:00 UTC。实际冻结原计划、续接执行计划均为2027-03-31 00:01 UTC，SHA和原执行证据保持不变。身份说明的已绑定原字节保留，本说明仅纠正元数据标签；未修改原冻结规则、账户、终止时点或重新计算结果。

已知Nov21_08:00:00.003三永续此前均已记账一次，本轮不重复；当前资金费记录={"SMA": 0, "candidate": 6, "l4h02": 0, "fewm": 0}。08全链唯一计数各6，首次捕获UTC和原始来源SHA保持；下一窗口继续freshGET与按账户去重，不提前记账。

旧Nov21_16事件三个永续各6个唯一键，本轮旧事件0新增；本轮其他资金费与原日决策成交按自身q/mark/rate/成本逐项重核，十八本现金完整对账。详见actual16_nov21_reconciliation.json，未重跑模型或账户窗口。

本轮只读复核命令（不得重跑已完成金融模型或账户窗口）：

```sh
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T172418Z/component_reuse_review.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T172418Z/funding_availability_review.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T172418Z/compare_previous_H.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T172418Z/review_economic_identity.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T172418Z/review_SMA_terminal_label.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T172418Z/reconcile_actual08.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T172418Z/reconcile_actual16.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T172418Z/complete_midnight_handoff.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T172418Z/review_next_handoff.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T172418Z/final_notes.py
```
