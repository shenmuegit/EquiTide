本轮复现与真实执行记录

固定执行目录：`/home/desktop/Documents/Codex/EquiTide`，仅main；同一branch.lock内运行，未建立其他分支/工作树。

解释器：`/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B`；只借用解释器，全部代码与数据操作均在本EquiTide目录。环境：`PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`。

本轮实际阶段命令形式：`<解释器> research/experiments/20261107T165106Z/commands.py <phase>`。全部绝对命令、cwd、执行起止、真实退出码及stdout/stderr日志见每个`*_commands.json`。每个12新定义的registry.py reserve/finish实际调用在reserve_batches/finish_batches。

已执行阶段：freeze → 预期失败合成负例 → initial（351边界/未来不变性、18邻域、完整银行与错位时间轴检查、36源绑定）→ reserve_batch_0/1 → evaluate → audit → counts → summary → exports → decisions → grid → finish_batch_0/1 → finish。summary_retry1只修复图与说明的ETH退出标签，未计算策略、改金融报告或绑定源码；初版证据保留。

原账户：midnight_archive只读历史午夜证据；l4h02、fewm、candidate、forward分阶段实际运行。L4/FEWM窗口14:10→16:10UTC跨实际16资金费，分别使用各自q、rate/mark/ns，不复制现金流；single/SMA12:30→14:30未跨16。four原计划、现金、持仓、已计成本、fullNAV前缀不变，不从现金重开，不重复首单、00/08或旧资金费。forward末尾--reproduce离线重放，无HTTP/ledger写入。

后续只读review核对完整登记、旧对照、数值权重等价、输入哈希、各自身账本和完整净值；原样运行`python3 checks/strategy_registry.py`、`python3 research/monitor/snapshot.py`、`python3 checks/monitor_snapshot.py`。collect保留当前真实输入和必要状态，finalize封存，publish非强制main push并完整远端tree/blob哈希核验，最后释放锁。

行情路径/版本/行数/数据SHA在plan.json.data和data_manifest.json；大历史Parquet保留于忽略data/。新原生完整分段状态、决策、真实历史回测成交和资金费证据在results/*.json.gz；父组合按保存轴对齐完整银行NAV，无父订单/转账/再平衡/重复资本权重。逐成本、逐30日折、近期5日折和全连续OOS日净值、敏感性CSV齐全。

全部当前公共响应URL、检索UTC、原始压缩字节与哈希、毫秒转纳秒、bar闭合状态和overlap对应保留input_manifest/raw_evidence_index；保留原账户首段warmup和历史链。重新复核先校验绑定源码、输入和结果哈希。

同一具体配置已有finished结果，读旧证据；以上为本轮已执行复现过程，不在main再次reserve/evaluate/observer已完成窗口。所有历史正负及失败均留档；本轮没有根据OOS结果改变参数、邻域或失败门槛。370日与近期40日都是反复研究的开发/验证历史，不能称独立最终或稳定实盘盈利。
