# 复核与复现

固定工作目录 `/home/desktop/Documents/Codex/EquiTide`，仅main；运行时 `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python` 只提供Python/依赖，不切换仓库。

实际命令、cwd、起止时间、退出码、stdout/stderr见 `all_command_receipts.json`、各阶段 `*_commands.json` 及12项逐条reserve/finish回执。先合成TDD红/绿及完整spec冻结，全部12定义reserve后，金融计算只执行一次：

```bash
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261102T035722Z/commands.py evaluate
```

已有报告/完成登记禁止重测，不删除报告、改名或绕过状态检查。只读核算复核命令如下：

```bash
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261102T035722Z/check_holding.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261102T035722Z/audit.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261102T035722Z/check_decisions.py
PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261102T035722Z/forward.py --reproduce
python3 checks/strategy_registry.py
python3 checks/monitor_snapshot.py
```

审核不调用金融simulate/decide/trade、不产生新订单/观察/登记；部分检查会重写自身核验JSON，封存证据应保留原字节，需复核时在受控环境比对。两份永续审核绑定本轮共享指针，后续推进后应使用本轮保存的指针与完整历史链，不覆盖共享最新指针。

新18原生成本账本保存370天真实决策、成功成交、持仓日龄、到期标记、资金费和分段现金/数量。审核以成功开仓成交时间戳及当前决策时间戳独立推导日龄，验证72/168小时边界、跨折保留和当次平仓不重开，再重建完整分钟/事件NAV并核对hash。父18路径按原[1,1]相加BTC3750与ETH15000的真实美元NAV，不另造父成交。所有D7成本净值与匹配OFF原结果相同，别名不算独立alpha，已保留原登记与结果。

8份原生行情/mark/funding/约束文件路径、字节与SHA256见plan和data_manifest，大行情保留于忽略的data/normalized，不提交。完整账户HTTP/packet与失败尝试在raw_evidence及index保留；SMA本轮minute数组与上一实际65日上下文分开，完整daily来源20261102T015622Z/forward_inputs.json.gz。

下一SMA/singleS28窗口02:30至04:30须04:31参考闭合后执行；L4下一04:10至06:10须06:11闭合后。均持有同main排他锁、3个新观察reserve后继续原规则/本金/cash/q/risk，不重复00资金费、不注入研究期限。历史通过仅是固定局部门槛通过，D3虽改变路径但收益/DD不及旧对照，D7是旧路径别名，未启动新前向账户或定时任务。
