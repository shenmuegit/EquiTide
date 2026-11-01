"""Synthetic only: lagged funding selection, strict payment caps, exit/retention and causality."""
import copy,json
from decimal import Decimal as D
from common import *
import engine
base={'parameters':{'lookback_days':3,'trend_lookback_days':28,'entry_volatility_window_days':10,'entry_volatility_ceiling':.045,'exit_buffer_fraction':.0025,'return_hurdle':.025,'funding_entry_cap_rate':0,'funding_signal_extra_lag_seconds':3600,'funding_signal_max_age_hours':16}}
cut=45*DAY;hist=[{'source_index':0,'settlement_ts':cut-8*HOUR,'available_ts':cut-7*HOUR,'realized_rate':D('.0002')},{'source_index':1,'settlement_ts':cut,'available_ts':cut+HOUR,'realized_rate':D('-.01')}]
cl=[D(60)]*25+[D(100)]*19+[D(96)];m={'asset':'ETH','closes':cl,'first_ns':0,'funding_signal_history':hist}
w,a=engine.decide(base,m,45,0)
assert w==0,'new long must reject known positive funding payment; unseen new rate must not rescue entry'
checks=[]
for L in [3,4,5]:
 for C in [0,.0001,None]:
  sp=copy.deepcopy(base);sp['parameters'].update(lookback_days=L,funding_entry_cap_rate=C);mm=copy.deepcopy(m)
  w,a=engine.decide(sp,mm,45,0);assert w==(1 if C is None else 0)
  if C is not None:assert a['funding_signal']['source_index']==0 and a['funding_signal']['available_ts']+HOUR<=cut
  later=copy.deepcopy(mm);later['funding_signal_history'].append({'source_index':2,'settlement_ts':cut+HOUR,'available_ts':cut+2*HOUR,'realized_rate':D('-999')});assert engine.decide(sp,later,45,0)==(w,a)
  mm['funding_signal_history'][0]['realized_rate']=D('-.0002');assert engine.decide(sp,mm,45,0)[0]==1
  mm['closes']=[D(200)]*25+[D(100)]*19+[D(104)];assert engine.decide(sp,mm,45,0)[0]==(-1 if C is None else 0)
  mm['funding_signal_history'][0]['realized_rate']=D('.0002');assert engine.decide(sp,mm,45,0)[0]==-1
  mm['closes']=[D(60)]*25+[D(100)]*19+[D('100.1')];mm['funding_signal_history'][0]['realized_rate']=D('.01');assert engine.decide(sp,mm,45,1)[0]==1
  mm['closes'][-1]=D('100.25');assert engine.decide(sp,mm,45,1)[0]==0
  mm['closes'][-1]=D(96);assert engine.decide(sp,mm,45,-1)[0]==(1 if C is None else 0)
  checks.append([L,C,'past-only-source/payment-side/retention/exit/failed-flip/future-append'])
sp=copy.deepcopy(base);sp['parameters']['funding_entry_cap_rate']=.0001;mm=copy.deepcopy(m);mm['funding_signal_history'][0]['realized_rate']=D('.0001');assert engine.decide(sp,mm,45,0)[0]==1
mm['funding_signal_history'][0]['realized_rate']=D('.0001000001');assert engine.decide(sp,mm,45,0)[0]==0
sp=copy.deepcopy(base);mm=copy.deepcopy(m);mm['funding_signal_history'][1].update(settlement_ts=cut-2*HOUR,available_ts=cut-HOUR,realized_rate=D('-.0002'));assert engine.decide(sp,mm,45,0)[0]==1
mm['funding_signal_history'][1]['available_ts']+=1;assert engine.decide(sp,mm,45,0)[0]==0
sp=copy.deepcopy(base);sp['parameters']['funding_entry_cap_rate']=None;assert engine.decide(sp,{'asset':'ETH','closes':cl},45,0)[0]==1
assert engine.entry_filter(1,0,.045,.045)==1 and engine.entry_filter(1,0,.045001,.045)==0
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'actual_market_backtests':0,'cases':checks+['payment-equality/extra1h-availability-equality','OFF-no-funding-dependency','volboundary']})
print('PASS L/F raw funding-cap directions/causality/equalities/exit/retention/OFF')
