"""Read-only reconciliation of actual Nov21_16 own-ledger booking and next pending split."""
from decimal import Decimal as D,localcontext
from common import *
rd=lambda p:json.loads(p.read_text());pre=rd(R/'actual16_nov21_prebinding_source.json');doc=rd(ROOT/pre['source']);aw=rd(R/'account_window_verification.json');prep=rd(R/'next_midnight_preparation.json');ns=rd(R/'next_research_state.json');h=ns['UTC_midnight_handoff'];rh=sha(R/'report.json');accounts=['candidate','l4h02','fewm'];times={str(int(z['fundingTime'])*1000000) for xs in doc['public_fields_by_asset'].values() for z in xs}
assert pre['passed'] and aw['passed'] and sha(ROOT/pre['source'])==pre['sha256']=='47c8cd048c477ef0a860dba45e5298f3402141f0f3f353364835826b8d4ecc96' and doc['recorded_utc']=='2026-11-22T05:30:01.859371Z' and times=={'1795276800000000000'}
counts={a:{t:aw['full_chain_once_counts'][a]['funding'].get(t,0) for t in times} for a in accounts};assert counts==pre['expected_current_full_chain_counts'] and {a:sum(row.values()) for a,row in counts.items()}=={'candidate':6,'l4h02':6,'fewm':6}
flows=[z for z in aw['actual_new_settlement_own_cashflows'] if str(z['actual_settlement_ns']) in times];assert {a:sum(z['account']==a for z in flows) for a in accounts}=={'candidate':0,'l4h02':0,'fewm':0};ownproof=[]
for stem in accounts:
 before=rd(ROOT/rd(R/(stem+'_observation/previous_pointer.json'))['state']);after=rd(R/(stem+'_observation/state.json'));v=rd(R/(stem+'_verification.json'));assert v['passed'] and v['new_fills']==0 and v['new_funding_settlements']==0
 for asset,bs in before['books'].items():
  source=doc['public_fields_by_asset'][asset][0]
  for k,b in bs.items():
   assert D(b['signed_units'])==({'candidate':D('-.012'),'l4h02':D('-.006'),'fewm':D('-.009')}[stem] if asset=='BTC' else 0)
   selected=[z for z in flows if z['account']==stem and z['asset']==asset and str(z['cost'])==str(k)];assert len(selected)==0
   with localcontext() as ctx:
    ctx.prec=28
    raw=-D(b['signed_units'])*D(source['markPrice'])*D(source['fundingRate']);expected=raw*D(k) if raw<0 else raw
    amount=D(selected[0]['own_amount_usdt']) if selected else D(0)
    if selected:
     assert amount==expected and D(selected[0]['held_units'])==D(b['signed_units']) and selected[0]['first_actual_current_settlement_public_capture_UTC']==doc['recorded_utc']
    assert D(after['books'][asset][k]['cash'])==D(b['cash'])+amount
   assert all(after['books'][asset][k][key]==value for key,value in b.items() if key!='cash')
   ownproof.append({'account':stem,'asset':asset,'cost':k,'held_units':b['signed_units'],'actual_current_amount_usdt':str(amount),'cash_before':b['cash'],'cash_after':after['books'][asset][k]['cash'],'source_mark':source['markPrice'],'source_rate':source['fundingRate'],'income_unamplified_outflow_stressed':True,'all_non_cash_state_unchanged':True})
ms=lambda s:int(datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()*1000)
pending={a:0 if a=='SMA' else 3*sum(ms(win[0])<int(z['fundingTime'])<=ms(win[1]) for xs in doc['public_fields_by_asset'].values() for z in xs) for a,win in prep['next_original_windows'].items()};assert pending=={'SMA':0,'candidate':0,'l4h02':0,'fewm':0}
h.update(actual_Nov21_16_source=pre['source'],actual_Nov21_16_source_sha256=pre['sha256'],original_Nov21_16_capture_utc=pre['first_capture_utc'],known_actual_Nov21_16_public_fields=doc['public_fields_by_asset'],actual_Nov21_16_counts_by_account=counts,L4_FEWM_actualNov21_16_booked_once=True,single_actualNov21_16_not_yet_booked=False,all3_perp_actualNov21_16_booked_once=True,actual_Nov21_16_pending_by_next_window=pending)
h['next_window_funding_action']='All three original perps previously booked actualNov21_16:00:00.000 exactly once; no current repeat. Next candidate18:30-20:30 and L4/FEWM20:10-22:10 exclude known16. Refresh complete actual publicGET, dedup each own window and reserve before any next account calculation. Preserve original q/cash/desired/costs and firstUTC/bytes. Next original dailyNov22_00:01; full73SPOT readonly.'
ns['UTC_midnight_handoff']=h;ns['next_preparation_contract'].update(actual_Nov21_16_counts_by_account=counts,actual_Nov21_16_source={'path':pre['source'],'sha256':pre['sha256'],'first_capture_utc':pre['first_capture_utc']},known_actual16_pending_by_next_window=pending);put(R/'next_research_state.json',ns)
put(R/'actual16_nov21_reconciliation.json',{'passed':True,'verified_utc':now(),'source':pre['source'],'source_sha256':pre['sha256'],'original_first_capture_utc':pre['first_capture_utc'],'current_unique_counts':counts,'current_funding_records_by_account':aw['current_funding_records_by_account'],'independent_own_book_cashflows':flows,'own_books_reconciliation':ownproof,'known16_pending_by_next_window':pending,'all3_booked_once_candidate_now_completed_L4_FEWM_not_repeated':True,'all_previous_known_settlements_not_repeated':True,'financial_report_sha256_unchanged':rh,'no_strategy_or_account_window_reexecution':True})
with (R/'result.md').open('a') as f:f.write('\n实际Nov21_16:00:00.000此前三永续均已按各自q/rate/mark/成本记账一次，全链唯一计数各6，本轮各新增0；十八个原账本不重置、不重复记资金费。首次来源UTC及SHA保持。下一SMA/candidate18:30→20:30、L4/FEWM20:10→22:10仍排除已知16结算；须刷新实际来源、按各自窗口去重并先reserve，不提前入账。\n')
assert sha(R/'report.json')==rh
print(json.dumps({'passed':True,'current_counts':counts,'current_rows':len(flows),'next_pending':pending,'own_books_checked':len(ownproof),'no_model_or_account_rerun':True}))
