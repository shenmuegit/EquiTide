# BTC/ETH 定时策略研究

通过 Codex 原生定时任务在当前会话每两小时执行。使用仓库 `.agents/skills/` 中的 walk-forward-validation、ml4t-sensitivity-analysis、ml4t-transaction-costs。后两个来自 `ml4t/skills`，固定版本 `f0ea01919e0c517cd9b1e014724a520facd8a742`，已保存 Markdown 到仓库，便于后续运行读取。

研究工作目录优先使用 `/home/desktop/.local/share/equitide-research/worktree`；若运行主机改变，在可访问的用户目录克隆 `https://github.com/shenmuegit/EquiTide.git` 并检出 `codex/strategy-research`。原 `/root` 工作目录不可访问时不得声称完成本地回测。

## 流程与查重

每轮读取完整 `registry.jsonl`、已有结果和本轮任务说明 `task.md`，探索 1–2 个策略方向及预设参数/权重批次，目标是找到正收益方法。优先补测初始 16 个条目中缺真实回测结果的配置；代码和工程检查不能替代回测结果。在看结果前固定假设、完整参数/权重、数据边界和失败判据。每个具体配置 reserve 成功后才回测，finish 后保存 spec、report、中文结论和可复现代码并提交推送。所有回测结果，包括负收益结果，都永久保留。

只有完整具体配置相同且有实际回测结果，才算已验证重复；相同配置正在执行时也拦截，防止并发重跑。不同参数、权重、币种、周期或组合设置均允许探索，不因策略族相同而排除。结构指纹忽略名称/来源/族名称，排序币种和组件、合并相同组件权重，数值 20 与 20.0 相同。组合保留权重原值，不自动归一化；权重意义由分配规则明确。参数/权重敏感性变体可共用报告，但每个实际评估的配置独立登记，后续精确重复时复用结果。

登记簿保留历史 ID 与组件引用，以当前完整规则重新核对旧配置。`result_available` 表示是否有实际回测结果；初始条目经归档证据核对后追加标记，缺结果的允许补测。完整回测 finish 为 passed/rejected 后标记有结果，无回测结果用 blocked/abandoned，可恢复或重试，历史记录不删除。

策略 spec 格式：

```json
{"kind":"strategy","family":"stable-family-id","market":"spot","universe":["BTC/USDT","ETH/USDT"],"timeframe":"1d","logic":{"entry":"明确的信号规则，常数写入 parameters","exit":"明确退出规则","sizing":"仓位和风险规则"},"parameters":{"lookback":20,"threshold":2}}
```

组合格式：`kind=combination`、稳定 `family`、`logic`（分配/再平衡规则）、`parameters`（如再平衡间隔），以及至少两个 `components=[{"fingerprint":"已登记策略SHA256","weight":1}, ...]`。weight 是正资金分仓权重或敞口，具体意义写入 logic；组件内部可以有空头。不同权重数值或组合参数会产生新指纹。

```sh
python3 research/automation/registry.py reserve research/experiments/<轮次>/spec.json
python3 research/automation/registry.py finish research/experiments/<轮次>/spec.json rejected research/experiments/<轮次>/report.json
python3 checks/strategy_registry.py
```

退出码 0 成功、3 已有相同配置结果或正在执行、2 输入/登记簿/结果无效。登记簿只追加，失败记录不删除。初始清单来自已提交结果和现存脚本；缺回测结果的条目进入补测队列，不能称验证已通过。

## 验证与推送

使用时间滚动验证和必要 purge/embargo；报告完整 OOS 净值回撤、至少两个参数的预设敏感性邻域、1/2/3 倍交易成本压力测试。纳入手续费、价差、滑点、冲击，空头/永续另含借币与资金费。已有 2025-09-16 至 2026-09-16 历史已反复研究，不再称为未触碰的最终测试集。

只提交本轮相关的轻量证据，不提交凭据和大行情。普通 git push 不可用时，使用已连接 GitHub 应用创建 tree/commit 并以 force=false 更新研究分支。远程 tree 与本地 staged tree 完全一致后才能 soft reset 对齐 HEAD。保留冲突、未推送提交及其他人的修改，不自动合并 main、不执行真实交易。正收益回测不能替代前向模拟。

## 最近完成的轮次

- [2026-10-01 01:33 UTC](../experiments/20261001T013355Z/result.md)：补齐初始缺结果条目中的 6 条；36 个单策略、6 个组合完成真实六折验证、全参数网格及 1/2/3 倍成本。42 个候选全部未通过完整门槛，27 个在 1 倍成本为正、15 个在 3 倍为正。两个同期持有比较配置额外登记并保存；本轮 44 个配置均 finish。原始 16 条仍有 5 条缺实际结果：B0/B1/M1、永续配对、跨交易所资金费 Z。
- 行情已缓存在忽略的 `data/raw/research_20261001/` 与 `data/normalized/binance/`。54 个官方 archive checksum 及规范化数据哈希见该轮 `data_manifest.json`。下一轮复用有效缓存，勿重新下载或重复已完成配置；数据文件版本兼容旧脚本路径，实际下载日期以 manifest 为准。
- 审计重放使用该轮 `reproduce.sh`，不写登记报告；新研究仍须新 spec、reserve 和 finish。该轮公开记录了两条基准首次计算未事前登记的流程偏差，后续比较配置也须先登记。
