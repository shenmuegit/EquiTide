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
   dims=list(axes(c));S=c[dims[0]];baseline=next(x for x in grid.values() if x['scope']==c['scope'] and x[dims[0]]==S and x[dims[1]]==3)
   for kind,y in [('same_bank_fast3',baseline),('same_bank_constant_long',holds[c['asset']])]:
    a=y['scenes'][k];assert y['capital_usdt']==c['capital_usdt'];comp.append({**meta,'cost_multiplier':int(k),'reference_kind':kind,'reference_name':y['name'],'reference_fingerprint':y['fingerprint'],'reference_original_status':y['status'],'new_return_pct':z['net_return_pct'],'reference_return_pct':a['net_return_pct'],'return_delta_pp':z['net_return_pct']-a['net_return_pct'],'DD_delta_pp':z['max_drawdown_pct']-a['max_drawdown_pct'],'recent40_return_delta_pp':z['recent40']['net_return_pct']-a['recent40']['net_return_pct'],'execution_delta':z['executions']-a['executions'],'cost_delta_usdt':z['cost_usdt']-a['cost_usdt'],'new_NAV_sha256':z['NAV_sha256_f64le'],'reference_NAV_sha256':a['NAV_sha256_f64le'],'cash_analytic_return_pct':0,'limit':'Samebank/N/slow/H/fixedBTC,differentETHspeed/realizedrisk' if kind=='same_bank_fast3' else 'Samebank/N constantlongreference,different native signals/exposure/risk'})
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
    mat=np.array([[(by[S,L]['scenes']['3']['recent40'] if rr else by[S,L]['scenes']['3'])[field] for L in LOOKS] for S in SLOWS],dtype=float);im=axs[i,j].imshow(mat,cmap='RdYlGn_r' if field=='max_drawdown_pct' else 'RdYlGn',vmin=0 if field=='max_drawdown_pct' else -limit,vmax=limit);axs[i,j].set_title(('Inherited40days' if rr else '370days')+' / 3x '+field);axs[i,j].set_xticks(range(3),LOOKS);axs[i,j].set_yticks(range(2),SLOWS);axs[i,j].set_xlabel('ETH reversal lookback L(days)');axs[i,j].set_ylabel('ETH slow gate S(days)')
    for x,y in itertools.product(range(2),range(3)):axs[i,j].text(y,x,('n/a' if np.isnan(mat[x,y]) else f'{mat[x,y]:+.3f}')+('*' if by[SLOWS[x],LOOKS[y]].get('read_only_anchor') else ''),ha='center',va='center')
    fig.colorbar(im,ax=axs[i,j])
  fig.suptitle(scope+' / '+('ETH 10000bank,N3000' if scope=='native' else 'BTC1000+ETH3000 entrybudgets,two10000banks raw1/1')+'\nH2%/ETHzeroexit; *old actual L3 cells;knownhistory');fig.savefig(R/f'sensitivity_{scope}.png',dpi=120);plt.close(fig)
 for field in ['sharpe3_delta']:
  vals=[abs(e[field]) for e in edges if e[field] is not None];cut=2*statistics.pstdev(vals) if vals else None
  for e in edges:e['full_sharpe_cliff']=e[field] is not None and abs(e[field])>cut;e['cliff_threshold']=cut
 counts={'cost':len(rows),'full_folds':len(folds),'recent40_folds':len(recent),'daily_NAV':len(daily),'edges':len(edges),'reference_comparisons':len(comp)};assert list(counts.values())==[42,546,336,8904,14,48]
 for name,data,zipit in [('sensitivity.csv',rows,False),('fold_results.csv',folds,False),('recent40_fold_results.csv',recent,False),('daily_equity.csv.gz',daily,True),('joint_edges.csv',edges,False),('reference_comparisons.csv',comp,False)]:table(R/name,data,zipit)
 r['joint_grid_sensitivity']={'dimension_count':2,'native_ETH_cells':6,'parent_cells':6,'new_cells':8,'readonly_old_cells':4,'old_hold_controls':2,'adjacent_edges':14,'cells':cells,'old_qualification_unchanged':True,'cliff_definition':'Descriptive absSharpe adjacentdelta >2populationSDof finiteabsdeltas;no oldrerating.'};put(R/'report.json',r)
 cs=list(r['configs'].values());summary={'new_financial_configs':8,'new_native_components':4,'new_passive_parents':4,'passed_candidates':len(r['summary']['passed']),'rejected_candidates':len(r['summary']['rejected']),'positive_configs_by_cost':r['summary']['positive_configs_by_cost'],'failed_criteria_counts':dict(Counter(p for c in cs for p in c['failed_criteria'])),'by_scope':{s:{'new':sum(c['scope']==s for c in cs),'passed':sum(c['scope']==s and c['status']=='passed' for c in cs),'best_full3':max(({'name':c['name'],'return3_pct':c['scenes']['3']['net_return_pct'],'whole_DD3_pct':c['scenes']['3']['max_drawdown_pct'],'recent_return3_pct':c['scenes']['3']['recent40']['net_return_pct'],'positive_months1':c['positive_complete_30d_folds_1x'],'positive_recent1':c['recent40_positive_5d_folds_1x'],'failed_criteria':c['failed_criteria']} for c in cs if c['scope']==s),key=lambda x:x['return3_pct'])} for s in ['native','parent']},'rows':counts};put(R/'summary.json',summary)
 ctx=json.loads((R/'context.json').read_text());lines=[f'# {R.name} 较长ETH反转周期验证',f'实际测试4个ETH原生策略＋4个组合，共8配置/24成本场景，历史通过{summary["passed_candidates"]}、淘汰{summary["rejected_candidates"]}。全文读取{ctx["registry_events"]}事件/{ctx["registry_ids"]}ID及{len(ctx["prior_conclusions_read"])}份结论；初始16项均有实际历史证据。',
 '本轮事前固定ETH慢28/31日×反转3/4/5日，阈值2%、零交叉退出、原生银行10000、固定入场3000；BTC固定ROC31/H4%/退出1%、银行10000、入场1000。快3日旧2原生＋2组合只读，快4/5日4原生＋4组合逐项先reserve才计算。原值1/1为两整个10000银行、组合本金20000；入场合计4000=初始本金20%，不归一化、不复利调仓、不转账/交叉保证金/再平衡。',
 'ETH此前完整L日ROC严格>2%反转空/<-2%反转多，带内多仅ROC<0、空仅ROC>0保留，零退出；慢ROC S正仅许多、负仅许空，零/不兼容即平仓，现金重入须新极端，无隐藏desired。UTC00:01真实OPEN执行，q=floor(N/此前完整close/lot)，先平后反开，不用未来OPEN/资金费/未闭合价格产生信号或手数。研究引擎仅放宽允许L到4/5，原信号/订单/费用/资金费/风险/指标函数其余字节保持；原冻结未来观察器代码未改。',
 '父组合仅将固定BTC已有真实净值与新ETH净值按共同(ns,eventcode)时序承接上一完成点后逐点相加，不平均收益/Sharpe；原生N3000重新实际撮合，未缩放旧净值。4个旧原生/12成本NAV源SHA校对，旧ETH3日与同N恒多逐档比较，现金0为解析对照。原资格不因新邻域重评级。',
 '真实8合并Parquet及16年度/近期源SHA固定；370日连续OOS2025-10-19UTC00:01..2026-10-24UTC00:01，33日上下文/3日初始embargo。静态规则无拟合/未来标签，purge不适用。12完整30日折＋10日尾折carry原现金/仓位/entry/费用，近期40日继承day330状态并分8×5日，不重置或诊断平仓；只有预定Oct24终点费用平仓。该历史反复研究，仅作开发验证，不称最终未触碰留出或独立新市场证据。',
 '每侧5bp费＋1bp半价差＋2bp滑点＋0.5×此前20日日log波动×sqrt(成交金额/此前20日ADV)冲击，参与率≤0.1%，真实不利tick/lot/最小金额、完全抵押入场限制；实际资金费=-q×结算mark×rate，流出乘1/2/3，流入不放大。永续无虚构现货借币。无L2/TCA/完整历史阶梯与tick清算，1%小时不利mark维持保证金仅代理。',
 '资格未放宽：全期/近期三档净正，1倍月正折≥9/12且近期≥6/8，3倍整体DD≤25%，二维相邻索引含自身净正率≥60%，≥4往返、(参考毛利＋资金费)/费用≥2.5，现金/拒单/风险代理违规0、终点空仓。两作用域分别6格、7边；全部净收益、整体回撤、Sharpe/Calmar、陡变/边界及逐折留档，2图12面板。',
 '计算前复核发现4个旧组合草案的周期说明/源规则哈希不一致，原样保留并finish abandoned/result_available=false；4原生定义有效未改。修正完整组合定义、再次reserve及预检后才计算，金融结果未重跑。具体注册与恢复回执均保留。',
 '结果：'+json.dumps(summary,ensure_ascii=False),
 '原H4/ETH3日冻结候选只续接至Oct27UTC08:30，跨实际08:00资金费，保持真实现金/数量/entry/风险段和完整净值链；旧SMA同样续接无强制平仓。两者是延迟闭合行情/资金费重建，不是paper10实时报价账户；paper10冻结账本只读。部分观察rejected不取消180日计划，短窗年化/盈利不解释为长期资格。',
 '一手背景复用此前2026-10-27实际访问的[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)（2012-05-01）与[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)（2012-12-05）。传统期货/股票背景到加密4/5日规则为推论，非论文复现或利润/容量移植。新8相关配置承受多重选择，未证明DSR/PBO或稳定实盘盈利。',
 '复现工作目录/home/desktop/Documents/Codex/EquiTide；audit.py/audit_native.py、check_sources.py、check_definitions.py、audit_candidate.py、forward.py --reproduce/audit_forward.py只读保存的真实结果，不重新reserve/evaluate/summarize已完成配置。main普通非强推、freshfetch/独立allheads/完整tree/blob核验后释放自己锁；不建分支/任务、重部署或真实下单。'];(R/'result.md').write_text('\n\n'.join(lines)+'\n');print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
