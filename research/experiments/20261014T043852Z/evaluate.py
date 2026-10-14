#!/usr/bin/env python3
"""Evaluate a frozen daily failed-breakdown/reclaim, long-only hold grid."""
import csv,hashlib,json,math,os,sys
from datetime import datetime,timezone
from decimal import Decimal as D
from pathlib import Path
import numpy as np
import polars as pl
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sys.path.insert(0,str(ROOT/'research/experiments/20261001T133655Z'));import kernel
DAY=86_400_000;MINUTE=60_000

def stamp(ms):return datetime.fromtimestamp(ms/1000,timezone.utc).isoformat().replace('+00:00','Z')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dec(v):return D(str(v))
def clean(x):return json.loads(json.dumps(x,default=str,ensure_ascii=False,allow_nan=False))
def write_json(p,x):p.write_text(json.dumps(clean(x),indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def drawdown(path):
 ar=np.asarray(path,dtype=np.float64);peaks=np.maximum.accumulate(ar);return float(np.max(np.where(peaks>0,100*(1-ar/peaks),0),initial=0))

def load_market(plan):
 assets={}
 for asset in ('BTC','ETH'):
  frames=[]
  for meta in plan['data']['assets'][asset]:
   p=ROOT/meta['path'];assert sha(p)==meta['sha256'] and p.stat().st_size==meta['bytes']
   f=pl.read_parquet(p,columns=['open_ts','available_ts','open','high','low','close','quote_volume','is_closed'])
   assert f.height==525600 and f['is_closed'].all() and f['open_ts'].is_sorted()
   assert (f['available_ts'].to_numpy()-f['open_ts'].to_numpy()==MINUTE*1_000_000).all()
   assert (f['open_ts'].diff().drop_nulls()==MINUTE*1_000_000).all();frames.append(f)
  f=pl.concat(frames).sort('open_ts');ts=f['open_ts'].to_numpy()//1_000_000
  assert len(ts)==1_051_200 and ts[0]==int(datetime(2024,9,16,tzinfo=timezone.utc).timestamp()*1000) and ts[-1]+MINUTE==int(datetime(2026,9,16,tzinfo=timezone.utc).timestamp()*1000)
  assert (np.diff(ts)==MINUTE).all(),f'{asset} gap/overlap'
  daily=(f.with_columns((pl.col('open_ts')//(DAY*1_000_000)*DAY).alias('day_ts'))
      .group_by('day_ts',maintain_order=True)
      .agg(pl.col('open').first().cast(pl.Float64).alias('open'),pl.col('high').max().cast(pl.Float64).alias('high'),pl.col('low').min().cast(pl.Float64).alias('low'),pl.col('close').last().cast(pl.Float64).alias('close'),pl.col('quote_volume').sum().cast(pl.Float64).alias('quote_volume'),pl.len().alias('minute_count')))
  assert daily.height==730 and (daily['minute_count']==1440).all() and daily['day_ts'].is_sorted()
  assert (np.diff(daily['day_ts'].to_numpy())==DAY).all()
  m={'minute_ts':ts,'minute_open':f['open'].cast(pl.Float64).to_numpy(),'minute_close':f['close'].cast(pl.Float64).to_numpy(),'day_ts':daily['day_ts'].to_numpy(),'open':daily['open'].to_numpy(),'high':daily['high'].to_numpy(),'low':daily['low'].to_numpy(),'close':daily['close'].to_numpy(),'quote_volume':daily['quote_volume'].to_numpy()}
  assert all(np.isfinite(m[x]).all() for x in ('minute_open','minute_close','open','high','low','close','quote_volume'))
  assert (m['minute_open']>0).all() and (m['minute_close']>0).all() and (m['quote_volume']>=0).all() and ((m['low']<=m['close'])&(m['close']<=m['high'])).all()
  assets[asset]=m
 ex=json.loads((ROUND/'exchange_info_raw.json').read_text());filters={}
 for a in ('BTC','ETH'):
  s=next(x for x in ex['symbols'] if x['symbol']==a+'USDT');assert s['status']=='TRADING' and s.get('isSpotTradingAllowed',True)
  filters[a]={f['filterType']:f for f in s['filters']}
  for kind in ('PRICE_FILTER','LOT_SIZE','NOTIONAL','PERCENT_PRICE_BY_SIDE'):assert kind in filters[a]
 return assets,filters

def evaluate_sleeve(name,asset,params,mult,m,filters,plan):
 capital=D('1000');cash=capital;units=D(0);cost_parts={x:D(0) for x in ('fee','half_spread','slippage','impact','tick_rounding')}
 trades=[];decisions=[];daily_equity=[];daily_nav=[];event_marks=[];nav_path=[float(capital)];fold_nav=[float(capital)]
 pending=None;position=None;fills=rejects=round_trips=0
 start_ms=int(datetime.fromisoformat(plan['data']['start_utc'].replace('Z','+00:00')).timestamp()*1000)
 end_ms=int(datetime.fromisoformat(plan['data']['end_exclusive_utc'].replace('Z','+00:00')).timestamp()*1000)
 assert end_ms-start_ms==360*DAY and start_ms%DAY==MINUTE and end_ms%DAY==MINUTE
 minute_start=(start_ms-int(m['minute_ts'][0]))//MINUTE;minute_end=(end_ms-int(m['minute_ts'][0]))//MINUTE
 assert m['minute_ts'][minute_start]==start_ms and m['minute_ts'][minute_end]==end_ms
 n=params['breakdown_lookback_days'];kdays=params['reclaim_window_days'];hold=params['fixed_holding_days'];first_day=int(m['day_ts'][0])
 for step in range(360):
  exec_ms=start_ms+step*DAY;signal_ms=exec_ms-MINUTE-DAY;di=(signal_ms-first_day)//DAY;assert m['day_ts'][di]==signal_ms
  close=float(m['close'][di]);prior_low=float(np.min(m['low'][di-n:di]));pending_before=None if pending is None else dict(pending)
  action='hold';reclaim=False;breakdown=False;expired=False;reason=None
  if position is not None:
   if exec_ms>=position['exit_due_ms']:
    action='time_exit';reason='fixed_holding_period_expired'
   else:reason='position_open_signals_ignored'
  else:
   if pending is not None and di>pending['expiry_day_index']:
    pending=None;expired=True
   if pending is not None and di>pending['breakdown_day_index'] and di<=pending['expiry_day_index'] and close>pending['break_level']:
    reclaim=True;action='reclaim_entry';reason='close_reclaimed_stored_breakdown_level'
   elif pending is None and close<prior_low:
    pending={'break_level':prior_low,'breakdown_day_index':int(di),'expiry_day_index':int(di+kdays)};breakdown=True;action='arm_failed_breakdown';reason='close_below_strict_prior_N_day_low'
  decision={'configuration':name,'asset':asset,'cost_multiplier':mult,'signal_day_utc':stamp(signal_ms),'signal_available_at_utc':stamp(signal_ms+DAY),'simulated_decision_at_utc':stamp(exec_ms),'execution_delay_seconds':60,'close':close,'prior_N_day_low':prior_low,'breakdown_lookback_days':n,'reclaim_window_days':kdays,'fixed_holding_days':hold,'pending_before':pending_before,'pending_after':None if pending is None else dict(pending),'setup_breakdown':breakdown,'setup_reclaim':reclaim,'setup_expired':expired,'position_open_before':position is not None,'action':action,'reason':reason}
  decisions.append(decision)
  should_buy=reclaim and position is None;should_sell=(position is not None and action=='time_exit')
  mi=(exec_ms-int(m['minute_ts'][0]))//MINUTE;ref=dec(m['minute_open'][mi]);avgmins=int(filters['PERCENT_PRICE_BY_SIDE']['avgPriceMins']);avg=dec(np.mean(m['minute_close'][mi-avgmins:mi])) if avgmins else ref
  if should_buy or should_sell:
   vv=np.diff(np.log(m['close'][di-20:di+1]));sigma=dec(np.std(vv,ddof=1));adv=dec(np.mean(m['quote_volume'][di-19:di+1]));assert adv>0
   before_position=position.copy() if position else None
   cash2,units2,tr=kernel.fill(cash,units,should_buy,ref,adv,sigma,mult,filters,avg)
   tr.update({'configuration':name,'asset':asset,'cost_multiplier':mult,'trade_id':f'{name}:{mult}:{asset}:{exec_ms}:{action}','signal_day_utc':stamp(signal_ms),'signal_available_at_utc':stamp(signal_ms+DAY),'simulated_at_utc':stamp(exec_ms),'quote_reference':'archived Binance 1m open; virtual reference, not actual book quote','minute_index':int(mi),'terminal':False,'setup_action':action,'setup_reason':reason,'break_level':str(before_position['break_level'] if before_position else (pending_before['break_level'] if pending_before else prior_low)),'breakdown_day_utc':stamp(int(m['day_ts'][before_position['breakdown_day_index'] if before_position else (pending_before['breakdown_day_index'] if pending_before else di)])),'reclaim_days_after_breakdown':int(di-(before_position['breakdown_day_index'] if before_position else (pending_before['breakdown_day_index'] if pending_before else di))) if should_buy else None,'position_entry_at_utc':before_position['entry_at_utc'] if before_position else None})
   trades.append(tr)
   if tr['status']=='filled':
    fills+=1;cash,units=cash2,units2
    for key in cost_parts:cost_parts[key]+=D(tr['cost_parts'][key])
    if should_buy:
     pending=None;position={'entry_at_utc':stamp(exec_ms),'entry_reference':str(ref),'exit_due_ms':exec_ms+hold*DAY,'break_level':tr['break_level'],'breakdown_day_index':int(before_position['breakdown_day_index'] if before_position else int(di-(tr['reclaim_days_after_breakdown'] or 0)))}
    else:
     round_trips+=1;position=None;pending=None
   else:
    rejects+=1
    if should_buy:pending=None  # one-shot reclaim order; rejection consumes the setup
   event_marks.append({'minute_index':int(mi),'reference':str(ref),'cash_after':str(cash),'units_after':str(units),'status':tr['status']})
  post_nav=float(cash+units*ref);nav_path.append(post_nav)
  close_end=mi+1440;assert close_end<=minute_end
  nav_path.extend((float(cash)+float(units)*m['minute_close'][mi:close_end]).tolist())
  eod_i=mi+1438;eod_ms=int(m['minute_ts'][eod_i])+MINUTE;assert eod_ms==exec_ms+DAY-MINUTE
  eod_nav=float(cash)+float(units)*float(m['minute_close'][eod_i]);daily_equity.append({'configuration':name,'cost_multiplier':mult,'asset':asset,'timestamp_utc':stamp(eod_ms),'nav_usdt':eod_nav});daily_nav.append(eod_nav)
  if step>0 and step%30==0:fold_nav.append(post_nav)
 mi=minute_end;ref=dec(m['minute_open'][mi]);avgmins=int(filters['PERCENT_PRICE_BY_SIDE']['avgPriceMins']);avg=dec(np.mean(m['minute_close'][mi-avgmins:mi])) if avgmins else ref
 if units>0:
  terminal_signal_ms=end_ms-MINUTE-DAY;terminal_di=(terminal_signal_ms-first_day)//DAY;assert m['day_ts'][terminal_di]==terminal_signal_ms
  adv=dec(np.mean(m['quote_volume'][terminal_di-19:terminal_di+1]));sigma=dec(np.std(np.diff(np.log(m['close'][terminal_di-20:terminal_di+1])),ddof=1))
  ca,ua,tr=kernel.fill(cash,units,False,ref,adv,sigma,mult,filters,avg)
  tr.update({'configuration':name,'asset':asset,'cost_multiplier':mult,'trade_id':f'{name}:{mult}:{asset}:{end_ms}:terminal','signal_day_utc':stamp(terminal_signal_ms),'signal_available_at_utc':stamp(end_ms-MINUTE),'simulated_at_utc':stamp(end_ms),'quote_reference':'archived Binance 1m open; terminal virtual liquidation','minute_index':int(mi),'terminal':True,'setup_action':'terminal_exit','setup_reason':'predeclared_OOS_terminal_close','break_level':None,'breakdown_day_utc':None,'reclaim_days_after_breakdown':None,'position_entry_at_utc':position['entry_at_utc']})
  trades.append(tr)
  if tr['status']=='filled':
   fills+=1;round_trips+=1;cash,units=ca,ua;position=None
   for key in cost_parts:cost_parts[key]+=D(tr['cost_parts'][key])
  else:rejects+=1
  event_marks.append({'minute_index':int(mi),'reference':str(ref),'cash_after':str(cash),'units_after':str(units),'status':tr['status']})
 terminal_nav=float(cash+units*ref);nav_path.append(terminal_nav);fold_nav.append(terminal_nav)
 assert units==0 and position is None and len(fold_nav)==13
 folds=[]
 for i in range(12):
  a,b=fold_nav[i],fold_nav[i+1]
  folds.append({'fold':i+1,'start_utc':stamp(start_ms+i*30*DAY),'end_exclusive_utc':stamp(start_ms+(i+1)*30*DAY),'start_nav_usdt':a,'end_nav_usdt':b,'net_return_pct':(b/a-1)*100})
 cost=sum(cost_parts.values(),D(0));gross=D(str(terminal_nav))-capital+cost
 return {'terminal_nav_usdt':str(D(str(terminal_nav))),'net_pnl_usdt':str(D(str(terminal_nav))-capital),'net_return_pct':(terminal_nav/float(capital)-1)*100,'cost_usdt':str(cost),'cost_parts_usdt':{k:str(v) for k,v in cost_parts.items()},'gross_reference_pnl_usdt':str(gross),'gross_to_cost':float(gross/cost) if cost else None,'fills':fills,'rejected_orders':rejects,'round_trips':round_trips,'positive_folds':sum(f['net_return_pct']>0 for f in folds),'terminal_cash_usdt':str(cash),'terminal_units':str(units),'terminal_reference_price':str(ref),'max_drawdown_1m_sampled_pct':drawdown(nav_path),'daily_sample_drawdown_pct':drawdown([float(capital)]+daily_nav+[terminal_nav]),'drawdown_scope':'OOS 1-minute archived closes plus immediate post-fill reference marks; no intra-minute extrema.','folds':folds,'fold_nav':[str(x) for x in fold_nav],'minute_nav_samples':len(nav_path),'sampled_nav_sha256':hashlib.sha256(np.asarray(nav_path,dtype='<f8').tobytes()).hexdigest(),'daily_nav':daily_nav,'daily_equity':daily_equity,'trades':trades,'decisions':decisions,'event_marks':event_marks,'asset':asset,'configuration':name}

def main():
 plan=json.loads((ROUND/'plan.json').read_text());plan_sha=sha(ROUND/'plan.json');batch=json.loads((ROUND/'batch.json').read_text());ledger=Path(os.environ.get('RECLAIM_REGISTRY_LEDGER',ROOT/'research/automation/registry.jsonl'));rec=registry.read_records(ledger)
 for row in batch:
  spec=json.loads((ROOT/row['spec']).read_text());fp=registry.fingerprint(spec);r=rec.get(fp);assert r and r['status']=='reserved' and r['result_available'] is False,(row['name'],r)
 markets,filters=load_market(plan);all_trades=[];all_decisions=[];all_daily=[];configs={}
 start_ms=int(datetime.fromisoformat(plan['data']['start_utc'].replace('Z','+00:00')).timestamp()*1000);end_ms=int(datetime.fromisoformat(plan['data']['end_exclusive_utc'].replace('Z','+00:00')).timestamp()*1000)
 prior=json.loads((ROOT/'research/experiments/20261013T224056Z/report.json').read_text());baseline=prior['configs']['hold_360d_BTC_ETH_50_50_monthly_volmanaged']
 for row in batch:
  spec=json.loads((ROOT/row['spec']).read_text());p=spec['parameters'];scenes={}
  for mult in (1,2,3):
   sleeves={a:evaluate_sleeve(row['name'],a,p,mult,markets[a],filters[a],plan) for a in ('BTC','ETH')}
   for a in ('BTC','ETH'):all_trades.extend(sleeves[a]['trades']);all_decisions.extend(sleeves[a]['decisions']);all_daily.extend(sleeves[a]['daily_equity'])
   daily_nav=np.asarray(sleeves['BTC']['daily_nav'])+np.asarray(sleeves['ETH']['daily_nav']);terminal=sum((dec(sleeves[a]['terminal_nav_usdt']) for a in ('BTC','ETH')),D(0))
   cost=sum((dec(sleeves[a]['cost_usdt']) for a in ('BTC','ETH')),D(0));costparts={k:str(sum((dec(sleeves[a]['cost_parts_usdt'][k]) for a in ('BTC','ETH')),D(0))) for k in ('fee','half_spread','slippage','impact','tick_rounding')}
   mi_start=(start_ms-int(markets['BTC']['minute_ts'][0]))//MINUTE;mi_end=(end_ms-int(markets['BTC']['minute_ts'][0]))//MINUTE;minute_count=mi_end-mi_start
   per_asset_close={}
   for a in ('BTC','ETH'):
    m=markets[a];cl=m['minute_close'][mi_start:mi_end];casharr=np.full(len(cl),1000.0);unitsarr=np.zeros(len(cl));cash=1000.0;units=0.0;cursor=0
    for e in sorted(sleeves[a]['event_marks'],key=lambda z:z['minute_index']):
     pos=e['minute_index']-mi_start
     if pos<0 or pos>=len(cl):continue
     if pos>cursor:casharr[cursor:pos]=cash;unitsarr[cursor:pos]=units
     cash=float(dec(e['cash_after']));units=float(dec(e['units_after']));casharr[pos]=cash;unitsarr[pos]=units;cursor=pos+1
    if cursor<len(cl):casharr[cursor:]=cash;unitsarr[cursor:]=units
    per_asset_close[a]=casharr+unitsarr*cl
   portfolio_close=per_asset_close['BTC']+per_asset_close['ETH'];event_rows=[]
   for a in ('BTC','ETH'):
    for e in sleeves[a]['event_marks']:
     if e['minute_index']<mi_start or e['minute_index']>mi_end:continue
     pos=e['minute_index']-mi_start;wealth=0.0
     for b in ('BTC','ETH'):
      candidates=[z for z in sleeves[b]['event_marks'] if z['minute_index']<=e['minute_index']]
      ca,ua=(float(dec(candidates[-1]['cash_after'])),float(dec(candidates[-1]['units_after']))) if candidates else (1000.0,0.0)
      px=float(dec(e['reference'])) if b==a else float(markets[b]['minute_open'][e['minute_index']]);wealth+=ca+ua*px
     event_rows.append((pos,wealth))
   path=[2000.0];cursor=0
   for pos,wealth in sorted(set(event_rows)):
    if pos>cursor:path.extend(portfolio_close[cursor:pos].tolist())
    if pos==len(portfolio_close):path.append(wealth);cursor=pos
    else:path.extend([wealth,float(portfolio_close[pos])]);cursor=pos+1
   path.extend(portfolio_close[cursor:].tolist())
   folds=[]
   for i in range(12):
    a=sum((dec(sleeves[z]['fold_nav'][i]) for z in ('BTC','ETH')),D(0));b=sum((dec(sleeves[z]['fold_nav'][i+1]) for z in ('BTC','ETH')),D(0))
    folds.append({'fold':i+1,'start_utc':stamp(start_ms+i*30*DAY),'end_exclusive_utc':stamp(start_ms+(i+1)*30*DAY),'start_nav_usdt':str(a),'end_nav_usdt':str(b),'net_return_pct':float(100*(b/a-1))})
   daily_path=np.concatenate((np.asarray([2000.0]),daily_nav,np.asarray([float(terminal)])));returns=daily_path[1:]/daily_path[:-1]-1;sd=float(np.std(returns,ddof=1)) if len(returns)>1 else 0
   sharpe=float(np.mean(returns)/sd*math.sqrt(365)) if sd else None;dddaily=drawdown(daily_path);cagr=((float(terminal)/2000)**(365/360)-1)*100
   scene={'terminal_nav_usdt':str(terminal),'net_pnl_usdt':str(terminal-D(2000)),'net_return_pct':float(100*(terminal/D(2000)-1)),'cost_usdt':str(cost),'cost_parts_usdt':costparts,'gross_reference_pnl_usdt':str(sum((dec(sleeves[a]['gross_reference_pnl_usdt']) for a in ('BTC','ETH')),D(0))),'gross_to_cost':float(sum((dec(sleeves[a]['gross_reference_pnl_usdt']) for a in ('BTC','ETH')),D(0))/cost) if cost else None,'fills':sum(sleeves[a]['fills'] for a in ('BTC','ETH')),'rejected_orders':sum(sleeves[a]['rejected_orders'] for a in ('BTC','ETH')),'round_trips':sum(sleeves[a]['round_trips'] for a in ('BTC','ETH')),'positive_folds':sum(f['net_return_pct']>0 for f in folds),'daily_sharpe_annualized':sharpe,'cagr_pct':cagr,'calmar_daily_sampled':cagr/dddaily if dddaily else None,'daily_sample_drawdown_pct':dddaily,'terminal_units_by_asset':{a:sleeves[a]['terminal_units'] for a in ('BTC','ETH')},'max_drawdown_1m_sampled_pct':drawdown(path),'drawdown_scope':'Synchronized OOS 1-minute archived closes plus immediate fill/terminal marks; no intra-minute extrema.','folds':folds,'minute_nav_samples':len(path),'minute_nav_sha256':hashlib.sha256(np.asarray(path,dtype='<f8').tobytes()).hexdigest(),'asset_sleeves':{a:{k:v for k,v in sleeves[a].items() if k not in ('daily_nav','daily_equity','trades','decisions','event_marks')} for a in ('BTC','ETH')},'daily_nav_sha256':hashlib.sha256(np.asarray(daily_nav,dtype='<f8').tobytes()).hexdigest()}
   scenes[str(mult)]=scene
  cfg={'name':row['name'],'spec_path':row['spec'],'fingerprint':registry.fingerprint(spec),'parameters':p,'cost_scenarios':scenes,'role':'candidate'};c1=scenes['1'];c3=scenes['3']
  for mult in ('1','2','3'):
   sc=scenes[mult];sc['max_drawdown_pct']=sc['max_drawdown_1m_sampled_pct'];sc['sampled_1m_nav_drawdown_pct']=sc['max_drawdown_1m_sampled_pct'];sc['sharpe_annualized_daily']=sc['daily_sharpe_annualized'];sc['minute_nav_sha256_f64le']=sc['minute_nav_sha256'];sc['daily_nav_drawdown_pct']=sc['daily_sample_drawdown_pct'];sc['positive_1x_folds']=sc['positive_folds']
  cfg['gates']={'positive_1x_folds':c1['positive_folds'],'3x_sampled_drawdown_pct':c3['max_drawdown_1m_sampled_pct'],'zero_rejected_orders':all(scenes[k]['rejected_orders']==0 for k in ('1','2','3')),'terminal_flat':all(D(v)==0 for k in ('1','2','3') for v in scenes[k]['terminal_units_by_asset'].values())}
  configs[row['name']]=cfg
  print(f"{row['name']} {[round(scenes[k]['net_return_pct'],3) for k in ('1','2','3')]}",flush=True)
 for row in batch:
  c=configs[row['name']];p=c['parameters'];neighbors=[]
  for other in batch:
   q=json.loads((ROOT/other['spec']).read_text())['parameters']
   if abs([10,20,40].index(q['breakdown_lookback_days'])-[10,20,40].index(p['breakdown_lookback_days']))<=1 and abs([1,2,3].index(q['reclaim_window_days'])-[1,2,3].index(p['reclaim_window_days']))<=1:neighbors.append(other['name'])
  frac=sum(configs[x]['cost_scenarios']['3']['net_return_pct']>0 for x in neighbors)/len(neighbors);c['sensitivity']={'local_3x_neighbor_positive_fraction':frac,'neighbor_count':len(neighbors),'neighbors':neighbors}
  s1,s3=c['cost_scenarios']['1'],c['cost_scenarios']['3'];g=s1['positive_folds']>=8 and s3['max_drawdown_1m_sampled_pct']<=25 and frac>=.60 and s1['gross_to_cost'] is not None and s1['gross_to_cost']>=2.5 and all(c['cost_scenarios'][k]['net_return_pct']>0 for k in ('1','2','3')) and all(c['cost_scenarios'][k]['rejected_orders']==0 for k in ('1','2','3')) and all(D(v)==0 for k in ('1','2','3') for v in c['cost_scenarios'][k]['terminal_units_by_asset'].values())
  c['status']='passed' if g else 'rejected'
 baseline=json.loads((ROOT/'research/experiments/20261013T224056Z/report.json').read_text())['configs']['hold_360d_BTC_ETH_50_50_monthly_volmanaged']
 report={'round':ROUND.name,'plan_sha256':plan_sha,'evaluation_started_utc':datetime.now(timezone.utc).isoformat(),'plan':plan,'data_manifest':{'assets':{a:{'source_files':plan['data']['assets'][a],'minute_rows':len(markets[a]['minute_ts']),'daily_rows':len(markets[a]['day_ts']),'daily_ohlcv_sha256_f64le':hashlib.sha256(np.column_stack([markets[a][k] for k in ('open','high','low','close','quote_volume')]).astype('<f8').tobytes()).hexdigest()} for a in ('BTC','ETH')}},'benchmark_read_only':{'source_report':'research/experiments/20261013T224056Z/report.json','configuration':'hold_360d_BTC_ETH_50_50_monthly_volmanaged','status':'read_only_same_window_reference','cost_scenarios':baseline['cost_scenarios']},'summary':{'candidate_configs':9,'passed':sum(c['status']=='passed' for c in configs.values()),'rejected':sum(c['status']=='rejected' for c in configs.values()),'oos_days':360,'folds':12,'fold_days':30,'cost_scenes':27,'positive_configs_by_cost_multiplier':{k:sum(c['cost_scenarios'][k]['net_return_pct']>0 for c in configs.values()) for k in ('1','2','3')},'ranked_by_1x_net_return':sorted(configs,key=lambda x:configs[x]['cost_scenarios']['1']['net_return_pct'],reverse=True)},'configs':configs}
 write_json(ROUND/'report.json',report)
 for file,rows in (('trades.csv',all_trades),('decisions.csv',all_decisions),('daily_equity.csv',all_daily)):
  fields=sorted({k for row in rows for k in row})
  with (ROUND/file).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
 print(json.dumps(report['summary'],ensure_ascii=False),flush=True)
if __name__=='__main__':main()
