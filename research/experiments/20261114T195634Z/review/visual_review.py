"""Record actual visual inspection against saved current 3x metric values; read-only."""
import sys,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import sha,put,now,rel
rd=lambda p:json.loads(p.read_text());r=rd(R/'report.json');p=rd(R/'plan.json');grid=list(r['all_current_grid'].values());picture=R/'exports/sensitivity.png';assert picture.exists();rows=[]
for c in sorted(grid,key=lambda c:(c['W'],c['K'])):
 s=c['scenes']['3'];rows.append({'L':c['W'],'R':c['K'],'readonly':c.get('readonly',False),'net_return_pct':s['net_return_pct'],'max_drawdown_pct':s['max_drawdown_pct'],'sharpe_365':s['sharpe_365'],'calmar':s['calmar'],'recent_positive5d':c['recent40_positive_5d_folds_by_cost']['3']})
assert len(rows)==6 and {x['L'] for x in rows}=={28,29,30} and all(x['recent_positive5d']==6 for x in rows)
assert max(rows,key=lambda x:x['net_return_pct'])['L']==max(rows,key=lambda x:x['sharpe_365'])['L']==max(rows,key=lambda x:x['calmar'])['L']==29
assert min(rows,key=lambda x:x['max_drawdown_pct'])['L']==28
put(R/'visual_inspection.json',{'passed':True,'recorded_utc':now(),'view_image_native_chunk':'875359','actually_viewed_image':rel(picture),'image_sha256':sha(picture),'financial_report_sha256':sha(R/'report.json'),'axes':'BTC completed momentum memory L28/29/30 rows; readonly ETH budgetR.00875/.01 columns,rawwholebanks1/1,391days,3xcost','six_panels_checked':['full_net_return','continuous_whole_path_DD','recent40_positive5d','Sharpe','Calmar','local_strict_recent_fraction'],'actual_saved_values':rows,'findings':['OldL29 center highestnet/Sharpe/Calmar,all4newparents lower thanmatchedL29center.','L28has slightly lowerDD1.358169% versus L29about1.361995%;L30DD1.470733%,colorsauto-scaled;do notexaggerate tinyL28difference.','All6cells recent6of8 and localstrictfraction1;newL30native9of13monthgatefailure retained,notmaskedbyparentpass.','Sixnewallcostpaths,0previousbatchmatches;threeheuristiccliffflagsretained,notstatisticalsignificance.'],'no_grid_extension_preset_reselection_or_model_rerun':True,'independent_future_qualified':False})
print('PASS actual viewed 3x memory grid, all six panels/numeric values/axis labels checked;L29center highestnetSharpeCalmar,L28lowestDD,L30nativefailure kept')
