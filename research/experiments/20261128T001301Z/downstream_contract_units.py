"""Exercise actual readonly renderer/count assertions against preregistered window metadata."""
import ast,gzip,json,re
from pathlib import Path
from common import ROOT,R,put,sha,rel,now
rd=lambda p:json.loads(p.read_text());w=rd(R/'account_windows.json');accounts=['SMA','candidate','l4h02','fewm'];fc={a:w[a]['expected_funding_records'] for a in accounts};dc={a:len(w[a]['expected_daily_events_utc']) for a in accounts};assert fc==dc==dict.fromkeys(accounts,0)
# Evaluate the actual f-string used by the report at the transport-retention boundary.
tree=ast.parse((R/'collect.py').read_text());nodes=[n for n in ast.walk(tree) if isinstance(n,ast.JoinedStr) and any(isinstance(v,ast.Constant) and isinstance(v.value,str) and '公共GET失败' in v.value for v in n.values)];assert len(nodes)==1
rendered=eval(compile(ast.Expression(nodes[0]),'<actual_report_transport_phrase>','eval'),{'nonzero':[],'facts':[]});assert len(re.findall(r'公共GET失败\d+条',rendered))==1 and '初步' not in rendered
# Test the actual preplanned current-window handoff-count assertion; all historical counts are real previous-chain counts.
prior=rd(ROOT/'research/experiments/20261127T221229Z/account_window_verification.json');aw={'accounts':{a:{'new_daily_events':dc[a]} for a in accounts},'current_funding_records_by_account':fc,'actualNov26_00_unique_counts':prior['actualNov26_00_unique_counts'],'actualNov26_00_daily_once_counts':prior['actualNov26_00_daily_once_counts']}
t=ast.parse((R/'handoff_contract.py').read_text());node=next(n for n in t.body if isinstance(n,ast.Assert) and 'current_funding_records_by_account' in ast.unparse(n));assert eval(compile(ast.Expression(node.test),'<actual_handoff_window_contract>','eval'),{'aw':aw})
nextcheck=(R/'verify_next_funding_handoff.py').read_text();assert "aw['current_funding_records_by_account']=={a:rd(R/'account_windows.json')[a]['expected_funding_records'] for a in ['SMA','candidate','l4h02','fewm']}" in nextcheck
assert "len(r['configs'])==4" in (R/'saved_review.py').read_text() and "len(r['configs'])==12" not in (R/'saved_review.py').read_text()
# Read actual previous nested daily/minute input and Float state. No new account step is called.
P=ROOT/'research/experiments/20261127T221229Z';rep=rd(P/'forward_report.json');state=rd(P/'forward_state.json');raw=json.loads(gzip.decompress((ROOT/rep['source_inputs_path']).read_bytes()));assert state['source_report_sha256']==sha(P/'forward_report.json')
for a in ['BTC','ETH']:
 minute=raw[a]['1m'] if isinstance(raw[a],dict) else raw[a];assert isinstance(minute,list) and len(minute)==121
 full=json.loads(gzip.decompress((ROOT/'research/experiments/20261127T201157Z/sma65_prebinding_inputs.json.gz').read_bytes()));assert len(full[a]['1d'])==79
 cfg=rep['configs']['forward_snapshot_'+a];assert 'decision' in cfg and 'latest_daily_decision' in cfg
 for k,s in cfg['scenes'].items():
  pos=state['positions_by_asset_and_cost'][a][k];assert s['equity_usdt'][-1]==pos['cash_usdt']+pos['units']*float(minute[-1][4]) and s['terminal_action']=='mark only;no forced exit'
put(R/'downstream_contract_verification.json',{'passed':True,'recorded_utc':now(),'actual_renderer_fstring_checked':True,'transport_expected_pattern_matches_once':True,'actual_current_count_assertion_checked':True,'current_funding_counts':fc,'current_daily_counts':dc,'source12_prior_booked_all_accounts_once':True,'actual_previous_SMA_minute_array_full79_background_and_Float_balances_checked':True,'summary_count4_matches_frozen_batch':len(rd(R/'batch.json'))==4,'normal_success_only_gates':True,'before_any_reserve':True,'new_strategy_or_account_or_cashflow_evaluations':0});print('PASS actual renderer/transport regex, current-count handoff, four-config summary, and previous minute-array/full79 Float input contract;0modelcalls')
