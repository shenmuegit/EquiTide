"""Resume only saved-evidence rendering; preserve failed GETs and block future incomplete queries."""
import ast,gzip,hashlib,json
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
rd=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
b=rd(R/'blocked_collection_binding.json');assert sha(Path(__file__))==b['source_sha256'];assert sha(R/'collect.py')==b['original_collector_sha256'];assert sha(R/'collect_blocked_adapted.py.txt')==b['adapted_sha256']
for p,h in b['immutable_inputs_sha256'].items():assert sha(ROOT/p)==h,p
allowed={'collect','funding_retry','funding_extended_retry'};actual={p.stem for p in (R/'command_receipts').glob('*.json') if not rd(p)['passed']};assert actual==allowed
original=rd(R/'next_window_transport_attempts.json');btc=next(x for x in original if x['asset']=='BTC' and x['http_status']==200 and not x['curl_exit_code']);btc_rows=json.loads(gzip.decompress((ROOT/btc['raw']).read_bytes()));lo,hi=b['query_window_ms'];known_eth=[]
for e in rd(ROOT/'research/experiments/20261127T080551Z/next_research_state.json')['UTC_midnight_handoff']['next_window_known_actual_funding_sources']:
 assert sha(ROOT/e['path'])==e['sha256']
 known_eth += [z for z in e['actual_public_fields']['ETH'] if lo<int(z['fundingTime'])<=hi]
assert len({z['fundingTime'] for z in known_eth})==len(known_eth);payload={'BTC':btc_rows,'ETH':sorted(known_eth,key=lambda z:z['fundingTime'])};assert all(lo<int(z['fundingTime'])<=hi for xs in payload.values() for z in xs)
attempts=original+rd(R/'next_funding_recovery_transport_attempts.json')+rd(R/'next_funding_extended_recovery_transport_attempts.json');assert sum(x['http_status']==0 and x['curl_exit_code']==35 for x in attempts)==7
unknown={'SMA':0,'candidate':None,'l4h02':None,'fewm':None}
def guarded_put(p,x):
 rel=str(p.relative_to(ROOT))
 if rel in b['immutable_inputs_sha256']:
  assert p.exists() and json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n'==p.read_text(),rel
  return
 if p.name=='next_window_funding_lookup.json':
  x.update(passed=False,query_status='blocked_ETH_TLS_transport',complete_actual_query=False,ETH_rows_origin='known_original_first_settlement_documents_only_not_a_new_successful_HTTP_response',BTC_complete_HTTP200=True,ETH_complete_HTTP200=False,known_source_coverage_counts=x['own_next_window_pending_counts'],own_next_window_pending_counts=unknown,additional_ETH_events_in_unqueried_interval_unknown=True,next_reserve_blocked_until_complete_fresh_query=True,all_seven_failed_GETs_preserved=True)
 if p.name=='next_research_state.json':
  h=x['UTC_midnight_handoff'];known=h['next_new_actual_funding_pending_by_own_window'];h['known_source_only_coverage_counts']=known;h['next_new_actual_funding_pending_by_own_window']=unknown;h['next_required_resume_mode_by_account']={a:'blocked_until_complete_actual_funding_query_before_reserve' for a in unknown};h['next_funding_first_source_by_own_window']['known_source_only_coverage_counts']=known;h['next_funding_first_source_by_own_window']['pending_records_by_account']=unknown;h['next_funding_first_source_by_own_window']['complete_actual_query']=False;h['next_actual_funding_prebinding_contract']='Before ANY next reserve, obtain and bind complete successful BTC and ETH funding responses across every own next window. Current ETH next-window query is blocked by seven TLS35 failures. Saved known-source coverage is a lower bound only;do not infer absence of other events or simulate future cashflows.';h['rules']+=' Future ETH query incomplete;all next reserves blocked until refreshed.';x.update(next_funding_query_status='blocked_ETH_TLS_transport',next_reserve_requires_complete_actual_funding_query=True,known_source_only_coverage_counts=known)
 put(p,x)
ns={'__name__':'readonly_blocked_collection','__file__':str(R/'collect.py'),'readonly_put':guarded_put,'RECOVERY_KNOWN_PAYLOAD':payload,'RECOVERY_ACTUAL_ATTEMPTS':attempts,'RECOVERY_ALLOWED_FAILURES':allowed};code=(R/'collect_blocked_adapted.py.txt').read_text();tree=ast.parse(code)
assert not any(isinstance(n,ast.Call) and (isinstance(n.func,ast.Name) and n.func.id in {'call','evaluate','simulate','reserve','finish'} or isinstance(n.func,ast.Attribute) and n.func.attr in {'simulate','evaluate','reserve','finish','run','Popen'}) for n in ast.walk(tree))
exec(compile(tree,'<bound saved-evidence collector;future query explicitly blocked>','exec'),ns)
state=rd(R/'next_research_state.json');assert state['next_funding_query_status']=='blocked_ETH_TLS_transport' and state['next_reserve_requires_complete_actual_funding_query'];assert state['UTC_midnight_handoff']['next_new_actual_funding_pending_by_own_window']==unknown
p=R/'result.md';text=p.read_text();literal=str(ns['nextfund']);text=text.replace('下一真实待处理资金费'+literal,'下轮完整资金费查询受阻；仅已知来源覆盖'+literal+'（并非完整待处理计数，其他ETH事件未知）');text+='\n只读汇总恢复：原collect与两次有限恢复均有真实失败回执，七次ETH TLS35失败未收到HTTP响应；原BTC成功响应保留。为保存本轮已完成结果，只重做账本读取核对与文字/JSON汇总，没有重放模型或任何已完成账户窗口。下轮ETH查询不完整；已知来源覆盖仅为下界，所有下轮reserve前必须取得完整新查询，不能据此计算未来现金流或宣称没有其他结算。原冻结报告、状态、账本、指针和登记原字节均保持。详见blocked_collection_verification.json。\n';p.write_text(text)
for p,h in b['immutable_inputs_sha256'].items():assert sha(ROOT/p)==h,p
put(R/'blocked_collection_verification.json',{'passed':True,'recorded_utc':datetime.now(timezone.utc).isoformat(),'scope':'integrity_of_completed_current_results_and_explicitly_blocked_next_query','source_sha256':b['source_sha256'],'original_failed_phases_preserved':sorted(allowed),'original_failed_phase_receipt_sha256':{a:sha(R/'command_receipts'/(a+'.json')) for a in allowed},'financial_report_sha256_unchanged':sha(R/'report.json'),'SMA_report_sha256_unchanged':sha(R/'forward_report.json'),'every_current_book_state_delta_report_pointer_and_registry_unchanged':True,'financial_or_account_window_replays':0,'next_query_complete':False,'all_next_reserves_blocked_until_complete_fresh_funding_query':True,'known_source_only_coverage_counts':ns['nextfund'],'actual_failed_ETH_GETs':7});print('PASS saved current-evidence rendering only;next ETH query remains BLOCKED,seven failures preserved',flush=True)
