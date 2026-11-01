# 复现与实际执行证据

固定工作目录 `/home/desktop/Documents/Codex/EquiTide`。Python `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python`，环境 `PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`。执行前核验项目根目录、main及远端，排他 branch.lock 由PID702139持续持有到实际提交、非强制推送和完整远端验证结束；不得另建分支／工作树。

实际命令／退出码在 `*_commands.json`、`*_receipt.json`，主序列为 bootstrap → freeze → commands.py initial → reserve_batch_0 → evaluate → audit → summary → decision_check／grid_diagnostics → exports → finish_batch_0／finish → forward → candidate → candidate_checks_retry2 → l4h02 → observer_status／review → gates → feed → collect_evidence.py → finalize.py → publish.py publish。summary_retry1／exports_retry1仅修正图表说明文字并复核导出，未重算金融模型。所有步骤固定cwd；长时阶段必须等工具返回实际退出码，不能以文件出现推定成功。

新历史批次是固定ETH L4/S28、V10样本log波动cap4.5%，退出绝对ROC缓冲E=[0,0.0025,0.005]×入场H=[0.02,0.025]。E0两原生／两父仅只读旧结果；4新原生＋4新父共8完整配置／24成本场景，逐spec实际reserve成功后才evaluate。原始权重[1,1]、BTC5000/N500和ETH15000/N4500原生银行，无资金归一化／NAV缩放／免费调仓。真实连续370日、13月折含尾折、近期40日8×5日状态继承、1/2/3倍手续费／半价差／滑点／实际成交量冲击和资金费、原生LOT/tick／抵押限制／小时维护代理逐档核验；全部实际结果独立finish，不改旧资格。数据8个真实Parquet及16旧年／近期输入SHA在manifest。完整新NAV由轻量状态段、逐笔成交／资金费、完整日NAV和SHA复核，不提交可重建大数组。

研究独立audit使用Fraction政策和Decimal原生账务，12新原生＋12新父、13080312NAV点、4440日决策、33300资金费、1422成交、588整体／月指标及129474风险检查实际通过；旧18原生／12父NAV只读复用。10个CSV与经实际图像查看的图表包含逐折／近期／敏感性／成本／持有／零缓冲分解。4父符合本批历史门槛，4ETH因近期5/8不足6及局部近期失败淘汰。E0.25%执行数不减、成本略升；E0.5%少2执行但净收益下降，不能声称降低换手普遍改善收益。重复使用历史不称最终未触碰测试集，2列H与描述性悬崖保留局限。

原SMA65现货Float账户固定旧1500/500、65日与1%规则，forward.py reserve/capture/evaluate → audit_forward.py → finish → --reproduce已实际完成。跨Oct31UTC22:30至Nov1UTC00:30，含00:01日决策；4真实分钟／65日响应、既有64日／分钟重叠、原NAV前缀与Float cash/units/desired/cost/trades独立验证。0新订单，累计30日／43261NAV点。下一Nov2日决策前采用能够接受当前dict1d/1m输入的mark-only续接；本轮dailyhelper固定有一次日事件，不可盲用于无事件下一窗。

原singleS28使用20261026T110637Z冻结observer/core和20261026T090537Z原plan，本金10000/10000、N1000/3000、ETHL3不变。独立L4/H2继续20261031T174613Z/prospective_l4原plan/core/observer/binding、本金5000/15000、N500/4500、未过滤L4/H2/S28零退出不变。各用独立pointer、3份新spec reserve才advance/finish，闭合参考分钟真实可用后capture，不互相继承钱／仓位。原S2800:30前真实6资金费／6日决策／0成交，7398NAV点／7229分钟／183ID；新L4续00:10至02:10，本窗0新日决策／成交／资金费，累计135NAV点／129分钟／6ID。实际短观察全部按部分资格finish rejected、保留180日计划；不把部分年化指标当收益能力，不把延迟shadow混入十策略真实报价账户。

账户audit_incremental_recovered.py仅复用冻结normalize的闭合数据／事件组装，独立验证新完整日volume/count、Fraction方向、Decimal原生quantity／tick／费用／冲击／资金费／cash、正持续时间小时风险、全旧NAV前缀及全新NAV链、统计／日边界／部分资格。不调用原target/trade/transition/advance，不重跑已完成观察。旧审计器在原S28缺capitals字段处KeyError；保留绑定原文件及初次／误重试两份实际失败日志。新审计器从各自冻结plan components取得本金，仅只读恢复核验／索引actual0；修订生成器一次写前assert失败也在repair_plan留档。报告／状态／指针守护SHA一致，registry仅后续独立L4追加6事件。两次新L4 TLS35失败原页／stderr与成功重试都保存；成功页才进入packet，未关闭证书校验。

所有当前2小时HTTP尝试与packet、SMA4原始响应完整轻量入Git，raw_evidence_index逐一将原path／已提交copy与SHA／字节关联；已有R内SMA响应不重复复制。旧完整年度行情与新L4首窗33日预热原样保留忽略data，无大行情提交或删除。保留全部账户账本、规则、登记、失败与必要恢复状态，清除范围仅本轮可重建临时文件（本轮无大数组／pyc／checkpoint残留）。

gates同一锁内精确执行 `python3 checks/strategy_registry.py`、`python3 research/monitor/snapshot.py`、`python3 checks/monitor_snapshot.py`；feed逐旧显示行及新结果SHA检查。只读汇总原十账户／报告，不下新模拟成交、不改冻结本金／仓位，不重部署网页或增定时器。快照失败必须恢复上次有效文件并记录真实失败。提交范围仅本轮目录和registry／两个独立pointer／monitor两个共享文件，预存data/normalized不改。

封存后不再重写本轮证据。`publish.py publish`用普通SSH直接推main、force=false语义，不创建其他分支；完整远端递归tree、所有必要blob SHA、全部原账户／独立L4观察链、真实publisher终态退出0及解锁后检查存 `.git/automation_proofs/20261101T014820Z.json`。该证明位于.git以避免向已封存报告追写自身commit SHA。不会提前把push记为成功。
