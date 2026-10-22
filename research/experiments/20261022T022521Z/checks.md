本轮只在固定工作目录及 `codex/strategy-research` 分支执行，起点为 `b6d9e1a92d7d8556abe400b8fe6fce765bc9ff3e`。先同步远端并读取完整登记、139份既往结论及三个指定验证技能；初始16项均已有实际结果。研究、登记、监控及提交推送始终持有同一分支排他锁。

18个预登记 MACD histogram 配置完成54个成本场景、648个逐折结果；全部 rejected，所有负收益保留。1/2/3倍净正数量8/7/4。最优 ETH F24/S72 虽有 +40.0176%/+38.5444%/+37.0836%，但只有5/12盈利折、4次往返、33.3%邻域三倍盈利，未满足预先冻结的门槛。没有根据结果追加网格或放宽失败判据。

信号自检覆盖首值种子与递推、恒价/上涨/下跌、MACD及signal关系、未来前缀不变、尺度/平移和零边界。闭式EMA权重与 math.fsum 独立核对19440个决策状态和时间，核对1164笔成交余额、54条完整分钟路径的本金锚定回撤、648折及19494个日净值点。18种完整三成本NAV路径均不同，但不代表独立市场样本。完整重放报告哈希保持 `2ea134e3dcad908fce02e685469ac4f10ce526b05940ab53c4c4adedef4b855b`。

本轮 run.py verify 仅调整账户保护的复现范围：核验一次调用前后共享账户不变；未来 paper10 状态可由独立任务合法推进。冻结 paper10 计划和旧SMA源报告/源状态仍严格验证历史哈希。本轮收尾另验证四个受保护输入均等于冻结前哈希。调整后的实际命令 exit0，见 verification_scope_command.json；会计引擎、已finish金融报告、收益和账户未改。

原冻结SMA从 UTC 00:20 续接至02:00，新增100闭合分钟。九场景完整28841点旧前缀保留并追加至28941点，累计28919分钟/20完整天；零新增日决策、参考点及模拟成交。现金、数量、desired、交易和费用保持。源分钟输入按其真实1d/1m字典容器读取。本轮下一日决策仍为2026-10-23T00:01:00Z，不能重复已经完成的Oct22决策，也不能越过下一日决策只mark。forward_report原始SHA为 `6b4af44c42b8dc21698109369e2605d1723898b575a279ee28c3057836fb1a75`，独立续接审计及九场景离线精确重放均实际exit0。

final_gates.json记录以下五个实际进程全部exit0，分别保留原stdout/stderr及日志；不是用cat日志的退出码代替检查结果：

- `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261022T022521Z/forward.py --reproduce`
- `python3 checks/strategy_registry.py`
- `python3 research/monitor/snapshot.py`
- `python3 checks/monitor_snapshot.py`
- `git diff --check`

监控为3721个研究配置、10账户、87次观察，受保护输入未变。本轮18配置/54成本场景的收益、整体分钟回撤、逐折收益、往返、NAV哈希及OOS边界与原报告逐项一致，见 feed_verification.json。旧exclusive-end回归指纹537f5a8fc4b6e58511fabbde15096659e072be117d9a365d3827ac178134c70e仍可展示。本轮不修改共享监控读取代码，历史失败事实不覆盖。一次只读留档枚举误读不存在的results键而exit1，按真实configs键恢复并留在inspection_notes.json；没有因此重算回测或重写金融结果。

21项reserve/finish均保存实际成功记录与原报告SHA。核验后仅删除54个可重建checkpoint及本轮字节码，详见cleanup.json；原始响应、必要重放输入、所有完整结果、源状态、冻结规则及账户账本保留。必要的大结果JSON保持原字节，不另做压缩迁移。大行情仍留忽略data，四个原始Parquet的路径、大小和SHA及所有轻量证据哈希见data_manifest.json。只提交本轮目录、登记和两份监控feed；随后普通SSH非强推、fetch/ls-remote及完整tree核验，完成后释放已有锁。

未下真实订单、未新建定时任务或委派子代理；未重部署网页。2025–2026为反复使用的开发历史，SMA仍只有20完整天的延迟shadow，没有实盘成交、未触碰最终测试集或稳定盈利证据。
