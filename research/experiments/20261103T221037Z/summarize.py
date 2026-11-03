"""Saved native/parent S/E surfaces, all folds, controls and provenance; no simulation."""
import collections,csv,json,statistics
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import *
r=json.loads((R/'report.json').read_text());p=json.loads((R/'plan.json').read_text());rows={}
def write(name,cols,items):
 with (R/name).open('w',newline='') as f:w=csv.writer(f,lineterminator='\n');w.writerow(cols);w.writerows(items)
 rows[name]=len(items)
cost=[];wf=[];recent=[];daily=[];edges=[];sources=[];alloc=[]
for c in r['configs'].values():
 for k,s in c['scenes'].items():
  cost.append([c['name'],c['fingerprint'],c['scope'],c['role'],c['asset'],c['L'],c['H'],c['capital_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['cost_usdt'],s['cost_pct_initial'],s['funding_usdt'],s['gross_reference_PnL_to_execution_cost'],s['executions'],s['round_trips'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),c['status']])
  wf.extend([c['name'],c['scope'],c['L'],c['H'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['duration_days'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['folds'])
  recent.extend([c['name'],c['scope'],c['L'],c['H'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['recent40']['folds'])
  daily.extend([c['name'],c['scope'],k,i,v] for i,v in enumerate(s['daily_equity_usdt']))
write('cost_scenes.csv',['configuration','fingerprint','scope','role','asset','ETH_reversal_L','symmetric_entry_fraction_H','initial_capital','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','cost_usdt','cost_pct_initial','funding_usdt','gross_plus_funding_to_cost','executions','closes','recent40_return_pct','positive5d_folds','status'],cost)
write('walk_forward_folds.csv',['configuration','scope','ETH_reversal_L','symmetric_entry_fraction_H','cost_multiplier','fold','start_utc','end_exclusive_utc','days','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],wf)
write('recent40_folds.csv',['configuration','scope','ETH_reversal_L','symmetric_entry_fraction_H','cost_multiplier','fold','start_utc','end_exclusive_utc','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],recent)
write('daily_NAV.csv',['configuration','scope','cost_multiplier','boundary','NAV_usdt'],daily)
cols=['ETH_reversal_L','symmetric_entry_fraction_H','fingerprint','readonly_old','unchanged_canonical_status','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','recent40_return_pct','positive5d_folds','local_positive3_fraction','local_recent_fraction'];flags={};readonly=[]
for scope,grid,key in [('parent',p['grid'],'all_current_grid'),('native',p['native_grid'],'all_current_native_grid')]:
 full=r[key];items=[]
 for g in grid:
  c=full[g['fingerprint']]
  for k,s in c['scenes'].items():
   d=c['current_grid_diagnostic_sensitivity'];z=[g['L'],g['H'],g['fingerprint'],g['readonly'],c['status'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),d['local_positive3_fraction'],d['local_strict_recent_fraction']];items.append(z)
   if scope=='parent' and g['readonly']:readonly.append(z)
 for k in ['1','2','3']:
  for g in grid:
   i,j=p['lookbacks'].index(g['L']),p['hurdles'].index(g['H']);ng=[h for h in grid if i<2 and h['L']==p['lookbacks'][i+1] and h['H']==g['H'] or j<2 and h['H']==p['hurdles'][j+1] and h['L']==g['L']]
   for h in ng:
    a,b=full[g['fingerprint']]['scenes'][k],full[h['fingerprint']]['scenes'][k];edges.append([scope,k,g['L'],g['H'],h['L'],h['H'],g['fingerprint'],h['fingerprint'],abs(a['sharpe_365']-b['sharpe_365']),abs(a['net_return_pct']-b['net_return_pct']),abs(a['max_drawdown_pct']-b['max_drawdown_pct'])])
 flags[scope]={}
 for k in ['1','2','3']:
  v=[x[8] for x in edges if x[0]==scope and x[1]==k];threshold=2*statistics.stdev(v);flags[scope][k]={'edge_count':len(v),'max_Sharpe_change':max(v),'two_std_change_threshold':threshold,'descriptive_cliff_flag':max(v)>threshold,'scope':'Dependentedge descriptive heuristic only,not significance/DSR/PBO or a posthoc gate.'}
 write('sensitivity_grid.csv' if scope=='parent' else 'native_sensitivity_grid.csv',cols,items)
external=[]
for fp in p['external_control_fingerprints']:
 ref=p['read_only_references'][fp];c=next(x for x in json.loads((ROOT/ref['report']).read_text())['configs'].values() if x['fingerprint']==fp)
 for k,s in c['scenes'].items():external.append([c['name'],fp,ref['capital_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),c['status'],ref['report'],ref['report_sha256']])
write('readonly_reused_scenes.csv',['configuration','fingerprint','capital','cost_multiplier','return_pct','whole_DD_pct','Sharpe365','Calmar','recent40_return_pct','positive5d_folds','unchanged_canonical_status','original_report','report_sha256'],external);write('adjacent_edges.csv',['scope','cost_multiplier','from_L','from_H','to_L','to_H','from_fp','to_fp','absolute_Sharpe_change','absolute_return_change_pp','absolute_DD_change_pp'],edges)
cs=r['matched_hold_comparisons'];write('matched_hold_comparisons.csv',list(cs[0]),[list(x.values()) for x in cs])
for fp,x in p['read_only_references'].items():
 if x['scope']!='native':continue
 sp=json.loads((ROOT/x['spec']).read_text());c=next(z for z in json.loads((ROOT/x['report']).read_text())['configs'].values() if z['fingerprint']==fp)
 for k,s in c['scenes'].items():sources.append([fp,x['asset'],x['capital_usdt'],sp['parameters']['fixed_entry_notional_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['cost_usdt'],s['funding_usdt'],s['executions'],s['NAV_sha256_f64le'],x['report'],x['report_sha256'],True])
for c in r['configs'].values():
 if c['scope']!='native':continue
 for k,s in c['scenes'].items():sources.append([c['fingerprint'],c['asset'],c['capital_usdt'],4500,k,s['net_return_pct'],s['max_drawdown_pct'],s['cost_usdt'],s['funding_usdt'],s['executions'],s['NAV_sha256_f64le'],rel(R/'report.json'),sha(R/'report.json'),False])
write('source_curves.csv',['fingerprint','asset','actual_bank_capital','actual_entry_N','cost_multiplier','return_pct','whole_DD_pct','cost_usdt','funding_usdt','executions','NAV_sha256','provenance_report','report_sha256','readonly_old'],sources)
for g in p['grid']:alloc.append([g['fingerprint'],'candidate',g['L'],g['H'],3750,15000,18750,750,4500,1,1,.2,.8,g['readonly']])
alloc.append([p['benchmark_parent_fingerprint'],'matched_initial_budget_hold',None,None,3750,15000,18750,750,4500,1,1,.2,.8,True]);write('fixed_allocations.csv',['fingerprint','role','ETH_L','symmetric_entry_fraction_H','BTC_bank','ETH_bank','total_initial_capital','BTC_N','ETH_N','raw_BTC_weight','raw_ETH_weight','BTC_capital_share','ETH_capital_share','readonly'],alloc);put(R/'edge_flags.json',flags)
fig,axs=plt.subplots(2,4,figsize=(16,9),layout='constrained')
for row,(scope,key) in enumerate([('ETH native15000/N4500','all_current_native_grid'),('BTC3750/N750+ETH15000/N4500 parent','all_current_grid')]):
 full=r[key]
 for j,(label,fn) in enumerate([('3x continuous370 return %',lambda c:c['scenes']['3']['net_return_pct']),('3x wholecurve DD %',lambda c:c['scenes']['3']['max_drawdown_pct']),('3x daily Sharpe365',lambda c:c['scenes']['3']['sharpe_365']),('3x recent positive5d /8',lambda c:sum(f['net_return_pct']>0 for f in c['scenes']['3']['recent40']['folds']))]):
  arr=np.empty((3,3))
  for c in full.values():arr[p['lookbacks'].index(c['L']),p['hurdles'].index(c['H'])]=fn(c)
  ax=axs[row,j];im=ax.imshow(arr,cmap='RdYlGn_r' if j==1 else 'RdYlGn',**({'vmin':0,'vmax':8} if j==3 else {}));ax.set_xticks(range(3),['H1.25%','H1.75%','H2.25%']);ax.set_yticks(range(3),['L4','L5','L6']);ax.set_xlabel('ETH symmetric reversal entry H (%)');ax.set_ylabel('ETH reversal lookback L (days)');ax.set_title(scope+'\n'+label,fontsize=10)
  for c in full.values():i,k=p['lookbacks'].index(c['L']),p['hurdles'].index(c['H']);ax.text(k,i,f'{arr[i,k]:.3f}'+(' O' if c['readonly'] else ' N'),ha='center',va='center',fontsize=9)
  fig.colorbar(im,ax=ax,shrink=.7)
fig.suptitle('ETH SMA32-gated reversal nearby L4/5/6 x H1.25/1.75/2.25% | fixed E0.5%,V10/cap4.5%\nBTC3750/N750 + ETH15000/N4500 | raw[1,1],capitalshares20/80%,noNAVscaling | All grids N=newnative/parent;oldL4/L5SMA controls outsidegrid | reused history');fig.savefig(R/'sensitivity.png',dpi=140);plt.close(fig)
summary={'report_sha256':sha(R/'report.json'),**p['expected_counts'],'passed':len(r['summary']['passed']),'rejected':len(r['summary']['candidate_rejected']),'failed_criteria':dict(collections.Counter(f for c in r['configs'].values() for f in c['failed_criteria'])),'CSV_rows':rows,'edge_flags':flags};put(R/'sensitivity_summary.json',summary)
ctx=json.loads((R/'context.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');eq=[]
def compare(c,base):
 return {k:{'return_pct':z['net_return_pct'],'whole_DD_pct':z['max_drawdown_pct'],'control_return_pct':base['scenes'][k]['net_return_pct'],'control_DD_pct':base['scenes'][k]['max_drawdown_pct'],'delta_return_to_control_pp':z['net_return_pct']-base['scenes'][k]['net_return_pct'],'delta_DD_to_control_pp':z['max_drawdown_pct']-base['scenes'][k]['max_drawdown_pct'],'new_recent_positive5d':sum(f['net_return_pct']>0 for f in z['recent40']['folds']),'control_recent_positive5d':sum(f['net_return_pct']>0 for f in base['scenes'][k]['recent40']['folds'])} for k,z in c['scenes'].items()}
control_fp=p['primary_control_fingerprint'];ref=p['read_only_references'][control_fp];base=next(c for c in json.loads((ROOT/ref['report']).read_text())['configs'].values() if c['fingerprint']==control_fp)
for c in r['configs'].values():
 if c['scope']!='parent':continue
 eq.append({'name':c['name'],'fingerprint':c['fingerprint'],'L':c['L'],'H':c['H'],'S':32,'E':.005,'N':750,'control_fingerprint':control_fp,'control_report':ref['report'],'control_report_sha256':ref['report_sha256'],'all_cost_NAV_identical':all(s['NAV_sha256_f64le']==base['scenes'][k]['NAV_sha256_f64le'] for k,s in c['scenes'].items()),'cost_comparisons':compare(c,base)})
assert len(eq)==9;put(R/'equivalent_realized_NAV_paths.json',{'report_sha256':sha(R/'report.json'),'comparisons':eq,'scope':'Preset oldL5/H.02/SMA32/E.005 actualcontrol,before newresults,canonicalbroadlocalrejectionretained.Samebank/N,costs/time.No extra financialvaluation.'})
groups={}
for c in r['configs'].values():
 if c['scope']=='parent':groups.setdefault('|'.join(c['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3']),[]).append(c['fingerprint'])
put(R/'prior_grid_NAV_aliases.json',{'new_definitions_matching_a_prior_path':sum(x['all_cost_NAV_identical'] for x in eq),'within_new_parent_grid_alias_groups':[v for v in groups.values() if len(v)>1],'scope':'Fullbank parent hashes only;native and parent capitals not compared as equal.'})
newfps={c['fingerprint'] for c in r['configs'].values()};hist={}
for fp,z in records.items():
 sp=z.get('spec',{});obs=sp.get('family')=='paper-live-portfolio-observation' or sp.get('name','').startswith('forward_snapshot_') or 'observation_terminal_action' in sp.get('parameters',{})
 if fp in newfps or not sp or obs:continue
 hist.setdefault(reg.fingerprint(sp),[]).append(z)
trials={'canonical_prior_research_definitions':len(hist),'registry_marked_actual':sum(any(z.get('result_available') is True for z in zs) for zs in hist.values()),'not_marked_actual':sum(not any(z.get('result_available') is True for z in zs) for zs in hist.values()),'initial16_actual_evidence':16,'new_financial_definitions':18,'new_native_models':9,'new_cost_scenes':54,'observations_excluded':True};put(R/'prior_actual_research_counts.json',trials)
lines=['SMA32 慢门槛下快反转回看与入场阈值的联合验证','',p['hypothesis'],'',f"完整读取{ctx['registry_events']}事件/{ctx['registry_ids']}ID、{len(ctx['prior_conclusions_read'])}份既往结论；初始16有原档实际证据、缺结果0。此前研究定义{trials['canonical_prior_research_definitions']}，标实际{trials['registry_marked_actual']}、未标{trials['not_marked_actual']}，不将全部登记当全部实际回测；大量反复历史研究存在多重选择偏差。",'', '事前固定较近快反转 L4/5/6 日×交错对称入场 H1.25/1.75/2.25%，SMA32、退出E0.5%、entry-onlyV10/cap4.5%固定。r=C[i−1]/C[i−1−L]−1；r>H做空、r<−H做多，入场等号不触发。否则实际多仓只在r<E保留、空仓只在r>−E保留，退出等号平仓。慢门槛为sign(C[i−1]/mean(C[i−32:i])−1)，包含最新完整收盘，零/相反方向flat；仅对新增/反转仓应用波动门槛，原方向仓位不因单独高波动退出。', '', '九个新ETH原生各本金15000/N4500；九个新组合持有完整BTC3750/N750旧银行+对应ETH15000/N4500新银行，raw[1,1]、总本金18750、资金份额20/80%、名义入场占比4/24%。保持原权重，不归一化、不缩放旧净值/真实数量、不平均收益/Sharpe/DD、不跨银行调仓/交叉保证金或转移，0父订单。三项旧SMA32/E0.5%控制L5/H1.5%、L5/H2%、L4/H2%在网格外只读；预定主控制是上轮事前中心L5/H2%。三者原rejected资格及旧宽网格支持33%/22%失败不改，不能混入本轮局部L/H邻域。较窄网格由已见结果启发，即使本轮局部通过也不代替宽网格或独立未来验证。', '', 'Walk-forward：2025-10-19UTC00:01至2026-10-24UTC00:01，连续370日，12×30日完整折+10日尾折；逐折不重置现金/仓位，整体DD来自完整分钟/事件OOS净值。近期40日承接day330实际状态，8×5日。固定规则无拟合/标签、purge0、事前33日线足够SMA32；下一UTC00:01原生OPEN执行，数量按过去完整收盘/LOT算，反手先平后开，终点计成本平仓。属于反复使用的开发历史，不是未触碰最终测试或独立未来验证。', '', '成本：5bp手续费+1bp半价差+2bp滑点+0.5×past20样本logvol×sqrt(实际q×OPEN/past20完整日quoteADV)。1/2/3倍放大执行和资金费支出，资金费收入不放大；实际settlement ns/rate/mark/heldq。LOT/tick/minnotional、参与率<=0.1%、费后1倍入场抵押、独立1%闭合小时不利mark风险代理；永续空头无需现货借币，不虚构借币费用。同资本/N750/4500持有和现金0%对照只读。缺盘口/TCA、历史完整保证金层级/最大量、逐tick强平和容量证明。', '', '固定失败门槛：各成本全年净正；1倍至少9/12正完整月；近期各成本总收益正且>=6/8正5日折；3倍整体DD<=25%；含中心L/H索引半径1邻域，3倍正和严格近期合格比例均>=60%；>=4底层平仓；毛参考PnL+资金费/执行成本>=2.5；0订单/现金/保证金代理违规，终点flat、至少180日。全部18项按同一事前标准裁定，不据结果增格/改门槛。', '', '|新配置|scope|L日数|H比例|1x收益%|2x收益%|3x收益%|3x整体DD%|1x正月|近期正折1/2/3|状态|','|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|']
for c in r['configs'].values():lines.append('|'+ '|'.join([c['name'],c['scope'],str(c['L']),str(c['H']),*[f"{c['scenes'][k]['net_return_pct']:.6f}" for k in ['1','2','3']],f"{c['scenes']['3']['max_drawdown_pct']:.6f}",str(c['positive_complete_30d_folds_1x']),'/'.join(str(c['recent40_positive_5d_folds_by_cost'][k]) for k in ['1','2','3']),c['status']])+'|')
lines.extend(['',f"九个新组合通过{len(r['summary']['passed'])}、淘汰{len(r['summary']['candidate_rejected'])}；九个新原生独立状态列上。逐项失败{ {c['name']:c['failed_criteria'] for c in r['configs'].values()} }。对同SMA32/同E0.5%旧L5/H2%主控制，全成本NAV同路径{sum(x['all_cost_NAV_identical'] for x in eq)}/9，同网格别名另存；不将改名/相同净值当新收益路径。",'', '11CSV保存54成本场景、702月/尾折、432近期折、20034日NAV、两个九格L/H面、9旧SMA控制场景、72相邻边、27持有/现金比较、45新旧原生成本路径及10资金分配。正负折、完整DD/Sharpe/Calmar/成本/成交数全部保留。边界按L4/6与H1.25/2.25%端点核对，相邻cliff仅描述依赖样本，非DSR/PBO显著性或新增裁定标准。', '', '作者一手[SMA趋势估计器论文入口](https://mebfaber.com/white-papers/)与[Binance USD-M市场数据API](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)均于2026-11-03UTC访问。SMA32、快逆势L/H、永续双向/退出/波动过滤是本项目实验，不能移植作者原10月长仓模型收益；官方字段不是成交、盈利或容量证明。8行情/mark/资金费/约束文件的边界/字节/SHA及新旧实现版本见plan/data_manifest。', '', '全部18份spec先分三批reserve成功，才实际计算27原生+27父成本路径；33来源代码在首个reserve前绑定。合成检查覆盖错误双重加权负对照、非平均收益/DD、错位事件轴拒绝、18个L/H邻域、future价格不可见、L4/5/6精确回看、SMA32真实窗口及与ROC端点区分、双向反转、入退场等号与entry-only波动过滤。独立Fraction信号、Decimal真实q/费用/冲击/资金费/小时风险和完整NAV核验后逐项finish，负结果同样留档。', '', '原SMA65和single续18:30→20:30，原L4/H2续20:10→22:10，仅22:11执行参考闭合后采集。下轮L4的22:10→Nov4UTC00:10会跨真实00资金费与00:01冻结日决策，须00:11参考闭合后取得本账户真实结算并完成整日上下文，不能事前假设资金费/持仓或重复00/08/16。原现金/q/desired/cost/risk/context/完整NAV前缀和终止日保持；00/08/16资金费已按各自实际q入账，不得重复；是否有新结算以真实响应/事件核验，不预设为零。无新日线决策，不强制截止平仓或采纳本批研究。原SMA65日线源20261103T020232Z保持，partial不冒充180日/六折；旧延迟shadow与十策略报价模拟分开。', '', '仅清理本轮可重建中间物；保留真实结果/完整账本、登记、冻结规则、spec/代码、原始短窗响应和失败事实。同main排他锁内更新只读监控并非强制push；实际发布终态、远端完整tree/证据哈希和解锁凭据见.git/automation_proofs/'+R.name+'.json。'])
(R/'result.md').write_text('\n'.join(lines).rstrip()+'\n');print(json.dumps(summary),flush=True)
