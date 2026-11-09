执行目录固定 /home/desktop/Documents/Codex/EquiTide；本地/远端唯一 main；研究、登记、原账户续接、原生监控和 Git 操作持有 research/automation/branch.lock 排他锁。未建分支/工作树，未下真实订单。

解释器 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B；环境 PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1。bootstrap_receipt.json、*_commands.json、reserve_batches/、finish_batches/、review_*_receipt.json 和日志保存实际命令、cwd、UTC、真实原生退出码、stdout/stderr。

实际流程：bootstrap完整历史 → capture_current08_public只读官方结算字段（无账户计算）→ freeze → 两项纯合成错误检测 → initial（边界/未来隔离/邻域/36源与真实08字段绑定）→ reserve_batch_0/1 → evaluate → audit/counts/summary/exports/decisions/grid → finish_batch_0/1/finish → l4h02/fewm/candidate/forward → midnight_archive/observer_status/fewm_status → summary_retry1仅缩短拥挤图标签、核对11CSV/report原字节不变 → 独立只读review/journal_layout → strategy_registry → snapshot/monitor_snapshot → feed → collect → seal → main commit/push → 独立远端ref/tree/blob与完整账户链核验。

已经完成配置只读复用，不重复reserve/evaluate。specs/、report.json、results/*.json.gz、逐成本/逐折/每日/敏感性CSV以及各账户完整链为真实依据。新VC3.5/4%组件各自实际计算，旧VC4.5%三K列及BTC3750/N1000银行只读；只过滤新开/反手，同向原数量保留。audit.py/audit_native.py用保存账本独立Fraction/Decimal核验信号、LOT、费用/量冲击、实际资金费、风险代理和完整连续NAV，不调用策略simulate/decide/trade重跑。

真实源、边界与SHA256见plan.json、data_manifest.json、各账户input_manifest.json/raw_evidence_index.json与forward_report.json.provenance。大行情留在忽略data/，完整初始FEWM warmup、账户账本、冻结规则及必要原响应保留。SMA当前/上轮分钟数组实际重叠核对，完整65日上下文仍为20261109T030420Z已验证1d/1m输入。

当前SMA/single04:30→06:30仅闭合mark；L4/FEWM06:10→08:10各自结算实际2026-11-09T08:00:00.001Z资金费。公开fundingTime/rate/mark从官方新响应取得，+1毫秒精度保留；现金流按自身结算前q计算，收入不放大、仅支出受成本压力。各自完整NAV前缀保留，无新日决策/成交，不重启/强制平仓/采用研究VC。

下一L4/FEWM08:10→10:10仅mark，禁止重计08；single06:30→08:30尚需自己的08结算。当前公开字段/raw可保留原检索UTC/hash只读复用，不能复制L4/FEWM现金流或旧Nov8字段。SMA现货无资金费，下一同窗仅mark。四账户下一日决策Nov10_00:01，届时SMA新65日上下文须重新核对。

原生命令 python3 research/monitor/snapshot.py 和 python3 checks/monitor_snapshot.py 只汇总已有证据；未修改checker/预算/规则/本金/持仓，没有新报价成交、网页重部署或重复定时任务。封存后发布SHA与解锁回执只写.git/automation_proofs/20261109T090618Z.json，不重写本轮完成证据。
