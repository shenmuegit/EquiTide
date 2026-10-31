# 独立 L4/H2% 未来验证

冻结开始为2026-11-01 UTC00:01，180日终止2027-04-30 UTC00:01。当前账户未创建、观察0、未来收益0条；工程检查和2220条历史决策身份检查不是新的金融结果，不得登记为新回测。沿用btc-eth定时线程，不新建定时器、网站部署或真实订单。

本协议固定旧L4/H2父候选：BTC5000USDT／N500、L31/H4%/退出缓冲1%；ETH15000／N4500、L4/H2%/S28/零退出，始终慢趋势门控真实仓位，无入场波动率上限。原始子乘数1/1，总本金20000，不归一化／转账／NAV调整／跨行抵押。plan.components中源logic与历史日期/input_hashes保留原来源证据；本协议具体金额、未来区间和策略参数由plan.rules_policy、initial_state_policy、components精确数值及binding/core断言共同固定，旧源示例范围不改变当前数值。

运行前读plan.json/binding.json并核验SHA。`observer.py status`完全只读；未到开始前`run`必须在创建目录、HTTP、账户或登记之前拒绝。实际未来窗口只在开始之后且所有分钟／小时／参考价闭合后运行，保存具体spec，逐BTC／ETH／组合reserve成功才advance；每次窗口全现金/q/entry/cost/funding/NAV链续接，不从现金重开、不重复首笔、不在中间截止强平。

新指针为research/automation/l4h02_forward_latest.json，窗口子目录l4h02_observation，与candidate_forward_latest.json及原SMA65/单S28/十策略完全隔离。调用示例在未来真实窗口可用后：解释器`/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python`，脚本`research/experiments/20261031T174613Z/prospective_l4/observer.py run --round <当轮UTC目录> --cutoff <闭合分钟UTC> --lock-pid <实际branch.lock持有者PID>`，显式cwd仓库根、PYTHONDONTWRITEBYTECODE=1。尖括号是运行时必填参数，禁止按当前日期伪造实际回执。

必须持有相同branch.lock，验证main及源文件、全原始页SHA/UTC/可得性/重叠/完整性/真实funding/元数据；预留前抓取失败保留raw和真实错误、旧指针不改；预留后无结果finish blocked，已有complete真实结果只恢复finish不得重跑。TLS逐次捕获2次有界尝试，不跳过证书验证。

本候选的历史选择偏差、L2/TCA缺失及1%闭合小时维护代理限制仍在，不称稳定实盘盈利。原SMA65与singleS28须独立持续，不可误用本计划的未开始字段判断原账户状态。完成每轮真实登记后仍需只读monitor snapshot/check与轻量证据一起main推送。
