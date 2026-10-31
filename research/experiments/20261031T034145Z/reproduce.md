# 复现与只读核验

固定/home/desktop/Documents/Codex/EquiTide，main only、同branch.lock排他锁。解释器/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python；PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1，runtime含版本。

实际金融顺序：bootstrap全量读取→freeze6完整W20/30×L7/14/28定义→initial排除最新收盘/未来扰动/退化方差/beta名义及付费撤销检查、代码绑定→reserve6成功→evaluate一次106fit/318score及18成本场景（36银行+18联合）→audit独立拟合/原生LOT/政策/账本/全NAV→finish6→summary/8CSV与图、exports逐行/LF检查。仅图注澄清score方向/入场beta重新summary_retry1与exports_retry1，不重算金融模型或更改其报告/绑定。所有真实正负结果保留，不重复reserve/evaluate。

只读核验：

```sh
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261031T034145Z/audit.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261031T034145Z/check_exports.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261031T034145Z/forward.py --reproduce
```

8真实Parquet、16历史源输入、4只读控制spec/report/archive SHA在manifest；缺数据停止，不合成。每周固定锚点，beta为过去20/30每日log收益OLS，训练最后i-2、排除最新momentumclosei-1；score=logETH_L-beta*logBTC_L（alpha不减），ETHN2000/BTCentrybeta*2000、独立10000各/raw[1,1]不归一化。同方向不免费调beta/数量，只有新入场按新的eligible beta[.5,2]定量，所有真实费用/资金费/维护代理不改。

独审不调用新fit/calculate/simulate/core.trade：106拟合/318score独立math.fsum计算、原生LOT数量一致，6660逐日/954周决策、54新曲线29430702NAV点/414联合整体逐折近期；另6旧银行/3父SHA；新加旧1356fills/46620fund/420132小时风险状态。18成本场景中2x/3x全负，6配置全部淘汰，不择优/反转/降成本挽救，也不称重复开发历史未触碰测试或稳定实盘盈利。

原SMA只增120mark，41940点/41909分钟，0新日决策/成交；保存65日上下文仍在20261031T014115Z/forward_inputs.json.gz，当前按币种为minute数组，兼容以前1d/1m字典。候选初次metadata两次timeout28后停止，0预留/0计算，保留failure目录/raw/pointer。恢复准备路径ValueError及缺失wrapper exit2不产生额外HTTP/预留/计算；修正absolute路径后另一个capture目录verifiedTLS/ipv4/connect10/max30/2次，8HTTP200验证后才reserve一次账户窗口。累计150ID/6047点/5909分钟，5925旧点保持，0新决策/成交/资金费；37日上下文/5dailyNAV边界和午夜前2ms/postfund两段状态被9小时风险检查覆盖后清到02单状态，无违规、不重复记00资金费。原cash/q/entry和冻结规则/本金/终止日不变，非paper10报价模拟。

所有actual命令/时间/退出/log在all_command_receipts，包含失败candidate、candidate_retry2以及成功candidate_retry1；额外setup tool失败/完整rootcause和hash在read_failures与candidate_retry_diagnosis，原失败文件移到candidate_observation_failed_capture_000不覆盖。10真实GET中2失败/8成功原始压缩响应hash均保存，窗口不重跑。金融6+实际观察6=12新ID/24追加事件。

随后同锁registry、python3 snapshot/monitor检查和旧网页每行完整比对，paper10只读，无真实订单/重部署/新任务。新proposal原ETH S35历史特征需真实Sep13..15收盘和Sep16重叠，不能用负数组下标拿到未来，完整查重/冻结/各变体reserve之后才可计算。下一原账户窗口02:30至04:30按真实packet继续，不假设零事件、不回滚未来共享指针。

publish.py只提交本轮及4共享文件，SSH非force main，fetch/独立lsremote/完整tree/所有必要blob与原输入核验，发布实际exit0后解锁。真实SHA/进程/解锁见.git/automation_proofs/20261031T034145Z.json。

比较表元数据校正：首次推送后复核将CSV列same_nominal_gross_entry_budget_usdt更名为benchmark_nominal_gross_entry_budget_usdt，4000只描述旧长持基准预算；新beta策略预算3000–6000，原冻结规则与正文已说明敞口不匹配。18行所有数字、金融报告/登记/账户和图均不变；只校正表头与生成器并重新核验导出，追加main提交，无金融重算。
