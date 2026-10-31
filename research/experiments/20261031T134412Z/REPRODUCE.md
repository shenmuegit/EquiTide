# 复现与留档

固定工作目录 `/home/desktop/Documents/Codex/EquiTide`，解释器 `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python`；环境 `PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`。

真实命令顺序见所有`*_commands.json`／`*_receipt.json`及日志：bootstrap，freeze，initial，reserve_batch_0/1，evaluate，audit，decision_check，summary，exports，grid_diagnostics，finish_batch_0/1，finish，forward，candidate，observer_status，review，gates，feed。每个新具体配置实际reserve成功在第一次valuation之前；既成配置不重新reserve或回测。全部负收益、负折和实际失败同样保留。

只读结果复核可运行`audit.py`、`check_decisions.py`和`check_grid_diagnostics.py`：从真实行情／已保存实际状态段独立重建信号与会计、指标和资格，不执行策略新模拟成交或登记。它们会重写本轮可重建verification文件；在封存工作树中只比较输出，不改原spec/report/registry。8个真实市场Parquet和16份原有输入的SHA/字节数在data_manifest；缺真实输入记录blocked，不生成价格。新实际archive的状态段、每笔成交／资金费／费用及545013点NAV SHA足以复核，全dailyNAV／逐折／逐变体CSV和图保留，不提交可重建大数组。

4个原生＋4个父旧格点的24成本场景只读复用。旧spec/criteria/sensitivity/status/report均原字节保护；外扩网格的邻域诊断单独存current_grid_diagnostic_sensitivity，不重评旧资格，不以不同名称或文字清理再次回测相同规则。

SMA65与singleS28继续原现金、数量、desired、entry和已计成本，新增截止先reserve；不得重跑已完成观察窗口。`forward.py --reproduce`离线精确复核本轮输入，不发HTTP、不写registry。不要再次运行observer或reserve/finish。每个原始公开响应和packet在raw_evidence_index中有精确提交副本；冻结规则／全部账户历史保护，不替换为本轮新金额。

同branch.lock内只读snapshot与monitor检查通过后，仅提交本轮轻量证据及4个共享文件。main非强制push、远端完整tree及全部必要blob SHA、真实publisher退出0和解锁证明在`.git/automation_proofs/20261031T134412Z.json`，不把事先写入的预期结果当成功证据。
