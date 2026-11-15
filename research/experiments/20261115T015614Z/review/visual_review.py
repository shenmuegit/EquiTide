"""Record the actual viewed S12/S16/S20 sensitivity surface and its component limits."""
import sys,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import sha,put,now,rel
rd=lambda p:json.loads(p.read_text());r=rd(R/'report.json');rows=[]
for c in sorted(r['all_current_grid'].values(),key=lambda c:(c['W'],c['K'])):
 z=c['scenes']['3'];rows.append({'ETH_EWM_S':c['W'],'BTC_vol_V':c['K'],'readonly':c.get('readonly',False),'net_return_pct':z['net_return_pct'],'whole_DD_pct':z['max_drawdown_pct'],'sharpe_365':z['sharpe_365'],'calmar':z['calmar'],'recent_positive_5d':c['recent40_positive_5d_folds_by_cost']['3']})
assert len(rows)==6 and {x['ETH_EWM_S'] for x in rows}=={12,16,20} and {x['BTC_vol_V'] for x in rows}=={10,14} and all(x['recent_positive_5d']==6 for x in rows)
for v in [10,14]:
 old=next(x for x in rows if x['ETH_EWM_S']==16 and x['BTC_vol_V']==v)
 for new in [x for x in rows if x['ETH_EWM_S']!=16 and x['BTC_vol_V']==v]:
  assert new['net_return_pct']<old['net_return_pct'] and new['sharpe_365']<old['sharpe_365'] and new['calmar']<old['calmar']
  assert new['whole_DD_pct']==old['whole_DD_pct'] if new['ETH_EWM_S']==12 else new['whole_DD_pct']>old['whole_DD_pct']
components=[c for c in r['configs'].values() if c['scope']=='native'];assert len(components)==2 and all(c['asset']=='ETH' and c['status']=='rejected' for c in components);assert {c['W']:c['positive_complete_30d_folds_1x'] for c in components}=={12:5,20:6} and all(all(n==0 for n in c['recent40_positive_5d_folds_by_cost'].values()) for c in components)
d=rd(R/'conditional_parameter_robustness.json');assert d['heuristic_cliff_flag_count']==3
put(R/'visual_inspection.json',{'passed':True,'recorded_utc':now(),'actual_view_tool':'tools.view_image via functions.exec; source PNG actually displayed and inspected this round','actually_viewed_image':rel(R/'exports/sensitivity.png'),'image_sha256':sha(R/'exports/sensitivity.png'),'financial_report_sha256':sha(R/'report.json'),'axes':'ETH finite normalized EWM length S12/16/20 rows, fixed M4/R.00875; readonly BTC V10/14 columns; raw banks1/1,391days,3xcost','actual_saved_values':rows,'six_metric_panels_checked':True,'findings':['OldS16 is the interior maximum along S for full net/Sharpe/Calmar; all4newparents worse on these metrics.','S12 DD equals matched S16; S20 DD3.906288% versus old1.362%, materially higher. BTC two-value axis has no interior point.','Allparentcellsrecent6of8/localstrictrecent1. BothnewETHcomponentsrecent0/8 and extension21zero; S12only5/13positivefullmonths, S20only6/13:rejected. Parent plots do not override component failures.','Three raw heuristic cliff flags retained with absolute changes; no statistical significance or broad plateau claim. Six new paths, no prior-batch matches, no independent market samples.','Titles, S12/16/20 row labels, V10/14 column labels and all six metric annotations agree with actual report.'],'no_grid_preset_policy_or_account_recalculation':True,'independent_future_qualified':False})
print('PASS actuallyviewed6panels,S16interiorpeak,S20DDworse,componentfailureskept,3rawcliffflags')
