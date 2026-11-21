# 20261121T104930Z BTC真实组件入场金额与ETH较高反转门槛成熟资金费数的新组合

本轮结论：12个新组合均通过事前历史门槛，passed状态保留；但相同本金/金额/M下，高门槛2.25%的三倍成本收益比旧2%低3.747992–4.642874个百分点，整体DD高0.037608–0.227450个百分点，因此没有形成更优替代，不改变原观察账户。该比较仅诊断，不改事前通过标准。

事前固定BTC原生目标750/1000旧/1125/1250/1375 USDT × ETH成熟数M4/5/6，共15格；1000行3格只读，新增12个被动组件图，全部先reserve、评估一次并finish。历史门槛通过12/12。预设1125/M5未按结果改选；新原生策略运行0次，14个真实原生银行与8个旧父组合只读。

完整读取登记40144事件/19933ID及497份结论，初始16项实际结果缺口0。规范研究定义11829→11841，不是独立试验数。

原始银行乘数[1,1]不归一化。本金BTC3750+ETH15000=18750，资本20/80；初始目标总额4750..5375 USDT。BTC不同金额来源是之前分别执行过的真实LOT/数量、费用、成交量冲击、资金费与保证金账本，不是把BTC1000的NAV或数量按比例缩放。ETH固定C15000/N4000及反转门槛2.25%，仅M4/5/6来源不同。无父订单、转账、再平衡或跨保证金。

All component signals are read-only actually completed rules:BTC L29H.03E.005,V10cap.0275,strictpositiveROC5>.0025;ETH L5contrarianH.0225,E.0075,finiteEWMS16beta15/17,D3K.0075,V6cap.05625,M4/5/6,age1..48h,R.0075,VW9. No new native execution or signal fitting.

验证范围为反复使用的391日开发历史2025-10-19 00:01→2026-11-14 00:01；不是未触碰最终测试。无拟合/标签、33个闭合上下文日、embargo0，13完整30日折+1日尾段；近期40日8×5，扩展21日5/5/5/6。折间继承现金/q，末端计费平仓，用连续完整NAV计算整体回撤。少数旧spec的warmup30/embargo3/完整折12是旧非执行描述，实际原生账本和独立审计按上述时间轴核对，旧记录不改。

每边5bp手续费、1bp半价差、2bp滑点、0.5×过去20日样本logvol×sqrt(实际订单额/过去20日quoteADV)的冲击，不利tick/LOT/最低金额/参与率≤.001；实际资金费及1/2/3倍执行成本与资金费支出压力，收入不放大。线性永续无现货借币；1倍抵押入场及1%小时不利价维持保证金代理。匹配实际金额的持有组合和零利息现金作为对照。缺L2/TCA、完整历史tiers、tick级清算和容量实证。

相同M、相同资本与ETH金额，对BTC1000旧组合的四指标严格改善0/12。提高BTC目标可能同时提高收益和回撤；实际价格损益/资金费/执行成本差逐项核对，ETH差额为0，见sizing_effect_decomposition.json。

|BTC真实目标USDT|ETH成熟M|状态|净收益1/2/3倍%|整体DD3%|Sharpe3|Calmar3|正30日折1倍|近40日正5日折1/2/3|
|---|---|---|---|---|---|---|---|---|
|750|4|passed|3.176299 / 2.898735 / 2.621162|1.358397|1.446281|1.799733|10/13|6/6/6（各/8）|
|750|5|passed|3.176299 / 2.898735 / 2.621162|1.358397|1.446281|1.799733|10/13|6/6/6（各/8）|
|750|6|passed|3.883814 / 3.560952 / 3.238082|1.358397|1.466151|2.222873|10/13|6/6/6（各/8）|
|1125|4|passed|4.716664 / 4.339627 / 3.962582|1.404242|1.536204|2.630800|10/13|6/6/6（各/8）|
|1125|5|passed|4.716664 / 4.339627 / 3.962582|1.404242|1.536204|2.630800|10/13|6/6/6（各/8）|
|1125|6|passed|5.424178 / 5.001844 / 4.579502|1.404242|1.570397|3.039773|10/13|6/6/6（各/8）|
|1250|4|passed|5.145973 / 4.732765 / 4.319529|1.543441|1.526926|2.608841|10/13|6/6/6（各/8）|
|1250|5|passed|5.145973 / 4.732765 / 4.319529|1.543441|1.526926|2.608841|10/13|6/6/6（各/8）|
|1250|6|passed|5.853488 / 5.394983 / 4.936449|1.543441|1.565664|2.980846|10/13|6/6/6（各/8）|
|1375|4|passed|5.582742 / 5.141259 / 4.699787|1.664786|1.528578|2.631285|10/13|6/6/6（各/8）|
|1375|5|passed|5.582742 / 5.141259 / 4.699787|1.664786|1.528578|2.631285|10/13|6/6/6（各/8）|
|1375|6|passed|6.290256 / 5.803476 / 5.316707|1.664786|1.572285|2.976092|10/13|6/6/6（各/8）|

失败判据事前固定：全期、近期与扩展段各成本为正；1倍≥10/13正月；近期各成本≥6/8正5日折；扩展各成本≥3/4正折；DD3≤25%；邻域正及近期合格≥60%；≥4次底层平仓；1倍毛损益加资金费/执行成本≥2.5；无拒单/负抵押/保证金代理违规；终点flat。

parent_BTCN750_ETHlongonlyH225M4Age48h_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，独立前向验证待完成。
parent_BTCN750_ETHlongonlyH225M5Age48h_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，独立前向验证待完成。
parent_BTCN750_ETHlongonlyH225M6Age48h_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，独立前向验证待完成。
parent_BTCN1125_ETHlongonlyH225M4Age48h_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，独立前向验证待完成。
parent_BTCN1125_ETHlongonlyH225M5Age48h_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，独立前向验证待完成。
parent_BTCN1125_ETHlongonlyH225M6Age48h_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，独立前向验证待完成。
parent_BTCN1250_ETHlongonlyH225M4Age48h_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，独立前向验证待完成。
parent_BTCN1250_ETHlongonlyH225M5Age48h_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，独立前向验证待完成。
parent_BTCN1250_ETHlongonlyH225M6Age48h_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，独立前向验证待完成。
parent_BTCN1375_ETHlongonlyH225M4Age48h_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，独立前向验证待完成。
parent_BTCN1375_ETHlongonlyH225M5Age48h_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，独立前向验证待完成。
parent_BTCN1375_ETHlongonlyH225M6Age48h_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，独立前向验证待完成。

相邻敏感性边22，启发式Sharpe悬崖=[{"scope": "parent", "from": "parent_BTCN750_ETHlongonlyH225M4Age48h_N4000_raw1_1_C3750_15000_391d", "to": "parent_ETH_EntryH0p0225_V6L5E0p0075_EWMS16D3_FundingM4Age48hR0p0075_N4000_BTCN1000_C3750_15000_391d", "delta_net_pp": 0.9320553906216, "delta_sharpe": 0.07244488231124313, "delta_DD_pp": 0.037974301449750225, "delta_Calmar": 0.5728966883723119}, {"scope": "parent", "from": "parent_BTCN750_ETHlongonlyH225M5Age48h_N4000_raw1_1_C3750_15000_391d", "to": "parent_ETH_EntryH0p0225_V6L5E0p0075_EWMS16D3_FundingM5Age48hR0p0075_N4000_BTCN1000_C3750_15000_391d", "delta_net_pp": 0.9320553906216, "delta_sharpe": 0.07244488231124313, "delta_DD_pp": 0.037974301449750225, "delta_Calmar": 0.5728966883723119}, {"scope": "parent", "from": "parent_BTCN750_ETHlongonlyH225M6Age48h_N4000_raw1_1_C3750_15000_391d", "to": "parent_ETH_EntryH0p0225_V6L5E0p0075_EWMS16D3_FundingM6Age48hR0p0075_N4000_BTCN1000_C3750_15000_391d", "delta_net_pp": 0.9320553906215778, "delta_sharpe": 0.0838156777693857, "delta_DD_pp": 0.037974301449750225, "delta_Calmar": 0.5611427191947547}]；边界最优仅诊断，不按结果扩网格。全部净收益、DD、Sharpe和Calmar见exports/。
12定义有8种完整三档成本路径，与选定旧对照的重复按NAV_alias_inventory披露；组件与路径共用，不能算独立alpha。核对只读原生42条与新父组合36条成本曲线；旧父组合24条，原生新执行0次。

本轮四账户各续接120闭合分钟；原日决策数{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、成交数{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、实际新增资金费记录{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}，逐笔核对原现金/数量/费用及完整NAV。Nov20原日决策和三永续实际00:00:00.001资金费均在本轮前处理完毕；三永续实际08资金费此前均已各记一次；本轮按各自新窗口完整查询，只处理实际新事件，不重复，不复制其他账户金额。SMA复用真实full72 SPOT权威和原Float记账，只增加分钟估值。下一SMA/candidate['2026-11-20T18:30:00Z', '2026-11-20T20:30:00Z']、L4/FEWM['2026-11-20T20:10:00Z', '2026-11-20T22:10:00Z']均仅mark并查询实际新资金费；所有账户下一日决策Nov21_00:01。不重置、不强制平仓、不采用研究配置。

原SMA三倍成本累计-7.468958%，仍为延迟shadow，原10bp每边费用及Float核算保持，未采用研究5bp/LOT规则；新研究与十策略实盘报价模拟记录分开，均未下真实订单。180日/六折资格尚未成熟。
只读监控生成成功=True，研究行11400，旧行11388完整字典一致。真实GET回执20，已观察传输失败0，失败原始包及恢复见read_failures.json。

实际阶段复现命令（已完成策略、组合及账户窗口不得重复计算）：

```sh
cd /home/desktop/Documents/Codex/EquiTide
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T104930Z/commands.py prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T104930Z/commands.py freeze
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T104930Z/commands.py units
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T104930Z/commands.py bind
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T104930Z/commands.py reserve_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T104930Z/commands.py reserve_1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T104930Z/commands.py evaluate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T104930Z/commands.py audit
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T104930Z/commands.py exports
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T104930Z/commands.py finish_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T104930Z/commands.py finish_1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T104930Z/commands.py research_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T104930Z/commands.py l4h02
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T104930Z/commands.py fewm
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T104930Z/commands.py candidate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T104930Z/commands.py forward
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T104930Z/commands.py accounts_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T104930Z/commands.py journal
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T104930Z/commands.py sources_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T104930Z/commands.py gates
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T104930Z/commands.py feed
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T104930Z/commands.py midnight_prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T104930Z/commands.py collect
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T104930Z/commands.py final_checks
```

官方来源和访问UTC见primary_source_access.json：[Binance资金费与市场数据文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)。数据SHA256、实际来源、独立核算和代码均保留；正收益历史回测不代表稳定实盘盈利。

固定评估完成后的只读诊断：与上轮BTC相同金额、ETH相同M及本金的2%门槛旧结果比较，未重跑旧配置，也未改本轮门槛。三档成本网格正Sharpe比例={"1": 1.0, "2": 1.0, "3": 1.0}；12组逐成本收益与整体DD差见lower_hurdle_readonly_comparison.json。该比较不是事前通过条件，不据此改选。

Nov20原跨日已完成：三永续实际00:00:00.001资金费均恰好记一次，四账户原00:01日决策均已处理；首捕获UTC=2026-11-20T13:12:16.739946Z保持。下一SMA/candidate16:30→18:30、L4/FEWM18:10→20:10仅mark并先查询实际新资金费，下一原日决策Nov21 00:01，SMA保留真实SPOT full72。不预记未来事件。

Nov20_16三永续此前均已各记一次，本轮各0条；三永续唯一计数均6。首捕获UTC=2026-11-21T05:15:47.350340Z及原始毫秒/mark/rate保持。下一SMA/candidate18:30→20:30、L4/FEWM20:10→22:10，须新鲜查询实际事件，不重复已记16，不提前记账。

本轮仅评估12个新被动组合，复用14个实际完成的原生银行与8个旧父组合。BTC入场金额750/1125/1250/1375与ETH成熟数M4/5/6为两轴；BTC1000为旧对照。H2.25%、V6上限5.625%、E.0075、VW9固定；原始银行权重[1,1]及本金20/80不归一化，不缩放净值，不重跑原生模型。M4/M5/M6是成熟实际资金费记录条数。实际结构化参数、每条已保存政策决策及原生现金流已独立核对；见funding_policy_metadata_review.json与verification.json。原有仓位不会因vol或funding入口门槛变化被强平或改量。

Nov20实际08:00资金费的三永续唯一计数均为6，本轮不重复；原首捕获UTC=2026-11-20T21:14:36.626765Z保持。下一窗口的实际资金费首次来源、精确毫秒时间和待入账分配保存在next_required_settlement_binding_state；必须重新查询和去重，当前只读准备不提前入账；原SMA继续使用full72真实SPOT权威，下一原日决策Nov21_00:01。详见next_required_settlement_binding_state。

本轮额外实际只读复核命令（已完成市场回测和账户窗口不得重复执行）：

```sh
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T104930Z/funding_availability_review.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T104930Z/component_reuse_review.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T104930Z/review_economic_identity.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261121T104930Z/final_notes.py
```
