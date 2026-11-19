"""Prepare independent saved-bank combinations and four original frozen windows with actual funding coverage."""
import ast,copy,gzip,hashlib,json,subprocess,sys,urllib.parse
from datetime import datetime,timezone,timedelta
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
P=ROOT/'research/experiments/20261119T183629Z';MARK=P
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rel=lambda p:str(p.relative_to(ROOT))
now=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
rd=lambda p:json.loads(p.read_text())
def put(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def gz(p):return json.loads(gzip.decompress(p.read_bytes()))
PID=rd(R/'startup.json')['branch_lock_broker_pid'];assert PID==3711429
assert any('FLOCK' in l and str(PID) in l.split() for l in Path('/proc/locks').read_text().splitlines())
assert not (R/'plan.json').exists() and not (R/'account_windows.json').exists()
sources={rel(P/n):sha(P/n) for n in ['common.py', 'engine.py', 'core391_tail_safe.py', 'market.py', 'recent.py', 'portfolio.py', 'run.py', 'audit.py', 'audit_native.py', 'audit_helpers_complete.py', 'audit_incremental.py', 'audit_l4h02.py', 'audit_candidate.py', 'audit_fewm.py', 'project_l4h02_batch.py', 'project_candidate_batch.py', 'project_fewm_batch.py', 'parent_units.py', 'exports.py', 'observe_l4h02.py', 'observe_fewm.py', 'observe_candidate.py', 'journal.py', 'forward.py', 'forward_registry.py', 'audit_forward.py', 'commands.py', 'checks.py', 'collect.py', 'finalize.py', 'publish.py', 'definitions.py', 'freeze_confirmation.py', 'sizing_units.py']}
assert sha(R/'engine.py')==sha(P/'engine.py') and sha(R/'core391_tail_safe.py')==sha(P/'core391_tail_safe.py')
put(R/'template_sources.json',{'recorded_utc':now(),'source_SHA256':sources,'frozen_engine_and_native_accounting_bytes_exact':True,'SMA_mark_only_template':'research/experiments/20261119T123454Z/forward.py','SMA_original_daily_kernel_not_called_this_window':True,'transport_change_only':'No transport change;reuse verifiedTLSminimum1.2/HTTP1.1/bounded3publicGETattempts and unchanged observer kernels/registration.'})
for f in P.glob('funding*_nov*_preflight.json'):(R/f.name).write_bytes(f.read_bytes())
put(R/'immutable_settlement_sources.json',{'passed':True,'copied_without_relabeling_capture_UTC':{rel(R/f.name):{'prior_path':rel(f),'sha256':sha(f)} for f in P.glob('funding*_nov*_preflight.json')},'no_cashflows_reused':True})
previous=rd(P/'next_research_state.json')['UTC_midnight_handoff'];qlo=min(previous['next_SMA_single_window_utc'][0],previous['next_L4_FEWM_window_utc'][0]);qend=(datetime.fromisoformat(max(previous['next_SMA_single_window_utc'][1],previous['next_L4_FEWM_window_utc'][1]).replace('Z','+00:00'))+timedelta(minutes=1)).isoformat().replace('+00:00','Z');qstartms=int(datetime.fromisoformat(qlo.replace('Z','+00:00')).timestamp()*1000);qendms=int(datetime.fromisoformat(qend.replace('Z','+00:00')).timestamp()*1000)
if not (R/'window_funding_preflight.json').exists():
 attempts=[];responses={};rawdir=R/'window_funding_responses';rawdir.mkdir(exist_ok=True)
 for asset in ['BTC','ETH']:
  params={'symbol':asset+'USDT','startTime':qstartms,'endTime':qendms,'limit':1000};url='https://fapi.binance.com/fapi/v1/fundingRate?'+urllib.parse.urlencode(params)
  for attempt in range(1,4):
   started=now();z=subprocess.run(['curl','--ipv4','--compressed','--http1.1','--tlsv1.2','--silent','--show-error','--connect-timeout','10','--max-time','30','--write-out','\n%{http_code}',url],cwd=ROOT,capture_output=True,timeout=65)
   body,code=z.stdout.rsplit(b'\n',1) if b'\n' in z.stdout else (z.stdout,b'000');f=rawdir/(asset+'_'+str(attempt)+'.json.gz');f.write_bytes(gzip.compress(body,mtime=0));item={'asset':asset,'url':url,'started_utc':started,'finished_utc':now(),'http_status':int(code),'curl_exit_code':z.returncode,'raw':rel(f),'sha256':sha(f),'raw_body_sha256':hashlib.sha256(body).hexdigest(),'bytes':len(body),'stderr':z.stderr.decode(errors='replace')};attempts.append(item);put(R/'window_funding_preflight_attempts.json',attempts)
   if z.returncode==0 and int(code)==200:responses[asset]=json.loads(body);break
  else:raise RuntimeError('Public funding preflight failed; no reserve or model/account calculation has occurred')
  assert isinstance(responses[asset],list) and len(responses[asset])<1000
 assert all(isinstance(xs,list) for xs in responses.values())
 assert all(qstartms<int(z['fundingTime'])<=qendms and 'fundingRate' in z and 'markPrice' in z for xs in responses.values() for z in xs),responses
 fresh={'recorded_utc':now(),'public_fields_by_asset':responses,'query_window_utc':[qlo,qend],'all_pages_completed':True,'HTTP_receipts':attempts,'purpose':'Fresh complete actual settlement lookup before reserve; no nominal funding schedule assumed.'};put(R/'window_funding_preflight.json',fresh);assert sha(R/'funding08_nov17_preflight.json')==sha(P/'funding08_nov17_preflight.json')
else:
 fresh=rd(R/'window_funding_preflight.json');responses=fresh['public_fields_by_asset'];attempts=fresh['HTTP_receipts']
 assert fresh['query_window_utc']==[qlo,qend] and fresh['all_pages_completed']
 for z in attempts:
  assert z['http_status']==200 and z['curl_exit_code']==0 and sha(ROOT/z['raw'])==z['sha256']
  assert hashlib.sha256(gzip.decompress((ROOT/z['raw']).read_bytes())).hexdigest()==z['raw_body_sha256']
 assert all(qstartms<int(z['fundingTime'])<=qendms for xs in responses.values() for z in xs)
first00=R/'funding00_nov19_preflight.json';assert first00.exists() and sha(first00)==sha(P/first00.name)
original00=rd(first00);assert original00['recorded_utc']==previous['original_Nov19_00_capture_utc']
covered00={a:[z for z in original00['public_fields_by_asset'][a] if qstartms<int(z['fundingTime'])<=qendms] for a in ['BTC','ETH']}
for a in ['BTC','ETH']:
 known={int(z['fundingTime']) for z in original00['public_fields_by_asset'][a]};assert [z for z in responses[a] if int(z['fundingTime']) in known]==covered00[a]
first08=R/'funding08_nov19_preflight.json'
actual08={a:list(responses[a]) for a in ['BTC','ETH']} # Exact returned milliseconds,including08:00:00.002;never substitute nominal schedule.
if not first08.exists():
 assert all(len(v)==1 for v in actual08.values()),actual08
 put(first08,{**fresh,'public_fields_by_asset':actual08,'purpose':'Original first observed actualNov19_08 source;preserve this UTC/bytes before ANY current reservation;no cashflows calculated.'})
source08=rd(first08)
for a in ['BTC','ETH']:
 covered=[z for z in source08['public_fields_by_asset'][a] if qstartms<int(z['fundingTime'])<=qendms]
 assert [z for z in responses[a] if int(z['fundingTime']) in {int(v['fundingTime']) for v in source08['public_fields_by_asset'][a]}]==covered
put(R/'actual08_nov19_prebinding_source.json',{'passed':True,'source':rel(first08),'sha256':sha(first08),'first_capture_utc':source08['recorded_utc'],'fresh_current_query_utc':fresh['recorded_utc'],'actual_public_fields':source08['public_fields_by_asset'],'recorded_before_any_current_reservation':True,'original_first_source_retained_without_relabeling':True,'cashflow_calculations':0})
put(R/'actual00_nov19_prebinding_source.json',{'passed':True,'source':rel(first00),'sha256':sha(first00),'first_capture_utc':original00['recorded_utc'],'fresh_current_query_utc':fresh['recorded_utc'],'actual_public_fields':original00['public_fields_by_asset'],'current_covered_original_fields':covered00,'query_window_utc':fresh['query_window_utc'],'recorded_before_any_current_reservation':True,'first_source_copied_without_relabeling':True,'cashflow_calculations':0})

put(R/'new_actual_settlement_preflight.json',{**fresh,'fresh_complete_window_query':True,'original_first_source_retained':True,'no_cashflow_calculation_yet':True});assert sha(R/'funding00_nov18_preflight.json')==sha(P/'funding00_nov18_preflight.json')
assert sha(R/'funding08_nov18_preflight.json')==sha(P/'funding08_nov18_preflight.json');assert rd(R/'funding08_nov18_preflight.json')['recorded_utc']==previous['original_Nov18_08_capture_utc']
known08=rd(R/'funding08_nov18_preflight.json')['public_fields_by_asset']
for asset in ['BTC','ETH']:
 known={int(x['fundingTime']):x for x in known08[asset]};covered=[x for x in known08[asset] if qstartms<=int(x['fundingTime'])<=qendms];observed=[x for x in responses[asset] if int(x['fundingTime']) in known];assert observed==covered

first16=R/'funding16_nov18_preflight.json';assert first16.exists() and sha(first16)==sha(P/first16.name)
known16=rd(first16);assert known16['recorded_utc']==previous['original_Nov18_16_capture_utc']
covered16={a:[z for z in known16['public_fields_by_asset'][a] if qstartms<=int(z['fundingTime'])<=qendms] for a in ['BTC','ETH']}
for a in ['BTC','ETH']:
 known_times={int(z['fundingTime']) for z in known16['public_fields_by_asset'][a]};observed=[z for z in responses[a] if int(z['fundingTime']) in known_times];assert observed==covered16[a]
put(R/'actual16_prebinding_source.json',{'passed':True,'source':rel(first16),'sha256':sha(first16),'first_capture_utc':known16['recorded_utc'],'fresh_current_query_utc':fresh['recorded_utc'],'original_known16_public_fields':known16['public_fields_by_asset'],'current_query_covered_known16_fields':covered16,'current_query_includes_known16':any(covered16.values()),'first_source_copied_without_relabeling':True,'before_any_current_reserve':True,'cashflow_calculations':0})
previous=rd(P/'next_research_state.json')['UTC_midnight_handoff'];windows={}
for a in ['SMA','candidate','l4h02','fewm']:
 if a=='SMA':start=rd(P/'forward_state.json')['last_completed_mark_utc'];daily=rd(P/'forward_state.json')['next_daily_decision_utc']
 else:
  point=rd(ROOT/('research/automation/'+a+'_forward_latest.json'));state=rd(ROOT/point['state']);start=datetime.fromtimestamp(point['cutoff_ns']/1e9,timezone.utc).isoformat().replace('+00:00','Z');daily=previous['next_daily_decision_by_account'][a]
 cut=(datetime.fromisoformat(start.replace('Z','+00:00'))+timedelta(hours=2)).isoformat().replace('+00:00','Z')
 assert start==previous['next_SMA_single_window_utc' if a in ['SMA','candidate'] else 'next_L4_FEWM_window_utc'][0]
 events=[];d=daily
 while d<=cut:
  if start<d:events.append(d)
  d=(datetime.fromisoformat(d.replace('Z','+00:00'))+timedelta(days=1)).isoformat().replace('+00:00','Z')
 nextdaily=d
 startms=int(datetime.fromisoformat(start.replace('Z','+00:00')).timestamp()*1000);cutms=int(datetime.fromisoformat(cut.replace('Z','+00:00')).timestamp()*1000);fr={s:[z for z in responses[s] if startms<int(z['fundingTime'])<=cutms] for s in ['BTC','ETH']} if a!='SMA' else {'BTC':[],'ETH':[]};times=sorted({int(z['fundingTime']) for xs in fr.values() for z in xs});windows[a]={'start_utc':start,'cutoff_utc':cut,'expected_daily_events_utc':events,'expected_funding_utc':[datetime.fromtimestamp(t/1000,timezone.utc).isoformat().replace('+00:00','Z') for t in times],'expected_funding_by_asset':fr,'expected_funding_records':3*sum(map(len,fr.values())),'next_daily_decision_utc':nextdaily}
windows.update(recorded_utc=now(),rules='All4currentwindowshavezeroNov20dailydecisions;deriveeachactualfundingeventfromcompletepubliclookup;all3perpsNov19fundingandall4dailyalreadybookedonce;exactownstart/cutoffanddaily/fundingeventsaredeclaredinthisdocument. Freshcompleteactualfundinglookup,bookonlyown(start,cutoff],neverrepeatNov18_00or00:01. Preserveeachq/desired/entry/costsandfullNAV;bookonlynewactualownfundingcash;candidateETHalreadyclosedNov19_00:01;full71SPOTauthorityexact70prefix_readonly. No researchsizing/risk-rule adoption;all3perpsalreadybookedknown16once,queryallcurrentwindowsforactualspecialevents.')
put(R/'account_windows.json',windows)
lp=copy.deepcopy(rd(P/'l4h02_resume_plan.json'));point=ROOT/'research/automation/l4h02_forward_latest.json';lp.update(frozen_at_utc=now(),recorded_utc=now(),round=R.name,previous_pointer=rd(point),previous_pointer_sha256=sha(point),cutoff_utc=windows['l4h02']['cutoff_utc'],cutoff_ns=int(datetime.fromisoformat(windows['l4h02']['cutoff_utc'].replace('Z','+00:00')).timestamp()*1e9),branch_lock_broker_pid=PID,rules=windows['rules']);put(R/'l4h02_resume_plan.json',lp)
for path,h in lp['source_sha256'].items():assert sha(ROOT/path)==h,path
authorities={}
for n in [66,67,68,69,70]:
 path=ROOT/previous[f'SMA_full{n}_authority'];data=gz(path);assert sha(path)==previous[f'SMA_full{n}_sha256'] and all(len(data[a]['1d'])==n for a in ['BTC','ETH']);authorities[str(n)]={'path':rel(path),'sha256':sha(path),'days':n}
for high,low in [(70,69),(69,68),(68,67),(67,66)]:
 a=gz(ROOT/authorities[str(high)]['path']);b=gz(ROOT/authorities[str(low)]['path']);assert all(a[s]['1d'][:low]==b[s]['1d'] for s in ['BTC','ETH'])
old65=gz(ROOT/'research/experiments/20261113T033939Z/forward_inputs.json.gz');d66=gz(ROOT/authorities['66']['path']);assert all(d66[a]['1d'][:65]==old65[a]['1d'] for a in ['BTC','ETH'])
path=ROOT/previous['SMA_full71_authority'];assert sha(path)==previous['SMA_full71_sha256'];data71=gz(path);assert all(len(data71[a]['1d'])==71 and data71[a]['1d'][:70]==gz(ROOT/authorities['70']['path'])[a]['1d'] for a in ['BTC','ETH']);authorities['71']={'path':rel(path),'sha256':sha(path),'days':71}
put(R/'SMA_background_authorities.json',{'passed':True,'authorities':authorities,'full71_to_original65_prefix_exact':True,'current_SMA_window_requires_zero_daily_decisions':True,'all4_original_Nov19_daily_already_booked':True,'complete71_authority_readonly_reused':True,'current_minute_packet_is_not_daily_authority':True})
names2=['funding08_nov19_preflight.json','actual08_nov19_prebinding_source.json','observe_l4h02.py','observe_fewm.py','observe_candidate.py','forward.py','forward_registry.py','audit_incremental.py','audit_l4h02.py','audit_fewm.py','audit_candidate.py','audit_forward.py','window_funding_preflight.json','immutable_settlement_sources.json','SMA_background_authorities.json','new_actual_settlement_preflight.json','funding08_nov18_preflight.json','funding00_nov19_preflight.json','actual00_nov19_prebinding_source.json']+(['funding16_nov18_preflight.json','actual16_prebinding_source.json'] if (R/'actual16_prebinding_source.json').exists() else [])
binding={rel(R/n):sha(R/n) for n in names2};binding.update(lp['source_sha256']);binding.update({z['path']:z['sha256'] for z in authorities.values()})
put(R/'original_accounts_binding.json',{'recorded_utc':now(),'sources_sha256':binding,'original_kernels_unchanged':True,'frozen_before_current_account_calculation':True,'SMA_current_mark_only_adapter':rel(R/'forward.py'),'SMA_full71_authority':authorities['71'],'all4windows_predeclared_before_reserve':True})
put(R/'read_failures.json',{'facts':rd(R/'read_failures.json')['facts']+[{**z,'resolved':True,'reason':'Later bounded publicGET succeeded before any reserve/calculation'} for z in attempts if z['curl_exit_code'] or z['http_status']!=200]})
put(R/'implementation_plan.json',{'frozen_utc':now(),**rd(R/'research_design.json')})
assert all(not windows[a]['expected_daily_events_utc'] for a in ['SMA','candidate','l4h02','fewm'])
print(json.dumps({'prepared':True,'financial_calculations':0,'account_calculations':0,'funding_by_asset':responses,'windows':{a:[windows[a]['start_utc'],windows[a]['cutoff_utc']] for a in ['SMA','candidate','l4h02','fewm']},'full69authority':authorities['69']}),flush=True)
