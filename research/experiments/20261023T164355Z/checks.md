# 本轮真实核验与失败事实

金融报告最终SHA256 `088aad5d26deb60a1b6138b5b3383a6734e2c0d8088ab5d2a4d6fc6c6cb796ba`，原SMA报告 `db208afe31b19747f7bead726970a5a17d867ff14d0995b48b95e2bd905157fb`；21项均已finish rejected且有真实结果，不重写已finish报告。

最终门禁：

`python3 checks/strategy_registry.py`：实际exit0；stdout/stderr见final_gates.json及对应日志。
`python3 research/monitor/snapshot.py`：实际exit0；stdout/stderr见final_gates.json及对应日志。
`python3 checks/monitor_snapshot.py`：实际exit0；stdout/stderr见final_gates.json及对应日志。
`python3 research/experiments/20261023T164355Z/check_feed.py`：实际exit0；stdout/stderr见final_gates.json及对应日志。
`git diff --check`：实际exit0；stdout/stderr见final_gates.json及对应日志。

监控4131配置、106观察、10账户，受保护输入未改；旧exclusive-end报告别名537f5a8f…仍可见。

金融独立审计54成本场景/594逐折、26249022完整NAV点、4116笔成交、53460条结算、405075次状态—小时保证金代理检查；整数信号不调用生产target。原SMA9场景精确离线重放通过，保留31132旧点前缀，追加120点至31252，无新成交/现金重开。

读取失败两次实际exit1（猜测测试文件缺失、初始导入缺新版结果字段的过窄断言）均保留read_failures.json；原始ZIP/WF证据已核验。预期合成红灯实际exit1，随后绿灯实际exit0，单列synthetic_red.json。场景计数模板60→54在finish前修正文案元数据，未改金融结果，未重复计算；保留纠正说明。

敏感性图已实际打开检查：两资产最长20日行正收益，短周期多负收益；预设中心新旧曲线未形成稳定净正。未把混合采样DD当逐tick mark权益。

所有原报告、源状态、冻结计划哈希保持。清理核验发现本轮无可重建磁盘NPY/checkpoint/缓存；18个完整交易/资金费/状态gzip和必要原SMA累计JSON及原始HTTP响应保留。

发布：同一排他锁持有至普通SSH非强推、fresh fetch/独立ls-remote及完整Git树/结果/源数据SHA核验。发布回执保存在.git/automation_proofs/20261023T164355Z.json，核验后仅释放本轮broker，不删除共享锁文件。
