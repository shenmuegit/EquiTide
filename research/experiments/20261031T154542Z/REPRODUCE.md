# 复现与证据

执行目录固定 `/home/desktop/Documents/Codex/EquiTide`，Python `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python`，环境`PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`。

实际命令：bootstrap、freeze、initial、reserve_batch_0、evaluate、audit、decision_check、summary、exports、grid_diagnostics、finish_batch_0、finish、forward、candidate（capture失败退出1）、candidate_recovery1、observer_status、review、gates、feed。实际退出码／stdout在`*_commands.json`、`*_receipt.json`及日志。4新金融定义逐个reserve成功先于首次valuation；14旧格点每范围只读，不用改名、排序或格式再次登记。

独立核对可运行`audit.py`、`check_decisions.py`、`check_grid_diagnostics.py`，它们重建保存的状态段和真实价格、独立核查信号／会计／指标／资格，未执行策略新模拟成交或新增登记。会重写可重建verification；在封存树只比较输出，不改旧spec/report/registry。完整4x4新旧场景分别标识，12新＋84只读，8CSV含所有变体、逐折与完整dailyNAV，状态段与源报告足以重建完整NAV，未提交大数组。

原始8市场Parquet和16历史输入的SHA／字节数见data_manifest；缺真实数据记录blocked，不合成行情。原始公开账户响应和packet精确小副本见raw_evidence_index。原冻结SMA／singleS28按真实现金、q、desired、entry和已计费用延续；每新截止先reserve，禁止重跑已完成观察窗口，`forward.py --reproduce`只做离线精确复核，无HTTP／登记写入。十策略账户及所有旧文件只读保护。

同branch.lock内执行registry、snapshot和monitor检查；只提交本轮轻量证据及4个共享文件，main非强制push。实际远端完整tree／所有必要blob、publisher退出0及解锁后核验在`.git/automation_proofs/20261031T154542Z.json`；封存文档不预写成功SHA。

传输恢复：原SMA一次TLS35由原curl自动重试成功，具体资产与精确总次数未逐次标注，原stderr留档。singleS28首轮capture8次GET中6成功／2次ETH小时TLS35失败，在任何spec/reserve/advance之前退出1，failure目录移至candidate_capture_failure_01保留。恢复计划先冻结代码／原文件SHA，6页逐URL/SHA复用，仅补两缺页，用verifiedTLS1.2/HTTP1.1，原observer/core规则与会计未修改；新capture成功后才reserve3观察并advance一次。共10次明确候选GET（8成功／2失败），不把缓存复用计为新GET；所有失败raw／stderr与恢复验证保存。
