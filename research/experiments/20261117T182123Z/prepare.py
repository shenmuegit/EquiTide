"""Prepare one frozen slope-hurdle batch and four original mark-only windows."""
import ast,copy,gzip,hashlib,json,subprocess,sys,urllib.parse
from datetime import datetime,timezone,timedelta
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
P=ROOT/'research/experiments/20261117T162156Z';MARK=P
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rel=lambda p:str(p.relative_to(ROOT))
now=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
rd=lambda p:json.loads(p.read_text())
def put(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def gz(p):return json.loads(gzip.decompress(p.read_bytes()))
PID=rd(R/'startup.json')['branch_lock_broker_pid'];assert PID==2931227
assert any('FLOCK' in l and str(PID) in l.split() for l in Path('/proc/locks').read_text().splitlines())
assert not (R/'plan.json').exists() and not (R/'account_windows.json').exists()
sources={rel(P/n):sha(P/n) for n in ['common.py', 'engine.py', 'core391_tail_safe.py', 'market.py', 'recent.py', 'portfolio.py', 'run.py', 'audit.py', 'audit_native.py', 'audit_helpers_complete.py', 'audit_incremental.py', 'audit_l4h02.py', 'audit_candidate.py', 'audit_fewm.py', 'project_l4h02_batch.py', 'project_candidate_batch.py', 'project_fewm_batch.py', 'parent_units.py', 'exports.py', 'observe_l4h02.py', 'observe_fewm.py', 'observe_candidate.py', 'journal.py', 'forward.py', 'forward_registry.py', 'audit_forward.py', 'commands.py', 'checks.py', 'collect.py', 'finalize.py', 'publish.py', 'definitions.py', 'freeze_confirmation.py', 'units_funding_ratio.py']}
assert sha(R/'engine.py')==sha(P/'engine.py') and sha(R/'core391_tail_safe.py')==sha(P/'core391_tail_safe.py')
put(R/'template_sources.json',{'recorded_utc':now(),'source_SHA256':sources,'frozen_engine_and_native_accounting_bytes_exact':True,'SMA_mark_only_template':rel(MARK/'forward.py'),'SMA_original_daily_kernel_not_called_this_window':True,'transport_change_only':'Remove TLS maximum1.2; retain certificate verification/minimum1.2/HTTP1.1/bounded3 publicGET attempts. No observer kernel/state/registration change.'})
for f in P.glob('funding*_nov*_preflight.json'):(R/f.name).write_bytes(f.read_bytes())
put(R/'immutable_settlement_sources.json',{'passed':True,'copied_without_relabeling_capture_UTC':{rel(R/f.name):{'prior_path':rel(f),'sha256':sha(f)} for f in P.glob('funding*_nov*_preflight.json')},'no_cashflows_reused':True})
attempts=[];responses={};rawdir=R/'window_funding_responses';rawdir.mkdir()
for asset in ['BTC','ETH']:
 params={'symbol':asset+'USDT','startTime':1794904200000,'endTime':1794917460000,'limit':1000};url='https://fapi.binance.com/fapi/v1/fundingRate?'+urllib.parse.urlencode(params)
 for attempt in range(1,4):
  started=now();z=subprocess.run(['curl','--ipv4','--compressed','--http1.1','--tlsv1.2','--silent','--show-error','--connect-timeout','10','--max-time','30','--write-out','\n%{http_code}',url],cwd=ROOT,capture_output=True,timeout=65)
  body,code=z.stdout.rsplit(b'\n',1) if b'\n' in z.stdout else (z.stdout,b'000');f=rawdir/(asset+'_'+str(attempt)+'.json.gz');f.write_bytes(gzip.compress(body,mtime=0));item={'asset':asset,'url':url,'started_utc':started,'finished_utc':now(),'http_status':int(code),'curl_exit_code':z.returncode,'raw':rel(f),'sha256':sha(f),'raw_body_sha256':hashlib.sha256(body).hexdigest(),'bytes':len(body),'stderr':z.stderr.decode(errors='replace')};attempts.append(item);put(R/'window_funding_preflight_attempts.json',attempts)
  if z.returncode==0 and int(code)==200:responses[asset]=json.loads(body);break
 else:raise RuntimeError('Public funding preflight failed; no reserve or model/account calculation has occurred')
 assert isinstance(responses[asset],list) and len(responses[asset])<1000
assert responses=={'BTC':[],'ETH':[]},responses
assert all(1794904200000<int(z['fundingTime'])<=1794917460000 and 'fundingRate' in z and 'markPrice' in z for xs in responses.values() for z in xs),responses
fresh={'recorded_utc':now(),'public_fields_by_asset':responses,'query_window_utc':['2026-11-17T08:30:00Z','2026-11-17T12:11:00Z'],'all_pages_completed':True,'HTTP_receipts':attempts,'purpose':'Fresh complete actual settlement lookup before reserve; no nominal funding schedule assumed.'};put(R/'window_funding_preflight.json',fresh);assert sha(R/'funding08_nov17_preflight.json')==sha(P/'funding08_nov17_preflight.json')
previous=rd(P/'next_research_state.json')['UTC_midnight_handoff'];windows={}
for a in ['SMA','candidate','l4h02','fewm']:
 if a=='SMA':start=rd(P/'forward_state.json')['last_completed_mark_utc'];daily=rd(P/'forward_state.json')['next_daily_decision_utc']
 else:
  point=rd(ROOT/('research/automation/'+a+'_forward_latest.json'));state=rd(ROOT/point['state']);start=datetime.fromtimestamp(point['cutoff_ns']/1e9,timezone.utc).isoformat().replace('+00:00','Z');daily='2026-11-18T00:01:00Z'
 cut=(datetime.fromisoformat(start.replace('Z','+00:00'))+timedelta(hours=2)).isoformat().replace('+00:00','Z')
 assert start==previous['next_SMA_single_window_utc' if a in ['SMA','candidate'] else 'next_L4_FEWM_window_utc'][0] and cut<daily
 startms=int(datetime.fromisoformat(start.replace('Z','+00:00')).timestamp()*1000);cutms=int(datetime.fromisoformat(cut.replace('Z','+00:00')).timestamp()*1000);fr={s:[z for z in responses[s] if startms<int(z['fundingTime'])<=cutms] for s in ['BTC','ETH']} if a!='SMA' else {'BTC':[],'ETH':[]};times=sorted({int(z['fundingTime']) for xs in fr.values() for z in xs});windows[a]={'start_utc':start,'cutoff_utc':cut,'expected_daily_events_utc':[],'expected_funding_utc':[datetime.fromtimestamp(t/1000,timezone.utc).isoformat().replace('+00:00','Z') for t in times],'expected_funding_by_asset':fr,'expected_funding_records':3*sum(map(len,fr.values())),'next_daily_decision_utc':daily}
windows.update(recorded_utc=now(),rules='SMA/single08:30to10:30;L4/FEWM10:10to12:10. Freshcompleteactualfundinglookup hasnoevents;all3perpsalreadybooked08once,neverrepeat. Zero newdailydecisions/fills;preserve each owncash/q/desired/costs andfullNAVprefix,allnextdailyNov18_00:01,SMAfull69authorityunchanged,no newresearchVW adoption.')
put(R/'account_windows.json',windows)
lp=copy.deepcopy(rd(P/'l4h02_resume_plan.json'));point=ROOT/'research/automation/l4h02_forward_latest.json';lp.update(frozen_at_utc=now(),recorded_utc=now(),round=R.name,previous_pointer=rd(point),previous_pointer_sha256=sha(point),cutoff_utc=windows['l4h02']['cutoff_utc'],cutoff_ns=int(datetime.fromisoformat(windows['l4h02']['cutoff_utc'].replace('Z','+00:00')).timestamp()*1e9),branch_lock_broker_pid=PID,rules=windows['rules']);put(R/'l4h02_resume_plan.json',lp)
for path,h in lp['source_sha256'].items():assert sha(ROOT/path)==h,path
authorities={}
for n in [66,67,68,69]:
 path=ROOT/previous[f'SMA_full{n}_authority'];data=gz(path);assert sha(path)==previous[f'SMA_full{n}_sha256'] and all(len(data[a]['1d'])==n for a in ['BTC','ETH']);authorities[str(n)]={'path':rel(path),'sha256':sha(path),'days':n}
for high,low in [(69,68),(68,67),(67,66)]:
 a=gz(ROOT/authorities[str(high)]['path']);b=gz(ROOT/authorities[str(low)]['path']);assert all(a[s]['1d'][:low]==b[s]['1d'] for s in ['BTC','ETH'])
old65=gz(ROOT/'research/experiments/20261113T033939Z/forward_inputs.json.gz');d66=gz(ROOT/authorities['66']['path']);assert all(d66[a]['1d'][:65]==old65[a]['1d'] for a in ['BTC','ETH'])
put(R/'SMA_background_authorities.json',{'passed':True,'authorities':authorities,'full69_to_original65_prefix_exact':True,'current_window_requires_zero_daily_decisions':True,'do_not_treat_current_minute_only_input_as_daily_authority':True})
names2=['observe_l4h02.py','observe_fewm.py','observe_candidate.py','forward.py','forward_registry.py','audit_incremental.py','audit_l4h02.py','audit_fewm.py','audit_candidate.py','audit_forward.py','window_funding_preflight.json','immutable_settlement_sources.json','SMA_background_authorities.json']
binding={rel(R/n):sha(R/n) for n in names2};binding.update(lp['source_sha256']);binding.update({z['path']:z['sha256'] for z in authorities.values()})
put(R/'original_accounts_binding.json',{'recorded_utc':now(),'sources_sha256':binding,'original_kernels_unchanged':True,'frozen_before_current_account_calculation':True,'SMA_current_mark_only_adapter':rel(R/'forward.py'),'SMA_full69_authority':authorities['69'],'all4windows_predeclared_before_reserve':True})
put(R/'read_failures.json',{'facts':[{**z,'resolved':True,'reason':'Later bounded publicGET succeeded before any reserve/calculation'} for z in attempts if z['curl_exit_code'] or z['http_status']!=200]})
put(R/'implementation_plan.json',{'frozen_utc':now(),'hypothesis':'VW7/VW9 faster/slower completed sample logvol may adapt the carry budget to changing risk; oldVW8readonly. FixedR.0075/M4/entryriskV6cap.05625/fastROC/finiteEWM/native money. RepresentativeVW7/BTCH.03 setbeforeoutcomes.','axes':{'ETH_FUNDING_BUDGET_WINDOW':[7,8,9],'BTC_MAIN_ENTRY_H':[.03,.0325]},'new_ETH_budget_windows':[7,9],'readonly_ETH_budget_window':8,'new_configs':6,'representative':{'ETH_budget_window':7,'BTC_H':.03},'stages':['freeze specs and gates','synthetic budget/cause/equality checks','bind sources/data','reserve6','actual391d evaluateonce','independent fullpolicy/money/cost/fund/risk/NAV/fold audits','full exports','finish6','continue4originalaccounts afterindividualreserve','fullaccountchainaudit','appendonlyjournal','registry/readonlymonitorchecks','collect/seal/commit/pushmain','fullremoteevidenceverify','nativeunlock/postreleaseverify'],'no_subagents':True,'no_real_orders':True,'no_new_paper10_trades':True})
print(json.dumps({'prepared':True,'financial_calculations':0,'account_calculations':0,'funding_by_asset':responses,'windows':{a:[windows[a]['start_utc'],windows[a]['cutoff_utc']] for a in ['SMA','candidate','l4h02','fewm']},'full69authority':authorities['69']}),flush=True)
