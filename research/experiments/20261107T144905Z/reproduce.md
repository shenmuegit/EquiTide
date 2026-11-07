本轮实际执行与复核命令（UTC 20261107T144905Z）

固定执行目录：`/home/desktop/Documents/Codex/EquiTide`，仅 main，同一 branch.lock，未创建分支/工作树。

Python解释器：`/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B`；仅使用该解释器，所有代码/数据操作工作目录均为上列EquiTide仓库。环境：`PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`。

本轮命令通过 `research/experiments/20261107T144905Z/commands.py <phase>` 逐阶段真实运行，各 `<phase>_commands.json` 保留绝对命令、工作目录、开始/结束时间、退出码与stdout/stderr日志；reserve_batches及finish_batches保留每个registry.py真实调用。

顺序：freeze → 合成负例（预期exit1）→ initial（参数边界/未来追加不变性、完整银行相加及错位时间轴检查与36源绑定）→ reserve_batch_0/1 → evaluate → audit → counts → summary → exports → decisions → grid → finish_batch_0/1 → finish。

原账户：midnight_archive只读检查既往午夜证据；l4h02 → fewm（仅复用同窗口真实公共行情，独立自身账本）→ candidate（仅复用公共metadata/time，自取其窗口行情）→ forward（reserve/observe/audit/finish/离线reproduce）。实际截止时间见account_windows.json，严格延续原计划和原净值，不从现金重开。

然后review只读完整登记/哈希/数值权重等价/原账户全净值与原始输入，执行原样 `python3 checks/strategy_registry.py`、`python3 research/monitor/snapshot.py`、`python3 checks/monitor_snapshot.py`，最后collect和finalize封存、main非强制push及远程完整树/内容核对。

复现所需真实行情路径/版本/行数/SHA见plan.json.data及data_manifest.json.real_market_inputs；逐成本新原生完整分段账户/实际成交/资金费证据和父组合对齐轴摘要在results/*.json.gz，未提交大行情。来源公共响应的URL、检索时刻、内容哈希、UTC单位、overlap和source输入均保留。input_manifest及raw_evidence_index追溯原始证据；忽略目录的原始数据与首段warmup保留。

每个新参数与组合spec在计算前已reserve；已有实际结果只读。同一main已有finished配置不要再次reserve或重新运行evaluate/observer；这些命令是已执行过程的复现记录。离线核算应先核对绑定源、全部输入/结果哈希和原账户链，当前轮实际audit/forward --reproduce结果在对应真实退出码收据。

本轮没有重新拟合或OOS择优改门槛；370天及近期40天均是重复研究的开发/验证历史，非独立最终/未来/实盘收益。
