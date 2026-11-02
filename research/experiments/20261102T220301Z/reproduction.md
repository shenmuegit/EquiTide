# 复现命令与边界

固定workdir=/home/desktop/Documents/Codex/EquiTide，main；所有登记/结果/监控/Git写操作持有branch.lock。运行时/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B，环境PYTHONDONTWRITEBYTECODE=1、OPENBLAS_NUM_THREADS=1、OMP_NUM_THREADS=1。各commands.json与日志保留实际cmd/cwd/开始结束/exit/stdout/stderr；plan/data_manifest保留输入版本、闭合边界和SHA256。

本轮文件前缀research/experiments/20261102T220301Z/，实际流程如下：

1. bootstrap.py读取完整registry主簿/所有片段、280历史结论、task/三技能/README、freqtrade JSON/ZIP、checks/*oos.py，核验初始16实际证据和旧源/账本。
2. check_asymmetric.py --legacy-slow-range为旧S28范围预期红灯，实际exit1单独保存。commands.py freeze保存12spec及全规则、L3/4/5×S24/28/32、数据时界和固定失败判据。commands.py initial完成144策略fixture、18准确S滞后/慢ROC等号flat、18旧行/邻域、S32首i33有33close可执行及不足33拒绝，绑定全部必要代码。
3. commands.py reserve_batch_0、reserve_batch_1共12项实际reserve成功后，commands.py evaluate计算6原生和6组合/36成本场景；S28实际旧曲线、BTC和同银行持有控制只读，不精确重跑完成配置。
4. commands.py audit独立Fraction/Decimal审核；summary只读导出。audit成功后counts、decisions，summary成功后grid、exports。包含13逐月/尾折、8近期折、每日NAV、全曲线DD、Sharpe/Calmar与两轴敏感性/边界/悬崖。只读比较以前已执行的参数网格hash/收益/DD不另跑策略。
5. 观察登记串行：forward延续原SMA18:30→20:30（预登记、实算、独立审计、finish、离线精确重放）；candidate续原singleS28同窗口；l4h02续原未过滤L4/H2的20:10→22:10，仅22:11参考闭合后采集。原cash/q/desired/risk/context和NAV链不变，Nov2_00/08/16资金费不重复。此次无新日决策/预计结算，仍审核真实完整响应。
6. finish_batch_0、finish_batch_1、finish分别逐项完成12实际结果，包括全部淘汰与负收益期间；observer_status只读；review核验21新ID/42追加事件、旧源、精确ledger前缀和绑定代码。
7. gates实际执行python3 checks/strategy_registry.py、research/monitor/snapshot.py、checks/monitor_snapshot.py；feed核对12新增行/36场景与全部旧展示完整字典；collect保存原始短窗响应/packet、账本和必要下轮状态。监控不新回测/成交，失败恢复旧有效汇总。
8. 实际view_image检查sensitivity.png；仅清可重建缓存，保留完整实际结果/规则/登记/账本。finalize.py直接核验并封存；publish.py publish仅stage本轮和五个必要共享文件，commit、SSH非强制push main、fetch/独立ls-remote/全tree与必要远端blob SHA核验。真实exit0后记录私有回执、释放仅本轮broker再复查。

完成轮次只读核验，不覆盖封存文件、不重复reserve/计算、不补下过去报价订单、不新建分支/worktree。下一L4窗口22:10→Nov3UTC00:10跨新的午夜资金费及00:01原规则决策，必须按新实际settlement/daily数据审核，不能复制当前零日事件假设，也不能把Nov2已记资金费当成Nov3已记；本轮不预先登记或计算未来窗口。
