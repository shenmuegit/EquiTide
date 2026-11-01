"""Export saved real native/parent L/A results; no strategy calculation."""
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
  cost.append([c['name'],c['fingerprint'],c['scope'],c['role'],c['asset'],c['L'],c['A'],c['capital_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['cost_usdt'],s['cost_pct_initial'],s['funding_usdt'],s['gross_reference_PnL_to_execution_cost'],s['executions'],s['round_trips'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),c['status']])
  wf.extend([c['name'],c['scope'],c['L'],c['A'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['duration_days'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['folds'])
  recent.extend([c['name'],c['scope'],c['L'],c['A'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['recent40']['folds'])
  daily.extend([c['name'],c['scope'],k,i,v] for i,v in enumerate(s['daily_equity_usdt']))
write('cost_scenes.csv',['configuration','fingerprint','scope','role','asset','ETH_fast_L','BTC_return_control_A','initial_capital','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','cost_usdt','cost_pct_initial','funding_usdt','gross_plus_funding_to_cost','executions','closes','recent40_return_pct','positive5d_folds','status'],cost)
write('walk_forward_folds.csv',['configuration','scope','ETH_fast_L','BTC_return_control_A','cost_multiplier','fold','start_utc','end_exclusive_utc','days','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],wf)
write('recent40_folds.csv',['configuration','scope','ETH_fast_L','BTC_return_control_A','cost_multiplier','fold','start_utc','end_exclusive_utc','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],recent)
write('daily_NAV.csv',['configuration','scope','cost_multiplier','boundary','NAV_usdt'],daily)
cols=['ETH_fast_L','BTC_return_control_A','fingerprint','readonly_old','unchanged_canonical_status','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','recent40_return_pct','positive5d_folds','local_positive3_fraction','local_recent_fraction'];flags={};readonly=[]
for scope,grid,key in [('parent',p['grid'],'all_current_grid'),('native',p['native_grid'],'all_current_native_grid')]:
 full=r[key];items=[]
 for g in grid:
  c=full[g['fingerprint']]
  for k,s in c['scenes'].items():
   d=c['current_grid_diagnostic_sensitivity'];z=[g['L'],g['A'],g['fingerprint'],g['readonly'],c['status'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),d['local_positive3_fraction'],d['local_strict_recent_fraction']];items.append(z)
   if scope=='parent' and g['readonly']:readonly.append(z)
 for k in ['1','2','3']:
  for g in grid:
   i,j=p['lookbacks'].index(g['L']),p['btc_control_weights'].index(g['A']);ng=[h for h in grid if i<2 and h['L']==p['lookbacks'][i+1] and h['A']==g['A'] or j<2 and h['A']==p['btc_control_weights'][j+1] and h['L']==g['L']]
   for h in ng:
    a,b=full[g['fingerprint']]['scenes'][k],full[h['fingerprint']]['scenes'][k];edges.append([scope,k,g['L'],g['A'],h['L'],h['A'],g['fingerprint'],h['fingerprint'],abs(a['sharpe_365']-b['sharpe_365']),abs(a['net_return_pct']-b['net_return_pct']),abs(a['max_drawdown_pct']-b['max_drawdown_pct'])])
 flags[scope]={}
 for k in ['1','2','3']:
  v=[x[8] for x in edges if x[0]==scope and x[1]==k];t=2*statistics.stdev(v);flags[scope][k]={'edge_count':len(v),'max_Sharpe_change':max(v),'two_std_change_threshold':t,'descriptive_cliff_flag':max(v)>t,'scope':'Dependentedgeheuristiconly,notstatisticalsignificance,DSRorPBO.'}
 write('sensitivity_grid.csv' if scope=='parent' else 'native_sensitivity_grid.csv',cols,items)
write('readonly_reused_scenes.csv',cols,readonly)
write('adjacent_edges.csv',['scope','cost_multiplier','from_L','from_A','to_L','to_A','from_fp','to_fp','absolute_Sharpe_change','absolute_return_change_pp','absolute_DD_change_pp'],edges)
cs=r['matched_hold_comparisons'];write('matched_hold_comparisons.csv',list(cs[0]),[list(x.values()) for x in cs])
for fp,x in p['read_only_references'].items():
 if x['scope']!='native':continue
 sp=json.loads((ROOT/x['spec']).read_text());old=next(c for c in json.loads((ROOT/x['report']).read_text())['configs'].values() if c['fingerprint']==fp)
 for k,s in old['scenes'].items():sources.append([fp,x['asset'],x['capital_usdt'],sp['parameters']['fixed_entry_notional_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['cost_usdt'],s['funding_usdt'],s['executions'],s['NAV_sha256_f64le'],x['report'],x['report_sha256']])
write('source_curves.csv',['fingerprint','asset','actual_bank_capital','actual_entry_N','cost_multiplier','return_pct','whole_DD_pct','cost_usdt','funding_usdt','executions','NAV_sha256','readonly_report','readonly_report_sha256'],sources)
for g in p['grid']:alloc.append([g['fingerprint'],'candidate',g['L'],g['A'],3750,15000,18750,375,4500,1,1,.2,.8,g['readonly']])
alloc.append([p['benchmark_parent_fingerprint'],'matched_initial_budget_hold',None,None,3750,15000,18750,375,4500,1,1,.2,.8,True]);write('fixed_allocations.csv',['fingerprint','role','ETH_L','BTC_return_control_A','BTC_bank','ETH_bank','total_initial_capital','BTC_N','ETH_N','raw_BTC_weight','raw_ETH_weight','BTC_capital_share','ETH_capital_share','readonly'],alloc)
put(R/'edge_flags.json',flags)
fig,axs=plt.subplots(2,4,figsize=(16,9),layout='constrained')
for row,(scope,key) in enumerate([('ETH native15000/N4500','all_current_native_grid'),('BTC3750+ETH15000 parent','all_current_grid')]):
 full=r[key]
 for j,(label,fn) in enumerate([('3x continuous370 return %',lambda c:c['scenes']['3']['net_return_pct']),('3x wholecurve DD %',lambda c:c['scenes']['3']['max_drawdown_pct']),('3x daily Sharpe365',lambda c:c['scenes']['3']['sharpe_365']),('3x recent positive5d /8',lambda c:sum(f['net_return_pct']>0 for f in c['scenes']['3']['recent40']['folds']))]):
  arr=np.empty((3,3))
  for c in full.values():arr[p['lookbacks'].index(c['L']),p['btc_control_weights'].index(c['A'])]=fn(c)
  ax=axs[row,j];im=ax.imshow(arr,cmap='RdYlGn_r' if j==1 else 'RdYlGn',**({'vmin':0,'vmax':8} if j==3 else {}));ax.set_xticks(range(3),['A0','A0.5','A1']);ax.set_yticks(range(3),['L3','L4','L5']);ax.set_xlabel('BTC return control coefficient A');ax.set_ylabel('ETH fast lookback L');ax.set_title(scope+'\n'+label,fontsize=10)
  for c in full.values():i,k=p['lookbacks'].index(c['L']),p['btc_control_weights'].index(c['A']);ax.text(k,i,f'{arr[i,k]:.3f}'+(' O' if c['readonly'] else ' N'),ha='center',va='center',fontsize=9)
  fig.colorbar(im,ax=ax,shrink=.7)
fig.suptitle('ETH fastL3/4/5 x BTC control A0/0.5/1, fixed slowS28, fixedH2.5%, E0.25%, V10/cap4.5%\nActualBTC3750/N375 andETH15000/N4500 | rawweights[1,1],shares20/80%,noNAVscaling | O=readonly,N=new | reuseddevelopmenthistory')
fig.savefig(R/'sensitivity.png',dpi=140);plt.close(fig)
s={'report_sha256':sha(R/'report.json'),**p['expected_counts'],'passed':len(r['summary']['passed']),'rejected':len(r['summary']['candidate_rejected']),'failed_criteria':dict(collections.Counter(f for c in r['configs'].values() for f in c['failed_criteria'])),'CSV_rows':rows,'edge_flags':flags};put(R/'sensitivity_summary.json',s)
ctx=json.loads((R/'context.json').read_text());lines=['# BTC控制的ETH反向信号验证','',f"完整读取{ctx['registry_events']}登记事件/{ctx['registry_ids']}ID、{len(ctx['prior_conclusions_read'])}份历史结论；初始16项真实结果证据齐全。预设L3/4/5×A0/0.5/1，A0三格原生和三格父及匹配持有父/来源共10个旧定义只读。A0.5/A1新增6个ETH组件和6个BTC/ETH组合、36个成本场景，每个配置先reserve成功后计算并独立finish。",'',
'经济假设：用BTC同期已实现收益控制ETH短窗收益中的共同市场成分，可能改善反向信号，也可能移除有用反转信息。固定系数不拟合，不在本轮结果上再选择网格。上一轮连续确认不注入本机制。','',p['hypothesis'],'',
'完整规则：两币L日简单收益r=C[i-1]/C[i-1-L]−1，x=rETH−A*rBTC，L=3/4/5、A=0/0.5/1；x>2.5%空、x<−2.5%多。带内实际多仅x<0.25%、实际空仅x>−0.25%保留，等号退出；ETH绝对28日slow方向不匹配始终退出，当前ETH10日样本logvol>4.5%只阻止新入场/翻向。同向保留不重置q，反向先平再开。A只控制信号，不改变资金权重或数量，不创建BTC对冲订单，不声称市场中性。','',
'两币完整分钟open时间轴和日close索引对齐；信号可得时间取两币真实available最大值，只使用此前已完成日线，之后下一UTC00:01原生OPEN执行。ETH按原生LOT从固定名义预算4500/前日ETHclose向下取整，费用和funding均使用实际ETHq；BTC独立组件原ROC31/H4%/E1%原生3750本金/375名义路径只读复用。ETH本金15000，原权重[1,1]代表两份完整银行，美元净值相加，总本金18750，资金份额20%/80%不再次乘权重、不归一化。无父调仓、转账、线性NAV缩放或跨抵押。','',
'真实边界2025-10-19UTC00:01至2026-10-24UTC00:01，连续370天、12完整30天折加10天尾段；状态/现金/q/成本跨折不重置，day330继承近期40天/8×5天。固定无训练标签，purge0、30日预热加3日间隔；所有价格/quoteADV/logvol当时已可得。反复开发历史及全部试验数量在context，不能称未触碰最终测试；局部比例没有消除多重选择偏差，未声称DSR/PBO显著性。','',
'失败判据预固定：每档全年净正、1倍>=9/12正完整月；每档近期净正且>=6/8正5日折；3倍整体DD<=25%；L/A索引半径1含中心局部3倍净正和严格近期支持均>=60%；>=4平仓、毛参考PnL加fund/执行成本>=2.5，零拒单/负抵押/维护代理违规，终止flat、至少180天。原生与父分别判定；旧A0的canonical资格/原敏感性/报告不改，仅另列当前邻域诊断。','',
'费用每边5bp、半价差1bp、滑点2bp、冲击0.5×过去20日样本logvol×sqrt(实际q×OPEN/过去20完整日quoteADV)，1/2/3倍压力；真实funding纳秒/rate/mark/当时q，支出倍增、正收入不放大。原生LOT/tick/minnotional、参与率<=0.001、费用后1倍入场抵押、独立银行1%闭合小时不利mark维护代理。线性永续不需要现货借币，不虚构借币费；无TCA/L2、完整历史档位/逐tick清算或容量证明。匹配本金/初始N持有与现金0%为对照，非满仓或同风险持有。','',
'|新配置|范围|L|A|1倍净%|2倍净%|3倍净%|3倍整体DD%|正月/12|近期正折1/2/3倍|状态|','|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|']
for c in r['configs'].values():lines.append('|'+c['name']+'|'+c['scope']+f"|{c['L']}|{c['A']}|"+'|'.join(f"{c['scenes'][k]['net_return_pct']:.6f}" for k in ['1','2','3'])+f"|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['positive_complete_30d_folds_1x']}|"+'/'.join(str(c['recent40_positive_5d_folds_by_cost'][k]) for k in ['1','2','3'])+'|'+c['status']+'|')
lines+=['',f"新父候选：{len(r['summary']['passed'])}历史通过、{len(r['summary']['candidate_rejected'])}淘汰。所有新配置失败原因：{ {c['name']:c['failed_criteria'] for c in r['configs'].values()} }。所有负收益/负期间保存，不放宽门槛或按新结果增加其他系数。",'',
'11CSV保存全部36成本场景、逐完整月和尾段、近期5日折、每日NAV、原生/父完整9格敏感性、72相邻边、匹配持有/现金、旧来源与原资金分配。完整NAV SHA及必要逐笔/资金费/状态段/父来源哈希支持独立重建。多指标与描述性2std悬崖不等于统计显著性；最大值在边界如实标明，不自动扩展本批。','',
'合成TDD旧代码不能在A1抵消两币共同变化，预期红灯留档；新实现验证残差Fraction、两方向/等号/slow门控/保留/退出/A0恒等和两币未来扰动。实际独审直接读取BTC原数据独立计算信号和两币可得时间最大值，不借用策略decide。','',
'冻结原SMA/singleS28按原cash/q/desired/risk/全NAV续16:30至18:30，独立未过滤L4/H2续18:10至20:10且20:11参考分钟闭合后采集；16资金费已实际计入，不能重记。原规则/本金/终止计划不改，本轮A不注入原账户；部分观察rejected不取消长期计划，延迟shadow不作十策略实盘报价成交。','',
'一手来源于2026-11-01复查：[Binance官方市场数据文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)；接口版本/字段见primary_sources，文档样例不作行情证据，实际Parquet/API字节和SHA单独核验。','',
'全程同main排他锁；监控只读既有报告和账户，不产生成交，不改冻结规则/本金/持仓，不重部署网页或建定时任务，不下真实订单。']
(R/'result.md').write_text('\n'.join(lines)+'\n');print(json.dumps(s),flush=True)
