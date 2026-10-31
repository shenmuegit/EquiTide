"""Same original causal policies, fresh actual native capital/quantity/cost/funding ledgers."""
import copy
from decimal import Decimal as D,ROUND_FLOOR
import numpy as np
from common import *
START,END,DAYS=core.START,core.END,core.DAYS
trade,funding_amount,summary=core.trade,core.funding_amount,core.summary
btc=module(ROOT/'research/experiments/20261025T065405Z/engine.py','original_BTC_ROC_policy')
eth=module(ROOT/'research/experiments/20261026T070542Z/engine.py','original_ETH_slowgate_policy')
def decide(spec,m,i,actual):
 p=spec['parameters']
 if p.get('signal_mode')=='constant_long_reference':return 1,{'kind':'constant_long_reference'}
 if m['asset']=='BTC':
  assert p['lookback_days']==31 and p['return_hurdle']==.04 and p['exit_buffer_fraction']==.01 and i-32>=0
  wanted,r=btc.target(m['closes'],i,31,.04,actual,.01);return wanted,{'kind':'BTC_momentum','return_exact':r}
 from fractions import Fraction as F
 L=int(p['lookback_days']);S=int(p['trend_lookback_days']);assert L in [3,4,5] and S==28 and p['return_hurdle'] in [.02,.025,.03] and p['exit_buffer_fraction']==0 and i-1-max(L,S)>=0
 r=F(m['closes'][i-1])/F(m['closes'][i-1-L])-1;s=F(m['closes'][i-1])/F(m['closes'][i-1-S])-1;h=F(str(p['return_hurdle']))
 base=-1 if r>h else 1 if r<-h else actual if (actual==1 and r<0) or (actual==-1 and r>0) else 0;gate=(s>0)-(s<0);wanted=base if base==gate else 0
 return wanted,{'kind':'ETH_gated_reversal','return_exact':str(r),'slow_return_exact':str(s)}

def simulate(spec,m,mult):
 p=spec['parameters'];notional=D(str(p['fixed_entry_notional_usdt']));capital=D(str(p['initial_capital_usdt']));assert 0<notional<=capital;state={'cash':str(capital),'signed_units':'0','entry_price':'0','entry_reference':'0'};v=np.empty(len(m['ts']));segments=[];trades=[];funds=[];decisions=[];start=0;segment_start=0;segment_state=copy.deepcopy(state);wanted=0
 def execute(i,change,opening,axis_index,terminal=False):
  nonlocal state
  adv,sigma=m['cost_inputs'][i];state,t=trade(state,change,m['frame']['open'][i*1440+1],adv,sigma,m['meta'],mult,opening);t.update(decision_index=i,trade_ts_ns=int(m['ts'][axis_index]),axis_index=int(axis_index),terminal=terminal,asset=m['asset']);trades.append(t)
 for idx in m['controls']:
  idx=int(idx);cash,q,entry=[float(state[k]) for k in ['cash','signed_units','entry_price']];v[start:idx]=cash+q*(m['axis_prices'][start:idx]-entry);code=int(m['codes'][idx]);ref=int(m['refs'][idx]);before=copy.deepcopy(state)
  if code==4:
   e=m['funds'][ref];base,amount=funding_amount(D(state['signed_units']),e['mark_price_at_settlement'],e['realized_rate'],mult);cb=D(state['cash'])
   if amount:state['cash']=str(cb+amount)
   funds.append({'source_index':e['source_index'],'settlement_ts_ns':e['settlement_ts'],'available_ts_ns':e['available_ts'],'realized_rate':str(e['realized_rate']),'mark_price':str(e['mark_price_at_settlement']),'actual_interval_hours':str(e['actual_interval_hours']),'signed_units':state['signed_units'],'base_amount_usdt':str(base),'amount_usdt':str(amount),'cash_before':str(cb),'cash_after':state['cash'],'axis_index':idx})
  elif code==6:
   actual=1 if D(state['signed_units'])>0 else -1 if D(state['signed_units'])<0 else 0;wanted,bounds=decide(spec,m,ref,actual);q=D(state['signed_units']);decisions.append({'decision_index':ref,'signal_available_ts_ns':int(m['frame']['available_ts'][ref*1440-1]),'execution_ts_ns':int(m['ts'][idx]),'policy_audit':bounds,'desired_direction':wanted,'fixed_entry_notional_usdt':float(notional),'state_before':copy.deepcopy(state)})
   if q and (1 if q>0 else -1)!=wanted:execute(ref,-q,False,idx)
  elif code==7:
   if wanted and D(state['signed_units'])==0:
    lot=D(m['meta']['lot_size']);quantity=(notional/m['closes'][ref-1]/lot).to_integral_value(rounding=ROUND_FLOOR)*lot;execute(ref,D(wanted)*quantity,True,idx)
   decisions[-1]['state_after']=copy.deepcopy(state)
  elif code==9:
   if D(state['signed_units']):execute(END,-D(state['signed_units']),False,idx,True)
  if state!=before:
   if idx>segment_start:segments.append({'axis_start':segment_start,'axis_end_exclusive':idx,**segment_state})
   segment_start=idx;segment_state=copy.deepcopy(state)
  start=idx
 cash,q,entry=[float(state[k]) for k in ['cash','signed_units','entry_price']];v[start:]=cash+q*(m['axis_prices'][start:]-entry);segments.append({'axis_start':segment_start,'axis_end_exclusive':len(v),**segment_state});assert D(state['signed_units'])==0 and len(decisions)==DAYS and (v>0).all() and np.isfinite(v).all()
 return v,{'decisions':decisions,'trades':trades,'funding_events':funds,'state_segments':segments,'terminal_state':state,'summary':summary(m,v,trades,funds,segments)}
