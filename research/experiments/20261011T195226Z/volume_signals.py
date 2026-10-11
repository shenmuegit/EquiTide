"""Prior-close channel entry confirmed by disjoint preceding quote-turnover mean."""
from decimal import Decimal as D,getcontext
getcontext().prec=28

def volume_channel(rows,entry_days,exit_days,volume_days,minimum_ratio,start=183,end=363):
 values=[D(r['close'])for r in rows];volumes=[D(str(r['quote_volume']))for r in rows];threshold=D(str(minimum_ratio))
 assert min(entry_days,exit_days,volume_days)>0 and max(entry_days,exit_days,volume_days)+1<=start and end<=len(rows) and threshold>0
 state=False;out=[]
 for i in range(start,end):
  last=values[i-1];before=state;upper=max(values[i-entry_days-1:i-1]);lower=min(values[i-exit_days-1:i-1]);history=volumes[i-volume_days-1:i-1]
  assert len(history)==volume_days and all(q>=0 for q in history)
  average=sum(history)/volume_days;relative=volumes[i-1]/average if average>0 else None;eligible=average>0 and volumes[i-1]>=threshold*average
  if last<lower:state=False
  elif last>upper and eligible:state=True
  out.append({'decision_index':i,'prior_close':str(last),'entry_channel_prior':str(upper),'exit_channel_prior':str(lower),'quote_volume_prior':str(volumes[i-1]),'quote_volume_reference_mean':str(average),'relative_quote_volume':str(relative) if relative is not None else None,'volume_eligible':eligible,'price_breakout':last>upper,'long':state,'action':'entry' if state and not before else 'exit' if before and not state else 'hold'})
 return out
