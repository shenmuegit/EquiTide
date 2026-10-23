# 原冻结SMA：12:30→14:30闭合分钟续接

3个新截止先reserve后实际续接、独立审计再finish。报告SHA256`2b198dee41b557ac57fbfb9c110e119dc65578043eb8ea54b82fbd393b4e16b6`，原冻结计划SHA256`2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81`。

保持原SMA65±1%、BTC1500/ETH500原75/25及Float现金/数量。旧31012点完整NAV前缀原样保留，各场景只追加120闭合分钟到31132点，累计31109分钟（21日＋869分钟）。BTC持币、ETH现金，旧现金/数量/desired/历史成交/成本完全保持；无新日决策、参考点、成交或费用，无重开账户、转账、调仓或强平。

|成本|累计净收益|连续整体DD|累计成本USDT|新增成交|
|---|---:|---:|---:|---:|
|1x|-5.733116%|9.338833%|3.204208|0|
|2x|-5.885664%|9.367352%|6.400993|0|
|3x|-6.037859%|9.395856%|9.590378|0|

Walk-forward仍21完整日部分观察，未成熟180日/六折；三个截止有真实结果而rejected，不取消原长期冻结计划。敏感性为原规则不调参；原1/2/3倍成本路径保留。永续父组合研究不替换原现货账户。

两币各121根真实分钟bar（含1重叠），保留两份完整原始HTTP响应gzip、输入gzip、URL/取得时间与原始/压缩SHA。curl取数期间曾诊断TLS35 unexpectedEOF，内置重试后外层Python实际exit0；未单独捕获失败资产或单次尝试退出码，真实stderr和回执留档read_failures.json/forward.log。不能以外层0否认该失败事实。

后续已核对全部闭合时间、重叠、连续轴、原状态字段与完整NAV前缀；audit_forward.py和forward.py --reproduce真实exit0，成功响应hash匹配。重放不访问HTTP或写登记，不通过重置/改收益消除错误。paper10计划/状态未动，旧延迟shadow不是十策略真实报价模拟。

下轮从2026-10-23 14:30UTC继续，下个日事件Oct24 00:01UTC，原终点2027-03-31不变。新截止先reserve，本完整报告/源状态是下轮必需输入，已finish报告不为压缩迁移字节。

复核：`PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T144255Z/forward.py --reproduce`。
