# 20261118T122939Z 运行摘要更正

原封存轮次的 runtime_note.json 把 single/candidate 新模拟成交数写成0；实际为3，分别对应1/2/3倍成本场景各1笔。这是2026-11-18 UTC00:01按原冻结策略执行的一次ETH开空动作，数量1.644ETH，在三个成本场景分别记账；属于延迟shadow模拟，未发送真实订单。

正式报告、完整账本、独立审计、next_research_state.json、中文result.md原已正确记录3笔。错误只在手工汇总的运行摘要，现以本追加更正记录为准。原封存文件与其SHA保留不改，未重跑模型或观察窗口，未修改冻结规则、本金、持仓、费用或资金费；后续必须从正确的candidate state继续ETH负持仓。

逐场景原始成交及所有权威来源SHA见同名JSON，可执行同名Python检查器进行只读核验。

补充发布前首次只读范围校验因私有Git状态解析器去掉首行状态空格而退出1，未stage、未commit、未push。失败回执见同目录publication_preflight_failure JSON；修复解析后仅重试发布，没有重跑金融或账户计算。
