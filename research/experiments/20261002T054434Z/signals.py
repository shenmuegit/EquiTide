"""Confirmed SMA hysteresis using only completed daily closes."""
from decimal import Decimal as D

def confirmed_sma_hysteresis(closes,lookback,confirmation,start=183,end=363):
 values=[D(c) for c in closes]
 assert lookback<=start and end<=len(values) and confirmation>=2
 state=False;above=below=0;out=[]
 for i in range(start,end):
  mean=sum(values[i-lookback:i])/lookback;last=values[i-1];before=state
  above=above+1 if last>mean*D('1.01') else 0
  below=below+1 if last<mean*D('.99') else 0
  if above>=confirmation:state=True
  elif below>=confirmation:state=False
  out.append({'decision_index':i,'prior_close':str(last),'SMA_prior':str(mean),'above_run':above,'below_run':below,'long':state,'action':'entry' if state and not before else 'exit' if before and not state else 'hold'})
 return out
