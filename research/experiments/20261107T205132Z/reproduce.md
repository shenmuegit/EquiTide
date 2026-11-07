本轮复现工作目录固定为 /home/desktop/Documents/Codex/EquiTide，使用 main 与 research/automation/branch.lock 排他锁。所有步骤与实际起止时间、退出码见 *_commands.json、review_*_receipt.json，首次 reserve 及 finish 的逐项回执见 reserve_batches/、finish_batches/。不要在原目录重复 reserve/evaluate/观察续接，也不要覆盖旧真实结果；先读取完整逻辑登记和 spec 指纹查重。

解释器为 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B；这是依赖解释器路径，执行 cwd 始终为当前 EquiTide。设置 PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1。本轮代码先冻结、校验和绑定，再逐定义 reserve 成功，最后才计算。

真实执行次序：commands.py freeze；已保存预期失败的纯工程 TDD_red 检查；commands.py initial；commands.py reserve_batch_0；commands.py reserve_batch_1；commands.py evaluate；commands.py audit；commands.py counts；commands.py summary；commands.py exports；commands.py decisions；commands.py grid；commands.py finish_batch_0；commands.py finish_batch_1；commands.py finish。commands.py 均指本轮目录中的绝对脚本路径，不能把代码检查当实际结果。独立审计只重算核验公式，不重新运行策略、下单或改资格。

本轮6个ETH原生 D6/7/8×K1.25/1.75%与6个完整银行raw[1,1]组合，旧K1.5%三格和固定BTC29/H3/E1 C3750/N1000仅只读，所有新原生资金量/成本/资金费/数量独立计算。数据来自旧 data_manifest 中冻结的真实370日历史、33日过去完整收盘和真实资金费/mark/成交量，原始行情不提交。各新完整路径、逐折、近期继承状态和1/2/3倍成本结果在实际report、归档和CSV中，所有指纹及数据/源代码哈希以spec、plan、code_binding与data_manifest为准。反复使用开发历史并非未触碰最终样本。

原四账户先完成 commands.py l4h02，再 fewm、candidate、forward；各步骤独立终态0后才启动下一步。L4/FEWM续接Nov7 UTC18:10→20:10，SMA/single续接16:30→18:30，先绑定窗口、原现金/q/成本/风险与完整NAV，再逐观察定义 reserve/finish；无新日决策、资金费或成交。FEWM仅复用L4同窗口公共行情，single只复用元数据/时间再获取本账户窗口。forward.py --reproduce 为只读离线复核，不产生新账户、订单或估值登记。SMA完整65日上下文保留R024625来源，三个永续各自已计16资金费不得重复。下一日决策UTC Nov8 00:01；所有账户仍partial延迟shadow。

审查：review/run_checks.py 运行 control_diagnostics.py、realized_aliases.py、account_windows.py、market_reuse.py、evidence.py；完成全部24ID后才运行 journal_layout.py、metadata.py；commands.py review、gates、feed、collect。其中 gates 在同一main锁内实际运行 python3 checks/strategy_registry.py、python3 research/monitor/snapshot.py、python3 checks/monitor_snapshot.py，只读汇总已有账户与报告。独立校验每条旧monitor行、paper账户、原账本和冻结规则不变。

仅在全部回执和必要检查通过后直接运行 finalize.py 封存；随后 publish.py publish 使用非强制main push，再独立HTTPS读取远端ref/fulltree/blob内容，与本地真实完整证据逐项核验。成功后释放原锁broker，再运行.git/automation_proofs中本轮postrelease脚本。真实提交SHA、远端核验与锁释放退出码仅写.git私有出版回执，不自引用改变已封存提交。所有失败原回执保留；不重跑已完成金融配置或账户。
