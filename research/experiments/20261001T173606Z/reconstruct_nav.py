"""Reconstruct archived minute NAV cache from frozen positions, without new trials."""
import gzip
import hashlib
import json
from decimal import Decimal as D
from pathlib import Path
import numpy as np
import polars as pl

ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
report=json.loads((ROUND/'report.json').read_text());batch=json.loads((ROUND/'batch.json').read_text())
cache=ROOT/'data/runs'/ROUND.name;cache.mkdir(parents=True,exist_ok=True)
frames={}
for asset,p in report['data'].items():
    path=ROOT/p['path'];assert hashlib.sha256(path.read_bytes()).hexdigest()==p['sha256']
    frames[asset]=pl.read_parquet(path,columns=['open','close'])
vectors={};created=0
for b in batch:
    row=report['configs'][b['name']];path=ROOT/row['archive']
    assert hashlib.sha256(path.read_bytes()).hexdigest()==row['archive_sha256']
    a=json.loads(gzip.decompress(path.read_bytes()))
    for k,s in a['scenes'].items():
        if a['spec']['kind']=='strategy':
            asset=a['spec']['universe'][0].split('/')[0];frame=frames[asset];closes=np.asarray(frame['close'].cast(pl.Float64))
            v=np.empty(259382);v[0]=a['spec']['parameters']['initial_capital_usdt']
            for state in s['position_segments']:
                c=D(state['cash']);u=D(state['units'])
                for d in range(state['day_offset'],state['end_day_exclusive']):
                    i=183+d;v[d*1441+1]=float(c+u*frame['open'][i*1440+1])
                    v[d*1441+2:(d+1)*1441+1]=float(c)+float(u)*closes[i*1440+1:(i+1)*1440+1]
            v[-1]=float(D(s['terminal_cash'])+D(s['terminal_units'])*frame['open'][363*1440+1])
        else:
            names=s['component_names'];v=vectors[(names[0],k)]+vectors[(names[1],k)]
        expected=s['summary']['NAV_sha256_f64le']
        assert hashlib.sha256(v.astype('<f8').tobytes()).hexdigest()==expected,(b['name'],k)
        dest=cache/f'{b["name"]}_{k}.npy'
        if dest.exists():assert np.array_equal(np.load(dest,allow_pickle=False),v),'Existing different NAV preserved: '+str(dest)
        else:np.save(dest,v,allow_pickle=False);created+=1
        vectors[(b['name'],k)]=v
print(f'PASS:90 archived complete NAV vectors reconstructed and SHA-verified;created{created} missing local cache files;no strategy calculation or ledger mutation')
