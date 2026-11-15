"""Prepare existing-engine entry hurdle variants before any reservation or calculation."""
import ast,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2]
def edit(name,pairs):
 p=R/name;s=p.read_text()
 for a,b in pairs:assert a in s,(name,a);s=s.replace(a,b)
 ast.parse(s);p.write_text(s)
for name in ['run.py','audit.py','exports.py']:edit(name,[('BTC_LOOKBACK_DAYS','BTC_ENTRY_HURDLE')])
edit('definitions.py',[("q['lookback_days'] in [28,30]","q['lookback_days']==29"),("q['return_hurdle']==.03","q['return_hurdle'] in [.025,.035]")])
edit('parent_units.py',[("g['W']==29","g['W']==.03")])
edit('exports.py',[("BTC completed ROC lookback L; H3%/E0.5%/V10cap3%","BTC ROC entry threshold H"),("['28 days','29 days','30 days']","['2.5%','3.0%','3.5%']"),('Preregistered BTC ROC lookback / reused ETH funding budget','Preregistered BTC entry hurdle H / reused ETH funding budget')])
for name in ['observe_fewm.py','observe_candidate.py']:edit(name,[('1995416','2026073')])
previous=json.loads((ROOT/'.git/automation_proofs/20261115T075947Z.json').read_text());assert previous['status']=='completed_published_verified_unlocked' and previous['fresh_final_git_verification']['passed'];head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();assert head==subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT,text=True).strip();assert json.loads((R/'exact_parameter_registry_screen.json').read_text())['passed']
(R/'startup.json').write_text(json.dumps({'round':R.name,'trigger_utc':'2026-11-15T09:59:44.962Z','base_commit':head,'branch_lock_broker_pid':2026073,'branch_lock_session':87716,'branch_lock_native_start_chunk':'78e6a9','root_native_verification_chunk':'afb37d','successful_fetch_start_chunk':'72ac9f','successful_fetch_completion_chunk':'178fb7','successful_fetch_session':11194,'successful_fetch_exit_code':0,'initial_sync_no_merge_required':True,'initial_tracked_and_index_clean':True,'only_preexisting_untracked':'data/normalized','previous_round_publication_verified':previous['status'],'previous_commit':previous['commit'],'previous_final_main_commit':previous['final_main_commit'],'last_actual_account_round':'20261115T075947Z','previous_stale_lock_recovery_not_repeated':True,'peer_current_quote_and_sampling_gap_commit_preserved':head,'old_blocked_failure_records_unchanged':True},indent=2)+'\n')
checked=[]
for p in R.rglob('*.py'):
 t=ast.parse(p.read_text());assert not[n for n in ast.walk(t) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id in ['ROOT','R','P']],str(p);checked.append(str(p.relative_to(ROOT)))
(R/'path_join_guard.json').write_text(json.dumps({'passed':True,'checked':checked,'Path_names_not_subscripted':True,'before_binding_and_evaluation':True,'no_model_or_account_calculations':True},indent=2)+'\n');print('PASS BTC H.025/.035 fixedL29/E.005/V10cap3 xreadonlyETHR, originalmarkonly, PID2026073')
