"""Official futures minute/mark-hour archives, actual rate+settlement-mark API and metadata."""
import concurrent.futures
import hashlib
import io
import json
import subprocess
import zipfile
from datetime import datetime,timezone
from decimal import Decimal
from pathlib import Path
import polars as pl
ROOT=Path(__file__).resolve().parents[3]
ROUND=Path(__file__).resolve().parent
CACHE=ROOT/'data/raw/research_20261001_perp'
CACHE.mkdir(parents=True,exist_ok=True)
VERSION='20250916T000000Z_20260916T000000Z_archive_20260929'
START=int(datetime(2025,9,16,tzinfo=timezone.utc).timestamp())*10**9
END=int(datetime(2026,9,16,tzinfo=timezone.utc).timestamp())*10**9
MINUTE=60*10**9
HOUR=60*MINUTE
COLS=['raw_open_ts','open','high','low','close','base_volume','raw_close_ts','quote_volume','trades','taker_base','taker_quote','ignore']

def get(url,path):
 if not path.exists():
  temp=Path(str(path)+'.part')
  p=subprocess.run(['curl','--http1.1','--retry','3','--retry-all-errors','--retry-delay','1','--connect-timeout','10','--max-time','90','-fsSL',url,'-o',str(temp)],capture_output=True,text=True)
  if p.returncode:raise RuntimeError(f'{url}: curl {p.returncode}: {p.stderr[-1200:]}')
  temp.replace(path)
 return path.read_bytes()

def archive(asset,category,period,daily=False):
 symbol=asset+'USDT'
 interval='1m' if category=='klines' else '1h'
 name=f'{symbol}-{interval}-{period}.zip'
 path=CACHE/category/name
 path.parent.mkdir(exist_ok=True)
 url=f'https://data.binance.vision/data/futures/um/{"daily" if daily else "monthly"}/{category}/{symbol}/{interval}/{name}'
 body=get(url,path)
 expected=get(url+'.CHECKSUM',Path(str(path)+'.CHECKSUM')).decode().split()[0]
 actual=hashlib.sha256(body).hexdigest()
 assert expected==actual,name
 return {'asset':asset,'category':category,'interval':interval,'url':url,'path':str(path.relative_to(ROOT)),'sha256':actual,'published_sha256':expected,'bytes':len(body)}

def normalized(asset,category,sources):
 frames=[];units=set()
 interval=MINUTE if category=='klines' else HOUR
 for source in sorted(sources,key=lambda x:x['url']):
  if source['asset']!=asset or source['category']!=category:continue
  with zipfile.ZipFile(ROOT/source['path']) as z:
   assert len(z.namelist())==1 and z.testzip() is None
   body=z.read(z.namelist()[0])
  header=not body.split(b',',1)[0].isdigit()
  frame=pl.read_csv(io.BytesIO(body),has_header=header,new_columns=COLS,infer_schema=False)
  raw=frame['raw_open_ts'].cast(pl.Int64)
  unit='us' if raw[0]>10**14 else 'ms';factor=1000 if unit=='us' else 10**6
  units.add(unit)
  frame=frame.with_columns((pl.col('raw_open_ts').cast(pl.Int64)*factor).alias('open_ts'),(pl.col('raw_close_ts').cast(pl.Int64)*factor).alias('source_close_ts'))
  assert ((frame['source_close_ts']-frame['open_ts'])==interval-factor).all()
  frame=frame.filter((pl.col('open_ts')>=START)&(pl.col('open_ts')<END)).select('open_ts',*[pl.col(x).cast(pl.Decimal(38,18)) for x in ('open','high','low','close','base_volume','quote_volume')])
  frames.append(frame)
 frame=pl.concat(frames).sort('open_ts').with_columns((pl.col('open_ts')+interval).alias('available_ts'),pl.lit(True).alias('is_closed'))
 expected=pl.Series('expected',range(START,END,interval),dtype=pl.Int64)
 missing=expected.filter(~expected.is_in(frame['open_ts'].implode()))
 print(json.dumps({'normalizing':asset+'/'+category,'rows':frame.height,'expected':len(expected),'missing_count':len(missing),'missing_first_ns':missing.head(20).to_list(),'duplicate_count':frame.height-frame['open_ts'].n_unique()}),flush=True)
 repairs=[]
 if len(missing):
  # Restore only missing timestamps from the actual official historical REST endpoint.
  # Never infer a bar from neighbors or fabricate zero-volume observations.
  for offset in range(0,len(missing),1000):
   wanted=missing.slice(offset,1000).to_list()
   begin,finish=wanted[0]//10**6,(wanted[-1]+interval)//10**6-1
   endpoint='klines' if category=='klines' else 'markPriceKlines'
   interval_name='1m' if category=='klines' else '1h'
   url=f'https://fapi.binance.com/fapi/v1/{endpoint}?symbol={asset}USDT&interval={interval_name}&startTime={begin}&endTime={finish}&limit=1000'
   path=CACHE/f'{asset}-{category}-repair-{begin}-{finish}.json'
   body=get(url,path);page=json.loads(body)
   assert isinstance(page,list) and page,repr(page)[:200]
   records=[]
   for row in page:
    ts=int(row[0])*10**6
    if ts not in set(wanted):continue
    assert int(row[6])*10**6-ts==interval-10**6
    records.append({'open_ts':ts,**{c:Decimal(str(row[j])) for c,j in [('open',1),('high',2),('low',3),('close',4),('base_volume',5),('quote_volume',7)]},'available_ts':ts+interval,'is_closed':True})
   assert len(records)==len(wanted),(asset,category,len(records),len(wanted))
   restored=pl.DataFrame(records).cast(frame.schema).select(frame.columns)
   frame=pl.concat([frame,restored]).sort('open_ts')
   repairs.append({'url':url,'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(body).hexdigest(),'actual_restored_rows':len(records),'missing_archive_timestamps_ns':wanted})
 assert frame.height==(END-START)//interval
 assert frame['open_ts'][0]==START and frame['open_ts'][-1]==END-interval
 assert (frame['open_ts'].diff().drop_nulls()==interval).all()
 assert (frame['low']>0).all() and (frame['high']>=frame['low']).all()
 assert ((frame['open']>=frame['low'])&(frame['open']<=frame['high'])&(frame['close']>=frame['low'])&(frame['close']<=frame['high'])).all()
 target=ROOT/'data/normalized/binance'/asset/f'binance_{asset}_{VERSION}'/('perp_bars.parquet' if category=='klines' else 'mark_hour_bars.parquet')
 target.parent.mkdir(parents=True,exist_ok=True)
 frame.write_parquet(target)
 return {'path':str(target.relative_to(ROOT)),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'rows':frame.height,'source_units':sorted(units),'canonical_unit':'ns','available_ts':'open + full closed interval','version_note':'fresh October1 retrieval under legacy compatibility directory','official_rest_repairs':repairs}

def funding(asset):
 symbol=asset+'USDT'
 cursor=START//10**6-86400000
 end=END//10**6-1
 sources=[];events=[]
 while cursor<=end:
  url=f'https://fapi.binance.com/fapi/v1/fundingRate?symbol={symbol}&startTime={cursor}&endTime={end}&limit=1000'
  path=CACHE/f'{symbol}-funding-{cursor}-{end}.json'
  body=get(url,path)
  page=json.loads(body)
  assert isinstance(page,list) and page,repr(page)[:500]
  assert all(int(a['fundingTime'])<int(b['fundingTime']) for a,b in zip(page,page[1:]))
  sources.append({'url':url,'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(body).hexdigest(),'rows':len(page)})
  events+=page
  if len(page)<1000:break
  next_cursor=int(page[-1]['fundingTime'])+1
  assert next_cursor>cursor
  cursor=next_cursor
 events=sorted(events,key=lambda x:int(x['fundingTime']))
 assert len({x['fundingTime'] for x in events})==len(events)
 selected=[]
 for i,row in enumerate(events):
  ts=int(row['fundingTime'])*10**6
  if not START<=ts<END:continue
  assert row['symbol']==symbol and Decimal(row['markPrice'])>0 and Decimal(row['fundingRate']).is_finite()
  assert i>0
  # Observed event jitter of a few milliseconds is preserved. Scheduled cycle is 8h.
  gap=(int(row['fundingTime'])-int(events[i-1]['fundingTime']))/3600000
  assert abs(gap-8)<.001,gap
  selected.append({'settlement_ts':ts,'available_ts':ts+HOUR,'realized_rate':Decimal(row['fundingRate']),'mark_price_at_settlement':Decimal(row['markPrice']),'actual_interval_hours':Decimal('8')})
 assert len(selected)==1095,len(selected)
 target=ROOT/'data/normalized/binance'/asset/f'binance_{asset}_{VERSION}'/'funding_settlement.parquet'
 pl.DataFrame(selected).with_columns(*[pl.col(x).cast(pl.Decimal(38,18)) for x in ('realized_rate','mark_price_at_settlement','actual_interval_hours')]).write_parquet(target)
 return {'sources':sources,'normalized':{'path':str(target.relative_to(ROOT)),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'rows':len(selected),'rate_and_mark':'actual Binance API associated funding charge rate and mark, no proxy','event_jitter_preserved':True,'available_ts':'actual funding timestamp + conservative 1-hour publication buffer for any signal input'}}

def metadata(asset,body):
 symbol=asset+'USDT'
 row=next(x for x in body['symbols'] if x['symbol']==symbol)
 filters={x['filterType']:x for x in row['filters']}
 meta={'lot_size':Decimal(filters['LOT_SIZE']['stepSize']),'tick_size':Decimal(filters['PRICE_FILTER']['tickSize']),'min_notional':Decimal(filters['MIN_NOTIONAL']['notional']),'contract_multiplier':Decimal(1)}
 target=ROOT/'data/normalized/binance'/asset/f'binance_{asset}_{VERSION}'/'perp_instrument_meta.parquet'
 pl.DataFrame([meta]).with_columns(*[pl.col(x).cast(pl.Decimal(38,18)) for x in meta]).write_parquet(target)
 return {'path':str(target.relative_to(ROOT)),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'values':{k:str(v) for k,v in meta.items()},'scope':'current Oct1 exchange snapshot; not a historical rule archive'}

def main():
 requests=[]
 for asset in ('BTC','ETH'):
  for category in ('klines','markPriceKlines'):
   for year,months in [(2025,range(9,13)),(2026,range(1,9))]:
    requests.extend((asset,category,f'{year}-{month:02}') for month in months)
   requests.extend((asset,category,f'2026-09-{d:02}',True) for d in range(1,16))
 manifest={'retrieved_at_utc':datetime.now(timezone.utc).isoformat(),'archives':[],'errors':[],'normalized':{},'funding':{},'metadata':{}}
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  jobs={pool.submit(archive,*args):args for args in requests}
  for f in concurrent.futures.as_completed(jobs):
   try:
    value=f.result();manifest['archives'].append(value)
    print(json.dumps({'archives':len(manifest['archives']),'url':value['url']}),flush=True)
   except Exception as error:
    manifest['errors'].append({'request':jobs[f],'error':str(error)})
    print(json.dumps({'error':str(error)}),flush=True)
   (ROUND/'binance_data_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 if manifest['errors']:raise RuntimeError('Incomplete real futures archives; no backtest allowed')
 meta_path=CACHE/'futures_exchange_info_20261001.json'
 meta_bytes=get('https://fapi.binance.com/fapi/v1/exchangeInfo',meta_path)
 meta_body=json.loads(meta_bytes)
 manifest['metadata_snapshot']={'url':'https://fapi.binance.com/fapi/v1/exchangeInfo','path':str(meta_path.relative_to(ROOT)),'sha256':hashlib.sha256(meta_bytes).hexdigest()}
 for asset in ('BTC','ETH'):
  manifest['normalized'][asset]={category:normalized(asset,category,manifest['archives']) for category in ('klines','markPriceKlines')}
  manifest['funding'][asset]=funding(asset)
  manifest['metadata'][asset]=metadata(asset,meta_body)
  (ROUND/'binance_data_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(json.dumps({'normalized':manifest['normalized'],'funding_counts':{a:v['normalized']['rows'] for a,v in manifest['funding'].items()}}),flush=True)

if __name__=='__main__':main()
