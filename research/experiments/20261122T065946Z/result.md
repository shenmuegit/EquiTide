# 20261122T065946Z BTC实际入场金额与ETH成熟资金费样本数验证

事前固定BTC实际原生目标N1000旧/1500/1750 × ETH M2/3/5。ETH固定H=.02、S16/衰减15/17、最大年龄36小时、趋势斜率K=.0075；六个新被动父组合分别reserve、计算一次及finish，十个原生银行和六个旧父/持有对照只读；历史通过6/6。预设N1500/M3，不按结果改选。

完整读取40728事件/20225ID和507份结论；初始16项实际结果缺口0。规范研究定义11901→11907，不能将相关路径和历史选择视为独立试验。

改变ETH新入场资金费过滤所需的最近成熟实际结算样本数M，可能改变carry估计稳定性和缺历史阻拦，并影响与较大BTC银行的互补。事前固定BTC实际目标N1000旧/1500/1750 × ETH M2/3/5；固定ETH C15000/N4000、L5/H.02/E.0075、S16beta15/17/D3/斜率.0075、V6cap.05625、结算年龄1..36h、R.0075/VW9。六个新被动组合，十个旧原生银行及六个旧父/持有只读；另绑定同BTC金额M4两份旧报告比较。预设BTC1500/M3，不按本轮结果改选扩网格。原银行乘数[1,1]、资本3750+15000=18750、20/80、初始目标5500/5750；保持实际原银行q/费用/非线性冲击/资金费/保证金，完整共同轴美元净值相加。

All component signals are read-only actually completed rules:BTC L29H.03E.005,V10cap.0275,strictpositiveROC5>.0025;ETH L5contrarianH.02,E.0075,finiteEWMS16beta15/17,D3K.0075,V6cap.05625,M2/3/5,age1..36h,R.0075,VW9. No new native execution or signal fitting.

原始银行乘数[1,1]不归一化，C3750+15000=18750，资本20/80；本轮目标BTC1500或1750+ETH4000=5500或5750。每个原生组件均已按实际金额计算过LOT数量、非线性成交量冲击、费用、资金费及保证金，直接复用完整净值；父组合对齐共同时间轴相加美元NAV，无新增父订单、转账、再平衡或跨保证金，不线性缩放NAV。

391日为反复使用的开发历史2025-10-19 00:01→2026-11-14 00:01，不能称未触碰最终测试。无拟合标签，实际33闭合上下文日、embargo0；13个完整30日折+1日尾段，近期40日8×5、扩展21日5/5/5/6。折间继承现金/q，全期终点平仓计成本；整体回撤从连续完整NAV计算。

每边手续费5bp、半价差1bp、滑点2bp、0.5×过去20日样本logvol×sqrt(实际订单额/过去20日quoteADV)冲击；不利tick、LOT/最低金额、参与率≤.001。执行成本及实际资金费支出按1/2/3倍，收入不放大。线性永续无现货借币；1倍入场抵押及小时不利价1%维持保证金代理。对比等目标金额的实际持有组合和零息现金。缺L2/TCA、完整tiers、tick清算与容量实证。

|范围|BTC目标USDT|ETH成熟资金费样本M|状态|净收益1/2/3倍%|整体DD3%|Sharpe3|Calmar3|正30日折1倍|近40日正5日折1/2/3|
|---|---|---|---|---|---|---|---|---|---|
|parent|1500|2|passed|10.074460 / 9.446577 / 8.818851|1.534455|2.206086|5.349794|12/13|6/6/6（各/8）|
|parent|1500|3|passed|9.776732 / 9.185515 / 8.594454|1.534455|2.157279|5.214035|11/13|6/6/6（各/8）|
|parent|1500|5|passed|5.409338 / 5.040792 / 4.672237|1.793675|1.525616|2.427913|10/13|6/6/6（各/8）|
|parent|1750|2|passed|11.052857 / 10.356929 / 9.661172|1.820303|2.176365|4.939133|12/13|6/6/6（各/8）|
|parent|1750|3|passed|10.755130 / 10.095867 / 9.436776|1.820303|2.131990|4.824752|11/13|6/6/6（各/8）|
|parent|1750|5|passed|6.387735 / 5.951145 / 5.514558|2.118338|1.526881|2.425771|10/13|6/6/6（各/8）|

事前失败判据：全期、近期和扩展各成本为正；1倍≥10/13正月；近期各成本≥6/8正5日折；扩展各成本≥3/4正折；DD3≤25%；邻域正及近期合格均≥60%；≥4次底层平仓；1倍毛损益加资金费/执行成本≥2.5；无拒单/负抵押/保证金代理违规；终点flat。

parent_BTCN1500_ETHlongonlyH200M2S16D3Age36hSlopeK0075VW9R0075_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1500_ETHlongonlyH200M3S16D3Age36hSlopeK0075VW9R0075_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1500_ETHlongonlyH200M5S16D3Age36hSlopeK0075VW9R0075_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1750_ETHlongonlyH200M2S16D3Age36hSlopeK0075VW9R0075_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1750_ETHlongonlyH200M3S16D3Age36hSlopeK0075VW9R0075_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1750_ETHlongonlyH200M5S16D3Age36hSlopeK0075VW9R0075_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。

相同EWM窗口和本金，对旧BTC1000中心四指标严格改善父组合0/6。实际损益、资金费和执行成本差见sizing_effect_decomposition.json；全部变体/成本/逐折及连续每日净值见exports/。
完整三成本路径共6种；旧路径重复按NAV_alias_inventory保留披露，不能把相关路径算独立alpha。正Sharpe比例={"parent": {"1": 1.0, "2": 1.0, "3": 1.0}}；相邻敏感性边12，启发式警示3条，边界表现仅诊断，不扩网格或改选。
BTC金额轴为1000/1500/1750，间距不均；邻域按事前索引半径1定义。这是有限局部诊断，不代表完整响应面或参数显著性。Sharpe变化警示保持披露，未据此扩网格。

本轮四账户续接120闭合分钟；原日决策{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、资金费{'SMA': 0, 'candidate': 0, 'l4h02': 6, 'fewm': 6}。已知Nov21_08三永续此前均已记账，本轮不重复；其他实际事件依freshGET与各自窗口处理。下一SMA/candidate['2026-11-21T14:30:00Z', '2026-11-21T16:30:00Z']、L4/FEWM['2026-11-21T16:10:00Z', '2026-11-21T18:10:00Z']须freshGET、去重并先reserve，不提前记账、不重置、不强平、不采用研究规则；SMA73日背景只读。

原SMA三倍成本累计-7.468958%，仍为延迟shadow；原10bp与Float核算不变，未采用研究规则，不冒充十策略实盘报价模拟。所有账户尚未达到180日/六折资格。
监控成功=True，展示11466项，旧11460行完整字典保持。实际GET30，传输失败10；工程/读取失败原回执与恢复见read_failures.json。

实际复现命令（已完成模型和账户窗口不得重复计算）：

```sh
cd /home/desktop/Documents/Codex/EquiTide
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T065946Z/commands.py prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T065946Z/commands.py freeze
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T065946Z/commands.py units
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T065946Z/commands.py bind
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T065946Z/commands.py reserve_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T065946Z/commands.py evaluate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T065946Z/commands.py audit
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T065946Z/commands.py exports
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T065946Z/commands.py finish_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T065946Z/commands.py research_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T065946Z/commands.py l4h02
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T065946Z/commands.py fewm
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T065946Z/commands.py candidate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T065946Z/commands.py forward
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T065946Z/commands.py accounts_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T065946Z/commands.py journal
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T065946Z/commands.py sources_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T065946Z/commands.py gates
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T065946Z/commands.py feed
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T065946Z/commands.py midnight_prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T065946Z/commands.py collect
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T065946Z/commands.py final_checks
```

官方来源和访问UTC见primary_source_access.json：[Binance市场数据文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)。正收益回测不代表稳定实盘盈利。

原Nov21日决策与已知00/08资金费均此前处理，本轮按各自实际窗口核验，未重复、未提前记账。下一原日决策Nov22_00:01，当前与下一窗口仍在其之前，原SMA73日背景只读。

Nov20_16三永续此前均已各记一次，本轮各0条；三永续唯一计数均6。首捕获UTC=2026-11-21T05:15:47.350340Z及原始毫秒/mark/rate保持。下一SMA/candidateNov21 14:30→16:30、L4/FEWM16:10→18:10（四原账户均已处理原Nov21日决策/资金费），须新鲜查询实际事件，不重复已记16，不提前记账。

与同金额、M4、H.02、年龄36小时且固定EWM窗口S16的已完成结果比较：
BTC N1500/M2：收益差-0.894882pp、整体DD差0.000000pp、Sharpe差-0.097057、Calmar差-0.541214；完整NAV同路径=False。
BTC N1500/M3：收益差-1.119278pp、整体DD差0.000000pp、Sharpe差-0.145864、Calmar差-0.676972；完整NAV同路径=False。
BTC N1500/M5：收益差-5.041496pp、整体DD差0.259220pp、Sharpe差-0.777527、Calmar差-3.463095；完整NAV同路径=False。
BTC N1750/M2：收益差-0.894882pp、整体DD差0.000000pp、Sharpe差-0.090692、Calmar差-0.455992；完整NAV同路径=False。
BTC N1750/M3：收益差-1.119278pp、整体DD差0.000000pp、Sharpe差-0.135067、Calmar差-0.570373；完整NAV同路径=False。
BTC N1750/M5：收益差-5.041496pp、整体DD差0.298035pp、Sharpe差-0.740176、Calmar差-2.969354；完整NAV同路径=False。
全部18个逐成本比较见exports/previous_M4_comparisons.csv；仅比较已完成报告，不重跑旧组件或旧组合。

与同金额M4的18个逐成本比较：四指标同时改善0项，旧M4支配18项，完整NAV同路径0项；全成本同旧M4路径的新图0个。见comparison_scope_review.json。历史门槛状态与比较优劣分别保留；维持事前1500/M3，不据结果换候选，不修改原冻结账户。相关配置和重复历史不构成独立前向或实盘盈利证据。

下一原冻结账户窗口的历史真实结算留证：fundingTime毫秒=[1795276800000]，各自下一窗口待处理记录={"SMA": 0, "candidate": 6, "l4h02": 0, "fewm": 0}。首次捕获UTC=2026-11-22T05:30:01.859371Z及来源SHA保持；本轮未提前入账。下一轮须刷新实际来源、按自身窗口去重并先reserve，再以自身q/成本核算，不复用其他账户金额。详见next_preparation_contract.new_actual_settlement_handoff。

成熟样本审计：M2、M3全部391个决策均有足够历史；M5在年龄1..36小时内每次仅4个样本，391/391次不足，全部成本场景ETH开仓0。故M5父组合的正收益来自BTC银行，不能解释为ETH新增贡献或独立alpha。旧M5原生spec的persistence文字保留了M4旧描述，实际结构化entry_funding_settlement_count=5及完整逐日policy_audit已独立核验；本轮父组合按实际组件及结构化参数登记，旧文件和冻结spec/金融报告均未改写，说明见source_policy_prose_review.json。六个新组合对旧同金额M4的三成本18行均无优势，不提升新候选，不修改冻结账户。

已知Nov21_08:00:00.003三永续此前均已记账一次，本轮不重复；当前资金费记录={"SMA": 0, "candidate": 0, "l4h02": 6, "fewm": 6}。08全链唯一计数各6，首次捕获UTC和原始来源SHA保持；下一窗口继续freshGET与按账户去重，不提前记账。

实际Nov21_16:00:00.000本轮仅L4、FEWM各记6条（两币种×三成本），candidate未覆盖记0；各自原持仓逐笔计算，BTC空头收入不随成本倍数放大，ETH零仓亦保留零记录。首次来源UTC2026-11-22T05:30:01.859371Z及SHA不变。下一candidate14:30→16:30尚需6条，L4/FEWM16:10→18:10需0条；须freshGET/去重/先reserve，不提前记账。

下一窗口来源初查因本地127.0.0.1:7890代理不可用连续6次失败，验证证书的直接连接又有2次TLS重置；代理恢复后2次公共GET均成功，首次UTC/来源SHA未改。另有候选获取中2次TLS失败后恢复。本轮共30个真实GET尝试、10次失败均保存，失败和恢复命令见next_source_recovery_native_receipts.json。仅恢复只读下一窗口来源，无模型或已完成账户窗口重跑；下一次仍须新鲜查询后reserve。

本轮只读复核命令（不得重跑已完成金融模型或账户窗口）：

```sh
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T065946Z/component_reuse_review.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T065946Z/funding_availability_review.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T065946Z/compare_previous_H.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T065946Z/review_economic_identity.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T065946Z/reconcile_actual08.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T065946Z/reconcile_actual16.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T065946Z/review_next_handoff.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261122T065946Z/final_notes.py
```

首次封存因复制模板保留上轮下一窗口的断言失败（实际退出1）。账户报告与本轮预登记窗口正确；保留seal_initial_failure.json、原源码文本和日志，仅将封存断言改为从本轮截止时间推导下一两小时。未改策略spec、金融报告、账本、冻结规则或重跑已完成计算。

第二次封存因更正代码把startup字典变量start覆盖为窗口字符串失败（退出1）；失败源码/日志保留。已改用window_start_utc/window_end_utc，并直接核验下一窗口与startup字典均保持正确。未改金融结果或账户，不重跑已完成模型/窗口。
