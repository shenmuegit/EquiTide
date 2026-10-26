# 原候选独立新数据观察器

冻结依据为 `research/experiments/20261026T090537Z/candidate_prospective_plan.json`。候选仍是 070542 的 BTC ROC31/入场4%/退出1%/N1000，加 ETH S28/L3/入场2%/过零退出/N3000；两个完整10000 USDT银行，原值乘数1/1、父本金20000，总固定入场4000。当前 BTC 入场2%的研究结果不替换这个选择。

计划2026-10-27 UTC00:01开始，2027-04-25 UTC00:01终止，共180日。当前仅完成执行器和工程校验，未创建该候选的账户、窗口登记、模拟成交或收益。`status` 只读、不HTTP、不写登记；计划开始前 `run` 在下载/建账户/登记前失败。观察模式是预先冻结的新数据延迟闭合bar/结算重建，并非实时盘口报价模拟，更非真实交易或paper10。

`prospective_core.py` 复用并固定原原生信号/Decimal成本函数的SHA。`prospective_observer.py` 提供公开数据分页捕获、输入验证、三配置逐项reserve、增量状态/账本/NAV保存、finish及原子状态指针。每天只以此前完整1m聚合日线决定，00:01 OPEN为实际参考；资金费按当时持仓和真实结算mark/费率计入，流出随成本放大，流入不放大。手续费/半价差/滑点/成交量冲击、参与率、lot/tick/最小金额、保证金代理均沿冻结规则。资金费安全比按原历史门槛的1x口径，其他三档净正及3x回撤门槛不变。

所有窗口传递实际现金、数量、入场价、费用/资金费、未完小时的持仓分段、日线完整/未完整上下文及NAV哈希链。跨窗口核对分钟、执行参考、小时和资金费重叠，缺闭合bar、缺结算、时间单位错误、元数据改变或来源SHA改变均阻止计算，不修改冻结规则。整点资金费的毫秒偏移保留；00:00结算先于00:01决策。父NAV逐点加两个独立银行，不平均收益或重设现金。不在观察截止或折边界平仓；只在180日终点强制计成本退出。小时不利mark/1%维持保证金仅为代理，缺L2/队列/历史阶梯的限制继续披露。

工程检查使用人工构造的输入验证转移和捕获适配器；未把人工数据当策略回测。另以原候选六个保存的成本账本只读回放实际成交/资金费现金链，未重跑历史信号/撮合/资金费模型。公开只读预检实际读取exchangeInfo/time及两币资金费字段，原始HTTP响应和SHA保留；首个真实窗口仍须重新下载、核对元数据及全部实际数据，今天的工程通过不证明未来接口/数据可用或策略盈利。

后续沿现有btc-eth自动任务调用，不新建定时器或分支。在 `/home/desktop/Documents/Codex/EquiTide`、已验证main、持有同一个branch.lock的外层broker期间，使用金融环境执行：

```bash
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261026T110637Z/prospective_observer.py status
```

首个可用窗口需先创建该轮UTC实验目录，然后以该轮真实已闭合截止和外层锁PID执行 `prospective_observer.py run --round <UTC轮次> --cutoff <真实UTC截止> --lock-pid <持锁PID>`。运行保存于该轮 `candidate_observation/`，大原始页/packet位于忽略data。每窗3项观察（BTC/ETH/COMBO）均先reserve；各spec包含实际新输入SHA、未来起止、原计划及前态SHA。`forward_snapshot_candidate_*`名称保持观察归类，不把周期截止当新增策略试验。

首次真实成功后才创建 `research/automation/candidate_forward_latest.json`。后续轮次将该共享指针、本轮完整state/report/delta/complete/spec/receipts及登记和监控对一起提交推送。指针只存前态指针文件的路径/SHA，避免深层递归文件增长；全历史完整账本/独立窗口delta不可清理。汇总六个30日折和近期40日诊断时继承原状态、使用整条NAV计算回撤。前180日实际部分观察finish rejected仅表示证据未成熟，绝不取消/重置计划。

下载或验证失败保存failure/raw/实际错误，尚未产生真实计算结果的已reserve项finish blocked；前态指针不前移。若实际结果与complete已经保存而finish/指针更新中断，不将有结果项改为无结果：保留完整文件，下一轮先核对complete的state/report/delta SHA、前态指针SHA和三项登记，按已保存报告补finish仅仍reserved的项，再原子补指针。禁止重新计算该窗口或从现金重开。有candidate登记却无指针时执行器主动阻止自动重开；需要上述明确恢复。输入/磁盘中断留下的不完整窗口同样先审查失败记录，不覆盖。

官方接口字段依据：[Binance USDⓈ-M市场数据文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)，访问2026-10-26，资金费历史含实际fundingTime/fundingRate及对应markPrice。文档及预检不是未来绩效证据。
