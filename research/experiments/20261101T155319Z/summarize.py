"""Export saved real native/parent L/H results; no strategy calculation."""
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
  cost.append([c['name'],c['fingerprint'],c['scope'],c['role'],c['asset'],c['L'],c['S'],c['capital_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['cost_usdt'],s['cost_pct_initial'],s['funding_usdt'],s['gross_reference_PnL_to_execution_cost'],s['executions'],s['round_trips'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),c['status']])
  wf.extend([c['name'],c['scope'],c['L'],c['S'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['duration_days'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['folds'])
  recent.extend([c['name'],c['scope'],c['L'],c['S'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['recent40']['folds'])
  daily.extend([c['name'],c['scope'],k,i,v] for i,v in enumerate(s['daily_equity_usdt']))
write('cost_scenes.csv',['configuration','fingerprint','scope','role','asset','ETH_fast_L','ETH_slow_S','initial_capital','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','cost_usdt','cost_pct_initial','funding_usdt','gross_plus_funding_to_cost','executions','closes','recent40_return_pct','positive5d_folds','status'],cost)
write('walk_forward_folds.csv',['configuration','scope','ETH_fast_L','ETH_slow_S','cost_multiplier','fold','start_utc','end_exclusive_utc','days','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],wf)
write('recent40_folds.csv',['configuration','scope','ETH_fast_L','ETH_slow_S','cost_multiplier','fold','start_utc','end_exclusive_utc','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],recent)
write('daily_NAV.csv',['configuration','scope','cost_multiplier','boundary','NAV_usdt'],daily)
cols=['ETH_fast_L','ETH_slow_S','fingerprint','readonly_old','unchanged_canonical_status','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','recent40_return_pct','positive5d_folds','local_positive3_fraction','local_recent_fraction'];flags={};readonly=[]
for scope,grid,key in [('parent',p['grid'],'all_current_grid'),('native',p['native_grid'],'all_current_native_grid')]:
 full=r[key];items=[]
 for g in grid:
  c=full[g['fingerprint']]
  for k,s in c['scenes'].items():
   d=c['current_grid_diagnostic_sensitivity'];z=[g['L'],g['S'],g['fingerprint'],g['readonly'],c['status'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),d['local_positive3_fraction'],d['local_strict_recent_fraction']];items.append(z)
   if scope=='parent' and g['readonly']:readonly.append(z)
 for k in ['1','2','3']:
  for g in grid:
   i,j=p['lookbacks'].index(g['L']),p['slow_windows'].index(g['S']);ng=[h for h in grid if i<2 and h['L']==p['lookbacks'][i+1] and h['S']==g['S'] or j<2 and h['S']==p['slow_windows'][j+1] and h['L']==g['L']]
   for h in ng:
    a,b=full[g['fingerprint']]['scenes'][k],full[h['fingerprint']]['scenes'][k];edges.append([scope,k,g['L'],g['S'],h['L'],h['S'],g['fingerprint'],h['fingerprint'],abs(a['sharpe_365']-b['sharpe_365']),abs(a['net_return_pct']-b['net_return_pct']),abs(a['max_drawdown_pct']-b['max_drawdown_pct'])])
 flags[scope]={}
 for k in ['1','2','3']:
  v=[x[8] for x in edges if x[0]==scope and x[1]==k];t=2*statistics.stdev(v);flags[scope][k]={'edge_count':len(v),'max_Sharpe_change':max(v),'two_std_change_threshold':t,'descriptive_cliff_flag':max(v)>t,'scope':'Dependentedgeheuristiconly,notstatisticalsignificance,DSRorPBO.'}
 write('sensitivity_grid.csv' if scope=='parent' else 'native_sensitivity_grid.csv',cols,items)
write('readonly_reused_scenes.csv',cols,readonly)
write('adjacent_edges.csv',['scope','cost_multiplier','from_L','from_S','to_L','to_S','from_fp','to_fp','absolute_Sharpe_change','absolute_return_change_pp','absolute_DD_change_pp'],edges)
cs=r['matched_hold_comparisons'];write('matched_hold_comparisons.csv',list(cs[0]),[list(x.values()) for x in cs])
for fp,x in p['read_only_references'].items():
 if x['scope']!='native':continue
 sp=json.loads((ROOT/x['spec']).read_text());old=next(c for c in json.loads((ROOT/x['report']).read_text())['configs'].values() if c['fingerprint']==fp)
 for k,s in old['scenes'].items():sources.append([fp,x['asset'],x['capital_usdt'],sp['parameters']['fixed_entry_notional_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['cost_usdt'],s['funding_usdt'],s['executions'],s['NAV_sha256_f64le'],x['report'],x['report_sha256']])
write('source_curves.csv',['fingerprint','asset','actual_bank_capital','actual_entry_N','cost_multiplier','return_pct','whole_DD_pct','cost_usdt','funding_usdt','executions','NAV_sha256','readonly_report','readonly_report_sha256'],sources)
for g in p['grid']:alloc.append([g['fingerprint'],'candidate',g['L'],g['S'],3750,15000,18750,375,4500,1,1,.2,.8,g['readonly']])
alloc.append([p['benchmark_parent_fingerprint'],'matched_initial_budget_hold',None,None,3750,15000,18750,375,4500,1,1,.2,.8,True]);write('fixed_allocations.csv',['fingerprint','role','ETH_L','ETH_slow_S','BTC_bank','ETH_bank','total_initial_capital','BTC_N','ETH_N','raw_BTC_weight','raw_ETH_weight','BTC_capital_share','ETH_capital_share','readonly'],alloc)
put(R/'edge_flags.json',flags)
fig,axs=plt.subplots(2,4,figsize=(16,9),layout='constrained')
for row,(scope,key) in enumerate([('ETH native15000/N4500','all_current_native_grid'),('BTC3750+ETH15000 parent','all_current_grid')]):
 full=r[key]
 for j,(label,fn) in enumerate([('3x continuous370 return %',lambda c:c['scenes']['3']['net_return_pct']),('3x wholecurve DD %',lambda c:c['scenes']['3']['max_drawdown_pct']),('3x daily Sharpe365',lambda c:c['scenes']['3']['sharpe_365']),('3x recent positive5d /8',lambda c:sum(f['net_return_pct']>0 for f in c['scenes']['3']['recent40']['folds']))]):
  arr=np.empty((3,3))
  for c in full.values():arr[p['lookbacks'].index(c['L']),p['slow_windows'].index(c['S'])]=fn(c)
  ax=axs[row,j];im=ax.imshow(arr,cmap='RdYlGn_r' if j==1 else 'RdYlGn',**({'vmin':0,'vmax':8} if j==3 else {}));ax.set_xticks(range(3),['S24','S28','S32']);ax.set_yticks(range(3),['L3','L4','L5']);ax.set_xlabel('ETH slow trend lookback S');ax.set_ylabel('ETH fast lookback L');ax.set_title(scope+'\n'+label,fontsize=10)
  for c in full.values():i,k=p['lookbacks'].index(c['L']),p['slow_windows'].index(c['S']);ax.text(k,i,f'{arr[i,k]:.3f}'+(' O' if c['readonly'] else ' N'),ha='center',va='center',fontsize=9)
  fig.colorbar(im,ax=ax,shrink=.7)
fig.suptitle('ETH fastL3/4/5 x slowS24/28/32, fixedH2.5%, E0.25%, V10/cap4.5%\nActualBTC3750/N375 andETH15000/N4500 | rawweights[1,1],shares20/80%,noNAVscaling | O=readonly,N=new | reuseddevelopmenthistory')
fig.savefig(R/'sensitivity.png',dpi=140);plt.close(fig)
s={'report_sha256':sha(R/'report.json'),**p['expected_counts'],'passed':len(r['summary']['passed']),'rejected':len(r['summary']['candidate_rejected']),'failed_criteria':dict(collections.Counter(f for c in r['configs'].values() for f in c['failed_criteria'])),'CSV_rows':rows,'edge_flags':flags};put(R/'sensitivity_summary.json',s)
ctx=json.loads((R/'context.json').read_text());lines=['# ETH快慢周期门控联合验证','',f"本轮12个新定义：快周期L3/4/5交叉慢趋势S24/32，共6个原生ETH配置和6个BTC/ETH组合，36个1/2/3倍成本场景全部实际reserve后计算。S28的3个原生与3个父格点、旧匹配持有父及来源只读，共10唯一旧定义；不因family相同排除新参数，也不精确重复旧结果。完整读取{ctx['registry_events']}登记事件/{ctx['registry_ids']}ID、{len(ctx['prior_conclusions_read'])}份结论，初始16项实际证据齐全。",'',
'预冻结假设：既有L4/S28峰值与新L3局部支持仍受近期弱一致性影响。本轮将慢趋势门控从28日扰动为24/32日，交叉快周期3/4/5日，固定H=2.5%、退出缓冲绝对ROC0.0025、V10样本logvol cap0.045，检验门控时域能否改善平台，而不是继续细化资金或入场阈值。参数选择受既往研究影响，这仍是重复开发历史，不是未触碰最终测试。','',
'BTC原ROC31/H4%/E1%不变。ETH fastROC=C[i-1]/C[i-1-L]-1、slowROC=C[i-1]/C[i-1-S]-1；fast>0.025空、<−0.025多。带内实际多仅r<0.0025、实际空仅r>−0.0025保留，等号退出，slow方向始终门控；V10波动上限只过滤新入场/翻向，不阻止退出或同向保留。原生q=floor(N/prior完整close/LOT)×LOT，下一UTC00:01原生OPEN不利tick，反向先平后开，终止计成本平仓。','',
'固定实际银行BTC3750/N375、ETH15000/N4500，总初始资本18750；原权重[1,1]为两份完整银行，资金份额20%/80%，总初始入场预算4875/18750=26%。按真实银行美元净值相加，不归一化权重、不重复乘资金份额、不线性缩放旧净值、复制同币银行、转账、父调仓、NAVresize或跨账户抵押。旧常多参考匹配银行和初始N，不是满仓买持或同风险基准；现金0%另列。','',
'数据边界为真实2025-10-19 UTC00:01至2026-10-24 UTC00:01连续370天，12完整30天折+10天尾折，状态/现金/q/成本/资金费跨折不重置。近期40天继承day330、8×5天折。固定规则无训练/标签，purge0、预热30天/间隔3天；33个已完整预热日使S32首决策i=33可用close[0]，不负索引或未来填充。所有信号、past20完整日quoteADV/logvol只用当时过去数据。多重选择偏差没有被局部比例或简单正Sharpe消除，未计算DSR/PBO显著性。','',
'1/2/3倍成本包括每边5bp费用、1bp半价差、2bp滑点和0.5×past20logvol×sqrt(actualq×OPEN/past20quoteADV)。真实资金费结算纳秒/rate/mark/当时q，支出倍增、正收入不放大；原生LOT/tick/minnotional、参与率<=0.001、费用后1倍入场抵押、各银行独立1%闭合小时不利mark维护代理。线性永续无现货借币，不虚构借币费；没有L2/TCA、完整历史阶梯/逐tick清算或真实容量证明。','',
'原门槛不放宽：每档全年净正、1倍>=9/12正完整月；每档近期净正且>=6/8正5日折；3倍完整DD<=25%；快L/慢S索引半径1含中心的局部3倍净正和严格近期比例均>=60%；至少4平仓、毛价差PnL+fund/执行成本>=2.5，零拒单/负抵押/维护代理违规、终止flat、至少180天。原生与父各在自身3×3面判定，单币与组合资格分开。旧canonical状态/判据/敏感性不重写，只增加当前诊断。','',
'|新配置|范围/角色|L|S|1倍净%|2倍净%|3倍净%|3倍整体DD%|正月/12|近期正折1/2/3倍|状态|','|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|']
for c in r['configs'].values():lines.append('|'+c['name']+'|'+c['scope']+'/'+c['role']+f"|{c['L']}|{c['S']}|"+'|'.join(f"{c['scenes'][k]['net_return_pct']:.6f}" for k in ['1','2','3'])+f"|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['positive_complete_30d_folds_1x']}|"+'/'.join(str(c['recent40_positive_5d_folds_by_cost'][k]) for k in ['1','2','3'])+'|'+c['status']+'|')
lines+=['',f"6新父候选{len(r['summary']['passed'])}历史通过/{len(r['summary']['candidate_rejected'])}淘汰。全部原生与父失败判据{ {c['name']:c['failed_criteria'] for c in r['configs'].values()} }。所有负收益/负期段与失败保留并finish，不按全年正收益放宽近期或邻域要求。",'',
'11CSV保存36新场景、逐月/近期折/每日NAV、原生与父两张完整9格点、9旧父场景、72相邻边、27同资金hold/cash比较、18旧原生成本来源及10条固定分配说明。保留完整NAV SHA、原生必要逐笔/资金费/状态段及父源哈希；独立审计用Fraction信号和Decimal账务，不调用simulate/decide/trade进行金融重跑。全格点正Sharpe比例、多指标、边界和描述性2std悬崖均报告，描述性启发式不是统计显著性或稳定实盘盈利证明。','',
'原SMA65及原singleS28续Nov1 UTC12:30至14:30；独立未过滤L4/H2续14:10至16:10，仅16:11参考闭合后采集，必须真实核算16资金费纳秒/rate/mark/当时q并只记一次、保留前后正时长风险状态。三账户原规则/本金/q/现金/desired/risk/费用/完整NAV前缀及终止计划保持，本轮L/S/缓冲/波动参数不注入已有账户。部分rejected继续180天计划，延迟shadow不充当十策略真实报价成交。','',
'同main排他锁完成registry/snapshot/monitor门禁，快照只读已有证据，不新回测/产生成交、不改账户/规则/资金/持仓/预算、不部署网页/建定时器/下真实订单。失败保留上一有效快照与具体证据。初始合成夹具曾因S24读取另一历史段而失败，原脚本/日志/根因/修正回执保留；只调整合成历史段，策略/规格/判据不改，且在任何reserve或真实回测前恢复通过。']
(R/'result.md').write_text('\n'.join(lines)+'\n');print(json.dumps(s),flush=True)
