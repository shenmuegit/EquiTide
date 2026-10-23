"""Render all new portfolios, matched historical controls and cost/sensitivity evidence."""
import csv,gzip,hashlib,io,json,statistics
from collections import Counter
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run import ROOT,R,reg,sha,put,CAPS,SPANS

def csvwrite(path,rows,compressed=False):
 fields=list(dict.fromkeys(k for x in rows for k in x));b=io.StringIO(newline='');w=csv.DictWriter(b,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows);raw=b.getvalue().encode()
 path.write_bytes(gzip.compress(raw,mtime=0) if compressed else raw)

def main():
 report=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text());ctx=json.loads((R/'context.json').read_text());by={(x['year'],x['BTC_annual_volatility_ceiling'],x['ETH_EMA_span_days']):x for x in report['configs'].values()};rows=[];folds=[];daily=[];costs=[];edges=[]
 control_path=ROOT/'research/experiments/20261009T070950Z/report.json';control=json.loads(control_path.read_text());controls={}
 for name,c in control['configs'].items():
  if c['ETH_channel_entry_days']==15:controls[c['year'],c['BTC_annual_volatility_ceiling']]={'name':name,'fingerprint':c['fingerprint'],'source_report':str(control_path.relative_to(ROOT)),'source_report_sha256':sha(control_path),'scenes':c['scenes'],'status':c['status']}
 report['read_only_matched_controls']={c['name']:c for c in controls.values()};report['read_only_holds']={}
 oldplan=json.loads((ROOT/'research/experiments/20261009T070950Z/spec.json').read_text())
 for ref in oldplan['read_only_comparator_refs']:
  if 'hold_equal2000' in ref['name']:
   assert sha(ROOT/ref['report'])==ref['report_sha256'];cfg=json.loads((ROOT/ref['report']).read_text())['configs'][ref['name']];report['read_only_holds'][ref['year']]={'name':ref['name'],'source_report':ref['report'],'source_report_sha256':ref['report_sha256'],'scenes':cfg['scenes'],'scope':'Total2000USDT50/50buy-hold,not matched75/25risk/allocation;read-only directional context.'}
 for c in report['configs'].values():
  control=controls[c['year'],c['BTC_annual_volatility_ceiling']];c['matched_plain_channel_comparison']={k:{'return_difference_pct':z['net_return_pct']-control['scenes'][k]['net_return_pct'],'minute_drawdown_difference_pct':z['max_drawdown_pct']-control['scenes'][k]['max_drawdown_pct']} for k,z in c['scenes'].items()}
  for k,z in c['scenes'].items():
   meta={'configuration':c['name'],'year':c['year'],'BTC_annual_volatility_ceiling':c['BTC_annual_volatility_ceiling'],'ETH_EMA_span_days':c['ETH_EMA_span_days'],'cost_multiplier':k}
   rows.append({**meta,'net_return_pct':z['net_return_pct'],'minute_drawdown_pct':z['max_drawdown_pct'],'daily_drawdown_pct':z['daily_mark_drawdown_pct'],'daily_sharpe365':z['sharpe_365'],'minute_calmar':z['calmar'],'cost_usdt':z['cost_usdt'],'cost_pct_initial':z['cost_pct_initial'],'gross_reference_pnl_to_cost':z['gross_reference_PnL_to_execution_cost'],'executions':z['executions'],'round_trips':z['round_trips'],'positive_folds':sum(f['net_return_pct']>0 for f in z['folds']),'local3_positive_fraction':c['sensitivity']['local_3x_neighbor_positive_fraction'],'status':c['status'],'paired_periods_passed':c['both_periods_meet_full_gates']})
   folds.extend({**meta,**f} for f in z['folds']);daily.extend({**meta,'daily_boundary_index':i,'NAV_usdt':v} for i,v in enumerate(z['daily_equity_usdt']));costs.append({**meta,'total_cost_usdt':z['cost_usdt'],**{p+'_usdt':v for p,v in z['cost_parts_usdt'].items()}})
 for year in ['2025','2026']:
  for i,cap in enumerate(CAPS):
   for j,span in enumerate(SPANS):
    a=by[year,cap,span]
    for ni,nj,axis in [(i+1,j,'BTC_volatility_ceiling'),(i,j+1,'ETH_EMA_span')]:
     if ni>=3 or nj>=3:continue
     b=by[year,CAPS[ni],SPANS[nj]];edges.append({'year':year,'from':a['name'],'to':b['name'],'axis':axis,'absolute_3x_Sharpe_difference':abs(a['scenes']['3']['sharpe_365']-b['scenes']['3']['sharpe_365'])})
 for year in ['2025','2026']:
  es=[e for e in edges if e['year']==year];cutoff=2*statistics.stdev(e['absolute_3x_Sharpe_difference'] for e in es)
  for e in es:e['threshold']=cutoff;e['descriptive_cliff_flag']=e['absolute_3x_Sharpe_difference']>cutoff
 report['sensitivity_cliffs']={'heuristic':'Adjacent3x dailySharpe difference>2sampleSD;descriptive,not significance.','edges':edges};report['failure_counts']=dict(Counter(k for c in report['configs'].values() for k,v in c['criteria'].items() if not v))
 # Exact repeated numerical paths are disclosed separately from valid parameter novelty.
 records=reg.read_records(ROOT/'research/automation/registry.jsonl');oldpaths=set();oldreports={}
 for path in sorted((ROOT/'research/experiments').glob('*/report.json')):
  if path.parent.name>=R.name:continue
  obj=json.loads(path.read_text());oldreports[str(path.relative_to(ROOT))]=sha(path);cfgs=obj.get('configs',{})
  if not isinstance(cfgs,dict):continue
  for cfg in cfgs.values():
   if not isinstance(cfg,dict):continue
   record=records.get(cfg.get('fingerprint'),{});p=record.get('spec',{}).get('parameters',{});start=p.get('start_utc',p.get('oos_start_utc'));end=p.get('end_utc',p.get('oos_end_exclusive_utc'));capital=p.get('initial_capital_usdt');scenes=cfg.get('scenes',{})
   if not isinstance(scenes,dict):continue
   for z in scenes.values():
    if isinstance(z,dict) and z.get('NAV_sha256_f64le') and start and end and capital:oldpaths.add((start,end,capital,z['NAV_sha256_f64le']))
 seen=0
 for c in report['configs'].values():
  p=json.loads((ROOT/c['spec']).read_text())['parameters'];c['identical_NAV_already_reported']={k:(p['start_utc'],p['end_utc'],2000,z['NAV_sha256_f64le']) in oldpaths for k,z in c['scenes'].items()};seen+=sum(c['identical_NAV_already_reported'].values())
 report['history_path_comparison']={'prior_reports_sha256':oldreports,'prior_exact_same_period_capital_paths':len(oldpaths),'new_parent_cost_scenes_already_seen':seen,'new_parent_cost_scenes_not_seen':54-seen,'scope':'SameUTCstart/end,initialcapital and exact same encoded fullNAV SHA only. A new parameter/configuration is valid even with a known path;none is an independent market sample.'}
 report['research_context']={'prior_canonical_definitions':ctx['canonical_research_definitions_excluding_observations'],'new_parent_configs':18,'new_component_backtests':0,'independent_final_holdout':False,'DSR_PBO_computed':False};report['artifacts']={'full_parent_results':'results/*.json.gz','sensitivity':'sensitivity.csv','fold_results':'fold_results.csv','daily_equity':'daily_equity.csv.gz','costs':'cost_scenarios.csv','surface':'sensitivity_surface.png','verification':'verification.json'};put(R/'report.json',report)
 csvwrite(R/'sensitivity.csv',rows);csvwrite(R/'fold_results.csv',folds);csvwrite(R/'daily_equity.csv.gz',daily,True);csvwrite(R/'cost_scenarios.csv',costs)
 fig,axes=plt.subplots(1,2,figsize=(10,4),constrained_layout=True);limit=max(abs(c['scenes']['3']['net_return_pct']) for c in report['configs'].values())
 for year,ax in zip(['2025','2026'],axes):
  vals=np.array([[by[year,cap,span]['scenes']['3']['net_return_pct'] for span in SPANS] for cap in CAPS]);im=ax.imshow(vals,cmap='RdYlGn',vmin=-limit,vmax=limit);ax.set(xticks=range(3),xticklabels=SPANS,yticks=range(3),yticklabels=CAPS,xlabel='ETH EMA span days',ylabel='BTC annual volatility ceiling',title=year+' 3x cost net return')
  for i in range(3):
   for j in range(3):ax.text(j,i,f'{vals[i,j]:+.2f}%',ha='center',va='center')
 fig.colorbar(im,ax=axes,label='Net return %',shrink=.8);fig.savefig(R/'sensitivity_surface.png',dpi=140);plt.close(fig)
 s=report['summary'];lines=['# BTC波动门槛SMA＋ETH通道EMA：同资金新组合','',f"轮次`{R.name}`，冻结计划SHA256`{report['frozen_plan_sha256']}`。18项新父组合均先reserve后计算，复用12项已完成同资金组件、36成本路径；没有重跑源信号/订单、重登记组件或改写历史状态。",'',
 '## 冻结规则与现金含义','',
 '每组合2000USDT，原值BTC75%/ETH25%代表实际1500/500USDT独立资金袖套。已有组件恰以相同金额、相同日期与各成本核算；两条绝对NAV逐点相加一次，不再乘75/25、不归一化、不调仓、无跨袖套转账或额外换手。组合收益、Sharpe和回撤从总NAV重新计算，不平均组件指标。',
 'BTC固定SMA65，入场上方1.25%、退出下方0.5%；过去21个闭合收盘产生20个log收益，Decimal28样本年化波动sqrt(365×样本方差)，高于40%/50%/60%门槛置现金，其余按原滞回保留desired。ETH固定15日入场/30日退出收盘通道，再联合EMA25/30/35日、对称1.25%缓冲，通道参考排除被比较的收盘；入场两条件同日成立、退出任一条件成立即置现金。EMA原Float adjust=False自数据第一日收盘种子递推，历史规则原样保留。完整每叶spec和来源SHA见plan.component_refs与fixed_rules。',
 '一手参考：[Binance公开归档](https://github.com/binance/binance-public-data)、[pandas EMA递推文档](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html)、[官方交易过滤器](https://developers.binance.com/en/docs/products/spot/filters)，2026-10-23查阅。文档参考不代表盈利背书；本轮不升级库或重算叶策略。', '',
 '## 三项实际验证','',
 '- Walk-forward：两段2025/2026年03-18 00:01至09-14 00:01UTC，各180日/六连续30日折；180日滚动上下文、3日初始间隔。固定规则无拟合/未来标签，purge不适用，源现金/数量/desired跨折连续。两年历史都反复用于研发，不是未触碰最终测试。每折和完整259382点组合NAV指标全部报告；全局与逐折回撤使用原分钟收盘及每日postdecision开盘参考标记，包括初始本金和终点成本，不含分钟内极值。',
 '- 敏感性：每年预设40/50/60% BTC波动门槛×ETH EMA25/30/35日3×3，局部相邻索引矩形含中心；保留所有收益/DD/Sharpe/Calmar、邻域3倍正比例和24条邻接边。陡变标记只作描述。跨期资格要求同参数在两段各自通过，不拼接年份调权，也不按最高收益增加本轮格点。',
 '- 成本：同金额源执行包含每侧10bp手续费、1bp半价差、2bp滑点，加0.5×前20完整日样本波动×sqrt(预算/前20日quote ADV)冲击；参与率≤0.1%，Decimal tick/lot/notional及前置5分钟VWAP代理校验。1/2/3倍同时放大所有成本，终点平仓计费。新组合不另产生调仓，源成本逐项相加；现货无做空/借币/永续资金费。Oct1过滤器是历史代理，缺L2/TCA、排队、延迟和真实IOC成交证明。',
 '门槛：各成本净正、1倍至少4/6正折、3倍分钟整体DD≤25%、局部3倍净正≥60%、至少2往返、1倍毛参考PnL/成本≥2.5、无负现金/数量、无交易/容量拒单、终点空仓。毛成本加回不是独立零成本策略或相对持有alpha。', '',
 '## 实际结果','',f"18配置通过{len(s['passed'])}、淘汰{len(s['rejected'])}；1/2/3倍净正数{s['positive_configs_by_cost']['1']}/{s['positive_configs_by_cost']['2']}/{s['positive_configs_by_cost']['3']}。{len(s['new_both_periods_passed_combination_pairs'])}组参数在两段历史都通过；这只是重复历史验证，不是新前向资格或稳定实盘盈利。",'',
 '|年份|BTC波动门槛|ETH EMA|1倍|2倍|3倍|1倍正折|3倍整体DD|往返|本期状态|两期皆通过|','|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|']
 for c in report['configs'].values():
  a,b,z=[c['scenes'][k] for k in ['1','2','3']];lines.append(f"|{c['year']}|{c['BTC_annual_volatility_ceiling']:.0%}|{c['ETH_EMA_span_days']}|{a['net_return_pct']:+.3f}%|{b['net_return_pct']:+.3f}%|{z['net_return_pct']:+.3f}%|{c['positive_folds_1x']}/6|{z['max_drawdown_pct']:.3f}%|{a['round_trips']}|{c['status']}|{c['both_periods_meet_full_gates']}|")
 lines+=['','失败数量：`'+json.dumps(report['failure_counts'])+'`。','','## 同期只读参考及真实性限制','',
 '六项匹配对照为相同BTC门槛、同1500/500预算而ETH只有15/30通道、不加EMA；完整三成本收益与DD差额逐配置保留。同期买入持有只读复用2000USDT的50/50等额组合，分配与本批75/25不同，作为方向参考，不声称严格风险匹配alpha。现金零收益解析基准0。', '',
 '|年份|50/50持有1倍|2倍|3倍|3倍分钟DD|','|---|---:|---:|---:|---:|']
 for year,x in report['read_only_holds'].items():
  a,b,z=[x['scenes'][k] for k in ['1','2','3']];lines.append(f"|{year}|{a['net_return_pct']:+.3f}%|{b['net_return_pct']:+.3f}%|{z['net_return_pct']:+.3f}%|{z['max_drawdown_pct']:.3f}%|")
 lines+=['',f"计算前完整登记{ctx['registry_events']}事件、{ctx['registry_ids']}ID、{ctx['canonical_research_definitions_excluding_observations']}个规范研究定义及{len(ctx['prior_conclusions_read'])}份既往结论已读；初始16项有实际证据，无待补项。本批无任何旧同组件对，18父配置合法新颖；54条新组合成本路径中{seen}条已在同日期/资本旧报告出现，{54-seen}条未见，不把等价路径当独立市场证据。",'',
 '旧NPY缓存不存在，本轮只在RAM按源position_segments与原SHA行情恢复36条叶曲线，逐条等于原NAV SHA，不重跑旧信号、订单或成本。不缩放旧NAV代替新资金；源金额未变。闭合分钟保留原Polars Float64编码，postdecision开盘保持原生Decimal后才一次转Float64。最初恢复失败与完整exit1日志、1个诊断序列化错误及修正证据保留；未为通过校验修改历史收益。', '',
 '原SMA独立从02:30续至04:30，仅120个闭合分钟，无新日决策/成交；按原现金/数量/desired/费用与完整NAV前缀继续，下一日事件Oct24 00:01，长期终点2027-03-31不变。paper10计划/状态只读，原SMA不是十策略真实报价模拟。详见forward_result.md。', '',
 f"复核：`PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/{R.name}/audit.py`，验证源账本、分钟NAV、54父场景及逐折指标。完整父结果results/*.json.gz、源archive/spec/report与四Parquet哈希保留；不提交可重建大NPY，不改已finish报告字节。历史复用、多重比较和成本代理限制所有结论，未计算DSR/PBO或实盘TCA。",'']
 (R/'result.md').write_text('\n'.join(lines));print(json.dumps({'passed':len(s['passed']),'rejected':len(s['rejected']),'paired_passed':len(s['new_both_periods_passed_combination_pairs']),'old_identical_cost_paths':seen,'failure_counts':report['failure_counts']},ensure_ascii=False),flush=True)
if __name__=='__main__':main()
