# 复现与核验

工作目录 `/home/desktop/Documents/Codex/EquiTide`；解释器 `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B`。实际命令、UTC及退出码见command_receipts。

原始audit.py及其失败日志保留；有效只读金融核验器为audit_count_recovery.py，只修正旧对照计数断言，数值核算不变。audit_forward.py及三个audit_*原账户核验器只读检查，不产生新模拟成交。已finish配置不可重reserve/执行。

plan.json:data保存原大行情路径/SHA，read_only_references保存原spec/report/archive SHA；必要原始raw/packet小副本及按原路径恢复方法见raw_evidence_index，原大行情仍在忽略缓存。

registry_records.jsonl为本轮32条原始事件，既有registry读取主簿和全部片段；归档完整性见registry_archive_verification。官方访问URL/UTC/源码内容版本SHA见primary_source_access，下载代码未执行。
