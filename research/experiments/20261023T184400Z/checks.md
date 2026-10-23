# 本轮核验与留档

12新策略/36场景、6旧锚只读/18场景，3原SMA真实partial观察；15新ID/30追加事件全部finish。金融报告SHA `f102fec7ac3042383415e17f955e71bc3ea03040fb195c85600f3e21a52f9015`；原SMA报告 `b2ff9467b05445d5baf59fb1f2d467efe5ad7b58bb5dc31ca34b3dfd18e286d2`，原字节与登记一致。

实际最终门禁：

`python3 checks/strategy_registry.py`：实际exit0，stdout/stderr见final_gates.json及对应日志。
`python3 research/monitor/snapshot.py`：实际exit0，stdout/stderr见final_gates.json及对应日志。
`python3 checks/monitor_snapshot.py`：实际exit0，stdout/stderr见final_gates.json及对应日志。
`python3 research/experiments/20261023T184400Z/check_feed.py`：实际exit0，stdout/stderr见final_gates.json及对应日志。
`git diff --check`：实际exit0，stdout/stderr见final_gates.json及对应日志。

监控4143配置/107观察/10账户；受保护输入未改，旧exclusive-end别名537f5a8f…保留。

独立审计1848笔成交、35640条资金费结算、17499348完整新NAV点、432整体/逐折指标、289743状态—小时保证金代理边界；整数信号不调用生产target。6旧锚只核对源SHA/状态/存储指标，不重算NAV、不改资格。

原SMA保持31252旧点前缀，追加120至31372，各成本现金/数量/desired/交易/费用连续；独立审计与离线精确重放actualexit0。下一决策2026-10-24UTC00:01、原终止2027-03-31不变。

敏感性图已实际打开核验：ETH20/25/30行全9点3倍净正，BTC4/9；ETH最高30日/2%仅7/11正折，按8折原门槛淘汰。旧20日状态不追溯重评；没把同一开发历史称独立测试或稳定实盘盈利。

本轮没有实际命令/访问失败；read_failures.json仅描述本轮。继承文献scope的旧回看字样已在报告中解释，冻结plan/grid/spec和原收益未改。先前失败保留原轮次，不伪装新失败。

清理核验无可重建NPY/checkpoint/缓存。必要新结果、全状态/资金费、原SMA累计JSON及原始HTTP字节保留。6旧锚仅SHA/路径引用，完整原始结果留原位置。

发布协议：同一锁内普通SSH非强推，fresh fetch、独立ls-remote、完整Git树及结果/数据/源SHA核验后仅释放本轮broker。发布回执留.git/automation_proofs/20261023T184400Z.json，不删除共享锁文件。
