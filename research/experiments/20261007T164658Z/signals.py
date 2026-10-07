"""Prior-close breakout versus disjoint strictly earlier completed-close ranges."""
from decimal import Decimal as D

def close_channel(closes,entry_days,exit_days,start=183,end=363):
 values=[D(c) for c in closes]
 assert min(entry_days,exit_days)>0 and max(entry_days,exit_days)+1<=start and end<=len(values)
 state=False;out=[]
 for i in range(start,end):
  last=values[i-1];before=state;up=values[i-entry_days-1:i-1];down=values[i-exit_days-1:i-1]
  assert len(up)==entry_days and len(down)==exit_days
  upper=max(up);lower=min(down)
  if last>upper:state=True
  elif last<lower:state=False
  out.append({'decision_index':i,'prior_close':str(last),'entry_channel_prior':str(upper),'exit_channel_prior':str(lower),'long':state,'action':'entry' if state and not before else 'exit' if before and not state else 'hold'})
 return out
