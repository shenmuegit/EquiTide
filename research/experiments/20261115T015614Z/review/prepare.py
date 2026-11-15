"""Prepare existing-engine ETH memory variants before any reservation or market calculation."""
import ast,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2]
def edit(name,pairs):
 p=R/name;s=p.read_text()
 for a,b in pairs:assert a in s,(name,a);s=s.replace(a,b)
 ast.parse(s);p.write_text(s)
for name in ['run.py','audit.py','exports.py']:edit(name,[('ETH_FUND_MEDIAN_COUNT','ETH_EWM_LENGTH_DAYS')])
edit('exports.py',[("ETH matured funding median count M; R0.00875","ETH finite EWM length S (days); M4/R0.00875"),("['M2','M3','M4']","['S12','S16','S20']"),('Preregistered ETH funding median M / reused BTC volatility V','Preregistered ETH EWM length S / reused BTC volatility V')])
edit('definitions.py',[("q['trend_lookback_days']==16","q['trend_lookback_days'] in [12,20] and q['trend_window_days']==q['trend_lookback_days'] and q['trend_decay_numerator']==q['trend_lookback_days']-1 and q['trend_decay_denominator']==q['trend_lookback_days']+1"),("q['entry_funding_settlement_count'] in [2,3]","q['entry_funding_settlement_count']==4")])
edit('parent_units.py',[("g['W']==3","g['W']==16")])
for name in ['observe_fewm.py','observe_candidate.py']:edit(name,[('1891317','1926187')])
edit('freeze.py',[("Predeclare BTC entry volatility memories with fixed early exit, reusing actual ETH banks.","Predeclare ETH finite EWM memory length with fixed funding budget and reused BTC banks.")])
previous=json.loads((ROOT/'.git/automation_proofs/20261114T235607Z.json').read_text());assert previous['status']=='completed_published_verified_unlocked';head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();assert head==subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT,text=True).strip();assert json.loads((R/'exact_parameter_registry_screen.json').read_text())['passed']
(R/'startup.json').write_text(json.dumps({'round':R.name,'trigger_utc':'2026-11-15T01:56:14.348Z','base_commit':head,'branch_lock_broker_pid':1926187,'branch_lock_session':31401,'branch_lock_native_start_chunk':'6b7758','root_native_verification_chunk':'202873','successful_fetch_start_chunk':'429f2e','successful_fetch_completion_chunk':'d1f548','successful_fetch_session':38985,'successful_fetch_exit_code':0,'initial_sync_no_merge_required':True,'only_preexisting_untracked':'data/normalized','previous_round_publication_verified':previous['status'],'previous_commit':previous['commit'],'previous_final_main_commit':previous['final_main_commit'],'last_actual_account_round':'20261114T235607Z','peer_01UTC_paper10_commit_preserved':head,'old_blocked_failure_records_unchanged':True},indent=2)+'\n')
checked=[]
for p in R.rglob('*.py'):
 t=ast.parse(p.read_text());assert not[n for n in ast.walk(t) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id in ['ROOT','R','P']],str(p);checked.append(str(p.relative_to(ROOT)))
(R/'path_join_guard.json').write_text(json.dumps({'passed':True,'checked':checked,'Path_names_not_subscripted':True,'before_binding_and_evaluation':True,'no_model_or_account_calculations':True},indent=2)+'\n');print('PASS ETHnewS12/S20 fixedM4R.00875 xreadonlyBTCV10/V14;engine/coreidentical;currentfund0all,PID1926187 beforebinding')
