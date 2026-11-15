"""Freeze a new cap neighborhood and validate its allowlist before first reservation."""
import ast,copy,importlib.util,json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];P=ROOT/'research/experiments/20261115T115951Z';sys.path.insert(0,str(R));from common import sha,put,rel,now,reg
oldguard='cap in [.025,.03,.035,.04,.05]';newguard='cap in [.0225,.025,.0275,.03,.035,.04,.05]'
def edit(name,pairs):
 p=R/name;s=p.read_text()
 for a,b in pairs:assert a in s,(name,a);s=s.replace(a,b)
 ast.parse(s);p.write_text(s)
edit('engine.py',[(oldguard,newguard)])
edit('audit.py',[(oldguard,newguard)])
edit('definitions.py',[("ast.parse(f.read_text())","ast.parse(f.read_text().replace("+repr(newguard)+","+repr(oldguard)+"))"),("q['entry_volatility_ceiling'] in [.025,.035]","q['entry_volatility_ceiling'] in [.0225,.0275]"),("'policy_and_accounting_source_equal_to_prior':True","'policy_and_accounting_source_equal_to_prior':False,'policy_and_money_formulas_unchanged_except_predeclared_parameter_allowlist':True"),("'all_policy_and_native_money_AST_unchanged':True","'all_policy_and_native_money_AST_unchanged_after_allowlist_normalization':True")])
edit('parent_units.py',[("for cap in [.025,.03,.035,.04,.05]:","for cap in [.0225,.025,.0275,.03,.035,.04,.05]:"),("g['W']==.03","g['W']==.025")])
edit('freeze.py',[
 ('96a6c17aceebe9885daeb45520d5e7aef8eb07506f066c2c2cbf41eabdbc04e5','ba6c570ac9c64ef57fdcc21d3320fe8defb3529ff645b0994cb303d2303c2185'),
 ('23f59d89bb092422e945f5de3f3f068c924c06cb819488637a9e955472cc6d94','72c778c12f8cefb3104cbf270ce3a64f5d658da9aee22a370b01ecb52fa95c73'),
 ('41f377ade77f1c2630d40b9816bec506a9a8bb26bbb143d89534c555e942bdf7','6dcbe8366b3d72478c077eb1206a7cc986832c469b6df40cb48bf8adb9019cbe'),
 ('bs={.03:reuse(B,.03,.01)};es={r:reuse(actual(fp),.03,r)','bs={.025:reuse(B,.025,.01)};es={r:reuse(actual(fp),.025,r)'),
 ('[.025,.035]','[.0225,.0275]'),('[.025,.03,.035]','[.0225,.025,.0275]'),('if V==.03:','if V==.025:'),("==(.025,.01)","==(.0225,.01)"),("'representative_preset':{'W':.025","'representative_preset':{'W':.0225"),
 ('Does BTC V10 entry volatility cap.025/.035 at fixedL29/H.03/E.005 improve chronological net performance around actualcap.03? Cap[.0225,.025,.0275] x readonlyETHR[.00875,.01]. Presetcap.025/R.01 frozenbeforeoutcomes: lower cap may avoid volatile entries at an opportunity cost;cap.035 tests relaxed risk screening. No result-driven extension/reselection. Cap.03/ETHbanks/centerparents/holds readonly.','Does BTC V10 cap.0225/.0275 at fixedL29/H.03/E.005 improve chronological net performance around actualcap.025? Cap[.0225,.025,.0275] x readonlyETHR[.00875,.01]. Presetcap.0225/R.01 frozenbeforeoutcomes. New preregistered neighborhood brackets prior boundary best .025; test whether conservative filtering keeps an interior plateau or loses opportunities. No after-result extension/reselection. Cap.025/ETHbanks/centerparents/holds readonly.'),
 ('.025/.03/.035=2.5/3/3.5percent','.0225/.025/.0275=2.25/2.5/2.75percent'),
 ('NewBTCcap.025/.035 atfixedL29/H.03/E.005/V10,exactcoreparameterlookup only foundactualcap.03/.04/.05;two newcaps absent','NewBTCcap.0225/.0275 atfixedL29/H.03/E.005/V10;actualcap.025 center and ETHbanks readonly;exact newcaps absent')])
edit('exports.py',[("['2.5%','3.0%','3.5%']","['2.25%','2.50%','2.75%']")])
edit('review/diagnostics.py',[("center=btc[.03]","center=btc[.025]"),('[.025,.035]','[.0225,.0275]'),("c['W']==.03","c['W']==.025"),('matched_cap3','matched_cap2p5'),('old_cap3','old_cap2p5')])
edit('review/visual_review.py',[('{.025,.03,.035}','{.0225,.025,.0275}'),('[.025,.035]','[.0225,.0275]'),("y['BTC_V10_logvol_cap']==.03","y['BTC_V10_logvol_cap']==.025"),('old_cap3','old_cap2p5'),('cap2.5/3/3.5percent','cap2.25/2.5/2.75percent')])
rs=reg.read_records(ROOT/'research/automation/registry.jsonl');hits=[]
for fp,z in rs.items():
 q=z.get('spec',{}).get('parameters',{});s=z.get('spec',{})
 if s.get('kind')=='strategy' and s.get('universe')==['BTC/USDT'] and q.get('lookback_days')==29 and q.get('return_hurdle')==.03 and q.get('exit_buffer_fraction')==.005 and q.get('entry_volatility_window_days')==10 and q.get('continuous_oos_days')==391 and q.get('initial_capital_usdt')==3750 and q.get('fixed_entry_notional_usdt')==1000:hits.append({'fingerprint':fp,'cap':q.get('entry_volatility_ceiling'),'status':z['status'],'result_available':z['result_available']})
assert hits and not any(z['cap'] in [.0225,.0275] and (z['result_available'] or z['status']=='reserved') for z in hits);put(R/'exact_parameter_registry_screen.json',{'passed':True,'recorded_utc':now(),'fixed':{'asset':'BTC/USDT','L':29,'H':.03,'E':.005,'V':10,'capital':3750,'notional':1000,'start':'2025-10-19T00:01:00Z','end':'2026-11-14T00:01:00Z'},'new_caps':[.0225,.0275],'matching_fixed_definitions':hits,'no_market_model_or_account_calculations':True})
old=(P/'engine.py').read_text();new=(R/'engine.py').read_text();assert new.replace(newguard,oldguard)==old;assert sha(P/'core391_tail_safe.py')==sha(R/'core391_tail_safe.py')
def module(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
om,nm=module('old_guard',P/'engine.py'),module('new_guard',R/'engine.py');spec=copy.deepcopy(rs['ba6c570ac9c64ef57fdcc21d3320fe8defb3529ff645b0994cb303d2303c2185']['spec']);m={'asset':'BTC','closes':[100+j*.2 for j in range(60)]};tests=[]
for cap in [.0225,.025,.0275,.03,.035,.04,.05]:
 sp=copy.deepcopy(spec);sp['parameters']['entry_volatility_ceiling']=cap;result=nm.base_decide(sp,m,40,0);sigma=nm.btc_entry_sigma(m['closes'],40,10);raw=1 if m['closes'][39]/m['closes'][10]-1>.03 else 0;assert result[0]==(0 if raw and sigma>cap else raw) and result[1]['entry_volatility_ceiling']==cap
 if cap not in [.0225,.0275]:assert om.base_decide(sp,m,40,0)==result
 tests.append({'cap':cap,'passed':True,'old_value_exact_equivalence':cap not in [.0225,.0275]})
put(R/'prebinding_cap_guard_verification.json',{'passed':True,'recorded_utc':now(),'old_source':rel(P/'engine.py'),'old_sha256':sha(P/'engine.py'),'new_source':rel(R/'engine.py'),'new_sha256':sha(R/'engine.py'),'exact_only_source_change':{'old':oldguard,'new':newguard},'formulas_and_full_AST_unchanged_after_validation_list_normalization':True,'simulate_and_money_core_bytes_unchanged':True,'synthetic_checks':tests,'before_first_reservation_or_market_calculation':True,'current_evaluation_failures':0})
previous=json.loads((ROOT/'.git/automation_proofs/20261115T115951Z.json').read_text());assert previous['status']=='completed_published_verified_unlocked' and previous['fresh_final_git_verification']['passed'];head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert head==subprocess.check_output(['git','rev-parse','origin/main'],text=True).strip()
put(R/'startup.json',{'round':R.name,'trigger_utc':'2026-11-15T14:00:53.520Z','base_commit':head,'branch_lock_broker_pid':2090003,'branch_lock_session':70123,'branch_lock_native_start_chunk':'efdab7','root_native_verification_chunk':'80f393','successful_fetch_start_chunk':'a720f1','successful_fetch_completion_chunk':'46c9ff','successful_fetch_session':81313,'successful_fetch_exit_code':0,'initial_sync_no_merge_required':True,'initial_tracked_and_index_clean':True,'only_preexisting_untracked':'data/normalized','previous_round_publication_verified':previous['status'],'previous_commit':previous['commit'],'previous_final_main_commit':previous['final_main_commit'],'last_actual_account_round':P.name,'previous_stale_lock_recovery_not_repeated':True,'peer_current_quote_commit_preserved':head,'old_blocked_failure_records_unchanged':True})
checked=[]
for f in R.rglob('*.py'):
 tree=ast.parse(f.read_text());assert not[n for n in ast.walk(tree) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id in ['ROOT','R','P']],str(f);checked.append(rel(f))
put(R/'path_join_guard.json',{'passed':True,'checked':checked,'Path_names_not_subscripted':True,'before_binding_and_evaluation':True,'no_model_or_account_calculations':True});print('PASS preregistered BTC cap2.25/2.5/2.75 neighborhood,2.5centerreadonly,7syntheticguardcases,0actualcalculations')
