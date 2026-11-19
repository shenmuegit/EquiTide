# 20261119T063119Z BTC实际入场金额与匹配持有基准研究

预先固定BTC每次新入场目标N=[1000旧只读,1250,1500]USDT × 已有ETH入场V6波动上限[0.0525,0.05625]，代表N1250/cap0.05625不随结果改变。10项新配置包括2个BTC策略银行、2个BTC同金额持有银行、4个策略组合和2个组合持有基准，均先独立reserve后计算一次并finish。组合历史门槛通过4/4，BTC组件通过2/2。严格同时改善收益、整体DD、Sharpe和Calmar为0/4。历史正收益不代表稳定实盘盈利，仍无独立未来资格。

完整读取38492条登记事件、19107个ID、472份既往结论、29份附加材料。初始16项实际结果缺口0；legacy原标记及原始ZIP证据分别保留。规范研究定义11551→11561，正式有结果11348；定义数并非独立试验数，无DSR/PBO显著性证明。

经济假设：提高BTC实际入场金额可能提高其对BTC/ETH组合的贡献，同时增加风险、费用和冲击。BTC本金3750、ETH本金15000，总初始18750不变；原始完整银行权重[1,1]原值保留，20/80仅初始本金占比。ETH每次入场目标4000；BTC目标1250/1500分别占其本金1/3、40%，与ETH同时新开仓时合计目标5250/5500，并非总风险不变。每次数量按前一完整日收盘和LOT向下取整，下一分钟OPEN按不利tick成交；全部新BTC策略及持有金额重新计算现金、手续费、价差、滑点、量相关冲击、资金费和保证金代理。没有线性缩放旧NAV、转移保证金、每日再平衡、父组合订单或跨银行抵消。

完整固定规则：StrategyBTC fixedL29/strictH.03/exitE.005;entryV10 samplelogvol<=.0275 and direction*strictRecent5ROC>.0025 onlynew/reversed;keepactualsame-directionq. Vary onlyactualBTCentryN1000readonly/1250/1500 atC3750. ETHexactreadonlylongonlyL5/H.02/E.0075,finiteEWMS16beta15/17,D3strictabsoluteK.0075,entryV6cap[.0525,.05625],M4signedactualmature1to36hfundmedian,VW9budgetmin(.0002,R.0075*samplelogvol9*actualpastintervalh/24),missingblocksnewentryonly,thenlongonly. Constant-long reference specs use signal_mode=constant_long_reference, bypass strategy filters and retain their actual q until finalcostexit. No fit,labels,futurevalues or outcome-dependent choices.

持有比较：每个BTC金额都有自己的同本金、同目标入场金额的constant-long银行；ETH持有银行仍为本金15000/目标4000。组合持有基准逐一匹配BTC金额，保留真实负收益和成本，不把1000金额的旧持有曲线冒充1250/1500的基准。现金收益为0。匹配的是本金和目标金额，并不声称动态风险完全相同。

Walk-forward：2025-10-19 00:01→2026-11-14 00:01，391日复用开发历史、33日闭合上下文。固定规则，无拟合、标签或未来值；13个完整30日折加1日尾段、近40日8×5日、扩展21日5/5/5/6日。跨折继承现金和数量，仅终点计费平仓；整体回撤来自连续完整NAV。已有反复研究日期不能称未触碰最终测试集。

成本1/2/3倍：每边手续费5bp、半价差1bp、滑点2bp，冲击0.5×过去20日样本对数波动×sqrt(实际订单额/过去20日quoteADV)。不利tick、LOT和minnotional，参与率≤0.001、完全抵押1倍入场上限、小时不利价1%维持保证金代理。永续资金费支出随倍率增加，收入不放大；USDT线性永续无现货借币。手续费及盘口成本为研究假设，缺L2/TCA、完整历史阶梯、tick清算和容量实证。

|类型/配置|状态|净收益1x/2x/3x %|整体DD3 %|Sharpe3|Calmar3|正30日折1x|近5日正折1/2/3|
|---|---|---|---|---|---|---|---|
|native/component BTC N=1250|passed|22.720839 / 21.162758 / 19.604534|7.257704|1.548612|2.506190|10/13|6/6/6（各/8）|
|native/benchmark BTC N=1250|rejected|-12.330897 / -13.483312 / -14.635730|18.221668|-1.305221|-0.753649|6/13|1/1/1（各/8）|
|native/component BTC N=1500|passed|27.046688 / 25.203962 / 23.361183|8.349940|1.555188|2.592947|10/13|6/6/6（各/8）|
|native/benchmark BTC N=1500|rejected|-15.693907 / -17.160616 / -18.627367|23.036101|-1.277577|-0.759865|6/13|1/1/1（各/8）|
|parent/benchmark BTC N=1250|rejected|-13.633689 / -14.474407 / -15.315129|19.089354|-1.360490|-0.752977|6/13|1/1/1（各/8）|
|parent/benchmark BTC N=1500|rejected|-14.306291 / -15.209868 / -16.113456|20.043921|-1.357439|-0.754723|6/13|1/1/1（各/8）|
|parent/candidate BTC N=1250 ETHcap=0.0525|passed|10.187134 / 9.574699 / 8.962403|1.393497|2.324128|5.986568|12/13|6/6/6（各/8）|
|parent/candidate BTC N=1250 ETHcap=0.05625|passed|10.187134 / 9.574699 / 8.962403|1.393497|2.324128|5.986568|12/13|6/6/6（各/8）|
|parent/candidate BTC N=1500 ETHcap=0.0525|passed|11.052304 / 10.382940 / 9.713733|1.534455|2.303143|5.891008|12/13|6/6/6（各/8）|
|parent/candidate BTC N=1500 ETHcap=0.05625|passed|11.052304 / 10.382940 / 9.713733|1.534455|2.303143|5.891008|12/13|6/6/6（各/8）|

相对同ETH上限、BTC旧N1000组合的三倍成本增量：
N=1250/ETHcap=0.0525：净收益0.766312个百分点，整体DD0.035664个百分点，Sharpe-0.018823，Calmar0.366722。收益提高若伴随DD上升或Sharpe下降，按真实风险取舍披露，不称全部指标改善。
N=1250/ETHcap=0.05625：净收益0.766312个百分点，整体DD0.035664个百分点，Sharpe-0.018823，Calmar0.366722。收益提高若伴随DD上升或Sharpe下降，按真实风险取舍披露，不称全部指标改善。
N=1500/ETHcap=0.0525：净收益1.517641个百分点，整体DD0.176621个百分点，Sharpe-0.039808，Calmar0.271161。收益提高若伴随DD上升或Sharpe下降，按真实风险取舍披露，不称全部指标改善。
N=1500/ETHcap=0.05625：净收益1.517641个百分点，整体DD0.176621个百分点，Sharpe-0.039808，Calmar0.271161。收益提高若伴随DD上升或Sharpe下降，按真实风险取舍披露，不称全部指标改善。

同本金且同目标金额持有基准（3倍成本）：
BTC N=1000/ETH N4000：净收益-14.782911%，整体DD18.454767%；来源指纹102c4b4aa82c9d870d3a8be8ef235a82139aa0518e0a4a2a6d5dcff2de7bb3a4。
BTC N=1250/ETH N4000：净收益-15.315129%，整体DD19.089354%；来源指纹c7502ea5334079a33c05409f8439a41a5fe474362773d5e07da2701a15cce6a3。
BTC N=1500/ETH N4000：净收益-16.113456%，整体DD20.043921%；来源指纹c9a1ce162e468f0c2a2fb64c66310081b732cf51fe1b1dab8c058069d4b1f287。

敏感性保存全部54成本场景、756个逐折、432个近期折、216个扩展折、21168行日NAV、10条相邻边及六面热图；各新配置含3成本场景。新定义10项有8条不同完整成本路径，其中0条匹配旧参考。ETH上限不同可能产生相同路径，均如实保留，不将其当独立盈利证据。
启发式跳变边：[{"scope": "parent", "from": "parent_BTC_N1250_ETHCap0p0525_C3750_15000_ETHN4000_391d", "to": "parent_BTC_N1500_ETHCap0p0525_C3750_15000_ETHN4000_391d", "delta_net_pp": 0.7513297919299777, "delta_sharpe": -0.02098466242503072, "delta_DD_pp": 0.1409573818246912, "delta_Calmar": -0.09556023289812021}, {"scope": "parent", "from": "parent_BTC_N1250_ETHCap0p05625_C3750_15000_ETHN4000_391d", "to": "parent_BTC_N1500_ETHCap0p05625_C3750_15000_ETHN4000_391d", "delta_net_pp": 0.7513297919299777, "delta_sharpe": -0.02098466242503072, "delta_DD_pp": 0.1409573818246912, "delta_Calmar": -0.09556023289812021}]
小网格只说明固定信号和资金规模下的局部结果。金额边界、平局、变差指标和各分项成本全部保留，不根据结果扩网格或把1500替换成事前代表1250；增加敞口并不提供新的预测信息。

失败判据保持：各成本全期/近期净收益为正、1x≥10/13正月、各成本近40日≥6/8正5日折、扩展≥3/4正折、DD3≤25%、局部正收益和严格近期比例≥60%、≥4次平仓、1x(毛价差收益+资金费)/执行费用≥2.5、无拒单/现金/保证金代理违规、终点flat。持有基准只作为比较，其不满足交易策略门槛仍以实际结果rejected保留。
BTC_L29H0p03E0p005_V10Cap0p0275Confirm5Min0p0025_C3750_N1250_391d：通过预设历史门槛，仍待独立未来验证。
hold_BTC_C3750_N1250_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
BTC_L29H0p03E0p005_V10Cap0p0275Confirm5Min0p0025_C3750_N1500_391d：通过预设历史门槛，仍待独立未来验证。
hold_BTC_C3750_N1500_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_matched_hold_BTCN1250_ETHN4000_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_matched_hold_BTCN1500_ETHN4000_C3750_15000_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_BTC_N1250_ETHCap0p0525_C3750_15000_ETHN4000_391d：通过预设历史门槛，仍待独立未来验证。
parent_BTC_N1250_ETHCap0p05625_C3750_15000_ETHN4000_391d：通过预设历史门槛，仍待独立未来验证。
parent_BTC_N1500_ETHCap0p0525_C3750_15000_ETHN4000_391d：通过预设历史门槛，仍待独立未来验证。
parent_BTC_N1500_ETHCap0p05625_C3750_15000_ETHN4000_391d：通过预设历史门槛，仍待独立未来验证。

独立核验4692个新决策、5865个只读决策及完整现金/LOT/成交/资金费/成本/小时风险/NAV。sizing_effect_decomposition.json逐成本核对旧新真实现金流增量；合成18用例可检出朴素数量和冲击线性缩放，合成检查不算行情回测。
准备阶段family大写格式和沿用旧轴名称各触发一次真实失败，均在首个reserve前修复。原未执行草稿、stdout/stderr及有效freeze_retry1/units_retry1回执保留；没有行情模型或已完成账户窗口重跑。

本轮SMA/single 2026-11-18T16:30:00Z→2026-11-18T18:30:00Z、L4/FEWM 2026-11-18T18:10:00Z→2026-11-18T20:10:00Z均无日决策。实际资金费行{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、日事件{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、新成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}来自实际执行和完整历史链审计。三永续账户在前轮均已各记16一次，本轮窗口位于其后，不重复入账；现金按实际本窗事件核对，持仓/入场/desired/执行费用保持，资金费后的现金不重置。首16来源UTC仍2026-11-19T02:38:28.559917Z且SHA不变，首00/08亦保留；新查询UTC为2026-11-19T06:42:41.791483Z，本窗不包含已知16记录时不把空响应当旧记录变更。下一SMA/single ['2026-11-18T18:30:00Z', '2026-11-18T20:30:00Z']、L4/FEWM ['2026-11-18T20:10:00Z', '2026-11-18T22:10:00Z']继续各自原账本、不得重复16，仍须完整查询实际特殊事件。四账户下一原日决策Nov19_00:01，完整70日SPOT权威及69日前缀保留；不采用本轮研究金额或风险参数，不重启、强平或重置本金。

原SMA三倍成本累计收益-7.468958%。四原账户为延迟shadow，原180日/六折计划尚未成熟；十策略真实报价模拟仅只读汇总，未创建新成交或改冻结规则。
保存20份唯一公共GET回执，本轮20、复用旧0、真实运输失败2。未重新下载SPOT日线，原完整70日权威另保留，第一00/08/16来源UTC和SHA保持。
只读监控生成成功=True；11120研究配置，11110旧行完整字典不变。

实际执行命令（已完成目录禁止重评；读取既有证据核验）：

```sh
cd /home/desktop/Documents/Codex/EquiTide
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T063119Z/commands.py prepare # native exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T063119Z/commands.py freeze # native exit=1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T063119Z/commands.py freeze_retry1 # native exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T063119Z/commands.py units # native exit=1
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T063119Z/commands.py units_retry1 # native exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T063119Z/commands.py bind # native exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T063119Z/commands.py reserve_0 # native exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T063119Z/commands.py reserve_1 # native exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T063119Z/commands.py evaluate # native exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T063119Z/commands.py audit # native exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T063119Z/commands.py exports # native exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T063119Z/commands.py finish_0 # native exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T063119Z/commands.py finish_1 # native exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T063119Z/commands.py research_check # native exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T063119Z/commands.py l4h02 # native exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T063119Z/commands.py fewm # native exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T063119Z/commands.py candidate # native exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T063119Z/commands.py forward # native exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T063119Z/commands.py accounts_check # native exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T063119Z/commands.py journal # native exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T063119Z/commands.py sources_check # native exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T063119Z/commands.py gates # native exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T063119Z/commands.py feed # native exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T063119Z/commands.py collect # native exit=0
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261119T063119Z/commands.py final_checks # native exit=0
```

全部真实结果、负折、独立登记、原始响应、数据SHA和失败记录保留。实际资金费/交易过滤字段参考[Binance官方REST文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)，数据格式参考[Binance公共数据README](https://github.com/binance/binance-public-data/blob/master/README.md)。成本系数、风险代理、固定信号及预算均为明确的研究假设，不是交易所对收益或容量的保证；访问日期和版本说明见primary_source_access.json。

收尾说明：本轮始于2026-11-19 06:31 UTC，08:32 UTC触发时先继续保存并推送本批未完成工作；截至本条核验已超过约90分钟目标。没有另开08:32批次、重复回测或重复已完成账户窗口。实际阶段、时间和原生退出码见各commands回执；两个准备失败及运输失败仍完整保留。
