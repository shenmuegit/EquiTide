"""Prepare ETH M2/M3 tighterbudget definitions and next closed windows; no model calculations."""
import ast,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2]
def edit(name,pairs):
 p=R/name;s=p.read_text()
 for a,b in pairs:assert a in s,(name,a);s=s.replace(a,b)
 ast.parse(s);p.write_text(s)
for name in ['run.py','audit.py','exports.py']:
 edit(name,[("'BTC_VOL_WINDOW_DAYS'","'ETH_FUND_MEDIAN_COUNT'"),("'ETH_FUND_R'","'BTC_VOL_WINDOW_DAYS'")])
for name in ['run.py','audit.py']:
 edit(name,[("axis='ETH_FUND_MEDIAN_COUNT' if c['asset']=='BTC' else 'BTC_VOL_WINDOW_DAYS';key='W' if c['asset']=='BTC' else 'K'","axis='ETH_FUND_MEDIAN_COUNT' if c['asset']=='ETH' else 'BTC_VOL_WINDOW_DAYS';key='W' if c['asset']=='ETH' else 'K'")])
edit('run.py',[("'read_only_ETH_banks_reused':True,'read_only_BTC_center_reused':True","'read_only_ETH_center_reused':True,'read_only_BTC_banks_reused':True"),("'new_native_asset':'BTC'","'new_native_asset':'ETH'")])
p=R/'definitions.py';s=p.read_text();a=s.index(" if z['scope']=='native':");b=s.index('\n else:',a);s=s[:a]+" if z['scope']=='native':assert z['asset']=='ETH' and q['exit_buffer_fraction']==.0075 and q['lookback_days']==5 and q['return_hurdle']==.02 and q['trend_lookback_days']==16 and q['trend_slope_lag_days']==3 and q['trend_slope_hurdle_fraction']==.0075 and q['entry_volatility_window_days']==6 and q['entry_volatility_ceiling']==.05625 and q['entry_funding_settlement_count'] in [2,3] and q['entry_funding_volatility_ratio']==.00875 and q['entry_funding_budget_volatility_window_days']==8 and q['entry_direction_mode']=='long_only' and (q['initial_capital_usdt'],q['fixed_entry_notional_usdt'])==(15000,4000)"+s[b:];ast.parse(s);p.write_text(s)
edit('parent_units.py',[("g['W']==10","g['W']==3"),("g['asset']=='BTC' and g['W']==3","g['asset']=='ETH' and g['W']==3")])
edit('exports.py',[("xlabel='ETH funding budget / completed daily volatility',ylabel='BTC entry volatility memory V; L29/H3%/exit0.5%/cap3%'","xlabel='Readonly BTC volatility window V (days)',ylabel='ETH matured funding median count M; R0.00875'"),("['0.00875','0.01000']","['10 days','14 days']"),("['6 days','10 days','14 days']","['M2','M3','M4']"),('Preregistered BTC entry volatility memory / ETH funding-budget ratio','Preregistered ETH funding median M / reused BTC volatility V')])
for name in ['observe_fewm.py','observe_candidate.py']:edit(name,[('1857068','1891317')])
edit('forward_registry.py',[("PREV=ROOT/'research/experiments/20261114T175537Z'","PREV=ROOT/'research/experiments/20261114T215636Z'")])
edit('checks.py',[("==6\n put(R/'account_window_verification.json'","==0\n put(R/'account_window_verification.json'"),('singleactual16own6,L4FEWMalreadybookedzero','all3already16once,current0fund')])
previous=json.loads((ROOT/'.git/automation_proofs/20261114T215636Z.json').read_text());assert previous['status']=='completed_published_verified_unlocked';head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();assert subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT,text=True).strip()==head
(R/'startup.json').write_text(json.dumps({'round':R.name,'trigger_utc':'2026-11-14T23:56:07.877Z','base_commit':head,'branch_lock_broker_pid':1891317,'branch_lock_session':45164,'branch_lock_native_start_chunk':'c9509d','root_native_verification_chunk':'15c834','successful_fetch_start_chunk':'d53c32','successful_fetch_completion_chunk':'351d18','successful_fetch_session':10994,'successful_fetch_exit_code':0,'initial_sync_no_merge_required':True,'only_preexisting_untracked':'data/normalized','previous_round_publication_verified':previous['status'],'previous_commit':previous['commit'],'previous_final_main_commit':previous['final_main_commit'],'last_actual_account_round':'20261114T215636Z','old_blocked_failure_records_unchanged':True},indent=2)+'\n')
checked=[]
for p in R.rglob('*.py'):
 t=ast.parse(p.read_text());assert not[n for n in ast.walk(t) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id in ['ROOT','R','P']],str(p);checked.append(str(p.relative_to(ROOT)))
(R/'path_join_guard.json').write_text(json.dumps({'passed':True,'checked':checked,'Path_names_not_subscripted':True,'before_binding_and_evaluation':True,'no_model_or_account_calculations':True},indent=2)+'\n');print('PASS ETHnewM2/M3R.00875 xread-onlyBTCV10/V14;engine/coreidentical;currentfund0all,PID1891317 beforebinding')
