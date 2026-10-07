"""Reconstruct missing exact read-only NAV caches from archived balances and real prices."""
import gzip,hashlib,json,sys
from pathlib import Path
from decimal import Decimal as D
import numpy as np
import polars as pl
T=Path(__file__).resolve().parent;R=T.parents[2];SPAN=1441;POINTS=259382
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
nh=lambda v:hashlib.sha256(np.asarray(v,dtype='<f8').tobytes()).hexdigest()
p=json.loads((T/'spec.json').read_text());batch=json.loads((T/'grid_batch.json').read_text());prices={};daily={};vectors={};restored=[]
for y,part in p['periods'].items():
 daily[y]=json.loads(gzip.decompress((R/'research/experiments'/part['source_round']/'daily_inputs.json.gz').read_bytes()))
 for asset,md in part['normalized_data'].items():
  path=R/md['path'];assert sha(path)==md['sha256'];prices[y,asset]=np.asarray(pl.read_parquet(path,columns=['close'])['close'].cast(pl.Float64))
for b in batch:
 if b['is_new']:continue
 ref=b['source_ref'];archive=R/ref['archive'];assert sha(archive)==ref['archive_sha256'];a=json.loads(gzip.decompress(archive.read_bytes()));assert a['fingerprint']==b['fingerprint']
 for k,s in a['scenes'].items():
  if b['role']=='component':
   capital=a['spec']['parameters']['initial_capital_usdt'];v=np.empty(POINTS);v[0]=capital;rows=daily[b['year']][b['asset']];marks=prices[b['year'],b['asset']]
   states={d:z for z in s['position_segments'] for d in range(z['day_offset'],z['end_day_exclusive'])};assert sorted(states)==list(range(180))
   for d,i in enumerate(range(183,363)):
    z=states[d];cash=D(z['cash']);units=D(z['units']);v[d*SPAN+1]=float(cash+units*D(str(rows[i]['trade_open'])));v[d*SPAN+2:(d+1)*SPAN+1]=float(cash)+float(units)*marks[i*1440+1:(i+1)*1440+1]
   v[-1]=float(D(s['terminal_cash'])+D(s['terminal_units'])*D(str(rows[363]['trade_open'])))
  else:v=sum(vectors[c['fingerprint'],k] for c in a['spec']['components'])
  assert nh(v)==s['summary']['NAV_sha256_f64le'],b['name'];path=R/'data/runs'/ref['source_round']/f'{b["name"]}_{k}.npy';path.parent.mkdir(parents=True,exist_ok=True)
  if path.exists():assert nh(np.load(path,allow_pickle=False))==nh(v)
  else:np.save(path,v,allow_pickle=False);restored.append(str(path.relative_to(R)))
  vectors[b['fingerprint'],k]=v
note={'new_backtests':0,'read_only_scenes_reconstructed_and_hash_verified':len(vectors),'missing_cache_files_restored':restored,'source_sha256':sha(Path(__file__)),'method':'Archived exact cash/units segments and same-SHA real minute closes;no signal/trade rerun or NAV scaling'}

if not (T/'cache_recovery.json').exists():(T/'cache_recovery.json').write_text(json.dumps(note,indent=2)+'\n')
print(json.dumps({'new_backtests':0,'read_only_scenes_hash_verified':len(vectors),'missing_files_restored':len(restored)}))
