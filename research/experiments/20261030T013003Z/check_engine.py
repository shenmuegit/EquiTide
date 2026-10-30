"""Unchanged native engines;synthetic fast/slow and causal-entry funding checks only."""
import json
from decimal import Decimal as D
from fractions import Fraction as F
from run import ROOT,R,sha,put
import engine
P=ROOT/'research/experiments/20261029T232932Z'
assert all(sha(R/n)==sha(P/n) for n in ['engine.py','btc_engine.py'])
values=[D(100)+D(i%9-4)/10+D(i)/100 for i in range(40)];tests=0
for L in [2,3,4]:
 for S in [27,28,29]:
  for current in [-1,0,1]:
   j=35;r=F(values[j])/F(values[j-L])-1;returns=[F(values[j])/F(values[j-s])-1 for s in [S-1,S,S+1]];median=sorted(returns)[1];allowed=1 if median>0 else -1 if median<0 else 0;H,E=F('.025'),F('-.01');want=-1 if r>H else 1 if r<-H else 1 if current==1 and r<E else -1 if current==-1 and r>-E else 0;expected=want if current and want==current else want if want==allowed else 0
   out=engine.majority_target(values,j+1,L,.025,current,-.01,S,'entries_only');assert out==(expected,str(r),str(median)) and out==engine.majority_target(values[:j+1]+[D(100000)],j+1,L,.025,current,-.01,S,'entries_only');tests+=1
# At00,unavailable current00 funding must not enter signal;16h freshness and allsix available records remain explicit.
class Frame:
 def __getitem__(self,key):return [None]*1439+[0]
m={'frame':Frame(),'funding_feature_history':[{'available_ts':-6+i,'settlement_ts':-7+i,'source_index':i,'realized_rate':D('.00001')} for i in range(6)]+[{'available_ts':engine.HOUR,'settlement_ts':0,'source_index':6,'realized_rate':D('1')}]}
p={'entry_funding_lookback_settlements':6,'entry_funding_cost_cap_per_settlement':.00005,'entry_funding_application':'new_and_reversal_entries_only','entry_funding_max_age_hours':16};direction,a=engine.funding_entry_gate(p,m,1,1,D(0));assert direction==1 and a['source_indices']==list(range(6)) and a['stress_does_not_change_signal'];tests+=1
put(R/'engine_change_verification.json',{'passed':True,'financial_evaluations':0,'engine_source_unchanged':True,'source_round':P.name,'engine_sha256':sha(R/'engine.py'),'BTC_engine_sha256':sha(R/'btc_engine.py'),'synthetic_fast_slow_future_append_and_unavailable_funding_checks':tests});print('PASS unchanged engines and',tests,'synthetic timing/signalchecks')
