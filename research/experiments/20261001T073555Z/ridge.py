"""Training-only original factors, matured carry labels and reserved Ridge models."""
from __future__ import annotations
import bisect,hashlib,json,math,sys
from decimal import Decimal
from pathlib import Path
import numpy as np
import polars as pl
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
import importlib.util

def module(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
carry=module('carry_prior_ridge',ROOT/'research/experiments/20261001T053425Z/carry.py')
sys.modules['carry']=carry
prev=module('native_prior_ridge',ROOT/'research/experiments/20261001T053425Z/evaluate.py')
old=carry.old
Ledger,FundingBook,HOUR,MINUTE,DAY,VERSION=carry.Ledger,carry.FundingBook,carry.HOUR,carry.MINUTE,carry.DAY,carry.VERSION
per_side,load,ns,utc=carry.per_side,carry.load,carry.ns,carry.utc
from usdt_quant.backtest import BacktestData,MarketPoint,InstrumentMetadata,run_backtest
from usdt_quant.strategy import BacktestConfig
from usdt_quant.research import factor_frame,label_frame,FACTORS

def train_mask(times,ends,available,start,end):
 return (times>=start)&(times<end)&(ends<end)&(available<end)

def fit_ridge(x,y,alpha):
 p=Pipeline([('impute',SimpleImputer(strategy='median')),('scale',StandardScaler()),('model',Ridge(alpha=alpha,solver='svd'))]);p.fit(x,y);return p

def native_data(data,m=1):
 d=Decimal;meta=data['meta']
 market=tuple(MarketPoint.from_mid(r['ts'],r['close'],r['close_perp'],data['marks'][r['ts']-HOUR]['close'],d(0)) for r in data['rows'])
 metadata=InstrumentMetadata(d(1),d(str(meta['spot_lot'])),d(str(meta['perp_lot'])),d(str(meta['spot_tick'])),d(str(meta['perp_tick'])))
 events=tuple(prev.StressedFundingPoint(e['ts'],e['available'],d(str(e['rate']*(m if e['rate']<0 else 1))),d(str(e['mark'])),d(str(e['hours'])),d(str(e['rate']))) for e in data['events'])
 return BacktestData(market,events,tuple(e.observation() for e in events),metadata)

def native_config(data,m=1,whole_history=False):
 d=Decimal;start=ns('2026-03-18T00:00:00Z');end=ns('2026-03-21T00:00:00Z');row=data['rows'][data['times'].index(start)];q=math.floor(4500/float(row['close'])/data['meta']['common_lot'])*data['meta']['common_lot']
 return BacktestConfig(baseline='M1',data_version=VERSION,exchange='binance',base_asset=data['asset'],start_ns=data['times'][0] if whole_history else start,end_ns=data['times'][-1] if whole_history else end,decision_interval_ns=HOUR,holding_period_ns=24*HOUR,funding_window=21,initial_spot_usdt=d(5000),initial_perp_usdt=d(5000),target_spot_base=d(str(q)),spot_taker_fee=d('.001')*m,perp_taker_fee=d('.0002')*m,execution_bps_per_leg=d(5)*m,buffer_usdt=d(1))

def continuous_labels(data):
 rows=[];event_times=[e['ts'] for e in data['events']];span=24
 for i,r in enumerate(data['rows']):
  t=r['ts'];j=i+span
  if j>=len(data['rows']):continue
  exitrow=data['rows'][j];assert exitrow['ts']==t+24*HOUR
  if t//DAY not in data['costs'][0] or t//DAY not in data['costs'][1]:continue
  q=math.floor(2500/float(r['close'])/data['meta']['common_lot'])*data['meta']['common_lot']
  total=0.;execution_cost=0.;fees=0.
  for row,change in ((r,q),(exitrow,-q)):
   refs=[float(row['fill']),float(row['fill_perp'])];_,details=per_side(data,row['ts'],change,refs)
   for k in (0,1):
    sign=change if k==0 else -change;tick=data['meta']['spot_tick' if k==0 else 'perp_tick'];fee=details[k]['base_fee']
    px=old.execution_price(refs[k],sign,fee,.0001,.0002,details[k]['impact'],tick)
    paid=abs(change*px)*fee;total-=sign*px+paid;fees+=paid;execution_cost+=abs(change)*abs(px-refs[k])+paid
  entry=t+MINUTE;end=exitrow['ts']+MINUTE;events=data['events'][bisect.bisect_right(event_times,entry):bisect.bisect_right(event_times,end)]
  funding=sum(q*e['mark']*e['rate'] for e in events);net=total+funding
  rows.append({'decision_ts':t,'entry_ts':entry,'label_end_ts':end,'label_available_ts':max([end]+[e['available'] for e in events]),'y_net':net/10000,'target_quantity':q,'funding_usdt':funding,'fees_usdt':fees,'execution_cost_usdt':execution_cost})
 return pl.DataFrame(rows)

def fitted_predictions(frame,folds,alpha,native=False):
 times=frame['decision_ts'].to_numpy();ends=frame['label_end_ts'].fill_null(2**63-1).to_numpy();av=frame['label_available_ts'].fill_null(2**63-1).to_numpy();y=frame['y_net'].to_numpy();pred={};audits=[]
 for f in folds:
  start=ns(f['train_start_utc']);end=ns(f['train_end_exclusive_utc']);mask=train_mask(times,ends,av,start,end)&np.isfinite(y)
  train=frame.filter(pl.Series(mask));coverage={name:train[name].drop_nulls().len()/train.height for name in FACTORS};active=[name for name in FACTORS if coverage[name]>=.98];assert active and train.height>len(active)+1
  model=fit_ridge(train.select(active).to_numpy(),train['y_net'].to_numpy(),alpha)
  test=frame.filter((pl.col('decision_ts')>=f['test_start_signal_ns'])&(pl.col('decision_ts')<f['test_end_signal_ns']))
  values=model.predict(test.select(active).to_numpy());pred.update(zip(test['decision_ts'].to_list(),map(float,values)))
  imp=model.named_steps['impute'];scale=model.named_steps['scale'];est=model.named_steps['model'];indices=np.flatnonzero(mask).tolist()
  audits.append({'fold':f['fold'],'alpha':alpha,'train_start':start,'train_end_exclusive':end,'model_available_ts':f['test_start_signal_ns'],'native_label_quantity_known_ts':f['test_start_signal_ns'] if native else None,'test_start_signal_ns':f['test_start_signal_ns'],'test_end_signal_ns':f['test_end_signal_ns'],'training_rows':train.height,'purged_unmatured':int(np.sum((times>=start)&(times<end)&np.isfinite(y)&((ends>=end)|(av>=end)))),'unavailable_label_rows':int(np.sum((times>=start)&(times<end)&~np.isfinite(y))),'total_excluded_training_rows':int(np.sum((times>=start)&(times<end)&~mask)),'train_max_decision':int(train['decision_ts'].max()),'train_max_label_end':int(train['label_end_ts'].max()),'train_max_label_available':int(train['label_available_ts'].max()),'active_factors':active,'factor_coverage':coverage,'training_row_indices':indices,'training_data_sha256':hashlib.sha256(json.dumps(train.to_dicts(),sort_keys=True,allow_nan=False).encode()).hexdigest(),'imputer_medians':imp.statistics_.tolist(),'scale_mean':scale.mean_.tolist(),'scale_scale':scale.scale_.tolist(),'ridge_coefficients':est.coef_.tolist(),'ridge_intercept':float(est.intercept_),'prediction_min':float(values.min()),'prediction_max':float(values.max()),'predicted_positive_hours':int(np.sum(values>0)),'predictions':[[int(t),float(v)] for t,v in zip(test['decision_ts'],values)]})
 return pred,audits

def native_run(data,p,m,prediction):
 cfg=native_config(data,m);directory=ROOT/'data/runs/20261001T073555Z_native'/f"M1_{data['asset']}_c{m}"
 result=run_backtest(cfg,native_data(data,m),directory,{t:Decimal(str(v)) for t,v in prediction.items()})
 result['full_native_artifacts']={name:[json.loads(line) for line in Path(path).read_text().splitlines()] for name,path in result['artifacts'].items() if name!='summary'}
 result['actual_source_funding']=[e for e in data['events'] if cfg.start_ns<=e['ts']<=cfg.end_ns];result['forecast_source']='first pre-embargo180d matured original24h-label model; frozen base-cost predictions for72h and all three cost scenarios'
 return result

def simulate(data,parameters,multiplier,folds,predictions):
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
   prediction=predictions[t];action='enter' if prediction*known_nav>buffer else 'skip'
   if quantity*min(known)<max(data['meta']['spot_min'],data['meta']['perp_min']):action='below_min_notional'
   if action=='enter':
    if execute(row,quantity,'entry'):expiry=t+h*HOUR;entry_count+=1
    else:action='spot_cash_rejected'
   else:skipped+=1
   decisions.append({'ts':t,'action':action,'prediction_y_net':prediction,'predicted_net_usdt':prediction*known_nav,'hourly_rate':rate,'known_spot':known[0],'known_perp':known[1],'target_quantity':quantity,'per_leg_fraction':fraction,'estimated_roundtrip_cost_usdt':2*quantity*(known[0]*rates[0]+known[1]*rates[1])})
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

