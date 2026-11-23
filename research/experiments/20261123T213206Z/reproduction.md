# 已实际执行的复现与核验

工作目录固定 `/home/desktop/Documents/Codex/EquiTide`。解释器 `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B`。

所有实际命令、UTC和退出码见 `command_receipts/*.json`；历史命令包括失败units与修正units_retry。原配置已finish，避免重新reserve/执行同一配置。

只读复核可执行 `audit.py`（原生账本、全NAV、逐折、成本、资金费、保证金及敏感性）、`audit_forward.py`（SMA全前缀与本轮120分钟mark）、三个`audit_*`观察核验器以及 `checks/strategy_registry.py`。它们不产生新策略或账户成交。图表/经济比较仅读取已保存结果。

数据原始路径及SHA256见 `plan.json:data`；源报告/压缩账本/specSHA见 `read_only_references`。官方只读接口访问日期、SDK内容SHA和原始gzip见 `primary_source_access.json`，不执行下载代码。
