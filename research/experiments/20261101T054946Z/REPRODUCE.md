# 复现及真实执行证据

固定工作目录 `/home/desktop/Documents/Codex/EquiTide`，Python `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python`，环境 `PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`。启动前核验root/main、普通SSH fetch和独立ls-remote；base为f10fb9cb的05UTC paper提交，上轮已推送，预存data/normalized保持。共用branch.lock PID761242持续持有到非强制push与完整远端校验，不建分支／工作树。

实际命令／退出码在 *_commands.json、*_receipt.json：bootstrap完整读登记及260结论；freeze.py初次family大写错误，freeze_recovered.py准确复用旧基准后预期计数错，原源／失败回执保持；freeze_final.py只修正格式／计数，6候选数值规则不变，实际冻结6新候选／0新基准／0新组件。initial成功绑定代码 → reserve_batch_0六项实际成功 → evaluate → audit → summary → check_decisions/check_grid_diagnostics → exports → finish_batch_0/finish → forward → candidate → l4h02 → observer_status/review → gates → feed → collect → seal → publish。报告源码生成器一次字符串转义错误在写入前被AST拒绝，literal源码AST修复不涉及策略；真实失败单独留档，非金融失败结果。所有步骤等实际工具终态退出，不以文件出现代替成功。

预定BTC银行5000/10000/15000×ETH H2/2.5/3%，固定ETH15000/N4500、L4/S28/E0.25%、V10样本logvolcap4.5%。原生BTC预算500/1000/1500、实际q/LOT/tick/费用／冲击／funding均为已真实执行的对应规模路径；不线性放大小银行净值，不同步克隆同币订单。父原始权重[1,1]保留，美元净值直接相加，总C0=20000/25000/30000，初始资金BTC25%/40%/50%；无归一化、转账、重复加权、免费再平衡或跨抵押。3旧候选、3匹配银行／预算持有父和10原生组件只读复用，16唯一实际来源。6个全新父各先成功reserve，再计算18成本场景；没有组件策略／基准重跑。constantlong基准非满仓或等风险比较，现金0%另列。

真实370日2025-10-19 UTC00:01至2026-10-24 UTC00:01，12完整30日折＋10日尾折，状态／成本／funding跨折连续；近期40日继承day330，8×5日折。无拟合／标签、purge0、30日预热／3日间隔；prior完整close信号，下一00:01原生OPEN不利tick，成本只用past20完整日quoteADV/logvol。1/2/3倍费5bp／半价差1bp／滑点2bp／0.5sigma√(actualq×OPEN/ADV)冲击；实际资金费支出加压、正收入不放大。原生参与率<=.001、费用后1倍抵押、LOT/tick/minnotional和独立银行1%闭合小时不利mark维护代理。无L2/TCA、完整档位／逐tick清算／实盘容量证明。

独立审计从真实原归档恢复30旧原生成本曲线，Decimal逐笔核验cash/q/fund/fee/impact/hourrisk，并重新验证每个原生开仓quantity=floor(originalN/priorclose/LOT)和信号可得时间；新18父曲线完整NAV／月折／近期指标重算，不调用原simulate/target/trade。独立check_decisions与check_grid_diagnostics在见本轮结果前固定，所有门槛保持，旧3格点canonicalstatus/criteria/sensitivity不重写。10CSV保留全部18新场景、逐月／近期／连续日NAV、9格点／相邻边、匹配hold/cash、30旧原生来源和12资金分配，图表实际查看。历史反复研究仅开发验证，不称最终留出或稳定实盘盈利；全格点正Sharpe、边界／悬崖和多重选择局限均披露。

原SMA65按旧1500/500 Floatcash/units/desired/trades/cost续02:30至04:30；forward_registry reserve → forward.py → audit_forward → finish → --reproduce离线核验，原NAV前缀＋120已闭合mark，不重开现金／日决策。最新65dailycontext仍20261101T014820Z/forward_inputs.json.gz，当前分钟数组分开保留，兼容字典1d/1m或数组；Nov2UTC00:01前无新日决策。

原singleS28沿用20261026T110637Z core/observer及原plan，10000/10000、N1000/3000、ETHL3，续02:30至04:30。独立未过滤L4/H2沿用20261031T174613Z/prospective_l4原plan/core/observer/binding，5000/15000、N500/4500，续04:10至06:10，参考分钟06:11闭合后才capture。原规则、资金、q、风险／已入账funding和完整NAV前缀延续；新历史bankmix不改冻结账户。两专属pointer／全链独立计数，新截止各3reserve再advance/finish，不重跑完成窗，不强制每轮平仓，不把partialrejected当取消180日计划。只读账户audit只复用normalize做数据／事件组装，独立信号／Decimal账本／正持续时间风险和完整NAV链，不调用target/trade/advance。部分年化指标不解释为收益能力，三shadow不混入十策略真实公开报价。

当前2小时原始HTTP尝试／packet、SMA2页轻量raw复制并存SHA／字节；年度行情和首窗33日预热留在忽略data，完整账本／规则／登记／核验源保留，无大npy/pyc/tmp/checkpoint。公共GET保留TLS与有界重试，失败尝试／stderr／raw及所有恢复按真实情况留档。

同锁精确执行python3 checks/strategy_registry.py、python3 research/monitor/snapshot.py、python3 checks/monitor_snapshot.py；feed逐旧行及新报告／资格／成本／NAVhash比较。生成失败先恢复上次有效汇总，实际失败记录后只做必要非金融修复并重新验证；不删历史／负收益，不改冻结规则／资本／持仓，不新增十策略成交，不重新部署或设定时任务。若发生展示体积门禁修复，原checker/README字节和上次有效汇总SHA保留，完整旧行不变，修复回执详列，不把它充作策略通过。

只提交本轮及实际修改的共享registry／两pointer／monitor文件和必要非金融门禁文档；不提交凭据或大行情。封存后不写回报告追加自身SHA；普通SSH非强制推main，完整远端递归tree及必要blob SHA、原singleS28与独立L4全链、publisher实际终态退出0、解锁后核验在.git/automation_proofs/20261101T054946Z.json。发布前不预写成功commit或push状态。
