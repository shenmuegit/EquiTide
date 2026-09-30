# BTC/ETH 定时策略研究

通过 Codex 原生定时任务在当前会话每两小时执行。使用仓库 `.agents/skills/` 中的 walk-forward-validation、ml4t-sensitivity-analysis、ml4t-transaction-costs。后两个来自 `ml4t/skills`，固定版本 `f0ea01919e0c517cd9b1e014724a520facd8a742`，已保存 Markdown 到仓库，便于后续运行读取。

研究工作目录优先使用 `/home/desktop/.local/share/equitide-research/worktree`；若运行主机改变，在可访问的用户目录克隆 `https://github.com/shenmuegit/EquiTide.git` 并检出 `codex/strategy-research`。原 `/root` 工作目录不可访问时不得声称完成本地回测。

## 流程与查重

每轮读取完整 `registry.jsonl`、已有结果和本轮任务说明 `task.md`，找或生成 1–2 个新策略/组合；在看回测结果前固定假设、参数、数据边界和失败判据。reserve 成功后才允许回测。完成三项验证后保存 `research/experiments/<UTC轮次>/` 下的 spec、report、中文结论及可复现代码，finish 登记并提交推送到研究分支。负收益、失败和中断记录同样保留。

结构指纹忽略名称/来源，排序币种列表；组合按组件指纹排序、合并重复组件、归一化权重。另用稳定族 ID 和逻辑指纹排除仅改参数/币种/周期/权重。任意程序语义等价无法仅靠哈希识别，执行者必须阅读历史进行语义查重。参数敏感性变体合并到同次报告，不能在下一轮作为新策略重跑。

策略 spec 格式：

```json
{"kind":"strategy","family":"stable-family-id","market":"spot","universe":["BTC/USDT","ETH/USDT"],"timeframe":"1d","logic":{"entry":"明确的信号规则，常数写入 parameters","exit":"明确退出规则","sizing":"仓位和风险规则"},"parameters":{"lookback":20,"threshold":2}}
```

组合格式：`kind=combination`、稳定 `family`、`logic`（分配/再平衡规则），以及至少两个 `components=[{"fingerprint":"已登记策略SHA256","weight":1}, ...]`。weight 是正资金分仓权重；组件内部可以有空头。

```sh
python3 research/automation/registry.py reserve research/experiments/<轮次>/spec.json
python3 research/automation/registry.py finish research/experiments/<轮次>/spec.json rejected research/experiments/<轮次>/report.json
python3 checks/strategy_registry.py
```

退出码 0 成功、3 重复、2 输入/登记簿/结果无效。登记簿只追加，失败记录不删除。初始清单来自已提交结果和现存脚本，`legacy-script` 表示只有代码、当前没有结果证据，保守排除重复；不能称验证已通过。

## 验证与推送

使用时间滚动验证和必要 purge/embargo；报告完整 OOS 净值回撤、至少两个参数的预设敏感性邻域、1/2/3 倍交易成本压力测试。纳入手续费、价差、滑点、冲击，空头/永续另含借币与资金费。已有 2025-09-16 至 2026-09-16 历史已反复研究，不再称为未触碰的最终测试集。

只提交本轮相关的轻量证据，不提交凭据和大行情。普通 git push 不可用时，使用已连接 GitHub 应用创建 tree/commit 并以 force=false 更新研究分支。远程 tree 与本地 staged tree 完全一致后才能 soft reset 对齐 HEAD。保留冲突、未推送提交及其他人的修改，不自动合并 main、不执行真实交易。正收益回测不能替代前向模拟。
