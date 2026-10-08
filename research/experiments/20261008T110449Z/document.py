"""Describe funded EMA-span combinations and explicitly expose repeated return paths."""
from pathlib import Path
import collections,gzip,hashlib,json,subprocess
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
T=Path(__file__).resolve().parent;R=T.parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((T/'report.json').read_text());p=r['plan'];f=json.loads((T/'forward_report.json').read_text());h=json.loads((T/'history_paths.json').read_text());prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()))
baseline=json.loads(subprocess.check_output(['git','show',prior['base_head']+':research/monitor/latest.json'],cwd=R));fresh={n:c for n,c in r['configs'].items() if c['is_new']};lookup={(c['year'],c['BTC_EMA_span_days'],c['ETH_EMA_span_days']):c for c in r['configs'].values()};failed=collections.Counter(k for c in fresh.values() for k in c['failed_criteria'])
eq={}
for year in ('2025','2026'):
 for asset in ('BTC','ETH'):
  hashes={}
  for fp,ref in r['component_sources'].items():
   if ref['year']!=year or ref['asset']!=asset:continue
   arc=json.loads(gzip.decompress((R/ref['archive']).read_bytes()));span=arc['spec']['parameters']['EMA_span_days'];hashes[str(span)]=[arc['scenes'][k]['summary']['NAV_sha256_f64le'] for k in ('1','2','3')]
  assert set(hashes)=={'25','27','29'}
  eq[year+'_'+asset]={'all_cost_NAV_hashes_by_span':hashes,'all_three_spans_same_costed_NAV':len({tuple(v) for v in hashes.values()})==1}
comparison={'report_sha256':sha(T/'report.json'),'matched_diagonal_comparisons':[],'new_both_periods_qualified':len(r['summary']['new_both_periods_passed_combination_pairs']),'full_grid_both_periods_qualified':len(r['summary']['both_periods_passed_combination_pairs']),'focus_status':{y:lookup[y,29,25]['status'] for y in ('2025','2026')},'failure_counts':dict(failed),'source_component_path_equivalence':eq,'scope':'Matched1350/650funding and exact whole-NAV comparison. New parameter definitions need not create new return paths or independent evidence.'}
for n,c in fresh.items():
 for span in (25,27,29):
  old=lookup[c['year'],span,span]
  comparison['matched_diagonal_comparisons'].append({'config':n,'year':c['year'],'comparator':old['name'],'diagonal_span':span,'read_only':True,'return3_difference_pp':c['scenes']['3']['net_return_pct']-old['scenes']['3']['net_return_pct'],'minute_DD3_difference_pp':c['scenes']['3']['max_drawdown_pct']-old['scenes']['3']['max_drawdown_pct'],'all_cost_NAV_identical':all(c['scenes'][k]['NAV_sha256_f64le']==old['scenes'][k]['NAV_sha256_f64le'] for k in ('1','2','3'))})
comparison['focus_all_cost_NAV_identical_to25_diagonal_both_years']=all(next(x for x in comparison['matched_diagonal_comparisons'] if x['config']==lookup[y,29,25]['name'] and x['diagonal_span']==25)['all_cost_NAV_identical'] for y in ('2025','2026'))
(T/'comparison.json').write_text(json.dumps(comparison,ensure_ascii=False,indent=2)+'\n')
fig,axes=plt.subplots(1,2,figsize=(12,5),layout='constrained');values=[c['scenes']['3']['net_return_pct'] for c in r['configs'].values()];lo,hi=min(values),max(values)
for ax,y in zip(axes,('2025','2026')):
 z=np.array([[lookup[y,bs,es]['scenes']['3']['net_return_pct'] for es in (25,27,29)] for bs in (25,27,29)]);im=ax.imshow(z,cmap='YlGnBu',vmin=lo,vmax=hi)
 ax.set(xticks=range(3),xticklabels=[25,27,29],yticks=range(3),yticklabels=[25,27,29],xlabel='ETH EMA span days',ylabel='BTC EMA span days',title=y+' reused 180-day history / 3x cost')
 for i,bs in enumerate((25,27,29)):
  for j,es in enumerate((25,27,29)):
   c=lookup[y,bs,es];label=('NEW' if c['is_new'] else 'OLD')+' / '+('PASS' if c['status']=='passed' else 'REJECT');ax.text(j,i,f'{z[i,j]:.2f}%\n{label}',ha='center',va='center',fontsize=10,color='white' if z[i,j]>(lo+hi)/2 else '#172126')
fig.colorbar(im,ax=axes,label='Cumulative net return %; not annualized',shrink=.85);fig.suptitle('Channel15/30 + EMA band3%; BTC/ETH67.5/32.5; NEW=12 configs, OLD=6 diagonals',fontsize=12);fig.savefig(T/'sensitivity.png',dpi=150);plt.close(fig)
lines=['# 两币独立EMA过滤速度组合：'+T.name,'',f'12个新年度参数配置/36个1、2、3倍成本场景全部净正；{len(r["summary"]["passed"])}通过、{len(r["summary"]["rejected"])}淘汰，6组新参数对分别在两段历史通过。全部36个新场景的完整分钟NAV路径在旧报告已出现，新增收益路径0；事前焦点与原EMA25/25两年全成本净值完全相同。保留为参数稳定性证据，不更换固定模拟盘。','', '## 事前假设、规则与资金','', '前几轮纯收盘通道的入场/退出差异没有新增跨期合格。本轮固定通道15日入场、30日退出、EMA对称3%阈值，将BTC EMA25/27/29与ETH EMA25/27/29交叉，检验两币不同过滤速度能否改变趋势捕获或折一致性。旧中心27/27只读，事前焦点BTC29/ETH25。原21日同资金组件不可用，故在任何新计算前根据既有数据可用性冻结25/27/29；前期报告字段span_days与spec字段EMA_span_days差异已在无新结果时核对，见preflight_notes.json。','', '技术指标为闭合UTC日收盘通道与递推EMA。决策i比较C[i-1]，通道参考max(C[i-16:i-1])/min(C[i-31:i-1])，止于i-2并排除被比较的收盘。严格上破通道且float(C[i-1])>EMA[i-1]×1.03才设多头；严格下破退出通道或float(C[i-1])<EMA[i-1]×0.97设现金，退出优先；等号/死区保留desired，无延迟arming。','', 'EMA使用Python float，alpha=2/(span+1)，E[0]=该年度数据集首个已闭合日收盘，E[j]=(1-alpha)E[j-1]+alpha×float(C[j])；adjust=False，从数据集day0连续递推，不逐折重置。只比较已完成上一日的C与EMA，不用当前未闭合日；EMA种子记忆可以早于滚动训练窗。OOS起点现金/desired-cash，历史成交参考下一UTC00:01分钟开盘，跨折保持状态，期末计成本平仓。','', '原始BTC/ETH67.5%/32.5%是2000USDT初始1350/650独立分仓。无自动归一化、转账、维持比例或再平衡；同资金规模已扣成本的绝对NAV相加一次，不二次乘权重或平均Sharpe/收益。非线性冲击、价格/数量取整已经按源真实1350/650预算计算。','',f'读取完整{prior["lines"]}行登记、{prior["preserved_ids"]}个保留ID/{prior["canonical"]}个规范定义、{len(prior["conclusions"])}轮全文结论、7个Freqtrade文件及4个OOS源文件。此前历史配置{baseline["research"]["counts"]["registered"]}个、观察定义{baseline["research"]["counts"]["observation_records_excluded"]}个，不混称独立试验。初始16条均有实际归档/report与SHA，需补测项0。12个同预算源组件、6个旧对角参数只读，12个非对角年度配置和3个旧SMA截止分别先reserve再计算。','', '## 三项验证与门槛','', 'Walk-forward完成：2025及2026各UTC03-18 00:01至09-14 00:01，180天、6个连续30天诊断折；180日滚动历史、3日gap、purge0，无模型/标签/逐折或OOS拟合。每场259382个分钟/执行参考点，计算逐折和连续OOS整体回撤；两年独立资金，不跨年拼接复利。两段已反复开发，不能称未触碰最终测试集。','', 'Sensitivity完成：BTC和ETH EMA跨度两参数同时变化，两张3×3表面，保存全部成本、净收益、分钟/日回撤、Sharpe365、Calmar、六折及12条邻接边/描述性2sd差异。两段BTC轴的全部成本分钟NAV完全相同，表面变化由ETH组件造成；这提供局部参数不敏感证据，未提供两个独立变化维度或独立市场验证。','', 'Costs完成：手续费10bp/侧、估计半价差1bp、滑点2bp，加0.5×滞后20完整日样本波动率×sqrt(实际预算/滞后20日quoteADV)冲击；四项同乘1/2/3，参与率上限0.001。Decimal28、PRICE/LOT、最低名义额、前5闭合分钟VWAP百分价格代理与Oct1静态过滤快照沿用。立即全额LIMIT IOC、较新过滤快照用于历史均为假设，缺历史盘口/TCA校准，未证明真实接单或容量；现货只做多，无资金费/借币。','', '八门槛不变：所有成本净正、1x≥4/6盈利折、3x分钟整体回撤≤25%、3x邻域净正≥60%、至少2次组件往返、1x毛参考PnL/成本≥2.5、无负余额、期末空仓。旧6个精确对角保持原status/criteria，不覆写旧登记。12新配置通过全部门槛，负收益折依然完整保留。','', '## 2026年按3倍成本收益倒序','', '|BTC/ETH EMA跨度|共同通道/EMA阈值|原始权重|1x收益%|2x收益%|3x收益%|3x分钟整体回撤%|1x盈利折|2025年3x收益%|双期通过|','|---|---|---|---|---|---|---|---|---|---|']
for c in sorted((c for c in fresh.values() if c['year']=='2026'),key=lambda c:-c['scenes']['3']['net_return_pct']):
 s=c['scenes'];other=r['configs'][c['other_period_config']];lines.append(f'|{c["BTC_EMA_span_days"]}/{c["ETH_EMA_span_days"]}|收盘通道15/30＋EMA±3%|67.5%/32.5%|{s["1"]["net_return_pct"]:.6f}|{s["2"]["net_return_pct"]:.6f}|{s["3"]["net_return_pct"]:.6f}|{s["3"]["max_drawdown_pct"]:.6f}|{c["positive_folds_1x"]}/6|{other["scenes"]["3"]["net_return_pct"]:.6f}|{c["both_periods_meet_full_gates"]}|')
lines+=['','收益为各180天累计、非年化。相同收益与回撤不能当多个独立成功；同资金对角锚差值和全路径等价见comparison.json。','', '## 全部新配置、成本和逐折结果','', '|年度配置|成本|收益%|分钟整体回撤%|Sharpe365|Calmar|往返|成本占本金%|六折净收益%|状态|','|---|---|---|---|---|---|---|---|---|---|']
for n,c in fresh.items():
 for k,s in c['scenes'].items():
  folds=','.join(f'{x["net_return_pct"]:.5f}' for x in s['folds']);lines.append(f'|{n}|{k}|{s["net_return_pct"]:.6f}|{s["max_drawdown_pct"]:.6f}|{s["sharpe_365"]:.6f}|{s["calmar"]:.6f}|{s["round_trips"]}|{s["cost_pct_initial"]:.6f}|{folds}|{c["status"]}|')
lines+=['','## 旧对角锚与上下文参照','', '|年度|同预算EMA对角跨度|1x/2x/3x收益%|3x分钟整体回撤%|原状态|','|---|---|---|---|---|']
for c in r['configs'].values():
 if c['is_new']:continue
 returns='/'.join(f'{c["scenes"][k]["net_return_pct"]:.6f}' for k in ('1','2','3'));lines.append(f'|{c["year"]}|{c["BTC_EMA_span_days"]}/{c["ETH_EMA_span_days"]}|{returns}|{c["scenes"]["3"]["max_drawdown_pct"]:.6f}|{c["status"]}|')
lines+=['','零利率现金参照收益0。以下旧持有/SMA/纯通道按原报告保留原资金与分配，不是本批67.5/32.5匹配风险/资金的alpha控制；不缩放旧持有路径或忽略非线性成本。','', '|年度|原报告只读对照|3x收益%|3x分钟整体回撤%|原状态|','|---|---|---|---|---|']
for n,c in r['read_only_comparators'].items():
 s=c['scenes']['3'];lines.append(f'|{c["year"]}|{n}|{s["net_return_pct"]:.6f}|{s["max_drawdown_pct"]:.6f}|{c["status"]}|')
lines+=['','## 参数新颖性与收益路径重复','',f'全历史{h["prior_unique_scene_paths"]}个整体NAV SHA、{h["prior_unique_cross_period_combo_path_pairs"]}个跨期全成本配对SHA。本轮36个新场景{h["new_scenes_already_in_any_prior_report"]}个路径已见、{h["new_scenes_not_in_any_prior_report"]}个未见；合格跨期新路径{h["qualified_cross_period_pairs_not_in_any_prior_report"]}组。参数确有不同、逐个登记并保留passed；未制造新的收益证据。焦点BTC29/ETH25与旧25/25在两年1/2/3倍成本下全部分钟NAV完全相同，未形成收益/回撤改进。','']
start=len(lines);fr=p['forward_resume'];s=f['configs']['forward_snapshot_combo']['scenes']['1'];returns='/'.join(f'{z["net_return_pct"]:.6f}%' for z in f['configs']['forward_snapshot_combo']['scenes'].values())
lines+=['## 原SMA延迟shadow续接（与十策略真实报价账户分开）','',f'原SMA65±1%、75/25从{f["resume_utc"]}至{f["cutoff_utc"]}只增加{fr["new_minutes"]}个真实闭合分钟mark；{fr["prior_NAV_points"]}点旧前缀保持，现{fr["total_NAV_points"]}点、{s["elapsed_minutes"]}累计分钟/{s["elapsed_complete_days"]}完整日。无新日线决策、执行参考、成交或成本；现金/数量/desired及原交易保持。下次决策2026-10-09UTC00:01，原2027-03-31终止计划保持。','',f'1/2/3倍累计收益{returns}。公共原始分钟响应、取得时间、重叠bar和SHA留档；这是延迟shadow重建，不是paper10当时报价业绩。不足180天/6折，原账户继续，不强制退出或重开。','',f'paper10冻结计划/第9次实际报价账户状态SHA不变：{prior["paper10_plan_sha256"]} / {prior["paper10_state_sha256"]}。','']
(T/'forward_result.md').write_text('\n'.join(lines[start:]).rstrip()+'\n')
lines+=['## 数据、审计、复现及结论','', '官方来源：https://github.com/binance/binance-public-data ，访问2026-10-08；现货2025起原始归档时间为微秒且可能修订。本轮固定四个原SHA规范分钟parquet，525600条/文件、UTC纳秒连续/闭合检查；API分钟按毫秒。未换行情版本。','', '实际独立审计36个源组件成本场景与54个新/旧组合场景（14,006,628个组合NAV点），验证现金/数量、参考毛现金流减成本=终值PnL、逐折复利=连续OOS终值与整体回撤；旧SMA九场景另核对原前缀、真实闭合bar与不变状态。15个新定义逐个reserve、实际计算、finish，其中12个为新历史参数配置，3个为原shadow观察截止。所有负折、正收益、失败对照保留。','', '复现：bash research/experiments/'+T.name+'/reproduce.sh；读取既存真实输入/归档重建缓存与完整报告，不HTTP、不写登记、不生成订单。完整spec、report、数据/代码SHA、逐折逐变体、stdout与必要代码留档；大行情/NAV数组留在忽略data。网页只读汇总同步，无需新部署。','', '结论：12个新参数配置通过历史门槛、6组跨期设置，收益路径和跨期路径全部已有。局部过滤速度稳定性得到描述性支持，BTC轴未在这些样本改变源NAV，没有新的经济改进或独立稳定盈利证据。不替换冻结10组账户；后续应优先真正改变执行路径的经济假设并继续避免精确重复。']
(T/'result.md').write_text('\n'.join(lines)+'\n');print(json.dumps({'new_configs':12,'passed':len(r['summary']['passed']),'new_both_periods_qualified':comparison['new_both_periods_qualified'],'new_NAV_paths':h['new_scenes_not_in_any_prior_report'],'focus_equivalent_to_old':comparison['focus_all_cost_NAV_identical_to25_diagonal_both_years']},ensure_ascii=False))
