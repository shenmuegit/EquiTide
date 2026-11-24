# 复现与核验

工作目录 `/home/desktop/Documents/Codex/EquiTide`；解释器 `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B`。

实际命令、开始/结束UTC及退出码见command_receipts/*.json。已finish配置只读复核，不能重新reserve/执行相同配置。audit.py独立检查实际源账本、完整NAV、逐折/敏感性、数量、成本、资金费和保证金；audit_forward.py及三个audit_*核验原观察前缀，不产生新模拟成交。

plan.json:data保存原大行情路径/SHA，read_only_references保存原spec/report/archive SHA。原始大行情留在忽略缓存；观察raw/packet若缓存缺失，可从raw_evidence_index按原路径恢复精确压缩字节后运行只读核验器。

registry_records.jsonl为本轮32条未重编码的原reserve/finish事件；使用现有registry.read_events/read_records读取完整主簿及全部片段。checks/strategy_registry.py与本轮checks.py已实际运行。

官方源码访问URL、日期及内容SHA见primary_source_access.json；下载代码仅只读，不执行。
