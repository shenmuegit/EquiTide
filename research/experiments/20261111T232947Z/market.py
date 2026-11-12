"""Real later-period data loader and causal union event-axis alignment; no strategy valuation."""
import hashlib,json,math,statistics
import numpy as np
import polars as pl
from decimal import Decimal as D
from common import *
def native_market(asset,files):
 frames={}
 for z in files:
  p=ROOT/z['path'];assert sha(p)==z['sha256'] and p.stat().st_size==z['bytes'];frames[p.stem]=pl.read_parquet(p)
 f,h,fu=frames['perp_bars'],frames['mark_hour_bars'],frames['funding_settlement'];meta=frames['perp_instrument_meta'].to_dicts()[0];assert meta['contract_multiplier']==1
 assert f.height==51*1440+2 and f['is_closed'].all() and (f['open_ts'].diff().drop_nulls()==MIN).all() and (f['available_ts']-f['open_ts']==MIN).all();assert h.height==51*24 and h['is_closed'].all() and (h['available_ts']-h['open_ts']==HOUR).all() and (h['open_ts'].diff().drop_nulls()==HOUR).all()
 assert (f['open']>0).all() and (f['close']>0).all() and (f['quote_volume']>=0).all() and (h['low']>0).all() and (h['high']>=h['low']).all();daily=f.with_columns((pl.col('open_ts')//DAY).alias('day')).group_by('day',maintain_order=True).agg(pl.col('close').last().alias('close'),pl.col('quote_volume').sum().alias('quote_volume'),pl.len().alias('bars')).sort('day');rows=daily.to_dicts();assert len(rows)==52 and all(x['bars']==1440 for x in rows[:51]) and rows[51]['bars']==2;prices=[x['close'] for x in rows];first=int(f['open_ts'][0]);S=first+START*DAY+MIN;E=first+END*DAY+MIN;assert core.stamp(first)=='2026-09-21T00:00:00Z' and core.stamp(S)=='2026-10-24T00:01:00Z' and core.stamp(E)=='2026-11-11T00:01:00Z'
 allfunds=fu.to_dicts();assert all(x['available_ts']-x['settlement_ts']==HOUR and x['mark_price_at_settlement']>0 and x['actual_interval_hours']>0 for x in allfunds);signal=[{**x,'source_index':j,'entry_interval_hours':D(x['settlement_ts']-allfunds[j-1]['settlement_ts'])/D(HOUR) if j and allfunds[j-1]['available_ts']<=x['available_ts'] else None} for j,x in enumerate(allfunds)];funds=[x for x in signal if S<x['settlement_ts']<=E];assert len(funds)==json.loads((R/'cohort_inputs.json').read_text())['counts'][asset]['OOS_funding_rows']
 parts=[]
 def add(ts,code,px,refs):
  ts=np.atleast_1d(np.asarray(ts,dtype=np.int64));n=len(ts);parts.append((ts,np.full(n,code,dtype=np.int8),np.atleast_1d(np.asarray(px,dtype=np.float64)),np.atleast_1d(np.asarray(refs,dtype=np.int32))));assert all(len(x)==n for x in parts[-1])
 lo,hi=START*1440+1,END*1440+1;add(S,0,float(f['open'][lo]),-1);add(np.asarray(f['available_ts'][lo:hi]),1,[float(x) for x in f['close'][lo:hi]],np.arange(lo,hi));hs=[j for j,x in enumerate(h['available_ts']) if S<int(x)<=E];add([int(h['available_ts'][j]) for j in hs],2,[float(h['close'][j]) for j in hs],hs)
 for code in [3,4]:add([x['settlement_ts'] for x in funds],code,[float(x['mark_price_at_settlement']) for x in funds],np.arange(len(funds)))
 for code in [5,6,7]:add([first+i*DAY+MIN for i in range(START,END)],code,[float(f['open'][i*1440+1]) for i in range(START,END)],np.arange(START,END))
 for code in [8,9]:add(E,code,float(f['open'][hi]),END)
 ts,codes,px,refs=[np.concatenate([x[j] for x in parts]) for j in range(4)];order=np.lexsort((codes,ts));ts,codes,px,refs=[x[order] for x in [ts,codes,px,refs]];pre=np.flatnonzero(codes==5);assert len(pre)==DAYS and len(ts)==1+18*1440+len(hs)+2*len(funds)+18*3+2 and np.all(np.diff(ts)>=0);axis_sha=hashlib.sha256(ts.astype('<i8').tobytes()+codes.tobytes()+refs.astype('<i4').tobytes()).hexdigest();controls=np.flatnonzero(np.isin(codes,[4,6,7,9]));daily_idx=np.asarray([0,*pre[1:],len(ts)-1],dtype=int);bounds=np.asarray([0,*pre[np.arange(3,DAYS,3)],len(ts)-1],dtype=int);cost_inputs={}
 for i in range(START,END+1):
  adv=statistics.mean(float(x['quote_volume']) for x in rows[i-20:i]);rr=[math.log(float(prices[j])/float(prices[j-1])) for j in range(i-20,i)];cost_inputs[i]=(D(str(adv)),D(str(statistics.stdev(rr))))
 return {'asset':asset,'frame':f,'hour':h,'funds':funds,'meta':meta,'rows':rows,'closes':prices,'ts':ts,'codes':codes,'axis_prices':px,'refs':refs,'controls':controls,'daily_indices':daily_idx,'fold_indices':bounds,'cost_inputs':cost_inputs,'start_ns':S,'end_ns':E,'axis_sha256':axis_sha,'axis_price_sha256_f64le':core.navhash(px),'signal_funds':signal,'first_ns':first,'fund_lookup':{x['settlement_ts']:x for x in funds},'terminal_reference_decimal':f['open'][hi]}
def load(plan):
 ms={a:native_market(a,fs) for a,fs in plan['data']['assets'].items()};start=ms['BTC']['start_ns'];end=ms['BTC']['end_ns'];keys={a:(m['ts']-start)*16+m['codes'] for a,m in ms.items()};union=np.union1d(keys['BTC'],keys['ETH']);project={a:np.searchsorted(ks,union,side='right')-1 for a,ks in keys.items()};assert all((ix>=0).all() and (ix<len(ms[a]['ts'])).all() and np.all(keys[a][ix]<=union) for a,ix in project.items());daily=np.array([0,*[np.searchsorted(union,j*DAY*16+5) for j in range(1,DAYS)],len(union)-1],dtype=int);fold=np.array([daily[j] for j in [0,3,6,9,12,15,18]],dtype=int);assert len(daily)==19 and len(fold)==7 and union[0]==0 and union[-1]==(end-start)*16+9
 cm={'keys':union,'sha256':hashlib.sha256(union.astype('<i8').tobytes()).hexdigest(),'projections':project,'daily_indices':daily,'fold_indices':fold,'start_ns':start,'end_ns':end};return ms,cm
