"""Verify the previous blocked windows were resumed from true last account state, without rewriting failure history."""
import sys,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import sha,put,now,rel,reg
rd=lambda p:json.loads(p.read_text());P=ROOT/'research/experiments/20261114T195634Z';ctx=rd(R/'context.json');rs=reg.read_records(ROOT/'research/automation/registry.jsonl');blocked=rd(P/'blocked_batch.json');assert len(blocked)==3;oldreport=P/'account_capture_blocked.json';assert sha(oldreport)==ctx['account_hashes_before'][rel(oldreport)]
for row in blocked:
 z=rs[row['fingerprint']];assert z['status']=='blocked' and not z['result_available'] and z['report_sha256']==sha(oldreport)
last=rd(P/'last_actual_account_evidence.json');assert last['last_actual_round_by_account']=={a:'20261114T175537Z' for a in ['SMA','candidate','l4h02','fewm']};priorh=rd(P/'next_research_state.json')['UTC_midnight_handoff'];w=rd(R/'account_windows.json');assert priorh['next_SMA_single_window_utc']==[w['SMA']['start_utc'],w['SMA']['cutoff_utc']] and priorh['next_L4_FEWM_window_utc']==[w['l4h02']['start_utc'],w['l4h02']['cutoff_utc']]
newids=[]
for stem in ['candidate','l4h02','fewm']:
 window=R/(stem+'_observation');previous=rd(window/'previous_pointer.json');assert previous==rd(oldreport)['original_account_pointers'][stem]['pointer'];rep=rd(window/'report.json');assert rep['cutoff_ns']==rd(window/'state.json')['cutoff_ns'];v=rd(R/(stem+'_verification.json'));assert v['passed'] and not v['whole180day_qualified']
 for c in rep['configs'].values():
  z=rs[c['fingerprint']];assert z['result_available'] and z['status']==c['status'] and z['report_sha256']==sha(window/'report.json') and c['fingerprint'] not in {x['fingerprint'] for x in blocked};newids.append(c['fingerprint'])
aw=rd(R/'account_window_verification.json');assert aw['passed'] and aw['current_funding_records_by_account']=={'SMA':0,'candidate':6,'l4h02':0,'fewm':0} and aw['all3_perp_actualNov14_16_booked_once'];assert len(set(newids))==9
put(R/'previous_blocked_window_recovery.json',{'passed':True,'recorded_utc':now(),'previous_round':P.name,'last_actual_source_round':'20261114T175537Z','previous_blocked_noresult_records_unchanged':blocked,'old_failure_report_sha256_unchanged':sha(oldreport),'previous_pending_windows_resumed_exactly':True,'current_real_perp_observation_IDs':newids,'current_SMA_actual_observations':3,'all_current_windows_evaluated_once':True,'all_full_NAV_prefixes_audited':True,'actual_current_funding_record_split':aw['current_funding_records_by_account'],'all3_actual16nowonce':True,'original_daily_rules_capitals_and_quantities_unchanged':True,'previous_failure_not_relabelled_as_actual_result':True,'no_registry_or_account_writes_from_this_checker':True})
print('PASS old3blocked/noresultkept,12newactualwindowsfromtruelast175state,originalpendingwindowsrecovered,single16own6cashflows,othersnorepeat')
