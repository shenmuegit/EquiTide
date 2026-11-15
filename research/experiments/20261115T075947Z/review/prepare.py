"""Prepare unchanged-engine ROC lookbacks and actual original midnight adapters before calculation."""
import ast,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2]
def edit(name,pairs):
 p=R/name;s=p.read_text()
 for a,b in pairs:assert a in s,(name,a);s=s.replace(a,b)
 ast.parse(s);p.write_text(s)
for name in ['run.py','audit.py','exports.py']:edit(name,[('BTC_VOL_CEILING','BTC_LOOKBACK_DAYS')])
edit('definitions.py',[("q['lookback_days']==29","q['lookback_days'] in [28,30]"),("q['entry_volatility_ceiling'] in [.04,.05]","q['entry_volatility_ceiling']==.03")])
edit('parent_units.py',[("g['W']==.04","g['W']==29")])
edit('exports.py',[("BTC entry volatility ceiling; L29/H3%/E0.5%/V10","BTC completed ROC lookback L; H3%/E0.5%/V10cap3%"),("['3%','4%','5%']","['28 days','29 days','30 days']"),('Preregistered BTC entry volatility ceiling / reused ETH funding budget','Preregistered BTC ROC lookback / reused ETH funding budget')])
for name in ['observe_fewm.py','observe_candidate.py']:edit(name,[('1956168','1995416')])
previous=json.loads((ROOT/'.git/automation_proofs/20261115T035715Z.json').read_text());recovery=json.loads((R/'recovered_prior_publication.json').read_text());assert previous['status']=='completed_published_verified_unlocked' and recovery['passed'];head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();assert head==subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT,text=True).strip()==recovery['commit'];assert json.loads((R/'exact_parameter_registry_screen.json').read_text())['passed']
(R/'startup.json').write_text(json.dumps({'round':R.name,'trigger_utc':'2026-11-15T07:59:47.679Z','base_commit':head,'branch_lock_broker_pid':1995416,'branch_lock_session':8963,'branch_lock_native_start_chunk':'f6526d','branch_lock_native_acquisition_chunk':'f90e3a','root_native_verification_chunk':'87c74b','successful_fetch_start_chunk':'fdb5ab','successful_fetch_completion_chunk':'a06375','successful_fetch_session':91677,'successful_fetch_exit_code':0,'initial_sync_no_merge_required_after_prior_recovery':True,'initial_37_staged_peer_files_preserved_and_published':True,'recovered_peer_commit':recovery['commit'],'only_preexisting_untracked':'data/normalized','previous_round_publication_verified':previous['status'],'previous_commit':previous['commit'],'previous_final_main_commit':previous['final_main_commit'],'last_actual_account_round':'20261115T035715Z','old_blocked_failure_records_unchanged':True},indent=2)+'\n')
checked=[]
for p in R.rglob('*.py'):
 t=ast.parse(p.read_text());assert not[n for n in ast.walk(t) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id in ['ROOT','R','P']],str(p);checked.append(str(p.relative_to(ROOT)))
(R/'path_join_guard.json').write_text(json.dumps({'passed':True,'checked':checked,'Path_names_not_subscripted':True,'before_binding_and_evaluation':True,'no_model_or_account_calculations':True},indent=2)+'\n');print('PASS BTCL28/L30fixedcap3,ETHbanksreadonly;SMAoriginaldaily67prepared,PID1995416')
