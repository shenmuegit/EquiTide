# 本轮复现命令与时序边界

固定workdir=/home/desktop/Documents/Codex/EquiTide，main；所有登记、研究写入、快照和Git操作持有branch.lock。运行时/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B，环境PYTHONDONTWRITEBYTECODE=1、OPENBLAS_NUM_THREADS=1、OMP_NUM_THREADS=1。commands.json/log保存每条实际cmd/cwd/时间/exit/stdout/stderr；plan/data_manifest保存原始数据路径、版本、闭合边界、字节与SHA256。

文件前缀research/experiments/20261103T000256Z/，实际流程：

1. bootstrap.py读取完整registry主簿/片段、281份旧结论、task/三技能/README、freqtrade JSON/ZIP及checks/*oos.py，核验初始16原始实际证据和保护源/账本。
2. commands.py midnight_archive仅审核已完成Nov2午夜实际账本的完整日volume/close、6条资金费/6条原规则决策，旧证据/当前账户均不写入。该归档核验不计算Nov3结果。check_asymmetric.py --legacy-slow-range对旧范围为预期exit1；freeze预先固定L3/4/5×S26/28/30及12spec、数据、完整规则和失败判据；initial完成144政策、18准确滞后/等号、18旧行邻域及S30最早31close/真实首i33可得性检查，绑定全部必要代码。
3. reserve_batch_0、reserve_batch_1逐项调用registry.py reserve，共12成功才evaluate实际计算6原生+6组合/36成本场景。S28/E0.005实际旧曲线、BTC及匹配持有只读，不精确重算已完成配置。
4. audit独立Fraction/Decimal核验完整实际信号、数量、成本/funding/风险、整条NAV及折；summary只读导出。audit成功后counts/decisions，summary成功后grid/exports。旧资格保留，新窄邻域不能覆盖上一轮宽邻域失败或冒充独立最终测试。
5. 观察登记串行：forward原SMA从Nov2_20:30续22:30（先reserve、实际闭合mark、审计、finish及离线精确重放）；candidate原singleS28同窗口。两者尚未处理Nov3午夜，不因当前时钟已过午夜而提前推进。
6. l4h02原未过滤L4/H2从Nov2_22:10续Nov3_00:10，仅00:11参考闭合后采集。先reserve3ID，按实际NEW Nov3fundingTime/rate/mark/当时heldq入账一次，区分Nov2已记资金费；再00:01按原冻结规则，以新完成Nov2完整日close/quotevolume和past20成本决策，先平后开，不预设零成交。独立审核新日事件、6原规则决策、全部实际费用/资金费/逐步账本/NAV链；规则、N和本金不变。
7. finish_batch_0/1、finish逐项完成12真实结果，包含所有淘汰/负收益期间；observer_status只读；review核验21新ID/42追加事件、旧源、绑定代码和完整账本前缀。readonly_control_parameter_verification核对S28/E0.005旧控制的实际原始参数与图表标签。
8. gates实际执行python3 checks/strategy_registry.py、research/monitor/snapshot.py、checks/monitor_snapshot.py；feed核对12新增行/36场景及所有旧行完整字典；collect保留全部真实短窗原始响应/packet和下轮状态。监控不新回测/成交，失败恢复上次有效输出。
9. 实际view_image检查PNG、只清本轮可重建缓存，保留全部真实结果、必要代码、冻结规则和完整账本。finalize.py直接验证并封存；publish.py publish仅stage本轮和五共享文件，commit、SSH非强制push main、fetch/独立ls-remote、全tree和必要远端blob SHA核验；实际终态exit0后释放本轮broker并复查。

已完成轮次只读核验，不覆盖封存文件、不重复reserve/重跑策略、不补下旧报价订单，不创建其他分支/worktree。下一SMA/single窗口跨Nov3午夜，须更新原冻结日处理而不能复制mark-only/零日事件假设；L4已在本轮处理新午夜及00:01决策，下一00:10→02:10不能重复，均需新截止先reserve。本轮不计算未来窗口。
