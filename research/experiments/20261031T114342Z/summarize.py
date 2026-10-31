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
   grid.append([scope,g['L'],g['H'],g['fingerprint'],g['readonly'],c['status'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['recent40']['net_return_pct'],sum(z['net_return_pct']>0 for z in s['recent40']['folds']),recent_ok(c),c.get('sensitivity',{}).get('local_3x_neighbor_positive_fraction'),c.get('sensitivity',{}).get('local_recent_allcost_qualifying_fraction')])
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
write('sensitivity_grid.csv',cols,grid);write('readonly_center_scenes.csv',cols,readonly)
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
fig.suptitle('ETH actual15000cash/4500entry | slowS28/zeroexit fixed\nParent adds BTC actual5000cash/500entry at raw child multipliers1/1 | O=readonly unchanged status, N=new actual | reused development history');fig.savefig(R/'sensitivity.png',dpi=140);plt.close(fig)
summary={'report_sha256':sha(R/'report.json'),**plan['expected_counts'],'passed':len(rep['summary']['passed']),'rejected':len(rep['summary']['rejected']),'failed_criteria_by_scope':{scope:dict(collections.Counter(x for c in cfgs.values() if c['scope']==scope for x in c['failed_criteria'])) for scope in ['native','parent']},'positive_by_scope_role_cost':rep['summary']['positive_configs_by_scope_role_cost'],'strict_recent_grid_qualified':{scope:sum(recent_ok(full[g['fingerprint']]) for g in items) for scope,items in [('native',plan['native_grid']),('parent',plan['grid'])]},'CSV_rows':rows,'edge_flags':flags};put(R/'sensitivity_summary.json',summary)
lines=['# ETH 快反转回看期与门槛联合验证','',f"本轮{len(cfgs)}个新配置／{len(cost)}成本场景，{summary['passed']}项passed，{summary['rejected']}项rejected。8个新ETH原生定义＋8个对应父组合均已实际计算；两个旧中心只读复用，历史rejected状态不重评。所有正负收益、负折及失败均保留。",'',
'假设：在BTC实际5000USDT本金／500固定入场预算、ETH实际15000／4500预算下，快反转L=[2,3,4]日与严格入场H=[1.5%,2%,2.5%]联合网格能否形成稳健平台。ETH慢趋势S28、零线退出、逐日作用于新旧真实仓位的方向门控固定；BTC原L31/H4%/退出缓冲1%规则固定。相同具体旧中心复用；其他同族但退出缓冲、门控应用或资金费过滤不同的历史不排除本轮新配置。完整14项原生15000/4500历史规则、参数和指纹的查重清单已存semantic_inventory.json。','',
'原始子乘数[1,1]表示两个完整实际银行，合计20000USDT；初始本金分配25%／75%，不自动归一化、不转账、不再平衡、无借款或跨仓抵押净额。每次新入场原生数量=floor(固定预算/前一完整日收盘/LOT)×LOT，下一UTC00:01真实OPEN不利tick执行；同方向保留真实数量，退出后重新入场须新严格极值，不保留隐藏仓位。全部16项逐个reserve成功后才开始计算。','',
'Walk-forward：真实2025-10-19 UTC00:01至2026-10-24 UTC00:01共370日，12完整30日折＋10日尾折；现金、数量、入场价、资金费、费用跨折连续，仅期末付费平仓。近期40日继承day330状态，8个5日折，无诊断重开仓。固定确定性规则无需拟合／标签，标签purge0；预热30日＋3日间隔，最大S28和L4全部只读过去完整close，信号可得后60秒执行。已有历史反复开发，非未触碰最终留出；本轮不按OOS优选后宣称独立验证。','',
'参数敏感性：两轴完整3×3，索引半径1含中心，原生／组合分别比较；沿用全年各档净正、1x至少9/12正月折、近期各档正且≥6/8正五日折、3x整体DD≤25%、局部正收益和局部严格近期合格比例均≥60%、至少4次平仓及毛价差PnL＋资金费/执行成本≥2.5等冻结门槛。旧中心资格保持原报告原字节；参与邻域统计不构成重评。逐变体Sharpe/Calmar/净收益/整体DD和描述性邻接变化完整保留，无DSR/PBO、多重选择校正或独立样本声明。','',
'成本：每边手续费5bp＋半价差1bp＋滑点2bp＋0.5×过去20完整日样本log波动×sqrt(实际数量×OPEN/过去20日quoteADV)冲击；1/2/3倍压力，原生tick/LOT/minnotional／参与率≤0.001／费用后抵押1倍入场上限。永续用真实资金费结算ns、mark及当时数量，负支出加压、正收入不放大；永续不用虚构现货借币。每银行独立1%闭合小时不利mark高低维护代理。价差／滑点／冲击为估计，缺L2/TCA和完整历史保证金档位，不能视为真实容量或逐tick清算验证。','',
'|配置|范围|L|H|1x净%|2x净%|3x净%|3x完整DD%|正月折/12|正五日折1/2/3x|状态|','|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|']
for c in cfgs.values():lines.append('|'+c['name']+'|'+c['scope']+f"|{c['L']}|{c['H']*100:g}%|"+'|'.join(f"{c['scenes'][k]['net_return_pct']:.6f}" for k in ['1','2','3'])+f"|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['positive_complete_30d_folds_1x']}|"+'/'.join(str(c['recent40_positive_5d_folds_by_cost'][k]) for k in ['1','2','3'])+'|'+c['status']+'|')
lines+=['',f"淘汰门槛分布：{json.dumps(summary['failed_criteria_by_scope'],ensure_ascii=False)}。严格近期合格格点数（含旧中心只读）：{summary['strict_recent_grid_qualified']}。全年成本后盈利不能代替近期和邻域稳健性。",'',
'比较：同本金、同固定入场预算的真实持有基准完全只读复用，逐9父格点／3成本比较与解析现金0%均存matched_hold_comparisons.csv；相同本金不代表相同持仓风险。组合由对齐联合时间轴的完整实际净值相加计算整体／逐折DD、Sharpe、Calmar，不平均单币指标。数据8文件SHA及版本见plan/data_manifest，完整交易／资金费／状态段足以重建每档545013点净值，未提交可重建大数组。','',
'独立审计：Fraction重算全部8880条新ETH日决策，Decimal重建实际成交／现金／费用／资金费／LOT与小时维护代理，再独立核对24原生＋24父曲线和完整／逐月／近期指标；旧源只读状态重建核验原NAV SHA，无旧策略再运行。具体审计计数见verification.json。原冻结SMA65、singleS28账户各自延续，保持原本金／规则／持仓和终止日；十策略账户只读。','',
'预检一次BTC分支编辑错误在任何reserve／真实计算前被合成测试捕获并修复，原失败日志留档；初始16项已有真实证据，未伪装补测。实际金融回测结果与原始登记保留。旧资格不改，正收益回测不称稳定实盘盈利。','',
'一手背景：[AQR Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)，作者2012-12-05工作论文网页，访问2026-10-31。仅为传统股票短反转成本敏感性的背景，不用于加密成本数值校准或收益背书。','',
'复现：先阅读REPRODUCE.md；审计与只读导出不下单、不改旧结果。实际reserve／finish命令回执、完整失败事实、真实输入小响应副本、main提交／推送与全远端必要blob核验均留档。']
(R/'result.md').write_text('\n'.join(lines)+'\n');print(json.dumps(summary),flush=True)
