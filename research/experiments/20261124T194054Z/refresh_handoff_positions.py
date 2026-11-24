"""Refresh only inherited handoff position metadata from each already audited original state."""
import copy,hashlib,json
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
rd=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rel=lambda p:str(p.relative_to(ROOT));put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
binding=rd(R/'handoff_positions_binding.json');assert binding['source_sha256']==sha(Path(__file__)) and binding['bound_after_financial_and_account_execution_before_metadata_correction']
reports={R/'report.json':rd(R/'verification.json')['report_sha256'],R/'forward_report.json':rd(R/'forward_verification.json')['report_sha256'],R/'forward_state.json':binding['SMA_state_sha256']}
states={};positions={};sources={}
for a in ['candidate','l4h02','fewm']:
 check=rd(R/(a+'_verification.json'));assert check['passed'];pointer=ROOT/'research/automation'/f'{a}_forward_latest.json';ptr=rd(pointer);assert ptr['state']==rel(R/(a+'_observation/state.json'))
 for k in ['state','report','delta','complete']:
  f=ROOT/ptr[k];assert sha(f)==ptr[k+'_sha256'];sources[rel(f)]=sha(f)
 state=rd(ROOT/ptr['state']);assert sha(ROOT/ptr['state'])==check['state_sha256'];positions[a]={asset:{k:z['signed_units'] for k,z in books.items()} for asset,books in state['books'].items()};states[a]={'pointer':rel(pointer),'pointer_sha256':sha(pointer),'state':ptr['state'],'state_sha256':ptr['state_sha256']}
assert all(sha(f)==h for f,h in reports.items());target=R/'next_research_state.json';before=rd(target);first=R/'next_research_state_first_collected.json';assert not first.exists();first.write_bytes(target.read_bytes());old=before['UTC_midnight_handoff']['current_original_signed_units_by_asset_cost'];assert old!=positions and old['candidate']['ETH']=={'1':'0','2':'0','3':'0'} and positions['candidate']['ETH']=={'1':'-1.754000000000000000','2':'-1.754000000000000000','3':'-1.754000000000000000'}
after=copy.deepcopy(before);after['UTC_midnight_handoff']['current_original_signed_units_by_asset_cost']=positions
changed=copy.deepcopy(after);changed['UTC_midnight_handoff']['current_original_signed_units_by_asset_cost']=old;assert changed==before
put(target,after);assert rd(target)['UTC_midnight_handoff']['current_original_signed_units_by_asset_cost']==positions and all(sha(ROOT/f)==h for f,h in sources.items()) and all(sha(f)==h for f,h in reports.items())
out={'passed':True,'recorded_utc':datetime.now(timezone.utc).isoformat(),'source_binding':rel(R/'handoff_positions_binding.json'),'root_cause':'collect.py copies previous UTC_midnight_handoff and refreshes event counts/calendars, but does not refresh current_original_signed_units_by_asset_cost after a real original daily position change. Financial/account states and their audits were correct.','reproduced_prior_inherited_metadata_differs_from_each_own_audited_state':True,'first_collected_state':rel(first),'first_collected_state_sha256':sha(first),'effective_next_state':rel(target),'effective_next_state_sha256':sha(target),'only_changed_field':'UTC_midnight_handoff.current_original_signed_units_by_asset_cost','before':old,'after':positions,'each_own_authoritative_sources':states,'all_account_reports_states_deltas_complete_unchanged':sources,'financial_and_SMA_report_SHA_unchanged':{rel(f):h for f,h in reports.items()},'new_financial_account_order_or_cashflow_evaluations':0,'next_round_must_refresh_this_field_from_each_current_audited_state_even_if_previous_field_present':True}
put(R/'handoff_positions_verification.json',out)
text=(R/'result.md').read_text();text+='\n## 交接持仓元数据核验\n\ncandidate原冻结规则在Nov24_00:01令ETH开空，每个成本场景实际保存数量−1.754 ETH。首次汇总继承前轮ETH零持仓字段；首次汇总已原样留档next_research_state_first_collected.json，现仅将current_original_signed_units_by_asset_cost按各自已审计状态刷新。资金费仍按结算时旧数量记账，不能倒用开空后的数量。金融与四账户首次报告、实际状态和账本未改、未重跑。下一轮须从各自当前已审计state刷新交接持仓，不沿用旧元数据。核验见handoff_positions_verification.json。\n';(R/'result.md').write_text(text)
print(json.dumps({'passed':True,'only_changed_field':out['only_changed_field'],'candidate_current_ETH_units':positions['candidate']['ETH'],'all_actual_reports_states_and_ledgers_unchanged':True,'new_financial_or_account_evaluations':0},ensure_ascii=False))
