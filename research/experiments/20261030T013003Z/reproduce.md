# 复现与只读核验

固定目录 `/home/desktop/Documents/Codex/EquiTide`，解释器 `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python`，环境 `PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`。L2/3/4×S27/28/29完整价格网格18格，L3/S28的2旧中心只读复用；16新金融配置逐份保存完整spec、成功reserve后实际评估48成本场景、分别finish rejected。另6原冻结观察分别reserve/finish，共22新ID/44追加事件。已完成精确配置不可在正式登记重复回测、改名重开或改原账户规则/本金。

所有真实复现调用、stdout/stderr、实际退出见all_command_receipts.json、reserve_batches/finish_batches；bootstrap_receipt另存完整登记和234结论读取证明。没有无效金融运行或配置重试；初始等待锁broker中断与公共GET一次TLS35内部重试均保留真实事实，不当作金融回测。原rawresponse_SHA/4SMA响应/8候选响应与packet已绑定，不编造未记录的失败子请求。

真实8合并Parquet与16原始/近期来源、所有旧spec/report/archive、冻结源代码与账户哈希见data_manifest。大行情与候选公共HTTP原始响应留ignoreddata，SMA4个小原响应留本轮gzip。缺真实匹配输入必须停止，不合成。资金费特征使用1212条完整历史、available_ts/settlement_ts均≤信号，1110条OOS结算仅作现金入账。5旧原生银行15曲线只读账本恢复，BTC5000银行固定N500，8新ETH15000银行固定N4500，raw[1,1]真实完整净值相加；不得再次乘25/75或缩放旧数量冒充新执行。

封存版本只读审计既有账本与导出（不产生新策略结果或账户交易）：

```sh
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T013003Z/audit.py
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T013003Z/check_exports.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T013003Z/forward.py --reproduce
```

独审以整数/有理数重建信号、Decimal重算成交/资金费/保证金与全部NAV，组合按(ns,eventcode)对齐，不调用simulate/target/trade。后续共享账户正常推进后，应读取本轮提交blob、保存pointer和完整账本，保护哈希变化不能成为回滚main/账户的理由。旧中心原正式资格和新价格网格诊断分开，offcenter与固定未过滤中心对比不是匹配过滤因果实验；不声称未触碰最终留出、独立未来或实盘稳定盈利。2图12面板实际打开并留证，全部正负回测保留。

原singleS28/SMA65从22:30跨UTC00资金费与00:01日决策至00:30已核验，规则不变。下轮00:30→02:30仅闭合mark；singleS28当前00时入账前/后同时间状态，前者零时长，下一闭合小时不得重复风险检查前者。不得重复贷记Oct30UTC00资金费，不把两旧延迟shadow当十策略实时模拟；只读monitor只汇总已有报告与账户。
