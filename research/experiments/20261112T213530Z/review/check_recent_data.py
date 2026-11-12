"""Independent public response/bundle association and unchanged-finance check."""
import gzip,hashlib,json,sys,urllib.parse
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import sha,put,now,rel
rd=lambda p:json.loads(p.read_text());prep=rd(R/'recent_data_readiness.json');plan=rd(R/'recent_data_preparation_plan.json');rows=rd(R/'recent_data_capture_attempts.json');assert prep['passed'] and prep['source_HTTP_attempts']==len(rows)==44 and prep['new_financial_configurations_evaluated']==prep['simulated_trades_or_NAV']==prep['registry_events']==prep['account_state_changes']==0
groups={};rawpaths=set()
for z in rows:
 f=ROOT/z['raw'];assert z['raw'] not in rawpaths;rawpaths.add(z['raw']);body=gzip.decompress(f.read_bytes());assert sha(f)==z['sha256'] and len(body)==z['bytes'] and hashlib.sha256(body).hexdigest()==z['body_sha256'] and z['curl_exit_code']==0 and z['http_status']==200
 u=urllib.parse.urlparse(z['url']);q=urllib.parse.parse_qs(u.query);assert u.scheme=='https' and u.netloc=='fapi.binance.com' and u.path in ['/fapi/v1/klines','/fapi/v1/markPriceKlines','/fapi/v1/fundingRate'];asset=q['symbol'][0][:-4];assert asset in ['BTC','ETH'];groups.setdefault((asset,u.path),[]).extend(json.loads(body));assert plan['recorded_before_capture_utc']<=z['started_utc']<=z['finished_utc']
for x in prep['inputs']:assert sha(ROOT/x['path'])==x['sha256'] and (ROOT/x['path']).stat().st_size==x['bytes']
for asset in ['BTC','ETH']:
 packet=json.loads(gzip.decompress(next(ROOT/x['path'] for x in prep['inputs'] if x['path'].endswith(asset+'_public_bundle.json.gz')).read_bytes()));bars=packet['minutes']+packet['terminal_reference_minutes'];assert bars==groups[asset,'/fapi/v1/klines'] and packet['closed_mark_hours']==groups[asset,'/fapi/v1/markPriceKlines'] and packet['actual_funding_with_two_day_context']==groups[asset,'/fapi/v1/fundingRate'];assert len(bars)==27362 and len({int(z[0]) for z in bars})==27362 and all(int(b[0])-int(a[0])==60000 for a,b in zip(bars,bars[1:])) and all(int(z[6])+1==int(z[0])+60000 for z in bars);assert len(packet['closed_mark_hours'])==456 and len(packet['actual_funding_with_two_day_context'])==64 and not packet['current_financial_or_account_results_computed']
assert sha(R/'report.json')==rd(R/'research_verification.json')['report_sha256']==rd(R/'verification.json')['report_sha256']
for stem in ['candidate','l4h02','fewm']:
 v=rd(R/(stem+'_verification.json'));assert v['passed'] and sha(R/(stem+'_observation/report.json'))==v['report_sha256'] and sha(R/(stem+'_observation/state.json'))==v['state_sha256']
put(R/'recent_data_verification.json',{'passed':True,'checked_utc':now(),'actual_HTTP_raw_responses_sha_and_body_sha_checked':44,'bundle_source_associations_checked':2,'closed_no_gap_minute_rows_including_references_per_asset':27362,'hour_rows_per_asset':456,'funding_rows_per_asset_with_context':64,'all_current_financial_and_original_account_report_hashes_unchanged':True,'zero_new_financial_backtests_trades_registry_or_account_writes':True});print('PASS44officialrawresponses->2bundles,27362minutes/456hours/64funds each, original financial/account hashes unchanged')
