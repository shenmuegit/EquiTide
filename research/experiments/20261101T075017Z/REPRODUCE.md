# 复现与实际证据

固定工作目录 /home/desktop/Documents/Codex/EquiTide；Python /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python，环境PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1。执行前核验root/main，普通SSH fetch及独立ls-remote，保留07UTC paper提交和预存data/normalized。branch.lock由PID793945持续持有到非强制push及完整远端验证结束，不创建其他分支或worktree。

真实命令／终态退出码保存在 *_commands.json、*_receipt.json。顺序：bootstrap全读24900登记事件、12328ID、261结论／初始16原证据／freqtrade ZIP及checks/*oos；freeze固定规则／数据／门槛及spec；initial检查并绑定源；reserve_batch_0八次实际成功才evaluate；audit独立复核；summary/check_decisions/check_grid_diagnostics/exports与实际看图；finish_batch_0八项独立finish、finish验证；原forward/candidate与独立l4h02；observer_status/review；gates精确运行python3 checks/strategy_registry.py、python3 research/monitor/snapshot.py、python3 checks/monitor_snapshot.py；feed逐旧行；collect；seal；publish。不能以文件出现替代工具真实退出0。

固定银行轴BTC3750/5000/6250和H2/2.5/3%，ETH15000/N4500、L4/S28/E0.25%、V10样本logvolcap4.5不变。原始子权重[1,1]为完整原生银行所有权，总C0=18750/20000/21250，BTC初始份额20%/25%/29.4118%；实际BTCN375/500/625，ETHN4500。原数量LOT/tick／费／规模冲击／funding/cash路径各自已有真实结果，不放大较小银行净值，不同步复制同币订单，不重复乘资本权重或做免费调仓／转账／交叉抵押。新6候选＋2匹配持有父，共8定义／24成本场景；3旧中心候选＋1旧中心hold及10原生组件共14唯一来源只读复用，0原生重测。新hold也是实际新组合，先reserve再算、独立finish，负收益完整保留；角色benchmark不算候选通过。

真实连续370日2025-10-19 UTC00:01至2026-10-24 UTC00:01，12完整30日折＋10日尾折，不重开cash/q/entry/成本；近期40日继承day330、8×5日折。信号prior完整close，下一UTC00:01原生OPEN不利tick，q=floor(N/priorclose/LOT)×LOT，同向真实q不变，反向先平后开，终止付费平仓。固定规则无拟合／标签，purge0、30日预热与3日间隔；past20完整日quoteADV/logvol成本。重复历史只作开发验证，无未触碰最终留出或DSR/PBO证明。

每边5bp手续费＋1bp半价差＋2bp滑点＋0.5×past20logvol×sqrt(actualq×OPEN/past20quoteADV)，1/2/3倍压力；真实纳秒/rate/mark/当时q资金费，支出加压、正收入不放大。线性永续无现货借币，未虚构借币费；LOT/tick/minnotional、参与率<=.001、费用后1倍抵押与独立1%闭合小时不利mark维护代理。缺L2/TCA、完整历史档位和逐tick清算／实盘容量证明。所有新整体净值由各原生美元路径共同轴相加，完整DD/Sharpe/Calmar重新计算，不平均单策略指标。

独立audit恢复30旧原生成本曲线，Decimal逐笔核验并检查420次原生开仓N/LOT/lag，33300资金费、840成交、756整体／月指标、214764小时风险状态；24新父13080312完整NAV点及全部近期折独立复核。check_decisions和grid诊断在当前计算前固定，所有门槛和旧canonical资格保持。10CSV保存24新场景、月折／近期／连续日NAV、9格点／相邻边、同银行同预算常多hold/cash、30来源场景与12份分配；该hold非满仓或同风险基准。图表实际打开核验，边界／描述性悬崖和多重选择限制保留。

4新候选达到本批历史门槛、H3%的2候选失败，2新hold真实负收益按benchmark保存。通过仅当前有限邻域历史证据，最大Sharpe仍位于BTC3750/H2.5边界，不能声称全域最优或稳定实盘盈利。原组件账本／报告及8真实Parquet、16年／近期输入SHA保持，重建全NAV只在内存，不保存可重建大npy。

原SMA65以旧1500/500和Floatcash/units/desired/trades/cost从04:30续06:30：forward_registry reserve→forward.py→audit_forward→finish→--reproduce离线核验；只加120闭合mark，原43501NAV至43621点／43589分钟，不产生新日决策／成交。65daily上下文仍20261101T014820Z/forward_inputs.json.gz，当前分钟数组独立保存，兼容字典1d/1m或数组，nextdailyNov2UTC00:01才更新。

原singleS28沿用20261026T110637Z原core/observer和原plan，10000/10000、N1000/3000、ETHL3，续04:30至06:30。独立未过滤L4/H2沿用20261031T174613Z/prospective_l4原plan/core/observer/binding，5000/15000、N500/4500，续06:10至08:10；08:11参考分钟闭合后才capture，本窗跨08资金费，精确核对实际ns/rate/mark/heldq/成本档现金流并只入账一次。两套pointer／登记链／账本分开，不继承彼此现金，不用本轮bankmix替换冻结规则。各截止3reserve后advance/finish，部分rejected不取消180日计划，不强制每轮平仓，短观察年化指标不解释为盈利能力。

账户audit仅复用冻结normalize做闭合数据／事件组装，独立核验Fraction方向、Decimal数量／费／impact／fund/cash、正持续时间风险段、完整旧NAV前缀／新全NAV链／日边界／部分资格，不调用原target/trade/transition/advance重算窗口。所有HTTP尝试、成功与失败raw/packet/stderr及有界重试记录保持TLS校验；原始响应与新窗口轻量证据复制入Git、逐个SHA和字节核验。年度行情和首窗33日大预热留忽略data，不删除账户／规则／登记／结果核验必要证据。

同一main锁内生成只读monitor，沿用上轮已经验证的5MB门禁，不改网页／监控代码／预算，不重新部署或新增定时任务，不改十策略计划／资本／持仓或创建新模拟成交。全部旧展示行和每个新场景报告SHA／资格／成本／NAVhash逐项对照，失败先恢复上次有效汇总并留档。三份延迟shadow不充当十策略实时公开报价执行，不下真实订单。

仅提交当前轮证据与registry／两独立pointer／monitor两个共享文件。封存后不重写报告追加自身commit；普通SSH非强制推main，完整tree／必要blob SHA、原singleS28和独立L4全链、publisher真实退出0和释放锁后核验存.git/automation_proofs/20261101T075017Z.json，不在实际成功前预写push状态。

发布辅助脚本曾重复准备同一解锁后校验文件，not-exists保护触发一次真实exit1；确认已存文件与期望字节一致后复用，未重写既有证明，未改模型／账户／报告／登记，无完成模型或观察重跑。失败及恢复在pre_publication_engineering_failure和execution_exit_verification中留档。
