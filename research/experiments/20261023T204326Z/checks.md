# 本轮真实核验与留档

81新组合/243场景，18源组件54路径只读恢复匹配原SHA。84新ID/168追加事件各自finish：7历史passed、74策略rejected、3原SMApartialrejected。金融报告SHA `c3faac52df2a2e31770e8562878f3872c7f3f8b5ee4396265bd59e03ff844889`；原SMA报告SHA `f04e2454ae8f8d81a7d332c41209b9e81321f7e0cedecfb80564968fbf0b4919`，原字节保持。

实际最终门禁：

`python3 checks/strategy_registry.py`：实际exit0；stdout/stderr见final_gates.json及对应日志。
`python3 research/monitor/snapshot.py`：实际exit0；stdout/stderr见final_gates.json及对应日志。
`python3 checks/monitor_snapshot.py`：实际exit0；stdout/stderr见final_gates.json及对应日志。
`python3 research/experiments/20261023T204326Z/check_feed.py`：实际exit0；stdout/stderr见final_gates.json及对应日志。
`git diff --check`：实际exit0；stdout/stderr见final_gates.json及对应日志。

监控4224配置/108观察/10账户；受保护输入不变，旧exclusive-end别名537f5a8f…保留。

独立恢复2802笔已存源成交/53460结算（含空仓0），18源完整54路径SHA匹配，不重跑源策略或费用选择。243父路径共118120599点，2916整体/逐折指标实际核验。结构化时间键与生产相对整数键独立对齐，raw1/1=两整份10k合计20k，无归一、交叉保证金救助或重复费用。

两张图已实际打开检查：完整4D81格和预设/事后最高/通过组最高/旧恒多参考连续日NAV。75个3倍净正；7个通过皆在ETH30日上界，原范围选择偏差仍在。最高整体收益点因正折不足rejected，最高通过点1倍8/11正折。passed不等于独立前向/实盘盈利证明。

原SMA保持31372旧点完整前缀，追加120到31492，各成本现金/units/desired/交易/费用连续；独立审计和离线重放actualexit0。下一决策Oct24UTC00:01、原2027-03-31终点保持。没有新前向账户或paper10修改。

当前轮无实际命令/访问失败，read_failures.json只覆盖本轮；先前真实失败保留原轮次。全部已finish报告原字节/SHA优先，必要大JSON不迁移。无本轮NPY/checkpoint/缓存可清理。完整源账本仍在原路径，行情留data。

发布：同一锁内普通SSH非强推、fresh fetch/独立ls-remote、完整Git树及结果/源/数据SHA核验后只释放本轮broker。回执在.git/automation_proofs/20261023T204326Z.json，不删除共享锁文件。
