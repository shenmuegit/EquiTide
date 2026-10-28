"""Export new two-axis voting surfaces and matched immutable single-horizon controls."""
import copy,csv,gzip,io,itertools,json,statistics
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run import ROOT,R,SLOWS,LOOKS,axes,anchor_configs,grid_configs,sha,put

def table(path,rows,compress=False):
 fields=list(dict.fromkeys(k for row in rows for k in row));b=io.StringIO(newline='');w=csv.DictWriter(b,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows);path.write_bytes(gzip.compress(b.getvalue().encode(),mtime=0) if compress else b.getvalue().encode())
def main():
 assert not(R/'finish.json').exists();r=json.loads((R/'report.json').read_text());grid=grid_configs(r['configs']);old=anchor_configs();assert len(grid)==len(old)==12;holds={}
 for key,ref in json.loads((R/'holds.json').read_text()).items():
  assert sha(ROOT/ref['report'])==ref['report_sha256'];c=copy.deepcopy(json.loads((ROOT/ref['report']).read_text())['configs'][ref['name']]);c.update(read_only_anchor=True,scope=ref['scope'],asset=ref['asset'],capital_usdt=ref['capital_usdt'])
  for z in c['scenes'].values():
   if 'recent40' not in z:z['recent40']=copy.deepcopy(z['extension40'])
  holds[key]=c
 allby={**old,**grid,**{x['name']:x for x in holds.values()}};rows=[];folds=[];recent=[];daily=[];comp=[];edges=[];cells={}
 for c in allby.values():
  ro=c.get('read_only_anchor',False);meta={'name':c['name'],'scope':c['scope'],'asset':c['asset'],'role':c['role'],'read_only_anchor':ro,'capital_usdt':c['capital_usdt'],'trend_gate_mode':c.get('trend_gate_mode','single_horizon' if c['role']=='candidate' else 'constant_long')}
  if c['role']=='candidate':meta.update({p:c[p] for p in axes(c)})
  cells[c['name']]={**meta,'fingerprint':c['fingerprint'],'original_or_new_status':c['status'],'scenes':{k:{p:z[p] for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','NAV_sha256_f64le']} for k,z in c['scenes'].items()}}
  for k,z in c['scenes'].items():
   rows.append({**meta,'cost_multiplier':int(k),'status':c['status'],**{p:z[p] for p in ['net_return_pct','max_drawdown_pct','daily_mark_drawdown_pct','sharpe_365','calmar','cost_usdt','cost_pct_initial','funding_usdt','gross_reference_PnL_to_execution_cost','executions','round_trips','NAV_sha256_f64le']},**{'recent40_'+p:z['recent40'][p] for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','NAV_sha256_f64le']},**{'cost_'+p:v for p,v in z['cost_parts_usdt'].items()}});folds.extend({**meta,'cost_multiplier':int(k),**f} for f in z['folds']);recent.extend({**meta,'cost_multiplier':int(k),**f} for f in z['recent40']['folds'])
   if ro:continue
   daily.extend({**meta,'cost_multiplier':int(k),'boundary_index':j,'equity_usdt':v} for j,v in enumerate(z['daily_equity_usdt']))
   for kind,y in [('same_bank_single_horizon',old[c['matched_single_reference']]),('same_bank_constant_long',holds[c['asset']])]:
    a=y['scenes'][k];assert y['capital_usdt']==c['capital_usdt'];comp.append({**meta,'cost_multiplier':int(k),'reference_kind':kind,'reference_name':y['name'],'reference_fingerprint':y['fingerprint'],'reference_original_status':y['status'],'new_return_pct':z['net_return_pct'],'reference_return_pct':a['net_return_pct'],'return_delta_pp':z['net_return_pct']-a['net_return_pct'],'DD_delta_pp':z['max_drawdown_pct']-a['max_drawdown_pct'],'recent40_return_delta_pp':z['recent40']['net_return_pct']-a['recent40']['net_return_pct'],'recent_positive5d_delta':c['recent40_positive_5d_folds_1x']-y['recent40_positive_5d_folds_1x'] if kind=='same_bank_single_horizon' else None,'execution_delta':z['executions']-a['executions'],'cost_delta_usdt':z['cost_usdt']-a['cost_usdt'],'new_NAV_sha256':z['NAV_sha256_f64le'],'reference_NAV_sha256':a['NAV_sha256_f64le'],'cash_analytic_return_pct':0,'limit':'Samebank/N/H/S/L/fixedBTC;onlyactualETHslowfilterchanges' if kind=='same_bank_single_horizon' else 'Samecapital/Nconstantlong,differentsignals/exposure/risk'})
 for scope in ['native','parent']:
  subset=[c for c in grid.values() if c['scope']==scope];dims=axes(subset[0]);fields=list(dims);by={tuple(c[p] for p in fields):c for c in subset};assert set(by)==set(itertools.product(*dims.values()));scope_edges=[]
  for key,c in by.items():
   for i,(field,axis) in enumerate(dims.items()):
    j=axis.index(key[i])
    if j+1==len(axis):continue
    other=list(key);other[i]=axis[j+1];y=by[tuple(other)];a,b=c['scenes']['3'],y['scenes']['3'];scope_edges.append({'scope':scope,'axis':field,'from':c['name'],'to':y['name'],'return3_delta_pp':b['net_return_pct']-a['net_return_pct'],'DD3_delta_pp':b['max_drawdown_pct']-a['max_drawdown_pct'],'sharpe3_delta':b['sharpe_365']-a['sharpe_365'] if a['sharpe_365'] is not None and b['sharpe_365'] is not None else None,'recent40_return3_delta_pp':b['recent40']['net_return_pct']-a['recent40']['net_return_pct']})
  vals=[abs(e['sharpe3_delta']) for e in scope_edges if e['sharpe3_delta'] is not None];cut=2*statistics.pstdev(vals) if vals else None
  for e in scope_edges:e['full_sharpe_cliff']=e['sharpe3_delta'] is not None and abs(e['sharpe3_delta'])>cut;e['cliff_threshold']=cut
  edges.extend(scope_edges);fig,axs=plt.subplots(3,4,figsize=(18,10),layout='constrained')
  for i,field in enumerate(['net_return_pct','sharpe_365','max_drawdown_pct']):
   vv=[(x['scenes']['3']['recent40'] if rr else x['scenes']['3'])[field] for c in subset for x in [c,old[c['matched_single_reference']]] for rr in [False,True]];limit=max([abs(x) for x in vv if x is not None] or [1]) or 1
   for j,(legacy,rr) in enumerate([(True,False),(False,False),(True,True),(False,True)]):
    def metric(S,L):
     c=by[S,L];c=old[c['matched_single_reference']] if legacy else c;return (c['scenes']['3']['recent40'] if rr else c['scenes']['3'])[field]
    mat=np.asarray([[metric(S,L) for L in LOOKS] for S in SLOWS],dtype=float);im=axs[i,j].imshow(mat,aspect='auto',cmap='RdYlGn_r' if field=='max_drawdown_pct' else 'RdYlGn',vmin=0 if field=='max_drawdown_pct' else -limit,vmax=limit);axs[i,j].set_title(('Single S' if legacy else 'Majority S-1/S/S+1')+' / '+('40d' if rr else '370d')+'\n3x '+field);axs[i,j].set_xticks(range(len(LOOKS)),LOOKS);axs[i,j].set_yticks(range(len(SLOWS)),SLOWS);axs[i,j].set_xlabel('Fast L (days)');axs[i,j].set_ylabel('Slow center S (days)')
    for a,b in itertools.product(range(len(SLOWS)),range(len(LOOKS))):axs[i,j].text(b,a,'n/a' if np.isnan(mat[a,b]) else f'{mat[a,b]:+.3f}',ha='center',va='center',fontsize=9)
    fig.colorbar(im,ax=axs[i,j])
  fig.suptitle(scope+' / ETH H2.5% zero exit; '+('10000bank,N3000' if scope=='native' else 'two10000banks,N1000/3000,raw1/1;fixedBTC31/H4/E1')+'\nKnown repeatedly researched history; single-S columns are immutable old controls');fig.savefig(R/f'sensitivity_{scope}.png',dpi=120);plt.close(fig)
 counts={'cost':len(rows),'full_folds':len(folds),'recent40_folds':len(recent),'daily_NAV':len(daily),'edges':len(edges),'reference_comparisons':len(comp)};assert list(counts.values())==[78,1014,624,13356,14,72]
 for name,data,zipit in [('sensitivity.csv',rows,False),('fold_results.csv',folds,False),('recent40_fold_results.csv',recent,False),('daily_equity.csv.gz',daily,True),('joint_edges.csv',edges,False),('reference_comparisons.csv',comp,False)]:table(R/name,data,zipit)
 r['joint_grid_sensitivity']={'dimension_count':2,'native_ETH_cells':6,'parent_cells':6,'new_cells':12,'readonly_single_horizon_control_cells':12,'old_hold_controls':2,'adjacent_edges':14,'neighbors_include_only_new_majority_rule':True,'cells':cells,'old_qualification_unchanged':True};put(R/'report.json',r);cs=list(r['configs'].values());summary={'new_financial_configs':12,'new_native_components':6,'new_passive_parents':6,'passed_candidates':len(r['summary']['passed']),'rejected_candidates':len(r['summary']['rejected']),'positive_configs_by_cost':r['summary']['positive_configs_by_cost'],'failed_criteria_counts':dict(Counter(p for c in cs for p in c['failed_criteria'])),'by_scope':{s:{'new':sum(c['scope']==s for c in cs),'passed':sum(c['scope']==s and c['status']=='passed' for c in cs),'best_full3':max(({'name':c['name'],'return3_pct':c['scenes']['3']['net_return_pct'],'whole_DD3_pct':c['scenes']['3']['max_drawdown_pct'],'recent_return3_pct':c['scenes']['3']['recent40']['net_return_pct'],'positive_months1':c['positive_complete_30d_folds_1x'],'positive_recent1':c['recent40_positive_5d_folds_1x'],'failed_criteria':c['failed_criteria']} for c in cs if c['scope']==s),key=lambda x:x['return3_pct'])} for s in ['native','parent']},'rows':counts};put(R/'summary.json',summary)
 ctx=json.loads((R/'context.json').read_text());lines=[f'# {R.name} ETH相邻慢周期多数表决的原生与组合验证',f'实际计算6个新ETH原生＋6个BTC/ETH组合，共12配置/36成本场景；历史通过{summary["passed_candidates"]}、淘汰{summary["rejected_candidates"]}。完整读取{ctx["registry_events"]}登记事件/{ctx["registry_ids"]}ID、{len(ctx["prior_conclusions_read"])}份结论；初始16项均有实际证据。',
 '针对前轮慢28日近期资格孤立于27/29日的问题，事前固定新规则：ETH快ROC L3/4，阈值2.5%、零交叉退出；S27/28/29中心各取S−1/S/S+1三个慢ROC，至少两票严格正允许多、至少两票严格负允许空，其他平仓。快反转方向与慢多数方向一致才持仓；现金须新严格极端入场，无隐藏desired，不新建三个并行ETH订单。S和L二维6格/作用域、7相邻边/作用域，新多数规则自身邻域用于资格；12旧单S对照保持原结果与状态，不混入新规则邻域。',
 '新ETH银行10000USDT、固定入场3000。BTC固定ROC31/H4%/退出1%、银行10000、入场1000；父层原值1/1代表两个完整独立银行，本金20000、入场预算4000=初始父本金20%。不归一化、不复利调仓、不转账/交叉保证金/再平衡/现金利息。8旧原生/24成本NAV按实际现金/数量/entry分段恢复并核对SHA；新6原生实际执行专属成交/成本/资金费/风险，新6组合按共同(ns,eventcode)轴因果承接上一完成NAV再逐点相加，不平均收益/Sharpe/回撤或缩放其他金额结果。',
 'UTC00:01实际OPEN执行，信号与q=floor(N/前一完整close/lot)*lot只读此前已闭合信息。先平不兼容持仓后按新极端开仓；同方向保留实际数量。TDD先观察旧单S在“两邻负/中心正”例子中不能开空，再验证新规则、镜像开多、零票、带内现金不入场、实际持仓保留、零退出、精确中位ROC及未来数据不变性。仅新target选择与三票证据记录改变；原单S函数、成本/资金费/行情/风险/统计函数原字节保持。真实回测另用独立整数票决、Decimal成交/资金费和全净值核验。',
 '8真实合并Parquet与16年度/近期源SHA/字节固定。连续370日OOS2025-10-19UTC00:01至2026-10-24UTC00:01，33日上下文、3日初始embargo，最大慢视窗30日可用。静态规则无拟合或未来标签，purge不适用。12完整30日折＋10日尾折承接现金/数量/费用；近期40日从day330真实状态继承并分8×5日，不重开本金或诊断平仓；只在原终点计费平仓。这些数据反复研究，属于开发验证，不是未触碰最终测试或独立未来证据。',
 '每侧5bp手续费＋1bp半价差＋2bp滑点＋0.5×此前20日log收益样本波动×sqrt(实际成交金额/此前20日quoteADV)冲击，参与率≤0.1%，真实不利tick/lot/最小金额及100%抵押入场约束。永续资金费=-q×真实结算mark×rate，流出按1/2/3倍、收入不放大；无虚构现货借币。缺L2/TCA/完整历史保证金阶梯，1%维持保证金＋闭合小时不利mark仅风险代理，不保证tick清算安全或实盘容量。',
 '门槛不变：全期/近期三档净正、1倍月正折≥9/12及近期≥6/8、三倍完整连续净值DD≤25%、二维排序相邻索引半径1含自身且仅同新规则邻域三倍净正≥60%、至少4往返、(参考毛利＋资金费)/执行成本≥2.5、现金/拒单/风险代理违规0、终点空仓且≥180日。2图24面板比较旧单S/新多数过滤的全期及近期收益、Sharpe、回撤；78成本行、1014全期折、624近期折、13356新日边界、14敏感性边及72匹配对照均保存。',
 '结果：'+json.dumps(summary,ensure_ascii=False),
 '原单S冻结候选与旧SMA从Oct28UTC08:30续接至10:30，不切换到新多数规则。保留实际现金、数量、entry、费用、已计08:00资金费及完整净值链；09:00闭合小时检查承接08小时结算前/后风险栈，不重计资金费、不重开本金、不强制截止平仓。下一资金费16:00、下一日决策Oct29UTC00:01。真实闭合行情延迟重建，区别于paper10十策略实时报价账户；partial的rejected不取消长期计划。',
 '背景沿用此前2026-10-27实际访问的[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)及[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)。本多数规则是研究推论，不是论文复现或利润/容量移植。全登记关键词命中的资金费中位数、岭回归中位插补、现货滚动价格中位策略，与此ETH永续快反转＋相邻慢ROC票决的完整规则不同。12新相关试验及所有既往试验存在多重选择偏差，无DSR/PBO、独立前向盈利或稳定实盘盈利证明。',
 '复现工作目录/home/desktop/Documents/Codex/EquiTide。audit.py/audit_native.py、check_sources.py、audit_candidate.py、audit_forward.py、forward.py --reproduce只读已完成真实证据；勿重新reserve/evaluate/summarize相同已完成配置。原始命令日志保持字节，发布空白检查排除*.log，全部日志仍做完整tree/blob/SHA验证；main普通非强推，不建分支、定时任务或重部署。'];(R/'result.md').write_text('\n\n'.join(lines)+'\n');print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
