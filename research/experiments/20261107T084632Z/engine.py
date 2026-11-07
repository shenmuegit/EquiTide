"""Finite normalized EWM S/exitE-gated reversal with varied fastL/H;unchanged audited native accounting."""
import copy,math,statistics
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
  assert p['lookback_days']==29 and p['return_hurdle'] in [.03,.04,.05] and p['exit_buffer_fraction'] in [.005,.01,.015] and i-1-p['lookback_days']>=0
  wanted,r=btc.target(m['closes'],i,p['lookback_days'],p['return_hurdle'],actual,p['exit_buffer_fraction']);return wanted,{'kind':'BTC_momentum','return_exact':r}
 from fractions import Fraction as F
 L=int(p['lookback_days']);S=int(p['trend_lookback_days']);lag=int(p['trend_slope_lag_days']);V=int(p['entry_volatility_window_days']);cap=float(p['entry_volatility_ceiling']);E=float(p['exit_buffer_fraction']);H=float(p['return_hurdle']);assert L==5 and S==24 and p['trend_slope_hurdle_fraction'] in [.01,.02,.03] and lag in [6,7,8] and V==10 and cap==.045 and E==.005 and H==.02 and p['long_entry_return_hurdle']==p['short_entry_return_hurdle']==H and p['trend_estimator']=='finite_normalized_exponentially_weighted_mean_slope' and p['trend_decay_numerator']==S-1 and p['trend_decay_denominator']==S+1 and p['trend_window_days']==S and i-S-lag>=0 and p['trend_gate_scope']=='new_or_reversed_position_only'
 r=F(m['closes'][i-1])/F(m['closes'][i-6])-1;beta=F(S-1,S+1);weights=[beta**j for j in range(S)];mass=sum(weights);level=sum((F(m['closes'][i-1-j])*weights[j] for j in range(S)),F(0))/mass;reference=sum((F(m['closes'][i-1-lag-j])*weights[j] for j in range(S)),F(0))/mass;s=level/reference-1;h=F('.02');e=F('.005')
 base=-1 if r>h else 1 if r<-h else actual if actual==1 and r<e or actual==-1 and r>-e else 0;gate=slope_gate(s,F(str(p['trend_slope_hurdle_fraction'])));raw=base if base==actual or base==gate else 0;sigma=statistics.stdev([math.log(float(m['closes'][j])/float(m['closes'][j-1])) for j in range(i-V,i)]);wanted=entry_filter(raw,actual,sigma,cap)
 return wanted,{'kind':'ETH_finite_EWMslope_entry_gate_reversal_entry_vol','ungated_desired':base,'slowgate_direction':gate,'trend_gate_applied':bool(base and base!=actual),'trend_gate_scope':'new_or_reversed_position_only','exit_buffer_fraction':E,'slow_lookback_days':S,'slope_lag_days':lag,'slope_hurdle_fraction':p['trend_slope_hurdle_fraction'],'return_exact':str(r),'slow_mean_exact':str(level),'slow_reference_mean_exact':str(reference),'slow_distance_exact':str(s),'slow_distance_basis':'finite_EWM_slope_ratio','raw_desired_before_entry_filter':raw,'entry_filter_applied':bool(raw and raw!=actual),'observed_sample_logvol':sigma,'volatility_window_days':V,'entry_volatility_ceiling':cap,'long_entry_return_hurdle':H,'short_entry_return_hurdle':H}

def slope_gate(s,k):
 return (s>k)-(s<-k)

def entry_filter(raw,actual,sigma,cap):
 return 0 if raw and raw!=actual and sigma>cap else raw

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
