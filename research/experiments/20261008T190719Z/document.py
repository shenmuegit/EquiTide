"""Describe the full frozen EMA20/50/80 grid, matched controls and exact path reuse."""
from pathlib import Path
import collections, gzip, hashlib, json, subprocess
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
T = Path(__file__).resolve().parent; R = T.parents[2]
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
r = json.loads((T/'report.json').read_text()); p = r['plan']
f = json.loads((T/'forward_report.json').read_text()); h = json.loads((T/'history_paths.json').read_text())
prior = json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()))
baseline = json.loads(subprocess.check_output(['git','show',prior['base_head']+':research/monitor/latest.json'],cwd=R))
fresh = {n:c for n,c in r['configs'].items() if c['is_new']}
lookup = {(c['year'],c['BTC_EMA_span_days'],c['ETH_EMA_span_days']):c for c in r['configs'].values()}
values = p['grid']['BTC_EMA_span_days']; focus = p['grid']['predeclared_focus']; center = p['grid']['predeclared_center']
focus_by_year = {y:lookup[y,focus['BTC_EMA_span_days'],focus['ETH_EMA_span_days']] for y in ('2025','2026')}
failed = collections.Counter(k for c in fresh.values() for k in c['failed_criteria'])
equivalence = {}
for year in ('2025','2026'):
    for asset in ('BTC','ETH'):
        hashes = {}
        for ref in r['component_sources'].values():
            if (ref['year'],ref['asset']) != (year,asset): continue
            arc = json.loads(gzip.decompress((R/ref['archive']).read_bytes()))
            hashes[str(arc['spec']['parameters']['EMA_span_days'])] = [arc['scenes'][k]['summary']['NAV_sha256_f64le'] for k in ('1','2','3')]
        assert set(hashes) == {str(v) for v in values}
        equivalence[year+'_'+asset] = {'all_cost_NAV_hashes_by_span':hashes,'distinct_all_cost_paths':len({tuple(v) for v in hashes.values()})}
comparison = {'report_sha256':sha(T/'report.json'),'matched_diagonal_comparisons':[],
              'new_both_periods_qualified':len(r['summary']['new_both_periods_passed_combination_pairs']),
              'full_grid_both_periods_qualified':len(r['summary']['both_periods_passed_combination_pairs']),
              'focus_status':{y:c['status'] for y,c in focus_by_year.items()},'failure_counts':dict(failed),
              'source_component_path_equivalence':equivalence,'qualified_new_pairs_vs50_center':[],
              'scope':'Exact same-funded1350/650 NAV controls;existing statuses retained;new parameter definitions and new paths are not independent market samples.'}
for n,c in fresh.items():
    for span in values:
        old = lookup[c['year'],span,span]
        comparison['matched_diagonal_comparisons'].append({'config':n,'year':c['year'],'comparator':old['name'],'diagonal_span':span,'read_only':True,
            'return_differences_pp':{k:c['scenes'][k]['net_return_pct']-old['scenes'][k]['net_return_pct'] for k in ('1','2','3')},
            'return3_difference_pp':c['scenes']['3']['net_return_pct']-old['scenes']['3']['net_return_pct'],
            'minute_DD3_difference_pp':c['scenes']['3']['max_drawdown_pct']-old['scenes']['3']['max_drawdown_pct'],
            'all_cost_NAV_identical':all(c['scenes'][k]['NAV_sha256_f64le']==old['scenes'][k]['NAV_sha256_f64le'] for k in ('1','2','3'))})
for pair in r['summary']['new_both_periods_passed_combination_pairs']:
    controls = [lookup[r['configs'][n]['year'],center['BTC_EMA_span_days'],center['ETH_EMA_span_days']] for n in pair]
    returns = [r['configs'][n]['scenes'][k]['net_return_pct']-old['scenes'][k]['net_return_pct'] for n,old in zip(pair,controls) for k in ('1','2','3')]
    drawdowns = [r['configs'][n]['scenes']['3']['max_drawdown_pct']-old['scenes']['3']['max_drawdown_pct'] for n,old in zip(pair,controls)]
    comparison['qualified_new_pairs_vs50_center'].append({'pair':pair,'all_returns_nonworse_both_years':all(x>=0 for x in returns),'DD3_nonworse_both_years':all(x<=0 for x in drawdowns),
        'joint_improvement_both_years':all(x>=0 for x in returns) and all(x<=0 for x in drawdowns) and (any(x>0 for x in returns) or any(x<0 for x in drawdowns))})
comparison['focus_vs50_diagonal'] = [x for x in comparison['matched_diagonal_comparisons'] if x['diagonal_span']==50 and x['config'] in {c['name'] for c in focus_by_year.values()}]
comparison['surface_diagnostics']={}
for year in ('2025','2026'):
    cells=[c for c in r['configs'].values() if c['year']==year]
    peak=max(c['scenes']['3']['net_return_pct'] for c in cells)
    best=[c for c in cells if c['scenes']['3']['net_return_pct']==peak]
    sens=next(v for k,v in r['sensitivity'].items() if k.startswith(year+'_'))
    comparison['surface_diagnostics'][year]={'positive3_fraction':sens['metrics']['3']['positive_return_fraction'],'full_gate_pass_fraction':sum(c['status']=='passed' for c in cells)/9,'descriptive_cliff_flags':sum(e['cliff_flag_2sd'] for e in sens['adjacent_edges']),'adjacent_edges':12,'best_return3_coordinates':[[c['BTC_EMA_span_days'],c['ETH_EMA_span_days']] for c in best],'best_on_boundary':any(c['BTC_EMA_span_days'] in (values[0],values[-1]) or c['ETH_EMA_span_days'] in (values[0],values[-1]) for c in best),'scope':'Descriptive sensitivity only,not statistical significance or independent final optimization.'}
previous_path=R/'research/experiments/20261008T170619Z/report.json'
previous=json.loads(previous_path.read_text());comparison['read_only_previous50_30_source']={'path':str(previous_path.relative_to(R)),'sha256':sha(previous_path)}
comparison['focus_vs_previous50_30']=[]
for year in ('2025','2026'):
    old=next(c for c in previous['configs'].values() if c['year']==year and c['BTC_EMA_span_days']==50 and c['ETH_EMA_span_days']==30)
    new=focus_by_year[year]
    comparison['focus_vs_previous50_30'].append({'year':year,'read_only_config':old['name'],'status':new['status'],'return3_difference_pp':new['scenes']['3']['net_return_pct']-old['scenes']['3']['net_return_pct'],'minute_DD3_difference_pp':new['scenes']['3']['max_drawdown_pct']-old['scenes']['3']['max_drawdown_pct']})
(T/'comparison.json').write_text(json.dumps(comparison,ensure_ascii=False,indent=2)+'\n')

fig,axes = plt.subplots(1,2,figsize=(12,5),layout='constrained')
returns = [c['scenes']['3']['net_return_pct'] for c in r['configs'].values()]; lo,hi=min(returns),max(returns)
for ax,y in zip(axes,('2025','2026')):
    z=np.array([[lookup[y,b,e]['scenes']['3']['net_return_pct'] for e in values] for b in values]); im=ax.imshow(z,cmap='YlGnBu',vmin=lo,vmax=hi)
    ax.set(xticks=range(3),xticklabels=values,yticks=range(3),yticklabels=values,xlabel='ETH EMA span days',ylabel='BTC EMA span days',title=y+' reused 180-day history / 3x cost')
    for i,b in enumerate(values):
        for j,e in enumerate(values):
            c=lookup[y,b,e]; status=('NEW' if c['is_new'] else 'OLD')+' / '+('PASS' if c['status']=='passed' else 'REJECT')
            ax.text(j,i,f'{z[i,j]:.2f}%\n{status}',ha='center',va='center',fontsize=10,color='white' if z[i,j]>(lo+hi)/2 else '#172126')
fig.colorbar(im,ax=axes,label='Cumulative net return %; not annualized',shrink=.85)
fig.suptitle('Channel15/30 + EMA band3%; BTC/ETH67.5/32.5; NEW=12 configs, OLD=6 diagonals',fontsize=12)
fig.savefig(T/'sensitivity.png',dpi=150);plt.close(fig)

lines=['# 两币独立EMA20/50/80过滤速度：'+T.name,'',
 f'12个新年度配置/36个1、2、3倍成本场景全净正；{len(r["summary"]["passed"])}通过、{len(r["summary"]["rejected"])}淘汰，{comparison["new_both_periods_qualified"]}组新参数对分别在两段历史通过。{h["new_scenes_already_in_any_prior_report"]}场景路径已见、{h["new_scenes_not_in_any_prior_report"]}场景未见，合格跨期此前未见路径{h["qualified_cross_period_pairs_not_in_any_prior_report"]}种；没有新设置同时提高两期各成本收益并降低两期三倍整体回撤。单年度通过不构成双期资格，固定10组模拟盘继续。','',
 '## 事前假设、指标与资金','',
 '上一轮30/50/70的最高收益落在旧30/30边界；50/30提高两期收益，但2025回撤增加。本轮固定通道15日入场/30日退出与EMA对称3%，扩大两币EMA跨度至20/50/80；事前焦点BTC50/ETH20、旧中心50/50只读。更快ETH可能更早退出反转，也可能增加来回损耗；80日控制检验过慢响应。冻结前仅查源可用性/旧路径身份，未看未登记新组合收益，包含已被历史门槛淘汰的实际源组件。','',
 '决策i只比较闭合UTC日C[i-1]；入场通道max(C[i-16:i-1])、退出min(C[i-31:i-1])止于i-2，排除被比较收盘。严格上破通道且float(C[i-1])>EMA[i-1]×1.03才设多头；严格下破退出通道或float(C[i-1])<EMA[i-1]×0.97设现金，退出优先。等号/死区保留desired，无延迟arming。','',
 'EMA按Python float、alpha=2/(span+1)、E[0]=该年度数据集首个已闭合日收盘，E[j]=(1-alpha)E[j-1]+alpha×float(C[j])，adjust=False。由day0连续递推，不逐折重置，种子记忆可早于滚动训练窗；不用未闭合日线。OOS现金/desired-cash开始，历史成交参考次UTC00:01分钟开盘，跨折保持，期末计成本平仓。','',
 '原始BTC/ETH67.5%/32.5%代表2000USDT初始1350/650独立分仓，无归一化、转账、维持比例或再平衡。复用同预算已经扣成本的绝对NAV并相加一次，不缩放异规模净值、不二次乘权重、不平均收益率或Sharpe；非线性冲击与价格/LOT取整已在实际源预算核算。','',
 f'事前读取完整{prior["lines"]}行登记、{prior["preserved_ids"]}个保留ID/{prior["canonical"]}个规范定义、{len(prior["conclusions"])}轮全文结论、7个Freqtrade文件及4个OOS源码。此前历史配置{baseline["research"]["counts"]["registered"]}个、观察定义{baseline["research"]["counts"]["observation_records_excluded"]}个，不能混称独立试验。12个年度非对角配置和3个原SMA观察截止先独立reserve后计算；12个同资金源组件、6个旧对角结果只读。','',
 '初始16条按原始登记前16行逐一核对真实报告/归档SHA，缺实际结果0；第15/16项保留旧ID并用规范指纹匹配实际结果。150549Z已更正旧排序取样审计，本轮沿用正确顺序。旧carry工程范围由已存短案例恢复，不能称180天验证通过。','',
 '## 三项验证与失败判据','',
 'Walk-forward完成：2025、2026各UTC03-18 00:01至09-14 00:01，各180天/6个连续30天诊断折，180日滚动历史、3日gap、purge0。固定因果规则，无模型/标签/逐折或OOS拟合；每成本场景259382个分钟收盘/执行参考点，以完整连续OOS计算整体回撤。年度资金独立，不串接复利。两段历史反复开发，不能称未触碰最终测试集，亦不对本轮择优作独立证明。','',
 'Sensitivity完成：两币EMA跨度两参数同时变化，两张3×3表面，保存全成本收益、分钟/日整体回撤、Sharpe365、Calmar、六折及12条邻接边/描述性2sd差异。源全成本路径2025 BTC3种/ETH2种、2026 BTC3种/ETH3种，两个轴实际改变交易路径；配置与收益路径仍是同一批市场历史，不能当独立样本。','',
 '2sd相邻差异启发式标记：2025为2/12、2026为12/12条边；标记比较绝对差异与差异标准差，不是显著性检验或过拟合概率。2025最高收益在50/50与50/80并列，2026最高位于旧20/20边界；全图三倍净正100%，仅旧50/50在两期都满足全部门槛（1/9）。2025 BTC20行/ETH20列、2026 BTC80行/ETH80列均折一致性不足；旧2026双80仅1/6盈利折。参数邻域存在可靠性边界，不能认定为稳健平台。','',
 'Costs完成：每侧10bp手续费、估计半价差1bp、滑点2bp，加0.5×滞后20完整日样本波动率×sqrt(实际预算/滞后20日quote ADV)冲击；四项同时放大1/2/3倍，最大参与率0.001。Decimal28、PRICE/LOT、最低名义额、前5闭合分钟VWAP百分价格代理、Oct1静态过滤快照沿用。立即全额LIMIT IOC、较新交易规则快照用于旧历史是估计；缺历史盘口/TCA与真实接单/容量证明。现货只做多，资金费/借币不适用。','',
 f'八门槛冻结：所有成本净正、1x≥4/6盈利折、3x分钟整体回撤≤25%、3x邻域净正≥60%、至少2次组件往返、1x毛参考PnL/成本≥2.5、无负余额及终止空仓。旧对角保留原criteria/status；新失败计数{dict(failed)}，8个淘汰年度配置都仅3/6盈利折。净收益正值不能覆盖真实逐折失败，全部负折留档。','',
 '## 2026年按3倍成本收益倒序','',
 '|BTC/ETH EMA跨度|指标/原始权重|1x收益%|2x收益%|3x收益%|3x分钟整体回撤%|1x盈利折|3x前五折%|2025年3x收益%|双期通过|',
 '|---|---|---|---|---|---|---|---|---|---|']
for c in sorted((c for c in fresh.values() if c['year']=='2026'),key=lambda c:-c['scenes']['3']['net_return_pct']):
    s=c['scenes'];other=r['configs'][c['other_period_config']]
    lines.append(f'|{c["BTC_EMA_span_days"]}/{c["ETH_EMA_span_days"]}|通道15/30＋EMA±3%；67.5/32.5|{s["1"]["net_return_pct"]:.6f}|{s["2"]["net_return_pct"]:.6f}|{s["3"]["net_return_pct"]:.6f}|{s["3"]["max_drawdown_pct"]:.6f}|{c["positive_folds_1x"]}/6|{s["3"]["first_five_fold_return_pct"]:.6f}|{other["scenes"]["3"]["net_return_pct"]:.6f}|{c["both_periods_meet_full_gates"]}|')
lines+=['','收益是各180天累计，非年化。前五折与末折集中度逐场保存，全部负折完整留档。','',
 '## 全部新配置、成本与逐折','',
 '|年度配置|成本|收益%|分钟整体回撤%|Sharpe365|Calmar|往返|成本占本金%|六折收益%|状态|','|---|---|---|---|---|---|---|---|---|---|']
for n,c in fresh.items():
    for k,s in c['scenes'].items():
        folds=','.join(f'{x["net_return_pct"]:.5f}' for x in s['folds'])
        lines.append(f'|{n}|{k}|{s["net_return_pct"]:.6f}|{s["max_drawdown_pct"]:.6f}|{s["sharpe_365"]:.6f}|{s["calmar"]:.6f}|{s["round_trips"]}|{s["cost_pct_initial"]:.6f}|{folds}|{c["status"]}|')
lines+=['','## 同预算旧对角与上下文参照','',
 '|年度|旧EMA跨度|1x/2x/3x收益%|3x分钟整体回撤%|原状态|','|---|---|---|---|---|']
for c in r['configs'].values():
    if c['is_new']: continue
    returns='/'.join(f'{c["scenes"][k]["net_return_pct"]:.6f}' for k in ('1','2','3'))
    lines.append(f'|{c["year"]}|{c["BTC_EMA_span_days"]}/{c["ETH_EMA_span_days"]}|{returns}|{c["scenes"]["3"]["max_drawdown_pct"]:.6f}|{c["status"]}|')
lines+=['','现金参照收益0。以下旧持有/SMA/纯通道按原资金和分配只读，不是本批67.5/32.5匹配风险/资金的alpha控制，不缩放净值。','',
 '|年度|旧对照|3x收益%|3x分钟整体回撤%|原状态|','|---|---|---|---|---|']
for n,c in r['read_only_comparators'].items():
    s=c['scenes']['3'];lines.append(f'|{c["year"]}|{n}|{s["net_return_pct"]:.6f}|{s["max_drawdown_pct"]:.6f}|{c["status"]}|')
lines+=['','## 路径新颖性与经济改进','',
 f'既往{h["prior_unique_scene_paths"]}个整体NAV SHA、{h["prior_unique_cross_period_combo_path_pairs"]}个跨期全成本配对SHA；新36场景{h["new_scenes_already_in_any_prior_report"]}已见/{h["new_scenes_not_in_any_prior_report"]}未见，2026三倍新唯一路径{h["new_2026_combo_3x_paths_not_in_any_prior_report"]}种、合格跨期新路径{h["qualified_cross_period_pairs_not_in_any_prior_report"]}种。两个年度仍是同一批复用市场历史，新路径与新配置不能叫独立市场证据。','']
for y,c in focus_by_year.items():
    s=c['scenes']['3'];diff=next(v for v in comparison['focus_vs50_diagonal'] if v['year']==y)
    lines.append(f'焦点BTC50/ETH20，{y}三倍收益{s["net_return_pct"]:.6f}%、整体回撤{s["max_drawdown_pct"]:.6f}%；相对同预算旧50/50收益差{diff["return3_difference_pp"]:+.6f}个百分点、回撤差{diff["minute_DD3_difference_pp"]:+.6f}个百分点。')
lines+=['','事前焦点50/20在2026通过，但2025仅3/6盈利折而淘汰，未修复原50/30的2025风险交换。相对旧50/30：2025三倍收益低19.410728个百分点、整体回撤高3.846724个百分点；2026三倍收益高0.512803个百分点、回撤低0.318790个百分点。所有12新年度组合没有新的双期通过设置，不替换冻结P01–P10。','']
start=len(lines);fr=p['forward_resume'];returns='/'.join(f'{s["net_return_pct"]:.6f}%' for s in f['configs']['forward_snapshot_combo']['scenes'].values())
lines+=['## 原SMA延迟shadow续接（单独账本）','',
 f'SMA65±1%、BTC/ETH75/25从{f["resume_utc"]}至{f["cutoff_utc"]}增加{fr["new_minutes"]}个真实已闭合分钟mark，{fr["prior_NAV_points"]}点旧前缀保持，现{fr["total_NAV_points"]}点/{fr["cumulative_minutes"]}累计分钟/{fr["cumulative_minutes"]//1440}完整日。无新日线决策、执行参考、成交、成本；原现金/数量/desired/交易保持，下次2026-10-09UTC00:01，原2027-03-31终止计划保持。','',
 f'1/2/3倍累计收益{returns}，依旧不足180天/6折；原账户继续，不强制退出或重开。原始公共分钟响应、实际取得时间、重叠bar和SHA保存，这是延迟shadow重建，与paper10实际观察报价成交分开。','',
 f'paper10保持第13次观察状态；冻结计划SHA {prior["paper10_plan_sha256"]}，状态SHA {prior["paper10_state_sha256"]}，本轮未运行十策略执行器。','']
(T/'forward_result.md').write_text('\n'.join(lines[start:]).rstrip()+'\n')
lines+=['## 数据、复现、检查与结论','',
 '来源：https://github.com/binance/binance-public-data ，访问2026-10-08；原现货归档2025起微秒且可能修订，本轮使用固定SHA的四个规范分钟parquet，525600行/文件、UTC纳秒连续/闭合核对；API分钟为毫秒。未改数据版本。','',
 '独立审计36个源组件成本场景、54个新/旧组合场景及14,006,628个组合净值点；核对现金/数量、毛参考现金流减费用=终值PnL、逐折复利和整体回撤。原SMA九场景另查前缀/时序/不变状态。15个定义均reserve、真实计算、finish；完整只读重放、登记和网页汇总检查留日志，包含正收益、负折、旧失败对照。大行情和NAV数组保存在忽略data，Git仅存轻量充分证据。','',
 '复现：bash research/experiments/'+T.name+'/reproduce.sh；复用真实输入重建缓存与完整报告，不HTTP、不写登记或新下订单。计划、spec、report、代码/数据哈希、全部变体/折、stdout、必要代码与中文说明保留。网页随分支汇总更新，无需重新部署。','',
 f'结论：4个新年度设置通过、8因盈利折不足淘汰；新增跨期合格设置0。EMA20/50/80的双参数敏感性、滚动诊断与1/2/3成本压力完成，焦点2025失败，参数响应边界和重复历史选择限制保留，不称稳定实盘盈利。']
lines+=['','复现执行说明：首次shell会话报告退出143，日志已有全部阶段成功标记；原因未确定，原日志保留在reproduce_attempt1.log。随后用replay_verify.py逐进程运行相同六条只读复现命令，六项返回码及包装进程均为0（reproduction_execution.json/reproduction_note.json），财务报告/登记/输入未改。复核命令：.venv/bin/python research/experiments/'+T.name+'/replay_verify.py。']
(T/'result.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({'passed':len(r['summary']['passed']),'new_paired_parameters':comparison['new_both_periods_qualified'],'new_paired_paths':h['qualified_cross_period_pairs_not_in_any_prior_report'],'joint_improvements':sum(x['joint_improvement_both_years'] for x in comparison['qualified_new_pairs_vs50_center'])}))
