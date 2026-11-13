"""Capture signed completed premium-index daily OHLC; no signal or valuation."""
import gzip,json,subprocess,sys,urllib.parse
from datetime import datetime
from decimal import Decimal as D
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));from common import *
ms=lambda x:int(datetime.fromisoformat(x.replace('Z','+00:00')).timestamp()*1000)
lo=ms('2025-09-16T00:00:00Z');hi=ms('2026-11-12T00:00:00Z');out=R/'premium_raw';out.mkdir();receipts=[]
url='https://fapi.binance.com/fapi/v1/premiumIndexKlines?'+urllib.parse.urlencode(dict(symbol='ETHUSDT',interval='1d',startTime=lo,endTime=hi-1,limit=499))
for attempt in range(3):
 started=now();cmd=['curl','--ipv4','--compressed','--http1.1','--silent','--show-error','--connect-timeout','10','--max-time','30','--write-out','\n%{http_code}',url];z=subprocess.run(cmd,cwd=ROOT,capture_output=True,timeout=40);body,code=z.stdout.rsplit(b'\n',1) if b'\n' in z.stdout else (z.stdout,b'000');path=out/f'ETH_{attempt}.json.gz';path.write_bytes(gzip.compress(body,mtime=0));row=dict(asset='ETH',url=url,started_utc=started,finished_utc=now(),http_status=int(code),curl_exit_code=z.returncode,raw=rel(path),sha256=sha(path),body_sha256=hashlib.sha256(body).hexdigest(),bytes=len(body),stderr=z.stderr.decode(errors='replace'));receipts.append(row);put(R/'premium_transport_attempts.json',receipts)
 if z.returncode==0 and int(code)==200:break
else:raise RuntimeError('Official daily premium unavailable; no dependent strategy calculation')
bars=json.loads(body);assert len(bars)==422 and [x[0] for x in bars]==list(range(lo,hi,86400000))
for b in bars:
 assert len(b)==12 and b[6]+1==b[0]+86400000<=hi
 O,H,L,C=map(D,[b[1],b[2],b[3],b[4]]);assert all(v.is_finite() for v in [O,H,L,C]) and L<=min(O,C)<=max(O,C)<=H
plan=json.loads((ROOT/'research/experiments/20261112T233703Z/plan.json').read_text());f=next(x for x in plan['data']['assets']['ETH'] if x['path'].endswith('perp_bars.parquet'));assert sha(ROOT/f['path'])==f['sha256'];import polars as pl
dates=pl.read_parquet(ROOT/f['path'],columns=['open_ts']).head(422*1440).to_series().gather_every(1440).to_list();assert [t//1000000 for t in dates]==[b[0] for b in bars]
put(R/'premium_data_manifest.json',{'passed':True,'recorded_utc':now(),'asset':'ETH','raw':rel(path),'sha256':sha(path),'daily_bars':422,'start_utc':'2025-09-16T00:00:00Z','end_exclusive_utc':'2026-11-12T00:00:00Z','receipts':receipts,'signed_OHLC_not_positive_price':True,'native_ETH_dates_all_exact':True,'close_field_index':4,'close_time_field_index':6,'ignored_fields_not_volume':[5,7,8,9,10,11],'availability':'Complete UTCdaily closeTime+1<=signal,execute next00:01;historical arrival time assumed atclose','source_url':'https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data','access_utc_date':now()[:10],'new_strategy_or_account_calculations':0,'interpretation':'Signed premium-index closes are a predictive entry proxy,not future realized funding,spot/perp executable basis or observed orderbook.'})
print('PASS422actualsigneddailyETHpremiumbars;closed/finite/OHLC/calendar/SHAchecked;0strategycalculations')
