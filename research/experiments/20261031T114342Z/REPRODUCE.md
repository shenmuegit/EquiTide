# 复现与证据核验

固定工作目录 `/home/desktop/Documents/Codex/EquiTide`，Python `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python`，环境 `PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`。8个原始真实市场Parquet及16份旧原始输入在忽略的data中，精确SHA/字节数见data_manifest；轻量账户原始响应副本见raw_evidence_index。缺真实输入时记录blocked，不生成价格。

本轮实际命令顺序及stdout：bootstrap、freeze、initial（一次合成预检失败）、initial_retry1、reserve_batch_0/1、evaluate、audit、decision_check、summary、exports、finish_batch_0/1、finish、forward、candidate、observer_status、review、gates、feed。`*_commands.json`和`*_receipt.json`记录真实命令与退出码；financial全部reserve成功先于首次evaluation_started_utc。失败日志保持。

已完成同具体配置不得再reserve或真实回测。只读重核可执行：

```sh
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261031T114342Z/audit.py
PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261031T114342Z/check_decisions.py
```

这些审计从已保存状态段／真实价格独立复核信号和会计，不产生新策略订单或新账户观察。会重写本轮可重建verification文件；已封存Git工作树中先只读比较其输出，不重写冻结spec/report/registry。完整新报告16配置/48场景，旧中心只读6场景，独立标记；8CSV包含逐折、全部变体和连续dailyNAV。每档545013点完整净值的SHA及必要状态段见results，每笔真实模型成交、funding、费用和margin可独立恢复，无需提交大数组。

原冻结SMA和singleS28仅续接新闭合分钟／小时／实际funding，不重跑既成窗口。`forward.py --reproduce`仅离线复核同次输入；不要再次执行reserve/finish/observe_candidate.py。十策略账户和所有旧报告均在protected_inputs中逐字节保护。main发布程序在同flock内非强推，最终commit/tree/所有必要remote blob SHA/实际publisher退出与解锁证明留在`.git/automation_proofs/20261031T114342Z.json`。
