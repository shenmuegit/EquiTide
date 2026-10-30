import math,statistics
from decimal import Decimal as D
import numpy as np
from common import core as engine

def near(a,b,tol=1e-9):assert abs(float(a)-float(b))<=tol*max(1,abs(float(a)),abs(float(b))),(a,b)

def metrics(curve,daily,days,saved):
 values=np.asarray(curve);d=np.asarray(daily);rr=d[1:]/d[:-1]-1;sd=np.std(rr,ddof=1);cagr=100*((values[-1]/values[0])**(365/days)-1);dd=float(max(100*(1-values/np.maximum.accumulate(values))));near(saved['net_return_pct'],100*(values[-1]/values[0]-1),1e-12);near(saved['max_drawdown_pct'],dd,1e-12);near(saved['cagr_pct'],cagr,1e-12);near(saved['daily_mark_drawdown_pct'],max(100*(1-d/np.maximum.accumulate(d))),1e-12)
 if sd:near(saved['sharpe_365'],np.mean(rr)/sd*math.sqrt(365),1e-10)
 else:assert saved['sharpe_365'] is None
 if dd:near(saved['calmar'],cagr/dd,1e-10)
 else:assert saved['calmar'] is None

def verify_recent(v,m,z):
 ix=m['daily_indices'];daily=v[ix].tolist();a=ix[330];tail=v[a:];t=z['recent40'];assert t['NAV_points']==len(tail) and t['NAV_sha256_f64le']==hashlib.sha256(tail.astype('<f8').tobytes()).hexdigest() and t['daily_equity_usdt']==daily[330:] and t['initial_NAV_usdt']==v[a] and t['final_NAV_usdt']==v[-1];metrics(tail,daily[330:],40,t)
 for j,f in enumerate(t['folds']):
  l,h=330+5*j,335+5*j;aa,bb=ix[[l,h]];assert f['duration_days']==5 and f['start_utc']==engine.stamp(int(m['ts'][aa])) and f['end_exclusive_utc']==engine.stamp(int(m['ts'][bb]));metrics(v[aa:bb+1],daily[l:h+1],5,f)
 assert len(t['folds'])==8 and abs(math.prod(1+f['net_return_pct']/100 for f in t['folds'])-tail[-1]/tail[0])<1e-12

def independent_margin(m,segments):
 ta=[int(m['ts'][s['axis_start']]) for s in segments];tb=[int(m['ts'][s['axis_end_exclusive']-1]) for s in segments];minimum=None;count=viol=0
 for hour in m['hour'].to_dicts():
  if hour['open_ts']<m['start_ns'] or hour['available_ts']>m['end_ns']:continue
  lo=bisect.bisect_left(tb,hour['open_ts']);hi=bisect.bisect_left(ta,hour['available_ts'])
  for s in segments[lo:hi]:
   q=D(s['signed_units'])
   if not q:continue
   adverse=hour['low'] if q>0 else hour['high'];cushion=D(s['cash'])+q*(adverse-D(s['entry_price']))-D('.01')*abs(q)*adverse;minimum=cushion if minimum is None else min(minimum,cushion);count+=1;viol+=int(cushion<=0)
 return minimum,count,viol
