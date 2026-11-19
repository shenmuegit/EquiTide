# 20261119T223758Z 复用真实银行净值的BTC/ETH独立目标组合

事前固定BTC目标750/1125/1750与ETH目标3500/3750/4000完整3×3网格，ETH V6波动上限固定0.05625。旧ETH3750金额的3个策略组合和3个持有组合只读；6个真正新策略交叉组合、6个匹配持有基准全部先reserve后计算一次并finish。新组合通过历史门槛6/6、持有基准淘汰6/6，负收益不删除。事前代表1125/3500不随结果改变。严格同时改善收益、整体回撤、Sharpe、Calmar为0/6；没有独立未来或稳定实盘盈利资格。

完整读取39000条事件、19361个ID、479份既往结论及29份附加材料。初始16项真实回测缺口0。规范研究定义11641→11653，正式有结果11440；定义数、相关路径数均不是独立试验次数，没有DSR/PBO显著性证明。

经济含义：BTC本金3750、ETH本金15000、总18750和原始银行权重[1,1]保持；20/80是初始本金占比，不自动归一化，不转移资金。两轴是独立的原银行入场目标金额，目标总额4250–5750随格点变化，不再固定5000，更不固定实际动态敞口。较高收益可能只是目标金额/风险增加；同初始目标持有基准也不匹配动态风险。

底层12个已完成银行（6个策略、6个持有）全部只读复用：从原状态片段与原价格还原完整NAV后核对原全路径哈希，再在共同事件轴逐点相加美元净值；不缩放收益、平均Sharpe、不重跑策略或产生新底层订单。父组合无订单、再平衡、抵押转移或跨保证金净额。原ETH组件的一致性淘汰状态保留。

完整规则：All underlying BTC L29/H.03/E.005/V10cap.0275/strictdirection*ROC5>.0025 and ETHlongonly L5/H.02/E.0075/finiteEWMS16beta15/17/D3K.0075/V6cap.05625/M4R.0075VW9 native rules,quantities,funding,costs and margin are exactly the saved completed source banks. No source strategy or order is recomputed. New candidates only change which independently funded existingBTC/ETH banks are jointly held.

按时间验证：391日反复开发历史，2025-10-19 00:01→2026-11-14 00:01，33个闭合上下文日；固定规则无拟合、训练或标签，purge不适用、标签embargo为0。13个完整30日折+1日尾段，近40日8×5日、扩展21日5/5/5/6；跨折继承实际源银行现金/q，原终点计费平仓，整体回撤由连续完整NAV计算。不能称未触碰最终留出。

成本1/2/3倍沿用源银行实际数量核算：每边手续费5bp、半价差1bp、滑点2bp、0.5×过去20日样本对数波动×sqrt(实际订单额/过去20日quoteADV)，不利tick/LOT/最低金额/参与率≤0.001；完全抵押1倍入场与小时不利价1%维持保证金代理。真实永续资金费支出随倍数增加、收入不放大；线性永续无现货借币。原费用/资金费逐项相加并独立复核；父组合没有新成交成本。估计费用缺真实L2/TCA、完整阶梯、tick清算与容量实证。

|BTC/ETH目标USDT|初始总目标|类型|状态|净收益1x/2x/3x %|整体DD3 %|Sharpe3|Calmar3|正30日折1x|近40日正5日折1/2/3|
|---|---|---|---|---|---|---|---|---|---|
|750/3500|4250|benchmark|rejected|-11.336885 / -12.017237 / -12.697641|15.907331|-1.373240|-0.748445|6/13|1/1/1（各/8）|
|750/4000|4750|benchmark|rejected|-12.736893 / -13.493795 / -14.250701|17.819127|-1.363058|-0.750293|6/13|1/1/1（各/8）|
|1125/3500|4625|benchmark|rejected|-12.009483 / -12.752698 / -13.495959|16.864963|-1.371666|-0.750549|6/13|1/1/1（各/8）|
|1125/4000|5125|benchmark|rejected|-13.409491 / -14.229256 / -15.049020|18.772191|-1.361309|-0.752320|6/13|1/1/1（各/8）|
|1750/3500|5250|benchmark|rejected|-13.354680 / -14.223622 / -15.092615|18.788120|-1.365308|-0.753872|6/13|1/1/1（各/8）|
|1750/4000|5750|benchmark|rejected|-14.754689 / -15.700180 / -16.645676|20.681498|-1.354979|-0.755766|6/13|1/1/1（各/8）|
|750/3500|4250|candidate|passed|7.511711 / 7.072799 / 6.633821|1.173370|2.317913|5.266327|12/13|6/6/6（各/8）|
|750/4000|4750|candidate|passed|8.217460 / 7.740668 / 7.264036|1.320789|2.299304|5.121964|12/13|6/6/6（各/8）|
|1125/3500|4625|candidate|passed|9.052075 / 8.513692 / 7.975241|1.225780|2.337173|6.057952|12/13|6/6/6（各/8）|
|1125/4000|5125|candidate|passed|9.757824 / 9.181560 / 8.605456|1.365560|2.345147|5.866396|12/13|6/6/6（各/8）|
|1750/3500|5250|candidate|passed|11.324952 / 10.625423 / 9.925839|1.822976|2.230612|5.066581|11/13|6/6/6（各/8）|
|1750/4000|5750|candidate|passed|12.030701 / 11.293292 / 10.556054|1.820303|2.267057|5.395126|12/13|6/6/6（各/8）|

预设失败判据：全期/近期各成本正、1x≥10/13正月、近40日各成本≥6/8正5日折、扩展各成本≥3/4正折、DD3≤25%、邻域正收益与近期合格比例≥60%、至少4次底层平仓、1x(毛价差收益+资金费)/费用≥2.5，无拒单/负抵押/保证金代理违规、原终点flat。持有基准无可调alpha参数，不强行构造邻域。

parent_independentEntry_matched_hold_BTCN750_ETHN3500_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_independentEntry_matched_hold_BTCN750_ETHN4000_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_independentEntry_matched_hold_BTCN1125_ETHN3500_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_independentEntry_matched_hold_BTCN1125_ETHN4000_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_independentEntry_matched_hold_BTCN1750_ETHN3500_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_independentEntry_matched_hold_BTCN1750_ETHN4000_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_independentEntry_BTCN750_ETHN3500_Cap0p05625_C3750_15000_391d：通过预设历史门槛，待独立未来验证。
parent_independentEntry_BTCN750_ETHN4000_Cap0p05625_C3750_15000_391d：通过预设历史门槛，待独立未来验证。
parent_independentEntry_BTCN1125_ETHN3500_Cap0p05625_C3750_15000_391d：通过预设历史门槛，待独立未来验证。
parent_independentEntry_BTCN1125_ETHN4000_Cap0p05625_C3750_15000_391d：通过预设历史门槛，待独立未来验证。
parent_independentEntry_BTCN1750_ETHN3500_Cap0p05625_C3750_15000_391d：通过预设历史门槛，待独立未来验证。
parent_independentEntry_BTCN1750_ETHN4000_Cap0p05625_C3750_15000_391d：通过预设历史门槛，待独立未来验证。

相对旧1125/3750中心的三倍成本变化：
BTC/ETH=750/3500，目标总额4250：收益-1.656416个百分点，整体DD-0.118814个百分点，Sharpe-0.024566，Calmar-0.706691；敞口不同，不解释为独立alpha提升。
BTC/ETH=750/4000，目标总额4750：收益-1.026202个百分点，整体DD0.028605个百分点，Sharpe-0.043175，Calmar-0.851054；敞口不同，不解释为独立alpha提升。
BTC/ETH=1125/3500，目标总额4625：收益-0.314997个百分点，整体DD-0.066405个百分点，Sharpe-0.005305，Calmar0.084934；敞口不同，不解释为独立alpha提升。
BTC/ETH=1125/4000，目标总额5125：收益0.315218个百分点，整体DD0.073376个百分点，Sharpe0.002669，Calmar-0.106622；敞口不同，不解释为独立alpha提升。
BTC/ETH=1750/3500，目标总额5250：收益1.635602个百分点，整体DD0.530792个百分点，Sharpe-0.111866，Calmar-0.906437；敞口不同，不解释为独立alpha提升。
BTC/ETH=1750/4000，目标总额5750：收益2.265817个百分点，整体DD0.528119个百分点，Sharpe-0.075421，Calmar-0.577893；敞口不同，不解释为独立alpha提升。

敏感性全部保存：90个成本场景、1260逐折、720近期折、360扩展折、35280日NAV行、27个匹配持有对比及12条相邻边；新12配置有12条不同完整成本路径。启发式跳变边=[{"scope": "parent", "from": "parent_independentEntry_BTCN1125_ETHN3500_Cap0p05625_C3750_15000_391d", "to": "parent_independentEntry_BTCN1750_ETHN3500_Cap0p05625_C3750_15000_391d", "delta_net_pp": 1.9505984264312595, "delta_sharpe": -0.10656053874183646, "delta_DD_pp": 0.5971966063920253, "delta_Calmar": -0.9913709683881624}, {"scope": "parent", "from": "parent_independentEntry_BTCN1125_ETHN3750_Cap0p05625_C3750_15000_391d", "to": "parent_independentEntry_BTCN1750_ETHN3750_Cap0p05625_C3750_15000_391d", "delta_net_pp": 1.9505984264312612, "delta_sharpe": -0.09223410689767508, "delta_DD_pp": 0.5294544078719099, "delta_Calmar": -0.7423238021945382}, {"scope": "parent", "from": "parent_independentEntry_BTCN1125_ETHN4000_Cap0p05625_C3750_15000_391d", "to": "parent_independentEntry_BTCN1750_ETHN4000_Cap0p05625_C3750_15000_391d", "delta_net_pp": 1.9505984264312595, "delta_sharpe": -0.07809006068784186, "delta_DD_pp": 0.4547432157954612, "delta_Calmar": -0.47127072235575174}]
收益最优若在金额网格边缘，仅作敞口诊断；不根据结果扩网格或替换代表。小网格不证明全域稳健。
独立核验只读源银行36条完整曲线、14076个原政策决策、42228条资金费、原成交/费用/小时风险，并核验新组合36条连续NAV、逐折和全部门槛；新增native策略决策/执行次数为0。父组合相对旧中心的货币现金流桥接见sizing_effect_decomposition.json。

本轮四账户各续接120个闭合分钟，日决策{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}；实际资金费记录{'SMA': 0, 'candidate': 6, 'l4h02': 0, 'fewm': 0}。candidate在08:00:00.002按自己BTC-0.012/ETH0和成本规则记账；L4/FEWM本轮窗口开始08:10，不重复旧08结算。各账户现金变化逐笔核对，持仓/desired/入场价/累计执行费用保持。完整71日SPOT权威及原70精确前缀只读，分钟包不是日线权威。首08来源UTC保持2026-11-19T20:40:54.314631Z，实际fundingTime1795075200002不替换为名义整点；目前三永续均恰好记08一次。下一SMA/candidate['2026-11-19T08:30:00Z', '2026-11-19T10:30:00Z']，L4/FEWM['2026-11-19T10:10:00Z', '2026-11-19T12:10:00Z']，均不重复08，先查询实际特殊资金费；下一日决策Nov20_00:01。不重置本金、不强制平仓、不采用新研究配置。

原SMA三倍成本累计-7.468958%；原账户为延迟shadow，180日/六折资格未成熟。十策略仅只读汇总，未改冻结规则/本金/持仓或产生新成交。
保存18份唯一公共GET回执，本轮18、旧复用0、已记录运输错误1（内置重试的失败子请求URL/时间/HTTP响应未独立采集，保留stderr，不补造缺失细节）；旧首资金费来源UTC/SHA保留，完整71日SPOT权威只读。其他实际失败事实：[{"passed": true, "type": "legacy_internal_curl_retry_TLS35", "recorded_utc": "2026-11-19T23:00:47.424043+00:00", "observed_curl_error_code": 35, "observed_stderr_error_line_count": 1, "observed_stderr_lines": ["curl: (35) TLS connect error: error:0A000126:SSL routines::unexpected eof while reading"], "outer_source_capture_native_receipt": {"command": ["/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python", "-B", "/home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T223758Z/forward.py"], "cwd": "/home/desktop/Documents/Codex/EquiTide", "started_utc": "2026-11-19T22:57:09.396673Z", "finished_utc": "2026-11-19T22:57:26.623764Z", "exit_code": 0, "log": "research/experiments/20261119T223758Z/forward.log", "stderr": "curl: (35) TLS connect error: error:0A000126:SSL routines::unexpected eof while reading\n"}, "outer_source_capture_exit_code": 0, "final_successful_responses": [{"asset": "BTC", "interval": "1m", "url": "https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=1m&startTime=1795069740000&endTime=1795076999999&limit=1000", "status": 200, "retrieved_utc": "2026-11-19T22:57:15.496233+00:00", "raw_response_sha256": "cdf84ef1deb5c9a54412f5a0e607f1d37c811b00b4ef1bf6cb3a51bbbf28bdf5", "raw_gzip_path": "data/runs/automation/20261119T223758Z/forward_raw/forward_response_BTC_1m.json.gz", "raw_gzip_sha256": "ed70f2d85aea22ebda5bd5deb3b7ea5970e366461647dd6ad389cc2992d61e25", "bars": 121, "timestamp_unit": "milliseconds", "closed_by_fixed_cutoff": true, "delayed_shadow_reconstruction": true}, {"asset": "ETH", "interval": "1m", "url": "https://data-api.binance.vision/api/v3/klines?symbol=ETHUSDT&interval=1m&startTime=1795069740000&endTime=1795076999999&limit=1000", "status": 200, "retrieved_utc": "2026-11-19T22:57:25.764811+00:00", "raw_response_sha256": "9e95944425cf70fb2d700fa45ad47574aed0308041e01efdc6fb88158c16d29d", "raw_gzip_path": "data/runs/automation/20261119T223758Z/forward_raw/forward_response_ETH_1m.json.gz", "raw_gzip_sha256": "6c36660a291620b2e03b524806d2c613193555f487967662e6f2c3091017ec6d", "bars": 121, "timestamp_unit": "milliseconds", "closed_by_fixed_cutoff": true, "delayed_shadow_reconstruction": true}], "original_stderr_log": "research/experiments/20261119T223758Z/forward.log", "original_stderr_log_sha256": "9cd218787cf844a828002f4ed13e5430aacca3e2a9854d0dec0143e9350bdff5", "failed_attempt_exact_URL_asset_time_and_HTTP_response_not_separately_captured": true, "failed_raw_HTTP_response_body_available": false, "exact_total_network_attempt_count_not_observed": true, "no_failed_response_body_URL_time_or_HTTP_status_fabricated": true, "resolved": true, "resolution": "Legacycurl internal retry recovered within original sourcecapture;both final200rawresponses retained and full closed-mark/ledger audit passed.No extra model or completed account window run.Original stderr preserved;failed subattempt metadata remains unobserved."}]
监控生成成功=True，11212研究配置，11200旧行完整字典不变。

实际完成阶段命令（完成目录不得重跑市场/账户，仅保留核验和数据哈希）：

```sh
cd /home/desktop/Documents/Codex/EquiTide
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T223758Z/commands.py prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T223758Z/commands.py freeze
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T223758Z/commands.py units
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T223758Z/commands.py bind
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T223758Z/commands.py reserve_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T223758Z/commands.py reserve_1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T223758Z/commands.py evaluate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T223758Z/commands.py audit
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T223758Z/commands.py exports
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T223758Z/commands.py finish_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T223758Z/commands.py finish_1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T223758Z/commands.py research_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T223758Z/commands.py l4h02
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T223758Z/commands.py fewm
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T223758Z/commands.py candidate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T223758Z/commands.py forward
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T223758Z/commands.py accounts_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T223758Z/commands.py journal
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T223758Z/commands.py sources_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T223758Z/commands.py gates
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T223758Z/commands.py feed
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T223758Z/commands.py collect
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T223758Z/commands.py final_checks
```

字段格式与版本见primary_source_access.json的[Binance官方REST文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)及[公共数据README](https://github.com/binance/binance-public-data/blob/master/README.md)。所有负收益、失败、来源和冻结规则均保留；成本系数是研究假设。
