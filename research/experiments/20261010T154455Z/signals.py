"""Joint breakout/EMA entry and either-condition exit from completed closes only."""
from decimal import Decimal as D

def filtered_channel(closes,entry_days,exit_days,span,band,start=183,end=363):
 values=[D(c) for c in closes];assert max(entry_days,exit_days)+1<=start and end<=len(values)
 alpha=2/(span+1);level=float(values[0]);ema=[]
 for j,c in enumerate(values):
  if j:level=(1-alpha)*level+alpha*float(c)
  ema.append(level)
 state=False;out=[]
 for i in range(start,end):
  last=values[i-1];reference=ema[i-1];upper=max(values[i-entry_days-1:i-1]);lower=min(values[i-exit_days-1:i-1]);before=state
  channel_up=last>upper;channel_down=last<lower;EMA_up=float(last)>reference*(1+band);EMA_down=float(last)<reference*(1-band)
  if channel_down or EMA_down:state=False
  elif channel_up and EMA_up:state=True
  out.append({'decision_index':i,'prior_close':str(last),'entry_channel_prior':str(upper),'exit_channel_prior':str(lower),'EMA_prior':reference,'channel_entry':channel_up,'channel_exit':channel_down,'EMA_entry':EMA_up,'EMA_exit':EMA_down,'long':state,'action':'entry' if state and not before else 'exit' if before and not state else 'hold'})
 return out
