"""Export saved real native/parent L/D results; no strategy calculation."""
import collections,csv,json,statistics
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import *
r=json.loads((R/'report.json').read_text());p=json.loads((R/'plan.json').read_text());rows={}
def write(name,cols,items):
 with(R/name).open('w',newline='') as f:w=csv.writer(f,lineterminator='\n');w.writerow(cols);w.writerows(items)
 rows[name]=len(items)
cost=[];wf=[];recent=[];daily=[];edges=[];alloc=[];sources=[]
for c in r['configs'].values():
 for k,s in c['scenes'].items():
  cost.append([c['name'],c['fingerprint'],c['scope'],c['role'],c['asset'],c['L'],c['D'],c['capital_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['cost_usdt'],s['cost_pct_initial'],s['funding_usdt'],s['gross_reference_PnL_to_execution_cost'],s['executions'],s['round_trips'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),c['status']])
  wf.extend([c['name'],c['scope'],c['L'],c['D'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['duration_days'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['folds'])
  recent.extend([c['name'],c['scope'],c['L'],c['D'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['recent40']['folds'])
  daily.extend([c['name'],c['scope'],k,i,v] for i,v in enumerate(s['daily_equity_usdt']))
write('cost_scenes.csv',['configuration','fingerprint','scope','role','asset','ETH_fast_L','max_holding_days_D','initial_capital','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','cost_usdt','cost_pct_initial','funding_usdt','gross_plus_funding_to_cost','executions','closes','recent40_return_pct','positive5d_folds','status'],cost)
write('walk_forward_folds.csv',['configuration','scope','ETH_fast_L','max_holding_days_D','cost_multiplier','fold','start_utc','end_exclusive_utc','days','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],wf)
write('recent40_folds.csv',['configuration','scope','ETH_fast_L','max_holding_days_D','cost_multiplier','fold','start_utc','end_exclusive_utc','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],recent)
write('daily_NAV.csv',['configuration','scope','cost_multiplier','boundary','NAV_usdt'],daily)
cols=['ETH_fast_L','max_holding_days_D','fingerprint','readonly_old','unchanged_canonical_status','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','recent40_return_pct','positive5d_folds','local_positive3_fraction','local_recent_fraction'];flags={};readonly=[]
for scope,grid,key in [('parent',p['grid'],'all_current_grid'),('native',p['native_grid'],'all_current_native_grid')]:
 full=r[key];items=[]
 for g in grid:
  c=full[g['fingerprint']]
  for k,s in c['scenes'].items():
   d=c['current_grid_diagnostic_sensitivity'];z=[g['L'],g['D'],g['fingerprint'],g['readonly'],c['status'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),d['local_positive3_fraction'],d['local_strict_recent_fraction']];items.append(z)
   if scope=='parent' and g['readonly']:readonly.append(z)
 for k in ['1','2','3']:
  for g in grid:
   i,j=p['lookbacks'].index(g['L']),p['holding_limits'].index(g['D']);ng=[h for h in grid if i<2 and h['L']==p['lookbacks'][i+1] and h['D']==g['D'] or j<2 and h['D']==p['holding_limits'][j+1] and h['L']==g['L']]
   for h in ng:
    a,b=full[g['fingerprint']]['scenes'][k],full[h['fingerprint']]['scenes'][k];edges.append([scope,k,g['L'],g['D'],h['L'],h['D'],g['fingerprint'],h['fingerprint'],abs(a['sharpe_365']-b['sharpe_365']),abs(a['net_return_pct']-b['net_return_pct']),abs(a['max_drawdown_pct']-b['max_drawdown_pct'])])
 flags[scope]={}
 for k in ['1','2','3']:
  v=[x[8] for x in edges if x[0]==scope and x[1]==k];t=2*statistics.stdev(v);flags[scope][k]={'edge_count':len(v),'max_Sharpe_change':max(v),'two_std_change_threshold':t,'descriptive_cliff_flag':max(v)>t,'scope':'Dependentedgeheuristiconly,notstatisticalsignificance,DSRorPBO.'}
 write('sensitivity_grid.csv' if scope=='parent' else 'native_sensitivity_grid.csv',cols,items)
write('readonly_reused_scenes.csv',cols,readonly)
write('adjacent_edges.csv',['scope','cost_multiplier','from_L','from_D','to_L','to_D','from_fp','to_fp','absolute_Sharpe_change','absolute_return_change_pp','absolute_DD_change_pp'],edges)
cs=r['matched_hold_comparisons'];write('matched_hold_comparisons.csv',list(cs[0]),[list(x.values()) for x in cs])
for fp,x in p['read_only_references'].items():
 if x['scope']!='native':continue
 sp=json.loads((ROOT/x['spec']).read_text());old=next(c for c in json.loads((ROOT/x['report']).read_text())['configs'].values() if c['fingerprint']==fp)
 for k,s in old['scenes'].items():sources.append([fp,x['asset'],x['capital_usdt'],sp['parameters']['fixed_entry_notional_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['cost_usdt'],s['funding_usdt'],s['executions'],s['NAV_sha256_f64le'],x['report'],x['report_sha256']])
write('source_curves.csv',['fingerprint','asset','actual_bank_capital','actual_entry_N','cost_multiplier','return_pct','whole_DD_pct','cost_usdt','funding_usdt','executions','NAV_sha256','readonly_report','readonly_report_sha256'],sources)
for g in p['grid']:alloc.append([g['fingerprint'],'candidate',g['L'],g['D'],3750,15000,18750,375,4500,1,1,.2,.8,g['readonly']])
alloc.append([p['benchmark_parent_fingerprint'],'matched_initial_budget_hold',None,None,3750,15000,18750,375,4500,1,1,.2,.8,True]);write('fixed_allocations.csv',['fingerprint','role','ETH_L','max_holding_days_D','BTC_bank','ETH_bank','total_initial_capital','BTC_N','ETH_N','raw_BTC_weight','raw_ETH_weight','BTC_capital_share','ETH_capital_share','readonly'],alloc)
put(R/'edge_flags.json',flags)
fig,axs=plt.subplots(2,4,figsize=(16,9),layout='constrained')
for row,(scope,key) in enumerate([('ETH native15000/N4500','all_current_native_grid'),('BTC3750+ETH15000 parent','all_current_grid')]):
 full=r[key]
 for j,(label,fn) in enumerate([('3x continuous370 return %',lambda c:c['scenes']['3']['net_return_pct']),('3x wholecurve DD %',lambda c:c['scenes']['3']['max_drawdown_pct']),('3x daily Sharpe365',lambda c:c['scenes']['3']['sharpe_365']),('3x recent positive5d /8',lambda c:sum(f['net_return_pct']>0 for f in c['scenes']['3']['recent40']['folds']))]):
  arr=np.empty((3,3))
  for c in full.values():arr[p['lookbacks'].index(c['L']),p['holding_limits'].index(c['D'])]=fn(c)
  ax=axs[row,j];im=ax.imshow(arr,cmap='RdYlGn_r' if j==1 else 'RdYlGn',**({'vmin':0,'vmax':8} if j==3 else {}));ax.set_xticks(range(3),['3 days','7 days','OFF old']);ax.set_yticks(range(3),['L3','L4','L5']);ax.set_xlabel('Maximum actual ETH holding days D');ax.set_ylabel('ETH fast lookback L');ax.set_title(scope+'\n'+label,fontsize=10)
  for c in full.values():i,k=p['lookbacks'].index(c['L']),p['holding_limits'].index(c['D']);ax.text(k,i,f'{arr[i,k]:.3f}'+(' O' if c['readonly'] else ' N'),ha='center',va='center',fontsize=9)
  fig.colorbar(im,ax=ax,shrink=.7)
fig.suptitle('ETH fastL3/4/5 x maximum holding3/7days/OFF, fixed slowS28, fixedH2.5%, E0.25%, V10/cap4.5%\nActualBTC3750/N375 andETH15000/N4500 | rawweights[1,1],shares20/80%,noNAVscaling | O=readonly,N=new | reuseddevelopmenthistory')
fig.savefig(R/'sensitivity.png',dpi=140);plt.close(fig)
s={'report_sha256':sha(R/'report.json'),**p['expected_counts'],'passed':len(r['summary']['passed']),'rejected':len(r['summary']['candidate_rejected']),'failed_criteria':dict(collections.Counter(f for c in r['configs'].values() for f in c['failed_criteria'])),'CSV_rows':rows,'edge_flags':flags};put(R/'sensitivity_summary.json',s)
ctx=json.loads((R/'context.json').read_text());eq=[]
for c in r['configs'].values():
 grid=p['native_grid'] if c['scope']=='native' else p['grid'];key='all_current_native_grid' if c['scope']=='native' else 'all_current_grid';off=next(g for g in grid if g['L']==c['L'] and g['D'] is None);base=r[key][off['fingerprint']]
 eq.append({'name':c['name'],'fingerprint':c['fingerprint'],'scope':c['scope'],'L':c['L'],'D':c['D'],'matched_unlimited_fingerprint':off['fingerprint'],'identical_full_NAV_by_cost':{k:c['scenes'][k]['NAV_sha256_f64le']==base['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3']},'all_cost_NAV_identical':all(c['scenes'][k]['NAV_sha256_f64le']==base['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3']),'cost_comparisons':{k:{'return_pct':c['scenes'][k]['net_return_pct'],'whole_DD_pct':c['scenes'][k]['max_drawdown_pct'],'OFF_return_pct':base['scenes'][k]['net_return_pct'],'OFF_DD_pct':base['scenes'][k]['max_drawdown_pct'],'delta_return_to_OFF_pp':c['scenes'][k]['net_return_pct']-base['scenes'][k]['net_return_pct'],'delta_DD_to_OFF_pp':c['scenes'][k]['max_drawdown_pct']-base['scenes'][k]['max_drawdown_pct']} for k in ['1','2','3']}})
put(R/'equivalent_realized_NAV_paths.json',{'report_sha256':sha(R/'report.json'),'comparisons':eq,'policy':'Finite duration differs as a rule even if no extra expiry changes this realized sample; identical fullNAV aliases disclosed, not independent alpha. OFF canonical results/statuses unchanged and policies not rerun.'})
lines=['# ETH 最大实际持仓期限验证','',f"完整读取{ctx['registry_events']}事件/{ctx['registry_ids']}ID和{len(ctx['prior_conclusions_read'])}份结论；排除持续观察后的历史研究定义数{ctx['canonical_research_definitions_excluding_observations']}。初始16项均有实际证据，不重跑已完成配置。本轮6个新ETH原生与6个新父组合、36成本场景均逐项reserve成功后实际计算，所有正负期间与结果留档。",'',p['hypothesis'],'',
'预设两轴：ETH快回望L=[3,4,5]，最长实际持仓D=[3天,7天,None=不限制]。H=0.025、E=+0.0025、S28方向始终门控、V10样本logvol上限0.045固定。OFF三个ETH与三个父、BTC和匹配持有父/两原生共10唯一旧结果只读；有限期限六原生与六父为新定义。旧pairOLS720配对研究曾用48小时上限，规则、资金和市场模型不同，不能据策略族/期限概念相同排除此批；完整spec指纹逐项查重。','',
'完整价格信号不变：ETH fastROC=C[i−1]/C[i−1−L]−1，严格>H空、<−H多；带内实际多仅ROC<E、实际空仅ROC>−E保留，等号退出。绝对slow28方向不匹配退出，V10波动>4.5%只过滤新开/翻向。之后实际非零持仓日龄>=D时强制desired=0，无论原目标同向或翻向：当前日决策先平仓并保持空仓，禁止当次重开/翻向；下一日可按原信号再入场。更早原退出/翻向照常，BTC无新期限。','',
'日龄来自本币本成本场景最近一次成功原生开仓的UTC日索引，到当前00:01决策的整日差；原生开仓和平仓都在00:01，因此到期边界对应实际72/168小时。只在成功成交时更新开仓日期，拒单不重置；实际持仓/日龄跨walk-forward折保持。00资金费若先于00:01平仓，仍按真实持仓支付/收取，不能因即将到期免计。终止平仓照常计成本，不为研究窗口平仓冻结账户。','',
'经济假设是限制陈旧信号的价格与资金费暴露；代价可能是更高换手和错过后续利润。3天/7天期限在结果前固定，不利用近期收益调整持仓日龄、重新选择门槛或宽限6/8近期要求。没有新资金费信号、BTC残差或慢趋势幅度过滤。','',
'资金及原权重：BTC真实银行3750/N375旧ROC31/H4%/E1%曲线只读，ETH15000/N4500独立原生数量/冲击/抵押实际重测。总初始18750，原[1,1]直接相加两银行美元NAV，20%/80%仅初始本金份额，不再次乘权重或自动归一化；初始总名义4875=26%本金。固定N/前完整close按LOT向下取整，下一00:01原生OPEN不利tick，普通翻向先平后开，同向保留实际q。无父调仓、转账、跨抵押、复利调N或线性缩放旧路径。','',
'按时间验证：2025-10-19UTC00:01至2026-10-24UTC00:01连续370天，12完整30日折+10日尾折；现金、数量、费用及开仓日龄跨折不重置，全分钟/事件NAV计算整体回撤。近期40天固定day330与8×5日折。无拟合/标签，purge0、预热30+间隔3，ADV和波动仅前20完整日。该历史经过大量反复开发，全部试验数留档，不称未触碰最终留出、独立未来资格或DSR/PBO显著性。','',
'1/2/3倍成本：每边5bp费用、1bp半价差、2bp滑点及0.5×past20样本logvol×sqrt(实际q×OPEN/past20完整quoteADV)冲击。所有到期平仓及下一日重开均真实付费；真实资金费按settlement/rate/mark/heldq入账，支出倍增、收入不放大。原生LOT/tick/minnotional、参与率<=0.001、费用后1倍抵押、各银行独立1%闭合小时不利mark维护代理均核验。线性永续无现货借币，不虚构借币费；缺L2/TCA、完整历史档位与逐tick清算/容量证明。匹配本金及初始N持有和现金0%并列，非满仓或同风险持有。','',
'固定失败门槛：每成本全年净正，1倍至少9/12正完整月；每成本近期净正且至少6/8正5日折；3倍整体DD<=25%；L/D索引半径1含中心邻域的3倍净正与严格近期支持均>=60%；至少4平仓，毛参考价格PnL加fund/执行成本>=2.5；零拒单/负抵押/小时维护代理违规，终止flat且>=180天。新原生与父独立判断，OFF原资格/报告不变，当前邻域诊断另列。D=[3,7,None]邻域采用预声明索引，不把None解释为0天。','',
'|新配置|范围|L|期限天|1倍净%|2倍净%|3倍净%|3倍整体DD%|正月/12|近期正折1/2/3倍|状态|','|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|']
for c in r['configs'].values():
 lines.append('|'+c['name']+'|'+c['scope']+f"|{c['L']}|{c['D']}|"+'|'.join(f"{c['scenes'][k]['net_return_pct']:.6f}" for k in ['1','2','3'])+f"|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['positive_complete_30d_folds_1x']}|"+'/'.join(str(c['recent40_positive_5d_folds_by_cost'][k]) for k in ['1','2','3'])+'|'+c['status']+'|')
lines.extend(['',f"新父历史通过{len(r['summary']['passed'])}、淘汰{len(r['summary']['candidate_rejected'])}。逐项失败判据{ {c['name']:c['failed_criteria'] for c in r['configs'].values()} }。年度正收益不能代替近期、月折和邻域门槛。",'',f"同L匹配OFF三成本完整NAV全同{sum(z['all_cost_NAV_identical'] for z in eq)}/{len(eq)}；逐成本收益/DD及来源hash见equivalent_realized_NAV_paths.json。新参数不等于独立alpha，同路径别名明确披露，不删结果或改旧资格。",'',
'11CSV保存36场景、逐月/尾折/近期折、每日NAV、两个9格完整敏感性面、72相邻边、持有/现金、旧来源与原分配。两面八指标图分别显示收益/全曲线DD/Sharpe/近期正折；Sharpe正格比例、边界峰值、描述性2std悬崖另列，不作为显著性。CSV空期限值表示OFF不限制，不是缺失结果。','',
'合成TDD先确认旧decide接口不接受实际日龄而红灯；加入期限后验证L3/4/5×3/7/OFF、年龄2/3/6/7/8边界、多空到期、当次不翻向、下一次正常开仓、原更早退出、未来bar追加不变、非法日龄与vol边界。独立审核从保存的成功开仓成交时间戳推导entry_day，核对决策真实时间戳/日龄及过期平仓优先级，再用Fraction重算信号、Decimal重建成交、费用、资金费、小时风险及完整NAV；不调用simulate/decide/trade重新回测。','',
'原冻结账户单独续接：SMA及singleS28从Nov2UTC00:30至02:30，Nov2零点日决策/资金费已完成，不重复。独立未过滤L4/H2从02:10至04:10，仅04:11参考闭合后采集。全部保留cash/q/desired/risk/上下文/NAV前缀，不注入本轮持仓期限，不用部分延迟shadow替代十策略真实报价模拟，未取消长期计划或新建账户。','',
'官方一手资料实际访问2026-11-02：[Binance市场数据API](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)。原生bars/mark/funding/约束8文件hash与边界见plan/data_manifest；API文档不证明期限策略盈利或历史网络到达时间。本轮期限假设与可得时间局限单列。','',
'同main排他锁内逐项finish、检查、生成只读监控、提交非强制push。汇总不生成交易、不改冻结规则/本金/持仓、不部署网页或新建定时任务。不下真实订单，正回测不称稳定实盘盈利。'])
(R/'result.md').write_text('\n'.join(lines)+'\n');print(json.dumps(s),flush=True)
