# 本轮实际命令与证据复现

固定目录 `/home/desktop/Documents/Codex/EquiTide`，main，分支排他锁。命令与真实退出码见各 `*_commands.json`、reserve_batches/finish_batches 及 bootstrap/freeze/scope_annotation/decision/grid/collect 回执；不安装依赖。

```bash
cd /home/desktop/Documents/Codex/EquiTide
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
PY=/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python
R=research/experiments/20261101T115248Z
$PY $R/bootstrap.py
$PY $R/freeze.py
$PY $R/commands.py initial
$PY $R/commands.py reserve_batch_0
$PY $R/commands.py reserve_batch_1
$PY $R/commands.py evaluate
$PY $R/annotate_scope.py
$PY $R/commands.py audit
$PY $R/check_decisions.py
$PY $R/commands.py summary
$PY $R/commands.py exports
$PY $R/check_grid_diagnostics.py
$PY $R/commands.py finish_batch_0
$PY $R/commands.py finish_batch_1
$PY $R/commands.py finish
$PY $R/commands.py forward
$PY $R/commands.py candidate
$PY $R/commands.py l4h02
$PY $R/commands.py observer_status
$PY $R/commands.py review
$PY $R/commands.py gates
$PY $R/commands.py feed
$PY $R/collect_evidence.py
$PY $R/finalize.py
$PY $R/publish.py publish
```

这是本轮真实执行顺序；不能在完成目录原地重复金融计算。驱动会拒绝已有结果，保留完整 reserve/finish 记录、报告和账户全账本。所有12项reserve实际成功才计算，36个成本场景含全部负收益；旧3个候选、1个持有父和6个原生定义只读，不重写其资格。

年度数据为 plan.json 中8份真实Parquet，路径/大小/SHA和16份既往必要输入列于data_manifest。四个新BTC路径用真实3125/4375资金、N312.5/437.5、原生LOT/tick、过去20日规模冲击、费用/价差/滑点、真实资金费和独立小时抵押代理；父组合按原始[1,1]相加两份实际银行美元净值。两个资金档与ETH H2/2.5/3的具体变体各自登记；原生component、原生/父持有控制与父候选单独计数。对照为匹配银行及初始N的常多参考，不是满仓或同风险买持。

原始计算报告保存在report_as_executed.json.gz，解压后字节SHA见scope_annotation.json。原执行器带有上一轮execution_scope说明，annotate_scope.py只更正该字段，全部其他字段/规格/规则/门槛/指标/状态/归档完全相等；该更正在独立audit和finish之前完成。已绑定金融代码字节不修改，无回测重跑。后续新轮次可在绑定前让说明来自新冻结计划，避免沿用旧文字；本轮封存代码保持真实执行版本。

独立audit以Fraction重建信号和数量、Decimal重建现金/成本/资金费/抵押，验证全部完整净值及逐月/近期折/整体DD，不调用simulate/decide/trade进行新金融试验。代码与旧数据/组件来源由code_binding_before_evaluation和data_manifest固定，模型无训练/标签，所有信号和成本统计仅使用过去可得数据；重复开发历史不是独立最终测试集。

原SMA65及原singleS28续08:30至10:30；独立未过滤L4/H2续10:10至12:10，必须在12:11参考分钟闭合后开始采集，真实启动/闭合证明见l4h02_reference_closure。三账户现金/q/desired/risk/成本和全部NAV前缀延续，08资金费仅入账一次，不重置账户或替换冻结规则，不拿历史研究当真实报价成交。所有部分观察登记并finish，不取消原180日计划。

保留当前轻量HTTP原始尝试/响应和packet副本、所有spec、归档、状态段/必要逐笔、CSV/图和下一轮必需状态；行情大文件继续留在忽略data，不入Git。核验后仅清理可从基准登记重建的语义元数据清单，原SHA/数量/字节数见cleanup_verification，金融结果和账户账本删除均为0。

快照只读已有研究/账户，同main排他锁内执行registry/snapshot/monitor检查，不产生新回测/成交，不改预算、冻结参数、本金或持仓，不部署网页/创建定时器/下真实订单。实际SSH非强制push main后，重新fetch与独立ls-remote核对完整tree和每个必要blob的字节SHA；见.git/automation_proofs。必须见publisher实际终态exit0后释放锁，再独立检查封存内容/main/账户链/工作区，不预写发布SHA。
