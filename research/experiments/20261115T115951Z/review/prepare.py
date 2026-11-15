"""Predeclare native BTC volatility ceilings using unchanged policy and money kernels."""
import ast,json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import sha,put,rel,now,reg

def edit(name,pairs):
 p=R/name;s=p.read_text()
 for a,b in pairs:
  assert a in s,(name,a);s=s.replace(a,b)
 ast.parse(s);p.write_text(s)
for name in ['run.py','audit.py','exports.py']:edit(name,[('BTC_ENTRY_HURDLE','BTC_VOL_CAP')])
edit('audit.py',[("cap in [.03,.04,.05]","cap in [.025,.03,.035,.04,.05]")])
edit('definitions.py',[("q['return_hurdle'] in [.025,.035]","q['return_hurdle']==.03"),("q['entry_volatility_ceiling']==.03","q['entry_volatility_ceiling'] in [.025,.035]")])
edit('parent_units.py',[("for cap in [.03,.04,.05]:","for cap in [.025,.03,.035,.04,.05]:")])
edit('exports.py',[('BTC ROC entry threshold H','BTC V10 daily logvol ceiling'),('Preregistered BTC entry hurdle H / reused ETH funding budget','Preregistered BTC volatility ceiling / reused ETH funding budget')])
edit('freeze.py',[
 ('BTC entry threshold with fixed ROC memory,volatility and early exit','BTC entry volatility ceiling with fixed ROC memory,entry and early exit'),
 ("rules['signal']='BTC strictcompletedROC L29/entryH[.025,.03,.035]/exitE.005,priorV10sampledailylogvol<=.03,new/reversedentryonly;","rules['signal']='BTC strictcompletedROC L29/entryH.03/exitE.005,priorV10sampledailylogvol<=cap[.025,.03,.035],new/reversedentryonly;"),
 ("name=f'BTC_L29_H{str(V).replace(chr(46),chr(112))}_E0p005_V10cap3_391d'","name=f'BTC_L29_H3_E0p005_V10cap{str(V).replace(chr(46),chr(112))}_391d'"),
 ("sp['parameters']['return_hurdle']=V","sp['parameters']['entry_volatility_ceiling']=V"),
 ('btc-entry-hurdle-earlyexit-neighborhood','btc-volatility-ceiling-earlyexit-neighborhood'),
 ("name=f'parent_BTCH{str(V).replace(chr(46),chr(112))}_L29_V10cap3_E0p005_ETHR","name=f'parent_BTCV10cap{str(V).replace(chr(46),chr(112))}_L29_H3_E0p005_ETHR"),
 ('btc-entry-hurdle-earlyexit-eth-carry-bank-combination','btc-volatility-ceiling-eth-carry-bank-combination'),
 ('BTC_ENTRY_HURDLE','BTC_VOL_CAP'),
 ('BTC absolute completed29dayROC entry thresholdH fraction,.025/.03/.035=2.5/3/3.5percent;L29/E.005/V10cap.03fixed','BTC unbiased sample daily logvol V10 entry ceiling fraction,.025/.03/.035=2.5/3/3.5percent;L29/H.03/E.005fixed;new or reversed entry only'),
 ('Does BTC entryH.025/.035 at fixedL29/E.005/V10cap.03 improve chronological net performance around actualH.03? H[.025,.03,.035] x readonlyETHR[.00875,.01]. PresetH.025/R.01 frozenbeforeoutcomes: earlier weaker trend entries may retain opportunities,whileH.035 tests stronger confirmation. No result-driven extension/reselection. H.03/ETHbanks/centerparents/holds readonly.','Does BTC V10 entry volatility cap.025/.035 at fixedL29/H.03/E.005 improve chronological net performance around actualcap.03? Cap[.025,.03,.035] x readonlyETHR[.00875,.01]. Presetcap.025/R.01 frozenbeforeoutcomes: lower cap may avoid volatile entries at an opportunity cost;cap.035 tests relaxed risk screening. No result-driven extension/reselection. Cap.03/ETHbanks/centerparents/holds readonly.'),
 ('BTC_native_only_own_entry_hurdle_axis','BTC_native_only_own_entry_volatility_cap_axis'),
 ('ThreeBTCentryhurdle x2ETHbudget','ThreeBTCvolatilitycap x2ETHbudget'),
 ('NewBTCH.025/.035 atfixedL29/E.005/V10cap.03,exactcoreparameterlookup only foundactualH.03','NewBTCcap.025/.035 atfixedL29/H.03/E.005/V10,exactcoreparameterlookup only foundactualcap.03/.04/.05;two newcaps absent'),
 ('PASS6new/8readonly,predeclared3BTCentryHx2ETHR','PASS6new/8readonly,predeclared3BTCvolcapsx2ETHR')])
edit('review/diagnostics.py',[('ROC-entry-hurdle','entry-volatility-ceiling'),('BTC_ROC_entry_hurdle_fraction','BTC_V10_entry_volatility_cap_fraction'),('different_daily_desired_count_vs_old_H3','different_daily_desired_count_vs_old_cap3'),('optima_at_BTC_entry_hurdle_axis_boundary','optima_at_BTC_volatility_cap_axis_boundary'),('matched_H3','matched_cap3'),('BTC ROC entry hurdle trade changes','BTC entry-volatility-cap trade changes')])
# Current original account windows advance exactly two hours; full67 authority stays the original dictionary.
edit('collect.py',[("SMA_original_latest_daily_adapter=rel(P/'forward.py')","SMA_original_latest_daily_adapter='research/experiments/20261115T075947Z/forward.py'")])
previous=json.loads((ROOT/'.git/automation_proofs/20261115T095944Z.json').read_text());assert previous['status']=='completed_published_verified_unlocked' and previous['fresh_final_git_verification']['passed'];head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();assert head==subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT,text=True).strip()
rs=reg.read_records(ROOT/'research/automation/registry.jsonl');hits=[]
for fp,z in rs.items():
 s=z.get('spec',{});q=s.get('parameters',{})
 if s.get('kind')=='strategy' and s.get('universe')==['BTC/USDT'] and q.get('lookback_days')==29 and q.get('return_hurdle')==.03 and q.get('exit_buffer_fraction')==.005 and q.get('entry_volatility_window_days')==10 and q.get('continuous_oos_days')==391 and q.get('initial_capital_usdt')==3750 and q.get('fixed_entry_notional_usdt')==1000 and q.get('start_utc')=='2025-10-19T00:01:00Z' and q.get('end_utc')=='2026-11-14T00:01:00Z':hits.append({'fingerprint':fp,'cap':q.get('entry_volatility_ceiling'),'status':z['status'],'result_available':z['result_available']})
assert hits and not any(z['cap'] in [.025,.035] and (z['result_available'] or z['status']=='reserved') for z in hits)
put(R/'exact_parameter_registry_screen.json',{'passed':True,'recorded_utc':now(),'fixed':{'asset':'BTC/USDT','L':29,'H':.03,'E':.005,'V':10,'capital':3750,'notional':1000,'start':'2025-10-19T00:01:00Z','end':'2026-11-14T00:01:00Z'},'new_caps':[.025,.035],'matching_fixed_definitions':hits,'no_market_model_or_account_calculations':True})
put(R/'startup.json',{'round':R.name,'trigger_utc':'2026-11-15T11:59:51.558Z','base_commit':head,'branch_lock_broker_pid':2057114,'branch_lock_session':44268,'branch_lock_native_start_chunk':'c57dde','root_native_verification_chunk':'0a7704','successful_fetch_start_chunk':'b579c5','successful_fetch_completion_chunk':'14c41d','successful_fetch_session':9536,'successful_fetch_exit_code':0,'initial_sync_no_merge_required':True,'initial_tracked_and_index_clean':True,'only_preexisting_untracked':'data/normalized','previous_round_publication_verified':previous['status'],'previous_commit':previous['commit'],'previous_final_main_commit':previous['final_main_commit'],'last_actual_account_round':'20261115T095944Z','previous_stale_lock_recovery_not_repeated':True,'peer_current_quote_commit_preserved':head,'old_blocked_failure_records_unchanged':True})
checked=[]
for f in R.rglob('*.py'):
 t=ast.parse(f.read_text());assert not[n for n in ast.walk(t) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id in ['ROOT','R','P']],str(f);checked.append(rel(f))
put(R/'path_join_guard.json',{'passed':True,'checked':checked,'Path_names_not_subscripted':True,'before_binding_and_evaluation':True,'no_model_or_account_calculations':True})
print('PASS BTC cap.025/.035 at fixedL29/H.03/E.005/V10 xreadonlyETHR;currentPID2057114;0calculations')
