"""Export saved real native/parent L/K results; no strategy calculation."""
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
  cost.append([c['name'],c['fingerprint'],c['scope'],c['role'],c['asset'],c['L'],c['K'],c['capital_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['cost_usdt'],s['cost_pct_initial'],s['funding_usdt'],s['gross_reference_PnL_to_execution_cost'],s['executions'],s['round_trips'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),c['status']])
  wf.extend([c['name'],c['scope'],c['L'],c['K'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['duration_days'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['folds'])
  recent.extend([c['name'],c['scope'],c['L'],c['K'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['recent40']['folds'])
  daily.extend([c['name'],c['scope'],k,i,v] for i,v in enumerate(s['daily_equity_usdt']))
write('cost_scenes.csv',['configuration','fingerprint','scope','role','asset','ETH_fast_L','ETH_entry_confirmation_K','initial_capital','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','cost_usdt','cost_pct_initial','funding_usdt','gross_plus_funding_to_cost','executions','closes','recent40_return_pct','positive5d_folds','status'],cost)
write('walk_forward_folds.csv',['configuration','scope','ETH_fast_L','ETH_entry_confirmation_K','cost_multiplier','fold','start_utc','end_exclusive_utc','days','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],wf)
write('recent40_folds.csv',['configuration','scope','ETH_fast_L','ETH_entry_confirmation_K','cost_multiplier','fold','start_utc','end_exclusive_utc','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],recent)
write('daily_NAV.csv',['configuration','scope','cost_multiplier','boundary','NAV_usdt'],daily)
cols=['ETH_fast_L','ETH_entry_confirmation_K','fingerprint','readonly_old','unchanged_canonical_status','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','recent40_return_pct','positive5d_folds','local_positive3_fraction','local_recent_fraction'];flags={};readonly=[]
for scope,grid,key in [('parent',p['grid'],'all_current_grid'),('native',p['native_grid'],'all_current_native_grid')]:
 full=r[key];items=[]
 for g in grid:
  c=full[g['fingerprint']]
  for k,s in c['scenes'].items():
   d=c['current_grid_diagnostic_sensitivity'];z=[g['L'],g['K'],g['fingerprint'],g['readonly'],c['status'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),d['local_positive3_fraction'],d['local_strict_recent_fraction']];items.append(z)
   if scope=='parent' and g['readonly']:readonly.append(z)
 for k in ['1','2','3']:
  for g in grid:
   i,j=p['lookbacks'].index(g['L']),p['confirmation_days'].index(g['K']);ng=[h for h in grid if i<2 and h['L']==p['lookbacks'][i+1] and h['K']==g['K'] or j<2 and h['K']==p['confirmation_days'][j+1] and h['L']==g['L']]
   for h in ng:
    a,b=full[g['fingerprint']]['scenes'][k],full[h['fingerprint']]['scenes'][k];edges.append([scope,k,g['L'],g['K'],h['L'],h['K'],g['fingerprint'],h['fingerprint'],abs(a['sharpe_365']-b['sharpe_365']),abs(a['net_return_pct']-b['net_return_pct']),abs(a['max_drawdown_pct']-b['max_drawdown_pct'])])
 flags[scope]={}
 for k in ['1','2','3']:
  v=[x[8] for x in edges if x[0]==scope and x[1]==k];t=2*statistics.stdev(v);flags[scope][k]={'edge_count':len(v),'max_Sharpe_change':max(v),'two_std_change_threshold':t,'descriptive_cliff_flag':max(v)>t,'scope':'Dependentedgeheuristiconly,notstatisticalsignificance,DSRorPBO.'}
 write('sensitivity_grid.csv' if scope=='parent' else 'native_sensitivity_grid.csv',cols,items)
write('readonly_reused_scenes.csv',cols,readonly)
write('adjacent_edges.csv',['scope','cost_multiplier','from_L','from_K','to_L','to_K','from_fp','to_fp','absolute_Sharpe_change','absolute_return_change_pp','absolute_DD_change_pp'],edges)
cs=r['matched_hold_comparisons'];write('matched_hold_comparisons.csv',list(cs[0]),[list(x.values()) for x in cs])
for fp,x in p['read_only_references'].items():
 if x['scope']!='native':continue
 sp=json.loads((ROOT/x['spec']).read_text());old=next(c for c in json.loads((ROOT/x['report']).read_text())['configs'].values() if c['fingerprint']==fp)
 for k,s in old['scenes'].items():sources.append([fp,x['asset'],x['capital_usdt'],sp['parameters']['fixed_entry_notional_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['cost_usdt'],s['funding_usdt'],s['executions'],s['NAV_sha256_f64le'],x['report'],x['report_sha256']])
write('source_curves.csv',['fingerprint','asset','actual_bank_capital','actual_entry_N','cost_multiplier','return_pct','whole_DD_pct','cost_usdt','funding_usdt','executions','NAV_sha256','readonly_report','readonly_report_sha256'],sources)
for g in p['grid']:alloc.append([g['fingerprint'],'candidate',g['L'],g['K'],3750,15000,18750,375,4500,1,1,.2,.8,g['readonly']])
alloc.append([p['benchmark_parent_fingerprint'],'matched_initial_budget_hold',None,None,3750,15000,18750,375,4500,1,1,.2,.8,True]);write('fixed_allocations.csv',['fingerprint','role','ETH_L','ETH_entry_confirmation_K','BTC_bank','ETH_bank','total_initial_capital','BTC_N','ETH_N','raw_BTC_weight','raw_ETH_weight','BTC_capital_share','ETH_capital_share','readonly'],alloc)
put(R/'edge_flags.json',flags)
fig,axs=plt.subplots(2,4,figsize=(16,9),layout='constrained')
for row,(scope,key) in enumerate([('ETH native15000/N4500','all_current_native_grid'),('BTC3750+ETH15000 parent','all_current_grid')]):
 full=r[key]
 for j,(label,fn) in enumerate([('3x continuous370 return %',lambda c:c['scenes']['3']['net_return_pct']),('3x wholecurve DD %',lambda c:c['scenes']['3']['max_drawdown_pct']),('3x daily Sharpe365',lambda c:c['scenes']['3']['sharpe_365']),('3x recent positive5d /8',lambda c:sum(f['net_return_pct']>0 for f in c['scenes']['3']['recent40']['folds']))]):
  arr=np.empty((3,3))
  for c in full.values():arr[p['lookbacks'].index(c['L']),p['confirmation_days'].index(c['K'])]=fn(c)
  ax=axs[row,j];im=ax.imshow(arr,cmap='RdYlGn_r' if j==1 else 'RdYlGn',**({'vmin':0,'vmax':8} if j==3 else {}));ax.set_xticks(range(3),['K1','K2','K3']);ax.set_yticks(range(3),['L3','L4','L5']);ax.set_xlabel('ETH consecutive entry confirmation K');ax.set_ylabel('ETH fast lookback L');ax.set_title(scope+'\n'+label,fontsize=10)
  for c in full.values():i,k=p['lookbacks'].index(c['L']),p['confirmation_days'].index(c['K']);ax.text(k,i,f'{arr[i,k]:.3f}'+(' O' if c['readonly'] else ' N'),ha='center',va='center',fontsize=9)
  fig.colorbar(im,ax=ax,shrink=.7)
fig.suptitle('ETH fastL3/4/5 x confirmationK1/2/3, fixed slowS28, fixedH2.5%, E0.25%, V10/cap4.5%\nActualBTC3750/N375 andETH15000/N4500 | rawweights[1,1],shares20/80%,noNAVscaling | O=readonly,N=new | reuseddevelopmenthistory')
fig.savefig(R/'sensitivity.png',dpi=140);plt.close(fig)
s={'report_sha256':sha(R/'report.json'),**p['expected_counts'],'passed':len(r['summary']['passed']),'rejected':len(r['summary']['candidate_rejected']),'failed_criteria':dict(collections.Counter(f for c in r['configs'].values() for f in c['failed_criteria'])),'CSV_rows':rows,'edge_flags':flags};put(R/'sensitivity_summary.json',s)
ctx=json.loads((R/'context.json').read_text());lines=['# ETH连续入场确认联合验证','',f"完整读取{ctx['registry_events']}登记事件/{ctx['registry_ids']}ID、{len(ctx['prior_conclusions_read'])}份既往结论，初始16项实际结果证据齐全。本轮固定L3/4/5×K1/2/3，K1的3个原生及3个父格点、匹配持有父和来源共10个旧定义只读。K2/K3新增6个ETH原生与6个BTC/ETH父定义；12配置36成本场景均先reserve再计算并独立finish，所有负收益及失败保留。",'',p['hypothesis'],'',
'经济假设：连续多个已完成日的同向ROC极值可减少瞬时反转噪声与换手，也可能错过反转早段。只测这一预定机制与快周期敏感性；历史SMA或排名确认实验的不同完整配置不能替代本次真实结果。','',
p['rules']['signal'],'',p['rules']['allocation'],'',p['rules']['execution'],'',p['rules']['costs'],'',
'真实数据边界2025-10-19UTC00:01至2026-10-24UTC00:01，连续370日、12完整30日折加10日尾段；不按折重开账户，近期40日继承day330现金/数量/成本，8个5日折。固定规则没有训练标签，purge0，30日预热加3日间隔；所有确认日和过去20日成本统计来自当时已完成数据。此历史已反复用于选择，不能称未触碰最终测试或独立未来证据；登记试验数见context，多重选择偏差未由局部比例消除，未声称DSR/PBO统计显著性。','',
'失败判据沿用：每档全年净正、1倍>=9/12正完整月；每档近期净正且>=6/8正5日折；3倍全曲线DD<=25%；L/K索引半径1含中心的局部3倍净正、严格近期比例均>=60%；至少4次平仓、毛参考PnL加fund/执行成本>=2.5；零拒单/负抵押/维护代理违规、终止flat、至少180日。单币与父组合分别判断；旧canonical状态、原敏感性与报告字节均不重写，当前邻域仅另作诊断。','',
'成本模型包含5bp费用、1bp半价差、2bp滑点、按实际成交q/过去20日quoteADV和logvol的平方根冲击；1/2/3倍费用与负资金费压力，真实funding结算时刻/rate/mark/当时q，正收入不放大。原生LOT/tick/minnotional、参与率<=0.001、费用后1倍入场抵押、独立银行1%闭合小时不利mark维护代理。线性永续没有现货借币；不虚构借币费、历史完整档位、TCA/L2/逐tick清算或容量证明。匹配持有与现金0%为对照，匹配持有仅同资金/初始N，并非满仓或同风险配置。','',
'|新配置|范围|L|K|1倍净%|2倍净%|3倍净%|3倍整体DD%|正月/12|近期正折1/2/3倍|状态|','|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|']
for c in r['configs'].values():
 lines.append('|'+c['name']+'|'+c['scope']+f"|{c['L']}|{c['K']}|"+'|'.join(f"{c['scenes'][k]['net_return_pct']:.6f}" for k in ['1','2','3'])+f"|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['positive_complete_30d_folds_1x']}|"+'/'.join(str(c['recent40_positive_5d_folds_by_cost'][k]) for k in ['1','2','3'])+'|'+c['status']+'|')
lines += ['',f"6个新父候选：{len(r['summary']['passed'])}历史通过、{len(r['summary']['candidate_rejected'])}淘汰。全部新配置失败原因：{ {c['name']:c['failed_criteria'] for c in r['configs'].values()} }。不根据新结果放宽门槛或加测格点。",'',
'11个CSV保留全部成本场景、逐折/近期折、每日NAV、原生和父完整九格敏感性、72相邻边、匹配持有和现金比较、旧来源路径与固定资金分配。完整NAV哈希、必要逐笔/资金费/状态段/父来源哈希支持独立重建。两张多指标曲面及描述性相邻2std悬崖检查不等于统计显著性；最大值在边界时如实指出，不自动追加试验。','',
'冻结账户分别延续原现金/q/desired/risk与完整NAV前缀：原SMA65和singleS28计划续14:30至16:30，需实际处理singleS28的16资金费；独立未过滤L4/H2续16:10至18:10，仅18:11参考闭合后采集，carry已计16funding并核验正时长风险段。此次确认/缓冲/过滤参数不注入任何原账户。部分观察rejected不取消长期计划，延迟shadow不充当十策略真实报价成交。','',
'源码合成检查采用TDD：旧代码在单日极值K2测试预期失败，新规则加入后确认/等号/退出/保留/翻向/未来扰动通过。此为预登记前合成工程证据，没有真实回测或账户重跑。','',
'一手数据接口说明已于2026-11-01访问：[Binance官方市场数据文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)，字段与路由记录见primary_sources.json；实际数据与哈希独立核验，文档样例不作行情证据。','',
'所有研究/登记/快照/提交在main排他锁内；快照只读取既有账户与报告，不产生成交或改冻结规则/本金/持仓，不部署网页或增加定时任务，不下真实订单。']
(R/'result.md').write_text('\n'.join(lines)+'\n');print(json.dumps(s),flush=True)
