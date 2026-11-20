# 20261120T124414Z ETH成熟资金费条数与BTC入场金额验证

事前冻结ETH M4/5/6 × BTC目标750/1000/1250完整3×3网格；M4及其3个父组合只读，M2/M3旧组件也只读。新增2个ETH原生配置和6个组合全部先reserve后实际计算一次并finish。历史父组合通过6/6、ETH原生通过0/2；全部负收益/零交易/淘汰结果保留。事前代表M5/BTC1000不按结果改变。与同BTC金额的旧M4对照严格同时改善收益、整体DD、Sharpe、Calmar为0/6。

完整读取39404条事件、19563个ID、486份结论及29份附加材料。初始16项实际回测缺口0。规范研究定义11701→11709，正式有结果11496；多重历史选择和相关路径不等于独立试验，无DSR/PBO显著性证明。

本金：BTC3750、ETH15000、合计18750，原始银行权重[1,1]不归一化，20/80仅为初始本金占比。ETH入场目标4000固定，BTC750/1000/1250使初始总目标4750/5000/5250；不是固定实际动态敞口。ETH轴是所需成熟结算条数，年龄仍为1–36小时、保守延迟1小时；普通8小时结算在日信号时可能只有4条合格记录。历史不足仅阻止新/反向入场，不阻止原持仓退出；零交易是已实际评估的现金fallback结果，不解释为策略收益。

10个已有原生银行与6个已有父组合只读复用；2个新ETH模型实际重算信号、数量、成本、资金费、保证金代理。四个核心会计/行情文件字节一致，引擎仅把允许M域增加5/6。父组合在共同完整事件轴逐点相加美元NAV，无父订单、再平衡、转账、跨保证金或线性缩放。旧父标量与真实组件不一致时按子spec和源NAV哈希解释，原证据不改写。

完整规则：BTC unchanged original L29/H.03/E.005/V10cap.0275 and strictdirection*completedROC5>.0025,retainedsame-directionquantity;actualoldC3750/N750/1000/1250 banks readonly. ETHlongonly L5/H.02/E.0075,finiteEWMS16beta15/17/D3K.0075,V6cap.05625,carry median of latestM4old/5/6 genuinely matured realizedsettlements,conservative1h availabilitydelay and ages1..36h inclusive;budgetmin(.0002,.0075*pastVW9samplelogvol*latestactualpastintervalhours/24). Missing requiredM observations blocks only new/reversed entry;retainedpositions/exits unaffected. No fit/labels/future rate.

391日反复使用的开发历史，2025-10-19 00:01→2026-11-14 00:01，33个闭合上下文日；固定规则无拟合/标签，purge不适用、标签embargo0。13个完整30日折+1日尾段，近40日8×5日、扩展21日5/5/5/6。跨折继承现金/q，原终点计费平仓，整体回撤由连续完整NAV计算。不能称未触碰最终测试集、独立未来验证或稳定实盘盈利。

1/2/3倍成本：每边5bp手续费+1bp半价差+2bp滑点+0.5×过去20日样本对数波动×sqrt(实际订单额/过去20日quoteADV)；不利tick/LOT/最低金额/参与率≤0.001，完全抵押1倍入场和小时不利价1%维持保证金代理。真实永续资金费支出加倍、收入不放大，线性永续无现货借币。缺L2/TCA、完整阶梯、tick清算及容量实证。

|范围|ETH M|BTC/ETH目标|状态|净收益1/2/3倍 %|整体DD3 %|Sharpe3|Calmar3|正30日折1倍|近40日正5日折1/2/3|
|---|---|---|---|---|---|---|---|---|---|
|native|5|—/4000|rejected|0.000000 / 0.000000 / 0.000000|0.000000|未定义|未定义|0/13|0/0/0（各/8）|
|native|6|—/4000|rejected|0.000000 / 0.000000 / 0.000000|0.000000|未定义|未定义|0/13|0/0/0（各/8）|
|parent|5|750/4000|passed|2.574494 / 2.398521 / 2.222540|0.847415|1.525739|2.446532|10/13|6/6/6（各/8）|
|parent|5|1000/4000|passed|3.646041 / 3.400311 / 3.154595|1.215308|1.540471|2.420599|10/13|6/6/6（各/8）|
|parent|5|1250/4000|passed|4.544168 / 4.232552 / 3.920907|1.543441|1.523293|2.368393|10/13|6/6/6（各/8）|
|parent|6|750/4000|passed|2.574494 / 2.398521 / 2.222540|0.847415|1.525739|2.446532|10/13|6/6/6（各/8）|
|parent|6|1000/4000|passed|3.646041 / 3.400311 / 3.154595|1.215308|1.540471|2.420599|10/13|6/6/6（各/8）|
|parent|6|1250/4000|passed|4.544168 / 4.232552 / 3.920907|1.543441|1.523293|2.368393|10/13|6/6/6（各/8）|

预设门槛：全期/近期各成本正、1倍≥10/13正完整30日折、近40日各成本≥6/8正5日折、扩展各成本≥3/4正折、整体DD3≤25%、邻域正收益及近期合格比例≥60%、≥4次底层平仓、1倍(毛价差收益+资金费)/费用≥2.5；无拒单、负抵押和保证金代理违规，原终点flat。原生ETH邻域1维，父组合2维；全部实际失败判据如下。

ETH_longonly_L5H0p02E0p0075_EWMS16D3K0p0075_V6Cap0p05625_M5BudgetVW9R0p0075_C15000_N4000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
ETH_longonly_L5H0p02E0p0075_EWMS16D3K0p0075_V6Cap0p05625_M6BudgetVW9R0p0075_C15000_N4000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_ETHFundingM5_N4000_BTCN750_C3750_15000_391d：通过预设历史门槛，独立未来验证未完成。
parent_ETHFundingM5_N4000_BTCN1000_C3750_15000_391d：通过预设历史门槛，独立未来验证未完成。
parent_ETHFundingM5_N4000_BTCN1250_C3750_15000_391d：通过预设历史门槛，独立未来验证未完成。
parent_ETHFundingM6_N4000_BTCN750_C3750_15000_391d：通过预设历史门槛，独立未来验证未完成。
parent_ETHFundingM6_N4000_BTCN1000_C3750_15000_391d：通过预设历史门槛，独立未来验证未完成。
parent_ETHFundingM6_N4000_BTCN1250_C3750_15000_391d：通过预设历史门槛，独立未来验证未完成。

与同BTC目标的M4旧父组合（三倍成本）：
M5/BTC750：收益差-5.041496个百分点、整体DD差-0.473374个百分点、Sharpe差-0.773565、Calmar差-2.675432。
M5/BTC1000：收益差-5.041496个百分点、整体DD差-0.142526个百分点、Sharpe差-0.802479、Calmar差-3.199247。
M5/BTC1250：收益差-5.041496个百分点、整体DD差0.149944个百分点、Sharpe差-0.800834、Calmar差-3.618174。
M6/BTC750：收益差-5.041496个百分点、整体DD差-0.473374个百分点、Sharpe差-0.773565、Calmar差-2.675432。
M6/BTC1000：收益差-5.041496个百分点、整体DD差-0.142526个百分点、Sharpe差-0.802479、Calmar差-3.199247。
M6/BTC1250：收益差-5.041496个百分点、整体DD差0.149944个百分点、Sharpe差-0.800834、Calmar差-3.618174。

全部导出行数：{"costs": 72, "walk_forward_folds": 1008, "recent40_folds": 576, "extension21_folds": 288, "daily_NAV": 28224, "joint_sensitivity": 72, "matched_hold_comparisons": 27, "adjacent_sensitivity_edges": 14}；相邻边14条。启发式Sharpe跳变边=[{"scope": "parent", "from": "parent_independentEntry_BTCN750_ETHN4000_Cap0p05625_C3750_15000_391d", "to": "parent_ETHFundingM5_N4000_BTCN750_C3750_15000_391d", "delta_net_pp": -5.041496184072214, "delta_sharpe": -0.7735647865082937, "delta_DD_pp": -0.47337431895658755, "delta_Calmar": -2.675432040133335}, {"scope": "parent", "from": "parent_ETHEntryRiskV6Cap0p05625BudgetVW9R0p0075_BTCH0p03Confirm5Min0p0025_391d", "to": "parent_ETHFundingM5_N4000_BTCN1000_C3750_15000_391d", "delta_net_pp": -5.041496184072213, "delta_sharpe": -0.8024794915078406, "delta_DD_pp": -0.14252611380617397, "delta_Calmar": -3.1992471547902537}, {"scope": "parent", "from": "parent_BTC_N1250_ETHCap0p05625_C3750_15000_ETHN4000_391d", "to": "parent_ETHFundingM5_N4000_BTCN1250_C3750_15000_391d", "delta_net_pp": -5.041496184072236, "delta_sharpe": -0.8008344069826945, "delta_DD_pp": 0.149943584500134, "delta_Calmar": -3.6181744540867666}]。新8定义共有4种完整成本路径，0组匹配当前旧对照；定义数不是独立信息。
成熟记录/新入场可用性只读复核：[{"fingerprint": "1267addf6253ef522513cbbee7477b99c39c4cd0e5c0f2543f71eac8a1265fd9", "ETH_M": 5, "cost": 1, "daily_decisions": 391, "required_mature_history_available": 0, "required_mature_history_unavailable": 391, "new_or_reversed_requests_before_funding": 23, "funding_gate_blocked_requests": 23, "actual_executions": 0, "actual_net_return_pct": 0.0, "actual_sharpe": null, "actual_cost_usdt": 0.0, "actual_status": "rejected"}, {"fingerprint": "1267addf6253ef522513cbbee7477b99c39c4cd0e5c0f2543f71eac8a1265fd9", "ETH_M": 5, "cost": 2, "daily_decisions": 391, "required_mature_history_available": 0, "required_mature_history_unavailable": 391, "new_or_reversed_requests_before_funding": 23, "funding_gate_blocked_requests": 23, "actual_executions": 0, "actual_net_return_pct": 0.0, "actual_sharpe": null, "actual_cost_usdt": 0.0, "actual_status": "rejected"}, {"fingerprint": "1267addf6253ef522513cbbee7477b99c39c4cd0e5c0f2543f71eac8a1265fd9", "ETH_M": 5, "cost": 3, "daily_decisions": 391, "required_mature_history_available": 0, "required_mature_history_unavailable": 391, "new_or_reversed_requests_before_funding": 23, "funding_gate_blocked_requests": 23, "actual_executions": 0, "actual_net_return_pct": 0.0, "actual_sharpe": null, "actual_cost_usdt": 0.0, "actual_status": "rejected"}, {"fingerprint": "eded818583cd65a3261fd95488e9429a1d8fbc98c7c7a6db4d910f97434a0e15", "ETH_M": 6, "cost": 1, "daily_decisions": 391, "required_mature_history_available": 0, "required_mature_history_unavailable": 391, "new_or_reversed_requests_before_funding": 23, "funding_gate_blocked_requests": 23, "actual_executions": 0, "actual_net_return_pct": 0.0, "actual_sharpe": null, "actual_cost_usdt": 0.0, "actual_status": "rejected"}, {"fingerprint": "eded818583cd65a3261fd95488e9429a1d8fbc98c7c7a6db4d910f97434a0e15", "ETH_M": 6, "cost": 2, "daily_decisions": 391, "required_mature_history_available": 0, "required_mature_history_unavailable": 391, "new_or_reversed_requests_before_funding": 23, "funding_gate_blocked_requests": 23, "actual_executions": 0, "actual_net_return_pct": 0.0, "actual_sharpe": null, "actual_cost_usdt": 0.0, "actual_status": "rejected"}, {"fingerprint": "eded818583cd65a3261fd95488e9429a1d8fbc98c7c7a6db4d910f97434a0e15", "ETH_M": 6, "cost": 3, "daily_decisions": 391, "required_mature_history_available": 0, "required_mature_history_unavailable": 391, "new_or_reversed_requests_before_funding": 23, "funding_gate_blocked_requests": 23, "actual_executions": 0, "actual_net_return_pct": 0.0, "actual_sharpe": null, "actual_cost_usdt": 0.0, "actual_status": "rejected"}]
不按收益扩网格或替换代表。保持36小时年龄边界时提高M，可能只是让策略退回现金；现金fallback不是新的收益来源。
独立核验新原生6条、父18条成本曲线及2346个新政策决策；只读原生30条、父18条及11730个旧政策决策。真实资金费、成交/费用、小时风险及连续NAV均已核对。货币现金流对照见sizing_effect_decomposition.json。

本轮四账户各续接120个闭合分钟，日决策{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}；实际资金费记录{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}。本轮各永续只处理当前各自窗口实际新增结算，不重复旧08:00:00.002资金费。各账户现金变化逐笔核对，持仓/desired/入场价/累计执行费用保持。完整71日SPOT权威及原70精确前缀只读，分钟包不是日线权威。首08来源UTC保持2026-11-19T20:40:54.314631Z，实际fundingTime1795075200002不替换为名义整点；目前三永续均恰好记08一次。下一SMA/candidate['2026-11-19T20:30:00Z', '2026-11-19T22:30:00Z']，L4/FEWM['2026-11-19T22:10:00Z', '2026-11-20T00:10:00Z']，均不重复08，先查询实际特殊资金费；下一日决策Nov20_00:01。不重置本金、不强制平仓、不采用新研究配置。

原SMA三倍成本累计-7.468958%；原账户为延迟shadow、180日/六折资格未成熟；十策略只读汇总，未改冻结规则/本金/持仓或生成新成交。
捕获数据适配器GET回执23，本轮23、旧复用0，可观察运输错误1。来源网页访问单独见primary_source_access.json，不推断未捕获的网络内部细节。真实失败事实：[{"type": "readonly_diagnostic_generator_syntax_error", "recorded_utc": "2026-11-20T13:03:49.843936+00:00", "native_chunk_id": "0668dd", "native_exit_code": 1, "observed_stderr": "SyntaxError: Generator expression must be parenthesized", "scope": "Inline read-only search diagnostic; Python failed at parse before any file access/writes or financial/account calculations.", "resolved": true, "resolution": "Corrected read-only search executed successfully in this diagnostic; all completed creators,financial reports and accounts unchanged."}, {"asset": "ETH", "kind": "funding", "url": "https://fapi.binance.com/fapi/v1/fundingRate?symbol=ETHUSDT&startTime=1795126200000&endTime=1795133460000&limit=1000", "started_utc": "2026-11-20T13:12:08.055285Z", "finished_utc": "2026-11-20T13:12:13.067953Z", "http_status": 0, "curl_exit_code": 35, "raw": "research/experiments/20261120T124414Z/next_midnight_responses/ETH_funding_1.json.gz", "sha256": "f61f27bd17de546264aa58f40f3aafaac7021e0ef69c17f6b1b4cd7664a037ec", "raw_body_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "bytes": 0, "stderr": "curl: (35) TLS connect error: error:0A000126:SSL routines::unexpected eof while reading\n", "resolved": true, "resolution": "Later bounded exact GET succeeded; readonly source capture only."}]
监控成功=True，研究配置11268，旧展示行11260完整字典保持。

下一窗口：SMA/candidate20:30→22:30仍仅mark；L4/FEWM22:10→Nov20 00:10跨原Nov20 00:01日决策，必须按原kernel、原持仓与已计成本续接，并按精确资金费时间顺序入账。next_midnight_preparation.json只缓存真实下一窗口原始输入，不创建资金费/交易/日决策。随后SMA跨日须真实SPOT full72权威与原日线adapter，当前full71不改写。

实际完成阶段命令（市场/账户阶段完成后不得重跑）：

```sh
cd /home/desktop/Documents/Codex/EquiTide
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T124414Z/commands.py prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T124414Z/commands.py freeze
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T124414Z/commands.py units
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T124414Z/commands.py bind
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T124414Z/commands.py reserve_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T124414Z/commands.py reserve_1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T124414Z/commands.py evaluate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T124414Z/commands.py audit
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T124414Z/commands.py exports
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T124414Z/commands.py finish_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T124414Z/commands.py finish_1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T124414Z/commands.py research_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T124414Z/commands.py l4h02
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T124414Z/commands.py fewm
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T124414Z/commands.py candidate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T124414Z/commands.py forward
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T124414Z/commands.py accounts_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T124414Z/commands.py journal
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T124414Z/commands.py sources_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T124414Z/commands.py gates
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T124414Z/commands.py feed
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T124414Z/commands.py midnight_prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T124414Z/commands.py collect
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T124414Z/commands.py final_checks
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T124414Z/commands.py final_checks_retry1
```

字段/版本见primary_source_access.json：[Binance官方REST文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)、[公共数据README](https://github.com/binance/binance-public-data/blob/master/README.md)、[Python中位数定义](https://docs.python.org/3/library/statistics.html#statistics.median)。所有负收益、零交易、失败和原始冻结证据保留。

原账户实际资金费新增分配={"SMA": 0, "candidate": 0, "l4h02": 0, "fewm": 0}。本轮各账户仅按自身持仓处理窗口内真实新增结算，逐笔现金流见funding16_nov19_reconciliation.json；L4/FEWM不重复既有16结算。三永续现均恰好记Nov19实际16:00:00.002一次；首完整来源UTC=2026-11-20T06:49:33.776616Z、SHA256=c639902f4a4b8469e17ad16d7da0acfa598a6fb9ba8b242dbc2bfa786a8d7393原样保留。下一SMA/candidate20:30→22:30，L4/FEWM22:10→Nov20_00:10，均先完整查询实际新增结算，不按名义时间预记、不重置本金/持仓，下一日决策Nov20 00:01。

下一跨日交接按实际返回时间1795132800001000000纳秒登记待处理源，首次捕获UTC=2026-11-20T13:12:16.739946Z。此缓存尚未计入任何账户；L4/FEWM下一窗口各按自身继承持仓先结算资金费、再处理原00:01日决策。准确下一窗口作用域见next_midnight_handoff_scope_verification.json；旧Nov19_16空待处理列表只属于已结算旧事件。

归档复现清单检查曾漏列补全跨日交接后执行的只读final_checks_retry1，现已按全部25个实际原生命令补齐；原24行清单、失败回执与前后哈希保留在reproduction_command_label_review.json。该问题不涉及金融/账户重新计算，原report.json保持124d6b050ecbc348757060f1f02203099da9db84b3bc76a353cd5a346d55359d。
