# 实际核验与保留范围

所有命令工作目录均为 `/home/desktop/Documents/Codex/EquiTide`，持有本轮 broker PID 1685627 的 branch.lock 排他锁。金融解释器 `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python`；PYTHONDONTWRITEBYTECODE=1、OPENBLAS_NUM_THREADS=1、OMP_NUM_THREADS=1。

54新父组合在计算前逐项reserve成功，54项按最终报告原SHA逐项finish；原SMA新截止的3项同样先reserve后finish。合计57ID/114条只追加事件，无组件策略重跑，无旧父组合重算或重新评级。通过18、淘汰36，三成本均净正；淘汰原因全为1倍正折不足8/11。

`initial_commands.json`：相对时间键/错位资金费/因果携带/原值资金相加合成检查及54项预登记，均真实exit0。

`forward_commands.json`：原SMA跨日reserve、真实数据抓取、续接、独立审计、精确离线重放、finish六步均实际exit0。4份原HTTP响应/组合输入留档，两个65日线源重叠64条一致，两个121分钟输入含1条源重叠，新增120分钟和1参考；31612旧NAV前缀完整，新31733点，累计31709分钟/22完整日。BTC hold_long、ETH hold_cash，全成本新增成交0。下一原日决策2026-10-25UTC00:01，冻结2027-03-31终点保持。

`research_commands.json`：54父组合计算、初审、完整表格/热图、终审、finish五步均实际exit0。54源NAV从18旧账本及原行情恢复，全部原SHA匹配；独立审计另从2574源成交/53460资金费事件重建，结构化时间键对齐，162新父路径78747066点、1944整体/逐折指标核对。初审SHA在描述性汇总前，终审SHA在全部描述后且finish前；finish后未改报告字节。

`source_check_receipt.json` 和 `source_checks.log` 保存实际执行exit0：原27父组合状态/原NAV/源报告不变，18源组件、8份原Parquet、4268受保护文件不变，全部57ID严格只追加reserve+finish。`review_commands.json` 实际exit0：243成本行（含旧只读）、2673折行（含旧只读）、53622新日NAV、216四维邻接边核对。54/54新组3倍收益低于匹配ETH30旧组；12项1倍正折增加、10项减少。描述性Sharpe邻接诊断标记45条边，不改冻结门槛或已finish资格。

`gates_commands.json` 中真正执行 `checks/strategy_registry.py`、`research/monitor/snapshot.py`、`checks/monitor_snapshot.py`，三者exit0。监控4284配置/110观察/10账户，受保护输入未变。`feed_commands.json` 中归属核验实际exit0：54新父组合162场景、原27父状态/criteria/NAV不变，历史排他end别名537f5a8fc4b6e58511fabbde15096659e072be117d9a365d3827ac178134c70e仍展示。没有把cat日志的退出码当执行成功。

真实失败事实：只读定位时误尝试不存在的旧轮manifest.json，FileNotFoundError/exit1；随后列目录并读取实际data_manifest.json，记录于read_failures.json。新轮启动元数据规范试验数的过滤谓词原含SMA快照，已按monitor相同口径修正4856→4481，原值和原因留context.json；未改冻结计划、收益、账户或报告。没有金融计算/正式门禁失败。

热图已实际打开目视核验；旧ETH30只读列与新31/32列明确区分。图中各色均以同一0起点色阶显示实际正收益，不据颜色代替通过门槛。

保留完整已finish JSON原字节、54新archive/spec、原SMA完整9场景NAV/状态/输入/4原响应、逐折/成本/敏感性与哈希。旧完整源账本只引用原路径/SHA，不复制；8份约56.8MB原Parquet留忽略data及哈希/路径。未生成磁盘NPY/checkpoint/pycache/重复下载页，故无需删除。必要结果JSON不为体积迁移或改写。

复核：以固定金融解释器运行本轮 `audit.py`、`check_sources.py`、`forward.py verify`、`audit_forward.py`、`check_feed.py`，均只读已finish结果/原行情。重新抓取数据可能修订；离线重放使用本轮保存原响应。不得再次reserve/评估已finish指纹。真实账户、冻结规则/本金/持仓、旧收益/状态/报告和注册历史保持。

提交和普通SSH非强推后，以fetch、独立ls-remote、完整递归tree/所有证据blob与源哈希进行终验；发布/锁释放回执保存在.git/automation_proofs/20261024T004356Z.json。只有完整终验实际通过后释放本轮broker，不删除共享锁文件。
