"""Prepare new BTC variance-memory windows, keeping cap and all money formulas fixed."""
import ast,copy,importlib.util,json,re,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];P=ROOT/'research/experiments/20261115T140053Z';sys.path.insert(0,str(R));from common import sha,put,rel,now,reg
oldguard='V in [6,10,14]';newguard='V in [6,8,10,12,14]'
def edit(name,pairs):
 p=R/name;s=p.read_text()
 for a,b in pairs:assert a in s,(name,a);s=s.replace(a,b)
 ast.parse(s);p.write_text(s)
edit('engine.py',[(oldguard,newguard)])
edit('audit.py',[(oldguard,newguard),('BTC_VOL_CAP','BTC_VOL_WINDOW')])
edit('run.py',[('BTC_VOL_CAP','BTC_VOL_WINDOW')])
edit('definitions.py',[("'cap in [.0225,.025,.0275,.03,.035,.04,.05]','cap in [.025,.03,.035,.04,.05]'",repr(newguard)+','+repr(oldguard)),("q['entry_volatility_window_days']==10","q['entry_volatility_window_days'] in [8,12]"),("q['entry_volatility_ceiling'] in [.0225,.0275]","q['entry_volatility_ceiling']==.0275")])
edit('parent_units.py',[("g['W']==.025","g['W']==10"),("for V in [6,10,14]:","for V in [6,8,10,12,14]:")])
edit('freeze.py',[
 ('ba6c570ac9c64ef57fdcc21d3320fe8defb3529ff645b0994cb303d2303c2185','078ecce7a424462c86b0559ffae47e176f267d2841790565d4f092976bd88797'),
 ('72c778c12f8cefb3104cbf270ce3a64f5d658da9aee22a370b01ecb52fa95c73','dda0521e94bd136aadf60ea7a5ea011854a281dd5579559a21e7cb28d6cee36b'),
 ('6dcbe8366b3d72478c077eb1206a7cc986832c469b6df40cb48bf8adb9019cbe','6c3e417f232a5eba7a7d44074d0415c085c283c49993f7a497d460c5222c24f0'),
 ('bs={.025:reuse(B,.025,.01)};es={r:reuse(actual(fp),.025,r)','bs={10:reuse(B,10,.01)};es={r:reuse(actual(fp),10,r)'),
 ('[.0225,.0275]','[8,12]'),('[.0225,.025,.0275]','[8,10,12]'),('if V==.025:','if V==10:'),("==(.0225,.01)","==(8,.01)"),("'representative_preset':{'W':.0225","'representative_preset':{'W':8"),
 ('priorV10sampledailylogvol<=cap[8,10,12]','priorV[8,10,12]sampledailylogvol<=cap.0275'),
 ("sp['parameters']['entry_volatility_ceiling']=V","sp['parameters']['entry_volatility_window_days']=V"),
 ("name=f'BTC_L29_H3_E0p005_V10cap{str(V).replace(chr(46),chr(112))}_391d'","name=f'BTC_L29_H3_E0p005_V{V}cap0p0275_391d'"),
 ("name=f'parent_BTCV10cap{str(V).replace(chr(46),chr(112))}_L29_H3_E0p005_ETHR","name=f'parent_BTCV{V}cap0p0275_L29_H3_E0p005_ETHR"),
 ('btc-volatility-ceiling-earlyexit-neighborhood','btc-volatility-window-earlyexit-neighborhood'),('btc-volatility-ceiling-eth-carry-bank-combination','btc-volatility-window-eth-carry-bank-combination'),
 ('BTC_VOL_CAP','BTC_VOL_WINDOW'),('BTC_native_only_own_entry_volatility_cap_axis','BTC_native_only_own_entry_volatility_window_axis'),('ThreeBTCvolatilitycap','ThreeBTCvolatilitywindows')])
f=R/'freeze.py';s=f.read_text();s,n=re.subn(r"'hypothesis':'[^']*'","'hypothesis':'Does BTC sample-logvol memoryV8/V12 at fixedL29/H.03/E.005/cap.0275 improve chronological net performance around actualV10? V[8,10,12] x readonlyETHR[.00875,.01]. PresetV8/R.01 frozenbeforeoutcomes: shorter memory responds faster to risk shifts; longer memory smooths noise but may delay risk screening. No after-result extension/reselection. V10/ETHbanks/centerparents/holds readonly.'",s);assert n==1;s,n=re.subn(r"'W':'[^']*'","'W':'BTC completed daily logreturn sample-volatility memory V in8/10/12 days;cap.0275,L29/H.03/E.005 fixed;new or reversed entries only'",s);assert n==1;s,n=re.subn(r"'novelty':'[^']*'","'novelty':'NewBTCvolwindows8/12 atfixedL29/H.03/E.005/cap.0275;existingV10center and ETHbanks readonly;new exactwindows absent.'",s);assert n==1;ast.parse(s);f.write_text(s)
edit('exports.py',[('BTC_VOL_CAP','BTC_VOL_WINDOW'),('BTC V10 daily logvol ceiling','BTC entry volatility window, days'),("['2.25%','2.50%','2.75%']","['8 days','10 days','12 days']"),('Preregistered BTC volatility ceiling / reused ETH funding budget','Preregistered BTC volatility memory / reused ETH funding budget')])
edit('review/diagnostics.py',[("center=btc[.025]","center=btc[10]"),('[.0225,.0275]','[8,12]'),("c['W']==.025","c['W']==10"),('BTC_V10_entry_volatility_cap_fraction','BTC_entry_volatility_window_days'),('BTC_volatility_cap_axis_boundary','BTC_volatility_window_axis_boundary'),('matched_cap2p5','matched_window10'),('old_cap2p5','old_window10'),('entry-volatility-ceiling','entry-volatility-window')])
edit('review/visual_review.py',[('BTC_V10_logvol_cap','BTC_entry_vol_window_days'),('{.0225,.025,.0275}','{8,10,12}'),('[.0225,.0275]','[8,12]'),("y['BTC_entry_vol_window_days']==.025","y['BTC_entry_vol_window_days']==10"),('old_cap2p5','old_window10'),("'BTC_cap':x['BTC_entry_vol_window_days']","'BTC_vol_window_days':x['BTC_entry_vol_window_days']"),('BTC V10 sampledailylogvol cap2.25/2.5/2.75percent rows','BTC sampledailylogvol memory8/10/12days rows,cap2.75percent fixed')])
rs=reg.read_records(ROOT/'research/automation/registry.jsonl');hits=[]
for fp,z in rs.items():
 q=z.get('spec',{}).get('parameters',{});s=z.get('spec',{})
 if s.get('kind')=='strategy' and s.get('universe')==['BTC/USDT'] and q.get('lookback_days')==29 and q.get('return_hurdle')==.03 and q.get('exit_buffer_fraction')==.005 and q.get('entry_volatility_ceiling')==.0275 and q.get('continuous_oos_days')==391 and q.get('initial_capital_usdt')==3750 and q.get('fixed_entry_notional_usdt')==1000 and q.get('start_utc')=='2025-10-19T00:01:00Z' and q.get('end_utc')=='2026-11-14T00:01:00Z':hits.append({'fingerprint':fp,'V':q.get('entry_volatility_window_days'),'status':z['status'],'result_available':z['result_available']})
assert hits and not any(z['V'] in [8,12] and (z['result_available'] or z['status']=='reserved') for z in hits);put(R/'exact_parameter_registry_screen.json',{'passed':True,'recorded_utc':now(),'fixed':{'asset':'BTC/USDT','L':29,'H':.03,'E':.005,'cap':.0275,'capital':3750,'notional':1000,'start':'2025-10-19T00:01:00Z','end':'2026-11-14T00:01:00Z'},'new_volatility_windows':[8,12],'matching_fixed_definitions':hits,'no_market_model_or_account_calculations':True})
old=(P/'engine.py').read_text();new=(R/'engine.py').read_text();assert new.replace(newguard,oldguard)==old;assert sha(P/'core391_tail_safe.py')==sha(R/'core391_tail_safe.py')
def module(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
om,nm=module('old_window_guard',P/'engine.py'),module('new_window_guard',R/'engine.py');spec=copy.deepcopy(rs['078ecce7a424462c86b0559ffae47e176f267d2841790565d4f092976bd88797']['spec']);m={'asset':'BTC','closes':[100+j*.2 for j in range(60)]};tests=[]
for V in [6,8,10,12,14]:
 sp=copy.deepcopy(spec);sp['parameters']['entry_volatility_window_days']=V;result=nm.base_decide(sp,m,40,0);sigma=nm.btc_entry_sigma(m['closes'],40,V);raw=1 if m['closes'][39]/m['closes'][10]-1>.03 else 0;assert result[0]==(0 if raw and sigma>.0275 else raw) and result[1]['volatility_window_days']==V
 if V in [6,10,14]:assert om.base_decide(sp,m,40,0)==result
 tests.append({'V':V,'passed':True,'old_value_exact_equivalence':V in [6,10,14]})
put(R/'prebinding_parameter_guard_verification.json',{'passed':True,'recorded_utc':now(),'old_source':rel(P/'engine.py'),'old_sha256':sha(P/'engine.py'),'new_source':rel(R/'engine.py'),'new_sha256':sha(R/'engine.py'),'exact_only_source_change':{'old':oldguard,'new':newguard},'formulas_and_full_AST_unchanged_after_validation_list_normalization':True,'simulate_and_money_core_bytes_unchanged':True,'synthetic_checks':tests,'before_first_reservation_or_market_calculation':True,'current_evaluation_failures':0})
previous=json.loads((ROOT/'.git/automation_proofs/20261115T140053Z.json').read_text());assert previous['status']=='completed_published_verified_unlocked' and previous['fresh_final_git_verification']['passed'];head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert head==subprocess.check_output(['git','rev-parse','origin/main'],text=True).strip();put(R/'startup.json',{'round':R.name,'trigger_utc':'2026-11-15T16:01:24.195Z','base_commit':head,'branch_lock_broker_pid':2121758,'branch_lock_session':33419,'branch_lock_native_start_chunk':'8f51d8','root_native_verification_chunk':'205fa2','successful_fetch_start_chunk':'399468','successful_fetch_completion_chunk':'bb2615','successful_fetch_session':64881,'successful_fetch_exit_code':0,'initial_sync_no_merge_required':True,'initial_tracked_and_index_clean':True,'only_preexisting_untracked':'data/normalized','previous_round_publication_verified':previous['status'],'previous_commit':previous['commit'],'previous_final_main_commit':previous['final_main_commit'],'last_actual_account_round':P.name,'previous_stale_lock_recovery_not_repeated':True,'peer_current_quote_commit_preserved':head,'old_blocked_failure_records_unchanged':True})
checked=[]
for f in R.rglob('*.py'):
 tree=ast.parse(f.read_text());assert not[n for n in ast.walk(tree) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id in ['ROOT','R','P']],str(f);checked.append(rel(f))
put(R/'path_join_guard.json',{'passed':True,'checked':checked,'Path_names_not_subscripted':True,'before_binding_and_evaluation':True,'no_model_or_account_calculations':True});print('PASS newBTCV8/V12 fixedcap.0275,H3/E.5/L29 xreadonlyETHR;5syntheticwindowchecks;0actualcalculations')
