"""Official bounded funding-history reads and definition-only exact component lookup."""
import gzip, json, subprocess, sys, urllib.parse
from datetime import datetime, timezone
from pathlib import Path
R=Path(__file__).resolve().parents[1]; ROOT=R.parents[2]
sys.path.insert(0,str(R));from common import *
ms=lambda s:int(datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()*1000)
lo=ms('2026-11-12T16:30:00Z');hi=ms('2026-11-12T20:10:00Z')
out=R/'window_funding_preflight';out.mkdir();receipts=[];fields={}
for asset in ['BTC','ETH']:
 url='https://fapi.binance.com/fapi/v1/fundingRate?'+urllib.parse.urlencode({'symbol':asset+'USDT','startTime':lo+1,'endTime':hi,'limit':1000})
 for attempt in range(3):
  started=now();cmd=['curl','--ipv4','--compressed','--http1.1','--silent','--show-error','--connect-timeout','10','--max-time','30','--write-out','\n%{http_code}',url];z=subprocess.run(cmd,cwd=ROOT,capture_output=True,timeout=40);body,code=z.stdout.rsplit(b'\n',1) if b'\n' in z.stdout else (z.stdout,b'000');path=out/f'{asset}_{attempt}.json.gz';path.write_bytes(gzip.compress(body,mtime=0));rec={'asset':asset,'url':url,'started_utc':started,'finished_utc':now(),'http_status':int(code),'curl_exit_code':z.returncode,'raw':rel(path),'sha256':sha(path),'body_sha256':hashlib.sha256(body).hexdigest(),'bytes':len(body),'stderr':z.stderr.decode(errors='replace')};receipts.append(rec);put(R/'window_funding_preflight_attempts.json',receipts)
  if z.returncode==0 and int(code)==200:
   rows=json.loads(body);assert isinstance(rows,list) and all(v['symbol']==asset+'USDT' and lo<v['fundingTime']<=hi for v in rows);fields[asset]=rows;break
 else:raise RuntimeError('Official funding preflight blocked; no dependent account calculation')
put(R/'window_funding_preflight.json',{'passed':True,'recorded_utc':now(),'start_exclusive_utc':'2026-11-12T16:30:00Z','end_inclusive_utc':'2026-11-12T20:10:00Z','public_fields_by_asset':fields,'raw_responses':receipts,'new_GETs':len(receipts),'financial_or_account_calculations':0,'scope':'Actual public settlement timestamps determine windows; nominal eight-hour schedule not assumed.'})
print('PASS actual closed-window funding capture',fields,flush=True)
