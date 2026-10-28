"""Export saved native/parent threshold surfaces, costs, folds and paired old-H2 controls."""
import copy,csv,gzip,io,itertools,json,statistics
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run import ROOT,R,HURDLES,SLOWS,LOOKS,axes,grid_configs,sha,put

def table(path,rows,compress=False):
 fields=list(dict.fromkeys(k for row in rows for k in row));b=io.StringIO(newline='');w=csv.DictWriter(b,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows);path.write_bytes(gzip.compress(b.getvalue().encode(),mtime=0) if compress else b.getvalue().encode())
def main():
 assert not(R/'finish.json').exists();r=json.loads((R/'report.json').read_text());grid=grid_configs(r['configs']);assert len(grid)==36;holds={};docs={}
 for key,ref in json.loads((R/'holds.json').read_text()).items():
  assert sha(ROOT/ref['report'])==ref['report_sha256']
  if ref['report'] not in docs:docs[ref['report']]=json.loads((ROOT/ref['report']).read_text())
  c=copy.deepcopy(docs[ref['report']]['configs'][ref['name']]);c.update(read_only_anchor=True,scope=ref['scope'],asset=ref['asset'],capital_usdt=ref['capital_usdt'])
  for z in c['scenes'].values():
   if 'recent40' not in z:z['recent40']=copy.deepcopy(z['extension40'])
  holds[key]=c
 allby={**grid,**{x['name']:x for x in holds.values()}};rows=[];folds=[];recent=[];daily=[];comp=[];edges=[];cells={}
 for c in allby.values():
  old=c.get('read_only_anchor',False);meta={'name':c['name'],'scope':c['scope'],'asset':c['asset'],'role':c['role'],'read_only_anchor':old,'capital_usdt':c['capital_usdt']}
  if c['role']=='candidate':meta.update({p:c[p] for p in axes(c)})
  cells[c['name']]={**meta,'fingerprint':c['fingerprint'],'original_or_new_status':c['status'],'scenes':{k:{p:z[p] for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','NAV_sha256_f64le']} for k,z in c['scenes'].items()}}
  for k,z in c['scenes'].items():
   rows.append({**meta,'cost_multiplier':int(k),'status':c['status'],**{p:z[p] for p in ['net_return_pct','max_drawdown_pct','daily_mark_drawdown_pct','sharpe_365','calmar','cost_usdt','cost_pct_initial','funding_usdt','gross_reference_PnL_to_execution_cost','executions','round_trips','NAV_sha256_f64le']},**{'recent40_'+p:z['recent40'][p] for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','NAV_sha256_f64le']},**{'cost_'+p:v for p,v in z['cost_parts_usdt'].items()}});folds.extend({**meta,'cost_multiplier':int(k),**f} for f in z['folds']);recent.extend({**meta,'cost_multiplier':int(k),**f} for f in z['recent40']['folds'])
   if old:continue
   daily.extend({**meta,'cost_multiplier':int(k),'boundary_index':j,'equity_usdt':v} for j,v in enumerate(z['daily_equity_usdt']))
   dims=list(axes(c));H,S,L=[c[d] for d in dims];baseline=next(x for x in grid.values() if x['scope']==c['scope'] and x[dims[0]]==.025 and x[dims[1]]==S and x[dims[2]]==L)
   for kind,y in [('same_bank_oldH025',baseline),('same_bank_constant_long',holds[c['asset']])]:
    a=y['scenes'][k];assert y['capital_usdt']==c['capital_usdt'];comp.append({**meta,'cost_multiplier':int(k),'reference_kind':kind,'reference_name':y['name'],'reference_fingerprint':y['fingerprint'],'reference_original_status':y['status'],'new_return_pct':z['net_return_pct'],'reference_return_pct':a['net_return_pct'],'return_delta_pp':z['net_return_pct']-a['net_return_pct'],'DD_delta_pp':z['max_drawdown_pct']-a['max_drawdown_pct'],'recent40_return_delta_pp':z['recent40']['net_return_pct']-a['recent40']['net_return_pct'],'execution_delta':z['executions']-a['executions'],'cost_delta_usdt':z['cost_usdt']-a['cost_usdt'],'new_NAV_sha256':z['NAV_sha256_f64le'],'reference_NAV_sha256':a['NAV_sha256_f64le'],'cash_analytic_return_pct':0,'limit':'Samebank/N/S/L/fixedBTC,differentETHthreshold/realizedrisk' if kind=='same_bank_oldH025' else 'Samebank/N constantlongreference,different native signals/exposure/risk'})
 for scope in ['native','parent']:
  subset=[c for c in grid.values() if c['scope']==scope];dims=axes(subset[0]);fields=list(dims);by={tuple(c[p] for p in fields):c for c in subset};assert set(by)==set(itertools.product(*dims.values()))
  for key,c in by.items():
   for i,(field,axis) in enumerate(dims.items()):
    j=axis.index(key[i])
    if j+1==len(axis):continue
    other=list(key);other[i]=axis[j+1];y=by[tuple(other)];a,b=c['scenes']['3'],y['scenes']['3'];edges.append({'scope':scope,'axis':field,'from':c['name'],'to':y['name'],'return3_delta_pp':b['net_return_pct']-a['net_return_pct'],'DD3_delta_pp':b['max_drawdown_pct']-a['max_drawdown_pct'],'sharpe3_delta':b['sharpe_365']-a['sharpe_365'] if a['sharpe_365'] is not None and b['sharpe_365'] is not None else None,'recent40_return3_delta_pp':b['recent40']['net_return_pct']-a['recent40']['net_return_pct']})
  for H in HURDLES:
   facet=[c for c in subset if c[fields[0]]==H];fig,axs=plt.subplots(3,2,figsize=(12,10),layout='constrained')
   for i,field in enumerate(['net_return_pct','sharpe_365','max_drawdown_pct']):
    values=[(c['scenes']['3']['recent40'] if rr else c['scenes']['3'])[field] for c in facet for rr in [False,True]];limit=max([abs(x) for x in values if x is not None] or [1]) or 1
    for j,rr in enumerate([False,True]):
     mat=np.array([[(by[H,S,L]['scenes']['3']['recent40'] if rr else by[H,S,L]['scenes']['3'])[field] for L in LOOKS] for S in SLOWS],dtype=float);im=axs[i,j].imshow(mat,aspect='auto',cmap='RdYlGn_r' if field=='max_drawdown_pct' else 'RdYlGn',vmin=0 if field=='max_drawdown_pct' else -limit,vmax=limit);axs[i,j].set_title(('Inherited40days' if rr else '370days')+' /3x '+field);axs[i,j].set_xticks(range(len(LOOKS)),LOOKS);axs[i,j].set_yticks(range(len(SLOWS)),SLOWS);axs[i,j].set_xlabel('ETH reversal lookback L(days)');axs[i,j].set_ylabel('ETH slow gate S(days)')
     for x,y in itertools.product(range(len(SLOWS)),range(len(LOOKS))):axs[i,j].text(y,x,('n/a' if np.isnan(mat[x,y]) else f'{mat[x,y]:+.3f}')+('*' if by[H,SLOWS[x],LOOKS[y]].get('read_only_anchor') else ''),ha='center',va='center',fontsize=10)
     fig.colorbar(im,ax=axs[i,j])
   fig.suptitle(scope+' / '+('ETH10000bank,N3000' if scope=='native' else 'BTC1000+ETH3000 entrybudgets,two10000banks raw1/1')+f'\nETH H{H*100:g}%/zeroexit; *oldH2.5majoritycells;knownhistory');fig.savefig(R/f'sensitivity_{scope}_H{int(round(H*1000)):03d}.png',dpi=120);plt.close(fig)
 for field in ['sharpe3_delta']:
  vals=[abs(e[field]) for e in edges if e[field] is not None];cut=2*statistics.pstdev(vals) if vals else None
  for e in edges:e['full_sharpe_cliff']=e[field] is not None and abs(e[field])>cut;e['cliff_threshold']=cut
 counts={'cost':len(rows),'full_folds':len(folds),'recent40_folds':len(recent),'daily_NAV':len(daily),'edges':len(edges),'reference_comparisons':len(comp)};assert list(counts.values())==[114,1482,912,26712,66,144]
 for name,data,zipit in [('sensitivity.csv',rows,False),('fold_results.csv',folds,False),('recent40_fold_results.csv',recent,False),('daily_equity.csv.gz',daily,True),('joint_edges.csv',edges,False),('reference_comparisons.csv',comp,False)]:table(R/name,data,zipit)
 r['joint_grid_sensitivity']={'dimension_count':3,'native_ETH_cells':18,'parent_cells':18,'new_cells':24,'readonly_old_cells':12,'old_hold_controls':2,'adjacent_edges':66,'cells':cells,'old_qualification_unchanged':True,'cliff_definition':'Descriptive absSharpe adjacentdelta >2populationSDof finiteabsdeltas;no oldrerating.'};put(R/'report.json',r)
 cs=list(r['configs'].values());summary={'new_financial_configs':24,'new_native_components':12,'new_passive_parents':12,'passed_candidates':len(r['summary']['passed']),'rejected_candidates':len(r['summary']['rejected']),'positive_configs_by_cost':r['summary']['positive_configs_by_cost'],'failed_criteria_counts':dict(Counter(p for c in cs for p in c['failed_criteria'])),'by_scope':{s:{'new':sum(c['scope']==s for c in cs),'passed':sum(c['scope']==s and c['status']=='passed' for c in cs),'best_full3':max(({'name':c['name'],'return3_pct':c['scenes']['3']['net_return_pct'],'whole_DD3_pct':c['scenes']['3']['max_drawdown_pct'],'recent_return3_pct':c['scenes']['3']['recent40']['net_return_pct'],'positive_months1':c['positive_complete_30d_folds_1x'],'positive_recent1':c['recent40_positive_5d_folds_1x'],'failed_criteria':c['failed_criteria']} for c in cs if c['scope']==s),key=lambda x:x['return3_pct'])} for s in ['native','parent']},'rows':counts};put(R/'summary.json',summary)
 ctx=json.loads((R/'context.json').read_text());lines=[f'# {R.name} 多数表决策略的入场阈值与周期联合敏感性验证',f'实际计算12个新ETH原生＋12个BTC/ETH组合，共24配置/72成本场景；历史通过{summary["passed_candidates"]}、淘汰{summary["rejected_candidates"]}。完整读取{ctx["registry_events"]}登记事件/{ctx["registry_ids"]}ID及{len(ctx["prior_conclusions_read"])}份结论；初始16项已有实际证据。',
 '事前固定多数表决规则下的ETH入场阈值2/2.5/3% × 慢中心27/28/29日 × 反转3/4日。每作用域18格，12个H2.5旧原生/父组合只读且原资格保持；H2/H3新增12原生＋12父组合先逐个成功reserve再计算。33相邻边/作用域。假设：阈值±20%扰动是否改善或破坏前轮S28的历史资格，计算前固定全部规则/金额/边界/门槛，不在本批结果上重调。',
 'ETH前一完整L日ROC严格>H反转空/<-H反转多；带内仅实际多且ROC<0、实际空且ROC>0保留，零退出。慢门控用S−1/S/S+1三个完整ROC，至少两票严格正允许多、至少两票严格负允许空，否则平仓；快反转方向与慢多数方向一致才持仓，现金重入须新严格极端，无隐藏desired。UTC00:01实际OPEN执行，q=floor(N/前一完整close/lot)*lot；不读未来OPEN/资金费/未闭合价格决定信号或数量。引擎与112019多数规则原字节相同，仅spec阈值变化；已运行新H2/H3严格等号不入场、微小越界多空入场及未来数据不变性检查。',
 'ETH独立银行10000、固定新入场3000；BTC固定ROC31/H4%/退出1%、银行10000、入场1000。原值1/1为两个完整独立银行，父本金20000、预算4000=初始父本金20%，不是目标权重或恒定风险；不归一化、不复利调仓、不转账/交叉保证金/再平衡。8旧原生/24成本NAV由真实已保存现金/数量/entry分段恢复并核对SHA；12新原生实际执行专属成交/成本/资金费/风险，12父组合沿共同(ns,eventcode)时轴因果承接上一个完成源点并逐点相加，整体指标重新从连续净值计算，不平均Sharpe/回撤或缩放其他金额。与同S/L的旧多数H2.5、同资金恒多及现金0比较。',
 '8真实合并Parquet及16年度/近期源SHA/字节固定。370日连续OOS2025-10-19UTC00:01至2026-10-24UTC00:01，33日上下文、3日初始embargo。静态规则无拟合/未来标签，purge不适用。12完整30日折＋10日尾折连续承接现金/数量/entry/费用，近期40日从day330继承状态并分8×5日，不重开本金或诊断平仓；仅原预定终点计费平仓。该历史反复研究，属于开发验证，不是未触碰最终测试或独立未来市场。',
 '每侧5bp费＋1bp半价差＋2bp滑点＋0.5×此前20日日log波动×sqrt(实际成交金额/此前20日ADV)冲击，参与率≤0.1%，实际不利tick/lot/最小金额及100%抵押入场上限。资金费=-q×实际结算mark×rate，流出乘1/2/3、收入不放大；永续空头无虚构现货借币。报告逐档执行数、成本占比、费用分项和资金费。缺L2/TCA/历史完整保证金阶梯，1%维持保证金＋闭合小时不利mark仅代理，不保证tick清算安全或实盘容量。',
 '门槛保持：全期/近期三档净正、1倍月正折≥9/12且近期≥6/8、三倍完整连续净值DD≤25%、三维排序索引半径1含自身邻域三倍净正≥60%、至少4往返、(参考毛利＋资金费)/执行成本≥2.5、现金/拒单/独立银行风险违规0、终点空仓且≥180日。旧H2.5十二格是同多数规则的真实参数邻居，但保持原状态，不以新邻域重评级。6图36面板、114成本行、1482全期折、912近期折、26712新日边界、66敏感性边及144匹配对照完整保存。',
 '结果：'+json.dumps(summary,ensure_ascii=False),
 '原单S28冻结候选和旧SMA从Oct28UTC10:30续接至12:30；承接各成本场景现金、数量、entry、费用、已计08:00资金费、已完成日决策、上下文、风险栈和完整净值链。不切换多数规则、不重开本金、不重复事件、不强制截止平仓。真实闭合数据延迟重建，区别于paper10实时报价执行；partial的rejected不取消长期计划。下一资金费16:00、下一日决策Oct29UTC00:01。',
 '背景沿用此前2026-10-27实际访问的[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)与[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)。本多数表决与阈值/周期规则是研究推论，不是论文复现或利润/容量移植。24个新相关试验及既往全部试验存在多重选择偏差，无DSR/PBO、独立未来资格或稳定实盘盈利证明。',
 '复现工作目录/home/desktop/Documents/Codex/EquiTide。audit.py/audit_native.py独立整数信号、Decimal费用/资金费、风险和完整净值；check_sources.py、audit_candidate.py、audit_forward.py及forward.py --reproduce只读真实证据，不重新reserve/evaluate/summarize已完成配置。main普通非强推、完整远端tree/blob/行情SHA验证后释放本轮锁，不建其他分支/定时任务或重部署。'];(R/'result.md').write_text('\n\n'.join(lines)+'\n');print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
