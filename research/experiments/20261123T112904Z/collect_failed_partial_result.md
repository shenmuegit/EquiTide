# 20261123T112904Z BTC实际入场金额与ETH入场波动率窗口组合验证

事前固定BTC实际原生目标N1000旧/1500/1750 × ETH 入场波动率窗口V5/6旧/7日。ETH固定S16、H=.02、退出E.0075、cap.05625、M4、预算VW9/R=.0075、最大年龄36小时，入场波动率窗口按V轴变化，退出E.0075与趋势门槛K.0075固定；四个新被动父组合分别reserve、计算一次及finish，十个原生银行和八个旧父/持有对照只读；历史通过4/4。预设N1500/V5，不按结果改选。

完整读取41448事件/20585ID和520份结论；初始16项实际结果缺口0。规范研究定义11965→11969，不能将相关路径和历史选择视为独立试验。

固定BTC实际原生入场目标1000旧/1500/1750 × ETH入场波动率窗口V5/6旧/7日，检验更短或更长的入场风险筛选与真实BTC下单金额的组合差异。ETH固定C15000/N4000、ROC L5/H.02/退出E.0075、有限EWM S16 beta15/17/D3/K.0075、波动率上限.05625、成熟M4/年龄1..36h、预算VW9/R.0075；BTC固定C3750、L29/H.03/E.005、V10cap.0275、strictpositiveROC5>.0025。预设1500/V5，不按结果改选。四个新被动组合，十个旧原生银行和八个旧父/持有只读；原银行乘数[1,1]不归一化，本金18750、资本20/80、初始目标5500/5750美元；保留实际LOT/q/非线性冲击/费用/资金费/保证金，不产生父订单、转账、再平衡或跨保证金。

All component signals are read-only actually completed rules:BTC L29H.03E.005,V10cap.0275,strictpositiveROC5>.0025;ETH L5contrarianH.02,exitE.0075,entryV5/6old/7,finiteEWMS16beta15/17,D3K.0075,entryV5/6old/7cap.05625,M4,age1..36h,R.0075,VW9. No new native execution or signal fitting.

原始银行乘数[1,1]不归一化，C3750+15000=18750，资本20/80；本轮目标BTC1500或1750+ETH4000=5500或5750。每个原生组件均已按实际金额计算过LOT数量、非线性成交量冲击、费用、资金费及保证金，直接复用完整净值；父组合对齐共同时间轴相加美元NAV，无新增父订单、转账、再平衡或跨保证金，不线性缩放NAV。

391日为反复使用的开发历史2025-10-19 00:01→2026-11-14 00:01，不能称未触碰最终测试。无拟合标签，实际33闭合上下文日、embargo0；13个完整30日折+1日尾段，近期40日8×5、扩展21日5/5/5/6。折间继承现金/q，全期终点平仓计成本；整体回撤从连续完整NAV计算。

每边手续费5bp、半价差1bp、滑点2bp、0.5×过去20日样本logvol×sqrt(实际订单额/过去20日quoteADV)冲击；不利tick、LOT/最低金额、参与率≤.001。执行成本及实际资金费支出按1/2/3倍，收入不放大。线性永续无现货借币；1倍入场抵押及小时不利价1%维持保证金代理。对比等目标金额的实际持有组合和零息现金。缺L2/TCA、完整tiers、tick清算与容量实证。

|范围|BTC目标USDT|ETH入场波动率窗口V（日）|状态|净收益1/2/3倍%|整体DD3%|Sharpe3|Calmar3|正30日折1倍|近40日正5日折1/2/3|
|---|---|---|---|---|---|---|---|---|---|
|parent|1500|5|passed|11.052304 / 10.382940 / 9.713733|1.534455|2.303143|5.891008|12/13|6/6/6（各/8）|
|parent|1500|7|passed|11.052304 / 10.382940 / 9.713733|1.534455|2.303143|5.891008|12/13|6/6/6（各/8）|
|parent|1750|5|passed|12.030701 / 11.293292 / 10.556054|1.820303|2.267057|5.395126|12/13|6/6/6（各/8）|
|parent|1750|7|passed|12.030701 / 11.293292 / 10.556054|1.820303|2.267057|5.395126|12/13|6/6/6（各/8）|

事前失败判据：全期、近期和扩展各成本为正；1倍≥10/13正月；近期各成本≥6/8正5日折；扩展各成本≥3/4正折；DD3≤25%；邻域正及近期合格均≥60%；≥4次底层平仓；1倍毛损益加资金费/执行成本≥2.5；无拒单/负抵押/保证金代理违规；终点flat。

parent_BTCN1500_ETHlongonlyL5H200M4D3Age36hSlopeK0075ExitE0075V5Cap05625_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1500_ETHlongonlyL5H200M4D3Age36hSlopeK0075ExitE0075V7Cap05625_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1750_ETHlongonlyL5H200M4D3Age36hSlopeK0075ExitE0075V5Cap05625_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。
parent_BTCN1750_ETHlongonlyL5H200M4D3Age36hSlopeK0075ExitE0075V7Cap05625_N4000_raw1_1_C3750_15000_391d：通过预设历史门槛，待独立前向验证。

相同ETH入场波动率窗口和本金，对旧BTC1000中心四指标严格改善父组合0/4。实际损益、资金费和执行成本差见sizing_effect_decomposition.json；全部变体/成本/逐折及连续每日净值见exports/。
完整三成本路径共2种；旧路径重复按NAV_alias_inventory保留披露，不能把相关路径算独立alpha。正Sharpe比例={"parent": {"1": 1.0, "2": 1.0, "3": 1.0}}；相邻敏感性边12，启发式警示3条，边界表现仅诊断，不扩网格或改选。
BTC金额轴为1000/1500/1750，间距不均；邻域按事前索引半径1定义。这是有限局部诊断，不代表完整响应面或参数显著性。Sharpe变化警示保持披露，未据此扩网格。

本轮四账户续接120闭合分钟；原日决策{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、资金费{'SMA': 0, 'candidate': 6, 'l4h02': 0, 'fewm': 0}。已知Nov21_08三永续此前均已记账，本轮不重复；其他实际事件依freshGET与各自窗口处理。下一SMA/candidate['2026-11-22T16:30:00Z', '2026-11-22T18:30:00Z']、L4/FEWM['2026-11-22T18:10:00Z', '2026-11-22T20:10:00Z']须freshGET、去重并先reserve，不提前记账、不重置、不强平、不采用研究规则；SMA74日背景/原日决策完整核验。

原SMA三倍成本累计-7.468958%，仍为延迟shadow；原10bp与Float核算不变，未采用研究规则，不冒充十策略实盘报价模拟。所有账户尚未达到180日/六折资格。
监控成功=True，展示11528项，旧11524行完整字典保持。实际GET20，传输失败0；工程/读取失败原回执与恢复见read_failures.json。

实际复现命令（已完成模型和账户窗口不得重复计算）：

```sh
cd /home/desktop/Documents/Codex/EquiTide
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T112904Z/commands.py prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T112904Z/commands.py freeze
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T112904Z/commands.py units
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T112904Z/commands.py bind
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T112904Z/commands.py reserve_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T112904Z/commands.py evaluate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T112904Z/commands.py audit
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T112904Z/commands.py exports
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T112904Z/commands.py finish_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T112904Z/commands.py research_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T112904Z/commands.py l4h02
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T112904Z/commands.py fewm
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T112904Z/commands.py candidate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T112904Z/commands.py forward
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T112904Z/commands.py accounts_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T112904Z/commands.py journal
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T112904Z/commands.py sources_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T112904Z/commands.py gates
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T112904Z/commands.py feed
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T112904Z/commands.py midnight_prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T112904Z/commands.py collect
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261123T112904Z/commands.py final_checks
```

官方来源、访问UTC和版本内容SHA见primary_source_access.json。本轮已读取现货官方接口文档及[Binance官方只读接口源代码](https://raw.githubusercontent.com/binance/binance-futures-connector-python/main/binance/um_futures/market.py)；行情及资金费以实际公共GET字节和哈希为准。正收益回测不代表稳定实盘盈利。

与同金额、H.02、年龄36小时、S16、成熟M4、预算VW9且趋势斜率门槛K.0075、波动率V6、ROC L5、退出E.0075的已完成结果比较：
