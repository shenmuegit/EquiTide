# 复现命令与边界

工作目录固定 `/home/desktop/Documents/Codex/EquiTide`，main 分支；写登记/结果/监控与Git时保持branch.lock排他锁。运行时 `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B`，环境PYTHONDONTWRITEBYTECODE=1、OPENBLAS_NUM_THREADS=1、OMP_NUM_THREADS=1。所有真实源输入路径/版本/时间边界/SHA256见plan及data_manifest；实际每条命令的cwd、开始/结束时间、exit code及stdout/stderr见各commands.json与日志。

以下为本轮实际顺序，文件前缀均为research/experiments/20261102T200225Z/：

1. bootstrap.py 完整读取registry主簿/片段、279份既往结论、任务和三技能、README、原freqtrade结果/ZIP、checks/*oos.py；核验初始16实际证据与全部保护文件。
2. check_asymmetric.py --legacy-exit-range：旧源合成接纳红灯实际exit1，单独保留。commands.py freeze 冻结12spec及完整两轴/时界/失败门槛；commands.py initial 完成144政策与18旧行fixture并唯一绑定全部必要源代码。
3. commands.py reserve_batch_0、reserve_batch_1：12次registry.py reserve均成功后，commands.py evaluate实际计算6原生和6父、36成本场景。旧E0.5%、BTC与同预算持有来源只读，禁止精确旧配置重算。
4. commands.py audit独立复核；commands.py summary只读导出。audit成功后counts、decisions；summary成功后grid、exports。原生/组合九格表、全部月/近期折、每日NAV、完整曲线DD、Sharpe/Calmar、邻域/边界/悬崖均保留。
5. 观察登记串行：commands.py forward延续SMA16:30→18:30并离线精确重放；commands.py candidate延续原single同窗口；commands.py l4h02延续原未过滤L4/H2的18:10→20:10，20:11参考必须已闭合。每窗口先reserve，保存原始GET/packet、精确原账户账本/NAV链，独立审计后finish；不替换冻结规则/本金/持仓，00/08/16已记资金费不重复。
6. commands.py finish_batch_0、finish_batch_1、finish分别完成所有12实际配置，不遗漏淘汰/负收益期间；observer_status只读旧账户。review核验21新ID/42追加事件及旧源/账本/代码哈希。
7. commands.py gates实际执行python3 checks/strategy_registry.py、research/monitor/snapshot.py、checks/monitor_snapshot.py；feed逐行核对全部旧展示与12新行/36场景；collect保存完整短窗原始证据和下轮账户状态。监控无新回测/成交，失败恢复上次有效汇总。
8. 实际view_image检查sensitivity.png；只清本轮可重建缓存，保留全部真实结果、必要代码、完整账本与失败。finalize.py直接运行核验并封存，封存后不修改本轮文件。
9. publish.py publish仅stage本轮和五个必要共享文件，commit并SSH非强制push main，fetch/独立ls-remote、完整递归tree与必要远端blob SHA256核验；实际终态exit0后释放本轮broker并复查。

已完成轮次以已有报告/原始账本进行只读核验，不覆盖封存文件、不重复reserve/重跑已完成策略、不补下过去报价订单、不创建其他分支或带分支worktree。观察续接必须另行预登记新的闭合截止。全部原始负收益折与淘汰结果是有效历史证据。
