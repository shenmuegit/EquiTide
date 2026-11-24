# 复现与核验

工作目录 `/home/desktop/Documents/Codex/EquiTide`；解释器 `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B`。实际命令、UTC及退出码见command_receipts。

有效只读金融核验器为audit.py，从首次执行即采用计划推导计数，独立检查现金/数量/信号/费用/资金费/保证金及全NAV。audit_forward.py及三个audit_*原账户核验器只读检查，不产生新模拟成交。已finish配置不可重reserve/执行。

plan.json:data保存原大行情路径/SHA，read_only_references保存原spec/report/archive SHA；必要原始raw/packet小副本及按原路径恢复方法见raw_evidence_index，原大行情仍在忽略缓存。

registry_records.jsonl为本轮30条原始事件，既有registry读取主簿和全部片段；归档完整性见registry_archive_verification。官方访问URL/UTC/源码内容版本SHA见primary_source_access，下载代码未执行。
