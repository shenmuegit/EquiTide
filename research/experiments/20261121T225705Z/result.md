# 20261121T225705Z BTC实际入场金额与ETH趋势确认滞后组合验证

事前固定BTC实际原生目标N1000旧/1500/1750 × ETH D1/2/4。ETH固定H=.02、M4、最大年龄36小时、趋势斜率K=.0075；六个新被动父组合分别reserve、计算一次及finish，十个原生银行和六个旧父/持有对照只读；历史通过6/6。预设N1500/D2，不按结果改选。

完整读取40504事件/20113ID和503份结论；初始16项实际结果缺口0。规范研究定义11877→11883，不能将相关路径和历史选择视为独立试验。

改变ETH有限EWM趋势斜率比较滞后D为已实际执行的1/2/4天，可能改变与较大BTC趋势银行的风险互补。事前固定BTC实际目标N1000旧/1500/1750 × ETH滞后D1/2/4；ETH L5/H.02/E.0075、S16/斜率K.0075、V6cap.05625、成熟M4、年龄1..36h、R.0075/VW9及C15000/N4000固定。六个新被动父组合，十个原生银行和六个旧父/持有对照只读；另预先绑定两笔同BTC金额、同M4/age36的已完成D3父组合仅作报告比较。预设BTC1500/D2，不据结果改选或扩网格。原始银行乘数[1,1]，C3750+15000=18750、资本20/80、初始目标5500/5750，不缩放数量或NAV、不归一化、不转账、不再平衡、不跨保证金。

All component signals are read-only actually completed rules:BTC L29H.03E.005,V10cap.0275,strictpositiveROC5>.0025;ETH L5contrarianH.02,E.0075,finiteEWMS16beta15/17,D1/2/4K.0075,V6cap.05625,M4,age1..36h,R.0075,VW9. No new native execution or signal fitting.

原始银行乘数[1,1]不归一化，C3750+15000=18750，资本20/80；本轮目标BTC1500或1750+ETH4000=5500或5750。每个原生组件均已按实际金额计算过LOT数量、非线性成交量冲击、费用、资金费及保证金，直接复用完整净值；父组合对齐共同时间轴相加美元NAV，无新增父订单、转账、再平衡或跨保证金，不线性缩放NAV。

391日为反复使用的开发历史2025-10-19 00:01→2026-11-14 00:01，不能称未触碰最终测试。无拟合标签，实际33闭合上下文日、embargo0；13个完整30日折+1日尾段，近期40日8×5、扩展21日5/5/5/6。折间继承现金/q，全期终点平仓计成本；整体回撤从连续完整NAV计算。

每边手续费5bp、半价差1bp、滑点2bp、0.5×过去20日样本logvol×sqrt(实际订单额/过去20日quoteADV)冲击；不利tick、LOT/最低金额、参与率≤.001。执行成本及实际资金费支出按1/2/3倍，收入不放大。线性永续无现货借币；1倍入场抵押及小时不利价1%维持保证金代理。对比等目标金额的实际持有组合和零息现金。缺L2/TCA、完整tiers、tick清算与容量实证。

|范围|BTC目标USDT|ETH趋势滞后D|状态|净收益1/2/3倍%|整体DD3%|Sharpe3|Calmar3|正30日折1倍|近40日正5日折1/2/3|
|---|---|---|---|---|---|---|---|---|---|
|parent|1500|1|passed|5.409338 / 5.040792 / 4.672237|1.793675|1.525616|2.427913|10/13|6/6/6（各/8）|
|parent|1500|2|passed|8.943123 / 8.398045 / 7.853124|1.534455|2.068338|4.765402|12/13|6/6/6（各/8）|
|parent|1500|4|passed|10.777419 / 10.015619 / 9.253934|4.197205|1.825671|2.052042|11/13|6/6/6（各/8）|
|parent|1750|1|passed|6.387735 / 5.951145 / 5.514558|2.118338|1.526881|2.425771|10/13|6/6/6（各/8）|
|parent|1750|2|passed|9.921521 / 9.308398 / 8.695445|1.820303|2.047996|4.446764|12/13|6/6/6（各/8）|
|parent|1750|4|passed|11.755816 / 10.925971 / 10.096256|4.476548|1.844202|2.098567|11/13|6/6/6（各/8）|

事前失败判据：全期、近期和扩展各成本为正；1倍≥10/13正月；近期各成本≥6/8正5日折；扩展各成本≥3/4正折；DD3≤25%；邻域正及近期合格均≥60%；≥4次底层平仓；1倍毛损益加资金费/执行成本≥2.5；无拒单/负抵押/保证金代理违规；终点flat。

parent_BTCN1500_ETHlongonlyH200M4D1Age36hSlopeK0075_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1500_ETHlongonlyH200M4D2Age36hSlopeK0075_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1500_ETHlongonlyH200M4D4Age36hSlopeK0075_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1750_ETHlongonlyH200M4D1Age36hSlopeK0075_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1750_ETHlongonlyH200M4D2Age36hSlopeK0075_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1750_ETHlongonlyH200M4D4Age36hSlopeK0075_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。

相同D和本金，对旧BTC1000中心四指标严格改善父组合0/6。实际损益、资金费和执行成本差见sizing_effect_decomposition.json；全部变体/成本/逐折及连续每日净值见exports/。
完整三成本路径共6种；旧路径重复按NAV_alias_inventory保留披露，不能把相关路径算独立alpha。正Sharpe比例={"parent": {"1": 1.0, "2": 1.0, "3": 1.0}}；相邻敏感性边12，启发式警示3条，边界表现仅诊断，不扩网格或改选。
BTC金额轴为1000/1500/1750，间距不均；邻域按事前索引半径1定义。这是有限局部诊断，不代表完整响应面或参数显著性。Sharpe变化警示保持披露，未据此扩网格。

本轮四账户各续接120闭合分钟；原日决策数{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、成交数{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、资金费记录{'SMA': 0, 'candidate': 0, 'l4h02': 6, 'fewm': 6}。Nov21_00及原日决策均此前已处理；本轮实际08:00:00.003由L4/FEWM各按自己的原持仓和成本场景核算6条记录，candidate本轮尚未覆盖，保持0。原现金/q/desired/成本和完整NAV连续核验，不重置、不强平、不采用研究配置。下一candidate['2026-11-21T06:30:00Z', '2026-11-21T08:30:00Z']覆盖08，须freshGET/去重/reserve后处理；下一L4/FEWM['2026-11-21T08:10:00Z', '2026-11-21T10:10:00Z']已在08之后，不重复支付。SMA背景73日只读，下一原日决策Nov22_00:01。

原SMA三倍成本累计-7.468958%，仍为延迟shadow；原10bp与Float核算不变，未采用研究规则，不冒充十策略实盘报价模拟。所有账户尚未达到180日/六折资格。
监控成功=True，展示11442项，旧11436行完整字典保持。实际GET21，传输失败1；工程/读取失败原回执与恢复见read_failures.json。

实际复现命令（已完成模型和账户窗口不得重复计算）：

```sh
cd /home/desktop/Documents/Codex/EquiTide
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T225705Z/commands.py prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T225705Z/commands.py freeze
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T225705Z/commands.py units
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T225705Z/commands.py bind
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T225705Z/commands.py reserve_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T225705Z/commands.py evaluate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T225705Z/commands.py audit
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T225705Z/commands.py exports
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T225705Z/commands.py finish_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T225705Z/commands.py research_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T225705Z/commands.py l4h02
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T225705Z/commands.py fewm
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T225705Z/commands.py candidate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T225705Z/commands.py forward
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T225705Z/commands.py accounts_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T225705Z/commands.py journal
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T225705Z/commands.py sources_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T225705Z/commands.py gates
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T225705Z/commands.py feed
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T225705Z/commands.py midnight_prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T225705Z/commands.py collect
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T225705Z/commands.py final_checks
```

官方来源和访问UTC见primary_source_access.json：[Binance市场数据文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)。正收益回测不代表稳定实盘盈利。

本轮没有新的原日决策或成交。已知Nov21_00结算此前三永续均各记一次，本轮不重复；实际Nov21_08:00:00.003本轮由L4/FEWM各按自己的原持仓计入6条资产×成本记录，candidate当前窗口未覆盖，保持0。下一candidate06:30→08:30覆盖08结算，须新鲜查询、去重并先reserve后处理；L4/FEWM下一08:10→10:10已在该结算之后，不能重复记账。原SMA完整73日背景只读，下一原日决策Nov22_00:01。

Nov20_16三永续此前均已各记一次，本轮各0条；三永续唯一计数均6。首捕获UTC=2026-11-21T05:15:47.350340Z及原始毫秒/mark/rate保持。下一SMA/candidateNov21 06:30→08:30、L4/FEWM08:10→10:10（四原账户均已处理原Nov21日决策/资金费），须新鲜查询实际事件，不重复已记16，不提前记账。

与同金额、M4、H.02、年龄36小时且滞后D3的已完成结果比较：
BTC N1500/D1：收益差-5.041496pp、整体DD差0.259220pp、Sharpe差-0.777527、Calmar差-3.463095；完整NAV同路径=False。
BTC N1500/D2：收益差-1.860609pp、整体DD差0.000000pp、Sharpe差-0.234805、Calmar差-1.125605；完整NAV同路径=False。
BTC N1500/D4：收益差-0.459798pp、整体DD差2.662750pp、Sharpe差-0.477472、Calmar差-3.838966；完整NAV同路径=False。
BTC N1750/D1：收益差-5.041496pp、整体DD差0.298035pp、Sharpe差-0.740176、Calmar差-2.969354；完整NAV同路径=False。
BTC N1750/D2：收益差-1.860609pp、整体DD差0.000000pp、Sharpe差-0.219061、Calmar差-0.948361；完整NAV同路径=False。
BTC N1750/D4：收益差-0.459798pp、整体DD差2.656245pp、Sharpe差-0.422855、Calmar差-3.296559；完整NAV同路径=False。
全部18个逐成本比较见exports/previous_D3_comparisons.csv；仅比较已完成报告，不重跑旧组件或旧组合。

六个新组合均通过预设历史门槛，但18个逐成本比较中，旧同金额D3方案净收益、Sharpe和Calmar均更高，整体回撤不更大（D2回撤相同）；本轮不提升候选、不修改原冻结账户。实际D1/D2/D4路径和全部结果保留，不是独立前向或实盘盈利证明。见lag_comparison_review.json。

本轮网格K列代表趋势滞后D1/2/4，成熟资金费记录数M固定4。一个只读查重证明沿用旧funding-count字段名，已只更正说明键并保存原稿；冻结spec、来源、计算、收益和账户均未改变，见grid_label_scope_review.json。

实际Nov21_08:00:00.003结算：L4/FEWM本轮各6条、candidate本轮0，完整唯一计数按账户验证。BTC原持仓的资金费收入不乘成本倍数，ETH原持仓为0时保留零金额结算记录；不复用他人现金流。下一candidate06:30→08:30须新鲜查询、去重并先reserve后处理08；L4/FEWM下一08:10→10:10已在结算之后，不重复。原首次捕获UTC=2026-11-21T21:14:55.193067Z和来源SHA保持。原绑定只读notes保留，使用按各自窗口覆盖判断的final_notes_effective.py，不改金融模型或冻结账户规则。

本轮只读复核命令（不得重跑已完成金融模型或账户窗口）：

```sh
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T225705Z/bootstrap.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T225705Z/component_reuse_review.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T225705Z/funding_availability_review.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T225705Z/compare_previous_H.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T225705Z/review_economic_identity.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T225705Z/reconcile_actual08.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T225705Z/review_next_handoff.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T225705Z/final_notes_effective.py
```
