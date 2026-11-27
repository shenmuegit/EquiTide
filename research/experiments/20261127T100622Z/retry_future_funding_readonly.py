"""Bound read-only recovery of the failed ETH historical funding GET; no accounts/models."""
import gzip,hashlib,json,subprocess,urllib.parse
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
rd=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');now=lambda:datetime.now(timezone.utc).isoformat()
b=rd(R/'funding_retry_binding.json');assert sha(Path(__file__))==b['source_sha256']
for p,h in b['immutable_inputs_sha256'].items():assert sha(ROOT/p)==h,p
old=rd(R/'next_window_transport_attempts.json');btc=next(z for z in old if z['asset']=='BTC' and z['http_status']==200 and not z['curl_exit_code']);eth=[z for z in old if z['asset']=='ETH'];assert len(eth)==3 and all(z['curl_exit_code']==35 and z['http_status']==0 for z in eth);url=eth[0]['url'];assert all(z['url']==url for z in eth);params=urllib.parse.parse_qs(urllib.parse.urlsplit(url).query);assert params['symbol']==['ETHUSDT'];lo,hi=int(params['startTime'][0]),int(params['endTime'][0]);folder=R/'next_funding_recovery_raw';folder.mkdir(exist_ok=True);attempts=[];response={'BTC':json.loads(gzip.decompress((ROOT/btc['raw']).read_bytes()))}
for i in range(1,4):
 started=now();z=subprocess.run(['curl','--ipv4','--compressed','--http1.1','--tlsv1.2','--tls-max','1.2','--silent','--show-error','--connect-timeout','10','--max-time','30','--write-out','\n%{http_code}',url],cwd=ROOT,capture_output=True,timeout=65);body,code=z.stdout.rsplit(b'\n',1) if b'\n' in z.stdout else(z.stdout,b'000');p=folder/f'ETH_{i}.gz';assert not p.exists();p.write_bytes(gzip.compress(body,mtime=0));row={'asset':'ETH','url':url,'started_utc':started,'retrieved_utc':now(),'raw':str(p.relative_to(ROOT)),'sha256':sha(p),'http_status':int(code),'curl_exit_code':z.returncode,'stderr':z.stderr.decode(errors='replace'),'read_only_recovery_not_model_or_account_replay':True};attempts.append(row);put(R/'next_funding_recovery_transport_attempts.json',attempts);print(json.dumps({'attempt':i,'HTTP':int(code),'curl_exit':z.returncode}),flush=True)
 if z.returncode==0 and int(code)==200:response['ETH']=json.loads(body);break
else:raise RuntimeError('Read-only ETH recovery GET still unavailable; preserve all completed results and every failed response.')
for a,rows in response.items():assert isinstance(rows,list) and len(rows)<1000 and all(lo<int(z['fundingTime'])<=hi and z['symbol']==a+'USDT' and 'markPrice' in z and 'fundingRate' in z for z in rows)
for e in rd(ROOT/'research/experiments/20261127T080551Z/next_research_state.json')['UTC_midnight_handoff']['next_window_known_actual_funding_sources']:
 for a,xs in e['actual_public_fields'].items():
  for z in xs:
   if lo<int(z['fundingTime'])<=hi:assert z in response[a]
put(R/'next_funding_recovery_response.json',{'passed':True,'recorded_utc':now(),'public_fields_by_asset':response,'query_window_ms':[lo,hi],'HTTP_receipts':old+attempts,'original_attempt_file_sha256':sha(R/'next_window_transport_attempts.json'),'original_failed_collect_receipt_sha256':sha(R/'command_receipts/collect.json'),'readonly_no_reserve_or_cashflow_calculation':True,'reuse_original_verified_BTC_HTTP200':True})
for p,h in b['immutable_inputs_sha256'].items():assert sha(ROOT/p)==h,p
put(R/'funding_retry_verification.json',{'passed':True,'bound_source_sha256':b['source_sha256'],'immutable_inputs_unchanged':True,'ETH_recovered':True,'original_BTC_HTTP200_reused':True,'original_failed_receipts_and_all_raw_responses_unchanged':True,'financial_strategy_or_account_window_replays':0});print('PASS readonly ETH response recovered;all completed financial/account bytes unchanged',flush=True)
