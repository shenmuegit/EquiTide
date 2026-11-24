"""Derive only the next-window calendar from actual saved states; never execute an account."""
import hashlib,json
from pathlib import Path
from datetime import datetime,timedelta,timezone
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
rd=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rel=lambda p:str(p.relative_to(ROOT));parse=lambda s:datetime.fromisoformat(s.replace('Z','+00:00'));stamp=lambda d:d.isoformat().replace('+00:00','Z');put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
binding=rd(R/'next_daily_handoff_binding.json');assert binding['bound_before_execution'] and all(sha(ROOT/p)==h for p,h in binding['source_sha256'].items())
probe=rd(R/'next_daily_boundary_probe.json');assert probe['expected_failure_observed'] and probe['actual_exit_code']==1 and probe['cases'][0]['legacy_matches'] and not probe['cases'][1]['legacy_matches']
first=rd(R/'verification.json')['report_sha256'];assert first==binding['finished_financial_report_sha256']==sha(R/'report.json')
paths=['report.json','forward_report.json','forward_state.json',*[a+'_observation/'+f for a in ['candidate','l4h02','fewm'] for f in ['report.json','state.json','delta.json.gz','complete.json']]];protected={rel(R/p):sha(R/p) for p in paths}
dest=R/'next_research_state.json';before_bytes=dest.read_bytes();state=rd(dest);h=state['UTC_midnight_handoff'];old_calendar=h['next_window_original_daily_events'];aw=rd(R/'account_window_verification.json');windows=rd(R/'account_windows.json');expected={};last_daily={};next_daily={}
for account in ['SMA','candidate','l4h02','fewm']:
 if account=='SMA':
  saved=rd(R/'forward_state.json');start=parse(saved['last_completed_mark_utc']);daily=parse(saved['next_daily_decision_utc'])
 else:
  saved=rd(R/(account+'_observation/state.json'));start=datetime.fromtimestamp(saved['cutoff_ns']//1000000000,timezone.utc);times=aw['full_chain_once_counts'][account]['daily'];latest=max(map(int,times));assert times[str(latest)]==6 and latest%1000000000==0;last_daily[account]=stamp(datetime.fromtimestamp(latest//1000000000,timezone.utc));daily=datetime.fromtimestamp(latest//1000000000,timezone.utc)+timedelta(days=1)
 assert start==parse(windows[account]['cutoff_utc']) and daily==parse(windows[account]['next_daily_decision_utc'])==parse(h['next_daily_decision_by_account'][account])
 next_window=h['next_SMA_single_window_utc'] if account in ['SMA','candidate'] else h['next_L4_FEWM_window_utc'];end=start+timedelta(hours=2);assert [stamp(start),stamp(end)]==next_window
 next_daily[account]=stamp(daily);expected[account]=[]
 while daily<=end:
  if start<daily:expected[account].append(stamp(daily))
  daily+=timedelta(days=1)
assert expected==probe['cases'][1]['derived_from_real_frozen_timestamps'] and expected['SMA']==expected['candidate']==[] and expected['l4h02']==expected['fewm']==['2026-11-24T00:01:00Z']
assert old_calendar!=expected and sha(R/'collect.py')==probe['collector_sha256']
backup=R/'next_research_state_before_midnight_handoff.json';assert not backup.exists();backup.write_bytes(before_bytes)
h['next_window_original_daily_events']=expected;h['next_SMA_single_expected_daily_events_utc']=expected['SMA'];h['next_L4_FEWM_expected_daily_events_utc']=expected['l4h02'];h['next_required_resume_mode_by_account']={a:('mark_only' if not rows else 'original_daily_decision_and_actual_funding_only_if_covered') for a,rows in expected.items()}
h['next_window_funding_action_legacy_superseded']='Next-window daily events are derived separately from actual saved original daily decisions and each own cutoff. SMA/candidate next windows end before Nov24_00:01;L4/FEWM next windows include that original daily event. Funding is independently derived from the fresh complete actual query and own coverage;the readonly first source is not booked early. Refresh and bind exact firstsourceSHA/originalUTC/time/rate/mark and own unique keys before ANY next reserve. Continue each own frozen cash/quantity/desired/costs;no restart or cross-account copy. SMA future Nov24daily still requires full76 completed SPOT background rebinding.'
h['rules']+=';Correct next-window original daily events='+str(expected)+';readonly handoff correction,no current or next account execution.'
state['next_required_effective_daily_handoff_checker']=rel(Path(__file__));state['next_daily_handoff_verification']=rel(R/'next_daily_handoff_verification.json');put(dest,state)
result=R/'result.md';before_result=sha(result);text=result.read_text();text+='\n## 下一窗口午夜边界核对\n\n原汇总模板把下一窗口日决策固定写空；真实冻结边界复现表明，本轮下一L4/FEWM窗口2026-11-23 22:10至Nov24 00:10 UTC包含Nov24 00:01原日决策，SMA/candidate下一20:30至22:30仍无日决策。已按各原账户真实完整决策链和状态推导并更正交接，保留原交接字节及失败复现。资金费仍由新鲜实际time/rate/mark独立判定，首次源SHA/原UTC与本账户唯一键必须在下轮任何reserve前重新绑定；没有提前执行日决策或记账。已完成的财务、NAV、现金、数量、规则、持仓和报告均未改变。\n';result.write_text(text)
assert all(sha(ROOT/p)==h for p,h in protected.items()) and sha(R/'report.json')==first
put(R/'next_daily_handoff_verification.json',{'passed':True,'recorded_utc':datetime.now(timezone.utc).isoformat(),'root_cause':'collect.py writes a constant empty next-window original daily calendar; previous non-midnight case worked, current next L4/FEWM windows cross the saved UTC00:01 schedule.','binding':rel(R/'next_daily_handoff_binding.json'),'before_source':rel(backup),'before_source_sha256':sha(backup),'after_source':rel(dest),'after_source_sha256':sha(dest),'last_actual_daily_utc':last_daily,'next_original_daily_utc':next_daily,'next_own_window_daily_events':expected,'legacy_calendar_before':old_calendar,'monetary_reports_states_ledgers_unchanged':protected,'result_before_sha256':before_result,'result_after_sha256':sha(result),'financial_report_sha256_unchanged':first,'new_strategy_or_account_or_cashflow_executions':0})
print(json.dumps({'passed':True,'next_own_daily_events':expected,'all_actual_reports_and_account_states_unchanged':True,'new_strategy_or_account_executions':0},ensure_ascii=False))
