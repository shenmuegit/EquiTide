"""Check both BTC axes, full bank sizing and chronological account/funding boundaries before reserve."""
import ast,re
from common import *
rd=lambda p:json.loads(p.read_text());p=rd(R/'plan.json');w=rd(R/'account_windows.json');P=ROOT/'research/experiments/20261128T021407Z';assert not(R/'reserve_batches').exists();ac=['SMA','candidate','l4h02','fewm'];dc={a:len(w[a]['expected_daily_events_utc']) for a in ac};fc={a:w[a]['expected_funding_records'] for a in ac};assert dc=={'SMA':0,'candidate':0,'l4h02':0,'fewm':0} and fc=={'SMA':0,'candidate':6,'l4h02':0,'fewm':0}
a=rd(R/'all_actual_funding_prebinding.json');assert a['source_count']==13
for z in a['sources']:
 q=rd(ROOT/z['path']);assert q['passed'] and q['before_any_current_reservation'] and sha(ROOT/z['path'])==z['sha256'] and sha(ROOT/q['source'])==q['sha256']
 expected_prior=None
 for name,ts in q['prior_unique_counts'].items():
  for t,count in ts.items():
   expected_inc=(6 if name=='candidate' else 0) if z['key']=='Nov27_08' else 0
   assert count==(0 if z['key']=='Nov27_08' and name=='candidate' else 6) and q['expected_current_increment_counts'][name][t]==expected_inc and count+expected_inc<=q['maximum_once_counts_by_timestamp'][t]
q=rd(R/'actual00_nov27_prebinding_source.json');assert q['sha256']=='df07c084e681d205d31c00d48adfa81c78cfc9227903dc3dffe694debfaf5902' and q['first_capture_utc']=='2026-11-27T16:33:56.662528Z';assert all(int(z['fundingTime'])*1000000==1795737600000000000<1795737660000000000 for xs in q['actual_public_fields'].values() for z in xs)
q13=rd(R/'actual08_nov27_prebinding_source.json');assert q13['sha256']=='7bd680daa658c9ef5f08174224dd174f3f7ede34d585e5bd2edda88d8a6454c0' and q13['first_capture_utc']=='2026-11-28T00:36:04.324220Z' and all(int(z['fundingTime'])==1795766400001 for xs in q13['actual_public_fields'].values() for z in xs)
full=rd(R/'SMA_full79_prebinding.json');assert full['passed'] and full['current_original_daily_event_count']==0 and full['full79_exact_original78_prefix'] and sha(ROOT/full['authority'])==full['sha256'] and rd(R/'SMA_old77_76_prefix_verification.json')['full77_exact_original76_prefix'] and rd(R/'SMA_markonly_kernel_identity.json')['original_Float_mark_arithmetic_exact_source_identity']
for n in ['engine.py','core391_tail_safe.py','market.py','portfolio.py','audit_native.py','observe_l4h02.py','observe_fewm.py','audit_incremental.py']:assert sha(R/n)==sha(P/n)
assert p['axes']=={'BTC_MAIN_LOOKBACK_DAYS':[28,29,30],'ETH_TREND_SLOPE_LAG_DAYS':[2,3,4]} and len(p['grid'])==9 and not p['native_grid'] and len(rd(R/'batch.json'))==4 and len(p['read_only_references'])==14
selector=next(z for z in ast.parse((R/'saved_review.py').read_text()).body if isinstance(z,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='rep' for t in z.targets));ns={'p':p,'r':{'configs':{z['fingerprint']:z for z in rd(R/'batch.json')}}};exec(compile(ast.Module(body=[selector],type_ignores=[]),'<pre-reserve representative selection>','exec'),ns);assert ns['rep']['fingerprint']==p['base_parent_fingerprint'] and ns['rep']['scope']=='parent' and (ns['rep']['W'],ns['rep']['K'])==(28,2)
archive=rd(R/'registry_archive_plan.json');assert archive['own_finished_IDs']==16 and archive['own_raw_reserve_finish_events']==32
monthly=rd(R/'candidate_completed_fold_audit_plan.json');assert monthly['planned_before_any_reserve'] and monthly['route_from_first_readonly_audit_attempt'] and monthly['current_complete30day_folds']==1 and sha(R/'audit_candidate_30day_recovery.py')==monthly['planned_source_sha256']
for n in R.glob('*.py'):
 assert not n.read_bytes().endswith(b'\n\n'),n
 ast.parse(n.read_text())
put(R/'boundary_unit_verification.json',{'passed':True,'current_daily_event_counts':dc,'actual_funding_counts':fc,'all13sources_prior_and_own_current_coverage_checked':True,'full79_old78_77_76prefix_originalFloat_marks_verified':True,'source12_actual_funding_before_own_original_daily_decision':True,'representative_parent_selection_exercised':True,'own_IDs':16,'own_events':32,'all_source_EOF_checked_before_binding':True,'before_any_current_reservation':True});print('PASS13firstsources/C_funding6_SMA_LF_funding0_daily0/full79/16ID32events')
