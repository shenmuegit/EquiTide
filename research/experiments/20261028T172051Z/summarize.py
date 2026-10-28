"""Export every new three-bank combination,old controls and within-pair sensitivity surface."""
import copy,csv,gzip,io,itertools,json,statistics
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run import ROOT,R,WEIGHTS,HURDLES,LOOKS,PAIRS,axes,grid_configs,anchor_configs,sha,put

def table(path,rows,compress=False):
 fields=list(dict.fromkeys(k for row in rows for k in row));b=io.StringIO(newline='');w=csv.DictWriter(b,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows);path.write_bytes(gzip.compress(b.getvalue().encode(),mtime=0) if compress else b.getvalue().encode())
def all_configs(report,plan):
 h=plan['read_only_hold_references']['COMBO'];c=copy.deepcopy(json.loads((ROOT/h['report']).read_text())['configs'][h['name']]);c.update(read_only_anchor=True,scope='parent',asset='COMBO',capital_usdt=20000);out={**anchor_configs(),**report['configs'],c['name']:c}
 for c in out.values():
  for z in c['scenes'].values():
   if 'recent40' not in z:z['recent40']=copy.deepcopy(z['extension40'])
 return out
def main():
 assert not(R/'finish_verification.json').exists();r=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text());grid=grid_configs(r['configs']);controls=anchor_configs();allby=all_configs(r,plan);hold=allby[plan['read_only_hold_references']['COMBO']['name']];assert len(grid)==54 and len(allby)==73;rows=[];folds=[];recent=[];daily=[];comp=[];edges=[]
 for c in allby.values():
  old=c.get('read_only_anchor',False);meta={'name':c['name'],'scope':'parent','asset':'COMBO','role':c['role'],'read_only_anchor':old,'capital_usdt':20000}
  if not old:meta.update(slow_pair_days='_'.join(map(str,c['slow_pair_days'])),**{p:c[p] for p in axes(c)})
  for k,z in c['scenes'].items():
   rows.append({**meta,'cost_multiplier':int(k),'status':c['status'],**{p:z[p] for p in ['net_return_pct','max_drawdown_pct','daily_mark_drawdown_pct','sharpe_365','calmar','cost_usdt','cost_pct_initial','funding_usdt','gross_reference_PnL_to_execution_cost','executions','round_trips','NAV_sha256_f64le']},**{'recent40_'+p:z['recent40'][p] for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','NAV_sha256_f64le']},**{'cost_'+p:v for p,v in z['cost_parts_usdt'].items()}});folds.extend({**meta,'cost_multiplier':int(k),**f} for f in z['folds']);recent.extend({**meta,'cost_multiplier':int(k),**f} for f in z['recent40']['folds'])
   if old:continue
   daily.extend({**meta,'cost_multiplier':int(k),'boundary_index':j,'equity_usdt':v} for j,v in enumerate(z['daily_equity_usdt']))
   refs=[(f'single_S{S}',next(x for x in controls.values() if x['trend_filter_lookback_days']==S and x['reversal_return_hurdle']==c['reversal_return_hurdle'] and x['reversal_lookback_days']==c['reversal_lookback_days'])) for S in [27,28,29]]+[('same_capital_constant_long',hold)]
   for kind,y in refs:
    a=y['scenes'][k];comp.append({**meta,'cost_multiplier':int(k),'reference_kind':kind,'reference_name':y['name'],'reference_fingerprint':y['fingerprint'],'reference_original_status':y['status'],'reference_capital_usdt':20000,'return_delta_pp':z['net_return_pct']-a['net_return_pct'],'DD_delta_pp':z['max_drawdown_pct']-a['max_drawdown_pct'],'recent40_return_delta_pp':z['recent40']['net_return_pct']-a['recent40']['net_return_pct'],'cost_delta_usdt':z['cost_usdt']-a['cost_usdt'],'new_NAV_sha256':z['NAV_sha256_f64le'],'reference_NAV_sha256':a['NAV_sha256_f64le'],'cash_analytic_return_pct':0,'limit':'Sameparentcapital20000/ownedentrybudget4000;differenttiming/exposure andindependentETHbankrisk,not equalrisk or new native order sizes.'})
 for pair in PAIRS:
  group=[c for c in grid.values() if c['slow_pair_days']==list(pair)];dims=axes(group[0]);fields=list(dims);by={tuple(c[p] for p in fields):c for c in group};assert len(by)==18
  for key,c in by.items():
   for i,(field,axis) in enumerate(dims.items()):
    j=axis.index(key[i])
    if j+1==len(axis):continue
    other=list(key);other[i]=axis[j+1];y=by[tuple(other)];a,b=c['scenes']['3'],y['scenes']['3'];edges.append({'scope':'parent','pair_group':'_'.join(map(str,pair)),'axis':field,'from':c['name'],'to':y['name'],'return3_delta_pp':b['net_return_pct']-a['net_return_pct'],'DD3_delta_pp':b['max_drawdown_pct']-a['max_drawdown_pct'],'sharpe3_delta':b['sharpe_365']-a['sharpe_365'],'recent40_return3_delta_pp':b['recent40']['net_return_pct']-a['recent40']['net_return_pct']})
  ge=[e for e in edges if e['pair_group']=='_'.join(map(str,pair))];assert len(ge)==33;cut=2*statistics.pstdev(abs(e['sharpe3_delta']) for e in ge)
  for e in ge:e['full_sharpe_cliff']=abs(e['sharpe3_delta'])>cut;e['cliff_threshold']=cut
  for L in LOOKS:
   fig,axs=plt.subplots(3,2,figsize=(12,10),layout='constrained')
   for i,field in enumerate(['net_return_pct','sharpe_365','max_drawdown_pct']):
    vals=[(by[a,H,L]['scenes']['3']['recent40'] if rr else by[a,H,L]['scenes']['3'])[field] for a,H,rr in itertools.product(WEIGHTS,HURDLES,[False,True])];limit=max(abs(x) for x in vals) or 1
    for j,rr in enumerate([False,True]):
     mat=np.asarray([[(by[a,H,L]['scenes']['3']['recent40'] if rr else by[a,H,L]['scenes']['3'])[field] for a in WEIGHTS] for H in HURDLES]);im=axs[i,j].imshow(mat,aspect='auto',cmap='RdYlGn_r' if field=='max_drawdown_pct' else 'RdYlGn',vmin=0 if field=='max_drawdown_pct' else -limit,vmax=limit);axs[i,j].set_title(('Inherited40days' if rr else '370days')+' /3x '+field);axs[i,j].set_xticks(range(3),WEIGHTS);axs[i,j].set_yticks(range(3),[100*H for H in HURDLES]);axs[i,j].set_xlabel(f'ETH S{pair[0]} ownership a (S{pair[1]} owns1-a)');axs[i,j].set_ylabel('ETH reversal threshold H(percent)')
     for x,y in itertools.product(range(3),range(3)):axs[i,j].text(y,x,f'{mat[x,y]:+.3f}',ha='center',va='center')
     fig.colorbar(im,ax=axs[i,j])
   fig.suptitle(f'BTC1 + ETH S{pair[0]}a + S{pair[1]}(1-a);L{L}\ncapital20000,budget4000;source N1000/3000/3000;known development history');fig.savefig(R/f'sensitivity_S{pair[0]}_{pair[1]}_L{L}.png',dpi=120);plt.close(fig)
 counts={'cost':len(rows),'full_folds':len(folds),'recent40_folds':len(recent),'daily_NAV':len(daily),'edges':len(edges),'reference_comparisons':len(comp)};assert list(counts.values())==[219,2847,1752,60102,99,648]
 for name,data,z in [('sensitivity.csv',rows,False),('fold_results.csv',folds,False),('recent40_fold_results.csv',recent,False),('daily_equity.csv.gz',daily,True),('joint_edges.csv',edges,False),('reference_comparisons.csv',comp,False)]:table(R/name,data,z)
 cs=list(r['configs'].values());summary={'new_financial_configs':54,'new_native_components':0,'new_passive_parents':54,'candidate_configs':54,'benchmark_configs':0,'passed_candidates':len(r['summary']['passed']),'rejected_candidates':len(r['summary']['rejected']),'positive_configs_by_cost':r['summary']['positive_configs_by_cost'],'failed_criteria_counts':dict(Counter(p for c in cs for p in c['failed_criteria'])),'rows':counts,'by_pair_group':{'_'.join(map(str,pair)):{'candidates':18,'passed':sum(c['slow_pair_days']==list(pair) and c['status']=='passed' for c in cs),'recent6of8':sum(c['slow_pair_days']==list(pair) and c['recent40_positive_5d_folds_1x']>=6 for c in cs),'full3x_positive_Sharpe_fraction':sum(c['slow_pair_days']==list(pair) and c['scenes']['3']['sharpe_365']>0 for c in cs)/18} for pair in PAIRS}};put(R/'summary.json',summary);ctx=json.loads((R/'context.json').read_text());lines=[f'# {R.name} 双ETH慢周期分散组合验证',f'实际54个新三资金账户组合，历史通过{summary["passed_candidates"]}、淘汰{summary["rejected_candidates"]}。完整读取{ctx["registry_events"]}事件/{ctx["registry_ids"]}ID及{len(ctx["prior_conclusions_read"])}份结论；初始16项实际结果齐全。',plan['hypothesis'],plan['rules']['allocation'],plan['rules']['composition'],plan['rules']['ledger'],plan['rules']['risk'],'事前固定三组慢周期配对27/28、28/29、27/29；每组ETH_A份额a=0.25/0.5/0.75、共同阈值H2/2.5/3%、快反转L3/4形成3D18格，合计54格、99条组内邻接边。分类配对不假定数值距离，不跨组凑邻域。所有54完整spec均包含三个原生源的全部参数字典，reserve前逐字段及周期三元组核验；不是模板继承单中心别名。相同组件和原值权重做语义查重，不因名字或组件顺序伪创新。','源BTC保持ROC31/H4%/E1%、N1000；两个ETH各用S−1/S/S+1严格符号多数门控，反转ROC L严格>H空/<−H多；带内仅实际多且ROC<0、实际空且ROC>0保留，零退出，门控不容许则平仓。日信号只用此前完成close，按此前close取lot，UTC00:01实际OPEN执行。无隐藏desired、未来OPEN/资金费或未闭合价格参与信号。完整规则/原生源FP与SHA随spec冻结。','21个旧原生/63成本NAV由保存的现金/数量/entry片段恢复并核对原SHA，不重跑源信号、成交或资金费模型。所有父层逐点相加后重新计算Sharpe、Calmar与连续整体DD，不能平均组件指标。不同参数虽可能回报接近，仍按完整具体配置分别登记。','真实8合并Parquet及16年度/近期源SHA/字节固定。370日OOS2025-10-19UTC00:01至2026-10-24UTC00:01，33日上下文含30预热和3日初始embargo；静态规则无拟合/未来标签，purge不适用。12个完整30日折与10日尾折承接账户；近期40日从day330继承分8×5日，既不重开本金也不诊断平仓，仅原终点计费退出。已反复使用的历史是开发验证，不能称未触碰最终测试。','成本保留原生实际订单：每侧5bp费＋1bp半价差＋2bp滑点＋0.5×此前20日样本日log波动×sqrt(实际源订单金额/此前20日quoteADV)冲击，参与率≤0.1%，tick/lot/最小金额与全额抵押入场约束保留。资金费=-有符号数量×实际结算mark×rate，流出乘1/2/3、收入不放大；永续不虚构现货借币。源原始N3000的成本只按银行所有权分摊，不声称已验证750/1500/2250的新订单成交或净额容量。','门槛保持：全期/近期各档净正，1倍月正折≥9/12、近期≥6/8，三倍连续整体DD≤25%，组内3D邻域三倍净正≥60%，≥4往返，(参考毛利＋资金费)/成本≥2.5，现金/拒单/独立银行风险违规0，终点空仓且≥180日。18个原单S27/28/29父组合及20k同预算恒多/现金0只读对照，原资格不变，不以新邻域重评级。',json.dumps(summary,ensure_ascii=False),'原单S28冻结候选与SMA65从UTC14:30续接至16:30；新窗口含16:00实际资金费，必须按实际结算时间/仓位/mark/rate逐条核验，仅计一次，收入不随成本放大，并保存16时段资金费前后风险状态供下轮17:00闭合小时检查。原策略/本金/持仓/entry/成本/完整净值前缀承接，不换新组合，不强制截止平仓。下一日决策Oct29UTC00:01。延迟真实闭合行情重建，不能冒充十策略实时公开报价执行。','背景沿用2026-10-27实际访问的一手[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)和[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)。本分散组合为研究推论，不是论文复现或收益移植。54个相关新试验加所有先前试验存在多重选择偏差；无DSR/PBO、独立未来验证或稳定实盘盈利证明。','复现工作目录/home/desktop/Documents/Codex/EquiTide；audit.py独立Decimal事件播放及全部组合NAV/折/资金费/成本检查；check_sources.py、check_exports.py、audit_candidate.py、audit_forward.py、check_feed.py只读证据，forward.py --reproduce离线复现；不重跑/预留/汇总已完成配置。只提交轻量研究证据，大行情/HTTPpacket留ignoreddata绑定SHA，原账户账本/冻结规则/登记和失败证据完整保留。main普通非强推，远端完整tree/blob/SHA核验后释放本轮锁。'];(R/'result.md').write_text('\n\n'.join(lines)+'\n');print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
