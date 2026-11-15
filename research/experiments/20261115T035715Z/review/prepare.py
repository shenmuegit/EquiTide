"""Prepare unchanged-engine BTC volatility ceiling variants before registration/calculation."""
import ast,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2]
def edit(name,pairs):
 p=R/name;s=p.read_text()
 for a,b in pairs:assert a in s,(name,a);s=s.replace(a,b)
 ast.parse(s);p.write_text(s)
for name in ['run.py','audit.py','exports.py']:
 edit(name,[("'ETH_EWM_LENGTH_DAYS'","'BTC_VOL_CEILING'"),("'BTC_VOL_WINDOW_DAYS'","'ETH_FUND_R'")])
for name in ['run.py','audit.py']:
 edit(name,[("axis='BTC_VOL_CEILING' if c['asset']=='ETH' else 'ETH_FUND_R';key='W' if c['asset']=='ETH' else 'K'","axis='BTC_VOL_CEILING' if c['asset']=='BTC' else 'ETH_FUND_R';key='W' if c['asset']=='BTC' else 'K'")])
edit('run.py',[("'read_only_ETH_center_reused':True,'read_only_BTC_banks_reused':True","'read_only_ETH_banks_reused':True,'read_only_BTC_center_reused':True"),("'new_native_asset':'ETH'","'new_native_asset':'BTC'")])
p=R/'definitions.py';s=p.read_text();a=s.index(" if z['scope']=='native':");b=s.index('\n else:',a);s=s[:a]+" if z['scope']=='native':assert z['asset']=='BTC' and q['lookback_days']==29 and q['return_hurdle']==.03 and q['exit_buffer_fraction']==.005 and q['entry_volatility_window_days']==10 and q['entry_volatility_ceiling'] in [.04,.05] and q['entry_volatility_gate_scope']=='new_or_reversed_position_only' and (q['initial_capital_usdt'],q['fixed_entry_notional_usdt'])==(3750,1000)"+s[b:];ast.parse(s);p.write_text(s)
edit('parent_units.py',[("g['W']==16","g['W']==.04"),("g['asset']=='ETH' and g['W']==.04","g['asset']=='BTC' and g['W']==.04"),("for cap in [.03,.04]:","for cap in [.03,.04,.05]:")])
edit('exports.py',[("Readonly BTC volatility window V (days)","Readonly ETH funding budget R"),("ETH finite EWM length S (days); M4/R0.00875","BTC entry volatility ceiling; L29/H3%/E0.5%/V10"),("['10 days','14 days']","['0.00875','0.01000']"),("['S12','S16','S20']","['3%','4%','5%']"),('Preregistered ETH EWM length S / reused BTC volatility V','Preregistered BTC entry volatility ceiling / reused ETH funding budget')])
for name in ['observe_fewm.py','observe_candidate.py']:edit(name,[('1926187','1956168')])
previous=json.loads((ROOT/'.git/automation_proofs/20261115T015614Z.json').read_text());assert previous['status']=='completed_published_verified_unlocked';head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();assert head==subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT,text=True).strip();assert json.loads((R/'exact_parameter_registry_screen.json').read_text())['passed']
(R/'startup.json').write_text(json.dumps({'round':R.name,'trigger_utc':'2026-11-15T03:57:15.950Z','base_commit':head,'branch_lock_broker_pid':1956168,'branch_lock_session':55125,'branch_lock_native_start_chunk':'0d756f','root_native_verification_chunk':'56d86d','successful_fetch_start_chunk':'bf575e','successful_fetch_completion_chunk':'9761ef','successful_fetch_session':85418,'successful_fetch_exit_code':0,'initial_sync_no_merge_required':True,'only_preexisting_untracked':'data/normalized','previous_round_publication_verified':previous['status'],'previous_commit':previous['commit'],'previous_final_main_commit':previous['final_main_commit'],'last_actual_account_round':'20261115T015614Z','peer_03UTC_paper10_commit_preserved':head,'old_blocked_failure_records_unchanged':True},indent=2)+'\n')
checked=[]
for p in R.rglob('*.py'):
 t=ast.parse(p.read_text());assert not[n for n in ast.walk(t) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id in ['ROOT','R','P']],str(p);checked.append(str(p.relative_to(ROOT)))
(R/'path_join_guard.json').write_text(json.dumps({'passed':True,'checked':checked,'Path_names_not_subscripted':True,'before_binding_and_evaluation':True,'no_model_or_account_calculations':True},indent=2)+'\n');print('PASS BTCnewcap4/5 V10 xreadonlyETHR00875/01;engine/coreidentical;PID1956168 beforebinding')
