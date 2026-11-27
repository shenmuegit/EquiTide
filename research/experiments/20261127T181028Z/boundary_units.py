"""Check both BTC axes, full bank sizing and chronological account/funding boundaries before reserve."""
import ast,re
from common import *
rd=lambda p:json.loads(p.read_text());p=rd(R/'plan.json');w=rd(R/'account_windows.json');P=ROOT/'research/experiments/20261127T160858Z';assert not(R/'reserve_batches').exists();ac=['SMA','candidate','l4h02','fewm'];dc={a:len(w[a]['expected_daily_events_utc']) for a in ac};fc={a:w[a]['expected_funding_records'] for a in ac};assert dc=={'SMA':0,'candidate':0,'l4h02':1,'fewm':1} and fc=={'SMA':0,'candidate':0,'l4h02':6,'fewm':6}
a=rd(R/'all_actual_funding_prebinding.json');assert a['source_count']==12
for z in a['sources']:
 q=rd(ROOT/z['path']);assert q['passed'] and q['before_any_current_reservation'] and sha(ROOT/z['path'])==z['sha256'] and sha(ROOT/q['source'])==q['sha256']
 expected_prior=0 if z['key']=='Nov27_00' else 6
 for name,ts in q['prior_unique_counts'].items():
  for t,count in ts.items():assert count==expected_prior and q['expected_current_increment_counts'][name][t]==(6 if z['key']=='Nov27_00' and name in ['l4h02','fewm'] else 0) and count+q['expected_current_increment_counts'][name][t]<=q['maximum_once_counts_by_timestamp'][t]
q=rd(R/'actual00_nov27_prebinding_source.json');assert q['sha256']=='df07c084e681d205d31c00d48adfa81c78cfc9227903dc3dffe694debfaf5902' and q['first_capture_utc']=='2026-11-27T16:33:56.662528Z';assert all(int(z['fundingTime'])*1000000==1795737600000000000<1795737660000000000 for xs in q['actual_public_fields'].values() for z in xs)
full=rd(R/'SMA_full78_prebinding.json');assert full['passed'] and full['current_original_daily_event_count']==0 and full['full78_exact_original77_prefix'] and sha(ROOT/full['authority'])==full['sha256'] and rd(R/'SMA_old77_76_prefix_verification.json')['full77_exact_original76_prefix'] and rd(R/'SMA_markonly_kernel_identity.json')['original_Float_mark_arithmetic_exact_source_identity']
for n in ['engine.py','core391_tail_safe.py','market.py','portfolio.py','audit_native.py','observe_l4h02.py','observe_fewm.py','audit_incremental.py']:assert sha(R/n)==sha(P/n)
assert p['axes']=={'BTC_MAIN_LOOKBACK_DAYS':[28,29,30],'BTC_ENTRY_RETURN_HURDLE':[.0275,.03,.0325]} and len(p['grid'])==len(p['native_grid'])==9 and len(rd(R/'batch.json'))==12 and len(p['read_only_references'])==10
selector=next(z for z in ast.parse((R/'saved_review.py').read_text()).body if isinstance(z,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='rep' for t in z.targets));ns={'p':p,'r':{'configs':{z['fingerprint']:z for z in rd(R/'batch.json')}}};exec(compile(ast.Module(body=[selector],type_ignores=[]),'<pre-reserve representative selection>','exec'),ns);assert ns['rep']['fingerprint']==p['base_parent_fingerprint'] and ns['rep']['scope']=='parent' and (ns['rep']['W'],ns['rep']['K'])==(28,.0275)
archive=rd(R/'registry_archive_plan.json');assert archive['own_finished_IDs']==24 and archive['own_raw_reserve_finish_events']==48
monthly=rd(R/'candidate_completed_fold_audit_plan.json');assert monthly['planned_before_any_reserve'] and monthly['route_from_first_readonly_audit_attempt'] and monthly['current_complete30day_folds']==1 and sha(R/'audit_candidate_30day_recovery.py')==monthly['planned_source_sha256']
for n in R.glob('*.py'):
 assert not n.read_bytes().endswith(b'\n\n'),n
 ast.parse(n.read_text())
put(R/'boundary_unit_verification.json',{'passed':True,'current_daily_event_counts':dc,'actual_funding_counts':fc,'old11sources_kept6each_new12prior0_currentLF6C0':True,'full78_old77_76prefix_originalFloat_marks_verified':True,'source12_actual_funding_before_own_original_daily_decision':True,'representative_parent_selection_exercised':True,'own_IDs':24,'own_events':48,'all_source_EOF_checked_before_binding':True,'before_any_current_reservation':True});print('PASS12firstsources/LFactualfunding6thenoriginaldaily1/C_SMAmarks0/full78/24ID48events')
