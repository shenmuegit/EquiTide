"""Hash-verified cache reconstruction only;no source signals or trades rerun."""
import gzip,hashlib,json,sys
from pathlib import Path
from decimal import Decimal as D
import numpy as np
import polars as pl
R=Path(__file__).resolve().parents[3];T=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
nh=lambda v:hashlib.sha256(np.asarray(v,dtype='<f8').tobytes()).hexdigest()
plan=json.loads((T/'spec.json').read_text());grid=json.loads((T/'grid_batch.json').read_text());prices={};daily={};vectors={};restored=[];checked=0
for y,p in plan['periods'].items():
 daily[y]=json.loads(gzip.decompress((R/'research/experiments'/p['source_round']/'daily_inputs.json.gz').read_bytes()))
 for asset,md in p['normalized_data'].items():
  path=R/md['path'];assert sha(path)==md['sha256'];prices[y,asset]=np.asarray(pl.read_parquet(path,columns=['close'])['close'].cast(pl.Float64))
refs={r['fingerprint']:{**r,'year':b['year']} for b in grid for r in b['component_refs']}
for fp,ref in refs.items():
 assert sha(R/ref['archive'])==ref['archive_sha256'] and sha(R/ref['report'])==ref['report_sha256']
 a=json.loads(gzip.decompress((R/ref['archive']).read_bytes()));assert a['fingerprint']==fp and registry.fingerprint(a['spec'])==fp
 for k,s in a['scenes'].items():
  v=np.empty(259382);v[0]=ref['capital_usdt'];rows=daily[ref['year']][ref['asset']];marks=prices[ref['year'],ref['asset']]
  states={d:z for z in s['position_segments'] for d in range(z['day_offset'],z['end_day_exclusive'])};assert sorted(states)==list(range(180))
  for d,i in enumerate(range(183,363)):
   z=states[d];cash=D(z['cash']);units=D(z['units']);v[d*1441+1]=float(cash+units*D(str(rows[i]['trade_open'])));v[d*1441+2:(d+1)*1441+1]=float(cash)+float(units)*marks[i*1440+1:(i+1)*1440+1]
  v[-1]=float(D(s['terminal_cash'])+D(s['terminal_units'])*D(str(rows[363]['trade_open'])));assert nh(v)==s['summary']['NAV_sha256_f64le']
  path=R/'data/runs'/ref['source_round']/f'{ref["name"]}_{k}.npy';path.parent.mkdir(parents=True,exist_ok=True)
  if path.exists():assert nh(np.load(path,allow_pickle=False))==nh(v)
  else:np.save(path,v,allow_pickle=False);restored.append(str(path.relative_to(R)))
  vectors[fp,k]=v;checked+=1
for b in grid:
 if b['is_new']:continue
 ref=b['source_ref'];a=json.loads(gzip.decompress((R/ref['archive']).read_bytes()));assert sha(R/ref['archive'])==ref['archive_sha256'] and a['fingerprint']==b['fingerprint']
 for k,s in a['scenes'].items():
  v=sum(vectors[c['fingerprint'],k] for c in a['spec']['components']);assert nh(v)==s['summary']['NAV_sha256_f64le'];checked+=1
  path=R/'data/runs'/ref['source_round']/f'{b["name"]}_{k}.npy'
  if path.exists():assert nh(np.load(path,allow_pickle=False))==nh(v)
  else:np.save(path,v,allow_pickle=False);restored.append(str(path.relative_to(R)))
assert len(refs)==12 and checked==78
note={'new_backtests':0,'source_components':12,'component_scenes':36,'existing_combination_scenes':42,'scenes_hash_verified':checked,'missing_cache_files_restored':restored,'source_sha256':sha(Path(__file__)),'method':'Reconstruct exact archived cash/units minute NAV from same-SHA real data;no old signal/trade reevaluation,capital scaling or criterion overwrite.'}
if not (T/'cache_recovery.json').exists():(T/'cache_recovery.json').write_text(json.dumps(note,indent=2)+'\n')
print(json.dumps({'new_backtests':0,'readonly_scenes_verified':checked,'missing_files_restored':len(restored)}))
