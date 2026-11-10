工作目录固定 /home/desktop/Documents/Codex/EquiTide，运行时 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B，环境 PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1。

实际argv/cwd/UTC/退出码见reproduction_history.json和*_commands.json。执行顺序：完整context/bootstrap；实际funding源及syntheticVW默认等价/边界/未来不变性；freeze与initial；两批各8项reserve；一次evaluate、独立audit/counts/summary/exports/decisions/grid；两批finish及确认。旧VW10/R0.0075中心仅复用压缩结果，未reserve或计算。

四原账户各一次新截止续记、独立全NAV核验；SMA --reproduce只读重建，不HTTP、不写ledger。随后同锁journal_layout、sourcecheck、strategy_registry、monitor snapshot/check、feed/collect。只读审计可运行audit.py/check_decisions.py/check_exports.py读取已保存结果与真实来源；不得重新推进完成的账户或登记完成配置。

完整data哈希/版本/来源在plan、funding_signal_preflight、data_manifest；实际raw响应和完整原账户链保留，下一SMA日上下文仍031055的65个SPOT日。当前四窗口均无资金费；下一L4/FEWM06:10–08:10需FRESH实际Nov10_08资金费字段和08:11闭合参考，不能使用Nov9_08预检或旧00率替代。

最后封存并普通非force push main，完整远端ref/tree/blob/账户链核验后解锁。封存后不得在本轮目录追加/重写任何回执、结果或下一状态。
