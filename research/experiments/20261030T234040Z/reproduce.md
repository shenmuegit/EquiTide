# 复现与只读核验

固定/home/desktop/Documents/Codex/EquiTide，main only、同branch.lock排他锁。解释器/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python，环境PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1；runtime.json含版本。

实际顺序：bootstrap完整读登记/历史→freeze6→initial过去信号/同价/固定检查锚点/第二腿拒单付费撤销边界检查及代码绑定→reserve6成功→evaluate一次18成本场景（36银行+18联合全路径）→audit独立分数排名/Decimal现金流/完整净值/原长持SHA→summary六CSV/六面板→exports逐数值和LF检查→finish6。全部实际命令/退出/log在all_command_receipts，冻结实际退出在freeze_execution。金融配置已有真实结果，不重复reserve/evaluate或调用旧控制策略simulate。

只读核验：

```sh
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T234040Z/audit.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T234040Z/check_exports.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T234040Z/forward.py --reproduce
```

真实8Parquet、16源输入、3旧长持spec/report/archive、原生资金与成交代码SHA均在manifest，缺输入停止不合成。六个新排名联合模型独立登记，L7/14/28×R7/14、总20000/raw[1,1]/每腿N2000、UTC00:01执行、同向不resize、双腿成本/拒单付费撤销/只平仓恢复/终止平仓全部冻结。旧长持同本金和初始gross而符号/换手/后续gross不同，保留原资格。

独审不调用新rank/simulate或core.trade：Fraction重算6660逐日决策/720排名，Decimal重建新模型及旧只读对照876fill/46620fund/419892小时风险状态，新54曲线29430702点和414联合整体/逐月/近期指标；3旧父净值精确SHA。六CSV全部行核对并显式LF，图已实际查看。复用开发历史/多重选择/无DSR或独立未来证据保留，6候选全部淘汰。

原SMA/singleS28分别reserve/finish20:30至22:30实际窗口，0新日决策/成交/资金费；保留41699/5798点完整连续账户，候选累计144ID，原账户规则、现金、q/entry不改；8公共HTTP200。下一窗22:30至Oct31UTC00:30跨资金费和日决策，须读next_research_state中真实原跨日驱动/65日上下文，不复制本轮mark-only断言或假设零事件。

随后实际registry检查、同锁python3 snapshot.py/monitor_snapshot.py及旧网页每行完全比较。共12新完成ID/24追加事件，paper10只读。共享状态未来可正常推进，以本轮candidate_current_pointer与manifest复核，不回滚。所有负收益保留，仅不保存可重建大数组，不重部署网页或新建任务。

publish.py只提交本轮目录与4共享文件，SSH非force推main，fetch/独立lsremote/完整tree和全部必要blob核验，发布进程实际exit0后再解锁。实际SHA/进程/解锁在.git/automation_proofs/20261030T234040Z.json。
