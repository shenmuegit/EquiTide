"""Export all a/HA/HB/S combinations and matched single-component historical controls."""
import copy,csv,gzip,io,itertools,json,statistics
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run import ROOT,R,WEIGHTS,HURDLES,SLOWS,axes,grid_configs,anchor_configs,sha,put

def table(path,rows,compress=False):
 fields=list(dict.fromkeys(k for row in rows for k in row));b=io.StringIO(newline='');w=csv.DictWriter(b,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows);path.write_bytes(gzip.compress(b.getvalue().encode(),mtime=0) if compress else b.getvalue().encode())
def all_configs(report,plan):
 h=plan['read_only_hold_references']['COMBO'];c=copy.deepcopy(json.loads((ROOT/h['report']).read_text())['configs'][h['name']]);c.update(read_only_anchor=True,scope='parent',asset='COMBO',capital_usdt=20000);out={**anchor_configs(),**report['configs'],c['name']:c}
 for c in out.values():
  for z in c['scenes'].values():
   if 'recent40' not in z:z['recent40']=copy.deepcopy(z['extension40'])
 return out
def main():
 assert not(R/'finish_verification.json').exists();r=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text());grid=grid_configs(r['configs']);controls=anchor_configs();allby=all_configs(r,plan);hold=allby[plan['read_only_hold_references']['COMBO']['name']];assert len(grid)==54 and len(allby)==82;rows=[];folds=[];recent=[];daily=[];comp=[];edges=[]
 for c in allby.values():
  old=c.get('read_only_anchor',False);meta={'name':c['name'],'scope':'parent','asset':'COMBO','role':c['role'],'read_only_anchor':old,'capital_usdt':20000}
  if not old:meta.update({p:c[p] for p in axes(c)})
  for k,z in c['scenes'].items():
   rows.append({**meta,'cost_multiplier':int(k),'status':c['status'],**{p:z[p] for p in ['net_return_pct','max_drawdown_pct','daily_mark_drawdown_pct','sharpe_365','calmar','cost_usdt','cost_pct_initial','funding_usdt','gross_reference_PnL_to_execution_cost','executions','round_trips','NAV_sha256_f64le']},**{'recent40_'+p:z['recent40'][p] for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','NAV_sha256_f64le']},**{'cost_'+p:v for p,v in z['cost_parts_usdt'].items()}});folds.extend({**meta,'cost_multiplier':int(k),**f} for f in z['folds']);recent.extend({**meta,'cost_multiplier':int(k),**f} for f in z['recent40']['folds'])
   if old:continue
   daily.extend({**meta,'cost_multiplier':int(k),'boundary_index':j,'equity_usdt':v} for j,v in enumerate(z['daily_equity_usdt']))
   refs=[('matched_single_A_L3or4',next(x for x in controls.values() if x['trend_filter_lookback_days']==c['trend_filter_lookback_days'] and x['reversal_return_hurdle']==c['reversal_return_hurdle'] and x['reversal_lookback_days']==c['ETH_A_lookback_days'])),('matched_single_B_L5',next(x for x in controls.values() if x['trend_filter_lookback_days']==c['trend_filter_lookback_days'] and x['reversal_return_hurdle']==c['reversal_return_hurdle'] and x['reversal_lookback_days']==5)),('same_capital_constant_long',hold)]
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
 for LA,a in itertools.product([3,4],WEIGHTS):
  fig,axs=plt.subplots(3,2,figsize=(12,10),layout='constrained')
  for i,field in enumerate(['net_return_pct','sharpe_365','max_drawdown_pct']):
   vals=[(by[a,H,S,LA]['scenes']['3']['recent40'] if rr else by[a,H,S,LA]['scenes']['3'])[field] for H,S,rr in itertools.product(HURDLES,SLOWS,[False,True])];limit=max(abs(x) for x in vals) or 1
   for j,rr in enumerate([False,True]):
    mat=np.asarray([[(by[a,H,S,LA]['scenes']['3']['recent40'] if rr else by[a,H,S,LA]['scenes']['3'])[field] for S in SLOWS] for H in HURDLES]);im=axs[i,j].imshow(mat,aspect='auto',cmap='RdYlGn_r' if field=='max_drawdown_pct' else 'RdYlGn',vmin=0 if field=='max_drawdown_pct' else -limit,vmax=limit);axs[i,j].set_title(('Inherited40days' if rr else '370days')+' /3x '+field);axs[i,j].set_xticks(range(3),SLOWS);axs[i,j].set_yticks(range(3),[100*H for H in HURDLES]);axs[i,j].set_xlabel('Shared ETH slowcenter S(days)');axs[i,j].set_ylabel('Shared ETH hurdle H(percent)')
    for x,y in itertools.product(range(3),range(3)):axs[i,j].text(y,x,f'{mat[x,y]:+.3f}',ha='center',va='center')
    fig.colorbar(im,ax=axs[i,j])
  fig.suptitle(f'BTC1 + ETH L{LA}({a:g}) + L5({1-a:g});shared H/S\ncapital20000,budget4000;source N1000/3000/3000;known development history');fig.savefig(R/f'sensitivity_LA{LA}_A{int(a*100):02d}.png',dpi=120);plt.close(fig)
 counts={'cost':len(rows),'full_folds':len(folds),'recent40_folds':len(recent),'daily_NAV':len(daily),'edges':len(edges),'reference_comparisons':len(comp)};assert list(counts.values())==[246,3198,1968,60102,135,486]
 for name,data,z in [('sensitivity.csv',rows,False),('fold_results.csv',folds,False),('recent40_fold_results.csv',recent,False),('daily_equity.csv.gz',daily,True),('joint_edges.csv',edges,False),('reference_comparisons.csv',comp,False)]:table(R/name,data,z)
 cs=list(r['configs'].values());summary={'new_financial_configs':54,'new_native_components':0,'new_passive_parents':54,'candidate_configs':54,'benchmark_configs':0,'passed_candidates':len(r['summary']['passed']),'rejected_candidates':len(r['summary']['rejected']),'positive_configs_by_cost':r['summary']['positive_configs_by_cost'],'failed_criteria_counts':dict(Counter(p for c in cs for p in c['failed_criteria'])),'rows':counts,'by_slow_center':{str(S):{'candidates':18,'passed':sum(c['trend_filter_lookback_days']==S and c['status']=='passed' for c in cs),'recent6of8':sum(c['trend_filter_lookback_days']==S and c['recent40_positive_5d_folds_1x']>=6 for c in cs),'full3x_positive_Sharpe_fraction':sum(c['trend_filter_lookback_days']==S and c['scenes']['3']['sharpe_365']>0 for c in cs)/18} for S in SLOWS}};put(R/'summary.json',summary);ctx=json.loads((R/'context.json').read_text());lines=[f'# {R.name} ETH快周期L3/4与L5的静态份额分散验证',f'实际54新组合，历史通过{summary["passed_candidates"]}、淘汰{summary["rejected_candidates"]}。完整读取{ctx["registry_events"]}事件/{ctx["registry_ids"]}ID与{len(ctx["prior_conclusions_read"])}份结论；初始16项均有实际证据。',plan['hypothesis'],plan['rules']['allocation'],plan['rules']['composition'],plan['rules']['ledger'],plan['rules']['risk'],'事前4D54格：ETH_A份额a0.25/0.5/0.75、共享入场H2/2.5/3%、共享慢中心S27/28/29、A快周期3/4，B固定5日，135相邻边。原生三参数字典完整写入spec并在reserve前检查。新组合不等于ETH750/1500/2250小订单重估；所有权原值不归一化。','30旧原生/90成本NAV仅回放已有现金/q/entry账本并核对原完整NAV SHA，不重跑旧信号/订单/资金费模型，也不新增父层成交。共享(ns,eventcode)因果时轴取最后完成值，逐点所有权组合后重算净收益、完整整体回撤、Sharpe、Calmar及逐折指标。两ETH账户可能重叠或相反，不净额抵消或假定统计独立。','8真实合并Parquet及16年度/近期源SHA/字节固定。370日OOS2025-10-19UTC00:01至2026-10-24UTC00:01；33日上下文含30预热与3日初始embargo。静态规则无拟合/未来标签，purge不适用；12完整30日折加10日尾折连续承接现金/q/entry/成本，近期40从day330继承分8×5日，不重开本金/诊断平仓，仅原终点计费退出。此反复使用历史属于开发验证，非未触碰最终测试。','成本保留实际源订单：每侧5bp手续费+1bp半价差+2bp滑点+0.5×滞后20日日log波动×sqrt(实际native订单金额/滞后20日quoteADV)冲击，参与率≤0.1%，不利tick/lot/最小金额/全额抵押约束。资金费=-有符号q×实际mark×rate，流出乘1/2/3、收入不放大；永续不虚构现货借币。独立银行闭合小时1%维持保证金为风险代理，缺L2/TCA/完整历史tier/tick清算及聚合容量证明。','固定门槛：全期/近期三档净正、1x月正折≥9/12及近期≥6/8、3x完整连续整体DD≤25%、4D邻域全期3x净正≥60%、≥4往返、(参考毛利+资金费)/成本≥2.5、现金/拒单/独立风险违规0、终点空仓且≥180日。27个旧单ETH父组合及同本金恒多只读，匹配A原周期和B5日原组合/同H/S比较，旧状态保持。全期源父组合均正会数学上产生正的凸组合，不能据此推断新增独立alpha；主要问题为近期时间覆盖和风险。',json.dumps(summary,ensure_ascii=False),'原单S28候选与SMA65从Oct28UTC22:30跨日至Oct29UTC00:30；实际00:00资金费、00:01日决策按原规则/原金额续接，更新35日候选/65日SMA上下文、保留完整净值前缀、资金费/交易和00小时风险栈，不换本轮组合、不重开本金、不强制截止平仓。下一小时必须检查当前00小时资金费/决策前后风险状态，下一资金费08:00、下一日决策Oct30UTC00:01。延迟闭合行情重建与paper10实时报价模拟分开。','背景沿用2026-10-27实际访问的一手[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)及[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)。本组合假设为研究推论。54个相关新试验及所有先前试验存在多重选择偏差，无DSR/PBO、独立未来资格或稳定实盘盈利证明。','复现工作目录/home/desktop/Documents/Codex/EquiTide。audit.py独立Decimal源事件播放及逐点/逐折核对；check_exports.py/check_sources.py/check_feed.py只读数字和SHA；audit_candidate.py/audit_forward.py独立跨日核验，forward.py --reproduce离线复现。不得重新reserve/evaluate已完成精确配置。正负结果、完整账户账本、规则和失败均留档，行情/HTTPpacket留ignoreddata绑定SHA；main非强推并核验完整远端tree/blob/数据后释放自己锁。'];(R/'result.md').write_text('\n\n'.join(lines)+'\n');print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
