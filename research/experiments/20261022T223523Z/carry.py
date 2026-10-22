"""Matched carry simulation with causal funding, isolated ledgers and existing cost functions."""
from __future__ import annotations
import bisect,csv,hashlib,importlib.util,json,math,sys
from decimal import Decimal
from pathlib import Path
import numpy as np
import polars as pl
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
HOUR=3600*10**9;MINUTE=60*10**9;DAY=24*HOUR
VERSION='20250916T000000Z_20260916T000000Z_archive_20260929'

def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);sys.modules[name]=mod;spec.loader.exec_module(mod);return mod
old=module('previous_cost_accounting',ROOT/'research/experiments/20261001T033355Z/evaluate.py')
utc,ns=old.utc,old.ns

class Ledger:
 def __init__(self,capital):self.spot_cash=capital/2;self.perp_cash=capital/2;self.q=0.;self.perp_entry=0.
 def nav(self,spot,perp):return self.spot_cash+self.q*spot+self.perp_cash+self.q*(self.perp_entry-perp)
 def trade(self,change,spot,perp,spot_fee,perp_fee):
  assert change!=0
  self.spot_cash-=change*spot+abs(change*spot)*spot_fee
  self.perp_cash-=abs(change*perp)*perp_fee
  if change>0:
   assert self.q==0;self.perp_entry=perp;self.q=change
  else:
   assert abs(change+self.q)<1e-8;self.perp_cash+=self.q*(self.perp_entry-perp);self.q=0.;self.perp_entry=0.

class FundingBook:
 def __init__(self,events):
  self.events=events;self.visible=sorted(events,key=lambda e:e['available']);self.available=[e['available'] for e in self.visible]
 def hourly_rate(self,t,window):
  n=bisect.bisect_right(self.available,t)
  if n<window:return None
  return float(np.median([e['rate']/e['hours'] for e in self.visible[n-window:n]]))
 def settle(self,index,cutoff,ledger,multiplier,details=None):
  while index<len(self.events) and self.events[index]['ts']<=cutoff:
   e=self.events[index];raw=ledger.q*e['mark']*e['rate'];amount=raw if raw>=0 else raw*multiplier
   if ledger.q:
    ledger.perp_cash+=amount
    if details is not None:details.append({**e,'quantity':ledger.q,'base_amount_usdt':raw,'amount_usdt':amount,'stress_increment_usdt':amount-raw})
   index+=1
  return index

def b1_actions(rate,perp_notional,hours,buffer,spot_rate,perp_rate,entered,spot_notional=None):
 if rate is None:return 'hold' if entered else 'skip'
 spot_notional=perp_notional if spot_notional is None else spot_notional
 cost=(spot_notional*spot_rate+perp_notional*perp_rate)*(1 if entered else 2)
 eligible=perp_notional*rate*hours-cost>buffer
 return ('hold' if eligible else 'exit') if entered else ('enter' if eligible else 'skip')

def load(asset):
 directory=ROOT/'data/normalized/binance'/asset/f'binance_{asset}_{VERSION}'
 frames={name:pl.read_parquet(directory/(name+'.parquet')) for name in ('spot_bars','perp_bars','mark_hour_bars','funding_settlement','perp_instrument_meta')}
 for key in ('spot_bars','perp_bars'):
  f=frames[key];assert f.height==525600 and f['is_closed'].all();assert f['open_ts'].diff().drop_nulls().unique().to_list()==[MINUTE]
 def hourly(f):return f.group_by((pl.col('open_ts')//HOUR*HOUR+HOUR).alias('ts'),maintain_order=True).agg(pl.col('close').last().alias('close')).sort('ts')
 s,p=hourly(frames['spot_bars']),hourly(frames['perp_bars'])
 fills=[]
 for f in (frames['spot_bars'],frames['perp_bars']):
  fills.append(f.filter(pl.col('open_ts')%HOUR==MINUTE).select((pl.col('open_ts')-MINUTE).alias('ts'),pl.col('open').alias('fill')))
 merged=s.join(p,on='ts',suffix='_perp').join(fills[0],on='ts').join(fills[1],on='ts',suffix='_perp').sort('ts')
 marks={r['open_ts']:r for r in frames['mark_hour_bars'].to_dicts()}
 events=[{'ts':int(e['settlement_ts']),'available':int(e['available_ts']),'rate':float(e['realized_rate']),'mark':float(e['mark_price_at_settlement']),'hours':float(e['actual_interval_hours'])} for e in frames['funding_settlement'].to_dicts()]
 assert len(events)==1095 and all(e['mark']>0 and e['hours']>0 and e['available']>=e['ts'] for e in events)
 perpm=frames['perp_instrument_meta'].to_dicts()[0]
 spot_raw=json.loads((ROUND/'spot_metadata_snapshot.json').read_text() if (ROUND/'spot_metadata_snapshot.json').exists() else (ROOT/'data/raw/research_20261001_perp/spot_exchangeInfo.json').read_text());spotm=next(x for x in spot_raw['symbols'] if x['symbol']==asset+'USDT');filters={x['filterType']:x for x in spotm['filters']}
 slot=float(filters['LOT_SIZE']['stepSize']);plot=float(perpm['lot_size']);common=max(slot,plot)
 assert abs(common/slot-round(common/slot))<1e-8 and abs(common/plot-round(common/plot))<1e-8
 meta={'spot_lot':slot,'perp_lot':plot,'common_lot':common,'spot_tick':float(filters['PRICE_FILTER']['tickSize']),'perp_tick':float(perpm['tick_size']),'spot_min':float(filters.get('NOTIONAL',filters.get('MIN_NOTIONAL',{})).get('minNotional',0)),'perp_min':float(perpm['min_notional'])}
 hashes={name:hashlib.sha256((directory/(name+'.parquet')).read_bytes()).hexdigest() for name in frames}
 return {'asset':asset,'rows':merged.to_dicts(),'times':merged['ts'].to_list(),'marks':marks,'events':events,'book':FundingBook(events),'costs':[old.cost_table(frames['spot_bars']),old.cost_table(frames['perp_bars'])],'meta':meta,'hashes':hashes,'frames':frames}

def per_side(data,t,q,prices):
 rates=[];details=[]
 for j,price in enumerate(prices):
  adv,sigma=data['costs'][j][t//DAY];part=abs(q)*price/adv
  assert part<=.001,'declared participation bound exceeded'
  impact=.5*sigma*math.sqrt(part)
  fee=.001 if j==0 else .0005;rate=fee+.0001+.0002+impact
  rates.append(rate);details.append({'ADV':adv,'vol':sigma,'participation':part,'impact':impact,'base_fee':fee})
 return rates,details

def simulate(data,parameters,multiplier,folds):
 start=folds[0]['test_start_signal_ns'];end=folds[-1]['test_end_signal_ns'];i0=data['times'].index(start);i1=data['times'].index(end)
 l=Ledger(10000);book=data['book'];index=bisect.bisect_left([x['ts'] for x in data['events']],start)
 eq=[10000.];trades=[];funding=[];violations=[];decisions=[];boundaries={};expiry=None;entry_count=0;skipped=0
 baseline=parameters['baseline'];h=parameters['holding_hours'];fraction=parameters['per_leg_fraction'];buffer=parameters['buffer_usdt'];bounds={f['test_start_signal_ns'] for f in folds}|{end}
 def execute(row,change,reason):
  prices=[float(row['fill']),float(row['fill_perp'])];rates,detail=per_side(data,row['ts'],change,prices)
  px=[];fees=[];costs=[]
  for leg in (0,1):
   sign=change if leg==0 else -change;tick=data['meta']['spot_tick' if leg==0 else 'perp_tick']
   imp=detail[leg]['impact']*multiplier
   price=old.execution_price(prices[leg],sign,detail[leg]['base_fee']*multiplier,.0001*multiplier,.0002*multiplier,imp,tick)
   fee=abs(change*price)*detail[leg]['base_fee']*multiplier;px.append(price);fees.append(fee);costs.append(abs(change)*abs(price-prices[leg])+fee)
  if change>0 and change*px[0]+fees[0]>l.spot_cash:return False
  l.trade(change,px[0],px[1],.001*multiplier,.0005*multiplier)
  for leg in (0,1):trades.append({'ts':row['ts']+MINUTE,'leg':('spot','perp')[leg],'side':('buy' if change>0 else 'sell') if leg==0 else ('sell' if change>0 else 'buy'),'quantity':abs(change),'reference':prices[leg],'execution':px[leg],'fee_usdt':fees[leg],'cost_usdt':costs[leg],'reason':reason,**detail[leg]})
  return True
 for i in range(i0,i1+1):
  row=data['rows'][i];t=row['ts'];fill=[float(row['fill']),float(row['fill_perp'])];known=[float(row['close']),float(row['close_perp'])]
  index=book.settle(index,t,l,multiplier,funding)
  known_nav=l.nav(*known)  # sizing sees only cash already settled at decision time
  rate=book.hourly_rate(t,21)
  index=book.settle(index,t+MINUTE,l,multiplier,funding)
  if t in bounds:boundaries[t]=l.nav(*fill)
  if t==end:
   if l.q:execute(row,-l.q,'terminal_exit')
  elif l.q:
   action='hold';remaining=max(0,(expiry-t)/HOUR)
   if t>=expiry:action='exit'
   elif baseline=='B1':
    rates,_=per_side(data,t,l.q,known);action=b1_actions(rate,l.q*known[1],remaining,buffer,*rates,True,l.q*known[0])
   if action=='exit':execute(row,-l.q,'fixed_expiry' if t>=expiry else 'remaining_funding_exit');expiry=None
   if baseline=='B1':decisions.append({'ts':t,'action':action,'hourly_rate':rate,'remaining_hours':remaining})
  elif t+h*HOUR<=end:
   quantity=math.floor(fraction*known_nav/known[0]/data['meta']['common_lot'])*data['meta']['common_lot']
   assert quantity>0
   rates,_=per_side(data,t,quantity,known)
   action='enter' if baseline=='B0' else b1_actions(rate,quantity*known[1],h,buffer,*rates,False,quantity*known[0])
   if quantity*min(known)<max(data['meta']['spot_min'],data['meta']['perp_min']):action='below_min_notional'
   if action=='enter':
    if execute(row,quantity,'entry'):expiry=t+h*HOUR;entry_count+=1
    else:action='spot_cash_rejected'
   else:skipped+=1
   decisions.append({'ts':t,'action':action,'hourly_rate':rate,'known_spot':known[0],'known_perp':known[1],'target_quantity':quantity,'per_leg_fraction':fraction,'estimated_roundtrip_cost_usdt':2*quantity*(known[0]*rates[0]+known[1]*rates[1])})
  if l.spot_cash<-.00001:violations.append({'ts':t,'kind':'spot_cash','value':l.spot_cash})
  if l.q:
   high=float(data['marks'][t]['high']);margin=l.perp_cash+l.q*(l.perp_entry-high);maintenance=.01*l.q*high
   if margin<=maintenance:violations.append({'ts':t,'kind':'conservative_hourly_perp_margin','equity':margin,'maintenance':maintenance})
  value=l.nav(*fill);assert value>0 and math.isfinite(value);eq.append(value)
 assert not l.q
 boundaries[end]=eq[-1]
 fold_results=[]
 for f in folds:
  a=data['times'].index(f['test_start_signal_ns'])-i0;b=data['times'].index(f['test_end_signal_ns'])-i0
  curve=[boundaries[f['test_start_signal_ns']]]+eq[a+1:b+1]+[boundaries[f['test_end_signal_ns']]]
  fold_results.append({**f,**old.metrics(curve,28*24,True),'start_nav':curve[0],'end_nav':curve[-1]})
 assert abs(np.prod([x['end_nav']/x['start_nav'] for x in fold_results])-eq[-1]/10000)<1e-9
 cost=sum(x['cost_usdt'] for x in trades);fund=sum(x['amount_usdt'] for x in funding);net=eq[-1]-10000;gross=net+cost
 return {**old.metrics(eq,(end-start)/HOUR,True),'initial_capital_usdt':10000,'final_NAV':eq[-1],'round_trips':entry_count,'executions':len(trades),'positive_folds_1x':sum(int(x['net_return_pct']>0) for x in fold_results),'execution_cost_usdt':cost,'execution_cost_pct_initial':cost/100,'funding_usdt':fund,'gross_PNL_before_execution_cost':gross,'gross_to_execution_cost':gross/cost if cost else None,'cash_margin_violations':violations,'folds':fold_results,'trades':trades,'funding_events':funding,'decisions':decisions,'skipped':skipped,'equity':eq,'equity_signal_times':data['times'][i0:i1+1]}

if __name__=='__main__':
 print('Use evaluate.py; reserve all configurations first.')
