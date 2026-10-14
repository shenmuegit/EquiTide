#!/usr/bin/env python3
"""Evaluate reserved hourly BTC/ETH lead-lag follower configurations on historical OHLCV."""
from __future__ import annotations
import csv,gzip,hashlib,importlib.util,json,math,statistics,sys
from datetime import datetime,timezone
from decimal import Decimal as D
from pathlib import Path
import numpy as np,polars as pl
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
MIN=60_000_000_000;DAY=1440*MIN;MIN_MS=60_000;DAY_MS=86_400_000
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sys.path.insert(0,str(ROOT/'research/experiments/20261001T133655Z'));from kernel import fill
engine_path=ROOT/'research/experiments/20261001T013355Z/evaluate.py'
spec=importlib.util.spec_from_file_location('leadlag_cost_engine',engine_path);engine=importlib.util.module_from_spec(spec);sys.modules[spec.name]=engine;spec.loader.exec_module(engine)

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def stamp_ms(ms):return datetime.fromtimestamp(ms/1000,timezone.utc).isoformat().replace('+00:00','Z')
def canonical(x):return json.loads(json.dumps(x,default=str,ensure_ascii=False,allow_nan=False))
def gzwrite(path,obj):
 path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('wb') as raw:
  with gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0) as f:f.write(json.dumps(canonical(obj),sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())

def load_asset(asset):
 paths=[ROOT/f'data/normalized/binance/{asset}/binance_{asset}_20240916T000000Z_20250916T000000Z_transfer_20261001/spot_bars.parquet',ROOT/f'data/normalized/binance/{asset}/binance_{asset}_20250916T000000Z_20260916T000000Z_archive_20260929/spot_bars.parquet']
 frames=[];files=[]
 for p in paths:
  f=pl.read_parquet(p,columns=['open_ts','available_ts','open','close','base_volume','quote_volume','is_closed'])
  assert f.height==365*1440 and f['is_closed'].all() and f['open_ts'].is_sorted()
  assert (f['open_ts'].diff().drop_nulls()==MIN).all() and (f['available_ts']-f['open_ts']==MIN).all()
  assert (f['open']>0).all() and (f['close']>0).all() and (f['base_volume']>=0).all() and (f['quote_volume']>=0).all()
  files.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size,'bars':f.height,'first_open_ns':int(f['open_ts'][0]),'last_open_ns':int(f['open_ts'][-1])});frames.append(f)
 minute=pl.concat(frames,how='vertical_relaxed').sort('open_ts');assert minute.height==730*1440 and (minute['open_ts'].diff().drop_nulls()==MIN).all()
 daily=minute.with_columns((pl.col('open_ts')//DAY).alias('day')).group_by('day').agg(pl.col('close').last(),pl.col('quote_volume').sum().alias('quote_volume'),pl.col('available_ts').last().alias('available_ts')).sort('day')
 dclose=daily['close'].to_list();qday=daily['quote_volume'].to_list();drows=[];day_keys=daily['day'].to_list()
 for day,close,qv,available in zip(day_keys,dclose,qday,daily['available_ts'].to_list()):
  day_open_ms=int(day)*DAY_MS;drows.append({'date':stamp_ms(day_open_ms).split('T')[0],'day_open_ms':day_open_ms,'close':D(str(close)),'quote_volume':D(str(qv)),'close_available_ms':int(available)//1_000_000})
 assert len(drows)==730 and drows[0]['date']=='2024-09-16' and drows[-1]['date']=='2026-09-15'
 return {'asset':asset,'files':files,'daily':drows,'minute_open':minute['open'].to_list(),'minute_close':minute['close'].cast(pl.Float64).to_numpy(),'minute_base':minute['base_volume'].to_list(),'minute_quote':minute['quote_volume'].to_list(),'minute_ts':minute['open_ts'].to_numpy(),'daily_close_sha256_f64le':hashlib.sha256(np.asarray([float(x['close']) for x in drows],dtype='<f8').tobytes()).hexdigest()}

def maxdd(values):
 a=np.asarray(values,dtype=np.float64);peak=np.maximum.accumulate(a);dd=1-a/peak;i=int(np.argmax(dd));return float(dd[i]*100),int(np.argmax(a[:i+1])),i
def metric(nav,ppy=365):
 a=np.asarray(nav,dtype=np.float64);assert len(a)>1 and np.all(np.isfinite(a)) and np.all(a>0)
 r=a[1:]/a[:-1]-1;sd=float(np.std(r,ddof=1)) if len(r)>1 else 0.;dd,pi,ti=maxdd(a);cagr=(a[-1]/a[0])**(ppy/(len(a)-1))-1
 return {'net_return_pct':float((a[-1]/a[0]-1)*100),'max_drawdown_pct':dd,'sharpe_annualized':float(np.mean(r)/sd*math.sqrt(ppy)) if sd else None,'cagr_pct':cagr*100,'calmar':cagr/(dd/100) if dd else None,'observations':len(a)-1,'drawdown_peak_index':pi,'drawdown_trough_index':ti}

def run(spec,markets,filters,mult):
 p=spec['parameters'];leader=p['leader'];follower=p['follower'];L=int(p['leader_lookback_minutes']);H=int(p['fixed_hold_minutes']);cap=D(str(p['initial_capital_usdt']));start=p['start_day_index']*1440;end=p['end_day_index']*1440
 assert start==368*1440 and end==728*1440
 lead=markets[leader];fol=markets[follower];cash=cap;units=D(0);held=False;expiry=None;trades=[];signals=[];events=[]
 def execute(buy,exec_i,signal_available_ms,reason,signal_details=None,terminal=False):
  nonlocal cash,units
  market=markets[follower];day_i=exec_i//1440;ref=D(str(market['minute_open'][exec_i]));adv,sigma=engine.lagged_cost_inputs(market['daily'],day_i)
  qsum=sum((D(str(x)) for x in market['minute_quote'][exec_i-5:exec_i]),D(0));bsum=sum((D(str(x)) for x in market['minute_base'][exec_i-5:exec_i]),D(0));proxy=qsum/bsum if bsum>0 else ref
  before_cash,before_units=cash,units
  cash,units,t=fill(cash,units,buy,ref,D(str(adv)),D(str(sigma)),mult,filters[follower+'USDT'],proxy)
  execution_ms=int(market['minute_ts'][exec_i])//1_000_000
  t.update({'asset':follower,'reason':reason,'bar_index':exec_i,'signal_available_utc':stamp_ms(signal_available_ms),'execution_utc':stamp_ms(execution_ms),'signal_to_execution_seconds':(execution_ms-signal_available_ms)/1000,'terminal':terminal,'cash_before':str(before_cash),'units_before':str(before_units),'cash_after':str(cash),'units_after':str(units),'observed_signal':signal_details})
  trades.append(t)
  if t['status']=='filled':events.append({'minute_index':exec_i,'asset_after':follower if units>0 else None,'cash_after':cash,'units_after':units,'mark':D(t['reference'])})
  return t
 # Hourly boundary m is when the prior 1m close becomes available. Execution is m+1 open.
 for m in range(start,end,60):
  if held and expiry is not None and m>=expiry:
   t=execute(False,m+1,int(lead['minute_ts'][m])//1_000_000,'scheduled_exit')
   if t['status']=='filled':held=False;expiry=None
   continue
  if held:continue
  rlead=D(str(lead['minute_close'][m-1]))/D(str(lead['minute_close'][m-L-1]))-D(1)
  rfollow=D(str(fol['minute_close'][m-1]))/D(str(fol['minute_close'][m-L-1]))-D(1);gap=rlead-rfollow
  if not (rlead>D(str(p['leader_return_threshold'])) and gap>D(str(p['leader_minus_follower_gap_threshold']))):continue
  detail={'decision_boundary_utc':stamp_ms(int(lead['minute_ts'][m])//1_000_000),'leader':leader,'follower':follower,'leader_return':str(rlead),'follower_return':str(rfollow),'gap':str(gap),'lookback_minutes':L,'hold_minutes':H};signals.append(detail)
  if m+H>end:detail['action']='skip_expiry_beyond_terminal';continue
  t=execute(True,m+1,int(lead['minute_ts'][m])//1_000_000,'btc_eth_leadlag_follower_entry',detail)
  if t['status']=='filled':held=True;expiry=m+H
 # Terminal liquidation at common next-day 00:01 open.
 terminal_i=end+1;terminal_ref=D(str(fol['minute_open'][terminal_i]))
 if held and units>0:execute(False,terminal_i,int(fol['minute_ts'][end])//1_000_000,'terminal',None,True)
 terminal_nav=cash+units*terminal_ref
 # Construct one-minute close NAV plus immediate post-fill reference marks for sampled drawdown.
 mark_end=end;first_mark=start+1;nav=np.full(mark_end-first_mark,float(cap));cursor=first_mark;cc=cap;uu=D(0);asset=None;event_marks=[]
 for event in events:
  i=event['minute_index']
  if i<first_mark or i>=mark_end:continue
  if i>cursor:
   nav[cursor-first_mark:i-first_mark]=(float(cc) if asset is None else float(cc)+float(uu)*markets[asset]['minute_close'][cursor:i])
  cc,uu,asset=event['cash_after'],event['units_after'],event['asset_after'];event_marks.append((i-first_mark,float(cc+uu*event['mark'])));cursor=i
 if cursor<mark_end:nav[cursor-first_mark:]=(float(cc) if asset is None else float(cc)+float(uu)*markets[asset]['minute_close'][cursor:mark_end])
 daily_nav=[float(cap)]
 for d in range(1,361):daily_nav.append(float(nav[((start//1440)+d)*1440-1-first_mark]))
 daily_nav[-1]=float(terminal_nav)
 points=[float(cap)];cursor=0
 for idx,v in event_marks:
  if idx+1>cursor:points.extend(nav[cursor:idx+1].tolist());cursor=idx+1
  points.append(v)
 points.extend(nav[cursor:].tolist());points.append(float(terminal_nav))
 minute_dd,_,_=maxdd(points);daily_metrics=metric(daily_nav,365);folds=[]
 for f in range(12):
  a=f*30;b=a+30;folds.append({'fold':f+1,'start_utc':markets[leader]['daily'][368+a]['date'],'end_exclusive_utc':markets[leader]['daily'][368+b]['date'],**metric(daily_nav[a:b+1],365)})
 filled=[t for t in trades if t['status']=='filled'];parts={k:str(sum((D(t['cost_parts'][k]) for t in filled),D(0))) for k in ('fee','half_spread','slippage','impact','tick_rounding')};cost=sum((D(v) for v in parts.values()),D(0));net=terminal_nav-cap;gross=net+cost
 summary={'net_return_pct':daily_metrics['net_return_pct'],'net_pnl_usdt':str(net),'terminal_nav_usdt':str(terminal_nav),'terminal_cash_usdt':str(cash),'terminal_units':str(units),'terminal_flat':units==0,'cost_usdt':str(cost),'cost_parts_usdt':parts,'gross_reference_pnl_usdt':str(gross),'gross_reference_pnl_to_cost':float(gross/cost) if cost else None,'max_drawdown_pct':minute_dd,'daily_mark_drawdown_pct':daily_metrics['max_drawdown_pct'],'drawdown_scope':'OOS 1m bar-close NAV plus immediate post-fill reference marks; excludes intraminute extrema.','sharpe_annualized_daily':daily_metrics['sharpe_annualized'],'cagr_pct':daily_metrics['cagr_pct'],'calmar':daily_metrics['calmar'],'attempts':len(trades),'executions':len(filled),'round_trips':sum(t['side']=='sell' for t in filled),'positive_1x_folds':sum(x['net_return_pct']>0 for x in folds),'rejected_orders':sum(t['status']!='filled' for t in trades),'rejection_reasons':{r:sum(t.get('reason')==r for t in trades if t['status']!='filled') for r in sorted({t.get('reason') for t in trades if t['status']!='filled'})},'capacity_rejections':sum(t.get('reason')=='participation' for t in trades if t['status']!='filled'),'signal_triggers':len(signals),'folds':folds,'daily_nav_sha256_f64le':hashlib.sha256(np.asarray(daily_nav,dtype='<f8').tobytes()).hexdigest(),'daily_nav_samples':len(daily_nav),'minute_nav_sha256_f64le':hashlib.sha256(np.asarray(points,dtype='<f8').tobytes()).hexdigest(),'minute_nav_samples':len(points),'cost_multiplier':mult}
 return {'name':spec['name'],'fingerprint':registry.fingerprint(spec),'spec':spec,'signals':signals,'trades':trades,'daily_nav_usdt':daily_nav,'summary':summary}

def main():
 plan=json.loads((ROUND/'plan.json').read_text());batch=json.loads((ROUND/'batch.json').read_text());fdata=json.loads((ROUND/'exchange_filters.json').read_text());filters={a+'USDT':({x['filterType']:x for x in rows} if isinstance(rows,list) else rows) for a,rows in (fdata.get('symbols') or fdata['filters']).items()}
 markets={a:load_asset(a) for a in ('BTC','ETH')};manifest={'assets':{a:{'source_files':m['files'],'minute_bars':len(m['minute_ts']),'first_minute_ns':int(m['minute_ts'][0]),'last_minute_ns':int(m['minute_ts'][-1]),'daily_bars':len(m['daily']),'daily_close_sha256_f64le':m['daily_close_sha256_f64le']} for a,m in markets.items()},'exchange_filter_snapshot':fdata.get('snapshot',fdata),'kernel_sha256':sha(ROOT/'research/experiments/20261001T133655Z/kernel.py'),'lagged_cost_engine_sha256':sha(engine_path)}
 (ROUND/'data_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');run_dir=ROOT/'data/runs'/ROUND.name;run_dir.mkdir(parents=True,exist_ok=True);cfg={};scenes=[];curves=[]
 for row in batch:
  sp=json.loads((ROOT/row['spec']).read_text());cfg[row['name']]={'role':'candidate','leader':row['leader'],'follower':row['follower'],'lookback_minutes':row['lookback_minutes'],'hold_minutes':row['hold_minutes'],'leader_threshold':row['leader_threshold'],'relative_gap_threshold':row['relative_gap_threshold'],'fingerprint':row['fingerprint'],'spec':row['spec'],'scenarios':{}}
  for mult in (1,2,3):
   arc=run(sp,markets,filters,mult);s=arc['summary'];cfg[row['name']]['scenarios'][str(mult)]=s;gzwrite(run_dir/f"{row['name']}_cost{mult}.json.gz",arc)
   scenes.append({'name':row['name'],'direction':row['leader']+'>'+row['follower'],'lookback_minutes':row['lookback_minutes'],'hold_minutes':row['hold_minutes'],'leader_threshold':row['leader_threshold'],'relative_gap_threshold':row['relative_gap_threshold'],'cost_multiplier':mult,**{k:s[k] for k in ('net_return_pct','net_pnl_usdt','cost_usdt','cost_parts_usdt','max_drawdown_pct','daily_mark_drawdown_pct','gross_reference_pnl_to_cost','round_trips','positive_1x_folds','rejected_orders','capacity_rejections','terminal_flat','signal_triggers')}})
   for d,v in enumerate(arc['daily_nav_usdt']):curves.append({'name':row['name'],'cost_multiplier':mult,'day_index':d,'date':markets[row['leader']]['daily'][368+d]['date'] if d<360 else plan['data']['oos_end_exclusive_utc'][:10],'nav_usdt':v})
  print(row['name'],*[round(cfg[row['name']]['scenarios'][str(m)]['net_return_pct'],5) for m in (1,2,3)],flush=True)
 threshold_values=plan['grid']['leader_return_threshold'];gap_values=plan['grid']['leader_minus_follower_gap_threshold']
 for row in batch:
  p=cfg[row['name']];ti=threshold_values.index(p['leader_threshold']);gi=gap_values.index(p['relative_gap_threshold']);neighbors=[]
  for other in batch:
   q=cfg[other['name']]
   if q['leader']==p['leader'] and abs(threshold_values.index(q['leader_threshold'])-ti)<=1 and abs(gap_values.index(q['relative_gap_threshold'])-gi)<=1:neighbors.append(other['name'])
  c=p['scenarios'];frac=sum(cfg[n]['scenarios']['3']['net_return_pct']>0 for n in neighbors)/len(neighbors)
  for mult in ('1','2','3'):c[mult]['neighborhood_positive_fraction_3x']=frac;c[mult]['neighborhood_size']=len(neighbors)
  gates={'all_cost_scenarios_positive':all(c[str(m)]['net_return_pct']>0 for m in (1,2,3)),'positive_1x_folds_at_least_8':c['1']['positive_1x_folds']>=8,'drawdown_3x_under_25pct':c['3']['max_drawdown_pct']<=25,'neighbor_fraction_at_least_0_60':frac>=0.6,'round_trips_at_least_4':c['1']['round_trips']>=4,'gross_to_cost_at_least_2_5':c['1']['gross_reference_pnl_to_cost'] is not None and c['1']['gross_reference_pnl_to_cost']>=2.5,'no_rejected_or_capacity_filtered_orders':all(c[str(m)]['rejected_orders']==0 and c[str(m)]['capacity_rejections']==0 for m in (1,2,3)),'terminal_flat':all(c[str(m)]['terminal_flat'] for m in (1,2,3))}
  p['gates']=gates;p['status']='passed' if all(gates.values()) else 'rejected'
 baseline=json.load(open(ROOT/'research/experiments/20261013T123949Z/report.json'));base_names=['hold_360d_btc_relative_strength_study','hold_360d_eth_relative_strength_study'];baseline_refs={n:{'source_report':'research/experiments/20261013T123949Z/report.json','source_report_sha256':sha(ROOT/'research/experiments/20261013T123949Z/report.json'),'scenarios':baseline['configs'][n]['scenarios']} for n in base_names}
 ranking=sorted(cfg,key=lambda n:cfg[n]['scenarios']['1']['net_return_pct'],reverse=True);report={'round':ROUND.name,'evaluation_started_utc':datetime.now(timezone.utc).isoformat(),'plan':plan,'data_manifest':manifest,'baseline_references':baseline_refs,'summary':{'candidate_configs':len(batch),'directions':2,'variants_per_direction':9,'candidate_passed':sum(cfg[n]['status']=='passed' for n in cfg),'candidate_rejected':sum(cfg[n]['status']=='rejected' for n in cfg),'oos_days':360,'walk_forward_folds':12,'cost_scenes':len(scenes),'pre_existing_registry_configurations':plan['prior_registry_snapshot']['unique_fingerprints'],'ranking_1x':ranking},'configs':cfg,'scene_summaries':scenes,'artifacts':{'fold_results':'research/experiments/'+ROUND.name+'/fold_results.csv','cost_scenarios':'research/experiments/'+ROUND.name+'/cost_scenarios.csv','equity_curves_daily':'research/experiments/'+ROUND.name+'/equity_curves_daily.csv','sensitivity':'research/experiments/'+ROUND.name+'/sensitivity.csv','sensitivity_surface':'research/experiments/'+ROUND.name+'/sensitivity_surface.svg'}}
 (ROUND/'report.json').write_text(json.dumps(canonical(report),indent=2,ensure_ascii=False,allow_nan=False)+'\n')
 with (ROUND/'fold_results.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['name','direction','lookback_minutes','hold_minutes','leader_threshold','relative_gap_threshold','cost_multiplier','fold','start_utc','end_exclusive_utc','net_return_pct','max_drawdown_pct','sharpe_annualized','cagr_pct','calmar','observations','drawdown_peak_index','drawdown_trough_index'],lineterminator='\n');w.writeheader()
  for row in batch:
   for m in ('1','2','3'):
    for fold in cfg[row['name']]['scenarios'][m]['folds']:w.writerow({'name':row['name'],'direction':row['leader']+'>'+row['follower'],'lookback_minutes':row['lookback_minutes'],'hold_minutes':row['hold_minutes'],'leader_threshold':row['leader_threshold'],'relative_gap_threshold':row['relative_gap_threshold'],'cost_multiplier':m,**fold})
 with (ROUND/'cost_scenarios.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(scenes[0]),lineterminator='\n');w.writeheader();w.writerows(scenes)
 with (ROUND/'equity_curves_daily.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(curves[0]),lineterminator='\n');w.writeheader();w.writerows(curves)
 print(json.dumps(report['summary'],ensure_ascii=False))
if __name__=='__main__':main()
