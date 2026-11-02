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
  cost.append([c['name'],c['fingerprint'],c['scope'],c['role'],c['asset'],c['L'],c['HL'],c['capital_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['cost_usdt'],s['cost_pct_initial'],s['funding_usdt'],s['gross_reference_PnL_to_execution_cost'],s['executions'],s['round_trips'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),c['status']])
  wf.extend([c['name'],c['scope'],c['L'],c['HL'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['duration_days'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['folds'])
  recent.extend([c['name'],c['scope'],c['L'],c['HL'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['recent40']['folds'])
  daily.extend([c['name'],c['scope'],k,i,v] for i,v in enumerate(s['daily_equity_usdt']))
write('cost_scenes.csv',['configuration','fingerprint','scope','role','asset','ETH_fast_L','long_entry_hurdle_HL','initial_capital','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','cost_usdt','cost_pct_initial','funding_usdt','gross_plus_funding_to_cost','executions','closes','recent40_return_pct','positive5d_folds','status'],cost)
write('walk_forward_folds.csv',['configuration','scope','ETH_fast_L','long_entry_hurdle_HL','cost_multiplier','fold','start_utc','end_exclusive_utc','days','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],wf)
write('recent40_folds.csv',['configuration','scope','ETH_fast_L','long_entry_hurdle_HL','cost_multiplier','fold','start_utc','end_exclusive_utc','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],recent)
write('daily_NAV.csv',['configuration','scope','cost_multiplier','boundary','NAV_usdt'],daily)
cols=['ETH_fast_L','long_entry_hurdle_HL','fingerprint','readonly_old','unchanged_canonical_status','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','recent40_return_pct','positive5d_folds','local_positive3_fraction','local_recent_fraction'];flags={};readonly=[]
for scope,grid,key in [('parent',p['grid'],'all_current_grid'),('native',p['native_grid'],'all_current_native_grid')]:
 full=r[key];items=[]
 for g in grid:
  c=full[g['fingerprint']]
  for k,s in c['scenes'].items():
   d=c['current_grid_diagnostic_sensitivity'];z=[g['L'],g['HL'],g['fingerprint'],g['readonly'],c['status'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),d['local_positive3_fraction'],d['local_strict_recent_fraction']];items.append(z)
   if scope=='parent' and g['readonly']:readonly.append(z)
 for k in ['1','2','3']:
  for g in grid:
   i,j=p['lookbacks'].index(g['L']),p['long_hurdles'].index(g['HL']);ng=[h for h in grid if i<2 and h['L']==p['lookbacks'][i+1] and h['HL']==g['HL'] or j<2 and h['HL']==p['long_hurdles'][j+1] and h['L']==g['L']]
   for h in ng:
    a,b=full[g['fingerprint']]['scenes'][k],full[h['fingerprint']]['scenes'][k];edges.append([scope,k,g['L'],g['HL'],h['L'],h['HL'],g['fingerprint'],h['fingerprint'],abs(a['sharpe_365']-b['sharpe_365']),abs(a['net_return_pct']-b['net_return_pct']),abs(a['max_drawdown_pct']-b['max_drawdown_pct'])])
 flags[scope]={}
 for k in ['1','2','3']:
  v=[x[8] for x in edges if x[0]==scope and x[1]==k];t=2*statistics.stdev(v);flags[scope][k]={'edge_count':len(v),'max_Sharpe_change':max(v),'two_std_change_threshold':t,'descriptive_cliff_flag':max(v)>t,'scope':'Dependentedgeheuristiconly,notstatisticalsignificance,DSRorPBO.'}
 write('sensitivity_grid.csv' if scope=='parent' else 'native_sensitivity_grid.csv',cols,items)
write('readonly_reused_scenes.csv',cols,readonly)
write('adjacent_edges.csv',['scope','cost_multiplier','from_L','from_HL','to_L','to_HL','from_fp','to_fp','absolute_Sharpe_change','absolute_return_change_pp','absolute_DD_change_pp'],edges)
cs=r['matched_hold_comparisons'];write('matched_hold_comparisons.csv',list(cs[0]),[list(x.values()) for x in cs])
for fp,x in p['read_only_references'].items():
 if x['scope']!='native':continue
 sp=json.loads((ROOT/x['spec']).read_text());old=next(c for c in json.loads((ROOT/x['report']).read_text())['configs'].values() if c['fingerprint']==fp)
 for k,s in old['scenes'].items():sources.append([fp,x['asset'],x['capital_usdt'],sp['parameters']['fixed_entry_notional_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['cost_usdt'],s['funding_usdt'],s['executions'],s['NAV_sha256_f64le'],x['report'],x['report_sha256']])
write('source_curves.csv',['fingerprint','asset','actual_bank_capital','actual_entry_N','cost_multiplier','return_pct','whole_DD_pct','cost_usdt','funding_usdt','executions','NAV_sha256','readonly_report','readonly_report_sha256'],sources)
for g in p['grid']:alloc.append([g['fingerprint'],'candidate',g['L'],g['HL'],3750,15000,18750,375,4500,1,1,.2,.8,g['readonly']])
alloc.append([p['benchmark_parent_fingerprint'],'matched_initial_budget_hold',None,None,3750,15000,18750,375,4500,1,1,.2,.8,True]);write('fixed_allocations.csv',['fingerprint','role','ETH_L','long_entry_hurdle_HL','BTC_bank','ETH_bank','total_initial_capital','BTC_N','ETH_N','raw_BTC_weight','raw_ETH_weight','BTC_capital_share','ETH_capital_share','readonly'],alloc)
put(R/'edge_flags.json',flags)
fig,axs=plt.subplots(2,4,figsize=(16,9),layout='constrained')
for row,(scope,key) in enumerate([('ETH native15000/N4500','all_current_native_grid'),('BTC3750+ETH15000 parent','all_current_grid')]):
 full=r[key]
 for j,(label,fn) in enumerate([('3x continuous370 return %',lambda c:c['scenes']['3']['net_return_pct']),('3x wholecurve DD %',lambda c:c['scenes']['3']['max_drawdown_pct']),('3x daily Sharpe365',lambda c:c['scenes']['3']['sharpe_365']),('3x recent positive5d /8',lambda c:sum(f['net_return_pct']>0 for f in c['scenes']['3']['recent40']['folds']))]):
  arr=np.empty((3,3))
  for c in full.values():arr[p['lookbacks'].index(c['L']),p['long_hurdles'].index(c['HL'])]=fn(c)
  ax=axs[row,j];im=ax.imshow(arr,cmap='RdYlGn_r' if j==1 else 'RdYlGn',**({'vmin':0,'vmax':8} if j==3 else {}));ax.set_xticks(range(3),['1%','1.5%','2% old']);ax.set_yticks(range(3),['L3','L4','L5']);ax.set_xlabel('ETH long hurdle HL (short fixed2.5%)');ax.set_ylabel('ETH fast lookback L');ax.set_title(scope+'\n'+label,fontsize=10)
  for c in full.values():i,k=p['lookbacks'].index(c['L']),p['long_hurdles'].index(c['HL']);ax.text(k,i,f'{arr[i,k]:.3f}'+(' O' if c['readonly'] else ' N'),ha='center',va='center',fontsize=9)
  fig.colorbar(im,ax=ax,shrink=.7)
fig.suptitle('ETH fastL3/4/5 x longHL1/1.5/2%, shortHS2.5%, fixed slowS28, E0.25%, V10/cap4.5%\nActualBTC3750/N375 andETH15000/N4500 | rawweights[1,1],shares20/80%,noNAVscaling | O=readonly,N=new | reuseddevelopmenthistory')
fig.savefig(R/'sensitivity.png',dpi=140);plt.close(fig)
s={'report_sha256':sha(R/'report.json'),**p['expected_counts'],'passed':len(r['summary']['passed']),'rejected':len(r['summary']['candidate_rejected']),'failed_criteria':dict(collections.Counter(f for c in r['configs'].values() for f in c['failed_criteria'])),'CSV_rows':rows,'edge_flags':flags};put(R/'sensitivity_summary.json',s)
ctx=json.loads((R/'context.json').read_text());eq=[]
for c in r['configs'].values():
 grid=p['native_grid'] if c['scope']=='native' else p['grid'];key='all_current_native_grid' if c['scope']=='native' else 'all_current_grid';baseg=next(g for g in grid if g['L']==c['L'] and g['HL']==.02);base=r[key][baseg['fingerprint']]
 eq.append({'name':c['name'],'fingerprint':c['fingerprint'],'scope':c['scope'],'L':c['L'],'HL':c['HL'],'matched_prior_HL2_fingerprint':baseg['fingerprint'],'identical_full_NAV_by_cost':{k:c['scenes'][k]['NAV_sha256_f64le']==base['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3']},'all_cost_NAV_identical':all(c['scenes'][k]['NAV_sha256_f64le']==base['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3']),'cost_comparisons':{k:{'return_pct':c['scenes'][k]['net_return_pct'],'whole_DD_pct':c['scenes'][k]['max_drawdown_pct'],'prior_HL2_return_pct':base['scenes'][k]['net_return_pct'],'prior_HL2_DD_pct':base['scenes'][k]['max_drawdown_pct'],'delta_return_to_prior_HL2_pp':c['scenes'][k]['net_return_pct']-base['scenes'][k]['net_return_pct'],'delta_DD_to_prior_HL2_pp':c['scenes'][k]['max_drawdown_pct']-base['scenes'][k]['max_drawdown_pct']} for k in ['1','2','3']}})
put(R/'equivalent_realized_NAV_paths.json',{'report_sha256':sha(R/'report.json'),'comparisons':eq,'policy':'Different long hurdle is retained as a new definition; any same realized fullNAV paths are disclosed, not independent alpha. Symmetric old canonical status/report unchanged, no completed-policy rerun.'})
lines=['# ETH 多空非对称入场阈值验证','',f"完整读取{ctx['registry_events']}事件/{ctx['registry_ids']}ID、{len(ctx['prior_conclusions_read'])}份既往结论，排除持续观察后的历史研究定义数{ctx['canonical_research_definitions_excluding_observations']}。初始16项均有实际证据，无缺失回测需要重跑。本轮6个新ETH组件+6个新BTC/ETH组合、36成本场景逐项reserve后实际计算，所有正负期间与结果完整保留。",'',p['hypothesis'],'',
'预设两轴为快回望L=[3,4,5]与多仓入场阈值HL=[0.01,0.015,0.02]，空仓阈值HS固定0.025，原return_hurdle字段表示本批固定空侧。HL=2%的三个原生/三个父、BTC和匹配持有父/两原生共10旧定义只读；其余6原生与6父为新配置。既往共同调整多空H的网格与本批不同；完整spec指纹查重，不按family排除。','',
'完整价格规则：fastROC=C[i−1]/C[i−1−L]−1。严格r>+HS空、r<−HL多；等号不新开。其余区间，实际多仅r<E、实际空仅r>−E保留，E=+0.0025，等号退出；绝对slow28方向始终门控，不匹配退出。V10样本logvol>0.045只过滤新开/翻向。原先更早退出及实际同向数量保留不变，普通翻向先平后开。无最长持仓、慢趋势幅度门槛、BTC残差或资金费入场信号。','',
'经济假设为多空触发条件可能偏好不同幅度，本批固定空侧以隔离多侧变化；更小HL可能增加换手，更大HL可能错失有效回撤。这是假设而非官方盈利结论，不在结果后改阈值或宽限近期/敏感性门槛。','',
'资金与原始权重：BTC真实银行3750/N375旧ROC31/H4%/E1%曲线只读；ETH15000/N4500按原生数量/冲击/抵押重新执行。原[1,1]是两个完整银行美元NAV相加，总本金18750，初始本金份额20%/80%仅说明资金分配，不再次相乘或自动归一化。初始名义总4875=26%本金。固定N/前完整close按LOT向下取整，下一UTC00:01原生OPEN不利tick，终止平仓计成本；无父调仓、转账、跨抵押、复利调N或线性缩放旧净值。','',
'Walk-forward区间2025-10-19UTC00:01至2026-10-24UTC00:01连续370天，12完整30日折+10日尾折；现金/数量/费用跨折不重置，全分钟/事件NAV计算整体回撤。近期40天继承day330与8×5日折。固定规则无拟合/标签，purge0、预热30+间隔3，ADV/波动仅前20完整日。历史经过大量反复开发，多重试验数保留，不称未触碰最终留出、独立未来或DSR/PBO显著性。','',
'1/2/3倍成本每边5bp手续费、1bp半价差、2bp滑点、0.5×past20样本logvol×sqrt(实际q×OPEN/past20完整quoteADV)冲击。真实资金费按每次settlement/rate/mark/heldq入账，支出倍增而正收入不放大。原生LOT/tick/minnotional、参与率<=0.001、费用后1倍抵押、各银行独立1%闭合小时不利mark维护代理均审核。线性永续不需现货借币，不虚构借币费；缺L2/TCA/完整历史档位/逐tick清算或容量证明。匹配本金与初始N持有及现金0%并列，非满仓或等风险持有。','',
'预先不变的失败门槛：每成本全年净正，1倍>=9/12正完整月；每成本近期净正且>=6/8正5日折；3倍整体DD<=25%；L/HL索引半径1含中心邻域的3倍净正及严格近期支持均>=60%；>=4平仓，毛参考价格PnL加fund/执行成本>=2.5；零拒单、负抵押、小时维护代理违规，终止flat且>=180天。新原生和父各自判断，旧HL2%结果不改资格，仅新增当前邻域诊断。','',
'|新配置|范围|L|多仓HL|1倍净%|2倍净%|3倍净%|3倍整体DD%|正月/12|近期正折1/2/3倍|状态|','|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|']
for c in r['configs'].values():
 lines.append('|'+c['name']+'|'+c['scope']+f"|{c['L']}|{c['HL']:.3f}|"+'|'.join(f"{c['scenes'][k]['net_return_pct']:.6f}" for k in ['1','2','3'])+f"|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['positive_complete_30d_folds_1x']}|"+'/'.join(str(c['recent40_positive_5d_folds_by_cost'][k]) for k in ['1','2','3'])+'|'+c['status']+'|')
lines.extend(['',f"新父历史通过{len(r['summary']['passed'])}、淘汰{len(r['summary']['candidate_rejected'])}，逐配置失败判据{ {c['name']:c['failed_criteria'] for c in r['configs'].values()} }。年度正收益不替代近期或局部邻域门槛。",'',f"新配置与同L旧HL2%/HS2.5%对照的三成本完整NAV全同{sum(z['all_cost_NAV_identical'] for z in eq)}/{len(eq)}，逐成本收益/DD差异与匹配fingerprint见equivalent_realized_NAV_paths。参数新颖不等于新alpha，同路径别名不删除、不改旧资格。",'',
'11CSV包含36场景、逐月/尾折/近期折、每日NAV、原生/父完整9格敏感性、72相邻边、持有/现金、旧来源与原分配。两面八指标图显示收益、全曲线DD、Sharpe和近期正折；Sharpe正格比例、边界峰值与描述性2std悬崖另列，不当作显著性，不按结果扩展本批门槛。','',
'合成TDD先证明旧代码用2.5%对称门槛会把新多侧1%策略的1.2%回撤留空；复用既有非对称引擎检查L3/4/5×HL1/1.5/2%、固定空侧2.5%等号/严格穿越、原持仓保留/退出/翻向、slow方向门、未来bar追加不变与隐式对称参数恒等。独立Fraction重算两侧价格规则，Decimal复核真实数量/成交/费用/资金费/小时风险/完整NAV及父对齐，不调用simulate/decide/trade重新回测。','',
'冻结账户另行续接：原SMA和singleS28从Nov2UTC04:30至06:30，已处理00资金费/日决策不重复；独立未过滤L4/H2从06:10至08:10，仅08:11参考闭合后采集。保留完整cash/q/desired/risk/上下文/NAV前缀，不注入研究非对称参数；SMA真实65日上下文继续引用20261102T015622Z。部分延迟shadow不替代十策略实时报价模拟，不取消长期计划或新建账户。','',
'一手来源实际访问2026-11-02：[Binance市场数据API](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)。8份真实bars/mark/funding/约束文件的hash、字节与边界在plan/data_manifest；文档不证明策略盈利或历史网络发布时刻，假设和局限分别留档。','',
'同main排他锁内逐项finish、登记/来源/导出/监控检查、提交非强制push。只读汇总不产生成交、不改冻结规则/本金/持仓、不部署网页或新建任务。不下真实订单，正回测不称稳定实盘盈利。'])
(R/'result.md').write_text('\n'.join(lines)+'\n');print(json.dumps(s),flush=True)
