工作目录固定 /home/desktop/Documents/Codex/EquiTide，main 分支，先验证 git rev-parse --show-toplevel。全轮持有 research/automation/branch.lock，先同步远端并读取完整逻辑登记及历史结论。解释器 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B，仅用于依赖；执行cwd一直为上述仓库。设置 PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1。不要重复reserve/evaluate已完成配置或重启账户。

所有实际命令、完整参数、cwd、时间与退出码见 *_commands.json、reserve_batches/、finish_batches/、review_*_receipt.json。顺序：bootstrap.py完整读历史；commands.py freeze；check_asymmetric.py --negative-control-double-weighting（预期合成检查退出1）；commands.py initial（18严格退出边界、27因果性、18邻域和源绑定）；commands.py midnight_archive/observer_status/fewm_status；commands.py reserve_batch_0/reserve_batch_1全部逐项成功后，commands.py evaluate；实际完成后 commands.py audit，再 counts、summary、exports、decisions、grid；finish_batch_0/finish_batch_1/finish。数学审计重算核验，不再运行策略或账户。

本轮固定K1.5%、ETH L5/H2%/S24/V10cap4.5%、C15000/N4500，D6/7/8×退出E0.25/0.5/0.75%，旧E0.5%三格原生及父组合只读。BTC29/H3%/E1% C3750/N1000银行只读，raw[1,1]完整银行相加，不归一化或缩放数量/成本。6新ETH实际数量、成交、费用、资金费、风险/NAV＋6新父组合，36成本场景。退出E从spec精确Fraction读取；所有simulate/trade/funding/accounting函数AST保持。数据来自旧data_manifest冻结的真实370日历史、33日过去完整收盘和真实资金费/mark/成交量，原始大行情留忽略data；每个spec/plan/归档/数据/代码SHA留档。全部逐折、近期继承状态、连续整体DD及1/2/3倍成本保留，重复开发历史不是未触碰最终样本。

金融finish后依次 commands.py l4h02、fewm、candidate、forward，各自完整实际终态0后才执行下一步。L4/FEWM从Nov7_22:10续至Nov8_00:10，逐窗口先reserve；00资金费按各自结算前q/rate/mark先入账，00:01才使用完整Nov7收盘/成交量做原冻结决策，持仓与成交不预设结果。FEWM仅复用L4同窗公共行情，ownbooks/context/账户推进独立；single仅复用公共metadata/time，自己取Nov7_20:30→22:30窗口。SMA同20:30→22:30，仅闭合mark，完整65日源仍R024625，旧新输入形状不同不能混用；forward.py --reproduce只读离线复核、不发HTTP或记账。无真实订单或新paper10观察。

审查 review/run_checks.py control_diagnostics.py realized_aliases.py funding_handoff.py midnight_daily.py account_windows.py market_reuse.py evidence.py；midnight_daily独立以各自carried partial＋真实分钟合成完整1440根Nov7日成交量和收盘，核对12个日决策。全部24ID/48事件finish后运行 journal_layout.py、metadata.py；commands.py review；gates实际运行 python3 checks/strategy_registry.py、python3 research/monitor/snapshot.py、python3 checks/monitor_snapshot.py；然后feed逐旧行核对及collect保存轻量证据。生成仅只读已有账户和报告，冻结规则、本金、持仓不被monitor改写。

全部必要检查实际完成后直接 finalize.py 封存，禁止再改轮次文件。publish.py publish仅main非强制push，再独立HTTPS读取ref/完整tree和所有必要blob原字节SHA；真实退出码与提交SHA留.git/automation_proofs本轮私有回执，核验后释放原broker、运行postrelease检查。不创建分支或新定时任务，不重新部署网页。

交接：本轮L4/FEWM 00资金费及00:01决策完成后，下一00:10→02:10不再重复00，下一日决策Nov9_00:01。SMA/single下一Nov7_22:30→Nov8_00:30仍待各自00:01；single须按自己的q核算00资金费，不能复制其他账户现金流。SMA使用原spot日线65完整收盘，不能替代为perp close；当前mark-only适配器不能直接跨日，需复用已真实跨日的R024625和原Float冻结核算，先预留窗口、保持现金/desired/费用/fullNAV，不从现金重开。
