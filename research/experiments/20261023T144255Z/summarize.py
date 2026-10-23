"""Complete joint-grid surfaces,portfolio outcomes and immutable-source disclosures."""
import csv,gzip,io,json,statistics
from collections import Counter,defaultdict
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run import ROOT,R,LOOKS,HURDLES,sha,put

def csvwrite(p,rows,compressed=False):
 fields=list(dict.fromkeys(k for x in rows for k in x));buf=io.StringIO(newline='');w=csv.DictWriter(buf,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows);raw=buf.getvalue().encode();p.write_bytes(gzip.compress(raw,mtime=0) if compressed else raw)

def main():
 report=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text());ctx=json.loads((R/'context.json').read_text());cfgs=report['configs'];cs=[c for c in cfgs.values() if c['role']=='candidate'];by={(c['BTC_lookback_days'],c['BTC_return_hurdle'],c['ETH_lookback_days'],c['ETH_return_hurdle']):c for c in cs};benchmark=next(c for c in cfgs.values() if c['role']=='benchmark');source=json.loads((ROOT/next(iter(plan['component_sources'].values()))['report']).read_text());source_by_fp={c['fingerprint']:c for c in source['configs'].values()};rows=[];folds=[];daily=[];costs=[];fund=[];edges=[];paths=defaultdict(list)
 for c in cfgs.values():
  paths[tuple(c['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3'])].append(c['name']);c['component_daily_return_correlations']={}
  for k,z in c['scenes'].items():
   a,b=[np.asarray(source_by_fp[fp]['scenes'][k]['daily_equity_usdt']) for fp in c['source_fingerprints']];ar,br=a[1:]/a[:-1]-1,b[1:]/b[:-1]-1;corr=float(np.corrcoef(ar,br)[0,1]) if ar.std() and br.std() else None;c['component_daily_return_correlations'][k]=corr;meta={p:c[p] for p in ['name','role','BTC_lookback_days','BTC_return_hurdle','ETH_lookback_days','ETH_return_hurdle']};meta['cost_multiplier']=k;rows.append({**meta,**{p:z[p] for p in ['net_return_pct','max_drawdown_pct','daily_mark_drawdown_pct','sharpe_365','calmar','cost_usdt','funding_usdt','gross_reference_PnL_to_execution_cost','executions','round_trips']},'positive_folds':sum(f['net_return_pct']>0 for f in z['folds']),'full4D_local3_positive_fraction':c['sensitivity'].get('four_dimensional_local_3x_positive_fraction'),'component_daily_return_correlation':corr,'status':c['status']});folds.extend({**meta,**f} for f in z['folds']);daily.extend({**meta,'boundary_index':i,'NAV_usdt':v} for i,v in enumerate(z['daily_equity_usdt']));costs.append({**meta,'total_execution_cost_usdt':z['cost_usdt'],**z['cost_parts_usdt']});fund.append({**meta,**{p:z[p] for p in ['funding_usdt','base_funding_same_exposure_usdt','funding_stress_increment_usdt','funding_income_usdt','funding_outflow_usdt','funding_settlements','nonzero_funding_settlements']}})
  if c['role']=='candidate':c['same_budget_hold_comparison']={k:{'return_difference_pct':z['net_return_pct']-benchmark['scenes'][k]['net_return_pct'],'composite_DD_difference_pct':z['max_drawdown_pct']-benchmark['scenes'][k]['max_drawdown_pct']} for k,z in c['scenes'].items()}
 axes={'BTC_lookback_days':LOOKS,'BTC_return_hurdle':HURDLES,'ETH_lookback_days':LOOKS,'ETH_return_hurdle':HURDLES}
 for c in cs:
  key=[c[p] for p in axes]
  for j,(p,levels) in enumerate(axes.items()):
   i=levels.index(c[p])
   if i+1<len(levels):
    other=key.copy();other[j]=levels[i+1];b=by[tuple(other)];edges.append({'from':c['name'],'to':b['name'],'axis':p,'absolute_3x_Sharpe_difference':abs(c['scenes']['3']['sharpe_365']-b['scenes']['3']['sharpe_365'])})
 threshold=2*statistics.stdev(e['absolute_3x_Sharpe_difference'] for e in edges)
 for e in edges:e.update(threshold=threshold,descriptive_cliff_flag=e['absolute_3x_Sharpe_difference']>threshold)
 slices=[]
 for lb in LOOKS:
  for le in LOOKS:
   cells=[c for c in cs if c['BTC_lookback_days']==lb and c['ETH_lookback_days']==le];slices.append({'BTC_lookback_days':lb,'ETH_lookback_days':le,'configs':[c['name'] for c in cells],'positive3_fraction_conditional_threshold_slice':sum(c['scenes']['3']['net_return_pct']>0 for c in cells)/9,'scope':'Descriptivefixed-lookbacksliceonly;qualificationusesfull4Dneighborincludinglookbackvariation.'})
 report['conditional_2D_threshold_slices']=slices;report['sensitivity_cliffs']={'heuristic':'Adjacent3xdailySharpe difference>2sampleSDacross4Dedges;descriptiveonly.','edges':edges};report['failure_counts']=dict(Counter(k for c in cs for k,v in c['criteria'].items() if not v));report['within_batch_path_equivalence']={'parameter_definitions':82,'unique_full_three_cost_NAV_paths':len(paths),'groups':[{'names':names,'NAV_sha256_by_cost':dict(zip(['1','2','3'],key))} for key,names in paths.items()],'scope':'Allsame330daymarket,not82independentsamples.'};report['research_context']={'prior_registry_events':ctx['registry_events'],'prior_registry_ids':ctx['registry_ids'],'prior_canonical_research_definitions':ctx['canonical_research_definitions_excluding_observations'],'prior_conclusions_read':len(ctx['prior_conclusions_read']),'initial16_missing_actual_results':0,'independent_final_holdout':False,'DSR_PBO_computed':False};report['axis']['extra_union_keys_over_source']={a:report['axis']['union_points']-n for a,n in report['axis']['source_points'].items()};report['artifacts']={'complete_parent_results':'results/*.json.gz','all_scenes':'sensitivity.csv','fold_results':'fold_results.csv','daily_NAV':'daily_equity.csv.gz','execution_costs':'cost_scenarios.csv','funding':'funding_scenarios.csv','full4D_slices':'sensitivity_surface.png','equity':'equity.png','verification':'verification.json'};put(R/'report.json',report)
 for name,data,z in [('sensitivity.csv',rows,False),('fold_results.csv',folds,False),('daily_equity.csv.gz',daily,True),('cost_scenarios.csv',costs,False),('funding_scenarios.csv',fund,False)]:csvwrite(R/name,data,z)
 limit=max(abs(c['scenes']['3']['net_return_pct']) for c in cs);fig,axs=plt.subplots(3,3,figsize=(12,11),constrained_layout=True)
 for i,lb in enumerate(LOOKS):
  for j,le in enumerate(LOOKS):
   ax=axs[i,j];v=np.asarray([[by[lb,hb,le,he]['scenes']['3']['net_return_pct'] for he in HURDLES] for hb in HURDLES]);im=ax.imshow(v,cmap='RdYlGn',vmin=-limit,vmax=limit);ax.set(xticks=range(3),xticklabels=['1%','2%','4%'],yticks=range(3),yticklabels=['1%','2%','4%'],xlabel='ETH return band',ylabel='BTC return band',title=f'BTC L{lb} / ETH L{le}')
   for a in range(3):
    for b in range(3):ax.text(b,a,f'{v[a,b]:+.2f}%',ha='center',va='center',fontsize=9)
 fig.suptitle('All81passive BTC/ETH pairs:3x costs;raw funded weights1/1',fontsize=14);fig.colorbar(im,ax=list(axs.ravel()),label='Net return % of20000initialcollateral',shrink=.6);fig.savefig(R/'sensitivity_surface.png',dpi=140);plt.close(fig)
 center=by[10,.02,10,.02];best=max(cs,key=lambda c:c['scenes']['3']['net_return_pct']);fig,ax=plt.subplots(figsize=(10,4.5),constrained_layout=True)
 for c,label in [(center,'PresetB10H2%/E10H2%'),(best,'Post-hocpeak,notqualified'),(benchmark,'Same-budgetconstantlong')]:
  v=np.asarray(c['scenes']['3']['daily_equity_usdt']);ax.plot(range(len(v)),v/200,label=label)
 ax.axhline(100,color='grey',linestyle=':',label='Cash,zero yield');ax.set(xlabel='ContinuousOOSdailyboundary(330days)',ylabel='NAV / initialcollateral %',title='3xcosts;raw weights1/1,total20000USDT');ax.legend(fontsize=8);fig.savefig(R/'equity.png',dpi=140);plt.close(fig)
 s=report['summary'];peak=best['scenes']['3'];maxfrac=max(c['sensitivity']['four_dimensional_local_3x_positive_fraction'] for c in cs);lines=['# BTC/ETH永续双向动量被动组合：完整四维网格','',f"轮次`{R.name}`，冻结计划SHA256`{report['frozen_plan_sha256']}`。81新候选父组合＋1恒多父参考，82项分别reserve后实际评估246成本场景/2706逐折；20旧组件及60成本路径只读复用，源信号、成交及资金费模型没有重跑。候选通过{len(s['passed'])}、淘汰{len(s['rejected'])}，1/2/3倍净正{s['positive_configs_by_cost']['1']}/{s['positive_configs_by_cost']['2']}/{s['positive_configs_by_cost']['3']}。",'',
 '## 假设、完整参数与原值资金','',
 '检验两独立永续动量袖套能否分散单币择时风险、改善逐折收益宽度。BTC与ETH各有L={5,10,20}日及H={1%,2%,4%}，9×9完整交叉共81，不只挑旧20日绿格。完整四维邻域同时扰动两币回看与门槛，避免将固定最优回看的阈值绿面当全面稳健性。原[AQR2017多市场趋势研究](https://www.aqr.com/insights/research/journal-article/a-century-of-evidence-on-trend-following-investing)只是动机，BTC/ETH相关性和盈利必须由本批数据检验，不把传统多资产结论当币圈收益证据。',
 '原值权重1/1表示各一份已用10000USDT建立的独立抵押账本，总本金20000。两条绝对NAV直接加一次，不把权重归一成0.5/0.5后再乘已分配本金，不缩放旧账户、转账、复投或再平衡。每组件固定入场名义额2000，因此两者都活跃时初始名义额合计4000，约总初始抵押20%；持仓数量、价格漂移与lot余量沿旧状态。各袖套独立检查保证金，不用另一账户现金抵消越界。',
 '旧组件仅用前一完整UTC永续日收盘ROC=C[j]/C[j−L]−1，严格>H做多、<−H做空，否则现金；下一00:01OPEN先平后开，同向不调数量。固定2000/当时前日已闭合收盘取lot，非未来OPEN/NAV/资金费定量。线性永续只扣手续费开仓，平仓结算带符号PnL；不借现货、无现金利息。所有原规则、源spec、原账本和报告SHA均保留，源rejected状态不因父组合改变。','',
 '## 净值复用和时间对齐','',
 '源20261023T124125Z已完成20配置/60场景，全量read-only。每条源NAV从保存state_segments的cash/signedunits/entry及真实原轴价格在RAM恢复，每点SHA与源报告完全一致；独立审计再从实际存储trade/funding事件另一条路径恢复，不执行源策略选择、撮合或费用模型，也不修改源文件/状态。所有原始交易和资金费完整留旧archive，父archive用准确指纹/源NAV SHA引用，避免重复抄大账本。',
 '按(真实纳秒时间,eventcode)合并两源轴，同一时间保留原minuteclose→hourmark→fundpre/post→tradepre/post顺序。某资产缺当前key则只沿用最近已完成源观察，禁止插值/前视。key=(ts−共同起点)×16+eventcode，先减epoch以避免int64溢出。实际两源轴本轮完全一致，共486093点，不捏造存在缺口；合成测试另验证毫秒错位资金费的因果carry及交易前后顺序。',
 '组合每日/逐折和整体收益、Sharpe、Calmar、回撤均从完整总NAV重新计算，不平均组件指标。没有新组合成交，旧执行成本和真实资金费各加一次，不额外造组合再平衡费用。','',
 '## 三项实际验证','',
 '- Walk-forward：真实8份永续分钟/标记小时/资金费/元数据文件，输入2025-09-16至2026-09-16；OOS2025-10-19 00:01至2026-09-14 00:01UTC，330日、11连续30日折，源初始上下文30日＋3日间隔，固定规则无拟合/未来标签，purge不适用。源现金/数量/入场价格/资金费跨折连续。已反复研究，不是未触碰最终测试。',
 '- Sensitivity：完整4D81格，邻域每轴相邻索引含自身，角点16邻居、全中心81。246场景含参考、2706逐折与所有净收益/DD/Sharpe/Calmar保留；216条四维相邻Sharpe边仅描述断崖。固定回看阈值切片只作展示，资格必须全4D邻域≥60%。',
 '- Costs：真实源每侧5bp手续费假设、1bp半价差、2bp滑点及0.5×过去20完整永续日波动×sqrt(名义额/quote ADV)冲击，参与率≤0.1%，原生Decimal tick/lot/minNotional；1/2/3倍执行成本及负资金费支出，正资金费收入不增。结算按真实ns/mark/rate计入当时旧持仓，原available_ts延迟保留且不作信号/定量输入。永续空头无现货借币。',
 '源风险仍是分钟成交价代理＋真实小时/结算mark及成交前后样本的混合风险曲线，不是逐tick mark权益。1%维护率/不利完整小时高低点是研究代理，缺历史完整阶梯/逐tick强平、VIP费率、maxQty/percentfilter和真实L2/队列/延迟/TCA。各袖套代理约束分别继承，不以组合分散抹掉源限制。',
 '门槛：三成本净正、1倍≥8/11正折、3倍整体混合DD≤25%、全四维邻域3倍净正≥60%、1倍≥4往返、毛参考价格PnL加真实资金费/执行费≥2.5、无负抵押/源拒单/任一袖套保证金代理越界、终点空仓。','',
 '## 结论与选择偏差','',f"事后最高{best['name']}三倍净收益{peak['net_return_pct']:+.6f}%，整体混合采样DD{peak['max_drawdown_pct']:.6f}%，1倍仅{best['positive_folds_1x']}/11正折，完整4D邻域正比例{best['sensitivity']['four_dimensional_local_3x_positive_fraction']:.2%}。相对源BTC20/1%的8正折，组合没有改善折数至门槛；即使回撤有所下降，也不能只报分散收益。",'',
 f"固定BTC/ETH皆20日时，9个两币阈值组合在3倍成本下全净正；但把回看长度也纳入后，全4D邻域最高仅{maxfrac:.2%}，远低于60%。这展示条件绿面为何不能代替适用参数的完整敏感性。81个候选全因正折不足及全4D邻域不足淘汰，不在看过结果后改变失败判据、扩参数或新建前向账户。",'',
 '失败计数：`'+json.dumps(report['failure_counts'])+'`。全部逐配置见下表；246场景完整细项在sensitivity.csv，资金费在funding_scenarios.csv。', '',
 '|BTC L/H|ETH L/H|1倍|2倍|3倍|1倍正折|3倍混合DD|4D正比例|状态|','|---|---|---:|---:|---:|---:|---:|---:|---|']
 for c in cs:
  a,b,z=[c['scenes'][k] for k in ['1','2','3']];lines.append(f"|{c['BTC_lookback_days']}/{c['BTC_return_hurdle']:.0%}|{c['ETH_lookback_days']}/{c['ETH_return_hurdle']:.0%}|{a['net_return_pct']:+.3f}%|{b['net_return_pct']:+.3f}%|{z['net_return_pct']:+.3f}%|{c['positive_folds_1x']}/11|{z['max_drawdown_pct']:.3f}%|{c['sensitivity']['four_dimensional_local_3x_positive_fraction']:.1%}|{c['status']}|")
 lines+=['',f"预设中心BTC10/2%＋ETH10/2%的1/2/3倍收益为"+'/'.join(f"{center['scenes'][k]['net_return_pct']:+.6f}%" for k in ['1','2','3'])+'。', '', '同预算双恒多参考（实际新父配置）1/2/3倍为'+'/'.join(f"{benchmark['scenes'][k]['net_return_pct']:+.6f}%" for k in ['1','2','3'])+'，其源资本/名义额/规则/成本全匹配，只作参照而不计候选资格；解析现金零利息为0。全部组合对参考逐成本差额和组件日收益相关性保留，相关性是描述性统计，未用来事后调权。','',
 '## 完整登记、审计与原冻结账户','',f"计算前读取{ctx['registry_events']}事件/{ctx['registry_ids']}ID、{ctx['canonical_research_definitions_excluding_observations']}个规范研究定义与{len(ctx['prior_conclusions_read'])}份旧结论，初始16项均有实际证据。82新父配置各自先reserve，源20配置未重登记/重测；新父结果逐项finish。81参数定义与82含参考路径仍属于同一重复市场，不当作独立试验，DSR/PBO未算。",'',
 '独立审计以结构化时间键另行对齐，重放存储的5244源成交及59400资金费记录（含空仓0），再与源持仓段恢复结果逐点一致且匹配原60个NAV SHA；不重跑源策略/费用选择。82父配置246成本曲线及2952组整体/逐折指标、原1/1资金、费用/资金费相加和两个独立保证金约束均核验，详细结果见verification.json。',
 '原SMA从12:30续到14:30，只增加120闭合分钟，旧31012点完整前缀保留、各场景31132点，累计31109分钟（21日＋869分钟）；无新日决策/参考点/成交/费用，原现金/数量/desired/累计成本保持。下一日事件Oct24 00:01UTC，原2027-03-31终点不变。paper10计划/状态只读，旧延迟shadow不是十策略真实报价模拟。',
 'HTTP取原SMA数据时curl曾报告TLS35（unexpected EOF），内置重试后外层Python实际exit0并获得真实响应；具体失败资产/单次重试退出码未独立捕获，不能从外层0否认该诊断。原stderr、日志SHA与成功响应SHA留read_failures.json，后续独立前缀/时间轴审计和离线重放实际exit0。不重置账户或改历史收益来通过检查。', '',
 f"复核：`PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/{R.name}/audit.py`；原SMA同解释器`research/experiments/{R.name}/forward.py --reproduce`。正式登记不重复reserve已完成ID；新父结果只在独立审计副本以源档案/原行情/独立登记重建，绝不重跑已完成组件策略。", '',
 '保留82父archive、完整spec/报告/折与日NAV、源文件哈希和必要代码/失败事实；完整源trade/funding账本仍在原20archive，原SMA完整报告/状态/输入和2原始HTTP响应保留。原始大行情留忽略data；无磁盘NPY/checkpoint，已finish报告原字节与登记SHA优先，不压缩迁移或删损结果。', '',
 '未验证：独立最终测试、365完整年度、DSR/PBO、逐tick mark强平/完整历史阶梯和实盘/TCA；本批只是既有330日上的被动组合检验。',''];(R/'result.md').write_text('\n'.join(lines));print(json.dumps({'parent_configs':82,'candidates':81,'benchmark_parents':1,'cost_scenes':len(rows),'fold_rows':len(folds),'daily_NAV_rows':len(daily),'four_dimensional_edges':len(edges),'max_full4D_positive_fraction':maxfrac,'passed':len(s['passed']),'rejected':len(s['rejected']),'failure_counts':report['failure_counts']}),flush=True)

if __name__=='__main__':main()
