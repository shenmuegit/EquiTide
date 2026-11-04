本轮复核与复现

固定目录 `/home/desktop/Documents/Codex/EquiTide`；只用main与共用branch.lock。各*_commands.json与reserve_batches/、finish_batches/保存精确命令、cwd、UTC起止及真实退出码；all_command_receipts.json为封存汇总。新16项分8+8预留成功后只实际计算一次。两九格面各含一个已有真实S32/E0.5%格，其旧spec/report/状态/criteria/敏感性不改，不重复reserve/finish或重跑。

固定快L5/H2%、V10/cap4.5%，变化有限EWM窗口S16/24/32与退出E0.375/0.5/0.625%，beta=(S−1)/(S+1)。engine.decide使用最新到最旧Fraction幂和，audit.policy用最旧到最新Fraction Horner独立核验。native simulate AST与前轮一致，复用原始Decimal成交/资金费/风险核算；BTC与只读旧EWM格不重跑政策。首个金融预留前更正继承stdout的18→16文字并刷新绑定，原绑定与逐字差异哈希保留，未改金融规则。

数据版本/边界/字节与全部SHA见plan.json、code_binding_before_evaluation.json、data_manifest.json。8个真实行情/mark/资金费/约束parquet保留在ignored data/normalized，不重新下载替代历史，不缩放旧数量或NAV。

在本轮main原始提交状态下执行以下复核，使用保存的实际输入和账本，不创建金融试验或成交。后续账户指针前移后旧观察审计会拒绝不匹配，不能倒改当前指针或重采过去窗口。

```bash
cd /home/desktop/Documents/Codex/EquiTide
research_py=/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python
research_round=research/experiments/20261104T061335Z
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

新旧资金费/成交计数分列于research_evidence_counts.json，旧重放不计新成交。固定S32/E0.5%参考与新S/E变体并非参数匹配比较；只比较相同资本/预算/快L/H/成本/时段下的保存指标。原SMA65、single L3/S28零退出和L4/S28零退出继续原冻结账户，不采纳本批研究、重置或强制截点平仓。SMA65完整日线上下文仍为20261104T021133Z/forward_inputs.json.gz；下一L4窗口跨08资金费，必须闭合后抓取实际结算和自身持仓，不预计算/复制金额。partial不是180日/六折资格。
