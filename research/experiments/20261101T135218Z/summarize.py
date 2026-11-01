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
  cost.append([c['name'],c['fingerprint'],c['scope'],c['role'],c['asset'],c['L'],c['H'],c['capital_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['cost_usdt'],s['cost_pct_initial'],s['funding_usdt'],s['gross_reference_PnL_to_execution_cost'],s['executions'],s['round_trips'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),c['status']])
  wf.extend([c['name'],c['scope'],c['L'],c['H'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['duration_days'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['folds'])
  recent.extend([c['name'],c['scope'],c['L'],c['H'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['recent40']['folds'])
  daily.extend([c['name'],c['scope'],k,i,v] for i,v in enumerate(s['daily_equity_usdt']))
write('cost_scenes.csv',['configuration','fingerprint','scope','role','asset','ETH_fast_L','ETH_H','initial_capital','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','cost_usdt','cost_pct_initial','funding_usdt','gross_plus_funding_to_cost','executions','closes','recent40_return_pct','positive5d_folds','status'],cost)
write('walk_forward_folds.csv',['configuration','scope','ETH_fast_L','ETH_H','cost_multiplier','fold','start_utc','end_exclusive_utc','days','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],wf)
write('recent40_folds.csv',['configuration','scope','ETH_fast_L','ETH_H','cost_multiplier','fold','start_utc','end_exclusive_utc','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],recent)
write('daily_NAV.csv',['configuration','scope','cost_multiplier','boundary','NAV_usdt'],daily)
cols=['ETH_fast_L','ETH_H','fingerprint','readonly_old','unchanged_canonical_status','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','recent40_return_pct','positive5d_folds','local_positive3_fraction','local_recent_fraction'];flags={};readonly=[]
for scope,grid,key in [('parent',p['grid'],'all_current_grid'),('native',p['native_grid'],'all_current_native_grid')]:
 full=r[key];items=[]
 for g in grid:
  c=full[g['fingerprint']]
  for k,s in c['scenes'].items():
   d=c['current_grid_diagnostic_sensitivity'];z=[g['L'],g['H'],g['fingerprint'],g['readonly'],c['status'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),d['local_positive3_fraction'],d['local_strict_recent_fraction']];items.append(z)
   if scope=='parent' and g['readonly']:readonly.append(z)
 for k in ['1','2','3']:
  for g in grid:
   i,j=p['lookbacks'].index(g['L']),p['fast_hurdles'].index(g['H']);ng=[h for h in grid if i<2 and h['L']==p['lookbacks'][i+1] and h['H']==g['H'] or j<2 and h['H']==p['fast_hurdles'][j+1] and h['L']==g['L']]
   for h in ng:
    a,b=full[g['fingerprint']]['scenes'][k],full[h['fingerprint']]['scenes'][k];edges.append([scope,k,g['L'],g['H'],h['L'],h['H'],g['fingerprint'],h['fingerprint'],abs(a['sharpe_365']-b['sharpe_365']),abs(a['net_return_pct']-b['net_return_pct']),abs(a['max_drawdown_pct']-b['max_drawdown_pct'])])
 flags[scope]={}
 for k in ['1','2','3']:
  v=[x[8] for x in edges if x[0]==scope and x[1]==k];t=2*statistics.stdev(v);flags[scope][k]={'edge_count':len(v),'max_Sharpe_change':max(v),'two_std_change_threshold':t,'descriptive_cliff_flag':max(v)>t,'scope':'Dependentedgeheuristiconly,notstatisticalsignificance,DSRorPBO.'}
 write('sensitivity_grid.csv' if scope=='parent' else 'native_sensitivity_grid.csv',cols,items)
write('readonly_reused_scenes.csv',cols,readonly)
write('adjacent_edges.csv',['scope','cost_multiplier','from_L','from_H','to_L','to_H','from_fp','to_fp','absolute_Sharpe_change','absolute_return_change_pp','absolute_DD_change_pp'],edges)
cs=r['matched_hold_comparisons'];write('matched_hold_comparisons.csv',list(cs[0]),[list(x.values()) for x in cs])
for fp,x in p['read_only_references'].items():
 if x['scope']!='native':continue
 sp=json.loads((ROOT/x['spec']).read_text());old=next(c for c in json.loads((ROOT/x['report']).read_text())['configs'].values() if c['fingerprint']==fp)
 for k,s in old['scenes'].items():sources.append([fp,x['asset'],x['capital_usdt'],sp['parameters']['fixed_entry_notional_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['cost_usdt'],s['funding_usdt'],s['executions'],s['NAV_sha256_f64le'],x['report'],x['report_sha256']])
write('source_curves.csv',['fingerprint','asset','actual_bank_capital','actual_entry_N','cost_multiplier','return_pct','whole_DD_pct','cost_usdt','funding_usdt','executions','NAV_sha256','readonly_report','readonly_report_sha256'],sources)
for g in p['grid']:alloc.append([g['fingerprint'],'candidate',g['L'],g['H'],3750,15000,18750,375,4500,1,1,.2,.8,g['readonly']])
alloc.append([p['benchmark_parent_fingerprint'],'matched_initial_budget_hold',None,None,3750,15000,18750,375,4500,1,1,.2,.8,True]);write('fixed_allocations.csv',['fingerprint','role','ETH_L','ETH_H','BTC_bank','ETH_bank','total_initial_capital','BTC_N','ETH_N','raw_BTC_weight','raw_ETH_weight','BTC_capital_share','ETH_capital_share','readonly'],alloc)
put(R/'edge_flags.json',flags)
fig,axs=plt.subplots(2,4,figsize=(16,9),layout='constrained')
for row,(scope,key) in enumerate([('ETH native15000/N4500','all_current_native_grid'),('BTC3750+ETH15000 parent','all_current_grid')]):
 full=r[key]
 for j,(label,fn) in enumerate([('3x continuous370 return %',lambda c:c['scenes']['3']['net_return_pct']),('3x wholecurve DD %',lambda c:c['scenes']['3']['max_drawdown_pct']),('3x daily Sharpe365',lambda c:c['scenes']['3']['sharpe_365']),('3x recent positive5d /8',lambda c:sum(f['net_return_pct']>0 for f in c['scenes']['3']['recent40']['folds']))]):
  arr=np.empty((3,3))
  for c in full.values():arr[p['lookbacks'].index(c['L']),p['fast_hurdles'].index(c['H'])]=fn(c)
  ax=axs[row,j];im=ax.imshow(arr,cmap='RdYlGn_r' if j==1 else 'RdYlGn',**({'vmin':0,'vmax':8} if j==3 else {}));ax.set_xticks(range(3),['2%','2.5%','3%']);ax.set_yticks(range(3),['L3','L4','L5']);ax.set_xlabel('ETH fast entry hurdle H');ax.set_ylabel('ETH fast lookback L');ax.set_title(scope+'\n'+label,fontsize=10)
  for c in full.values():i,k=p['lookbacks'].index(c['L']),p['fast_hurdles'].index(c['H']);ax.text(k,i,f'{arr[i,k]:.3f}'+(' O' if c['readonly'] else ' N'),ha='center',va='center',fontsize=9)
  fig.colorbar(im,ax=ax,shrink=.7)
fig.suptitle('ETH fast lookback3/4/5 x entryH2/2.5/3%, S28, E0.25%, V10/cap4.5%\nActualBTC3750/N375 andETH15000/N4500 | rawweights[1,1],shares20/80%,noNAVscaling | O=readonly,N=new | reuseddevelopmenthistory')
fig.savefig(R/'sensitivity.png',dpi=140);plt.close(fig)
s={'report_sha256':sha(R/'report.json'),**p['expected_counts'],'passed':len(r['summary']['passed']),'rejected':len(r['summary']['candidate_rejected']),'failed_criteria':dict(collections.Counter(f for c in r['configs'].values() for f in c['failed_criteria'])),'CSV_rows':rows,'edge_flags':flags};put(R/'sensitivity_summary.json',s)
ctx=json.loads((R/'context.json').read_text());lines=['# ETH快周期与入场门槛联合验证','',f"本轮12个新定义：ETH快周期L3/L5各交叉H2%/2.5%/3%，共6个实际原生配置和6个BTC/ETH父组合，36个1/2/3倍成本场景全部先reserve再实际计算。旧L4的3个原生和3个父格点、匹配持有父及其来源只读，共10个唯一旧定义；不因策略族相同排除新参数，也不重测已有结果。读取完整{ctx['registry_events']}事件/{ctx['registry_ids']}ID、{len(ctx['prior_conclusions_read'])}份结论，初始16项均有真实原始证据。",'',
'假设预先固定：已有L4/H2.5%和资金邻域支持仅属重复开发历史，本轮检验快周期改为相邻3或5天时能否保留支持，不进一步细化银行资本。固定BTC原ROC31/H4/E1、ETH S28、退出缓冲绝对ROC0.0025、V10样本logvol上限0.045。ETH priorfastROC>H空、<−H多，带内实际多仅r<E、空仅r>−E保留，等号退出；slow方向始终门控，波动率只过滤新入场/翻向。','',
'实际银行固定BTC3750/N375、ETH15000/N4500，总初始资本18750。原始权重[1,1]为两份完整银行，资金占比20%/80%，总初始入场预算4875/18750=26%；不自动归一化或重复乘份额，不线性缩放旧净值、复制同币银行、转移现金、父再平衡、NAVresize或跨抵押。原生q=floor(N/prior完整日close/LOT)×LOT，下一UTC00:01原生OPEN不利tick，翻向先平后开，同向保留q，终止计费平仓。','',
'真实2025-10-19 UTC00:01至2026-10-24 UTC00:01连续370日，12完整30日折+10日尾折，无跨折现金/持仓/成本/资金费重置；近期40日继承day330、8×5日折。固定规则无拟合/标签，purge0、预热30日/间隔3日，所有信号及past20完整日quoteADV/logvol仅用过去。参数选择已受既往研究影响，不能把这段历史称未触碰最终测试集或独立未来验证；未计算DSR/PBO显著性。','',
'成本1/2/3倍含每边5bp费用、1bp半价差、2bp滑点及0.5×past20logvol×sqrt(actualq×OPEN/past20quoteADV)。真实资金费settlement纳秒/mark/rate/当时q，支出倍增而正收入不放大；原生LOT/tick/minnotional、参与率<=.001、费用后1倍入场抵押，各银行独立1%闭合小时不利mark维护代理。线性永续无现货借币，不虚构借币费；无L2/TCA、完整历史清算档位/逐tick清算或真实容量证明。同期旧匹配持有为同银行与初始预算的常多参考，不是满仓买持或同风险基准，现金0%另列。','',
'预冻结门槛：每档全年净正、1倍>=9/12正完整月；每档近期净正且>=6/8正5日折；3倍完整DD<=25%；L/H索引半径1含中心的局部3倍正收益比例及严格近期比例各>=60%；至少4次平仓、毛价差PnL+fund/执行成本>=2.5，零拒单/负抵押/维护代理违规、终止flat、至少180日。原生ETH与父组合各自在自己的3×3面上独立判定；原生组件资格与父候选分开。旧canonical状态/判据/敏感性不重写，仅本轮诊断。','',
'|新配置|范围/角色|L|H%|1倍净%|2倍净%|3倍净%|3倍整体DD%|正月/12|近期正折1/2/3倍|状态|','|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|']
for c in r['configs'].values():lines.append('|'+c['name']+'|'+c['scope']+'/'+c['role']+f"|{c['L']}|{100*c['H']:g}|"+'|'.join(f"{c['scenes'][k]['net_return_pct']:.6f}" for k in ['1','2','3'])+f"|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['positive_complete_30d_folds_1x']}|"+'/'.join(str(c['recent40_positive_5d_folds_by_cost'][k]) for k in ['1','2','3'])+'|'+c['status']+'|')
lines+=['',f"6个新父候选{len(r['summary']['passed'])}通过/{len(r['summary']['candidate_rejected'])}淘汰。所有原生和父配置失败判据：{ {c['name']:c['failed_criteria'] for c in r['configs'].values()} }。所有正负收益、失败和每个变体保留并finish，不因全年正收益放宽近期/敏感性。",'',
'11份CSV保留36个新成本场景、逐月/近期折/每日NAV、原生与父两张完整9格点、9个旧父场景、72条相邻边、27次匹配hold/cash比较、18旧原生成本来源及10条固定分配说明。完整每场景NAV哈希、原生逐笔/资金费/状态段及父源哈希留存；独立Fraction信号/Decimal账务核验不调用策略simulate/decide/trade。全网格正Sharpe比例、多指标、边界和描述性相邻2std悬崖均披露；该启发式不是统计显著性，回测盈利不代表稳定实盘盈利。','',
'冻结观察分别续接：原SMA65与原singleS28从Nov1 UTC10:30至12:30；独立未过滤L4/H2从12:10至14:10，仅14:11参考分钟闭合后采集。保持原规则/本金/q/现金/desired/risk/费用/全部NAV前缀及终止计划，08资金费已记账不可重复；本轮历史L3/L5/缓冲/波动过滤不注入已有账户，部分rejected继续各自180日计划。延迟shadow不充当十策略真实报价成交。','',
'只读快照同main排他锁运行registry/snapshot/monitor门禁，只汇总已有证据，不产生新回测或成交、不改账户/规则/本金/持仓/预算、不部署网页/新建定时器/下真实订单。生成失败恢复上次有效快照并留具体失败。所有命令退出码、真实HTTP尝试和必要轻量证据留档。']
(R/'result.md').write_text('\n'.join(lines)+'\n');print(json.dumps(s),flush=True)
