# 复现与核验

固定工作目录/home/desktop/Documents/Codex/EquiTide，main only，同branch.lock排他锁。解释器/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python，环境PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1。runtime.json含版本。

实际顺序：bootstrap全量读取→freeze12完整定义→initial因果OPEN/同ns资金费/份额测试→reserve8+4成功→evaluate一次36新组合曲线（0源策略/订单重跑）→独立audit→summary/5CSV导出检查→finish8+4及状态核验。所有actual命令/时间/退出/log在all_command_receipts；冻结命令实际tool chunk/exit在freeze_execution.json。金融结果已完成，不重复reserve/evaluate。

只读核验：

```sh
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T214014Z/audit.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T214014Z/check_exports.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T214014Z/forward.py --reproduce
```

audit仅重建已有现金流/仓位与净值、校验已有结果；不调用原策略simulate/decide/trade或重新拟合源信号。资金单位owning完整出资源账户，原值[1,.25/.5/.75]不归一化，不是降低原生银行LOT后的重新成交。每源20000，总本金25000/30000/35000，3同本金加现金比较也单独登记。market.py构造真实因果公共事件轴，portfolio.py先验证全部545013/570543源净值哈希，后重估新增小时OPEN。5CSV/6panel图数值与完整OOS/13折/8近期折有独立核验。原数据8Parquet、既往16源输入及9只读来源spec/report/archive SHA在manifest；缺数据停止，不合成。

原SMA与单S28分别预留新20:30截止并只计算一次，保留41579/5676点账户、完整原账本/冻结规则。候选抓取3次timeout28重试成功，11尝试原始压缩响应/真实stderr与最终8HTTP200证据保留；0窗口重跑。随后registry检查、同锁python3 snapshot.py/monitor_snapshot.py和旧行完整对照；只读已有paper10，无真实订单。未来共享指针可合法推进；按本轮保存candidate_current_pointer.json及manifest核验，不回滚。

最终报告/登记不可为网页或测试通过而重写；所有新候选淘汰、正/负原结果与真实失败保留。publish.py提交本轮目录及4共享文件、SSH非force推main，fetch/独立lsremote/完整tree和全部必要blob哈希检查；发布进程实际exit0后释放既有锁。真实SHA/进程/解锁证明在.git/automation_proofs/20261030T214014Z.json。

发布前检查补充：首次git diff --cached --check实际exit2，CSV默认CRLF被判尾随空白，尚未创建commit。仅5份CSV行尾改为LF，逐字段完全相同且导出核验重试exit0；金融报告/登记/账户/原计算代码哈希不变，没有重算。真实完整失败回执gzip及修复证据保存，随后按同main锁重新提交推送。
