# 20261120T084011Z BTC入场波动窗口与ETH目标组合验证

事前冻结BTC窗口9/10/11天 × ETH目标3500/3750/4000的完整3×3网格；10天组件和3个10天父组合为已有结果，只读复用。新增2个BTC原生配置和6个父组合全部先reserve后计算一次并finish。新父组合通过预设历史门槛6/6；原生组件通过2/2。事前代表V9/ETH3750不按结果替换。相对同ETH目标、同本金的V10父组合，严格同时改善收益/整体DD/Sharpe/Calmar为0/6。所有淘汰和负收益保留；历史通过不构成稳定实盘盈利。

完整读取39284条事件、19503个ID、484份结论及29份附加材料。初始16项实际回测缺口0。规范研究定义11685→11693，正式有结果11480。相关配置和路径不等于独立试验，没有DSR/PBO显著性证明。

经济含义：BTC本金3750、ETH15000、总18750；原始银行权重[1,1]不自动归一化，20/80仅为初始本金占比。BTC入场目标固定1000，ETH3500/3750/4000，总初始目标4500/4750/5000。窗口轴是过去样本对数波动的天数，不是金额。V对照内初始目标相同，实际持仓及动态风险可因入场门变化；ETH目标之间是不同敞口。父组合逐点相加美元NAV，无转账、父订单、再平衡或跨保证金净额。

复用8个已有原生银行及6个已有父组合的真实完整结果；仅2个新BTC模型实际重算信号、数量、非线性冲击、资金费和保证金代理。四个核心会计/市场文件字节相同，引擎只把允许的V窗口域增加9和11，逆向替换和函数身份独立检查已保存。ETH及持有基准不重跑、不按比例缩放NAV。

完整规则：BTC completedROC L29 strictH.03/exitE.005; new or reversed entry requires completed samplelogvolV9/10old/11<=.0275 and strict direction*completedROC5>.0025; equality passes vol and blocks confirmation. Existing same-direction actual quantity retained, ordinary exits unaffected. ETH longonlyL5/H.02/E.0075,finiteEWMS16beta15/17/D3K.0075,V6cap.05625,M4mature1-36h funding median with conservative1h source delay,budgetmin(.0002,.0075*pastVW9samplelogvol*pastactualintervalhours/24),missingblocksnewentryonly. No fit/labels/future data.

按时间验证：391日反复开发历史，2025-10-19 00:01→2026-11-14 00:01，33个闭合上下文日；固定规则无拟合/标签，purge不适用、标签embargo0。13个完整30日折+1日尾段，近40日8×5日，扩展21日5/5/5/6。跨折继承源银行现金/q，原终点计费平仓；整体DD由连续完整NAV计算。该历史已被反复使用，不能称未触碰最终测试集或独立未来验证。

成本1/2/3倍：每边5bp手续费、1bp半价差、2bp滑点、0.5×过去20日样本对数波动×sqrt(实际订单额/过去20日quoteADV)；不利tick/LOT/最低金额/参与率≤0.001，完全抵押1倍入场及小时不利价1%维持保证金代理。实际永续资金费支出加倍、收入不放大；线性永续无现货借币。逐笔与完整路径独立复核；估计费用缺L2/TCA、完整阶梯、tick清算及容量实证。

|范围|BTC窗口天|BTC/ETH入场目标|状态|净收益1/2/3倍 %|整体DD3 %|Sharpe3|Calmar3|正30日折1倍|近期正5日折1/2/3|
|---|---|---|---|---|---|---|---|---|---|
|native|9|1000/—|passed|17.740916 / 16.466633 / 15.192417|5.814711|1.491627|2.427315|10/13|6/6/6（各/8）|
|native|11|1000/—|passed|17.746223 / 16.522235 / 15.298278|5.775982|1.523845|2.460539|10/13|6/6/6（各/8）|
|parent|9|1000/3500|passed|8.485400 / 7.967605 / 7.449765|1.212414|2.300034|5.722135|12/13|6/6/6（各/8）|
|parent|9|1000/3750|passed|8.838084 / 8.301252 / 7.764761|1.285720|2.302893|5.623477|12/13|6/6/6（各/8）|
|parent|9|1000/4000|passed|9.191149 / 8.635474 / 8.079980|1.359332|2.303379|5.534328|12/13|6/6/6（各/8）|
|parent|11|1000/3500|passed|8.486462 / 7.978726 / 7.470937|1.212169|2.318755|5.739519|12/13|6/6/6（各/8）|
|parent|11|1000/3750|passed|8.839146 / 8.312372 / 7.785934|1.285461|2.320500|5.639910|12/13|6/6/6（各/8）|
|parent|11|1000/4000|passed|9.192211 / 8.646594 / 8.101152|1.359058|2.319951|5.549909|12/13|6/6/6（各/8）|

预设失败判据：全期/近期各成本正、1倍≥10/13正月、近40日各成本≥6/8正5日折、扩展各成本≥3/4正折、DD3≤25%、邻域正收益及近期合格比例≥60%、≥4次底层平仓、1倍(毛价差收益+资金费)/费用≥2.5；无拒单、负抵押、保证金代理违规，原终点flat。原生BTC邻域为窗口一维，父组合为窗口×ETH目标二维。已有基准状态保持。

BTC_L29H0p03E0p005_V9Cap0p0275Confirm5Min0p0025_C3750_N1000_391d：通过预设历史门槛，独立未来验证尚未完成。
BTC_L29H0p03E0p005_V11Cap0p0275Confirm5Min0p0025_C3750_N1000_391d：通过预设历史门槛，独立未来验证尚未完成。
parent_BTCVolV9Cap0p0275_N1000_ETHN3500Cap0p05625_C3750_15000_391d：通过预设历史门槛，独立未来验证尚未完成。
parent_BTCVolV9Cap0p0275_N1000_ETHN3750Cap0p05625_C3750_15000_391d：通过预设历史门槛，独立未来验证尚未完成。
parent_BTCVolV9Cap0p0275_N1000_ETHN4000Cap0p05625_C3750_15000_391d：通过预设历史门槛，独立未来验证尚未完成。
parent_BTCVolV11Cap0p0275_N1000_ETHN3500Cap0p05625_C3750_15000_391d：通过预设历史门槛，独立未来验证尚未完成。
parent_BTCVolV11Cap0p0275_N1000_ETHN3750Cap0p05625_C3750_15000_391d：通过预设历史门槛，独立未来验证尚未完成。
parent_BTCVolV11Cap0p0275_N1000_ETHN4000Cap0p05625_C3750_15000_391d：通过预设历史门槛，独立未来验证尚未完成。

相对同ETH目标的V10旧父组合（三倍成本）：
V9/ETH3500：收益差-0.116112个百分点，整体DD差0.001343个百分点，Sharpe差-0.043159，Calmar差-0.095416。
V9/ETH3750：收益差-0.116112个百分点，整体DD差0.001421个百分点，Sharpe差-0.041312，Calmar差-0.090196。
V9/ETH4000：收益差-0.116112个百分点，整体DD差0.001498个百分点，Sharpe差-0.039571，Calmar差-0.085518。
V11/ETH3500：收益差-0.094940个百分点，整体DD差0.001098个百分点，Sharpe差-0.024438，Calmar差-0.078032。
V11/ETH3750：收益差-0.094940个百分点，整体DD差0.001161个百分点，Sharpe差-0.023705，Calmar差-0.073763。
V11/ETH4000：收益差-0.094940个百分点，整体DD差0.001225个百分点，Sharpe差-0.022999，Calmar差-0.069937。

敏感性全部保存：{"costs": 66, "walk_forward_folds": 924, "recent40_folds": 528, "extension21_folds": 264, "daily_NAV": 25872, "joint_sensitivity": 66, "matched_hold_comparisons": 27, "adjacent_sensitivity_edges": 14}；相邻边14条，启发式超过2个样本标准差的Sharpe跳变边[{"scope": "native", "from": "BTC_L29H0p03E0p005_V9Cap0p0275Confirm5Min0p0025_C3750_N1000_391d", "to": "BTC_L29_H3_E0p005_V10cap0p0275_RecentConfirm5_Min0p0025_391d", "delta_net_pp": 0.5805595898780833, "delta_sharpe": 0.06962440734342379, "delta_DD_pp": -0.03872929313052342, "delta_Calmar": 0.10921084890862787}]。新8配置有8条不同完整成本路径，旧路径别名组0。不按收益扩网格/替换代表；小网格不能证明全域稳健。
独立核验新原生6条/新父18条成本曲线，原生政策决策2346；只读原生24条/父18条、原政策决策9384。实际资金费逐条、成交/费用/小时风险与全连续NAV均核验。货币现金流桥接见sizing_effect_decomposition.json。

本轮四账户各续接120个闭合分钟，日决策{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}；实际资金费记录{'SMA': 0, 'candidate': 6, 'l4h02': 0, 'fewm': 0}。本轮各永续只处理当前各自窗口实际新增结算，不重复旧08:00:00.002资金费。各账户现金变化逐笔核对，持仓/desired/入场价/累计执行费用保持。完整71日SPOT权威及原70精确前缀只读，分钟包不是日线权威。首08来源UTC保持2026-11-19T20:40:54.314631Z，实际fundingTime1795075200002不替换为名义整点；目前三永续均恰好记08一次。下一SMA/candidate['2026-11-19T16:30:00Z', '2026-11-19T18:30:00Z']，L4/FEWM['2026-11-19T18:10:00Z', '2026-11-19T20:10:00Z']，均不重复08，先查询实际特殊资金费；下一日决策Nov20_00:01。不重置本金、不强制平仓、不采用新研究配置。

原SMA三倍成本累计-7.468958%；原账户为延迟shadow，180日/六折资格未成熟。十策略仅只读汇总，未改冻结规则/本金/持仓或产生新成交。
唯一公共GET回执19，本轮19、旧复用0；实际运输失败记录1。如内置重试仅有stderr，则保留该可观察边界，不补造URL/时刻/响应。其他真实失败事实：[{"type": "readonly_diagnostic_TypeError", "native_chunk": "173393", "exit_code": 1, "reason": "Diagnostic helper incorrectly passed a generator comparison bool into any; diagnostic omitted. No files modified by failed command, no registrations, market backtests or account advances.", "resolved": true}, {"type": "premature_readonly_identity_review_before_all_finish_receipts", "recorded_utc": "2026-11-20T09:06:20.263598+00:00", "native_session_id": 72830, "native_chunk_id": "249b94", "exit_code": 1, "source": "research/experiments/20261120T084011Z/review_economic_identity.py", "observed_stderr": "AssertionError: rs[fingerprint][result_available] while finish_0 was still in progress", "cause": "The independent read-only review loaded a registry snapshot before the batch finishing process completed; finance evaluation/audit already succeeded.", "resolved": true, "no_market_or_account_calculation": true, "no_financial_or_account_rerun": true, "resolution": "Same unchanged read-only identity review executed after finish_0/finish_1 completed; full registry shows all8 financial results and zero prior economic duplicates. No financial/account model rerun.", "successful_native_session_id": 83810, "successful_native_chunk_id": "f12188", "successful_native_exit_code": 0, "effective_verification": "research/experiments/20261120T084011Z/economic_configuration_identity_verification.json", "effective_verification_sha256": "8f48f8c047ea33c28ba61fb7b25d94bb675117fb999c89d2f686c7e711f9bc6c"}, {"url": "https://fapi.binance.com/fapi/v1/fundingRate?symbol=BTCUSDT&startTime=1795104000002&endTime=1795111800000&limit=1000", "started_utc": "2026-11-20T09:07:22.816212+00:00", "http_status": 0, "curl_exit_code": 35, "raw": "data/raw/binance/l4h02_forward/20261120T084011Z/http_0004.gz", "sha256": "f61f27bd17de546264aa58f40f3aafaac7021e0ef69c17f6b1b4cd7664a037ec", "bytes": 0, "stderr": "curl: (35) TLS connect error: error:0A000126:SSL routines::unexpected eof while reading\n", "transport": "verifiedTLSmin1.2HTTP1.1 publicGET,bounded3attempts", "resolved": true, "resolution": "Same exact URL has validated successful saved public bytes; original capture time retained, including earlier source reuse documented before first reserve. Successful original account packet and audit retained."}]
监控生成成功=True，11252研究配置，11244旧行完整字典不变。

实际执行阶段命令（已完成的市场/账户阶段不得重跑；只读核验可复现）：

```sh
cd /home/desktop/Documents/Codex/EquiTide
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T084011Z/commands.py prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T084011Z/commands.py freeze
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T084011Z/commands.py units
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T084011Z/commands.py bind
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T084011Z/commands.py reserve_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T084011Z/commands.py reserve_1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T084011Z/commands.py evaluate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T084011Z/commands.py audit
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T084011Z/commands.py exports
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T084011Z/commands.py finish_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T084011Z/commands.py finish_1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T084011Z/commands.py research_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T084011Z/commands.py l4h02
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T084011Z/commands.py fewm
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T084011Z/commands.py candidate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T084011Z/commands.py forward
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T084011Z/commands.py accounts_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T084011Z/commands.py journal
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T084011Z/commands.py sources_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T084011Z/commands.py gates
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T084011Z/commands.py feed
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T084011Z/commands.py collect
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T084011Z/commands.py final_checks
```

数据字段来源见primary_source_access.json：[Binance官方REST文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)、[公共数据README](https://github.com/binance/binance-public-data/blob/master/README.md)。样本方差定义对照[Python statistics官方文档](https://docs.python.org/3/library/statistics.html#statistics.stdev)并通过显式n−1公式验证；实际运行版本及冻结代码为准。全部负收益、失败、来源和冻结规则保留；成本系数是研究假设。

原账户实际资金费新增分配={"SMA": 0, "candidate": 6, "l4h02": 0, "fewm": 0}。candidate使用自身BTC-0.012/ETH0原持仓及原成本规则，逐笔现金流见funding16_nov19_reconciliation.json；L4/FEWM不重复既有16结算。三永续现均恰好记Nov19实际16:00:00.002一次；首完整来源UTC=2026-11-20T06:49:33.776616Z、SHA256=c639902f4a4b8469e17ad16d7da0acfa598a6fb9ba8b242dbc2bfa786a8d7393原样保留。下一SMA/candidate16:30→18:30，L4/FEWM18:10→20:10，均先完整查询实际新增结算，不按名义时间预记、不重置本金/持仓，下一日决策Nov20 00:01。
