"""Bind original settlement bytes and each account's already-booked/pending exact event before reservation."""
from common import *
P=ROOT/'research/experiments/20261120T104213Z';rd=lambda p:json.loads(p.read_text());w=rd(R/'account_windows.json');fresh=rd(R/'window_funding_preflight.json');assert fresh['all_pages_completed']
older={}
for f in P.glob('funding*_nov*_preflight.json'):
 target=R/f.name;assert sha(target)==sha(f);doc=rd(target);older[rel(target)]={'original_path':rel(f),'sha256':sha(target),'original_capture_utc':doc['recorded_utc']}
for stem in ['candidate','l4h02','fewm']:
 assert w[stem]['expected_funding_records']==3*sum(len(xs) for xs in w[stem]['expected_funding_by_asset'].values())
 start=int(datetime.fromisoformat(w[stem]['start_utc'].replace('Z','+00:00')).timestamp()*1e9)
 for old in ['funding08_nov17_preflight.json','funding16_nov17_preflight.json']+['funding00_nov18_preflight.json','funding08_nov18_preflight.json']:
  doc=rd(R/old);assert all(int(x['fundingTime'])*1000000<start for rows in doc['public_fields_by_asset'].values() for x in rows)
first16=rd(R/'funding16_nov18_preflight.json');prior=rd(P/'account_window_verification.json');times16={int(x['fundingTime'])*1000000 for rows in first16['public_fields_by_asset'].values() for x in rows};assert times16
coverage={}
for stem in ['candidate','l4h02','fewm']:
 start=int(datetime.fromisoformat(w[stem]['start_utc'].replace('Z','+00:00')).timestamp()*1e9);end=int(datetime.fromisoformat(w[stem]['cutoff_utc'].replace('Z','+00:00')).timestamp()*1e9)
 before={str(t):prior['full_chain_once_counts'][stem]['funding'].get(str(t),0) for t in times16};assert all(n==6 for n in before.values())
 expected={a:[z for z in first16['public_fields_by_asset'][a] if start<int(z['fundingTime'])*1000000<=end] for a in ['BTC','ETH']}
 for a in ['BTC','ETH']:
  observed=[z for z in w[stem]['expected_funding_by_asset'][a] if int(z['fundingTime'])*1000000 in times16];assert observed==expected[a]
 coverage[stem]={'previous_chain_counts':before,'actual_known16_rows_in_own_new_window':3*sum(map(len,expected.values())),'own_window':[w[stem]['start_utc'],w[stem]['cutoff_utc']]}
put(R/'settlement_source_binding.json',{'passed':True,'recorded_utc':now(),'current_public_query_sha256':sha(R/'window_funding_preflight.json'),'older_sources':older,'current_expected_funding_split':{s:w[s]['expected_funding_records'] for s in ['SMA','candidate','l4h02','fewm']},'new_windows_exclude_all_already_booked_Nov17_and_Nov18_00_08':True,'known_Nov18_16_per_account_coverage_before_reserve':coverage,'all_three_perps_known_actual16_already_booked_before_window':True,'L4_FEWM_known16_already_booked_not_repeated':True,'current16_first_source_sha256':sha(R/'funding16_nov18_preflight.json'),'current16_original_first_capture_utc':first16['recorded_utc'],'older_sources_copied_without_relabeling_original_capture_time':True,'cashflow_calculations':0,'no_market_or_account_reexecution':True});print('PASS immutable first sources;known16 all3alreadybooked/per-account coverage checked;current funding actions derived before reserve,zero cashflow calculations')
