import copy
from decimal import Decimal as D
import numpy as np
from common import *
helpers=module(ROOT/'research/experiments/20261030T194013Z/pair_model.py','immutable_paired_execution_helpers')

def rank(closes,i,L):
 a=closes['BTC'][i-1]/closes['BTC'][i-1-L]-1;b=closes['ETH'][i-1]/closes['ETH'][i-1-L]-1;winner=1 if a>b else -1 if a<b else 0
 return -winner,{'BTC_return':str(a),'ETH_return':str(b),'BTC_direction':winner,'ETH_direction':-winner,'feature_end_day_index':i-1,'feature_start_day_index':i-1-L}

def confirmed_target(diff,H,K,current_side,previous_probe,previous_streak):
 probe=1 if diff>H else -1 if diff< -H else 0
 streak=(previous_streak+1 if probe==previous_probe else 1) if probe else 0
 fresh=-probe if probe and streak>=K else 0
 desired=(fresh if diff*D(-current_side)<=0 else current_side) if current_side else fresh
 return desired,probe,streak

def simulate(spec,ms,axis,mult):
 p=spec['parameters'];L,period=p['lookback_days'],p['rebalance_interval_days'];books={a:{'cash':'10000','signed_units':'0','entry_price':'0','entry_reference':'0'} for a in ms};trades={a:[] for a in ms};funds={a:[] for a in ms};segments={a:[] for a in ms};segment_start={a:0 for a in ms};segment_book=copy.deepcopy(books);curves={a:np.empty(len(axis['ts'])) for a in ms};closes={a:m['closes'] for a,m in ms.items()};start=0;side=0;recovery=False;completed=0;pending=0;probe=0;streak=0;decisions=[]
 for idx0 in axis['controls']:
  idx=int(idx0);t=int(axis['ts'][idx]);code=int(axis['codes'][idx]);before=copy.deepcopy(books)
  for a,m in ms.items():
   b=books[a];curves[a][start:idx]=float(b['cash'])+float(b['signed_units'])*(m['axis_prices'][start:idx]-float(b['entry_price']))
  if code==4:
   for a,m in ms.items():
    if t not in m['fund_lookup']:continue
    e=m['fund_lookup'][t];base,amount=core.funding_amount(D(books[a]['signed_units']),e['mark_price_at_settlement'],e['realized_rate'],mult);cb=D(books[a]['cash'])
    if amount:books[a]['cash']=str(cb+amount)
    funds[a].append({'source_index':e['source_index'],'settlement_ts_ns':t,'available_ts_ns':e['available_ts'],'realized_rate':str(e['realized_rate']),'mark_price':str(e['mark_price_at_settlement']),'actual_interval_hours':str(e['actual_interval_hours']),'signed_units':books[a]['signed_units'],'base_amount_usdt':str(base),'amount_usdt':str(amount),'cash_before':str(cb),'cash_after':books[a]['cash'],'axis_index':idx})
  else:
   day=int((t-axis['first_ns']-MIN)//DAY);contexts={a:{'reference':m['frame']['open'][day*1440+1],'prior_close':m['closes'][day-1],'ADV':m['cost_inputs'][day][0],'sigma':m['cost_inputs'][day][1],'meta':m['meta']} for a,m in ms.items()}
   if code==6:
    pending=0;scheduled=(day-33)%period==0;event={'day_index':day,'execution_ts_ns':t,'signal_available_ts_ns':int(ms['BTC']['frame']['available_ts'][day*1440-1]),'scheduled':scheduled,'state_before':copy.deepcopy(books),'pair_side_before':side,'recovery_before':recovery,'rank':None,'action':'hold','desired_side':side,'probe_before':probe,'streak_before':streak}
    if scheduled:
     _,ra=rank(closes,day,L);diff=D(ra['BTC_return'])-D(ra['ETH_return']);desired,probe,streak=confirmed_target(diff,D(str(p['relative_return_entry_deadband'])),p['consecutive_scheduled_confirmations'],side,probe,streak);event.update(rank={**ra,'relative_return_difference':str(diff)},desired_side=desired)
    event.update(probe_after=probe,streak_after=streak)
    if recovery:
     flat=helpers.close_pair(books,contexts,mult,t,idx,trades,'daily_close_only_recovery')
     if flat:completed+=int(side!=0);side=0;recovery=False
     event['action']='recovery_only'
    elif scheduled:
     if side and desired!=side:
      flat=helpers.close_pair(books,contexts,mult,t,idx,trades,'scheduled_rank_change')
      if flat:completed+=1;side=0
      else:recovery=True
     if not recovery and desired and not side:pending=desired
     event['action']='scheduled'
    event.update(pending_open_side=pending,state_after_close=copy.deepcopy(books));decisions.append(event)
   elif code==7:
    if pending:
     z=helpers.open_pair(books,contexts,pending,D(1),D(2000),mult,t,idx,trades);side=pending if z['opened'] else 0;recovery=z['recovery']
    decisions[-1].update(state_after=copy.deepcopy(books),pair_side_after=side,recovery_after=recovery);pending=0
   elif code==9:
    flat=helpers.close_pair(books,contexts,mult,t,idx,trades,'terminal',True)
    if flat:completed+=int(side!=0);side=0;recovery=False
  for a in ms:
   if books[a]!=before[a]:
    if idx>segment_start[a]:segments[a].append({'axis_start':segment_start[a],'axis_end_exclusive':idx,**segment_book[a]})
    segment_start[a]=idx;segment_book[a]=copy.deepcopy(books[a])
  start=idx
 legs={}
 for a,m in ms.items():
  b=books[a];curves[a][start:]=float(b['cash'])+float(b['signed_units'])*(m['axis_prices'][start:]-float(b['entry_price']));segments[a].append({'axis_start':segment_start[a],'axis_end_exclusive':len(axis['ts']),**segment_book[a]});assert np.isfinite(curves[a]).all() and (curves[a]>0).all();legs[a]={'trades':trades[a],'funding_events':funds[a],'state_segments':segments[a],'terminal_state':b,'summary':helpers.native_summary(m,curves[a],trades[a],funds[a],segments[a])}
 assert len(decisions)==370;v=curves['BTC']+curves['ETH'];return {'decisions':decisions,'legs':legs,'terminal_books':books,'terminal_pair_state':{'side':side,'recovery':recovery,'completed_pairs':completed,'probe':probe,'streak':streak},'summary':helpers.aggregate(v,axis,legs,completed,books)}
