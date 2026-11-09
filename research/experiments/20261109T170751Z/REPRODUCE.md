# 本轮复现与核验

工作目录固定 `/home/desktop/Documents/Codex/EquiTide`，仅 main。已完成定义只读复用，不重复 reserve/evaluate；不再次运行已完成的账户观察，不改冻结账户。

`reproduction_history.json` 及各 `*_commands.json` 保存本轮实际命令、时间、退出码和原日志；`report.json`/`plan.json`、`results/*.json.gz`、全部成本/逐折/敏感性 CSV 与 `data_manifest.json` 保存定义、结果、实际账本、完整净值摘要及输入 SHA256。大行情留在清单所指的忽略 data 目录，当前真实公共响应已复制至 `raw_evidence/`，本次16资金费公共响应保存在 `funding16_current_preflight/`。

实际金融阶段顺序为：`freeze`、合成错误对照与 `initial`、`reserve_batch_0`、`reserve_batch_1`、`evaluate`、`audit`、`counts`、`summary`、`exports`、`decisions`、`grid`、两次 finish batch 和 `finish`。每个阶段实际调用以下形式，精确完整命令见回执，不应对同一已完成定义重新计算：

```
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261109T170751Z/commands.py <实际阶段>
```

`audit.py` 为独立读取保存账本和真实数据的核算器，不调用策略交易器；审计时检查实际退出阈值、Fraction 慢趋势、数量/LOT、Decimal 费用/冲击/资金费、抵押、小时风险代理、逐折及连续净值、K/E 邻域。原生退出0回执保存在 `audit_commands.json`。`check_sources.py` 必须在 `review/journal_layout.py` 完成48条记录的无损片段整理后运行；原先排序错误导致的退出1和同代码后续退出0都保留。

四原账户分别由既有观察器单次 reserve/advance/finish。本窗 single/SMA 到14:30；L4/FEWM 到16:10，各自16:00:00.001资金费按本账户结算前数量计算。只有公开数据共用，现金流、数量、风险和NAV分别核验。不要在复现中再次运行观察器写入同一窗口。

监控实际运行 `python3 research/monitor/snapshot.py` 与 `python3 checks/monitor_snapshot.py`，回执均退出0；它们只读取已有证据。后续main上有新观察时，重新汇总会反映新证据，历史快照应以本轮提交对象为准。

以下只读检查本轮已提交对象的关键文件哈希，不修改工作树、不调用行情API、不计算策略或账户：

```sh
python3 -B - <<'PYCODE'
import hashlib,json,subprocess
from pathlib import Path
root=Path('/home/desktop/Documents/Codex/EquiTide')
r='research/experiments/20261109T170751Z'
git=lambda *args:subprocess.check_output(['git',*args],cwd=root)
commit=git('log','-1','--format=%H','--',r+'/data_manifest.json').decode().strip()
assert commit
manifest=json.loads(git('show',commit+':'+r+'/data_manifest.json'))
for name in ['report.json','plan.json','forward_report.json','candidate_observation/report.json','l4h02_observation/report.json','fewm_observation/report.json','current_actual16_funding_verification.json']:
    path=r+'/'+name
    assert hashlib.sha256(git('show',commit+':'+path)).hexdigest()==manifest['artifacts'][path],path
print(commit,'关键已提交证据SHA256一致')
PYCODE
```

反复使用的开发历史、多重选择、同路径别名及缺盘口/TCA/逐tick强平限制全部保留，历史通过不等于独立前向或稳定实盘收益。
