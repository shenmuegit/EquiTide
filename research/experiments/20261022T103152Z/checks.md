固定工作目录、研究分支及共享排他锁均遵守用户要求。起点5e5b8c249cbf91d236b566c52a22802f25edc7ed与fetch远端一致，只有既有data软链接未跟踪。读取完整登记/片段10800事件、5296条登记、143份既往结论及现有freqtrade结果/OOS检查；初始16项均有真实结果，无待恢复登记。三个指定技能均已读取执行，没有委派子代理。

真实失败与恢复：第一次freeze因family ID误含大写CCI被schema拒绝，实际exit1，尚未reserve、计算收益或生成report。initial_commands.json、reserve.log及failures目录保留原始失败输出、源码、spec。仅将模板family改为小写，不修改共享校验器；family_id_correction.json记录前后源码SHA及原plan/context SHA。recover_reservations.py先重现拒绝、确认元数据外字段不变，再按既有冻结网格补齐18个spec并逐项reserve。恢复命令实际exit0，原冻结plan/context哈希不变；没有再次refreeze或先算后补登记。后续所有收益计算、审计及finish均在成功reserve后。

18个CCI配置完成54成本场景/648逐折结果，全部finish rejected。回看20/40/80日×入场50/100/150，退出0，0.015系数、N根完整HLC窗口、均值绝对偏差、零偏差CCI=0及严格入场边界预先固定。交易用未除法的分子/分母比较，显示CCI的Decimal28舍入不决定交易。每配置独立2000USDT，原始单资产资金占比1，不归一化。三个成本下各2配置净正，但无完整资格通过。

最佳ETH N40/E150为+4.669662%/+3.572474%/+2.486187%，仅3/12正折、4次往返，三倍连续OOS分钟回撤26.904038%，邻域盈利16.7%。18项均未过8正折和60%邻域，12项未过25%回撤，12项未过8往返，16项未过全成本净正及2.5毛参考盈亏/成本门槛。全部负收益、负折和正收益未合格结果保留，未放宽门槛或看结果后扩网格。18种完整三成本NAV路径不同，不代表独立市场样本。

数学自检包括N根窗口端点、恰好CCI100的严格边界、绝对偏差、零偏差状态、未来前缀、尺度/平移。独立验证用Fraction典型价/均值/绝对偏差重新计算，与生产Decimal分子分母之比精确一致，核对19440决策状态及时间。2920个日高低值通过独立NumPy分钟重排验证，690笔成交余额、54条本金锚定完整分钟回撤、648折及19494日净值点核验通过。真实四个Parquet的UTC纳秒、闭合/连续性、大小/SHA及日高低/收盘数组哈希保留。共享Decimal成交/成本引擎未改，未新增依赖；敏感性图已实际查看，两轴及18格对应原报告。

原冻结SMA从UTC08:00追加120闭合分钟至10:00，九场景完整29301点旧前缀保留至29421点，累计29399分钟/20完整天。0新增日决策、参考点和模拟成交，现金、数量、desired、交易及费用保持，BTC继续持仓、ETH继续现金；两份原始响应各121条（含重叠bar）及重放输入保留。forward.py/audit_forward.py与上轮源码字节相同；续接、独立审计和离线精确重放均实际exit0。3项部分观察finish rejected是因180天/六折未成熟，长期计划继续；下一原日决策仍为2026-10-23T00:01:00Z，不重复Oct22、不越界只mark。

final_gates.json五个实际进程全部exit0，stdout/stderr与原日志逐字一致，不以cat日志的退出码代替检查：

- `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261022T103152Z/forward.py --reproduce`
- `python3 checks/strategy_registry.py`
- `python3 research/monitor/snapshot.py`
- `python3 checks/monitor_snapshot.py`
- `git diff --check`

监控3793配置、10账户、91观察；18新配置/54成本场景的收益、整体分钟回撤、逐折收益、往返、NAV哈希及OOS边界与原报告逐项匹配。旧exclusive-end指纹537f5a8fc4b6e58511fabbde15096659e072be117d9a365d3827ac178134c70e仍可见。四个受保护输入等于本轮冻结前哈希；未来paper10状态可由独立任务合法推进，重放仍保护本次调用前后不变及全部冻结来源哈希。监控不产生账户观察或成交。

21个finish的report_sha256匹配原字节：研究a26af1184d43837f03ca0ba5474d19f3481e9bf310de7a4bf8c6e0ea579c0170；SMA5d3cd734c1b8cffd8f440bb82f46ca537ff8ea89bea2383c9871797cbccffa4e。核验后仅删除54个可重建checkpoint和本轮字节码，保留全部结果、源状态、完整净值、原始响应、冻结规则、账本、失败事实及下一轮输入；不迁移或重写已finish报告。大行情留忽略data并保留路径/SHA。仅提交本轮证据、登记和两份feed，普通SSH非强推后用fetch/ls-remote及完整tree核验，再释放新锁。

上一轮08:30收尾核验延至本轮开始，超过约90分钟预算，已如实保存在prior_round_closeout.json。旧提交4757c1dfc301b0745c834294c98c4c261d9a4c28已核验17436项完整tree及78产物/受保护输入，旧broker1218437确认退出并释放锁后才等待模拟盘完成，取得本轮新锁；没有重算旧18配置或改历史收益。此项延后原因未进一步核实，不把它写成回测或监控检查失败。

未下真实订单、重置账户、创建定时任务或重部署网页。反复使用的2025–2026历史不是最终未触碰留出，20完整天延迟shadow不证明180天资格、当时可成交或稳定实盘盈利。
