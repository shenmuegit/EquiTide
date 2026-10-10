"""Describe preregistered mixed confirmations and unchanged accounts using completed evidence only."""
from pathlib import Path
from collections import Counter
import csv,gzip,hashlib,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
T=Path(__file__).resolve().parent;R=T.parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((T/'report.json').read_text());f=json.loads((T/'forward_report.json').read_text());h=json.loads((T/'history_paths.json').read_text());prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));cs=r['configs'];grid=r['plan']['grid'];summary=r['summary'];comparisons=[];secondary=[]
def compare(c,name,o):return {'config':c['name'],'year':c['year'],'comparator':name,'kind':o['kind'],'same_initial_funding':[1500,500],'return_differences_pp':{k:c['scenes'][k]['net_return_pct']-o['scenes'][k]['net_return_pct']for k in('1','2','3')},'minute_DD3_difference_pp':c['scenes']['3']['max_drawdown_pct']-o['scenes']['3']['max_drawdown_pct'],'all_cost_NAV_identical':all(c['scenes'][k]['NAV_sha256_f64le']==o['scenes'][k]['NAV_sha256_f64le']for k in('1','2','3'))}
for c in cs.values():
 name,o=next((n,o)for n,o in r['read_only_comparators'].items()if o['kind']=='MATCHED_BTC_VOLUME_PURE_ETH_CHANNEL'and o['year']==c['year']and o['BTC_minimum_volume_ratio']==c['BTC_minimum_volume_ratio']);comparisons.append(compare(c,name,o))
 if c['BTC_minimum_volume_ratio']==1:
  name,o=next((n,o)for n,o in r['read_only_comparators'].items()if o['kind']=='BTC_R1_PURE_ETH_EMA_SAME_SPAN'and o['year']==c['year']and o['ETH_EMA_span_days']==c['ETH_EMA_span_days']);secondary.append(compare(c,name,o))
pairs=[]
for pair in summary['new_both_periods_passed_combination_pairs']:
 xs=[next(x for x in comparisons if x['config']==n)for n in pair];ret=[v for x in xs for v in x['return_differences_pp'].values()];dd=[x['minute_DD3_difference_pp']for x in xs];pairs.append({'pair':pair,'joint_improvement_both_years':all(v>=0 for v in ret)and all(v<=0 for v in dd)and(any(v>0 for v in ret)or any(v<0 for v in dd))})
surfaces={}
for year in('2025','2026'):
 cells=[c for c in cs.values()if c['year']==year];sens=r['sensitivity'][year+'_BTC_VOLUME_ETH_FILTERED_EMA'];best=max(c['scenes']['3']['net_return_pct']for c in cells)
 surfaces[year]={'positive3_fraction':sum(c['scenes']['3']['net_return_pct']>0 for c in cells)/9,'full_gate_pass_fraction':sum(c['status']=='passed'for c in cells)/9,'descriptive_cliff_flags':sum(e['cliff_flag_2sd']for e in sens['adjacent_edges']),'adjacent_edges':12,'best_return3_coordinates':[[c['BTC_minimum_volume_ratio'],c['ETH_EMA_span_days']]for c in cells if c['scenes']['3']['net_return_pct']==best],'whole_cost_path_signature_count':len({tuple(c['scenes'][k]['NAV_sha256_f64le']for k in('1','2','3'))for c in cells})}
comparison={'report_sha256':sha(T/'report.json'),'matched_comparisons':comparisons,'secondary_BTC1_same_EMA_span_comparisons':secondary,'qualified_pairs_vs_matched_controls':pairs,'new_both_periods_qualified':len(pairs),'new_pairs_jointly_improve_same_BTC_pure_ETH_channel_controls':sum(p['joint_improvement_both_years']for p in pairs),'failure_counts':dict(Counter(k for c in cs.values()for k in c['failed_criteria'])),'source_component_path_signature_counts':prior['existing_component_path_signature_counts'],'surface_diagnostics':surfaces,'scope':'Primary:match BTCvolume threshold and replace pureETHchannel with channelEMAfilter. Secondary:BTCratio1 holds fixed and compare ETHfilteredEMA to pureEMA atsame span. Allsame1500/500funding,prior actual reports read-only;no independent finalholdout claim.'}
(T/'comparison.json').write_text(json.dumps(comparison,indent=2)+'\n')
with(T/'folds.csv').open('w',newline='')as out:
 w=csv.writer(out,lineterminator='\n');w.writerow(['config','year','is_new','BTC_volume_ratio','ETH_EMA_span_days','cost','fold','net_return_pct','minute_DD_pct','Sharpe365','Calmar'])
 for c in cs.values():
  for k,z in c['scenes'].items():
   for ff in z['folds']:w.writerow([c['name'],c['year'],True,c['BTC_minimum_volume_ratio'],c['ETH_EMA_span_days'],k,ff['fold'],ff['net_return_pct'],ff['max_drawdown_pct'],ff['sharpe_365'],ff['calmar']])
fig,axes=plt.subplots(2,3,figsize=(15,9),layout='constrained')
for j,year in enumerate(('2025','2026')):
 cells={(c['BTC_minimum_volume_ratio'],c['ETH_EMA_span_days']):c for c in cs.values()if c['year']==year}
 for i,(key,title)in enumerate([('net_return_pct','3x net return %'),('max_drawdown_pct','3x whole minute NAV drawdown %'),('sharpe_365','3x daily Sharpe (365)')]):
  ax=axes[j,i];matrix=np.array([[cells[ratio,span]['scenes']['3'][key]for span in grid['ETH_EMA_span_days']]for ratio in grid['BTC_minimum_volume_ratio']]);im=ax.imshow(matrix,cmap='YlGnBu'if i!=1 else'YlOrRd',aspect='auto')
  for a in range(3):
   for b in range(3):ax.text(b,a,f'{matrix[a,b]:.3f}',ha='center',va='center',fontsize=11,color='white'if matrix[a,b]>(matrix.min()+matrix.max())/2 else'#111111')
  ax.set(xticks=range(3),xticklabels=grid['ETH_EMA_span_days'],yticks=range(3),yticklabels=grid['BTC_minimum_volume_ratio'],xlabel='ETH EMA span days (symmetric1.5%)',ylabel='BTC entry turnover ratio (mean30days)',title=year+' | '+title);bar=fig.colorbar(im,ax=ax,fraction=.035);bar.ax.ticklabel_format(style='plain',useOffset=False,axis='y')
fig.suptitle('BTC quote-turnover confirmation + ETH channel/EMA confirmation\nBoth close-channel15/30 | Raw75/25:1500/500USDT | 18 new annualparents | reused180-day histories',fontsize=14);fig.savefig(T/'sensitivity.png',dpi=130);plt.close(fig)
paperstate=json.loads((R/'research/paper10/state.json').read_text());paper=json.loads((R/'research/paper10/observations'/paperstate['last_observation_id']/'summary.json').read_text());fr=r['plan']['forward_resume']
lines=['# BTC成交额确认＋ETH通道EMA确认：独立两轴组合','',f"18个新年度组合、54新成本场景实际执行：1x/3x净正{summary['positive_1x']}/{summary['positive_3x']}；{len(summary['passed'])}通过、{len(summary['rejected'])}淘汰，{len(pairs)}组跨期参数合格。12个同预算源组件/36场景和12个匹配旧父组合只读；0新组件信号/成交重跑，21个新定义（含原shadow截止）均先reserve并finish。",'',
'## 事前假设、完整规则和资金','',
'本轮事前固定BTC收盘通道15/30＋前30日USDT成交额均值确认，入场倍率0.9/1/1.1；交叉ETH收盘通道15/30＋EMA50/65/80日、对称1.5%确认。关注点BTC倍率1/ETH EMA65。假设两币不同活动/趋势确认能限制风险而保留增长；完整3×3×两年在结果之前冻结，不根据OOS扩参。主匹配对照保持同BTC倍率，ETH使用旧纯通道；第二对照在BTC倍率1下保持ETH同EMA跨度、去掉通道条件。','',
'BTC决策i只用前完整UTC日C[i−1]、成交额Q[i−1]。严格C[i−1]>max(C[i−16:i−1])且Q[i−1]≥r×mean(Q[i−31:i−1])、均额>0才进入；严格C[i−1]<min(C[i−31:i−1])退出，不以低成交额本身退出。价格/成交额参考排除被比较日、止于i−2；成交额相等通过、价格相等/死区保持desired。Q是1440个真实分钟quote_volume的Decimal和，均额/倍率Decimal28。','',
'ETH在同15日入场收盘通道上，须同时满足float(C[i−1])>EMA[i−1]×1.015；低于前30日退出通道或float(C[i−1])<EMA[i−1]×0.985即设cash，退出优先，其余/相等保持desired。EMA为alpha=2/(span+1)，首个数据日完成收盘float初始化，逐日(1-alpha)×EMA+alpha×close、adjust=False，跨折不重置。无arming、止损、空头或延迟确认。完整源spec/组件指纹见grid_batch.json和report.json。','',
'原始BTC/ETH 75/25表示每个2000USDT账户初始独立1500/500USDT。直接相加相同预算、同UTC分钟/执行轴、已扣费的组件绝对NAV一次；不缩放、二次乘权重、归一化、转账或再平衡。OOS183现金/desired-cash启动，暖机不造旧持仓；六折连续继承资金和状态。','',
f"完整读取{prior['lines']}行登记、{prior['preserved_ids']}保留ID/{prior['canonical']}规范定义、{len(prior['conclusions'])}轮全文结论、7个Freqtrade结果、4个OOS源码与3技能。初始16原始行/别名实际证据完整，无缺结果条目。本轮新增18个历史定义；旧源2026 ETH组件虽原先淘汰仍作为实际结果保留，旧status/criteria不改。",'',
'## 三项验证、失败判据与局限','',
'Walk-forward实际完成：2025、2026各03-18UTC00:01至09-14UTC00:01，分别180天、六个连续30天折；180日滚动历史、3日gap、purge0，无模型/标签/逐折拟合或OOS调参。信号可得后用下一00:01真实历史分钟开盘估计IOC，期末含成本平仓。各场景259382个连续分钟收盘/执行节点计算整体DD，不平均逐折回撤；两年初始资金独立。两段历史均反复使用，不称未触碰最终测试集。','',
'Sensitivity实际完成：BTC倍率和ETH EMA速度两个参数同时变化，完整9格×两年×1/2/3成本。sensitivity.csv保存54新场景的净收益/整体与日采样DD/Sharpe365/Calmar/成本/往返；folds.csv保存324折，负折与零折均留档。相邻Sharpe差超过2倍差异样本标准差仅是描述性陡峭边，不是显著性、DSR/PBO或独立样本证明。','',
'Costs实际完成：每侧10bp手续费、估计半点差1bp、滑点2bp，加0.5×滞后20完整UTC日未年化样本log波动率×sqrt(预算/滞后quoteADV)冲击，所有成本同时×1/2/3；参与率≤0.001。Decimal28余额、PRICE不利tick、LOT下取整、最低名义额和前5完整分钟VWAP百分价格代理核对。Oct1静态过滤规则应用旧历史是估计假设；没有历史L2、TCA、队列、部分成交或真实IOC接单/容量保证。仅现货做多，借币/资金费不适用。','',
'八门槛固定：1/2/3成本净正；1x至少4/6严格正折；3x整体DD≤25%；3x邻域净正≥60%；1x至少2组件往返；1x毛参考盈亏/执行成本≥2.5；无负现金/数量；终止空仓。组合按自身共同轴判断，不平均源收益率或Sharpe。','',
f"36源场景和54新组合场景独立重建核对，14,006,628个新NAV点；12匹配旧对照只读。失败条件计数{comparison['failure_counts']}，全部正/负结果、失败折和敏感性单元保留。工程准备时一个大写family名称被登记模式校验拒绝，在首个reserve/计算前改为小写；未改经济规则或冻结spec；修复、原错误和静态说明检查见engineering_recovery.json/prepare_failure_1.log，不作为收益结果。",'',
'## 新组合按各年1x净收益倒序','',
'|年份|BTC倍率/ETH EMA日|原权重|1x%|2x%|3x%|3x整体分钟DD%|正折1|成交/往返1|成本1USDT（手续费/冲击）|状态|','|---|---|---|---:|---:|---:|---:|---:|---|---|---|']
for c in sorted(cs.values(),key=lambda c:(c['year'],-c['scenes']['1']['net_return_pct'],c['name'])):
 z=c['scenes']['1'];p=z['cost_parts_usdt'];lines.append(f"|{c['year']}|{c['BTC_minimum_volume_ratio']}/{c['ETH_EMA_span_days']}|75/25|{z['net_return_pct']:.6f}|{c['scenes']['2']['net_return_pct']:.6f}|{c['scenes']['3']['net_return_pct']:.6f}|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['positive_folds_1x']}/6|{z['executions']}/{z['round_trips']}|{z['cost_usdt']:.6f}（{p['fee']:.6f}/{p['impact']:.6f}）|{c['status']}|")
lines+=['','## 匹配对照、平台和新颖性','']
for year in('2025','2026'):
 c=next(c for c in cs.values()if c['year']==year and c['BTC_minimum_volume_ratio']==1 and c['ETH_EMA_span_days']==65);x=next(x for x in comparisons if x['config']==c['name']);sx=next(x for x in secondary if x['config']==c['name']);z=c['scenes']['3'];lines.append(f"事前关注点{year}倍率1/EMA65：三倍收益{z['net_return_pct']:.6f}%、整体分钟DD{z['max_drawdown_pct']:.6f}%；对同BTC纯ETH通道收益差{x['return_differences_pp']['3']:.6f}pp、DD差{x['minute_DD3_difference_pp']:.6f}pp；对同BTC/EMA跨度的纯ETH EMA收益差{sx['return_differences_pp']['3']:.6f}pp、DD差{sx['minute_DD3_difference_pp']:.6f}pp。")
for year,d in surfaces.items():lines.append(f"{year}三倍净正{100*d['positive3_fraction']:.3f}%，完整门槛通过{100*d['full_gate_pass_fraction']:.3f}%；描述性陡峭边{d['descriptive_cliff_flags']}/12；最高三倍收益坐标{d['best_return3_coordinates']}；全成本路径种数{d['whole_cost_path_signature_count']}。边界或重复路径不算独立成功。")
if comparison['new_pairs_jointly_improve_same_BTC_pure_ETH_channel_controls']==0:
 lines += ['', '本轮没有同时改善匹配收益与回撤的更强候选。预定关注点以更低收益交换更低回撤；保留为历史合格组合供比较，固定前向账户仍按原冻结计划运行。2026最高收益EMA50处于预设边界，不能在本轮看到结果后追加更短跨度；未来如检验须另行事前固定及登记，也不能称为新的独立市场确认。']
lines += ['',f"{len(pairs)}个新参数对跨期通过绝对门槛；两期全成本收益及3x整体DD相对匹配纯ETH通道都不更差且至少一处改善者{comparison['new_pairs_jointly_improve_same_BTC_pure_ETH_channel_controls']}组。18主比较和6个次比较见comparison.json；现金0及旧持有/SMA为背景，不是新增研究结果。",'',f"54新场景中{h['new_scenes_already_in_any_prior_report']}已见/{h['new_scenes_not_in_any_prior_report']}未见；去重后{h['distinct_new_scene_paths_not_in_prior']}种未见单场景路径、2026新3x组合路径{h['new_2026_combo_3x_paths_not_in_any_prior_report']}、未见合格跨期配对{h['qualified_cross_period_pairs_not_in_any_prior_report']}种。源路径种数{prior['existing_component_path_signature_counts']}；参数新颖性与市场样本独立性不同，所有旧/新重复路径均披露。",'', '正收益只说明这两段重复开发历史中的成本后表现；无稳定实盘盈利保证。本轮不追加未冻结参数、不替换固定模拟盘；若新指标或资金、周期变动须重新事前登记。','', '## 原SMA延迟shadow、真实报价账户与复现','']
shadow=f"原SMA65/1%延迟shadow由{f['resume_utc']}续至{f['cutoff_utc']}，处理冻结Oct10UTC00:01日线参考（BTC/ETH均{f['daily_decisions_by_asset']['BTC']['action']}/{f['daily_decisions_by_asset']['ETH']['action']}）；65日完整数据及64日重叠校验，每成本独立6个日线决策核对。原{fr['prior_NAV_points']}点完整前缀保留，增加120闭合分钟mark＋1参考到{fr['total_NAV_points']}点/{fr['cumulative_minutes']}分钟、8完整日；新虚拟成交{sum(s['new_executions']for c in f['configs'].values()if 'asset'in c for s in c['scenes'].values())}笔，下一日线Oct11UTC00:01，3x累计{f['configs']['forward_snapshot_combo']['scenes']['3']['net_return_pct']:.6f}%。原2027-03-31计划及SHA不变；这是后来取得真实历史bar的延迟重建，原时间戳为冻结历史参考，不是十策略当时实际报价执行或实时业绩。"
lines += [shadow,'',f"P01–P10第{paper['actual_quote_observations']}次真实报价账户（{paper['observed_at_utc']}，{paper['elapsed_seconds']/3600:.6f}小时，主账户合计{paper['totals_by_cost']['1']['NAV_usdt']}USDT）完整保持。本轮没有运行paper10执行器，没有改冻结本金、规则、数量、desired、成本、日线处理状态或账本。其180天/六窗未成熟，DD仅为实际报价快照采样；网页只读汇总，未重新部署。",'',f"离线复现：`.venv/bin/python research/experiments/{T.name}/replay_verify.py`；6阶段精确重放缓存、原SMA日线/分钟续接、新组合、独立审计与登记，不HTTP、不写账户/登记、不产生新成交。四份真实525600行parquet、聚合日线、源spec/组件归档、代码和输入哈希见spec.json、report.json、data_manifest.json；大行情/NPY留忽略data，Git保存轻量充分证据。",'', '## 一手资料', '', '[Binance公开历史数据](https://github.com/binance/binance-public-data)、[现货市场数据REST](https://developers.binance.com/en/docs/catalog/core-trading-spot-trading/api/rest-api/market)、[过滤规则](https://developers.binance.com/en/docs/products/spot/filters)于本轮读取。访问UTC与用途见sources.json；交易假设和收益来自本地已登记实际研究，不是文档的盈利承诺。']
(T/'result.md').write_text('\n'.join(lines)+'\n');(T/'forward_result.md').write_text('# 原SMA冻结延迟shadow续接\n\n'+shadow+'\n');print(json.dumps({'new_configs':18,'passed':len(summary['passed']),'rejected':len(summary['rejected']),'cross_period_pairs':len(pairs),'joint_primary_control_improvements':comparison['new_pairs_jointly_improve_same_BTC_pure_ETH_channel_controls'],'surface_diagnostics':surfaces},ensure_ascii=False))
