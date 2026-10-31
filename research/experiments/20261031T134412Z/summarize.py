"""Exports from actual saved reports only; no strategy/order calculation."""
import collections,csv,json,statistics
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import *
from run import recent_ok
rep=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text());cfgs=rep['configs'];full=rep['all_current_grid'];Ls=plan['lookbacks'];Hs=plan['hurdles'];rows={}
def write(name,cols,items):
 with (R/name).open('w',newline='') as f:w=csv.writer(f,lineterminator='\n');w.writerow(cols);w.writerows(items)
 rows[name]=len(items)
cost=[];wf=[];tail=[];daily=[];grid=[];edges=[];readonly=[]
for c in cfgs.values():
 for k,s in c['scenes'].items():
  cost.append([c['name'],c['fingerprint'],c['scope'],c['L'],c['H'],c['capital_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['cost_usdt'],s['cost_pct_initial'],s['funding_usdt'],s['gross_reference_PnL_to_execution_cost'],s['executions'],s['round_trips'],s['recent40']['net_return_pct'],sum(x['net_return_pct']>0 for x in s['recent40']['folds']),c['status']])
  wf.extend([c['name'],c['scope'],c['L'],c['H'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['duration_days'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['folds'])
  tail.extend([c['name'],c['scope'],c['L'],c['H'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['recent40']['folds'])
  daily.extend([c['name'],c['scope'],k,i,v] for i,v in enumerate(s['daily_equity_usdt']))
for scope,items in [('native',plan['native_grid']),('parent',plan['grid'])]:
 for g in items:
  c=full[g['fingerprint']]
  for k,s in c['scenes'].items():
   grid.append([scope,g['L'],g['H'],g['fingerprint'],g['readonly'],c['status'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['recent40']['net_return_pct'],sum(z['net_return_pct']>0 for z in s['recent40']['folds']),recent_ok(c),c['current_grid_diagnostic_sensitivity']['local_positive3_fraction'],c['current_grid_diagnostic_sensitivity']['local_strict_recent_fraction']])
   if g['readonly']:readonly.append(grid[-1])
 for k in ['1','2','3']:
  for g in items:
   i,j=Ls.index(g['L']),Hs.index(g['H']);neighbors=[h for h in items if i<2 and h['L']==Ls[i+1] and h['H']==g['H'] or j<2 and h['H']==Hs[j+1] and h['L']==g['L']]
   for h in neighbors:
    a,b=full[g['fingerprint']]['scenes'][k],full[h['fingerprint']]['scenes'][k];edges.append([scope,k,g['L'],g['H'],h['L'],h['H'],g['fingerprint'],h['fingerprint'],abs(a['sharpe_365']-b['sharpe_365']),abs(a['net_return_pct']-b['net_return_pct']),abs(a['max_drawdown_pct']-b['max_drawdown_pct'])])
write('cost_scenes.csv',['configuration','fingerprint','scope','L','H','initial_capital_usdt','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','cost_usdt','cost_pct_initial','funding_usdt','gross_plus_funding_to_cost','underlying_executions','underlying_closes','recent40_return_pct','positive5d_folds','status'],cost)
write('walk_forward_folds.csv',['configuration','scope','L','H','cost_multiplier','fold','start_utc','end_exclusive_utc','days','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],wf)
write('recent40_folds.csv',['configuration','scope','L','H','cost_multiplier','fold','start_utc','end_exclusive_utc','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],tail)
write('daily_NAV.csv',['configuration','scope','cost_multiplier','boundary','NAV_usdt'],daily)
cols=['scope','L','H','fingerprint','readonly_old','unchanged_canonical_status','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','recent40_return_pct','positive5d_folds','strict_recent_gate_diagnostic','local_positive3_fraction','local_recent_fraction']
write('sensitivity_grid.csv',cols,grid);write('readonly_reused_scenes.csv',cols,readonly)
write('adjacent_edges.csv',['scope','cost_multiplier','from_L','from_H','to_L','to_H','from_fp','to_fp','absolute_Sharpe_change','absolute_return_change_pp','absolute_DD_change_pp'],edges)
comparisons=rep['matched_hold_comparisons'];write('matched_hold_comparisons.csv',list(comparisons[0]),[list(x.values()) for x in comparisons])
flags={}
for scope in ['native','parent']:
 for k in ['1','2','3']:
  vals=[x[8] for x in edges if x[:2]==[scope,k]];threshold=2*statistics.stdev(vals);flags[scope+'_'+k]={'edge_count':len(vals),'max_Sharpe_change':max(vals),'two_std_change_threshold':threshold,'descriptive_cliff_flag':max(vals)>threshold,'scope':'Descriptive dependent-edge heuristic only, not statistical significance/PBO/DSR.'}
put(R/'edge_flags.json',flags)
fig,axs=plt.subplots(2,4,figsize=(17,8),layout='constrained')
for i,(scope,items) in enumerate([('native',plan['native_grid']),('parent',plan['grid'])]):
 for j,(label,fn) in enumerate([('3x continuous370 return %',lambda c:c['scenes']['3']['net_return_pct']),('3x wholecurve DD %',lambda c:c['scenes']['3']['max_drawdown_pct']),('3x daily Sharpe365',lambda c:c['scenes']['3']['sharpe_365']),('3x recent positive5d /8',lambda c:sum(z['net_return_pct']>0 for z in c['scenes']['3']['recent40']['folds']))]):
  arr=np.empty((3,3))
  for g in items:arr[Ls.index(g['L']),Hs.index(g['H'])]=fn(full[g['fingerprint']])
  ax=axs[i,j];im=ax.imshow(arr,cmap='RdYlGn_r' if j==1 else 'RdYlGn',**({'vmin':0,'vmax':8} if j==3 else {}));ax.set_xticks(range(3),[f'{x*100:g}%' for x in Hs]);ax.set_yticks(range(3),Ls);ax.set_xlabel('Strict fast return hurdle H');ax.set_ylabel('Fast lookback L days');ax.set_title(scope+'\n'+label)
  for g in items:
   a,b=Ls.index(g['L']),Hs.index(g['H']);ax.text(b,a,f'{arr[a,b]:.3f}'+(' O' if g['readonly'] else ' N'),ha='center',va='center',fontsize=9)
  fig.colorbar(im,ax=ax,shrink=.75)
fig.suptitle('Outward L3/4/5 x H2/2.5/3% | ETH actual15000cash/4500entry | S28/zeroexit fixed\nParent adds BTC actual5000cash/500entry at raw child multipliers1/1 | O=readonly unchanged status, N=new actual | reused development history');fig.savefig(R/'sensitivity.png',dpi=140);plt.close(fig)
summary={'report_sha256':sha(R/'report.json'),**plan['expected_counts'],'passed':len(rep['summary']['passed']),'rejected':len(rep['summary']['rejected']),'failed_criteria_by_scope':{scope:dict(collections.Counter(x for c in cfgs.values() if c['scope']==scope for x in c['failed_criteria'])) for scope in ['native','parent']},'positive_by_scope_role_cost':rep['summary']['positive_configs_by_scope_role_cost'],'strict_recent_grid_qualified':{scope:sum(recent_ok(full[g['fingerprint']]) for g in items) for scope,items in [('native',plan['native_grid']),('parent',plan['grid'])]},'CSV_rows':rows,'edge_flags':flags};put(R/'sensitivity_summary.json',summary)
lines=['# ETH 快反转回看期与门槛外扩验证','',f"本轮实际新增{len(cfgs)}配置／{len(cost)}成本场景：5个ETH原生＋5个BTC/ETH组合，{summary['passed']}项passed、{summary['rejected']}项rejected。L=[3,4,5]日×H=[2%,2.5%,3%]完整9点网格每个范围中4点已完成，24旧成本场景仅只读；所有旧资格保持原样，包括上轮3个passed组合与原rejected中心。不同参数允许新测，仅改名称／组件顺序／数值格式不重测。查重22份ETH实际15000/4500完整定义与规则见semantic_inventory.json。",'',
'假设：上轮2/3倍成本的Sharpe较高点位于H2.5%边界，扩大到L5及H3%能否维持平台，而不是不断在重复历史上选高点。全部新L/H事先冻结并逐项reserve成功，再用真实数据执行；新spec.signal直接写明具体L/H，避免旧示例网格。S28、零线退出、对现有与新实际仓位始终应用慢趋势方向门控固定，现金重新入场必须出现新的严格快ROC极值，无隐藏仓位。','',
'BTC原L31/H4%/1%退出缓冲保持，真实本金5000USDT／固定入场预算500；ETH真实本金15000／固定入场预算4500。组合原始子乘数[1,1]代表两个完整实际银行，总本金20000USDT，初始25%／75%本金占比；无自动归一化、转账、借款、抵押净额、免费再平衡或NAV复利调整。已有精确BTC和持有基准复用原始净值，非对10000本金净值线性缩放。','',
'Walk-forward：2025-10-19 UTC00:01至2026-10-24 UTC00:01，370日连续OOS，12完整30日折＋10日尾折。逐折继承现金／数量／入场价／资金费／费用，不重开仓；近期40日继承day330，8个5日折。确定性规则无拟合／标签、purge0；30日预热＋3日间隔，L5和S28均只使用前一完整日以前数据，信号可得后60秒在真实00:01OPEN执行；期末付费平仓。反复使用的历史仍是开发／验证，非未触碰最终测试集，无独立未来或多重选择偏差校正。','',
'成本：每边5bp手续费＋1bp半价差＋2bp滑点＋0.5×过去20完整日样本log波动×sqrt(实际下单量×OPEN/过去20日quoteADV)冲击；每次入场数量floor(固定预算/前一完整收盘/LOT)×LOT，原生LOT／tick／minnotional、参与率≤0.001、费用后1倍入场抵押上限。同向保留数量，反向先平再开。1/2/3倍同时加压执行费用与负资金费，正资金收入不放大；真实settlement纳秒、mark及当时数量记账，资金费available_ts不用于信号。永续空头是现金抵押，无虚构现货借币。逐原生银行独立检查1%闭合小时不利mark高低维护代理；缺L2/TCA、历史完整档位和逐tick清算，不能声称真实容量／成交已验证。','',
'敏感性：完整两轴3×3，索引半径1含自身，原生与组合分开。沿用全部成本净正、1x至少9/12正完整月折、近期各档净正且至少6/8正五日折、3x完整曲线DD≤25%、局部正3倍比例与局部严格近期合格比例均≥60%、至少4次平仓、1x毛价差PnL＋资金费/执行成本≥2.5、无拒单／负抵押／维护代理违规及终止平仓等全部预定判据。旧8点本轮邻域诊断单列，不重写原报告、原criteria或资格；表中旧status仍为原值。全格正Sharpe比例、邻接变化、边界点及Sharpe/Calmar/DD共同判断，见sensitivity_diagnostics与图，不在看结果后修改失败判据。','',
'|新配置|范围|L|H|1x净%|2x净%|3x净%|3x整体DD%|正月折/12|正五日折1/2/3x|状态|','|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|']
for c in cfgs.values():lines.append('|'+c['name']+'|'+c['scope']+f"|{c['L']}|{c['H']*100:g}%|"+'|'.join(f"{c['scenes'][k]['net_return_pct']:.6f}" for k in ['1','2','3'])+f"|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['positive_complete_30d_folds_1x']}|"+'/'.join(str(c['recent40_positive_5d_folds_by_cost'][k]) for k in ['1','2','3'])+'|'+c['status']+'|')
lines+=['',f"失败判据分布：{json.dumps(summary['failed_criteria_by_scope'],ensure_ascii=False)}。本轮全网格严格近期合格数（含只读旧点）：{summary['strict_recent_grid_qualified']}。通过本轮门槛只作为历史候选，不等于全域平滑、最优参数定位或稳定实盘盈利。",'',
'父组合完整净值按共同整数相对ns／事件代码时间轴对齐，保留分钟、闭合小时mark、资金费和交易前后优先级；整体／逐折DD、Sharpe、Calmar从完整合成净值重算，不平均单币指标。所有实际成交、资金费、费用分解和状态段保存，足以重建每档545013点净值；完整dailyNAV和逐变体／逐折CSV留档，未提交可重建大数组。','',
'同实际本金和同固定入场预算的真实持有基准只读复用，27逐格／成本对比与解析现金0%在matched_hold_comparisons.csv；本金相同不代表持仓风险相同。独立审计以Fraction重算5550条新日决策，Decimal独立核算实际资金／LOT／费用／冲击／资金费／小时风险，核验15新原生＋15新父、21只读原生与15只读父NAV哈希及全折／近期指标。资格另独立重算；旧源不重新生成信号或成交。','',
'原冻结SMA65和singleS28账户分别延续，不使用本轮5000/15000本金替换原账户，不改冻结规则／持仓／终止日；十策略真实报价模拟盘只读。账户完整前缀和新增事件、全部登记／命令退出码／原始响应小副本／数据SHA／失败事实及只读监控证明一并封存。','',
'一手背景：[AQR Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)，作者2012-12-05网页，访问2026-10-31，仅为传统股票短反转成本研究背景，不用于加密成本数值校准或收益背书。复现顺序和只读核验见REPRODUCE.md。']
(R/'result.md').write_text('\n'.join(lines)+'\n');print(json.dumps(summary),flush=True)
