"""Export every saved scene and fixed bank/H grid; no strategy calculation."""
import collections,csv,json,statistics
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import *
rep=json.loads((R/'report.json').read_text());p=json.loads((R/'plan.json').read_text());full=rep['all_current_grid'];rows={}
def write(n,cols,items):
 with (R/n).open('w',newline='') as f:w=csv.writer(f,lineterminator='\n');w.writerow(cols);w.writerows(items)
 rows[n]=len(items)
cost=[];wf=[];recent=[];daily=[];grid=[];readonly=[];edges=[];alloc=[];sources=[]
for c in rep['configs'].values():
 for k,s in c['scenes'].items():
  cost.append([c['name'],c['fingerprint'],c['BTC_capital_usdt'],c['H'],c['capital_usdt'],c['BTC_capital_usdt']/c['capital_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['cost_usdt'],s['cost_pct_initial'],s['funding_usdt'],s['gross_reference_PnL_to_execution_cost'],s['executions'],s['round_trips'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),c['status']])
  wf.extend([c['name'],c['BTC_capital_usdt'],c['H'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['duration_days'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['folds'])
  recent.extend([c['name'],c['BTC_capital_usdt'],c['H'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['recent40']['folds'])
  daily.extend([c['name'],k,i,v] for i,v in enumerate(s['daily_equity_usdt']))
for g in p['grid']:
 c=full[g['fingerprint']];C=g['BTC_capital_usdt'];alloc.append([g['fingerprint'],'candidate',C,15000,C+15000,C/10,4500,1,1,C/(C+15000),15000/(C+15000),g['H'],g['readonly']])
 for k,s in c['scenes'].items():
  d=c['current_grid_diagnostic_sensitivity'];z=[C,g['H'],g['fingerprint'],g['readonly'],c['status'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),d['local_positive3_fraction'],d['local_strict_recent_fraction']];grid.append(z)
  if g['readonly']:readonly.append(z)
for g in p['benchmarks']:
 C=g['BTC_capital_usdt'];alloc.append([g['fingerprint'],'matched_budget_hold',C,15000,C+15000,C/10,4500,1,1,C/(C+15000),15000/(C+15000),None,g['readonly']])
for k in ['1','2','3']:
 for g in p['grid']:
  i,j=p['BTC_capitals'].index(g['BTC_capital_usdt']),p['fast_hurdles'].index(g['H']);ng=[h for h in p['grid'] if i<2 and h['BTC_capital_usdt']==p['BTC_capitals'][i+1] and h['H']==g['H'] or j<2 and h['H']==p['fast_hurdles'][j+1] and h['BTC_capital_usdt']==g['BTC_capital_usdt']]
  for h in ng:
   a,b=full[g['fingerprint']]['scenes'][k],full[h['fingerprint']]['scenes'][k];edges.append([k,g['BTC_capital_usdt'],g['H'],h['BTC_capital_usdt'],h['H'],g['fingerprint'],h['fingerprint'],abs(a['sharpe_365']-b['sharpe_365']),abs(a['net_return_pct']-b['net_return_pct']),abs(a['max_drawdown_pct']-b['max_drawdown_pct'])])
for fp,x in p['read_only_references'].items():
 if x['scope']!='native':continue
 sp=json.loads((ROOT/x['spec']).read_text());old=next(c for c in json.loads((ROOT/x['report']).read_text())['configs'].values() if c['fingerprint']==fp)
 for k,s in old['scenes'].items():sources.append([fp,x['asset'],x['capital_usdt'],sp['parameters']['fixed_entry_notional_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['cost_usdt'],s['funding_usdt'],s['executions'],s['NAV_sha256_f64le'],x['report'],x['report_sha256']])
write('cost_scenes.csv',['configuration','fingerprint','BTC_bank','signal_H','total_capital','BTC_capital_share','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','cost_usdt','cost_pct_initial','funding_usdt','gross_plus_funding_to_cost','underlying_executions','underlying_closes','recent40_return_pct','positive5d_folds','status'],cost)
write('walk_forward_folds.csv',['configuration','BTC_bank','ETH_H','cost_multiplier','fold','start_utc','end_exclusive_utc','days','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],wf)
write('recent40_folds.csv',['configuration','BTC_bank','ETH_H','cost_multiplier','fold','start_utc','end_exclusive_utc','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],recent)
write('daily_NAV.csv',['configuration','cost_multiplier','boundary','NAV_usdt'],daily)
cols=['BTC_bank','ETH_H','fingerprint','readonly_old','unchanged_canonical_status','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','recent40_return_pct','positive5d_folds','local_positive3_fraction','local_recent_fraction']
write('sensitivity_grid.csv',cols,grid);write('readonly_reused_scenes.csv',cols,readonly)
write('adjacent_edges.csv',['cost_multiplier','from_BTC_bank','from_H','to_BTC_bank','to_H','from_fp','to_fp','absolute_Sharpe_change','absolute_return_change_pp','absolute_DD_change_pp'],edges)
cs=rep['matched_hold_comparisons'];write('matched_hold_comparisons.csv',list(cs[0]),[list(x.values()) for x in cs])
write('source_curves.csv',['fingerprint','asset','actual_bank_capital','actual_initial_entry_N','cost_multiplier','return_pct','wholeDD_pct','cost_usdt','funding_usdt','executions','NAV_sha256','readonly_report','readonly_report_sha256'],sources)
write('bank_allocations.csv',['fingerprint','role','BTC_bank','ETH_bank','total_initial_capital','BTC_N','ETH_N','raw_BTC_component_weight','raw_ETH_component_weight','explicit_BTC_capital_share','explicit_ETH_capital_share','ETH_H','readonly'],alloc)
flags={}
for k in ['1','2','3']:
 vals=[x[7] for x in edges if x[0]==k];threshold=2*statistics.stdev(vals);flags[k]={'edge_count':len(vals),'max_Sharpe_change':max(vals),'two_std_change_threshold':threshold,'descriptive_cliff_flag':max(vals)>threshold,'scope':'Descriptive dependent-edge heuristic, not DSR/PBO or statistical significance.'}
put(R/'edge_flags.json',flags)
fig,axs=plt.subplots(1,4,figsize=(16,5.2),layout='constrained')
for j,(label,fn) in enumerate([('3x continuous370 return %',lambda c:c['scenes']['3']['net_return_pct']),('3x wholecurve DD %',lambda c:c['scenes']['3']['max_drawdown_pct']),('3x daily Sharpe365',lambda c:c['scenes']['3']['sharpe_365']),('3x recent positive5d /8',lambda c:sum(z['net_return_pct']>0 for z in c['scenes']['3']['recent40']['folds']))]):
 arr=np.empty((3,3))
 for g in p['grid']:arr[p['BTC_capitals'].index(g['BTC_capital_usdt']),p['fast_hurdles'].index(g['H'])]=fn(full[g['fingerprint']])
 ax=axs[j];im=ax.imshow(arr,cmap='RdYlGn_r' if j==1 else 'RdYlGn',**({'vmin':0,'vmax':8} if j==3 else {}));ax.set_xticks(range(3),['2%','2.5%','3%']);ax.set_yticks(range(3),[f'{C} / {100*C/(C+15000):.2f}%' for C in p['BTC_capitals']]);ax.set_xlabel('ETH fast entry hurdle H');ax.set_ylabel('BTC actual bank / share of total');ax.set_title(label)
 for g in p['grid']:
  i,k=p['BTC_capitals'].index(g['BTC_capital_usdt']),p['fast_hurdles'].index(g['H']);ax.text(k,i,f'{arr[i,k]:.3f}'+(' O' if g['readonly'] else ' N'),ha='center',va='center',fontsize=9)
 fig.colorbar(im,ax=ax,shrink=.7)
fig.suptitle('Actual BTC bank2500/3750/5000 at native N250/375/500 | fixed ETH15000/N4500\nETH L4/S28, E0.25%, V10/cap4.5% | raw child multipliers [1,1], no NAV scaling | O=readonly, N=new | reused development history')
fig.savefig(R/'sensitivity.png',dpi=140);plt.close(fig)
summary={'report_sha256':sha(R/'report.json'),**p['expected_counts'],'passed':len(rep['summary']['passed']),'rejected':len(rep['summary']['candidate_rejected']),'failed_criteria':dict(collections.Counter(x for c in rep['configs'].values() for x in c['failed_criteria'])),'CSV_rows':rows,'edge_flags':flags};put(R/'sensitivity_summary.json',summary)
ctx=json.loads((R/'context.json').read_text());cand=[c for c in rep['configs'].values() if c['role']=='candidate'];comp=[c for c in rep['configs'].values() if c['role']=='component'];controls=[c for c in rep['configs'].values() if c['role'].startswith('benchmark')]
lines=['# BTC较小原生资金边界与ETH入场门槛联合验证','',f"本轮6个新金融定义：2个BTC原生2500银行/N250路径（动量组件及常多持有控制），3个BTC2500×ETH H2%/2.5%/3%新组合候选，1个BTC2500+ETH15000常多组合参考；18个1/2/3倍成本场景全部先reserve后实际计算并逐项finish。既有3750/5000银行的6个组合候选、2个匹配持有父及8个原生来源只读复用，共16个不同旧定义。完整读{ctx['registry_events']}事件、{ctx['registry_ids']}ID、{len(ctx['prior_conclusions_read'])}份结论；初始16项已有真实原始证据，不重复回测。",'',
'假设预先固定：上轮最佳Sharpe仍在BTC3750/H2.5%较小银行边界；本轮只延伸到2500，并以3750/5000旧结果组成3×3邻域。原生N始终为BTC银行初始资金10%，属于绑定资金/预算的可行性变化，不能称两个独立参数。新2500路径从真实行情重新计算LOT、tick、规模冲击、现金与资金费，不能线性缩放旧5000净值。','',
'组合权重原值[1,1]表示各一份完整BTC银行和ETH15000银行。总初始资金17500/18750/20000，BTC资金占比14.285714%/20%/25%；BTC入场N250/375/500、ETH N4500，总初始N/C0为27.142857%/26%/25%。净值直接相加美元账户，不重复乘资本份额，不平均Sharpe；无资金转账、父订单、NAVresize、再平衡或跨账户保证金抵消。资金比例不同不能解释为同风险比较。常多控制匹配原生银行与初始入场预算，非满仓买持或同风险基准；现金0%另列。','',
'BTC原ROC31/H4%/E1%；ETH固定L4/S28、退出缓冲绝对ROC0.0025、V10样本logvol上限0.045，仅新入场/翻向过滤。ETH priorfastROC>H空、<−H多；带内实际多仅r<E、空仅r>−E保留，等号退出，slow方向始终门控。q=floor(N/prior完整日close/LOT)×LOT，下一UTC00:01原生OPEN不利tick，反向先平后开，保留同向真实q，终止计费平仓。','',
'真实历史边界2025-10-19 UTC00:01至2026-10-24 UTC00:01，连续370天，12个完整30天折及10天尾折；跨折无状态/成本/资金费重置。近期40天继承day330状态，8个5天折。固定规则无训练/标签，purge0、预热30天/间隔3天，信号仅prior完整close；成本仅past20完整日quoteADV和logvol。历史已多次研究，属于开发验证，不称未触碰最终留出或独立未来验证。','',
'1/2/3倍成本包括每边5bp费、1bp半价差、2bp滑点及0.5×past20logvol×sqrt(actualq×OPEN/past20quoteADV)。真实结算纳秒/mark/rate/当时q记资金费，支出倍增、正收入不放大。真实LOT/tick/minnotional、参与率<=0.001、费用后1倍入场抵押，各原生银行1%闭合小时不利mark维护代理；线性永续无现货借币，不虚构借币费。没有盘口/TCA、完整历史阶梯或逐tick清算/容量证明。','',
'见结果前冻结门槛：每档全年净正，1倍>=9/12正完整月折；每档近期40天净正且>=6/8正5天折；3倍完整净值DD<=25%；银行/H索引半径1含中心的局部3倍正收益比例、严格近期达标比例均>=60%；至少4次平仓、毛价差PnL+fund/执行成本>=2.5，零拒单/负抵押/维护代理违规、终止flat、至少180天。原生动量组件用资金轴一维邻域执行同一财务门槛，单列component资格，不算组合候选。两个常多控制按预定非候选criterion=false留真实结果；不把控制角色失败解释成未计算。','',
'|新配置|角色|BTC银行/总C0|H%|1倍净%|2倍净%|3倍净%|3倍整体DD%|正月/12|近期正折1/2/3倍|状态|','|---|---|---|---:|---:|---:|---:|---:|---:|---|---|']
for c in rep['configs'].values():
 h='—' if c['H'] is None else f"{c['H']*100:g}"
 lines.append('|'+c['name']+'|'+c['role']+f"|{c['BTC_capital_usdt']}/{c['capital_usdt']}|{h}|"+'|'.join(f"{c['scenes'][k]['net_return_pct']:.6f}" for k in ['1','2','3'])+f"|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['positive_complete_30d_folds_1x']}|"+'/'.join(str(c['recent40_positive_5d_folds_by_cost'][k]) for k in ['1','2','3'])+'|'+c['status']+'|')
lines+=['',f"新组合候选{len(rep['summary']['passed'])}通过、{len(rep['summary']['candidate_rejected'])}淘汰；原生动量组件状态{[(c['status'],c['failed_criteria']) for c in comp]}；两个控制单独留档。各定义失败判据：{ {c['name']:c['failed_criteria'] for c in rep['configs'].values()} }。全部负收益及逐折结果保留。",'',
'10份CSV含18新成本场景、逐月/近期折和每日NAV、9格点、18只读旧组合场景、36相邻边、27同资金hold/cash比较、24旧原生成本来源场景及12资本分配。完整每场景545013点SHA、状态段和必要成交/资金费证据保留。独立审计使用Fraction信号和Decimal账务，核算实际q/LOT、费用/价差/滑点/冲击、资金费、抵押、小时风险和连续净值/逐折DD；审计不调用simulate/decide/trade进行金融重跑。','',
'局部支持、边界和描述性相邻悬崖均披露，旧配置仅新增当前邻域诊断，原status/criteria/sensitivity不重写。有限网格、重复开发历史和正收益不能称全域最优或稳定实盘盈利。','',
'三份冻结延迟观察各自延续：原SMA65及原singleS28从Nov1 UTC06:30至08:30，原S28必须按真实08资金费结算；独立未过滤L4/H2从08:10至10:10，仅10:11参考闭合后采集，08资金费已在上轮入账，必须保留前后风险状态且不得重复记账。旧规则/本金/持仓/成本/全NAV前缀保持，不用当前较小银行研究替换冻结账户。部分rejected只表示180天门槛未成熟，继续原计划。观察不充当十策略实时公开报价成交。','',
'公开只读快照在同main排他锁内生成，registry及monitor门禁实际执行；失败保留上次有效快照并留档。只汇总已有账户/报告，不新建纸面成交，不改规则/资金/监控预算，不部署网页、不创建定时器、不下真实订单。']
(R/'result.md').write_text('\n'.join(lines)+'\n');print(json.dumps(summary),flush=True)
