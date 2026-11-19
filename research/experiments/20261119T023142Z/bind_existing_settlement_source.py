"""Bind immutable older actual settlements and prove the new windows exclude them."""
from common import *
P=ROOT/'research/experiments/20261119T003111Z';rd=lambda p:json.loads(p.read_text());w=rd(R/'account_windows.json');fresh=rd(R/'window_funding_preflight.json');assert fresh['all_pages_completed']
older={}
for f in P.glob('funding*_nov*_preflight.json'):
 target=R/f.name;assert sha(target)==sha(f);doc=rd(target);older[rel(target)]={'original_path':rel(f),'sha256':sha(target),'original_capture_utc':doc['recorded_utc']}
for stem in ['candidate','l4h02','fewm']:
 assert w[stem]['expected_funding_records']==3*sum(len(xs) for xs in w[stem]['expected_funding_by_asset'].values())
 start=int(datetime.fromisoformat(w[stem]['start_utc'].replace('Z','+00:00')).timestamp()*1e9)
 for old in ['funding08_nov17_preflight.json','funding16_nov17_preflight.json']+['funding00_nov18_preflight.json','funding08_nov18_preflight.json']:
  doc=rd(R/old);assert all(int(x['fundingTime'])*1000000<start for rows in doc['public_fields_by_asset'].values() for x in rows)
put(R/'settlement_source_binding.json',{'passed':True,'recorded_utc':now(),'current_public_query_sha256':sha(R/'window_funding_preflight.json'),'older_sources':older,'current_expected_funding_split':{s:w[s]['expected_funding_records'] for s in ['SMA','candidate','l4h02','fewm']},'new_windows_exclude_already_booked_08_and_16':True,'all3_current_windows_start_after_already_booked00':True,'L4_FEWM_start_after_already_booked00':True,'older_sources_copied_without_relabeling_original_capture_time':True,'cashflow_calculations':0,'no_market_or_account_reexecution':True});print('PASS original actual08/16 source bytes and capture times retained; all current windows exclude older already booked settlements;currentnewfundingpredeclaredbutnotcalculated')
