本轮原始执行目录：/home/desktop/Documents/Codex/EquiTide；唯一分支 main；持有 research/automation/branch.lock 排他锁。解释器 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B；环境 PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1。

实际命令、完整 cwd、起止时间、原生退出码与 stdout/stderr 均见 *_commands.json、bootstrap_receipt.json、review_*_receipt.json 和对应日志。实际依赖顺序为 bootstrap → freeze（只读草稿检查后在首个 reserve 前再次冻结）→ 两项纯合成错误检测 → initial → reserve_batch_0/1 → evaluate → audit/counts/summary/exports/decisions/grid → finish_batch_0/1/finish → l4h02/fewm/candidate/forward → midnight_archive/observer_status/fewm_status → 独立只读 review → strategy_registry → snapshot/monitor_snapshot → feed → collect → seal → main commit/push 与远端 tree/blob 校验。

已完成配置不能再次 reserve/evaluate；使用登记的 report、results/*.json.gz 与 read_only_references 比较。audit.py/audit_native.py 用保存的完整真实源和逐事件账本独立核对信号、LOT/手续费/量冲击/资金费、净值与整体回撤；不调用策略 simulate/decide/trade。原账户的独立核验见 audit_incremental.py、audit_forward.py；保留完整自身指针链和首段行情，不能从现金重开或用其他账户复制金额。SMA 本轮 forward.py 是处理真实跨午夜的原冻结规则续接版；下一窗口只补 mark 时，按 next_research_state.json 使用此前 mark-only 模板并固定新窗口，不能复用本轮已完成 cutoff。

市场数据及 SHA256 见 plan.json 的 data、data_manifest.json 的 real_market_inputs/source_annual_and_recent_inputs，以及各账户 input_manifest.json、raw_evidence_index.json、forward_provenance.json。大行情仍在忽略的 data/ 路径，所有必要原响应/首次 warmup/完整账户账本保留。UTC单位 ns/ms 明确区分；午夜资金费原公开响应只读复用，原检索 UTC 未重写，单策略现金流按自己结算前 q 推导。

只读公开汇总的实际原生命令为 python3 research/monitor/snapshot.py 与 python3 checks/monitor_snapshot.py；不改 checker、冻结规则、本金或持仓。封存后不得把 post-push SHA 写入本目录；完整发布回执保存在 .git/automation_proofs/20261109T030420Z.json。
