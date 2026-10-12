#!/usr/bin/env python3
"""Evaluate the reserved 15m BTC/ETH downside-shock rebound strategy grid."""
from __future__ import annotations
import gzip,hashlib,importlib.util,json,math,statistics,sys
from datetime import datetime,timezone
from decimal import Decimal as D
from pathlib import Path
import numpy as np,polars as pl
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
MIN=60_000_000_000;DAY=1440*MIN
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sys.path.insert(0,str(ROOT/'research/experiments/20261001T133655Z'))
from kernel import fill

def loadmod(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
engine=loadmod('r54_lagged_daily_cost_engine',ROOT/'research/experiments/20261001T013355Z/evaluate.py')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def stamp(ns):return datetime.fromtimestamp(ns/1e9,timezone.utc).isoformat().replace('+00:00','Z')
def canonical(x):return json.loads(json.dumps(x,default=str,ensure_ascii=False,allow_nan=False))
def gzwrite(p,x):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('wb') as f:
  with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as g:g.write(json.dumps(canonical(x),sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())

def load_asset(asset):
 paths=[ROOT/f'data/normalized/binance/{asset}/binance_{asset}_20240916T000000Z_20250916T000000Z_transfer_20261001/spot_bars.parquet',ROOT/f'data/normalized/binance/{asset}/binance_{asset}_20250916T000000Z_20260916T000000Z_archive_20260929/spot_bars.parquet']
 parts=[];info=[]
 for p in paths:
  f=pl.read_parquet(p,columns=['open_ts','available_ts','open','close','base_volume','quote_volume','is_closed'])
  assert f.height==365*1440 and f['is_closed'].all() and f['open_ts'].is_sorted()
  assert (f['open_ts'].diff().drop_nulls()==MIN).all() and (f['available_ts']-f['open_ts']==MIN).all()
  assert (f['open']>0).all() and (f['close']>0).all() and (f['quote_volume']>=0).all() and (f['base_volume']>=0).all()
  info.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size,'bars':f.height,'first_open_ns':int(f['open_ts'][0]),'last_open_ns':int(f['open_ts'][-1])});parts.append(f)
 m=pl.concat(parts,how='vertical_relaxed').sort('open_ts');assert m.height==730*1440 and (m['open_ts'].diff().drop_nulls()==MIN).all()
 op=m['open'].to_list();cl=m['close'].to_list();qv=m['quote_volume'].to_list();bv=m['base_volume'].to_list();ts=m['open_ts'].to_numpy();cf=m['close'].cast(pl.Float64).to_numpy()
 nbar=730*96;bars=[]
 for j in range(nbar):
  start=j*15;close_i=start+14;avail=int(ts[close_i])+MIN
  bars.append({'open_ts':int(ts[start]),'available_ts':avail,'close':D(str(cl[close_i])),'quote_volume':sum((D(str(x)) for x in qv[start:start+15]),D(0))})
 assert len(bars)==70080 and stamp(bars[0]['open_ts'])=='2024-09-16T00:00:00Z' and stamp(bars[-1]['available_ts'])=='2026-09-16T00:00:00Z'
 daily=[];proxy=[]
 for d in range(730):
  lo=d*1440;hi=(d+1)*1440;trade_i=lo+1;close_i=hi-1;open_ns=int(ts[lo]);avail=int(ts[close_i])+MIN;trade_ts=int(ts[trade_i])
  assert avail==open_ns+DAY and trade_ts==open_ns+MIN
  daily.append({'date':stamp(open_ns).split('T')[0],'day_open_ns':open_ns,'close':D(str(cl[close_i])),'close_available_ts':avail,'quote_volume':sum((D(str(x)) for x in qv[lo:hi]),D(0)),'trade_ts':trade_ts,'trade_open':D(str(op[trade_i]))})
  pq=sum((D(str(x)) for x in qv[trade_i-5:trade_i]),D(0));pb=sum((D(str(x)) for x in bv[trade_i-5:trade_i]),D(0));proxy.append(pq/pb if pb else D(0))
 return {'asset':asset,'bars':bars,'daily':daily,'proxy':proxy,'minute_open':op,'minute_close':cf,'minute_quote':qv,'minute_base':bv,'minute_ts':ts,'files':info,'daily_close_sha256_f64le':hashlib.sha256(np.asarray([float(x['close']) for x in daily],dtype='<f8').tobytes()).hexdigest(),'15m_close_sha256_f64le':hashlib.sha256(np.asarray([float(x['close']) for x in bars],dtype='<f8').tobytes()).hexdigest()}

def drawdown(x):
 a=np.asarray(x,dtype=np.float64);p=np.maximum.accumulate(a);d=1-a/p;j=int(np.argmax(d));return float(d[j]*100),int(np.argmax(a[:j+1])),j
def metrics(x,ppy):
 a=np.asarray(x,dtype=np.float64);assert len(a)>1 and np.isfinite(a).all() and (a>0).all();ret=a[1:]/a[:-1]-1;sd=float(np.std(ret,ddof=1)) if len(ret)>1 else 0.;dd,pi,ti=drawdown(a);cagr=(float(a[-1])/float(a[0]))**(ppy/(len(a)-1))-1
 return {'net_return_pct':float((a[-1]/a[0]-1)*100),'max_drawdown_pct':dd,'sharpe_annualized':float(np.mean(ret)/sd*math.sqrt(ppy)) if sd else None,'cagr_pct':cagr*100,'calmar':cagr/(dd/100) if dd else None,'drawdown_peak_index':pi,'drawdown_trough_index':ti,'observations':len(a)-1}

def run(spec,market,filters,mult,hold_ref=False):
 p=spec['parameters'];start=int(p['oos_start_15m_index']);end=int(p['oos_end_exclusive_15m_index']);cap=D('2000');cash=cap;units=D(0);held=False;entry_ref=None;entry_exec_bar=None;trades=[];decisions=[];events=[]
 assert start==35328 and end==69888
 def execute(buy,i,terminal=False,signal_i=None):
  nonlocal cash,units
  day=i//96;trade_m=i*15+1;ref=D(str(market['minute_open'][trade_m]));avg=market['proxy'][day];adv,sigma=engine.lagged_cost_inputs(market['daily'],day);cb,ub=cash,units
  cash,units,t=fill(cash,units,buy,ref,D(str(adv)),D(str(sigma)),mult,filters,avg)
  t.update({'asset':market['asset'],'bar_index':i,'signal_bar_index':signal_i,'signal_available_utc':stamp(market['bars'][signal_i]['available_ts']) if signal_i is not None else None,'execution_utc':stamp(int(market['minute_ts'][trade_m])),'signal_to_execution_seconds':(int(market['minute_ts'][trade_m])-market['bars'][signal_i]['available_ts'])/1e9 if signal_i is not None else None,'terminal':terminal,'cash_before':str(cb),'units_before':str(ub),'cash_after':str(cash),'units_after':str(units)})
  trades.append(t);return t
 for i in range(start,end):
  if hold_ref:
   action='buy' if i==start else None;signal_j=None
  else:
   j=i-1;ret=market['bars'][j]['close']/market['bars'][j-1]['close']-D(1);threshold=D(str(p['entry_15m_drop_fraction']))
   if not held:action='buy' if ret<=-threshold else None
   else:
    elapsed=i-entry_exec_bar
    action='sell' if market['bars'][j]['close']>=entry_ref or elapsed>=int(p['max_holding_15m_bars']) else None
   signal_j=j
   decisions.append({'decision_index':i,'signal_bar_index':j,'signal_available_utc':stamp(market['bars'][j]['available_ts']),'execution_utc':stamp(market['bars'][i]['open_ts']+MIN),'last_15m_return':str(ret),'entry_drop_threshold':str(threshold),'held_before':held,'bars_held_before':None if entry_exec_bar is None else i-entry_exec_bar,'recovery_reference':None if entry_ref is None else str(entry_ref),'action':action})
  if action:
   t=execute(action=='buy',i,False,signal_j)
   mi=i*15+1
   if action=='buy' and t['status']=='filled':held=True;entry_ref=D(str(market['bars'][i-1]['close']));entry_exec_bar=i
   elif action=='sell' and t['status']=='filled':held=False;entry_ref=None;entry_exec_bar=None
   events.append((mi,t,held,cash,units))
 if held:
  t=execute(False,end,True,end-1)
  if t['status']=='filled':held=False;entry_ref=None;entry_exec_bar=None
  events.append((end*15+1,t,held,cash,units))
 terminal_ref=D(str(market['minute_open'][end*15+1]));terminal_nav=cash+(units*terminal_ref if held else D(0))
 sm=start*15+1;tm=end*15+1;nav=[float(cap)];ci={};ei=0;mc=cap;mu=D(0);mh=False
 for mi in range(sm,tm):
  while ei<len(events) and events[ei][0]==mi:
   _,t,mh,mc,mu=events[ei];ref=D(t['reference']);nav.append(float(mc+(mu*ref if mh else D(0))));ei+=1
  if mh:nav.append(float(mc+mu*D(str(market['minute_close'][mi]))))
  else:nav.append(float(mc))
  ci[mi]=len(nav)-1
 nav.append(float(terminal_nav));daily_nav=[float(cap)]
 for d in range(1,361):daily_nav.append(nav[ci[sm+d*1440-1]])
 daily_nav[-1]=float(terminal_nav);dm=metrics(daily_nav,365);mdd,pi,ti=drawdown(nav);folds=[]
 for f in range(12):
  a=f*30;b=a+30;fold=metrics(daily_nav[a:b+1],365)
  folds.append({'fold':f+1,'start_utc':market['daily'][start//96+a]['date'],'end_exclusive_utc':market['daily'][start//96+b]['date'],**fold})
 fills=[t for t in trades if t['status']=='filled'];parts={k:str(sum((D(t['cost_parts'][k]) for t in fills),D(0))) for k in ('fee','half_spread','slippage','impact','tick_rounding')};cost=sum((D(v) for v in parts.values()),D(0));gross=terminal_nav-cap+cost
 summary={'net_return_pct':dm['net_return_pct'],'net_pnl_usdt':str(terminal_nav-cap),'terminal_nav_usdt':str(terminal_nav),'terminal_cash_usdt':str(cash),'terminal_units':str(units),'terminal_held':held,'cost_usdt':str(cost),'cost_parts_usdt':parts,'gross_reference_pnl_usdt':str(gross),'gross_reference_pnl_to_cost':float(gross/cost) if cost else None,'max_drawdown_pct':mdd,'daily_mark_drawdown_pct':dm['max_drawdown_pct'],'drawdown_scope':'All OOS one-minute close samples plus immediate post-fill reference marks; no within-minute extrema.','sharpe_annualized_daily':dm['sharpe_annualized'],'cagr_pct':dm['cagr_pct'],'calmar':dm['calmar'],'attempts':len(trades),'executions':len(fills),'round_trips':sum(t['side']=='sell' for t in fills),'positive_1x_folds':sum(x['net_return_pct']>0 for x in folds),'rejected_orders':sum(t['status']!='filled' for t in trades),'balance_violations':sum(D(t['cash_after'])<0 or D(t['units_after'])<0 for t in trades),'folds':folds,'minute_nav_sha256_f64le':hashlib.sha256(np.asarray(nav,dtype='<f8').tobytes()).hexdigest(),'minute_nav_samples':len(nav),'cost_multiplier':mult}
 return {'name':spec['name'],'fingerprint':registry.fingerprint(spec),'spec':spec,'decisions':decisions,'trades':trades,'daily_nav_usdt':daily_nav,'summary':summary}

def main():
 plan=json.loads((ROUND/'spec.json').read_text());batch=json.loads((ROUND/'batch.json').read_text());src=json.loads((ROOT/'research/experiments/20261012T035429Z/report.json').read_text());filters=src['plan']['execution']['filters'];markets={a:load_asset(a) for a in ('BTC','ETH')}
 manifest={'assets':{a:{'source_files':markets[a]['files'],'daily_count':len(markets[a]['daily']),'15m_bars':len(markets[a]['bars']),'daily_close_sha256_f64le':markets[a]['daily_close_sha256_f64le'],'15m_close_sha256_f64le':markets[a]['15m_close_sha256_f64le']} for a in markets},'filter_source_sha256':sha(ROOT/'research/experiments/20261012T035429Z/report.json')};(ROUND/'data_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 cfg={};rows=[];out=ROOT/'data/runs'/ROUND.name;out.mkdir(parents=True,exist_ok=True)
 for b in batch:
  spec=json.loads((ROOT/b['spec']).read_text());a=b.get('asset') or spec['universe'][0].split('/')[0];cfg[b['name']]={'fingerprint':b['fingerprint'],'spec':b['spec'],'is_comparator':b['is_comparator'],'scenarios':{}}
  for mult in (1,2,3):
   arc=run(spec,markets[a],filters[a+'USDT'],mult,b['is_comparator']);cfg[b['name']]['scenarios'][str(mult)]=arc['summary'];gzwrite(out/f"{b['name']}_cost{mult}.json.gz",arc);rows.append({'name':b['name'],'multiplier':mult,'is_comparator':b['is_comparator'],**arc['summary']})
  print(b['name'],*[round(cfg[b['name']]['scenarios'][str(m)]['net_return_pct'],4) for m in (1,2,3)],flush=True)
 for b in batch:
  if b['is_comparator']:continue
  p=json.loads((ROOT/b['spec']).read_text())['parameters'];neigh=[]
  horder={1:0,4:1,12:2};torder={0.005:0,0.01:1,0.02:2}
  for o in batch:
   if o['is_comparator'] or o['asset']!=b['asset']:continue
   q=json.loads((ROOT/o['spec']).read_text())['parameters']
   if abs(horder[q['max_holding_15m_bars']]-horder[p['max_holding_15m_bars']])<=1 and abs(torder[q['entry_15m_drop_fraction']]-torder[p['entry_15m_drop_fraction']])<=1:neigh.append(o['name'])
  c=cfg[b['name']]['scenarios'];frac=sum(cfg[n]['scenarios']['3']['net_return_pct']>0 for n in neigh)/len(neigh)
  for m in ('1','2','3'):c[m]['neighborhood_positive_fraction_3x']=frac;c[m]['neighborhood_size']=len(neigh)
  gates={'all_costs_positive':all(c[str(m)]['net_return_pct']>0 for m in (1,2,3)),'positive_1x_folds':c['1']['positive_1x_folds'],'drawdown_under_25pct':c['3']['max_drawdown_pct']<=25,'neighborhood_fraction_at_least_0_60':frac>=.6,'round_trips_at_least_2':c['1']['round_trips']>=2,'gross_to_cost_at_least_2_5':c['1']['gross_reference_pnl_to_cost'] is not None and c['1']['gross_reference_pnl_to_cost']>=2.5,'no_balance_violations':all(c[str(m)]['balance_violations']==0 for m in (1,2,3)),'terminal_flat':all(D(c[str(m)]['terminal_units'])==0 for m in (1,2,3))}
  cfg[b['name']]['gates']=gates;cfg[b['name']]['status']='passed' if all([gates['all_costs_positive'],gates['positive_1x_folds']>=7,gates['drawdown_under_25pct'],gates['neighborhood_fraction_at_least_0_60'],gates['round_trips_at_least_2'],gates['gross_to_cost_at_least_2_5'],gates['no_balance_violations'],gates['terminal_flat']]) else 'rejected'
 ranked=sorted([b['name'] for b in batch if not b['is_comparator']],key=lambda n:cfg[n]['scenarios']['1']['net_return_pct'],reverse=True)
 report={'round':ROUND.name,'evaluation_started_utc':datetime.now(timezone.utc).isoformat(),'plan':plan,'data_manifest':manifest,'summary':{'candidate_configs':18,'comparators':2,'candidate_passed':sum(cfg[n]['status']=='passed' for n in ranked),'candidate_rejected':sum(cfg[n]['status']=='rejected' for n in ranked),'oos_days':360,'folds':12,'ranking_1x':ranked,'cost_scenes':len(rows)},'configs':cfg,'cost_scene_summaries':rows};(ROUND/'report.json').write_text(json.dumps(canonical(report),indent=2,ensure_ascii=False)+'\n');print(json.dumps(report['summary']))
if __name__=='__main__':main()
