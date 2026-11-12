import gzip,hashlib,json,subprocess,urllib.parse
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z');put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');missing=json.loads((R/'review/BTC_coverage_before_gap_source.json').read_text())['missing_hours'];folder=R/'mark_hour_gap_raw';folder.mkdir();records=[]
for a in ['BTC','ETH']:
 url='https://fapi.binance.com/fapi/v1/markPriceKlines?'+urllib.parse.urlencode({'symbol':a+'USDT','interval':'1h','startTime':missing[0]//1000000,'endTime':(missing[-1]+3600000000000)//1000000-1,'limit':1500})
 for attempt in range(3):
  start=now();cmd=['curl','--ipv4','--compressed','--http1.1','--silent','--show-error','--connect-timeout','10','--max-time','30','--write-out','\n%{http_code}',url];p=subprocess.run(cmd,cwd=ROOT,capture_output=True,timeout=65);body,code=p.stdout.rsplit(b'\n',1) if b'\n' in p.stdout else (p.stdout,b'000');path=folder/(a+'_'+str(attempt)+'.json.gz');path.write_bytes(gzip.compress(body,mtime=0));row={'asset':a,'url':url,'started_utc':start,'retrieved_utc':now(),'http_status':int(code),'curl_exit_code':p.returncode,'raw':str(path.relative_to(ROOT)),'sha256':sha(path),'raw_response_sha256':hashlib.sha256(body).hexdigest(),'bytes':len(body),'stderr':p.stderr.decode(errors='replace')};records.append(row);put(R/'mark_hour_gap_receipts.json',records)
  if p.returncode==0 and int(code)==200:
   rows=json.loads(body);assert [int(x[0])*1000000 for x in rows]==missing and len(rows)==47 and all((int(x[6])+1-int(x[0]))==3600000 for x in rows);break
 else:raise RuntimeError('Missing real mark-hour official capture failed3attempts; no financial calculation allowed')
put(R/'mark_hour_gap_source.json',{'passed':True,'recorded_utc':now(),'receipts':records,'hours_per_asset':47,'missing_hour_ns':missing,'new_public_GETs':len(records),'financial_or_account_calculations':0,'interpolated_rows':0});print(json.dumps({'official_raw_gap_hours_per_asset':47,'GETs':len(records),'financial_or_account_calculations':0}),flush=True)
