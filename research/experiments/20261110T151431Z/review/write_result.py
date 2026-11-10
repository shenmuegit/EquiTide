"""Chinese wider S/D report from saved actual evidence; no strategy valuation."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));from common import sha,put,rel
rd=lambda n:json.loads((R/n).read_text())
p,r,v,ctx,a,feed,transport,fund,t=[rd(n) for n in ['plan.json','report.json','verification.json','context.json','same_bank_realized_NAV_alias_diagnostic.json','feed_verification.json','transport_failure_verification.json','current_actual_nov10_08_funding_verification.json','prior_actual_research_counts.json']]
cs=list(r['configs'].values());parents=[c for c in cs if c['scope']=='parent'];passed=[c for c in parents if c['status']=='passed'];preset=p['representative_preset'];rep=next(c for c in parents if all(c[k]==preset[k] for k in ['S','D','H','E','K','VC','R','M','VW']));center=r['read_only_grid'][p['current_center']['parent']];best=max(parents,key=lambda c:c['scenes']['3']['net_return_pct']);negative=[c for c in cs if all(c['scenes'][k]['net_return_pct']<0 for k in ['1','2','3'])]
assert len(cs)==16 and len(passed)==len(r['summary']['passed']) and fund['own_current_funding_records']=={'candidate':0,'l4h02':0,'fewm':0}
body=[]
def para(s):body.extend([s,''])
para(f"完成宽S/D批次16项/48个成本场景：{len(passed)}/8个父组合历史通过，3个D1组合及8个ETH组件淘汰。{len(negative)}个ETH定义在三档成本下全期均净负，完整结果永久保留。预设代表S16/D1三倍收益{rep['scenes']['3']['net_return_pct']:.6f}%、连续整体回撤{rep['scenes']['3']['max_drawdown_pct']:.6f}%，未通过月度/近期一致性。事后高收益格S{best['S']}/D{best['D']}三倍收益{best['scenes']['3']['net_return_pct']:.6f}%、整体DD{best['scenes']['3']['max_drawdown_pct']:.6f}%；它提高收益，也扩大回撤，非稳定实盘盈利证明。")
para(p['hypothesis'])
para(f"完整读取{ctx['registry_events']}事件/{ctx['registry_ids']}ID和{len(ctx['prior_conclusions_read'])}份既往结论。初始16项证据齐全（11正式+5旧ZIP实际回测），无缺实际结果项；5个legacy标志与历史文件不改。此前规范研究定义{t['canonical_prior_research_definitions']}，标实际{t['registry_marked_actual']}、未标实际{t['not_marked_actual']}，不能声称所有登记都完成验证。16项完整参数/数值组件图查重、保存spec、成功reserve后才算，全部finish；10个旧源结果和旧S16/D3中心只读。另12个原账户真实观察，共28ID/56事件。")
para("规则只变有限EWM窗口S=[12,16,20]及斜率滞后D=[1,3,5]。每个S采用beta=(S−1)/(S+1)，最近S个已完成日收盘归一化有限均值与D日前同窗口均值相比。固定ROC5/H2%/E0.75%、斜率K0.75%、价格样本logvol V10/上限5%，严格边界、同向实际数量保留、反手先平旧仓及下一UTC00:01 OPEN执行均保持。351个Fraction/Horner合成检查覆盖长度、衰减、滞后、边界、持仓/反手、未来数据隔离与固定预算不变性，4项预期RED单列。仅decide的S/D可接受域改变，其余函数AST保持。")
para("ETH最大信号上下文25日（20+5）、成本21日、预算需9个收盘；BTC需30日。33日源上下文足够，无未来初始化。没有模型拟合/标签/purge/embargo；开发历史已经反复使用，不能称未触碰最终测试集。")
para("资金费固定为UTC00:00信号前可用、结算年龄1–36小时的最新4笔SIGNED实际费率，取中间两项均值；max(原方向×median,0)≤min(0.0002,0.00875×过去8日样本logvol×最新成熟真实结算间隔小时/24)。间隔取最新合格fundingTime与直接上一笔真实时间之差，双方信号时可得并保留毫秒抖动；归一化名义8小时不是实测间隔。缺记录/间隔只阻止新开/反手。每资产1212笔实际资金费及370次成熟来源选择核验。available_ts=结算后1小时是保守假设，非网络到达实测，过去费率不是未来费率。")
para("组合使用旧BTC29/H3%/E1%银行3750、N1000完整路径及新ETH银行15000、N4500逐项实际数量/LOT、成本、冲击、资金费、抵押/保证金代理和全NAV。raw[1,1]相加完整独立银行，总本金18750；20%/80%是资本份额，不再次加权、不归一化、不缩放NAV、不转移资金、不再平衡、不下父订单、无交叉抵押。旧预算、无过滤同C/N、同期常持有和现金0%对照均保存；多参数不同的对照仅作描述，不能把全部差异归因于资金费过滤。")
para("Walk-forward完成：2025-10-19 UTC00:01至2026-10-24 UTC00:01连续370日，12个30日完整折+10日尾；近期40日继承day330现金/仓位，分8个5日折，不折间重开。8份真实归一化输入的版本、SHA256、边界和必要原始数据留档。624逐折、384近期折、17808日净值行及完整连续净值整体DD保存；终点平仓含成本。重复开发和多重选择偏差保留，不称独立未来确认。")
para("敏感性完成：原生/父组合各9格（8新+1旧中心），72邻接边，净收益、整体DD、Sharpe、Calmar及三档成本完整保存。D1父组合只有7/7/8个盈利月、近期各档5/8正折，局部严格近期不足；其余5个新组合符合原门槛。ETH近期0–2/8正折、局部严格近期比例0，全8项淘汰，部分另有全期亏损、月数、平仓数或成本安全边际不足。原生7/9格Sharpe正、组合9/9格正，仍有明显邻接跳变；收益峰值位于S20/D5边界，不是稳定平台。旧中心canonical资格与旧敏感性不改，本轮诊断分存。")
para("成本1/2/3倍完成：每边手续费5bp+半价差1bp+滑点2bp，冲击=0.5×过去20日样本logvol×sqrt(实际abs(q)×原生OPEN/过去20日quoteADV)。执行成本和资金费支出随倍数放大，正资金费收入不放大。线性永续不借现货，逐笔真实time/rate/mark乘各自实际持仓，检查LOT/tick/minnotional、≤0.1%参与率、费后1倍抵押及1%闭合小时不利mark维护保证金代理。缺真实L2/TCA、完整历史风险档位/逐tick强平及真实容量证据。")
para("门槛不改：各成本全期/近期净正，1x≥9/12正完整月折，近期各档≥6/8正5日折，3x整体DD≤25%，局部3x净正及严格近期比例≥60%，≥4次原生平仓，毛价格PnL加净资金费/1x成本≥2.5，无抵押/订单/风险代理违规，终点flat且≥180日。不因正收益放宽门槛。")
body.extend(['|范围|S|D|1x净%|2x净%|3x净%|3x整体DD%|月正/12|近期正折1/2/3|状态|','|---|---:|---:|---:|---:|---:|---:|---:|---|---|'])
for c in cs+list(r['read_only_native_grid'].values())+list(r['read_only_grid'].values()):
 body.append('|'+ '|'.join([c['scope']+('旧中心' if c.get('readonly') else ''),str(c['S']),str(c['D']),*[f"{c['scenes'][k]['net_return_pct']:.6f}" for k in ['1','2','3']],f"{c['scenes']['3']['max_drawdown_pct']:.6f}",str(sum(z['net_return_pct']>0 for z in c['scenes']['1']['folds'][:12])),'/'.join(str(sum(z['net_return_pct']>0 for z in c['scenes'][k]['recent40']['folds'])) for k in ['1','2','3']),c['status']])+'|')
para('')
para(f"逐项淘汰理由：{ {c['name']:c['failed_criteria'] for c in cs if c['failed_criteria']} }。")
para(f"独立审计通过：24新原生+24新父组合+18旧成本曲线，8880次新决策、{v['counts']['funding']}条资金费、{v['counts']['fills']}笔成交、{v['counts']['metric_checks']}项全期/逐月指标、{v['counts']['margin_checks']}项风险检查，0订单拒绝。独立Fraction/Horner、实际数量/成本/现金流、完整NAV及逐折/整体DD重建，不调用新simulate/decide/trade。")
para(f"完整旧路径比较{a['prior_native_definitions_compared']}个同C/N原生定义、{a['prior_parent_definitions_compared']}个父组合，16项中{a['new_allcost_signatures_seen_in_prior_results']}项三档全路径此前出现。具体源与内部别名见NAV哈希诊断；不同实参各自登记，路径别名不是独立盈利样本。")
para(f"事后比较S{best['S']}/D{best['D']}：3x收益{best['scenes']['3']['net_return_pct']:.6f}%高于旧中心{center['scenes']['3']['net_return_pct']:.6f}%，整体DD{best['scenes']['3']['max_drawdown_pct']:.6f}%也高于旧中心{center['scenes']['3']['max_drawdown_pct']:.6f}%，不构成收益和回撤同时改善。该描述不替换预设S16/D1及其淘汰结论，不新增试验或宣称独立最优。")
para("原账户本窗仅闭合mark/risk：SMA/single Nov10 10:30–12:30，L4/FEWM12:10–14:10，0新资金费、日决策、成交。保持原现金、q、desired、成本、风险及完整NAV，不重开、不加本金、不采用研究规则。全链Nov10_00、08及原日决策各自一次，本窗不重复08，原公开字段/检索UTC/SHA保留。")
for stem,label in [('forward','SMA'),('candidate','single'),('l4h02','L4'),('fewm','FEWM')]:
 z=rd(stem+'_verification.json');before=z['original_NAV_prefix'] if stem=='forward' else z['prior_NAV_prefix'];elapsed=z['cumulative_minutes'] if stem=='forward' else z['elapsed_minutes'];para(f"{label}完整NAV前缀{before}→{z['NAV_points_per_scene']}，累计{elapsed}分钟；原账本与风险连续性独立核验。")
para("原SMA负收益及全部partial淘汰结果保留，继续原长期计划；这些是未成熟延迟shadow，不等同paper10十策略真实报价模拟或180日前向资格。SMA日上下文仍为031055轮65个完整SPOT日、截至Nov10 UTC00:00，当前minute数组不能替换日上下文。")
para("下轮SMA/single12:30–14:30只mark；L4/FEWM14:10–16:10跨16 UTC，须等16:11参考闭合、取得新的真实Nov10_16 fundingTime/rate/mark，并在绑定/reserve前核对，再按各自原q/现金结算一次。旧funding16_current_preflight是Nov9，不能替代Nov10或复制他人现金流；本轮未预抓取未来费率/时间，也未预测入账。将来single自己的14:30–16:30窗口跨16时可复用已验证公共字段，但用自己的持仓。下一日事件Nov11 UTC00:01，SMA届时从当前Float状态延续并刷新65日SPOT。")
para("下一方向提案未执行：固定资金费M4/VW8/R0.00875及EWM S16/D3/K0.75%、H2%/E0.75%/VC5%，检验快ROC窗口L=[4,5,6]×价格波动窗口V=[8,10,12]。L5/V10旧中心只读，其余先全登记簿/数值图查重；完整代码/spec及Fraction ROC、样本logvol、持仓/反手、因果/上下文检查后reserve。PRICE_V与资金费BUDGET_VW8独立，成本21日、趋势19日、BTC30日应由33日源覆盖但须复核。资本/名义金额/raw权重/时间/门槛不改，不预认改善，不建新冻结账户。")
monitor='原生生成及检查通过' if feed.get('monitor_generation_succeeded',True) else '原生检查失败，按任务保留上次有效快照'
para(f"只读监控：{monitor}；{feed['research_configs']}研究行、旧{feed['historical_rows_identical']}行保持，paper10共{feed['paper_accounts']}账户/{feed['paper_observations']}观察，gzip为{(ROOT/'research/monitor/configs.json.gz').stat().st_size}字节。原生回执留档，没有重部署或新建任务。十策略本轮失败由其自身留档，研究任务不重跑其窗口、不重置其账户。")
para(f"真实失败保留：准备/检查记录{len(rd('read_failures.json')['facts'])}项，HTTP/传输失败{transport['observed_actual_HTTP_or_transport_failures']}次。报告候选文本的一处引号错误在写文件前被compile拒绝，修正后再核验，原错误回执留档，实际回测/报告原字节保持。提交前空白门禁又发现文档末尾多余空行，首次封存与失败回执已完整归档；规范末尾空白后重新封存，金融结果不改。实际失败响应（含空响应）、stderr、原bounded重试均保存，TLS验证未关闭。4项预期合成RED分列；完整策略与已完成观察没有重跑。")
para("继承print或派生键名中的旧K/VC、H/E、VW/R及16资金费标签见derived_label_correction，以冻结S/D完整spec、绑定代码、逐笔/全NAV与独立核验为准；已finish报告不改写。复现argv/cwd/UTC/退出码见reproduction_history及commands/receipt，必要数据哈希、全部结果与账户账本保留，可重建中间文件清理。")
para('main排他锁内完成登记、核验、只读快照与封存；普通非force提交推送后核对远端ref、完整tree/blob及三条永续链，再释放锁。实际终态见.git/automation_proofs/'+R.name+'.json，本文不单独作为push成功证明。')
(R/'result.md').write_text('\n'.join(body).rstrip()+'\n')
put(R/'reproduction_history.json',{'working_directory':str(ROOT),'pipeline_commands':{f.name:json.loads(f.read_text()) for f in sorted(R.glob('*_commands.json'))},'review_receipts':{f.name:json.loads(f.read_text()) for f in sorted(R.glob('review_*_receipt.json'))},'bootstrap':rd('bootstrap_receipt.json'),'source_binding':rel(R/'code_binding_before_evaluation.json'),'all_new_financial_evaluations':1,'completed_account_window_reruns':0,'data_sources':p['data'],'historical_and_original_account_rules_not_modified':True})
