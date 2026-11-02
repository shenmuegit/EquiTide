# 复核与复现

固定工作目录 `/home/desktop/Documents/Codex/EquiTide`，仅 main。运行时使用 `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python`；此路径仅提供已安装的Python与库，不切换仓库。

本轮每条实际命令的工作目录、起止时间、真实退出码、stdout/stderr见 `all_command_receipts.json`、各阶段 `*_commands.json` 和12项逐条reserve/finish回执。先完成合成红/绿检查和定义冻结，再reserve全部12定义，之后仅执行一次金融计算：

```bash
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261102T015622Z/commands.py evaluate
```

已完成配置禁止重测。该命令的已有报告/登记状态保护不能绕过，不删除报告或改名重跑。复核已有结果使用保存的账本与来源哈希：

```bash
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261102T015622Z/check_strength.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261102T015622Z/audit.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261102T015622Z/check_decisions.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261102T015622Z/forward.py --reproduce
python3 checks/strategy_registry.py
python3 checks/monitor_snapshot.py
```

审核不调用金融simulate/decide/trade，不产生新观察、订单或登记。部分审核会重写自身核验JSON，封存证据应保持原字节；需复核时在受控环境比对，不改原封存轮次。两份永续审核使用本轮共享指针；后续轮次推进后，应读取本轮保存的指针/历史链，不覆盖共享最新指针。

新原生18条成本账本包含370天真实决策、资金费、成交和分段现金/数量，按真实价格轴重建完整NAV并比对原hash；18父路径仅按原始[1,1]相加BTC3750与ETH15000美元NAV，原生成交不另造父成交。11CSV保留全部36场景、逐月/尾折、近期折、每日NAV和两轴完整网格。

8份原生行情/mark/funding/交易约束文件的路径、字节、SHA256见 `plan.json` 与 `data_manifest.json`，大行情位于忽略的data/normalized，未提交。账户完整HTTP/packet与失败尝试在raw_evidence及index保留，SMA包含真实65日与121分钟输入及重叠核对。

原SMA65与singleS28本轮已处理Nov2零点；下一窗口00:30至02:30须02:31参考闭合后运行，SMA可复用原mark-only续接模板并保留本轮刷新65日上下文。L4已续至02:10，下一02:10至04:10须04:11闭合后。均须持有同一排他锁、3个新观察reserve后继续原规则/本金/cash/q/risk，不能重放已完成窗口或注入研究T门槛。
