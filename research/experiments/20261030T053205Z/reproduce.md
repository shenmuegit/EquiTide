# 复现与只读核验

固定目录 `/home/desktop/Documents/Codex/EquiTide`，解释器 `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python`，环境 `PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`。事前3D a25/50/75%×较长L20/25/30×H2/4/6，原值[1,a,1−a]，BTC原5000银行1份、ETH反转原15000银行a份、ETH动量原15000银行1−a份；拥有初始资本总20000，权重不归一化。27候选+3同原值常持指数逐份完整spec先成功reserve，实际计算90场景，再分别finish。另6原冻结观察各reserve/finish，共36新ID/72追加事件。已有精确配置只读，不改名重开或改原账户本金/规则。

14原生银行42条真实成本曲线从完整账本重建；source已有原始整数数量、成本、资金费与风险，不重跑target/trade/simulate。新组合没有新增原生订单，不把分数所有权或缩放后的q当新金额成交。指数认购/赎回按NAV额外费假设0，无可交易基金/缩小金额执行/实盘容量证明。完整source spec/report/archive和路径SHA见plan/data_manifest，24旧结果原资格保留。8真实合并Parquet及16原始/近期来源、公共HTTP原响应留ignoreddata并绑定SHA；缺匹配真实输入停止，不合成。

实际调用/退出及stdout/stderr见all_command_receipts.json、reserve_batches/finish_batches；bootstrap_receipt记录全登记与236结论读取。金融源代码/参数/份额/时间边界/门槛在结果前绑定；无新原生模拟或金融重算。公共GET一次curl35失败和独立重试实际记录及空响应均保留，不能把终态成功说成没有失败。

只读审计已有源账本、每条新组合完整NAV与导出（不产生新回测或账户成交）：

```sh
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T053205Z/audit.py
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T053205Z/check_exports.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T053205Z/forward.py --reproduce
```

组合按完整(ns,eventcode)真实轴加净值，不平均Sharpe/收益，成本和现金份额乘原值、覆盖交易数统计引用银行事件，保证金不净额抵消。12×30日+10尾日和day330继承近期8×5日、整体连续NAV回撤均独立核对。后续共享账户正常推进后，读本轮commit blob与保存pointer/全账本，不回滚main或账户。历史通过限本轮a/较长L/H邻域；短反转L3/S28的先前参数脆弱性没有消失。原作者2012论文非本组合或ETH20日盈利证据；正收益指数不代表未来或实盘盈利。

原SMA65/singleS28只续02:30→04:30，0日决策/成交/资金费，UTC00入账后cash/entry/q保留；下一窗04:30→06:30在08资金费前仅加闭合mark，仍按真实packet检查资金费。保留04时风险状态，不重复UTC00贷记，不把旧延迟shadow当十策略实时盘。只读monitor只汇总已有证据，无新回测/虚拟成交/重部署。
