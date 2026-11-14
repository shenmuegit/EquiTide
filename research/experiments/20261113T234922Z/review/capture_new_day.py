"""Read the new closed UTC day from official endpoints, never calculate a strategy."""
import gzip,hashlib,json,subprocess,sys,urllib.parse,time
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal as D
import polars as pl
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import sha,put,now,rel
P=ROOT/'research/experiments/20261113T214818Z';old=json.loads((P/'plan.json').read_text());ms=lambda s:int(datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()*1000);lo=ms('2026-11-11T00:00:00Z');hi=ms('2026-11-13T00:00:00Z');M=60000;H=3600000;dest=ROOT/'data/runs/automation'/R.name/'next_day';rawdir=dest/'raw';rawdir.mkdir(parents=True);attempts=[];bundles={};quality={};clockstart=time.monotonic();put(R/'data_capture_plan.json',{'recorded_before_capture_utc':now(),'capture_start_utc':'2026-11-11T00:00:00Z','capture_end_exclusive_utc':'2026-11-13T00:00:00Z','new_day_utc':'2026-11-12','overlap_day_utc':'2026-11-11','future_validation_end_utc':'2026-11-13T00:01:00Z','terminal_reference_minutes':2,'future_axes':{'BTC_VOL_CAP':[.03,.04],'ETH_FUND_R':[.00875,.01]},'future_preset':{'BTC_VOL_CAP':.04,'ETH_FUND_R':.01},'future_new_spec_reserve_required':True,'new_day_not_untouched_final_or_independent_future':True,'strategy_or_account_calculations':0})
def get(path,params):
 url='https://fapi.binance.com'+path+'?'+urllib.parse.urlencode(params)
 for a in range(3):
  assert time.monotonic()-clockstart<600
  st=now();z=subprocess.run(['curl','--ipv4','--compressed','--http1.1','--silent','--show-error','--connect-timeout','10','--max-time','30','--write-out','\n%{http_code}',url],cwd=ROOT,capture_output=True,timeout=40);body,status=z.stdout.rsplit(b'\n',1) if b'\n' in z.stdout else (z.stdout,b'000');f=rawdir/f'{len(attempts):03d}.json.gz';f.write_bytes(gzip.compress(body,mtime=0));row={'url':url,'started_utc':st,'finished_utc':now(),'curl_exit_code':z.returncode,'http_status':int(status),'raw':rel(f),'sha256':sha(f),'body_sha256':hashlib.sha256(body).hexdigest(),'bytes':len(body),'stderr':z.stderr.decode(errors='replace')};attempts.append(row);put(R/'new_day_capture_attempts.json',attempts)
  if z.returncode==0 and int(status)==200:
   d=json.loads(body);assert isinstance(d,list);return d
 raise RuntimeError('bounded new-day public data reads failed')
for asset in ['BTC','ETH']:
 bars=[];cursor=lo
 while cursor<hi:
  part=get('/fapi/v1/klines',{'symbol':asset+'USDT','interval':'1m','startTime':cursor,'endTime':hi-1,'limit':1500});assert part and int(part[0][0])==cursor;bars+=part;cursor=int(part[-1][0])+M
 terminal=get('/fapi/v1/klines',{'symbol':asset+'USDT','interval':'1m','startTime':hi,'endTime':hi+2*M-1,'limit':1500});hours=get('/fapi/v1/markPriceKlines',{'symbol':asset+'USDT','interval':'1h','startTime':lo,'endTime':hi-1,'limit':1500});funds=get('/fapi/v1/fundingRate',{'symbol':asset+'USDT','startTime':lo-2*86400000,'endTime':hi,'limit':1000});assert len(bars)==2880 and len(terminal)==2 and len(hours)==48
 for j,b in enumerate(bars+terminal):assert int(b[0])==lo+j*M and int(b[6])+1==int(b[0])+M<=ms(now()) and D(b[3])<=min(D(b[1]),D(b[4]))<=max(D(b[1]),D(b[4]))<=D(b[2]) and D(b[3])>0 and D(b[7])>=0
 for j,b in enumerate(hours):assert int(b[0])==lo+j*H and int(b[6])+1==int(b[0])+H<=ms(now()) and D(b[3])<=min(D(b[1]),D(b[4]))<=max(D(b[1]),D(b[4]))<=D(b[2]) and D(b[3])>0
 assert funds and all(f['symbol']==asset+'USDT' and D(f['markPrice'])>0 for f in funds) and all(a['fundingTime']<b['fundingTime'] for a,b in zip(funds,funds[1:]));fs={Path(z['path']).stem:z for z in old['data']['assets'][asset]}
 for x in fs.values():assert sha(ROOT/x['path'])==x['sha256']
 prior=pl.read_parquet(ROOT/fs['perp_bars']['path']).filter(pl.col('open_ts')>=lo*1000000).to_dicts();assert len(prior)==1442
 for a,b in zip(prior,bars):
  assert a['open_ts']==int(b[0])*1000000 and a['available_ts']==(int(b[6])+1)*1000000
  for k,j in [('open',1),('high',2),('low',3),('close',4),('base_volume',5),('quote_volume',7)]:assert a[k]==D(b[j])
 ph=pl.read_parquet(ROOT/fs['mark_hour_bars']['path']).filter(pl.col('open_ts')>=lo*1000000).to_dicts();assert len(ph)==24
 for a,b in zip(ph,hours):
  for k,j in [('open',1),('high',2),('low',3),('close',4)]:assert a[k]==D(b[j])
 pf={r['settlement_ts']:r for r in pl.read_parquet(ROOT/fs['funding_settlement']['path']).to_dicts()};shared=[r for r in funds if r['fundingTime']*1000000 in pf];assert len(shared)>=6
 for f in shared:assert pf[f['fundingTime']*1000000]['realized_rate']==D(f['fundingRate']) and pf[f['fundingTime']*1000000]['mark_price_at_settlement']==D(f['markPrice'])
 packet={'asset':asset,'minutes':bars,'terminal_reference_minutes':terminal,'closed_mark_hours':hours,'actual_funding_with_two_day_context':funds,'captured_utc':now()};f=dest/(asset+'_public_bundle.json.gz');f.write_bytes(gzip.compress(json.dumps(packet,sort_keys=True,separators=(',',':')).encode(),mtime=0));bundles[asset]={'path':rel(f),'sha256':sha(f),'bytes':f.stat().st_size};quality[asset]={'minutes_with_overlap':len(bars),'new_complete_day_minutes':1440,'closed_hours_with_overlap':len(hours),'new_closed_hours':24,'old_minute_overlap_rows_verified':len(prior),'old_hour_overlap_rows_verified':len(ph),'old_funding_events_verified':len(shared),'actual_funding_rows':len(funds)};print('PREPARED',asset,quality[asset],flush=True)
put(R/'new_day_readiness.json',{'passed':True,'recorded_utc':now(),'bundles':bundles,'quality':quality,'capture_attempts':len(attempts),'failed_attempts':sum(x['http_status']!=200 or x['curl_exit_code']!=0 for x in attempts),'all_closed_continuous_real_source_data':True,'zero_strategy_or_account_calculations':True,'new_day_not_independent_future':True});print('PASS actual newday ready,0financialcalculations',flush=True)
