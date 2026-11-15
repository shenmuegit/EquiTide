"""Record actually viewed ETH median/BTC memory sensitivity, including rejected component limitations."""
import sys,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import sha,put,now,rel
rd=lambda p:json.loads(p.read_text());r=rd(R/'report.json');rows=[]
for c in sorted(r['all_current_grid'].values(),key=lambda c:(c['W'],c['K'])):
 z=c['scenes']['3'];rows.append({'ETH_median_M':c['W'],'BTC_vol_V':c['K'],'readonly':c.get('readonly',False),'net_return_pct':z['net_return_pct'],'whole_DD_pct':z['max_drawdown_pct'],'sharpe_365':z['sharpe_365'],'calmar':z['calmar'],'recent_positive_5d':c['recent40_positive_5d_folds_by_cost']['3']})
assert len(rows)==6 and {x['ETH_median_M'] for x in rows}=={2,3,4} and {x['BTC_vol_V'] for x in rows}=={10,14} and all(x['recent_positive_5d']==6 for x in rows)
for v in [10,14]:
 old=next(x for x in rows if x['ETH_median_M']==4 and x['BTC_vol_V']==v)
 for new in [x for x in rows if x['ETH_median_M']!=4 and x['BTC_vol_V']==v]:assert new['net_return_pct']<old['net_return_pct'] and new['sharpe_365']<old['sharpe_365'] and new['whole_DD_pct']==old['whole_DD_pct']
components=[c for c in r['configs'].values() if c['scope']=='native'];assert len(components)==2 and all(c['asset']=='ETH' and c['status']=='rejected' and c['positive_complete_30d_folds_1x']==6 for c in components);assert all(all(n==0 for n in c['recent40_positive_5d_folds_by_cost'].values()) for c in components)
d=rd(R/'conditional_parameter_robustness.json');assert d['heuristic_cliff_flag_count']==3
put(R/'visual_inspection.json',{'passed':True,'recorded_utc':now(),'viewed_image_tool_group_native_chunk':'6b914c','actually_viewed_image':rel(R/'exports/sensitivity.png'),'image_sha256':sha(R/'exports/sensitivity.png'),'financial_report_sha256':sha(R/'report.json'),'axes':'ETHpastmaturedfundingmedianM2/3/4 rows,fixedR.00875;readonlyBTCV10/14columns;rawbanks1/1,391days,3xcost','actual_saved_values':rows,'six_metric_panels_checked':True,'findings':['All4newparentslower net/Sharpe/Calmar than matchedoldM4;no wholepathDD reduction.','OldM4/BTCV14 bestatMboundary;noafterresultgridextension.','Allparentcellsrecent6of8/localrecentfraction1;theseplotsdo notshowstandaloneETHqualification. BothnewETHcomponentsonly6/13positivefullmonths,recent0/8 and extension21zero:rejected.','DDplotuses+1.362offset:BTCV10vs14differenceabout.000725percentagepoints,notdramaticabsoluteeffect.','3heuristiccliffflagskeptwithactualdeltas,not statistical significance;6newpaths,0priorbatchmatches,not independentmarketsamples.'],'no_grid_preset_policy_or_account_recalculation':True,'independent_future_qualified':False})
print('PASS viewedM2/M3/M4xBTCV10/V14sixpanels;oldM4better,ETHcomponentfailuresnotmasked,3rawcliffflagsretained')
