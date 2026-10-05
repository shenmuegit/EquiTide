"""Read-only compare current new paths against every prior actual report."""
from pathlib import Path
import json,hashlib
T=Path(__file__).resolve().parent;R=T.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
all_scenes=set();all_pairs=set();sources={}
for p in sorted((R/'research/experiments').glob('*/report.json')):
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
v={'report_sha256':sha(T/'report.json'),'all_prior_report_sha256':sources,'prior_unique_scene_paths':len(all_scenes),'prior_unique_cross_period_combo_path_pairs':len(all_pairs),'new_scenes_already_in_any_prior_report':sum(z['NAV_sha256_f64le'] in all_scenes for c in new for z in c['scenes'].values()),'new_scenes_not_in_any_prior_report':sum(z['NAV_sha256_f64le'] not in all_scenes for c in new for z in c['scenes'].values()),'new_2026_combo_3x_paths_not_in_any_prior_report':len({c['scenes']['3']['NAV_sha256_f64le'] for c in new if c['role']=='combination' and c['year']=='2026'}-all_scenes),'qualified_cross_period_pairs_not_in_any_prior_report':len({tuple(r['configs'][n]['scenes'][k]['NAV_sha256_f64le'] for n in pair for k in ('1','2','3')) for pair in pairs}-all_pairs),'scope':'Exact SHA of whole minute NAVs and ordered all-cost paired histories;parameter novelty remains valid even if NAV seen;not independence evidence.'}
(T/'history_paths.json').write_text(json.dumps(v,indent=2)+'\n');print(json.dumps({k:v for k,v in v.items() if k!='all_prior_report_sha256'}))
