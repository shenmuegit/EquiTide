"""Export complete two-dimensional native/parent results and unchanged old controls."""
import copy,csv,gzip,io,itertools,json,statistics
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run import ROOT,R,SLOWS,LOOKS,axes,grid_configs,sha,put

def table(path,rows,compress=False):
 fields=list(dict.fromkeys(k for row in rows for k in row));b=io.StringIO(newline='');w=csv.DictWriter(b,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows);path.write_bytes(gzip.compress(b.getvalue().encode(),mtime=0) if compress else b.getvalue().encode())
def main():
 assert not(R/'finish.json').exists();r=json.loads((R/'report.json').read_text());grid=grid_configs(r['configs']);assert len(grid)==12;holds={};docs={}
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
   rows.append({**meta,'cost_multiplier':int(k),'status':c['status'],**{p:z[p] for p in ['net_return_pct','max_drawdown_pct','daily_mark_drawdown_pct','sharpe_365','calmar','cost_usdt','funding_usdt','gross_reference_PnL_to_execution_cost','executions','round_trips','NAV_sha256_f64le']},**{'recent40_'+p:z['recent40'][p] for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','NAV_sha256_f64le']},**{'cost_'+p:v for p,v in z['cost_parts_usdt'].items()}});folds.extend({**meta,'cost_multiplier':int(k),**f} for f in z['folds']);recent.extend({**meta,'cost_multiplier':int(k),**f} for f in z['recent40']['folds'])
   if old:continue
   daily.extend({**meta,'cost_multiplier':int(k),'boundary_index':j,'equity_usdt':v} for j,v in enumerate(z['daily_equity_usdt']))
   dims=list(axes(c));S=c[dims[0]];baseline=next(x for x in grid.values() if x['scope']==c['scope'] and x[dims[0]]==S and x[dims[1]]==5)
   for kind,y in [('same_bank_oldfast5',baseline),('same_bank_constant_long',holds[c['asset']])]:
    a=y['scenes'][k];assert y['capital_usdt']==c['capital_usdt'];comp.append({**meta,'cost_multiplier':int(k),'reference_kind':kind,'reference_name':y['name'],'reference_fingerprint':y['fingerprint'],'reference_original_status':y['status'],'new_return_pct':z['net_return_pct'],'reference_return_pct':a['net_return_pct'],'return_delta_pp':z['net_return_pct']-a['net_return_pct'],'DD_delta_pp':z['max_drawdown_pct']-a['max_drawdown_pct'],'recent40_return_delta_pp':z['recent40']['net_return_pct']-a['recent40']['net_return_pct'],'execution_delta':z['executions']-a['executions'],'cost_delta_usdt':z['cost_usdt']-a['cost_usdt'],'new_NAV_sha256':z['NAV_sha256_f64le'],'reference_NAV_sha256':a['NAV_sha256_f64le'],'cash_analytic_return_pct':0,'limit':'Samebank/N/S/H/fixedBTC,differentETHspeed/realizedrisk' if kind=='same_bank_oldfast5' else 'Samebank/N constantlongreference,different native signals/exposure/risk'})
 for scope in ['native','parent']:
  subset=[c for c in grid.values() if c['scope']==scope];dims=axes(subset[0]);fields=list(dims);by={tuple(c[p] for p in fields):c for c in subset};assert set(by)==set(itertools.product(*dims.values()))
  for key,c in by.items():
   for i,(field,axis) in enumerate(dims.items()):
    j=axis.index(key[i])
    if j+1==len(axis):continue
    other=list(key);other[i]=axis[j+1];y=by[tuple(other)];a,b=c['scenes']['3'],y['scenes']['3'];edges.append({'scope':scope,'axis':field,'from':c['name'],'to':y['name'],'return3_delta_pp':b['net_return_pct']-a['net_return_pct'],'DD3_delta_pp':b['max_drawdown_pct']-a['max_drawdown_pct'],'sharpe3_delta':b['sharpe_365']-a['sharpe_365'] if a['sharpe_365'] is not None and b['sharpe_365'] is not None else None,'recent40_return3_delta_pp':b['recent40']['net_return_pct']-a['recent40']['net_return_pct']})
  fig,axs=plt.subplots(3,2,figsize=(12,10),layout='constrained')
  for i,field in enumerate(['net_return_pct','sharpe_365','max_drawdown_pct']):
   values=[(c['scenes']['3']['recent40'] if rr else c['scenes']['3'])[field] for c in subset for rr in [False,True]];limit=max([abs(x) for x in values if x is not None] or [1]) or 1
   for j,rr in enumerate([False,True]):
    mat=np.array([[(by[S,L]['scenes']['3']['recent40'] if rr else by[S,L]['scenes']['3'])[field] for L in LOOKS] for S in SLOWS],dtype=float);im=axs[i,j].imshow(mat,aspect='auto',cmap='RdYlGn_r' if field=='max_drawdown_pct' else 'RdYlGn',vmin=0 if field=='max_drawdown_pct' else -limit,vmax=limit);axs[i,j].set_title(('Inherited40days' if rr else '370days')+' / 3x '+field);axs[i,j].set_xticks(range(3),LOOKS);axs[i,j].set_yticks(range(len(SLOWS)),SLOWS);axs[i,j].set_xlabel('ETH reversal lookback L(days)');axs[i,j].set_ylabel('ETH slow gate S(days)')
    for x,y in itertools.product(range(len(SLOWS)),range(len(LOOKS))):axs[i,j].text(y,x,('n/a' if np.isnan(mat[x,y]) else f'{mat[x,y]:+.3f}')+('*' if by[SLOWS[x],LOOKS[y]].get('read_only_anchor') else ''),ha='center',va='center')
    fig.colorbar(im,ax=axs[i,j])
  fig.suptitle(scope+' / '+('ETH 10000bank,N3000' if scope=='native' else 'BTC1000+ETH3000 entrybudgets,two10000banks raw1/1')+'\nH2%/ETHzeroexit; *old actual L5 cells;knownhistory');fig.savefig(R/f'sensitivity_{scope}.png',dpi=120);plt.close(fig)
 for field in ['sharpe3_delta']:
  vals=[abs(e[field]) for e in edges if e[field] is not None];cut=2*statistics.pstdev(vals) if vals else None
  for e in edges:e['full_sharpe_cliff']=e[field] is not None and abs(e[field])>cut;e['cliff_threshold']=cut
 counts={'cost':len(rows),'full_folds':len(folds),'recent40_folds':len(recent),'daily_NAV':len(daily),'edges':len(edges),'reference_comparisons':len(comp)};assert list(counts.values())==[42,546,336,8904,14,48]
 for name,data,zipit in [('sensitivity.csv',rows,False),('fold_results.csv',folds,False),('recent40_fold_results.csv',recent,False),('daily_equity.csv.gz',daily,True),('joint_edges.csv',edges,False),('reference_comparisons.csv',comp,False)]:table(R/name,data,zipit)
 r['joint_grid_sensitivity']={'dimension_count':2,'native_ETH_cells':6,'parent_cells':6,'new_cells':8,'readonly_old_cells':4,'old_hold_controls':2,'adjacent_edges':14,'cells':cells,'old_qualification_unchanged':True,'cliff_definition':'Descriptive absSharpe adjacentdelta >2populationSDof finiteabsdeltas;no oldrerating.'};put(R/'report.json',r)
 cs=list(r['configs'].values());summary={'new_financial_configs':8,'new_native_components':4,'new_passive_parents':4,'passed_candidates':len(r['summary']['passed']),'rejected_candidates':len(r['summary']['rejected']),'positive_configs_by_cost':r['summary']['positive_configs_by_cost'],'failed_criteria_counts':dict(Counter(p for c in cs for p in c['failed_criteria'])),'by_scope':{s:{'new':sum(c['scope']==s for c in cs),'passed':sum(c['scope']==s and c['status']=='passed' for c in cs),'best_full3':max(({'name':c['name'],'return3_pct':c['scenes']['3']['net_return_pct'],'whole_DD3_pct':c['scenes']['3']['max_drawdown_pct'],'recent_return3_pct':c['scenes']['3']['recent40']['net_return_pct'],'positive_months1':c['positive_complete_30d_folds_1x'],'positive_recent1':c['recent40_positive_5d_folds_1x'],'failed_criteria':c['failed_criteria']} for c in cs if c['scope']==s),key=lambda x:x['return3_pct'])} for s in ['native','parent']},'rows':counts};put(R/'summary.json',summary)
 ctx=json.loads((R/'context.json').read_text());lines=[f'# {R.name} ETH六至七日反转与慢趋势交互验证',f'实际计算4个ETH原生策略＋4个组合，共8配置/24成本场景，历史通过{summary["passed_candidates"]}、淘汰{summary["rejected_candidates"]}。完整读取{ctx["registry_events"]}事件/{ctx["registry_ids"]}ID及{len(ctx["prior_conclusions_read"])}份结论，初始16项均有真实历史证据，无缺结果条目可补。',
 '事前预设ETH慢28/31日×反转5/6/7日，阈值2%、零交叉退出、原生银行10000、固定入场3000。6/7日4原生＋4组合各自先reserve后计算，5日旧2原生＋2组合只读，保留旧资格。BTC固定此前完整31日ROC严格>4%多/<-4%空，带内多仅ROC>-1%、空仅ROC<1%保持；完整反向极端先平后开，银行10000、固定入场1000。此前L5位于回看网格边界，扩大周期检验频率与近期分折，不能把结果当独立新市场证据。',
 'ETH此前完整L日ROC严格>2%反转空/<-2%反转多，带内多仅ROC<0、空仅ROC>0保留，零退出；慢S日ROC正仅许多、负仅许空，零/不兼容平实际仓位，现金重入须新极端，无隐藏desired。UTC00:01真实OPEN执行，数量floor(N/此前完整close/lot)，信号/手数不使用未来OPEN、未闭合价格或资金费。引擎仅扩大允许反转回看到6/7，其余信号、订单、成本、资金费、风险、指标代码保持字节一致。',
 '原值1/1指两个完整10000USDT独立银行，组合本金20000；入场预算合计4000=初始本金20%，不是实际恒定风险比例，不归一化、不复利调仓、不转账/交叉保证金/再平衡。4旧原生/12成本NAV从真实账本只读恢复并核对原SHA，不重跑旧模型；新N3000原生逐档实际模拟。父组合按共同(ns,eventcode)时轴承接上一完成点后逐点相加并重算指标，不平均Sharpe/收益或缩放旧净值。每新项与相同S/N的旧L5、同金额恒多及解析现金0逐档比较。',
 '真实8合并Parquet和16年度/近期源SHA/字节固定。370日连续OOS2025-10-19UTC00:01至2026-10-24UTC00:01，33日上下文、3日初始embargo，覆盖最大慢31/反转7日。静态规则无拟合/未来标签，purge不适用；12完整30日折＋10日尾折连续carry现金/数量/entry/成本，近期40日继承day330状态并分8×5日，不重开本金/诊断平仓，仅预定终点计费平仓。反复使用历史只属开发验证，不称最终未触碰留出。',
 '每侧5bp费＋1bp半价差＋2bp滑点＋0.5×此前20日日log波动×sqrt(成交金额/此前20日ADV)冲击，参与率≤0.1%；实际不利tick/lot/最小金额、100%抵押入场。资金费=-q×实际结算mark×rate，流出乘1/2/3，收入不放大；永续无虚构现货借币。成本金额、分项、占本金比例、资金费和交易数逐档保存。价差/滑点/冲击是估计，缺L2/TCA/完整历史margin阶梯；1%维持保证金＋闭合小时不利mark仅代理，不保证容量或tick清算安全。',
 '预设门槛保持：全期/近期三档净正，1倍完整月正折≥9/12且近期≥6/8，3倍完整连续NAV最大DD≤25%，二维排序相邻索引半径1含自身邻域净正≥60%，≥4往返、(参考毛利＋资金费)/费用≥2.5，现金/拒单/风险代理违规0、终点空仓且≥180日。两作用域各6格、7边，全部收益/回撤/Sharpe/Calmar、陡变/边界、逐折/逐变体留档。旧资格不按新邻域重评级。',
 '结果：'+json.dumps(summary,ensure_ascii=False),
 '原H4/ETH慢28日反转3日冻结前向候选及旧SMA仅续接至Oct27UTC14:30，承接12:30完整现金/数量/entry/费用/资金费/风险段/NAV链，不重复08:00.001旧资金费。无新增日决策/强制平仓，两者为延迟闭合行情重建，不能当paper10真实报价账户或成熟前向资格。paper10冻结账本只读，部分观察rejected不取消长期计划。',
 '一手背景复用此前2026-10-27实际访问的[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)（2012-05-01）及[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)（2012-12-05）。加密6/7日反转与慢门槛为本研究推论，非论文复现或传统市场利润/容量移植。8个新相关试验存在多重选择偏差，无DSR/PBO或稳定实盘盈利证明。',
 '复现工作目录/home/desktop/Documents/Codex/EquiTide；audit.py调用audit_native.verify独立核验整数信号、Decimal费用/资金费/状态/NAV。check_sources.py、audit_candidate.py、audit_forward.py及forward.py --reproduce只读已有实际证据，不重复reserve/evaluate/summarize已完成配置。main普通非强推并完成freshfetch/独立allheads/完整tree/blob/行情SHA证明后释放自己锁，不建分支/重复任务、不重部署或真实下单。'];(R/'result.md').write_text('\n\n'.join(lines)+'\n');print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
