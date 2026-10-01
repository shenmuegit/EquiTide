"""Fetch official Binance archives and verify their published SHA256 before use."""
import concurrent.futures
import hashlib
import io
import json
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
import polars as pl

ROOT = Path(__file__).resolve().parents[3]
ROUND = Path(__file__).resolve().parent
CACHE = ROOT / 'data/raw/research_20261001T173606'
CACHE.mkdir(parents=True, exist_ok=True)
START = int(datetime(2024,9,16,tzinfo=timezone.utc).timestamp()) * 10**9
END = int(datetime(2025,9,16,tzinfo=timezone.utc).timestamp()) * 10**9
MINUTE = 60 * 10**9
VERSION = '20240916T000000Z_20250916T000000Z_transfer_20261001'
COLS = ['raw_open_ts','open','high','low','close','base_volume','raw_close_ts','quote_volume','trades','taker_base','taker_quote','ignore']


def fetch(asset, period, daily=False):
 symbol = asset+'USDT'
 name = f'{symbol}-1m-{period}.zip'
 url = f'https://data.binance.vision/data/spot/{"daily" if daily else "monthly"}/klines/{symbol}/1m/{name}'
 target = CACHE / name
 for suffix in ('', '.CHECKSUM'):
  path = Path(str(target)+suffix)
  if not path.exists():
   temp = Path(str(path)+'.part')
   p = subprocess.run(['curl','--http1.1','--retry','3','--retry-all-errors','--retry-delay','1','--connect-timeout','10','--max-time','90','-fsSL',url+suffix,'-o',str(temp)],capture_output=True,text=True)
   if p.returncode:
    return {'asset':asset,'url':url+suffix,'error':p.stderr[-1500:],'download_returncode':p.returncode}
   temp.replace(path)
 expected = Path(str(target)+'.CHECKSUM').read_text().split()[0]
 actual = hashlib.sha256(target.read_bytes()).hexdigest()
 if actual != expected:
  raise ValueError(f'Checksum mismatch: {name}')
 return {'asset':asset,'url':url,'path':str(target.relative_to(ROOT)),'sha256':actual,'published_sha256':expected,'bytes':target.stat().st_size}


def main():
 requests=[]
 for asset in ('BTC','ETH'):
  for year, months in [(2024,range(9,13)),(2025,range(1,10))]:
   requests += [(asset,f'{year}-{month:02}') for month in months]
 replay='--reproduce' in sys.argv
 manifest_path=ROOT/'data/runs/reproduce_20261001T173606_manifest.json' if replay else ROUND/'download_manifest.json'
 manifest_path.parent.mkdir(parents=True,exist_ok=True)
 archived=json.loads((ROUND/'download_manifest.json').read_text()) if replay else None
 manifest={'retrieved_at_utc':datetime.now(timezone.utc).isoformat(),'archives':[],'errors':[],'window_start_utc':'2024-09-16T00:00:00Z','window_end_exclusive_utc':'2025-09-16T00:00:00Z'}
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  jobs={pool.submit(fetch,*args):args for args in requests}
  for future in concurrent.futures.as_completed(jobs):
   result=future.result()
   manifest['errors' if 'error' in result else 'archives'].append(result)
   print(json.dumps({'downloaded':len(manifest['archives']),'errors':len(manifest['errors']),'url':result['url']}),flush=True)
   manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
 if manifest['errors']:
  raise RuntimeError('Missing archives; no invented or filled bars permitted')
 manifest['normalized']={}
 for asset in ('BTC','ETH'):
  frames=[]
  units=set()
  for archive in sorted(manifest['archives'],key=lambda x:x['url']):
   if archive['asset'] != asset:
    continue
   with zipfile.ZipFile(ROOT/archive['path']) as z:
    names=z.namelist()
    assert len(names)==1 and names[0].endswith('.csv')
    frame=pl.read_csv(io.BytesIO(z.read(names[0])),has_header=False,new_columns=COLS,infer_schema=False)
   raw=frame['raw_open_ts'].cast(pl.Int64)
   unit='us' if raw[0] > 10**14 else 'ms'
   factor=1000 if unit=='us' else 10**6
   units.add(unit)
   frame=frame.with_columns((pl.col('raw_open_ts').cast(pl.Int64)*factor).alias('open_ts'),(pl.col('raw_close_ts').cast(pl.Int64)*factor).alias('source_close_ts'))
   assert ((frame['source_close_ts']-frame['open_ts']) == MINUTE-factor).all()
   frame=frame.filter((pl.col('open_ts')>=START)&(pl.col('open_ts')<END)).select('open_ts',*[pl.col(c).cast(pl.Decimal(38,18)) for c in ('open','high','low','close','base_volume','quote_volume')])
   frames.append(frame)
  frame=pl.concat(frames).sort('open_ts').with_columns((pl.col('open_ts')+MINUTE).alias('available_ts'),pl.lit(True).alias('is_closed'))
  assert frame.height==365*1440 and frame['open_ts'][0]==START and frame['open_ts'][-1]==END-MINUTE
  assert (frame['open_ts'].diff().drop_nulls()==MINUTE).all()
  assert (frame['base_volume']>=0).all() and (frame['quote_volume']>=0).all()
  assert (frame['low']>0).all() and (frame['high']>=frame['low']).all()
  assert ((frame['open']>=frame['low']) & (frame['open']<=frame['high']) & (frame['close']>=frame['low']) & (frame['close']<=frame['high'])).all()
  path=ROOT/'data/normalized/binance'/asset/f'binance_{asset}_{VERSION}'/'spot_bars.parquet'
  path.parent.mkdir(parents=True,exist_ok=True)
  frame.write_parquet(path)
  manifest['normalized'][asset]={'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'rows':frame.height,'timestamp_source_units':sorted(units),'canonical_timestamp_unit':'ns','available_ts':'minute open + 60 seconds; archive close time verified','path_version_note':'new earlier calendar cache for2025 transfer diagnostic; timestamp units measured per archive'}
 if replay:
  for asset,row in manifest['normalized'].items():
   assert row['sha256']==archived['normalized'][asset]['sha256'],asset
  assert sorted(x['sha256'] for x in manifest['archives'])==sorted(x['sha256'] for x in archived['archives'])
  print('REPRODUCE PASS: published archive hashes and normalized Parquet hashes match',flush=True)
 manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
 print(json.dumps({'normalized':manifest['normalized']}),flush=True)

if __name__=='__main__':
 main()
