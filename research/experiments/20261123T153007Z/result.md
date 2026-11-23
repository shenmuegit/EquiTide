# 20261123T153007Z BTC实际入场金额与ETH资金费预算波动率窗口组合验证

事前固定BTC实际原生目标N750/1000旧/1250 × ETH 资金费预算波动率窗口VW8/9旧/12日。ETH固定趋势K.0075、S16、D3、入场V6、H=.02、退出E.0075、cap.05625、M4、预算比R=.0075、最大年龄36小时，资金费预算波动率窗口按VW轴变化，趋势K.0075、退出E.0075与入场波动率V6固定；四个新被动父组合分别reserve、计算一次及finish，十个原生银行和八个旧父/持有对照只读；历史通过4/4。预设N750/VW8，不按结果改选。

完整读取41552事件/20637ID和522份结论；初始16项实际结果缺口0。规范研究定义11973→11977，不能将相关路径和历史选择视为独立试验。

固定BTC实际原生入场目标750/1000旧/1250USDT × ETH资金费预算波动率窗口VW8/9旧/12日，检验短窗口预算反应与长窗口平滑预算在较低BTC敞口下的组合效应。ETH固定C15000/N4000、ROC L5/H.02/E.0075、有限EWMS16 beta15/17/D3/趋势K.0075、入场V6cap.05625、成熟M4/年龄1..36h、资金费预算比R.0075；BTC固定C3750、L29/H.03/E.005、V10cap.0275、strictpositiveROC5>.0025。预设750/VW8，不按结果改选。四个新被动组合；十个旧原生银行与八个旧父/持有只读，原银行乘数[1,1]不归一化，本金18750、资本20/80，初始目标4750/5250USDT。保留原LOT/q/非线性冲击/费用/资金费/保证金，无父订单、转账、再平衡或跨保证金。

All sources are actually completed unchanged banks: BTC L29H.03E.005,V10cap.0275,strictpositiveROC5>.0025; ETH L5contrarianH.02,E.0075,finiteEWMS16beta15/17,D3K.0075,V6cap.05625,M4,age1..36h,R.0075,funding-budget volatility VW8/9old/12. No fitting or native execution.

原始银行乘数[1,1]不归一化，C3750+15000=18750，资本20/80；本轮目标BTC750或1250+ETH4000=4750或5250。每个原生组件均已按实际金额计算过LOT数量、非线性成交量冲击、费用、资金费及保证金，直接复用完整净值；父组合对齐共同时间轴相加美元NAV，无新增父订单、转账、再平衡或跨保证金，不线性缩放NAV。

391日为反复使用的开发历史2025-10-19 00:01→2026-11-14 00:01，不能称未触碰最终测试。无拟合标签，实际33闭合上下文日、embargo0；13个完整30日折+1日尾段，近期40日8×5、扩展21日5/5/5/6。折间继承现金/q，全期终点平仓计成本；整体回撤从连续完整NAV计算。

每边手续费5bp、半价差1bp、滑点2bp、0.5×过去20日样本logvol×sqrt(实际订单额/过去20日quoteADV)冲击；不利tick、LOT/最低金额、参与率≤.001。执行成本及实际资金费支出按1/2/3倍，收入不放大。线性永续无现货借币；1倍入场抵押及小时不利价1%维持保证金代理。对比等目标金额的实际持有组合和零息现金。缺L2/TCA、完整tiers、tick清算与容量实证。

|范围|BTC目标USDT|ETH资金费预算波动率窗口VW（日）|状态|净收益1/2/3倍%|整体DD3%|Sharpe3|Calmar3|正30日折1倍|近40日正5日折1/2/3|
|---|---|---|---|---|---|---|---|---|---|
|parent|750|8|passed|8.048273 / 7.631669 / 7.215225|1.320789|2.323603|5.087626|12/13|6/6/6（各/8）|
|parent|750|12|passed|7.947131 / 7.466522 / 6.986074|1.320789|2.189690|4.926404|12/13|6/6/6（各/8）|
|parent|1250|8|passed|10.017947 / 9.465700 / 8.913592|1.393497|2.343530|5.954055|12/13|6/6/6（各/8）|
|parent|1250|12|passed|9.916805 / 9.300553 / 8.684441|1.393497|2.236322|5.801405|12/13|6/6/6（各/8）|

事前失败判据：全期、近期和扩展各成本为正；1倍≥10/13正月；近期各成本≥6/8正5日折；扩展各成本≥3/4正折；DD3≤25%；邻域正及近期合格均≥60%；≥4次底层平仓；1倍毛损益加资金费/执行成本≥2.5；无拒单/负抵押/保证金代理违规；终点flat。

parent_BTCN750_ETHlongonlyL5H200M4D3Age36hSlopeK0075E0075V6Cap05625VW8R0075_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN750_ETHlongonlyL5H200M4D3Age36hSlopeK0075E0075V6Cap05625VW12R0075_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1250_ETHlongonlyL5H200M4D3Age36hSlopeK0075E0075V6Cap05625VW8R0075_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1250_ETHlongonlyL5H200M4D3Age36hSlopeK0075E0075V6Cap05625VW12R0075_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。

相同ETH资金费预算波动率窗口和本金，对旧BTC1000中心四指标严格改善父组合0/4。实际损益、资金费和执行成本差见sizing_effect_decomposition.json；全部变体/成本/逐折及连续每日净值见exports/。
完整三成本路径共4种；旧路径重复按NAV_alias_inventory保留披露，不能把相关路径算独立alpha。正Sharpe比例={"parent": {"1": 1.0, "2": 1.0, "3": 1.0}}；相邻敏感性边12，启发式警示3条，边界表现仅诊断，不扩网格或改选。
BTC金额轴为750/1000/1250等距；预算窗口8/9/12日间距不均；邻域按事前索引半径1定义。这是有限局部诊断，不代表完整响应面或参数显著性。Sharpe变化警示保持披露，未据此扩网格。

本轮四账户续接120闭合分钟；原日决策{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、资金费{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}。已知Nov21_08三永续此前均已记账，本轮不重复；其他实际事件依freshGET与各自窗口处理。下一SMA/candidate['2026-11-22T20:30:00Z', '2026-11-22T22:30:00Z']、L4/FEWM['2026-11-22T22:10:00Z', '2026-11-23T00:10:00Z']须freshGET、去重并先reserve，不提前记账、不重置、不强平、不采用研究规则；SMA74日背景/原日决策完整核验。

原SMA三倍成本累计-7.468958%，仍为延迟shadow；原10bp与Float核算不变，未采用研究规则，不冒充十策略实盘报价模拟。所有账户尚未达到180日/六折资格。
监控成功=True，展示11536项，旧11532行完整字典保持。实际GET23，传输失败3；工程/读取失败原回执与恢复见read_failures.json。

实际复现命令（已完成模型和账户窗口不得重复计算）：

```sh
cd /home/desktop/Documents/Codex/EquiTide
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/commands.py prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/commands.py freeze
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/commands.py units
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/commands.py bind
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/commands.py reserve_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/commands.py evaluate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/commands.py audit
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/commands.py audit_retry1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/commands.py exports
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/commands.py finish_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/commands.py research_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/commands.py l4h02
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/commands.py fewm
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/commands.py candidate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/commands.py forward
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/commands.py accounts_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/commands.py journal
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/commands.py sources_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/commands.py gates
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/commands.py feed
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/commands.py midnight_prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/commands.py collect
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/commands.py final_checks
```

官方来源、访问UTC和版本内容SHA见primary_source_access.json。本轮已读取永续公开接口文档及[Binance官方只读接口源代码](https://raw.githubusercontent.com/binance/binance-futures-connector-python/main/binance/um_futures/market.py)；行情及资金费以实际公共GET字节和哈希为准。正收益回测不代表稳定实盘盈利。

与同金额、H.02、年龄36小时、S16、成熟M4、资金费预算窗口VW9且趋势斜率K.0075、波动率V6、ROC L5、退出E.0075的已完成结果比较：
BTC N750/VW8：收益差-0.048811pp、整体DD差0.000000pp、Sharpe差0.024299、Calmar差-0.034339；完整NAV同路径=False。
BTC N750/VW12：收益差-0.277962pp、整体DD差0.000000pp、Sharpe差-0.109613、Calmar差-0.195560；完整NAV同路径=False。
BTC N1250/VW8：收益差-0.048811pp、整体DD差0.000000pp、Sharpe差0.019402、Calmar差-0.032513；完整NAV同路径=False。
BTC N1250/VW12：收益差-0.277962pp、整体DD差0.000000pp、Sharpe差-0.087806、Calmar差-0.185163；完整NAV同路径=False。
全部12个逐成本比较见exports/previous_VW9_comparisons.csv；仅比较已完成报告，不重跑旧组件或旧组合。

与同金额VW9的12个逐成本比较：四指标同时改善0项，旧VW9支配8项，完整NAV同路径0项；全成本同旧VW9路径的新图0个。见comparison_scope_review.json。历史门槛状态与比较优劣分别保留；维持事前750/VW8，不据结果换候选，不修改原冻结账户。相关配置和重复历史不构成独立前向或实盘盈利证据。

下一原冻结账户窗口的历史真实结算留证：fundingTime毫秒=[1795392000000]，各自下一窗口待处理记录={"SMA": 0, "candidate": 0, "l4h02": 6, "fewm": 6}。首次捕获UTC=2026-11-23T16:05:46.851318Z及来源SHA保持；本轮未提前入账。下一轮须刷新实际来源、按自身窗口去重并先reserve，再以自身q/成本核算，不复用其他账户金额。详见next_preparation_contract.new_actual_settlement_handoff。

本轮原冻结账户各续接120分钟，无原日决策及成交；实际08:00:00.003三个永续均已按自身窗口入账，本轮不重复；实际16:00资金费三个永续此前均已按自身窗口各记6唯一键，本轮不重复；SMA无永续资金费。Nov22日决策及三个永续实际00:00:00.001资金费均已按自身窗口完成，只读保留各6唯一键，不重复。SMA full74真实现货背景只读、现金/数量/desired/成本不重置。下一SMA/candidate窗口无日决策，L4/FEWM窗口跨Nov23_00:01原日决策；各永续账户资金费以只读实际查询的独立窗口待处理字段为准，未提前入账。下一原日决策UTC Nov23_00:01。

已知Nov21_08:00:00.003三永续此前均已记账一次，本轮不重复；当前资金费记录={"SMA": 0, "candidate": 0, "l4h02": 0, "fewm": 0}。08全链唯一计数各6，首次捕获UTC和原始来源SHA保持；下一窗口继续freshGET与按账户去重，不提前记账。

旧Nov21_16事件三个永续各6个唯一键，本轮旧事件0新增；本轮其他资金费与原日决策成交按自身q/mark/rate/成本逐项重核，十八本现金完整对账。详见actual16_nov21_reconciliation.json，未重跑模型或账户窗口。

本轮只读复核命令（不得重跑已完成金融模型或账户窗口）：

```sh
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/exports.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/component_reuse_review.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/funding_availability_review.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/compare_previous_H.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/review_economic_identity.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/review_sensitivity_axes.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/review_reservation_metadata.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/review_funding_window_economics.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/reconcile_actual08.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/reconcile_actual16.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/complete_midnight_handoff.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/review_next_handoff.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/review_next_settlement_split.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/reconcile_nov22_16.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/review_next_daily_boundary.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/final_notes.py
```

本轮资金费预算波动率窗口最终结论：4个新被动组合均已实际计算并finish，历史通过4、淘汰0；三项验证均已执行。与同BTC金额旧VW9的12个逐成本比较中，完整NAV相同0项、四指标同时改善0项、旧VW9支配8项。保留事前750/VW8，不按已见结果改选；仅重复开发历史，无独立前向或稳定实盘盈利资格。
相邻启发式警示按真实坐标统计={"BTC_ENTRY_TARGET_USDT": 0, "ETH_FUNDING_BUDGET_VOLATILITY_WINDOW_DAYS": 3}；真实入场筛选、成交、净值及损益/成本/资金费差见funding_window_economic_review.json，保留全部逐折/逐成本/连续NAV。
原冻结账户实际Nov22_16：本轮candidate、L4、FEWM均无新增资金费；此前三个账户分别已按自身原q及1/2/3成本各入账6条，不重复。三个永续账户现在各6个唯一资金费键；原先BTC负费率对应各自空头支出且按成本倍增，ETH原q为0；本轮不重复记账。原始fundingTime=1795363200000毫秒、首次捕获UTC2026-11-23T07:58:27.090648Z及SHA24324b8334f9eb1c74153aa29f82fda3a35b8cfdd4448bca421dba74064763c3保持。下一各自窗口待处理={"SMA": 0, "candidate": 0, "l4h02": 6, "fewm": 6}；仅保存准备状态，不提前入账。详见actual16_nov22_reconciliation.json及next_required_Nov22_16_state。

资金费预算机制复核（1倍成本，相同ETH银行）：
VW8相对旧VW9：资金费阻断标志差2天、最终desired差8天；轮数差-1、执行差-2、毛损益差-42.902440 USDT、资金费净额差4.666191 USDT、执行成本差-6.513684 USDT、终值差-31.722565 USDT。差额按原乘数1完整进入父组合，不线性缩放。
VW12相对旧VW9：资金费阻断标志差1天、最终desired差1天；轮数差0、执行差0、毛损益差-49.987890 USDT、资金费净额差-0.750879 USDT、执行成本差-0.052046 USDT、终值差-50.686722 USDT。差额按原乘数1完整进入父组合，不线性缩放。
较短VW8节省交易和成本，但本段历史中少赚的毛损益更大；VW12也未改善净收益。Sharpe与净收益取舍保留在逐成本比较中，不据重复历史改选或替换原冻结账户。
下一原窗口的UTC日决策边界已单独复核：SMA/candidate仍无日决策；L4/FEWM22:10到次日00:10包含Nov23_00:01，须刷新真实闭合日线、实际资金费来源、按自身窗口去重并先reserve，之后才调用原日内核。当前Nov23日决策及该未来结算均未入账。详见next_daily_boundary_verification.json。

审计恢复留档：初次只读审计错误地将资金费预算窗口作为趋势门槛；已保留原失败源audit.py、失败日志及绑定。实际成功核验使用audit_count_recovery.py，恢复上轮逐字节相同的独立policy函数，趋势门槛仍为.0075，资金费预算窗口仍为8/9/12。修复后已实际通过12条新父曲线及全部旧原生信号、成交、资金费、保证金和净值核对，未修改原引擎、spec或首次金融report.json，未重算任何已完成模型或账户。metadata说明脚本的一次失败和实际TLS重试也保留在read_failures.json。后续有效只读审计源及SHA见next_required_effective_audit_source，复现请用该源。

封存前额外只读检查（汇总的旧mark-only断言已按真实下轮日历修复，原失败源及实际恢复回执见closure_metadata_recovery.json）：

```sh
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T153007Z/checks.py final
```
