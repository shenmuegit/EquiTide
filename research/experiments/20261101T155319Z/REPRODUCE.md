# 本轮真实命令与复现证据

固定目录 `/home/desktop/Documents/Codex/EquiTide`，main，共用分支排他锁。不安装依赖，不读取凭据。所有真实退出码/stdout/stderr在 `*_commands.json`、reserve_batches/finish_batches、bootstrap/freeze/decision/grid/collect回执。

```bash
cd /home/desktop/Documents/Codex/EquiTide
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
PY=/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python
R=research/experiments/20261101T155319Z
$PY $R/bootstrap.py
$PY $R/freeze.py
$PY $R/commands.py initial
# 初始旧合成夹具失败；原脚本在check_primitives_before_fixture_fix.py。
# 原因/唯一修正/哈希见fixture_root_cause.json、fixture_fix.json。
$PY $R/commands.py initial_retry_fixture
$PY $R/commands.py reserve_batch_0
$PY $R/commands.py reserve_batch_1
$PY $R/commands.py evaluate
$PY $R/commands.py audit
$PY $R/check_decisions.py
$PY $R/commands.py summary
$PY $R/commands.py exports
$PY $R/check_grid_diagnostics.py
$PY $R/commands.py finish_batch_0
$PY $R/commands.py finish_batch_1
$PY $R/commands.py finish
$PY $R/commands.py forward
$PY $R/commands.py candidate
$PY $R/commands.py l4h02
$PY $R/commands.py observer_status
$PY $R/commands.py review
$PY $R/commands.py gates
$PY $R/commands.py feed
$PY $R/collect_evidence.py
$PY $R/finalize.py
$PY $R/publish.py publish
```

上列为真实顺序，不能在完成目录原地重跑金融试验。驱动拒绝已有结果，保留完整reserve/finish和账户账本。首次initial用当时旧夹具，当前check_primitives.py为唯一夹具修正后的版本；重建初始失败可使用保留的旧脚本和原哈希，而不是把它误认成当前模型失败。修正仅把合成低价段延长至索引24，并缩短后续段，45个价格和最近10个波动样本不变；S24读取索引20得到预期低价。原错误/初始exit1、根因诊断、重试exit0均保留。无策略、规格、门槛修改或真实回测重跑；全部12个reserve都发生在初始重试/代码绑定之后。

预先固定快L3/4/5 × 慢S24/28/32，H=2.5%、退出缓冲绝对ROC0.0025、V10样本logvol cap0.045。BTC原ROC31/H4/E1不变。S28的3个原生和3个父格点只读，只有S24/S32的6原生ETH及6父组合实际新算，36成本场景逐项保存。每个不同L/S配置独立登记。已有10个唯一来源含同资金/同初始N的常多参考，不重写其资格或算新控制。

本轮在绑定前只扩展engine慢窗口允许域24/28/32，实际slowROC按参数S索引。独立审计也按spec的S重建Fraction信号，不能继续固定i-29。S32首决策i=33取close[0]，33个已完整预热日足够，无负索引/未来填充。合成检查覆盖各L/S多空方向、E等号退出、V等号过滤、首个S32预热边界及美元净值相加，不计真实金融回测；之后所有已绑定代码字节保持。

年度数据为plan的8份真实Parquet，路径/大小/SHA和16份既往必要输入由data_manifest固定，大行情留忽略data。真实BTC3750/N375和ETH15000/N4500；原权重[1,1]为两个完整银行，资金份额20/80%，总初始C18750、总N4875。父净值为实际银行美元相加，不重复加权、线性缩放、跨抵押或免费转账/再平衡。完整连续370日、12完整30日折+10日尾折，近期40日继承day330状态；信号和past20成本统计只用过去，无训练/标签，purge0/预热30+间隔3。重复开发历史不是最终未触碰测试，多重选择偏差不因局部比例消失。

成本1/2/3倍含费用/价差/滑点/成交量相关冲击、真实资金费和适用借币/抵押约束。正资金费收入不放大、负支出加压；无L2/TCA或完整真实清算档位/容量证明。匹配持有为同银行/初始N常多控制，非满仓或同风险买持，现金0%另列。11CSV、两张L/S面、全部归档/必要逐笔/资金费/状态段及完整NAV哈希保留；独立审计不调用simulate/decide/trade进行新金融试验。所有失败、负收益期段和不合格变体保存。

原SMA65/原singleS28续Nov1 UTC12:30至14:30；独立未过滤L4/H2续14:10至16:10，必须16:11参考闭合后才采集并真实处理16资金费。准确纳秒/rate/mark/当时q一次记账，保留pre/post正时长风险状态，不重复08资金费、不把本轮L/S/缓冲/过滤策略注入旧计划。Asia/Shanghai已Nov2时仍按UTC判断日决策，下一UTC Nov2 00:01未提前触发。部分rejected不取消原180日/终止计划，不把延迟shadow充当十策略真实报价成交。

保留当前全部HTTP尝试、响应/packet副本、完整账户账本与下轮必要状态。核验后只清理可从基准登记重建的语义元数据，原SHA/字节/行数在cleanup_verification，金融结果/账户账本删除0。快照同锁只读已有证据，不新回测/成交、不改规则/本金/持仓/预算、不部署网页/建定时器/下真实订单。

SSH非强制push main后重新fetch和独立ls-remote，验证完整tree与必要blob逐字节SHA。见.git/automation_proofs；必须publisher真实终态exit0后再释放锁并独立核对封存文件/工作区/main/两条永续观察链。不预写commit SHA或成功状态。
