"""Read all already-registered outcomes; compare each new exit with matching old band1percent."""
import json,hashlib,collections
from pathlib import Path
T=Path(__file__).resolve().parent;ROOT=T.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((T/'report.json').read_text());rows=list(r['configs'].values());old={(c['year'],c.get('asset','combination'),c['entry_days']):c for c in rows if not c['is_new']}
comparisons=[]
for c in rows:
 if not c['is_new']:continue
 anchor=old[(c['year'],c.get('asset','combination'),c['entry_days'])]
 assert c['capital_usdt']==anchor['capital_usdt'] and c['raw_weights']==anchor['raw_weights']
 for k,s in c['scenes'].items():
  a=anchor['scenes'][k]
  comparisons.append({'config':c['name'],'anchor':anchor['name'],'year':c['year'],'role':c['role'],'asset':c.get('asset','combination'),'entry_days':c['entry_days'],'exit_days':c['exit_days'],'EMA_band':c['EMA_band'],'cost':k,'NAV_identical':s['NAV_sha256_f64le']==a['NAV_sha256_f64le'],'net_return_delta_pct':s['net_return_pct']-a['net_return_pct'],'minute_DD_delta_pct':s['max_drawdown_pct']-a['max_drawdown_pct'],'first_five_fold_return_delta_pct':s['first_five_fold_return_pct']-a['first_five_fold_return_pct']})
assert len(comparisons)==108
pairs=r['summary']['new_both_periods_passed_combination_pairs']
qualified_same=all(all(r['configs'][n]['scenes'][k]['NAV_sha256_f64le']==old[(r['configs'][n]['year'],'combination',r['configs'][n]['entry_days'])]['scenes'][k]['NAV_sha256_f64le'] for k in ('1','2','3')) for pair in pairs for n in pair)
d={'source_report_sha256':sha(T/'report.json'),'comparisons':comparisons,'identical_new_scenes_to_matching_old_band1pct':sum(x['NAV_identical'] for x in comparisons),'new_qualified_parameter_pairs':len(pairs),'all_new_cross_period_qualified_NAVs_identical_to_old_exit30':qualified_same,'new_cross_period_qualified_distinct_NAV_pairs':len({tuple(r['configs'][n]['scenes'][k]['NAV_sha256_f64le'] for n in pair for k in ('1','2','3')) for pair in pairs if any(r['configs'][n]['scenes'][k]['NAV_sha256_f64le']!=old[(r['configs'][n]['year'],'combination',r['configs'][n]['entry_days'])]['scenes'][k]['NAV_sha256_f64le'] for n in pair for k in ('1','2','3'))}),'failure_counts':dict(collections.Counter(k for c in rows if c['is_new'] for k in c['failed_criteria'])),'combo_2026_unique_3x_NAVs':len({c['scenes']['3']['NAV_sha256_f64le'] for c in rows if c['year']=='2026' and c['role']=='combination'}),'all_2026_combo_first5_3x_return_pct':sorted({c['scenes']['3']['first_five_fold_return_pct'] for c in rows if c['year']=='2026' and c['role']=='combination'}),'interpretation':'Rule variants are new configurations, not independent market regimes. Read actual EMA-band0.5/2.5percent comparisons and qualification counts;configuration novelty is not independent market evidence.'}
anchor2026={c['scenes']['3']['NAV_sha256_f64le'] for c in rows if c['year']=='2026' and c['role']=='combination' and not c['is_new']}
d['combo_2026_new_3x_NAVs_not_in_anchor']=len({c['scenes']['3']['NAV_sha256_f64le'] for c in rows if c['year']=='2026' and c['role']=='combination' and c['is_new']} - anchor2026)
(T/'diagnostic.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in d.items() if k!='comparisons'},ensure_ascii=False))
