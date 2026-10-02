"""Causal asymmetric SMA hysteresis with exact completed-close Decimal mean."""
from decimal import Decimal as D

def asymmetric_sma_hysteresis(closes,lookback,entry_band,exit_band,start=183,end=363):
 values=[D(c) for c in closes];entry=D(str(entry_band));exit=D(str(exit_band))
 assert lookback<=start and end<=len(values) and entry>exit>0
 state=False;out=[]
 for i in range(start,end):
  mean=sum(values[i-lookback:i])/lookback;last=values[i-1];before=state
  if last>mean*(1+entry):state=True
  elif last<mean*(1-exit):state=False
  out.append({'decision_index':i,'prior_close':str(last),'SMA_prior':str(mean),'long':state,'action':'entry' if state and not before else 'exit' if before and not state else 'hold'})
 return out
