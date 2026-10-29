"""Exact original independent utility bodies;no obsolete native-grid import dependency."""
import bisect,copy,gzip,hashlib,json,math,statistics
from decimal import Decimal as D,ROUND_CEILING,ROUND_FLOOR
from fractions import Fraction as F
import numpy as np
import engine

def near(a,b,tol=1e-9):assert abs(float(a)-float(b))<=tol*max(1,abs(float(a)),abs(float(b))),(a,b)

def metrics(curve,daily,days,saved):
 values=np.asarray(curve);d=np.asarray(daily);rr=d[1:]/d[:-1]-1;sd=np.std(rr,ddof=1);cagr=100*((values[-1]/values[0])**(365/days)-1);dd=float(max(100*(1-values/np.maximum.accumulate(values))));near(saved['net_return_pct'],100*(values[-1]/values[0]-1),1e-12);near(saved['max_drawdown_pct'],dd,1e-12);near(saved['cagr_pct'],cagr,1e-12);near(saved['daily_mark_drawdown_pct'],max(100*(1-d/np.maximum.accumulate(d))),1e-12)
 if sd:near(saved['sharpe_365'],np.mean(rr)/sd*math.sqrt(365),1e-10)
 else:assert saved['sharpe_365'] is None
 if dd:near(saved['calmar'],cagr/dd,1e-10)
 else:assert saved['calmar'] is None

def verify_axis(m):
 f,h=m['frame'],m['hour'];codes=m['codes'];ts=m['ts'];S,E=m['start_ns'],m['end_ns'];assert len(ts)==545013 and np.all(np.diff(ts)>=0) and np.array_equal(np.lexsort((codes,ts)),np.arange(len(ts)))
 for code in range(10):assert np.all(m['axis_prices'][codes==code]>0)
 ix=np.flatnonzero(codes==1);assert len(ix)==532800 and ts[ix].tolist()==f['available_ts'][engine.START*1440+1:engine.END*1440+1].to_list();assert np.array_equal(m['axis_prices'][ix],np.asarray([float(x) for x in f['close'][engine.START*1440+1:engine.END*1440+1]]))
 for code in [5,6,7]:
  ix=np.flatnonzero(codes==code);assert len(ix)==370 and ts[ix].tolist()==[S+i*engine.DAY for i in range(370)]
  assert m['axis_prices'][ix].tolist()==[float(f['open'][i*1440+1]) for i in range(engine.START,engine.END)]
 for code in [3,4]:
  ix=np.flatnonzero(codes==code);assert len(ix)==1110 and ts[ix].tolist()==[e['settlement_ts'] for e in m['funds']]
  assert m['axis_prices'][ix].tolist()==[float(e['mark_price_at_settlement']) for e in m['funds']]
 ix=np.flatnonzero(codes==2);expected=[j for j,z in enumerate(h['available_ts']) if S<int(z)<=E];assert len(ix)==8880 and ts[ix].tolist()==[int(h['available_ts'][j]) for j in expected];assert len(m['controls'])==1851 and len(m['daily_indices'])==371 and len(m['fold_indices'])==14
 assert ts[0]==S and ts[-1]==E and codes[0]==0 and codes[-1]==9

def verify_recent(v,m,z):
 ix=m['daily_indices'];daily=v[ix].tolist();a=ix[330];tail=v[a:];t=z['recent40'];assert t['NAV_points']==len(tail) and t['NAV_sha256_f64le']==hashlib.sha256(tail.astype('<f8').tobytes()).hexdigest() and t['daily_equity_usdt']==daily[330:] and t['initial_NAV_usdt']==v[a] and t['final_NAV_usdt']==v[-1];metrics(tail,daily[330:],40,t)
 for j,f in enumerate(t['folds']):
  l,h=330+5*j,335+5*j;aa,bb=ix[[l,h]];assert f['duration_days']==5 and f['start_utc']==engine.stamp(int(m['ts'][aa])) and f['end_exclusive_utc']==engine.stamp(int(m['ts'][bb]));metrics(v[aa:bb+1],daily[l:h+1],5,f)
 assert len(t['folds'])==8 and abs(math.prod(1+f['net_return_pct']/100 for f in t['folds'])-tail[-1]/tail[0])<1e-12

def recover_from_recorded_events(m,scene,counters,multiplier):
 state={'cash':D(10000),'signed_units':D(0),'entry_price':D(0),'entry_reference':D(0)};v=np.empty(len(m['ts']));events=sorted([(int(t['axis_index']),'trade',t) for t in scene['trades']]+[(int(f['axis_index']),'fund',f) for f in scene['funding_events']]);assert len({i for i,_,_ in events})==len(events);start=0
 for idx,kind,e in events:
  v[start:idx]=float(state['cash'])+float(state['signed_units'])*(m['axis_prices'][start:idx]-float(state['entry_price']))
  if kind=='trade':
   assert e['status']=='filled' and {k:D(x) for k,x in e['state_before'].items()}==state and e['trade_ts_ns']==int(m['ts'][idx]);q=state['signed_units'];cash=state['cash'];change=D(e['change_signed_units']);ref=D(e['reference']);px=D(e['execution']);fee=D(e['cost_parts']['fee']);cost=sum(D(x) for x in e['cost_parts'].values());assert abs(change)==D(e['quantity'])
   if e['opening']:
    assert q==0;new={'cash':cash-fee,'signed_units':change,'entry_price':px,'entry_reference':ref};assert abs(change)*px<=new['cash']
   else:
    assert change==-q;near(D(e['reference_price_PnL_usdt']),q*(ref-state['entry_reference']),1e-13);new={'cash':cash+q*(px-state['entry_price'])-fee,'signed_units':D(0),'entry_price':D(0),'entry_reference':D(0)}
   assert abs(cash+q*(ref-state['entry_price'])-(new['cash']+new['signed_units']*(ref-new['entry_price']))-cost)<D('1e-18');assert {k:D(x) for k,x in e['state_after'].items()}==new;state=new;counters['source_recorded_trades_checked']+=1
  else:
   assert int(m['codes'][idx])==4 and e['settlement_ts_ns']==int(m['ts'][idx]) and D(e['signed_units'])==state['signed_units'] and D(e['cash_before'])==state['cash'];base=-state['signed_units']*D(e['mark_price'])*D(e['realized_rate']);assert base==D(e['base_amount_usdt']);amount=D(e['amount_usdt']);assert amount==(base if base>=0 else base*multiplier)
   if amount:state['cash']+=amount
   assert state['cash']==D(e['cash_after']);counters['source_recorded_funding_checked']+=1
  start=idx
 v[start:]=float(state['cash'])+float(state['signed_units'])*(m['axis_prices'][start:]-float(state['entry_price']));assert state['signed_units']==0 and {k:D(x) for k,x in scene['terminal_state'].items()}==state
 # The actual event ledger and independent saved-state encoding must produce every same point.
 n=0
 for s in scene['state_segments']:
  a,b=s['axis_start'],s['axis_end_exclusive'];assert a==n;other=float(s['cash'])+float(s['signed_units'])*(m['axis_prices'][a:b]-float(s['entry_price']));assert np.array_equal(v[a:b],other);n=b
 assert n==len(v) and hashlib.sha256(v.astype('<f8').tobytes()).hexdigest()==scene['summary']['NAV_sha256_f64le'];return v
