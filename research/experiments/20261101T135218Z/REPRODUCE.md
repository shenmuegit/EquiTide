# 本轮真实命令与复现证据

固定目录 `/home/desktop/Documents/Codex/EquiTide`，main，持有与paper10共用分支排他锁。不安装依赖，不读取凭据。真实退出码/stdout/stderr见各 `*_commands.json`、reserve_batches/finish_batches、bootstrap/freeze/decision/grid/collect 回执。

```bash
cd /home/desktop/Documents/Codex/EquiTide
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
PY=/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python
R=research/experiments/20261101T135218Z
$PY $R/bootstrap.py
$PY $R/freeze.py
$PY $R/commands.py initial
$PY $R/commands.py reserve_batch_0
$PY $R/commands.py reserve_batch_1
$PY $R/commands.py evaluate
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

这是实际顺序，不能在完成目录原地重跑金融试验。驱动拒绝已有结果，保留全部reserve/finish/报告/账户账本；独立审计不调用策略simulate/decide/trade。12项全部reserve成功后才算，6新原生ETH与6新父组合、36成本场景均保存；旧L4的3原生和3父格点、匹配持有父及其来源共10个唯一旧定义只读，不重写资格。

参数为ETH快周期L3/4/5 × H2/2.5/3%，固定S28、退出缓冲绝对ROC0.0025、V10样本logvol cap0.045，BTC原ROC31/H4/E1不变。新L3/L5参数的原生真实N4500/C15000数量、LOT/tick、冲击、费用、资金费和小时抵押从真实数据计算；父组合复用旧BTC3750/N375及各ETH实际净值。原始[1,1]为两份完整银行，资金占比20%/80%，总18750；无NAV线性缩放、份额重复加权、转账或父再平衡。

仅在绑定前扩展新engine的ETH允许域L3/4/5和H2/2.5/3；独立审计已有通用Fraction政策重建。初始合成检查覆盖L3/L5因果信号、E=0.0025等号退出、V=0.045等号过滤、同向保留/退出和美元净值相加，不使用真实市场收益，实际回测为0。之后所有已绑定金融代码字节不改。execution_scope直接取冻结计划计数，避免继承旧说明。

年度真实数据为plan中8份Parquet，路径/大小/SHA和16份既往必要输入由data_manifest固定，大行情留忽略data。连续370日、12完整月折+10日尾折，近期40日继承day330状态。固定规则无训练/标签，purge0、预热30日/间隔3日，信号/成本统计严格只用已完整过去数据。该历史被反复研究，局部通过不能称最终未触碰测试、全域稳健或稳定实盘盈利。

1/2/3倍成本含费/价差/滑点/成交量相关冲击、真实资金费及借币适用性/抵押代理。匹配持有是旧同银行/同初始N常多控制，非满仓或同风险买持；现金0%另列。11CSV、两张L/H面、全部新归档/必要逐笔/资金费/状态段与完整NAV SHA保留，所有正负期段及失败不隐藏。

原SMA65和原singleS28续10:30至12:30；独立未过滤L4/H2续12:10至14:10，必须14:11参考分钟闭合后才采集，见l4h02_reference_closure真实启动时间。现金/q/desired/risk/成本/所有NAV前缀延续，08资金费不重记，不把本轮L3/L5/缓冲/过滤参数注入原账户。原S28的ETHL3零缓冲不等于新研究带缓冲/过滤的L3。部分rejected只说明180日资格未成熟，保留原终止计划。下一L4窗口14:10至16:10会跨16资金费，须16:11之后按真实纳秒/mark/rate/当时q记账一次并保留前后风险状态。

保留当前全部HTTP尝试、响应/packet副本、完整账户账本与下轮必要状态；核验后只清理可从基准登记重建的语义元数据清单，原SHA/字节数/行数见cleanup_verification，金融结果/账户账本删除0。快照只读已有证据，不产生新回测/成交，不改规则/资金/持仓/预算，不部署网页/新建定时器/下真实订单。

实际SSH非强制push main后重新fetch、独立ls-remote核对完整tree和必要blob逐字节SHA。见.git/automation_proofs；只有publisher实际终态exit0后才释放锁，再单独核对封存内容/工作区/main/原S28和独立L4两条链。不预写发布SHA或成功状态。
