# 收盘通道突破固定批次

应用walk-forward-validation、ml4t-sensitivity-analysis、ml4t-transaction-costs；固定main/branch.lock，不下订单/不委派。

- [x] 根目录/main远端、完整登记和241结论、初始16与旧账户保护、相关通道配置/精确常持对照查重
- [x] 冻结N20/25/30×M5/10/15、测试收盘不进入自身通道、入场/退出/反手优先级；27新spec先reserve再计算
- [x] 18原生+9父组合81成本场景，独立整数通道/每笔账本/完整NAV/逐折/三组敏感性核验
- [x] 全部finish保留负收益，原冻结账户12:30至14:30按原规则续接
- [x] 只读monitor/门禁/导出，完整封存main提交推送，远端核验后释放本人锁

研究、必要核验与封存完成；实际main推送、发布进程exit0和锁释放见.git证明。
