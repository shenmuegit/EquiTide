"""Read official completed daily taker quote volume; no strategy evaluation."""
import gzip,json,subprocess,sys,urllib.parse
from datetime import datetime
from decimal import Decimal as D
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));from common import *
P=ROOT/'research/experiments/20261112T233703Z'
plan=json.loads((P/'plan.json').read_text());import polars as pl
out=R/'flow_raw';out.mkdir();receipts=[];assets={}
ms=lambda x:int(datetime.fromisoformat(x.replace('Z','+00:00')).timestamp()*1000)
lo=ms('2025-09-16T00:00:00Z');hi=ms('2026-11-12T00:00:00Z')
for asset in ['BTC','ETH']:
 url='https://fapi.binance.com/fapi/v1/klines?'+urllib.parse.urlencode(dict(symbol=asset+'USDT',interval='1d',startTime=lo,endTime=hi-1,limit=499))
 for attempt in range(3):
  started=now();cmd=['curl','--ipv4','--compressed','--http1.1','--silent','--show-error','--connect-timeout','10','--max-time','30','--write-out','\n%{http_code}',url];z=subprocess.run(cmd,cwd=ROOT,capture_output=True,timeout=40);body,code=z.stdout.rsplit(b'\n',1) if b'\n' in z.stdout else (z.stdout,b'000');path=out/f'{asset}_{attempt}.json.gz';path.write_bytes(gzip.compress(body,mtime=0));row=dict(asset=asset,url=url,started_utc=started,finished_utc=now(),http_status=int(code),curl_exit_code=z.returncode,raw=rel(path),sha256=sha(path),body_sha256=hashlib.sha256(body).hexdigest(),bytes=len(body),stderr=z.stderr.decode(errors='replace'));receipts.append(row);put(R/'flow_transport_attempts.json',receipts)
  if z.returncode==0 and int(code)==200:break
 else:raise RuntimeError('Daily flow data unavailable; no dependent evaluation')
 bars=json.loads(body);assert len(bars)==422 and [x[0] for x in bars]==list(range(lo,hi,86400000))
 fp=ROOT/next(x['path'] for x in plan['data']['assets'][asset] if x['path'].endswith('perp_bars.parquet'));frame=pl.read_parquet(fp);daily=frame.head(422*1440).with_columns((pl.col('open_ts')//DAY).alias('day')).group_by('day',maintain_order=True).agg(pl.col('close').last(),pl.col('quote_volume').sum())
 rows=daily.to_dicts()
 for b,d in zip(bars,rows):
  assert len(b)==12 and b[6]+1==b[0]+86400000 and b[6]+1<=hi and d['day']*86400000==b[0]
  assert D(b[4])==d['close'] and D(b[7])==d['quote_volume'] and D(0)<=D(b[10])<=D(b[7]) and D(b[7])>0
 assets[asset]={'raw':rel(path),'sha256':sha(path),'daily_bars':422,'close_and_quote_volume_match_all_minute_aggregates':True,'completed_only':True,'minimum_signal_delay_ns':MIN,'availability':'daily close at day+1 UTC00:00; signal uses only rows closed <= signal available, execution >=00:01','field_indices':{'quote_volume':7,'taker_buy_quote_volume':10}}
put(R/'flow_data_manifest.json',{'passed':True,'recorded_utc':now(),'assets':assets,'receipts':receipts,'new_financial_calculations':0,'source_url':'https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data','access_utc_date':now()[:10],'interpretation':'Taker initiated buy quote share only; not comprehensive signed order flow or contemporaneous execution evidence.'})
print('PASS422completedUTCdays perasset;all844closes/quotevolumes exact;0strategycalculations')
