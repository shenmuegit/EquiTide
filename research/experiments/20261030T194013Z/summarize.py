import csv,itertools,json,math
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import *
from run import positive_recent,stress_fold_ok
from controls import reference
r=json.loads((R/'report.json').read_text());assert json.loads((R/'verification.json').read_text())['passed'];cs=r['configs'];ref=reference();allc={**cs,ref['name']:ref};cost=[];folds=[];recent=[];daily=[];edges=[];comparisons=[];cols=['net_return_pct','max_drawdown_pct','sharpe_365','calmar']
for c in allc.values():
 for k,s in c['scenes'].items():
  cost.append({'name':c['name'],'scope':c['scope'],'entry_z':c['entry_z'],'exit_z':c['exit_z'],'capital_usdt':20000,'cost_multiplier':int(k),'status':c['status'],'read_only_reference':bool(c.get('read_only_reference')),**{z:s[z] for z in cols},'recent40_return_pct':s['recent40']['net_return_pct'],'recent40_DD_pct':s['recent40']['max_drawdown_pct'],'positive_complete30d_folds':sum(f['net_return_pct']>0 for f in s['folds'][:12]),'positive_recent5d_folds':sum(f['net_return_pct']>0 for f in s['recent40']['folds']),'round_trips':s['round_trips'],'executions':s['executions'],'cost_usdt':s['cost_usdt'],'cost_pct_initial':s['cost_pct_initial'],'funding_usdt':s['funding_usdt'],'gross_plus_funding_to_cost':s['gross_reference_PnL_to_execution_cost'],'NAV_sha256_f64le':s['NAV_sha256_f64le'],'NAV_points':s['NAV_points']})
  for dest,ff in [(folds,s['folds']),(recent,s['recent40']['folds'])]:
   for f in ff:dest.append({'name':c['name'],'cost_multiplier':int(k),'fold':f['fold'],'duration_days':f['duration_days'],'start_utc':f['start_utc'],'end_exclusive_utc':f['end_exclusive_utc'],**{z:f[z] for z in cols}})
  if c['name'] in cs:
   for i,v in enumerate(s['daily_equity_usdt']):daily.append({'name':c['name'],'cost_multiplier':int(k),'day_boundary_index':i,'NAV_usdt':v})
for c in cs.values():
 for axis,values in [('entry_z',ENTRIES),('exit_z',EXITS)]:
  i=values.index(c[axis])
  if i==2:continue
  other=next(x for x in cs.values() if x[axis]==values[i+1] and x['exit_z' if axis=='entry_z' else 'entry_z']==c['exit_z' if axis=='entry_z' else 'entry_z']);a,b=c['scenes']['3'],other['scenes']['3'];edges.append({'axis':axis,'from_name':c['name'],'to_name':other['name'],'return_change3_pct':b['net_return_pct']-a['net_return_pct'],'DD_change3_pct':b['max_drawdown_pct']-a['max_drawdown_pct'],'Sharpe_change3':b['sharpe_365']-a['sharpe_365'] if b['sharpe_365'] is not None and a['sharpe_365'] is not None else None})
 for k,s in c['scenes'].items():
  b=ref['scenes'][k];comparisons.append({'name':c['name'],'cost_multiplier':int(k),'reference':ref['name'],'new_return_pct':s['net_return_pct'],'reference_return_pct':b['net_return_pct'],'return_difference_pct':s['net_return_pct']-b['net_return_pct'],'new_DD_pct':s['max_drawdown_pct'],'reference_DD_pct':b['max_drawdown_pct'],'same_funded_capital':True,'equal_risk_or_notional_match':False,'new_NAV_points':s['NAV_points'],'reference_original_NAV_points':b['NAV_points']})
rows={'cost_results':cost,'walk_forward_folds':folds,'recent40_folds':recent,'daily_NAV':daily,'sensitivity_edges':edges,'reference_comparisons':comparisons};expected={'cost_results':30,'walk_forward_folds':390,'recent40_folds':240,'daily_NAV':10017,'sensitivity_edges':12,'reference_comparisons':27};exports={}
for n,rr in rows.items():
 assert len(rr)==expected[n];p=R/(n+'.csv')
 with p.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rr[0]),lineterminator='\n');w.writeheader();w.writerows(rr)
 exports[n]={'path':rel(p),'rows':len(rr),'sha256':sha(p)}
fig,axes=plt.subplots(2,3,figsize=(17,9));fns=[('3x full net %',lambda c:c['scenes']['3']['net_return_pct']),('3x continuous max DD %',lambda c:c['scenes']['3']['max_drawdown_pct']),('3x daily Sharpe',lambda c:c['scenes']['3']['sharpe_365']),('3x Calmar',lambda c:c['scenes']['3']['calmar']),('3x recent40 net %',lambda c:c['scenes']['3']['recent40']['net_return_pct']),('Minimum positive5d folds 1/2/3x',lambda c:min(positive_recent(c,k) for k in ['1','2','3']))]
for ax,(title,fn) in zip(axes.flat,fns):
 matrix=np.array([[fn(next(c for c in cs.values() if c['entry_z']==E and c['exit_z']==X)) for X in EXITS] for E in ENTRIES],dtype=float);im=ax.imshow(np.ma.masked_invalid(matrix),cmap='viridis',aspect='auto');ax.set_xticks(range(3),EXITS);ax.set_yticks(range(3),ENTRIES);ax.set_xlabel('Exit crossing Z threshold');ax.set_ylabel('Entry absolute Z threshold');ax.set_title(title);fig.colorbar(im,ax=ax)
 for i,j in itertools.product(range(3),repeat=2):ax.text(j,i,'NA' if not np.isfinite(matrix[i,j]) else f'{matrix[i,j]:.2f}',ha='center',va='center',color='white')
fig.suptitle('BTC/ETH relative-price OLS720; 24-bar training embargo; repeated development history');fig.tight_layout();png=R/'sensitivity.png';fig.savefig(png,dpi=125);plt.close(fig)
center=next(c for c in cs.values() if c['entry_z']==2.5 and c['exit_z']==1);s3=center['scenes']['3'];rep={'name':center['name'],'fingerprint':center['fingerprint'],'selection':'Prespecified2.5/1,notbestPnL','status':center['status'],'net_return_by_cost':{k:s['net_return_pct'] for k,s in center['scenes'].items()},'return3_pct':s3['net_return_pct'],'whole_DD3_pct':s3['max_drawdown_pct'],'recent_return3_pct':s3['recent40']['net_return_pct'],'positive_recent_folds_by_cost':{k:positive_recent(center,k) for k in ['1','2','3']},'completed_pairs1x':center['scenes']['1']['round_trips'],'sensitivity':center['sensitivity'],'failed_criteria':center['failed_criteria']};put(R/'representative.json',rep)
sharpechanges=[x['Sharpe_change3'] for x in edges if x['Sharpe_change3'] is not None];threshold=2*float(np.std(sharpechanges)) if sharpechanges else None;cliffs=[x for x in edges if x['Sharpe_change3'] is not None and threshold is not None and abs(x['Sharpe_change3'])>threshold];summary={'report_sha256':sha(R/'report.json'),'exports':exports,'figure':{'path':rel(png),'sha256':sha(png),'panels':6},'candidate_cells':9,'passed':len(r['summary']['passed']),'rejected':len(r['summary']['rejected']),'positive_configs_by_cost':r['summary']['positive_configs_by_cost'],'strict_individual_recent_passes':sum(stress_fold_ok(c) for c in cs.values()),'failed_criterion_counts':dict(Counter(k for c in cs.values() for k in c['failed_criteria'])),'positive_Sharpe_fraction3':sum(c['scenes']['3']['sharpe_365'] is not None and c['scenes']['3']['sharpe_365']>0 for c in cs.values())/9,'edges':12,'cliffs_heuristic':cliffs,'global_optimum_not_claimed':True};put(R/'sensitivity_summary.json',summary)
text='''# BTC/ETH 小时相对价格回归价差

本轮9个联合双币策略配置、27个1/2/3成本场景均先reserve才实际计算。每配置是一个耦合双腿状态机，两银行账本属于内部证据，不冒充独立单币策略。固定滚动720小时logETH对logBTC含截距OLS，训练窗口排除被测闭合小时及之前24个完整小时，残差sample std(ddof1)标准化当前Z；训练只用当时可得价格，不拟合未来收益/标签，purge0，无ADF或协整盈利保证。33日上下文覆盖首个720+24+1小时；并非把旧方向倒置后宣称复刻作者业绩。

固定入场|Z|2/2.5/3×退出 crossing0.5/1/1.5，中心2.5/1事前确定。eligible beta[0.5,2]且有效std；Z>=E空ETH多BTC、Z<=-E反向。旧仓最多48小时，invalidfit/timeout平仓且同小时不重开；否则反向新阈值先平后反手，多价差Z>=-X退出、空价差Z<=X退出，防止跳过零点仍保留。保持原数量不重平衡。BTC先成交、ETH后成交；首腿拒绝则跳过另一腿，第二腿拒绝则付费尝试平掉第一腿，未平部分进入后续小时close-only恢复，不虚构原子成交或免费回滚。终止退出亦计成本。

各银行10000USDT，总20000；ETH每次目标名义2000，BTC为入场beta×2000，使用闭合小时价格先floor原生LOT，再在下一个h:01真实分钟OPEN成交。原值银行单位[1,1]不归一化，不按NAV扩仓、不转账、不跨账户抵押/费用净额抵消。beta合格时总目标名义3000至6000即初始总本金15%至30%，实际价格、LOT和空仓影响暴露；不称真正市场/美元中性。

370日连续OOS为2025-10-19UTC00:01至2026-10-24UTC00:01，真实8Parquet、404日数据；滚动拟合每小时更新，仅用截至当时的训练窗。12完整30日折+10日尾折，近期40日继承day330现金/持仓、8×5日不重开账户。新增小时参考价/交易事件与分钟/小时mark、真实纳秒资金费对齐，完整570543点NAV计算全期回撤，未用最大单折代替整体回撤。

沿用已验证native Decimal费用：每侧5bp手续费、1bp半价差、2bp滑点、0.5×滞后20完整日样本日对数波动×sqrt(实际q×OPEN/滞后quoteADV)冲击，LOT/minnotional、不利tick、参与率<=0.1%、付费后1x全抵押进入约束。真实永续资金费按实际纳秒/mark/旧持仓，负支出×成本倍数、收入不放大，无现货借币费。每银行独立1%闭合小时不利mark保证金代理；不模拟新的盘中清算成交，风险违规淘汰。首尾未闭合完整小时风险范围、历史过滤/档位、L2/TCA、真实容量/逐tick清算均不足，不称实盘安全或稳定盈利。

旧9个OLS/ADF模型已有真实结果，未重跑：其logBTC对logETH/ADF门槛/资本和时段等与本批完整规则不同。本轮完整登记与243历史结论已读，初始16项实际证据完整。反复使用的历史仍为开发验证，无未触碰最终测试、DSR/PBO或独立未来收益证据。

门槛保持：各成本全期/近期净正、1x完整月折>=9/12、各成本近期正5日折>=6/8、局部3x净正/严格率各>=60%、完整DD3<=25%、>=4个完整双腿往返、毛参考PnL加资金费/执行成本1x>=2.5，无负银行现金/拒单/保证金代理违规，终止双腿平仓且>=180天。完成双腿往返与单腿平仓次数分别保存，避免重复计数。

'''
text+=f"9项通过{summary['passed']}、淘汰{summary['rejected']}；1/2/3倍全期净正数量"+'/'.join(str(r['summary']['positive_configs_by_cost'][k]) for k in ['1','2','3'])+'。全部负收益保留。\n\n|E|X|状态|1x净收益%|2x%|3x%|完整DD3%|Sharpe3|Calmar3|近期3x%|1/2/3正5日折|完整pair往返1x|\n|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---|---:|\n'
for E,X in itertools.product(ENTRIES,EXITS):
 c=next(c for c in cs.values() if c['entry_z']==E and c['exit_z']==X);ss=c['scenes'];z=ss['3'];text+=f"|{E}|{X}|{c['status']}|{ss['1']['net_return_pct']:.6f}|{ss['2']['net_return_pct']:.6f}|{z['net_return_pct']:.6f}|{z['max_drawdown_pct']:.6f}|{z['sharpe_365']:.6f}|{z['calmar']:.6f}|{z['recent40']['net_return_pct']:.6f}|"+'/'.join(str(positive_recent(c,k)) for k in ['1','2','3'])+f"|{ss['1']['round_trips']}|\n"
text+=f"\n事前中心2.5/1净收益1/2/3倍为"+'/'.join(f"{rep['net_return_by_cost'][k]:.6f}%" for k in ['1','2','3'])+f"，完整DD3 {rep['whole_DD3_pct']:.6f}%，近期40日3x {rep['recent_return3_pct']:.6f}%。\n\n"
text+='同本金旧常持B1000/E2000组合只读比较，原始545013点报告/资格/成本/NAV不改；其名义与风险、标记时钟均与本策略不同，不能称同暴露改善。现金0%只是数学基准。六CSV保留逐成本、逐折、近期、日NAV、相邻边和比较，六面板图同时展示收益/DD/Sharpe/Calmar/近期/折数；不会根据孤立边缘收益选择参数或放宽成本。\n\n'
text+='来源：[作者OLS/ADF配对仓库](https://github.com/Bauch0430/crypto-pairs-trading-btc-eth)仅概念与旧规则背景，非复刻或外部盈利验证；[statsmodels滚动回归官方文档](https://www.statsmodels.org/stable/examples/notebooks/generated/rolling_ls.html)说明窗口对齐，本轮显式移位和训练间隔独立固定；[Binance官方资金费资料](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)。访问失败的论文页面如实留档，未引用其未读取内容。\n'
(R/'result.md').write_text(text);print(json.dumps(summary),flush=True)
