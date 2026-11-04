本轮复核与复现

固定执行目录 /home/desktop/Documents/Codex/EquiTide，仅main，与paper10共用research/automation/branch.lock。真实命令、cwd、UTC时间和退出码在各*_commands.json、reserve_batches/、finish_batches/；封存all_command_receipts.json汇总。18新配置分8+8+2成功reserve后，只进行一次实际估值。10旧结果/6原生银行/18成本路径只读，原status/criteria/sensitivity及报告字节不变。

本批固定S24、L5/H2%、E0.5%、V10/cap4.5%。M(i,24)使用i−24..i−1完整收盘，beta23/25；s=M(i,24)/M(i−D,24)−1，K0.1/0.2/0.3% × D1/3/5。gate仅s>K为+1、s<−K为−1，其余含等号0；与raw逆势desired不等时flat，含已有仓。最多29日上下文，源有33日。engine用Fraction幂和、audit以独立Horner双窗口复核，原生simulate AST与上轮相同。旧K0参考逐格S/D匹配，仅强度K不同；同路径别名不算独立alpha。

8个实际行情/mark/资金费/约束parquet、全部源spec/report/archive/code的版本、字节和SHA在plan/code_binding_before_evaluation/data_manifest，原行情保留在ignored data/normalized，不重新下载替换已用历史。固定370日连续轴、12×30日+10日尾折、近期40日8×5日；所有正负折和成本场景完整保留。

在本轮main原始提交状态下复核以下已保存输入和账本。后续共享指针已前移时，旧观察审计会主动拒绝不匹配；保留当前账户，不能倒改指针、对已有过去截止重采或重下模拟单。

```bash
cd /home/desktop/Documents/Codex/EquiTide
research_py=/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python
research_round=research/experiments/20261104T101506Z
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

第一次实际计算命令保存在evaluate_commands.json：先完整执行reserve_batches的18条成功预留，再以相同cwd/env调用研究venv的commands.py evaluate。该命令保护已存在report，故完成后只读审计重建NAV及账本，不重复reserve/估值/finish旧配置。9个新ETH原生策略和9个完整银行组合均有3档真实结果，不线性缩放旧NAV/数量或平均指标，raw[1,1]、本金3750+15000=18750、预算500/4500。

原SMA与single窗口Nov4UTC06:30→08:30，L4为08:10→10:10。single以本轮抓取的fundingTime/fundingRate/markPrice及自身BTC−0.012数量核算08结算，L4的08资金费已在上轮处理而不重复。原SMA完整日线上下文20261104T021133Z/forward_inputs.json.gz不变。原规则/本金、持仓、risk/context和完整NAV前缀保持，未采纳研究参数、不截点强平、不重置。partial不是180日/六折资格，旧延迟shadow与十策略报价账户分开。

初始锁忙真实退出1留档，等原owner推送核验和释放后才写研究。公共GET使用预定有限次TLS校验重试，全部失败与成功响应及完整packet保留；不重新执行任何已完成金融或观察结果。本轮Pandas3.1.0与Binance官方文档读取成功，实际结算仍以API原始响应为依据。metadata_interpretation.json解释继承的scope标签与immutable observer只读预检计数，数值/资格/原report字节未改。

最终发布实际退出码、远端完整tree/blob校验和解锁证据留在.git/automation_proofs/20261104T101506Z.json，避免向已封存报告追写commit SHA。只读网页自动读取main，不创建重复部署或定时任务。
