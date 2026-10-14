#!/usr/bin/env python3
"""Evaluate the frozen monthly volatility-managed BTC/ETH cash-sleeve grid."""
from __future__ import annotations
import csv,hashlib,json,math,os,statistics,sys,time
from datetime import datetime,timezone
from decimal import Decimal as D
from pathlib import Path
import numpy as np
import polars as pl
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sys.path.insert(0,str(ROOT/'research/experiments/20261001T133655Z'));from kernel import floor_step,adverse_tick
MIN=60_000_000_000;DAY=1440*MIN;SQRT365=math.sqrt(365.0)

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def stamp(ns):return datetime.fromtimestamp(ns/1e9,timezone.utc).isoformat().replace('+00:00','Z')
def dec(x):return D(str(x))
def clean(x):return json.loads(json.dumps(x,default=str,ensure_ascii=False,allow_nan=False))
def drawdown(x):
 a=np.asarray(x,dtype=np.float64);peak=np.maximum.accumulate(a);v=1-a/peak;j=int(np.argmax(v));return float(100*v[j]),int(np.argmax(a[:j+1])),j

def load_asset(asset):
 paths=[ROOT/f'data/normalized/binance/{asset}/binance_{asset}_20240916T000000Z_20250916T000000Z_transfer_20261001/spot_bars.parquet',ROOT/f'data/normalized/binance/{asset}/binance_{asset}_20250916T000000Z_20260916T000000Z_archive_20260929/spot_bars.parquet']
 frames=[];files=[]
 for p in paths:
  f=pl.read_parquet(p,columns=['open_ts','available_ts','open','close','base_volume','quote_volume','is_closed'])
  assert f.height==365*1440 and f['is_closed'].all() and f['open_ts'].is_sorted()
  assert (f['open_ts'].diff().drop_nulls()==MIN).all() and (f['available_ts']-f['open_ts']==MIN).all()
  assert (f['open']>0).all() and (f['close']>0).all() and (f['base_volume']>=0).all() and (f['quote_volume']>=0).all()
  files.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size,'rows':f.height});frames.append(f)
 f=pl.concat(frames,how='vertical_relaxed').sort('open_ts');assert f.height==730*1440
 assert (f['open_ts'].diff().drop_nulls()==MIN).all()
 opens=f['open'].to_numpy();closes=f['close'].cast(pl.Float64).to_numpy()
 qv=f['quote_volume'].cast(pl.Float64).to_numpy();bv=f['base_volume'].cast(pl.Float64).to_numpy();ts=f['open_ts'].to_numpy()
 assert int(ts[0])==1726444800000000000
 daily=f.with_columns((pl.col('open_ts')//DAY).alias('day')).group_by('day').agg(
     pl.col('close').last().alias('close'),pl.col('available_ts').last().alias('available_ns'),
     pl.col('quote_volume').sum().alias('quote_volume')).sort('day').to_dicts()
 assert len(daily)==730
 return {'asset':asset,'open':opens,'close':closes,'open_decimal':f['open'],'quote':qv,'base':bv,'ts':ts,'daily':daily,'files':files}

def cost_inputs(daily,day):
 if day<21:raise ValueError(f'need at least 21 closed daily rows before day {day}')
 adv=sum((dec(x['quote_volume']) for x in daily[day-20:day]),D(0))/D(20)
 closes=[float(daily[i]['close']) for i in range(day-21,day)]
 sigma=statistics.stdev(math.log(b/a) for a,b in zip(closes,closes[1:]))
 return adv,D(str(sigma))

def vwap5(m,minute):
 qq=float(np.sum(m['quote'][minute-5:minute],dtype=np.float64));bb=float(np.sum(m['base'][minute-5:minute],dtype=np.float64))
 return dec(qq/bb) if bb else D(0)

def rebalance(cash,units,target_fraction,ref,adv,sigma,mult,filters,avg,asset,ts,minute_index,reason):
 nav=cash+units*ref; target=nav*target_fraction; held=units*ref; delta=target-held
 side='buy' if delta>D('0.00000001') else ('sell' if delta<D('-0.00000001') else None)
 if side is None:return cash,units,{'status':'no_order','asset':asset,'decision_reason':reason,'cash_after':str(cash),'units_after':str(units),'minute_index':minute_index}
 buy=side=='buy'; budget=abs(delta); participation=budget/adv if adv>0 else D('Infinity')
 row={'asset':asset,'side':side,'decision_reason':reason,'execution_utc':stamp(ts),'minute_index':minute_index,'reference':str(ref),'target_fraction':str(target_fraction),'pre_nav':str(nav),'order_budget_estimate':str(budget),'lagged_ADV':str(adv),'lagged_sigma':str(sigma),'participation_estimate':str(participation),'cost_multiplier':mult,'proxy_VWAP5':str(avg)}
 def reject(why):return cash,units,{**row,'status':'rejected','reason':why,'cash_after':str(cash),'units_after':str(units)}
 if participation>D('0.001'):return reject('participation')
 spread=D('.0001')*mult;slip=D('.0002')*mult;fee=D('.001')*mult
 impact=D('.5')*sigma*participation.sqrt()*mult
 theoretical=ref*(D(1)+(spread+slip+impact)*(1 if buy else -1))
 pf=filters['PRICE_FILTER'];lf=filters['LOT_SIZE'];nf=filters['NOTIONAL']
 price=adverse_tick(theoretical,D(pf['tickSize']),buy)
 if not D(pf['minPrice'])<=price<=D(pf['maxPrice']):return reject('price')
 if buy:
  q=floor_step(min(budget/(price*(1+fee)),cash/(price*(1+fee))),D(lf['stepSize']))
 else:q=floor_step(min(budget/price,units),D(lf['stepSize']))
 if q==0 or q<D(lf['minQty']):return cash,units,{**row,'status':'skipped_below_lot','cash_after':str(cash),'units_after':str(units)}
 notional=q*price
 if not D(nf['minNotional'])<=notional<=D(nf['maxNotional']):return reject('notional')
 percent=filters.get('PERCENT_PRICE_BY_SIDE')
 if percent:
  prefix='bid' if buy else 'ask'
  if not avg*D(percent[prefix+'MultiplierDown'])<=price<=avg*D(percent[prefix+'MultiplierUp']):return reject('percent_price_proxy')
 actual_participation=q*ref/adv if adv>0 else D('Infinity')
 if actual_participation>D('.001'):return reject('rounded_participation')
 costs={'fee':q*price*fee,'half_spread':q*ref*spread,'slippage':q*ref*slip,'impact':q*ref*impact,'tick_rounding':q*abs(price-theoretical)}
 total=sum(costs.values(),D(0));fee_paid=costs['fee']
 cash2=cash-notional-fee_paid if buy else cash+notional-fee_paid
 units2=units+q if buy else units-q
 assert cash2>=0 and units2>=0
 assert abs(nav-(cash2+units2*ref)-total)<D('1e-18')
 out={**row,'status':'filled','execution':str(price),'theoretical_execution':str(theoretical),'quantity':str(q),'fee_rate':str(fee),'half_spread_rate':str(spread),'slippage_rate':str(slip),'impact_rate':str(impact),'actual_participation':str(actual_participation),'cost_usdt':str(total),'cost_parts':{k:str(v) for k,v in costs.items()},'cash_after':str(cash2),'units_after':str(units2)}
 return cash2,units2,out

def run_sleeve(spec,m,filters,mult,is_comparator=False):
 plan=json.loads((ROUND/'plan.json').read_text());start_day=368;end_day=728
 p=spec['parameters'];L=int(p.get('realized_vol_lookback_days',0));target=float(p.get('target_annual_volatility',1));sma_days=int(p.get('sma_gate_days',200))
 oos_minutes_start=start_day*1440+1;terminal_min=end_day*1440+1
 dates=[datetime.fromtimestamp(int(m['ts'][d*1440])/1e9,timezone.utc).date() for d in range(730)]
 rebalance_days=[start_day]+[d for d in range(start_day+1,end_day) if dates[d].day==1]
 cash=D('1000');units=D(0);trades=[];decisions=[];order_days=set();
 if is_comparator:rebalance_days=[start_day]
 for d in rebalance_days:
  minute=d*1440+1; ref=dec(m['open_decimal'][minute]); avg=vwap5(m,minute);adv,sigma=cost_inputs(m['daily'],d)
  if is_comparator:frac=1.0;reason='initial_buy_hold_entry'
  else:
   close_hist=[float(m['daily'][i]['close']) for i in range(d-L-1,d)]
   rets=[math.log(b/a) for a,b in zip(close_hist,close_hist[1:])]
   realized=statistics.stdev(rets)*SQRT365
   gate_window=[float(m['daily'][i]['close']) for i in range(d-sma_days,d)]
   gate_sma=sum(gate_window)/float(sma_days);signal_close=float(m['daily'][d-1]['close']);eligible=signal_close>gate_sma
   frac=(min(1.0,(target/realized)**2) if realized>0 else 1.0) if eligible else 0.0
   reason=f'monthly target; SMA200 close={signal_close:.10f}; sma={gate_sma:.10f}; eligible={eligible}; L={L}; realized_ann={realized:.10f}; target={target:.4f}'
  cash,units,t=rebalance(cash,units,D(str(frac)),ref,adv,sigma,mult,filters,avg,m['asset'],int(m['ts'][minute]),minute,reason)
  if t['status']!='no_order':trades.append(t)
  if t['status']=='filled':order_days.add(d)
  if t['status'] in ('no_order','skipped_below_lot'):
   decisions.append({'asset':m['asset'],'date':str(dates[d]),'target_fraction':str(frac),'status':t['status'],'reason':reason})
 if units>0:
  d=end_day;minute=terminal_min;ref=dec(m['open_decimal'][minute]);avg=vwap5(m,minute);adv,sigma=cost_inputs(m['daily'],d)
  cash,units,t=rebalance(cash,units,D(0),ref,adv,sigma,mult,filters,avg,m['asset'],int(m['ts'][minute]),minute,'terminal_liquidation');t['terminal']=True;trades.append(t)
 terminal_nav=float(cash+units*dec(m['open_decimal'][terminal_min]));assert units==0 or trades[-1]['status']!='filled'
 # Replay changes in cash/units on the historical minute-close series; no minute extrema are used.
 start= oos_minutes_start; stop=terminal_min
 idx=np.arange(start,stop+1,dtype=np.int64); minute_closes=m['close'][idx]
 d_cash=np.zeros(len(idx),dtype=np.float64);d_units=np.zeros(len(idx),dtype=np.float64)
 c0=D('1000');u0=D(0);event_marks=[]
 for t in trades:
  if t['status']!='filled':continue
  mi=int(t['minute_index'])
  pos=mi-start
  assert 0<=pos<len(idx)
  ca=dec(t['cash_after']);ua=dec(t['units_after'])
  d_cash[pos]+=float(ca-c0);d_units[pos]+=float(ua-u0)
  c0,u0=ca,ua
  event_marks.append((mi,float(ca+ua*dec(t['reference']))))
 cash_arr=1000.0+np.cumsum(d_cash);unit_arr=np.cumsum(d_units);navclose=cash_arr+unit_arr*minute_closes
 sample=[1000.0];cursor=0
 for mi,value in event_marks:
  pos=mi-start
  if pos>=cursor:sample.extend(navclose[cursor:pos].tolist())
  sample.append(value);sample.append(float(navclose[pos]));cursor=max(cursor,pos+1)
 sample.extend(navclose[cursor:].tolist());mdd=drawdown(sample)[0]
 daily_marks=np.arange(start+1439,stop,1440,dtype=np.int64)
 daily_nav=[1000.0]+[float(navclose[i-start]) for i in daily_marks]+[terminal_nav]
 daily_dd=drawdown(daily_nav)[0]
 # 12 continuous 30-day return folds based on daily marked NAV.
 folds=[]
 for k in range(12):
  a=k*30;b=(k+1)*30
  folds.append({'fold':k+1,'start_utc':stamp(int(m['ts'][(start_day+a)*1440+1])),'end_exclusive_utc':stamp(int(m['ts'][(start_day+b)*1440+1])),'start_nav_usdt':daily_nav[a],'end_nav_usdt':daily_nav[b],'net_return_pct':(daily_nav[b]/daily_nav[a]-1)*100})
 costparts={key:str(sum((dec(t.get('cost_parts',{}).get(key,'0')) for t in trades),D(0))) for key in ('fee','half_spread','slippage','impact','tick_rounding')}
 cost=sum((dec(x) for x in costparts.values()),D(0));gross=dec(terminal_nav)-D('1000')+cost
 rebalances=sum(t['status']=='filled' and not t.get('terminal') for t in trades)
 daily_returns=np.asarray(daily_nav[1:-1],dtype=np.float64)[1:]/np.asarray(daily_nav[1:-1],dtype=np.float64)[:-1]-1
 daily_sd=float(np.std(daily_returns,ddof=1)) if len(daily_returns)>1 else 0.0
 ddaily,_,_=drawdown(daily_nav)
 cagr=(terminal_nav/1000.0)**(365.0/360.0)-1
 return {'terminal_nav_usdt':str(terminal_nav),'terminal_cash_usdt':str(cash),'net_pnl_usdt':str(dec(terminal_nav)-D(1000)),'net_return_pct':(terminal_nav/1000-1)*100,'cost_usdt':str(cost),'cost_parts_usdt':costparts,'gross_reference_pnl_usdt':str(gross),'gross_to_cost':float(gross/cost) if cost else None,'fills':sum(t['status']=='filled' for t in trades),'rebalances':rebalances,'rejected_orders':sum(t['status']=='rejected' for t in trades),'skipped_below_lot':sum(t['status']=='skipped_below_lot' for t in trades),'round_trips':sum(t['side']=='sell' for t in trades if t['status']=='filled'),'terminal_units':str(units),'terminal_reference_price':str(ref),'max_drawdown_1m_sampled_pct':mdd,'daily_sample_drawdown_pct':ddaily,'drawdown_scope':'OOS 1-minute closes plus immediate post-fill reference marks; no intra-minute extrema.','daily_nav_usdt':daily_nav,'folds':folds,'minute_nav_sha256':hashlib.sha256(np.asarray(navclose,dtype='<f8').tobytes()).hexdigest(),'minute_nav_samples':len(navclose),'_minute_nav':navclose,'trades':trades,'decisions':decisions,'filled_rebalance_days':sorted(order_days),'daily_sharpe_annualized':float(np.mean(daily_returns)/daily_sd*math.sqrt(365)) if daily_sd else None,'cagr_pct':cagr*100,'calmar_daily':cagr/(ddaily/100) if ddaily else None}

def main():
 started=time.time();plan=json.loads((ROUND/'plan.json').read_text());batch=json.loads((ROUND/'batch.json').read_text());sources=json.loads((ROUND/'exchange_filters.json').read_text())
 registry_records=registry.read_records(Path(os.environ.get('VOLMANAGED_REGISTRY_LEDGER',ROOT/'research/automation/registry.jsonl')))
 for row in batch:
  s=json.loads((ROOT/row['spec']).read_text());fp=registry.fingerprint(s);r=registry_records.get(fp)
  assert r and r['status']=='reserved' and r['result_available'] is False, f"Not reserved: {row['name']}"
 markets={x:load_asset(x) for x in ('BTC','ETH')};filters=sources['symbols'];cfgs={};trade_rows=[];decision_rows=[];daily_rows=[]
 # UTC epoch day indices are fixed by the continuous source-series start 2024-09-16.
 assert stamp(int(markets['BTC']['ts'][368*1440]))=='2025-09-19T00:00:00Z' and stamp(int(markets['BTC']['ts'][728*1440]))=='2026-09-14T00:00:00Z'
 data={'built_at_utc':datetime.now(timezone.utc).isoformat(),'frozen_plan_sha256':sha(ROUND/'plan.json'),'exchange_filter_raw_sha256':sources['raw_sha256'],'assets':{a:{'source_files':m['files'],'one_minute_rows':len(m['open']),'daily_rows':len(m['daily']),'daily_closes_sha256_f64le':hashlib.sha256(np.asarray([float(x['close']) for x in m['daily']],dtype='<f8').tobytes()).hexdigest()} for a,m in markets.items()}}
 for row in batch:
  spec=json.loads((ROOT/row['spec']).read_text());scenes={};
  for mult in (1,2,3):
   sleeves={a:run_sleeve(spec,markets[a],filters[a+'USDT'],mult,row['role']=='comparator') for a in ('BTC','ETH')}
   for a in ('BTC','ETH'):
    trade_rows.extend({'configuration':row['name'],'cost_multiplier':mult,**t} for t in sleeves[a]['trades'])
    decision_rows.extend({'configuration':row['name'],'cost_multiplier':mult,**t} for t in sleeves[a]['decisions'])
   daily=[sleeves['BTC']['daily_nav_usdt'][i]+sleeves['ETH']['daily_nav_usdt'][i] for i in range(len(sleeves['BTC']['daily_nav_usdt']))]
   total_nav=float(dec(sleeves['BTC']['terminal_nav_usdt'])+dec(sleeves['ETH']['terminal_nav_usdt']))
   e= np.asarray(sleeves['BTC']['daily_nav_usdt'])+np.asarray(sleeves['ETH']['daily_nav_usdt'])
   daily_returns=np.diff(np.asarray(daily[:-1],dtype=np.float64))/np.asarray(daily[:-1],dtype=np.float64)[:-1]
   daily_sd=float(np.std(daily_returns,ddof=1)) if len(daily_returns)>1 else 0.0
   portfolio_daily_sharpe=float(np.mean(daily_returns)/daily_sd*math.sqrt(365)) if daily_sd else None
   portfolio_cagr=(total_nav/2000.0)**(365.0/360.0)-1
   costs=sum((dec(sleeves[a]['cost_usdt']) for a in ('BTC','ETH')),D(0));gross=sum((dec(sleeves[a]['gross_reference_pnl_usdt']) for a in ('BTC','ETH')),D(0))
   folds=[{'fold':i+1,'start_utc':sleeves['BTC']['folds'][i]['start_utc'],'end_exclusive_utc':sleeves['BTC']['folds'][i]['end_exclusive_utc'],'start_nav_usdt':daily[i*30],'end_nav_usdt':daily[(i+1)*30],'net_return_pct':(daily[(i+1)*30]/daily[i*30]-1)*100} for i in range(12)]
   # Exact synchronized minute risk path with immediate reference marks at all rebalance fills.
   start=368*1440+1;end=728*1440+1;portfolio_minute=sleeves['BTC']['_minute_nav']+sleeves['ETH']['_minute_nav']
   event_maps={}
   for a in ('BTC','ETH'):
    em={}
    for t in sleeves[a]['trades']:
     if t['status']=='filled':em[int(t['minute_index'])]=t
    event_maps[a]=em
   times=sorted(set(event_maps['BTC'])|set(event_maps['ETH']));state_times={a:sorted(event_maps[a]) for a in ('BTC','ETH')};state_trades={a:[event_maps[a][t] for t in state_times[a]] for a in ('BTC','ETH')}
   from bisect import bisect_right
   marks=[]
   for minute in times:
    wealth=0.0
    for a in ('BTC','ETH'):
     j=bisect_right(state_times[a],minute)-1
     ca,ua=(1000.0,0.0) if j<0 else (float(dec(state_trades[a][j]['cash_after'])),float(dec(state_trades[a][j]['units_after'])))
     t=event_maps[a].get(minute);px=float(dec(t['reference'])) if t else float(markets[a]['open'][minute]);wealth+=ca+ua*px
    marks.append((minute-start,wealth))
   samples=[2000.0];cursor=0
   for pos,value in marks:
    if pos>=cursor:samples.extend(portfolio_minute[cursor:pos].tolist())
    samples.append(value);samples.append(float(portfolio_minute[pos]));cursor=max(cursor,pos+1)
   samples.extend(portfolio_minute[cursor:].tolist());portfolio_dd=drawdown(samples)[0]
   costparts={k:str(sum((dec(sleeves[a]['cost_parts_usdt'][k]) for a in ('BTC','ETH')),D(0))) for k in ('fee','half_spread','slippage','impact','tick_rounding')}
   scene={'terminal_nav_usdt':str(total_nav),'net_pnl_usdt':str(dec(total_nav)-D(2000)),'net_return_pct':(total_nav/2000-1)*100,'cost_usdt':str(costs),'cost_parts_usdt':costparts,'gross_reference_pnl_usdt':str(gross),'gross_to_cost':float(gross/costs) if costs else None,'fills':sum(sleeves[a]['fills'] for a in ('BTC','ETH')),'rebalances':sum(sleeves[a]['rebalances'] for a in ('BTC','ETH')),'rejected_orders':sum(sleeves[a]['rejected_orders'] for a in ('BTC','ETH')),'skipped_below_lot':sum(sleeves[a]['skipped_below_lot'] for a in ('BTC','ETH')),'round_trips':sum(sleeves[a]['round_trips'] for a in ('BTC','ETH')),'terminal_units_by_asset':{a:sleeves[a]['terminal_units'] for a in ('BTC','ETH')},'daily_nav_usdt':daily,'daily_sample_drawdown_pct':drawdown(daily)[0],'max_drawdown_1m_sampled_pct':portfolio_dd,'minute_nav_sha256':hashlib.sha256(np.asarray(samples,dtype='<f8').tobytes()).hexdigest(),'minute_nav_samples':len(samples),'drawdown_scope':'Synchronized portfolio OOS 1-minute closes plus immediate post-fill reference marks; no intra-minute extrema.','daily_sharpe_annualized':portfolio_daily_sharpe,'cagr_pct':portfolio_cagr*100,'calmar_daily':portfolio_cagr/(drawdown(daily)[0]/100) if drawdown(daily)[0] else None,'folds':folds,'asset_sleeves':{a:{k:v for k,v in sleeves[a].items() if k not in ('daily_nav_usdt','folds','trades','decisions','_minute_nav')} for a in ('BTC','ETH')}}
   scenes[str(mult)]=scene
   for dayi,nav in enumerate(daily):daily_rows.append({'configuration':row['name'],'cost_multiplier':mult,'day_index':dayi,'nav_usdt':nav})
  cfgs[row['name']]={'spec_path':row['spec'],'fingerprint':registry.fingerprint(spec),'role':row['role'],'cost_scenarios':scenes}
  print(f"{row['name']}: {scenes['1']['net_return_pct']:.4f}% / {scenes['3']['net_return_pct']:.4f}%",flush=True)
 candidates=[r for r in batch if r['role']=='candidate']
 for row in candidates:
  c=cfgs[row['name']];p=json.loads((ROOT/row['spec']).read_text())['parameters'];neighbors=[]
  for o in candidates:
   q=json.loads((ROOT/o['spec']).read_text())['parameters']
   if abs([20,60,120].index(q['realized_vol_lookback_days'])-[20,60,120].index(p['realized_vol_lookback_days']))<=1 and abs([0.20,0.30,0.40].index(q['target_annual_volatility'])-[0.20,0.30,0.40].index(p['target_annual_volatility']))<=1:neighbors.append(o)
  frac=sum(cfgs[o['name']]['cost_scenarios']['3']['net_return_pct']>0 for o in neighbors)/len(neighbors)
  s1,s2,s3=(c['cost_scenarios'][str(i)] for i in (1,2,3));positive=sum(x['net_return_pct']>0 for x in s1['folds'])
  gates={'all_cost_scenes_positive':all(c['cost_scenarios'][str(i)]['net_return_pct']>0 for i in (1,2,3)),'positive_1x_folds':positive,'positive_1x_folds_at_least_8':positive>=8,'3x_sampled_drawdown_pct':s3['max_drawdown_1m_sampled_pct'],'3x_drawdown_at_most_25pct':s3['max_drawdown_1m_sampled_pct']<=25,'local_3x_neighbor_positive_fraction':frac,'local_3x_neighbors_at_least_60pct':frac>=0.6,'neighbor_count':len(neighbors),'1x_rebalances':s1['rebalances'],'at_least_4_rebalances':s1['rebalances']>=4,'1x_gross_to_cost':s1['gross_to_cost'],'gross_to_cost_at_least_2_5':s1['gross_to_cost'] is not None and s1['gross_to_cost']>=2.5,'zero_rejected_orders':all(c['cost_scenarios'][str(i)]['rejected_orders']==0 for i in (1,2,3)),'terminal_flat':all(dec(v)==0 for mult in ('1','2','3') for v in c['cost_scenarios'][mult]['terminal_units_by_asset'].values())}
  gates['pass']=all(gates[k] for k in ('all_cost_scenes_positive','positive_1x_folds_at_least_8','3x_drawdown_at_most_25pct','local_3x_neighbors_at_least_60pct','at_least_4_rebalances','gross_to_cost_at_least_2_5','zero_rejected_orders','terminal_flat'))
  c['sensitivity']={'local_3x_neighbor_positive_fraction':frac,'neighbor_count':len(neighbors),'neighbors':[o['name'] for o in neighbors]};c['gates']=gates;c['status']='passed' if gates['pass'] else 'rejected'
 prior=json.loads((ROOT/'research/experiments/20261013T224056Z/report.json').read_text())
 report={'round':ROUND.name,'plan_sha256':sha(ROUND/'plan.json'),'evaluation_started_utc':datetime.now(timezone.utc).isoformat(),'plan':plan,'data_manifest':data,'comparison_reference':{'source_report':'research/experiments/20261013T224056Z/report.json','configuration':'hold_360d_BTC_ETH_50_50_monthly_volmanaged','cost_scenarios':prior['configs']['hold_360d_BTC_ETH_50_50_monthly_volmanaged']['cost_scenarios'],'status':'read_only_previously_finished_exact_same_window_50_50_hold_comparator'},'summary':{'candidate_count':9,'comparator_count':0,'passed':sum(cfgs[r['name']]['status']=='passed' for r in candidates),'rejected':sum(cfgs[r['name']]['status']=='rejected' for r in candidates),'oos_days':360,'folds':12,'decision_minutes':518400,'ranked_by_1x_net_return':[r['name'] for r in sorted(candidates,key=lambda r:cfgs[r['name']]['cost_scenarios']['1']['net_return_pct'],reverse=True)]},'configs':cfgs}
 (ROUND/'report.json').write_text(json.dumps(clean(report),indent=2,ensure_ascii=False)+'\n')
 for filename,rows in (('trades.csv',trade_rows),('decisions.csv',decision_rows),('daily_equity.csv',daily_rows)):
  keys=sorted({k for row in rows for k in row})
  with (ROUND/filename).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=keys,lineterminator='\n');w.writeheader();w.writerows(rows)
 print(json.dumps(report['summary'],ensure_ascii=False),flush=True)
if __name__=='__main__':main()
