本轮复核与复现

固定目录 `/home/desktop/Documents/Codex/EquiTide`；只用main和共用branch.lock。精确执行命令、cwd、UTC起止、真实退出码见各*_commands.json、reserve_batches/、finish_batches/，封存汇总为all_command_receipts.json。18配置分8+8+2成功reserve后，实际9新ETH原生与9父组合计算一次；数据/代码版本与全部SHA见plan.json、code_binding_before_evaluation.json及data_manifest.json。

新信号是最后32完整收盘的归一化几何权重(beta31/33)，并非无限EMA。engine.decide使用从最新到最旧的Fraction幂和；audit.policy以从最旧到最新的Fraction Horner递推独立核验。native simulate函数AST与旧实际SMA32引擎相同，复用原始Decimal成交/资金费/风险核算；BTC及全部SMA控制不重跑政策。大行情8parquet保留在ignored data/normalized，不重新下载替换。

在本轮main原始提交状态下执行以下复核；读取已保存实际原始响应与账本，不创建新金融试验或成交。后续指针前移后账户审计会拒绝不匹配，不应倒改当前指针或重采过去观察。

```bash
cd /home/desktop/Documents/Codex/EquiTide
research_py=/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python
research_round=research/experiments/20261104T041304Z
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
"$research_py" -B "$research_round/audit.py"
"$research_py" -B "$research_round/check_decisions.py"
"$research_py" -B "$research_round/audit_forward.py"
"$research_py" -B "$research_round/forward.py" --reproduce
"$research_py" -B "$research_round/audit_candidate.py"
"$research_py" -B "$research_round/audit_l4h02.py"
python3 checks/strategy_registry.py
python3 checks/monitor_snapshot.py
```

复核仍需本轮所引用的完整历史源文件和精确parquet。原SMA65、single L3/S28零退出、独立L4/S28零退出均继续原冻结账户，不采纳本批EWM；保留完整NAV前缀，不从现金重开。partial不是180日/六折资格。新旧资金费/成交计数在research_evidence_counts.json分列，不能将旧重放条数当新成交。
