# 20261119T143526Z 固定总目标5000的BTC/ETH分配研究

事前固定BTC/ETH新入场目标750/4250、1250/3750旧只读、1750/3250，交叉ETH入场V6波动上限.0525/.05625。代表750/4250及cap.05625不随结果改变。16项新配置：2个BTC及4个ETH策略银行、4个同金额持有银行、4个策略组合、2个组合持有基准，全部先reserve后实际计算一次并finish。历史门槛通过组合4/4，新组件2/6；所有淘汰结果留档。严格同时改善收益、整体回撤、Sharpe、Calmar为0/4；没有独立未来资格或稳定实盘盈利结论。

完整读取38720条登记事件、19221个ID、475份既往结论、29份附加材料。初始16项真实结果缺口0；规范研究定义11589→11605、正式有结果11392。定义数量不是独立试验次数，无DSR/PBO显著性证明。

经济假设：扩大既有1250/3750中心的固定总入场目标5000分配范围，检验750/4250与1750/3250的收益/风险取舍。BTC本金3750、ETH本金15000、总18750和原始银行权重[1,1]保持；20/80是初始本金占比，目标名义分配为15/85、25/75、35/65，不自动归一化或转移资金。原同方向q保留，实际动态敞口可随价格/持仓改变。两资产变金额的数量、LOT、tick、手续费、价差、滑点、平方根成交量冲击、资金费和保证金代理均重新计算；只有精确旧中心银行只读复用，无NAV线性缩放、父组合订单或再平衡。

完整规则：BTCfixedL29/H.03/exitE.005,V10samplelogvolcap.0275,strictdirection*recent5ROC>.0025 new/reversalonly,retainactualq. ETHlongonlyL5/H.02/E.0075,finiteEWMS16beta15/17,D3strictabsoluteK.0075,entryV6samplelogvolcaps.0525/.05625,M4signedmature1to36hrealizedfundingmedian,budgetmin(.0002,.0075*samplelogvol9*pastactualintervalh/24),missingblocksnewentryonly. ChangeonlyactualBTC/ETHentryN750/4250,1250/3750readonly,1750/3250;unchangeddirectionretainsactualq. Constant-long holds bypassstrategyfiltersandkeepactualqtofinalcostexit. No fit/labels/futurevalues/outcome-dependentchoices.

新父组合描述字段逐项从实际子spec生成，旧spec、report和状态保持；本批派生一致性检查见parent_metadata_consistency.json。真正变化是BTC与ETH实际入场金额及对应新组件图，N/C派生比例同步更新，描述修正不作为新预测信息。

时间与walk-forward：391日重复开发历史，2025-10-19 00:01→2026-11-14 00:01，33个已闭合上下文日，固定规则无训练、标签或拟合，purge不适用、无标签embargo；新spec明确33/0。13个完整30日折加1日尾段；近40日8×5日；扩展21日5/5/5/6日。跨折继承实际现金和数量，终点计费平仓；整体回撤从连续全NAV计算。重复使用的历史不是未触碰最终测试集。

成本1/2/3倍：每边手续费5bp、半价差1bp、滑点2bp、0.5×过去20日样本对数波动×sqrt(实际订单额/过去20日quoteADV)；不利tick、LOT/minnotional、参与率≤0.001，独立银行完全抵押1倍入场约束和小时不利价1%维持保证金代理。永续资金费支出随倍率增加、收入不放大；线性永续无现货借币。费用和盘口估计是研究假设，缺真实L2/TCA、完整历史阶梯、tick清算及容量实证。

|类型/配置|状态|净收益1x/2x/3x %|整体DD3 %|Sharpe3|Calmar3|正30日折1x|近期5日正折1/2/3|
|---|---|---|---|---|---|---|---|
|BTC component N=750 cap=None|passed|12.872468 / 11.992604 / 11.112699|4.095655|1.539913|2.523858|10/13|6/6/6（各/8）|
|BTC benchmark N=750 cap=None|rejected|-7.846916 / -8.580252 / -9.313590|11.700657|-1.339416|-0.745440|6/13|1/1/1（各/8）|
|ETH component N=4250 cap=0.0525|rejected|7.494946 / 7.095275 / 6.695780|1.618906|1.860646|3.852567|7/13|0/0/0（各/8）|
|ETH component N=4250 cap=0.05625|rejected|7.494946 / 7.095275 / 6.695780|1.618906|1.860646|3.852567|7/13|0/0/0（各/8）|
|ETH benchmark N=4250 cap=None|rejected|-14.827610 / -15.637919 / -16.448087|20.570648|-1.337913|-0.750764|6/13|1/1/1（各/8）|
|BTC component N=1750 cap=None|passed|31.938675 / 29.755723 / 27.572790|9.759986|1.560450|2.615132|10/13|6/6/6（各/8）|
|BTC benchmark N=1750 cap=None|rejected|-17.935893 / -19.612175 / -21.288462|26.210108|-1.258092|-0.764038|6/13|1/1/1（各/8）|
|ETH component N=3250 cap=0.0525|rejected|5.731091 / 5.426091 / 5.121066|1.253963|1.861648|3.805964|7/13|0/0/0（各/8）|
|ETH component N=3250 cap=0.05625|rejected|5.731091 / 5.426091 / 5.121066|1.253963|1.861648|3.805964|7/13|0/0/0（各/8）|
|ETH benchmark N=3250 cap=None|rejected|-11.341154 / -11.960822 / -12.580549|15.823889|-1.360430|-0.745421|6/13|1/1/1（各/8）|
|组合 benchmark BTC/ETH=750/4250 cap=None|rejected|-13.431471 / -14.226386 / -15.021188|18.764361|-1.357990|-0.751234|6/13|1/1/1（各/8）|
|组合 benchmark BTC/ETH=1750/3250 cap=None|rejected|-12.660102 / -13.491093 / -14.322132|17.845633|-1.370325|-0.752954|6/13|1/1/1（各/8）|
|组合 candidate BTC/ETH=750/4250 cap=0.0525|passed|8.570450 / 8.074741 / 7.579164|1.393581|2.288984|5.064515|12/13|6/6/6（各/8）|
|组合 candidate BTC/ETH=750/4250 cap=0.05625|passed|8.570450 / 8.074741 / 7.579164|1.393581|2.288984|5.064515|12/13|6/6/6（各/8）|
|组合 candidate BTC/ETH=1750/3250 cap=0.0525|passed|10.972608 / 10.292018 / 9.611411|1.824314|2.207982|4.902967|11/13|6/6/6（各/8）|
|组合 candidate BTC/ETH=1750/3250 cap=0.05625|passed|10.972608 / 10.292018 / 9.611411|1.824314|2.207982|4.902967|11/13|6/6/6（各/8）|

相对旧固定总额1250/3750、同ETH上限的三倍成本变化：
BTC/ETH=750/4250 cap=0.0525：收益-1.068021个百分点，整体DD0.061041个百分点，Sharpe-0.028418，Calmar-0.976320。
BTC/ETH=750/4250 cap=0.05625：收益-1.068021个百分点，整体DD0.061041个百分点，Sharpe-0.028418，Calmar-0.976320。
BTC/ETH=1750/3250 cap=0.0525：收益0.964226个百分点，整体DD0.491774个百分点，Sharpe-0.109421，Calmar-1.137868。
BTC/ETH=1750/3250 cap=0.05625：收益0.964226个百分点，整体DD0.491774个百分点，Sharpe-0.109421，Calmar-1.137868。

同本金且同目标金额持有基准（三倍成本）：
BTC/ETH=750/4250：净收益-15.021188%，整体DD18.764361%；指纹2c5b491d9fa8a432c767f7d23bfa8f0af4a91d4830918f528a8856a08916c8c3。
BTC/ETH=1250/3750：净收益-14.532603%，整体DD18.130209%；指纹d3c0aacfc001f6879026616b22d4e443bb9792dedf84f89e2211636a377a1845。
BTC/ETH=1750/3250：净收益-14.322132%，整体DD17.845633%；指纹6960bf2a5b31fd413a1fb721c528dc332cf1770154a27679e585bd8cecf1d167。

敏感性保存全部72成本场景、1008逐折、576近期折、288扩展折、28224日NAV行、16条相邻边及六面热图。新定义16项有12条不同完整成本路径；ETH native同时检验金额/上限两轴，BTC组件沿金额一轴；只读历史对照不重分类。
启发式跳变边：[{"scope": "parent", "from": "parent_fixedGross5000_BTCN1250_ETHN3750_Cap0p0525_C3750_15000_391d", "to": "parent_fixedGross5000_BTCN1750_ETHN3250_Cap0p0525_C3750_15000_391d", "delta_net_pp": 0.964226180974137, "delta_sharpe": -0.10942097551032948, "delta_DD_pp": 0.4917737298350988, "delta_Calmar": -1.1378682707654795}, {"scope": "parent", "from": "parent_fixedGross5000_BTCN1250_ETHN3750_Cap0p05625_C3750_15000_391d", "to": "parent_fixedGross5000_BTCN1750_ETHN3250_Cap0p05625_C3750_15000_391d", "delta_net_pp": 0.964226180974137, "delta_sharpe": -0.10942097551032948, "delta_DD_pp": 0.4917737298350988, "delta_Calmar": -1.1378682707654795}]
参数边界、重复路径、平局与变差指标全部保留；小网格不能证明全域稳健，不根据结果增加网格或替换事前代表。

失败判据保持：各成本全期/近期为正、1x≥10/13正月、各成本近40日≥6/8正5日折、扩展≥3/4正折、DD3≤25%、局部正收益/近期比例≥60%、≥4次平仓、1x(毛价差收益+资金费)/费用≥2.5，无拒单/负抵押/保证金代理违规、终点flat。
BTC_L29H0p03E0p005V10Cap0p0275Confirm5Min0p0025_C3750_N750_391d：通过预设历史门槛，仍待独立未来验证。
hold_BTC_C3750_N750_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
ETH_L5H0p02E0p0075EWMS16D3K0p0075V6Cap0p0525_M4R0p0075VW9_C15000_N4250_391d：ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_recent6of8_allcost_gte60pct；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
ETH_L5H0p02E0p0075EWMS16D3K0p0075V6Cap0p05625_M4R0p0075VW9_C15000_N4250_391d：ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_recent6of8_allcost_gte60pct；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
hold_ETH_C15000_N4250_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
BTC_L29H0p03E0p005V10Cap0p0275Confirm5Min0p0025_C3750_N1750_391d：通过预设历史门槛，仍待独立未来验证。
hold_BTC_C3750_N1750_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；composite_DD3_lte25pct；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
ETH_L5H0p02E0p0075EWMS16D3K0p0075V6Cap0p0525_M4R0p0075VW9_C15000_N3250_391d：ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_recent6of8_allcost_gte60pct；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
ETH_L5H0p02E0p0075EWMS16D3K0p0075V6Cap0p05625_M4R0p0075VW9_C15000_N3250_391d：ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_recent6of8_allcost_gte60pct；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
hold_ETH_C15000_N3250_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_fixedGross5000_matched_hold_BTCN750_ETHN4250_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_fixedGross5000_matched_hold_BTCN1750_ETHN3250_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_fixedGross5000_BTCN750_ETHN4250_Cap0p0525_C3750_15000_391d：通过预设历史门槛，仍待独立未来验证。
parent_fixedGross5000_BTCN750_ETHN4250_Cap0p05625_C3750_15000_391d：通过预设历史门槛，仍待独立未来验证。
parent_fixedGross5000_BTCN1750_ETHN3250_Cap0p0525_C3750_15000_391d：通过预设历史门槛，仍待独立未来验证。
parent_fixedGross5000_BTCN1750_ETHN3250_Cap0p05625_C3750_15000_391d：通过预设历史门槛，仍待独立未来验证。

独立核验11730个新决策、5865个旧决策及完整现金/LOT/成交/资金费/成本/小时风险/NAV；BTC/ETH真实旧新现金流增量桥接见sizing_effect_decomposition.json，完整原中心NAV复用。36组合成LOT/非线性冲击/资金费用例不算行情回测。

本轮SMA/candidate 2026-11-18T22:30:00Z→2026-11-19T00:30:00Z按各自原冻结内核处理Nov19_00:01；SMA真实71日SPOT在任何本轮reserve前获取且保持原70精确前缀，candidate以其自身旧q记实际00资金费，资金费支出按1/2/3倍、收入不放大。L4/FEWM 2026-11-19T00:10:00Z→2026-11-19T02:10:00Z仅延续闭合分钟，已记00及日决策不重复。实际日事件{'SMA': 1, 'candidate': 1, 'l4h02': 0, 'fewm': 0}、资金费{'SMA': 0, 'candidate': 6, 'l4h02': 0, 'fewm': 0}、成交{'SMA': 0, 'candidate': 3, 'l4h02': 0, 'fewm': 0}来自独立核验原账本；现金逐笔衔接，不重置本金/desired/持仓。首Nov19_00来源UTC保持2026-11-19T12:46:38.135135Z，所有旧首来源字节/时间不变。现三永续00与四账户Nov19日决策均恰好一次；下一SMA/candidate ['2026-11-19T00:30:00Z', '2026-11-19T02:30:00Z']、L4/FEWM ['2026-11-19T02:10:00Z', '2026-11-19T04:10:00Z']均在Nov20_00:01前只增加闭合分钟并查询实际特殊资金费，不预记未来事件。SMA下轮复用完整71日权威，分钟包不能充当日线。研究金额不写入冻结账户。

原SMA三倍成本累计收益-7.468958%。原账户为延迟shadow，原180日/六折资格未成熟；十策略实时公开报价模拟仅只读汇总，未产生新成交或改冻结规则。
保存21份唯一公共GET回执，本轮21、旧复用0、实际运输失败1。首00/08/16的UTC/SHA保持，full71 SPOT真实权威及完整70日原始前缀保留。本轮其他失败事实：[{"command": ["/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python", "-B", "/home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T143526Z/prefetch_sma71.py"], "cwd": "/home/desktop/Documents/Codex/EquiTide", "started_utc": "2026-11-19T14:44:00.567134Z", "finished_utc": "2026-11-19T14:44:00.876339Z", "exit_code": 1, "log": "research/experiments/20261119T143526Z/sma65_prebinding_capture.log", "stderr": "Traceback (most recent call last):\n  File \"/home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T143526Z/prefetch_sma71.py\", line 21, in <module>\n    authority = ROOT / h['SMA_full71_authority']\n                       ~^^^^^^^^^^^^^^^^^^^^^^^^\nKeyError: 'SMA_full71_authority'\n", "resolved": true, "reason": "Pre-request source-key error fixed before any data request/reservation/account or financial computation;failed exact source retained", "failed_source": "research/experiments/20261119T143526Z/pre_context_key_fix/prefetch_sma71.py", "failed_source_sha256": "ffdb6f4ce94b30d723221c32c5759e98519e63ef4554bdf5190cc05bb9f73422"}, {"url": "https://fapi.binance.com/fapi/v1/markPriceKlines?symbol=BTCUSDT&interval=1h&startTime=1795035600000&endTime=1795042800000&limit=1500", "started_utc": "2026-11-19T14:54:50.401713+00:00", "http_status": 0, "raw": "data/raw/binance/candidate_forward/20261119T143526Z/http_attempt_0001.gz", "sha256": "f61f27bd17de546264aa58f40f3aafaac7021e0ef69c17f6b1b4cd7664a037ec", "bytes": 0, "transport": "curl compressed verifiedTLSmin1.2,separate bounded attempts", "curl_exit_code": 28, "stderr": "curl: (28) Connection timed out after 10000 milliseconds\n", "resolved": true, "resolution": "Same exact URL has validated successful saved public bytes; original capture time retained, including earlier source reuse documented before first reserve. Successful original account packet and audit retained."}]
只读监控生成成功=True；11164研究配置，11148旧行完整字典不变。

实际阶段命令（已完成目录禁止重评，回执与数据哈希用于核验）：

```sh
cd /home/desktop/Documents/Codex/EquiTide
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T143526Z/commands.py prefetch # 原准备失败exit1，后续retry有效
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T143526Z/commands.py prefetch_retry1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T143526Z/commands.py prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T143526Z/commands.py freeze
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T143526Z/commands.py units
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T143526Z/commands.py bind
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T143526Z/commands.py reserve_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T143526Z/commands.py reserve_1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T143526Z/commands.py evaluate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T143526Z/commands.py audit
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T143526Z/commands.py exports
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T143526Z/commands.py finish_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T143526Z/commands.py finish_1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T143526Z/commands.py research_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T143526Z/commands.py l4h02
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T143526Z/commands.py fewm
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T143526Z/commands.py candidate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T143526Z/commands.py forward
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T143526Z/commands.py accounts_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T143526Z/commands.py journal
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T143526Z/commands.py sources_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T143526Z/commands.py gates
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T143526Z/commands.py feed
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T143526Z/commands.py collect
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T143526Z/commands.py final_checks
```

全部真实结果、负折、spec、登记、原始响应、来源SHA及实际失败保留。字段依据[Binance官方REST文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)，格式依据[公共数据README](https://github.com/binance/binance-public-data/blob/master/README.md)；访问日期及版本限定见primary_source_access.json。成本系数与模型不是交易所收益保证。
