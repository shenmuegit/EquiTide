# 复现与实际执行证据

工作目录固定 `/home/desktop/Documents/Codex/EquiTide`。Python `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python`；环境`PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`。本地/远端只用main，branch.lock持续持有到完整发布/远端证据验证结束。

命令顺序和退出码在`*_commands.json`、`*_receipt.json`：bootstrap全量读登记和257结论；freeze；initial与initial_retry1仅完善计数标签/首次独立资格检查后再次绑定源（此时无reserve/计算）；reserve_batch_0六项成功才evaluate；audit/summary/decision_check/exports/grid_diagnostics；finish_batch_0/finish；原账户forward/candidate；新独立l4h02；observer_status/review；gates精确执行`python3 checks/strategy_registry.py`、`python3 research/monitor/snapshot.py`、`python3 checks/monitor_snapshot.py`；feed；collect；seal及非强制push。

新历史批次固定L3/4/5×H2/2.5/3%，V10/cap4.5固定。仅3原生+3父的H3新配置，6个定义/18成本场景；每范围6旧点、36旧成本场景只读复用。新spec/规则/权重/成本/时界/失败门槛先冻结，各ID实际reserve后才计算，实际正负/淘汰全部finish保存；旧参数不重跑不改资格。连续370日、逐月与近期折、完整NAV SHA、状态段、交易与资金费及9CSV保留，无大数组。8真实Parquet和16旧输入精确SHA见manifest。

独立未来计划始终引用`research/experiments/20261031T174613Z/prospective_l4/`原core/observer/plan/binding，无过滤旧L4/H2、5000/15000银行、N500/4500，原180日规则不改。本轮第一截止在见未来数据前固定2026-11-01UTC00:10，原执行器要求参考分钟确实闭合（>=00:11）后才capture，完整校验数据后3reserve再advance。原冻结observer/core不编辑。`audit_l4h02_final.py`是独立只读首窗审计：实际33日raw汇总上下文，Fraction目标，Decimal LOT/tick/费/规模冲击/funding/现金/q，完整短NAV和链、部分资格逐条核验；不调用原normalize/target/trade/advance/transition。传输审计先验完善以保留失败尝试，仅成功页参与packet，原受绑定初稿保留，修订和SHA在future_integration_plan，修订时尚未采集未来数据。

首次真实33日1m warmup完整HTTP页和packet保存在忽略`data/raw/binance/l4h02_forward/<本轮>/`，`l4h02_raw_manifest.json`逐个记SHA/字节，不清理真实输入，不提交大预热行情。Git保留轻量公开metadata/time/hour/funding原页、来自真实packet的11分钟执行引用bar和daily上下文胶囊、全部短NAV/逐笔账本及源SHA。可用本地完整packet离线独立核验；不把合成工程检查或9分钟观察当180日通过，不把部分年化指标当可投资收益。

原SMA65/singleS28按旧本金/现金/q/desired/entry/费用/funding续接至Oct31UTC22:30，不强制平仓、不重新开现金。后续22:30至Nov1UTC00:30跨00funding与00:01日转移，必须真执行原规则并扩展独立审计，不能再套无事件mark-only。新L4独立pointer/batch/账本，原singleS28累计ID链和新L4链分别计数，不互相继承本金/持仓，不混入paper10报价账户或研究试验数。

所有恢复/失败按真实情况留档，不重跑已完成金融模型或观察窗口。只提交本轮证据与5共享文件（registry、两个独立pointer、monitor两文件）。完整main commit/非强制push、递归tree/所有必要blob、两独立观察链、真实publisher退出0及解锁证明在`.git/automation_proofs/20261031T234844Z.json`。网页自动读取main，无重部署/新定时器/真实订单。

首次实际l4h02命令中的模型执行actual0、3项均已finish；只读audit_l4h02_final因API和冻结元数据Decimal尾零不同误判字符串等值（所有数值及NAV链已匹配）actual1。原日志/源不改。l4h02_audit_diagnosis与repair_plan保存完整定位及状态/report/registry SHA守护；audit_l4h02_recovered改用已验证数值相同的冻结精度，l4h02_checks_retry1仅只读审计/索引actual0，未调用observer或再reserve/advance。所有失败和恢复计入manifest；不能直接重跑原l4h02阶段。
