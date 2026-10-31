"""Capture only real closed daily warmup; no financial calculation or strategy signal."""
import datetime,gzip,hashlib,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parent
start=int(datetime.datetime(2025,9,13,tzinfo=datetime.timezone.utc).timestamp()*1000);end=int(datetime.datetime(2025,9,17,tzinfo=datetime.timezone.utc).timestamp()*1000)-1
url=f'https://fapi.binance.com/fapi/v1/klines?symbol=ETHUSDT&interval=1d&startTime={start}&endTime={end}&limit=10'
raw=R/'warmup_raw.json';cmd=['curl','-4','--silent','--show-error','--connect-timeout','10','--max-time','30','--retry','1','--retry-delay','1','--fail-with-body',url]
p=subprocess.run(cmd,capture_output=True)
(R/'warmup_raw.json.gz').write_bytes(gzip.compress(p.stdout,mtime=0));(R/'warmup_stderr.log').write_bytes(p.stderr)
proof={'argv':cmd,'actual_exit_code':p.returncode,'raw_response_gz_sha256':hashlib.sha256((R/'warmup_raw.json.gz').read_bytes()).hexdigest(),'uncompressed_sha256':hashlib.sha256(p.stdout).hexdigest(),'received_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
(R/'warmup_capture.json').write_text(json.dumps(proof,indent=2)+'\n');assert p.returncode==0,p.stderr
rows=json.loads(p.stdout);assert len(rows)==4 and [x[0] for x in rows]==[start+i*86400000 for i in range(4)]
for x in rows:assert x[6]==x[0]+86400000-1 and float(x[4])>0 and float(x[7])>=0
print(json.dumps({'rows':len(rows),'dates':[datetime.datetime.fromtimestamp(x[0]/1000,datetime.timezone.utc).isoformat() for x in rows],'actual_exit_code':p.returncode}),flush=True)
