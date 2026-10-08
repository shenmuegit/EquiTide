"""Document all frozen variants and render the actual two-parameter sensitivity surface."""
from pathlib import Path
import collections,gzip,hashlib,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
T=Path(__file__).resolve().parent;R=T.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((T/'report.json').read_text());p=r['plan'];f=json.loads((T/'forward_report.json').read_text());h=json.loads((T/'history_paths.json').read_text());prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()))
fresh={n:c for n,c in r['configs'].items() if c['is_new']};failed=collections.Counter(k for c in fresh.values() for k in c['failed_criteria'])
lookup={(c['year'],c['BTC_exit_days'],c['ETH_exit_days']):c for c in r['configs'].values()}
comparisons=[]
for n,c in fresh.items():
 for label,bx,ex in [('both_slow_anchor',30,30),('prior_BTCfast_ETHslow',10,30)]:
  old=lookup[c['year'],bx,ex]
  comparisons.append({'config':n,'year':c['year'],'comparator':old['name'],'kind':label,'old_result_read_only':True,'return3_difference_pp':c['scenes']['3']['net_return_pct']-old['scenes']['3']['net_return_pct'],'minute_DD3_difference_pp':c['scenes']['3']['max_drawdown_pct']-old['scenes']['3']['max_drawdown_pct'],'NAV3_identical':c['scenes']['3']['NAV_sha256_f64le']==old['scenes']['3']['NAV_sha256_f64le']})
comparison={'report_sha256':sha(T/'report.json'),'matched_anchor_comparisons':comparisons,'new_both_periods_qualified':len(r['summary']['new_both_periods_passed_combination_pairs']),'full_grid_both_periods_qualified':len(r['summary']['both_periods_passed_combination_pairs']),'focus_status':{y:lookup[y,10,20]['status'] for y in ('2025','2026')},'failure_counts':dict(failed),'meaning':'No new setting passes both reused periods. Exact old cells and old costed sleeves are read-only references,not new trials or independent evidence.'}
(T/'comparison.json').write_text(json.dumps(comparison,ensure_ascii=False,indent=2)+'\n')
fig,axes=plt.subplots(1,2,figsize=(12,5),layout='constrained')
values=np.array([c['scenes']['3']['net_return_pct'] for c in r['configs'].values()]);lo,hi=values.min(),values.max()
for ax,y in zip(axes,('2025','2026')):
 z=np.array([[lookup[y,bx,ex]['scenes']['3']['net_return_pct'] for ex in (10,20,30)] for bx in (10,20,30)])
 im=ax.imshow(z,cmap='YlGnBu',vmin=lo,vmax=hi)
 ax.set(xticks=range(3),xticklabels=[10,20,30],yticks=range(3),yticklabels=[10,20,30],xlabel='ETH close-channel exit days',ylabel='BTC close-channel exit days',title=y+' reused 180-day history / 3x cost')
 for i,bx in enumerate((10,20,30)):
  for j,ex in enumerate((10,20,30)):
   c=lookup[y,bx,ex];label=('NEW' if c['is_new'] else 'OLD')+' / '+('PASS' if c['status']=='passed' else 'REJECT')
   ax.text(j,i,f'{z[i,j]:.2f}%\n{label}',ha='center',va='center',fontsize=10,color='white' if z[i,j]>(lo+hi)/2 else '#172126')
fig.colorbar(im,ax=axes,label='Cumulative net return %; not annualized',shrink=.85)
fig.suptitle('Both assets: entry20; original BTC/ETH75/25; NEW=4 portfolios, OLD=14 read-only cells',fontsize=12)
fig.savefig(T/'sensitivity.png',dpi=150);plt.close(fig)
lines=['# 两币独立快退出收盘通道组合：'+T.name,'',f'4个新历史组合、12个1/2/3倍成本场景全部净正；{len(r["summary"]["passed"])}个单年度通过、{len(r["summary"]["rejected"])}个淘汰。新增双期同时通过设置0组。14个精确历史格点、12个实际1500/500USDT组件只读复用。','', '## 事前假设、指标和资金','', '上一轮分别让BTC或ETH保留30日退出。本轮固定两币20日入场，将BTC退出10/20/30日与ETH退出10/20/30日交叉，检验同时较快而不相同的退出能否改善风险和折一致性。仅BTC10/ETH20与BTC20/ETH10两组退出分配在每年份为新配置；其余已有真实结果，按指纹读取旧报告，不改名称重跑。事前焦点BTC退出10日、ETH退出20日；它位于网格边界，不是观察新收益后挑选的最佳点。','', '技术指标仅闭合UTC日收盘通道：决策i用C[i-1]，入场比较max(C[i-21:i-1])，退出比较min(C[i-X-1:i-1])；参考范围止于i-2，排除被比较的收盘。严格上破设多头、严格下破设现金，等号和死区保持desired。下一UTC00:01分钟开盘作为历史成交参考；OOS从现金开始，跨折不重置，期末计成本平仓。源spec、组件指纹和规则原文都保留。','', 'BTC/ETH原始75%/25%是2000USDT初始1500/500独立分仓；不自动归一化、维持权重、转账或再平衡。仅将同资金规模、共同时间轴的成本后绝对NAV相加一次，不二次加权、不平均收益率或Sharpe。成本冲击和数量取整已经在实际1500/500预算下核算。','',f'读取完整{prior["lines"]}行登记、{prior["preserved_ids"]}个保留ID/{prior["canonical"]}个规范定义、{len(prior["conclusions"])}轮全文结论、7个Freqtrade结果文件及4个OOS检查源文件。规范定义包含观察截止；此前实际历史配置2164个，观察定义230个，不混称独立策略。初始16条均核验真实归档/report及SHA，需补测项0。paper10无结果观察保留原样，未当历史策略重试。','', '## 三项验证及门槛','', 'Walk-forward完成：2025、2026分别UTC03-18 00:01至09-14 00:01，每段180天、6个连续30天折。180日滚动历史、3日gap、purge0；固定因果规则，无标签/模型拟合或逐折/OOS调参。每场259382个分钟/执行参考NAV点，完整连续OOS计算整体回撤和逐折指标。两段已反复用于开发，不能称未触碰最终测试集；独立起始资金，不跨年串联复利。','', 'Sensitivity完成：BTC退出×ETH退出同时变化，两张3×3表面，保留所有成本、收益、分钟/日回撤、Sharpe365、Calmar、盈利折、往返和12条邻接边。所有收益为正不表示所有格点通过折一致性；边界最佳点与2sd差异只是描述，不是独立显著性。','', 'Costs完成：手续费10bp/侧、估计半价差1bp、滑点2bp，加0.5×滞后20完整日样本波动率×sqrt(实际预算/滞后20日quoteADV)冲击；四项一起乘1/2/3。参与率上限0.001。Decimal28、PRICE/LOT、最低名义额、5个闭合分钟VWAP百分价格代理、Oct1静态过滤快照沿用。历史盘口缺失、TCA未校准，立即全额LIMIT IOC和历史使用较新过滤快照均为假设；现货只做多，无资金费/借币。未证明真实成交或容量。','', '八项失败门槛冻结不变：所有成本净正、1x至少4/6盈利折、3x分钟整体回撤≤25%、3x邻域净正≥60%、至少2次组件往返、1x毛参考PnL/成本≥2.5、无负余额、期末空仓。旧精确格点保留原status/criteria，不用本轮邻域覆写历史。','',f'新配置失败计数：{dict(failed)}。两组2025新配置均只有3/6盈利折（第一折为零不算盈利），虽总收益为正仍淘汰；2026两组通过只是一段历史资格。完整网格跨两段通过{len(r["summary"]["both_periods_passed_combination_pairs"])}/9，全部属于旧配置。事前焦点状态{comparison["focus_status"]}。同时快退出未获得新的跨期确认。','', '## 新配置按3倍成本收益倒序','', '|年度|技术指标/参数|BTC/ETH原始比例|1x收益%|2x收益%|3x收益%|3x整体分钟回撤%|1x盈利折|3x前五折%|状态|','|---|---|---|---|---|---|---|---|---|---|']
for n,c in sorted(fresh.items(),key=lambda kv:-kv[1]['scenes']['3']['net_return_pct']):
 s=c['scenes'];label=f'BTC收盘通道20/{c["BTC_exit_days"]}；ETH收盘通道20/{c["ETH_exit_days"]}'
 lines.append(f'|{c["year"]}|{label}|75%/25%|{s["1"]["net_return_pct"]:.6f}|{s["2"]["net_return_pct"]:.6f}|{s["3"]["net_return_pct"]:.6f}|{s["3"]["max_drawdown_pct"]:.6f}|{c["positive_folds_1x"]}/6|{s["3"]["first_five_fold_return_pct"]:.6f}|{c["status"]}|')
lines+=['','不同年份独立分组解释，收益是各180天累计，非年化。所有新变体只保留历史证据，不更换冻结P01–P10。','', '## 每个新变体及全部成本/逐折','', '|配置|成本|收益%|分钟整体回撤%|Sharpe365|Calmar|往返|成本占本金%|六折净收益%|失败判据|','|---|---|---|---|---|---|---|---|---|---|']
for n,c in fresh.items():
 for k,s in c['scenes'].items():
  folds=','.join(f'{z["net_return_pct"]:.5f}' for z in s['folds'])
  lines.append(f'|{n}|{k}|{s["net_return_pct"]:.6f}|{s["max_drawdown_pct"]:.6f}|{s["sharpe_365"]:.6f}|{s["calmar"]:.6f}|{s["round_trips"]}|{s["cost_pct_initial"]:.6f}|{folds}|{",".join(c["failed_criteria"])}|')
lines+=['','## 完整敏感性表面（含只读格点）','', '|年度|BTC/ETH退出日数|新配置|1x/2x/3x收益%|3x分钟整体回撤%|状态|','|---|---|---|---|---|---|']
for c in r['configs'].values():
 returns='/'.join(f'{c["scenes"][k]["net_return_pct"]:.6f}' for k in ('1','2','3'))
 lines.append(f'|{c["year"]}|{c["BTC_exit_days"]}/{c["ETH_exit_days"]}|{c["is_new"]}|{returns}|{c["scenes"]["3"]["max_drawdown_pct"]:.6f}|{c["status"]}|')
lines+=['','逐格、逐成本、逐折、回撤、Sharpe、Calmar和成交均在report.json、sensitivity.csv及源归档。sensitivity.png表示实测收益及旧/新状态。','', '## 旧参照及收益路径重复','', '|年度|只读参照|3x收益%|3x分钟整体回撤%|原状态|','|---|---|---|---|---|']
for n,c in r['read_only_comparators'].items():
 z=c['scenes']['3'];lines.append(f'|{c["year"]}|{n}|{z["net_return_pct"]:.6f}|{z["max_drawdown_pct"]:.6f}|{c["status"]}|')
lines+=['',f'与全部既往报告对比：{h["prior_unique_scene_paths"]}个旧整体NAV路径哈希、{h["prior_unique_cross_period_combo_path_pairs"]}个旧跨期全成本配对哈希。本轮12个新配置成本场景中{h["new_scenes_already_in_any_prior_report"]}个整体路径已出现、{h["new_scenes_not_in_any_prior_report"]}个未出现；2026三倍成本仅{h["new_2026_combo_3x_paths_not_in_any_prior_report"]}个此前未见路径。9个未见场景不等于9个独立策略。2026BTC10/ETH20退出与旧BTC10/ETH30退出路径相同；参数仍属新配置，但不能称新市场证据。完整锚差值见comparison.json。','', '## 原SMA延迟shadow续接（与十策略实盘报价分开）','',f'冻结SMA65±1%、75/25账户从{f["resume_utc"]}续至{f["cutoff_utc"]}，仅增加130个已闭合真实分钟mark。8937点完整旧净值前缀保留，现9067点、9059累计分钟、6个完整日；没有新日线决策/执行参考/成交/成本，现金/数量/desired和原交易完全不变。下一决策2026-10-09UTC00:01，原2027-03-31终止计划不变。','', '1/2/3倍成本累计收益：'+ '/'.join(f'{z["net_return_pct"]:.6f}%' for z in f['configs']['forward_snapshot_combo']['scenes'].values())+'。公共分钟响应和取得时间、重叠bar、哈希留档；这是取得时间晚于历史参考分钟的延迟shadow重建，不能冒充paper10当时报价前向业绩。不足180天/六折，继续原账户，不强制退出或从现金重启。','',f'paper10冻结计划与最新第7次实际报价状态保持SHA {prior["paper10_plan_sha256"]} / {prior["paper10_state_sha256"]}。','', '## 数据、检查、复现与结论','', '官方来源：https://github.com/binance/binance-public-data ，访问2026-10-08；文档规定2025起现货归档为微秒并可能修订。实际使用已固定SHA的四个规范分钟parquet，525600条/文件，UTC纳秒连续性与闭合状态逐项检查；实时API响应按毫秒核对。未换数据版本、未将暖机变成早期交易。','', '独立审计重建36个源组件成本场景与54个新/旧组合场景（14,006,628个组合NAV点），核对现金/数量、逐笔参考毛现金流减成本=终值PnL、每折复利=连续OOS终值及整体回撤。旧SMA九场景另核对时序、原前缀和不变状态。7个新定义分别reserve、实际计算、finish；仅4个属于新历史策略配置。负折、正收益但未通过、旧参照均保存。','', '复现：bash research/experiments/'+T.name+'/reproduce.sh；只读重建已存缓存/报告，不HTTP、不写登记、不产生新订单。完整报告、输入来源/哈希、配置、所有stdout与审计保留；大分钟数据和NAV数组留在忽略data。网页只读汇总随后同步。','', '结论：新双快退出设置没有一组在2025/2026均通过。2026通过不能覆盖2025折一致性失败；不改变冻结模拟盘。后续研究应提出不同经济假设或独立资金分配，并继续保留重复使用历史和多重选择的局限，避免精确重复。']
note='复制旧SMA模板时少数描述字段和重放stdout仍带上轮数字；结构化9059分钟/8937点旧前缀/130新mark/9067点现NAV经独立审计正确。原report与代码保持完成登记时SHA，另存forward_annotations.json及errata.md更正说明，不改原账务或补做交易。'
lines.insert(lines.index('## 数据、检查、复现与结论')-1,note)
(T/'result.md').write_text('\n'.join(lines)+'\n')
(T/'forward_result.md').write_text('\n'.join(lines[lines.index('## 原SMA延迟shadow续接（与十策略实盘报价分开）'):lines.index('## 数据、检查、复现与结论')]).rstrip()+'\n')
print(json.dumps({'new_historical_configs':4,'new_both_periods_qualified':0,'failure_counts':dict(failed),'sensitivity_plot':str((T/'sensitivity.png').relative_to(R))},ensure_ascii=False))
