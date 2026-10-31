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
   i,j=Ls.index(g['L']),Hs.index(g['H']);neighbors=[h for h in items if i<3 and h['L']==Ls[i+1] and h['H']==g['H'] or j<3 and h['H']==Hs[j+1] and h['L']==g['L']]
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
fig,axs=plt.subplots(2,4,figsize=(18,10),layout='constrained')
for i,(scope,items) in enumerate([('native',plan['native_grid']),('parent',plan['grid'])]):
 for j,(label,fn) in enumerate([('3x continuous370 return %',lambda c:c['scenes']['3']['net_return_pct']),('3x wholecurve DD %',lambda c:c['scenes']['3']['max_drawdown_pct']),('3x daily Sharpe365',lambda c:c['scenes']['3']['sharpe_365']),('3x recent positive5d /8',lambda c:sum(z['net_return_pct']>0 for z in c['scenes']['3']['recent40']['folds']))]):
  arr=np.empty((4,4))
  for g in items:arr[Ls.index(g['L']),Hs.index(g['H'])]=fn(full[g['fingerprint']])
  ax=axs[i,j];im=ax.imshow(arr,cmap='RdYlGn_r' if j==1 else 'RdYlGn',**({'vmin':0,'vmax':8} if j==3 else {}));ax.set_xticks(range(4),[f'{x*100:g}%' for x in Hs]);ax.set_yticks(range(4),Ls);ax.set_xlabel('Strict fast return hurdle H');ax.set_ylabel('Fast lookback L days');ax.set_title(scope+'\n'+label)
  for g in items:
   a,b=Ls.index(g['L']),Hs.index(g['H']);ax.text(b,a,f'{arr[a,b]:.3f}'+(' O' if g['readonly'] else ' N'),ha='center',va='center',fontsize=8)
  fig.colorbar(im,ax=ax,shrink=.75)
fig.suptitle('Complete union L2/3/4/5 x H1.5/2/2.5/3% | ETH actual15000cash/4500entry | S28/zeroexit fixed\nParent adds BTC actual5000cash/500entry at raw child multipliers1/1 | O=readonly unchanged status, N=new actual | reused development history');fig.savefig(R/'sensitivity.png',dpi=140);plt.close(fig)
summary={'report_sha256':sha(R/'report.json'),**plan['expected_counts'],'passed':len(rep['summary']['passed']),'rejected':len(rep['summary']['rejected']),'failed_criteria_by_scope':{scope:dict(collections.Counter(x for c in cfgs.values() if c['scope']==scope for x in c['failed_criteria'])) for scope in ['native','parent']},'positive_by_scope_role_cost':rep['summary']['positive_configs_by_scope_role_cost'],'strict_recent_grid_qualified':{scope:sum(recent_ok(full[g['fingerprint']]) for g in items) for scope,items in [('native',plan['native_grid']),('parent',plan['grid'])]},'CSV_rows':rows,'edge_flags':flags};put(R/'sensitivity_summary.json',summary)
lines=['# ETH 快反转完整联合网格验证','',f"补齐预先指定的两个相反角点：L2/H3%与L5/H1.5%，新增2个ETH实际原生定义和2个对应父组合，共{len(cfgs)}配置／{len(cost)}成本场景，{summary['passed']}项passed、{summary['rejected']}项rejected。其余每范围14个实际格点只读复用，84旧成本场景不再运行策略。两范围合计完整32个具体配置／96成本场景，旧资格原样保留；27份ETH15000/4500完整经济定义的查重见semantic_inventory.json。",'',
'经济假设：联合L=[2,3,4,5]日×严格H=[1.5%,2%,2.5%,3%]避免仅移动测试局部窗口。两个缺点在上轮已提出但未预留／计算，本轮完整规则／输入／时间边界／失败判据和每个具体spec冻结并reserve成功后才执行。ETH S28、零线退出、慢趋势方向门控作用于现有及新实际仓位，保持真正q，不保留隐藏方向；现金重新入场须新的严格快ROC极值。新signal文字显式写各具体L/H，不继承旧示例范围。','',
'BTC原L31/H4%/退出缓冲1%固定，本金5000USDT／固定入场预算500；ETH本金15000／预算4500。组合子乘数原值[1,1]表示两个完整实际银行，总本金20000，初始本金占比25%／75%；无自动归一化、NAV份额缩放、转账、再平衡、借款或跨行抵押抵消。新参数ETH实际重新计算整数LOT数量／冲击／费用／资金费；父组合优先使用已完成精确BTC净值，持有基准也按同实际本金和入场预算只读复用。','',
'Walk-forward：真实2025-10-19 UTC00:01至2026-10-24 UTC00:01连续370日，12完整30日折＋10日尾折；现金／q／entry／资金费／费用跨折继承，只有最终付费平仓，近期40日从day330真实状态继续并报告8个5日折。确定性规则无需拟合／标签，purge0，30日预热＋3日间隔，L5和S28只读过去已闭合close，信号可得后60秒在00:01实际OPEN执行。规则已用历史反复开发，本轮也属于开发验证，不称未触碰最终测试集或独立未来，无DSR/PBO、多重选择校正声明。','',
'成本：每边5bp手续费＋1bp半价差＋2bp滑点＋0.5×过去20完整日样本log波动×sqrt(实际下单量×OPEN/过去20日quoteADV)冲击，1/2/3倍压力。q=floor(固定预算/前一完整close/LOT)×LOT，原生不利tick、minnotional、参与率≤0.001、费用后1倍入场抵押上限；同向保留q，反向先平再开。真实资金费settlement纳秒／mark／当时q记账，负支出加压，正收入不增；available_ts不进入信号。永续现金抵押空头无虚构现货借币。逐行独立1%闭合小时不利mark高低维护代理；价差、滑点和冲击为冻结估计，缺L2/TCA、历史完整档位及逐tick清算，不能声称真实容量或成交已验证。','',
'敏感性：完整两轴4×4，索引半径1含中心，不挑窄窗口；原生与组合分别计算正Sharpe比例、边界极值、描述性邻接变化、Sharpe、Calmar及完整曲线DD。沿用全成本净正、1x至少9/12正完整月折、近期各成本净正且至少6/8正五日折、3x整体DD≤25%、局部正3倍和严格近期合格率分别≥60%、至少4次平仓、1x毛价差PnL＋资金费／执行成本≥2.5、零拒单／负抵押／维护代理违规及终止平仓等全部原门槛。旧criteria／sensitivity／status／report保持，当前完整联合邻域另存current_grid_diagnostic_sensitivity，不重评旧资格。','',
'|新配置|范围|L|H|1x净%|2x净%|3x净%|3x整体DD%|正月折/12|正五日折1/2/3x|状态|','|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|']
for c in cfgs.values():lines.append('|'+c['name']+'|'+c['scope']+f"|{c['L']}|{c['H']*100:g}%|"+'|'.join(f"{c['scenes'][k]['net_return_pct']:.6f}" for k in ['1','2','3'])+f"|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['positive_complete_30d_folds_1x']}|"+'/'.join(str(c['recent40_positive_5d_folds_by_cost'][k]) for k in ['1','2','3'])+'|'+c['status']+'|')
lines+=['',f"新配置失败判据分布：{json.dumps(summary['failed_criteria_by_scope'],ensure_ascii=False)}；完整网格严格近期合格格点数：{summary['strict_recent_grid_qualified']}。全年净正和历史局部passed不自动推导长期稳定盈利，负收益／负折／失败均留档。",'',
'组合按真实共同整数相对ns与事件优先级对齐完整NAV，整体／月折／近期DD、Sharpe和Calmar重新从合成曲线计算，不平均单币收益或指标。48逐父格点／成本的同实际本金持有对比和解析现金0%见matched_hold_comparisons；相同本金不等于相同风险。全部新实际交易、资金费、费用、状态段及每档545013点NAV SHA保留，完整dailyNAV／逐折／全部变体导出8CSV，未提交可重建大数组。','',
'独立核验以Fraction重算2220条新日决策，以Decimal重建成交、现金、LOT／tick／ADV冲击、费用、资金费和小时维护代理；核对6新原生＋6新父、51只读原生与45只读父的完整净值SHA及整体／月折／近期指标。另独立核对4项新资格和28项旧格点原criteria／sensitivity／status，旧策略不重新生成信号或成交。','',
'原冻结SMA65和singleS28账户独立续接，保持原本金／规则／真实模拟持仓及终止日，不替换为本轮5000/15000金额；十策略真实报价账户只读。数据SHA、完整账本、原始小响应副本、登记／finish、检查／失败事实和只读监控更新一并保存。','',
'一手背景：[AQR Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)，作者2012-12-05网页，访问2026-10-31，仅作传统股票短反转成本背景，不用于加密成本数值校准或收益背书。复现顺序与只读核验见REPRODUCE.md。']
(R/'result.md').write_text('\n'.join(lines)+'\n');print(json.dumps(summary),flush=True)
