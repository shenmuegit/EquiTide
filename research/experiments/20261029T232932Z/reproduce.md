# 复现与只读核验

固定目录 `/home/desktop/Documents/Codex/EquiTide`，解释器 `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python`，环境 `PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`。42金融配置各保存完整spec并先成功reserve，21原生执行与21父组合各实际评估一次，再分别finish；另6原冻结账户观察独立reserve/finish，共48新ID、96追加事件。已完成精确配置只读结果，不在正式登记中重复回测、重开账户或改本金/冻结规则。

完整复现调用、每批实际reserve/finish及实际退出见all_command_receipts.json、reserve_batches和finish_batches。initial freeze的旧hold缺未使用字段、过早reserve找不到batch在成功冻结/42有效预约之前发生，无实际金融结果。保留failed freeze代码、草稿哈希与失败日志；unusedL/H/E显式填写后从头冻结，未发生已登记金融配置重试。所有实际正负结果完整保留，不把工程通过当金融passed。

8合并真实Parquet、16原始/近期输入、所有源spec/report/archive与冻结源版本SHA见data_manifest。原行情/公共HTTP原响应留ignoreddata并绑定SHA，不提交大行情；缺真实匹配输入必须停止。资金费特征使用1212条完整历史、available_ts及settlement_ts均不晚于信号时点；1110条OOS资金费只用于实际现金入账。固定原始权重不归一化：实际父组合raw[1,1]相加两已分配资金银行；旧银行所有权对照raw[2w,2(1-w)]仅比较净值。各spec的capital_policy/entry_notional/source_component_parameters固定具体分支。

封存版本可只读核验已有账本（不产生新策略结果或账户成交）：

```sh
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261029T232932Z/audit.py
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261029T232932Z/check_execution.py
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261029T232932Z/check_exports.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261029T232932Z/forward.py --reproduce
```

审计独立重建信号、Decimal成交/资金费/保证金状态与全净值，按(ns,eventcode)组合，不调用simulate/target/trade。未来共享账户推进后，读取本轮提交blob、保存pointer和完整账本，不回滚账户或main。历史通过仅限预设资本/资金费网格，无独立未来或实盘盈利证明。只读monitor不产生模拟成交。下一轮跨UTC00资金费和00:01日决策，必须用原跨日observer与完整65/35日上下文，不能将当前mark-only续记直接越过日决策。
