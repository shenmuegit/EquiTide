"""Prepare actual public metadata and original account windows before any reservation."""
import ast,copy,gzip,hashlib,json,subprocess,urllib.parse
from datetime import datetime,timezone,timedelta
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;P=ROOT/'research/experiments/20261123T233413Z';M=ROOT/'research/experiments/20261123T173139Z'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rel=lambda p:str(p.relative_to(ROOT));rd=lambda p:json.loads(p.read_text());gz=lambda p:json.loads(gzip.decompress(p.read_bytes()));now=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z');put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
PID=rd(R/'startup.json')['branch_lock_broker_pid'];assert PID==1097428 and any('FLOCK' in l and str(PID) in l.split() for l in Path('/proc/locks').read_text().splitlines());assert not (R/'plan.json').exists() and not (R/'reserve_batches').exists()
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
rawdir=R/'preflight_raw';rawdir.mkdir(exist_ok=True);attempts=[]
def get(name,url):
 for i in range(1,4):
  started=now();z=subprocess.run(['curl','--ipv4','--compressed','--http1.1','--tlsv1.2','--tls-max','1.2','--silent','--show-error','--connect-timeout','10','--max-time','30','--write-out','\n%{http_code}',url],cwd=ROOT,capture_output=True,timeout=65);body,code=z.stdout.rsplit(b'\n',1) if b'\n' in z.stdout else(z.stdout,b'000');dest=rawdir/f'{name}_{i}.gz';assert not dest.exists();dest.write_bytes(gzip.compress(body,mtime=0));item={'name':name,'url':url,'started_utc':started,'retrieved_utc':now(),'http_status':int(code),'curl_exit_code':z.returncode,'raw':rel(dest),'sha256':sha(dest),'raw_body_sha256':hashlib.sha256(body).hexdigest(),'bytes':len(body),'stderr':z.stderr.decode(errors='replace')};attempts.append(item);put(R/'preflight_transport_attempts.json',attempts)
  if z.returncode==0 and int(code)==200:return body,item
 raise RuntimeError('Public preflight failed three bounded attempts;no reservation or model/account execution')
response={}
for a in ['BTC','ETH']:
 url='https://fapi.binance.com/fapi/v1/fundingRate?'+urllib.parse.urlencode({'symbol':a+'USDT','startTime':ms(lo),'endTime':ms(end),'limit':1000});body,item=get(a+'_funding',url);response[a]=json.loads(body);assert isinstance(response[a],list) and len(response[a])<1000 and all(ms(lo)<int(z['fundingTime'])<=ms(end) and z['symbol']==a+'USDT' and 'markPrice' in z and 'fundingRate' in z for z in response[a])
put(R/'window_funding_preflight.json',{'recorded_utc':now(),'query_window_utc':[lo,end],'public_fields_by_asset':response,'all_pages_completed':True,'HTTP_receipts':[z for z in attempts if z['name'].endswith('_funding')],'purpose':'Fresh complete actual timestamps,not assumed nominal settlement schedule;before reserve.'})
for a,w in windows.items():
 fr={s:[z for z in response[s] if ms(w['start_utc'])<int(z['fundingTime'])<=ms(w['cutoff_utc'])] for s in ['BTC','ETH']} if a!='SMA' else {'BTC':[],'ETH':[]};times=sorted({int(z['fundingTime']) for xs in fr.values() for z in xs});w.update(expected_funding_by_asset=fr,expected_funding_records=3*sum(map(len,fr.values())),expected_funding_utc=[datetime.fromtimestamp(t/1000,timezone.utc).isoformat().replace('+00:00','Z') for t in times])
windows.update(recorded_utc=now(),rules='Each original account continues its own frozen cash,quantity,desired,costs and NAV. CurrentSMA/candidateNov23_04:30..06:30;L4/FEWM06:10..08:10. Daily events derived from original state and funding from fresh exact public timestamps. No reset,early booking,new research adoption or forced close;next dailyNov24_00:01,original terminal2027-03-31_00:01.')
put(R/'account_windows.json',windows)
assert all(not windows[a]['expected_daily_events_utc'] for a in ['SMA','candidate','l4h02','fewm'])
for n in P.glob('funding*_nov*_preflight.json'):(R/n.name).write_bytes(n.read_bytes());sources[rel(R/n.name)]=sha(n)
# Bind the original first08:00:00.004 source and own zero prior keys before ANY reservation.
first=ROOT/h['actual_Nov23_08_source'];doc=rd(first);assert sha(first)==h['actual_Nov23_08_source_sha256']=='7214d0f1d827bf7d105cb6e12ef25eaebe68d90c08d48f2fc80103aec0089dd5' and doc['recorded_utc']=='2026-11-23T23:51:12.472710Z'
local=R/first.name;assert sha(local)==sha(first);times08={str(int(z['fundingTime'])*1000000) for xs in doc['public_fields_by_asset'].values() for z in xs};assert times08=={'1795420800004000000'}
for asset in ['BTC','ETH']:
 ids={int(z['fundingTime']) for z in doc['public_fields_by_asset'][asset]};assert [z for z in response[asset] if int(z['fundingTime']) in ids]==[z for z in doc['public_fields_by_asset'][asset] if ms(lo)<int(z['fundingTime'])<=ms(end)]
prior08=rd(P/'account_window_verification.json')['full_chain_once_counts'];pc={a:{t:prior08[a]['funding'].get(t,0) for t in times08} for a in ['candidate','l4h02','fewm']};assert all(n==0 for x in pc.values() for n in x.values());inc08={a:{t:sum(3 for xs in windows[a]['expected_funding_by_asset'].values() for z in xs if str(int(z['fundingTime'])*1000000)==t) for t in times08} for a in pc};assert {a:sum(x.values()) for a,x in inc08.items()}=={'candidate':0,'l4h02':6,'fewm':6};proof=R/'actual08_nov23_prebinding_source.json';put(proof,{'passed':True,'recorded_utc':now(),'source':rel(local),'sha256':sha(local),'original_source':rel(first),'first_capture_utc':doc['recorded_utc'],'actual_public_fields':doc['public_fields_by_asset'],'prior_unique_counts':pc,'expected_current_increment_counts':inc08,'fresh_exact_source_fields_equal':True,'before_any_current_reservation':True,'cashflow_calculations':0,'own_signed_q_and_cost_required_no_cashflow_copy':True});sources.update({rel(proof):sha(proof),rel(first):sha(first)})
path75=ROOT/h['SMA_full75_authority'];path74=ROOT/h['SMA_full74_authority'];a75=gz(path75);a74=gz(path74);assert sha(path75)==h['SMA_full75_sha256'] and sha(path74)==h['SMA_full74_sha256'] and all(len(a75[a]['1d'])==75 and a75[a]['1d'][:74]==a74[a]['1d'] for a in ['BTC','ETH']);sources.update({rel(path75):sha(path75),rel(path74):sha(path74)})
put(R/'SMA_full75_prebinding.json',{'passed':True,'recorded_utc':now(),'authority':rel(path75),'sha256':sha(path75),'full74_authority':rel(path74),'full74_sha256':sha(path74),'full75_realSPOT_exact74prefix':True,'current_original_daily_event_count':0,'current_markonly_context_readonly':True,'before_any_current_reservation':True})
old=(M/'forward.py').read_text();new=(R/'forward.py').read_text();a=ast.parse(old);b=ast.parse(new)
for tree in [a,b]:
 for node in ast.walk(tree):
  if isinstance(node,ast.Constant) and isinstance(node.value,str):node.value=node.value.replace('SMA_full74_prebinding','SMA_full75_prebinding').replace('Nov22','Nov23')
assert ast.dump(a,include_attributes=False)==ast.dump(b,include_attributes=False)
put(R/'SMA_markonly_kernel_identity.json',{'passed':True,'old_source':rel(M/'forward.py'),'old_sha256':sha(M/'forward.py'),'new_source':rel(R/'forward.py'),'new_sha256':sha(R/'forward.py'),'AST_equal_except_current_background_filename_and_handoff_prose':True,'full_daily_background':75,'previous_state_bound':rel(P/'forward_state.json'),'new_daily_decisions':0,'original_Float_arithmetic_unchanged':True})
lp=copy.deepcopy(rd(P/'l4h02_resume_plan.json'));pt=ROOT/'research/automation/l4h02_forward_latest.json';lp.update(frozen_at_utc=now(),recorded_utc=now(),round=R.name,previous_pointer=rd(pt),previous_pointer_sha256=sha(pt),cutoff_utc=windows['l4h02']['cutoff_utc'],cutoff_ns=ms(windows['l4h02']['cutoff_utc'])*1000000,branch_lock_broker_pid=PID,rules=windows['rules']);put(R/'l4h02_resume_plan.json',lp);sources.update(lp['source_sha256'])
for n in ['research/experiments/20261104T201939Z/prospective_fewm','research/experiments/20261026T110637Z']:
 for p in (ROOT/n).glob('*.py'):sources[rel(p)]=sha(p)
for n in ['binding.json','plan.json']:
 p=ROOT/'research/experiments/20261104T201939Z/prospective_fewm'/n;sources[rel(p)]=sha(p)
oldhours=P/'l4h02_observation/input_manifest.json';sources[rel(oldhours)]=sha(oldhours)
for z in rd(oldhours)['provenance']:
 if '/fapi/v1/markPriceKlines?' in z['url']:assert sha(ROOT/z['raw'])==z['sha256'];sources[z['raw']]=z['sha256']
body,item=get('official_market_py','https://raw.githubusercontent.com/binance/binance-futures-connector-python/main/binance/um_futures/market.py');assert b'def funding_rate' in body and b'/fapi/v1/fundingRate' in body
put(R/'primary_source_access.json',{'recorded_utc':now(),'browser_reads':[{'url':'https://github.com/binance/binance-futures-connector-python/blob/main/binance/um_futures/market.py','reference':'turn410view0','purpose':'Official publicGET implementation fields;read-only source,not executed'},{'url':'https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data','reference':'turn410view1','purpose':'Official endpoint documentation;old link redirected'}],'official_SDK_code':item,'source_code_version_sha256':hashlib.sha256(body).hexdigest(),'downloaded_code_not_executed':True})
put(R/'original_accounts_binding.json',{'recorded_utc':now(),'sources_sha256':sources,'source_pointers_before':{a:rd(ROOT/'research/automation'/f'{a}_forward_latest.json') for a in ['candidate','l4h02','fewm']},'SMA_current_mark_only_adapter':rel(R/'forward.py'),'SMA_current_full_daily_context':75,'all4windows_predeclared_before_reserve':True,'immutable_financial_kernels_unchanged':True,'no_financial_or_account_calculation_yet':True})
print(json.dumps({'prepared':True,'fresh_funding':response,'windows':{a:[windows[a]['start_utc'],windows[a]['cutoff_utc']] for a in ['SMA','candidate','l4h02','fewm']},'SMA_full_background':75,'evaluations':0}),flush=True)
