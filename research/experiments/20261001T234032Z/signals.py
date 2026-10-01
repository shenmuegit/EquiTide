"""Recursive EMA; each decision sees completed daily closes only."""
def ema_hysteresis(closes,span,band,start=183,end=363):
 alpha=2/(span+1);ema=[];level=float(closes[0])
 for j,c in enumerate(closes):
  if j:level=(1-alpha)*level+alpha*float(c)
  ema.append(level)
 state=False;out=[]
 for i in range(start,end):
  close=float(closes[i-1]);reference=ema[i-1];before=state
  if close>reference*(1+band):state=True
  elif close<reference*(1-band):state=False
  out.append({'decision_index':i,'prior_close':close,'EMA_prior':reference,'long':state,'action':'entry' if state and not before else 'exit' if before and not state else 'hold'})
 return out
