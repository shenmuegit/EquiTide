"""Coupled pair decisions; native per-bank cash, fills and funding remain explicit."""
import copy,math,statistics
from decimal import Decimal as D,ROUND_FLOOR
import numpy as np
from common import core,HOUR,MIN,DAY

def decide(side,entry_ns,recovery,f,E,X,t):
 if recovery:return {'close':True,'open_side':0,'reason':'recovery'}
 if not f['eligible']:return {'close':bool(side),'open_side':0,'reason':'invalid_fit'}
 if side and t-entry_ns>=48*HOUR:return {'close':True,'open_side':0,'reason':'timeout'}
 z=f['z'];fresh=1 if z<=-E else -1 if z>=E else 0
 if not side:return {'close':False,'open_side':fresh,'reason':'entry' if fresh else 'flat'}
 if fresh and fresh!=side:return {'close':True,'open_side':fresh,'reason':'reverse'}
 if side==1 and z>=-X or side==-1 and z<=X:return {'close':True,'open_side':0,'reason':'exit_crossing'}
 return {'close':False,'open_side':0,'reason':'hold'}

def _fill(books,contexts,a,change,opening,m,t,idx,trades,reason,terminal=False):
 ctx=contexts[a];before=books[a];after,z=core.trade(before,change,ctx['reference'],ctx['ADV'],ctx['sigma'],ctx['meta'],m,opening);books[a]=after;z.update(asset=a,trade_ts_ns=t,axis_index=idx,opening=opening,decision_reason=reason,terminal=terminal);trades[a].append(z);return z['status']=='filled'

def open_pair(books,contexts,side,beta,notional,m,t,idx,trades):
 assert side in [-1,1] and all(D(x['signed_units'])==0 for x in books.values())
 quantities={}
 for a,amount,sgn in [('BTC',beta*notional,-side),('ETH',notional,side)]:
  lot=D(contexts[a]['meta']['lot_size']);q=(amount/contexts[a]['prior_close']/lot).to_integral_value(rounding=ROUND_FLOOR)*lot;quantities[a]=D(sgn)*q
 if not _fill(books,contexts,'BTC',quantities['BTC'],True,m,t,idx,trades,'open_first'):
  return {'opened':False,'recovery':False}
 if not _fill(books,contexts,'ETH',quantities['ETH'],True,m,t,idx,trades,'open_second'):
  _fill(books,contexts,'BTC',-D(books['BTC']['signed_units']),False,m,t,idx,trades,'second_leg_reject_unwind');return {'opened':False,'recovery':any(D(b['signed_units'])!=0 for b in books.values())}
 return {'opened':True,'recovery':False}

def close_pair(books,contexts,m,t,idx,trades,reason,terminal=False):
 for a in ['BTC','ETH']:
  if D(books[a]['signed_units']):_fill(books,contexts,a,-D(books[a]['signed_units']),False,m,t,idx,trades,reason,terminal)
 return all(D(b['signed_units'])==0 for b in books.values())

def recent(v,m):
 ix=m['daily_indices'];daily=v[ix].tolist();tail=v[ix[330]:];s=core.stats(tail,daily[330:],40);s.update(start_utc='2026-09-14T00:01:00Z',end_exclusive_utc='2026-10-24T00:01:00Z',initial_NAV_usdt=float(tail[0]),final_NAV_usdt=float(tail[-1]),NAV_points=len(tail),NAV_sha256_f64le=core.navhash(tail),daily_equity_usdt=daily[330:],state_policy='Inherited actual day330 books, no reset or diagnostic orders.',folds=[])
 for j in range(8):
  l,h=330+5*j,335+5*j;a,b=ix[[l,h]];s['folds'].append({'fold':j+1,'start_utc':core.stamp(int(m['ts'][a])),'end_exclusive_utc':core.stamp(int(m['ts'][b])),'duration_days':5,**core.stats(v[a:b+1],daily[l:h+1],5)})
 return s

def aggregate(v,m,legs,completed,terminal):
 daily=v[m['daily_indices']].tolist();s=core.stats(v,daily,370);s['folds']=[]
 for j,(a,b) in enumerate(zip(m['fold_indices'],m['fold_indices'][1:])):
  days=min(30,370-30*j);s['folds'].append({'fold':j+1,'start_utc':core.stamp(int(m['ts'][a])),'end_exclusive_utc':core.stamp(int(m['ts'][b])),'duration_days':days,**core.stats(v[a:b+1],daily[30*j:30*j+days+1],days)})
 ss=[x['summary'] for x in legs.values()];money=['cost_usdt','funding_usdt','base_funding_same_exposure_usdt','funding_stress_increment_usdt','funding_income_usdt','funding_outflow_usdt','gross_reference_price_PnL_usdt'];counts=['executions','rejected_orders','cash_or_units_violations','funding_settlements','nonzero_funding_settlements'];s.update({k:sum(x[k] for x in ss) for k in money+counts});s.update(initial_capital_usdt=20000,final_NAV_usdt=float(v[-1]),cost_pct_initial=s['cost_usdt']/200,cost_parts_usdt={k:sum(x['cost_parts_usdt'][k] for x in ss) for k in ss[0]['cost_parts_usdt']},round_trips=completed,completed_pair_round_trips=completed,leg_round_trips=sum(x['round_trips'] for x in ss),terminal_units=str(sum(abs(D(b['signed_units'])) for b in terminal.values())),terminal_flat=all(D(b['signed_units'])==0 for b in terminal.values()),daily_equity_usdt=daily,NAV_points=len(v),NAV_sha256_f64le=core.navhash(v),axis_sha256=m['axis_sha256'],margin={'independent_sleeve_violations':sum(x['margin']['violations'] for x in ss),'minimum_individual_sleeve_cushion_usdt':min((x['margin']['minimum_equity_minus_maintenance_usdt'] for x in ss if x['margin']['minimum_equity_minus_maintenance_usdt'] is not None),default=None),'no_cross_margin_netting':True})
 s['gross_reference_PnL_to_execution_cost']=(s['gross_reference_price_PnL_usdt']+s['funding_usdt'])/s['cost_usdt'] if s['cost_usdt'] else None;s['recent40']=recent(v,m);assert abs(s['gross_reference_price_PnL_usdt']+s['funding_usdt']-s['cost_usdt']-(v[-1]-20000))<1e-8;return s

def simulate(spec,markets,m,features,mult):
 p=spec['parameters'];books={a:{'cash':'10000','signed_units':'0','entry_price':'0','entry_reference':'0'} for a in ['BTC','ETH']};trades={a:[] for a in books};funds={a:[] for a in books};segments={a:[] for a in books};segstart={a:0 for a in books};segstate=copy.deepcopy(books);vs={a:np.empty(len(m['ts'])) for a in books};start=0;side=0;entry=None;recovery=False;completed=0;wanted=0;decisions=[]
 def context(h):
  out={}
  for a,mm in markets.items():
   adv,sigma=mm['cost_inputs'][h//24];out[a]={'reference':mm['frame']['open'][h*60+1],'prior_close':mm['hour_closes'][h-1],'ADV':adv,'sigma':sigma,'meta':mm['meta']}
  return out
 for idx0 in m['controls']:
  idx=int(idx0);t=int(m['ts'][idx]);code=int(m['codes'][idx]);before=copy.deepcopy(books)
  for a,b in books.items():vs[a][start:idx]=float(b['cash'])+float(b['signed_units'])*(markets[a]['axis_prices'][start:idx]-float(b['entry_price']))
  if code==4:
   for a,mm in markets.items():
    if t not in mm['fund_lookup']:continue
    e=mm['fund_lookup'][t];b=books[a];base,amount=core.funding_amount(D(b['signed_units']),e['mark_price_at_settlement'],e['realized_rate'],mult);cash=D(b['cash'])
    if amount:b['cash']=str(cash+amount)
    funds[a].append({'source_index':e['source_index'],'settlement_ts_ns':t,'available_ts_ns':e['available_ts'],'realized_rate':str(e['realized_rate']),'mark_price':str(e['mark_price_at_settlement']),'actual_interval_hours':str(e['actual_interval_hours']),'signed_units':b['signed_units'],'base_amount_usdt':str(base),'amount_usdt':str(amount),'cash_before':str(cash),'cash_after':b['cash'],'axis_index':idx})
  elif code==6:
   h=(t-m['first_ns']-MIN)//HOUR;f=features[h-33*24];act=decide(side,entry,recovery,f,p['entry_z'],p['exit_z'],t);d={'hour':h,'signal_available_ts_ns':t-MIN,'execution_ts_ns':t,'feature_index':h-33*24,'side_before':side,'entry_ns_before':entry,'recovery_before':recovery,**act};wanted=0
   if act['close']:
    closed=close_pair(books,context(h),mult,t,idx,trades,act['reason'])
    if closed:
     completed+=int(side!=0);side=0;entry=None;recovery=False
    else:recovery=True
   if act['open_side'] and all(D(b['signed_units'])==0 for b in books.values()):wanted=act['open_side']
   decisions.append(d)
  elif code==7:
   h=(t-m['first_ns']-MIN)//HOUR
   if wanted:
    f=features[h-33*24];out=open_pair(books,context(h),wanted,D(str(f['beta'])),D(str(p['ETH_entry_notional_usdt'])),mult,t,idx,trades)
    if out['opened']:side=wanted;entry=t
    recovery=out['recovery']
   decisions[-1].update(side_after=side,entry_ns_after=entry,recovery_after=recovery,completed_pairs_so_far=completed)
  elif code==9:
   h=403*24;closed=close_pair(books,context(h),mult,t,idx,trades,'terminal',True)
   if closed:completed+=int(side!=0);side=0;entry=None;recovery=False
   else:recovery=True
  for a,b in books.items():
   if b!=before[a]:
    if idx>segstart[a]:segments[a].append({'axis_start':segstart[a],'axis_end_exclusive':idx,**segstate[a]})
    segstart[a]=idx;segstate[a]=copy.deepcopy(b)
  start=idx
 for a,b in books.items():
  vs[a][start:]=float(b['cash'])+float(b['signed_units'])*(markets[a]['axis_prices'][start:]-float(b['entry_price']));segments[a].append({'axis_start':segstart[a],'axis_end_exclusive':len(m['ts']),**segstate[a]});assert np.isfinite(vs[a]).all() and (vs[a]>0).all()
 legs={a:{'trades':trades[a],'funding_events':funds[a],'state_segments':segments[a],'terminal_state':books[a],'summary':native_summary(markets[a],vs[a],trades[a],funds[a],segments[a])} for a in books};v=vs['BTC']+vs['ETH'];summary=aggregate(v,m,legs,completed,books);return {'decisions':decisions,'legs':legs,'terminal_books':books,'terminal_pair_state':{'side':side,'entry_ns':entry,'recovery':recovery},'summary':summary}

def native_summary(m,v,trades,funding,segments):
 daily=v[m['daily_indices']].tolist();s=core.stats(v,daily,370);s['folds']=[]
 for j,(a,b) in enumerate(zip(m['fold_indices'],m['fold_indices'][1:])):s['folds'].append({'fold':j+1,'start_utc':core.stamp(m['start_ns']+j*30*core.DAY),'end_exclusive_utc':core.stamp(m['start_ns']+min((j+1)*30,370)*core.DAY),'duration_days':min(30,370-j*30),**core.stats(v[a:b+1],daily[j*30:min((j+1)*30,370)+1],min(30,370-j*30))})
 filled=[x for x in trades if x['status']=='filled'];parts={k:float(sum(D(t['cost_parts'][k]) for t in filled)) for k in ['fee','half_spread','slippage','impact','tick_rounding']};cost=sum(parts.values());fund=sum(D(x['amount_usdt']) for x in funding);basefund=sum(D(x['base_amount_usdt']) for x in funding);closedgross=sum(D(t['reference_price_PnL_usdt']) for t in filled);last=segments[-1];unrealized=D(last['signed_units'])*(m['terminal_reference_decimal']-D(last['entry_reference']));gross=closedgross+unrealized;assert abs(float(gross+fund)-cost-(v[-1]-float(v[0])))<1e-8;assert abs(math.prod(1+f['net_return_pct']/100 for f in s['folds'])-v[-1]/v[0])<1e-12
 mark=np.isin(m['codes'],[0,2,3,4,9]);mv=v[mark];minute=np.isin(m['codes'],[0,1,3,4,5,6,7,8,9]);pv=v[minute];margin=core.margin_audit(m,segments)
 s.update(initial_capital_usdt=float(v[0]),final_NAV_usdt=float(v[-1]),cost_usdt=cost,cost_pct_initial=100*cost/float(v[0]),cost_parts_usdt=parts,funding_usdt=float(fund),base_funding_same_exposure_usdt=float(basefund),funding_stress_increment_usdt=float(fund-basefund),funding_income_usdt=float(sum(D(x['amount_usdt']) for x in funding if D(x['amount_usdt'])>0)),funding_outflow_usdt=float(-sum(D(x['amount_usdt']) for x in funding if D(x['amount_usdt'])<0)),gross_reference_price_PnL_usdt=float(gross),closed_reference_price_PnL_usdt=float(closedgross),terminal_unrealized_reference_PnL_usdt=float(unrealized),gross_reference_PnL_to_execution_cost=float((gross+fund)/D(str(cost))) if cost else None,executions=len(filled),round_trips=sum(not t['opening'] for t in filled),rejected_orders=len(trades)-len(filled),cash_or_units_violations=sum(D(x['cash'])<0 for x in segments),terminal_units=segments[-1]['signed_units'],daily_equity_usdt=daily,NAV_points=len(v),NAV_sha256_f64le=core.navhash(v),axis_sha256=m['axis_sha256'],axis_prices_sha256_f64le=m['axis_price_sha256_f64le'],mark_observation_drawdown_pct=100*float(np.max(1-mv/np.maximum.accumulate(mv))),trade_proxy_drawdown_pct=100*float(np.max(1-pv/np.maximum.accumulate(pv))),margin=margin,funding_settlements=len(funding),nonzero_funding_settlements=sum(D(x['signed_units'])!=0 for x in funding));return s
