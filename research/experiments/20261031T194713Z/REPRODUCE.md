# 复现与留档

固定cwd `/home/desktop/Documents/Codex/EquiTide`，解释器 `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python`，环境`PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`。

实际顺序及真实回执在`*_commands.json`／`*_receipt.json`／日志：bootstrap，freeze，initial，reserve_batch_0/1，evaluate，audit，decision_check，summary，exports，grid_diagnostics，finish_batch_0/1，finish，forward，candidate，observer_status，review，gates，feed。14个新具体定义分别reserve成功后才计算，2旧原生＋2旧父的12场景只读复用，不改名重测。

只读核验脚本audit.py、check_decisions.py、check_grid_diagnostics.py重建保存状态段与真实价格、独立核查信号和会计及资格，不执行新策略回测／账户观察／登记；会重写本轮可重建verification，封存后只比较输出，不改spec/report/registry。42新场景＋12只读网格场景全部标记，9CSV含每变体／逐折／连续dailyNAV。完整545013点NAV SHA及足够状态／交易／资金费证据保留，不提交大数组。

8真实市场Parquet、16既有输入的精确SHA/字节数见data_manifest，缺数据记录blocked、不合成。原始公开新窗口小响应和packet精确副本见raw_evidence_index。原SMA及singleS28按实际现金/q/desired/entry/费用／funding继续，每新截止先reserve；已完成窗口不重跑，forward.py --reproduce仅离线精确复核、不发HTTP或写registry。

独立未来计划继续引用20261031T174613Z/prospective_l4原文件，本轮仅status确认waiting；不复制、不重绑或用本轮结果修改。0新未来账户／观察，工程结果不算金融回测。首次真实窗口以后须独立核查其新账本并扩展批次、pointer和manifest计数，不影响原SMA/singleS28/十策略。

同branch.lock内完成registry／readonly snapshot／monitor检查与旧行逐字典验证。只提交本轮证据＋4共享文件，main非强制push；全部远端tree／必要blob、动态原候选观察链ID数、publisher真实退出0及解锁证明留在.git/automation_proofs/20261031T194713Z.json。
