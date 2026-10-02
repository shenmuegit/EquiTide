"""Completed-close Decimal asymmetric SMA with an explicit lagged-volatility cash guard."""
from decimal import Decimal as D

def volatility_guarded_asymmetric_sma(closes,lookback,entry_band,exit_band,volatility_lookback,annual_volatility_ceiling,start=183,end=363):
 values=[D(c) for c in closes];entry=D(str(entry_band));exit=D(str(exit_band));cap=D(str(annual_volatility_ceiling));n=volatility_lookback
 assert lookback<=start and n+1<=start and end<=len(values) and entry>exit>0 and n>1 and cap>0
 state=False;out=[]
 for i in range(start,end):
  mean=sum(values[i-lookback:i])/lookback;last=values[i-1];before=state
  window=values[i-n-1:i];returns=[(b/a).ln() for a,b in zip(window,window[1:])];average=sum(returns)/n
  variance=sum((x-average)**2 for x in returns)/(n-1);volatility=(variance*D(365)).sqrt();eligible=volatility<=cap
  if not eligible:state=False
  elif last>mean*(1+entry):state=True
  elif last<mean*(1-exit):state=False
  out.append({'decision_index':i,'prior_close':str(last),'SMA_prior':str(mean),'annual_volatility_prior':str(volatility),'volatility_eligible':eligible,'long':state,'action':'entry' if state and not before else 'exit' if before and not state else 'hold'})
 return out
