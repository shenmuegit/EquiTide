"""Export saved real native/parent L/N results; no strategy calculation."""
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
  cost.append([c['name'],c['fingerprint'],c['scope'],c['role'],c['asset'],c['L'],c['N'],c['capital_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['cost_usdt'],s['cost_pct_initial'],s['funding_usdt'],s['gross_reference_PnL_to_execution_cost'],s['executions'],s['round_trips'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),c['status']])
  wf.extend([c['name'],c['scope'],c['L'],c['N'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['duration_days'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['folds'])
  recent.extend([c['name'],c['scope'],c['L'],c['N'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['recent40']['folds'])
  daily.extend([c['name'],c['scope'],k,i,v] for i,v in enumerate(s['daily_equity_usdt']))
write('cost_scenes.csv',['configuration','fingerprint','scope','role','asset','ETH_fast_L','funding_mean_window_N','initial_capital','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','cost_usdt','cost_pct_initial','funding_usdt','gross_plus_funding_to_cost','executions','closes','recent40_return_pct','positive5d_folds','status'],cost)
write('walk_forward_folds.csv',['configuration','scope','ETH_fast_L','funding_mean_window_N','cost_multiplier','fold','start_utc','end_exclusive_utc','days','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],wf)
write('recent40_folds.csv',['configuration','scope','ETH_fast_L','funding_mean_window_N','cost_multiplier','fold','start_utc','end_exclusive_utc','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],recent)
write('daily_NAV.csv',['configuration','scope','cost_multiplier','boundary','NAV_usdt'],daily)
cols=['ETH_fast_L','funding_mean_window_N','fingerprint','readonly_old','unchanged_canonical_status','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','recent40_return_pct','positive5d_folds','local_positive3_fraction','local_recent_fraction'];flags={};readonly=[]
for scope,grid,key in [('parent',p['grid'],'all_current_grid'),('native',p['native_grid'],'all_current_native_grid')]:
 full=r[key];items=[]
 for g in grid:
  c=full[g['fingerprint']]
  for k,s in c['scenes'].items():
   d=c['current_grid_diagnostic_sensitivity'];z=[g['L'],g['N'],g['fingerprint'],g['readonly'],c['status'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),d['local_positive3_fraction'],d['local_strict_recent_fraction']];items.append(z)
   if scope=='parent' and g['readonly']:readonly.append(z)
 for k in ['1','2','3']:
  for g in grid:
   i,j=p['lookbacks'].index(g['L']),p['funding_windows'].index(g['N']);ng=[h for h in grid if i<2 and h['L']==p['lookbacks'][i+1] and h['N']==g['N'] or j<2 and h['N']==p['funding_windows'][j+1] and h['L']==g['L']]
   for h in ng:
    a,b=full[g['fingerprint']]['scenes'][k],full[h['fingerprint']]['scenes'][k];edges.append([scope,k,g['L'],g['N'],h['L'],h['N'],g['fingerprint'],h['fingerprint'],abs(a['sharpe_365']-b['sharpe_365']),abs(a['net_return_pct']-b['net_return_pct']),abs(a['max_drawdown_pct']-b['max_drawdown_pct'])])
 flags[scope]={}
 for k in ['1','2','3']:
  v=[x[8] for x in edges if x[0]==scope and x[1]==k];t=2*statistics.stdev(v);flags[scope][k]={'edge_count':len(v),'max_Sharpe_change':max(v),'two_std_change_threshold':t,'descriptive_cliff_flag':max(v)>t,'scope':'Dependentedgeheuristiconly,notstatisticalsignificance,DSRorPBO.'}
 write('sensitivity_grid.csv' if scope=='parent' else 'native_sensitivity_grid.csv',cols,items)
write('readonly_reused_scenes.csv',cols,readonly)
write('adjacent_edges.csv',['scope','cost_multiplier','from_L','from_N','to_L','to_N','from_fp','to_fp','absolute_Sharpe_change','absolute_return_change_pp','absolute_DD_change_pp'],edges)
cs=r['matched_hold_comparisons'];write('matched_hold_comparisons.csv',list(cs[0]),[list(x.values()) for x in cs])
for fp,x in p['read_only_references'].items():
 if x['scope']!='native':continue
 sp=json.loads((ROOT/x['spec']).read_text());old=next(c for c in json.loads((ROOT/x['report']).read_text())['configs'].values() if c['fingerprint']==fp)
 for k,s in old['scenes'].items():sources.append([fp,x['asset'],x['capital_usdt'],sp['parameters']['fixed_entry_notional_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['cost_usdt'],s['funding_usdt'],s['executions'],s['NAV_sha256_f64le'],x['report'],x['report_sha256']])
write('source_curves.csv',['fingerprint','asset','actual_bank_capital','actual_entry_N','cost_multiplier','return_pct','whole_DD_pct','cost_usdt','funding_usdt','executions','NAV_sha256','readonly_report','readonly_report_sha256'],sources)
for g in p['grid']:alloc.append([g['fingerprint'],'candidate',g['L'],g['N'],3750,15000,18750,375,4500,1,1,.2,.8,g['readonly']])
alloc.append([p['benchmark_parent_fingerprint'],'matched_initial_budget_hold',None,None,3750,15000,18750,375,4500,1,1,.2,.8,True]);write('fixed_allocations.csv',['fingerprint','role','ETH_L','funding_mean_window_N','BTC_bank','ETH_bank','total_initial_capital','BTC_N','ETH_N','raw_BTC_weight','raw_ETH_weight','BTC_capital_share','ETH_capital_share','readonly'],alloc)
put(R/'edge_flags.json',flags)
fig,axs=plt.subplots(2,4,figsize=(16,9),layout='constrained')
for row,(scope,key) in enumerate([('ETH native15000/N4500','all_current_native_grid'),('BTC3750+ETH15000 parent','all_current_grid')]):
 full=r[key]
 for j,(label,fn) in enumerate([('3x continuous370 return %',lambda c:c['scenes']['3']['net_return_pct']),('3x wholecurve DD %',lambda c:c['scenes']['3']['max_drawdown_pct']),('3x daily Sharpe365',lambda c:c['scenes']['3']['sharpe_365']),('3x recent positive5d /8',lambda c:sum(f['net_return_pct']>0 for f in c['scenes']['3']['recent40']['folds']))]):
  arr=np.empty((3,3))
  for c in full.values():arr[p['lookbacks'].index(c['L']),p['funding_windows'].index(c['N'])]=fn(c)
  ax=axs[row,j];im=ax.imshow(arr,cmap='RdYlGn_r' if j==1 else 'RdYlGn',**({'vmin':0,'vmax':8} if j==3 else {}));ax.set_xticks(range(3),['N1 old','N3','N6']);ax.set_yticks(range(3),['L3','L4','L5']);ax.set_xlabel('Latest eligible funding mean window N');ax.set_ylabel('ETH fast lookback L');ax.set_title(scope+'\n'+label,fontsize=10)
  for c in full.values():i,k=p['lookbacks'].index(c['L']),p['funding_windows'].index(c['N']);ax.text(k,i,f'{arr[i,k]:.3f}'+(' O' if c['readonly'] else ' N'),ha='center',va='center',fontsize=9)
  fig.colorbar(im,ax=ax,shrink=.7)
fig.suptitle('ETH fastL3/4/5 x funding mean N1/3/6, cap0, fixed slowS28, fixedH2.5%, E0.25%, V10/cap4.5%\nActualBTC3750/N375 andETH15000/N4500 | rawweights[1,1],shares20/80%,noNAVscaling | O=readonly,N=new | reuseddevelopmenthistory')
fig.savefig(R/'sensitivity.png',dpi=140);plt.close(fig)
s={'report_sha256':sha(R/'report.json'),**p['expected_counts'],'passed':len(r['summary']['passed']),'rejected':len(r['summary']['candidate_rejected']),'failed_criteria':dict(collections.Counter(f for c in r['configs'].values() for f in c['failed_criteria'])),'CSV_rows':rows,'edge_flags':flags};put(R/'sensitivity_summary.json',s)
ctx=json.loads((R/'context.json').read_text());eq=[]
for c in r['configs'].values():
 grid=p['native_grid'] if c['scope']=='native' else p['grid'];key='all_current_native_grid' if c['scope']=='native' else 'all_current_grid';single=next(g for g in grid if g['L']==c['L'] and g['N']==1);base=r[key][single['fingerprint']];ug=next(g for g in p['unfiltered_comparison_grid'][c['scope']] if g['L']==c['L']);ur=p['read_only_unfiltered_references'][ug['fingerprint']]
 for typ in ['spec','report','archive']:assert sha(ROOT/ur[typ])==ur[typ+'_sha256']
 off=next(z for z in json.loads((ROOT/ur['report']).read_text())['configs'].values() if z['fingerprint']==ug['fingerprint'])
 eq.append({'name':c['name'],'fingerprint':c['fingerprint'],'scope':c['scope'],'L':c['L'],'N':c['N'],'matched_N1_fingerprint':single['fingerprint'],'matched_OFF_fingerprint':ug['fingerprint'],'identical_full_NAV_to_N1_by_cost':{k:c['scenes'][k]['NAV_sha256_f64le']==base['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3']},'all_cost_NAV_identical':all(c['scenes'][k]['NAV_sha256_f64le']==base['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3']),'all_cost_NAV_identical_to_OFF':all(c['scenes'][k]['NAV_sha256_f64le']==off['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3']),'cost_comparisons':{k:{'return_pct':c['scenes'][k]['net_return_pct'],'whole_DD_pct':c['scenes'][k]['max_drawdown_pct'],'N1_return_pct':base['scenes'][k]['net_return_pct'],'N1_DD_pct':base['scenes'][k]['max_drawdown_pct'],'OFF_return_pct':off['scenes'][k]['net_return_pct'],'OFF_DD_pct':off['scenes'][k]['max_drawdown_pct'],'delta_return_to_N1_pp':c['scenes'][k]['net_return_pct']-base['scenes'][k]['net_return_pct'],'delta_DD_to_N1_pp':c['scenes'][k]['max_drawdown_pct']-base['scenes'][k]['max_drawdown_pct']} for k in ['1','2','3']}})
put(R/'equivalent_realized_NAV_paths.json',{'report_sha256':sha(R/'report.json'),'comparisons':eq,'policy':'Distinct parameters are retained; identical realized fullNAV paths are disclosed as aliases, not independent alpha. Ten old definitions reconstructed from saved states plus six original OFF metadata references read without revaluation. Old canonical statuses unchanged.'})
lines=['# 滞后资金费均值窗口稳健性验证','',f"完整读取 {ctx['registry_events']} 条事件、{ctx['registry_ids']} 个ID、{len(ctx['prior_conclusions_read'])}份既往结论；初始16项实际证据齐全。既往研究定义数（排除观察）{ctx['canonical_research_definitions_excluding_observations']}，查重依据完整配置。新6个ETH组件+6个BTC/ETH父组合共12定义，36成本场景，先逐项reserve后计算；所有正负结果完整保留。",'',p['hypothesis'],'',
'固定两轴：ETH快回望L=[3,4,5] × 资金费均值窗口N=[1,3,6]，支付率上限F=0。N1三个原生与三个父旧结果只读，BTC及匹配持有父/原生另4定义，共10旧结果重建；6个原始OFF定义只读报告指标和哈希，不重新估值。N3/N6六个组件与六个父组合为新配置。旧均值6研究还涉及其他退出、慢门或资金配置，与本轮完整规则不同；没有因为family相同排除。','',
'价格规则：ETH快ROC=C[i−1]/C[i−1−L]−1；H=2.5%，严格>H空、<−H多，带内实际多仅ROC<0.25%、实际空仅ROC>−0.25%保留，等号退出。绝对slow28方向始终门控；当前V10样本logvol>4.5%只过滤新开/翻向。之后仅非零且与实际方向不同的desired检验 direction×最近N条已可得realized_rate的精确Fraction算术均值<=0；同向保留和必须退出不受资金费过滤阻止。N1旧政策不重算。','',
'资金费特征：1212条原始真实结算，按settlement排序取最近完整N条；每条settlement<=当日UTC00且normalized available+3600秒<=UTC00；最新一条年龄<=16h。N3/N6较旧来源自然跨24/48小时，16h检查仅针对最新来源，不能错误裁剪旧N事件。缺N、重复结算或最新过期阻断，不降N、不补0。normalized available=settlement+1h另加1h是保守2h模型，未证明历史网络到达。00刚结算费率不能进入00信号。特征原率不随成本倍数放大，也不预测下一结算；实际现金资金费仍按未来各真实结算时刻、rate、mark和当时q逐笔记账。','',
'资金与原始权重：BTC实际本金3750、固定名义375的ROC31/H4%/E1%完整路径只读；ETH本金15000、固定名义4500。本轮父初始本金18750，原权重[1,1]直接相加两独立银行美元NAV；20%/80%仅初始本金份额，不再次相乘或归一化。初始总名义4875即26%本金。数量=固定N/前完整close/LOT向下取整，下一UTC00:01原生OPEN不利tick，翻向先平后开、同向保留实际数量、终止计成本平仓。无父调仓、资金转移、跨抵押、复利调N或缩放旧曲线。','',
'按时间验证：2025-10-19UTC00:01至2026-10-24UTC00:01连续370天，12完整30日折+10日尾折；现金/数量/成本跨折不重置，全曲线计算整体回撤。近期40天固定day330、8×5日折。无模型拟合/标签，purge0、预热30+间隔3；ADV及波动只用前20完整日，价格与资金费按可得时间。历史已反复开发及多重筛选，全部trial计数保留，不能称未触碰最终OOS、独立未来资格或DSR/PBO显著性。','',
'预先固定失败门槛：每成本全年净正，1倍>=9/12正完整月；每成本近期净正且>=6/8正5日折；3倍全曲线DD<=25%；L/N索引半径1含中心邻域中3倍净正比例与严格近期支持均>=60%；>=4平仓，毛参考价格PnL加fund/执行成本>=2.5；零拒单/负抵押/小时维护代理违规，终止flat且>=180天。新原生与父分别判断，旧N1原状态/门槛/报告不改，只另列当前邻域诊断。','',
'1/2/3倍成本：每边5bp费用、1bp半价差、2bp滑点、0.5×past20样本logvol×sqrt(实际q×OPEN/past20完整quoteADV)冲击；资金费支出倍增、正收入不放大。原生LOT/tick/minnotional、参与率<=0.001、费用后1倍入场抵押、各银行独立1%闭合小时不利mark维护代理。线性永续无现货借币，未虚构借币费。缺L2/TCA、完整历史档位及逐tick清算/容量证明；匹配本金和初始N持有及现金0%并列，不是满仓或等风险基准。','',
'|新配置|范围|L|均值N|1倍净%|2倍净%|3倍净%|3倍整体DD%|正月/12|近期正折1/2/3倍|状态|','|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|']
for c in r['configs'].values():
 lines.append('|'+c['name']+'|'+c['scope']+f"|{c['L']}|{c['N']}|"+'|'.join(f"{c['scenes'][k]['net_return_pct']:.6f}" for k in ['1','2','3'])+f"|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['positive_complete_30d_folds_1x']}|"+'/'.join(str(c['recent40_positive_5d_folds_by_cost'][k]) for k in ['1','2','3'])+'|'+c['status']+'|')
lines.extend(['',f"新父历史通过{len(r['summary']['passed'])}、淘汰{len(r['summary']['candidate_rejected'])}。逐配置失败判据：{ {c['name']:c['failed_criteria'] for c in r['configs'].values()} }。年度正收益不能替代近期和邻域门槛，负收益期间完整保留。",'',f"新配置完整NAV与同L/N1三成本全同{sum(x['all_cost_NAV_identical'] for x in eq)}/{len(eq)}，与原始OFF三成本全同{sum(x['all_cost_NAV_identical_to_OFF'] for x in eq)}/{len(eq)}；逐成本收益/DD差值与匹配来源见equivalent_realized_NAV_paths.json。参数新颖不等于独立alpha，不删除别名结果或改旧资格。",'',
'11份CSV包括所有36成本场景、逐月/尾折/近期折、每日NAV、两张9格敏感性面、72相邻边、匹配持有与现金、旧来源和原分配。两面八指标图同时显示收益/DD/Sharpe/近期折；完整Sharpe正比例、最大值边界及描述性2std悬崖单列，不作为显著性。未按结果增加阈值或重测变体。','',
'合成TDD先确认旧N1实现错误拦截最近三次均值为负但最近一次为正的新多仓，再实现最小均值扩展；实际检查N1/3/6、完整窗口、最新年龄、未来扰动、available+1h等号与+1ns、0均值等号、同向保留/等号退出/翻向及vol边界。独立Fraction审核从历史重新选N来源并算均值/信号；Decimal账本重建费用、数量、冲击、funding、小时风险及完整NAV，不调用simulate/decide/trade重新回测。','',
'原SMA与singleS28本轮续UTC20:30至22:30；独立未过滤L4/H2续22:10至次日00:10，仅00:11参考分钟闭合后采集。L4必须处理真实00资金费和00:01原冻结日决策；只适配只读审核的跨日窗口，冻结执行器/计划不改。新均值过滤不注入旧账户。完整cash/q/risk/上下文/NAV前缀保持，部分延迟shadow不替代十策略真实报价模拟，也不取消原长期冻结计划。','',
'一手来源实际访问2026-11-02：[Binance官方资金费历史API](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)。文档支持真实率/结算/mark字段，不证明历史网络发布时间或策略盈利；primary_sources.json与funding_data_availability.json分别记录假设和真实输入哈希。','',
'同main排他锁内逐项finish、检查、只读监控汇总、提交与非强制push。汇总不生成模拟成交，不改冻结规则/本金/持仓，不部署网页或创建任务，不下真实订单。正回测不是稳定实盘盈利；未新增前向账户。'])
(R/'result.md').write_text('\n'.join(lines)+'\n');print(json.dumps(s),flush=True)
