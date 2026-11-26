"""Prepare actual public metadata and original account windows before any reservation."""
import ast,copy,gzip,hashlib,json,subprocess,urllib.parse
from datetime import datetime,timezone,timedelta
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;P=ROOT/'research/experiments/20261126T055257Z';M=ROOT/'research/experiments/20261123T173139Z'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rel=lambda p:str(p.relative_to(ROOT));rd=lambda p:json.loads(p.read_text());gz=lambda p:json.loads(gzip.decompress(p.read_bytes()));now=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z');put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
PID=rd(R/'startup.json')['branch_lock_broker_pid'];assert PID==1933718 and any('FLOCK' in l and str(PID) in l.split() for l in Path('/proc/locks').read_text().splitlines());assert not (R/'plan.json').exists() and not (R/'reserve_batches').exists()
assert rd(R/'context.json')['initial_16_missing_actual_results']==0
windows={};h=rd(P/'next_research_state.json')['UTC_midnight_handoff'];sources={}
for a in ['SMA','candidate','l4h02','fewm']:
 if a=='SMA':state=rd(P/'forward_state.json');start=state['last_completed_mark_utc'];daily=state['next_daily_decision_utc'];sources.update({rel(P/n):sha(P/n) for n in ['forward_state.json','forward_report.json']})
 else:
  pt=ROOT/'research/automation'/f'{a}_forward_latest.json';point=rd(pt);start=datetime.fromtimestamp(point['cutoff_ns']/1e9,timezone.utc).isoformat().replace('+00:00','Z');daily=h['next_daily_decision_by_account'][a]
  for k in ['state','report','delta','complete']:assert sha(ROOT/point[k])==point[k+'_sha256'];sources[point[k]]=point[k+'_sha256']
 cut=(datetime.fromisoformat(start.replace('Z','+00:00'))+timedelta(hours=2)).isoformat().replace('+00:00','Z');events=[];d=daily
 while d<=cut:
  if start<d:events.append(d)
  d=(datetime.fromisoformat(d.replace('Z','+00:00'))+timedelta(days=1)).isoformat().replace('+00:00','Z')
 windows[a]={'start_utc':start,'cutoff_utc':cut,'expected_daily_events_utc':events,'next_daily_decision_utc':d}
lo=min(z['start_utc'] for z in windows.values());end=(datetime.fromisoformat(max(z['cutoff_utc'] for z in windows.values()).replace('Z','+00:00'))+timedelta(minutes=1)).isoformat().replace('+00:00','Z');ms=lambda s:int(datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()*1000)
earliest_doc=rd(ROOT/h['actual_Nov23_08_source']);first_ms=min(int(z['fundingTime']) for xs in earliest_doc['public_fields_by_asset'].values() for z in xs);lo=datetime.fromtimestamp(min(ms(lo),first_ms-1)/1000,timezone.utc).isoformat().replace('+00:00','Z')
rawdir=R/'preflight_raw';rawdir.mkdir(exist_ok=True);attempts=[]
def get(name,url):
 for i in range(1,4):
  started=now();z=subprocess.run(['curl','--ipv4','--compressed','--http1.1','--tlsv1.2','--tls-max','1.2','--silent','--show-error','--connect-timeout','10','--max-time','30','--write-out','\n%{http_code}',url],cwd=ROOT,capture_output=True,timeout=65);body,code=z.stdout.rsplit(b'\n',1) if b'\n' in z.stdout else(z.stdout,b'000');dest=rawdir/f'{name}_{i}.gz';assert not dest.exists();dest.write_bytes(gzip.compress(body,mtime=0));item={'name':name,'url':url,'started_utc':started,'retrieved_utc':now(),'http_status':int(code),'curl_exit_code':z.returncode,'raw':rel(dest),'sha256':sha(dest),'raw_body_sha256':hashlib.sha256(body).hexdigest(),'bytes':len(body),'stderr':z.stderr.decode(errors='replace')};attempts.append(item);put(R/'preflight_transport_attempts.json',attempts)
  if z.returncode==0 and int(code)==200:return body,item
 raise RuntimeError('Public preflight failed three bounded attempts;no reservation or model/account execution')
response={}
for a in ['BTC','ETH']:
 url='https://fapi.binance.com/fapi/v1/fundingRate?'+urllib.parse.urlencode({'symbol':a+'USDT','startTime':ms(lo),'endTime':ms(end),'limit':1000});body,item=get(a+'_funding',url);response[a]=json.loads(body);assert isinstance(response[a],list) and len(response[a])<1000 and all(ms(lo)<int(z['fundingTime'])<=ms(end) and z['symbol']==a+'USDT' and 'markPrice' in z and 'fundingRate' in z for z in response[a])
put(R/'window_funding_preflight.json',{'recorded_utc':now(),'query_window_utc':[lo,end],'public_fields_by_asset':response,'all_pages_completed':True,'HTTP_receipts':[z for z in attempts if z['name'].endswith('_funding')],'purpose':'Fresh complete actual timestamps including all seven first actual settlement sources;cashflow booking separately restricted to each own current window,before reserve.'})
for a,w in windows.items():
 fr={s:[z for z in response[s] if ms(w['start_utc'])<int(z['fundingTime'])<=ms(w['cutoff_utc'])] for s in ['BTC','ETH']} if a!='SMA' else {'BTC':[],'ETH':[]};times=sorted({int(z['fundingTime']) for xs in fr.values() for z in xs});w.update(expected_funding_by_asset=fr,expected_funding_records=3*sum(map(len,fr.values())),expected_funding_utc=[datetime.fromtimestamp(t/1000,timezone.utc).isoformat().replace('+00:00','Z') for t in times])
accounts=['SMA','candidate','l4h02','fewm'];assert {a:windows[a]['expected_funding_records'] for a in accounts}=={'SMA':0,'candidate':0,'l4h02':0,'fewm':0} and all(not windows[a]['expected_daily_events_utc'] and windows[a]['next_daily_decision_utc']=='2026-11-26T00:01:00Z' for a in accounts)
windows.update(recorded_utc=now(),rules='Original SMA/C append closed marks Nov25_10:30..12:30;L4/FEWM12:10..14:10. Fresh actual query confirms funding0 for each own current window; all seven retained first funding sources already have6 unique keys per original perp account. Daily0all,nextNov26_00:01. Preserve all old6 settlements and olddaily once;no reset,transfer,rebalance,new research adoption,forcedclose,early or duplicate funding booking. Full77SPOT exact76prefix readonly; futureNov26dailyrequiresnewfull78/originalFloatadapter.')
put(R/'account_windows.json',windows)
priorcounts=rd(P/'account_window_verification.json')['full_chain_once_counts'];entries=h['next_window_known_actual_funding_sources'];assert len(entries)==7;proofs=[]
for entry in entries:
 origin=ROOT/entry['path'];doc=rd(origin);local=R/origin.name;assert not local.exists();local.write_bytes(origin.read_bytes());assert sha(local)==sha(origin)==entry['sha256'] and doc['recorded_utc']==entry['original_capture_utc'] and doc['public_fields_by_asset']==entry['actual_public_fields']
 times={str(int(z['fundingTime'])*1000000) for xs in doc['public_fields_by_asset'].values() for z in xs};dt=datetime.fromtimestamp(min(map(int,times))/1e9,timezone.utc);name=f'actual{dt.hour:02d}_nov{dt.day}_prebinding_source.json'
 old=P/name
 if old.exists():
  previous=rd(old);assert previous['sha256']==sha(origin) and previous['first_capture_utc']==doc['recorded_utc']
 for asset,fields in doc['public_fields_by_asset'].items():
  ids={int(z['fundingTime']) for z in fields};assert [z for z in response[asset] if int(z['fundingTime']) in ids]==fields
 for item in doc['HTTP_receipts']:
  assert sha(ROOT/item['raw'])==item['sha256'];sources[item['raw']]=item['sha256']
  if item['http_status']==200 and not item['curl_exit_code']:
   rows=gz(ROOT/item['raw'])
   for asset,fields in doc['public_fields_by_asset'].items():
    if 'symbol='+asset+'USDT' in item['url']:assert all(z in rows for z in fields)
 pc={a:{t:priorcounts[a]['funding'].get(t,0) for t in times} for a in ['candidate','l4h02','fewm']};inc={a:{t:sum(3 for xs in windows[a]['expected_funding_by_asset'].values() for z in xs if str(int(z['fundingTime'])*1000000)==t) for t in times} for a in pc};maximum={t:sum(3 for xs in doc['public_fields_by_asset'].values() for z in xs if str(int(z['fundingTime'])*1000000)==t) for t in times};assert pc==entry['current_own_booked_counts']
 for a in pc:
  for t in times:assert pc[a][t] in [0,maximum[t]] and inc[a][t] in [0,maximum[t]] and pc[a][t]+inc[a][t]<=maximum[t]
 proof=R/name;assert not proof.exists();put(proof,{'passed':True,'recorded_utc':now(),'source':rel(local),'sha256':sha(local),'original_source':rel(origin),'first_capture_utc':doc['recorded_utc'],'actual_public_fields':doc['public_fields_by_asset'],'prior_unique_counts':pc,'expected_current_increment_counts':inc,'maximum_once_counts_by_timestamp':maximum,'fresh_exact_source_fields_equal':True,'original_successful_HTTP_raw_bytes_verified':True,'before_any_current_reservation':True,'cashflow_calculations':0,'own_signed_q_and_cost_required_no_cashflow_copy':True});sources.update({rel(proof):sha(proof),rel(local):sha(local),rel(origin):sha(origin)});proofs.append({'key':f'Nov{dt.day}_{dt.hour:02d}','path':rel(proof),'sha256':sha(proof)})
allproof=R/'all_actual_funding_prebinding.json';put(allproof,{'passed':True,'sources':proofs,'source_count':len(proofs),'before_any_current_reservation':True,'current_expected_records_by_account':{a:windows[a]['expected_funding_records'] for a in accounts},'cashflow_calculations':0});sources[rel(allproof)]=sha(allproof)
contract=rd(P/'next_research_state.json')['next_SMA_rebinding_contract'];path77=ROOT/contract['full77_authority'];path76=ROOT/contract['old_full76_prefix_authority'];assert sha(path77)==contract['full77_sha256']=='009a199f6af91db9e61ed64f087fc5adb7992e50e14837e08554d1d4454f798a' and sha(path76)==contract['old_full76_sha256']=='7ef4aae3704627ef124e052643062e1635bf837aef9ae0c14371b86dda326b5e';daily=gz(path77);older=gz(path76);assert all(len(daily[a]['1d'])==77 and daily[a]['1d'][:76]==older[a]['1d'] for a in ['BTC','ETH']);proof=R/'SMA_full77_prebinding.json';put(proof,{'passed':True,'recorded_utc':now(),'authority':rel(path77),'sha256':sha(path77),'full76_authority':rel(path76),'full76_sha256':sha(path76),'real_SPOT_daily_context':77,'full77_exact_original76_prefix':True,'current_original_daily_event_count':0,'no_new_SPOT_daily_capture':True,'before_any_current_reservation':True});sources.update({rel(path77):sha(path77),rel(path76):sha(path76),rel(proof):sha(proof)})
template=P/'forward.py';expected=template.read_text();assert (R/'forward.py').read_text()==expected;identity=R/'SMA_markonly_kernel_identity.json';put(identity,{'passed':True,'recorded_utc':now(),'template':rel(template),'template_sha256':sha(template),'source':rel(R/'forward.py'),'source_sha256':sha(R/'forward.py'),'exact_template_except_full77_guard_and_completed_daily_date_prose':True,'original_Float_financial_arithmetic_unchanged':True,'before_any_current_reservation':True});sources.update({rel(template):sha(template),rel(identity):sha(identity)})
for a in ['candidate','l4h02','fewm']:
 point=rd(ROOT/'research/automation'/f'{a}_forward_latest.json');state=rd(ROOT/point['state']);actual={asset:{k:z['signed_units'] for k,z in books.items()} for asset,books in state['books'].items()};assert actual==h['current_original_signed_units_by_asset_cost'][a] and priorcounts[a]['daily']['1795564860000000000']==6
for name in ['research/experiments/20261011T014626Z/forward.py','research/experiments/20261001T113625Z/signals.py','research/experiments/20261001T013355Z/evaluate.py','research/experiments/20261125T174746Z/forward_registry.py','research/experiments/20261125T174746Z/audit_forward.py']:sources[name]=sha(ROOT/name)
lp=copy.deepcopy(rd(P/'l4h02_resume_plan.json'));pt=ROOT/'research/automation/l4h02_forward_latest.json';lp.update(frozen_at_utc=now(),recorded_utc=now(),round=R.name,previous_pointer=rd(pt),previous_pointer_sha256=sha(pt),cutoff_utc=windows['l4h02']['cutoff_utc'],cutoff_ns=ms(windows['l4h02']['cutoff_utc'])*1000000,branch_lock_broker_pid=PID,rules=windows['rules']);put(R/'l4h02_resume_plan.json',lp);sources.update(lp['source_sha256'])
for name in ['research/experiments/20261104T201939Z/prospective_fewm','research/experiments/20261026T110637Z']:
 for q in (ROOT/name).glob('*.py'):sources[rel(q)]=sha(q)
for name in ['binding.json','plan.json']:
 q=ROOT/'research/experiments/20261104T201939Z/prospective_fewm'/name;sources[rel(q)]=sha(q)
oldhours=P/'l4h02_observation/input_manifest.json';sources[rel(oldhours)]=sha(oldhours)
for z in rd(oldhours)['provenance']:
 if '/fapi/v1/markPriceKlines?' in z['url']:assert sha(ROOT/z['raw'])==z['sha256'];sources[z['raw']]=z['sha256']
body,item=get('official_market_py','https://raw.githubusercontent.com/binance/binance-futures-connector-python/main/binance/um_futures/market.py');assert b'def funding_rate' in body and b'/fapi/v1/fundingRate' in body;put(R/'primary_source_access.json',{'recorded_utc':now(),'browser_reads':[{'url':'https://raw.githubusercontent.com/binance/binance-futures-connector-python/main/binance/um_futures/market.py','reference':'turn438view0','purpose':'Official publicGET implementation read only,not executed'}],'official_SDK_code':item,'source_code_version_sha256':hashlib.sha256(body).hexdigest(),'downloaded_code_not_executed':True})
put(R/'original_accounts_binding.json',{'recorded_utc':now(),'sources_sha256':sources,'source_pointers_before':{a:rd(ROOT/'research/automation'/f'{a}_forward_latest.json') for a in ['candidate','l4h02','fewm']},'SMA_current_mark_only_adapter':rel(R/'forward.py'),'SMA_current_full_daily_context':77,'all4windows_predeclared_before_reserve':True,'immutable_financial_kernels_unchanged':True,'no_financial_or_account_calculation_yet':True});print(json.dumps({'prepared':True,'windows':{a:[windows[a]['start_utc'],windows[a]['cutoff_utc']] for a in accounts},'current_funding_counts':{a:windows[a]['expected_funding_records'] for a in accounts},'current_daily_counts':0,'SMA_full77_readonly_exact76prefix':True,'evaluations':0}),flush=True)
