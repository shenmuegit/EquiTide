# 本轮实际核验与必要留档

18个收盘区间位置配置分别先reserve后实际完成54成本场景，全部finish rejected且result_available=true。1/2/3倍净正配置数1/1/0，全部正负收益保留；最高1倍收益仍不满足成本、回撤、折间及邻域门槛，不据此扩大本轮网格。

自检覆盖含当前已闭合信号bar的区间、平坦/上涨/下跌、未来前缀、缩放/平移、精确入退场相等及非法输入。独立Fraction有理数公式、区间极值、实际持仓状态和UTC时序共19,440条；1,080笔Decimal余额/成本/步长/tick约束；54条初始本金锚定连续分钟回撤；648逐折结果和19,494日净值及全成本NAV哈希精确重放，全部通过。

原SMA另3个新截止先reserve，追加120闭合分钟、0新日决策/成交，9场景原28,580点完整NAV前缀、现金/数量/desired/交易/成本保持。累计28,679分钟、19完整天、28,700点NAV及nextstate核对与离线重放通过后finish rejected，仅因不足180天/六折资格；原长期计划继续collecting。paper10 plan/state及旧源状态/报告SHA不变。

下一原冻结日决策为UTC2026-10-22 00:01。下一轮若跨该时刻，须读取本轮forward_state并按原规则执行该日唯一决策，不能将本轮只追加mark脚本越界使用，也不能从现金重启。使用新闭合日线与滞后成本输入、保持完整账户历史，详见forward_result.md。

initial_commands.json、research_commands.json、forward_commands.json与final_gates.json保留真实命令returncode/stdout/stderr。候选审计、原SMA重放、checks/strategy_registry.py、snapshot.py、checks/monitor_snapshot.py和git diff --check均实际exit0；不以cat日志的退出码替代。本轮进程和HTTP无失败输出；既往失败事实与已finish报告不改写。

监控3,685配置/85观察；新18配置54成本场景的收益、回撤、逐折及往返数逐值核对，历史exclusive-end别名仍在，受保护输入不变。两份监控汇总和本轮轻量证据同分支提交推送。

核验后仅清理54个可重建checkpoint及本轮字节码；保留完整已finish报告原字节、账户续接、冻结spec、两份原始分钟响应、必要复现输入和代码。原始大Parquet继续留忽略data，路径/SHA见data_manifest.json；不做格式迁移、账户重置、真实下单、网页重部署或重复定时任务。

提交后使用普通SSH非强推，fetch/ls-remote与远端完整tree核验后释放分支broker。
