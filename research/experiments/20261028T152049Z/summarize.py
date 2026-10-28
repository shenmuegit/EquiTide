"""Export every actual weighted variant and old readonly grid cell; no model evaluation."""
import copy,csv,gzip,io,itertools,json,statistics
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run import ROOT,R,WEIGHTS,HURDLES,SLOWS,LOOKS,axes,grid_configs,sha,put

def table(path,rows,compress=False):
 fields=list(dict.fromkeys(k for row in rows for k in row));b=io.StringIO(newline='');w=csv.DictWriter(b,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows);path.write_bytes(gzip.compress(b.getvalue().encode(),mtime=0) if compress else b.getvalue().encode())
def main():
 assert not(R/'finish.json').exists();r=json.loads((R/'report.json').read_text());grid=grid_configs(r['configs']);assert len(grid)==54;plan=json.loads((R/'plan.json').read_text());h=plan['read_only_hold_references']['COMBO'];c=copy.deepcopy(json.loads((ROOT/h['report']).read_text())['configs'][h['name']]);c.update(read_only_anchor=True,scope='parent',asset='COMBO',capital_usdt=20000);allby={**grid,**{n:c for n,c in r['configs'].items() if c['role']=='benchmark'},c['name']:c};assert len(allby)==57
 rows=[];folds=[];recent=[];daily=[];comp=[];edges=[]
 for c in allby.values():
  old=c.get('read_only_anchor',False);meta={'name':c['name'],'scope':'parent','asset':'COMBO','role':c['role'],'read_only_anchor':old,'capital_usdt':c['capital_usdt']}
  if c['role']=='candidate':meta.update({p:c[p] for p in axes(c)})
  for k,z in c['scenes'].items():
   if 'recent40' not in z:z['recent40']=copy.deepcopy(z['extension40'])
   rows.append({**meta,'cost_multiplier':int(k),'status':c['status'],**{p:z[p] for p in ['net_return_pct','max_drawdown_pct','daily_mark_drawdown_pct','sharpe_365','calmar','cost_usdt','cost_pct_initial','funding_usdt','gross_reference_PnL_to_execution_cost','executions','round_trips','NAV_sha256_f64le']},**{'recent40_'+p:z['recent40'][p] for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','NAV_sha256_f64le']},**{'cost_'+p:v for p,v in z['cost_parts_usdt'].items()}});folds.extend({**meta,'cost_multiplier':int(k),**f} for f in z['folds']);recent.extend({**meta,'cost_multiplier':int(k),**f} for f in z['recent40']['folds'])
   if old:continue
   daily.extend({**meta,'cost_multiplier':int(k),'boundary_index':j,'equity_usdt':v} for j,v in enumerate(z['daily_equity_usdt']))
   if c['role']=='benchmark':continue
   baseline=next(x for x in grid.values() if x['BTC_ownership_multiplier']==1 and all(x[p]==c[p] for p in ['reversal_return_hurdle','trend_filter_lookback_days','reversal_lookback_days']));hold=next(x for x in r['configs'].values() if x['role']=='benchmark' and x['BTC_ownership_multiplier']==c['BTC_ownership_multiplier'])
   for kind,y in [('same_native_pair_old_raw1_1',baseline),('same_raw_ownership_constant_long',hold)]:
    a=y['scenes'][k];comp.append({**meta,'cost_multiplier':int(k),'reference_kind':kind,'reference_name':y['name'],'reference_fingerprint':y['fingerprint'],'reference_original_status':y['status'],'reference_capital_usdt':y['capital_usdt'],'return_delta_pp':z['net_return_pct']-a['net_return_pct'],'DD_delta_pp':z['max_drawdown_pct']-a['max_drawdown_pct'],'recent40_return_delta_pp':z['recent40']['net_return_pct']-a['recent40']['net_return_pct'],'cost_delta_usdt':z['cost_usdt']-a['cost_usdt'],'new_NAV_sha256':z['NAV_sha256_f64le'],'reference_NAV_sha256':a['NAV_sha256_f64le'],'cash_analytic_return_pct':0,'limit':'Old1/1 has different initialcapital and exposure;no equalrisk assertion.' if kind=='same_native_pair_old_raw1_1' else 'Same rawownership,capital,underlyingN;constantlong differs in exposure path.'})
 fields=list(axes(next(iter(grid.values()))));by={tuple(c[p] for p in fields):c for c in grid.values()};dims=axes(next(iter(grid.values())))
 for key,c in by.items():
  for i,(field,axis) in enumerate(dims.items()):
   j=axis.index(key[i])
   if j+1==len(axis):continue
   other=list(key);other[i]=axis[j+1];y=by[tuple(other)];a,b=c['scenes']['3'],y['scenes']['3'];edges.append({'scope':'parent','axis':field,'from':c['name'],'to':y['name'],'return3_delta_pp':b['net_return_pct']-a['net_return_pct'],'DD3_delta_pp':b['max_drawdown_pct']-a['max_drawdown_pct'],'sharpe3_delta':b['sharpe_365']-a['sharpe_365'],'recent40_return3_delta_pp':b['recent40']['net_return_pct']-a['recent40']['net_return_pct']})
 cut=2*statistics.pstdev(abs(e['sharpe3_delta']) for e in edges)
 for e in edges:e['full_sharpe_cliff']=abs(e['sharpe3_delta'])>cut;e['cliff_threshold']=cut
 for H,L in itertools.product(HURDLES,LOOKS):
  fig,axs=plt.subplots(3,2,figsize=(12,10),layout='constrained')
  for i,field in enumerate(['net_return_pct','sharpe_365','max_drawdown_pct']):
   vals=[(by[w,H,S,L]['scenes']['3']['recent40'] if recent40 else by[w,H,S,L]['scenes']['3'])[field] for w,S,recent40 in itertools.product(WEIGHTS,SLOWS,[False,True])];limit=max(abs(x) for x in vals) or 1
   for j,recent40 in enumerate([False,True]):
    mat=np.asarray([[(by[w,H,S,L]['scenes']['3']['recent40'] if recent40 else by[w,H,S,L]['scenes']['3'])[field] for w in WEIGHTS] for S in SLOWS]);im=axs[i,j].imshow(mat,aspect='auto',cmap='RdYlGn_r' if field=='max_drawdown_pct' else 'RdYlGn',vmin=0 if field=='max_drawdown_pct' else -limit,vmax=limit);axs[i,j].set_title(('Inherited40days' if recent40 else '370days')+' /3x '+field);axs[i,j].set_xticks(range(3),WEIGHTS);axs[i,j].set_yticks(range(3),SLOWS);axs[i,j].set_xlabel('BTC raw bank ownership (ETH fixed1)');axs[i,j].set_ylabel('ETH slow center S(days)')
    for x,y in itertools.product(range(3),range(3)):axs[i,j].text(y,x,f'{mat[x,y]:+.3f}'+('*' if WEIGHTS[y]==1 else ''),ha='center',va='center')
    fig.colorbar(im,ax=axs[i,j])
  fig.suptitle(f'Majority ETH H{H*100:g}% L{L}; BTC31/H4/E1\nraww/1;capital15k/20k/25k;*old1/1;known development history');fig.savefig(R/f'sensitivity_H{int(round(H*1000)):03d}_L{L}.png',dpi=120);plt.close(fig)
 counts={'cost':len(rows),'full_folds':len(folds),'recent40_folds':len(recent),'daily_NAV':len(daily),'edges':len(edges),'reference_comparisons':len(comp)};assert list(counts.values())==[171,2223,1368,42294,135,216]
 for name,data,z in [('sensitivity.csv',rows,False),('fold_results.csv',folds,False),('recent40_fold_results.csv',recent,False),('daily_equity.csv.gz',daily,True),('joint_edges.csv',edges,False),('reference_comparisons.csv',comp,False)]:table(R/name,data,z)
 candidates=[c for c in r['configs'].values() if c['role']=='candidate'];summary={'new_financial_configs':38,'new_native_components':0,'new_passive_parents':38,'candidate_configs':36,'benchmark_configs':2,'passed_candidates':len(r['summary']['passed']),'rejected_candidates':len(r['summary']['rejected']),'positive_configs_by_cost':r['summary']['positive_configs_by_cost'],'failed_criteria_counts':dict(Counter(p for c in candidates for p in c['failed_criteria'])),'rows':counts,'by_BTC_raw_ownership':{str(w):{'candidates':18,'passed':sum(c['BTC_ownership_multiplier']==w and c['status']=='passed' for c in candidates),'recent6of8':sum(c['BTC_ownership_multiplier']==w and c['recent40_positive_5d_folds_1x']>=6 for c in candidates)} for w in [.5,1.5]}};put(R/'summary.json',summary)
 ctx=json.loads((R/'context.json').read_text());lines=[f'# {R.name} 固定银行份额与多数门控参数联合验证',f'实际38项：36候选＋2同权重恒多对照；历史通过{summary["passed_candidates"]}、候选淘汰{summary["rejected_candidates"]}。完整读取{ctx["registry_events"]}事件/{ctx["registry_ids"]}ID、{len(ctx["prior_conclusions_read"])}份结论，初始16项实际证据齐全。',plan['hypothesis'],plan['rules']['allocation'],plan['rules']['composition'],'事前固定 BTC原值份额0.5/1/1.5、ETH份额1，与ETH阈值2/2.5/3%、慢中心27/28/29和快反转3/4日联合形成四维54格、135相邻边；18个raw1/1旧格只读，36新候选和2新恒多对照均先成功reserve，再实际计算。父本金15000/20000/25000，继承入场预算3500/4000/4500，占比23.333%/20%/18%；不归一化。相同组件及原值权重进行语义查重，未按名称或顺序伪创新。','21个旧原生/63成本NAV由已保存现金、数量与entry片段重建并校验原SHA；不重跑信号、下单或资金费模型。源账本的非线性成交量冲击及tick/lot/抵押、资金费和风险完整保留。份额缩放的是经济所有权；成本/损益/资金费按份额乘，源成交及事件计数不乘；不能把本研究当BTC N500/N1500的新订单回测或按缩放后数量重新估成本。实际模拟银行之间不净额成交、不交叉救助。','370日连续OOS为2025-10-19UTC00:01至2026-10-24UTC00:01。33日上下文含30日预热与3日初始embargo，静态规则无训练/未来标签、purge不适用；日信号只用此前完成close、数量由此前close取lot，UTC00:01实际OPEN执行。12个完整30日折及10日尾折承接现金/仓位；近期40日从day330继承，8×5日折不重置或额外平仓，终点原定平仓计费。所有组合沿共同(ns,eventcode)时轴因果承接源NAV，整体回撤及Sharpe从实际加权连续净值重新计算。','每侧5bp费、1bp半价差、2bp滑点加0.5×此前20日样本日log波动×sqrt(实际源订单金额/此前20日quoteADV)冲击；参与率≤0.1%，全额抵押入场。资金费=-有符号数量×实际结算mark×rate，流出乘成本倍数，收入不放大；永续无需虚构现货借币。1%维持保证金与已闭合小时不利mark仅风险代理，缺盘口/TCA/历史完整阶梯和tick清算证据。','门槛保持全期及近期三档净正、月正折≥9/12、近期正折≥6/8、三倍连续整体DD≤25%、四维邻域三倍净正≥60%、≥4往返、参考毛利＋资金费/成本≥2.5、现金/拒单/独立银行风险违规0、终点空仓且≥180日。恒多仅对照，以reference_only原因rejected，不冒称alpha资格。','与同权重恒多及现金0比较；旧1/1对照资本/风险不同，报告金额与收益率，不作等风险比较。全历史多次使用，属于开发验证；38个新相关试验加所有先前试验存在多重选择偏差，无DSR/PBO或未触碰最终测试资格。',json.dumps(summary,ensure_ascii=False),'原单S28冻结候选与SMA65从UTC12:30续接至14:30，持仓/现金/成本/资金费/风险栈/完整净值前缀承接，不换新权重，不重复08资金费或日决策，不截止强平。下一16:30窗口含16:00实际资金费、下一日决策Oct29UTC00:01。延迟真实闭合行情重建，不是十策略同期报价执行或真实订单。','背景沿用以前实际访问的一手AQR Time Series Momentum与Trading Costs of Asset Pricing Anomalies；本权重/多数门控为研究推论，不是论文复制或收益移植。新历史通过也不代表稳定实盘盈利。','复现工作目录/home/desktop/Documents/Codex/EquiTide；audit.py独立播放记录事件并核对每个加权NAV、折、资金费和原资格。check_sources.py/audit_forward.py/audit_candidate.py/check_feed.py只读证据，forward.py --reproduce离线复现；不重新reserve/evaluate/summarize已完成配置。main普通非强推，远端完整tree/blob/SHA核验后释放本轮锁。']
 (R/'result.md').write_text('\n\n'.join(lines)+'\n');print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
