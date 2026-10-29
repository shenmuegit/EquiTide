"""Export saved native/parent threshold surfaces, costs, folds and paired old-H2 controls."""
import copy,csv,gzip,io,itertools,json,statistics
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run import ROOT,R,HURDLES,SLOWS,LOOKS,axes,grid_configs,anchor_configs,sha,put

def table(path,rows,compress=False):
 fields=list(dict.fromkeys(k for row in rows for k in row));b=io.StringIO(newline='');w=csv.DictWriter(b,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows);path.write_bytes(gzip.compress(b.getvalue().encode(),mtime=0) if compress else b.getvalue().encode())
def all_configs(report,plan):
 out={**anchor_configs(),**report['configs']}
 for ref in plan['read_only_hold_references'].values():
  c=copy.deepcopy(json.loads((ROOT/ref['report']).read_text())['configs'][ref['name']]);c.update(read_only_anchor=True,scope=ref['scope'],asset=ref['asset'],capital_usdt=ref['capital_usdt'])
  for z in c['scenes'].values():
   if 'recent40' not in z:z['recent40']=copy.deepcopy(z['extension40'])
  out[c['name']]=c
 return out
def main():
 assert not(R/'finish_verification.json').exists();r=json.loads((R/'report.json').read_text());grid=grid_configs(r['configs']);assert len(grid)==36;holds={};docs={}
 for key,ref in json.loads((R/'holds.json').read_text()).items():
  assert sha(ROOT/ref['report'])==ref['report_sha256']
  if ref['report'] not in docs:docs[ref['report']]=json.loads((ROOT/ref['report']).read_text())
  c=copy.deepcopy(docs[ref['report']]['configs'][ref['name']]);c.update(read_only_anchor=True,scope=ref['scope'],asset=ref['asset'],capital_usdt=ref['capital_usdt'])
  for z in c['scenes'].values():
   if 'recent40' not in z:z['recent40']=copy.deepcopy(z['extension40'])
  holds[key]=c
 allby={**anchor_configs(),**grid,**{x['name']:x for x in holds.values()}};rows=[];folds=[];recent=[];daily=[];comp=[];edges=[];cells={}
 for c in allby.values():
  old=c.get('read_only_anchor',False);meta={'name':c['name'],'scope':c['scope'],'asset':c['asset'],'role':c['role'],'read_only_anchor':old,'capital_usdt':c['capital_usdt']}
  if c['role']=='candidate':meta.update({p:c[p] for p in axes(c)})
  cells[c['name']]={**meta,'fingerprint':c['fingerprint'],'original_or_new_status':c['status'],'scenes':{k:{p:z[p] for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','NAV_sha256_f64le']} for k,z in c['scenes'].items()}}
  for k,z in c['scenes'].items():
   rows.append({**meta,'cost_multiplier':int(k),'status':c['status'],**{p:z[p] for p in ['net_return_pct','max_drawdown_pct','daily_mark_drawdown_pct','sharpe_365','calmar','cost_usdt','cost_pct_initial','funding_usdt','gross_reference_PnL_to_execution_cost','executions','round_trips','NAV_sha256_f64le']},**{'recent40_'+p:z['recent40'][p] for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','NAV_sha256_f64le']},**{'cost_'+p:v for p,v in z['cost_parts_usdt'].items()}});folds.extend({**meta,'cost_multiplier':int(k),**f} for f in z['folds']);recent.extend({**meta,'cost_multiplier':int(k),**f} for f in z['recent40']['folds'])
   if old:continue
   daily.extend({**meta,'cost_multiplier':int(k),'boundary_index':j,'equity_usdt':v} for j,v in enumerate(z['daily_equity_usdt']))
   dims=list(axes(c));H,S,L=[c[d] for d in dims];baseline=allby[c['matched_reference']]
   for kind,y in [('matched_old_full_gate',baseline),('same_bank_constant_long',holds[c['asset']])]:
    a=y['scenes'][k];assert y['capital_usdt']==c['capital_usdt'];comp.append({**meta,'cost_multiplier':int(k),'reference_kind':kind,'reference_name':y['name'],'reference_fingerprint':y['fingerprint'],'reference_original_status':y['status'],'new_return_pct':z['net_return_pct'],'reference_return_pct':a['net_return_pct'],'return_delta_pp':z['net_return_pct']-a['net_return_pct'],'DD_delta_pp':z['max_drawdown_pct']-a['max_drawdown_pct'],'recent40_return_delta_pp':z['recent40']['net_return_pct']-a['recent40']['net_return_pct'],'execution_delta':z['executions']-a['executions'],'cost_delta_usdt':z['cost_usdt']-a['cost_usdt'],'new_NAV_sha256':z['NAV_sha256_f64le'],'reference_NAV_sha256':a['NAV_sha256_f64le'],'cash_analytic_return_pct':0,'limit':'Samebank/N/H/S/L/fixedBTC;only slow gate application differs;actual timing/exposure/risk differ' if kind=='matched_old_full_gate' else 'Samebank/N constantlongreference,different native signals/exposure/risk'})
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
   fig.suptitle(scope+' / '+('ETH10000bank,N3000' if scope=='native' else 'BTC1000+ETH3000 entrybudgets,two10000banks raw1/1')+f'\nETH H{H*100:g}%/zeroexit; entry-only slow gate; reused history');fig.savefig(R/f'sensitivity_{scope}_H{int(round(H*1000)):03d}.png',dpi=120);plt.close(fig)
 for field in ['sharpe3_delta']:
  vals=[abs(e[field]) for e in edges if e[field] is not None];cut=2*statistics.pstdev(vals) if vals else None
  for e in edges:e['full_sharpe_cliff']=e[field] is not None and abs(e[field])>cut;e['cliff_threshold']=cut
 counts={'cost':len(rows),'full_folds':len(folds),'recent40_folds':len(recent),'daily_NAV':len(daily),'edges':len(edges),'reference_comparisons':len(comp)};assert list(counts.values())==[222,2886,1776,40068,66,216]
 for name,data,zipit in [('sensitivity.csv',rows,False),('fold_results.csv',folds,False),('recent40_fold_results.csv',recent,False),('daily_equity.csv.gz',daily,True),('joint_edges.csv',edges,False),('reference_comparisons.csv',comp,False)]:table(R/name,data,zipit)
 joint={'dimension_count':3,'native_ETH_cells':18,'parent_cells':18,'new_cells':36,'readonly_old_cells':36,'old_hold_controls':2,'adjacent_edges':66,'cells':cells,'old_qualification_unchanged':True,'cliff_definition':'Descriptive absSharpe adjacentdelta >2populationSDof finiteabsdeltas;no oldrerating.'};put(R/'joint_grid_sensitivity.json',joint)
 cs=list(r['configs'].values());summary={'new_financial_configs':36,'new_native_components':18,'new_passive_parents':18,'passed_candidates':len(r['summary']['passed']),'rejected_candidates':len(r['summary']['rejected']),'positive_configs_by_cost':r['summary']['positive_configs_by_cost'],'failed_criteria_counts':dict(Counter(p for c in cs for p in c['failed_criteria'])),'by_scope':{s:{'new':sum(c['scope']==s for c in cs),'passed':sum(c['scope']==s and c['status']=='passed' for c in cs),'best_full3':max(({'name':c['name'],'return3_pct':c['scenes']['3']['net_return_pct'],'whole_DD3_pct':c['scenes']['3']['max_drawdown_pct'],'recent_return3_pct':c['scenes']['3']['recent40']['net_return_pct'],'positive_months1':c['positive_complete_30d_folds_1x'],'positive_recent1':c['recent40_positive_5d_folds_1x'],'failed_criteria':c['failed_criteria']} for c in cs if c['scope']==s),key=lambda x:x['return3_pct'])} for s in ['native','parent']},'rows':counts};put(R/'summary.json',summary)
 ctx=json.loads((R/'context.json').read_text());lines=[f'# {R.name} 慢多数门控仅约束入场',f'实际18个ETH原生＋18个固定BTC/ETH组合，共36配置、108成本场景；历史通过{summary["passed_candidates"]}、淘汰{summary["rejected_candidates"]}。读取{ctx["registry_events"]}事件/{ctx["registry_ids"]}ID及{len(ctx["prior_conclusions_read"])}份既往结论，初始16项已有实际证据。','事前固定H2/2.5/3% × S27/28/29 × L3/4，18格每作用域；新规则只对现金新开或反向开仓检查S−1/S/S+1至少两票同号慢ROC。已有实际持仓只要快ROC仍支持同方向即保留，不因慢票变化平仓。快ROC零/反向仍退出；现金重新入场仍需新严格极端，无隐藏desired。旧相同H/S/L的完整慢门控36个结果只读作对照，不混入新参数邻域，不重新评级。','ETH独立10000银行固定N3000；BTC旧ROC31/H4/退出1%固定N1000、10000银行。组合原值[1,1]持有两整银行，本金20000、入场预算4000=20%；不归一化、净值缩放、转账、交叉保证金或再平衡。21个旧原生/63条成本曲线从真实已保存账本回放并核对原SHA；18个新原生实际独立计算成交、费用、资金费、风险，再与旧BTC完整因果时轴对齐相加。','下一UTC00:01真实OPEN执行；q=floor(N/此前完整close/lot)*lot。33日上下文含30预热及3日初始embargo；静态规则无拟合、未来标签，purge不适用。370日OOS为2025-10-19UTC00:01至2026-10-24UTC00:01，12完整30日折＋10日尾折连续承接现金/数量/entry/费用；近期40由day330继承状态分8×5日，不重开本金或诊断平仓，仅原终点计费退出。反复研究的历史属于开发验证，非未触碰最终测试。','每侧5bp费＋1bp半价差＋2bp滑点＋0.5×滞后20日日log波动×sqrt(实际成交金额/滞后20日quoteADV)冲击，参与率≤0.1%，tick/lot/最小金额/100%抵押约束。资金费=−有符号q×实际结算mark×rate，流出按1/2/3倍成本放大、收入不放大；永续无虚构现货借币。闭合小时不利mark高低和正时长状态重叠检查独立银行1%维持保证金代理；缺L2/TCA/历史完整tier/tick清算/容量证明。','固定门槛：全期及近期三成本净正、1x月正折≥9/12、近期≥6/8、全连续OOS的3x整体回撤≤25%、同机制三维相邻索引半径1含自身全期3x净正≥60%、≥4往返、(参考毛利＋资金费)/成本≥2.5、现金/拒单/风险违规0、终点平仓、≥180日。预设36配置和全部既往试验存在多重选择偏差，无DSR/PBO或稳定实盘盈利证明。',json.dumps(summary,ensure_ascii=False),'新规则合成测试先RED后GREEN，2970组严格边界/实际持仓状态/未来不变性及旧默认规则回归；仅majority_target和simulate改变，数据、数量、执行成本、资金费和风险函数原字节保持。实际回测由独立整数信号、Decimal成交/资金费、逐点净值及整体/逐折指标审计。','6图36面板及全部收益/Sharpe/Calmar/回撤/相邻边/匹配旧规则和恒多对照留档。原冻结单S28候选与SMA65独立续接02:30至04:30，仅已闭合mark，规则/本金/持仓/成本完整承接；这两个延迟shadow账户与十策略实时报价账户分开。下一日决策Oct30UTC00:01，下一资金费Oct29UTC08:00。','背景沿用2026-10-27实际访问的一手[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)及[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)。门控仅用于入场是本轮研究假设，非原论文复现或盈利迁移结论。','复现工作目录/home/desktop/Documents/Codex/EquiTide，audit.py/audit_native.py/check_sources.py/check_exports.py/check_feed.py只读核验；原账户audit_candidate.py/audit_forward.py和forward.py --reproduce复现。已完成精确配置不得再次reserve/evaluate。所有正负结果与失败事实保留，行情及原始HTTPpacket位于ignoreddata并绑定SHA。main普通非强推及完整远端tree/blob/行情核验后释放自身排他锁。'];(R/'result.md').write_text('\n\n'.join(lines)+'\n');print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
