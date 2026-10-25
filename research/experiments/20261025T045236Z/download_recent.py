"""Capture genuine recent futures data; no signal or PnL calculation here."""
import concurrent.futures,copy,gzip,hashlib,importlib.util,io,json,subprocess,sys,zipfile
from datetime import datetime,timezone,timedelta
from decimal import Decimal as D
from pathlib import Path
import polars as pl
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;CACHE=ROOT/'data/raw/research_20261025_recent';CACHE.mkdir(parents=True,exist_ok=True)
DAY=86400000000000;MIN=60000000000;HOUR=60*MIN
ns=lambda s:int(datetime.fromisoformat(s.replace('Z','+00:00')).timestamp())*10**9
START,END=ns('2026-08-12T00:00:00Z'),ns('2026-10-25T00:00:00Z')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rel=lambda p:str(p.relative_to(ROOT))
COLS=['raw_open_ts','open','high','low','close','base_volume','raw_close_ts','quote_volume','trades','taker_base','taker_quote','ignore']
put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
old=json.loads((ROOT/'research/experiments/20261025T005204Z/plan.json').read_text())['data']['assets'];manifest={'recorded_utc':datetime.now(timezone.utc).isoformat(),'input_start_utc':'2026-08-12T00:00:00Z','input_end_exclusive_utc':'2026-10-25T00:00:00Z','planned_oos_start_utc':'2026-09-14T00:01:00Z','planned_oos_end_exclusive_utc':'2026-10-24T00:01:00Z','no_financial_evaluation_performed':True,'requests':[],'errors':[],'normalized':{},'previous_real_source_files':old,'prior_failure_manifest':{'path':rel(R/'recent_data_manifest_failed.json'),'sha256':sha(R/'recent_data_manifest_failed.json')},'Oct24_archive404_recovery':'OfficialREST1440closedminutes perasset;failedoriginalrequests preserved separately'}
def get(url,path):
 if path.exists():return path.read_bytes()
 p=subprocess.run(['curl','--http1.1','--fail','--silent','--show-error','--retry','2','--retry-all-errors','--connect-timeout','10','--max-time','35',url],capture_output=True,timeout=120)
 if p.returncode:raise RuntimeError(f'curl exit{p.returncode}: {url}: {p.stderr.decode(errors="replace")}')
 path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(p.stdout);return p.stdout
def archive(asset,date):
 name=f'{asset}USDT-1m-{date}.zip';url=f'https://data.binance.vision/data/futures/um/daily/klines/{asset}USDT/1m/{name}';path=CACHE/asset/name;raw=get(url,path);checksum=get(url+'.CHECKSUM',Path(str(path)+'.CHECKSUM')).decode().split()[0];assert hashlib.sha256(raw).hexdigest()==checksum
 with zipfile.ZipFile(io.BytesIO(raw)) as z:assert z.testzip() is None and len(z.namelist())==1
 return {'asset':asset,'category':'perp_minute_archive','date':date,'url':url,'path':rel(path),'sha256':sha(path),'published_sha256':checksum,'bytes':len(raw)}
def main():
 requests=[];date=datetime(2026,9,16,tzinfo=timezone.utc)
 while date<datetime(2026,10,24,tzinfo=timezone.utc):
  requests.extend((a,date.strftime('%Y-%m-%d')) for a in ['BTC','ETH']);date+=timedelta(days=1)
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  jobs={pool.submit(archive,*args):args for args in requests}
  for f in concurrent.futures.as_completed(jobs):
   try:manifest['requests'].append(f.result());print('ARCHIVE',len(manifest['requests']),jobs[f],flush=True)
   except Exception as e:manifest['errors'].append({'request':jobs[f],'error':str(e)});print('ERROR',str(e),flush=True)
   put(R/'recent_data_manifest.json',manifest)
 assert not manifest['errors'],'Incomplete genuine archives; do not backtest'
 for asset in ['BTC','ETH']:
  paths={Path(x['path']).stem:x for x in old[asset]}
  for x in old[asset]:assert sha(ROOT/x['path'])==x['sha256']
  frame=pl.read_parquet(ROOT/paths['perp_bars']['path']).filter((pl.col('open_ts')>=START)&(pl.col('open_ts')<ns('2026-09-16T00:00:00Z')));parts=[frame]
  for item in sorted([x for x in manifest['requests'] if x['asset']==asset],key=lambda x:x['date']):
   with zipfile.ZipFile(ROOT/item['path']) as z:raw=z.read(z.namelist()[0])
   df=pl.read_csv(io.BytesIO(raw),has_header=not raw.split(b',',1)[0].isdigit(),new_columns=COLS,infer_schema=False);unit=1000 if int(df['raw_open_ts'][0])>10**14 else 1000000;df=df.with_columns((pl.col('raw_open_ts').cast(pl.Int64)*unit).alias('open_ts'),(pl.col('raw_close_ts').cast(pl.Int64)*unit).alias('source_close_ts'));assert (df['source_close_ts']-df['open_ts']==MIN-unit).all();df=df.select('open_ts',*[pl.col(k).cast(pl.Decimal(38,18)) for k in ['open','high','low','close','base_volume','quote_volume']]).with_columns((pl.col('open_ts')+MIN).alias('available_ts'),pl.lit(True).alias('is_closed'));parts.append(df.cast(frame.schema).select(frame.columns))
  rest_start=ns('2026-10-24T00:00:00Z');rest_rows=[]
  for page,(a,b) in enumerate([(rest_start,rest_start+1000*MIN),(rest_start+1000*MIN,END)]):
   url=f'https://fapi.binance.com/fapi/v1/klines?symbol={asset}USDT&interval=1m&startTime={a//10**6}&endTime={b//10**6-1}&limit=1000';q=CACHE/f'{asset}-20261024-minute-page{page}.json';raw=get(url,q);bars=json.loads(raw);assert isinstance(bars,list) and [int(z[0])*10**6 for z in bars]==list(range(a,b,MIN))
   for z in bars:
    assert int(z[6])+1==int(z[0])+60000
    rest_rows.append({'open_ts':int(z[0])*10**6,**{k:D(str(z[j])) for k,j in [('open',1),('high',2),('low',3),('close',4),('base_volume',5),('quote_volume',7)]},'available_ts':(int(z[0])+60000)*10**6,'is_closed':True})
   manifest['requests'].append({'asset':asset,'category':'Oct24_genuine_minute_REST_recovery','url':url,'path':rel(q),'sha256':sha(q),'bytes':len(raw),'rows':len(bars),'archive404_recovery':True})
  assert len(rest_rows)==1440;parts.append(pl.DataFrame(rest_rows).cast(frame.schema).select(frame.columns))
  minute=pl.concat(parts).sort('open_ts');assert minute.height==74*1440 and minute['open_ts'][0]==START and minute['open_ts'][-1]==END-MIN and (minute['open_ts'].diff().drop_nulls()==MIN).all() and minute['open_ts'].n_unique()==minute.height
  target=ROOT/f'data/normalized/binance/{asset}/binance_{asset}_20260812T000000Z_20261025T000000Z_recent_20261025';target.mkdir(parents=True,exist_ok=True);minute.write_parquet(target/'perp_bars.parquet')
  hstart=ns('2026-09-16T00:00:00Z');url=f'https://fapi.binance.com/fapi/v1/markPriceKlines?symbol={asset}USDT&interval=1h&startTime={hstart//10**6}&endTime={END//10**6-1}&limit=1500';p=CACHE/f'{asset}-mark-hour.json';raw=get(url,p);bars=json.loads(raw);assert isinstance(bars,list) and len(bars)==39*24;hour=pl.read_parquet(ROOT/paths['mark_hour_bars']['path']).filter((pl.col('open_ts')>=START)&(pl.col('open_ts')<hstart));new=[]
  for b in bars:
   assert int(b[6])+1==int(b[0])+3600000
   new.append({'open_ts':int(b[0])*10**6,**{k:D(str(b[j])) for k,j in [('open',1),('high',2),('low',3),('close',4),('base_volume',5),('quote_volume',7)]},'available_ts':(int(b[0])+3600000)*10**6,'is_closed':True})
  hour=pl.concat([hour,pl.DataFrame(new).cast(hour.schema).select(hour.columns)]).sort('open_ts');assert hour.height==74*24 and (hour['open_ts'].diff().drop_nulls()==HOUR).all();hour.write_parquet(target/'mark_hour_bars.parquet');manifest['requests'].append({'asset':asset,'category':'mark_hour_REST','url':url,'path':rel(p),'sha256':sha(p),'bytes':len(raw),'rows':len(bars)})
  url=f'https://fapi.binance.com/fapi/v1/fundingRate?symbol={asset}USDT&startTime={(START-DAY)//10**6}&endTime={END//10**6-1}&limit=1000';p=CACHE/f'{asset}-funding.json';raw=get(url,p);events=json.loads(raw);assert isinstance(events,list) and len(events)>=222;fund=[]
  for i,e in enumerate(events):
   t=int(e['fundingTime'])*10**6
   if not START<=t<END:continue
   assert i>0 and e['symbol']==asset+'USDT' and D(e['markPrice'])>0 and abs((t-int(events[i-1]['fundingTime'])*10**6)/HOUR-8)<.001
   fund.append({'settlement_ts':t,'available_ts':t+HOUR,'realized_rate':D(e['fundingRate']),'mark_price_at_settlement':D(e['markPrice']),'actual_interval_hours':D(8)})
  assert len(fund)==222;df=pl.DataFrame(fund).with_columns(*[pl.col(k).cast(pl.Decimal(38,18)) for k in ['realized_rate','mark_price_at_settlement','actual_interval_hours']]);df.write_parquet(target/'funding_settlement.parquet');manifest['requests'].append({'asset':asset,'category':'actual_funding_REST','url':url,'path':rel(p),'sha256':sha(p),'bytes':len(raw),'rows':len(events),'no_rate_or_mark_proxy':True})
  (target/'perp_instrument_meta.parquet').write_bytes((ROOT/paths['perp_instrument_meta']['path']).read_bytes());manifest.setdefault('metadata_scope',{})[asset]='Reuse actual previous Oct1 contract snapshot as fixed tick/lot/minnotional assumption. Not complete point-in-time historicalfilters; no invented data.'
  manifest['normalized'][asset]=[{'path':rel(q),'sha256':sha(q),'bytes':q.stat().st_size,'rows':pl.read_parquet(q).height} for q in sorted(target.glob('*.parquet'))]
  put(R/'recent_data_manifest.json',manifest);print('NORMALIZED',asset,manifest['normalized'][asset],flush=True)
 manifest['completed_utc']=datetime.now(timezone.utc).isoformat();put(R/'recent_data_manifest.json',manifest);print('GENUINE_RECENT_DATA_COMPLETE',flush=True)
if __name__=='__main__':
 try:main()
 except BaseException as e:
  manifest['errors'].append({'phase':'normalize_or_capture','error':str(e),'type':type(e).__name__});put(R/'recent_data_manifest.json',manifest);raise
