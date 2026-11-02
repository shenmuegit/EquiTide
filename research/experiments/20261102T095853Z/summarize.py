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
  cost.append([c['name'],c['fingerprint'],c['scope'],c['role'],c['asset'],c['L'],c['HS'],c['capital_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['cost_usdt'],s['cost_pct_initial'],s['funding_usdt'],s['gross_reference_PnL_to_execution_cost'],s['executions'],s['round_trips'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),c['status']])
  wf.extend([c['name'],c['scope'],c['L'],c['HS'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['duration_days'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['folds'])
  recent.extend([c['name'],c['scope'],c['L'],c['HS'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['recent40']['folds'])
  daily.extend([c['name'],c['scope'],k,i,v] for i,v in enumerate(s['daily_equity_usdt']))
write('cost_scenes.csv',['configuration','fingerprint','scope','role','asset','ETH_fast_L','short_entry_hurdle_HS','initial_capital','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','cost_usdt','cost_pct_initial','funding_usdt','gross_plus_funding_to_cost','executions','closes','recent40_return_pct','positive5d_folds','status'],cost)
write('walk_forward_folds.csv',['configuration','scope','ETH_fast_L','short_entry_hurdle_HS','cost_multiplier','fold','start_utc','end_exclusive_utc','days','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],wf)
write('recent40_folds.csv',['configuration','scope','ETH_fast_L','short_entry_hurdle_HS','cost_multiplier','fold','start_utc','end_exclusive_utc','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],recent)
write('daily_NAV.csv',['configuration','scope','cost_multiplier','boundary','NAV_usdt'],daily)
cols=['ETH_fast_L','short_entry_hurdle_HS','fingerprint','readonly_old','unchanged_canonical_status','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','recent40_return_pct','positive5d_folds','local_positive3_fraction','local_recent_fraction'];flags={};readonly=[]
for scope,grid,key in [('parent',p['grid'],'all_current_grid'),('native',p['native_grid'],'all_current_native_grid')]:
 full=r[key];items=[]
 for g in grid:
  c=full[g['fingerprint']]
  for k,s in c['scenes'].items():
   d=c['current_grid_diagnostic_sensitivity'];z=[g['L'],g['HS'],g['fingerprint'],g['readonly'],c['status'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),d['local_positive3_fraction'],d['local_strict_recent_fraction']];items.append(z)
   if scope=='parent' and g['readonly']:readonly.append(z)
 for k in ['1','2','3']:
  for g in grid:
   i,j=p['lookbacks'].index(g['L']),p['short_hurdles'].index(g['HS']);ng=[h for h in grid if i<2 and h['L']==p['lookbacks'][i+1] and h['HS']==g['HS'] or j<2 and h['HS']==p['short_hurdles'][j+1] and h['L']==g['L']]
   for h in ng:
    a,b=full[g['fingerprint']]['scenes'][k],full[h['fingerprint']]['scenes'][k];edges.append([scope,k,g['L'],g['HS'],h['L'],h['HS'],g['fingerprint'],h['fingerprint'],abs(a['sharpe_365']-b['sharpe_365']),abs(a['net_return_pct']-b['net_return_pct']),abs(a['max_drawdown_pct']-b['max_drawdown_pct'])])
 flags[scope]={}
 for k in ['1','2','3']:
  v=[x[8] for x in edges if x[0]==scope and x[1]==k];t=2*statistics.stdev(v);flags[scope][k]={'edge_count':len(v),'max_Sharpe_change':max(v),'two_std_change_threshold':t,'descriptive_cliff_flag':max(v)>t,'scope':'Dependentedgeheuristiconly,notstatisticalsignificance,DSRorPBO.'}
 write('sensitivity_grid.csv' if scope=='parent' else 'native_sensitivity_grid.csv',cols,items)
write('readonly_reused_scenes.csv',cols,readonly)
write('adjacent_edges.csv',['scope','cost_multiplier','from_L','from_HS','to_L','to_HS','from_fp','to_fp','absolute_Sharpe_change','absolute_return_change_pp','absolute_DD_change_pp'],edges)
cs=r['matched_hold_comparisons'];write('matched_hold_comparisons.csv',list(cs[0]),[list(x.values()) for x in cs])
for fp,x in p['read_only_references'].items():
 if x['scope']!='native':continue
 sp=json.loads((ROOT/x['spec']).read_text());old=next(c for c in json.loads((ROOT/x['report']).read_text())['configs'].values() if c['fingerprint']==fp)
 for k,s in old['scenes'].items():sources.append([fp,x['asset'],x['capital_usdt'],sp['parameters']['fixed_entry_notional_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['cost_usdt'],s['funding_usdt'],s['executions'],s['NAV_sha256_f64le'],x['report'],x['report_sha256']])
write('source_curves.csv',['fingerprint','asset','actual_bank_capital','actual_entry_N','cost_multiplier','return_pct','whole_DD_pct','cost_usdt','funding_usdt','executions','NAV_sha256','readonly_report','readonly_report_sha256'],sources)
for g in p['grid']:alloc.append([g['fingerprint'],'candidate',g['L'],g['HS'],3750,15000,18750,375,4500,1,1,.2,.8,g['readonly']])
alloc.append([p['benchmark_parent_fingerprint'],'matched_initial_budget_hold',None,None,3750,15000,18750,375,4500,1,1,.2,.8,True]);write('fixed_allocations.csv',['fingerprint','role','ETH_L','short_entry_hurdle_HS','BTC_bank','ETH_bank','total_initial_capital','BTC_N','ETH_N','raw_BTC_weight','raw_ETH_weight','BTC_capital_share','ETH_capital_share','readonly'],alloc)
put(R/'edge_flags.json',flags)
fig,axs=plt.subplots(2,4,figsize=(16,9),layout='constrained')
for row,(scope,key) in enumerate([('ETH native15000/N4500','all_current_native_grid'),('BTC3750+ETH15000 parent','all_current_grid')]):
 full=r[key]
 for j,(label,fn) in enumerate([('3x continuous370 return %',lambda c:c['scenes']['3']['net_return_pct']),('3x wholecurve DD %',lambda c:c['scenes']['3']['max_drawdown_pct']),('3x daily Sharpe365',lambda c:c['scenes']['3']['sharpe_365']),('3x recent positive5d /8',lambda c:sum(f['net_return_pct']>0 for f in c['scenes']['3']['recent40']['folds']))]):
  arr=np.empty((3,3))
  for c in full.values():arr[p['lookbacks'].index(c['L']),p['short_hurdles'].index(c['HS'])]=fn(c)
  ax=axs[row,j];im=ax.imshow(arr,cmap='RdYlGn_r' if j==1 else 'RdYlGn',**({'vmin':0,'vmax':8} if j==3 else {}));ax.set_xticks(range(3),['2%','2.5% old','3%']);ax.set_yticks(range(3),['L3','L4','L5']);ax.set_xlabel('ETH short hurdle HS (long fixed1.5%)');ax.set_ylabel('ETH fast lookback L');ax.set_title(scope+'\n'+label,fontsize=10)
  for c in full.values():i,k=p['lookbacks'].index(c['L']),p['short_hurdles'].index(c['HS']);ax.text(k,i,f'{arr[i,k]:.3f}'+(' O' if c['readonly'] else ' N'),ha='center',va='center',fontsize=9)
  fig.colorbar(im,ax=ax,shrink=.7)
fig.suptitle('ETH fastL3/4/5 x shortHS2/2.5/3%, longHL1.5%, fixed slowS28, E0.25%, V10/cap4.5%\nActualBTC3750/N375 andETH15000/N4500 | rawweights[1,1],shares20/80%,noNAVscaling | O=readonly,N=new | reuseddevelopmenthistory')
fig.savefig(R/'sensitivity.png',dpi=140);plt.close(fig)
s={'report_sha256':sha(R/'report.json'),**p['expected_counts'],'passed':len(r['summary']['passed']),'rejected':len(r['summary']['candidate_rejected']),'failed_criteria':dict(collections.Counter(f for c in r['configs'].values() for f in c['failed_criteria'])),'CSV_rows':rows,'edge_flags':flags};put(R/'sensitivity_summary.json',s)
ctx=json.loads((R/'context.json').read_text());eq=[]
for c in r['configs'].values():
 grid=p['native_grid'] if c['scope']=='native' else p['grid'];key='all_current_native_grid' if c['scope']=='native' else 'all_current_grid';g=next(g for g in grid if g['L']==c['L'] and g['HS']==.025);base=r[key][g['fingerprint']]
 eq.append({'name':c['name'],'fingerprint':c['fingerprint'],'scope':c['scope'],'L':c['L'],'HS':c['HS'],'HL':.015,'matched_control_fingerprint':g['fingerprint'],'identical_full_NAV_by_cost':{k:c['scenes'][k]['NAV_sha256_f64le']==base['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3']},'all_cost_NAV_identical':all(c['scenes'][k]['NAV_sha256_f64le']==base['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3']),'cost_comparisons':{k:{'return_pct':c['scenes'][k]['net_return_pct'],'whole_DD_pct':c['scenes'][k]['max_drawdown_pct'],'control_return_pct':base['scenes'][k]['net_return_pct'],'control_DD_pct':base['scenes'][k]['max_drawdown_pct'],'delta_return_to_control_pp':c['scenes'][k]['net_return_pct']-base['scenes'][k]['net_return_pct'],'delta_DD_to_control_pp':c['scenes'][k]['max_drawdown_pct']-base['scenes'][k]['max_drawdown_pct']} for k in ['1','2','3']}})
put(R/'equivalent_realized_NAV_paths.json',{'report_sha256':sha(R/'report.json'),'comparisons':eq,'policy':'NewshortHS values are preserved as new definitions; identical realized fullNAV paths, if any, are disclosed rather than called independentalpha. PriorHS2.5 canonicalstatus/report unchanged, no completed-policy rerun.'})
lines=['# ETH 空侧入场门槛独立扰动验证','',f"完整读取{ctx['registry_events']}事件/{ctx['registry_ids']}ID、{len(ctx['prior_conclusions_read'])}份既往结论，排除持续观察后的完整历史研究定义数{ctx['canonical_research_definitions_excluding_observations']}。初始16条均已有真实证据，没有仅代码而缺实际回测的待补项。本轮6个ETH原生组件与6个BTC/ETH组合、36成本场景，各项reserve成功后才计算；所有正负期间、失败配置完整保存。",'',p['hypothesis'],'',
'预设两轴为快回望L=[3,4,5]与空头入场HS=[0.02,0.025,0.03]，多头HL=0.015固定。HS=2.5%的三个原生、三个组合、BTC与匹配持有父及其两个原生共10旧定义只读。原return_hurdle字段表示空侧，long_entry_return_hurdle表示固定多侧。仅不同名称或组件顺序不计新配置，完整规则/参数/资金/权重指纹查重。','',
'完整规则：fastROC=C[i−1]/C[i−1−L]−1，严格r>HS做空、r<−0.015做多，等号不新开；否则实际多仅r<E保留、实际空仅r>−E保留，E=+0.0025、等号退出。绝对slow28方向始终门控，不同向即退出。V10样本logvol>0.045只过滤新开/翻向，同向实际数量不变，翻向先平后开。没有最长持仓、慢趋势幅度、残差或资金费信号过滤。所有指标来自前完整日，信号可得后下一UTC00:01原生OPEN执行。','',
'资金与原始权重：BTC真实3750银行/N375沿用原ROC31/H4%/E1%已验证净值；ETH真实15000银行/N4500重新按原生数量、冲击和抵押核算。原[1,1]为两个完整银行美元NAV相加，本金18750；20%/80%仅初始本金份额，不再乘一次或自动归一化。初始名义4875=26%本金，固定N除以前完整close按LOT向下取整，OPEN不利tick；普通翻向和终止平仓都计成本。没有父调仓、资金转移、同币克隆、跨抵押、复利调N或线性放缩旧NAV。','',
'Walk-forward：2025-10-19UTC00:01至2026-10-24UTC00:01，连续370天，12个完整30日折加10日尾折。现金/数量/已付费用跨折连续，不重开银行；整体DD从完整分钟/事件NAV计算。近期40天从day330继承，含8个5日折。固定规则无拟合/标签，purge0、预热30日加3日间隔，成本ADV与样本logvol仅用前20完整日。整段历史已大量反复开发，保留总试验数，不称未触碰最终留出、独立未来或DSR/PBO显著性。','',
'成本：每边5bp手续费、1bp半价差、2bp滑点和0.5×past20样本logvol×sqrt(实际q×OPEN/past20完整quoteADV)冲击，分别1/2/3倍。资金费按真实结算ns、rate、mark与heldq入账，支出倍增、收入不放大。核对LOT/tick/minnotional、参与率<=0.001、费用后1倍抵押及独立银行1%闭合小时不利mark维护代理。线性永续无需现货借币，不虚构借币费；缺真实L2/TCA/完整历史档位/逐tick清算与容量证明。并列同本金/同初始N持有及现金0%，不称等风险或满仓持有。','',
'冻结失败判据：每成本全年净正；1倍>=9/12正完整月；每成本近期40天净正且>=6/8正5日折；3倍整体DD<=25%；L/HS索引半径1含中心邻域，3倍净正与严格近期合格支持各>=60%；>=4底层平仓；1倍毛参考价格PnL加funding/执行成本>=2.5；零拒单、负抵押、小时维护代理违规，终止flat且>=180日。新组件和组合分别判断，旧HS2.5原始资格不改，仅给出当前邻域诊断。','',
'|新配置|范围|L|空侧HS|1倍净%|2倍净%|3倍净%|3倍整体DD%|正月/12|近期正折1/2/3倍|状态|','|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|']
for c in r['configs'].values():lines.append('|'+c['name']+'|'+c['scope']+f"|{c['L']}|{c['HS']:.3f}|"+'|'.join(f"{c['scenes'][k]['net_return_pct']:.6f}" for k in ['1','2','3'])+f"|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['positive_complete_30d_folds_1x']}|"+'/'.join(str(c['recent40_positive_5d_folds_by_cost'][k]) for k in ['1','2','3'])+'|'+c['status']+'|')
lines.extend(['',f"新组合历史通过{len(r['summary']['passed'])}，淘汰{len(r['summary']['candidate_rejected'])}。每配置失败判据：{ {c['name']:c['failed_criteria'] for c in r['configs'].values()} }。年度正收益不能替代近期和局部支持门槛。",'',f"新配置相对同L固定HL1.5%/旧HS2.5%对照，三成本完整NAV全同{sum(z['all_cost_NAV_identical'] for z in eq)}/{len(eq)}。equivalent_realized_NAV_paths逐成本给出真实全曲线hash、收益和DD差异；参数新颖不等于独立alpha。",'',
'11份CSV含36场景、逐月/尾折/近期折、每日NAV、原生与组合完整九格敏感性、72条相邻边、旧来源、原分配与持有/现金对照。两面八指标图报告收益、完整DD、Sharpe与近期正折；Calmar在表内，Sharpe正格比例、边界峰值及描述性2std相邻悬崖另列，不当作独立统计显著性，不根据本批结果扩展参数。','',
'合成检查先运行固定空侧2.5%的错误适配器，2.2%上涨在新HS2%下应做空却没有触发，预期红灯已记录；正确通用引擎检查L3/4/5×HS2/2.5/3%，固定多侧1.5%独立性、两侧严格等号、原持仓保留/退出/翻向、slow方向、V10边界及追加未来bar不变。独立Fraction重算新价格决策，Decimal复核实际数量/现金/手续费/冲击/真实资金费/小时风险/完整NAV与父对齐，不调用simulate/decide/trade再跑策略。','',
'原SMA与原singleS28从Nov2UTC06:30续至08:30，原single在本窗口按真实事件处理08资金费一次；SMA仅分钟mark。独立未过滤L4/H2从08:10续至10:10，仅10:11参考闭合后采集，其08资金费上一窗口已入账，不重复。保留每成本cash/q/desired/risk/上下文/NAV前缀，不引入本批研究参数。SMA的65日上下文继续引用20261102T015622Z。所有部分延迟shadow不替代十策略实时报价模拟，也没有新建前向账户或改变原长期计划。','',
'一手来源实际访问2026-11-02：[Binance市场数据API](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)。8份真实年bars/mark/funding/约束文件路径、边界、字节及SHA256见plan和data_manifest。文档不证明本策略盈利、历史网络发布时刻或实测盘口成本。','',
'所有实际配置逐项finish，登记、来源、导出与监控检查在同main排他锁完成后提交、非强制push。只读汇总不产生成交，不改冻结规则/本金/持仓，不新部署网页或增加定时任务，不下真实订单。'])
(R/'result.md').write_text('\n'.join(lines)+'\n');print(json.dumps(s),flush=True)
