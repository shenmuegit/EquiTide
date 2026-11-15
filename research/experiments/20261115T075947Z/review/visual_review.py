"""Record actually viewed ROC lookback surface and verify distinct saved native paths."""
import sys,json,gzip
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import sha,put,now,rel
rd=lambda p:json.loads(p.read_text());gz=lambda p:json.loads(gzip.decompress(p.read_bytes()));r=rd(R/'report.json');rows=[]
for c in sorted(r['all_current_grid'].values(),key=lambda c:(c['W'],c['K'])):
 z=c['scenes']['3'];rows.append({'BTC_ROC_L':c['W'],'ETH_funding_R':c['K'],'readonly':c.get('readonly',False),'net_return_pct':z['net_return_pct'],'whole_DD_pct':z['max_drawdown_pct'],'sharpe_365':z['sharpe_365'],'calmar':z['calmar'],'recent_positive_5d':c['recent40_positive_5d_folds_by_cost']['3']})
assert len(rows)==6 and {x['BTC_ROC_L'] for x in rows}=={28,29,30} and {x['ETH_funding_R'] for x in rows}=={.00875,.01} and all(x['recent_positive_5d']==6 for x in rows)
for k in [.00875,.01]:
 old=next(x for x in rows if x['BTC_ROC_L']==29 and x['ETH_funding_R']==k)
 for x in [z for z in rows if z['BTC_ROC_L']!=29 and z['ETH_funding_R']==k]:
  assert x['net_return_pct']<old['net_return_pct'] and x['sharpe_365']<old['sharpe_365'] and x['calmar']<old['calmar']
  assert x['whole_DD_pct']<old['whole_DD_pct'] if x['BTC_ROC_L']==28 else x['whole_DD_pct']>old['whole_DD_pct']
components=sorted([c for c in r['configs'].values() if c['scope']=='native'],key=lambda c:c['W']);assert len(components)==2 and all(c['asset']=='BTC' and c['status']=='rejected' and c['positive_complete_30d_folds_1x']==9 and c['failed_criteria']==['ten_of_thirteen_positive_complete30d_1x_folds'] for c in components)
a,b=[gz(ROOT/c['archive']) for c in components];proof=[]
for k,x in a['scenes'].items():
 y=b['scenes'][k];assert x['summary']['NAV_sha256_f64le']!=y['summary']['NAV_sha256_f64le'];changes=sum(d['desired_direction']!=e['desired_direction'] for d,e in zip(x['decisions'],y['decisions']));assert changes>0;proof.append({'cost':k,'different_actual_desired_days':changes,'same_full_NAV':False,'same_trades':x['trades']==y['trades'],'same_funding':x['funding_events']==y['funding_events']})
put(R/'new_variant_alias_state_verification.json',{'passed':True,'recorded_utc':now(),'components':[c['fingerprint'] for c in components],'source_archives_sha256':{c['archive']:c['archive_sha256'] for c in components},'rows':proof,'actual_different_lookback_paths_not_same_path_alias':True,'no_market_model_account_or_registry_execution':True})
d=rd(R/'conditional_parameter_robustness.json');assert d['heuristic_cliff_flag_count']==3 and rd(R/'NAV_alias_inventory.json')['distinct_allcost_NAV_paths']==6
put(R/'visual_inspection.json',{'passed':True,'recorded_utc':now(),'actual_view_tool':'tools.view_image via functions.exec; generated PNG actually displayed and inspected this round','actually_viewed_image':rel(R/'exports/sensitivity.png'),'image_sha256':sha(R/'exports/sensitivity.png'),'financial_report_sha256':sha(R/'report.json'),'axes':'BTC ROC L28/29/30 rows; ETH R.00875/.01 columns; H3/E.005/V10cap3 fixed,rawbanks1/1,391days,3xcost','actual_saved_values':rows,'six_metric_panels_checked':True,'findings':['OldL29 internal maximum of full net/Sharpe/Calmar; all4newparents lower on these metrics.','L28 DD1.360349% slightly below oldL29 1.362720%, about.00237percentagepoints only; L30 DD1.471096% higher. Small color differences do not establish broad robustness.','Allparentcellsrecent6of8/localstrictrecent1; nativeBTC L28/L30 only9/13positivefullmonths,rejected. L28parents10/13, L30parents12/13; qualification not transferred to components.','Six distinct new paths, no matches to previous actual batch, still same reused market history.','Three raw heuristic cliff flags all retained; no statistical significance claim, no gridextension or preset reselection.'],'no_grid_preset_policy_or_account_recalculation':True,'independent_future_qualified':False})
print('PASS actual6panels,L29betterfullmetrics,L28tinyDDbenefit,L30higherDD,components9/13rejected,6distinctpaths/3flags')
