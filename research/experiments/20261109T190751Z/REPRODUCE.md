# 本轮复现与核验

工作目录固定 `/home/desktop/Documents/Codex/EquiTide`，仅main。已finish配置只读复用，不再次reserve/evaluate；已完成账户窗口不重新advance，不改变冻结规则或本金。

`reproduction_history.json`、各阶段 `*_commands.json`、原生日志和审计回执保存本轮实际命令/退出码/顺序。`plan.json`/`specs/`固定L4/5/6×E0.625/0.75/0.875%、K0.75%/VC5%/S16/D3/H2%，旧L5行只读。`report.json`、`results/*.json.gz`及全部成本/逐折/近期/日NAV/敏感性CSV保存所有12项真实淘汰结果和完整底层账本。大行情保留于清单指向的忽略data目录；当前公共响应和原账户输入已复制到`raw_evidence/`。历史08/16公共资金费字段沿用原始实际响应及原检索UTC，仅用各自账户q/cash计算，不复制其他账户现金流。

实际金融阶段依次为freeze、合成错误对照、initial、两次reserve batch、evaluate、audit、counts、summary、exports、decisions、grid、两次finish batch、finish。实际形式为：

```
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261109T190751Z/commands.py <实际阶段>
```

以上是历史执行说明，不应对已完成定义重复计算。独立`audit.py`只从真实输入和已保存账本核对Fraction信号、L/E邻域、数量/LOT、Decimal费用/量冲击/资金费、抵押、小时风险代理和连续/逐折净值；不调用simulate/decide/trade。`review/journal_layout.py`须在源核验`commands.py review`之前运行，48条事件与逻辑索引无损保留。

四原账户各单次reserve/advance/finish，SMA/single到16:30、L4/FEWM到18:10。single在本窗结算实际16:00:00.001，L4/FEWM已于各自上窗结算，本窗不重复。外层编排真实返回143，其具体原因未知，不能声称外层退出0；五个实际阶段均有退出0回执，已保存的四账户全NAV/资金费与24ID/48事件通过只读完整性复核，没有重跑。

监控实际运行`python3 research/monitor/snapshot.py`与`python3 checks/monitor_snapshot.py`，仅汇总已有记录；当前快照应以本轮提交对象为准，后续main自动更新可能包含后续观察。

以下命令只核验本轮提交对象的关键文件SHA256，不修改工作树、不请求行情、不计算策略或账户：

```sh
python3 -B - <<'PYCODE'
import hashlib,json,subprocess
from pathlib import Path
root=Path('/home/desktop/Documents/Codex/EquiTide')
r='research/experiments/20261109T190751Z'
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

开发历史反复使用、多重选择、参数敏感、同路径别名及缺L2/TCA/逐tick强平限制均保留；正收益历史回测不等于独立前向或稳定实盘收益。
