"""Preserve real minute/hour/funding events and add all hourly execution references."""
import hashlib
import numpy as np
from common import core,MIN,HOUR,DAY

def pack(ts,codes,start):return (np.asarray(ts,dtype=np.int64)-start)*16+np.asarray(codes,dtype=np.int64)

def load(plan):
 native={}
 for asset,files in plan['data']['assets'].items():
  m=core.load_market(asset,files);f=m['frame'];first=int(f['open_ts'][0]);hours=list(range(33*24,403*24));m['first_ns']=first;m['hour_closes']=[f['close'][i*60+59] for i in range(404*24)]
  keep=~np.isin(m['codes'],[5,6,7]);t=[m['ts'][keep]];c=[m['codes'][keep]];px=[m['axis_prices'][keep]];refs=[m['refs'][keep]]
  for code in [5,6,7]:
   t.append(np.array([first+h*HOUR+MIN for h in hours],dtype=np.int64));c.append(np.full(len(hours),code,dtype=np.int8));px.append(np.array([float(f['open'][h*60+1]) for h in hours]));refs.append(np.asarray(hours,dtype=np.int32))
  t,c,px,refs=[np.concatenate(z) for z in [t,c,px,refs]];order=np.lexsort((c,t));m.update(ts=t[order],codes=c[order],axis_prices=px[order],refs=refs[order]);assert len(t)==570543
  dt=np.dtype([('t','<i8'),('k','<i8')]);keys=np.empty(len(t),dtype=dt);keys['t']=m['ts'];keys['k']=m['codes'];m['structured_keys']=keys;native[asset]=m
 union=np.union1d(native['BTC']['structured_keys'],native['ETH']['structured_keys']);ts=union['t'];codes=union['k'];S=native['BTC']['start_ns'];E=native['BTC']['end_ns'];first=native['BTC']['first_ns'];packed=pack(ts,codes,S);axis_sha=hashlib.sha256(packed.astype('<i8').tobytes()).hexdigest();daily_pre=np.flatnonzero((codes==5)&((ts-first-MIN)%DAY==0));assert len(daily_pre)==370;daily=np.array([0,*daily_pre[1:],len(ts)-1]);folds=np.array([0,*daily_pre[np.arange(30,370,30)],len(ts)-1]);controls=np.flatnonzero(np.isin(codes,[4,6,7,9]))
 for asset,m in native.items():
  old=m['structured_keys'];j=np.searchsorted(old,union,side='right')-1;assert (j>=0).all() and ((old[j]['t']<ts)|((old[j]['t']==ts)&(old[j]['k']<=codes))).all();prices=m['axis_prices'][j];m.update(ts=ts,codes=codes,axis_prices=prices,axis_sha256=axis_sha,axis_price_sha256_f64le=core.navhash(prices),daily_indices=daily,fold_indices=folds,controls=controls,fund_lookup={x['settlement_ts']:x for x in m['funds']},terminal_reference_decimal=m['frame']['open'][403*1440+1])
 return native,{'ts':ts,'codes':codes,'daily_indices':daily,'fold_indices':folds,'controls':controls,'start_ns':S,'end_ns':E,'first_ns':first,'axis_sha256':axis_sha,'keys':union}
