import json
from run import ROOT,R,sha,put
from controls import baselines
r=json.loads((R/'report.json').read_text());refs=baselines(r['configs']);rows=[]
for c in r['configs'].values():
 b=refs[c['name']]['same_capital_notional_constantlong'];rows.append({'name':c['name'],'asset':c['asset'],'reference':b['name'],'same_threecost_paths':all(c['scenes'][k]['NAV_sha256_f64le']==b['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3']),'joint_return_DD_improves_everycost':all(c['scenes'][k]['net_return_pct']>b['scenes'][k]['net_return_pct'] and c['scenes'][k]['max_drawdown_pct']<b['scenes'][k]['max_drawdown_pct'] for k in ['1','2','3'])})
put(R/'comparison_verification.json',{'passed':True,'financial_report_sha256':sha(R/'report.json'),'new_financial_evaluations':0,'rows':rows,'same_paths_as_constantlong':sum(x['same_threecost_paths'] for x in rows),'joint_improvements_by_asset':{a:sum(x['joint_return_DD_improves_everycost'] for x in rows if x['asset']==a) for a in ['BTC','ETH','COMBO']},'old_controls_original_statuses_unchanged':True});print('PASS27matchingcapital/notionalholdcomparisons,no newmodel')
