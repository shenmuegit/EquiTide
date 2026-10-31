# 复现与核验

固定目录 `/home/desktop/Documents/Codex/EquiTide`、main、branch.lock排他锁。解释器 `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python`，环境 `PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`。

已完成定义仅读取，不再reserve或回测。以下为使用真实保存账本/行情的独立核验，不重新生成原生交易：

```bash
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261031T094316Z/audit.py
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261031T094316Z/check_exports.py
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261031T094316Z/forward.py --reproduce
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261031T094316Z/audit_candidate.py
python3 checks/strategy_registry.py
```

真实执行顺序：bootstrap完整读取→freeze语义查重与完整spec/plan→initial合成/定义检查→reserve_batch_0/1/2共20次成功→evaluate首次实际5原生/15成本场景→父汇总缺MONEY/COUNTS中断→recovery_plan保存全部完成原生archive哈希及原绑定代码→独立portfolio_complete/run_recovered只读恢复这些原生NAV，完成未完成15父组合/45场景→独审→summary/exports→finish_batch_0/1/2及finish。

原失败代码和evaluate.log完整保留。不要直接重新运行旧run.py evaluate或已完成的native simulate。run_recovered.py内无engine.simulate调用，已完成5个原生archive逐字节SHA不变；首个父1倍摘要中断前的部分统计在恢复时重新计算，并非已完成父结果重跑。复现路径、actualstdout/stderr/exit见所有commands与recovery_verification。

8原始Parquet、16上游年度/近期源及全部新/旧spec/report/archive/hash见plan/context/data_manifest。7个当前原生格点、3个当前父格点及26独立旧来源保持资格和原始报告字节。原生C=10000*w、N=BTC1000*w/ETH3000*w实际计算LOT/tick/量相关冲击/费/资金费；父只以raw1/1加完整实际银行，不线性缩放旧净值、数量或费用。源数据已反复开发，不称未触碰测试或稳定实盘盈利。

原SMA按06:30状态reserve新08:30截止，实际闭合分钟→独审→finish→无HTTP精确重放。原singleS28的8成功真实页面验证后才reserve3/advance一次/finish；ETH资金费GET有一次TLS35失败，bounded第二次成功，失败原始响应和stderr在attempts与raw_evidence留档。08UTC EXACTfunding已入账，不是午夜+2ms；next09小时要排除同ns零持续prefund状态，保留postfund现金。保持原规则/本金/q/entry/完整NAV前缀，不用本轮新金额替换原账户。

登记和必要检查完成后，同锁执行：

```bash
python3 research/monitor/snapshot.py
python3 checks/monitor_snapshot.py
```

监控只汇总已有账户/报价/研究，无回测、成交、冻结状态变化，无网页重部署或新定时器。普通SSH非force推送main，完整远端tree/blob、真实发布进程exit0/解锁/输入哈希证明在 `.git/automation_proofs/20261031T094316Z.json`。
