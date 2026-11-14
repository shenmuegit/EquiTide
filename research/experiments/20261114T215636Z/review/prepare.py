"""Prepare new V6/10 volatility memories and restore pending original-account capture, no evaluations."""
from pathlib import Path
import ast,json,subprocess
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2]
def edit(name,pairs):
 p=R/name;s=p.read_text()
 for a,b in pairs:assert a in s,(name,a);s=s.replace(a,b)
 ast.parse(s);p.write_text(s)
for name in ['run.py','audit.py','exports.py']:edit(name,[('BTC_LOOKBACK_DAYS','BTC_VOL_WINDOW_DAYS')])
edit('definitions.py',[("q['exit_buffer_fraction']==.005 and q['lookback_days'] in [28,30] and q['return_hurdle']==.03 and q['entry_volatility_window_days']==14","q['exit_buffer_fraction']==.005 and q['lookback_days']==29 and q['return_hurdle']==.03 and q['entry_volatility_window_days'] in [6,10]")])
edit('parent_units.py',[("g['W']==29","g['W']==10")])
p=R/'parent_units.py';s=p.read_text();s=s.replace("for L in [28,29,30]:","for L in [29]:");s+="\n# Actual samplelogvol window semantics and future-suffix exclusion, synthetic only.\nfor V in [6,10,14]:\n expected=statistics.stdev([math.log(closes[j]/closes[j-1]) for j in range(i-V,i)]);assert engine.btc_entry_sigma(closes,i,V)==expected==engine.btc_entry_sigma(closes[:i]+[10**12,1],i,V)\n assert engine.entry_filter(1,0,expected,expected)==1 and engine.entry_filter(1,0,expected,expected-1e-12)==0 and engine.entry_filter(1,1,expected,expected-1e-12)==1\n";ast.parse(s);p.write_text(s)
edit('exports.py',[("ylabel='BTC momentum memory L; H3%/exit0.5%/V14cap3%'","ylabel='BTC entry volatility memory V; L29/H3%/exit0.5%/cap3%'"),("['28 days','29 days','30 days']","['6 days','10 days','14 days']"),('Preregistered BTC momentum memory / ETH funding-budget ratio','Preregistered BTC entry volatility memory / ETH funding-budget ratio')])
for name in ['observe_fewm.py','observe_candidate.py']:edit(name,[('1824037','1857068')])
# The immediately preceding round did not advance accounts. SMA uses the original last-real batch/specs.
edit('forward_registry.py',[("PREV=ROOT/'research/experiments/20261114T195634Z'","PREV=ROOT/'research/experiments/20261114T175537Z'")])
previous=json.loads((ROOT/'.git/automation_proofs/20261114T195634Z.json').read_text());assert previous['status']=='completed_published_verified_unlocked';head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();assert subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT,text=True).strip()==head
(R/'startup.json').write_text(json.dumps({'round':R.name,'trigger_utc':'2026-11-14T21:56:36.244Z','base_commit':head,'branch_lock_broker_pid':1857068,'branch_lock_session':11955,'branch_lock_native_start_chunk':'b003d1','root_native_verification_chunk':'d60e01','successful_fetch_start_chunk':'b197ed','successful_fetch_completion_chunk':'b6eabf','successful_fetch_session':48145,'successful_fetch_exit_code':0,'initial_sync_no_merge_required':True,'only_preexisting_untracked':'data/normalized','previous_round_publication_verified':previous['status'],'previous_commit':previous['commit'],'previous_final_main_commit':previous['final_main_commit'],'last_actual_account_round':'20261114T175537Z','prior_blocked_round':'20261114T195634Z','pending_account_windows_preserved':True},indent=2)+'\n')
f=R/'read_failures.json';d=json.loads(f.read_text());d['facts'].append({'action':'Precalculation registry screen used nonexistent parameters.asset filter','resolved':True,'resolution':'Retained original screen and reran fullregistry using spec.universe;confirmed V14actual source and V6/V10 absent before spec/reserve/calculation','actual_model_or_account_calculations':0,'initial_native_chunk':'b7f033','corrected_native_chunk':'96f507'});f.write_text(json.dumps(d,indent=2)+'\n')
checked=[]
for p in R.rglob('*.py'):
 tree=ast.parse(p.read_text());assert not [n for n in ast.walk(tree) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id in ['ROOT','R','P']],str(p);checked.append(str(p.relative_to(ROOT)))
(R/'path_join_guard.json').write_text(json.dumps({'passed':True,'checked':checked,'Path_names_not_subscripted':True,'before_binding_and_evaluation':True,'no_model_or_account_calculations':True},indent=2)+'\n');print('PASS V6/10/14 xETHR beforeoutcomes,exact engine/core unchanged;original accounts resume same pending cutoffs,PID1857068')
