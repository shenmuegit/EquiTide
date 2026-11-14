"""Compare current saved full-bank paths to the previous actual batch, without rerunning."""
import gzip,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import *
rd=lambda p:json.loads(p.read_text());gz=lambda p:json.loads(gzip.decompress(p.read_bytes()));P=ROOT/'research/experiments/20261114T115333Z';prior=rd(P/'report.json');current=rd(R/'report.json');rs=reg.read_records(ROOT/'research/automation/registry.jsonl');rows=[]
for z in prior['configs'].values():assert rs[z['fingerprint']]['report_sha256']==sha(P/'report.json') and rs[z['fingerprint']]['result_available'] and sha(ROOT/z['archive'])==z['archive_sha256']
for c in current['configs'].values():
 sig=tuple(c['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3']);matches=[z for z in prior['configs'].values() if z['scope']==c['scope'] and tuple(z['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3'])==sig];details=[]
 for z in matches:
  same=None
  if c['scope']=='native':
   a,b=gz(ROOT/c['archive']),gz(ROOT/z['archive']);same=all(x['trades']==y['trades'] and x['funding_events']==y['funding_events'] and all((d['desired_direction'],d['state_before'],d['state_after'])==(e['desired_direction'],e['state_before'],e['state_after']) for d,e in zip(x['decisions'],y['decisions'])) for k in ['1','2','3'] for x,y in [(a['scenes'][k],b['scenes'][k])]);assert same
  details.append({'prior_fingerprint':z['fingerprint'],'prior_name':z['name'],'prior_archive':z['archive'],'prior_archive_sha256':z['archive_sha256'],'same_full_allcost_NAV':True,'same_native391_desired_book_states_trades_funding':same})
 rows.append({'fingerprint':c['fingerprint'],'name':c['name'],'scope':c['scope'],'matches':details})
put(R/'historical_path_alias_verification.json',{'passed':True,'verified_utc':now(),'financial_report_sha256':sha(R/'report.json'),'prior_actual_report':rel(P/'report.json'),'prior_actual_report_sha256':sha(P/'report.json'),'rows':rows,'new_configs_matching_previous_actual_paths':sum(bool(z['matches']) for z in rows),'parent_configs_matching_previous_actual_paths':sum(z['scope']=='parent' and bool(z['matches']) for z in rows),'scope':'Previous actual batch, supplemental to the8 preregistered grid references; saved NAV/state comparisons only,no model/data/account/registry calls or status changes.','different_fingerprints_not_independent_market_paths':True,'financial_or_account_recalculations':0});print('PASS previousactual batch path matches',sum(bool(z['matches']) for z in rows),'of6newdefinitions')
