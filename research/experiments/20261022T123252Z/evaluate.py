#!/usr/bin/env python3
"""Run the pre-reserved daily base-volume MFI momentum long/cash grid on archived Binance spot bars."""
import csv,gzip,hashlib,importlib.util,json,math,statistics,sys
from datetime import datetime,timezone
from decimal import Decimal as D,localcontext
from pathlib import Path
import numpy as np,polars as pl
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sys.path.insert(0,str(ROOT/'research/experiments/20261001T133655Z'));from kernel import fill
sp=importlib.util.spec_from_file_location('daily_mfi_cost_engine',ROOT/'research/experiments/20261001T013355Z/evaluate.py');engine=importlib.util.module_from_spec(sp);sys.modules[sp.name]=engine;sp.loader.exec_module(engine)
MIN_NS=60_000_000_000;MIN_MS=60000;DAY_NS=1440*MIN_NS;DAY_MS=1440*MIN_MS
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def stamp(ms):return datetime.fromtimestamp(ms/1000,timezone.utc).isoformat().replace('+00:00','Z')
def put(path,obj):path.write_text(json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def write_csv(path,rows):
 fields=list(dict.fromkeys(k for x in rows for k in x))
 with path.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
def write_gz_csv(path,rows):
 fields=list(dict.fromkeys(k for x in rows for k in x))
 import io
 b=io.StringIO(newline='');w=csv.DictWriter(b,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
 with path.open('wb') as raw:
  with gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0,compresslevel=9) as out:out.write(b.getvalue().encode())
def load_asset(asset,plan):
 fs=[];files=[]
 for item in plan['data']['assets'][asset]:
  p=ROOT/item['path'];assert p.is_file() and p.stat().st_size==item['bytes'] and sha(p)==item['sha256']
  x=pl.read_parquet(p,columns=['open_ts','available_ts','open','high','low','close','base_volume','quote_volume','is_closed'])
  assert x.height==525600 and x['is_closed'].all() and x['open_ts'].is_sorted()
  assert (x['open_ts'].diff().drop_nulls()==MIN_NS).all() and (x['available_ts']-x['open_ts']==MIN_NS).all()
  assert (x['open']>0).all() and (x['close']>0).all() and (x['quote_volume']>=0).all()
  assert x['base_volume'].null_count()==0 and (x['base_volume']>=0).all()
  assert (x['low']>0).all() and (x['high']>=x['open']).all() and (x['high']>=x['close']).all() and (x['low']<=x['open']).all() and (x['low']<=x['close']).all()
  files.append({**item,'minute_bars':x.height,'first_open_ns':int(x['open_ts'][0]),'last_open_ns':int(x['open_ts'][-1])});fs.append(x)
 m=pl.concat(fs,how='vertical_relaxed').sort('open_ts');assert m.height==1051200 and (m['open_ts'].diff().drop_nulls()==MIN_NS).all()
 d=(m.with_columns((pl.col('open_ts')//DAY_NS).alias('day_ns')).group_by('day_ns',maintain_order=True).agg(pl.col('close').last().cast(pl.Float64).alias('close'),pl.col('high').max().cast(pl.Float64).alias('high'),pl.col('low').min().cast(pl.Float64).alias('low'),pl.col('quote_volume').sum().cast(pl.Float64).alias('quote_volume'),pl.col('base_volume').sum().cast(pl.Float64).alias('base_volume'),pl.len().alias('n')).sort('day_ns'))
 assert d.height==730 and (d['n']==1440).all()
 ts=d['day_ns'].to_numpy()*DAY_MS;cl=d['close'].to_numpy();hi=d['high'].to_numpy();lo=d['low'].to_numpy();qv=d['quote_volume'].to_numpy();bv=d['base_volume'].to_numpy()
 assert np.all(np.diff(ts)==DAY_MS) and np.isfinite(cl).all() and np.isfinite(qv).all() and (cl>0).all() and (qv>=0).all()
 assert np.isfinite(hi).all() and np.isfinite(lo).all() and np.all(hi>=cl) and np.all(lo<=cl) and np.all(lo>0)
 assert np.isfinite(bv).all() and np.all(bv>=0)
 dr=[{'date':datetime.fromtimestamp(int(t)/1000,timezone.utc).date().isoformat(),'day_open_ms':int(t),'close':D(str(c)),'quote_volume':D(str(v))} for t,c,v in zip(ts,cl,qv)]
 return {'asset':asset,'files':files,'minute_ts':m['open_ts'].to_numpy()//1_000_000,'minute_open':m['open'].cast(pl.Float64).to_numpy(),'minute_high':m['high'].cast(pl.Float64).to_numpy(),'minute_low':m['low'].cast(pl.Float64).to_numpy(),'minute_close':m['close'].cast(pl.Float64).to_numpy(),'minute_base':m['base_volume'].cast(pl.Float64).to_numpy(),'minute_quote':m['quote_volume'].cast(pl.Float64).to_numpy(),'day_ts':ts,'daily_close':cl,'daily_rows':dr,'daily_close_sha256':hashlib.sha256(np.asarray(cl,dtype='<f8').tobytes()).hexdigest(),'daily_high':hi,'daily_low':lo,'daily_high_sha256':hashlib.sha256(np.asarray(hi,dtype='<f8').tobytes()).hexdigest(),'daily_low_sha256':hashlib.sha256(np.asarray(lo,dtype='<f8').tobytes()).hexdigest(),'daily_base_volume':bv,'daily_base_volume_sha256':hashlib.sha256(np.asarray(bv,dtype='<f8').tobytes()).hexdigest()}
def maxdd(vals):
 a=np.asarray(vals,dtype=np.float64);peak=np.maximum.accumulate(a);return float(np.max(np.where(peak>0,100*(1-a/peak),0),initial=0))
def mfi_features(highs,lows,closes,volumes,lookback):
 assert isinstance(lookback,int) and lookback>=2 and len(highs)==len(lows)==len(closes)==len(volumes) and len(highs)>lookback
 hs,ls,cs,vs=[[D(str(v)) for v in seq] for seq in (highs,lows,closes,volumes)]
 assert all(h.is_finite() and l.is_finite() and c.is_finite() and v.is_finite() and 0<l<=c<=h and v>=0 for h,l,c,v in zip(hs,ls,cs,vs))
 with localcontext() as ctx:
  ctx.prec=60
  tp3=[h+l+c for h,l,c in zip(hs,ls,cs)];positive=[D(0)]*len(tp3);negative=[D(0)]*len(tp3);out=[None]*len(tp3)
  for j in range(1,len(tp3)):
   flow=tp3[j]*vs[j]
   if tp3[j]>tp3[j-1]:positive[j]=flow
   elif tp3[j]<tp3[j-1]:negative[j]=flow
  for j in range(lookback,len(tp3)):
   pos=sum(positive[j-lookback+1:j+1],D(0));neg=sum(negative[j-lookback+1:j+1],D(0));num=100*pos;den=pos+neg
   out[j]=(num,den,num/den if den else D(50))
 return out

def desired_position(held,numerator,denominator,threshold):
 assert all(v.is_finite() for v in (numerator,denominator,threshold)) and denominator>=0 and 0<=threshold<=100
 with localcontext() as ctx:
  ctx.prec=60
  assert 0<=numerator<=100*denominator
  desired=(numerator>=45*denominator if held else numerator>threshold*denominator) if denominator else (True if held else D(50)>threshold)
 return desired,('hold_MFI_at_or_above45' if held and desired else 'entry_above_MFI_threshold' if desired else 'exit_MFI_below45' if held else 'remain_cash_below_or_at_entry_threshold')

def evaluate_one(row,mult,m,filters,plan):
 pars=json.loads((ROOT/row['spec']).read_text())['parameters'];asset=row['asset'];L=pars['mfi_lookback_days'];H=int(pars['entry_mfi_threshold']);capital=D('2000');cash=capital;units=D(0);desired=False
 start=int(datetime.fromisoformat(plan['time_boundaries']['oos_start_utc'].replace('Z','+00:00')).timestamp()*1000);end=int(datetime.fromisoformat(plan['time_boundaries']['oos_end_exclusive_utc'].replace('Z','+00:00')).timestamp()*1000)
 m0=int(m['minute_ts'][0]);start_i=(start-m0)//MIN_MS;end_i=(end-m0)//MIN_MS;day0=int(m['day_ts'][0]);assert m['minute_ts'][start_i]==start and m['minute_ts'][end_i]==end and end_i-start_i==360*1440
 assert start%DAY_MS==MIN_MS and end%DAY_MS==MIN_MS
 features=mfi_features(m['daily_high'],m['daily_low'],m['daily_close'],m['daily_base_volume'],L);rows=m['daily_rows'];events=[];trades=[];decisions=[];fills=rejects=trips=0;parts={k:D(0) for k in ('fee','half_spread','slippage','impact','tick_rounding')};cost_events=[]
 for step in range(360):
  exec_ms=start+step*DAY_MS;signal_ms=exec_ms-DAY_MS-MIN_MS;idx=(signal_ms-day0)//DAY_MS
  assert m['day_ts'][idx]==signal_ms and idx>=L
  close=D(str(m['daily_close'][idx]));numerator,denominator,score=features[idx];previous=desired
  desired,reason=desired_position(units>0,numerator,denominator,D(H))
  action='entry' if desired and units==0 else 'exit' if (not desired and units>0) else 'hold'
  avail_ms=signal_ms+DAY_MS
  decisions.append({'configuration':row['name'],'asset':asset,'cost_multiplier':mult,'signal_day_utc':stamp(signal_ms),'signal_available_at_utc':stamp(avail_ms),'simulated_decision_at_utc':stamp(exec_ms),'execution_delay_seconds':60,'daily_close':str(m['daily_close'][idx]),'mfi_lookback_days':L,'mfi_numerator':str(numerator),'mfi_denominator':str(denominator),'mfi_value':str(score),'entry_mfi_threshold':H,'daily_high':str(m['daily_high'][idx]),'daily_low':str(m['daily_low'][idx]),'daily_base_volume':str(m['daily_base_volume'][idx]),'prior_desired_long':previous,'desired_long':desired,'action':action,'decision_reason':reason})
  if action not in ('entry','exit'):continue
  mi=(exec_ms-m0)//MIN_MS;ref=D(str(m['minute_open'][mi]));day_i=(exec_ms-day0)//DAY_MS;adv,sigma=engine.lagged_cost_inputs(rows,int(day_i))
  avgmins=int(filters.get('PERCENT_PRICE_BY_SIDE',filters.get('PERCENT_PRICE',{})).get('avgPriceMins',5));base=m['minute_base'][mi-avgmins:mi];quote=m['minute_quote'][mi-avgmins:mi];bs=float(np.sum(base));qs=float(np.sum(quote));proxy=D(str(qs/bs if bs>0 else float(ref)))
  cb,ub=cash,units;c2,u2,t=fill(cash,units,action=='entry',ref,D(str(adv)),D(str(sigma)),mult,filters,proxy)
  t.update({'configuration':row['name'],'asset':asset,'cost_multiplier':mult,'trade_id':f'{row["name"]}:{mult}:{exec_ms}:{action}','reason':reason,'signal_day_utc':stamp(signal_ms),'signal_available_utc':stamp(avail_ms),'execution_utc':stamp(int(m['minute_ts'][mi])),'signal_to_execution_seconds':60,'minute_index':int(mi),'terminal':False,'cash_before':str(cb),'units_before':str(ub),'cash_after':str(c2),'units_after':str(u2),'observed_signal':{'mfi_numerator':str(numerator),'mfi_denominator':str(denominator),'mfi_value':str(score),'signal_close':str(close)}})
  trades.append(t)
  if t['status']=='filled':
   fills+=1;cash,units=c2,u2;events.append({'minute_index':int(mi),'reference':ref,'cash_after':cash,'units_after':units,'trade_id':t['trade_id']})
   for k,v in t['cost_parts'].items():parts[k]+=D(v)
   if action=='exit' and units==0:trips+=1
  else:rejects+=1
 # Terminal liquidation is fixed by OOS boundary; it is not a signal chosen with future observations.
 if units>0:
  ref=D(str(m['minute_open'][end_i]));adv,sigma=engine.lagged_cost_inputs(rows,int((end-day0)//DAY_MS));bs=float(np.sum(m['minute_base'][end_i-5:end_i]));qs=float(np.sum(m['minute_quote'][end_i-5:end_i]));proxy=D(str(qs/bs if bs>0 else float(ref)))
  cb,ub=cash,units;c2,u2,t=fill(cash,units,False,ref,D(str(adv)),D(str(sigma)),mult,filters,proxy)
  t.update({'configuration':row['name'],'asset':asset,'cost_multiplier':mult,'trade_id':f'{row["name"]}:{mult}:{end}:terminal','reason':'predeclared_terminal_liquidation','signal_day_utc':stamp(end-DAY_MS-MIN_MS),'signal_available_utc':stamp(end-MIN_MS),'execution_utc':stamp(int(m['minute_ts'][end_i])),'signal_to_execution_seconds':60,'minute_index':int(end_i),'terminal':True,'cash_before':str(cb),'units_before':str(ub),'cash_after':str(c2),'units_after':str(u2),'observed_signal':None})
  trades.append(t)
  if t['status']=='filled':
   fills+=1;cash,units=c2,u2;trips+=1;events.append({'minute_index':int(end_i),'reference':ref,'cash_after':cash,'units_after':units,'trade_id':t['trade_id']})
   for k,v in t['cost_parts'].items():parts[k]+=D(v)
  else:rejects+=1
 assert units==0,'Terminal liquidation failed; retain explicit balance and reject configuration.'
 # Continuous OOS minute-close NAV and immediate post-fill NAV reference samples.
 navclose=[];post={};cc,uu=capital,D(0);cursor=start_i
 for e in sorted(events,key=lambda x:x['minute_index']):
  mi=e['minute_index']
  if mi>=end_i:continue
  if mi>cursor:navclose.extend((float(cc)+float(uu)*m['minute_close'][cursor:mi]).tolist())
  cc,uu=e['cash_after'],e['units_after'];post[mi]=float(cc+uu*e['reference']);cursor=mi
 if cursor<end_i:navclose.extend((float(cc)+float(uu)*m['minute_close'][cursor:end_i]).tolist())
 assert len(navclose)==end_i-start_i
 sampled=[float(capital)]
 for i,v in enumerate(navclose):
  mi=start_i+i
  if mi in post:sampled.append(post[mi])
  sampled.append(v)
 dnav=[float(capital)]+[navclose[k*1440+1438] for k in range(360)]
 terminal_nav=cash+units*D(str(m['minute_open'][end_i]));assert units==0
 # Include the terminal liquidation mark/cost in continuous OOS drawdown and the final daily sample.
 dnav[-1]=float(terminal_nav);sampled.append(float(terminal_nav))
 folds=[]
 for f in range(12):
  a,b=dnav[f*30],dnav[(f+1)*30];seg=dnav[f*30:(f+1)*30+1]
  folds.append({'fold':f+1,'start_utc':stamp(start+f*30*DAY_MS),'end_exclusive_utc':stamp(start+(f+1)*30*DAY_MS),'start_nav_usdt':a,'end_nav_usdt':b,'net_return_pct':100*(b/a-1),'daily_sample_drawdown_pct':maxdd(seg),'observations':31})
 rr=np.asarray(dnav[1:])/np.asarray(dnav[:-1])-1;sd=float(np.std(rr,ddof=1));sh=float(np.mean(rr)/sd*math.sqrt(365)) if sd else None
 totalcost=sum(parts.values(),D(0));gross=terminal_nav-capital+totalcost;cagr=(float(terminal_nav)/float(capital))**(365/360)-1;daydd=maxdd(dnav)
 return {'configuration':row['name'],'asset':asset,'mfi_lookback_days':L,'entry_mfi_threshold':H,'exit_mfi_threshold':45,'cost_multiplier':mult,'terminal_nav_usdt':str(terminal_nav),'net_pnl_usdt':str(terminal_nav-capital),'net_return_pct':float(100*(terminal_nav/capital-1)),'terminal_cash_usdt':str(cash),'terminal_units':str(units),'terminal_flat':units==0,'cost_usdt':str(totalcost),'cost_parts_usdt':{k:str(v) for k,v in parts.items()},'gross_reference_pnl_usdt':str(gross),'gross_reference_pnl_to_cost':float(gross/totalcost) if totalcost else None,'max_drawdown_1m_sampled_pct':maxdd(sampled),'daily_sample_drawdown_pct':daydd,'drawdown_scope':'All OOS 1-minute close marks plus immediate post-fill reference marks; excludes intraminute extrema.','daily_sharpe_annualized':sh,'cagr_pct':cagr*100,'calmar_daily_sampled':cagr/(daydd/100) if daydd else None,'filled_orders':fills,'rejected_orders':rejects,'round_trips':trips,'positive_folds':sum(x['net_return_pct']>0 for x in folds),'folds':folds,'minute_nav_samples':len(sampled),'minute_nav_sha256_f64le':hashlib.sha256(np.asarray(sampled,dtype='<f8').tobytes()).hexdigest(),'daily_nav':dnav,'daily_nav_sha256_f64le':hashlib.sha256(np.asarray(dnav,dtype='<f8').tobytes()).hexdigest(),'trades':trades,'decisions':decisions}
def main():
 plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());filters=json.loads((R/'exchange_filters.json').read_text())['filters'];markets={a:load_asset(a,plan) for a in ('BTC','ETH')};configs={};trade_rows=[];decision_rows=[];daily_rows=[];fold_rows=[];cost_rows=[]
 for row in batch:
  spc=json.loads((ROOT/row['spec']).read_text());assert registry.fingerprint(spc)==row['fingerprint'];scenes={}
  for mult in (1,2,3):
   z=evaluate_one(row,mult,markets[row['asset']],filters[row['asset']],plan);scenes[str(mult)]=z;trade_rows+=z['trades'];decision_rows+=z['decisions']
   for j,v in enumerate(z['daily_nav']):daily_rows.append({'configuration':row['name'],'asset':row['asset'],'mfi_lookback_days':row['mfi_lookback_days'],'entry_mfi_threshold':row['entry_mfi_threshold'],'cost_multiplier':mult,'day_index':j,'nav_usdt':v})
   for fr in z['folds']:fold_rows.append({'configuration':row['name'],'asset':row['asset'],'mfi_lookback_days':row['mfi_lookback_days'],'entry_mfi_threshold':row['entry_mfi_threshold'],'cost_multiplier':mult,**fr})
   cost_rows.append({'configuration':row['name'],'asset':row['asset'],'mfi_lookback_days':row['mfi_lookback_days'],'entry_mfi_threshold':row['entry_mfi_threshold'],'cost_multiplier':mult,'net_return_pct':z['net_return_pct'],'cost_usdt':z['cost_usdt'],'gross_reference_pnl_to_cost':z['gross_reference_pnl_to_cost'],'positive_folds':z['positive_folds'],'round_trips':z['round_trips'],'rejected_orders':z['rejected_orders'],**{f'cost_{k}_usdt':v for k,v in z['cost_parts_usdt'].items()}})
   print(row['name'],mult,round(z['net_return_pct'],5),z['round_trips'],z['rejected_orders'],flush=True)
  configs[row['name']]={'name':row['name'],'asset':row['asset'],'mfi_lookback_days':row['mfi_lookback_days'],'entry_mfi_threshold':row['entry_mfi_threshold'],'fingerprint':row['fingerprint'],'spec_path':row['spec'],'initial_capital_usdt':2000,'raw_asset_weight':1.0,'scenarios':scenes}
 axisL=plan['grid']['mfi_lookback_days'];axisH=plan['grid']['entry_mfi_threshold'];by={(c['asset'],c['mfi_lookback_days'],c['entry_mfi_threshold']):c for c in configs.values()}
 for c in configs.values():
  li=axisL.index(c['mfi_lookback_days']);hi=axisH.index(c['entry_mfi_threshold']);ns=[]
  for ll in range(max(0,li-1),min(len(axisL),li+2)):
   for hh in range(max(0,hi-1),min(len(axisH),hi+2)):ns.append(by[(c['asset'],axisL[ll],axisH[hh])])
  frac=sum(n['scenarios']['3']['net_return_pct']>0 for n in ns)/len(ns);c['sensitivity']={'neighbor_count':len(ns),'local_3x_neighbor_positive_fraction':frac,'neighbor_names':[n['name'] for n in ns]}
  one=c['scenarios']['1'];three=c['scenarios']['3'];c['gates']={'all_cost_scenarios_positive':all(c['scenarios'][str(k)]['net_return_pct']>0 for k in (1,2,3)),'positive_1x_folds_at_least_8':one['positive_folds']>=8,'drawdown3_lte25':three['max_drawdown_1m_sampled_pct']<=25,'neighbor3_positive_fraction_gte60':frac>=.6,'round_trips1_gte8':one['round_trips']>=8,'gross_cost_ratio1_gte2_5':one['gross_reference_pnl_to_cost'] is not None and one['gross_reference_pnl_to_cost']>=2.5,'no_exchange_or_capacity_rejections':all(c['scenarios'][str(k)]['rejected_orders']==0 for k in (1,2,3)),'terminal_flat':all(c['scenarios'][str(k)]['terminal_flat'] for k in (1,2,3))};c['status']='passed' if all(c['gates'].values()) else 'rejected'
 prior=json.loads((ROOT/'research/experiments/20261014T084051Z/report.json').read_text());bench={a:prior['benchmark_read_only']['assets'][a] for a in ('BTC','ETH')}
 for c in configs.values():
  for z in c['scenarios'].values():
   for k in ('trades','decisions','daily_nav'):z.pop(k,None)
 input_manifest={'assets':{a:{'source_files':markets[a]['files'],'minute_bars':len(markets[a]['minute_ts']),'daily_bars':len(markets[a]['day_ts']),'daily_close_sha256_f64le':markets[a]['daily_close_sha256'],'daily_high_sha256_f64le':markets[a]['daily_high_sha256'],'daily_low_sha256_f64le':markets[a]['daily_low_sha256'],'daily_base_volume_sha256_f64le':markets[a]['daily_base_volume_sha256']} for a in markets}}
 report={'round':R.name,'frozen_plan_sha256':sha(R/'plan.json'),'input_data':input_manifest,'exchange_info_raw_sha256':sha(R/'exchange_info_raw.json'),'benchmark_read_only':{'source_report':'research/experiments/20261014T084051Z/report.json','same_OOS_period_buy_hold':bench,'rerun':False},'summary':{'candidate_configs':len(configs),'passed':sum(c['status']=='passed' for c in configs.values()),'rejected':sum(c['status']=='rejected' for c in configs.values()),'cost_scenarios':len(configs)*3,'oos_days':360,'folds':12,'fold_days':30,'positive_configs_by_cost':{str(k):sum(c['scenarios'][str(k)]['net_return_pct']>0 for c in configs.values()) for k in (1,2,3)},'configs_with_8_positive_1x_folds':sum(c['scenarios']['1']['positive_folds']>=8 for c in configs.values()),'global_3x_positive_neighbor_fraction':sum(c['scenarios']['3']['net_return_pct']>0 for c in configs.values())/len(configs),'ranked_by_1x_net_return':sorted(configs,key=lambda n:configs[n]['scenarios']['1']['net_return_pct'],reverse=True)},'configs':configs,'artifacts':{'fold_results':'fold_results.csv','cost_scenarios':'cost_scenarios.csv','daily_equity':'daily_equity.csv.gz','trades':'trades.csv.gz','decisions':'decisions.csv.gz'}}
 write_csv(R/'fold_results.csv',fold_rows);write_csv(R/'cost_scenarios.csv',cost_rows);write_gz_csv(R/'daily_equity.csv.gz',daily_rows);write_gz_csv(R/'trades.csv.gz',trade_rows);write_gz_csv(R/'decisions.csv.gz',decision_rows);put(R/'report.json',report)
 print('SUMMARY',json.dumps(report['summary'],sort_keys=True))
if __name__=='__main__':main()
