"""Two complete four-axis notional surfaces; old midpoint qualifications stay immutable."""
import copy,csv,gzip,io,itertools,json,statistics
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run import ROOT,R,SLOWS,LOOKS,HURDLES,NOTIONALS,axes,grid_configs,anchor_configs,sha,put

def table(path,rows,compressed=False):
 fields=list(dict.fromkeys(k for r in rows for k in r));b=io.StringIO(newline='');w=csv.DictWriter(b,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows);raw=b.getvalue().encode();path.write_bytes(gzip.compress(raw,mtime=0) if compressed else raw)
def main():
 assert not (R/'finish.json').exists();report=json.loads((R/'report.json').read_text());grid=grid_configs(report['configs']);plan=json.loads((R/'plan_corrected.json').read_text());assert len(grid)==162;holds={}
 for key,x in plan['read_only_hold_references'].items():
  assert sha(ROOT/x['report'])==x['report_sha256'];c=copy.deepcopy(json.loads((ROOT/x['report']).read_text())['configs'][x['name']])
  for z in c['scenes'].values():
   if 'recent40' not in z:z['recent40']=copy.deepcopy(z['extension40'])
  holds[key]=c
 rows=[];folds=[];recent=[];daily=[];comp=[];edges=[];cells={}
 for c in grid.values():
  old=c.get('read_only_anchor',False);scope=c['scope'];meta={'name':c['name'],'scope':scope,'asset':c['asset'],'read_only_anchor':old,'capital_usdt':c['capital_usdt'],**{p:c[p] for p in axes(c)}};cells[c['name']]={**meta,'fingerprint':c['fingerprint'],'original_or_new_status':c['status'],'positive_complete30d_folds1':c['positive_complete_30d_folds_1x'],'positive_recent5d_folds1':c['recent40_positive_5d_folds_1x'],'original_or_new_sensitivity':c['sensitivity'],'scenes':{k:{p:z[p] for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','NAV_sha256_f64le']} for k,z in c['scenes'].items()}}
  for k,z in c['scenes'].items():
   rows.append({**meta,'cost_multiplier':int(k),'status':c['status'],**{p:z[p] for p in ['net_return_pct','max_drawdown_pct','daily_mark_drawdown_pct','sharpe_365','calmar','cost_usdt','funding_usdt','gross_reference_PnL_to_execution_cost','executions','round_trips','NAV_sha256_f64le']},**{'recent40_'+p:z['recent40'][p] for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','NAV_sha256_f64le']},**{'cost_'+p:v for p,v in z['cost_parts_usdt'].items()}});folds.extend({**meta,'cost_multiplier':int(k),**f} for f in z['folds']);recent.extend({**meta,'cost_multiplier':int(k),**f} for f in z['recent40']['folds'])
   if old:continue
   daily.extend({**meta,'cost_multiplier':int(k),'boundary_index':j,'equity_usdt':v} for j,v in enumerate(z['daily_equity_usdt']))
   if scope=='native':
    mid=next(y for y in grid.values() if y['scope']==scope and y.get('read_only_anchor') and all(y[p]==c[p] for p in ['trend_lookback_days','lookback_days','return_hurdle']));hold=holds['native_N'+str(c['fixed_entry_notional_usdt'])]
   else:
    mid=next(y for y in grid.values() if y['scope']==scope and y.get('read_only_anchor') and all(y[p]==c[p] for p in ['trend_filter_lookback_days','reversal_lookback_days','reversal_return_hurdle']));hold=holds['parent_B'+str(c['BTC_fixed_entry_notional_usdt'])+'_E'+str(c['ETH_fixed_entry_notional_usdt'])]
   for kind,y in [('old_N2000',mid),('matched_hold',hold)]:
    a=y['scenes'][k];comp.append({**meta,'cost_multiplier':int(k),'reference_kind':kind,'reference_name':y['name'],'reference_fingerprint':y['fingerprint'],'reference_original_status':y['status'],'new_return_pct':z['net_return_pct'],'reference_return_pct':a['net_return_pct'],'return_delta_pp':z['net_return_pct']-a['net_return_pct'],'DD_delta_pp':z['max_drawdown_pct']-a['max_drawdown_pct'],'recent40_return_delta_pp':z['recent40']['net_return_pct']-a['recent40']['net_return_pct'],'execution_count_delta':z['executions']-a['executions'],'cost_delta_usdt':z['cost_usdt']-a['cost_usdt'],'new_NAV_sha256':z['NAV_sha256_f64le'],'reference_NAV_sha256':a['NAV_sha256_f64le'],'cash_analytic_return_pct':0})
 for scope in ['native','parent']:
  group=[c for c in grid.values() if c['scope']==scope];dims=axes(group[0]);fields=list(dims);by={tuple(c[p] for p in fields):c for c in group};assert len(group)==81 and set(by)==set(itertools.product(*dims.values()))
  for key,c in by.items():
   for i,(field,axis) in enumerate(dims.items()):
    j=axis.index(key[i])
    if j+1==len(axis):continue
    other=list(key);other[i]=axis[j+1];y=by[tuple(other)];a,b=c['scenes']['3'],y['scenes']['3'];edges.append({'scope':scope,'axis':field,'from':c['name'],'to':y['name'],'return3_delta_pp':b['net_return_pct']-a['net_return_pct'],'DD3_delta_pp':b['max_drawdown_pct']-a['max_drawdown_pct'],'sharpe3_delta':b['sharpe_365']-a['sharpe_365'] if a['sharpe_365'] is not None and b['sharpe_365'] is not None else None,'recent40_return3_delta_pp':b['recent40']['net_return_pct']-a['recent40']['net_return_pct'],'recent40_sharpe3_delta':b['recent40']['sharpe_365']-a['recent40']['sharpe_365'] if a['recent40']['sharpe_365'] is not None and b['recent40']['sharpe_365'] is not None else None})
  for field,flag in [('sharpe3_delta','full_sharpe_cliff'),('recent40_sharpe3_delta','recent40_sharpe_cliff')]:
   es=[e for e in edges if e['scope']==scope];vals=[abs(e[field]) for e in es if e[field] is not None];cut=2*statistics.pstdev(vals) if vals else None
   for e in es:e[flag]=e[field] is not None and abs(e[field])>cut;e[flag+'_threshold_abs_delta']=cut
  limits={rr:max(abs((c['scenes']['3']['recent40'] if rr else c['scenes']['3'])['net_return_pct']) for c in group) or 1 for rr in [False,True]}
  for S in SLOWS:
   fig,axs=plt.subplots(3,2,figsize=(10,12),layout='constrained')
   for i,N in enumerate(NOTIONALS):
    for j,rr in enumerate([False,True]):
     mat=np.array([[(by[N,S,L,H]['scenes']['3']['recent40'] if rr else by[N,S,L,H]['scenes']['3'])['net_return_pct'] for L in LOOKS] for H in HURDLES]);im=axs[i,j].imshow(mat,cmap='RdYlGn',vmin=-limits[rr],vmax=limits[rr]);title=f'ETH slow {S}d / ETH N{N}' + (f' / BTC N{4000-N}' if scope=='parent' else '')+(' / old midpoint*' if N==2000 else '');axs[i,j].set_title(title+'\n'+('Inherited 40 days' if rr else '370 days'));axs[i,j].set_xticks(range(3),[str(x) for x in LOOKS]);axs[i,j].set_yticks(range(3),[f'{x*100:g}%' for x in HURDLES]);axs[i,j].set_xlabel('ETH fast reversal lookback (days)');axs[i,j].set_ylabel('ETH reversal entry hurdle')
     for a,b in itertools.product(range(3),range(3)):axs[i,j].text(b,a,f'{mat[a,b]:+.3f}%'+('*' if N==2000 else ''),ha='center',va='center',fontsize=9)
     fig.colorbar(im,ax=axs[i,j],label='3x net return (%)')
   fig.suptitle(('ETH native bank 10,000' if scope=='native' else 'BTC trend + ETH gate | raw 1/1 | banks 20,000')+' | known history');fig.savefig(R/f'sensitivity_{scope}_S{S}.png',dpi=120);plt.close(fig)
 counts={'cost':len(rows),'full_folds':len(folds),'recent40_folds':len(recent),'daily_NAV':len(daily),'edges':len(edges),'reference_comparisons':len(comp)};assert list(counts.values())==[486,6318,3888,120204,432,648]
 for path,data,gz in [('sensitivity.csv',rows,False),('fold_results.csv',folds,False),('recent40_fold_results.csv',recent,False),('daily_equity.csv.gz',daily,True),('joint_edges.csv',edges,False),('reference_comparisons.csv',comp,False)]:table(R/path,data,gz)
 report['joint_grid_sensitivity']={'cell_count':162,'new_cells':108,'readonly_old_N2000_cells':54,'dimension_count_per_scope':4,'axes':{scope:axes(next(c for c in grid.values() if c['scope']==scope)) for scope in ['native','parent']},'cells':cells,'adjacent_edges':432,'old_qualification_unchanged':True,'cliff_definition':'AbsadjacentSharpedelta>2populationSDoffiniteabsadjacentSharpedeltaswithinrespectivescope81grid;descriptiveonly,Nonepreserved,nopostresultextension.'};put(R/'report.json',report)
 def brief(c):return {'name':c['name'],'scope':c['scope'],'capital_usdt':c['capital_usdt'],'full_return3_pct':c['scenes']['3']['net_return_pct'],'whole_DD3_pct':c['scenes']['3']['max_drawdown_pct'],'recent_return3_pct':c['scenes']['3']['recent40']['net_return_pct'],'recent_DD3_pct':c['scenes']['3']['recent40']['max_drawdown_pct'],'positive_complete30d_folds1':c['positive_complete_30d_folds_1x'],'positive_recent5d_folds1':c['recent40_positive_5d_folds_1x'],'status':c['status'],'failed_criteria':c['failed_criteria']}
 cs=list(report['configs'].values());summ={'new_financial_configs':108,'new_native_backtests':54,'new_passive_parents':54,'readonly_native_components':30,'readonly_midpoint_cells':54,'readonly_unique_results':63,'full_grid_cells':162,'passed_candidates':len(report['summary']['passed']),'rejected_candidates':len(report['summary']['rejected']),'positive_configs_by_cost':report['summary']['positive_configs_by_cost'],'recent_positive_configs_by_cost':{k:sum(c['scenes'][k]['recent40']['net_return_pct']>0 for c in cs) for k in ['1','2','3']},'failed_criteria_counts':dict(Counter(p for c in cs for p in c['failed_criteria'])),'rows':counts,'groups':{}}
 for scope in ['native','parent']:
  group=[c for c in cs if c['scope']==scope];summ['groups'][scope]={'configs':len(group),'passed':sum(c['status']=='passed' for c in group),'positive_configs_by_cost':{k:sum(c['scenes'][k]['net_return_pct']>0 for c in group) for k in ['1','2','3']},'recent_positive_configs_by_cost':{k:sum(c['scenes'][k]['recent40']['net_return_pct']>0 for c in group) for k in ['1','2','3']},'best_full':brief(max(group,key=lambda c:c['scenes']['3']['net_return_pct'])),'best_recent':brief(max(group,key=lambda c:c['scenes']['3']['recent40']['net_return_pct'])),'positive_complete30d_folds1_counts':dict(Counter(c['positive_complete_30d_folds_1x'] for c in group)),'positive_recent5d_folds1_counts':dict(Counter(c['recent40_positive_5d_folds_1x'] for c in group)),'failed_criteria_counts':dict(Counter(p for c in group for p in c['failed_criteria']))}
 put(R/'summary.json',summ);ctx=json.loads((R/'context.json').read_text());fwd=json.loads((R/'forward_report.json').read_text());fv=json.loads((R/'forward_verification.json').read_text())
 lines=[f'# {R.name} ETH趋势门槛反转的真实预算敏感性',f'实际新评估108项：54 ETH原生＋54 BTC趋势/ETH门槛反转组合，324个1/2/3倍成本场景；{summ["passed_candidates"]}通过/{summ["rejected_candidates"]}淘汰。每个实际定义先reserve，计算、独立核验后逐项finish，负收益/零收益/淘汰完整保存。全文读取{ctx["registry_events"]}事件/{ctx["registry_ids"]}ID与{len(ctx["prior_conclusions_read"])}份旧结论；初始16项均有实际历史证据。',
 '预设ETH固定N1000/2000/3000、慢ROC S7/14/28日、短ROC L1/2/3日、H2/4/6%；N2000旧27原生只读，54新N1000/3000按真实手数重新模拟，不能线性缩放NAV。BTC固定顺趋势ROC31日、入场4%、退出1%，复用其N1000/2000/3000三条实际旧账本。父组合ETH_N与BTC_N=4000-ETH_N，固定总入场预算4000；54新非对称配置与27旧2000/2000组成81格四维网格。原生也有81格四维，合计162格/432相邻边；54旧中点保留原资格，不重新评级。',
 '原值权重1/1表示两个各10000USDT完整独立银行，父本金20000，总入场预算4000=20%初始本金。1000/3000是固定风险预算分配，不是将银行资本归一化为25/75；每次新入场数量由N/前一完整close/真实lot向下取整，同向保留实际q，无NAV复利、转账、交叉保证金、现金生息、父再平衡或额外父交易。新原生参数派生资金比例严格为10%/30%。',
 'ETH短ROC>H空、<-H多；带内实际已有多头仅ROC<0保持，空头仅ROC>0保持，过零退出，反向极端先平后开。慢ROC>0仅允许多、<0仅空、=0全平；不兼容即平实际仓位，无隐藏desired，现金重入须新严格极端。BTC顺趋势ROC>4%多、<-4%空，带内多头仅ROC>-1%保持、空头仅ROC<1%保持，精确退出等号平；精确入场等号不新开。均只用前一完整close，次日UTC00:01 OPEN执行。',
 '实际Binance8合并Parquet及16年度/近期原输入留忽略data并固定路径/版本/字节/SHA。连续OOS2025-10-19 UTC00:01至2026-10-24 UTC00:01共370日、33日上下文；12完整30日折＋10日尾折，门槛至少9/12完整月正，尾折保留不计门槛。近期Sep14-Oct24从日330决策前状态续接，8个连续5日折至少6/8净正且各成本总净正。固定规则无拟合标签、purge不适用，因果执行/3日初始embargo保留；现金、仓位、成本跨折连续，不重开。全部历史已见，不称未触碰最终留出。',
 '每侧5bp手续费＋1bp半价差＋2bp滑点；冲击0.5×滞后20日对数波动×sqrt(订单参考金额/滞后20日ADV)，参与率≤0.1%，真实lot/不利tick/最小金额。新数量须重新核算实际fee、tick、影响、资金费、现金和小时保证金代理，未缩放旧净值。真实结算时点/mark对当时q计资金费，流出×k、流入不放大，未来公开费率不入信号/手数。永续空头以现金抵押，无虚构现货借贷。缺历史L2/队列/TCA/完整阶梯，1%维持保证金与小时不利mark高低价仅代理，混合分钟交易价/小时mark/结算完整NAV回撤不称tick级清算保证。',
 '三项验证：13时间折/8近期折和完整连续NAV整体DD；每scope81格S/L/H/N四维敏感性及全部432相邻边；324新1/2/3倍成本场景。其他门槛3x整体DD≤25%、局部邻域3x净正≥60%、至少4往返、(参考价毛利＋资金费)/成本≥2.5、现金/拒单/保证金代理违规0、源终点空仓。对照同S/L/H旧N2000路径与同实际预算恒多/现金；648逐成本对照保留，旧hold的extension40仅按同区间只读识别，不改旧报告。',
 f'全期净正数量{summ["positive_configs_by_cost"]}，近期净正{summ["recent_positive_configs_by_cost"]}；失败门槛{summ["failed_criteria_counts"]}。各scope完整结果{summ["groups"]}。',
 '预检实际exit1发现首批54原生派生raw_entry_notional_fraction仍为0.2，与固定N1000/3000矛盾；54依赖父也弃用，108定义均finish abandoned/result_available=false，无金融计算。原spec/plan/登记/失败日志和invalid_spec_report原SHA保留。plan_corrected与specs_corrected改为0.1/0.3及依赖指纹，所有108重新reserve且最终预检exit0后才计算。失败不计真实回测试验，不填零收益或标passed/rejected。',
 f'原SMA65/对称1%、BTC1500/ETH500从UTC04:30现金状态续至{fwd["cutoff_utc"]}，新增{fv["new_closed_marks_per_asset"]}闭合分钟、零日决策/参考/成交；旧{fv["original_NAV_prefix"]}点严格不变、新总{fv["NAV_points_per_scene"]}点。已完成Oct26UTC00:01BTC退出不重复；下一日2026-10-27UTC00:01、终点2027-03-31不变。逐成本现金/units/desired/费用/成交完整继承，不从2000重开。',
 '原SMA保留历史Float手数/10bp手续费，不套新永续5bp/lot/tick；24日初期延迟shadow不足180日/六折，不冒充paper10真实报价模拟，partial rejected不取消计划。最近65日日线上下文仍指010010/forward_inputs.json.gz及原SHA，当前mark-only输入是分钟数组，下一日不能误当日线字典。',
 '本轮读取AQR官方[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)（2012-05-01）和[交易成本研究](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)（2012-12-05），访问2026-10-26。传统12月期货趋势和股票反转成本仅作背景；ETH短反转加慢门槛及固定预算调整为本轮推断，非论文复现或利润/容量移植。108相关新实算依赖已见历史，不称独立留出、DSR/PBO校正或稳定实盘盈利，不据结果改冻结账户。',
 '复现目录/home/desktop/Documents/Codex/EquiTide；audit.py/check_sources.py/check_alignment.py/check_notional_spec.py只读当前冻结证据，forward.py --reproduce与audit_forward.py不HTTP取数或写登记。不要重新reserve/evaluate/summarize已finish配置。清理本轮可重建缓存/checkpoint，完整原生/账户/结果账本留存；行情忽略data。普通SSH非强推main，freshfetch/全heads/完整tree和必要blob/data/reportSHA核验后释放本轮broker；发布/释放回执在.git。']
 (R/'result.md').write_text('\n\n'.join(lines)+'\n');print(json.dumps(summ),flush=True)
if __name__=='__main__':main()
