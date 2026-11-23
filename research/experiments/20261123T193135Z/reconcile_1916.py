"""Readonly older-event once proof; current event cashflows remain separately scoped."""
import json
from common import ROOT,R,sha,rel,put,now
rd=lambda p:json.loads(p.read_text())
def main():
 P=ROOT/'research/experiments/20261123T173139Z';source=R/'funding16_nov19_preflight.json';pre=rd(R/'actual16_nov19_prebinding_source.json');src=rd(source);aw=rd(R/'account_window_verification.json');ns=rd(R/'next_research_state.json');h=ns['UTC_midnight_handoff'];old=rd(P/'next_research_state.json')['UTC_midnight_handoff'];first=old['original_Nov19_16_authoritative_source_path'];assert sha(ROOT/first)==sha(source)==pre['sha256'] and src['recorded_utc']==pre['first_capture_utc'];times=sorted({str(int(z['fundingTime'])*1000000) for xs in src['public_fields_by_asset'].values() for z in xs})
 for account in ['candidate','l4h02','fewm']:
  assert all(aw['full_chain_once_counts'][account]['funding'].get(t,0)==6 for t in times);assert not [z for z in aw['actual_new_settlement_own_cashflows'] if z['account']==account and str(z['actual_settlement_ns']) in times]
 h.update(actual_Nov19_16_source=rel(source),actual_Nov19_16_source_sha256=sha(source),original_Nov19_16_authoritative_source_path=first,original_Nov19_16_capture_utc=src['recorded_utc'],known_actual_Nov19_16_public_fields=src['public_fields_by_asset'],actual_Nov19_16_settlement_ns=times,L4_FEWM_actualNov19_16_booked_once=True,single_actualNov19_16_not_yet_booked=False,all3_perp_actualNov19_16_booked_once=True);ns['UTC_midnight_handoff']=h;put(R/'next_research_state.json',ns)
 put(R/'funding16_nov19_reconciliation.json',{'passed':True,'recorded_utc':now(),'source':rel(source),'source_sha256':sha(source),'original_authoritative_source_path':first,'original_first_capture_utc':src['recorded_utc'],'actual_fields':src['public_fields_by_asset'],'pre_reservation_binding':pre,'current_funding_records_by_account':aw['current_funding_records_by_account'],'old_event_current_cashflows':[],'all3_perps_now_booked_once':True,'source_first_time_never_relabeled':True,'no_financial_or_account_reexecution':True});print('PASSoldNov19_16once/notrepeated,currentNov20cashflowsseparate')
if __name__=='__main__':main()
