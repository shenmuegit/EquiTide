# 本轮实际核验、失败事实与必要留档

18个收盘通道/持仓时限配置分别先reserve后实际完成54成本场景，全部净亏损并finish rejected，result_available=true。全部负收益、逐折、敏感性和成本结果保存。

边界自检包括通道排除当前信号bar、未来前缀、缩放、严格价格相等、持仓年龄及时间退出优先。原始核验在独立检查器失败：误用all(close>=prior)要求高于所有历史收盘，冻结规则应为收盘不低于最低值，即any(close>=prior)。实际首个错误点位于上下轨之间，回测器本来正确。仅修检查器和增加中间价格回归fixture后重跑，实际exit0；没有重算新的经济配置、修改回测器或改写收益报告。

已核对19,440条独立通道极值、真实成交时钟/状态和UTC时序，1,290笔Decimal余额/成本/数量/价格约束，54条初始本金锚定分钟回撤，648逐折结果及19,494日净值；全成本NAV哈希精确重放通过。核验修正前后report SHA均为9ef6ae7725c1c1aaa97110965e4c637a5aa91930913c694f9a541116ab0da306，evaluate.py SHA均为8b742b6ff887b8c407d2da35d3a20e08eeae8251743a2e516110bc70e5c47b49。

verification_failed.log与research_commands.json保留首次真实exit1及stderr；verification_recovery_commands.json与verification.log记录修正后的真实exit0。构建期名称检查误拦历史RSI说明的另一次失败发生在reserve/计算前，见implementation_attempts.json；失败不被成功cat日志覆盖。

原SMA另3个新截止先reserve，追加120闭合分钟、0新增日决策/成交，9场景原28,460点NAV前缀和现金/数量/desired/交易/成本保持。累计28,559分钟、19完整天、28,580点NAV及nextstate核对与离线重放均通过后finish rejected，仅因不足180天/六折资格；原长期计划仍collecting。paper10 plan/state和源报告/状态SHA均未改。

final_gates.json逐项保存原SMA重放、checks/strategy_registry.py、snapshot.py、checks/monitor_snapshot.py、git diff --check的真实exit0/stdout/stderr。监控3,667配置/84观察，新18配置54场景的收益、回撤、逐折及往返数逐值核对，历史exclusive-end别名仍在，受保护输入不变。

核验后只清理54个可重建checkpoint与本轮字节码。保留所有已finish报告原字节、冻结spec、完整账户续接、原始分钟响应、必要输入和复现代码；大Parquet保留忽略data，路径及SHA见data_manifest.json。不做格式迁移、账户重置、真实下单、网页重部署或重复定时任务。

仅提交本轮相关证据、登记追加及两份监控汇总。提交后普通SSH非强推，fetch/ls-remote与完整tree核验后释放分支broker。
