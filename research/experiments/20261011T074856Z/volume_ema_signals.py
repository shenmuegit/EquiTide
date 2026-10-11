"""Same-decision price/volume/EMA entry;price-or-EMA exit,no delayed arming."""
from pathlib import Path
from decimal import Decimal as D
import importlib.util
spec=importlib.util.spec_from_file_location('R38_volume_reference',Path(__file__).with_name('volume_signals.py'));base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
def volume_ema_channel(rows,entry_days,exit_days,volume_days,minimum_ratio,span,band,start=183,end=363):
 assert span>0 and 0<band<1
 raw=base.volume_channel(rows,entry_days,exit_days,volume_days,minimum_ratio,start,end)
 alpha=2/(span+1);level=float(D(rows[0]['close']));ema=[]
 for i,r in enumerate(rows):
  if i:level=(1-alpha)*level+alpha*float(D(r['close']))
  ema.append(level)
 state=False;out=[]
 for v in raw:
  i=v['decision_index'];last=D(v['prior_close']);reference=ema[i-1];before=state
  ema_up=float(last)>reference*(1+band);ema_down=float(last)<reference*(1-band);channel_down=last<D(v['exit_channel_prior'])
  if channel_down or ema_down:state=False
  elif v['price_breakout']and v['volume_eligible']and ema_up:state=True
  out.append({**v,'EMA_prior':reference,'EMA_entry':ema_up,'EMA_exit':ema_down,'channel_exit':channel_down,'long':state,'action':'entry'if state and not before else'exit'if before and not state else'hold'})
 return out
