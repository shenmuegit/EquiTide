"""Finite normalized EWM S/D domains;unchanged audited native accounting."""
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
  assert p['lookback_days']==29 and p['return_hurdle'] in [.0275,.03,.0325] and p['exit_buffer_fraction'] in [.0075,.01,.0125] and i-1-p['lookback_days']>=0
  wanted,r=btc.target(m['closes'],i,p['lookback_days'],p['return_hurdle'],actual,p['exit_buffer_fraction']);return wanted,{'kind':'BTC_momentum','return_exact':r}
 from fractions import Fraction as F
 L=int(p['lookback_days']);S=int(p['trend_lookback_days']);lag=int(p['trend_slope_lag_days']);V=int(p['entry_volatility_window_days']);cap=float(p['entry_volatility_ceiling']);E=float(p['exit_buffer_fraction']);H=float(p['return_hurdle']);assert L in [4,5,6] and S in [12,16,20] and p['trend_slope_hurdle_fraction'] in [.00625,.0075,.00875] and lag in [1,2,3,4,5] and V in [5,6,7,8,10,12] and cap in [.045,.05,.0525,.055,.0575,.06] and E in [.00625,.0075,.00875] and E<H and H in [.0175,.02,.0225] and p['long_entry_return_hurdle']==p['short_entry_return_hurdle']==H and p['trend_estimator']=='finite_normalized_exponentially_weighted_mean_slope' and p['trend_decay_numerator']==S-1 and p['trend_decay_denominator']==S+1 and p['trend_window_days']==S and i-S-lag>=0 and p['trend_gate_scope']=='new_or_reversed_position_only'
 r=F(m['closes'][i-1])/F(m['closes'][i-1-L])-1;beta=F(S-1,S+1);weights=[beta**j for j in range(S)];mass=sum(weights);level=sum((F(m['closes'][i-1-j])*weights[j] for j in range(S)),F(0))/mass;reference=sum((F(m['closes'][i-1-lag-j])*weights[j] for j in range(S)),F(0))/mass;s=level/reference-1;h=F(str(p['return_hurdle']));e=F(str(p['exit_buffer_fraction']))
 base=-1 if r>h else 1 if r<-h else actual if actual==1 and r<e or actual==-1 and r>-e else 0;gate=slope_gate(s,F(str(p['trend_slope_hurdle_fraction'])));raw=base if base==actual or base==gate else 0;sigma=statistics.stdev([math.log(float(m['closes'][j])/float(m['closes'][j-1])) for j in range(i-V,i)]);wanted=entry_filter(raw,actual,sigma,cap)
 before_funding=wanted;sn=int(m['frame']['available_ts'][i*1440-1]);event=median_funding(m['signal_funds'],sn,int(p['entry_funding_settlement_count']));VW=int(p.get('entry_funding_budget_volatility_window_days',10));budget_sigma_value=budget_sigma(m['closes'],i,VW);budget=carry_cap(budget_sigma_value,p['entry_funding_volatility_ratio'],event);wanted,funding_audit=funding_filter(wanted,actual,event,sn,budget);funding_audit.update(budget_sigma_daily=str(budget_sigma_value),budget_volatility_window_days=VW,budget_ratio=str(p['entry_funding_volatility_ratio']),latest_past_interval_hours=str(event['events'][0]['entry_interval_hours']) if event and event['events'][0].get('entry_interval_hours') is not None else None,hard_cap_fraction='.0002',interval_policy='latesteligibleactualsettlementminusimmediatepredecessor,bothavailable;nanoseconddifference/3600000000000,Decimal28')
 return wanted,{'funding_filter':funding_audit,'raw_desired_before_funding_filter':before_funding,'kind':'ETH_finite_EWMslope_entry_gate_reversal_entry_vol','ungated_desired':base,'slowgate_direction':gate,'trend_gate_applied':bool(base and base!=actual),'trend_gate_scope':'new_or_reversed_position_only','exit_buffer_fraction':E,'fast_lookback_days':L,'slow_lookback_days':S,'slope_lag_days':lag,'slope_hurdle_fraction':p['trend_slope_hurdle_fraction'],'return_exact':str(r),'slow_mean_exact':str(level),'slow_reference_mean_exact':str(reference),'slow_distance_exact':str(s),'slow_distance_basis':'finite_EWM_slope_ratio','raw_desired_before_entry_filter':raw,'entry_filter_applied':bool(raw and raw!=actual),'observed_sample_logvol':sigma,'volatility_window_days':V,'entry_volatility_ceiling':cap,'long_entry_return_hurdle':H,'short_entry_return_hurdle':H}

def latest_funding(events,signal_ns):
 eligible=[e for e in events if HOUR<=signal_ns-e['settlement_ts']<=12*HOUR and e['available_ts']<=signal_ns]
 return max(eligible,key=lambda e:e['settlement_ts']) if eligible else None

def median_funding(events,signal_ns,count):
 assert count in [2,3,4]
 eligible=sorted([e for e in events if HOUR<=signal_ns-e['settlement_ts']<=36*HOUR and e['available_ts']<=signal_ns],key=lambda e:e['settlement_ts'],reverse=True)
 assert len({e['settlement_ts'] for e in eligible})==len(eligible)
 selected=eligible[:count]
 if len(selected)<count:return None
 rates=sorted(e['realized_rate'] for e in selected);mid=count//2;rate=rates[mid] if count%2 else (rates[mid-1]+rates[mid])/D(2)
 return {'events':selected,'median_rate':rate,'count':count}

def funding_filter(raw,actual,event,signal_ns,cap):
 applied=bool(raw and raw!=actual)
 valid=cap is not None and event is not None and len(event['events'])==event['count'] and all(HOUR<=signal_ns-e['settlement_ts']<=36*HOUR and e['available_ts']<=signal_ns for e in event['events'])
 outflow=max(D(raw)*event['median_rate'],D(0)) if valid else None;blocked=applied and (not valid or outflow>cap)
 audit={'applied':applied,'blocked':blocked,'cap_fraction_per_settlement':str(cap),'minimum_age_ns':HOUR,'maximum_age_ns':36*HOUR,'signal_available_ts_ns':signal_ns,'selected_settlements':[{'settlement_ts_ns':e['settlement_ts'],'available_ts_ns':e['available_ts'],'realized_rate':str(e['realized_rate']),'source_index':e['source_index']} for e in event['events']] if valid else [],'median_realized_rate':str(event['median_rate']) if valid else None,'settlement_count':event['count'] if valid else None,'expected_outflow_fraction':str(outflow) if outflow is not None else None,'availability_policy':'sourceconservative1hdelay;actualsettlements1to36holdinclusiveandavailable<=signal;latestNmedian,no future rate;missing required recordsblocks newentryonly','scope':'new_or_reversed_position_only'}
 return (0 if blocked else raw),audit

def budget_sigma(closes,i,window):
 assert window in [8,10,12] and i-window-1>=0
 return statistics.stdev([math.log(float(closes[j])/float(closes[j-1])) for j in range(i-window,i)])

def carry_cap(sigma,ratio,event):
 if event is None:return None
 hours=event['events'][0].get('entry_interval_hours')
 if hours is None or not D(0)<hours<=D(36):return None
 return min(D('.0002'),D(str(ratio))*D(str(sigma))*hours/D(24))

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
