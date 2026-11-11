"""Read-only fresh nominal Nov11 16 funding official funding fields; no strategy/account calculation."""
import gzip,hashlib,json,subprocess,urllib.parse
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z');put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
assert not (R/'funding16_nov11_preflight.json').exists();rawdir=R/'funding16_nov11_preflight';rawdir.mkdir();records=[];fields={};nominal=int(datetime(2026,11,11,16,tzinfo=timezone.utc).timestamp())*1000
for asset in ['BTC','ETH']:
 url='https://fapi.binance.com/fapi/v1/fundingRate?'+urllib.parse.urlencode({'symbol':asset+'USDT','startTime':nominal-1000,'endTime':nominal+1000,'limit':1000})
 for attempt in range(3):
  start=now();cmd=['curl','--ipv4','--compressed','--http1.1','--silent','--show-error','--connect-timeout','10','--max-time','30','--write-out','\n%{http_code}',url];p=subprocess.run(cmd,cwd=ROOT,capture_output=True,timeout=65);body,code=p.stdout.rsplit(b'\n',1) if b'\n' in p.stdout else (p.stdout,b'000');path=rawdir/(asset+'_'+str(attempt)+'.json.gz');path.write_bytes(gzip.compress(body,mtime=0));z={'asset':asset,'url':url,'started_utc':start,'http_status':int(code),'curl_exit_code':p.returncode,'raw':str(path.relative_to(ROOT)),'sha256':sha(path),'bytes':len(body),'stderr':p.stderr.decode(errors='replace')};records.append(z);put(R/'funding16_nov11_preflight_receipts.json',records)
  if p.returncode==0 and int(code)==200:
   rows=json.loads(body);assert isinstance(rows,list) and len(rows)==1 and rows[0]['symbol']==asset+'USDT' and abs(int(rows[0]['fundingTime'])-nominal)<=1000 and all(k in rows[0] for k in ['fundingTime','fundingRate','markPrice']);fields[asset]=rows;break
 else:raise RuntimeError('Actual public Nov11_16 funding funding capture failed three bounded attempts')
put(R/'funding16_nov11_preflight.json',{'recorded_utc':now(),'account_or_strategy_calculations':0,'nominal_UTC':'2026-11-11T16:00:00Z','public_fields_by_asset':fields,'scope':'Fresh genuine official settlement fields only. Preserve actual millisecond fundingTime; no ownq/cashflow or strategy evaluation. L4/FEWM still reserve before own original advance. Not oldNov11_00 orNov10_00/16/16 rates/marks or any other account cashflows.'});print(json.dumps({'public_fields_by_asset':fields,'actual_GETs':len(records),'failed_GETs':sum(x['curl_exit_code']!=0 or x['http_status']!=200 for x in records),'account_or_strategy_calculations':0}),flush=True)
