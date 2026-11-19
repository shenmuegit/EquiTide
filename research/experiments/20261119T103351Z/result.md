# 20261119T103351Z 固定总目标5000的BTC/ETH分配研究

事前固定BTC/ETH新入场目标1000/4000旧只读、1250/3750、1500/3500，交叉ETH入场V6波动上限.0525/.05625。代表1250/3750及cap.05625不随结果改变。12项新配置：4个ETH策略银行、2个ETH同金额持有银行、4个策略组合、2个组合持有基准，全部先reserve后实际计算一次并finish。历史门槛通过组合4/4，ETH组件0/4；所有淘汰结果留档。严格同时改善收益、整体回撤、Sharpe、Calmar为0/4；没有独立未来资格或稳定实盘盈利结论。

完整读取38576条登记事件、19149个ID、473份既往结论、29份附加材料。初始16项真实结果缺口0；规范研究定义11561→11573、正式有结果11360。定义数量不是独立试验次数，无DSR/PBO显著性证明。

经济假设：上一批提高BTC金额同时提高总目标敞口；本批固定初始目标总额5000，观察分配本身的影响。BTC本金3750、ETH本金15000，总18750、原始完整银行权重[1,1]和20/80初始本金占比保持，不归一化。目标分配为20/80、25/75、30/70的名义金额比例，并非本金再分配。每个银行保留同方向实际数量，价格和持仓状态改变会使实际动态敞口变化，不能称动态风险固定。BTC全部真实银行只读复用；只对改变金额的ETH数量、LOT、不利tick、手续费、价差、滑点、平方根成交量冲击、资金费和保证金代理重新核算，无NAV线性缩放、保证金转移、父组合交易或每日再平衡。

完整规则：BTCfixedL29/H.03/exitE.005,V10samplelogvolcap.0275,strictdirection*recent5ROC>.0025 new/reversalonly,retainactualq;allBTCbanksN1000/1250/1500readonly. ETHlongonlyL5/H.02/E.0075,finiteEWMS16beta15/17,D3strictabsoluteK.0075,entryV6samplelogvolcaps.0525/.05625,M4signedmature1to36hrealizedfundingmedian,budgetmin(.0002,.0075*samplelogvol9*pastactualintervalh/24),missingblocksnewentryonly. ChangeonlyETHactualentryN4000readonly/3750/3500;keepactualqonunchangeddirection. Constant-long holds bypass strategyfiltersandretainactualqtofinalcostexit. Nofit/labels/futurevalues/outcome-dependentchoices.

新父组合描述字段逐项从实际子spec生成。历史父spec中BTC退出/波动上限及ETH carry R/VW描述有沿用旧值，实际执行组件由冻结指纹和完整账本确定；旧spec/report/状态保持，本批派生一致性检查见parent_metadata_consistency.json。这类描述修正不作为新预测信息，真正变化是ETH实际金额及新组件图。

时间与walk-forward：391日重复开发历史，2025-10-19 00:01→2026-11-14 00:01，33个已闭合上下文日，固定规则无训练、标签或拟合，purge不适用、无标签embargo；新spec明确33/0。13个完整30日折加1日尾段；近40日8×5日；扩展21日5/5/5/6日。跨折继承实际现金和数量，终点计费平仓；整体回撤从连续全NAV计算。重复使用的历史不是未触碰最终测试集。

成本1/2/3倍：每边手续费5bp、半价差1bp、滑点2bp、0.5×过去20日样本对数波动×sqrt(实际订单额/过去20日quoteADV)；不利tick、LOT/minnotional、参与率≤0.001，独立银行完全抵押1倍入场约束和小时不利价1%维持保证金代理。永续资金费支出随倍率增加、收入不放大；线性永续无现货借币。费用和盘口估计是研究假设，缺真实L2/TCA、完整历史阶梯、tick清算及容量实证。

|类型/配置|状态|净收益1x/2x/3x %|整体DD3 %|Sharpe3|Calmar3|正30日折1x|近期5日正折1/2/3|
|---|---|---|---|---|---|---|---|
|ETH component N=3750 cap=0.0525|rejected|6.612376 / 6.259906 / 5.907848|1.437618|1.861160|3.828823|7/13|0/0/0（各/8）|
|ETH component N=3750 cap=0.05625|rejected|6.612376 / 6.259906 / 5.907848|1.437618|1.861160|3.828823|7/13|0/0/0（各/8）|
|ETH benchmark N=3750 cap=None|rejected|-13.077599 / -13.792144 / -14.506822|18.194813|-1.349410|-0.748078|6/13|1/1/1（各/8）|
|ETH component N=3500 cap=0.0525|rejected|6.171521 / 5.842848 / 5.514102|1.346518|1.861319|3.815900|7/13|0/0/0（各/8）|
|ETH component N=3500 cap=0.05625|rejected|6.171521 / 5.842848 / 5.514102|1.346518|1.861319|3.815900|7/13|0/0/0（各/8）|
|ETH benchmark N=3500 cap=None|rejected|-12.209377 / -12.876483 / -13.543653|17.011033|-1.354964|-0.746747|6/13|1/1/1（各/8）|
|组合 benchmark BTC/ETH=1250/3750 cap=None|rejected|-12.928259 / -13.730378 / -14.532603|18.130209|-1.365736|-0.752085|6/13|1/1/1（各/8）|
|组合 benchmark BTC/ETH=1500/3500 cap=None|rejected|-12.906283 / -13.733310 / -14.560396|18.147414|-1.367814|-0.752817|6/13|1/1/1（各/8）|
|组合 candidate BTC/ETH=1250/3750 cap=0.0525|passed|9.834069 / 9.240477 / 8.647185|1.332540|2.317403|6.040835|12/13|6/6/6（各/8）|
|组合 candidate BTC/ETH=1250/3750 cap=0.05625|passed|9.834069 / 9.240477 / 8.647185|1.332540|2.317403|6.040835|12/13|6/6/6（各/8）|
|组合 candidate BTC/ETH=1500/3500 cap=0.0525|passed|10.346555 / 9.715071 / 9.083518|1.536714|2.275565|5.501792|12/13|6/6/6（各/8）|
|组合 candidate BTC/ETH=1500/3500 cap=0.05625|passed|10.346555 / 9.715071 / 9.083518|1.536714|2.275565|5.501792|12/13|6/6/6（各/8）|

相对旧固定总额1000/4000、同ETH上限的三倍成本变化：
BTC/ETH=1250/3750 cap=0.0525：收益0.451093个百分点，整体DD-0.025293个百分点，Sharpe-0.025548，Calmar0.420989。
BTC/ETH=1250/3750 cap=0.05625：收益0.451093个百分点，整体DD-0.025293个百分点，Sharpe-0.025548，Calmar0.420989。
BTC/ETH=1500/3500 cap=0.0525：收益0.887427个百分点，整体DD0.178880个百分点，Sharpe-0.067385，Calmar-0.118054。
BTC/ETH=1500/3500 cap=0.05625：收益0.887427个百分点，整体DD0.178880个百分点，Sharpe-0.067385，Calmar-0.118054。

相对同BTC金额、旧ETH4000较高总额的三倍成本变化：
BTC/ETH=1250/3750 cap=0.0525：收益-0.315218个百分点，整体DD-0.060957个百分点，Sharpe-0.006725，Calmar0.054268。
BTC/ETH=1250/3750 cap=0.05625：收益-0.315218个百分点，整体DD-0.060957个百分点，Sharpe-0.006725，Calmar0.054268。
BTC/ETH=1500/3500 cap=0.0525：收益-0.630215个百分点，整体DD0.002259个百分点，Sharpe-0.027578，Calmar-0.389215。
BTC/ETH=1500/3500 cap=0.05625：收益-0.630215个百分点，整体DD0.002259个百分点，Sharpe-0.027578，Calmar-0.389215。

同本金且同目标金额持有基准（三倍成本）：
BTC/ETH=1000/4000：净收益-14.782911%，整体DD18.454767%；指纹102c4b4aa82c9d870d3a8be8ef235a82139aa0518e0a4a2a6d5dcff2de7bb3a4。
BTC/ETH=1250/3750：净收益-14.532603%，整体DD18.130209%；指纹d3c0aacfc001f6879026616b22d4e443bb9792dedf84f89e2211636a377a1845。
BTC/ETH=1500/3500：净收益-14.560396%，整体DD18.147414%；指纹b5a4c83a15705c80c04b7ff44e4d0feb624ff19e007ebda64ee601c74e24a6a2。

敏感性保存全部84成本场景、1176逐折、672近期折、336扩展折、32928日NAV行、16条相邻边及六面热图。新定义12项有8条不同完整成本路径；ETH native同时检验金额/上限两轴，BTC旧组件沿金额一轴；只读历史对照不重分类。
启发式跳变边：[{"scope": "parent", "from": "parent_fixedGross5000_BTCN1250_ETHN3750_Cap0p0525_C3750_15000_391d", "to": "parent_fixedGross5000_BTCN1500_ETHN3500_Cap0p0525_C3750_15000_391d", "delta_net_pp": 0.43633313481390523, "delta_sharpe": -0.04183764212850427, "delta_DD_pp": 0.20417358277181608, "delta_Calmar": -0.5390427929578481}, {"scope": "parent", "from": "parent_fixedGross5000_BTCN1250_ETHN3750_Cap0p05625_C3750_15000_391d", "to": "parent_fixedGross5000_BTCN1500_ETHN3500_Cap0p05625_C3750_15000_391d", "delta_net_pp": 0.43633313481390523, "delta_sharpe": -0.04183764212850427, "delta_DD_pp": 0.20417358277181608, "delta_Calmar": -0.5390427929578481}]
参数边界、重复路径、平局与变差指标全部保留；小网格不能证明全域稳健，不根据结果增加网格或替换事前代表。

失败判据保持：各成本全期/近期为正、1x≥10/13正月、各成本近40日≥6/8正5日折、扩展≥3/4正折、DD3≤25%、局部正收益/近期比例≥60%、≥4次平仓、1x(毛价差收益+资金费)/费用≥2.5，无拒单/负抵押/保证金代理违规、终点flat。
ETH_L5H0p02E0p0075_EWMS16D3K0p0075_V6Cap0p0525_M4R0p0075VW9_C15000_N3750_391d：ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_recent6of8_allcost_gte60pct；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
ETH_L5H0p02E0p0075_EWMS16D3K0p0075_V6Cap0p05625_M4R0p0075VW9_C15000_N3750_391d：ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_recent6of8_allcost_gte60pct；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
hold_ETH_C15000_N3750_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
ETH_L5H0p02E0p0075_EWMS16D3K0p0075_V6Cap0p0525_M4R0p0075VW9_C15000_N3500_391d：ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_recent6of8_allcost_gte60pct；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
ETH_L5H0p02E0p0075_EWMS16D3K0p0075_V6Cap0p05625_M4R0p0075VW9_C15000_N3500_391d：ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_recent6of8_allcost_gte60pct；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
hold_ETH_C15000_N3500_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_fixedGross5000_matched_hold_BTCN1250_ETHN3750_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_fixedGross5000_matched_hold_BTCN1500_ETHN3500_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_fixedGross5000_BTCN1250_ETHN3750_Cap0p0525_C3750_15000_391d：通过预设历史门槛，仍待独立未来验证。
parent_fixedGross5000_BTCN1250_ETHN3750_Cap0p05625_C3750_15000_391d：通过预设历史门槛，仍待独立未来验证。
parent_fixedGross5000_BTCN1500_ETHN3500_Cap0p0525_C3750_15000_391d：通过预设历史门槛，仍待独立未来验证。
parent_fixedGross5000_BTCN1500_ETHN3500_Cap0p05625_C3750_15000_391d：通过预设历史门槛，仍待独立未来验证。

独立核验7038个新决策、10557个旧决策及完整现金/LOT/成交/资金费/成本/小时风险/NAV；ETH真实旧新现金流增量桥接见sizing_effect_decomposition.json，BTC完整原NAV复用。18组合成LOT/非线性冲击/资金费用例不算行情回测。

下一L4/FEWM窗口跨Nov19_00:01：必须补齐Nov18完整永续日线、保留各自partial/现金/数量，用原冻结日决策核算；完整实际资金费查询须在下一次reserve前完成，新增首00来源保存原UTC/字节，不预入账、不沿用别人现金流。SMA/single下一窗仍mark-only、继续full70权威。 本轮SMA/single 2026-11-18T18:30:00Z→2026-11-18T20:30:00Z、L4/FEWM 2026-11-18T20:10:00Z→2026-11-18T22:10:00Z均无日决策。实际资金费行{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、日事件{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、新成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}来自实际执行和完整历史链审计。三永续账户在前轮均已各记16一次，本轮窗口位于其后，不重复入账；现金按实际本窗事件核对，持仓/入场/desired/执行费用保持，资金费后的现金不重置。首16来源UTC仍2026-11-19T02:38:28.559917Z且SHA不变，首00/08亦保留；新查询UTC为2026-11-19T10:41:28.785975Z，本窗不包含已知16记录时不把空响应当旧记录变更。下一SMA/single ['2026-11-18T20:30:00Z', '2026-11-18T22:30:00Z']、L4/FEWM ['2026-11-18T22:10:00Z', '2026-11-19T00:10:00Z']继续各自原账本、不得重复16，仍须完整查询实际特殊事件。四账户下一原日决策Nov19_00:01，完整70日SPOT权威及69日前缀保留；不采用本轮研究金额或风险参数，不重启、强平或重置本金。

原SMA三倍成本累计收益-7.468958%。原账户为延迟shadow，原180日/六折资格未成熟；十策略实时公开报价模拟仅只读汇总，未产生新成交或改冻结规则。
保存20份唯一公共GET回执，本轮20、旧复用0、实际运输失败2。首00/08/16的UTC/SHA保持，full70 SPOT原始权威保留。本轮其他失败事实：[{"url": "https://fapi.binance.com/fapi/v1/exchangeInfo", "started_utc": "2026-11-19T10:52:45.530632+00:00", "http_status": 0, "curl_exit_code": 35, "raw": "data/raw/binance/l4h02_forward/20261119T103351Z/http_0000.gz", "sha256": "f61f27bd17de546264aa58f40f3aafaac7021e0ef69c17f6b1b4cd7664a037ec", "bytes": 0, "stderr": "curl: (35) TLS connect error: error:0A000126:SSL routines::unexpected eof while reading\n", "transport": "verifiedTLSmin1.2HTTP1.1 publicGET,bounded3attempts", "resolved": true, "resolution": "Same exact URL has validated successful saved public bytes; original capture time retained, including earlier source reuse documented before first reserve. Successful original account packet and audit retained."}, {"url": "https://fapi.binance.com/fapi/v1/klines?symbol=ETHUSDT&interval=1m&startTime=1795032540000&endTime=1795039800000&limit=1500", "started_utc": "2026-11-19T10:53:22.255449+00:00", "http_status": 0, "curl_exit_code": 35, "raw": "data/raw/binance/l4h02_forward/20261119T103351Z/http_0006.gz", "sha256": "f61f27bd17de546264aa58f40f3aafaac7021e0ef69c17f6b1b4cd7664a037ec", "bytes": 0, "stderr": "curl: (35) TLS connect error: error:0A000126:SSL routines::unexpected eof while reading\n", "transport": "verifiedTLSmin1.2HTTP1.1 publicGET,bounded3attempts", "resolved": true, "resolution": "Same exact URL has validated successful saved public bytes; original capture time retained, including earlier source reuse documented before first reserve. Successful original account packet and audit retained."}]
只读监控生成成功=True；11132研究配置，11120旧行完整字典不变。

实际阶段命令（已完成目录禁止重评，回执与数据哈希用于核验）：

```sh
cd /home/desktop/Documents/Codex/EquiTide
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T103351Z/commands.py prepare
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T103351Z/commands.py freeze
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T103351Z/commands.py units
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T103351Z/commands.py bind
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T103351Z/commands.py reserve_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T103351Z/commands.py reserve_1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T103351Z/commands.py evaluate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T103351Z/commands.py audit
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T103351Z/commands.py exports
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T103351Z/commands.py finish_0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T103351Z/commands.py finish_1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T103351Z/commands.py research_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T103351Z/commands.py l4h02
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T103351Z/commands.py fewm
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T103351Z/commands.py candidate
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T103351Z/commands.py forward
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T103351Z/commands.py accounts_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T103351Z/commands.py journal
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T103351Z/commands.py sources_check
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T103351Z/commands.py gates
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T103351Z/commands.py feed
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T103351Z/commands.py collect
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T103351Z/commands.py final_checks
```

全部真实结果、负折、spec、登记、原始响应、来源SHA及实际失败保留。字段依据[Binance官方REST文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)，格式依据[公共数据README](https://github.com/binance/binance-public-data/blob/master/README.md)；访问日期及版本限定见primary_source_access.json。成本系数与模型不是交易所收益保证。
