"""Read-only reconciliation of actual Nov19 new settlement and next handoff."""
import collections,gzip,json
from decimal import Decimal as D
from common import ROOT,R,sha,rel,put,now
rd=lambda p:json.loads(p.read_text())
def main():
 source=R/'funding16_nov19_preflight.json';pre=rd(R/'actual16_nov19_prebinding_source.json');src=rd(source);aw=rd(R/'account_window_verification.json');w=rd(R/'account_windows.json');ns=rd(R/'next_research_state.json');h=ns['UTC_midnight_handoff'];expected=collections.Counter()
 assert pre['passed'] and pre['before_any_current_reservation'] and sha(source)==pre['sha256'] and src['recorded_utc']==pre['first_capture_utc']
 lookup={}
 for asset,rows in src['public_fields_by_asset'].items():
  for z in rows:
   timestamp=int(z['fundingTime'])*1000000;expected[str(timestamp)]+=3;lookup[asset,timestamp]=z
 assert expected and aw['passed']
 previous_h=rd(ROOT/'research/experiments/20261120T043737Z/next_research_state.json')['UTC_midnight_handoff'];first_path=previous_h.get('original_Nov19_16_authoritative_source_path',rel(source));assert sha(ROOT/first_path)==sha(source)
 flows=[];books={}
 for stem in ['l4h02','fewm']:
  folder=R/(stem+'_observation');before=rd(ROOT/rd(folder/'previous_pointer.json')['state']);after=rd(folder/'state.json');delta=json.loads(gzip.decompress((folder/'delta.json.gz').read_bytes()));journal=[z for z in delta['journal'] if z['kind']=='funding'];assert len(journal)==w[stem]['expected_funding_records']
  seen=set()
  for z in journal:
   key=z['asset'],z['timestamp_ns'];assert key in lookup;row=lookup[key];k=str(z['cost_multiplier']);unique=(z['asset'],k,z['timestamp_ns']);assert unique not in seen;seen.add(unique);q=D(z['signed_units']);assert q==D(before['books'][z['asset']][k]['signed_units']);base=-q*D(row['markPrice'])*D(row['fundingRate']);amount=base*int(k) if base<0 else base
   assert D(z['base_amount_usdt'])==base and D(z['amount_usdt'])==amount
   flows.append({'account':stem,'asset':z['asset'],'cost':k,'actual_settlement_ns':z['timestamp_ns'],'own_held_units':str(q),'own_amount_usdt':str(amount),'cash_before':z['cash_before'],'cash_after':z['cash_after'],'original_first_capture_utc':src['recorded_utc']})
  assert len(seen)==3*len(lookup)
  for timestamp,count in expected.items():assert aw['full_chain_once_counts'][stem]['funding'][timestamp]==count
  books[stem]={'state_sha256':sha(folder/'state.json'),'own_journal_funding_rows':len(journal),'asset_cost_timestamp_keys_unique':True,'booked_actual_event_once':True}
 candidate_counts={timestamp:aw['full_chain_once_counts']['candidate']['funding'].get(timestamp,0) for timestamp in expected};pending={timestamp:expected[timestamp]-count for timestamp,count in candidate_counts.items()};assert all(v>=0 for v in pending.values())
 h.update(actual_Nov19_16_source=rel(source),actual_Nov19_16_source_sha256=sha(source),original_Nov19_16_authoritative_source_path=first_path,original_Nov19_16_capture_utc=src['recorded_utc'],known_actual_Nov19_16_public_fields=src['public_fields_by_asset'],actual_Nov19_16_settlement_ns=sorted(expected),L4_FEWM_actualNov19_16_booked_once=True,single_actualNov19_16_not_yet_booked=any(pending.values()),all3_perp_actualNov19_16_booked_once=not any(pending.values()),candidate_actualNov19_16_current_once_counts=candidate_counts,candidate_actualNov19_16_pending_counts=pending)
 assert h['next_SMA_single_window_utc']==['2026-11-19T14:30:00Z','2026-11-19T16:30:00Z'] and h['next_L4_FEWM_window_utc']==['2026-11-19T16:10:00Z','2026-11-19T18:10:00Z']
 next_action={'actual_known_pending_event_ns':sorted(timestamp for timestamp,count in pending.items() if count),'first_source':rel(source),'first_source_sha256':sha(source),'original_first_source_UTC':src['recorded_utc'],'reuse_exact_original_fields_not_nominal_time':True,'candidate_use_own_inherited_BTC_minus0p012_ETH0_and_cost_rule_not_other_accounts_amounts':True,'fresh_full_window_actual_query_before_any_next_reserve':True,'no_prebooking_now':True,'L4_FEWM_already_booked_this_event_do_not_repeat':True}
 h['next_SMA_single_preparation_action']['candidate_actualNov19_16_preparation']=next_action;h['next_L4_FEWM_preparation_action']['already_booked_actualNov19_16_do_not_repeat']=True;h['next_nominal_boundary_handoff']={'nominal_boundary_utc':'2026-11-19T16:00:00Z','applies_to':['candidate'],'SMA_SPOT_no_perpetual_funding':True,**next_action};h['next_window_funding_action']='Current L4/FEWM booked the actual newNov19 event once using own inherited quantities. Candidate currentwindow ends14:30 before actual16event; next14:30-16:30 must use original first fields/UTC and own account quantities after a fresh complete lookup. L4/FEWM next16:10-18:10 must not repeat. No nominal timestamp replacement or copied cashflows.'
 h['rules'] += ' 本轮新增Nov19实际结算首次来源UTC='+src['recorded_utc']+'，精确fundingTime原毫秒字段保留。L4/FEWM各自按原持仓和成本记账一次；candidate尚未到该事件，留待下一窗口，不提前记账或复制其他账户现金流。'
 put(R/'funding16_nov19_reconciliation.json',{'passed':True,'recorded_utc':now(),'source':rel(source),'source_sha256':sha(source),'original_authoritative_source_path':first_path,'original_first_capture_utc':src['recorded_utc'],'actual_fields':src['public_fields_by_asset'],'pre_reservation_binding':pre,'expected_once_counts_per_account':dict(expected),'current_funding_records_by_account':aw['current_funding_records_by_account'],'actual_own_cashflows':flows,'current_own_books':books,'candidate_current_once_counts':candidate_counts,'candidate_pending_counts_next_window':pending,'all3_perps_now_booked_once':not any(pending.values()),'source_first_time_never_relabeled':True,'no_financial_or_account_reexecution':True})
 ns['UTC_midnight_handoff']=h;ns['next_saved_bank_graph_proposals']={'inventory_7x7_remaining_preexisting_unexecuted_graphs_after_this_batch':0,'basis':'Four previously recorded remaining graphs are all in current preregistered batch; full economic dedup audit and all actual results retained. Further different parameters or genuine raw weights require new complete specs, cost meaning, dedup and reserve.','no_next_candidate_selected_by_current_OOS_maximum':True};put(R/'next_research_state.json',ns)
 with (R/'result.md').open('a') as f:f.write('\n本轮金额轴为BTC1000/1375/1750、ETH3500/3625/3875/4000，ETH步长125/250/125 USDT；邻域采用格点索引。启发式Sharpe跳变保留为诊断，passed仅表示冻结的历史门槛通过。原固定5000及1000/4000顶层旧金额元数据已从本轮plan去除，每配置实际金额与源银行SHA为准。\n\nNov19实际新增资金费首次公共捕获UTC='+src['recorded_utc']+'，来源SHA256='+sha(source)+'。各账户实际新增资金费行='+json.dumps(aw['current_funding_records_by_account'],ensure_ascii=False)+'，逐笔自己持仓现金流='+json.dumps(flows,ensure_ascii=False)+'。L4/FEWM已各记一次，candidate本轮14:30截止，下一窗口才处理已知实际16事件，必须保留本次首来源UTC和精确毫秒字段并先完整查询。下一L4/FEWM16:10→18:10不得重复；下一SMA/candidate14:30→16:30，下一原日决策Nov20 00:01。\n')
 print(json.dumps({'new_actual_Nov19_settlement_reconciled':True,'funding_split':aw['current_funding_records_by_account'],'candidate_pending':pending,'no_reexecution':True}),flush=True)
