"""Reproduce the read-only comparison with the fixed15/30 historical reference."""
import gzip,json
from pathlib import Path
T=Path(__file__).resolve().parent
r=json.loads((T/'report.json').read_text());prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));pairs=r['summary']['new_both_periods_passed_combination_pairs'];rows=[]
for pair in pairs:
 for name in pair:
  c=r['configs'][name];base=next(z for z in r['read_only_comparators'].values() if z['year']==c['year'] and z['kind']=='CHANNEL15_30');a,b=c['scenes']['3'],base['scenes']['3']
  rows.append({'config':name,'year':c['year'],'new_return3_pct':a['net_return_pct'],'new_DD3_pct':a['max_drawdown_pct'],'channel15_30_return3_pct':b['net_return_pct'],'channel15_30_DD3_pct':b['max_drawdown_pct'],'return_difference_pp':a['net_return_pct']-b['net_return_pct'],'DD_difference_pp':a['max_drawdown_pct']-b['max_drawdown_pct']})
observer=lambda s:s.get('family')=='paper-live-portfolio-observation' or s.get('name','').startswith('forward_snapshot_') or 'observation_terminal_action' in s.get('parameters',{})
review={'new_pair_count':len(pairs),'new_fast_ETH_exit10or20_cross_period_pairs':sum(r['configs'][pair[0]]['ETH_exit_days']<30 for pair in pairs),'fixed_channel15_30_comparison':rows,'center2025':next(c['status'] for c in r['configs'].values() if c['year']=='2025' and c['BTC_entry_days']==15 and c['ETH_exit_days']==20),'trial_scope':{'prior_preserved_IDs':len(prior['records']),'prior_canonical_definitions_including_observations':prior['canonical'],'prior_observation_IDs':sum(observer(v['spec']) for v in prior['records'].values()),'new_historical_portfolio_definitions':16,'new_legacy_shadow_cutoff_definitions':3,'interpretation':'Registry definition counts include ongoing observation cutoffs;these are not independent strategy trials or market samples.'},'interpretation':'Historical candidates retained. Faster ETH exits did not generate a dual-period passing variant;no paper10 replacement or claim of a robust improvement.'}
(T/'decision_review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
p=T/'result.md';text=p.read_text();marker='## 与冻结双15/30的补充比较'
if marker not in text:
 lines=[marker,'','同资金、同时间区间、同三倍成本比较：','']
 for row in rows:
  lines.append(f"- {row['config']}：收益{row['new_return3_pct']:.6f}%、回撤{row['new_DD3_pct']:.6f}%；相对旧双15/30收益差{row['return_difference_pp']:.6f}个百分点、回撤差{row['DD_difference_pp']:.6f}个百分点。")
 lines+=['','更快ETH退出10/20日没有新增双期通过组合；新慢退候选不是两个时期同时改进。19个新登记中16个是历史组合、3个是旧SMA观察截止；持续观察不能计为独立策略挖掘试验。保留全部证据，固定10组前向账户继续原计划。','']
 text=text.replace('## 原SMA冻结账户：延迟shadow连续估值','\n'.join(lines)+'\n## 原SMA冻结账户：延迟shadow连续估值');p.write_text(text)
print(json.dumps({'read_only_pair_comparisons':len(rows),'new_fast_ETH_cross_pairs':review['new_fast_ETH_exit10or20_cross_period_pairs']}))
