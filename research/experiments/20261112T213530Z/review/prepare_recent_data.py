"""Read-only next-period real-data preparation; zero strategy/account/registry calls."""
import gzip,hashlib,json,subprocess,sys,time,urllib.parse
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal as D
import polars as pl
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import sha,put,now,rel
ms=lambda s:int(datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()*1000)
lo,hi=ms('2026-10-24T00:00:00Z'),ms('2026-11-12T00:00:00Z');MIN=60000;HOUR=60*MIN;DAY=24*HOUR
dest=ROOT/'data/runs/automation'/R.name/'next_period_inputs';rawdir=dest/'raw';rawdir.mkdir(parents=True,exist_ok=False);clockstart=time.monotonic();attempts=[];inputs=[];quality={}
assert not (R/'recent_data_readiness.json').exists()
plan={'recorded_before_capture_utc':now(),'market_start_inclusive_utc':'2026-10-24T00:00:00Z','market_end_exclusive_utc':'2026-11-12T00:00:00Z','days':19,'terminal_reference_minutes_utc':['2026-11-12T00:00:00Z','2026-11-12T00:01:00Z'],'funding_context_days':2,'proposed_future_research_window_utc':['2026-10-24T00:01:00Z','2026-11-12T00:01:00Z'],'future_grid_axes':{'BTC_VOL_CAP':[.03,.04,.05],'ETH_FUND_R':[.00875,.01,.01125]},'future_representative':{'BVC':.04,'R':.01},'existing_representative_fingerprint':'fdf88a9ff78fe32e8cdbb2a5252c69aab81f4d91f8b8fda1b2bdc3434c08201c','future_rules':'Existing exact whole-bank policies/C/N/raw1/1; any future time-bound configuration needs its own successful reserve before calculation. No tuning from prepared-period returns.','limits':'Data preparation only, no simulated trade/NAV/return or current financial-report change. This extension is historical and its market has been seen in other observations, not an untouched final or independent future sample.19days cannot establish180day/sixfold qualification. A calendar adapter and independent validation remain necessary.','capture_wall_budget_seconds':900,'public_GET_attempts_per_URL':2};put(R/'recent_data_preparation_plan.json',plan)
def request(path,params):
 assert path in ['/fapi/v1/klines','/fapi/v1/markPriceKlines','/fapi/v1/fundingRate'];url='https://fapi.binance.com'+path+'?'+urllib.parse.urlencode(params)
 for attempt in range(2):
  assert time.monotonic()-clockstart<900,'Read-only data preparation wall budget exceeded'
  a=now();cmd=['curl','--ipv4','--compressed','--http1.1','--silent','--show-error','--connect-timeout','10','--max-time','30','--write-out','\n%{http_code}',url];z=subprocess.run(cmd,cwd=ROOT,capture_output=True,timeout=40);body,code=z.stdout.rsplit(b'\n',1) if b'\n' in z.stdout else (z.stdout,b'000');f=rawdir/f'http_{len(attempts):04d}.json.gz';f.write_bytes(gzip.compress(body,mtime=0));row={'url':url,'started_utc':a,'finished_utc':now(),'curl_exit_code':z.returncode,'http_status':int(code),'raw':rel(f),'sha256':sha(f),'body_sha256':hashlib.sha256(body).hexdigest(),'bytes':len(body),'compressed_bytes':f.stat().st_size,'stderr':z.stderr.decode(errors='replace')};attempts.append(row);put(R/'recent_data_capture_attempts.json',attempts)
  if z.returncode==0 and int(code)==200:
   data=json.loads(body);assert isinstance(data,list);return data
 raise RuntimeError('Two bounded verified-TLS public GET attempts failed; no strategy or account calculation')
try:
 current=json.loads((R/'plan.json').read_text())
 for asset in ['BTC','ETH']:
  bars=[];cursor=lo
  while cursor<hi:
   chunk=request('/fapi/v1/klines',{'symbol':asset+'USDT','interval':'1m','startTime':cursor,'endTime':hi-1,'limit':1500});assert chunk and int(chunk[0][0])==cursor and all(cursor<=int(x[0])<hi for x in chunk);bars.extend(chunk);cursor=int(chunk[-1][0])+MIN
  assert len(bars)==19*1440 and int(bars[-1][0])+MIN==hi
  terminal=request('/fapi/v1/klines',{'symbol':asset+'USDT','interval':'1m','startTime':hi,'endTime':hi+2*MIN-1,'limit':1500});assert len(terminal)==2 and [int(x[0]) for x in terminal]==[hi,hi+MIN]
  for j,x in enumerate(bars+terminal):
   assert int(x[0])==lo+j*MIN and int(x[6])+1==int(x[0])+MIN<=ms(now()) and D(x[3])<=min(D(x[1]),D(x[4]))<=max(D(x[1]),D(x[4]))<=D(x[2]) and D(x[3])>0 and D(x[7])>=0
  hours=request('/fapi/v1/markPriceKlines',{'symbol':asset+'USDT','interval':'1h','startTime':lo,'endTime':hi-1,'limit':1500});assert len(hours)==19*24
  for j,x in enumerate(hours):assert int(x[0])==lo+j*HOUR and int(x[6])+1==int(x[0])+HOUR<=ms(now()) and D(x[3])<=min(D(x[1]),D(x[4]))<=max(D(x[1]),D(x[4]))<=D(x[2]) and D(x[3])>0
  funds=request('/fapi/v1/fundingRate',{'symbol':asset+'USDT','startTime':lo-2*DAY,'endTime':hi,'limit':1000});assert funds and len(funds)<1000 and all(x['symbol']==asset+'USDT' and lo-2*DAY<=x['fundingTime']<=hi and D(x['markPrice'])>0 for x in funds) and all(a['fundingTime']<b['fundingTime'] for a,b in zip(funds,funds[1:]))
  original={Path(z['path']).stem:z for z in current['data']['assets'][asset]}
  for x in original.values():assert sha(ROOT/x['path'])==x['sha256']
  old=pl.read_parquet(ROOT/original['perp_bars']['path']);overlap=old.filter((pl.col('open_ts')>=lo*1000000)&(pl.col('open_ts')<(lo+DAY)*1000000)).to_dicts();assert len(overlap)==1440
  for oldrow,row in zip(overlap,bars):
   assert oldrow['open_ts']==int(row[0])*1000000 and oldrow['available_ts']==(int(row[6])+1)*1000000
   for key,index in [('open',1),('high',2),('low',3),('close',4),('quote_volume',7)]:assert oldrow[key]==D(row[index]),(asset,key,oldrow['open_ts'])
  oldh=pl.read_parquet(ROOT/original['mark_hour_bars']['path']).filter((pl.col('open_ts')>=lo*1000000)&(pl.col('open_ts')<(lo+DAY)*1000000)).to_dicts();assert len(oldh)==24
  for oldrow,row in zip(oldh,hours):
   assert oldrow['open_ts']==int(row[0])*1000000
   for key,index in [('open',1),('high',2),('low',3),('close',4)]:assert oldrow[key]==D(row[index])
  oldf=pl.read_parquet(ROOT/original['funding_settlement']['path']).to_dicts();by={x['settlement_ts']:x for x in oldf};common=[x for x in funds if x['fundingTime']*1000000 in by];assert len(common)>=6
  for row in common:
   oldrow=by[row['fundingTime']*1000000];assert oldrow['realized_rate']==D(row['fundingRate']) and oldrow['mark_price_at_settlement']==D(row['markPrice'])
  packet={'asset':asset,'minutes':bars,'terminal_reference_minutes':terminal,'closed_mark_hours':hours,'actual_funding_with_two_day_context':funds,'funding_availability_assumption':'For future policy comparison only, retain source convention fundingTime+1hour; actual historical arrival not measured.','captured_utc':now(),'current_financial_or_account_results_computed':False};f=dest/(asset+'_public_bundle.json.gz');f.write_bytes(gzip.compress(json.dumps(packet,sort_keys=True,separators=(',',':')).encode(),mtime=0));inputs.append({'path':rel(f),'sha256':sha(f),'bytes':f.stat().st_size,'role':'Next-period real market data only; not used in current report'});quality[asset]={'minute_rows':len(bars),'terminal_reference_minute_rows':len(terminal),'closed_mark_hour_rows':len(hours),'actual_funding_rows_with_context':len(funds),'old_native_minute_overlap_rows_verified':len(overlap),'old_mark_hour_overlap_rows_verified':len(oldh),'old_funding_overlap_events_verified':len(common),'complete_no_gap_closed_minutes_and_OHLC':True,'old_original_data_hashes_unchanged':True};print('PREPARED',asset,quality[asset],flush=True)
 rawinputs=[{'path':x['raw'],'sha256':x['sha256'],'bytes':x['compressed_bytes'],'role':'Actual public GET raw response retained in ignored data'} for x in attempts];result={'passed':True,'status':'ready_for_future_calendar_adapter_and_preregistered_backtests','recorded_utc':now(),'preparation_plan_sha256':sha(R/'recent_data_preparation_plan.json'),'quality':quality,'inputs':inputs+rawinputs,'source_HTTP_attempts':len(attempts),'failed_HTTP_attempts':sum(x['curl_exit_code']!=0 or x['http_status']!=200 for x in attempts),'new_financial_configurations_evaluated':0,'simulated_trades_or_NAV':0,'account_state_changes':0,'registry_events':0,'limits':plan['limits']}
except Exception as e:
 result={'passed':False,'status':'blocked_data_preparation_only','recorded_utc':now(),'exception_type':type(e).__name__,'reason':str(e),'preparation_plan_sha256':sha(R/'recent_data_preparation_plan.json'),'quality_completed':quality,'inputs':inputs+[{'path':x['raw'],'sha256':x['sha256'],'bytes':x['compressed_bytes']} for x in attempts],'source_HTTP_attempts':len(attempts),'new_financial_configurations_evaluated':0,'simulated_trades_or_NAV':0,'account_state_changes':0,'registry_events':0,'limits':plan['limits']};print('ACTUAL_DATA_PREPARATION_BLOCKED',type(e).__name__,str(e),flush=True)
put(R/'recent_data_readiness.json',result);print(json.dumps({k:v for k,v in result.items() if k not in ['inputs','quality','quality_completed']}),flush=True)
