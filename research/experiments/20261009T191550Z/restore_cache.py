"""Exact archived same-funded cache recovery only;never rerun old signal/trade rules."""
from pathlib import Path
from decimal import Decimal as D
import gzip,hashlib,json
import numpy as np
import polars as pl
T=Path(__file__).resolve().parent;R=T.parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();nh=lambda v:hashlib.sha256(np.asarray(v,dtype='<f8').tobytes()).hexdigest();plan=json.loads((T/'spec.json').read_text());vectors={};missing=[];checked=0
for ref in plan['read_only_component_refs']:
 assert ref['capital_usdt']==(1500 if ref['asset']=='BTC'else 500)and sha(R/ref['archive'])==ref['archive_sha256']and sha(R/ref['report'])==ref['report_sha256'];a=json.loads(gzip.decompress((R/ref['archive']).read_bytes()));assert a['fingerprint']==ref['fingerprint']and a['spec']['parameters']['initial_capital_usdt']==ref['capital_usdt'];frame=None
 for k,z in a['scenes'].items():
  file=R/'data/runs'/ref['source_round']/f'{ref["name"]}_{k}.npy'
  if not file.exists():
   if frame is None:
    md=plan['periods'][ref['year']]['normalized_data'][ref['asset']];assert sha(R/md['path'])==md['sha256'];frame=pl.read_parquet(R/md['path']);prices=np.asarray(frame['close'].cast(pl.Float64))
   v=np.empty(259382);v[0]=ref['capital_usdt'];coverage=[]
   for st in z['position_segments']:
    cash=D(st['cash']);units=D(st['units'])
    for d in range(st['day_offset'],st['end_day_exclusive']):
     coverage.append(d);i=183+d;v[d*1441+1]=float(cash+units*frame['open'][i*1440+1]);v[d*1441+2:(d+1)*1441+1]=float(cash)+float(units)*prices[i*1440+1:(i+1)*1440+1]
   assert coverage==list(range(180));v[-1]=float(D(z['terminal_cash'])+D(z['terminal_units'])*frame['open'][363*1440+1]);assert nh(v)==z['summary']['NAV_sha256_f64le'];file.parent.mkdir(parents=True,exist_ok=True);np.save(file,v,allow_pickle=False);missing.append(str(file.relative_to(R)))
  v=np.load(file,allow_pickle=False);assert nh(v)==z['summary']['NAV_sha256_f64le'];vectors[ref['fingerprint'],k]=v;checked+=1
for ref in plan['read_only_grid_refs']:
 assert sha(R/ref['archive'])==ref['archive_sha256']and sha(R/ref['report'])==ref['report_sha256'];a=json.loads(gzip.decompress((R/ref['archive']).read_bytes()));fps=[x['fingerprint']for x in a['spec']['components']]
 for k,z in a['scenes'].items():
  v=vectors[fps[0],k]+vectors[fps[1],k];assert nh(v)==z['summary']['NAV_sha256_f64le'];file=R/'data/runs'/ref['source_round']/f'{ref["name"]}_{k}.npy'
  if not file.exists():file.parent.mkdir(parents=True,exist_ok=True);np.save(file,v,allow_pickle=False);missing.append(str(file.relative_to(R)))
  assert np.array_equal(v,np.load(file,allow_pickle=False));checked+=1
assert checked==30
proof={'new_backtests':0,'source_components':6,'read_only_portfolios':4,'scenes_hash_verified':checked,'missing_cache_files_restored':missing,'method':'Reconstruct exact old cash/coin minute NAV or sum1500/500same-funded sources,using same-SHA real prices;no old signals/trades,normalization or gate/status overwrite.'}
if not(T/'cache_recovery.json').exists():(T/'cache_recovery.json').write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps(proof))
