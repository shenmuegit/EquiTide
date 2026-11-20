# 20261120T104213Z BTC入场波动上限与ETH目标组合验证

事前冻结BTC V10波动上限0.026125/0.0275/0.028875 × ETH目标3500/3750/4000的完整3×3网格；0.0275组件和3个同上限父组合为已有结果，只读复用；另2个更近的旧上限0.02625/0.02875组件也只读保留。新增2个BTC原生配置和6个父组合全部先reserve后计算一次并finish。新父组合通过预设历史门槛6/6；原生组件通过2/2。事前代表上限0.026125/ETH3750不按结果替换。相对同ETH目标、同本金的上限0.0275/V10父组合，严格同时改善收益/整体DD/Sharpe/Calmar为0/6。所有淘汰和负收益保留；历史通过不构成稳定实盘盈利。

完整读取39344条事件、19533个ID、485份结论及29份附加材料。初始16项实际回测缺口0。规范研究定义11693→11701，正式有结果11488。相关配置和路径不等于独立试验，没有DSR/PBO显著性证明。

经济含义：BTC本金3750、ETH15000、总18750；原始银行权重[1,1]不自动归一化，20/80仅为初始本金占比。BTC入场目标固定1000，ETH3500/3750/4000，总初始目标4500/4750/5000。BTC轴是固定10日样本对数波动的无量纲上限，不是天数或金额。每个上限对照内初始目标相同，实际持仓及动态风险可因入场门变化；ETH目标之间是不同敞口。父组合逐点相加美元NAV，无转账、父订单、再平衡或跨保证金净额。

复用10个已有原生银行及6个已有父组合的真实完整结果；仅2个新BTC模型实际重算信号、数量、非线性冲击、资金费和保证金代理。四个核心会计/市场文件字节相同，引擎只把允许的BTC上限域增加0.026125和0.028875，逆向替换和函数身份独立检查已保存。ETH及持有基准不重跑、不按比例缩放NAV。

完整规则：BTC completedROC L29 strictH.03/exitE.005; new or reversed entry requires completed samplelogvolV10<=cap in .026125/.0275old/.028875 and strict direction*completedROC5>.0025. Capperturbation is exactly +/-5percent about .0275; equality passes volatility and blocks strictconfirmation. Existing same-direction actual quantity retained,ordinary exits unaffected. ETH longonlyL5/H.02/E.0075,finiteEWMS16beta15/17/D3K.0075,V6cap.05625,M4mature1-36h funding median with conservative1h source delay,budgetmin(.0002,.0075*pastVW9samplelogvol*pastactualintervalhours/24),missingblocksnewentryonly. No fit/labels/future data.

按时间验证：391日反复开发历史，2025-10-19 00:01→2026-11-14 00:01，33个闭合上下文日；固定规则无拟合/标签，purge不适用、标签embargo0。13个完整30日折+1日尾段，近40日8×5日，扩展21日5/5/5/6。跨折继承源银行现金/q，原终点计费平仓；整体DD由连续完整NAV计算。该历史已被反复使用，不能称未触碰最终测试集或独立未来验证。

成本1/2/3倍：每边5bp手续费、1bp半价差、2bp滑点、0.5×过去20日样本对数波动×sqrt(实际订单额/过去20日quoteADV)；不利tick/LOT/最低金额/参与率≤0.001，完全抵押1倍入场及小时不利价1%维持保证金代理。实际永续资金费支出加倍、收入不放大；线性永续无现货借币。逐笔与完整路径独立复核；估计费用缺L2/TCA、完整阶梯、tick清算及容量实证。

|范围|BTC波动上限|BTC/ETH入场目标|状态|净收益1/2/3倍 %|整体DD3 %|Sharpe3|Calmar3|正30日折1倍|近期正5日折1/2/3|
|---|---|---|---|---|---|---|---|---|---|
|native|0.026125|1000/—|passed|18.230204 / 17.001557 / 15.772976|5.775982|1.561251|2.536525|10/13|6/6/6（各/8）|
|native|0.028875|1000/—|passed|17.271348 / 15.996683 / 14.722059|5.833497|1.444086|2.344924|10/13|6/6/6（各/8）|
|parent|0.026125|1000/3500|passed|8.583258 / 8.074590 / 7.565877|1.211071|2.343193|5.817551|12/13|6/6/6（各/8）|
|parent|0.026125|1000/3750|passed|8.935942 / 8.408236 / 7.880873|1.284300|2.344206|5.713673|12/13|6/6/6（各/8）|
|parent|0.026125|1000/4000|passed|9.289007 / 8.742459 / 8.196091|1.357834|2.342950|5.619846|12/13|6/6/6（各/8）|
|parent|0.028875|1000/3500|passed|8.391487 / 7.873615 / 7.355693|1.213505|2.269775|5.644971|12/13|6/6/6（各/8）|
|parent|0.028875|1000/3750|passed|8.744171 / 8.207261 / 7.670690|1.286874|2.273795|5.550534|12/13|6/6/6（各/8）|
|parent|0.028875|1000/4000|passed|9.097236 / 8.541484 / 7.985908|1.360548|2.275381|5.465167|12/13|6/6/6（各/8）|

两条新BTC原生配置的1/2/3倍成本完整路径，均与已完成的旧上限模型重合；较低上限的3个父组合也与旧0.0275基准完全同路径，较高上限3个父组合三倍成本收益均下降0.210183个百分点，整体DD略增。参数定义不同，全部实际结果仍各自登记保留，但不解释为独立新增alpha或未来验证。详见incremental_evidence_review.json。
冻结只读查重器的计数标签14及BTC_V列名沿用旧模板，原循环已检查所有16个来源；原输出/源码保留，正确来源数10native+6parent及cap/V10单位见economic_identity_label_review.json，不改金融结果。

历史父组合的单个BTC上限标量写为0.04，但组件指纹及三档原NAV哈希均指向实际0.0275；旧spec/report/status未改写。本轮同上限对照按真实组件解释，新组合元数据从实际子spec生成。失败检查和只读核验见legacy_parent_scalar_cap_review.json。

预设失败判据：全期/近期各成本正、1倍≥10/13正月、近40日各成本≥6/8正5日折、扩展各成本≥3/4正折、DD3≤25%、邻域正收益及近期合格比例≥60%、≥4次底层平仓、1倍(毛价差收益+资金费)/费用≥2.5；无拒单、负抵押、保证金代理违规，原终点flat。原生BTC邻域为波动上限一维，父组合为上限×ETH目标二维。已有基准状态保持。

BTC_L29H0p03E0p005_V10Cap0p026125Confirm5Min0p0025_C3750_N1000_391d：通过预设历史门槛，独立未来验证尚未完成。
BTC_L29H0p03E0p005_V10Cap0p028875Confirm5Min0p0025_C3750_N1000_391d：通过预设历史门槛，独立未来验证尚未完成。
parent_BTCV10Cap0p026125_N1000_ETHN3500Cap0p05625_C3750_15000_391d：通过预设历史门槛，独立未来验证尚未完成。
parent_BTCV10Cap0p026125_N1000_ETHN3750Cap0p05625_C3750_15000_391d：通过预设历史门槛，独立未来验证尚未完成。
parent_BTCV10Cap0p026125_N1000_ETHN4000Cap0p05625_C3750_15000_391d：通过预设历史门槛，独立未来验证尚未完成。
parent_BTCV10Cap0p028875_N1000_ETHN3500Cap0p05625_C3750_15000_391d：通过预设历史门槛，独立未来验证尚未完成。
parent_BTCV10Cap0p028875_N1000_ETHN3750Cap0p05625_C3750_15000_391d：通过预设历史门槛，独立未来验证尚未完成。
parent_BTCV10Cap0p028875_N1000_ETHN4000Cap0p05625_C3750_15000_391d：通过预设历史门槛，独立未来验证尚未完成。

相对同ETH目标、上限0.0275/V10旧父组合（三倍成本）：
cap0.026125/ETH3500：收益差0.000000个百分点，整体DD差0.000000个百分点，Sharpe差0.000000，Calmar差0.000000。
cap0.026125/ETH3750：收益差0.000000个百分点，整体DD差0.000000个百分点，Sharpe差0.000000，Calmar差0.000000。
cap0.026125/ETH4000：收益差0.000000个百分点，整体DD差0.000000个百分点，Sharpe差0.000000，Calmar差0.000000。
cap0.028875/ETH3500：收益差-0.210183个百分点，整体DD差0.002433个百分点，Sharpe差-0.073417，Calmar差-0.172580。
cap0.028875/ETH3750：收益差-0.210183个百分点，整体DD差0.002574个百分点，Sharpe差-0.070411，Calmar差-0.163139。
cap0.028875/ETH4000：收益差-0.210183个百分点，整体DD差0.002714个百分点，Sharpe差-0.067570，Calmar差-0.154679。

敏感性全部保存：{"costs": 72, "walk_forward_folds": 1008, "recent40_folds": 576, "extension21_folds": 288, "daily_NAV": 28224, "joint_sensitivity": 72, "matched_hold_comparisons": 27, "adjacent_sensitivity_edges": 14}；相邻边14条，启发式超过2个样本标准差的Sharpe跳变边[{"scope": "native", "from": "BTC_L29_H3_E0p005_V10cap0p0275_RecentConfirm5_Min0p0025_391d", "to": "BTC_L29H0p03E0p005_V10Cap0p028875Confirm5Min0p0025_C3750_N1000_391d", "delta_net_pp": -1.0509170656284326, "delta_sharpe": -0.11716516798296817, "delta_DD_pp": 0.057514890610299574, "delta_Calmar": -0.1916019261972317}]。新8配置有8条不同完整成本路径，旧路径别名组5。不按收益扩网格/替换代表；小网格不能证明全域稳健。
独立核验新原生6条/新父18条成本曲线，原生政策决策2346；只读原生30条/父18条、原政策决策11730。实际资金费逐条、成交/费用/小时风险与全连续NAV均核验。货币现金流桥接见sizing_effect_decomposition.json。

本轮四账户各续接120个闭合分钟，日决策{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}；实际资金费记录{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}。本轮各永续只处理当前各自窗口实际新增结算，不重复旧08:00:00.002资金费。各账户现金变化逐笔核对，持仓/desired/入场价/累计执行费用保持。完整71日SPOT权威及原70精确前缀只读，分钟包不是日线权威。首08来源UTC保持2026-11-19T20:40:54.314631Z，实际fundingTime1795075200002不替换为名义整点；目前三永续均恰好记08一次。下一SMA/candidate['2026-11-19T18:30:00Z', '2026-11-19T20:30:00Z']，L4/FEWM['2026-11-19T20:10:00Z', '2026-11-19T22:10:00Z']，均不重复08，先查询实际特殊资金费；下一日决策Nov20_00:01。不重置本金、不强制平仓、不采用新研究配置。

原SMA三倍成本累计-7.468958%；原账户为延迟shadow，180日/六折资格未成熟。十策略仅只读汇总，未改冻结规则/本金/持仓或产生新成交。
唯一公共GET回执18，本轮18、旧复用0；实际运输失败记录0。如内置重试仅有stderr，则保留该可观察边界，不补造URL/时刻/响应。其他真实失败事实：[{"type": "official_document_old_URL_web_tool_inaccessible", "recorded_utc": "2026-11-20T10:47:38.981553+00:00", "requested_url": "https://developers.binance.com/en/docs/derivatives/usds-margined-futures/market-data/rest-api/Get-Funding-Rate-History", "observed_error": "web.run Internal Error: URL is not accessible via this tool", "resolved": true, "resolution": "Opened current official USD-M REST market-data catalog successfully; no market/account calculation or reservation occurred.", "effective_url": "https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data"}, {"command": ["/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python", "-B", "/home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T104213Z/sizing_units.py"], "cwd": "/home/desktop/Documents/Codex/EquiTide", "started_utc": "2026-11-20T10:48:59.118919Z", "finished_utc": "2026-11-20T10:48:59.383988Z", "exit_code": 1, "log": "research/experiments/20261120T104213Z/sizing_units.log", "stderr": "Traceback (most recent call last):\n  File \"/home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T104213Z/sizing_units.py\", line 11, in <module>\n    sp=json.loads((ROOT/row['spec']).read_text());q=sp['parameters'];assert [z['weight'] for z in sp['components']]==[1,1] and q['component_capitals_usdt']==[3750,15000] and q['component_initial_entry_notionals_usdt']==[1000,row['K']] and q['BTC_entry_volatility_ceiling']==row['W'] and q['BTC_entry_volatility_window_days']==10 and q['BTC_entry_notional_usdt']==1000 and q['ETH_entry_notional_usdt']==row['K']\n                                                                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nAssertionError\n", "resolved": true, "resolution": "Sizing checker traced the single stale scalar on a readonly historical parent to its exact child graph; all3sourceNAVhash lists match real cap.0275. Old spec/report/status untouched; corrected current checker validates actual child parameters and all new parent metadata. Units_retry1 native exit0 before any currentreserve.", "effective_check": "units_retry1_commands.json", "old_failed_checker": "preparation_failure/sizing_units_before_child_graph_review.py", "legacy_review": "legacy_parent_scalar_cap_review.json"}, {"type": "frozen_readonly_identity_count_and_axis_labels", "recorded_utc": "2026-11-20T10:58:15.182267+00:00", "native_exit_code": 0, "observed_native_chunk_id": "b8eadf", "observed_metadata": "Readonly reviewer checked all references in a dynamic loop but saved hardcoded count14; row BTC_V field holds cap values in this changed axis.", "resolved": true, "resolution": "Saved economic_identity_label_review.json with actual16(10native+6parent) reference hashes and each new cap/V10 unit mapping. Frozen reviewer,original output,financial report and all outcomes unchanged; no market/account rerun."}]
监控生成成功=True，11260研究配置，11252旧行完整字典不变。

实际执行阶段命令（已完成的市场/账户阶段不得重跑；只读核验可复现）：

```sh
cd /home/desktop/Documents/Codex/EquiTide
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T104213Z/commands.py prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T104213Z/commands.py freeze
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T104213Z/commands.py units
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T104213Z/commands.py units_retry1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T104213Z/commands.py bind
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T104213Z/commands.py reserve_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T104213Z/commands.py reserve_1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T104213Z/commands.py evaluate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T104213Z/commands.py audit
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T104213Z/commands.py exports
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T104213Z/commands.py finish_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T104213Z/commands.py finish_1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T104213Z/commands.py research_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T104213Z/commands.py l4h02
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T104213Z/commands.py fewm
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T104213Z/commands.py candidate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T104213Z/commands.py forward
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T104213Z/commands.py accounts_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T104213Z/commands.py journal
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T104213Z/commands.py sources_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T104213Z/commands.py gates
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T104213Z/commands.py feed
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T104213Z/commands.py collect
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261120T104213Z/commands.py final_checks
```

数据字段来源见primary_source_access.json：[Binance官方REST文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)、[公共数据README](https://github.com/binance/binance-public-data/blob/master/README.md)。样本方差定义对照[Python statistics官方文档](https://docs.python.org/3/library/statistics.html#statistics.stdev)并通过显式n−1公式验证；实际运行版本及冻结代码为准。全部负收益、失败、来源和冻结规则保留；成本系数是研究假设。

原账户实际资金费新增分配={"SMA": 0, "candidate": 0, "l4h02": 0, "fewm": 0}。本轮各账户仅按自身持仓处理窗口内真实新增结算，逐笔现金流见funding16_nov19_reconciliation.json；L4/FEWM不重复既有16结算。三永续现均恰好记Nov19实际16:00:00.002一次；首完整来源UTC=2026-11-20T06:49:33.776616Z、SHA256=c639902f4a4b8469e17ad16d7da0acfa598a6fb9ba8b242dbc2bfa786a8d7393原样保留。下一SMA/candidate18:30→20:30，L4/FEWM20:10→22:10，均先完整查询实际新增结算，不按名义时间预记、不重置本金/持仓，下一日决策Nov20 00:01。
