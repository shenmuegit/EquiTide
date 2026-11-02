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
  cost.append([c['name'],c['fingerprint'],c['scope'],c['role'],c['asset'],c['L'],c['VC'],c['capital_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['cost_usdt'],s['cost_pct_initial'],s['funding_usdt'],s['gross_reference_PnL_to_execution_cost'],s['executions'],s['round_trips'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),c['status']])
  wf.extend([c['name'],c['scope'],c['L'],c['VC'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['duration_days'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['folds'])
  recent.extend([c['name'],c['scope'],c['L'],c['VC'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['recent40']['folds'])
  daily.extend([c['name'],c['scope'],k,i,v] for i,v in enumerate(s['daily_equity_usdt']))
write('cost_scenes.csv',['configuration','fingerprint','scope','role','asset','ETH_fast_L','entry_V10_volatility_ceiling_VC','initial_capital','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','cost_usdt','cost_pct_initial','funding_usdt','gross_plus_funding_to_cost','executions','closes','recent40_return_pct','positive5d_folds','status'],cost)
write('walk_forward_folds.csv',['configuration','scope','ETH_fast_L','entry_V10_volatility_ceiling_VC','cost_multiplier','fold','start_utc','end_exclusive_utc','days','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],wf)
write('recent40_folds.csv',['configuration','scope','ETH_fast_L','entry_V10_volatility_ceiling_VC','cost_multiplier','fold','start_utc','end_exclusive_utc','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],recent)
write('daily_NAV.csv',['configuration','scope','cost_multiplier','boundary','NAV_usdt'],daily)
cols=['ETH_fast_L','entry_V10_volatility_ceiling_VC','fingerprint','readonly_old','unchanged_canonical_status','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','recent40_return_pct','positive5d_folds','local_positive3_fraction','local_recent_fraction'];flags={};readonly=[]
for scope,grid,key in [('parent',p['grid'],'all_current_grid'),('native',p['native_grid'],'all_current_native_grid')]:
 full=r[key];items=[]
 for g in grid:
  c=full[g['fingerprint']]
  for k,s in c['scenes'].items():
   d=c['current_grid_diagnostic_sensitivity'];z=[g['L'],g['VC'],g['fingerprint'],g['readonly'],c['status'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),d['local_positive3_fraction'],d['local_strict_recent_fraction']];items.append(z)
   if scope=='parent' and g['readonly']:readonly.append(z)
 for k in ['1','2','3']:
  for g in grid:
   i,j=p['lookbacks'].index(g['L']),p['volatility_caps'].index(g['VC']);ng=[h for h in grid if i<2 and h['L']==p['lookbacks'][i+1] and h['VC']==g['VC'] or j<2 and h['VC']==p['volatility_caps'][j+1] and h['L']==g['L']]
   for h in ng:
    a,b=full[g['fingerprint']]['scenes'][k],full[h['fingerprint']]['scenes'][k];edges.append([scope,k,g['L'],g['VC'],h['L'],h['VC'],g['fingerprint'],h['fingerprint'],abs(a['sharpe_365']-b['sharpe_365']),abs(a['net_return_pct']-b['net_return_pct']),abs(a['max_drawdown_pct']-b['max_drawdown_pct'])])
 flags[scope]={}
 for k in ['1','2','3']:
  v=[x[8] for x in edges if x[0]==scope and x[1]==k];t=2*statistics.stdev(v);flags[scope][k]={'edge_count':len(v),'max_Sharpe_change':max(v),'two_std_change_threshold':t,'descriptive_cliff_flag':max(v)>t,'scope':'Dependentedgeheuristiconly,notstatisticalsignificance,DSRorPBO.'}
 write('sensitivity_grid.csv' if scope=='parent' else 'native_sensitivity_grid.csv',cols,items)
write('readonly_reused_scenes.csv',cols,readonly)
write('adjacent_edges.csv',['scope','cost_multiplier','from_L','from_VC','to_L','to_VC','from_fp','to_fp','absolute_Sharpe_change','absolute_return_change_pp','absolute_DD_change_pp'],edges)
cs=r['matched_hold_comparisons'];write('matched_hold_comparisons.csv',list(cs[0]),[list(x.values()) for x in cs])
for fp,x in p['read_only_references'].items():
 if x['scope']!='native':continue
 sp=json.loads((ROOT/x['spec']).read_text());old=next(c for c in json.loads((ROOT/x['report']).read_text())['configs'].values() if c['fingerprint']==fp)
 for k,s in old['scenes'].items():sources.append([fp,x['asset'],x['capital_usdt'],sp['parameters']['fixed_entry_notional_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['cost_usdt'],s['funding_usdt'],s['executions'],s['NAV_sha256_f64le'],x['report'],x['report_sha256']])
write('source_curves.csv',['fingerprint','asset','actual_bank_capital','actual_entry_N','cost_multiplier','return_pct','whole_DD_pct','cost_usdt','funding_usdt','executions','NAV_sha256','readonly_report','readonly_report_sha256'],sources)
for g in p['grid']:alloc.append([g['fingerprint'],'candidate',g['L'],g['VC'],3750,15000,18750,375,4500,1,1,.2,.8,g['readonly']])
alloc.append([p['benchmark_parent_fingerprint'],'matched_initial_budget_hold',None,None,3750,15000,18750,375,4500,1,1,.2,.8,True]);write('fixed_allocations.csv',['fingerprint','role','ETH_L','entry_V10_volatility_ceiling_VC','BTC_bank','ETH_bank','total_initial_capital','BTC_N','ETH_N','raw_BTC_weight','raw_ETH_weight','BTC_capital_share','ETH_capital_share','readonly'],alloc)
put(R/'edge_flags.json',flags)
fig,axs=plt.subplots(2,4,figsize=(16,9),layout='constrained')
for row,(scope,key) in enumerate([('ETH native15000/N4500','all_current_native_grid'),('BTC3750+ETH15000 parent','all_current_grid')]):
 full=r[key]
 for j,(label,fn) in enumerate([('3x continuous370 return %',lambda c:c['scenes']['3']['net_return_pct']),('3x wholecurve DD %',lambda c:c['scenes']['3']['max_drawdown_pct']),('3x daily Sharpe365',lambda c:c['scenes']['3']['sharpe_365']),('3x recent positive5d /8',lambda c:sum(f['net_return_pct']>0 for f in c['scenes']['3']['recent40']['folds']))]):
  arr=np.empty((3,3))
  for c in full.values():arr[p['lookbacks'].index(c['L']),p['volatility_caps'].index(c['VC'])]=fn(c)
  ax=axs[row,j];im=ax.imshow(arr,cmap='RdYlGn_r' if j==1 else 'RdYlGn',**({'vmin':0,'vmax':8} if j==3 else {}));ax.set_xticks(range(3),['4%','4.5% old','5%']);ax.set_yticks(range(3),['L3','L4','L5']);ax.set_xlabel('ETH V10 entry volcap VC');ax.set_ylabel('ETH fast lookback L');ax.set_title(scope+'\n'+label,fontsize=10)
  for c in full.values():i,k=p['lookbacks'].index(c['L']),p['volatility_caps'].index(c['VC']);ax.text(k,i,f'{arr[i,k]:.3f}'+(' O' if c['readonly'] else ' N'),ha='center',va='center',fontsize=9)
  fig.colorbar(im,ax=ax,shrink=.7)
fig.suptitle('ETH fastL3/4/5 x V10cap4/4.5/5%, fixedHL1.5%/HS2.5%, fixed slowS28/E0.25%; V10 daily logvol ceiling varies\nActualBTC3750/N375 andETH15000/N4500 | rawweights[1,1],shares20/80%,noNAVscaling | O=readonly,N=new | reuseddevelopmenthistory')
fig.savefig(R/'sensitivity.png',dpi=140);plt.close(fig)
s={'report_sha256':sha(R/'report.json'),**p['expected_counts'],'passed':len(r['summary']['passed']),'rejected':len(r['summary']['candidate_rejected']),'failed_criteria':dict(collections.Counter(f for c in r['configs'].values() for f in c['failed_criteria'])),'CSV_rows':rows,'edge_flags':flags};put(R/'sensitivity_summary.json',s)
ctx=json.loads((R/'context.json').read_text());eq=[]
for c in r['configs'].values():
 grid=p['native_grid'] if c['scope']=='native' else p['grid'];key='all_current_native_grid' if c['scope']=='native' else 'all_current_grid';g=next(g for g in grid if g['L']==c['L'] and g['VC']==.045);base=r[key][g['fingerprint']]
 eq.append({'name':c['name'],'fingerprint':c['fingerprint'],'scope':c['scope'],'L':c['L'],'VC':c['VC'],'HL':.015,'matched_cap4_5_control_fingerprint':g['fingerprint'],'identical_full_NAV_by_cost':{k:c['scenes'][k]['NAV_sha256_f64le']==base['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3']},'all_cost_NAV_identical':all(c['scenes'][k]['NAV_sha256_f64le']==base['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3']),'cost_comparisons':{k:{'return_pct':c['scenes'][k]['net_return_pct'],'whole_DD_pct':c['scenes'][k]['max_drawdown_pct'],'control_return_pct':base['scenes'][k]['net_return_pct'],'control_DD_pct':base['scenes'][k]['max_drawdown_pct'],'delta_return_to_control_pp':c['scenes'][k]['net_return_pct']-base['scenes'][k]['net_return_pct'],'delta_DD_to_control_pp':c['scenes'][k]['max_drawdown_pct']-base['scenes'][k]['max_drawdown_pct']} for k in ['1','2','3']}})
put(R/'equivalent_realized_NAV_paths.json',{'report_sha256':sha(R/'report.json'),'comparisons':eq,'policy':'NewVC values are preserved as new definitions; identical realized fullNAV paths, if any, are disclosed rather than called independentalpha. Priorcap4.5 canonicalstatus/report unchanged, no completed-policy rerun.'})
lines=['# ETH 入场波动上限与回望联合验证','',f"完整读取{ctx['registry_events']}事件/{ctx['registry_ids']}ID、{len(ctx['prior_conclusions_read'])}份既往结论；排除观察后的完整研究定义数{ctx['canonical_research_definitions_excluding_observations']}。初始16条均有实际证据，无仅代码而缺实际回测的配置待补。本轮6个ETH原生与6个BTC/ETH组合、36成本场景逐项reserve后真实执行，正负期间与失败结果全部保留。",'',p['hypothesis'],'',
'预设两轴为快回望L=[3,4,5]与入场VC=[0.04,0.045,0.05]，V10是10个已完成日log收益的样本标准差，不是年化波动。多侧HL=0.015、空侧HS=0.025、E=0.0025、slowS28固定。4.5%的3原生/3组合、BTC和匹配持有父及其2原生共10个旧结果只读；不同实际VC参数是新定义，名称、组件顺序或数字格式本身不构成新配置。','',
'价格规则：fastROC=C[i−1]/C[i−1−L]−1，严格r>0.025空、r<−0.015多；等号不新开。否则实际多仅r<E保留、实际空仅r>−E保留，E=+0.0025、等号退出；绝对slow28方向始终门控，不同向退出。当rawdesired非零且不同于actual方向时，V10 samplelogvol>VC才过滤新开/翻向至flat；等号允许，同向已持仓不因高波动单独强平。没有最长持仓、慢幅度、残差或funding信号过滤。全部指标仅用前完整日，下一UTC00:01原生OPEN执行，翻向先平后开。','',
'原始资金和权重：BTC真实3750银行/N375沿用原ROC31/H4%/E1%实际净值；ETH真实15000银行/N4500以原生数量/成交/冲击/抵押执行。原[1,1]为两个完整银行美元NAV相加，总本金18750；20%/80%只是初始本金份额，不再乘一次或归一化。初始名义4875=26%本金，固定N除以前完整close后按LOT取整，OPEN不利tick，翻向/终止平仓计成本；无父调仓、同币克隆、资金转移、跨抵押、NAV复利调N或线性放缩旧净值。','',
'Walk-forward：2025-10-19UTC00:01至2026-10-24UTC00:01连续370天，12个完整30日折与10日尾折。账户现金、数量、已付成本跨折连续，完整分钟/事件NAV计算整体回撤。近期40天从day330继承，含8个5日折。固定规则无拟合/标签，purge0、预热30日+3日间隔，成本量/波动统计只用前20完整日。大量重复开发历史与总试验数已披露，不称未触碰最终留出、独立未来或DSR/PBO显著性。','',
'成本：每边手续费5bp、半价差1bp、滑点2bp、0.5×past20样本logvol×sqrt(实际q×OPEN/past20完整quoteADV)冲击，逐1/2/3倍。真实funding按结算ns/rate/mark/heldq入账，支出倍增、正收入不放大。核对LOT/tick/minnotional、参与率<=0.001、费用后1倍抵押和各银行独立1%闭合小时不利mark维护代理。线性永续无需现货借币，不虚构借币费；缺实测L2/TCA/完整历史档位/逐tick清算及容量证明。同本金/同初始N持有与现金0%并列，不称满仓或等风险对照。','',
'固定失败判据：各成本全年净正；1倍>=9/12正完整月；各成本近期净正且>=6/8正5日折；3倍整体DD<=25%；L/VC索引半径1含中心邻域的3倍净正、严格近期支持均>=60%；>=4底层平仓；1倍毛参考价格PnL+funding/执行成本>=2.5；零拒单、负抵押和小时代理违规、终止flat且>=180日。新原生与组合分别判断，旧4.5%原资格不改，当前邻域诊断另列。','',
'|新配置|范围|L|VC|1倍净%|2倍净%|3倍净%|3倍整体DD%|正月/12|近期正折1/2/3倍|状态|','|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|']
for c in r['configs'].values():lines.append('|'+c['name']+'|'+c['scope']+f"|{c['L']}|{c['VC']:.3f}|"+'|'.join(f"{c['scenes'][k]['net_return_pct']:.6f}" for k in ['1','2','3'])+f"|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['positive_complete_30d_folds_1x']}|"+'/'.join(str(c['recent40_positive_5d_folds_by_cost'][k]) for k in ['1','2','3'])+'|'+c['status']+'|')
lines.extend(['',f"新组合历史通过{len(r['summary']['passed'])}、淘汰{len(r['summary']['candidate_rejected'])}。逐项失败判据：{ {c['name']:c['failed_criteria'] for c in r['configs'].values()} }。年度收益不替代近期和邻域门槛。",'',f"新定义相对同L旧cap4.5%对照的三成本完整NAV全同{sum(z['all_cost_NAV_identical'] for z in eq)}/{len(eq)}；equivalent_realized_NAV_paths给出每成本hash、收益、完整DD差异。规则参数新颖不等于独立alpha，别名若存在也保留披露。",'',
'11份CSV包含36场景、完整月/尾折/近期折、每日NAV、原生和组合各九格敏感性、72条相邻边、来源/分配与持有/现金。图含收益、完整DD、Sharpe和近期正折，Calmar在表内。Sharpe正格比例、网格边界、描述性2std相邻悬崖单列，不当显著性或结果后追加门槛。','',
'合成检查先证明旧引擎只接纳4.5%而拒绝新4%参数；最小修改仅扩展为预设4/4.5/5%可接纳范围。72个L/VC/波动区间/方向案例覆盖样本sigma3.75/4.25/4.75/5.25%、新开/翻向过滤、同向持仓保留、VC等号和追加未来bar不变。18个旧对照行缺少新VC字段的fixture先于登记验证，检查VC元数据补齐、4/6/9邻域与原资格字段不变，避免上轮错误。独立Fraction/Decimal复核策略决策、实际数量/费用/冲击/资金费/小时风险/完整NAV与组合对齐，不调用simulate/decide/trade重新跑策略。','',
'原SMA与原singleS28从Nov2UTC08:30续至10:30，00/08资金费此前已记，不重复；SMA仅闭合分钟mark。独立未过滤L4/H2从10:10续至12:10，仅12:11参考闭合后采集，00/08不重记。全部cash/q/desired/risk/上下文/NAV前缀保留，不注入本批VC或非对称价格参数；SMA65日上下文仍引用20261102T015622Z。部分延迟shadow不替代十策略实时报价模拟，不新建账户/定时任务或取消原长期计划。','',
'一手来源实际访问2026-11-02：[Binance市场数据API](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)。8份真实年bars/mark/funding/约束文件路径/边界/字节/SHA256见plan及data_manifest；文档不证明本假设盈利、历史发布时刻或实测交易成本。','',
'所有实际配置逐项finish，同main排他锁内完成登记/来源/导出/监控检查，再提交非强制push。只读汇总不产生成交、不改冻结规则/本金/持仓，不部署网页、不加任务、不下真实订单。'])
(R/'result.md').write_text('\n'.join(lines)+'\n');print(json.dumps(s),flush=True)
