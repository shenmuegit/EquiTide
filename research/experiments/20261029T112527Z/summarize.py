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
 assert not(R/'finish_verification.json').exists();r=json.loads((R/'report.json').read_text());grid=grid_configs(r['configs']);assert len(grid)==48;holds={};docs={}
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
   dims=list(axes(c));H,S,L=[c[d] for d in dims];baseline=next(x for x in grid.values() if x['scope']==c['scope'] and x[dims[0]]==0 and x[dims[1]]==S and x[dims[2]]==L)
   for kind,y in [('matched_old_E0',baseline),('same_bank_constant_long',holds[c['asset']])]:
    a=y['scenes'][k];assert y['capital_usdt']==c['capital_usdt'];comp.append({**meta,'cost_multiplier':int(k),'reference_kind':kind,'reference_name':y['name'],'reference_fingerprint':y['fingerprint'],'reference_original_status':y['status'],'new_return_pct':z['net_return_pct'],'reference_return_pct':a['net_return_pct'],'return_delta_pp':z['net_return_pct']-a['net_return_pct'],'DD_delta_pp':z['max_drawdown_pct']-a['max_drawdown_pct'],'recent40_return_delta_pp':z['recent40']['net_return_pct']-a['recent40']['net_return_pct'],'execution_delta':z['executions']-a['executions'],'cost_delta_usdt':z['cost_usdt']-a['cost_usdt'],'new_NAV_sha256':z['NAV_sha256_f64le'],'reference_NAV_sha256':a['NAV_sha256_f64le'],'cash_analytic_return_pct':0,'limit':'Samebank/N/fastH2.5/S/L/fixedBTC,oldE0versusnewfastExitE;differentgate/exposure/risk' if kind=='matched_old_E0' else 'Samebank/N constantlongreference,different native signals/exposure/risk'})
 for scope in ['native','parent']:
  subset=[c for c in grid.values() if c['scope']==scope];dims=axes(subset[0]);fields=list(dims);by={tuple(c[p] for p in fields):c for c in subset};assert set(by)==set(itertools.product(*dims.values()))
  for key,c in by.items():
   for i,(field,axis) in enumerate(dims.items()):
    j=axis.index(key[i])
    if j+1==len(axis):continue
    other=list(key);other[i]=axis[j+1];y=by[tuple(other)];a,b=c['scenes']['3'],y['scenes']['3'];edges.append({'scope':scope,'axis':field,'from':c['name'],'to':y['name'],'return3_delta_pp':b['net_return_pct']-a['net_return_pct'],'DD3_delta_pp':b['max_drawdown_pct']-a['max_drawdown_pct'],'sharpe3_delta':b['sharpe_365']-a['sharpe_365'] if a['sharpe_365'] is not None and b['sharpe_365'] is not None else None,'recent40_return3_delta_pp':b['recent40']['net_return_pct']-a['recent40']['net_return_pct']})
  for H in HURDLES[1:]:
   facet=[c for c in subset if c[fields[0]]==H];fig,axs=plt.subplots(3,2,figsize=(12,10),layout='constrained')
   for i,field in enumerate(['net_return_pct','sharpe_365','max_drawdown_pct']):
    values=[(c['scenes']['3']['recent40'] if rr else c['scenes']['3'])[field] for c in facet for rr in [False,True]];limit=max([abs(x) for x in values if x is not None] or [1]) or 1
    for j,rr in enumerate([False,True]):
     mat=np.array([[(by[H,S,L]['scenes']['3']['recent40'] if rr else by[H,S,L]['scenes']['3'])[field] for L in LOOKS] for S in SLOWS],dtype=float);im=axs[i,j].imshow(mat,aspect='auto',cmap='RdYlGn_r' if field=='max_drawdown_pct' else 'RdYlGn',vmin=0 if field=='max_drawdown_pct' else -limit,vmax=limit);axs[i,j].set_title(('Inherited40days' if rr else '370days')+' /3x '+field);axs[i,j].set_xticks(range(len(LOOKS)),LOOKS);axs[i,j].set_yticks(range(len(SLOWS)),SLOWS);axs[i,j].set_xlabel('ETH reversal lookback L(days)');axs[i,j].set_ylabel('ETH slow gate S(days)')
     for x,y in itertools.product(range(len(SLOWS)),range(len(LOOKS))):axs[i,j].text(y,x,('n/a' if np.isnan(mat[x,y]) else f'{mat[x,y]:+.3f}')+('*' if by[H,SLOWS[x],LOOKS[y]].get('read_only_anchor') else ''),ha='center',va='center',fontsize=10)
     fig.colorbar(im,ax=axs[i,j])
   fig.suptitle(scope+' / '+('ETH10000bank,N3000' if scope=='native' else 'BTC1000+ETH3000 entrybudgets,two10000banks raw1/1')+f'\nETH exit E{H*100:g}%/entryH2.5%/entry-only slow gate;reused history');fig.savefig(R/f'sensitivity_{scope}_H{int(round(H*1000)):03d}.png',dpi=120);plt.close(fig)
 for field in ['sharpe3_delta']:
  vals=[abs(e[field]) for e in edges if e[field] is not None];cut=2*statistics.pstdev(vals) if vals else None
  for e in edges:e['full_sharpe_cliff']=e[field] is not None and abs(e[field])>cut;e['cliff_threshold']=cut
 counts={'cost':len(rows),'full_folds':len(folds),'recent40_folds':len(recent),'daily_NAV':len(daily),'edges':len(edges),'reference_comparisons':len(comp)};assert list(counts.values())==[150,1950,1200,40068,92,216]
 for name,data,zipit in [('sensitivity.csv',rows,False),('fold_results.csv',folds,False),('recent40_fold_results.csv',recent,False),('daily_equity.csv.gz',daily,True),('joint_edges.csv',edges,False),('reference_comparisons.csv',comp,False)]:table(R/name,data,zipit)
 joint={'dimension_count':3,'native_ETH_cells':24,'parent_cells':24,'new_cells':36,'readonly_old_cells':12,'old_hold_controls':2,'adjacent_edges':92,'cells':cells,'old_qualification_unchanged':True,'cliff_definition':'Descriptive absSharpe adjacentdelta >2populationSDof finiteabsdeltas;no oldrerating.'};put(R/'joint_grid_sensitivity.json',joint)
 cs=list(r['configs'].values());summary={'new_financial_configs':36,'new_native_components':18,'new_passive_parents':18,'passed_candidates':len(r['summary']['passed']),'rejected_candidates':len(r['summary']['rejected']),'positive_configs_by_cost':r['summary']['positive_configs_by_cost'],'failed_criteria_counts':dict(Counter(p for c in cs for p in c['failed_criteria'])),'by_scope':{s:{'new':sum(c['scope']==s for c in cs),'passed':sum(c['scope']==s and c['status']=='passed' for c in cs),'best_full3':max(({'name':c['name'],'return3_pct':c['scenes']['3']['net_return_pct'],'whole_DD3_pct':c['scenes']['3']['max_drawdown_pct'],'recent_return3_pct':c['scenes']['3']['recent40']['net_return_pct'],'positive_months1':c['positive_complete_30d_folds_1x'],'positive_recent1':c['recent40_positive_5d_folds_1x'],'failed_criteria':c['failed_criteria']} for c in cs if c['scope']==s),key=lambda x:x['return3_pct'])} for s in ['native','parent']},'rows':counts};put(R/'summary.json',summary)
 ctx=json.loads((R/'context.json').read_text());lines=[f'# {R.name} 仅入场门控下的快ROC退出缓冲',f'实际18新ETH原生＋18固定BTC/ETH组合，共36配置/108成本场景；历史通过{summary["passed_candidates"]}、淘汰{summary["rejected_candidates"]}。完整读取{ctx["registry_events"]}事件/{ctx["registry_ids"]}ID和{len(ctx["prior_conclusions_read"])}份结论；初始16项均有实际证据。',json.loads((R/'plan.json').read_text())['hypothesis'],'事前固定E0.5/1/1.5% × S27/28/29 × L3/4，严格入场H2.5%固定，E<H。快ROC>H提议空、<-H提议多；否则已有多仓仅在ROC<E时保留，已有空仓仅在ROC>−E时保留，边界相等退出。E是快ROC越零后的退出阈值，不是按入场盈亏计算的止损。现金新入场仍需新的严格极端；慢多数S−1/S/S+1只约束现金/反向开仓，已有快方向一致持仓忽略慢票变化；无隐藏desired。','ETH独立10000银行固定N3000；BTC旧ROC31/H4/退出1%固定N1000、10000银行。原值[1,1]持有两整银行，父本金20000、入场预算4000=20%；不归一化/NAV缩放/转账/交叉保证金/再平衡。9旧原生/27成本NAV只从实际保存账本回放核对原SHA，不重跑源模型；18个新ETH原生实际计算自己的成交、资金费、成本与风险。18个父组合对齐因果纳秒/事件并集逐点相加，整体/逐折指标由完整净值重算，不平均Sharpe或收益率。','完整三维24格每作用域含6个旧E0真实数字邻居，合计92相邻边；旧12个结果保持原资格。匹配同H/S/L/N/仅入场门控的E0、同本金恒多及现金0对照。source E0 spec的persistence说明沿用了更早base文案；保留原字节，以原明确entries_only参数、实际执行代码及独立核验的实际决策绑定行为。新spec完整修正文案，E0全部旧行为回归通过；见spec_binding_review.json，历史未改写。','8真实合并Parquet及16年度/近期源SHA/字节固定。370日OOS2025-10-19UTC00:01至2026-10-24UTC00:01；33日上下文含30预热及3日初始embargo。静态规则不拟合，无未来标签，purge不适用；12完整30日折加10日尾折连续承接现金/数量/entry/成本/资金费。近期40从day330继承分8×5日，不重开本金或诊断平仓；仅原终点计费退出。重复历史属于开发验证，非未触碰最终测试。','每侧5bp费＋1bp半价差＋2bp滑点＋0.5×滞后20日日log波动×sqrt(实际原生成交金额/滞后20日quoteADV)冲击，参与率≤0.1%，不利tick/lot/最小金额/全额抵押约束。资金费=−有符号q×实际结算mark×rate，流出按1/2/3成本放大、收入不放大；永续不虚构现货借币。独立银行闭合小时不利mark和1%维持保证金为风险代理，缺L2/TCA/完整历史tier/tick清算/聚合容量证明。','固定门槛：全期/近期三档净正、1x月正折≥9/12及近期≥6/8、3x完整连续OOS整体DD≤25%、同作用域三维相邻索引半径1含自身全期3x净正≥60%、≥4往返、(参考毛利＋资金费)/成本≥2.5、现金/拒单/风险违规0、终点空仓及≥180日。资格未放宽。',json.dumps(summary,ensure_ascii=False),'合成测试先RED后GREEN：9360组严格边界、持仓状态、未来不变性和4680项旧E0行为回归。新引擎只修改majority_target，simulate及数据、数量、成本、资金费、风险函数字节不变。独立整数信号/Decimal成交资金费/风险、每个NAV点及整体/逐折指标均实际核验。','原冻结单S28候选及SMA65从UTC08:30续接至10:30，只增加已闭合mark，不重计08资金费、不换本轮E缓冲策略。BTC08小时前后风险状态同一精确08:00时间戳，前状态零时长，09close应排除零时长前缀并核验后状态；09小时在10close核验。保留完整现金/数量/entry/费用/NAV前缀、35日候选/65日SMA上下文和3个候选日NAV边界。下一资金费16UTC、下一日决策Oct30UTC00:01。两类延迟shadow与paper10十策略实时报价观察分开。','研究背景为一手[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)与[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)。本轮退出缓冲假设为研究推论，非原论文复现。36个相关新试验及全部历史存在多重选择偏差，无DSR/PBO、独立未来资格或稳定实盘盈利证明。','复现目录/home/desktop/Documents/Codex/EquiTide。audit.py/audit_native.py独立核验真实原生成交、资金费、风险及组合逐点净值；check_sources.py/check_exports.py/check_feed.py只读核验；audit_candidate.py/audit_forward.py及forward.py --reproduce复现原账户。已完成精确配置不得重新reserve/evaluate。全部正负结果和完整账户账本/冻结规则/登记/失败保留；行情及原始HTTPpacket留ignoreddata并绑定SHA。仅main普通非强推，完整远端tree/blob/数据核验及发布实际exit0后释放自己锁。'];(R/'result.md').write_text('\n\n'.join(lines)+'\n');print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
