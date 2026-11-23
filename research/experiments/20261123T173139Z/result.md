# 20261123T173139Z BTC实际金额 × ETH趋势斜率滞后验证

固定BTC实际原生入场目标750/1000旧/1250USDT × ETH趋势斜率滞后D2/3旧/4日，检验较快与较慢趋势过滤在较低BTC敞口下的组合效应。ETH固定C15000/N4000、ROC L5/H.02/E.0075、有限EWMS16 beta15/17、趋势门槛K.0075、入场V6cap.05625、成熟M4/年龄1..36h、资金费预算比R.0075/VW9；BTC固定C3750、L29/H.03/E.005、V10cap.0275、strictpositiveROC5>.0025。预设750/D2，不按结果改选。四个新被动组合；十个旧原生银行与八个旧父/持有只读。原银行乘数[1,1]不归一化，本金18750、资本20/80，初始目标4750/5250USDT；保留实际LOT/q/非线性冲击/费用/资金费/保证金，无父订单、转账、再平衡或跨保证金。

完整读取41604事件/20663ID、523份既往结论及初始16项原始证据；初始16项实际结果缺口0。四个新父组合分别先reserve再计算一次、finish；十个旧原生银行及八个旧父/持有只读。代表配置事前750/D2。

原银行乘数[1,1]不归一化，C3750+15000=18750，资本20/80，实际原始目标BTC750或1250+ETH4000=4750/5250。对齐完整共同时间轴相加美元NAV，复用原q、LOT、非线性成交量冲击、费用、资金费和保证金；无父订单、转账、再平衡或跨保证金。

历史2025-10-19 00:01至2026-11-14 00:01共391日，已反复研究，仅为开发验证历史。固定规则无拟合标签，33个完成上下文日，purge/embargo0；13个30日折加1日尾段，近40日8×5日和扩展21日5/5/5/6，折间延续账户，终点平仓计成本，整体回撤由完整连续NAV计算。不是未触碰最终测试、独立alpha或稳定实盘盈利。

每边手续费5bp、半价差1bp、滑点2bp，加0.5×过去20日logvol×sqrt(实际订单额/过去20日quoteADV)冲击；不利tick/LOT/最低金额，参与率≤.001。1/2/3倍执行成本和资金费支出，收入不放大。线性永续无现货借币，1倍入场抵押+小时不利价1%维持保证金代理；缺L2/TCA、完整tiers、tick清算及容量实证。

|BTC目标|ETH滞后日|状态|净收益1/2/3倍%|整体DD3%|Sharpe3|Calmar3|正30日折1倍|近40日正5日折1/2/3|
|---|---|---|---|---|---|---|---|---|
|750|2|passed|6.108279/5.755774/5.403427|1.019915|1.993261|4.936909|12/13|6/6/6|
|750|4|passed|7.942575/7.373347/6.804238|3.680060|1.656674|1.722186|11/13|6/6/6|
|1250|2|passed|8.077954/7.589805/7.101794|1.331668|2.074791|4.966912|12/13|6/6/6|
|1250|4|passed|9.912249/9.207378/8.502605|4.000404|1.792033|1.978657|11/13|6/6/6|

历史通过4/4，失败判据逐项见report.json。双轴3×3网格包含4新配置和5旧对照；全部逐变体/逐折/成本、完整日NAV及12条相邻边见exports/。敏感性启发式警告见sensitivity_axis_review.json，不据结果择优或延展网格。

同BTC金额、同资本旧D3逐成本对照：
BTC750/D2：收益差-1.860609pp、整体DD差-0.300874pp、Sharpe差-0.306042、Calmar差-0.185055，完整NAV同路径=False。
BTC750/D4：收益差-0.459798pp、整体DD差2.359271pp、Sharpe差-0.642629、Calmar差-3.399778，完整NAV同路径=False。
BTC1250/D2：收益差-1.860609pp、整体DD差-0.061829pp、Sharpe差-0.249336、Calmar差-1.019656，完整NAV同路径=False。
BTC1250/D4：收益差-0.459798pp、整体DD差2.606906pp、Sharpe差-0.532094、Calmar差-4.007911，完整NAV同路径=False。

四个新图的历史收益均为正，比较优劣与历史门槛状态分别保留；维持事前750/D2，不据已见历史改选，不改变原冻结账户。

原冻结账户各延续120分钟，当前原日决策计数={"SMA": 0, "candidate": 0, "l4h02": 1, "fewm": 1}，资金费记录={"SMA": 0, "candidate": 0, "l4h02": 6, "fewm": 6}，实际原内核成交={"SMA": 0, "candidate": 0, "l4h02": 0, "fewm": 0}。L4/FEWM各按自身旧q先处理实际Nov23_00资金费，再于00:01执行原冻结规则；candidate/SMA本轮只增估值。资金费时间1795392000000毫秒、首次UTC2026-11-23T16:05:46.851318Z和SHA2586dfdacfbc00962dd422ac4752b766a91f7f8f5a11924f7992cd53ebea9f1b保持；此前旧结算不重复。原SMA负收益仍保留，属于延迟shadow，独立于十策略真实报价模拟。

下一各自窗口={"SMA": ["2026-11-22T22:30:00Z", "2026-11-23T00:30:00Z"], "candidate": ["2026-11-22T22:30:00Z", "2026-11-23T00:30:00Z"], "l4h02": ["2026-11-23T00:10:00Z", "2026-11-23T02:10:00Z"], "fewm": ["2026-11-23T00:10:00Z", "2026-11-23T02:10:00Z"]}；原日决策={"SMA": ["2026-11-23T00:01:00Z"], "candidate": ["2026-11-23T00:01:00Z"], "l4h02": [], "fewm": []}；实际资金费待处理={"SMA": 0, "candidate": 6, "l4h02": 0, "fewm": 0}。SMA下一窗口须使用full75真实现货完整日数据（精确74日旧前缀），重绑原日决策适配器/登记及新闭合分钟后再reserve；L4/FEWM已处理Nov23日决策与资金费，不重复。当前仅只读准备，无提前记账。

所有实际失败、重试及只读模板文字局限见read_failures.json和stdout_label_notes.json。冻结plan/spec源原字节保留，结构化子组件参数及实际D2/3/4规则为数值依据。复现命令见commands_display_verification.json与各原始命令回执。

已知Nov21_08:00:00.003三永续此前均已记账一次，本轮不重复；当前资金费记录={"SMA": 0, "candidate": 0, "l4h02": 6, "fewm": 6}。08全链唯一计数各6，首次捕获UTC和原始来源SHA保持；下一窗口继续freshGET与按账户去重，不提前记账。

旧Nov21_16事件三个永续各6个唯一键，本轮旧事件0新增；本轮其他资金费与原日决策成交按自身q/mark/rate/成本逐项重核，十八本现金完整对账。详见actual16_nov21_reconciliation.json，未重跑模型或账户窗口。

本轮只读复核命令（不得重跑已完成金融模型或账户窗口）：

```sh
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/component_reuse_lag_review.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/funding_availability_lag_review.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/compare_previous_H.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/review_economic_identity.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/review_sensitivity_axes.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/review_reservation_metadata.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/review_trend_lag_economics.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/reconcile_actual08.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/reconcile_actual16.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/review_next_handoff_full75.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/review_next_settlement_split.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/reconcile_nov22_16.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/review_next_daily_boundary.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/exports.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/final_notes.py
```

三项验证均已执行，四个配置通过预设历史门槛；同金额旧D3逐成本比较四指标同时改善0项，旧D3支配6项；完整NAV同路径0项。敏感性三条启发式警告均在ETH滞后轴，非显著性检验。
ETH D2相对旧D3：趋势方向差45日、最终desired差9日；轮数差-3、执行差-6、毛损益差-416.739090USDT、资金费净额差1.415625USDT、执行成本差-19.852148USDT、终值差-395.471317USDT。
ETH D4相对旧D3：趋势方向差43日、最终desired差12日；轮数差2、执行差4、毛损益差-36.296740USDT、资金费净额差-2.264044USDT、执行成本差12.980146USDT、终值差-51.540930USDT。
D2减少交易和回撤但丢失更多毛收益；D4增加交易和成本且回撤更大。保留事前750/D2，不替换原冻结账户，不据重复历史推广。

实际复现与只读核对命令：

```sh
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/commands.py prepare
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/commands.py freeze
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/commands.py units
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/commands.py bind
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/commands.py reserve_0
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/commands.py evaluate
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/commands.py audit
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/commands.py exports
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/commands.py finish_0
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/commands.py research_check
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/commands.py l4h02
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/commands.py fewm
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/commands.py candidate
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/commands.py forward
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/commands.py accounts_check
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/commands.py journal
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/commands.py sources_check
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/commands.py gates
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/commands.py feed
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/commands.py midnight_prepare
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/commands.py collect
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/commands.py final_checks
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/component_reuse_lag_review.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/funding_availability_lag_review.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/compare_previous_H.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/review_economic_identity.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/review_sensitivity_axes.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/review_reservation_metadata.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/review_trend_lag_economics.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/reconcile_actual08.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/reconcile_actual16.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/review_next_handoff_full75.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/review_next_settlement_split.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/reconcile_nov22_16.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/review_next_daily_boundary.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/exports.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T173139Z/final_notes.py
```
已完成金融模型与账户窗口不得重复执行；上述原始命令含reserve，历史复现应使用隔离的登记副本，现有main只读核对已保存结果。
