本轮真实执行与复现记录

固定目录：`/home/desktop/Documents/Codex/EquiTide`，仅main，同一branch.lock。未创建分支或工作树；保留预先存在data/normalized。

解释器：`/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B`，只使用该解释器，所有代码、行情、Git操作cwd均为固定EquiTide目录。环境：`PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`。

阶段命令形式：`<解释器> research/experiments/20261107T185131Z/commands.py <phase>`；每个`*_commands.json`保存实际绝对命令、cwd、执行起止、真实退出码与stdout/stderr日志；reserve_batches/finish_batches保留12个新参数/父组合的逐项registry.py真实调用。

已执行：freeze→预期exit1合成双重权重负例→initial（18个D/K邻域、27未来追加不变性、15严格斜率边界、5入场波动/持有守则、完整银行和错位轴检查、36源绑定）→reserve_batch_0/1→evaluate→audit→counts_retry1→summary→exports→decisions→grid→finish_batch_0/1→finish。counts首次在审计文件未就绪时退出1，真实错误保留；审计exit0后只读counts_retry1通过，金融计算未重跑。

原账户：midnight_archive只读历史午夜证据；l4h02→fewm→candidate→forward分阶段真实执行。当前SMA/single14:30→16:30UTC，single资金费使用自己的真实rate/mark/ns/q，仅结算16一次；L4/FEWM16:10→18:10不重复既往16。各自身现金/实际q/desired/费用/风险/fullNAV连续，不从现金重开、无新日决策/成交。SMA65原Float规则及最后完整65日R024625源不变，forward最后--reproduce离线重放，无HTTP/登记写入。

只读review再核对新ETH完整参数、旧K2控制、数值权重等价、NAV别名、来源哈希及每个原账户完整链；原样执行`python3 checks/strategy_registry.py`、`python3 research/monitor/snapshot.py`、`python3 checks/monitor_snapshot.py`，collect和finalize封存后非强制main push、独立HTTPS及完整远端tree/blob核验。

真实历史数据路径/版本/行数/SHA在plan.json.data和data_manifest.json；大Parquet与旧首段warmup保留忽略data/，不提交。新ETH原生完整分段账本、决策、回测成交、资金费与风险证据在results/*.json.gz。父组合相加保存轴上的完整实际银行NAV，无父订单/转账/再平衡/缩放。所有逐成本、30日折、近期5日折、连续OOS日NAV和两轴敏感性CSV完整保存。

当前公共HTTP响应URL、检索UTC、原始字节/压缩哈希、毫秒→纳秒、闭合bar及overlap验证见input_manifest/raw_evidence_index。先核对36源绑定、全部输入/结果哈希及原账户链；以上命令记录是已经执行的过程。相同配置已finished时只读，不在main重复reserve/evaluate/observer已完成窗口。

原账户保持原规则；新历史passed不自动采用或建立新模拟账户。重复370日开发历史、大量试验、路径重复、下边界最佳及跳变均保留，不称独立最终/未来/稳定实盘盈利。
