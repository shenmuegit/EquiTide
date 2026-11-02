"""Synthetic regression: averaging N past-available settlements changes entry decisions."""
import copy
from decimal import Decimal as D
from fractions import Fraction as F
from common import *
import engine
base={'parameters':{'lookback_days':3,'trend_lookback_days':28,'entry_volatility_window_days':10,'entry_volatility_ceiling':.045,'exit_buffer_fraction':.0025,'return_hurdle':.025,'funding_entry_cap_rate':0,'funding_signal_extra_lag_seconds':3600,'funding_signal_max_age_hours':16,'funding_signal_lookback_settlements':3}}
cut=45*DAY
hist=[{'source_index':j,'settlement_ts':cut-(6-j)*8*HOUR,'available_ts':cut-(6-j)*8*HOUR+HOUR,'realized_rate':D('.0002') if j==5 else D('-.0003')} for j in range(6)]
hist.append({'source_index':6,'settlement_ts':cut,'available_ts':cut+HOUR,'realized_rate':D('9')})
cl=[D(60)]*25+[D(100)]*19+[D(96)];m={'asset':'ETH','closes':cl,'first_ns':0,'funding_signal_history':hist}
assert engine.decide(base,m,45,0)[0]==1,'N3 negative exact mean must allow a fresh long even when last rate is positive'
cases=[]
for L in [3,4,5]:
 for N in [1,3,6]:
  sp=copy.deepcopy(base);sp['parameters'].update(lookback_days=L,funding_signal_lookback_settlements=N)
  w,a=engine.decide(sp,m,45,0);assert w==(0 if N==1 else 1)
  chosen=hist[6-N:6];rate=sum((F(x['realized_rate']) for x in chosen),F(0))/N
  assert a['funding_mean_rate_exact']==str(rate) and a['funding_signal_lookback_settlements']==N and [x['source_index'] for x in a['funding_signals']]==list(range(6-N,6))
  assert a['directional_lagged_payment_rate_exact']==str(rate) and all(x['available_ts']+HOUR<=cut for x in a['funding_signals'])
  late=copy.deepcopy(m);late['funding_signal_history'][-1]['realized_rate']=D('-999');late['funding_signal_history'].append({'source_index':7,'settlement_ts':cut+HOUR,'available_ts':cut+2*HOUR,'realized_rate':D('-999')});assert engine.decide(sp,late,45,0)==(w,a)
  retained=copy.deepcopy(m);retained['closes'][-1]=D('100.1');assert engine.decide(sp,retained,45,1)[0]==1
  retained['closes'][-1]=D('100.25');assert engine.decide(sp,retained,45,1)[0]==0
  short=copy.deepcopy(m);short['closes']=[D(200)]*25+[D(100)]*19+[D(104)];assert engine.decide(sp,short,45,0)[0]==(-1 if N==1 else 0)
  assert engine.decide(sp,m,45,-1)[0]==(0 if N==1 else 1)
  same=copy.deepcopy(m)
  for ev in same['funding_signal_history'][:6]:ev['realized_rate']=D('0')
  assert engine.decide(sp,same,45,0)[0]==1
  cases.append({'L':L,'N':N,'exact_mean':str(rate),'fresh_long':w,'future_invariance':True,'retention_exit_flip_and_sign':True})
for count in [0,2,5]:
 sp=copy.deepcopy(base);sp['parameters']['funding_signal_lookback_settlements']=6;mm=copy.deepcopy(m);mm['funding_signal_history']=hist[:count]
 try:engine.decide(sp,mm,45,0)
 except AssertionError:pass
 else:raise AssertionError('Insufficient N sources must block, never shrink or impute')
mm=copy.deepcopy(m)
for ev in mm['funding_signal_history']:ev['settlement_ts']-=24*HOUR;ev['available_ts']-=24*HOUR
try:engine.decide(base,mm,45,0)
except AssertionError:pass
else:raise AssertionError('Latest eligible source older than16h must block')
sp=copy.deepcopy(base);sp['parameters']['funding_signal_lookback_settlements']=1;mm=copy.deepcopy(m);mm['funding_signal_history'][-1].update(settlement_ts=cut-2*HOUR,available_ts=cut-HOUR,realized_rate=D('-.0002'));assert engine.decide(sp,mm,45,0)[0]==1
mm['funding_signal_history'][-1]['available_ts']+=1;assert engine.decide(sp,mm,45,0)[0]==0
sp=copy.deepcopy(base);sp['parameters']['funding_entry_cap_rate']=None;assert engine.decide(sp,{'asset':'ETH','closes':cl},45,0)[0]==1
assert engine.entry_filter(1,0,.045,.045)==1 and engine.entry_filter(1,0,.045001,.045)==0
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'actual_market_backtests':0,'cases':cases,'extra_checks':['zero mean equality','full N required','newest source age only; older fullN span allowed','availability extra1h exact boundary and+1ns','future rates invariant','OFF no dependency','vol equality']})
print('PASS exact funding mean N1/3/6, fullN/newest-age/availability, future-invariance and original exits')
