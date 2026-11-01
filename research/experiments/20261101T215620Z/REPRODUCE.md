# 本轮复核与真实执行

固定cwd `/home/desktop/Documents/Codex/EquiTide`，main唯一分支；基准`08459895171cda61e8154e41deb5ceb865bf0812`。先核对git根目录/AGENTS/task，不切换其他工作区，不建分支/工作树，不读取凭据。解释器`/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python`仅作为已有环境，实际运行cwd始终是固定仓库；runtime.json记录版本、Decimal28、单线程，无依赖安装。

完整25314事件/12535ID、268份结论、原freqtrade ZIP/JSON及checks/*oos.py已读；初始16项原始实际证据与SHA在context。8个真实Parquet和16个来源输入SHA/字节/UTC、代码版本与完整账户链见data_manifest，大行情不提交。完整1212条ETH资金费用于过去可得特征，OOS1110条用于实际持仓现金入账。

新配置为L3/4/5×F0/1bp/OFF的6新原生/6新父，OFF三格/来源只读。价量规则固定ETH H2.5%、退出+0.25%、slow28始终门控、V10cap4.5%，后对fresh/flip检查direction×最近可用realized_rate<=F；保留和必须退出不受过滤拦截，信号率不随成本压力放大。只取settlement<=00且available+3600秒<=00的最新结算，年龄<=16h；缺失/过期blocked不补0。normalized available已为settlement+1h，故总保守模型2h延迟，不是官方标准/历史网络到达实测。00刚结算费率不能提前使用；未来实际funding仍按真实q/mark/rate逐次入账，支出1/2/3倍、收入不放大。

旧N6均值/负1%退出/多数慢门/无V10规则有11同规模相关定义，完整差异在prior_funding_config_comparison；不是按family名排除或仅改名重测。BTC3750/N375、ETH15000/N4500，原权重[1,1]原样，两完整银行美元NAV相加，总本金18750；20/80%为初始份额，非每日再平衡。不缩放旧NIV，不跨抵押/转账/NAV复利，过滤不折减实际ETH成本/抵押/未来funding。真实LOT/tick/minnotional、参与率、1x入场抵押及1%闭合小时风险代理按原引擎。

各新配置独立reserve成功才计算，实际命令：

```sh
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261101T215620Z/commands.py evaluate
```

这是已执行记录，不在当前完成ID上重跑；run.py拒绝覆盖report。12定义36成本场景全部finish，金融report原SHA`abf7b1df0bf60bbde27ed6e6b77ead8d0d4a8d8e14f3e6de5916f10c45604a06`。4父passed/8金融定义rejected；其中passed_changed_paths2，passed_OFF_equivalents2，F1bp全部6原生/父与OFF三档完整NAV相同。新参数不代表新独立市场证据，均留档且不改资格。L4/F0不在1倍成本上严格提高收益，L3/F0所有成本收益低于OFF，均未每档同时改善收益与回撤；边界峰值/全局描述性悬崖及历史选择偏差保留。

以下只读从真实行情和保存的必要状态段/逐笔/funding独立重建NAV/时序/账务，不调用simulate/decide/trade，不写账户或登记，不做新策略试验：

```sh
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261101T215620Z/audit.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261101T215620Z/check_decisions.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261101T215620Z/check_grid_diagnostics.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261101T215620Z/check_exports.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261101T215620Z/count_evidence.py
```

可能重写相同核验产物，日常只读封存回执。每phase命令/cwd/开始结束/stdout/stderr/实际exit在*_commands.json及logs。新18原生成本曲线19980funding/852成交、旧18曲线19980funding/618成交另列，父只复用来源操作；新6660资金费特征引用逐一核验过去可得。rule抑制114意图不是拒单，实际order_reject0。只读补充计数最初遇旧schema缺policy_audit，失败/evidence_count_failure和修复后的counts回执保留，金融/完成观察重跑0。

连续370日12完整30日+10尾日，不按折重开；近期40日继承day330/8×5日折。固定无训练/标签，purge0、30预热+3间隔；所有月/变体与全曲线回撤/Sharpe/Calmar、1/2/3倍费用/价差/滑点/成交额相关冲击/funding，以及匹配初始本金/N持有、现金0%均保留。此为反复开发历史，非未触碰最终OOS；无TCA/L2/完整历史保证金阶梯/逐tick清算/容量或稳定实盘盈利证明。

原SMA65/singleS28续Nov1UTC18:30至20:30，独立未过滤L4/H2续20:10至22:10且22:11闭合参考后启动；保持原cash/q/desired/risk/全NAV和规则/本金/终止计划，本窗0daily/fill/funding，不重记16费用。部分rejected继续原180日计划；没有给新候选创建账户/定时器或采用到原账户，延迟shadow不充当十账户真实报价模拟。

```sh
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261101T215620Z/audit_forward.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261101T215620Z/audit_candidate.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261101T215620Z/audit_l4h02.py
```

以后指针前进后本轮末指针assert会按设计失败，不能回退指针或重跑完成窗口；读本轮回执与完整链。下一L4窗口跨2026-11-02UTC00资金费和00:01日决策，必须原规则处理，现readonly窗口审计零daily假设需适配，不改冻结引擎或跳过。SMA当前mark-only脚本cut<next_daily，跨日须原SMA65/1%完整65日上下文（旧1d/1m字典与本轮minute数组都保留）。

同main锁实际执行python3 checks/strategy_registry.py、python3 research/monitor/snapshot.py、python3 checks/monitor_snapshot.py和每旧行字典核对，监控8968研究行/8956旧行原样、10固定报价账户/216既有观察，gzip4054956字节沿用5MB预算。只读聚合，不新成交/改冻结本金持仓，不部署网页/建重复定时任务，未下真实订单。

仅清理可重建语义查重材料，原SHA/字节/复现依据在cleanup_verification；保留全部真实正负结果、完整账户账本、冻结规则和必要输入/HTTP尝试。提交/非强制push/完整远端tree与必要blob及释放锁的真实进程终态见`.git/automation_proofs/20261101T215620Z.json`，不在提交前预写成功。
