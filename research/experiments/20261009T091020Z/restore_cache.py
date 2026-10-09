"""Rebuild only exact archived ETH NAV caches when missing;no old signal/trade backtest."""
from pathlib import Path
from decimal import Decimal as D
import gzip,hashlib,json,sys
import numpy as np
import polars as pl
T=Path(__file__).resolve().parent;R=T.parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();nh=lambda v:hashlib.sha256(np.asarray(v,dtype='<f8').tobytes()).hexdigest()
plan=json.loads((T/'spec.json').read_text());missing=[];checked=0
for ref in plan['read_only_component_refs']:
 assert ref['asset']=='ETH' and ref['capital_usdt']==500 and sha(R/ref['archive'])==ref['archive_sha256'] and sha(R/ref['report'])==ref['report_sha256'];a=json.loads(gzip.decompress((R/ref['archive']).read_bytes()));assert a['fingerprint']==ref['fingerprint'] and a['spec']['parameters']['initial_capital_usdt']==500;frame=None
 for k,z in a['scenes'].items():
  file=R/'data/runs'/ref['source_round']/f'{ref["name"]}_{k}.npy'
  if not file.exists():
   if frame is None:
    data=plan['periods'][ref['year']]['normalized_data']['ETH'];assert sha(R/data['path'])==data['sha256'];frame=pl.read_parquet(R/data['path']);prices=np.asarray(frame['close'].cast(pl.Float64))
   v=np.empty(259382);v[0]=500;coverage=[]
   for st in z['position_segments']:
    cash=D(st['cash']);units=D(st['units'])
    for d in range(st['day_offset'],st['end_day_exclusive']):
     coverage.append(d);i=183+d;v[d*1441+1]=float(cash+units*frame['open'][i*1440+1]);v[d*1441+2:(d+1)*1441+1]=float(cash)+float(units)*prices[i*1440+1:(i+1)*1440+1]
   assert coverage==list(range(180));v[-1]=float(D(z['terminal_cash'])+D(z['terminal_units'])*frame['open'][363*1440+1]);assert nh(v)==z['summary']['NAV_sha256_f64le'];file.parent.mkdir(parents=True,exist_ok=True);np.save(file,v,allow_pickle=False);missing.append(str(file.relative_to(R)))
  assert nh(np.load(file,allow_pickle=False))==z['summary']['NAV_sha256_f64le'];checked+=1
assert checked==6
proof={'new_backtests':0,'source_components':2,'scenes_hash_verified':checked,'missing_cache_files_restored':missing,'method':'Exact archived cash/units and same-SHA real minute-price reconstruction,no source signal/trade rerun or fund scaling.'}
if not (T/'cache_recovery.json').exists():(T/'cache_recovery.json').write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps(proof))
