"""Read-only compare current new paths against every prior actual report."""
from pathlib import Path
import json,hashlib,gzip
T=Path(__file__).resolve().parent;R=T.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
all_scenes=set();all_pairs=set();sources={}
prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()))
paths=set((R/'research/experiments').glob('*/report.json'))
for record in prior['records'].values():
 p=R/record.get('report','')
 if record.get('result_available') and p.suffix=='.json' and p.is_file() and p.is_relative_to(R/'research/experiments'):paths.add(p)
for p in sorted(paths):
 if p.parent.name>=T.name:continue
 r=json.loads(p.read_text());cs=r.get('configs',{});sources[str(p.relative_to(R))]=sha(p)
 for c in cs.values():
  for z in c.get('scenes',{}).values():
   if 'NAV_sha256_f64le' in z:all_scenes.add(z['NAV_sha256_f64le'])
 for c in cs.values():
  other=cs.get(c.get('other_period_config'),{})
  if c.get('year')=='2025' and c.get('role')=='combination' and other:
   try:all_pairs.add(tuple(x['scenes'][k]['NAV_sha256_f64le'] for x in (c,other) for k in ('1','2','3')))
   except KeyError:pass
r=json.loads((T/'report.json').read_text());pairs=r['summary']['new_both_periods_passed_combination_pairs']
new=[c for c in r['configs'].values() if c['is_new']]
v={'report_sha256':sha(T/'report.json'),'all_prior_report_sha256':sources,'prior_unique_scene_paths':len(all_scenes),'prior_unique_cross_period_combo_path_pairs':len(all_pairs),'new_scenes_already_in_any_prior_report':sum(z['NAV_sha256_f64le'] in all_scenes for c in new for z in c['scenes'].values()),'new_scenes_not_in_any_prior_report':sum(z['NAV_sha256_f64le'] not in all_scenes for c in new for z in c['scenes'].values()),'new_2026_combo_3x_paths_not_in_any_prior_report':len({c['scenes']['3']['NAV_sha256_f64le'] for c in new if c['role']=='combination' and c['year']=='2026'}-all_scenes),'qualified_cross_period_pairs_not_in_any_prior_report':len({tuple(r['configs'][n]['scenes'][k]['NAV_sha256_f64le'] for n in pair for k in ('1','2','3')) for pair in pairs}-all_pairs),'scope':'Exact SHA of whole minute NAVs and ordered all-cost paired histories;include all actual prior registry-referenced JSON reports,including supplementary component reports.Parameter novelty remains valid if path seen;not independence evidence.'}
v['distinct_new_scene_paths_not_in_prior']=len({z['NAV_sha256_f64le'] for c in new for z in c['scenes'].values()}-all_scenes)
v['qualified_pair_histories']=[{'pair':pair,'whole_path_seen_before':tuple(r['configs'][n]['scenes'][k]['NAV_sha256_f64le'] for n in pair for k in ('1','2','3')) in all_pairs} for pair in pairs]
(T/'history_paths.json').write_text(json.dumps(v,indent=2)+'\n');print(json.dumps({k:v for k,v in v.items() if k!='all_prior_report_sha256'}))
