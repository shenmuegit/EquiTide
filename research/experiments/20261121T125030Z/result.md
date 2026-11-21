# 20261121T125030Z ETH趋势斜率门槛与成熟资金费数联合验证

本轮结论：6个组合满足事前历史门槛、6个ETH单组件被拒绝；没有优于旧K.0075中心的新方法。K.00625降低净收益且扩大整体回撤，K.00875与旧完整成本路径一致。全部实际结果保留，原冻结账户不采用本轮参数。

事前固定有限EWM16、D3斜率门槛K=.00625/.0075旧/.00875 × M4/5/6。六个新ETH原生模型与六个新BTC1000父组合分别reserve、实际执行一次及finish；旧中心及12个来源只读。新父组合历史通过6/6，ETH新组件通过0/6。预设K.00625/M5不按结果改选。

完整读取40212事件/19967ID和498份结论，初始16项真实结果缺口0。规范研究定义11841→11853，相关路径及历史选择不构成独立试验。

在48小时成熟资金费历史下，降低/提高有限EWM16、滞后3日的趋势斜率门槛可能改变逆势入场质量与资金费过滤的交互。预设K.00625/.0075旧/.00875 × M4/5/6，六个新ETH原生配置及各自BTC1000父组合；旧中心及12个已完成来源只读。预设K.00625/M5，不按结果改选。原始银行乘数[1,1]，C3750+15000=18750，资本20/80；固定原生目标BTC1000+ETH4000=5000，无归一化、缩放、转账、再平衡或跨保证金。实际新ETH数量/费用/冲击/资金费/风险重算，BTC及持有原组件不重跑。

BTC readonlyL29H.03E.005,V10cap.0275,strictROC5>.0025,C3750N1000. ETH longonly L5 reversal H.02,E.0075 fixed;finite normalizedEWMS16 beta15/17,D3:strict slow slope > .00625/.0075old/.00875 for new long entries only. Existinglong retained while completedL5ROC<.0075;normalexit at equality. V6samplelogvol<=.05625;M4/5/6 mature actualfunding,minage1h/maxage48h,availability<=signal;budgetmin(.0002,.0075*VW9samplelogvol*latest actual intervalhours/24),interval<=36h. Gates do not resize or forceclose existingpositions. No fitting/future data.

旧父组合标量描述差异见legacy_parent_scalar_review.json，按实际子图核对，对旧记录不改写。原始银行乘数[1,1]不归一化；C3750+15000=18750，资本20/80，固定原生目标BTC1000+ETH4000=5000。新ETH各场景重算真实LOT数量、费用、成交量冲击、资金费及风险；BTC和持有原组件只读，父组合对齐完整共同时间轴相加美元NAV，无父订单、转账、再平衡或跨保证金。

全部391日为反复使用的开发历史2025-10-19 00:01→2026-11-14 00:01，不是未触碰最终测试；无拟合/标签、实际33闭合上下文日及embargo0，13个完整30日折+1日尾段，近期40日8×5、扩展21日5/5/5/6。折间继承现金/q，只在全期终点计费平仓，用连续完整NAV计算整体回撤。旧warmup30/embargo3/完整折12为非执行描述，实际代码/账本独立核对，旧记录不改。

每边手续费5bp、半价差1bp、滑点2bp及0.5×过去20日样本logvol×sqrt(实际订单额/过去20日quoteADV)冲击；不利tick、LOT/最低金额、参与率≤.001。实际资金费，执行成本及资金费支出1/2/3倍，收入不放大。线性永续无现货借币，1倍入场抵押及小时不利价1%维持保证金代理；匹配持有和零息现金对照。缺真实L2/TCA、完整tiers、tick清算与容量实证。

|范围|斜率K|成熟M|状态|净收益1/2/3倍%|整体DD3%|Sharpe3|Calmar3|正30日折1倍|近40日正5日折1/2/3|
|---|---|---|---|---|---|---|---|---|---|
|native|0.00625|4|rejected|5.632508 / 5.191694 / 4.751173|4.103613|1.077719|1.079134|7/13|0/0/0（各/8）|
|native|0.00625|5|rejected|4.410203 / 4.021240 / 3.632570|4.103613|0.863214|0.825364|6/13|0/0/0（各/8）|
|native|0.00625|6|rejected|5.294597 / 4.849012 / 4.403720|4.103613|0.994491|1.000329|7/13|0/0/0（各/8）|
|native|0.00875|4|rejected|7.053708 / 6.677684 / 6.301870|1.528984|1.860974|3.839649|7/13|0/0/0（各/8）|
|native|0.00875|5|rejected|5.831403 / 5.507230 / 5.183267|1.528984|1.642651|3.159229|6/13|0/0/0（各/8）|
|native|0.00875|6|rejected|6.715796 / 6.335002 / 5.954418|1.528984|1.738908|3.628353|7/13|0/0/0（各/8）|
|parent|0.00625|4|passed|8.152047 / 7.553666 / 6.955534|3.820753|1.609138|1.695572|11/13|6/6/6（各/8）|
|parent|0.00625|5|passed|7.174203 / 6.617304 / 6.060651|3.820753|1.466523|1.477845|11/13|6/6/6（各/8）|
|parent|0.00625|6|passed|7.881718 / 7.279521 / 6.677571|3.820753|1.537849|1.627956|11/13|6/6/6（各/8）|
|parent|0.00875|4|passed|9.289007 / 8.742459 / 8.196091|1.357834|2.342950|5.619846|12/13|6/6/6（各/8）|
|parent|0.00875|5|passed|8.311163 / 7.806096 / 7.301209|1.357834|2.230073|5.007665|12/13|6/6/6（各/8）|
|parent|0.00875|6|passed|9.018678 / 8.468313 / 7.918129|1.357834|2.244814|5.429731|12/13|6/6/6（各/8）|

事前失败判据：全期、近期和扩展各成本为正；1倍≥10/13正月；近期各成本≥6/8正5日折；扩展各成本≥3/4正折；DD3≤25%；邻域正及近期合格均≥60%；≥4次底层平仓；1倍毛损益加资金费/执行成本≥2.5；无拒单/负抵押/保证金代理违规；终点flat。

ETH_longonly_L5H0p02E0p0075_EWMS16D3K0p00625_V6Cap0p05625_M4Age48hBudgetVW9R0p0075_C15000_N4000_391d：ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_recent6of8_allcost_gte60pct；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
ETH_longonly_L5H0p02E0p0075_EWMS16D3K0p00625_V6Cap0p05625_M5Age48hBudgetVW9R0p0075_C15000_N4000_391d：ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_recent6of8_allcost_gte60pct；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
ETH_longonly_L5H0p02E0p0075_EWMS16D3K0p00625_V6Cap0p05625_M6Age48hBudgetVW9R0p0075_C15000_N4000_391d：ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_recent6of8_allcost_gte60pct；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
ETH_longonly_L5H0p02E0p0075_EWMS16D3K0p00875_V6Cap0p05625_M4Age48hBudgetVW9R0p0075_C15000_N4000_391d：ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_recent6of8_allcost_gte60pct；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
ETH_longonly_L5H0p02E0p0075_EWMS16D3K0p00875_V6Cap0p05625_M5Age48hBudgetVW9R0p0075_C15000_N4000_391d：ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_recent6of8_allcost_gte60pct；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
ETH_longonly_L5H0p02E0p0075_EWMS16D3K0p00875_V6Cap0p05625_M6Age48hBudgetVW9R0p0075_C15000_N4000_391d：ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_recent6of8_allcost_gte60pct；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_ETH_SlopeK0p00625_V6L5E0p0075_EWMS16D3_FundingM4Age48hR0p0075_N4000_BTCN1000_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_ETH_SlopeK0p00625_V6L5E0p0075_EWMS16D3_FundingM5Age48hR0p0075_N4000_BTCN1000_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_ETH_SlopeK0p00625_V6L5E0p0075_EWMS16D3_FundingM6Age48hR0p0075_N4000_BTCN1000_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_ETH_SlopeK0p00875_V6L5E0p0075_EWMS16D3_FundingM4Age48hR0p0075_N4000_BTCN1000_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_ETH_SlopeK0p00875_V6L5E0p0075_EWMS16D3_FundingM5Age48hR0p0075_N4000_BTCN1000_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_ETH_SlopeK0p00875_V6L5E0p0075_EWMS16D3_FundingM6Age48hR0p0075_N4000_BTCN1000_C3750_15000_391d：通过预设历史门槛，待独立前向验证。

相同M和资本，对旧K.0075中心四指标严格改善父组合0/6、ETH组件0/6。实际损益、资金费和执行成本差见sizing_effect_decomposition.json；全部变体/成本/逐折及连续每日净值见exports/。
完整三成本路径共12种；旧路径重复按NAV_alias_inventory保留披露，不能把相关路径算独立alpha。正Sharpe比例={"native": {"1": 1.0, "2": 1.0, "3": 1.0}, "parent": {"1": 1.0, "2": 1.0, "3": 1.0}}；相邻敏感性边24，启发式警示6条，边界表现仅诊断，不扩网格或改选。

本轮四账户各续接120闭合分钟；原日决策数{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、成交数{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、实际新增资金费记录{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}，逐笔核对原现金/数量/费用及完整NAV。Nov20原日决策和三永续实际00:00:00.001资金费均在本轮前处理完毕；三永续实际08资金费此前均已各记一次；本轮按各自新窗口完整查询，只处理实际新事件，不重复，不复制其他账户金额。SMA复用真实full72 SPOT权威和原Float记账，只增加分钟估值。下一SMA/candidate['2026-11-20T20:30:00Z', '2026-11-20T22:30:00Z']、L4/FEWM['2026-11-20T22:10:00Z', '2026-11-21T00:10:00Z']中SMA/candidate仅mark，L4/FEWM将跨原Nov21_00:01日决策，须使用完整闭合日上下文和原冻结日核算并独立核对实际新资金费；不提前记账。不重置、不强制平仓、不采用研究配置。

原SMA三倍成本累计-7.468958%，仍为延迟shadow；原10bp与Float核算不变，未采用研究规则，不冒充十策略实盘报价模拟。所有账户尚未达到180日/六折资格。
监控成功=True，展示11412项，旧11400行完整字典保持。实际GET21，传输失败1；工程/读取失败原回执与恢复见read_failures.json。

实际复现命令（已完成模型和账户窗口不得重复计算）：

```sh
cd /home/desktop/Documents/Codex/EquiTide
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T125030Z/commands.py prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T125030Z/commands.py freeze
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T125030Z/commands.py units
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T125030Z/commands.py units_retry1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T125030Z/commands.py bind
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T125030Z/commands.py reserve_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T125030Z/commands.py reserve_1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T125030Z/commands.py evaluate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T125030Z/commands.py audit
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T125030Z/commands.py exports
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T125030Z/commands.py finish_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T125030Z/commands.py finish_1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T125030Z/commands.py research_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T125030Z/commands.py l4h02
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T125030Z/commands.py fewm
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T125030Z/commands.py candidate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T125030Z/commands.py forward
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T125030Z/commands.py accounts_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T125030Z/commands.py journal
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T125030Z/commands.py sources_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T125030Z/commands.py gates
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T125030Z/commands.py feed
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T125030Z/commands.py midnight_prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T125030Z/commands.py collect
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T125030Z/commands.py final_checks
```

官方来源和访问UTC见primary_source_access.json：[Binance市场数据文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)。正收益回测不代表稳定实盘盈利。

Nov20原跨日已完成：三永续实际00:00:00.001资金费均恰好记一次，四账户原00:01日决策均已处理；首捕获UTC=2026-11-20T13:12:16.739946Z保持。下一SMA/candidate20:30→22:30仅mark；L4/FEWM22:10→Nov21 00:10将跨原日决策Nov21 00:01，须先查询实际新资金费和闭合日上下文，沿用原日核算，SMA保留真实SPOT full72。不预记未来事件。

Nov20_16三永续此前均已各记一次，本轮各0条；三永续唯一计数均6。首捕获UTC=2026-11-21T05:15:47.350340Z及原始毫秒/mark/rate保持。下一SMA/candidate20:30→22:30、L4/FEWM22:10→Nov21 00:10（将跨原00:01日决策），须新鲜查询实际事件，不重复已记16，不提前记账。

本轮实际评估6个ETH新原生斜率K.00625/.00875×成熟资金费M4/5/6，以及6个BTC1000父组合；K.0075中心行与12个来源只读。固定L5/H.02/E.0075、S16beta15/17/D3、V6上限.05625、R.0075/VW9、资金费年龄1..48h。ETH真实数量、费用、冲击、资金费和保证金按各配置重算，BTC与持有组件不重跑。原始银行乘数[1,1]和C3750+15000=18750资本20/80不归一化；没有父订单、转账或再平衡。结构化参数与已保存决策经独立核对。

Nov20实际08:00资金费的三永续唯一计数均为6，本轮不重复；原首捕获UTC=2026-11-20T21:14:36.626765Z保持。下一窗口的实际资金费首次来源、精确毫秒时间和待入账分配保存在next_required_settlement_binding_state；必须重新查询和去重，当前只读准备不提前入账；原SMA继续使用full72真实SPOT权威，下一原日决策Nov21_00:01。详见next_required_settlement_binding_state。

本轮额外实际只读复核命令（已完成市场回测和账户窗口不得重复执行）：

```sh
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T125030Z/funding_availability_review.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T125030Z/component_reuse_review.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T125030Z/review_slope_actions.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T125030Z/review_economic_identity.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T125030Z/review_policy_metadata.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T125030Z/final_notes.py
```
