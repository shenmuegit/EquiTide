执行目录固定 /home/desktop/Documents/Codex/EquiTide；本地/远端唯一 main；研究、登记、续接、原生监控和 Git 操作持有 research/automation/branch.lock 排他锁。未创建分支/工作树，未下真实订单。

解释器 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B；环境 PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1。bootstrap_receipt.json、*_commands.json、reserve_batches/、finish_batches/、review_*_receipt.json 和日志保存实际命令、cwd、UTC、真实原生退出码、stdout/stderr。

实际顺序：bootstrap完整历史读取 → freeze → 两项纯合成错误检测 → initial（边界/未来数据隔离/邻域、完整spec与36执行源绑定）→ reserve_batch_0/1 → evaluate → audit/counts/summary/exports/decisions/grid → finish_batch_0/1/finish → l4h02/fewm/candidate/forward → midnight_archive/observer_status/fewm_status → 全部独立只读review及journal_layout → strategy_registry → snapshot/monitor_snapshot → feed → collect → seal → main commit/push → 独立远端ref/tree/blob与账户全链核验。

已完成配置只读复用，不再次reserve/evaluate。十二完整spec、report.json、results/*.json.gz、十一份逐成本/逐折/逐日/敏感性CSV和全部账户原始链条为依据。audit.py/audit_native.py从保存账本独立Fraction/Decimal核验信号、LOT/执行成本/量冲击/实际资金费、保证金代理与完整连续净值，不调用策略simulate/decide/trade重跑。新E0.5/0.75%各自实际计算，旧E1%三K对照与BTC3750/N1000银行只读；重合净值不是数学等价或独立行情证据。

数据边界、真实源文件和SHA256见plan.json、data_manifest.json、各账户input_manifest.json/raw_evidence_index.json与forward_report.json.provenance。大行情留在忽略data/，完整初始FEWM warmup、冻结规则、账本及必要原响应保留。SMA当前/上轮分钟数组核对真实重叠，完整65日上下文仍来自20261109T030420Z真实1d/1m输入；其源哈希与前轮交接保持。

四冻结账户本轮仅补120分钟闭合mark/适用闭合小时风险，0新资金费、日决策、成交；原现金/q/desired/费用/完整NAV前缀不变，负收益保留。不从现金重开、复制金额或强制截止平仓。下一SMA/single04:30→06:30仍仅mark；L4/FEWM06:10→08:10可能跨名义08资金费，必须当实际结算后读取新真实fundingTime/rate/mark，保留毫秒/纳秒精度并按每个自身结算前q核算一次，支出压力、收入不放大。当前未来08计算为0，不用旧Nov8字段或其他账户现金流。下一日决策Nov10_00:01。

原生命令 python3 research/monitor/snapshot.py 与 python3 checks/monitor_snapshot.py 只汇总现有证据；未修改checker/预算/规则/本金/持仓，无新报价成交、网页重部署或重复定时任务。封存后发布SHA及解锁回执只写.git/automation_proofs/20261109T070547Z.json，不重写本轮完成结果。
