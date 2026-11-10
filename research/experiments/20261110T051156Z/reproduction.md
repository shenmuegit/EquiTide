全部命令工作目录固定为 /home/desktop/Documents/Codex/EquiTide。Python运行时 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B，PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1。

实际执行顺序与argv、UTC起止、原生退出码见 reproduction_history.json 和 *_commands.json：freeze、初始检查（含真实失败及initial_retry1）、三批reserve、一次evaluate、audit/counts/summary/exports/decisions/grid、三批finish及复核；四个原账户各一次续记与全NAV独立审计；同锁journal_layout、sourcecheck、strategy_registry、monitor snapshot/check、feed和collect。所有实际配置spec各自保存，registry_records.jsonl保留reserve/finish。

只读核验：用同一Python运行本轮 audit.py /check_decisions.py /check_exports.py 读取真实保存结果和真实源数据；这只审计既有路径，不应新reserve或重新计算完成的策略。原SMA forward.py --reproduce仅重构既有闭合窗口且不请求网络、不写账户或ledger。原始资金费/分钟/mark及版本SHA见plan、funding_signal_preflight、data_manifest；完整真实账户链与冻结规则不能删除。

封存/发布只运行本轮finalize.py一次，后续publish.py publish在已持有共享flock且main一致时普通非force推送，并核对完整远端tree/blob/账户链。不得在已封存目录重新写检查回执、重新finish或再次推进同一账户截止。
