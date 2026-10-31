"""Export completed funded-NAV allocation results; no new signals or financial paths."""
import collections,csv,json,math,statistics
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import *
from run import recent_ok
report=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text());configs=report['configs'];full={**report['read_only_grid'],**{c['fingerprint']:c for c in configs.values()}};axis=[.5,1,1.5]
def write(name,columns,rows):
 with (R/name).open('w',newline='') as f:
  w=csv.writer(f,lineterminator='\n');w.writerow(columns);w.writerows(rows)
cost=[];fold=[];recent=[];daily=[];gridrows=[];comparisons=[];edges=[];edgeflags={}
for c in configs.values():
 wb,we=c['raw_BTC_weight'],c['raw_ETH_weight']
 for k,z in c['scenes'].items():
  cost.append([c['name'],c['role'],wb,we,c['capital_usdt'],k,z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar'],z['cost_usdt'],z['cost_pct_initial'],z['funding_usdt'],z['gross_reference_PnL_to_execution_cost'],z['executions'],z['round_trips'],z['parent_executions'],z['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in z['recent40']['folds']),c['status']])
  fold.extend([c['name'],c['role'],k,f['fold'],f['start_utc'],f['end_exclusive_utc'],f['duration_days'],f['net_return_pct'],f['max_drawdown_pct'],f['sharpe_365'],f['calmar']] for f in z['folds'])
  recent.extend([c['name'],c['role'],k,f['fold'],f['start_utc'],f['end_exclusive_utc'],f['net_return_pct'],f['max_drawdown_pct'],f['sharpe_365'],f['calmar']] for f in z['recent40']['folds'])
  daily.extend([c['name'],c['role'],k,i,v] for i,v in enumerate(z['daily_equity_usdt']))
  if c['role']=='candidate':
   g=next(g for g in plan['grid'] if g['role']=='benchmark' and g['wB']==wb and g['wE']==we);ref=full[g['fingerprint']];s=ref['scenes'][k];comparisons.append([c['name'],wb,we,k,c['capital_usdt'],1000*wb+3000*we,ref['fingerprint'],g['readonly'],z['net_return_pct'],s['net_return_pct'],z['net_return_pct']-s['net_return_pct'],z['max_drawdown_pct'],s['max_drawdown_pct'],z['max_drawdown_pct']-s['max_drawdown_pct'],'same raw NAV interests/capital/source-unit entry budgets; signals, held notionals, timing and risk differ; no native order scaling/capacity proof'])
for g in plan['grid']:
 c=full[g['fingerprint']];gridrows.append([g['role'],g['wB'],g['wE'],10000*(g['wB']+g['wE']),g['fingerprint'],g['readonly'],c['status'],c['scenes']['3']['net_return_pct'],c['scenes']['3']['max_drawdown_pct'],c['scenes']['3']['sharpe_365'],c['scenes']['3']['calmar'],*[sum(f['net_return_pct']>0 for f in c['scenes'][k]['recent40']['folds']) for k in ['1','2','3']],recent_ok(c)])
for role in ['candidate','benchmark']:
 cells={(g['wB'],g['wE']):full[g['fingerprint']] for g in plan['grid'] if g['role']==role}
 for k in ['1','2','3']:
  deltas=[]
  for wb in axis:
   for we in axis:
    for nextpair in [(axis[axis.index(wb)+1],we)] if axis.index(wb)<2 else []:
     a,b=cells[wb,we]['scenes'][k],cells[nextpair]['scenes'][k];delta=abs(a['sharpe_365']-b['sharpe_365']);deltas.append(delta);edges.append([role,k,'BTC',wb,we,*nextpair,delta,abs(a['net_return_pct']-b['net_return_pct']),abs(a['max_drawdown_pct']-b['max_drawdown_pct'])])
    for nextpair in [(wb,axis[axis.index(we)+1])] if axis.index(we)<2 else []:
     a,b=cells[wb,we]['scenes'][k],cells[nextpair]['scenes'][k];delta=abs(a['sharpe_365']-b['sharpe_365']);deltas.append(delta);edges.append([role,k,'ETH',wb,we,*nextpair,delta,abs(a['net_return_pct']-b['net_return_pct']),abs(a['max_drawdown_pct']-b['max_drawdown_pct'])])
  assert len(deltas)==12;threshold=2*statistics.stdev(deltas);edgeflags[role+'_'+k]={'adjacent_edges':12,'max_absolute_Sharpe_change':max(deltas),'two_std_absolute_change_threshold':threshold,'heuristic_flag':max(deltas)>threshold,'scope':'Descriptive weight-surface heuristic; shared source paths/ratios, not independent significance, not corrected alpha or proof of overfit.'}
write('cost_scenes.csv',['configuration','role','raw_BTC_interest','raw_ETH_interest','funded_initial_capital_usdt','cost_multiplier','net_return_pct','whole_OOS_drawdown_pct','sharpe365','calmar','funded_execution_cost_usdt','cost_pct_initial','funded_funding_usdt','gross_plus_funding_to_cost','actual_underlying_executions','underlying_closes','new_parent_executions','recent40_return_pct','recent_positive5d_folds','status'],cost)
write('walk_forward_folds.csv',['configuration','role','cost_multiplier','fold','start_utc','end_exclusive_utc','days','net_return_pct','whole_fold_DD_pct','sharpe365','calmar'],fold)
write('recent40_folds.csv',['configuration','role','cost_multiplier','fold','start_utc','end_exclusive_utc','net_return_pct','whole_fold_DD_pct','sharpe365','calmar'],recent)
write('daily_NAV.csv',['configuration','role','cost_multiplier','boundary_index','funded_NAV_usdt'],daily)
write('sensitivity_grid.csv',['role','raw_BTC_interest','raw_ETH_interest','capital_usdt','fingerprint','old_result_readonly','canonical_status','net3_pct','DD3_pct','Sharpe3','Calmar3','recent_positive5d_1','recent_positive5d_2','recent_positive5d_3','strict_recent_gate_diagnostic'],gridrows)
write('reference_comparisons.csv',['candidate','raw_BTC_interest','raw_ETH_interest','cost_multiplier','same_funded_initial_capital_usdt','same_funded_source_entry_budget_usdt','hold_control_fingerprint','hold_control_readonly','candidate_return_pct','hold_return_pct','return_difference_pp','candidate_DD_pct','hold_DD_pct','DD_difference_pp','comparability_scope'],comparisons)
write('adjacent_edges.csv',['role','cost_multiplier','varied_axis','from_B','from_E','to_B','to_E','absolute_Sharpe_change','absolute_return_change_pp','absolute_DD_change_pp'],edges)
put(R/'edge_flags.json',edgeflags)
fig,axs=plt.subplots(2,4,figsize=(17,8),layout='constrained')
for row,role in enumerate(['candidate','benchmark']):
 for col,(title,fn) in enumerate([('3x full370 return %',lambda c:c['scenes']['3']['net_return_pct']),('3x complete-curve DD %',lambda c:c['scenes']['3']['max_drawdown_pct']),('3x daily Sharpe365',lambda c:c['scenes']['3']['sharpe_365']),('Recent positive5d at3x /8',lambda c:sum(f['net_return_pct']>0 for f in c['scenes']['3']['recent40']['folds']))]):
  arr=np.empty((3,3))
  for g in plan['grid']:
   if g['role']==role:arr[axis.index(g['wB']),axis.index(g['wE'])]=fn(full[g['fingerprint']])
  ax=axs[row,col];opts={'vmin':0,'vmax':8} if col==3 else {};im=ax.imshow(arr,cmap='RdYlGn_r' if col==1 else 'RdYlGn',aspect='auto',**opts);ax.set_xticks(range(3),axis);ax.set_yticks(range(3),axis);ax.set_xlabel('Raw ETH NAV interest');ax.set_ylabel('Raw BTC NAV interest');ax.set_title(role+'\n'+title)
  for g in plan['grid']:
   if g['role']==role:
    i,j=axis.index(g['wB']),axis.index(g['wE']);ax.text(j,i,f'{arr[i,j]:.2f}'+(' O' if g['readonly'] else ' N'),ha='center',va='center',fontsize=9)
  fig.colorbar(im,ax=ax,shrink=.75)
fig.suptitle('Fixed funded source NAV interests | O=old actual, N=new actual | capital=10000*(wB+wE)\nRepeated development history; raw interests unnormalized; native execution scaling/capacity not validated',fontsize=12);fig.savefig(R/'sensitivity.png',dpi=140);plt.close(fig)
fail={role:dict(collections.Counter(k for c in configs.values() if c['role']==role for k in c['failed_criteria'])) for role in ['candidate','benchmark']};summary={'report_sha256':sha(R/'report.json'),'new_financial_configs':12,'new_candidates':8,'new_matched_hold_controls':4,'new_cost_scenes':36,'old_grid_cells':6,'old_native_components':4,'old_statuses_unchanged':True,'positive_by_role_and_cost':report['summary']['positive_configs_by_role_and_cost'],'failed_criteria_by_role':fail,'recent_strict_qualified_cells_by_role':{role:sum(recent_ok(full[g['fingerprint']]) for g in plan['grid'] if g['role']==role) for role in ['candidate','benchmark']},'positive_Sharpe_fraction_by_role_and_cost':{role:{k:sum(c['scenes'][k]['sharpe_365']>0 for c in configs.values() if c['role']==role)/sum(c['role']==role for c in configs.values()) for k in ['1','2','3']} for role in ['candidate','benchmark']},'homothetic_effective_unique_ratios_per_role':7,'edge_flags':edgeflags};put(R/'sensitivity_summary.json',summary)
rep=next(c for c in configs.values() if c['role']=='candidate' and c['raw_BTC_weight']==1.5 and c['raw_ETH_weight']==1);put(R/'representative.json',{'selection_policy':plan['representative_preset'],'configuration':rep})
lines=['# 固定 BTC/ETH 净值权益权重验证','',
'实际新增8个候选、4个匹配持有对照，共12个定义／36成本场景，全部rejected。候选1/2/3倍成本全年净正均8/8，对照均0/4；全部负收益、负折和失败保留。原始份额两轴各[0.5,1,1.5]，旧1/1候选及5个旧持有格点只读，没有重跑或重写资格。','',
'BTC组件固定原趋势L31/H4%/退出缓冲1%/原生入场1000；ETH固定原慢趋势S28/快反转L3/H2%/零线退出/原生入场3000。严格信号、持仓数量、费用、资金费、抵押和终止平仓均来自已实际执行的完整原生账本。父组合不重跑旧信号或下单，只恢复现金／数量／入场价段与真实价格并核验原始NAV SHA，再按共同(ns,eventcode)轴做固定权益相加。','',
'wB/wE是完整独立10000USDT净值单位的固定资金权益；总初始本金=10000×(wB+wE)，不自动归一化、不固定为20000、不借款或跨银行转账。0.5是净值权益记账，不是半个永续下单手数；源银行仍按原生LOT/tick与原数量承担成交成本。组合净值=wB×BTC源净值+wE×ETH源净值，无免费再平衡、NAV复利调整或父组合新成交。源执行次数／已平仓次数按真实底层两账本整数报告，经济金额按权益加权，另存加权单位统计，不伪造小数笔成交。','',
'成本边界：继承真实原生数量下5bp手续费、1bp半价差、2bp滑点和0.5×过去20完整日样本log波动×sqrt(原生订单参考名义/过去20日quoteADV)冲击，逆向tick、LOT/minnotional、参与率<=0.001、开仓后费用抵押1x上限；1/2/3倍执行及负资金费压力路径分别保留。实际settlement纳秒／mark／当时数量记资金费，正收入不放大，未来资金费不进信号。线性永续无现货借币假设。权益申赎／管理额外费用假设为0；本轮未证明这些假设权益可实际交易，也未证明扩大或合并永续订单后的LOT、非线性冲击、容量或L2/TCA。若按放大合约数量落地，必须另行预登记原生执行核验，不能从本表直接外推。','',
'三项验证：370日连续历史2025-10-19 UTC00:01至2026-10-24 UTC00:01、12完整30日折＋10日尾折；不重置账本，近期40日从day330真实源权益继承，8个连续5日折。无新监督标签或权重拟合，purge horizon0；源信号前一完整收盘可得，00:01才成交。全部12次reserve成功后才做新组合收益计算，两个权重轴索引半径1含中心、角色分开；至少60%局部3倍净正且至少60%局部满足每档近期6/8正五日折，其他9/12月折、DD3<=25%、成本余量>=2.5和原生风险门槛冻结。重复开发历史不是未触碰最终测试集。','',
'[0.5,0.5]、[1,1]、[1.5,1.5]具有不同原始资金／金额净值，但归一化回报相同，不能算三份独立市场证据。每角色9格仅7种权重比例；全部格点共用两条底层策略路径。Sharpe/Calmar与整体回撤从完整联合曲线重算，不平均单币指标。邻接cliff仅描述性启发式，不是统计显著性、DSR/PBO或选择偏差校正。','',
'|配置|角色|本金|1x净%|2x净%|3x净%|3x完整DD%|正月折1x/12|正五日折1/2/3x|状态|','|---|---|---:|---:|---:|---:|---:|---:|---|---|']
for c in configs.values():lines.append('|'+c['name']+'|'+c['role']+f"|{c['capital_usdt']:.0f}|"+'|'.join(f"{c['scenes'][k]['net_return_pct']:.6f}" for k in ['1','2','3'])+f"|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['positive_complete_30d_folds_1x']}|"+'/'.join(str(c['recent40_positive_5d_folds_by_cost'][k]) for k in ['1','2','3'])+'|rejected|')
lines+=['',f"候选失败计数{json.dumps(fail['candidate'],ensure_ascii=False)}。0.5/1和0.5/1.5两个新候选在本点达到全年三档净正、近期每档6/8及其余点上门槛，但邻域严格近期合格比例只有1/3、1/2，均低于预注册60%，因此仍rejected。没有降低邻域门槛或把原始旧1/1的历史passed按当前严格规则重评为新资格。",'',
f"预设代表1.5/1（本金25000）三档收益{rep['scenes']['1']['net_return_pct']:.6f}%／{rep['scenes']['2']['net_return_pct']:.6f}%／{rep['scenes']['3']['net_return_pct']:.6f}%，3倍完整DD{rep['scenes']['3']['max_drawdown_pct']:.6f}%，近期正五日折5/5/5，局部严格近期合格为0。该代表在看OOS前固定，不以最高年收益格点替换。",'',
'逐权重／逐成本与同原始权益、本金、源单位入场预算的持有对照比较见reference_comparisons.csv；所有8个候选×3成本差值保留。对照的实际方向／持仓名义／时点／换手和风险不同，不声称等风险比较。解析现金参考为0%、不另行假造回测。旧对照复用真实报告而非同名重算，新4个持有负收益结果独立reserve/finish。','',
'独立审计从原生账本逐笔Decimal重建资金费、成交、成本、现金和小时维护代理，再恢复原始完整NAV SHA；逐项检查新组合原始资本、加权金额、共同时间轴、全部逐折／近期指标、同比分母与旧资格不变。不调用原生simulate/target/trade。细节在verification.json；图已区分旧O／新N和两角色，raw权重与不同本金明确。','',
'研究背景：[AQR交易成本研究](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)、[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)为传统股票／期货背景，不验证本轮加密权益组合，也不证明容量。','','原SMA65及单S28冻结账户另行按最新保存状态续接，paper10只读；新权重不替换冻结本金、持仓或规则。复现命令／全部结果／失败／输入哈希／必要代码与账本保留，发布SHA及真实push证明见.git/automation_proofs/20261031T074311Z.json。历史正收益不能称稳定实盘盈利。']
(R/'result.md').write_text('\n'.join(lines)+'\n');print(json.dumps(summary),flush=True)
