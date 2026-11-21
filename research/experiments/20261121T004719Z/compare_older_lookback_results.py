"""Read-only full-rule lookup and saved NAV-signature comparison; no model or account execution."""
import json
from decimal import Decimal
from common import ROOT,R,reg,sha,rel,put,now
rd=lambda p:json.loads(p.read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');report=rd(R/'report.json');reporthash=sha(R/'report.json');own={c['fingerprint'] for c in report['configs'].values()};ignore={'persistence','prior_370day_source_fingerprint'};sources={};oldnative={};oldparents={};rows=[];sig=lambda c:[c['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3']];btc='41de4309229b892489a07574af07a73ae93229a35c118558ed60362285e90c89'
def actual(fp):
 z=records[fp];assert z['result_available'] and sha(ROOT/z['report'])==z['report_sha256'];c=next(c for c in rd(ROOT/z['report'])['configs'].values() if c['fingerprint']==fp);sources[fp]={'report':z['report'],'report_sha256':z['report_sha256'],'archive':c['archive'],'archive_sha256':sha(ROOT/c['archive']),'spec':c['spec'],'spec_sha256':sha(ROOT/c['spec']),'status_unchanged':z['status']};return c
for exit in [4,6]:
 c=next(c for c in report['configs'].values() if c['scope']=='native' and c['W']==exit and c['K']==4);spec=rd(ROOT/c['spec']);target={k:v for k,v in spec['parameters'].items() if k not in ignore};target['entry_funding_max_age_hours']=36
 matches=[fp for fp,z in records.items() if fp not in own and z.get('result_available') and z.get('spec',{}).get('kind')==spec['kind'] and z['spec'].get('universe')==spec['universe'] and {k:v for k,v in z['spec'].get('parameters',{}).items() if k not in ignore}==target];assert len(matches)<=1,matches
 if not matches:continue
 fp=matches[0];oldnative[exit]=actual(fp)
 graph=sorted([(btc,Decimal(1)),(fp,Decimal(1))]);parents=[f for f,z in records.items() if z.get('result_available') and z.get('spec',{}).get('kind')=='combination' and sorted((x['fingerprint'],Decimal(str(x['weight']))) for x in z['spec'].get('components',[]))==graph and z['spec'].get('parameters',{}).get('start_utc')=='2025-10-19T00:01:00Z' and z['spec']['parameters'].get('end_utc')=='2026-11-14T00:01:00Z'];assert len(parents)<=1,parents
 if parents:oldparents[exit]=actual(parents[0])
for c in report['configs'].values():
 old=(oldnative if c['scope']=='native' else oldparents).get(c['W']);row={'fingerprint':c['fingerprint'],'scope':c['scope'],'new_fast_ROC_lookback_days':c['W'],'new_mature_count':c['K'],'new_max_age_hours':48,'old_same_lookback_M4_age36_actual_result_found':old is not None}
 if old:
  row.update(old_fingerprint=old['fingerprint'],new_NAV_signatures=sig(c),old_NAV_signatures=sig(old),same_allcost_complete_NAV=sig(c)==sig(old),new3_net_pct=c['scenes']['3']['net_return_pct'],old3_net_pct=old['scenes']['3']['net_return_pct'])
 rows.append(row)
assert sha(R/'report.json')==reporthash
put(R/'older_lookback_path_comparison.json',{'passed':True,'recorded_utc':now(),'scope':'Posthoc read-only actual older S16 fixed, L4/L6 M4 age36 full-rule lookup and saved 1/2/3cost NAV-hash comparisons. No grid extension, selection, reclassification, new evaluation, or original account execution.','financial_report_sha256_unchanged':reporthash,'old_actual_sources':sources,'rows':rows,'same_complete_cost_paths_to_older_lookback_M4_count':sum(z.get('same_allcost_complete_NAV',False) for z in rows),'complete_registry_IDs_screened':len(records),'full_other_parameters_compared':True,'definition_count_is_not_independent_information_count':True,'missing_actual_reference_not_inferred':True,'old_reports_specs_archives_statuses_not_rewritten':True,'no_strategy_account_or_market_execution':True});print(json.dumps({'passed':True,'old_actual_results_read':len(sources),'new_results_compared':len(rows),'same_complete_allcost_paths':sum(z.get('same_allcost_complete_NAV',False) for z in rows)}))
