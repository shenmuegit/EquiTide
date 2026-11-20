# 补充只读复核命令

以下为本轮实际执行的上下文读取及只读复核。金融/账户窗口均已完成，不再 reserve 或重算；原命令及结果保存于对应日志和登记。

```sh
cd /home/desktop/Documents/Codex/EquiTide
EQUITIDE_RESEARCH_PY=/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python
"$EQUITIDE_RESEARCH_PY" -B research/experiments/20261120T144446Z/bootstrap.py
"$EQUITIDE_RESEARCH_PY" -B research/experiments/20261120T144446Z/funding_availability_review.py
"$EQUITIDE_RESEARCH_PY" -B research/experiments/20261120T144446Z/review_economic_identity.py
```

bootstrap 是事前上下文命令，重读现在登记会改变事前快照，保留原 context.json，不在原目录覆盖执行。后两个命令仅核对已完成报告、真实原始资金费和全登记，不调用策略或账户推进。执行阶段完整顺序在 result.md；原始数据路径和 SHA256 在 plan.json、provenance 与最终 data_manifest.json。全部成本/逐折/变体结果在 exports/；冻结输入、完整账户账本保留。
