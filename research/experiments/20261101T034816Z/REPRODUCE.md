# 复现与实际执行证据

固定工作目录 `/home/desktop/Documents/Codex/EquiTide`。Python `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python`，环境 `PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`。项目根、main、普通SSH fetch与独立ls-remote已实际核验；上轮研究已推送，远端本轮base为paper10 03UTC提交，保留其修改及预存data/normalized。排他branch.lock由PID732044持有到非强制push及完整远端验证结束，不创建分支／工作树。

命令和真实退出码在 `*_commands.json`、`*_receipt.json`。主序列：bootstrap → freeze → commands.py initial → reserve_batch_0 → evaluate → audit → summary → check_decisions／check_grid_diagnostics → exports → finish_batch_0／finish → forward → candidate → l4h02 → observer_status／review → gates → feed → collect_evidence.py → finalize.py → publish.py publish。每一实际配置必须成功reserve才计算，完成结果独立finish。脚本输出和报告出现不等于进程成功，需等待工具真实终态退出码。

本轮预设固定ETH L4/S28、V10样本log波动cap4.5%，E绝对ROC缓冲=[0,0.0025,0.005]×H=[0.02,0.025,0.03]，9点／范围。只新算E0.25/0.5%、H3%的2ETH原生＋2父、4配置／12成本场景。14旧格点／42成本场景只读复用；共20唯一实际来源包括旧BTC、未过滤基线及同银行持有组件。60个既有ETH15000/N4500定义语义查重，不按名称或family排除新配置。原始子权重[1,1]，实际BTC5000/N500＋ETH15000/N4500，总20000，25/75初始本金；无归一化、NAV线性缩放、转账／免费调仓或跨银行抵押。

信号严格prior完整日close，次UTC00:01原生OPEN不利tick成交。370日开发验证历史2025-10-19至2026-10-24，12完整30日折＋10日尾折，状态／成本／funding跨折不重置；近期40日从day330实际状态继承8×5日折。无拟合／标签，purge0、预热30日、间隔3日；重复历史不是最终未触碰测试。1/2/3倍手续费5bp／半价差1bp／滑点2bp／0.5×past20logvol×sqrt(actualq×OPEN/past20quoteADV)冲击，真实资金费支出加压／收入不放大，LOT/tick/minnotional、参与率<=.001、费用后1倍抵押和正持续时间闭合小时1%维护代理。没有L2/TCA或逐tick容量／清算证明。

独立research audit：Fraction核对2220新决策，Decimal复算实际q／fee／spread／slip／volumeimpact／funding／cash及完整状态段风险。6新原生＋6新父共6540156NAV点、33只读原生／27只读父NAV SHA、43290资金费、1854成交、630整体／月指标、145080小时风险检查实际通过，0拒单。另check_boundary_attribution从已存同E/H2.5场景逐档核验净权益差额=毛价格PnL变化+资金费变化+节省执行成本，实际少6至8执行但12档净权益差额均负，不是新回测。独立check_decisions验证全部冻结门槛，check_grid_diagnostics保留旧criteria/status/sensitivity并只添加扩大网格诊断；10CSV保留各成本／折／近期／完整日NAV／原零缓冲／未过滤基线／同资金持有／现金比较。全部新配置各成本全年净正，但近期父5/8、ETH4/8，局部严格近期父50%、ETH0%，低于6/8和60%，4项全部rejected。负折与失败完整保存。

原SMA65现货Float账户继续旧1500/500、65日±1%原规则；forward_registry.py reserve → forward.py → audit_forward.py → forward_registry.py finish → forward.py --reproduce，续Nov1UTC00:30至02:30只加120已闭合分钟mark，无新日决策／成交。旧43261NAV前缀到43381点、累计43349分钟；cash/q/desired/trades/cost不变，0现金重开。当前分钟数组与上一轮1d/1m字典重叠核验，最新完整65daily上下文仍为20261101T014820Z/forward_inputs.json.gz；下次Nov2UTC00:01前才按原规则更新，不盲用单次dailyhelper。

原singleS28按20261026T110637Z冻结observer/core和20261026T090537Z原plan续00:30至02:30，原10000/10000银行、N1000/3000、ETHL3。独立未过滤L4/H2按20261031T174613Z/prospective_l4原plan/core/observer/binding续02:10至04:10，必须等04:11参考分钟确实闭合才capture，原5000/15000银行、N500/4500、ETHL4/H2/S28零退出，不采用当前研究过滤／缓冲。两套独立pointer／账本／登记链，每新截止3reserve后advance/finish，保留全部旧NAV前缀和实际Decimal仓位／现金／风险，不继承彼此本金、不重复已入账00资金费／日决策，不强制每轮平仓。部分结果rejected不取消各自180日计划，不把短观察年化数当收益能力。

账户audit_incremental.py使用上轮已核验本金schema兼容方案，从各自冻结plan独立取得本金，核对可选binding.capitals，原绑定及模型字节不改。仅复用原normalize做闭合数据／事件组装，独立校验原始HTTP／packet、分钟重叠、完整日上下文、Fraction信号、Decimal LOT/tick／费用／冲击／资金费／cash、正持续时间风险段和全旧NAV＋当前全NAV链、指标／日边界／部分资格，不调用原target/trade/transition/advance。两真实公开GET均保留TLS校验、每个失败尝试／raw／stderr和有界重试回执；原始失败不覆盖，实际资金费动作以原响应为准，不凭预计时间填零。

所有当前2小时HTTP尝试及完整packet、SMA2页raw轻量入Git，raw_evidence_index逐个关联原path／committed_copy／SHA／字节；年度大行情和原33日预热原样保留忽略data。不提交大npy或可重建数组，不删除完整账户账本／规则／登记／核验必需证据。

gates同一锁内精确执行 `python3 checks/strategy_registry.py`、`python3 research/monitor/snapshot.py`、`python3 checks/monitor_snapshot.py`；feed逐一比较全部旧展示行、每个新scene的原报告SHA／资格／成本／净值hash。快照生成失败必须恢复上次有效两个汇总文件并留档具体失败，不能删负收益或历史换取通过。只读汇总现有十策略真实公开报价账户／报告，不新建其成交、不改计划／资金／持仓，不把三份旧shadow当十策略实时执行；网页自动读main，不重部署或建新定时器。

只提交本轮目录及registry／两独立pointer／monitor两个共享文件，全部直接main非强制push。封存后不写回报告添加commitSHA。完整main commit/push/fetch/独立ls-remote、全递归tree／必要blob SHA、原singleS28与独立L4完整观察链、真实publisher退出0与解锁后核验在 `.git/automation_proofs/20261101T034816Z.json`，不会提前把发布记为成功。
