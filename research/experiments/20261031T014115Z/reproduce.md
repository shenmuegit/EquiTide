# 复现与只读核验

固定/home/desktop/Documents/Codex/EquiTide、main only、同branch.lock排他锁。解释器/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python，PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1；runtime含版本。

实际顺序：bootstrap完整读取→定义生成脚本SyntaxError（0write/0reserve/0compute，已记录）→修正生成→freeze6→initial过去信号/冷启动/死区/确认/跨零/付费撤销检查和代码绑定→reserve6真实成功→evaluate一次18场景→audit独立Fraction确认链/Decimal账本/全NAV→finish6→summary7CSV/六面板和exports逐行/LF检查。所有金融配置已有真实结果，不再次reserve/evaluate。actual命令、时间、退出和日志在all_command_receipts；生成失败在read_failures，冻结真实退出在freeze_execution。

只读核验：

```sh
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261031T014115Z/audit.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261031T014115Z/check_exports.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261031T014115Z/forward.py --reproduce
```

真实8Parquet、16源输入、4只读源spec/report/archive及资金/成交代码SHA在manifest，缺数据停止不合成。固定L14/R7，H1/2/4%×K1/2从0确认状态起步；两个10000银行/N2000each/raw[1,1]不归一化。全部370日OOS、13折、近期8折、成本/资金费/容量代理严格门槛不改；6新配置虽全年三档净正仍全部淘汰，旧未过滤与长持结果只读。

独审不调用新simulate/rank/confirmed_target/core.trade：逐日/周检查6660/954含确认状态，54新曲线29430702点与414联合整体/逐折/近期；另6旧长持银行/3父原SHA。新加旧对照672fills/46620fund/312096小时风险状态核验。7CSV所有行和LF、六面板实际查看。复用历史/选择偏差/无DSR或独立未来证据明确。

原SMA跨日驱动来自20261030T013003Z，仅改currentPREV/65dayoverlap/cut日期，原Float SMA65/1%/raw75/25不变；3新截止先reserve，再capture4个真实spot页面，64日重叠和闭合分钟独审/精确只读复现后finish。41820点/41789分钟，Oct31两币日决策各1、0新成交，nextdaily Nov1。当前完整1d/1m字典输入须保留作下一日65上下文；未来mark-only输入可为每资产数组，勿假定形状。

原candidate observer/core不改；11次真实GET中3timeout28重试后成功，8HTTP200输入验证后才reserve并计算一次新窗口。跨日独审从分钟重建37日上下文、Fraction原决策、Decimal实际fund/订单/现金/风险栈/全NAV：新6日决策、6fund账项、0fill，累计147ID/5925点/5789分钟，5日NAV边界。Oct31UTC00:00:00.002真实funding已入账，BTC+.092779960156524每档、ETH−0E−16；保留整点prefund/+2mspostfund两段正持续风险状态，下一窗不能再记。原q/entry与计划本金/终止日期不改，不把当前H/K替换原单S28。

随后registry检查、同锁python3 snapshot/monitor check与旧行完整比对；共12新完成ID/24追加事件，paper10只读，未重部署/新定时器。按本轮candidate_current_pointer和manifest复核，未来共享指针可合法推进，勿回滚。publish.py只提交本轮目录/4共享文件，SSH非force main，fetch/独立lsremote/完整tree/全部必要blob核验，发布进程实际exit0后解锁；实际SHA/进程/锁证明在.git/automation_proofs/20261031T014115Z.json。
