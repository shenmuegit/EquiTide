"""Export saved real native/parent L/F results; no strategy calculation."""
import collections,csv,json,statistics
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import *
r=json.loads((R/'report.json').read_text());p=json.loads((R/'plan.json').read_text());rows={}
def write(name,cols,items):
 with(R/name).open('w',newline='') as f:w=csv.writer(f,lineterminator='\n');w.writerow(cols);w.writerows(items)
 rows[name]=len(items)
cost=[];wf=[];recent=[];daily=[];edges=[];alloc=[];sources=[]
for c in r['configs'].values():
 for k,s in c['scenes'].items():
  cost.append([c['name'],c['fingerprint'],c['scope'],c['role'],c['asset'],c['L'],c['F'],c['capital_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['cost_usdt'],s['cost_pct_initial'],s['funding_usdt'],s['gross_reference_PnL_to_execution_cost'],s['executions'],s['round_trips'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),c['status']])
  wf.extend([c['name'],c['scope'],c['L'],c['F'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['duration_days'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['folds'])
  recent.extend([c['name'],c['scope'],c['L'],c['F'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['recent40']['folds'])
  daily.extend([c['name'],c['scope'],k,i,v] for i,v in enumerate(s['daily_equity_usdt']))
write('cost_scenes.csv',['configuration','fingerprint','scope','role','asset','ETH_fast_L','funding_entry_payment_cap_rate_F','initial_capital','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','cost_usdt','cost_pct_initial','funding_usdt','gross_plus_funding_to_cost','executions','closes','recent40_return_pct','positive5d_folds','status'],cost)
write('walk_forward_folds.csv',['configuration','scope','ETH_fast_L','funding_entry_payment_cap_rate_F','cost_multiplier','fold','start_utc','end_exclusive_utc','days','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],wf)
write('recent40_folds.csv',['configuration','scope','ETH_fast_L','funding_entry_payment_cap_rate_F','cost_multiplier','fold','start_utc','end_exclusive_utc','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],recent)
write('daily_NAV.csv',['configuration','scope','cost_multiplier','boundary','NAV_usdt'],daily)
cols=['ETH_fast_L','funding_entry_payment_cap_rate_F','fingerprint','readonly_old','unchanged_canonical_status','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','recent40_return_pct','positive5d_folds','local_positive3_fraction','local_recent_fraction'];flags={};readonly=[]
for scope,grid,key in [('parent',p['grid'],'all_current_grid'),('native',p['native_grid'],'all_current_native_grid')]:
 full=r[key];items=[]
 for g in grid:
  c=full[g['fingerprint']]
  for k,s in c['scenes'].items():
   d=c['current_grid_diagnostic_sensitivity'];z=[g['L'],g['F'],g['fingerprint'],g['readonly'],c['status'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),d['local_positive3_fraction'],d['local_strict_recent_fraction']];items.append(z)
   if scope=='parent' and g['readonly']:readonly.append(z)
 for k in ['1','2','3']:
  for g in grid:
   i,j=p['lookbacks'].index(g['L']),p['funding_caps'].index(g['F']);ng=[h for h in grid if i<2 and h['L']==p['lookbacks'][i+1] and h['F']==g['F'] or j<2 and h['F']==p['funding_caps'][j+1] and h['L']==g['L']]
   for h in ng:
    a,b=full[g['fingerprint']]['scenes'][k],full[h['fingerprint']]['scenes'][k];edges.append([scope,k,g['L'],g['F'],h['L'],h['F'],g['fingerprint'],h['fingerprint'],abs(a['sharpe_365']-b['sharpe_365']),abs(a['net_return_pct']-b['net_return_pct']),abs(a['max_drawdown_pct']-b['max_drawdown_pct'])])
 flags[scope]={}
 for k in ['1','2','3']:
  v=[x[8] for x in edges if x[0]==scope and x[1]==k];t=2*statistics.stdev(v);flags[scope][k]={'edge_count':len(v),'max_Sharpe_change':max(v),'two_std_change_threshold':t,'descriptive_cliff_flag':max(v)>t,'scope':'Dependentedgeheuristiconly,notstatisticalsignificance,DSRorPBO.'}
 write('sensitivity_grid.csv' if scope=='parent' else 'native_sensitivity_grid.csv',cols,items)
write('readonly_reused_scenes.csv',cols,readonly)
write('adjacent_edges.csv',['scope','cost_multiplier','from_L','from_F','to_L','to_F','from_fp','to_fp','absolute_Sharpe_change','absolute_return_change_pp','absolute_DD_change_pp'],edges)
cs=r['matched_hold_comparisons'];write('matched_hold_comparisons.csv',list(cs[0]),[list(x.values()) for x in cs])
for fp,x in p['read_only_references'].items():
 if x['scope']!='native':continue
 sp=json.loads((ROOT/x['spec']).read_text());old=next(c for c in json.loads((ROOT/x['report']).read_text())['configs'].values() if c['fingerprint']==fp)
 for k,s in old['scenes'].items():sources.append([fp,x['asset'],x['capital_usdt'],sp['parameters']['fixed_entry_notional_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['cost_usdt'],s['funding_usdt'],s['executions'],s['NAV_sha256_f64le'],x['report'],x['report_sha256']])
write('source_curves.csv',['fingerprint','asset','actual_bank_capital','actual_entry_N','cost_multiplier','return_pct','whole_DD_pct','cost_usdt','funding_usdt','executions','NAV_sha256','readonly_report','readonly_report_sha256'],sources)
for g in p['grid']:alloc.append([g['fingerprint'],'candidate',g['L'],g['F'],3750,15000,18750,375,4500,1,1,.2,.8,g['readonly']])
alloc.append([p['benchmark_parent_fingerprint'],'matched_initial_budget_hold',None,None,3750,15000,18750,375,4500,1,1,.2,.8,True]);write('fixed_allocations.csv',['fingerprint','role','ETH_L','funding_entry_payment_cap_rate_F','BTC_bank','ETH_bank','total_initial_capital','BTC_N','ETH_N','raw_BTC_weight','raw_ETH_weight','BTC_capital_share','ETH_capital_share','readonly'],alloc)
put(R/'edge_flags.json',flags)
fig,axs=plt.subplots(2,4,figsize=(16,9),layout='constrained')
for row,(scope,key) in enumerate([('ETH native15000/N4500','all_current_native_grid'),('BTC3750+ETH15000 parent','all_current_grid')]):
 full=r[key]
 for j,(label,fn) in enumerate([('3x continuous370 return %',lambda c:c['scenes']['3']['net_return_pct']),('3x wholecurve DD %',lambda c:c['scenes']['3']['max_drawdown_pct']),('3x daily Sharpe365',lambda c:c['scenes']['3']['sharpe_365']),('3x recent positive5d /8',lambda c:sum(f['net_return_pct']>0 for f in c['scenes']['3']['recent40']['folds']))]):
  arr=np.empty((3,3))
  for c in full.values():arr[p['lookbacks'].index(c['L']),p['funding_caps'].index(c['F'])]=fn(c)
  ax=axs[row,j];im=ax.imshow(arr,cmap='RdYlGn_r' if j==1 else 'RdYlGn',**({'vmin':0,'vmax':8} if j==3 else {}));ax.set_xticks(range(3),['0bp','1bp','OFF']);ax.set_yticks(range(3),['L3','L4','L5']);ax.set_xlabel('Latest known funding payment cap F');ax.set_ylabel('ETH fast lookback L');ax.set_title(scope+'\n'+label,fontsize=10)
  for c in full.values():i,k=p['lookbacks'].index(c['L']),p['funding_caps'].index(c['F']);ax.text(k,i,f'{arr[i,k]:.3f}'+(' O' if c['readonly'] else ' N'),ha='center',va='center',fontsize=9)
  fig.colorbar(im,ax=ax,shrink=.7)
fig.suptitle('ETH fastL3/4/5 x last funding cap0/1bp/OFF, fixed slowS28, fixedH2.5%, E0.25%, V10/cap4.5%\nActualBTC3750/N375 andETH15000/N4500 | rawweights[1,1],shares20/80%,noNAVscaling | O=readonly,N=new | reuseddevelopmenthistory')
fig.savefig(R/'sensitivity.png',dpi=140);plt.close(fig)
s={'report_sha256':sha(R/'report.json'),**p['expected_counts'],'passed':len(r['summary']['passed']),'rejected':len(r['summary']['candidate_rejected']),'failed_criteria':dict(collections.Counter(f for c in r['configs'].values() for f in c['failed_criteria'])),'CSV_rows':rows,'edge_flags':flags};put(R/'sensitivity_summary.json',s)
ctx=json.loads((R/'context.json').read_text());eq=[]
for c in r['configs'].values():
 grid=p['native_grid'] if c['scope']=='native' else p['grid'];key='all_current_native_grid' if c['scope']=='native' else 'all_current_grid';off=next(g for g in grid if g['L']==c['L'] and g['F'] is None);base=r[key][off['fingerprint']];eq.append({'name':c['name'],'fingerprint':c['fingerprint'],'scope':c['scope'],'L':c['L'],'F':c['F'],'matched_OFF_fingerprint':off['fingerprint'],'identical_full_NAV_by_cost':{k:c['scenes'][k]['NAV_sha256_f64le']==base['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3']},'all_cost_NAV_identical':all(c['scenes'][k]['NAV_sha256_f64le']==base['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3'])})
put(R/'equivalent_realized_NAV_paths.json',{'report_sha256':sha(R/'report.json'),'comparisons':eq,'policy':'Parameter novelty is not independent financial evidence; identical full paths are explicitly retained and not counted as new alpha. Canonical qualifications unchanged.'})
lines=['# 单次滞后资金费入场过滤验证','',f"完整读取{ctx['registry_events']}登记事件/{ctx['registry_ids']}ID、{len(ctx['prior_conclusions_read'])}份结论，初始16项真实证据齐全。本轮L3/4/5×资金费支付率上限F=0/1bp/OFF；OFF三个原生/三个父格点和匹配持有父及来源共10唯一旧定义只读。6个新ETH组件+6个新组合、36成本场景，均先逐个reserve成功再实际计算并finish；全部正负结果保存。",'',
'经济假设：最近已可得资金费的支付方向或反映拥挤，避免新开付费方向可能减少拖累，但也可能损失有利价格走势。历史已有六次结算均值、E−1%、多数慢门、无V10等配置；本轮最近1次、E+0.25%、始终slow28/V10与资金配置不同，精确查重后允许新测试。未把family相同视为重复。','',p['hypothesis'],'',
'完整价格规则：ETH快ROC=C[i−1]/C[i−1−L]−1，L3/4/5、H2.5%；严格>H空、<−H多，带内实际多仅ROC<0.25%、实际空仅ROC>−0.25%保留，等号退出。绝对slow28方向不匹配始终退出；当前V10样本logvol>4.5%只过滤新开/翻向。之后仅非零且与实际持仓方向不同的desired才检验direction×历史realized_rate<=F，F0/0.0001，按每次结算原率不是年化/本金/权重；同向保留和必须退出不受资金费门控阻止。OFF=None完全等价旧规则，不查资金费信号。无BTC收益控制或连续确认。','',
'特征从1212条完整真实历史选最新settlement，要求settlement<=当日00且available+3600秒<=00、源年龄<=16h；空缺/过期则blocked，不补0。normalized available本来为settlement+1小时，再加固定1小时，合计保守2小时模型延迟，不是官方标准或已验证的历史网络到达；00刚结算费率不得进入00信号。历史费率不预测/保证下一结算成本。实际未来资金费依每次真实settlement/rate/mark/当时q记账，信号费率不随1/2/3成本压力放大。','',
'BTC独立银行原ROC31/H4%/E1%真实3750本金/N375路径只读；ETH15000本金/N4500，按前完整ETHclose除以LOT向下取整，下一00:01原生OPEN不利tick，翻向先平后开，终止成本平仓。原[1,1]是两完整银行美元NAV相加，总本金18750；20%/80%只是初始份额，不再次乘权重，不归一化、父调仓、转账、跨抵押、NAV复利或线性缩放旧路径。','',
'真实区间2025-10-19UTC00:01至2026-10-24UTC00:01连续370天、12完整30日折+10日尾段，现金/q/成本跨折保持，近期40天继承day330/8×5天。固定无训练/标签，purge0、预热30+间隔3；信号、ADV/logvol与资金费源严格遵守过去可得性。该历史已反复开发，全部试验计数见context，不称未触碰最终OOS/DSR/PBO显著性或独立未来资格。','',
'失败门槛预先不变：每成本全年净正、1倍>=9/12正完整月；每成本近期净正且>=6/8正5日折；3倍全曲线DD<=25%；L/F索引半径1含中心的局部3倍净正与严格近期支持均>=60%；>=4平仓、毛参考PnL加fund/执行成本>=2.5、零拒单/负抵押/小时维护代理违规、终止flat且>=180天。原生和父分别判断，旧OFF原资格/报告/敏感性不改，只另列当前邻域诊断。','',
'成本每边5bp费用、1bp半价差、2bp滑点、0.5×past20ETH原生样本logvol×sqrt(实际q×OPEN/past20完整quoteADV)冲击，不因过滤缩小成本假设；实际资金费支出1/2/3倍、正收入不放大。原生LOT/tick/minnotional、参与率<=0.001、费用后1倍入场抵押、各银行独立1%闭合小时不利mark维护代理。线性永续无现货借币，不虚构借币费；没有L2/TCA/完整历史阶梯/逐tick清算或容量/实盘证明。匹配本金/初始N持有和现金0%另列，非满仓或同风险持有。','',
'|新配置|范围|L|F每次结算|1倍净%|2倍净%|3倍净%|3倍整体DD%|正月/12|近期正折1/2/3倍|状态|','|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|']
for c in r['configs'].values():lines.append('|'+c['name']+'|'+c['scope']+f"|{c['L']}|{c['F']*10000:.0f}bp|"+'|'.join(f"{c['scenes'][k]['net_return_pct']:.6f}" for k in ['1','2','3'])+f"|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['positive_complete_30d_folds_1x']}|"+'/'.join(str(c['recent40_positive_5d_folds_by_cost'][k]) for k in ['1','2','3'])+'|'+c['status']+'|')
lines += ['',f"新父候选{len(r['summary']['passed'])}历史通过、{len(r['summary']['candidate_rejected'])}淘汰。全新配置失败原因{ {c['name']:c['failed_criteria'] for c in r['configs'].values()} }。所有负收益/负期间同样留档，不按全年收益放宽近期或邻域门槛。",'',
f"同L/同资金OFF对照：{sum(x['all_cost_NAV_identical'] for x in eq)}/{len(eq)}个新配置三成本完整NAV哈希完全相同，详细匹配在equivalent_realized_NAV_paths.json。新参数不等于新独立alpha，不重跑旧组件或据路径相同删结果/改资格。",'',
'11CSV保存36场景、逐月/尾折/近期折、每日NAV、两张完整9格敏感性、72相邻边、持有/现金、旧来源及原分配；完整NAV哈希及必要逐笔/funding/状态段与父源哈希可独立重建。两面八指标图、Sharpe正比例/多指标/边界/描述性2std悬崖不等于统计显著性，不按结果扩展本批阈值。CSV资金费率以0、0.0001和空值None=OFF表达，图用0bp/1bp/OFF。','',
'合成TDD旧代码不能阻止已知付费新多仓，预期红灯后验证多/空支付符号、阈值等号、available+extra1h等号、未来费率扰动、持仓保留/退出/失败翻向/OFF恒等。独立Fraction审计从原历史按时刻重新选择来源并验证信号最大可得性；Decimal重建实际现金/数量/成本/资金费/全NAV，不调用simulate/decide/trade重跑。','',
'原SMA/singleS28冻结账户续18:30至20:30，独立未过滤L4/H2续20:10至22:10且22:11参考闭合后采集；保留完整cash/q/desired/risk/NAV前缀、16已计资金费不重记。新funding筛选不注入原账户，partial rejected继续长期原计划，延迟shadow不当十策略真实报价成交。','',
'一手来源2026-11-01实际复查：[Binance官方资金费历史API](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)。原率/settlement/mark有真实哈希，官方文档没有证明历史网络发布延迟或本策略收益，availability模型假设单列primary_sources和funding_data_availability。','',
'同main排他锁内登记/汇总/提交；监控只读既有账户与报告，不产生成交、不改冻结规则/本金/持仓，不部署网页/建定时任务，不下真实订单。']
(R/'result.md').write_text('\n'.join(lines)+'\n');print(json.dumps(s),flush=True)
