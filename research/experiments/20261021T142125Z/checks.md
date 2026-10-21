# 本轮实际核验与必要留档

18个中位数配置分别先reserve后实际计算54成本场景，全部finish rejected且result_available=true。边界自检包括奇偶中位数、离群点、未来前缀不变性、缩放与Decimal相等不交易。19,440条独立中位数/边界/时序、1,152笔余额守恒、54条初始本金锚定分钟回撤及完整成本/NAV回放通过。

原SMA另3个新截止先reserve，追加120闭合分钟、0新日决策/成交，9场景原NAV前缀、现金/数量/desired/交易/成本与nextstate核验及离线重放通过后finish rejected。19天尚未达到长期资格，不取消原冻结计划。

最终登记检查、SMA重放、snapshot、monitor检查与git diff --check均实际exit0；命令、返回码、stdout见final_gates.json，不使用cat日志返回码判断。feed_verification.json逐项比对18新配置的54档收益/回撤与原报告，监控3613配置/81观察，所有受保护源文件SHA保持。

公共分钟GET曾出现curl(35) TLS EOF，既有重试成功后才取得并核验真实响应；forward.log与implementation_attempts.json保留事实，未编造行情或重开账户。只清理54个可重建checkpoint及本轮字节码；已finish报告原字节、登记SHA、完整账户、必要输入及原始响应保留，不做格式迁移或改历史结果。
