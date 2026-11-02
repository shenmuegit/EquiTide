"""Export saved real native/parent L/T results; no strategy calculation."""
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
  cost.append([c['name'],c['fingerprint'],c['scope'],c['role'],c['asset'],c['L'],c['T'],c['capital_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['cost_usdt'],s['cost_pct_initial'],s['funding_usdt'],s['gross_reference_PnL_to_execution_cost'],s['executions'],s['round_trips'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),c['status']])
  wf.extend([c['name'],c['scope'],c['L'],c['T'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['duration_days'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['folds'])
  recent.extend([c['name'],c['scope'],c['L'],c['T'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['recent40']['folds'])
  daily.extend([c['name'],c['scope'],k,i,v] for i,v in enumerate(s['daily_equity_usdt']))
write('cost_scenes.csv',['configuration','fingerprint','scope','role','asset','ETH_fast_L','minimum_abs_slow_return_T','initial_capital','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','cost_usdt','cost_pct_initial','funding_usdt','gross_plus_funding_to_cost','executions','closes','recent40_return_pct','positive5d_folds','status'],cost)
write('walk_forward_folds.csv',['configuration','scope','ETH_fast_L','minimum_abs_slow_return_T','cost_multiplier','fold','start_utc','end_exclusive_utc','days','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],wf)
write('recent40_folds.csv',['configuration','scope','ETH_fast_L','minimum_abs_slow_return_T','cost_multiplier','fold','start_utc','end_exclusive_utc','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],recent)
write('daily_NAV.csv',['configuration','scope','cost_multiplier','boundary','NAV_usdt'],daily)
cols=['ETH_fast_L','minimum_abs_slow_return_T','fingerprint','readonly_old','unchanged_canonical_status','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','recent40_return_pct','positive5d_folds','local_positive3_fraction','local_recent_fraction'];flags={};readonly=[]
for scope,grid,key in [('parent',p['grid'],'all_current_grid'),('native',p['native_grid'],'all_current_native_grid')]:
 full=r[key];items=[]
 for g in grid:
  c=full[g['fingerprint']]
  for k,s in c['scenes'].items():
   d=c['current_grid_diagnostic_sensitivity'];z=[g['L'],g['T'],g['fingerprint'],g['readonly'],c['status'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),d['local_positive3_fraction'],d['local_strict_recent_fraction']];items.append(z)
   if scope=='parent' and g['readonly']:readonly.append(z)
 for k in ['1','2','3']:
  for g in grid:
   i,j=p['lookbacks'].index(g['L']),p['strength_thresholds'].index(g['T']);ng=[h for h in grid if i<2 and h['L']==p['lookbacks'][i+1] and h['T']==g['T'] or j<2 and h['T']==p['strength_thresholds'][j+1] and h['L']==g['L']]
   for h in ng:
    a,b=full[g['fingerprint']]['scenes'][k],full[h['fingerprint']]['scenes'][k];edges.append([scope,k,g['L'],g['T'],h['L'],h['T'],g['fingerprint'],h['fingerprint'],abs(a['sharpe_365']-b['sharpe_365']),abs(a['net_return_pct']-b['net_return_pct']),abs(a['max_drawdown_pct']-b['max_drawdown_pct'])])
 flags[scope]={}
 for k in ['1','2','3']:
  v=[x[8] for x in edges if x[0]==scope and x[1]==k];t=2*statistics.stdev(v);flags[scope][k]={'edge_count':len(v),'max_Sharpe_change':max(v),'two_std_change_threshold':t,'descriptive_cliff_flag':max(v)>t,'scope':'Dependentedgeheuristiconly,notstatisticalsignificance,DSRorPBO.'}
 write('sensitivity_grid.csv' if scope=='parent' else 'native_sensitivity_grid.csv',cols,items)
write('readonly_reused_scenes.csv',cols,readonly)
write('adjacent_edges.csv',['scope','cost_multiplier','from_L','from_T','to_L','to_T','from_fp','to_fp','absolute_Sharpe_change','absolute_return_change_pp','absolute_DD_change_pp'],edges)
cs=r['matched_hold_comparisons'];write('matched_hold_comparisons.csv',list(cs[0]),[list(x.values()) for x in cs])
for fp,x in p['read_only_references'].items():
 if x['scope']!='native':continue
 sp=json.loads((ROOT/x['spec']).read_text());old=next(c for c in json.loads((ROOT/x['report']).read_text())['configs'].values() if c['fingerprint']==fp)
 for k,s in old['scenes'].items():sources.append([fp,x['asset'],x['capital_usdt'],sp['parameters']['fixed_entry_notional_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['cost_usdt'],s['funding_usdt'],s['executions'],s['NAV_sha256_f64le'],x['report'],x['report_sha256']])
write('source_curves.csv',['fingerprint','asset','actual_bank_capital','actual_entry_N','cost_multiplier','return_pct','whole_DD_pct','cost_usdt','funding_usdt','executions','NAV_sha256','readonly_report','readonly_report_sha256'],sources)
for g in p['grid']:alloc.append([g['fingerprint'],'candidate',g['L'],g['T'],3750,15000,18750,375,4500,1,1,.2,.8,g['readonly']])
alloc.append([p['benchmark_parent_fingerprint'],'matched_initial_budget_hold',None,None,3750,15000,18750,375,4500,1,1,.2,.8,True]);write('fixed_allocations.csv',['fingerprint','role','ETH_L','minimum_abs_slow_return_T','BTC_bank','ETH_bank','total_initial_capital','BTC_N','ETH_N','raw_BTC_weight','raw_ETH_weight','BTC_capital_share','ETH_capital_share','readonly'],alloc)
put(R/'edge_flags.json',flags)
fig,axs=plt.subplots(2,4,figsize=(16,9),layout='constrained')
for row,(scope,key) in enumerate([('ETH native15000/N4500','all_current_native_grid'),('BTC3750+ETH15000 parent','all_current_grid')]):
 full=r[key]
 for j,(label,fn) in enumerate([('3x continuous370 return %',lambda c:c['scenes']['3']['net_return_pct']),('3x wholecurve DD %',lambda c:c['scenes']['3']['max_drawdown_pct']),('3x daily Sharpe365',lambda c:c['scenes']['3']['sharpe_365']),('3x recent positive5d /8',lambda c:sum(f['net_return_pct']>0 for f in c['scenes']['3']['recent40']['folds']))]):
  arr=np.empty((3,3))
  for c in full.values():arr[p['lookbacks'].index(c['L']),p['strength_thresholds'].index(c['T'])]=fn(c)
  ax=axs[row,j];im=ax.imshow(arr,cmap='RdYlGn_r' if j==1 else 'RdYlGn',**({'vmin':0,'vmax':8} if j==3 else {}));ax.set_xticks(range(3),['0 old','2.5%','5%']);ax.set_yticks(range(3),['L3','L4','L5']);ax.set_xlabel('Minimum abs(slow28 ROC) for fresh entry T');ax.set_ylabel('ETH fast lookback L');ax.set_title(scope+'\n'+label,fontsize=10)
  for c in full.values():i,k=p['lookbacks'].index(c['L']),p['strength_thresholds'].index(c['T']);ax.text(k,i,f'{arr[i,k]:.3f}'+(' O' if c['readonly'] else ' N'),ha='center',va='center',fontsize=9)
  fig.colorbar(im,ax=ax,shrink=.7)
fig.suptitle('ETH fastL3/4/5 x slowtrend strength min0/2.5/5%, fixed slowS28, fixedH2.5%, E0.25%, V10/cap4.5%\nActualBTC3750/N375 andETH15000/N4500 | rawweights[1,1],shares20/80%,noNAVscaling | O=readonly,N=new | reuseddevelopmenthistory')
fig.savefig(R/'sensitivity.png',dpi=140);plt.close(fig)
s={'report_sha256':sha(R/'report.json'),**p['expected_counts'],'passed':len(r['summary']['passed']),'rejected':len(r['summary']['candidate_rejected']),'failed_criteria':dict(collections.Counter(f for c in r['configs'].values() for f in c['failed_criteria'])),'CSV_rows':rows,'edge_flags':flags};put(R/'sensitivity_summary.json',s)
ctx=json.loads((R/'context.json').read_text());eq=[]
for c in r['configs'].values():
 grid=p['native_grid'] if c['scope']=='native' else p['grid'];key='all_current_native_grid' if c['scope']=='native' else 'all_current_grid';zero=next(g for g in grid if g['L']==c['L'] and g['T']==0);base=r[key][zero['fingerprint']]
 eq.append({'name':c['name'],'fingerprint':c['fingerprint'],'scope':c['scope'],'L':c['L'],'T':c['T'],'matched_T0_fingerprint':zero['fingerprint'],'identical_full_NAV_by_cost':{k:c['scenes'][k]['NAV_sha256_f64le']==base['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3']},'all_cost_NAV_identical':all(c['scenes'][k]['NAV_sha256_f64le']==base['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3']),'cost_comparisons':{k:{'return_pct':c['scenes'][k]['net_return_pct'],'whole_DD_pct':c['scenes'][k]['max_drawdown_pct'],'T0_return_pct':base['scenes'][k]['net_return_pct'],'T0_DD_pct':base['scenes'][k]['max_drawdown_pct'],'delta_return_to_T0_pp':c['scenes'][k]['net_return_pct']-base['scenes'][k]['net_return_pct'],'delta_DD_to_T0_pp':c['scenes'][k]['max_drawdown_pct']-base['scenes'][k]['max_drawdown_pct']} for k in ['1','2','3']}})
put(R/'equivalent_realized_NAV_paths.json',{'report_sha256':sha(R/'report.json'),'comparisons':eq,'policy':'Distinct positive strength thresholds retained; exact realized NAV aliases are disclosed, not counted as independent alpha. T0 actual canonical results/statuses unchanged, no completed policy revaluation.'})
lines=['# 慢趋势强度入场过滤验证','',f"完整读取{ctx['registry_events']}事件/{ctx['registry_ids']}ID、{len(ctx['prior_conclusions_read'])}份历史结论；排除持续观察后的历史研究定义数{ctx['canonical_research_definitions_excluding_observations']}。初始16项实际证据齐全，无缺失回测需要重跑。本轮6新ETH原生+6新父组合、36成本场景，逐项reserve后实际计算，全部正负期间及结果保存。",'',p['hypothesis'],'',
'预定两轴：快回望L=[3,4,5]与最低慢趋势幅度T=[0,0.025,0.05]。H=0.025、正退出缓冲E=0.0025、S28方向始终门控、V10样本logvol上限0.045均固定。T0三个原生与三个父、BTC及匹配持有父/两原生共10唯一旧结果只读；T2.5%/5%六原生与六父为新配置。完整spec指纹查重，不按family排除；不添加资金费预测特征或BTC残差控制。','',
'完整信号：ETH fastROC=C[i−1]/C[i−1−L]−1，严格>H空、<−H多；带内实际多仅ROC<E、实际空仅ROC>−E保留，等号退出。绝对slow28方向始终门控，不匹配退出；V10波动>4.5%只拦新开/翻向。之后仅非零且与实际持仓方向不同的desired要求abs(slow28ROC)>=T；严格小于拦截，等号允许。同向保留不要求幅度门槛，必须退出不受新门槛阻止；被拦翻向先退出旧方向而不新开。价格全为过去完整bar，Fraction精确阈值，不做未来收益调参。','',
'经济假设是强慢趋势中的快回撤或反弹可能比弱慢趋势更可靠，较大门槛也可能错失趋势初期、缩小成交样本。该假设由本轮提出，不来自官方API盈利承诺，不在结果后放宽近期6/8或邻域60%门槛。','',
'真实资金：BTC独立银行3750USDT/N375的ROC31/H4%/E1%旧路径只读，ETH15000/N4500按原生数量/冲击/抵押重新计算。总初始本金18750，原权重[1,1]是两完整银行美元NAV相加；20%/80%只是本金份额，不再次乘权重或自动归一化。初始名义总4875即26%本金。固定N/前完整close按LOT向下取整，下一00:01原生OPEN不利tick，翻向先平后开、保留实际同向q、终止成本平仓；无父调仓、转账、跨抵押、NAV复利调N或线性缩放旧路径。','',
'Walk-forward：2025-10-19UTC00:01至2026-10-24UTC00:01连续370天；12完整30日折+10日尾折，现金/数量/费用跨折不重置，全分钟/事件NAV计算整体回撤。近期40天继承day330，8×5日折。固定规则无拟合/标签，purge0，预热30+间隔3；ADV/波动只用前20完整日。所有历史已反复开发，多重试验计数见context；不称未触碰最终留出、独立前向或DSR/PBO显著性。','',
'1/2/3倍成本：每边5bp费用、1bp半价差、2bp滑点及0.5×past20样本logvol×sqrt(实际q×OPEN/past20完整quoteADV)冲击。实际资金费按每次真实settlement/rate/mark/heldq记账，支出倍增、正收入不放大；本轮不把funding用于入场信号。原生LOT/tick/minnotional、参与率<=0.001、费用后1倍抵押及各银行独立1%闭合小时不利mark维护代理均核验。线性永续无现货借币，不虚构借币费；没有L2/TCA/完整历史档位或逐tick清算/容量证明。匹配本金与初始N持有及现金0%并列，非满仓或同风险持有。','',
'预先固定失败门槛：每成本全年净正，1倍至少9/12正完整月；每成本近期净正且至少6/8正5日折；3倍整体DD<=25%；两轴索引半径1含中心邻域的3倍净正比例与严格近期支持均>=60%；>=4平仓，毛参考价格PnL加fund/执行成本>=2.5；零拒单、负抵押、小时维护代理违规，终止flat且>=180天。原生与父分别判断，旧T0原资格和报告不改，只列当前邻域诊断。','',
'|新配置|范围|L|T|1倍净%|2倍净%|3倍净%|3倍整体DD%|正月/12|近期正折1/2/3倍|状态|','|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|']
for c in r['configs'].values():
 lines.append('|'+c['name']+'|'+c['scope']+f"|{c['L']}|{c['T']:.4f}|"+'|'.join(f"{c['scenes'][k]['net_return_pct']:.6f}" for k in ['1','2','3'])+f"|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['positive_complete_30d_folds_1x']}|"+'/'.join(str(c['recent40_positive_5d_folds_by_cost'][k]) for k in ['1','2','3'])+'|'+c['status']+'|')
lines.extend(['',f"新父历史通过{len(r['summary']['passed'])}、淘汰{len(r['summary']['candidate_rejected'])}。全部新配置失败判据：{ {c['name']:c['failed_criteria'] for c in r['configs'].values()} }。年度正收益不能替代近期和邻域稳定性。",'',f"新配置与匹配T0三成本完整NAV哈希全同{sum(z['all_cost_NAV_identical'] for z in eq)}/{len(eq)}，逐成本收益/DD差异及来源见equivalent_realized_NAV_paths.json。参数新颖不等于新独立alpha，同路径不删除结果、不改旧资格。",'',
'11CSV保存36成本场景、逐月/尾折/近期折、每日NAV、原生和父完整9格敏感性、72相邻边、持有/现金、旧来源及原分配。两面八指标图显示收益、全曲线DD、Sharpe及近期正折；Sharpe正格比例、边界峰值、描述性2std悬崖单列，不作统计显著性或按结果扩展阈值。','',
'合成TDD先证明旧规则会允许1.05%慢趋势中新多仓，而新2.5%门槛应拦截；实际先红后绿，检查多空、阈值等号、未来bar追加不变、弱趋势持仓保留、等号退出、被拦翻向和vol边界。独立Fraction重算全部新信号；Decimal账本核对真实数量、成交、费用、资金费、小时风险、全NAV/回撤及父来源对齐，不调用simulate/decide/trade重新回测。','',
'冻结账户独立延续：原SMA65及singleS28从Nov1UTC22:30至Nov2UTC00:30，必须按原日切换规则处理00:01决策、single实际00资金费；独立未过滤L4/H2从Nov2UTC00:10至02:10，仅02:11参考闭合后采集，00资金费已记账不重复。新趋势强度门槛不注入任何冻结账户，保留全cash/q/desired/risk/上下文/NAV前缀。部分延迟shadow继续长期冻结计划，不替代十策略实时报价模拟。','',
'官方一手资料实际访问2026-11-02：[Binance市场数据API](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)，提供原生klines、mark、资金费和约束字段；真实8文件哈希见plan/data_manifest。官方文档不证明策略盈利或历史网络到达时间。','',
'同main排他锁内逐项finish、登记/导出/监控检查、提交非强制push。只读监控不产生交易、不改规则/本金/持仓、不部署网页或增加定时任务。正回测不称稳定实盘盈利，未新增前向账户。'])
(R/'result.md').write_text('\n'.join(lines)+'\n');print(json.dumps(s),flush=True)
