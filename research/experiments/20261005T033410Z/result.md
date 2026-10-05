# BTC/ETH策略研究：20261005T033410Z

本轮36个新历史配置、108成本场景；18个旧配置54场景只读。1倍成本正收益31个，3倍成本正收益28个；通过3、淘汰33。新增跨2025/2026同时合格组合0个。

## 冻结规则与验证

事前固定entry10/15/20 × exit5/10/30双轴，EMA50、±1.5%；中心entry15/exit30为旧只读。BTC/ETH原始资金比例67.5%/32.5%，总2000USDT，对应1350/650独立资金账户，无归一化、再平衡、资金转移或恒定敞口。
仅用已完成日收盘；00:01真实分钟开盘执行。收盘低于此前exit日最小收盘或EMA×.985优先退出；高于此前entry日最大收盘且高于EMA×1.015入场，否则维持。EMA从原始首日递推不重置。OOS起点空仓，期末成本平仓。
2025及2026分别Mar18 00:01至Sep14 00:01 UTC，180天6个连续30日折；180日历史、3日gap。无拟合标签，无同次测试集选择参数。这些历史反复使用，是开发数据，不是未触碰最终测试集。
手续费10bp、半价差1bp、滑点2bp、依赖实际成交金额/前20日quoteADV及收益波动的冲击；四层均施加1/2/3倍压力。最大参与率.001，Decimal28、tick/LOT舍入、最低名义金额及参考价格过滤；假定IOC完整成交，无真实盘口/TCA校准。现货仅多头，不涉及资金费与借币。
八门槛：所有成本正收益、1倍至少4/6正收益折、3倍逐分钟全期回撤≤25%、邻域3倍正收益占比≥60%、至少2轮交易、毛参考收益/成本≥2.5、无账户违规、期末平仓。参数敏感性完整3×3及邻接cliff统计；不同配置不等于独立市场证据。

## 筛选结论

新3个通过项均为2026年exit10组合，entry10/15/20；2025对应配置均因正收益折不足淘汰，因此不列为跨年度合格方法。
entry15组合：2026 exit10三倍成本收益8.60695%，分钟回撤10.49619%，前五折累计-0.14518%；旧exit30为14.94184%、13.21912%、-1.49708%。回撤及前五折改善但仍依赖末折；2025 exit10收益12.46026%，低于旧exit30的42.75414%。2026 exit5收益-1.77329%，不能通过。
淘汰门槛计数（可重叠）：{'four_positive_1x_folds': 33, 'minute_DD3_lte25pct': 5, 'positive_all_costs': 8, 'gross_to_cost1_gte2_5': 8}。新108场景无一个完整NAV与匹配旧exit30相同；2026组合三倍成本有5条不同NAV。

## 全配置、成本与逐折结果

|配置|新测|状态|成本|净收益%|分钟回撤%|六折净收益%|失败门槛|
|---|---|---|---|---|---|---|---|
|filtered_exit_2025_BTC_e10_x5_s50_c1350|True|rejected|1|14.276534|13.140051|0.00000,18.01661,-2.69877,5.98285,-5.22735,-0.92206|four_positive_1x_folds|
|filtered_exit_2025_BTC_e10_x5_s50_c1350|True|rejected|2|12.203532|13.817192|0.00000,17.86232,-3.07909,5.56726,-5.72128,-1.31047|four_positive_1x_folds|
|filtered_exit_2025_BTC_e10_x5_s50_c1350|True|rejected|3|10.169454|14.489817|0.00000,17.70830,-3.45787,5.15154,-6.21095,-1.69639|four_positive_1x_folds|
|filtered_exit_2025_BTC_e10_x10_s50_c1350|True|rejected|1|17.343956|14.019212|0.00000,18.01661,-3.85836,8.29186,-2.73474,-1.81334|four_positive_1x_folds|
|filtered_exit_2025_BTC_e10_x10_s50_c1350|True|rejected|2|15.821231|14.467057|0.00000,17.86232,-4.10846,8.01024,-2.98880,-2.19838|four_positive_1x_folds|
|filtered_exit_2025_BTC_e10_x10_s50_c1350|True|rejected|3|14.321261|14.912277|0.00000,17.70830,-4.35777,7.72904,-3.24121,-2.58025|four_positive_1x_folds|
|filtered_alloc_2025_BTC_e10_s50_c1350|False|passed|1|20.639250|12.130607|0.00000,18.01661,2.04138,4.48170,0.46979,-4.56813||
|filtered_alloc_2025_BTC_e10_s50_c1350|False|passed|2|19.694712|12.184604|0.00000,17.86232,2.04140,4.20644,0.46969,-4.94084||
|filtered_alloc_2025_BTC_e10_s50_c1350|False|passed|3|18.761039|12.415094|0.00000,17.70830,2.04141,3.93794,0.46988,-5.31516||
|filtered_exit_2025_BTC_e15_x5_s50_c1350|True|rejected|1|12.464912|13.912475|0.00000,18.01661,-2.69877,5.03643,-5.88880,-0.92267|four_positive_1x_folds|
|filtered_exit_2025_BTC_e15_x5_s50_c1350|True|rejected|2|10.433724|14.583841|0.00000,17.86232,-3.07909,4.63022,-6.37769,-1.31010|four_positive_1x_folds|
|filtered_exit_2025_BTC_e15_x5_s50_c1350|True|rejected|3|8.430389|15.380723|0.00000,17.70830,-3.45787,4.21773,-6.86412,-1.69664|four_positive_1x_folds|
|filtered_exit_2025_BTC_e15_x10_s50_c1350|True|rejected|1|15.488036|14.783586|0.00000,18.01661,-3.85836,7.32526,-3.41154,-1.81274|four_positive_1x_folds|
|filtered_exit_2025_BTC_e15_x10_s50_c1350|True|rejected|2|13.989846|15.227195|0.00000,17.86232,-4.10846,7.04576,-3.66354,-2.19733|four_positive_1x_folds|
|filtered_exit_2025_BTC_e15_x10_s50_c1350|True|rejected|3|12.511070|15.668171|0.00000,17.70830,-4.35777,6.76671,-3.91469,-2.58057|four_positive_1x_folds|
|filtered_alloc_2025_BTC_e15_s50_c1350|False|passed|1|19.564938|12.738335|0.00000,18.01661,2.04138,3.55079,0.46975,-4.56764||
|filtered_alloc_2025_BTC_e15_s50_c1350|False|passed|2|18.629221|12.965519|0.00000,17.86232,2.04140,3.27806,0.46962,-4.94008||
|filtered_alloc_2025_BTC_e15_s50_c1350|False|passed|3|17.703668|13.194059|0.00000,17.70830,2.04141,3.01149,0.46980,-5.31412||
|filtered_exit_2025_BTC_e20_x5_s50_c1350|True|rejected|1|20.660238|11.684758|0.00000,18.01661,1.97527,7.92356,-5.88661,-1.29061|four_positive_1x_folds|
|filtered_exit_2025_BTC_e20_x5_s50_c1350|True|rejected|2|19.097566|12.377076|0.00000,17.86232,1.84196,7.78711,-6.37781,-1.67691|four_positive_1x_folds|
|filtered_exit_2025_BTC_e20_x5_s50_c1350|True|rejected|3|17.550684|13.060286|0.00000,17.70830,1.70870,7.64555,-6.86449,-2.06259|four_positive_1x_folds|
|filtered_exit_2025_BTC_e20_x10_s50_c1350|True|rejected|1|20.959280|10.508960|0.00000,18.01661,0.51093,7.92562,-3.41223,-2.17811|four_positive_1x_folds|
|filtered_exit_2025_BTC_e20_x10_s50_c1350|True|rejected|2|19.699565|10.741890|0.00000,17.86232,0.37953,7.78345,-3.66389,-2.56135|four_positive_1x_folds|
|filtered_exit_2025_BTC_e20_x10_s50_c1350|True|rejected|3|18.457597|11.114599|0.00000,17.70830,0.24819,7.64674,-3.91600,-2.94290|four_positive_1x_folds|
|filtered_alloc_2025_BTC_e20_s50_c1350|False|passed|1|18.486866|12.130607|0.00000,18.01661,2.04138,2.99887,0.46962,-4.92123||
|filtered_alloc_2025_BTC_e20_s50_c1350|False|passed|2|17.562218|12.130704|0.00000,17.86232,2.04140,2.73279,0.46980,-5.29525||
|filtered_alloc_2025_BTC_e20_s50_c1350|False|passed|3|16.642182|12.130776|0.00000,17.70830,2.04141,2.46207,0.46966,-5.66474||
|filtered_exit_2025_ETH_e10_x5_s50_c650|True|rejected|1|47.293409|22.956478|0.00000,14.79365,-13.46319,21.65961,37.07328,-11.08699|four_positive_1x_folds|
|filtered_exit_2025_ETH_e10_x5_s50_c650|True|rejected|2|44.616491|23.558680|0.00000,14.64162,-14.02751,21.49953,36.71258,-11.66498|four_positive_1x_folds|
|filtered_exit_2025_ETH_e10_x5_s50_c650|True|rejected|3|41.990175|24.161299|0.00000,14.48987,-14.59265,21.34774,36.36370,-12.24628|four_positive_1x_folds|
|filtered_exit_2025_ETH_e10_x10_s50_c650|True|rejected|1|28.483063|25.402539|0.00000,14.79365,-9.67744,14.74507,29.57575,-16.65606|four_positive_1x_folds,minute_DD3_lte25pct|
|filtered_exit_2025_ETH_e10_x10_s50_c650|True|rejected|2|26.485232|25.649791|0.00000,14.64162,-9.91249,14.44686,29.23785,-17.19829|four_positive_1x_folds,minute_DD3_lte25pct|
|filtered_exit_2025_ETH_e10_x10_s50_c650|True|rejected|3|24.509616|26.039827|0.00000,14.48987,-10.14907,14.14679,28.90018,-17.73862|four_positive_1x_folds,minute_DD3_lte25pct|
|filtered_alloc_2025_ETH_e10_s50_c650|False|passed|1|96.855340|19.827489|0.00000,14.79365,0.48705,14.74763,44.99643,2.56949||
|filtered_alloc_2025_ETH_e10_s50_c650|False|passed|2|95.816892|20.036765|0.00000,14.64162,0.48703,14.44592,44.99386,2.43489||
|filtered_alloc_2025_ETH_e10_s50_c650|False|passed|3|94.782041|20.245376|0.00000,14.48987,0.48701,14.14470,44.99065,2.30012||
|filtered_exit_2025_ETH_e15_x5_s50_c650|True|rejected|1|32.923517|26.590786|0.00000,14.79365,-17.54503,21.66147,37.07234,-15.78990|four_positive_1x_folds,minute_DD3_lte25pct|
|filtered_exit_2025_ETH_e15_x5_s50_c650|True|rejected|2|30.506969|27.165049|0.00000,14.64162,-18.08334,21.50079,36.71729,-16.34023|four_positive_1x_folds,minute_DD3_lte25pct|
|filtered_exit_2025_ETH_e15_x5_s50_c650|True|rejected|3|28.140462|27.737117|0.00000,14.48987,-18.61958,21.34806,36.36508,-16.88808|four_positive_1x_folds,minute_DD3_lte25pct|
|filtered_exit_2025_ETH_e15_x10_s50_c650|True|rejected|1|15.954105|28.785392|0.00000,14.79365,-13.93632,14.74831,29.57621,-21.06370|four_positive_1x_folds,minute_DD3_lte25pct|
|filtered_exit_2025_ETH_e15_x10_s50_c650|True|rejected|2|14.152392|29.157785|0.00000,14.64162,-14.16136,14.45130,29.24004,-21.57725|four_positive_1x_folds,minute_DD3_lte25pct|
|filtered_exit_2025_ETH_e15_x10_s50_c650|True|rejected|3|12.354719|29.525949|0.00000,14.48987,-14.38563,14.14635,28.89145,-22.09032|four_positive_1x_folds,minute_DD3_lte25pct|
|filtered_alloc_2025_ETH_e15_s50_c650|False|passed|1|96.855340|19.827489|0.00000,14.79365,0.48705,14.74763,44.99643,2.56949||
|filtered_alloc_2025_ETH_e15_s50_c650|False|passed|2|95.816892|20.036765|0.00000,14.64162,0.48703,14.44592,44.99386,2.43489||
|filtered_alloc_2025_ETH_e15_s50_c650|False|passed|3|94.782041|20.245376|0.00000,14.48987,0.48701,14.14470,44.99065,2.30012||
|filtered_exit_2025_ETH_e20_x5_s50_c650|True|rejected|1|33.554941|27.129466|0.00000,14.79365,-17.54503,20.77432,37.07939,-14.77275|four_positive_1x_folds,minute_DD3_lte25pct|
|filtered_exit_2025_ETH_e20_x5_s50_c650|True|rejected|2|31.468402|27.699376|0.00000,14.64162,-18.08334,20.61330,36.72195,-15.10670|four_positive_1x_folds,minute_DD3_lte25pct|
|filtered_exit_2025_ETH_e20_x5_s50_c650|True|rejected|3|29.403578|28.265719|0.00000,14.48987,-18.61958,20.45119,36.36262,-15.44236|four_positive_1x_folds,minute_DD3_lte25pct|
|filtered_exit_2025_ETH_e20_x10_s50_c650|True|rejected|1|16.501528|29.307614|0.00000,14.79365,-13.93632,13.90931,29.57155,-20.10402|four_positive_1x_folds,minute_DD3_lte25pct|
|filtered_exit_2025_ETH_e20_x10_s50_c650|True|rejected|2|14.976394|29.675812|0.00000,14.64162,-14.16136,13.60492,29.23127,-20.41728|four_positive_1x_folds,minute_DD3_lte25pct|
|filtered_exit_2025_ETH_e20_x10_s50_c650|True|rejected|3|13.477640|30.042560|0.00000,14.48987,-14.38563,13.30967,28.89248,-20.73125|four_positive_1x_folds,minute_DD3_lte25pct|
|filtered_alloc_2025_ETH_e20_s50_c650|False|passed|1|95.416408|20.415190|0.00000,14.79365,0.48705,13.90755,44.99802,2.56956||
|filtered_alloc_2025_ETH_e20_s50_c650|False|passed|2|94.382885|20.622909|0.00000,14.64162,0.48703,13.60737,44.99440,2.43491||
|filtered_alloc_2025_ETH_e20_s50_c650|False|passed|3|93.352973|20.829950|0.00000,14.48987,0.48701,13.30770,44.99011,2.30010||
|filtered_exit_2025_combo_e10_x5_s50_btc0.675|True|rejected|1|25.007019|13.605525|0.00000,16.96915,-6.13214,10.59252,8.45565,-5.07771|four_positive_1x_folds|
|filtered_exit_2025_combo_e10_x5_s50_btc0.675|True|rejected|2|22.737743|14.246045|0.00000,16.81559,-6.57111,10.24333,8.00453,-5.55003|four_positive_1x_folds|
|filtered_exit_2025_combo_e10_x5_s50_btc0.675|True|rejected|3|20.511189|14.884049|0.00000,16.66231,-7.00928,9.89602,7.56039,-6.02272|four_positive_1x_folds|
|filtered_exit_2025_combo_e10_x10_s50_btc0.675|True|rejected|1|20.964166|16.040641|0.00000,16.96915,-5.71438,10.26363,7.53894,-7.49996|four_positive_1x_folds|
|filtered_exit_2025_combo_e10_x10_s50_btc0.675|True|rejected|2|19.287031|16.444816|0.00000,16.81559,-5.95966,9.97692,7.25811,-7.94518|four_positive_1x_folds|
|filtered_exit_2025_combo_e10_x10_s50_btc0.675|True|rejected|3|17.632476|16.848028|0.00000,16.66231,-6.20489,9.68989,6.97815,-8.38750|four_positive_1x_folds|
|filtered_alloc_2025_combo_e10_s50_btc0.675|False|passed|1|45.409480|12.534757|0.00000,16.96915,1.54561,7.72194,15.44036,-1.55393||
|filtered_alloc_2025_combo_e10_s50_btc0.675|False|passed|2|44.434420|12.607750|0.00000,16.81559,1.54563,7.43829,15.43931,-1.82614||
|filtered_alloc_2025_combo_e10_s50_btc0.675|False|passed|3|43.467865|12.800482|0.00000,16.66231,1.54564,7.15943,15.43763,-2.09948||
|filtered_exit_2025_combo_e15_x5_s50_btc0.675|True|rejected|1|19.113958|15.342483|0.00000,16.96915,-7.43406,9.75987,7.64067,-6.88490|four_positive_1x_folds|
|filtered_exit_2025_combo_e15_x5_s50_btc0.675|True|rejected|2|16.957528|15.970420|0.00000,16.81559,-7.86472,9.41433,7.19302,-7.34674|four_positive_1x_folds|
|filtered_exit_2025_combo_e15_x5_s50_btc0.675|True|rejected|3|14.836163|16.594636|0.00000,16.66231,-8.29366,9.06622,6.74908,-7.80776|four_positive_1x_folds|
|filtered_exit_2025_combo_e15_x10_s50_btc0.675|True|rejected|1|15.639508|17.751091|0.00000,16.96915,-7.07278,9.51801,6.79833,-9.04179|four_positive_1x_folds|
|filtered_exit_2025_combo_e15_x10_s50_btc0.675|True|rejected|2|14.042674|18.148328|0.00000,16.81559,-7.31485,9.23329,6.52018,-9.47480|four_positive_1x_folds|
|filtered_exit_2025_combo_e15_x10_s50_btc0.675|True|rejected|3|12.460256|18.543241|0.00000,16.66231,-7.55613,8.94654,6.23826,-9.90598|four_positive_1x_folds|
|filtered_alloc_2025_combo_e15_s50_btc0.675|False|passed|1|44.684319|12.947161|0.00000,16.96915,1.54561,7.08485,15.52939,-1.53805||
|filtered_alloc_2025_combo_e15_s50_btc0.675|False|passed|2|43.715214|13.137682|0.00000,16.81559,1.54563,6.80293,15.52832,-1.80959||
|filtered_alloc_2025_combo_e15_s50_btc0.675|False|passed|3|42.754140|13.329095|0.00000,16.66231,1.54564,6.52539,15.52667,-2.08224||
|filtered_exit_2025_combo_e20_x5_s50_btc0.675|True|rejected|1|24.851016|11.324651|0.00000,16.96915,-4.25084,11.45328,6.90186,-6.43625|four_positive_1x_folds|
|filtered_exit_2025_combo_e20_x5_s50_btc0.675|True|rejected|2|23.118087|11.492263|0.00000,16.81559,-4.51325,11.29666,6.40252,-6.79400|four_positive_1x_folds|
|filtered_exit_2025_combo_e20_x5_s50_btc0.675|True|rejected|3|21.402874|11.758560|0.00000,16.66231,-4.77497,11.13607,5.90581,-7.15202|four_positive_1x_folds|
|filtered_exit_2025_combo_e20_x10_s50_btc0.675|True|rejected|1|19.510511|14.647161|0.00000,16.96915,-4.09710,9.63835,6.39655,-8.67010|four_positive_1x_folds|
|filtered_exit_2025_combo_e20_x10_s50_btc0.675|True|rejected|2|18.164534|14.929233|0.00000,16.81559,-4.25831,9.44816,6.10010,-9.01685|four_positive_1x_folds|
|filtered_exit_2025_combo_e20_x10_s50_btc0.675|True|rejected|3|16.839111|15.211169|0.00000,16.66231,-4.41924,9.26459,5.80408,-9.36304|four_positive_1x_folds|
|filtered_alloc_2025_combo_e20_s50_btc0.675|False|passed|1|43.488967|13.366388|0.00000,16.96915,1.54561,6.44198,15.50989,-1.74517||
|filtered_alloc_2025_combo_e20_s50_btc0.675|False|passed|2|42.528935|13.593046|0.00000,16.81559,1.54563,6.16510,15.50808,-2.01787||
|filtered_alloc_2025_combo_e20_s50_btc0.675|False|passed|3|41.573189|13.818289|0.00000,16.66231,1.54564,5.88520,15.50634,-2.28796||
|filtered_exit_2026_BTC_e10_x5_s50_c1350|True|rejected|1|-0.791502|11.012421|-1.33445,-2.69735,0.00000,0.00000,-3.86686,7.49433|positive_all_costs,four_positive_1x_folds,gross_to_cost1_gte2_5|
|filtered_exit_2026_BTC_e10_x5_s50_c1350|True|rejected|2|-2.596829|11.939017|-1.72212,-3.33234,0.00000,0.00000,-4.11769,6.92952|positive_all_costs,four_positive_1x_folds,gross_to_cost1_gte2_5|
|filtered_exit_2026_BTC_e10_x5_s50_c1350|True|rejected|3|-4.367320|12.916928|-2.10828,-3.96432,0.00000,0.00000,-4.36720,6.37042|positive_all_costs,four_positive_1x_folds,gross_to_cost1_gte2_5|
|filtered_exit_2026_BTC_e10_x10_s50_c1350|True|rejected|1|9.640075|10.563555|4.24935,5.17201,0.00000,0.00000,-4.42082,4.62427|four_positive_1x_folds|
|filtered_exit_2026_BTC_e10_x10_s50_c1350|True|rejected|2|8.496410|10.869663|4.11394,5.03555,0.00000,0.00000,-4.67007,4.07367|four_positive_1x_folds|
|filtered_exit_2026_BTC_e10_x10_s50_c1350|True|rejected|3|7.364320|11.221957|3.97874,4.89909,0.00000,0.00000,-4.92076,3.52804|four_positive_1x_folds|
|filtered_alloc_2026_BTC_e10_s50_c1350|False|rejected|1|10.500154|13.695560|4.24935,4.09370,-3.53948,0.00000,-4.41989,10.44548|four_positive_1x_folds|
|filtered_alloc_2026_BTC_e10_s50_c1350|False|rejected|2|9.639281|14.148980|4.11394,4.09464,-3.66647,0.00000,-4.67040,10.15993|four_positive_1x_folds|
|filtered_alloc_2026_BTC_e10_s50_c1350|False|rejected|3|8.779319|14.599630|3.97874,4.09558,-3.79345,0.00000,-4.92027,9.86943|four_positive_1x_folds|
|filtered_exit_2026_BTC_e15_x5_s50_c1350|True|rejected|1|-0.791502|11.012421|-1.33445,-2.69735,0.00000,0.00000,-3.86686,7.49433|positive_all_costs,four_positive_1x_folds,gross_to_cost1_gte2_5|
|filtered_exit_2026_BTC_e15_x5_s50_c1350|True|rejected|2|-2.596829|11.939017|-1.72212,-3.33234,0.00000,0.00000,-4.11769,6.92952|positive_all_costs,four_positive_1x_folds,gross_to_cost1_gte2_5|
|filtered_exit_2026_BTC_e15_x5_s50_c1350|True|rejected|3|-4.367320|12.916928|-2.10828,-3.96432,0.00000,0.00000,-4.36720,6.37042|positive_all_costs,four_positive_1x_folds,gross_to_cost1_gte2_5|
|filtered_exit_2026_BTC_e15_x10_s50_c1350|True|rejected|1|9.640075|10.563555|4.24935,5.17201,0.00000,0.00000,-4.42082,4.62427|four_positive_1x_folds|
|filtered_exit_2026_BTC_e15_x10_s50_c1350|True|rejected|2|8.496410|10.869663|4.11394,5.03555,0.00000,0.00000,-4.67007,4.07367|four_positive_1x_folds|
|filtered_exit_2026_BTC_e15_x10_s50_c1350|True|rejected|3|7.364320|11.221957|3.97874,4.89909,0.00000,0.00000,-4.92076,3.52804|four_positive_1x_folds|
|filtered_alloc_2026_BTC_e15_s50_c1350|False|rejected|1|10.500154|13.695560|4.24935,4.09370,-3.53948,0.00000,-4.41989,10.44548|four_positive_1x_folds|
|filtered_alloc_2026_BTC_e15_s50_c1350|False|rejected|2|9.639281|14.148980|4.11394,4.09464,-3.66647,0.00000,-4.67040,10.15993|four_positive_1x_folds|
|filtered_alloc_2026_BTC_e15_s50_c1350|False|rejected|3|8.779319|14.599630|3.97874,4.09558,-3.79345,0.00000,-4.92027,9.86943|four_positive_1x_folds|
|filtered_exit_2026_BTC_e20_x5_s50_c1350|True|rejected|1|-0.791502|11.012421|-1.33445,-2.69735,0.00000,0.00000,-3.86686,7.49433|positive_all_costs,four_positive_1x_folds,gross_to_cost1_gte2_5|
|filtered_exit_2026_BTC_e20_x5_s50_c1350|True|rejected|2|-2.596829|11.939017|-1.72212,-3.33234,0.00000,0.00000,-4.11769,6.92952|positive_all_costs,four_positive_1x_folds,gross_to_cost1_gte2_5|
|filtered_exit_2026_BTC_e20_x5_s50_c1350|True|rejected|3|-4.367320|12.916928|-2.10828,-3.96432,0.00000,0.00000,-4.36720,6.37042|positive_all_costs,four_positive_1x_folds,gross_to_cost1_gte2_5|
|filtered_exit_2026_BTC_e20_x10_s50_c1350|True|rejected|1|9.640075|10.563555|4.24935,5.17201,0.00000,0.00000,-4.42082,4.62427|four_positive_1x_folds|
|filtered_exit_2026_BTC_e20_x10_s50_c1350|True|rejected|2|8.496410|10.869663|4.11394,5.03555,0.00000,0.00000,-4.67007,4.07367|four_positive_1x_folds|
|filtered_exit_2026_BTC_e20_x10_s50_c1350|True|rejected|3|7.364320|11.221957|3.97874,4.89909,0.00000,0.00000,-4.92076,3.52804|four_positive_1x_folds|
|filtered_alloc_2026_BTC_e20_s50_c1350|False|rejected|1|10.500154|13.695560|4.24935,4.09370,-3.53948,0.00000,-4.41989,10.44548|four_positive_1x_folds|
|filtered_alloc_2026_BTC_e20_s50_c1350|False|rejected|2|9.639281|14.148980|4.11394,4.09464,-3.66647,0.00000,-4.67040,10.15993|four_positive_1x_folds|
|filtered_alloc_2026_BTC_e20_s50_c1350|False|rejected|3|8.779319|14.599630|3.97874,4.09558,-3.79345,0.00000,-4.92027,9.86943|four_positive_1x_folds|
|filtered_exit_2026_ETH_e10_x5_s50_c650|True|rejected|1|7.494276|18.558869|4.48860,-7.86214,0.00000,1.35144,-7.81199,19.50167|four_positive_1x_folds|
|filtered_exit_2026_ETH_e10_x5_s50_c650|True|rejected|2|5.541361|19.409208|4.35103,-8.22498,0.00000,1.21806,-8.17348,18.57013|four_positive_1x_folds|
|filtered_exit_2026_ETH_e10_x5_s50_c650|True|rejected|3|3.614299|20.249761|4.21421,-8.58437,0.00000,1.08578,-8.53588,17.63362|four_positive_1x_folds|
|filtered_exit_2026_ETH_e10_x10_s50_c650|True|rejected|1|14.143564|16.635992|4.48860,-8.25755,0.00000,1.35110,-3.95340,22.32118|four_positive_1x_folds|
|filtered_exit_2026_ETH_e10_x10_s50_c650|True|rejected|2|12.652882|17.072048|4.35103,-8.61689,0.00000,1.21807,-4.08029,21.67846|four_positive_1x_folds|
|filtered_exit_2026_ETH_e10_x10_s50_c650|True|rejected|3|11.187805|17.504992|4.21421,-8.97474,0.00000,1.08576,-4.20693,21.04427|four_positive_1x_folds|
|filtered_alloc_2026_ETH_e10_s50_c650|False|rejected|1|29.083066|14.053683|4.48860,-5.41559,0.00000,1.35114,-1.93806,31.41705|four_positive_1x_folds|
|filtered_alloc_2026_ETH_e10_s50_c650|False|rejected|2|28.409780|14.279006|4.35103,-5.53921,0.00000,1.21804,-1.93826,31.24787|four_positive_1x_folds|
|filtered_alloc_2026_ETH_e10_s50_c650|False|rejected|3|27.740933|14.502708|4.21421,-5.66229,0.00000,1.08570,-1.93839,31.07779|four_positive_1x_folds|
|filtered_exit_2026_ETH_e15_x5_s50_c650|True|rejected|1|7.494276|18.558869|4.48860,-7.86214,0.00000,1.35144,-7.81199,19.50167|four_positive_1x_folds|
|filtered_exit_2026_ETH_e15_x5_s50_c650|True|rejected|2|5.541361|19.409208|4.35103,-8.22498,0.00000,1.21806,-8.17348,18.57013|four_positive_1x_folds|
|filtered_exit_2026_ETH_e15_x5_s50_c650|True|rejected|3|3.614299|20.249761|4.21421,-8.58437,0.00000,1.08578,-8.53588,17.63362|four_positive_1x_folds|
|filtered_exit_2026_ETH_e15_x10_s50_c650|True|rejected|1|14.143564|16.635992|4.48860,-8.25755,0.00000,1.35110,-3.95340,22.32118|four_positive_1x_folds|
|filtered_exit_2026_ETH_e15_x10_s50_c650|True|rejected|2|12.652882|17.072048|4.35103,-8.61689,0.00000,1.21807,-4.08029,21.67846|four_positive_1x_folds|
|filtered_exit_2026_ETH_e15_x10_s50_c650|True|rejected|3|11.187805|17.504992|4.21421,-8.97474,0.00000,1.08576,-4.20693,21.04427|four_positive_1x_folds|
|filtered_alloc_2026_ETH_e15_s50_c650|False|rejected|1|29.083066|14.053683|4.48860,-5.41559,0.00000,1.35114,-1.93806,31.41705|four_positive_1x_folds|
|filtered_alloc_2026_ETH_e15_s50_c650|False|rejected|2|28.409780|14.279006|4.35103,-5.53921,0.00000,1.21804,-1.93826,31.24787|four_positive_1x_folds|
|filtered_alloc_2026_ETH_e15_s50_c650|False|rejected|3|27.740933|14.502708|4.21421,-5.66229,0.00000,1.08570,-1.93839,31.07779|four_positive_1x_folds|
|filtered_exit_2026_ETH_e20_x5_s50_c650|True|rejected|1|-1.312808|15.466385|4.48860,-3.65961,0.00000,1.35115,-7.81096,4.92416|positive_all_costs,four_positive_1x_folds,gross_to_cost1_gte2_5|
|filtered_exit_2026_ETH_e20_x5_s50_c650|True|rejected|2|-2.604293|16.131883|4.35103,-3.78638,0.00000,1.21814,-8.17492,4.37267|positive_all_costs,four_positive_1x_folds,gross_to_cost1_gte2_5|
|filtered_exit_2026_ETH_e20_x5_s50_c650|True|rejected|3|-3.874372|16.790861|4.21421,-3.91262,0.00000,1.08556,-8.53632,3.82647|positive_all_costs,four_positive_1x_folds,gross_to_cost1_gte2_5|
|filtered_exit_2026_ETH_e20_x10_s50_c650|True|rejected|1|1.416199|12.833619|4.48860,-4.07180,0.00000,1.35145,-3.95493,3.94104|positive_all_costs,four_positive_1x_folds,gross_to_cost1_gte2_5|
|filtered_exit_2026_ETH_e20_x10_s50_c650|True|rejected|2|0.352962|13.061637|4.35103,-4.19771,0.00000,1.21804,-4.08071,3.39360|positive_all_costs,four_positive_1x_folds,gross_to_cost1_gte2_5|
|filtered_exit_2026_ETH_e20_x10_s50_c650|True|rejected|3|-0.695382|13.289682|4.21421,-4.32351,0.00000,1.08577,-4.20749,2.85270|positive_all_costs,four_positive_1x_folds,gross_to_cost1_gte2_5|
|filtered_alloc_2026_ETH_e20_s50_c650|False|rejected|1|29.083066|14.053683|4.48860,-5.41559,0.00000,1.35114,-1.93806,31.41705|four_positive_1x_folds|
|filtered_alloc_2026_ETH_e20_s50_c650|False|rejected|2|28.409780|14.279006|4.35103,-5.53921,0.00000,1.21804,-1.93826,31.24787|four_positive_1x_folds|
|filtered_alloc_2026_ETH_e20_s50_c650|False|rejected|3|27.740933|14.502708|4.21421,-5.66229,0.00000,1.08570,-1.93839,31.07779|four_positive_1x_folds|
|filtered_exit_2026_combo_e10_x5_s50_btc0.675|True|rejected|1|1.901375|13.054561|0.55804,-4.44152,0.00000,0.44005,-5.16311,11.32938|positive_all_costs,four_positive_1x_folds,gross_to_cost1_gte2_5|
|filtered_exit_2026_combo_e10_x5_s50_btc0.675|True|rejected|2|0.048083|13.888754|0.25166,-4.98747,0.00000,0.39802,-5.45379,10.65399|positive_all_costs,four_positive_1x_folds,gross_to_cost1_gte2_5|
|filtered_exit_2026_combo_e10_x5_s50_btc0.675|True|rejected|3|-1.773294|14.714993|-0.05347,-5.52995,0.00000,0.35605,-5.74413,9.98053|positive_all_costs,four_positive_1x_folds,gross_to_cost1_gte2_5|
|filtered_exit_2026_combo_e10_x10_s50_btc0.675|True|passed|1|11.103709|10.023051|4.32711,0.80065,0.00000,0.40027,-4.28103,9.93480||
|filtered_exit_2026_combo_e10_x10_s50_btc0.675|True|passed|2|9.847264|10.258448|4.19100,0.59169,0.00000,0.36019,-4.49418,9.34669||
|filtered_exit_2026_combo_e10_x10_s50_btc0.675|True|passed|3|8.606953|10.496188|4.05527,0.38321,0.00000,0.32047,-4.70846,8.76486||
|filtered_alloc_2026_combo_e10_s50_btc0.675|False|passed|1|16.539601|12.603352|4.32711,0.99839,-2.46053,0.42226,-3.63709,17.17680||
|filtered_alloc_2026_combo_e10_s50_btc0.675|False|passed|2|15.739693|12.911902|4.19100,0.95883,-2.54985,0.38066,-3.80943,16.93453||
|filtered_alloc_2026_combo_e10_s50_btc0.675|False|passed|3|14.941844|13.219117|4.05527,0.91943,-2.63922,0.33930,-3.98145,16.68877||
|filtered_exit_2026_combo_e15_x5_s50_btc0.675|True|rejected|1|1.901375|13.054561|0.55804,-4.44152,0.00000,0.44005,-5.16311,11.32938|positive_all_costs,four_positive_1x_folds,gross_to_cost1_gte2_5|
|filtered_exit_2026_combo_e15_x5_s50_btc0.675|True|rejected|2|0.048083|13.888754|0.25166,-4.98747,0.00000,0.39802,-5.45379,10.65399|positive_all_costs,four_positive_1x_folds,gross_to_cost1_gte2_5|
|filtered_exit_2026_combo_e15_x5_s50_btc0.675|True|rejected|3|-1.773294|14.714993|-0.05347,-5.52995,0.00000,0.35605,-5.74413,9.98053|positive_all_costs,four_positive_1x_folds,gross_to_cost1_gte2_5|
|filtered_exit_2026_combo_e15_x10_s50_btc0.675|True|passed|1|11.103709|10.023051|4.32711,0.80065,0.00000,0.40027,-4.28103,9.93480||
|filtered_exit_2026_combo_e15_x10_s50_btc0.675|True|passed|2|9.847264|10.258448|4.19100,0.59169,0.00000,0.36019,-4.49418,9.34669||
|filtered_exit_2026_combo_e15_x10_s50_btc0.675|True|passed|3|8.606953|10.496188|4.05527,0.38321,0.00000,0.32047,-4.70846,8.76486||
|filtered_alloc_2026_combo_e15_s50_btc0.675|False|passed|1|16.539601|12.603352|4.32711,0.99839,-2.46053,0.42226,-3.63709,17.17680||
|filtered_alloc_2026_combo_e15_s50_btc0.675|False|passed|2|15.739693|12.911902|4.19100,0.95883,-2.54985,0.38066,-3.80943,16.93453||
|filtered_alloc_2026_combo_e15_s50_btc0.675|False|passed|3|14.941844|13.219117|4.05527,0.91943,-2.63922,0.33930,-3.98145,16.68877||
|filtered_exit_2026_combo_e20_x5_s50_btc0.675|True|rejected|1|-0.960927|12.490988|0.55804,-3.02231,0.00000,0.45329,-5.20187,6.64831|positive_all_costs,four_positive_1x_folds,gross_to_cost1_gte2_5|
|filtered_exit_2026_combo_e20_x5_s50_btc0.675|True|rejected|2|-2.599255|13.331833|0.25166,-3.48594,0.00000,0.41080,-5.49693,6.08496|positive_all_costs,four_positive_1x_folds,gross_to_cost1_gte2_5|
|filtered_exit_2026_combo_e20_x5_s50_btc0.675|True|rejected|3|-4.207112|14.164152|-0.05347,-3.94680,0.00000,0.36800,-5.79063,5.52718|positive_all_costs,four_positive_1x_folds,gross_to_cost1_gte2_5|
|filtered_exit_2026_combo_e20_x10_s50_btc0.675|True|passed|1|6.967316|9.653128|4.32711,2.16312,0.00000,0.41306,-4.27709,4.41279||
|filtered_exit_2026_combo_e20_x10_s50_btc0.675|True|passed|2|5.849790|9.970208|4.19100,2.03013,0.00000,0.37227,-4.48842,3.86317||
|filtered_exit_2026_combo_e20_x10_s50_btc0.675|True|passed|3|4.744917|10.289237|4.05527,1.89717,0.00000,0.33184,-4.70113,3.31901||
|filtered_alloc_2026_combo_e20_s50_btc0.675|False|passed|1|16.539601|12.603352|4.32711,0.99839,-2.46053,0.42226,-3.63709,17.17680||
|filtered_alloc_2026_combo_e20_s50_btc0.675|False|passed|2|15.739693|12.911902|4.19100,0.95883,-2.54985,0.38066,-3.80943,16.93453||
|filtered_alloc_2026_combo_e20_s50_btc0.675|False|passed|3|14.941844|13.219117|4.05527,0.91943,-2.63922,0.33930,-3.98145,16.68877||

## 原冻结模拟观察

续接013340原state/report，从Oct5 01:10至03:10UTC，保留4394点完整NAV前缀，仅追加120闭合分钟，累计4509分钟（75小时9分、3完整日），4514点。无新日决策、无新成交，现金/持币/交易/成本全部保持。仍是原SMA65±1%、BTC75%/ETH25%浮点模型，禁止将本轮参数替换进去。下一次日决策Oct6UTC00:01。
|配置|成本|累计净收益%|全期回撤%|
|---|---|---|---|
|forward_snapshot_BTC|1|1.752863|3.655885|
|forward_snapshot_BTC|2|1.619637|3.655885|
|forward_snapshot_BTC|3|1.486696|3.655885|
|forward_snapshot_ETH|1|0.715408|4.176197|
|forward_snapshot_ETH|2|0.583770|4.176197|
|forward_snapshot_ETH|3|0.452413|4.176197|
|forward_snapshot_combo|1|1.493500|3.766197|
|forward_snapshot_combo|2|1.360670|3.766197|
|forward_snapshot_combo|3|1.228125|3.766197|

3个partial快照均rejected仅表示不足180日/六折，不终止长期观察。延迟真实数据模拟，无实盘订单，无实时成交证据，不称稳定盈利。

## 登记、证据和复现

完整读取登记簿2851行、1376规范定义、1378保留ID、34轮历史结论，初始16均已有结果。全部39新定义先reserve，审计通过后finish，负收益永久保留。
本轮历史独立审计全部162场景、42019884逐分钟NAV点、19440因果决策、72未来/当前收盘扰动探针、996成交，其中816新成交。观察审计9场景原账户连续性及HTTP200原始响应/hash/时间轴。
代码、spec、report、压缩逐配置结果、数据哈希、中文结果和必要日志均保存。大行情/NAV缓存留忽略data目录。spec.json/data_manifest.json记录具体SHA及数据范围；report.json/source_hashes绑定代码和原验证文件。
复现命令：`bash research/experiments/20261005T033410Z/reproduce.sh`；无HTTP或登记写入，108新历史+54只读+9观察精确重放。
下轮可预登记EMA退出阈值或中间退出窗口，关注跨年度折一致性，不因本轮排名追认合格。
