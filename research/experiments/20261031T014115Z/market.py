import hashlib
import numpy as np
from common import *
def load(plan):
 ms={a:core.load_market(a,fs) for a,fs in plan['data']['assets'].items()};dt=np.dtype([('t','<i8'),('k','<i8')]);keys={}
 for a,m in ms.items():
  z=np.empty(len(m['ts']),dtype=dt);z['t']=m['ts'];z['k']=m['codes'];keys[a]=z;m['native_axis_sha256']=m['axis_sha256'];m['native_keys']=z
 union=np.union1d(keys['BTC'],keys['ETH']);ts=union['t'];codes=union['k'];first=int(ms['BTC']['frame']['open_ts'][0]);start=ms['BTC']['start_ns'];pre=np.flatnonzero(codes==5);daily=np.array([0,*pre[1:],len(ts)-1]);folds=np.array([0,*pre[np.arange(30,370,30)],len(ts)-1]);controls=np.flatnonzero(np.isin(codes,[4,6,7,9]));ash=hashlib.sha256(((ts-start)*16+codes).astype('<i8').tobytes()).hexdigest()
 for a,m in ms.items():
  j=np.searchsorted(keys[a],union,side='right')-1;assert (j>=0).all();px=m['axis_prices'][j];m.update(ts=ts,codes=codes,axis_prices=px,axis_sha256=ash,axis_price_sha256_f64le=core.navhash(px),daily_indices=daily,fold_indices=folds,controls=controls,first_ns=first,fund_lookup={x['settlement_ts']:x for x in m['funds']},terminal_reference_decimal=m['frame']['open'][403*1440+1])
 axis={'ts':ts,'codes':codes,'keys':union,'daily_indices':daily,'fold_indices':folds,'controls':controls,'first_ns':first,'start_ns':start,'end_ns':ms['BTC']['end_ns'],'axis_sha256':ash};assert len(pre)==370 and len(daily)==371 and len(folds)==14;return ms,axis
