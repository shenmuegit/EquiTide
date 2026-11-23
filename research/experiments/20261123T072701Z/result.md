# 20261123T072701Z BTC实际入场金额与ETHROC回看周期组合验证

事前固定BTC实际原生目标N1000旧/1500/1750 × ETH ROC回看L4/5旧/6。ETH固定S16、H=.02、V6cap.05625、M4、预算VW9/R=.0075、最大年龄36小时，ROC回看按L轴变化，趋势门槛固定K.0075；四个新被动父组合分别reserve、计算一次及finish，十个原生银行和八个旧父/持有对照只读；历史通过4/4。预设N1500/L4，不按结果改选。

完整读取41344事件/20533ID和518份结论；初始16项实际结果缺口0。规范研究定义11957→11961，不能将相关路径和历史选择视为独立试验。

固定BTC实际原生目标1000旧/1500/1750 × ETH已闭合收盘价ROC回看L4/5旧/6日，检验快信号时间尺度变化与较大BTC银行的互补。ETH固定C15000/N4000、H.02/E.0075、有限EWM S16 beta15/17/D3/K.0075、入场V6cap.05625、成熟M4/年龄1..36h、预算VW9/R.0075；BTC固定C3750、L29/H.03/E.005、V10cap.0275、strictpositiveROC5>.0025。预设1500/L4，不按结果改选。四个新被动组合，十个实际旧原生银行和八个旧父/持有只读；原银行乘数[1,1]、本金18750、资本20/80、初始目标5500/5750美元，完整共同轴相加实际旧银行美元NAV，保留原LOT/q/非线性冲击/资金费/保证金，无归一化、父订单、转账、再平衡和跨保证金。

All component signals are read-only actually completed rules:BTC L29H.03E.005,V10cap.0275,strictpositiveROC5>.0025;ETH ROC L4/5old/6contrarianH.02,E.0075,finiteEWMS16beta15/17,D3K.0075,V6cap.05625,M4,age1..36h,R.0075,VW9. No new native execution or signal fitting.

原始银行乘数[1,1]不归一化，C3750+15000=18750，资本20/80；本轮目标BTC1500或1750+ETH4000=5500或5750。每个原生组件均已按实际金额计算过LOT数量、非线性成交量冲击、费用、资金费及保证金，直接复用完整净值；父组合对齐共同时间轴相加美元NAV，无新增父订单、转账、再平衡或跨保证金，不线性缩放NAV。

391日为反复使用的开发历史2025-10-19 00:01→2026-11-14 00:01，不能称未触碰最终测试。无拟合标签，实际33闭合上下文日、embargo0；13个完整30日折+1日尾段，近期40日8×5、扩展21日5/5/5/6。折间继承现金/q，全期终点平仓计成本；整体回撤从连续完整NAV计算。

每边手续费5bp、半价差1bp、滑点2bp、0.5×过去20日样本logvol×sqrt(实际订单额/过去20日quoteADV)冲击；不利tick、LOT/最低金额、参与率≤.001。执行成本及实际资金费支出按1/2/3倍，收入不放大。线性永续无现货借币；1倍入场抵押及小时不利价1%维持保证金代理。对比等目标金额的实际持有组合和零息现金。缺L2/TCA、完整tiers、tick清算与容量实证。

|范围|BTC目标USDT|ETH ROC回看L（日）|状态|净收益1/2/3倍%|整体DD3%|Sharpe3|Calmar3|正30日折1倍|近40日正5日折1/2/3|
|---|---|---|---|---|---|---|---|---|---|
|parent|1500|4|passed|8.698882 / 7.921683 / 7.144281|4.906961|1.489623|1.355984|10/13|6/6/6（各/8）|
|parent|1500|6|passed|7.901755 / 7.323075 / 6.744391|1.793675|1.885706|3.502377|10/13|6/6/6（各/8）|
|parent|1750|4|passed|9.677280 / 8.832035 / 7.986603|5.222781|1.523458|1.423814|10/13|6/6/6（各/8）|
|parent|1750|6|passed|8.880153 / 8.233427 / 7.586712|2.118338|1.852139|3.335080|10/13|6/6/6（各/8）|

事前失败判据：全期、近期和扩展各成本为正；1倍≥10/13正月；近期各成本≥6/8正5日折；扩展各成本≥3/4正折；DD3≤25%；邻域正及近期合格均≥60%；≥4次底层平仓；1倍毛损益加资金费/执行成本≥2.5；无拒单/负抵押/保证金代理违规；终点flat。

parent_BTCN1500_ETHlongonlyL4H200M4D3Age36hSlopeK0075E0075V6Cap05625_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1500_ETHlongonlyL6H200M4D3Age36hSlopeK0075E0075V6Cap05625_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1750_ETHlongonlyL4H200M4D3Age36hSlopeK0075E0075V6Cap05625_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1750_ETHlongonlyL6H200M4D3Age36hSlopeK0075E0075V6Cap05625_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。

相同ETH ROC回看周期和本金，对旧BTC1000中心四指标严格改善父组合0/4。实际损益、资金费和执行成本差见sizing_effect_decomposition.json；全部变体/成本/逐折及连续每日净值见exports/。
完整三成本路径共4种；旧路径重复按NAV_alias_inventory保留披露，不能把相关路径算独立alpha。正Sharpe比例={"parent": {"1": 1.0, "2": 1.0, "3": 1.0}}；相邻敏感性边12，启发式警示3条，边界表现仅诊断，不扩网格或改选。
BTC金额轴为1000/1500/1750，间距不均；邻域按事前索引半径1定义。这是有限局部诊断，不代表完整响应面或参数显著性。Sharpe变化警示保持披露，未据此扩网格。

本轮四账户续接120闭合分钟；原日决策{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、资金费{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}。已知Nov21_08三永续此前均已记账，本轮不重复；其他实际事件依freshGET与各自窗口处理。下一SMA/candidate['2026-11-22T12:30:00Z', '2026-11-22T14:30:00Z']、L4/FEWM['2026-11-22T14:10:00Z', '2026-11-22T16:10:00Z']须freshGET、去重并先reserve，不提前记账、不重置、不强平、不采用研究规则；SMA74日背景/原日决策完整核验。

原SMA三倍成本累计-7.468958%，仍为延迟shadow；原10bp与Float核算不变，未采用研究规则，不冒充十策略实盘报价模拟。所有账户尚未达到180日/六折资格。
监控成功=True，展示11520项，旧11516行完整字典保持。实际GET24，传输失败4；工程/读取失败原回执与恢复见read_failures.json。

实际复现命令（已完成模型和账户窗口不得重复计算）：

```sh
cd /home/desktop/Documents/Codex/EquiTide
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T072701Z/commands.py prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T072701Z/commands.py freeze
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T072701Z/commands.py units
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T072701Z/commands.py bind
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T072701Z/commands.py reserve_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T072701Z/commands.py evaluate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T072701Z/commands.py audit
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T072701Z/commands.py exports
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T072701Z/commands.py finish_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T072701Z/commands.py research_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T072701Z/commands.py l4h02
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T072701Z/commands.py fewm
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T072701Z/commands.py candidate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T072701Z/commands.py candidate_retry1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T072701Z/commands.py candidate_retry2
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T072701Z/commands.py forward
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T072701Z/commands.py accounts_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T072701Z/commands.py journal
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T072701Z/commands.py sources_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T072701Z/commands.py gates
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T072701Z/commands.py feed
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T072701Z/commands.py midnight_prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T072701Z/commands.py collect
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T072701Z/commands.py final_checks
```

官方来源、访问UTC和版本内容SHA见primary_source_access.json。本轮已读取现货官方接口文档及[Binance官方只读接口源代码](https://raw.githubusercontent.com/binance/binance-futures-connector-python/main/binance/um_futures/market.py)；行情及资金费以实际公共GET字节和哈希为准。正收益回测不代表稳定实盘盈利。

与同金额、H.02、年龄36小时、S16、成熟M4、预算VW9且趋势斜率门槛K.0075、波动率V6、ROC L5、退出E.0075的已完成结果比较：
BTC N1500/L4：收益差-2.569451pp、整体DD差3.372506pp、Sharpe差-0.813520、Calmar差-4.535024；完整NAV同路径=False。
BTC N1500/L6：收益差-2.969342pp、整体DD差0.259220pp、Sharpe差-0.417437、Calmar差-2.388631；完整NAV同路径=False。
BTC N1750/L4：收益差-2.569451pp、整体DD差3.402478pp、Sharpe差-0.743599、Calmar差-3.971312；完整NAV同路径=False。
BTC N1750/L6：收益差-2.969342pp、整体DD差0.298035pp、Sharpe差-0.414918、Calmar差-2.060046；完整NAV同路径=False。
全部12个逐成本比较见exports/previous_L5_comparisons.csv；仅比较已完成报告，不重跑旧组件或旧组合。

与同金额L5的12个逐成本比较：四指标同时改善0项，旧L5支配12项，完整NAV同路径0项；全成本同旧L5路径的新图0个。见comparison_scope_review.json。历史门槛状态与比较优劣分别保留；维持事前1500/L4，不据结果换候选，不修改原冻结账户。相关配置和重复历史不构成独立前向或实盘盈利证据。

下一原冻结账户窗口的历史真实结算留证：fundingTime毫秒=[1795363200000]，各自下一窗口待处理记录={"SMA": 0, "candidate": 0, "l4h02": 6, "fewm": 6}。首次捕获UTC=2026-11-23T07:58:27.090648Z及来源SHA保持；本轮未提前入账。下一轮须刷新实际来源、按自身窗口去重并先reserve，再以自身q/成本核算，不复用其他账户金额。详见next_preparation_contract.new_actual_settlement_handoff。

本轮原冻结账户各续接120分钟，无原日决策及成交；candidate、L4和FEWM均已处理实际08:00:00.003资金费各6唯一键，本轮不重复入账；SMA无永续资金费。Nov22日决策及三个永续实际00:00:00.001资金费均已按自身窗口完成，只读保留各6唯一键，不重复。SMA full74真实现货背景只读、现金/数量/desired/成本不重置。下一四窗口均无日决策；各永续账户资金费以只读实际查询的独立窗口待处理字段为准，未提前入账。下一原日决策UTC Nov23_00:01。

原candidate抓取发生两次未登记/未计算的失败：先是3次TLS握手EOF，随后恢复器遇到既有raw目录；均保留原回执和失败目录。成功恢复只对尚未执行的原candidate窗口计算一次，使用独立抓取目录，原核心策略/费用/资金费/保证金代码未变。完全相同URL的两份小时行情复用上轮实际HTTP200字节，保留原捕获UTC和SHA，不算本轮新增GET；本轮已取得分钟页及公开元数据也只读复用。统计中的唯一已保存GET回执含这些真实既往来源，详见candidate_capture_recovery_effective.json。

已知Nov21_08:00:00.003三永续此前均已记账一次，本轮不重复；当前资金费记录={"SMA": 0, "candidate": 0, "l4h02": 0, "fewm": 0}。08全链唯一计数各6，首次捕获UTC和原始来源SHA保持；下一窗口继续freshGET与按账户去重，不提前记账。

旧Nov21_16事件三个永续各6个唯一键，本轮旧事件0新增；本轮其他资金费与原日决策成交按自身q/mark/rate/成本逐项重核，十八本现金完整对账。详见actual16_nov21_reconciliation.json，未重跑模型或账户窗口。

本轮只读复核命令（不得重跑已完成金融模型或账户窗口）：

```sh
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T072701Z/component_reuse_review.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T072701Z/funding_availability_review.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T072701Z/compare_previous_H.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T072701Z/review_economic_identity.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T072701Z/review_sensitivity_axes.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T072701Z/review_reservation_metadata.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T072701Z/review_lookback_economics.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T072701Z/reconcile_actual08.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T072701Z/reconcile_actual16.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T072701Z/complete_midnight_handoff.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T072701Z/review_next_handoff.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T072701Z/review_next_settlement_split.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T072701Z/final_notes.py
```

本轮ROC回看最终结论：4个新被动组合全部实际计算并finish，历史通过4、淘汰0；三项验证均已执行。与同BTC金额的旧L5对照，12个逐成本比较中完整NAV相同0项、四指标同时改善0项。保留事前1500/L4，不按已见结果改选；通过状态只代表历史门槛，不代表独立前向或实盘盈利。
敏感性启发式警示按真实坐标分别统计：{"BTC_ENTRY_TARGET_USDT": 0, "ETH_FAST_ROC_LOOKBACK_DAYS": 3}。实际ETH源银行的信号、最终意向、执行数及损益/资金费/成本差见lookback_economic_review.json；12个新父组合成本场景的差异均与实际ETH银行净值差精确对账。下一原账户窗口实际资金费待处理记录={"SMA": 0, "candidate": 0, "l4h02": 6, "fewm": 6}；首次来源UTC/毫秒时间戳/mark/rate及SHA原样保留，本轮不提前入账。
同金额旧L5在全部12个逐成本比较中支配本轮L4/L6：收益更高，整体回撤更低，Sharpe与Calmar更高。因此保留历史passed记录但不晋级。L4三倍ETH执行18次/9回合，较L5多2回合，毛价差损益下降421.95103 USDT且成本增加37.835304845 USDT；L6执行10次/5回合，省成本40.223445015 USDT及资金费改善10.289752142 USDT，仍不足抵消毛价差损益下降607.26484 USDT。这里只解释实际已存账本，不改原规则，不据结果重新择优。
