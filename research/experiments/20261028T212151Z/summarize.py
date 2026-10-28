"""Export all BTC ownership/ETH H/S/L combinations and matched BTC_H4 historical controls."""
import copy,csv,gzip,io,itertools,json,statistics
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run import ROOT,R,WEIGHTS,HURDLES,SLOWS,LOOKS,axes,grid_configs,anchor_configs,sha,put

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
  if not old:meta.update({p:c[p] for p in axes(c)})
  for k,z in c['scenes'].items():
   rows.append({**meta,'cost_multiplier':int(k),'status':c['status'],**{p:z[p] for p in ['net_return_pct','max_drawdown_pct','daily_mark_drawdown_pct','sharpe_365','calmar','cost_usdt','cost_pct_initial','funding_usdt','gross_reference_PnL_to_execution_cost','executions','round_trips','NAV_sha256_f64le']},**{'recent40_'+p:z['recent40'][p] for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','NAV_sha256_f64le']},**{'cost_'+p:v for p,v in z['cost_parts_usdt'].items()}});folds.extend({**meta,'cost_multiplier':int(k),**f} for f in z['folds']);recent.extend({**meta,'cost_multiplier':int(k),**f} for f in z['recent40']['folds'])
   if old:continue
   daily.extend({**meta,'cost_multiplier':int(k),'boundary_index':j,'equity_usdt':v} for j,v in enumerate(z['daily_equity_usdt']))
   refs=[('matched_BTC_H4_same_ETH',next(x for x in controls.values() if all(x[f]==c[f] for f in ['trend_filter_lookback_days','reversal_return_hurdle','reversal_lookback_days']))),('same_capital_constant_long',hold)]
   for kind,y in refs:
    a=y['scenes'][k];comp.append({**meta,'cost_multiplier':int(k),'reference_kind':kind,'reference_name':y['name'],'reference_fingerprint':y['fingerprint'],'reference_original_status':y['status'],'reference_capital_usdt':20000,'return_delta_pp':z['net_return_pct']-a['net_return_pct'],'DD_delta_pp':z['max_drawdown_pct']-a['max_drawdown_pct'],'recent40_return_delta_pp':z['recent40']['net_return_pct']-a['recent40']['net_return_pct'],'cost_delta_usdt':z['cost_usdt']-a['cost_usdt'],'new_NAV_sha256':z['NAV_sha256_f64le'],'reference_NAV_sha256':a['NAV_sha256_f64le'],'cash_analytic_return_pct':0,'limit':'Samecapital20000/ownedentrybudget4000;source native sizes fixed,different timing/exposure/risk,not independent new market alpha.'})
 dims=axes(next(iter(grid.values())));fields=list(dims);by={tuple(c[p] for p in fields):c for c in grid.values()};assert len(by)==54
 for key,c in by.items():
  for i,(field,axis) in enumerate(dims.items()):
   j=axis.index(key[i])
   if j+1==len(axis):continue
   other=list(key);other[i]=axis[j+1];y=by[tuple(other)];a,b=c['scenes']['3'],y['scenes']['3'];edges.append({'scope':'parent','axis':field,'from':c['name'],'to':y['name'],'return3_delta_pp':b['net_return_pct']-a['net_return_pct'],'DD3_delta_pp':b['max_drawdown_pct']-a['max_drawdown_pct'],'sharpe3_delta':b['sharpe_365']-a['sharpe_365'],'recent40_return3_delta_pp':b['recent40']['net_return_pct']-a['recent40']['net_return_pct']})
 cut=2*statistics.pstdev(abs(e['sharpe3_delta']) for e in edges)
 for e in edges:e['full_sharpe_cliff']=abs(e['sharpe3_delta'])>cut;e['cliff_threshold']=cut
 for a,L in itertools.product(WEIGHTS,LOOKS):
  fig,axs=plt.subplots(3,2,figsize=(12,10),layout='constrained')
  for i,field in enumerate(['net_return_pct','sharpe_365','max_drawdown_pct']):
   vals=[(by[a,H,S,L]['scenes']['3']['recent40'] if rr else by[a,H,S,L]['scenes']['3'])[field] for H,S,rr in itertools.product(HURDLES,SLOWS,[False,True])];limit=max(abs(x) for x in vals) or 1
   for j,rr in enumerate([False,True]):
    mat=np.asarray([[(by[a,H,S,L]['scenes']['3']['recent40'] if rr else by[a,H,S,L]['scenes']['3'])[field] for S in SLOWS] for H in HURDLES]);im=axs[i,j].imshow(mat,aspect='auto',cmap='RdYlGn_r' if field=='max_drawdown_pct' else 'RdYlGn',vmin=0 if field=='max_drawdown_pct' else -limit,vmax=limit);axs[i,j].set_title(('Inherited40days' if rr else '370days')+' /3x '+field);axs[i,j].set_xticks(range(3),SLOWS);axs[i,j].set_yticks(range(3),[100*H for H in HURDLES]);axs[i,j].set_xlabel('ETH majority slow center S(days)');axs[i,j].set_ylabel('ETH fast threshold H(percent)')
    for x,y in itertools.product(range(3),range(3)):axs[i,j].text(y,x,f'{mat[x,y]:+.3f}',ha='center',va='center')
    fig.colorbar(im,ax=axs[i,j])
  fig.suptitle(f'BTC H2({a:g}) + H6({1-a:g}) + ETH L{L}(1)\ncapital20000,budget4000;source N1000/1000/3000;known development history');fig.savefig(R/f'sensitivity_A{int(a*100):02d}_L{L}.png',dpi=120);plt.close(fig)
 counts={'cost':len(rows),'full_folds':len(folds),'recent40_folds':len(recent),'daily_NAV':len(daily),'edges':len(edges),'reference_comparisons':len(comp)};assert list(counts.values())==[219,2847,1752,60102,135,324]
 for name,data,z in [('sensitivity.csv',rows,False),('fold_results.csv',folds,False),('recent40_fold_results.csv',recent,False),('daily_equity.csv.gz',daily,True),('joint_edges.csv',edges,False),('reference_comparisons.csv',comp,False)]:table(R/name,data,z)
 cs=list(r['configs'].values());summary={'new_financial_configs':54,'new_native_components':0,'new_passive_parents':54,'candidate_configs':54,'benchmark_configs':0,'passed_candidates':len(r['summary']['passed']),'rejected_candidates':len(r['summary']['rejected']),'positive_configs_by_cost':r['summary']['positive_configs_by_cost'],'failed_criteria_counts':dict(Counter(p for c in cs for p in c['failed_criteria'])),'rows':counts,'by_slow_center':{str(S):{'candidates':18,'passed':sum(c['trend_filter_lookback_days']==S and c['status']=='passed' for c in cs),'recent6of8':sum(c['trend_filter_lookback_days']==S and c['recent40_positive_5d_folds_1x']>=6 for c in cs),'full3x_positive_Sharpe_fraction':sum(c['trend_filter_lookback_days']==S and c['scenes']['3']['sharpe_365']>0 for c in cs)/18} for S in SLOWS}};put(R/'summary.json',summary);ctx=json.loads((R/'context.json').read_text());lines=[f'# {R.name} BTC入场阈值份额分散组合验证',f'实际54个新三银行组合，历史通过{summary["passed_candidates"]}、淘汰{summary["rejected_candidates"]}。完整读取{ctx["registry_events"]}事件/{ctx["registry_ids"]}ID、{len(ctx["prior_conclusions_read"])}份结论；初始16项已有实际证据。',plan['hypothesis'],plan['rules']['allocation'],plan['rules']['composition'],plan['rules']['ledger'],plan['rules']['risk'],'事前54格：BTC_H2份额a=0.25/0.5/0.75，BTC_H6份额1-a，ETH份额1；ETH阈值2/2.5/3%、慢中心S27/28/29、快周期L3/4。4D相邻135边，全部完整spec在reserve前核对三个源参数字典。两个BTC原生均N1000/初始10000，ETH原生N3000/初始10000；银行所有权不等于BTC250/500/750的新订单回测，权重不归一化。','370日连续OOS2025-10-19UTC00:01至2026-10-24UTC00:01；33日上下文含30预热及3日初始embargo。静态规则无拟合/未来标签，purge不适用；12完整30日折加10日尾折，逐折承接现金/q/entry/费用；近期40日由day330继承、8×5日，不重开本金、不产生诊断平仓，仅原终点计费退出。反复使用历史属于开发验证，不是未触碰最终测试。','23旧原生/69成本NAV按已有现金/数量/entry事件恢复并核对原SHA，不重跑信号、成交或资金费。共同纳秒/事件时轴使用最后完成值，逐点组合后重算完整整体回撤及逐折/近期指标，不平均组件指标。两个BTC共享价格和资金费，可重叠或相反，不假定独立或允许跨银行净额。','保留实际源订单成本：每侧5bp费+1bp半价差+2bp滑点+0.5×滞后20日样本log波动×sqrt(实际源订单金额/滞后20日quoteADV)冲击；参与率≤0.1%，tick/lot/最低金额及全额抵押约束。资金费=-有符号q×实际mark×rate，流出随1/2/3倍放大，收入不放大。永续不虚构现货借币；独立银行闭合小时1%维持保证金代理，不作跨银行救助/净额。','门槛固定：全期/近期三档净正、1x完整月≥9/12正折及近期≥6/8、3x完整连续整体DD≤25%、4D邻域全期3x净正≥60%、≥4往返、(参考毛利+资金费)/成本≥2.5、现金/拒单/风险违规0、终点空仓且≥180日。18个旧BTC_H4加同ETH父组合、20k恒多及现金0只读对照；保持旧资格，不评估未登记a=0/1端点。',json.dumps(summary,ensure_ascii=False),'原单S28冻结候选与SMA65从UTC18:30续接至20:30，资金费已在16:00:00.003入账，不重复。19:00闭合小时承接旧18小时风险状态，再处理20:00闭合小时；保留现金/数量/entry/净值完整前缀，不换本轮新组合。下一资金费Oct29UTC00:00、下一日决策00:01。延迟真实闭合行情重建与十策略实时报价账户分开。','背景沿用2026-10-27实际访问的一手[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)与[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)。本组合为研究推论；54个相关新试验及所有先前试验存在多重选择偏差，无DSR/PBO、独立未来验证或稳定实盘盈利证明。','复现工作目录/home/desktop/Documents/Codex/EquiTide。audit.py独立Decimal源事件播放，check_exports.py/check_sources.py核对真实结果，audit_candidate.py/audit_forward.py独立核对原账户，forward.py --reproduce离线复现。不重新reserve/evaluate已完成配置。仅提交轻量必要证据，行情/HTTPpacket留ignoreddata绑定SHA；main非强推并核验完整远端tree/blob/行情后释放本轮锁。'];(R/'result.md').write_text('\n\n'.join(lines)+'\n');print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
