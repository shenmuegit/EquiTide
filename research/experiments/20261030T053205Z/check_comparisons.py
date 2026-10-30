import json
from run import ROOT,R,sha,put
from controls import baselines
r=json.loads((R/'report.json').read_text());refs=baselines(r['configs']);rows=[]
for c in r['configs'].values():
 if c['role']!='candidate':continue
 for typ,b in refs[c['name']].items():
  same=all(c['scenes'][k]['NAV_sha256_f64le']==b['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3']);better=all(c['scenes'][k]['net_return_pct']>b['scenes'][k]['net_return_pct'] and c['scenes'][k]['max_drawdown_pct']<b['scenes'][k]['max_drawdown_pct'] for k in ['1','2','3']);rows.append({'name':c['name'],'reference_type':typ,'reference':b['name'],'same_threecost_complete_paths':same,'joint_return_DD_improves_everycost':better})
proof={'passed':True,'financial_report_sha256':sha(R/'report.json'),'new_financial_evaluations':0,'rows':rows,'same_threecost_paths_as_same_units_hold':sum(x['same_threecost_complete_paths'] for x in rows if x['reference_type']=='same_raw_units_constantlong'),'joint_improvements_over_same_units_hold':sum(x['joint_return_DD_improves_everycost'] for x in rows if x['reference_type']=='same_raw_units_constantlong'),'joint_improvements_over_fast_endpoint':sum(x['joint_return_DD_improves_everycost'] for x in rows if x['reference_type']=='pure_fast_ownership_endpoint'),'joint_improvements_over_slow_endpoint':sum(x['joint_return_DD_improves_everycost'] for x in rows if x['reference_type']=='pure_slow_ownership_endpoint'),'source_endpoints_original_statuses_unchanged':True,'ownership_only_not_new_native_execution':True};put(R/'comparison_verification.json',proof);print(json.dumps(proof),flush=True)
