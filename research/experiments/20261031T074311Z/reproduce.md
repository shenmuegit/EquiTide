# 复现与核验

工作目录固定 `/home/desktop/Documents/Codex/EquiTide`，main。解释器 `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python`，环境 `PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`。任何登记、研究写入、监控和发布均先持有 `research/automation/branch.lock` 排他锁。

完成的配置仅读取旧结果，不再次reserve/evaluate。以下独立核验只使用已存真实结果，不调用源信号或成交模拟：

```bash
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261031T074311Z/audit.py
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261031T074311Z/check_exports.py
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261031T074311Z/forward.py --reproduce
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261031T074311Z/audit_candidate.py
python3 checks/strategy_registry.py
```

首次真实执行：核对目录和SSH同步→bootstrap完整读取→freeze的两个无结果预检失败留档→freeze_retry2完整去重/计划→initial_retry1合成/定义核对→reserve_batch_0/1共12次成功→evaluate36实际组合场景→audit→summary/exports→finish_batch_0/1及finish核对。详细actual stdout/stderr/exit见命令回执、reserve_batches、finish_batches及failure_receipts。非小写family及已完成持有对照触发预检，在0金融预留/0金融计算时停止；没有以改名形式重跑对照。

8原生Parquet、16上游年度/近期源、4原生账本、6旧父结果和冻结规则SHA见plan/context/data_manifest。实际新增8候选、4匹配持有权益对照，原始权重保留不归一化，本金为10000×原始权重之和。旧原生来源只按保存状态/真实价重建并验证原始NAV SHA。每个源原生持仓的费用、资金费和风险是实际数量下原成本模型；没有新原生订单、放大合约或合并冲击的复现声明。若需要那种实施，必须另行预留新原生规格，不能改变本批结果。

原SMA按保存的04:30账户reserve新截止后追加真实闭合分钟，独审/finish后精确无HTTP重放。单S28以原observer/core与每档cash/q/entry续接；fresh原capture首先建立raw/packet目录，8个真实HTTP200输入验证后才reserve3并advance一次、finish与pointer更新。不得重复已经完成的观察窗口。原始2SMA+8候选页面和packet的轻量逐字节副本随本轮提交，原canonical输入路径不改。

完成登记和必要检查后，在同锁中执行：

```bash
python3 research/monitor/snapshot.py
python3 checks/monitor_snapshot.py
```

监控只汇总已有10账户/报价/研究报告，不产生回测、成交或冻结状态变化。无网页重部署或重复定时器。普通SSH非force提交main，远端完整tree/必要blob/输入及publisher实际退出0与解锁证明保存在 `.git/automation_proofs/20261031T074311Z.json`。
