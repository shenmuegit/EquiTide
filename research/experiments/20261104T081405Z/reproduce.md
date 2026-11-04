本轮复核与复现

固定目录 `/home/desktop/Documents/Codex/EquiTide`，只用main与共用branch.lock。各*_commands.json、reserve_batches/、finish_batches/保存精确命令、cwd、UTC时间及实际退出码，all_command_receipts.json为封存汇总。18新配置分8+8+2预留全部成功后仅计算一次。价格/均值水平控制、BTC旧银行和匹配本金/预算常多基准只读，原资格不改。

新策略的有限指数均值M(i,S)只取i−S..i−1完整收盘，beta=(S−1)/(S+1)；趋势门槛为M(i,S)/M(i−D,S)−1，S16/24/28、D1/3/5，快L5/H2%、退出E0.5%、entry-onlyV10/cap4.5%固定。最大S+D=33覆盖最早索引0；不是价格/EWM水平或ROC端点。engine使用最新到最旧Fraction幂和，audit用最旧到最新Fraction Horner双窗口独立核对；native simulate AST与前轮一致。

数据/代码版本、字节与SHA见plan、code_binding_before_evaluation、data_manifest；8个实际行情/mark/资金费/约束parquet保留在ignored data/normalized，不重新下载替换旧历史。S16/24使用相同窗口的水平门槛参考，S28使用S24，窗口差异明确，不将其变化孤立归因于斜率。

在本轮main原始提交状态下执行以下复核；使用已保存原始输入和账本，不创建新金融试验或成交。后续指针前移后旧观察审计主动拒绝不匹配，不应倒改当前指针或重采过去窗口。

```bash
cd /home/desktop/Documents/Codex/EquiTide
research_py=/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python
research_round=research/experiments/20261104T081405Z
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

画图初次有两处E/D索引错误，原脚本summarize_before_axis_fix.py.txt、summary.log和实际失败命令保留；仅saved-metric导出summary_retry1实际成功，金融reportSHA不变、无金融或观察重跑。当前官方市场文档网页三次超时仍失败；primary_funding_field_verification.json使用本轮真实BinanceAPI响应与独立现金流审计完成数据字段核验，不把文档失败说成恢复。

L4本轮以自身持仓处理真实08资金费；source/新账本计数分列，旧重放不是新成交。single下一06:30→08:30窗口必须抓自己的结算/rate/mark/q，不复制L4金额。原SMA65保留20261104T021133Z的65日上下文，所有冻结规则/本金/持仓和完整NAV前缀保持，不采纳研究参数或强制截点平仓。partial不代表180日/六折资格。
