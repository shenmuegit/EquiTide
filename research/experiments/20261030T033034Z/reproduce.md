# 复现与只读核验

固定目录 `/home/desktop/Documents/Codex/EquiTide`，解释器 `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python`，环境 `PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`。ETH顺势L20/25/30×H2/4/6%、退出缓冲1%，5000/15000实际银行、固定名义500/1500，原值raw[1,1]。20金融定义含18候选与2同名义常持，均逐份完整spec先成功reserve后真实计算60成本场景，再分别finish；另6原冻结观察各reserve/finish，共26新ID/52追加事件。已完成配置不再正式回测/改名重开，不改原账户本金和冻结规则。

完整调用、stdout/stderr和实际退出见all_command_receipts.json、reserve_batches/finish_batches；bootstrap_receipt记录完整登记和235结论读取。engine.py/btc_engine.py均为此前验证过的BTC动量核算原字节，ETH换真实数据/元数据/新规模，模拟实际lot/tick/冲击/资金费/抵押，未缩放旧N4500模型。两个constant_long_reference的signal_mode优先于通用动量公式，L/H/E=0未使用；首次决策开多、固定原生数量不再平衡、终止计成本退出，完整解释见计算前spec_clarification。

真实8合并Parquet、16原始/近期来源与所有源spec/report/archive/原响应/冻结代码SHA见data_manifest。大行情/公共响应留ignoreddata并保留哈希，不缺数据合成。本轮资金费只对实际持仓作1110条OOS结算，不作入场特征；1212条原始历史完整绑定。旧反转N4500基准的方向/规模/退出/筛选均不同，不是匹配因果对照；新常持N1500及其父组合实际重算。

封存版只读审计已有账本/导出（不产生新策略结果或账户交易）：

```sh
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T033034Z/audit.py
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T033034Z/check_exports.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T033034Z/forward.py --reproduce
```

独审以整数/有理数重建严格入场与持仓退出信号、Decimal重算成交/资金费/风险与完整NAV，组合按(ns,eventcode)对齐，不调用simulate/target/trade。未来共享账户正常推进后，应读取本轮提交blob、保存pointer与全账本，不回滚main/账户。重复历史不是未触碰最终留出；2012作者论文仅是概念启发，其12个月/非加密证据不能代替ETH实际验证。无独立未来、TCA或稳定实盘盈利证明。

原SMA65/singleS28只续00:30→02:30；singleS28 UTC00资金费后的原cash/units/entry保持，00时入账前状态零时长已在闭合小时检查排除，02时单一状态继续带入后窗。不重复贷记旧资金费、不采用新趋势参数，不把旧延迟shadow当十策略实时盘。只读monitor只汇总已有账户与报告，无新回测/成交/重部署。
