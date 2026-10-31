# 复现与留档

固定cwd `/home/desktop/Documents/Codex/EquiTide`，Python `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python`，环境`PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`。

实际命令／退出码／日志见`*_commands.json`、`*_receipt.json`和`engineering_failures/`：bootstrap全量读取，首次freeze因family大写schema拒绝且后续读取plan失败（均无金融reserve或计算）；保留失败源和spec后，仅修正family小写，freeze成功；initial原语与完整定义检查并绑定源码；reserve_batch_0/1逐个成功后才evaluate；audit、summary、decision_check、exports、grid_diagnostics；finish_batch_0/1及finish；原账户forward/candidate续接；observer_status、review；同branch.lock内gates运行`python3 checks/strategy_registry.py`、`python3 research/monitor/snapshot.py`、`python3 checks/monitor_snapshot.py`；feed逐行核验。

本轮固定V10/cap4.5%，L3/4/5×H1.5/2/2.5%为唯一新参数批次。16新金融定义／48成本场景，两个既有中心配置／6旧成本场景只读复用；相同配置不重跑，旧标准不重写。实际8市场输入及16既有输入SHA见data_manifest；每新成本完整545013点NAV SHA、状态段、交易、资金费、全部dailyNAV、逐月／近期折保留；不提交大行情和可重建数组。原生实际银行5000/15000与预算500/4500，不用线性NAV缩放代替真实数量／冲击。

`audit.py`、`check_decisions.py`、`check_grid_diagnostics.py`为独立只读核验：Fraction信号／Decimal会计与完整NAV／资格核查，不调用新simulate或推进账户。封存后只比较，不重写完成spec/report/registry。`forward.py --reproduce`仅离线复核完整旧NAV前缀和本窗口分钟mark，无HTTP／登记／新观察。

原SMA65保留各档Float现金/q/desired/成本，原singleS28保留各档Decimal现金/q/entry/funding/风险栈；每新截止先reserve，已完成窗口不重跑。下一Nov1UTC00:01跨日须使用原日转移和完整真实上下文，不把mark-only延伸跨日。

独立未来旧未过滤L4/H2仍引用`20261031T174613Z/prospective_l4`原冻结文件，本轮仅status确认waiting，0新账户／未来观察。首次实际未来窗口须独立审计并把新batch/pointer纳入登记／来源／manifest／发布核验，保持旧候选观察链分开，不复制重绑或事后改规则，不新建定时任务／重部署网页／下真实订单。

所有实际正负与淘汰／失败保存。只提交本轮证据和4共享文件，main非强制push，完整远端tree及所有必要blob、动态原候选完整观察链、publisher真实退出0及解锁证明在`.git/automation_proofs/20261031T214848Z.json`。
