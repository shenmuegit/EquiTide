#!/usr/bin/env python3
"""Run the reserved capital/holding-window grid for the quarter-hour event."""
from __future__ import annotations
import csv,gzip,hashlib,importlib.util,json,math,statistics,sys
from datetime import datetime,timezone
from decimal import Decimal as D
from pathlib import Path
import numpy as np
import polars as pl
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent;MIN=60_000_000_000;DAY=1440*MIN
sys.path.insert(0,str(ROOT/'research/automation'));import registry
def module(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
engine=module('turn15_cost_engine',ROOT/'research/experiments/20261001T013355Z/evaluate.py')
kernel=module('turn15_decimal_kernel',ROOT/'research/experiments/20261001T133655Z/kernel.py')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def stamp(ns):return datetime.fromtimestamp(ns/1e9,timezone.utc).isoformat().replace('+00:00','Z')
def load_asset(asset):
 paths=[ROOT/f'data/normalized/binance/{asset}/binance_{asset}_20240916T000000Z_20250916T000000Z_transfer_20261001/spot_bars.parquet',ROOT/f'data/normalized/binance/{asset}/binance_{asset}_20250916T000000Z_20260916T000000Z_archive_20260929/spot_bars.parquet']
 fs=[];manifest=[]
 for p in paths:
  f=pl.read_parquet(p,columns=['open_ts','available_ts','open','close','base_volume','quote_volume','is_closed'])
  assert f.height==365*1440 and f['is_closed'].all() and f['open_ts'].is_sorted() and (f['open_ts'].diff().drop_nulls()==MIN).all() and (f['available_ts']-f['open_ts']==MIN).all()
  manifest.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size,'bars':f.height});fs.append(f)
 f=pl.concat(fs,how='vertical_relaxed').sort('open_ts');assert f.height==730*1440 and (f['open_ts'].diff().drop_nulls()==MIN).all()
 op=f['open'].cast(pl.Float64).to_numpy();cl=f['close'].cast(pl.Float64).to_numpy();bv=f['base_volume'].cast(pl.Float64).to_numpy();qv=f['quote_volume'].cast(pl.Float64).to_numpy();ts=f['open_ts'].to_numpy()
 days=[]
 for d in range(730):
  lo=d*1440;hi=lo+1440
  days.append({'date':datetime.fromtimestamp(int(ts[lo])/1e9,timezone.utc).date().isoformat(),'close':float(cl[hi-1]),'quote_volume':float(sum(qv[lo:hi]))})
 return {'asset':asset,'open':op,'close':cl,'base':bv,'quote':qv,'ts':ts,'daily':days,'source_files':manifest,'daily_close_sha256_f64le':hashlib.sha256(np.asarray([x['close'] for x in days],dtype='<f8').tobytes()).hexdigest()}
def nav_stats(vals):
 assert len(vals)>1 and all(math.isfinite(x) and x>0 for x in vals),(min(vals),max(vals))
 peak=vals[0];dd=0
 for x in vals:peak=max(peak,x);dd=max(dd,(peak-x)/peak)
 rs=[b/a-1 for a,b in zip(vals,vals[1:])];sd=statistics.stdev(rs) if len(rs)>1 else 0
 cagr=(vals[-1]/vals[0])**(365/len(rs))-1
 return {'net_return_pct':100*(vals[-1]/vals[0]-1),'max_drawdown_pct':100*dd,'sharpe_annualized_daily':statistics.mean(rs)/sd*math.sqrt(365) if sd else None,'cagr_pct':100*cagr,'calmar':cagr/dd if dd else None,'daily_marks':len(vals)-1}
def run(spec,market,filters,mult,hold=False):
 p=spec['parameters'];asset=market['asset'];daily=market['daily'];start_day=next(i for i,x in enumerate(daily) if x['date']=='2025-09-19');end_day=next(i for i,x in enumerate(daily) if x['date']=='2026-09-14');assert end_day-start_day==360
 cap=D(str(p['initial_capital_usdt']));cash=cap;units=D(0);hold_min=int(p.get('hold_minutes',1));phase=int(p.get('phase_offset_minutes',0));events=0;entries=0;exits=0;fills=0;rejected=0;cash_mismatch=0;cost_parts={k:D(0) for k in ('fee','half_spread','slippage','impact','tick_rounding')};nav=[float(cap)];daily_nav=[float(cap)];flow=hashlib.sha256();trips=0;missed=0;capacity_rejects=0;pending_exit=False;next_free=-1
 def execute(mi,buy,terminal=False,scheduled_i=None):
  nonlocal cash,units,fills,rejected,capacity_rejects
  ref=D(str(market['open'][mi]));day=mi//1440;adv,sigma=engine.lagged_cost_inputs(daily,day);base=sum((D(str(v)) for v in market['base'][mi-5:mi]),D(0));quote=sum((D(str(v)) for v in market['quote'][mi-5:mi]),D(0));vwap=quote/base if base else D(0)
  beforec,beforeu=cash,units;cash,units,t=kernel.fill(cash,units,buy,ref,D(str(adv)),D(str(sigma)),mult,filters,vwap)
  t.update({'minute_index':mi,'execution_utc':stamp(int(market['ts'][mi])),'scheduled_start_utc':stamp(int(market['ts'][scheduled_i])) if scheduled_i is not None else None,'terminal':terminal,'cash_before':str(beforec),'units_before':str(beforeu),'cash_after':str(cash),'units_after':str(units)})
  flow.update(json.dumps(t,sort_keys=True,separators=(',',':')).encode()+b'\n')
  if t['status']=='filled':
   fills+=1
   for k,v in t['cost_parts'].items():cost_parts[k]+=D(v)
  else:
   rejected+=1
   if t.get('reason')=='participation':capacity_rejects+=1
  nav.append(float(cash+units*ref))
  return t
 # Precompute rolling lagged costs once per date; event fills use only that day's completed prior-20 window.
 for day in range(start_day,end_day):
  daystart=day*1440
  for quarter in range(0,1440,15):
   if hold and (day!=start_day or quarter!=0):continue
   i=daystart+quarter+phase
   if i<next_free:missed+=1;continue
   events+=1
   if units>0:
    # A rejected scheduled liquidation is retried at the first later one-minute open; no new signal is inserted.
    t=execute(i,False,False,i);exits+=1
    if t['status']=='filled':units=D(0);pending_exit=False;next_free=i+1;missed+=1;continue
    else:pending_exit=True;next_free=i+1;missed+=1;continue
   if hold:
    entries+=1;t=execute(i,True,False,i)
    continue
   entries+=1;t=execute(i,True,False,i)
   if t['status']!='filled':continue
   exit_i=i+hold_min;exits+=1;et=execute(exit_i,False,False,i)
   if et['status']=='filled':units=D(0);trips+=1;next_free=exit_i+1
   else:
    pending_exit=True;next_free=exit_i+1
    retry=exit_i+1
    while retry<min(i+15,end_day*1440) and units>0:
     rt=execute(retry,False,False,i);exits+=1
     if rt['status']=='filled':units=D(0);trips+=1;pending_exit=False;next_free=retry+1;break
     retry+=1
  dayclose=day*1440+1439
  close_nav=float(cash+units*D(str(market['close'][dayclose])))
  nav.append(close_nav);daily_nav.append(close_nav)
 # The scheduled terminal boundary is OOS end-exclusive UTC 2026-09-14 00:00.
 end_i=end_day*1440
 if units>0:
  t=execute(end_i,False,True,end_i);exits+=1
  if t['status']=='filled':units=D(0);trips+=1
 terminal_nav=float(cash+units*D(str(market['open'][end_i])));daily_nav[-1]=terminal_nav;nav.append(terminal_nav)
 assert len(daily_nav)==361,(asset,len(daily_nav))
 ds=nav_stats(daily_nav);peak=nav[0];event_dd=0
 for x in nav:peak=max(peak,x);event_dd=max(event_dd,(peak-x)/peak)
 folds=[]
 for f in range(12):
  a=f*30;b=(f+1)*30;folds.append({'fold':f+1,'start_utc':daily[start_day+a]['date'],'end_utc_inclusive':daily[start_day+b-1]['date'],'net_return_pct':100*(daily_nav[b]/daily_nav[a]-1)})
 totalcost=sum(cost_parts.values(),D(0));pnl=D(str(terminal_nav))-cap;gross=pnl+totalcost
 summary={**ds,'event_sample_max_drawdown_pct':100*event_dd,'terminal_nav_usdt':str(terminal_nav),'terminal_cash_usdt':str(cash),'terminal_units':str(units),'terminal_flat':units==0,'net_pnl_usdt':str(pnl),'cost_usdt':str(totalcost),'cost_parts_usdt':{k:str(v) for k,v in cost_parts.items()},'gross_reference_pnl_usdt':str(gross),'gross_reference_pnl_to_cost':float(gross/totalcost) if totalcost else None,'scheduled_event_windows':events,'entry_attempts':entries,'exit_attempts':exits,'filled_orders':fills,'round_trips':trips,'rejected_orders':rejected,'capacity_rejections':capacity_rejects,'missed_calendar_events':missed,'positive_1x_folds':sum(x['net_return_pct']>0 for x in folds),'folds':folds,'cost_multiplier':mult,'event_ledger_sha256':flow.hexdigest(),'daily_nav_sha256_f64le':hashlib.sha256(np.asarray(daily_nav,dtype='<f8').tobytes()).hexdigest(),'drawdown_scope':'UTC daily closes plus immediate post-fill reference marks; no within-minute extrema'}
 return {'summary':summary,'daily_nav':daily_nav,'event_ledger_sha256':flow.hexdigest()}
def main():
 plan=json.loads((ROUND/'plan.json').read_text());res=json.loads((ROUND/'reserve.json').read_text());assert all(x['exit_code']==0 for x in res)
 base=json.loads((ROOT/'research/experiments/20261012T035429Z/report.json').read_text());filters=base['plan']['execution']['filters'];markets={a:load_asset(a) for a in ('BTC','ETH')};run_dir=ROOT/'data/runs'/ROUND.name;run_dir.mkdir(parents=True,exist_ok=True)
 manifest={'source_files':{a:markets[a]['source_files'] for a in markets},'daily_close_sha256_f64le':{a:markets[a]['daily_close_sha256_f64le'] for a in markets},'filter_source_sha256':sha(ROOT/'research/experiments/20261012T035429Z/report.json'),'oos_days':360,'folds':12}
 configs={};benchmarks={}
 for row in res:
  spec=json.loads((ROOT/row['spec']).read_text());asset=spec['universe'][0].split('/')[0];name=spec['name'];sc={}
  for mult in (1,2,3):
   out=run(spec,markets[asset],filters[asset+'USDT'],mult,name.startswith('buy_hold_'));sc[str(mult)]=out['summary']
   with (run_dir/f'{name}_cost{mult}.json.gz').open('wb') as f:
    with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as g:g.write(json.dumps(out,sort_keys=True,separators=(',',':')).encode())
  if name.startswith('buy_hold_'):benchmarks[name]={'fingerprint':row['output'],'asset':asset,'scenarios':sc}
  else:configs[name]={'fingerprint':row['output'],'spec':row['spec'],'asset':asset,'phase':spec['parameters']['phase_offset_minutes'],'capital':spec['parameters']['initial_capital_usdt'],'hold':spec['parameters']['hold_minutes'],'scenarios':sc}
  print(name,*[round(sc[str(m)]['net_return_pct'],4) for m in (1,2,3)],flush=True)
 # Phase zero must beat both same-asset/capital/hold placebo offsets after 1x costs.
 for c in configs.values():
  n=[]
  for o in configs.values():
   if o['asset']==c['asset'] and o['capital']==c['capital'] and abs(o['phase']-c['phase'])<=1 and abs(o['hold']-c['hold'])<=1:n.append(o)
  c['neighborhood_size']=len(n);c['neighbor_3x_positive_fraction']=sum(x['scenarios']['3']['net_return_pct']>0 for x in n)/len(n)
  gates={'all_costs_positive':all(c['scenarios'][str(m)]['net_return_pct']>0 for m in (1,2,3)),'positive_1x_folds_at_least_8':c['scenarios']['1']['positive_1x_folds']>=8,'3x_drawdown_at_most_25pct':c['scenarios']['3']['event_sample_max_drawdown_pct']<=25,'neighbor_3x_positive_fraction_at_least_0_60':c['neighbor_3x_positive_fraction']>=.6,'at_least_100_round_trips':c['scenarios']['1']['round_trips']>=100,'gross_pnl_to_cost_at_least_2_5':c['scenarios']['1']['gross_reference_pnl_to_cost'] is not None and c['scenarios']['1']['gross_reference_pnl_to_cost']>=2.5,'no_rejections_or_capacity_violations':all(c['scenarios'][str(m)]['rejected_orders']==0 and c['scenarios'][str(m)]['capacity_rejections']==0 for m in (1,2,3)),'terminal_flat':all(c['scenarios'][str(m)]['terminal_flat'] for m in (1,2,3))}
  c['gates']=gates;c['status']='rejected' if c['phase']!=0 else 'pending_phase_gate'
 # Mean 1x net for phase 0 must beat each phase control, separately per asset/capital/duration.
 phase_stats={}
 for asset in ('BTC','ETH'):
  for cap in (5000,10000):
   for hold in (1,2,3):
    vals={p:configs[f'turn15_{asset.lower()}_cap{cap}_phase{p}_hold{hold}m']['scenarios']['1']['net_return_pct'] for p in (0,1,2)}
    phase_stats[f'{asset}_{cap}_{hold}m']=vals;key=f'turn15_{asset.lower()}_cap{cap}_phase0_hold{hold}m';c=configs[key];c['phase_comparison_1x']=vals;c['gates']['phase0_exceeds_both_placebos']=vals[0]>vals[1] and vals[0]>vals[2];c['status']='passed' if all(c['gates'].values()) else 'rejected'
 rankings=sorted(configs,key=lambda n:configs[n]['scenarios']['1']['net_return_pct'],reverse=True)
 report={'round':ROUND.name,'evaluation_started_utc':datetime.now(timezone.utc).isoformat(),'plan':plan,'data_manifest':manifest,'summary':{'candidate_configs':12,'placebo_controls':24,'benchmarks':4,'candidate_passed':sum(configs[k]['status']=='passed' for k in configs if configs[k]['phase']==0),'candidate_rejected':sum(configs[k]['status']=='rejected' for k in configs if configs[k]['phase']==0),'placebo_rejected':24,'cost_scenes':len(res)*3,'oos_days':360,'folds':12,'ranking_1x':rankings,'phase_specificity_by_asset_capital_hold':phase_stats},'configs':configs,'benchmarks':benchmarks,'conflicting_preexisting_reservations':{'round':'20261012T232807Z','all_20_reserves_returned_exit3':True,'no_calculation_performed':True,'current_active_or_pending_rows_preserved':True},'comparison':'Cash has 0% net return; buy-and-hold references are matched by asset and capital.'}
 (ROUND/'data_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');(ROUND/'report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
 with (ROUND/'sensitivity.csv').open('w',newline='') as f:
  w=csv.writer(f,lineterminator='\n');w.writerow(['name','asset','capital','phase_offset','hold_minutes','return_1x','return_2x','return_3x','3x_dd','3x_neighbor_fraction','status'])
  for n in rankings:
   c=configs[n];w.writerow([n,c['asset'],c['capital'],c['phase'],c['hold'],*[c['scenarios'][str(m)]['net_return_pct'] for m in (1,2,3)],c['scenarios']['3']['event_sample_max_drawdown_pct'],c['neighbor_3x_positive_fraction'],c['status']])
 print(json.dumps(report['summary'],indent=2))
if __name__=='__main__':main()
