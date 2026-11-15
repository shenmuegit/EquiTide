本轮真实完成6个新金融配置：BTC过去10日样本log波动率上限2.5%/3.5%两个原生组件，与已有ETH预算R=.00875/.01组成四父组合，共18条1/2/3倍成本场景。历史通过6个：4父组合+2个BTC组件；淘汰0父组合+0个BTC组件。8个旧实际配置/24场景只读复用。12项原冻结账户窗口各自reserve/finish，partial rejected只表示未成熟180日，不取消原长期计划。

事前假设：固定BTC ROC L29/严格入场H3%/退出E0.5%，改变过去V10样本日log波动率上限cap为2.5%/3.5%。更低上限可能过滤高波动新仓，但有错过趋势的机会成本；3.5%检验较宽风险筛选。cap=[.025,.03,.035]×已有ETH R=[.00875,.01]为3×2面，代表cap2.5%/R.01在结果前冻结；旧cap3%中心只读，cap4/5旧结果亦查重保留，未复算。所有新参数在计算前保存spec并reserve。

BTC本金3750/固定名义1000；29日ROC严格>3%多、<−3%空，入场优先；带内实际多头仅ROC>−.005、空头仅ROC<.005保留，相等退出。仅新/反手检查过去V10样本日log波动率≤cap，同向实际q保持。使用完成前缀，LOT向下、信号后下一00:01真实OPEN不利tick；新cap从原现金算完整391日数量、执行费用、成交量冲击、实际资金费和保证金，不把旧货币NAV缩放或复用为新参数结果。

ETH银行只读：本金15000/固定名义4000，long-only L5/H2%/退出E.75%，有限归一化EWMS16 beta15/17、D3严格K.75%、V6 cap5.625%。最近4笔实际已实现有符号资金费中位数，信号前1–36小时且available≤signal合格，缺4笔阻止新仓；预算min(.0002,R×过去V8样本logvol×最新合格实际过去结算间隔小时/24)。R原值.00875/.01，仅新入场过滤，原同向q与退出不变。旧E.005文字过期而机器一直E.0075，旧spec/报告/status原字节不改。

父组合本金18750/raw[1,1]直接相加BTC3750和ETH15000两个原规模完整独立银行的美元NAV，20/80仅初始本金占比。权重不归一化，不缩放、不转账/再平衡/父订单/跨保证金；完整事件轴对齐后重算整体NAV与DD，不平均收益、Sharpe或回撤。

完整读取36012登记事件/17873ID、429份结论、三技能/task/README/OOS及freqtrade原ZIP。初始16条均有真实归档，缺实际结果0，保留旧legacy/false与负结果。基于最新main及真实模拟盘报价/采样缺口提交；上轮推送与解锁后证明核对，无旧reserved，本轮未重复上轮锁恢复。保护78293份旧文件，paper10冻结计划/账本/缺口保持原字节。

Walk-forward已执行：2025-10-19T00:01Z→2026-11-14T00:01Z，391日和33日背景；每币610562分钟bar、10176小时mark、1273实际资金费，8份Parquet的SHA、单位、闭合/可得时间与连续性核验。固定规则无拟合或标签，只用当时完成前缀；13完整30日折+1日尾折，现金/持仓跨折连续，仅全期末计成本平仓，整体DD来自全事件NAV。近40日8×5及扩展21日5+5+5+6逐折保存，尾折Sharpe=None且不计完整正月。无标签时purge/embargo无标签用途，实际背景/下一可执行OPEN/资金费成熟界限另行核验。研究历史反复开发，非未触碰最终留出或独立未来。

Sensitivity已执行：BTC V10cap三档×ETH R两档六格；BTC原生只沿cap、ETH原生只沿R。全部净收益、整体DD、Sharpe、Calmar、近期正折、10条相邻变化与并列最优边界保留。局部3倍净正与严格近期比例各≥60%，原通过/淘汰规则不变。ETH仅两档，不能证明宽平台；不同参数即使产生相同NAV也独立登记并明确别名，不当作独立样本，不在看结果后扩网格/换代表。

Costs已执行：每边手续费5bp+半价差1bp+滑点2bp+0.5×过去20日samplelogvol×sqrt(abs(q)×真实OPEN/过去20日quoteADV)，不利tick；执行成本及负资金费1/2/3倍，收入不放大。含实际LOT/tick/minnotional、参与率≤0.1%、费后1倍抵押及闭合小时high/low的1%维持保证金代理。线性永续不借现货，不编借币费。冻结费率/价差仍是估计，缺历史L2/TCA、完整档位、tick强平及真实容量证明；交易数、分项成本/占比和匹配持有/现金0对照逐场景保存。

预设门槛：三成本全期/近期净正；1倍≥10/13正完整月；近期各成本≥6/8正5日折；扩展21日净正且≥3/4正折；3倍DD≤25%；适用局部两比例≥60%；至少4底层平仓；1倍(毛价格PnL+净资金费)/执行成本≥2.5；无拒单/负抵押/保证金代理违规、期末平仓且≥180日。失败即rejected，完整结果仍保留。

|BTC V10波动率上限|ETH预算R|来源/状态|1x净%|2x净%|3x净%|3x整体DD%|正月/13|近期正折1/2/3|
|---:|---:|---|---:|---:|---:|---:|---:|---|
|2.5%|0.00875|新/passed|9.130706366|8.553260024|7.976003029|1.361016625|12|6/6/6|
|2.5%|0.01|新/passed|9.069110555|8.487825864|7.906730519|1.361016625|12|6/6/6|
|3.0%|0.00875|旧只读/passed|9.000028418|8.422242505|7.844642170|1.362719676|12|6/6/6|
|3.0%|0.01|旧只读/passed|8.938432608|8.356808345|7.775369660|1.362719676|12|6/6/6|
|3.5%|0.00875|新/passed|8.829160048|8.240366393|7.651750810|1.365228189|12|6/6/6|
|3.5%|0.01|新/passed|8.767564237|8.174932234|7.582478301|1.365228189|12|6/6/6|


事前代表BTCcap2.5%/ETH R.01（6dcbe8366b3d72478c077eb1206a7cc986832c469b6df40cb48bf8adb9019cbe）：三成本净9.069110555%/8.487825864%/7.906730519%，3倍DD1.361016625%，Sharpe2.238365555、Calmar5.409253594，passed、失败项[]。

BTC V10cap2.5%组件passed：三成本净17.130721646%/15.728393418%/14.326171677%，3倍DD5.694252106%，Sharpe1.385356337，正月10/13、近期正折{'1': 6, '2': 6, '3': 6}，失败项[]。

BTC V10cap3.5%组件passed：三成本净15.622990057%/14.163925267%/12.704910583%，3倍DD6.404402461%，Sharpe1.217248357，正月10/13、近期正折{'1': 6, '2': 6, '3': 6}，失败项[]。

全部组件与父组合的通过/失败项均为真实计算结果，逐项列于report.json与上述表；通过只表示本轮预设历史门槛满足，淘汰结果保留。组合通过不替代组件资格，ETH扩展21日PnL为0时该段组合利润来自BTC。全期/近期多指标及旧cap3%配对差异见old_anchor_comparison与conditional_parameter_robustness，未扩批、调低门槛、换代表或修改冻结账户。

配对旧cap3%：新cap2.5%/ETH R0.00875，3倍净收益变化+0.131360859个百分点、整体DD变化-0.001703051个百分点、Sharpe变化+0.041492343、Calmar变化+0.096350996。

配对旧cap3%：新cap2.5%/ETH R0.01，3倍净收益变化+0.131360859个百分点、整体DD变化-0.001703051个百分点、Sharpe变化+0.041452058、Calmar变化+0.096295741。

配对旧cap3%：新cap3.5%/ETH R0.00875，3倍净收益变化-0.192891360个百分点、整体DD变化+0.002508512个百分点、Sharpe变化-0.060988413、Calmar变化-0.141089638。

配对旧cap3%：新cap3.5%/ETH R0.01，3倍净收益变化-0.192891360个百分点、整体DD变化+0.002508512个百分点、Sharpe变化-0.060926505、Calmar变化-0.141008493。

cap2.5%两个新父在上述四项全期指标均略优于匹配cap3%中心，cap3.5%则相反；全部六新配置满足冻结历史门槛。改善幅度有限，尤其DD仅千分之一个百分点量级；最优cap位于预声明网格边界，不能证明更低上限继续改善或广泛平台。保留预设cap2.5%/R.01作为历史候选，仍待独立未来验证；不改冻结账户、不事后扩网格或换代表。

六新配置三成本NAV签名6组，匹配八个预登记旧参考0组，上轮实际新/只读配置匹配0/6；新父3倍净收益低于对应cap3为2个、相同0个。实际目标/状态/成交/资金费/NAV差异只读核验，未重算市场策略。

原始abs(deltaSharpe)>2×sampleSTD(absdeltas)启发式标记4/10，绝对变化范围[0.019019579922731733, 0.09801236537986169]、样本STD0.026558169，全部保存，不是统计显著性或过拟合概率。全部指标及并列最优边界见sensitivity_metric_boundaries。父网格3倍净正/正Sharpe/严格近期比例1.000000/1.000000/1.000000。

匹配持有3倍净-14.782911083%、DD18.454766592%，现金0；18父成本场景BTC/ETH全期及扩展PnL加总守恒核对。独立审计新原生6条/新父12条、旧原生15条/旧父9条曲线，新决策2346、旧只读5865；42成本场景、588逐折、336近期折、168扩展折、16464日NAV、18持有对照、10边及3×2图保留。最初尝试在首个新决策的旧cap允许列表处停止，未产生完整新曲线；原绑定/源码/失败回执保留。仅扩展预登记cap2.5/3.5允许值，归一化该列表后完整函数AST相同，simulate及货币核算公式/核心字节未变。六spec/门槛/边界未改，原reserve继续使用；修复后完整金融评估一次，共两次尝试、一次早期中断。

原冻结账户窗口：SMA/single Nov15_02:30→04:30，L4/FEWM04:10→06:10；本轮日事件{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、新成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、资金费记录{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}全0。完整实际结算窗口公开查询为空，18本永续账簿cash/q/entry等原样；完整NAV前缀、历史资金费/日事件唯一键、Nov15午夜各自一次核对，不按名义八小时补造，也不重复已完成的原00:01日决策。

SMA原65/对称1%/Float/本金1500:500/raw75:25保持，只增加120闭合分钟估值，累计63629分钟/63675点。完整67日权威research/experiments/20261115T075947Z/forward_inputs.json.gz只读复用，旧66/65数组前缀完全一致，本轮没有新日线捕获/指标计算；当前输入是minute数组。原组合3倍累计净-7.468957812%，负收益完整保存。所有原账户未成熟180日，旧延迟shadow不冒充十策略真实报价模拟。

本轮SMA/single Nov15_02:30→04:30，L4/FEWM04:10→06:10，仅闭合分钟估值/风险，实际查询为空，日事件/资金费/成交全0，18本永续账簿保持。午夜资金费与原00:01日事件已各计一次。本轮不采纳研究cap参数。下轮SMA/single04:30→06:30，06:31后闭合；L4/FEWM06:10→08:10，08:11后闭合。后者跨08UTC，必须先查实际资金费并按各自持仓入账，不假定下一窗口全0；没有原日事件，下一日仍Nov16_00:01。SMA当前输入是minute数组，完整67日权威仍075947/forward_inputs，保留旧66/65前缀；不可重开、强平、转账或误用旧daily-only执行器。十策略真实报价与旧延迟shadow分开，保留所有缺口/blocked记录。

旧Nov15午夜公开字段原捕获UTC2026-11-15T08:17:46.618283Z保留；本轮查询UTC2026-11-15T12:07:44.960352Z字段为空，未把旧字段重标为新响应。下一原日事件所有账户均为Nov16_00:01。

保存唯一公共GET 18次、实际传输失败1次，URL/UTC/raw/body/gzipSHA及失败回执保留；FEWM仅复用同窗公开数据、candidate仅复用metadata/time，账户cashflow不复制。SMA原curl没有单独保存体/精确UTC的内部重试仅按stderr披露，不补造。

391日开发历史与多重选择偏差未消除，无DSR/PBO显著性结论；历史合格或正收益不代表稳定实盘盈利。[Binance官方市场/资金费文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)及[官方公共数据README](https://github.com/binance/binance-public-data/blob/master/README.md)本轮已读取，实际响应/数据哈希是复现依据。

实际命令cwd=/home/desktop/Documents/Codex/EquiTide，解释器/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B。review/launch.py先bootstrap.py，再review/prepare.py、review/preflight.py、review/setup.py；review/execute.py首次freeze units bind reserve_0 evaluate，旧cap允许列表使evaluate失败且完整新曲线0；review/guard_repair.py保留初始源码/绑定并仅扩展校验后，review/execute.py执行evaluate_retry1 audit exports finish_0 research_check全部成功；diagnostics/historical_aliases；原账户midnight_archive l4h02 fewm candidate forward accounts_check；实际view_image后visual_review/account_continuity/complete_transport_audit/validate_sources；journal sources_check gates feed collect final_checks、staged_whitespace、seal/publish。实际命令/UTC/退出码/log保留；prepare/setup为首次源变换，不在已变换源上重复。已有实际ID禁止精确回测或覆盖归档，forward --reproduce只读核验不新增窗口。

实际阻碍/失败：{"round": "20261115T115951Z", "facts": [{"type": "diagnostic_read_path_failure", "recorded_utc": "2026-11-15T12:04:37.272022+00:00", "command": "cat research/experiments/20261115T095944Z/review/bootstrap.py research/experiments/20261115T095944Z/startup.json", "cwd": "/home/desktop/Documents/Codex/EquiTide", "native_chunk_id": "a36320", "exit_code": 1, "stderr": "cat: research/experiments/20261115T095944Z/review/bootstrap.py: No such file or directory", "resolved": true, "recovery": "Read actual bootstrap.py at prior-round root; prior files unchanged."}, {"command": ["/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python", "-B", "/home/desktop/Documents/Codex/EquiTide/research/experiments/20261115T115951Z/run.py", "evaluate"], "cwd": "/home/desktop/Documents/Codex/EquiTide", "started_utc": "2026-11-15T12:10:46.111833Z", "finished_utc": "2026-11-15T12:10:50.859248Z", "exit_code": 1, "log": "research/experiments/20261115T115951Z/evaluate.log", "stderr": "Traceback (most recent call last):\n  File \"/home/desktop/Documents/Codex/EquiTide/research/experiments/20261115T115951Z/run.py\", line 64, in <module>\n    if __name__=='__main__':globals()[argparse.ArgumentParser().parse_known_args()[1][0]]()\n                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/desktop/Documents/Codex/EquiTide/research/experiments/20261115T115951Z/run.py\", line 38, in evaluate\n    m=ms[row['asset']];v,z=engine.simulate(sp,m,int(k));z['summary']['recent40']=recent(v,m);z['summary']['extension21']=extension(v,m);vectors[row['fingerprint'],k]=v[cm['projections'][row['asset']]];summaries[row['fingerprint'],k]=z['summary'];arc['scenes'][k]=z;scenes[k]=z['summary']\n                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/desktop/Documents/Codex/EquiTide/research/experiments/20261115T115951Z/engine.py\", line 90, in simulate\n    actual=1 if D(state['signed_units'])>0 else -1 if D(state['signed_units'])<0 else 0;wanted,bounds=decide(spec,m,ref,actual);q=D(state['signed_units']);decisions.append({'decision_index':ref,'signal_available_ts_ns':int(m['frame']['available_ts'][ref*1440-1]),'execution_ts_ns':int(m['ts'][idx]),'policy_audit':bounds,'desired_direction':wanted,'fixed_entry_notional_usdt':float(notional),'state_before':copy.deepcopy(state)})\n                                                                                                      ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/desktop/Documents/Codex/EquiTide/research/experiments/20261115T115951Z/engine.py\", line 71, in decide\n    raw,audit=base_decide(spec,m,i,actual);p=spec['parameters']\n              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/desktop/Documents/Codex/EquiTide/research/experiments/20261115T115951Z/engine.py\", line 15, in base_decide\n    V=int(p['entry_volatility_window_days']);cap=float(p['entry_volatility_ceiling']);assert V in [6,10,14] and cap in [.03,.04,.05] and p['entry_volatility_gate_scope']=='new_or_reversed_position_only'\n                                                                                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nAssertionError\n", "resolved": true, "resolved_utc": "2026-11-15T12:18:41.245336+00:00", "recovery": "Original engine and binding preserved; only preregistered cap allowlist extended and synthetic checked. Successful evaluate_retry1, independent audit, all6finish and research check exit0; no completed new curve before fix, specs/gates unchanged.", "successful_pipeline_native_completion_chunk": "93889f"}, {"type": "SMA_original_curl_internal_retry_stderr", "log": "research/experiments/20261115T115951Z/forward.log", "stderr": "curl: (35) TLS connect error: error:0A000126:SSL routines::unexpected eof while reading\n", "command_receipt": "research/experiments/20261115T115951Z/forward_commands.json", "command_receipt_sha256": "608ed2b29f54c490f118a2155df326471a0d59ebb9d115f55abfec96a1a66849", "command_start_utc": "2026-11-15T12:23:18.360798Z", "command_finished_utc": "2026-11-15T12:23:39.284523Z", "native_phase_exit_code": 0, "curl_error_codes": ["35"], "exact_failed_attempt_UTC_asset_URL_and_body_not_separately_saved": true, "resolved": true, "recovery": "Original bounded curl completed successfully; final raw responses and exact forward replay verified. Failed body,asset/URL,and exact attempt UTC unavailable and not fabricated."}]}。保留全部正/负/淘汰/失败、原账户账本、冻结规则、登记、必要原包/哈希和下轮状态，清理可重建缓存，大行情忽略。6金融+12实际观察/36事件独立归档；锁内snapshot只读汇总既有账户/报告，不新回测/成交/部署/定时任务。最终commit/push、完整远端树/blob与解锁后检查见.git/automation_proofs实际回执。
