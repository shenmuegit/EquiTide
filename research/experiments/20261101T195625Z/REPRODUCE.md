# 本轮执行与复核

固定cwd `/home/desktop/Documents/Codex/EquiTide`，main唯一分支；基准`79b422081f99402b9237a0bc77a9f8c4530f6941`。先核对git rev-parse根目录/AGENTS/task，不切换其他工作区，不读取凭据。解释器`/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python`仅使用现有环境，所有命令cwd始终为固定仓库；runtime.json保存实际版本、Decimal28及单线程设置，没有安装依赖。

完整历史25252事件/12504ID、267份结论、原始freqtrade ZIP/JSON与checks/*oos.py读取与初始16证据在context.json；8个真实Parquet/16个来源输入哈希及完整账户链在data_manifest.json。大行情留忽略data，Git仅保存结果、必要逐笔/funding/状态段、哈希及本窗真实轻量响应。

经济规则：固定简单收益残差x=rETH_L−A*rBTC_L，L3/4/5，A0/.5/1；A0规则等价旧配置只读。A.5/A1共6原生+6父，全部独立reserve成功后实际运行：

```sh
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261101T195625Z/commands.py evaluate
```

这是已执行命令，不在当前已完成ID上重跑。12配置36场景均finish rejected，实际reserve/finish回执分别在reserve_batches与finish_batches。金融report原SHA `74f236ccc7caaccd5a059bfad0d9df987106de7b21703f105f5597929c22dd5e`，所有负收益期间同样保留，未修改门槛或添加额外参数。

固定ETH slow28/H2.5%/exit0.25%/V10cap4.5%，对x做严格入场及缓冲退出。A只改变信号，既非资金权重亦非BTC对冲订单；BTC/ETH银行3750/15000、初始N375/4500、原权重[1,1]不归一化；美元NAV相加，无父调仓/转账/跨抵押/NAV缩放。ETH真实波动量价输入仍用于成本，未用较小残差波动折减冲击。两币完整分钟open轴/daily closes索引相同，两币真实available最大值早于下一00:01执行。

以下仅从真实行情与已存必要状态/成交/funding独立核验，无simulate/decide/trade调用，不写登记或账户，不做新策略试验：

```sh
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261101T195625Z/audit.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261101T195625Z/check_decisions.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261101T195625Z/check_grid_diagnostics.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261101T195625Z/check_exports.py
```

命令可能重写相同核验输出；日常只读本轮已封存回执。计数在research_evidence_counts分开：新18原生成本曲线19980funding、690成交；只读旧18曲线19980funding、618成交。父引用同源操作不作额外成交。各命令cwd/时间/stdout/stderr/实际exit记录在phase_commands.json及logs，全CSV与八面图为实际结果。

固定370日按12完整月加10日尾段持续核算，不重开账户；近期40日继承day330/8×5日折。重复开发历史不称未触碰最终OOS，固定系数不拟合，purge0、预热30+间隔3。完整全曲线DD、逐折/逐变体Sharpe/Calmar、1/2/3倍费用价差滑点规模冲击/真实funding、LOT/参与率/抵押/小时维护代理及匹配持有和现金对照均留档；没有TCA/L2、完整历史档位/逐tick清算/容量或实盘盈利证明。

冻结账户：原SMA65/singleS28从16:30至18:30；独立未过滤L4/H2从18:10至20:10且20:11参考闭合后才采集。全部继承cash/q/desired/risk/NAV，已计16funding不重记，不注入A，不因partial rejected取消原180日计划，不从现金重开或强制截止平仓，未下真实订单。

```sh
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261101T195625Z/audit_forward.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261101T195625Z/audit_candidate.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261101T195625Z/audit_l4h02.py
```

以后指针继续前进后，针对本轮末指针的assert将按设计失败，不可回退指针或重跑已完成观察；使用本轮审计回执及完整链核验。SMA源输入旧1d/1m字典和本轮minute数组结构都保留，原65日上下文路径在nextstate。

同锁内实际执行python3 checks/strategy_registry.py、python3 research/monitor/snapshot.py、python3 checks/monitor_snapshot.py及全部旧行字典核验；监控只读既有账户/报告，不产生成交、不改paper10原冻结计划/本金/持仓，不重部署或创建重复定时任务。保存真实HTTP尝试/成功或失败响应及stderr，不造未知尝试数。清理仅可重建查重材料，原SHA/字节/复现依据在cleanup_verification；金融结果、完整账户账本/冻结规则不删。

发布与解锁在封存后执行；真实main SHA、非强制push、完整远端tree/必要blob核验及进程终态在`.git/automation_proofs/20261101T195625Z.json`，不在提交前预写成功。
