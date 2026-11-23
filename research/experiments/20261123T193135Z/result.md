# 20261123T193135Z BTC实际金额 × ETH趋势强度门槛验证

固定BTC实际原生入场目标750/1000旧/1250USDT × ETH趋势斜率门槛K.00625/.0075旧/.00875，检验较宽松与较严格入场趋势强度过滤在较低BTC敞口下的组合效应。ETH固定C15000/N4000、ROC L5/H.02/E.0075、有限EWMS16 beta15/17、趋势滞后D3、入场V6cap.05625、成熟M4/年龄1..36h、资金费预算比R.0075/VW9；BTC固定C3750、L29/H.03/E.005、V10cap.0275、strictpositiveROC5>.0025。事前代表750/K.00625，不按结果改选；四个新被动组合，十个旧原生银行和八个旧父/持有只读。原银行乘数[1,1]不归一化，本金18750、资本20/80，初始目标4750/5250USDT；保留实际LOT/q/非线性冲击/费用/资金费/保证金，无父订单、转账、再平衡或跨保证金。

完整读取41656事件/20689ID、524份既往结论及初始16项原始证据；初始16项实际结果缺口0。四个新父组合分别先reserve再计算一次、finish；十个旧原生银行及八个旧父/持有只读。代表配置事前750/K.00625。

银行乘数[1,1]不归一化，C3750+15000=18750，资本20/80，实际原始目标BTC750或1250+ETH4000=4750/5250。完整共同时间轴相加美元NAV，复用原q、LOT、非线性冲击、费用、资金费及保证金；无父订单、转账、再平衡或跨保证金。

历史2025-10-19 00:01至2026-11-14 00:01共391日，已反复研究，仅为开发验证历史。固定规则无拟合标签，33个闭合上下文日，purge/embargo0；13个30日折加1日尾段、近40日8×5日、扩展21日5/5/5/6，折间延续账户，终点平仓计成本，整体回撤由完整连续NAV计算。不是未触碰最终测试、独立alpha或稳定实盘盈利。

每边手续费5bp、半价差1bp、滑点2bp，加0.5×过去20日logvol×sqrt(实际订单额/过去20日quoteADV)冲击；不利tick/LOT/最低金额、参与率≤.001。1/2/3倍执行成本和资金费支出，收入不放大。线性永续无现货借币，1倍入场抵押及小时不利价1%维持保证金代理；缺L2/TCA、完整tiers、tick清算及容量实证。

|BTC目标|ETH门槛K|状态|净收益1/2/3倍%|整体DD3%|Sharpe3|Calmar3|正30日折1倍|近40日正5日折1/2/3|
|---|---|---|---|---|---|---|---|---|
|750|0.00625|passed|7.080500/6.551876/6.023478|3.680060|1.503591|1.524951|11/13|6/6/6|
|750|0.00875|passed|8.217460/7.740668/7.264036|1.320789|2.299304|5.121964|12/13|6/6/6|
|1250|0.00625|passed|9.050174/8.385907/7.721845|4.000404|1.657855|1.797407|11/13|6/6/6|
|1250|0.00875|passed|10.187134/9.574699/8.962403|1.393497|2.324128|5.986568|12/13|6/6/6|

历史通过4/4；每项失败判据见report.json。双轴3×3网格含4新定义和5旧对照，全部逐变体/逐折/成本/完整日NAV及12条相邻边见exports/；启发式警告见sensitivity_axis_review.json，不按结果择优或延展网格。

同BTC金额、同资本旧K.0075逐成本对照：
BTC750/K0.00625：收益差-1.240558pp、整体DD差2.359271pp、Sharpe差-0.795713、Calmar差-3.597013，完整NAV同路径=False。
BTC750/K0.00875：收益差0.000000pp、整体DD差0.000000pp、Sharpe差0.000000、Calmar差0.000000，完整NAV同路径=True。
BTC1250/K0.00625：收益差-1.240558pp、整体DD差2.606906pp、Sharpe差-0.666272、Calmar差-4.189161，完整NAV同路径=False。
BTC1250/K0.00875：收益差0.000000pp、整体DD差0.000000pp、Sharpe差0.000000、Calmar差0.000000，完整NAV同路径=True。

实际执行路径与旧配置相同的定义仍保留独立参数登记，但不称新增独立收益证据。维持事前750/K.00625，不据已见历史改选，不改变原冻结账户。

本轮原账户各延续120闭合分钟，日决策计数={"SMA": 1, "candidate": 1, "l4h02": 0, "fewm": 0}、资金费记录={"SMA": 0, "candidate": 6, "l4h02": 0, "fewm": 0}、原内核实际成交={"SMA": 0, "candidate": 0, "l4h02": 0, "fewm": 0}。SMA用真实full75现货日数据、原SMA65/1%/75:25/Float10bp规则执行一次原日决策并按各成本插入一个日参考点；candidate先用自身旧q处理实际00资金费再执行原日规则；L4/FEWM本轮只增估值，已记入的Nov23事件不重复。SMA延迟shadow与十策略真实报价模拟盘分开，原负收益完整保留。

实际Nov23_00结算时间1795392000000毫秒，首次捕获UTC2026-11-23T16:05:46.851318Z与SHA2586dfdacfbc00962dd422ac4752b766a91f7f8f5a11924f7992cd53ebea9f1b保持；现三个永续账户各6个唯一键。下一各自窗口={"SMA": ["2026-11-23T00:30:00Z", "2026-11-23T02:30:00Z"], "candidate": ["2026-11-23T00:30:00Z", "2026-11-23T02:30:00Z"], "l4h02": ["2026-11-23T02:10:00Z", "2026-11-23T04:10:00Z"], "fewm": ["2026-11-23T02:10:00Z", "2026-11-23T04:10:00Z"]}，下一原日决策={"SMA": [], "candidate": [], "l4h02": [], "fewm": []}，实际资金费待处理={"SMA": 0, "candidate": 0, "l4h02": 0, "fewm": 0}；仍须新鲜完整查询、按自身窗口去重并先reserve。SMA下次mark-only须重绑当前状态及full75真实日背景，不能直接复制日决策适配器重跑；无提前记账。

数据哈希、复现命令和全部实际失败见data_manifest.json、commands_display_verification.json、read_failures.json；图表只画已完成结果。

SMA只读审计恢复：原绑定审计源audit_forward.py仍含74/73根日线数量断言，原源及失败日志保留；有效审计源为audit_forward_full75.py，仅将当前日线/旧重叠改为75/74。新审计已实际通过后才finish，金融报告、SMA首次报告/状态/输入/实算源的SHA全部保持。未重算账户。只读复核请直接运行该有效审计源，不使用旧forward.py verify入口所引用的原审计源。复现命令与next_required_effective_SMA_readonly_audit_source明确记录有效源。

已知Nov21_08:00:00.003三永续此前均已记账一次，本轮不重复；当前资金费记录={"SMA": 0, "candidate": 6, "l4h02": 0, "fewm": 0}。08全链唯一计数各6，首次捕获UTC和原始来源SHA保持；下一窗口继续freshGET与按账户去重，不提前记账。

旧Nov21_16事件三个永续各6个唯一键，本轮旧事件0新增；本轮其他资金费与原日决策成交按自身q/mark/rate/成本逐项重核，十八本现金完整对账。详见actual16_nov21_reconciliation.json，未重跑模型或账户窗口。

本轮只读复核命令（不得重跑已完成金融模型或账户窗口）：

```sh
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/component_reuse_review.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/funding_availability_review.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/compare_previous_H.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/review_economic_identity.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/review_sensitivity_axes.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/review_reservation_metadata.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/review_trend_hurdle_economics.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/reconcile_actual08.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/reconcile_actual16.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/review_next_handoff.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/review_next_settlement_split.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/reconcile_nov22_16.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/review_next_daily_boundary.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/final_notes.py
```

三项验证均已执行，四个配置通过预设历史门槛；同金额旧K.0075逐成本比较四指标同时改善0项，旧K.0075支配6项；完整NAV同路径6项。敏感性启发式警告见实际门槛轴记录，非显著性检验。
ETH K0.00625相对旧K.0075：趋势方向差18日、最终desired差8日；轮数差1、执行差2、毛损益差-204.038340USDT、资金费净额差-2.828161USDT、执行成本差6.313439USDT、终值差-213.179940USDT。
ETH K0.00875相对旧K.0075：趋势方向差14日、最终desired差0日；轮数差0、执行差0、毛损益差0.000000USDT、资金费净额差0.000000USDT、执行成本差0.000000USDT、终值差0.000000USDT。
低门槛K.00625增加交易、损失与回撤；高门槛K.00875保持旧K.0075完整路径。保留事前750/K.00625，不替换原冻结账户，不据重复历史推广。

实际复现与只读核对命令：

```sh
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/commands.py prepare
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/commands.py freeze
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/commands.py units
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/commands.py bind
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/commands.py reserve_0
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/commands.py evaluate
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/commands.py audit
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/commands.py exports
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/commands.py finish_0
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/commands.py research_check
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/commands.py l4h02
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/commands.py fewm
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/commands.py candidate
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/commands.py forward
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/commands.py forward_retry1
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/commands.py accounts_check
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/commands.py journal
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/commands.py sources_check
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/commands.py gates
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/commands.py feed
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/commands.py midnight_prepare
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/commands.py collect
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/commands.py final_checks
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/component_reuse_review.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/funding_availability_review.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/compare_previous_H.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/review_economic_identity.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/review_sensitivity_axes.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/review_reservation_metadata.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/review_trend_hurdle_economics.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/reconcile_actual08.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/reconcile_actual16.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/review_next_handoff.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/review_next_settlement_split.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/reconcile_nov22_16.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/review_next_daily_boundary.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T193135Z/final_notes.py
```
已完成金融模型与账户窗口不得重复执行；上述原始命令含reserve，历史复现应使用隔离的登记副本，现有main只读核对已保存结果。
