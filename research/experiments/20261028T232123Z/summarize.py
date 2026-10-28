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
def all_configs(report,plan):
 out=grid_configs(report['configs'])
 for ref in plan['read_only_hold_references'].values():
  c=copy.deepcopy(json.loads((ROOT/ref['report']).read_text())['configs'][ref['name']]);c.update(read_only_anchor=True,scope=ref['scope'],asset=ref['asset'],capital_usdt=ref['capital_usdt'])
  for z in c['scenes'].values():
   if 'recent40' not in z:z['recent40']=copy.deepcopy(z['extension40'])
  out[c['name']]=c
 return out
def main():
 assert not(R/'finish_verification.json').exists();r=json.loads((R/'report.json').read_text());grid=grid_configs(r['configs']);assert len(grid)==72;holds={};docs={}
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
   dims=list(axes(c));H,S,L=[c[d] for d in dims];baseline=next(x for x in grid.values() if x['scope']==c['scope'] and x[dims[0]]==H and x[dims[1]]==S and x[dims[2]]==(3 if L==2 else 4))
   for kind,y in [('matched_old_L3or4',baseline),('same_bank_constant_long',holds[c['asset']])]:
    a=y['scenes'][k];assert y['capital_usdt']==c['capital_usdt'];comp.append({**meta,'cost_multiplier':int(k),'reference_kind':kind,'reference_name':y['name'],'reference_fingerprint':y['fingerprint'],'reference_original_status':y['status'],'new_return_pct':z['net_return_pct'],'reference_return_pct':a['net_return_pct'],'return_delta_pp':z['net_return_pct']-a['net_return_pct'],'DD_delta_pp':z['max_drawdown_pct']-a['max_drawdown_pct'],'recent40_return_delta_pp':z['recent40']['net_return_pct']-a['recent40']['net_return_pct'],'execution_delta':z['executions']-a['executions'],'cost_delta_usdt':z['cost_usdt']-a['cost_usdt'],'new_NAV_sha256':z['NAV_sha256_f64le'],'reference_NAV_sha256':a['NAV_sha256_f64le'],'cash_analytic_return_pct':0,'limit':'Samebank/N/H/S/fixedBTC,oldL3fornewL2oroldL4fornewL5;differenttiming/exposure/risk' if kind=='matched_old_L3or4' else 'Samebank/N constantlongreference,different native signals/exposure/risk'})
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
   fig.suptitle(scope+' / '+('ETH10000bank,N3000' if scope=='native' else 'BTC1000+ETH3000 entrybudgets,two10000banks raw1/1')+f'\nETH H{H*100:g}%/zeroexit; *oldL3/4majoritycells;knownhistory');fig.savefig(R/f'sensitivity_{scope}_H{int(round(H*1000)):03d}.png',dpi=120);plt.close(fig)
 for field in ['sharpe3_delta']:
  vals=[abs(e[field]) for e in edges if e[field] is not None];cut=2*statistics.pstdev(vals) if vals else None
  for e in edges:e['full_sharpe_cliff']=e[field] is not None and abs(e[field])>cut;e['cliff_threshold']=cut
 counts={'cost':len(rows),'full_folds':len(folds),'recent40_folds':len(recent),'daily_NAV':len(daily),'edges':len(edges),'reference_comparisons':len(comp)};assert list(counts.values())==[222,2886,1776,40068,150,216]
 for name,data,zipit in [('sensitivity.csv',rows,False),('fold_results.csv',folds,False),('recent40_fold_results.csv',recent,False),('daily_equity.csv.gz',daily,True),('joint_edges.csv',edges,False),('reference_comparisons.csv',comp,False)]:table(R/name,data,zipit)
 joint={'dimension_count':3,'native_ETH_cells':36,'parent_cells':36,'new_cells':36,'readonly_old_cells':36,'old_hold_controls':2,'adjacent_edges':150,'cells':cells,'old_qualification_unchanged':True,'cliff_definition':'Descriptive absSharpe adjacentdelta >2populationSDof finiteabsdeltas;no oldrerating.'};put(R/'joint_grid_sensitivity.json',joint)
 cs=list(r['configs'].values());summary={'new_financial_configs':36,'new_native_components':18,'new_passive_parents':18,'passed_candidates':len(r['summary']['passed']),'rejected_candidates':len(r['summary']['rejected']),'positive_configs_by_cost':r['summary']['positive_configs_by_cost'],'failed_criteria_counts':dict(Counter(p for c in cs for p in c['failed_criteria'])),'by_scope':{s:{'new':sum(c['scope']==s for c in cs),'passed':sum(c['scope']==s and c['status']=='passed' for c in cs),'best_full3':max(({'name':c['name'],'return3_pct':c['scenes']['3']['net_return_pct'],'whole_DD3_pct':c['scenes']['3']['max_drawdown_pct'],'recent_return3_pct':c['scenes']['3']['recent40']['net_return_pct'],'positive_months1':c['positive_complete_30d_folds_1x'],'positive_recent1':c['recent40_positive_5d_folds_1x'],'failed_criteria':c['failed_criteria']} for c in cs if c['scope']==s),key=lambda x:x['return3_pct'])} for s in ['native','parent']},'rows':counts};put(R/'summary.json',summary)
 ctx=json.loads((R/'context.json').read_text());lines=[f'# {R.name} ETH多数门控快周期边界验证',f'实际18新ETH原生＋18新BTC/ETH组合，共36配置/108成本场景；历史通过{summary["passed_candidates"]}、淘汰{summary["rejected_candidates"]}。完整读取{ctx["registry_events"]}事件/{ctx["registry_ids"]}ID及{len(ctx["prior_conclusions_read"])}份结论；初始16项均已有实际证据。','事前补测L2/5 × H2/2.5/3% × S27/28/29，每作用域36格含18个旧L3/4只读真实邻居。新18原生＋18父组合逐个先reserve再计算，原旧资格保持、不按扩展邻域重评级。假设是邻近快周期能否拓宽近期正折表现；不因本轮结果放宽固定门槛。','ETH快ROC严格>H反转空/<-H反转多；带内只保留ROC<0的实际多、ROC>0的实际空，零退出；慢门控S-1/S/S+1至少两票严格正允许多、至少两票严格负允许空，否则平仓。快方向须与慢多数一致；现金重新入场需新严格极端，无隐藏desired。下一UTC00:01真实OPEN执行，q=floor(N/此前完整close/lot)*lot，不读未来OPEN/资金费/未闭合数据。引擎仅将允许快周期3/4扩至2/3/4/5，其他代码字节保持；360项合成信号边界/持仓状态/未来不变性检查通过。','ETH独立10000银行、固定N3000；BTC旧ROC31/H4/退出1%、10000银行固定N1000。原值[1,1]持有完整两银行，父本金20000、入场预算4000=20%，不归一化/NAV缩放/转账/交叉保证金/再平衡。21旧原生/63成本NAV从真实已保存账本恢复核对原SHA，18新原生实际计算专属成交/资金费/成本/风险；18父组合因果对齐完整纳秒事件时轴相加，指标从整体净值重算。','8真实合并Parquet和16年度/近期源SHA固定。370日OOS2025-10-19UTC00:01至2026-10-24UTC00:01；33日上下文含30预热、3日初始embargo。静态规则不拟合、无未来标签，purge不适用；12完整30日折加10日尾折连续承接现金/q/entry/费用，近期40由day330继承分8×5日，不重开本金或诊断平仓，仅原终点计费退出。反复使用历史属于开发验证，非未触碰最终测试。','每侧5bp费＋1bp半价差＋2bp滑点＋0.5×滞后20日日log波动×sqrt(实际native成交金额/滞后20日quoteADV)冲击，参与率≤0.1%，tick/lot/最小金额/100%抵押入场约束。资金费=-有符号q×实际mark×rate，流出乘成本1/2/3、收入不放大；永续无虚构现货借币。独立银行闭合小时1%维持保证金代理，不代表历史完整tier/tick清算或L2/TCA容量证明。','固定门槛：全期/近期三成本净正、1x月正折≥9/12及近期≥6/8、3x完整连续整体DD≤25%、三维相邻索引半径1含自身全期3x净正≥60%、≥4往返、(参考毛利＋资金费)/成本≥2.5、现金/拒单/风险违规0、终点空仓且≥180日。旧L3/L4邻居只读；新L2对旧L3、新L5对旧L4，匹配H/S/本金/原生N；另对照同本金恒多及现金0。',json.dumps(summary,ensure_ascii=False),'原单S28冻结候选与SMA65从UTC20:30续接至22:30，保留现金/数量/entry/成本/资金费/完整净值前缀，零新增日决策/资金费/成交；21close检查旧20小时风险状态、22close检查21小时。下一窗口00:30跨Oct29UTC00:00资金费及00:01日决策，必须用实际结算和更新后的原始34/65日日线上下文，不能继续markonly跨越。延迟闭合数据重建与paper10十策略实时报价观察分开。','背景沿用2026-10-27实际访问的一手[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)及[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)。新快周期假设为研究推论。36个相关新试验及全部既往试验存在多重选择偏差，无DSR/PBO、独立未来资格或稳定实盘盈利证明。','复现工作目录/home/desktop/Documents/Codex/EquiTide。audit.py/audit_native.py独立整数信号/Decimal成交资金费/风险及逐点NAV，check_sources.py/check_exports.py/check_feed.py只读验证；原账户audit_candidate.py/audit_forward.py及forward.py --reproduce只读复现。不得重reserve/evaluate已完成精确配置。全部正负结果保存，行情/HTTPpacket留ignoreddata绑定SHA；main非强推并核验完整远端tree/blob/行情后释放本轮锁。'];(R/'result.md').write_text('\n\n'.join(lines)+'\n');print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
