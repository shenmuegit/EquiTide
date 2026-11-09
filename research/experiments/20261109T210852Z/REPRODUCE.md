# 本轮复现与核验

工作目录固定 `/home/desktop/Documents/Codex/EquiTide`，仅main。已finish配置只读复用，不再次reserve/evaluate；已完成账户窗口不重新advance，不改变冻结规则或本金。

`reproduction_history.json`、各阶段`*_commands.json`、原生日志和审计回执保存实际命令/退出码/顺序。`plan.json`/`specs/`固定H1.75/2/2.25%×E0.625/0.75/0.875%、L5/K0.75%/VC5%/S16/D3，旧H2%行只读。`report.json`、`results/*.json.gz`及成本/逐折/近期/日NAV/敏感性CSV保存全部12项真实结果及底层账本。大行情位于清单所指忽略data目录；当前公共响应和原账户输入已复制至`raw_evidence/`，失败响应与stderr一并保留。

实际金融阶段依次为freeze、freeze_retry1（首次reserve前只澄清继承文字，不改数值规则）、合成错误对照、initial、两次reserve batch、evaluate、audit、counts、summary、exports、decisions、grid、两次finish batch、finish。实际形式为：

```
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261109T210852Z/commands.py <实际阶段>
```

这是历史执行说明，不应对已完成配置再次计算。独立`audit.py`从真实输入和保存账本核对Fraction信号、H/E邻域、数量/LOT、Decimal费用/量冲击/资金费、抵押、小时风险代理、连续和逐折净值，不调用simulate/decide/trade。`review/journal_layout.py`在`commands.py review`之前运行，48条事件与完整逻辑索引无损保留。

四原账户各单次reserve/advance/finish，SMA/single到18:30、L4/FEWM到20:10，均仅闭合mark/风险，0新资金费/日决策/成交。自身Nov9_16.001均已结算一次，不重复或复制现金流。两个顺序执行批次均正常结束。下一窗仍只mark；未来跨Nov10UTC00:01时需新实际00资金费字段和各自闭合日上下文，SMA65需刷新，不把旧Nov9字段或未闭合价格当作新数据。

监控实际运行`python3 research/monitor/snapshot.py`与`python3 checks/monitor_snapshot.py`，仅汇总已有记录；当前快照以本轮提交对象为准，后续main自动更新可能包含后续观察。

以下只读核验关键已提交文件SHA256，不修改工作树、不请求行情、不计算策略或账户：

```sh
python3 -B - <<'PYCODE'
import hashlib,json,subprocess
from pathlib import Path
root=Path('/home/desktop/Documents/Codex/EquiTide')
r='research/experiments/20261109T210852Z'
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

重复开发历史、多重选择、参数敏感、同路径别名以及缺L2/TCA/逐tick强平限制全部保留，历史通过不等于独立前向或稳定实盘盈利。
