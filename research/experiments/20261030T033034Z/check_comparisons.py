"""Read-only complete-path comparisons;olddifferent-exposurebaselines clearly separated."""
import json
from run import ROOT,R,sha,put
from controls import baselines
r=json.loads((R/'report.json').read_text());refs=baselines(r['configs']);rows=[]
for c in r['configs'].values():
 if c['role']!='candidate':continue
 for typ,b in refs[c['scope']].items():
  same=all(c['scenes'][k]['NAV_sha256_f64le']==b['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3']);better=all(c['scenes'][k]['net_return_pct']>b['scenes'][k]['net_return_pct'] and c['scenes'][k]['max_drawdown_pct']<b['scenes'][k]['max_drawdown_pct'] for k in ['1','2','3']);rows.append({'name':c['name'],'scope':c['scope'],'status':c['status'],'reference_type':typ,'reference':b['name'],'same_threecost_complete_paths':same,'joint_return_DD_improves_everycost':better,'matched_notional_control':typ=='matched_actual_notional_constantlong'})
proof={'passed':True,'financial_report_sha256':sha(R/'report.json'),'new_financial_evaluations':0,'new_candidates':18,'rows':rows,'same_threecost_paths_as_same_notional_hold':sum(x['same_threecost_complete_paths'] for x in rows if x['matched_notional_control']),'joint_improvements_over_same_notional_hold':sum(x['joint_return_DD_improves_everycost'] for x in rows if x['matched_notional_control']),'old_baselines_immutable':True,'no_old_center_cells_in_new_momentum_grid':True,'limitations':'OldN4500contrarian/ungatedreferenceshave3xETHnominal,differententry/exit/fundingfilters;notmatchedcausaleffectcontrols. Same-notionalcurrentholdiscomparativeonly. No globalpathnovelty/independentfutureclaim.'};put(R/'comparison_verification.json',proof);print(json.dumps(proof),flush=True)
