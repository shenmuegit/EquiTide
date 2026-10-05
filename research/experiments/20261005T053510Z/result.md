# BTC/ETH策略研究：20261005T053510Z

本轮36个新历史配置、108成本场景；18个旧配置54场景只读。1倍成本正收益36个，3倍成本正收益36个；通过4、淘汰32。新增跨2025/2026同时合格组合0个。

## 冻结规则与验证

事前固定entry10/15/20 × exit15/25/30双轴，EMA50、±1.5%；中心entry15/exit30为旧只读。BTC/ETH原始资金比例67.5%/32.5%，总2000USDT，对应1350/650独立资金账户，无归一化、再平衡、资金转移或恒定敞口。
仅用已完成日收盘；00:01真实分钟开盘执行。收盘低于此前exit日最小收盘或EMA×.985优先退出；高于此前entry日最大收盘且高于EMA×1.015入场，否则维持。EMA从原始首日递推不重置。OOS起点空仓，期末成本平仓。
2025及2026分别Mar18 00:01至Sep14 00:01 UTC，180天6个连续30日折；180日历史、3日gap。无拟合标签，无同次测试集选择参数。这些历史反复使用，是开发数据，不是未触碰最终测试集。
手续费10bp、半价差1bp、滑点2bp、依赖实际成交金额/前20日quoteADV及收益波动的冲击；四层均施加1/2/3倍压力。最大参与率.001，Decimal28、tick/LOT舍入、最低名义金额及参考价格过滤；假定IOC完整成交，无真实盘口/TCA校准。现货仅多头，不涉及资金费与借币。
八门槛：所有成本正收益、1倍至少4/6正收益折、3倍逐分钟全期回撤≤25%、邻域3倍正收益占比≥60%、至少2轮交易、毛参考收益/成本≥2.5、无账户违规、期末平仓。参数敏感性完整3×3及邻接cliff统计；不同配置不等于独立市场证据。

## 筛选结论

新4个通过项为2026年exit25组合entry10/15/20及exit15组合entry20；2025对应项均因正收益折不足淘汰，因此不列为跨年度合格方法。
entry15组合：2025 exit15三倍成本收益12.34838%，分钟回撤21.20713%，前五折累计19.88406%(rejected)；2025 exit25三倍成本收益26.53475%，分钟回撤21.96605%，前五折累计29.39456%(rejected)；2025 exit30三倍成本收益42.75414%，分钟回撤13.32909%，前五折累计45.78983%(passed)；2026 exit15三倍成本收益14.98914%，分钟回撤10.63987%，前五折累计-0.93568%(rejected)；2026 exit25三倍成本收益14.94184%，分钟回撤13.21912%，前五折累计-1.49708%(passed)；2026 exit30三倍成本收益14.94184%，分钟回撤13.21912%，前五折累计-1.49708%(passed)。中间退出窗口仍未提供跨年度合格改进；完整结果及每折收益见下表。
淘汰门槛计数（可重叠）：{'four_positive_1x_folds': 29, 'minute_DD3_lte25pct': 6}。新108场景与旧exit30相同的完整NAV数量见diagnostic.json；2026组合三倍成本有3条不同NAV。

## 全配置、成本与逐折结果

|配置|新测|状态|成本|净收益%|分钟回撤%|六折净收益%|失败门槛|
|---|---|---|---|---|---|---|---|
|filtered_exit_2025_BTC_e10_x15_s50_c1350|True|rejected|1|8.786685|17.989491|0.00000,18.01661,-6.26879,5.94814,-2.73478,-4.56724|four_positive_1x_folds|
|filtered_exit_2025_BTC_e10_x15_s50_c1350|True|rejected|2|7.369987|18.419722|0.00000,17.86232,-6.51527,5.66857,-2.98795,-4.94046|four_positive_1x_folds|
|filtered_exit_2025_BTC_e10_x15_s50_c1350|True|rejected|3|5.978595|18.842550|0.00000,17.70830,-6.75794,5.39162,-3.24004,-5.31145|four_positive_1x_folds|
|filtered_exit_2025_BTC_e10_x25_s50_c1350|True|rejected|1|10.814871|19.284182|0.00000,18.01661,-6.26879,4.48036,0.46963,-4.56641|four_positive_1x_folds|
|filtered_exit_2025_BTC_e10_x25_s50_c1350|True|rejected|2|9.660064|19.548852|0.00000,17.86232,-6.51527,4.21007,0.46985,-4.94228|four_positive_1x_folds|
|filtered_exit_2025_BTC_e10_x25_s50_c1350|True|rejected|3|8.520865|19.965240|0.00000,17.70830,-6.75794,3.93658,0.46970,-5.31291|four_positive_1x_folds|
|filtered_alloc_2025_BTC_e10_s50_c1350|False|passed|1|20.639250|12.130607|0.00000,18.01661,2.04138,4.48170,0.46979,-4.56813||
|filtered_alloc_2025_BTC_e10_s50_c1350|False|passed|2|19.694712|12.184604|0.00000,17.86232,2.04140,4.20644,0.46969,-4.94084||
|filtered_alloc_2025_BTC_e10_s50_c1350|False|passed|3|18.761039|12.415094|0.00000,17.70830,2.04141,3.93794,0.46988,-5.31516||
|filtered_exit_2025_BTC_e15_x15_s50_c1350|True|rejected|1|7.069269|18.719370|0.00000,18.01661,-6.26879,5.00490,-3.41200,-4.56565|four_positive_1x_folds|
|filtered_exit_2025_BTC_e15_x15_s50_c1350|True|rejected|2|5.670489|19.145377|0.00000,17.86232,-6.51527,4.72760,-3.66426,-4.94183|four_positive_1x_folds|
|filtered_exit_2025_BTC_e15_x15_s50_c1350|True|rejected|3|4.306974|19.566028|0.00000,17.70830,-6.75794,4.45904,-3.91536,-5.31212|four_positive_1x_folds|
|filtered_exit_2025_BTC_e15_x25_s50_c1350|True|rejected|1|9.831391|19.844040|0.00000,18.01661,-6.26879,3.55558,0.46989,-4.56895|four_positive_1x_folds|
|filtered_exit_2025_BTC_e15_x25_s50_c1350|True|rejected|2|8.683287|20.264392|0.00000,17.86232,-6.51527,3.28080,0.46976,-4.94124|four_positive_1x_folds|
|filtered_exit_2025_BTC_e15_x25_s50_c1350|True|rejected|3|7.554323|20.676499|0.00000,17.70830,-6.75794,3.00973,0.46958,-5.31175|four_positive_1x_folds|
|filtered_alloc_2025_BTC_e15_s50_c1350|False|passed|1|19.564938|12.738335|0.00000,18.01661,2.04138,3.55079,0.46975,-4.56764||
|filtered_alloc_2025_BTC_e15_s50_c1350|False|passed|2|18.629221|12.965519|0.00000,17.86232,2.04140,3.27806,0.46962,-4.94008||
|filtered_alloc_2025_BTC_e15_s50_c1350|False|passed|3|17.703668|13.194059|0.00000,17.70830,2.04141,3.01149,0.46980,-5.31412||
|filtered_exit_2025_BTC_e20_x15_s50_c1350|True|rejected|1|14.614406|12.698858|0.00000,18.01661,-2.01093,7.92470,-3.41251,-4.92274|four_positive_1x_folds|
|filtered_exit_2025_BTC_e20_x15_s50_c1350|True|rejected|2|13.425202|13.155735|0.00000,17.86232,-2.13911,7.78720,-3.66489,-5.29485|four_positive_1x_folds|
|filtered_exit_2025_BTC_e20_x15_s50_c1350|True|rejected|3|12.243977|13.606451|0.00000,17.70830,-2.26724,7.64440,-3.91534,-5.66555|four_positive_1x_folds|
|filtered_exit_2025_BTC_e20_x25_s50_c1350|True|rejected|1|19.222236|10.919497|0.00000,18.01661,-2.01093,7.92470,0.46967,-4.92187|four_positive_1x_folds|
|filtered_exit_2025_BTC_e20_x25_s50_c1350|True|rejected|2|18.291912|11.152819|0.00000,17.86232,-2.13911,7.78720,0.46986,-5.29609|four_positive_1x_folds|
|filtered_exit_2025_BTC_e20_x25_s50_c1350|True|rejected|3|17.366150|11.384397|0.00000,17.70830,-2.26724,7.64440,0.46973,-5.66585|four_positive_1x_folds|
|filtered_alloc_2025_BTC_e20_s50_c1350|False|passed|1|18.486866|12.130607|0.00000,18.01661,2.04138,2.99887,0.46962,-4.92123||
|filtered_alloc_2025_BTC_e20_s50_c1350|False|passed|2|17.562218|12.130704|0.00000,17.86232,2.04140,2.73279,0.46980,-5.29525||
|filtered_alloc_2025_BTC_e20_s50_c1350|False|passed|3|16.642182|12.130776|0.00000,17.70830,2.04141,2.46207,0.46966,-5.66474||
|filtered_exit_2025_ETH_e10_x15_s50_c650|True|rejected|1|46.803514|25.261255|0.00000,14.79365,-9.67744,14.74507,25.85824,-1.95924|four_positive_1x_folds,minute_DD3_lte25pct|
|filtered_exit_2025_ETH_e10_x15_s50_c650|True|rejected|2|44.897816|25.649791|0.00000,14.64162,-9.91249,14.44686,25.53345,-2.34565|four_positive_1x_folds,minute_DD3_lte25pct|
|filtered_exit_2025_ETH_e10_x15_s50_c650|True|rejected|3|43.009130|26.039827|0.00000,14.48987,-10.14907,14.14679,25.20887,-2.73081|four_positive_1x_folds,minute_DD3_lte25pct|
|filtered_exit_2025_ETH_e10_x25_s50_c650|True|rejected|1|76.932410|25.261255|0.00000,14.79365,-9.67744,14.74507,44.99128,2.56929|minute_DD3_lte25pct|
|filtered_exit_2025_ETH_e10_x25_s50_c650|True|rejected|2|75.551254|25.649791|0.00000,14.64162,-9.91249,14.44686,44.99248,2.43484|minute_DD3_lte25pct|
|filtered_exit_2025_ETH_e10_x25_s50_c650|True|rejected|3|74.172849|26.039827|0.00000,14.48987,-10.14907,14.14679,44.99383,2.30046|minute_DD3_lte25pct|
|filtered_alloc_2025_ETH_e10_s50_c650|False|passed|1|96.855340|19.827489|0.00000,14.79365,0.48705,14.74763,44.99643,2.56949||
|filtered_alloc_2025_ETH_e10_s50_c650|False|passed|2|95.816892|20.036765|0.00000,14.64162,0.48703,14.44592,44.99386,2.43489||
|filtered_alloc_2025_ETH_e10_s50_c650|False|passed|3|94.782041|20.245376|0.00000,14.48987,0.48701,14.14470,44.99065,2.30012||
|filtered_exit_2025_ETH_e15_x15_s50_c650|True|rejected|1|32.487822|28.785392|0.00000,14.79365,-13.93632,14.74831,25.86690,-7.15034|four_positive_1x_folds,minute_DD3_lte25pct|
|filtered_exit_2025_ETH_e15_x15_s50_c650|True|rejected|2|30.764614|29.157785|0.00000,14.64162,-14.16136,14.45130,25.53522,-7.51341|four_positive_1x_folds,minute_DD3_lte25pct|
|filtered_exit_2025_ETH_e15_x15_s50_c650|True|rejected|3|29.049771|29.525949|0.00000,14.48987,-14.38563,14.14635,25.20136,-7.87608|four_positive_1x_folds,minute_DD3_lte25pct|
|filtered_exit_2025_ETH_e15_x25_s50_c650|True|rejected|1|68.600521|28.785392|0.00000,14.79365,-13.93632,14.74831,44.99621,2.56948|minute_DD3_lte25pct|
|filtered_exit_2025_ETH_e15_x25_s50_c650|True|rejected|2|67.289963|29.157785|0.00000,14.64162,-14.16136,14.45130,45.00226,2.43521|minute_DD3_lte25pct|
|filtered_exit_2025_ETH_e15_x25_s50_c650|True|rejected|3|65.955633|29.525949|0.00000,14.48987,-14.38563,14.14635,44.99037,2.30033|minute_DD3_lte25pct|
|filtered_alloc_2025_ETH_e15_s50_c650|False|passed|1|96.855340|19.827489|0.00000,14.79365,0.48705,14.74763,44.99643,2.56949||
|filtered_alloc_2025_ETH_e15_s50_c650|False|passed|2|95.816892|20.036765|0.00000,14.64162,0.48703,14.44592,44.99386,2.43489||
|filtered_alloc_2025_ETH_e15_s50_c650|False|passed|3|94.782041|20.245376|0.00000,14.48987,0.48701,14.14470,44.99065,2.30012||
|filtered_exit_2025_ETH_e20_x15_s50_c650|True|rejected|1|33.113404|29.307614|0.00000,14.79365,-13.93632,13.90931,25.86689,-6.02480|four_positive_1x_folds,minute_DD3_lte25pct|
|filtered_exit_2025_ETH_e20_x15_s50_c650|True|rejected|2|31.711588|29.675812|0.00000,14.64162,-14.16136,13.60492,25.53231,-6.14742|four_positive_1x_folds,minute_DD3_lte25pct|
|filtered_exit_2025_ETH_e20_x15_s50_c650|True|rejected|3|30.341150|30.042560|0.00000,14.48987,-14.38563,13.30967,25.20733,-6.27163|four_positive_1x_folds,minute_DD3_lte25pct|
|filtered_exit_2025_ETH_e20_x25_s50_c650|True|rejected|1|67.372235|29.307614|0.00000,14.79365,-13.93632,13.90931,44.99986,2.56963|minute_DD3_lte25pct|
|filtered_exit_2025_ETH_e20_x25_s50_c650|True|rejected|2|66.035871|29.675812|0.00000,14.64162,-14.16136,13.60492,44.98819,2.43468|minute_DD3_lte25pct|
|filtered_exit_2025_ETH_e20_x25_s50_c650|True|rejected|3|64.739320|30.042560|0.00000,14.48987,-14.38563,13.30967,44.99048,2.30034|minute_DD3_lte25pct|
|filtered_alloc_2025_ETH_e20_s50_c650|False|passed|1|95.416408|20.415190|0.00000,14.79365,0.48705,13.90755,44.99802,2.56956||
|filtered_alloc_2025_ETH_e20_s50_c650|False|passed|2|94.382885|20.622909|0.00000,14.64162,0.48703,13.60737,44.99440,2.43491||
|filtered_alloc_2025_ETH_e20_s50_c650|False|passed|3|93.352973|20.829950|0.00000,14.48987,0.48701,13.30770,44.99011,2.30010||
|filtered_exit_2025_combo_e10_x15_s50_btc0.675|True|rejected|1|21.142155|18.753986|0.00000,16.96915,-7.35600,8.68366,6.65247,-3.55683|four_positive_1x_folds|
|filtered_exit_2025_combo_e10_x15_s50_btc0.675|True|rejected|2|19.566531|19.146140|0.00000,16.81559,-7.59882,8.39831,6.37611,-3.93512|four_positive_1x_folds|
|filtered_exit_2025_combo_e10_x15_s50_btc0.675|True|rejected|3|18.013519|19.534066|0.00000,16.66231,-7.83954,8.11408,6.09992,-4.31162|four_positive_1x_folds|
|filtered_exit_2025_combo_e10_x25_s50_btc0.675|True|rejected|1|32.303071|19.638795|0.00000,16.96915,-7.35600,7.67230,15.22364,-1.59080|four_positive_1x_folds|
|filtered_exit_2025_combo_e10_x25_s50_btc0.675|True|rejected|2|31.074701|19.917808|0.00000,16.81559,-7.59882,7.39335,15.22417,-1.86599|four_positive_1x_folds|
|filtered_exit_2025_combo_e10_x25_s50_btc0.675|True|rejected|3|29.857760|20.301337|0.00000,16.66231,-7.83954,7.11150,15.22408,-2.13817|four_positive_1x_folds|
|filtered_alloc_2025_combo_e10_s50_btc0.675|False|passed|1|45.409480|12.534757|0.00000,16.96915,1.54561,7.72194,15.44036,-1.55393||
|filtered_alloc_2025_combo_e10_s50_btc0.675|False|passed|2|44.434420|12.607750|0.00000,16.81559,1.54563,7.43829,15.43931,-1.82614||
|filtered_alloc_2025_combo_e10_s50_btc0.675|False|passed|3|43.467865|12.800482|0.00000,16.66231,1.54564,7.15943,15.43763,-2.09948||
|filtered_exit_2025_combo_e15_x15_s50_btc0.675|True|rejected|1|15.330298|20.440861|0.00000,16.96915,-8.71439,7.93484,5.94824,-5.54730|four_positive_1x_folds|
|filtered_exit_2025_combo_e15_x15_s50_btc0.675|True|rejected|2|13.826080|20.826086|0.00000,16.81559,-8.95400,7.65161,5.67091,-5.91852|four_positive_1x_folds|
|filtered_exit_2025_combo_e15_x15_s50_btc0.675|True|rejected|3|12.348383|21.207125|0.00000,16.66231,-9.19078,7.37204,5.39250,-6.28580|four_positive_1x_folds|
|filtered_exit_2025_combo_e15_x25_s50_btc0.675|True|rejected|1|28.931358|21.209476|0.00000,16.96915,-8.71439,6.92134,14.83954,-1.66026|four_positive_1x_folds|
|filtered_exit_2025_combo_e15_x25_s50_btc0.675|True|rejected|2|27.730457|21.590841|0.00000,16.81559,-8.95400,6.63987,14.84202,-1.93538|four_positive_1x_folds|
|filtered_exit_2025_combo_e15_x25_s50_btc0.675|True|rejected|3|26.534749|21.966046|0.00000,16.66231,-9.19078,6.35854,14.83734,-2.21015|four_positive_1x_folds|
|filtered_alloc_2025_combo_e15_s50_btc0.675|False|passed|1|44.684319|12.947161|0.00000,16.96915,1.54561,7.08485,15.52939,-1.53805||
|filtered_alloc_2025_combo_e15_s50_btc0.675|False|passed|2|43.715214|13.137682|0.00000,16.81559,1.54563,6.80293,15.52832,-1.80959||
|filtered_alloc_2025_combo_e15_s50_btc0.675|False|passed|3|42.754140|13.329095|0.00000,16.66231,1.54564,6.52539,15.52667,-2.08224||
|filtered_exit_2025_combo_e20_x15_s50_btc0.675|True|rejected|1|20.626580|16.214030|0.00000,16.96915,-5.81459,9.66893,5.45096,-5.32094|four_positive_1x_folds|
|filtered_exit_2025_combo_e20_x15_s50_btc0.675|True|rejected|2|19.368278|16.492705|0.00000,16.81559,-5.97363,9.48119,5.15690,-5.60236|four_positive_1x_folds|
|filtered_exit_2025_combo_e20_x15_s50_btc0.675|True|rejected|3|18.125558|16.769725|0.00000,16.66231,-6.13238,9.29245,4.86798,-5.88379|four_positive_1x_folds|
|filtered_exit_2025_combo_e20_x25_s50_btc0.675|True|rejected|1|34.870986|16.214030|0.00000,16.96915,-5.81459,9.66893,13.94988,-2.03609|four_positive_1x_folds|
|filtered_exit_2025_combo_e20_x25_s50_btc0.675|True|rejected|2|33.808699|16.492705|0.00000,16.81559,-5.97363,9.48119,13.92086,-2.32327|four_positive_1x_folds|
|filtered_exit_2025_combo_e20_x25_s50_btc0.675|True|rejected|3|32.762430|16.769725|0.00000,16.66231,-6.13238,9.29245,13.89707,-2.60737|four_positive_1x_folds|
|filtered_alloc_2025_combo_e20_s50_btc0.675|False|passed|1|43.488967|13.366388|0.00000,16.96915,1.54561,6.44198,15.50989,-1.74517||
|filtered_alloc_2025_combo_e20_s50_btc0.675|False|passed|2|42.528935|13.593046|0.00000,16.81559,1.54563,6.16510,15.50808,-2.01787||
|filtered_alloc_2025_combo_e20_s50_btc0.675|False|passed|3|41.573189|13.818289|0.00000,16.66231,1.54564,5.88520,15.50634,-2.28796||
|filtered_exit_2026_BTC_e10_x15_s50_c1350|True|rejected|1|14.126087|10.646050|4.24935,4.09370,-0.13075,0.00000,-4.42009,10.17643|four_positive_1x_folds|
|filtered_exit_2026_BTC_e10_x15_s50_c1350|True|rejected|2|13.233947|11.115221|4.11394,4.09464,-0.26148,0.00000,-4.67124,9.88856|four_positive_1x_folds|
|filtered_exit_2026_BTC_e10_x15_s50_c1350|True|rejected|3|12.350589|11.579863|3.97874,4.09558,-0.39220,0.00000,-4.91951,9.60080|four_positive_1x_folds|
|filtered_exit_2026_BTC_e10_x25_s50_c1350|True|rejected|1|10.500154|13.695560|4.24935,4.09370,-3.53948,0.00000,-4.41989,10.44548|four_positive_1x_folds|
|filtered_exit_2026_BTC_e10_x25_s50_c1350|True|rejected|2|9.639281|14.148980|4.11394,4.09464,-3.66647,0.00000,-4.67040,10.15993|four_positive_1x_folds|
|filtered_exit_2026_BTC_e10_x25_s50_c1350|True|rejected|3|8.779319|14.599630|3.97874,4.09558,-3.79345,0.00000,-4.92027,9.86943|four_positive_1x_folds|
|filtered_alloc_2026_BTC_e10_s50_c1350|False|rejected|1|10.500154|13.695560|4.24935,4.09370,-3.53948,0.00000,-4.41989,10.44548|four_positive_1x_folds|
|filtered_alloc_2026_BTC_e10_s50_c1350|False|rejected|2|9.639281|14.148980|4.11394,4.09464,-3.66647,0.00000,-4.67040,10.15993|four_positive_1x_folds|
|filtered_alloc_2026_BTC_e10_s50_c1350|False|rejected|3|8.779319|14.599630|3.97874,4.09558,-3.79345,0.00000,-4.92027,9.86943|four_positive_1x_folds|
|filtered_exit_2026_BTC_e15_x15_s50_c1350|True|rejected|1|14.126087|10.646050|4.24935,4.09370,-0.13075,0.00000,-4.42009,10.17643|four_positive_1x_folds|
|filtered_exit_2026_BTC_e15_x15_s50_c1350|True|rejected|2|13.233947|11.115221|4.11394,4.09464,-0.26148,0.00000,-4.67124,9.88856|four_positive_1x_folds|
|filtered_exit_2026_BTC_e15_x15_s50_c1350|True|rejected|3|12.350589|11.579863|3.97874,4.09558,-0.39220,0.00000,-4.91951,9.60080|four_positive_1x_folds|
|filtered_exit_2026_BTC_e15_x25_s50_c1350|True|rejected|1|10.500154|13.695560|4.24935,4.09370,-3.53948,0.00000,-4.41989,10.44548|four_positive_1x_folds|
|filtered_exit_2026_BTC_e15_x25_s50_c1350|True|rejected|2|9.639281|14.148980|4.11394,4.09464,-3.66647,0.00000,-4.67040,10.15993|four_positive_1x_folds|
|filtered_exit_2026_BTC_e15_x25_s50_c1350|True|rejected|3|8.779319|14.599630|3.97874,4.09558,-3.79345,0.00000,-4.92027,9.86943|four_positive_1x_folds|
|filtered_alloc_2026_BTC_e15_s50_c1350|False|rejected|1|10.500154|13.695560|4.24935,4.09370,-3.53948,0.00000,-4.41989,10.44548|four_positive_1x_folds|
|filtered_alloc_2026_BTC_e15_s50_c1350|False|rejected|2|9.639281|14.148980|4.11394,4.09464,-3.66647,0.00000,-4.67040,10.15993|four_positive_1x_folds|
|filtered_alloc_2026_BTC_e15_s50_c1350|False|rejected|3|8.779319|14.599630|3.97874,4.09558,-3.79345,0.00000,-4.92027,9.86943|four_positive_1x_folds|
|filtered_exit_2026_BTC_e20_x15_s50_c1350|True|rejected|1|14.126087|10.646050|4.24935,4.09370,-0.13075,0.00000,-4.42009,10.17643|four_positive_1x_folds|
|filtered_exit_2026_BTC_e20_x15_s50_c1350|True|rejected|2|13.233947|11.115221|4.11394,4.09464,-0.26148,0.00000,-4.67124,9.88856|four_positive_1x_folds|
|filtered_exit_2026_BTC_e20_x15_s50_c1350|True|rejected|3|12.350589|11.579863|3.97874,4.09558,-0.39220,0.00000,-4.91951,9.60080|four_positive_1x_folds|
|filtered_exit_2026_BTC_e20_x25_s50_c1350|True|rejected|1|10.500154|13.695560|4.24935,4.09370,-3.53948,0.00000,-4.41989,10.44548|four_positive_1x_folds|
|filtered_exit_2026_BTC_e20_x25_s50_c1350|True|rejected|2|9.639281|14.148980|4.11394,4.09464,-3.66647,0.00000,-4.67040,10.15993|four_positive_1x_folds|
|filtered_exit_2026_BTC_e20_x25_s50_c1350|True|rejected|3|8.779319|14.599630|3.97874,4.09558,-3.79345,0.00000,-4.92027,9.86943|four_positive_1x_folds|
|filtered_alloc_2026_BTC_e20_s50_c1350|False|rejected|1|10.500154|13.695560|4.24935,4.09370,-3.53948,0.00000,-4.41989,10.44548|four_positive_1x_folds|
|filtered_alloc_2026_BTC_e20_s50_c1350|False|rejected|2|9.639281|14.148980|4.11394,4.09464,-3.66647,0.00000,-4.67040,10.15993|four_positive_1x_folds|
|filtered_alloc_2026_BTC_e20_s50_c1350|False|rejected|3|8.779319|14.599630|3.97874,4.09558,-3.79345,0.00000,-4.92027,9.86943|four_positive_1x_folds|
|filtered_exit_2026_ETH_e10_x15_s50_c650|True|rejected|1|22.379793|18.518239|4.48860,-10.32860,0.00000,1.35122,-1.93818,31.41893|four_positive_1x_folds|
|filtered_exit_2026_ETH_e10_x15_s50_c650|True|rejected|2|21.421495|18.943075|4.35103,-10.67949,0.00000,1.21852,-1.93817,31.24648|four_positive_1x_folds|
|filtered_exit_2026_ETH_e10_x15_s50_c650|True|rejected|3|20.469210|19.366072|4.21421,-11.02926,0.00000,1.08552,-1.93809,31.07280|four_positive_1x_folds|
|filtered_exit_2026_ETH_e10_x25_s50_c650|True|rejected|1|29.083066|14.053683|4.48860,-5.41559,0.00000,1.35114,-1.93806,31.41705|four_positive_1x_folds|
|filtered_exit_2026_ETH_e10_x25_s50_c650|True|rejected|2|28.409780|14.279006|4.35103,-5.53921,0.00000,1.21804,-1.93826,31.24787|four_positive_1x_folds|
|filtered_exit_2026_ETH_e10_x25_s50_c650|True|rejected|3|27.740933|14.502708|4.21421,-5.66229,0.00000,1.08570,-1.93839,31.07779|four_positive_1x_folds|
|filtered_alloc_2026_ETH_e10_s50_c650|False|rejected|1|29.083066|14.053683|4.48860,-5.41559,0.00000,1.35114,-1.93806,31.41705|four_positive_1x_folds|
|filtered_alloc_2026_ETH_e10_s50_c650|False|rejected|2|28.409780|14.279006|4.35103,-5.53921,0.00000,1.21804,-1.93826,31.24787|four_positive_1x_folds|
|filtered_alloc_2026_ETH_e10_s50_c650|False|rejected|3|27.740933|14.502708|4.21421,-5.66229,0.00000,1.08570,-1.93839,31.07779|four_positive_1x_folds|
|filtered_exit_2026_ETH_e15_x15_s50_c650|True|rejected|1|22.379793|18.518239|4.48860,-10.32860,0.00000,1.35122,-1.93818,31.41893|four_positive_1x_folds|
|filtered_exit_2026_ETH_e15_x15_s50_c650|True|rejected|2|21.421495|18.943075|4.35103,-10.67949,0.00000,1.21852,-1.93817,31.24648|four_positive_1x_folds|
|filtered_exit_2026_ETH_e15_x15_s50_c650|True|rejected|3|20.469210|19.366072|4.21421,-11.02926,0.00000,1.08552,-1.93809,31.07280|four_positive_1x_folds|
|filtered_exit_2026_ETH_e15_x25_s50_c650|True|rejected|1|29.083066|14.053683|4.48860,-5.41559,0.00000,1.35114,-1.93806,31.41705|four_positive_1x_folds|
|filtered_exit_2026_ETH_e15_x25_s50_c650|True|rejected|2|28.409780|14.279006|4.35103,-5.53921,0.00000,1.21804,-1.93826,31.24787|four_positive_1x_folds|
|filtered_exit_2026_ETH_e15_x25_s50_c650|True|rejected|3|27.740933|14.502708|4.21421,-5.66229,0.00000,1.08570,-1.93839,31.07779|four_positive_1x_folds|
|filtered_alloc_2026_ETH_e15_s50_c650|False|rejected|1|29.083066|14.053683|4.48860,-5.41559,0.00000,1.35114,-1.93806,31.41705|four_positive_1x_folds|
|filtered_alloc_2026_ETH_e15_s50_c650|False|rejected|2|28.409780|14.279006|4.35103,-5.53921,0.00000,1.21804,-1.93826,31.24787|four_positive_1x_folds|
|filtered_alloc_2026_ETH_e15_s50_c650|False|rejected|3|27.740933|14.502708|4.21421,-5.66229,0.00000,1.08570,-1.93839,31.07779|four_positive_1x_folds|
|filtered_exit_2026_ETH_e20_x15_s50_c650|True|rejected|1|30.924202|12.833619|4.48860,-4.07180,0.00000,1.35145,-1.93851,31.42448|four_positive_1x_folds|
|filtered_exit_2026_ETH_e20_x15_s50_c650|True|rejected|2|30.233528|13.061637|4.35103,-4.19771,0.00000,1.21804,-1.93826,31.24799|four_positive_1x_folds|
|filtered_exit_2026_ETH_e20_x15_s50_c650|True|rejected|3|29.555786|13.289682|4.21421,-4.32351,0.00000,1.08577,-1.93852,31.07992|four_positive_1x_folds|
|filtered_exit_2026_ETH_e20_x25_s50_c650|True|rejected|1|29.083066|14.053683|4.48860,-5.41559,0.00000,1.35114,-1.93806,31.41705|four_positive_1x_folds|
|filtered_exit_2026_ETH_e20_x25_s50_c650|True|rejected|2|28.409780|14.279006|4.35103,-5.53921,0.00000,1.21804,-1.93826,31.24787|four_positive_1x_folds|
|filtered_exit_2026_ETH_e20_x25_s50_c650|True|rejected|3|27.740933|14.502708|4.21421,-5.66229,0.00000,1.08570,-1.93839,31.07779|four_positive_1x_folds|
|filtered_alloc_2026_ETH_e20_s50_c650|False|rejected|1|29.083066|14.053683|4.48860,-5.41559,0.00000,1.35114,-1.93806,31.41705|four_positive_1x_folds|
|filtered_alloc_2026_ETH_e20_s50_c650|False|rejected|2|28.409780|14.279006|4.35103,-5.53921,0.00000,1.21804,-1.93826,31.24787|four_positive_1x_folds|
|filtered_alloc_2026_ETH_e20_s50_c650|False|rejected|3|27.740933|14.502708|4.21421,-5.66229,0.00000,1.08570,-1.93839,31.07779|four_positive_1x_folds|
|filtered_exit_2026_combo_e10_x15_s50_btc0.675|True|rejected|1|16.808542|9.933721|4.32711,-0.60081,-0.09235,0.39715,-3.68368,16.59356|four_positive_1x_folds|
|filtered_exit_2026_combo_e10_x15_s50_btc0.675|True|rejected|2|15.894900|10.288110|4.19100,-0.71432,-0.18491,0.35748,-3.86255,16.33463|four_positive_1x_folds|
|filtered_exit_2026_combo_e10_x15_s50_btc0.675|True|rejected|3|14.989141|10.639865|4.05527,-0.82750,-0.27767,0.31787,-4.03979,16.07524|four_positive_1x_folds|
|filtered_exit_2026_combo_e10_x25_s50_btc0.675|True|passed|1|16.539601|12.603352|4.32711,0.99839,-2.46053,0.42226,-3.63709,17.17680||
|filtered_exit_2026_combo_e10_x25_s50_btc0.675|True|passed|2|15.739693|12.911902|4.19100,0.95883,-2.54985,0.38066,-3.80943,16.93453||
|filtered_exit_2026_combo_e10_x25_s50_btc0.675|True|passed|3|14.941844|13.219117|4.05527,0.91943,-2.63922,0.33930,-3.98145,16.68877||
|filtered_alloc_2026_combo_e10_s50_btc0.675|False|passed|1|16.539601|12.603352|4.32711,0.99839,-2.46053,0.42226,-3.63709,17.17680||
|filtered_alloc_2026_combo_e10_s50_btc0.675|False|passed|2|15.739693|12.911902|4.19100,0.95883,-2.54985,0.38066,-3.80943,16.93453||
|filtered_alloc_2026_combo_e10_s50_btc0.675|False|passed|3|14.941844|13.219117|4.05527,0.91943,-2.63922,0.33930,-3.98145,16.68877||
|filtered_exit_2026_combo_e15_x15_s50_btc0.675|True|rejected|1|16.808542|9.933721|4.32711,-0.60081,-0.09235,0.39715,-3.68368,16.59356|four_positive_1x_folds|
|filtered_exit_2026_combo_e15_x15_s50_btc0.675|True|rejected|2|15.894900|10.288110|4.19100,-0.71432,-0.18491,0.35748,-3.86255,16.33463|four_positive_1x_folds|
|filtered_exit_2026_combo_e15_x15_s50_btc0.675|True|rejected|3|14.989141|10.639865|4.05527,-0.82750,-0.27767,0.31787,-4.03979,16.07524|four_positive_1x_folds|
|filtered_exit_2026_combo_e15_x25_s50_btc0.675|True|passed|1|16.539601|12.603352|4.32711,0.99839,-2.46053,0.42226,-3.63709,17.17680||
|filtered_exit_2026_combo_e15_x25_s50_btc0.675|True|passed|2|15.739693|12.911902|4.19100,0.95883,-2.54985,0.38066,-3.80943,16.93453||
|filtered_exit_2026_combo_e15_x25_s50_btc0.675|True|passed|3|14.941844|13.219117|4.05527,0.91943,-2.63922,0.33930,-3.98145,16.68877||
|filtered_alloc_2026_combo_e15_s50_btc0.675|False|passed|1|16.539601|12.603352|4.32711,0.99839,-2.46053,0.42226,-3.63709,17.17680||
|filtered_alloc_2026_combo_e15_s50_btc0.675|False|passed|2|15.739693|12.911902|4.19100,0.95883,-2.54985,0.38066,-3.80943,16.93453||
|filtered_alloc_2026_combo_e15_s50_btc0.675|False|passed|3|14.941844|13.219117|4.05527,0.91943,-2.63922,0.33930,-3.98145,16.68877||
|filtered_exit_2026_combo_e20_x15_s50_btc0.675|True|passed|1|19.585475|8.077203|4.32711,1.43580,-0.09050,0.41639,-3.64837,16.90135||
|filtered_exit_2026_combo_e20_x15_s50_btc0.675|True|passed|2|18.758810|8.366667|4.19100,1.39549,-0.18106,0.37528,-3.82213,16.65468||
|filtered_exit_2026_combo_e20_x15_s50_btc0.675|True|passed|3|17.942278|8.653965|4.05527,1.35520,-0.27170,0.33452,-3.99420,16.41075||
|filtered_exit_2026_combo_e20_x25_s50_btc0.675|True|passed|1|16.539601|12.603352|4.32711,0.99839,-2.46053,0.42226,-3.63709,17.17680||
|filtered_exit_2026_combo_e20_x25_s50_btc0.675|True|passed|2|15.739693|12.911902|4.19100,0.95883,-2.54985,0.38066,-3.80943,16.93453||
|filtered_exit_2026_combo_e20_x25_s50_btc0.675|True|passed|3|14.941844|13.219117|4.05527,0.91943,-2.63922,0.33930,-3.98145,16.68877||
|filtered_alloc_2026_combo_e20_s50_btc0.675|False|passed|1|16.539601|12.603352|4.32711,0.99839,-2.46053,0.42226,-3.63709,17.17680||
|filtered_alloc_2026_combo_e20_s50_btc0.675|False|passed|2|15.739693|12.911902|4.19100,0.95883,-2.54985,0.38066,-3.80943,16.93453||
|filtered_alloc_2026_combo_e20_s50_btc0.675|False|passed|3|14.941844|13.219117|4.05527,0.91943,-2.63922,0.33930,-3.98145,16.68877||

## 原冻结模拟观察

续接033410原state/report，从Oct5 03:10至05:10UTC，保留4514点完整NAV前缀，仅追加120闭合分钟，累计4629分钟（77小时9分、3完整日），4634点。无新日决策、无新成交，现金/持币/交易/成本全部保持。仍是原SMA65±1%、BTC75%/ETH25%浮点模型，禁止将本轮参数替换进去。下一次日决策Oct6UTC00:01。
|配置|成本|累计净收益%|全期回撤%|
|---|---|---|---|
|forward_snapshot_BTC|1|0.758908|3.655885|
|forward_snapshot_BTC|2|0.626983|3.655885|
|forward_snapshot_BTC|3|0.495341|3.655885|
|forward_snapshot_ETH|1|-0.226437|4.176197|
|forward_snapshot_ETH|2|-0.356844|4.176197|
|forward_snapshot_ETH|3|-0.486973|4.176197|
|forward_snapshot_combo|1|0.512572|3.766197|
|forward_snapshot_combo|2|0.381026|3.766197|
|forward_snapshot_combo|3|0.249762|3.766197|

3个partial快照均rejected仅表示不足180日/六折，不终止长期观察。延迟真实数据模拟，无实盘订单，无实时成交证据，不称稳定盈利。

## 登记、证据和复现

完整读取登记簿2929行、1415规范定义、1417保留ID、35轮历史结论，初始16均已有结果。全部39新定义先reserve，审计通过后finish，负收益永久保留。
本轮历史独立审计全部162场景、42019884逐分钟NAV点、19440因果决策、72未来/当前收盘扰动探针、660成交，其中480新成交。观察审计9场景原账户连续性及HTTP200原始响应/hash/时间轴。
代码、spec、report、压缩逐配置结果、数据哈希、中文结果和必要日志均保存。大行情/NAV缓存留忽略data目录。spec.json/data_manifest.json记录具体SHA及数据范围；report.json/source_hashes绑定代码和原验证文件。
复现命令：`bash research/experiments/20261005T053510Z/reproduce.sh`；无HTTP或登记写入，108新历史+54只读+9观察精确重放。
下轮可预登记EMA退出阈值或新策略方向，关注跨年度折一致性，不因本轮排名追认合格。
