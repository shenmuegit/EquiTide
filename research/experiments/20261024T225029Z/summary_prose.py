"""Chinese audit narrative; values are taken only from actual saved results."""
import json
from run import ROOT,R,put
def write_texts(report,summary,audit,fwd,fv,ctx):
 cs=list(report['configs'].values());passed=[c for c in cs if c['status']=='passed'];best=max(cs,key=lambda c:c['scenes']['3']['net_return_pct'])
 lines=['# BTC/ETH回看单币扰动：补齐固定四格比较','',f"实际完成280个新被动组合、840成本场景、9240个新逐折结果；{len(passed)}项通过预设历史门槛，{280-len(passed)}项淘汰。48个已有组件的144条成本净值只读复用，组件策略重跑0。296个旧组合保持原报告字节、登记SHA、资格和原邻域，构成576格六轴描述性网格。",'',
 '经济假设：前轮同时延长两币回看，不能区分哪一侧影响。本轮分别固定BTC32/ETH28和BTC31/ETH29，各H={2%,4%}、E={0,0.25%,0.5%,1%,1.5%,2%}的144格中，4个既有零/零退出组合只读、140格逐项先reserve再计算，共280新格。匹配同H/E的已完成BTC31/ETH28基准及BTC32/ETH29联合变化结果；全部576格均实际有结果，无网格外推、无后验扩张。新组合精确指纹首次评估，但组成路径和全330日数据早已见过。', '',
 '原值权重1/1表示一整份10000USDT的BTC独立抵押账本加一整份10000USDT的ETH账本，总初始本金20000。绝对NAV相加一次，权重不自动归一化，无转账、复投、再平衡或交叉保证金。各组件入场固定原始2000USDT，双活跃约4000=初始总资金20%；价格跳空及lot会改变实际比例。原rejected组件同样按事先固定网格纳入，不能先按结果过滤。', '',
 '完整规则：每日决策i仅用此前完整价格，ROC=C[i−1]/C[i−1−L]−1；严格ROC>H做多，ROC<−H做空，反向入场优先并先平旧再开新。其余区域已有多仓严格ROC>−E保留、空仓严格ROC<E保留，退出边界等号平仓；±H边界不新开，同向不调整实际数量。E<=H，E0使用既有零退出组件，未重复等价回测。下一UTC00:01原生分钟OPEN参考成交，数量按2000/此前完整close和lot取整，不看未来OPEN/NAV/未公布资金费。', '',
 'Walk-forward：8份真实永续分钟、小时mark、资金费及合约元数据Parquet，输入2025-09-16至2026-09-16。连续OOS2025-10-19UTC00:01至2026-09-14UTC00:01，共330日、11×30日。30日上下文及3日初始间隔，无拟合、无未来标签，标签purge不适用；L32首个信号使用C32/C0，L33不可用。现金、数量、费用和资金费跨折连续，终点计成本平仓。全曲线相加重算收益、整体DD、逐折、Sharpe及Calmar，不平均组件指标或逐折DD。', '',
 '资格继续使用各固定回看组内四个H/E轴的相邻索引联合邻域，最多36格；要求三档净正、1倍≥8/11正折、3倍全OOS混合NAV回撤≤25%、四轴局部三倍净正≥60%、1倍≥4组件往返、1倍毛参考价格PnL加资金费/执行成本≥2.5，无任一源负抵押、拒单或保证金代理越界、终点空仓。六轴576格及2112邻接边、Sharpe陡变仅描述，不能改资格、重评296个旧结果或证明独立稳健。1728成本行、19008折行含旧只读；278040新日NAV、840匹配比较、432四格分解行和两张四面板图全部保存。', '',
 '成本：每侧5bp手续费假设、1bp半价差、2bp滑点，加0.5×此前20完整日日log波动×sqrt(订单名义/此前20日quote ADV)冲击，参与率≤0.1%。Decimal28不利tick、原生lot/minNotional，开仓名义≤扣费后抵押1倍。线性永续开仓仅扣手续费，平仓实现带符号PnL，不能按现货扣掉名义本金；未借入现货。真实结算按−signedq×mark×rate事后记账，费率不用于信号或数量；执行成本和负资金费支出乘1/2/3，正资金费收入不放大。父层仅相加一次，不净额后压力化。', '',
 '[Binance资金费说明](https://www.binance.com/en/support/faq/detail/360033525031)和[Mark/Last及清算说明](https://www.binance.com/en/support/faq/detail/360033525271)于本轮重新读取，原实际资金费与mark输入不改。源1%维护保证金代理对完整OOS小时中每个持仓状态按多头low/空头high核验，各账本独立、另一币现金不抵销越界。混合分钟成交收盘代理、小时/结算mark、成交前后NAV不是逐tick mark风险，缺完整历史风险阶梯、过滤器、VIP费率、L2/排队/延迟/实盘TCA。', '',
 '[AQR原作者时序动量论文](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)只作传统12个月多期货背景，沿用同UTC日早轮读取，未在本轮重新请求。两组加密参数变化是单独开发假设。反复历史、多重试验、候选事后排序仍有限制，无未触碰最终留出、DSR/PBO、独立确认或稳定实盘盈利证明。', '',
 '单币变化与相同H/E旧基准比较：'+json.dumps(report['single_asset_lookback_tradeoff'],ensure_ascii=False),
 '四格分解：'+json.dumps(report['lookback_factorial'],ensure_ascii=False),
 '解释：BTC-only与ETH-only收益差在此固定本金、原值1/1的独立账本加法中严格相加，收益交互接近零是核算恒等式，不是发现市场独立或实盘因果。整体DD及Sharpe是非线性的，交互只作同段模拟对照。',
 '各成本576格不同完整NAV哈希数：'+json.dumps(report['distinct_NAV_paths_by_cost'],ensure_ascii=False)+'；不同参数可能产生相同离散路径，不能视作576次独立确认。',
 '失败标准计数（可能重叠）：'+json.dumps(report['failure_counts'],ensure_ascii=False),
 '与本组零/零退出对照：'+json.dumps(report['buffer_tradeoff'],ensure_ascii=False),
 f"新组事后最高{best['name']}：1/2/3倍"+'/'.join(f"{best['scenes'][k]['net_return_pct']:+.6f}%" for k in ['1','2','3'])+f"，完整DD3 {best['scenes']['3']['max_drawdown_pct']:.6f}%，1倍{best['positive_folds_1x']}/11正折，{best['status']}。收益排名与资格分开，不据排名自动替换冻结账户。", '',
 '同本金20000、各2000入场双恒多参考只读已有结果：1/2/3倍收益'+'/'.join(f"{report['readonly_hold_returns_by_cost'][k]:+.6f}%" for k in ['1','2','3'])+'。现金解析收益0；840行对照在hold_comparison.csv，未重复参考回测。', '',
 f"独立审计从{audit['source_recorded_trades_checked']}笔原存成交、{audit['source_recorded_funding_checked']}条原资金费（含空仓0）重建144条组件NAV，与源SHA逐点匹配；结构化时间键另一路核对840新父NAV、{audit['new_parent_NAV_points_audited']}点及10080整体/逐折指标。未调用组件simulate/target/trade/funding生成新源结果。", '',
 f"完整读取{ctx['registry_events']}事件、{ctx['registry_ids']}ID及{len(ctx['prior_conclusions_read'])}份既往结论。初始16条均有实际ZIP/WF或finish报告，5条legacy缺新版标志不当缺结果。280新配置先逐项reserve、按最终报告SHA逐项finish，正负和淘汰结果一并保留；旧296父、48源和144旧基准原报告及资格保持。", '',
 f"原冻结SMA从{fwd['resume_utc']}续至{fwd['cutoff_utc']}，120新增闭合分钟，无日决策/参考/成交/费用。旧{fv['original_NAV_prefix']}点精确前缀，各场景{fv['NAV_points_per_scene']}点，累计{fv['cumulative_minutes']}分钟。65日/1%浮点规则、1500/500、cash/units/desired、旧交易及成本不变；下一Oct25UTC00:01、终止2027-03-31保持。仅不足180日/六折的partial延迟shadow，不冒充十策略实时盘。", '']
 if passed:
  q=max(passed,key=lambda c:c['scenes']['3']['net_return_pct']);summary['highest_qualified']={'name':q['name'],'return3':q['scenes']['3']['net_return_pct'],'DD3':q['scenes']['3']['max_drawdown_pct'],'positive_folds1':q['positive_folds_1x']};lines.append(f"当前历史合格组最高{q['name']}，三倍{q['scenes']['3']['net_return_pct']:+.6f}%，DD3 {q['scenes']['3']['max_drawdown_pct']:.6f}%，正折{q['positive_folds_1x']}/11。仍待独立前向验证。")
 lines+=['','|BTC L/H/E|ETH L/H/E|1倍|2倍|3倍|正折1|DD3|四轴正3|状态|','|---|---|---:|---:|---:|---:|---:|---:|---|']
 for c in cs:
  s=c['scenes'];lines.append(f"|{c['BTC_lookback_days']}/{c['BTC_return_hurdle']:.0%}/{c['BTC_exit_buffer_fraction']:.2%}|{c['ETH_lookback_days']}/{c['ETH_return_hurdle']:.0%}/{c['ETH_exit_buffer_fraction']:.2%}|{s['1']['net_return_pct']:+.3f}%|{s['2']['net_return_pct']:+.3f}%|{s['3']['net_return_pct']:+.3f}%|{c['positive_folds_1x']}/11|{s['3']['max_drawdown_pct']:.3f}%|{c['sensitivity']['four_dimensional_local_3x_positive_fraction']:.1%}|{c['status']}|")
 lines+=['','固定cwd金融解释器audit.py、check_sources.py、forward.py --reproduce及audit_forward.py只审计已存结果，不重复reserve/评估或改已finish报告。必要完整JSON、280父archive/spec、原SMA完整9场景NAV/state/2原HTTP响应保留；48源完整账本只引用原路径/SHA。大行情留忽略data。只清理本轮可重建缓存和checkpoint；失败事实留原日志，不以cat退出码代替检查退出码。',''];(R/'result.md').write_text('\n'.join(lines));put(R/'summary.json',summary)
 (R/'forward_result.md').write_text('\n'.join(['# 原冻结SMA闭合分钟续接','',f"{fwd['resume_utc']}→{fwd['cutoff_utc']}，120新mark，旧{fv['original_NAV_prefix']}点精确前缀，新{fv['NAV_points_per_scene']}点，累计{fv['cumulative_minutes']}分钟。",'组合1/2/3倍累计收益'+ '/'.join(f"{fwd['configs']['forward_snapshot_combo']['scenes'][k]['net_return_pct']:+.9f}%" for k in ['1','2','3'])+'。','无新决策/参考/成交/费用，旧cash/units/desired及交易成本不变。下一Oct25UTC00:01和2027-03-31终止保持；partial观察不取消原计划，不是十策略实时报价盘。','2原HTTP响应、重叠bar/闭合性、源状态SHA、完整NAV及独立审计、精确重放全部保留。','']))
