"""Verify saved complete evidence after actual outer143; never advance or replay accounts."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));from common import sha,put,now
rd=lambda p:json.loads(p.read_text());fact=rd(R/'outer_accounts_terminal_143.json');assert fact['actual_exit_code']==143 and fact['do_not_claim_outer_terminal_zero'];rows=rd(ROOT/'.git/automation_proofs/20261109T190751Z_accounts_pipeline.json');assert len(rows)==5 and all(x['actual_exit_code']==0 for x in rows)
for n,h in fact['saved_phase_receipt_sha256'].items():assert sha(R/n)==h
for phase in ['l4h02','fewm','candidate','forward','observer_status','review']:
 assert all(x['exit_code']==0 for x in rd(R/(phase+'_commands.json')))
for name in ['forward_verification.json','candidate_verification.json','l4h02_verification.json','fewm_verification.json','source_verification.json','registry_fragment_layout.json']:assert rd(R/name)['passed']
b=rd(R/'code_binding_before_evaluation.json');assert all(sha(ROOT/p)==h for p,h in {**b['source_sha256'],**b['immutable_source_sha256']}.items());source=rd(R/'source_verification.json');layout=rd(R/'registry_fragment_layout.json');assert source['new_finished_IDs']==24 and source['registry_append_only_events']==layout['current_round_events']==48 and layout['logical_records_and_all_event_contents_equal_before_after'] and layout['current_round_finished_IDs']==24
for stem in ['candidate','l4h02','fewm']:
 v=rd(R/(stem+'_verification.json'))
 for name in ['report','state']:assert sha(R/(stem+'_observation')/(name+'.json'))==v[name+'_sha256']
 assert v['new_daily_events']==v['new_exact_causal_decisions']==v['new_fills']==v['new_rejected_orders']==v['new_risk_proxy_violations']==0
assert rd(R/'candidate_verification.json')['new_funding_settlements']==6 and rd(R/'l4h02_verification.json')['new_funding_settlements']==rd(R/'fewm_verification.json')['new_funding_settlements']==0
put(R/'outer_terminal_integrity_verification.json',{'passed':True,'verified_utc':now(),'actual_outer_terminal_exit_code_retained':143,'native_tool_chunk':'84e661','actual_individual_phase_codes':fact['individual_phase_exit_codes'],'same_original_phase_receipt_sha256':fact['saved_phase_receipt_sha256'],'same_saved_independent_account_audits':True,'all_bound_sources_exact':True,'new_finished_IDs':24,'append_only_events_preserved':48,'financial_and_account_reruns':0,'termination_cause':'Unknown;notrelabelledaszero. Completesavedresultsindependentlyverified;privatepipelineexit143preserved.','resolution':'All5individualphasesalreadyexited0,all4ownaccountauditfiles/complete48eventjournal/sameimmutablecheck_sourcesnativelyverified0. Proceedwithsavedcompleteevidencewithoutrepeatingobservations.'})
print('PASS completed5phase0/4originalaccounts/24finishedIDs/48events/allboundhashes;outer143retained,0accountreplay')
