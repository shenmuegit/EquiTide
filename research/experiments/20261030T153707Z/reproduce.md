# 复现与只读核验

固定工作目录 /home/desktop/Documents/Codex/EquiTide；main only，持有research/automation/branch.lock。解释器 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python；环境PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1，版本见runtime.json。

执行顺序和实际退出、时间、stdout日志及stderr见all_command_receipts.json：bootstrap→initial→reserve_batch_0..3（8/8/8/3）→evaluate一次→audit→summary→exports→comparison→finish_batch_0..3→finish→forward→candidate→observer_status→review→gates→feed。已完成配置不可再次reserve/重算；应只读核验已有结果。所有27候选与81成本场景真实执行且独立finish，无新benchmark。旧同本金常持3项只读。

事前完整规则/参数/时间/成本/失败门槛见plan.json/spec.json及27specs。通道N20/25/30×M5/10/15按BTC、ETH、COMBO三组各9格；中心25/10事前固定。入/退出通道均排除被测已完成收盘，次日00:01真实OPEN，原数量退出/反手先平后开。两银行各10000，固定名义1000/2000，父原值[1,1]总20000不归一化。信号改动独立135边界/优先级与135未来价格扰动验证，原费用/资金费/风险/数据/统计AST保持，code_binding_before_evaluation绑定计算前代码。

只读复核已有结果（不执行run.py evaluate/reserve/finish、不再次获取观察窗口）：

```sh
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T153707Z/audit.py
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T153707Z/check_exports.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T153707Z/forward.py --reproduce
```

独审整数价格信号/Fraction持仓/Decimal成交费用与资金费/保证金状态/完整NAV；无调用新simulate/target/trade。84场景45,781,092点。6CSV逐数值及3图18面板实际查看。数据清单含8真实Parquet、16来源输入、原公共响应路径和SHA；缺输入即停止，不合成行情。完整账本和实际正负结果保留，大行情留本地ignoreddata。

原冻结SMA65和singleS28只续12:30至14:30 UTC，6原观察ID加27金融ID共33新ID/66追加事件；规则/本金/持仓不改。当前14小时单一风险状态与08:00:00.001已入账资金费保留，下一窗14:30至16:30跨真实16UTC结算须按实际ns/mark/rate/旧数量入账一次，不能假设零结算或整小时。次日日决策2026-10-31UTC00:01，36日上下文及4日NAV边界连续；SMA65旧日上下文见next_research_state。旧延迟观察不称十策略实时报价模拟。

27项均被原月折/近期五日折/邻域严格门槛淘汰；1/2/3成本全期净正27/26/25项不替代资格。事前中心全期净正而近期负，不能选边缘年度最优点称稳健。三旧控制/17715受保护文件不变，旧canonical资格保持历史范围。历史重复开发不是未触碰最终测试或独立未来盈利。

next_direction_proposal仅提出九格因果信号共识与迟滞门槛，零reserve/零实际结果。下轮完整查重/冻结定义/独立登记后才能计算。原ROC/S边界停止决定保留，不继续追逐边界或放宽门槛。

检查与只读snapshot在同一main排他锁中实际执行；paper10只读，页面自动读取main，不需重部署或新定时任务。publish.py提交并推送main，fetch/独立lsremote/全递归tree与每个所需blob及数据哈希核验，发布进程真实exit0后释放本人锁。实际SHA和进程/解锁/发布后核验见.git/automation_proofs/20261030T153707Z.json；其他任务以后正常推进按保存pointer与本轮commit核对，不回滚共享账户。
