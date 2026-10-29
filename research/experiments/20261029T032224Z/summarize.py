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
   for kind,y in [('matched_old_G0',baseline),('same_bank_constant_long',holds[c['asset']])]:
    a=y['scenes'][k];assert y['capital_usdt']==c['capital_usdt'];comp.append({**meta,'cost_multiplier':int(k),'reference_kind':kind,'reference_name':y['name'],'reference_fingerprint':y['fingerprint'],'reference_original_status':y['status'],'new_return_pct':z['net_return_pct'],'reference_return_pct':a['net_return_pct'],'return_delta_pp':z['net_return_pct']-a['net_return_pct'],'DD_delta_pp':z['max_drawdown_pct']-a['max_drawdown_pct'],'recent40_return_delta_pp':z['recent40']['net_return_pct']-a['recent40']['net_return_pct'],'execution_delta':z['executions']-a['executions'],'cost_delta_usdt':z['cost_usdt']-a['cost_usdt'],'new_NAV_sha256':z['NAV_sha256_f64le'],'reference_NAV_sha256':a['NAV_sha256_f64le'],'cash_analytic_return_pct':0,'limit':'Samebank/N/fastH2.5/S/L/fixedBTC,oldG0versusnewslowG;differentgate/exposure/risk' if kind=='matched_old_G0' else 'Samebank/N constantlongreference,different native signals/exposure/risk'})
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
   fig.suptitle(scope+' / '+('ETH10000bank,N3000' if scope=='native' else 'BTC1000+ETH3000 entrybudgets,two10000banks raw1/1')+f'\nETH slow G{H*100:g}%/fastH2.5%/zeroexit;known repeatedhistory;knownhistory');fig.savefig(R/f'sensitivity_{scope}_H{int(round(H*1000)):03d}.png',dpi=120);plt.close(fig)
 for field in ['sharpe3_delta']:
  vals=[abs(e[field]) for e in edges if e[field] is not None];cut=2*statistics.pstdev(vals) if vals else None
  for e in edges:e['full_sharpe_cliff']=e[field] is not None and abs(e[field])>cut;e['cliff_threshold']=cut
 counts={'cost':len(rows),'full_folds':len(folds),'recent40_folds':len(recent),'daily_NAV':len(daily),'edges':len(edges),'reference_comparisons':len(comp)};assert list(counts.values())==[150,1950,1200,40068,92,216]
 for name,data,zipit in [('sensitivity.csv',rows,False),('fold_results.csv',folds,False),('recent40_fold_results.csv',recent,False),('daily_equity.csv.gz',daily,True),('joint_edges.csv',edges,False),('reference_comparisons.csv',comp,False)]:table(R/name,data,zipit)
 joint={'dimension_count':3,'native_ETH_cells':24,'parent_cells':24,'new_cells':36,'readonly_old_cells':12,'old_hold_controls':2,'adjacent_edges':92,'cells':cells,'old_qualification_unchanged':True,'cliff_definition':'Descriptive absSharpe adjacentdelta >2populationSDof finiteabsdeltas;no oldrerating.'};put(R/'joint_grid_sensitivity.json',joint)
 cs=list(r['configs'].values());summary={'new_financial_configs':36,'new_native_components':18,'new_passive_parents':18,'passed_candidates':len(r['summary']['passed']),'rejected_candidates':len(r['summary']['rejected']),'positive_configs_by_cost':r['summary']['positive_configs_by_cost'],'failed_criteria_counts':dict(Counter(p for c in cs for p in c['failed_criteria'])),'by_scope':{s:{'new':sum(c['scope']==s for c in cs),'passed':sum(c['scope']==s and c['status']=='passed' for c in cs),'best_full3':max(({'name':c['name'],'return3_pct':c['scenes']['3']['net_return_pct'],'whole_DD3_pct':c['scenes']['3']['max_drawdown_pct'],'recent_return3_pct':c['scenes']['3']['recent40']['net_return_pct'],'positive_months1':c['positive_complete_30d_folds_1x'],'positive_recent1':c['recent40_positive_5d_folds_1x'],'failed_criteria':c['failed_criteria']} for c in cs if c['scope']==s),key=lambda x:x['return3_pct'])} for s in ['native','parent']},'rows':counts};put(R/'summary.json',summary)
 ctx=json.loads((R/'context.json').read_text());lines=[f'# {R.name} 多数慢趋势最小幅度G验证',f'实际18新ETH原生＋18新BTC/ETH组合，36配置/108成本场景；历史通过{summary["passed_candidates"]}、淘汰{summary["rejected_candidates"]}。完整读取{ctx["registry_events"]}事件/{ctx["registry_ids"]}ID及{len(ctx["prior_conclusions_read"])}份结论；初始16项已有实际证据。','本轮事前固定快反转阈值H2.5%、快周期L3/4、慢中心S27/28/29；新慢趋势最小幅度G0.5/1/2%，旧G0六原生＋六组合只读。全3D G0/0.5/1/2% × S27/28/29 × L3/4，每作用域24格/46相邻边，合计48格/92边；36新配置逐个先reserve再计算，旧资格保持。假设是忽略接近零的弱慢趋势，能否改善S28附近的近期集中，计算前固定全部参数、边界和门槛。','ETH前一完整L日ROC严格>2.5%反转空/<-2.5%反转多，带内只保留ROC<0的实际多、ROC>0的实际空，零退出。S-1/S/S+1三个完整慢ROC至少两票严格>G允许多、至少两票严格<-G允许空，否则平仓；等号与中性带不允许开仓或保留不兼容持仓。快方向须匹配慢允许方向，现金重入需新严格快极端，无隐藏desired。UTC00:01实际OPEN执行，q=floor(N/此前完整close/lot)*lot；不读未来OPEN/资金费/未闭合数据决定信号或数量。396项合成边界、投票、持仓/现金与未来不变性和G0回归检查已通过，不计作真实回测。','新引擎只修改majority_target与simulate的G传递/投票日志，其余数据、成交、资金费、数量、成本与风险函数原字节保持。ETH独立银行10000，固定N3000；BTC旧ROC31/H4%/退出1%、银行10000、N1000。父层原值[1,1]持有两完整银行，初始20000、入场预算4000=20%，不归一化、NAV缩放、转账、交叉保证金或再平衡。9旧原生/27成本NAV从已保存账本恢复核对原SHA；18新ETH实际计算专属成交/资金费/成本/风险；18组合沿共同纳秒/事件时轴因果相加，整体指标从完整净值重算。','8真实合并Parquet及16年度/近期源SHA固定。370日OOS2025-10-19UTC00:01至2026-10-24UTC00:01；33日上下文含30预热与3日初始embargo。静态规则无拟合/未来标签，purge不适用；12完整30日折加10日尾折连续承接现金/q/entry/费用，近期40从day330继承分8×5日，不重开本金或诊断平仓，仅原终点计费退出。反复使用历史属于开发验证，不是未触碰最终测试。','每侧5bp费+1bp半价差+2bp滑点+0.5×滞后20日日log波动×sqrt(实际订单金额/滞后20日quoteADV)冲击，参与率≤0.1%，不利tick/lot/最小金额/全额抵押约束。资金费=-有符号q×实际mark×rate，流出随1/2/3放大、收入不放大；永续不虚构现货借币。独立银行闭合小时1%维持保证金代理，缺L2/TCA/完整历史tier/tick清算及聚合容量证明。','门槛保持全期/近期三成本净正、1x完整月≥9/12正折且近期≥6/8、3x完整连续整体DD≤25%、3D相邻索引半径1含自身全期3x净正≥60%、≥4往返、(参考毛利+资金费)/成本≥2.5、现金/拒单/风险违规0、终点空仓且≥180日。匹配同H/S/L/N的G0旧规则、同本金恒多及现金0；旧资格不按扩展邻域重评。',json.dumps(summary,ensure_ascii=False),'原单S28候选及SMA65按原规则从UTC00:30续接至02:30，35日候选/65日SMA上下文、第三个日净值点与完整净值前缀承接；00:00资金费已在上轮入账，不重复。BTC00小时风险栈两条状态同为00:00，第一条持续时长为零，01close只检查有正重叠的资金费后状态，再检查01小时到02close；不丢失风险栈、不重开本金、不切换新G规则。下一资金费08:00、下一日决策Oct30UTC00:01。延迟闭合行情重建与paper10实时报价模拟分开。','背景沿用2026-10-27实际访问的一手[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)及[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)。新G假设是研究推论。36个相关新试验加全部既往试验存在多重选择偏差，无DSR/PBO、独立未来或稳定实盘盈利证明。','复现工作目录/home/desktop/Documents/Codex/EquiTide。audit.py/audit_native.py独立整数信号、Decimal成交/资金费、逐点NAV/风险核验，check_exports.py/check_sources.py/check_feed.py只读验证；audit_candidate.py/audit_forward.py、forward.py --reproduce复现原账户。不得重reserve/evaluate已完成精确配置；所有正负结果/账户账本/规则/失败保留，行情/HTTPpacket留ignoreddata绑定SHA；main非强推并验证完整远端tree/blob/行情后释放本轮锁。'];(R/'result.md').write_text('\n\n'.join(lines)+'\n');print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
