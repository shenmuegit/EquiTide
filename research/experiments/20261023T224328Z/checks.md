# 本轮核验与下轮必需状态

6新ETH/18成本场景，3旧30日锚只读；9新ID/18追加事件均真实finish rejected。金融报告 `ed81f2fd4478b8dd6ce4d33642b3f253fc4d026d7f7bdd49bfca024ca4c31ed9`；原SMA报告 `6d94002a9166effc737a49402e71234d2ad0d15bb6b25453953700873a55044a`，原字节与登记一致。

最终实际门禁：

`python3 checks/strategy_registry.py`：实际exit0，stdout/stderr见final_gates.json及对应日志。
`python3 research/monitor/snapshot.py`：实际exit0，stdout/stderr见final_gates.json及对应日志。
`python3 checks/monitor_snapshot.py`：实际exit0，stdout/stderr见final_gates.json及对应日志。
`python3 research/experiments/20261023T224328Z/check_feed.py`：实际exit0，stdout/stderr见final_gates.json及对应日志。
`git diff --check`：实际exit0，stdout/stderr见final_gates.json及对应日志。

监控4230配置/109观察/10账户，受保护输入不变，旧exclusive-end报告别名537f5a8f…保留。

独立审计804笔成交、17820条资金费（含空仓0）、8749674个新完整NAV点、216整体/逐折指标、149631状态—小时保证金边界。最长32日首取C0，33日会负索引，合成和实际整数信号核对无未来尾部引用。

敏感性图已实际打开：30/31/32日9格均3倍净正，31/32较旧30日收益下降；新6项全部因1倍正折不足8/11淘汰。原7父组合资格/报告SHA保持，不计算或外推新父组合。

原SMA31492旧NAV点完整前缀保留，追加120至31612，累计31589分钟；现金/units/desired/交易/费用不变，独立审计和离线重放actualexit0。下次2026-10-24UTC00:01需处理实际日事件，当前mark-onlyhelper不可跨过；保留完整源链与2027-03-31计划。

当前无实际命令/访问失败，原历史失败仍留原位置。无本轮NPY/checkpoint/缓存可清理；必要大JSON及原HTTP字节保留，已finish结果不格式迁移。

发布：同一锁内普通SSH非强推、fresh fetch/独立ls-remote和完整Git树/结果/源/数据SHA核验后释放本轮broker。回执留.git/automation_proofs/20261023T224328Z.json，不删除共享锁文件。
