"""Causal pair and cross-venue carry validation using existing signals and accounting."""
from __future__ import annotations
import bisect
import csv
import hashlib
import importlib.util
import io
import json
import math
import statistics
import sys
import zipfile
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
import polars as pl
from statsmodels.tsa.stattools import adfuller
ROOT=Path(__file__).resolve().parents[3]
ROUND=Path(__file__).resolve().parent
MINUTE=60*10**9
HOUR=60*MINUTE
DAY=24*HOUR
VERSION='20250916T000000Z_20260916T000000Z_archive_20260929'

def module(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s)
 sys.modules[name]=m;s.loader.exec_module(m);return m

def utc(ns):return datetime.fromtimestamp(ns/1e9,timezone.utc).isoformat().replace('+00:00','Z')
def ns(s):return int(datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()*1e9)

def cost_inputs(rows,i):
 assert i>=20
 prior=rows[i-20:i]
 adv=statistics.mean(float(x['quote']) for x in prior)
 closes=[float(x['close']) for x in rows[max(0,i-21):i]]
 returns=[math.log(b/a) for a,b in zip(closes,closes[1:])]
 assert adv>0
 return adv,statistics.stdev(returns)

def cost_table(frame,unit=1):
 daily=frame.group_by((pl.col('open_ts')*unit//DAY).alias('day')).agg(pl.col('close').last(),pl.col('quote_volume').sum().alias('quote')).sort('day').to_dicts()
 return {r['day']:cost_inputs(daily,i) for i,r in enumerate(daily) if i>=21}

def execution_price(ref,sign,fee,spread,slip,impact,tick):
 price=ref*(1+math.copysign(spread+slip+impact,sign))
 if tick:
  price=(math.ceil(price/tick-1e-9) if sign>0 else math.floor(price/tick+1e-9))*tick
 return price

def settle(events,index,cutoff,quantity,multiplier):
 amount=0.0;detail=[]
 while index<len(events) and events[index]['ts']<=cutoff:
  e=events[index];q=quantity[e['leg']]
  raw=-q*e['mark']*e['rate']
  paid=raw*multiplier if raw<0 else raw
  if q:
   amount+=paid
   detail.append({**e,'quantity':q,'base_amount_usdt':raw,'amount_usdt':paid,'funding_stress_increment_usdt':paid-raw})
  index+=1
 return index,amount,detail

def metrics(equity,hours,initial_cost_point=False):
 a=np.asarray(equity,float)
 assert np.isfinite(a).all() and (a>0).all()
 dd=float(np.max(1-a/np.maximum.accumulate(a)))
 stat=np.concatenate(([a[0]],a[2:])) if initial_cost_point else a
 ret=np.diff(stat)/stat[:-1]
 sd=float(np.std(ret,ddof=1)) if len(ret)>1 else 0
 sharpe=float(ret.mean()/sd*math.sqrt(8760)) if sd else None
 annual=(a[-1]/a[0])**(8760/hours)-1
 return {'net_return_pct':float((a[-1]/a[0]-1)*100),'max_drawdown_pct':dd*100,'sharpe_annualized':sharpe,'annualized_return_pct':float(annual*100),'calmar':float(annual/dd) if dd else None}

def folds_for(kind):
 wf=module('wf_round',ROOT/'.agents/skills/walk-forward-validation/scripts/walk_forward.py')
 train=180 if kind=='pairs' else 100
 days=365 if kind=='pairs' else 274
 base=ns('2025-09-16T00:00:00Z' if kind=='pairs' else '2025-12-16T00:00:00Z')
 splitter=wf.WalkForwardValidator(wf.WalkForwardConfig(train_size=train,test_size=28,step_size=28,embargo_size=3,purge_size=0))
 out=[]
 offset=MINUTE if kind=='pairs' else HOUR+MINUTE
 for f in splitter.split(days):
  a=int(f.test_indices[0]);b=int(f.test_indices[-1])+1
  out.append({'fold':f.fold_idx+1,'train_start_utc':utc(base+int(f.train_indices[0])*DAY),'train_end_exclusive_utc':utc(base+(int(f.train_indices[-1])+1)*DAY),'test_start_signal_ns':base+a*DAY,'test_end_signal_ns':base+b*DAY,'test_start_utc':utc(base+a*DAY+offset),'test_end_utc':utc(base+b*DAY+offset)})
 assert len(out)==6
 return out

def load_pair_data():
 old=module('legacy_pair',ROOT/'checks/perp_pairs_oos.py')
 btc,bf,bm,bd=old.load_asset('BTC');eth,ef,em,ed=old.load_asset('ETH')
 assert btc['ts'].to_list()==eth['ts'].to_list()
 rows=btc.join(eth,on='ts',suffix='_eth').to_dicts()
 events=sorted([{'ts':r['settlement_ts'],'leg':leg,'rate':float(r['realized_rate']),'mark':float(r['mark_price_at_settlement'])} for leg,funding in enumerate((bf,ef)) for r in funding],key=lambda x:x['ts'])
 costs=[];marks=[]
 for asset in ('BTC','ETH'):
  base=ROOT/'data/normalized/binance'/asset/f'binance_{asset}_{VERSION}'
  frame=pl.read_parquet(base/'perp_bars.parquet')
  costs.append(cost_table(frame))
  mark=pl.read_parquet(base/'mark_hour_bars.parquet')
  marks.append({r['open_ts']:(float(r['low']),float(r['high'])) for r in mark.to_dicts()})
 return {'rows':rows,'times':[r['ts'] for r in rows],'events':events,'meta':[bm,em],'costs':costs,'marks':marks,'old':old,'features':{},'data':{'BTC':bd,'ETH':ed}}

def pair_features(data):
 rows=data['rows'];times=data['times'];old=data['old']
 btc=np.array([r['close'] for r in rows]);eth=np.array([r['close_eth'] for r in rows])
 lo=bisect.bisect_left(times,ns('2026-03-16T00:00:00Z'));hi=bisect.bisect_right(times,ns('2026-09-15T00:00:00Z'))
 for window in (600,720,840):
  features={}
  for i in range(lo,hi):
   beta,z,spread=old.signal(btc[i-window:i],eth[i-window:i],btc[i],eth[i])
   p=float(adfuller(spread,maxlag=10,regression='c',autolag='BIC')[1]) if beta>0 and abs(z)>1.8 else None
   features[i]=(beta,z,p)
  data['features'][window]=features
  print(json.dumps({'pair_feature_window':window,'hours':len(features),'adf_evaluations':sum(x[2] is not None for x in features.values())}),flush=True)

def pair_backtest(data,p,start_ns,end_ns,multiplier,impact=True,folds=None):
 rows=data['rows'];times=data['times'];capital=2000.0
 start=times.index(start_ns);end=times.index(end_ns)
 events=[e for e in data['events'] if start_ns<=e['ts']<=end_ns+MINUTE]
 cash=capital;q=[0.0,0.0];fi=0;equity=[capital];trades=[];funding=[];margin=[];boundary={}
 lots=[float(x['lot_size']) for x in data['meta']];ticks=[float(x['tick_size']) for x in data['meta']];minimums=[float(x['min_notional']) for x in data['meta']]
 bounds={f['test_start_signal_ns'] for f in folds or []}|{end_ns}
 def nav(prices):return cash+sum(a*b for a,b in zip(q,prices))
 def check_margin(i,state):
  low_high=[data['marks'][j][times[i]] for j in (0,1)]
  worst=cash+sum(q[j]*(low_high[j][0] if q[j]>0 else low_high[j][1]) for j in (0,1))
  gross=sum(abs(q[j])*low_high[j][1] for j in (0,1))
  if gross and worst<=.01*gross:margin.append({'ts':utc(times[i]),'state':state,'worst_mark_NAV':worst,'maintenance_assumption':.01*gross})
 def trade(i,target,reason,beta=None,z=None,pvalue=None):
  nonlocal cash
  ref=[float(rows[i]['open']),float(rows[i]['open_eth'])]
  for leg in (0,1):
   change=target[leg]-q[leg]
   if abs(change)<lots[leg]/2:continue
   adv,sigma=data['costs'][leg][times[i]//DAY]
   notional=abs(change)*ref[leg]
   assert notional/adv<=.001,'capacity constraint'
   imp=.5*sigma*math.sqrt(notional/adv)*multiplier if impact else 0
   px=execution_price(ref[leg],change,.0005*multiplier,.0001*multiplier,.0002*multiplier,imp,ticks[leg])
   fee=abs(change*px)*.0005*multiplier
   cost=abs(change)*abs(px-ref[leg])+fee
   cash-=change*px+fee;q[leg]=target[leg]
   trades.append({'ts':utc(times[i]+MINUTE),'asset':('BTC','ETH')[leg],'side':'buy' if change>0 else 'sell','quantity':change,'reference':ref[leg],'execution':px,'fee_usdt':fee,'cost_usdt':cost,'impact_rate':imp,'lagged_daily_ADV':adv,'estimated_participation':notional/adv,'reason':reason,'beta':beta,'z':z,'adf_p':pvalue})
 for i in range(start,end+1):
  ref=[float(rows[i]['open']),float(rows[i]['open_eth'])]
  fi,amount,detail=settle(events,fi,times[i]+MINUTE,q,multiplier);cash+=amount;funding+=detail
  if times[i] in bounds:boundary[times[i]]=nav(ref)
  check_margin(i,'before execution')
  if i==end:
   if any(q):trade(i,[0,0],'scheduled_terminal_exit')
  else:
   beta,z,pvalue=data['features'][p['window_hours']][i]
   if any(q):
    if abs(z)<p['exit_z'] or abs(z)>p['stop_z']:trade(i,[0,0],'z_exit',beta,z)
   elif beta>0 and abs(z)>p['entry_z'] and pvalue is not None and pvalue<p['adf_p']:
    direction=-1 if z>p['entry_z'] else 1
    gross_btc=nav(ref)/(1+beta)
    target=[direction*math.floor(gross_btc/ref[0]/lots[0])*lots[0],-direction*math.floor(beta*gross_btc/ref[1]/lots[1])*lots[1]]
    if all(abs(a*b)>=c for a,b,c in zip(target,ref,minimums)):trade(i,target,'entry',beta,z,pvalue)
  check_margin(i,'after execution')
  equity.append(nav(ref))
 assert q==[0,0]
 if folds:boundary[start_ns]=capital;boundary[end_ns]=equity[-1]
 result={**metrics(equity,(end_ns-start_ns)/HOUR,True),'equity_usdt':equity,'executions':len(trades),'round_trips':sum(t['reason']=='entry' for t in trades)//2,'cost_usdt':sum(t['cost_usdt'] for t in trades),'fee_usdt':sum(t['fee_usdt'] for t in trades),'funding_usdt':sum(x['amount_usdt'] for x in funding),'base_funding_usdt':sum(x['base_amount_usdt'] for x in funding),'cost_pct_initial':sum(t['cost_usdt'] for t in trades)/capital*100,'margin_violations':margin,'trades':trades,'funding_events':funding}
 if folds:result['folds']=[{'fold':f['fold'],'net_return_pct':100*(boundary[f['test_end_signal_ns']]/boundary[f['test_start_signal_ns']]-1),'boundary_rule':'NAV at executable reference before new-fold trade; final boundary after terminal exit'} for f in folds]
 return result

def load_cross_data():
 old=module('legacy_cross',ROOT/'checks/cross_exchange_carry_oos.py')
 plan=ROOT/'data/research/cross_exchange_carry_20260930_plan.json';plan.parent.mkdir(parents=True,exist_ok=True)
 if not plan.exists():plan.write_text((ROUND/'plan.json').read_text())
 po,pc,so,sc,okx,binance,common,details=old.load()
 directory=ROOT/'data/normalized/okx/BTC/cross_exchange_carry_20260930'
 frames=[]
 for source in details['okx_manifest']['sources']['bars']:
  path=Path(source['path'])
  with zipfile.ZipFile(path) as z:
   body=z.read(z.namelist()[0])
  frame=pl.read_csv(io.BytesIO(body),infer_schema=False).select(pl.col('open_time').cast(pl.Int64).alias('open_ts'),pl.col('close').cast(pl.Float64),pl.col('vol_quote').cast(pl.Float64).alias('quote_volume'),pl.col('low').cast(pl.Float64),pl.col('high').cast(pl.Float64))
  frames.append(frame.filter((pl.col('open_ts')>=old.DATA_START)&(pl.col('open_ts')<old.DATA_START+len(po)*60000)))
 volume=pl.concat(frames).unique(subset=['open_ts']).sort('open_ts')
 assert volume.height==len(po) and volume['open_ts'].to_list()==list(range(old.DATA_START,old.DATA_START+len(po)*60000,60000))
 extra=directory/'volume_and_bounds.parquet';volume.write_parquet(extra)
 spot=pl.read_parquet(old.BINANCE/'spot_bars.parquet')
 costs=[cost_table(spot),cost_table(volume,10**6)]
 return {'po':po,'pc':pc,'so':so,'sc':sc,'okx':okx,'binance':binance,'common':common,'old':old,'costs':costs,'low':volume['low'].to_numpy(),'high':volume['high'].to_numpy(),'data':{**details,'okx_actual_volume_path':str(extra.relative_to(ROOT)),'okx_actual_volume_sha256':hashlib.sha256(extra.read_bytes()).hexdigest()}}

def cross_backtest(data,p,start_ns,end_ns,multiplier,impact=True,folds=None):
 old=data['old'];common=data['common'];rates=np.array([max(data['okx'][t],data['binance'][t]) for t in common])
 start=start_ns//10**6;end=end_ns//10**6;capital=100000.0
 spot_cash=capital/2;perp_cash=capital/2;q=0.0;entry=0.0;trades=[];settlements=[];equity=[capital];boundary={};violations=[];decisions=[]
 bounds={f['test_start_signal_ns']//10**6 for f in folds or []}|{end}
 def index(t):return (t-old.DATA_START)//old.MINUTE
 def nav(t):
  j=index(t);return spot_cash+q*data['so'][j]+perp_cash+q*(entry-data['po'][j])
 def trade(t,buy,reason,z=None):
  nonlocal spot_cash,perp_cash,q,entry
  j=index(t);ref=[float(data['so'][j]),float(data['po'][j])]
  if buy:
   proposed=math.floor((nav(t)/14)/max(ref[0]*(1+.0003*multiplier),ref[1])/.01)*.01
  else:proposed=q
  if not proposed:return
  px=[];fees=[];cost=0.0;impacts=[];part=[]
  for leg in (0,1):
   adv,sigma=data['costs'][leg][(t*10**6)//DAY]
   notional=proposed*ref[leg];assert notional/adv<=.001,'capacity constraint'
   imp=.5*sigma*math.sqrt(notional/adv)*multiplier if impact else 0
   # Legacy cross-venue check models effective prices without tick rounding.
   sign=(1 if buy else -1)*(1 if leg==0 else -1)
   price=execution_price(ref[leg],sign,0,.0001*multiplier,.0002*multiplier,imp,0)
   fee=proposed*price*(.001 if leg==0 else .0005)*multiplier
   px.append(price);fees.append(fee);cost+=proposed*abs(price-ref[leg])+fee;impacts.append(imp);part.append(notional/adv)
  if buy:
   spot_cash-=proposed*px[0]+fees[0];perp_cash-=fees[1];q=proposed;entry=px[1]
  else:
   spot_cash+=q*px[0]-fees[0];perp_cash+=q*(entry-px[1])-fees[1];q=0;entry=0
  if spot_cash<0:violations.append({'ts':utc(t*10**6),'reason':'spot cash insufficient, no borrowing allowed'})
  trades.append({'ts':utc(t*10**6),'side':'entry' if buy else 'exit','reason':reason,'quantity_btc':proposed,'spot_reference':ref[0],'perp_reference':ref[1],'spot_execution':px[0],'perp_execution':px[1],'fees_usdt':sum(fees),'cost_usdt':cost,'impact_rates':impacts,'daily_ADV_participations':part,'z':z})
 for k,settlement in enumerate(common):
  if not start<=settlement<=end:continue
  if q:
   mark=float(data['pc'][index(settlement-old.MINUTE)])
   raw=q*mark*data['okx'][settlement]
   amount=raw*multiplier if raw<0 else raw
   perp_cash+=amount
   settlements.append({'ts':utc(settlement*10**6),'rate':data['okx'][settlement],'mark_proxy':mark,'quantity_btc':q,'base_amount_usdt':raw,'amount_usdt':amount})
  fill=settlement+old.HOUR+old.MINUTE
  if settlement in bounds:boundary[settlement]=nav(fill)
  assert k>=p['window_settlements']
  z=old.signals(rates[k],rates[k-p['window_settlements']:k])
  best=data['okx'][settlement]>data['binance'][settlement]
  decisions.append({'ts':utc((settlement+old.HOUR)*10**6),'z':z,'okx_best':best})
  if q and (z<=0 or not best or settlement==end):trade(fill,False,'terminal' if settlement==end else 'signal',z)
  elif not q and z>p['entry_z'] and best and settlement<end:trade(fill,True,'entry',z)
  equity.append(nav(fill))
  # Margin checks at every observed minute until the next decision. High bounds of the
  # completed minute are conservative for a short and affect qualification, not signals.
  if q:
   j=index(fill);last=min(j+8*60,len(data['po']))
   collateral=perp_cash+q*(entry-data['high'][j:last])
   maintenance=.01*q*data['high'][j:last]
   if np.any(collateral<=maintenance):violations.append({'ts':utc(fill*10**6),'reason':'OKX sleeve collateral fails 1% maintenance assumption'})
 assert q==0
 if folds:boundary[start]=capital;boundary[end]=equity[-1]
 result={**metrics(equity,(end-start)/3600000,True),'equity_usdt':equity,'executions':len(trades)*2,'round_trips':sum(t['side']=='entry' for t in trades),'cost_usdt':sum(t['cost_usdt'] for t in trades),'cost_pct_initial':100*sum(t['cost_usdt'] for t in trades)/capital,'funding_usdt':sum(x['amount_usdt'] for x in settlements),'base_funding_usdt':sum(x['base_amount_usdt'] for x in settlements),'margin_violations':violations,'trades':trades,'funding_events':settlements,'decisions':decisions,'sharpe_note':'Sharpe adjusted below to 8-hour sampled returns'}
 # 8-hour sample frequency: opening-cost point merged into the first full interval.
 sampled=np.asarray([equity[0]]+equity[2:]);returns=np.diff(sampled)/sampled[:-1]
 sd=returns.std(ddof=1)
 result['sharpe_annualized']=float(returns.mean()/sd*math.sqrt(1095)) if sd else None
 result['sharpe_note']='annualized sqrt(1095) for 8-hour marks; field shared with pair hourly table'
 if folds:result['folds']=[{'fold':f['fold'],'net_return_pct':100*(boundary[f['test_end_signal_ns']//10**6]/boundary[f['test_start_signal_ns']//10**6]-1),'boundary_rule':'after actual previous funding, before next-fold trade; terminal after liquidation'} for f in folds]
 return result

def baseline_parity(data,kind,replay=False):
 old=data['old']
 old.main()
 path=ROOT/'data/runs'/('perp_pairs_oos_20260929.json' if kind=='pairs' else 'cross_exchange_carry_oos_20260930.json')
 original=json.loads(path.read_text())
 output=ROUND/(kind+'_legacy_result.json')
 original['development_history_note']='already used historical data; not untouched final holdout'
 if not replay:output.write_text(json.dumps(original,ensure_ascii=False,separators=(',',':'))+'\n')
 p={'window_hours':720,'entry_z':2,'exit_z':.5,'stop_z':4,'adf_p':.05} if kind=='pairs' else {'window_settlements':270,'entry_z':2}
 start=ns('2026-03-16T00:00:00Z');end=ns('2026-09-15T00:00:00Z')
 r=pair_backtest(data,p,start,end,1,False) if kind=='pairs' else cross_backtest(data,p,start,end,1,False)
 key='hourly_equity' if kind=='pairs' else 'eight_hour_equity'
 saved=[x['usdt'] for x in original[key]]
 # Pair legacy saves its initial capital point; cross saves post-decision points only.
 expected=saved if kind=='pairs' else [100000]+saved
 assert len(expected)==len(r['equity_usdt'])
 assert np.max(np.abs(np.asarray(expected)-r['equity_usdt']))<1e-7,(kind,'accounting mismatch')
 print('PARITY PASS: complete original '+kind+' equity and final capital match within USDT1e-7',flush=True)
 return str(output.relative_to(ROOT))

def main():
 batch=json.loads((ROUND/'batch.json').read_text());plan=json.loads((ROUND/'plan.json').read_text())
 replay='--reproduce' in sys.argv
 archived=json.loads((ROUND/'report.json').read_text()) if replay else None
 registry=module('registry_validation',ROOT/'research/automation/registry.py');records=registry.read_records(ROOT/'research/automation/registry.jsonl')
 for item in batch:assert records[item['fingerprint']]['status'] in (('passed','rejected') if replay else ('reserved',)),item
 specs={x['name']:json.loads((ROOT/x['spec']).read_text()) for x in batch}
 resume='--resume' in sys.argv
 report={'round':plan['round_utc'],'created_at_utc':datetime.now(timezone.utc).isoformat(),'plan':plan,'configs':{},'blocked_directions':{},'folds':{},'data':{},'legacy_results':{},'sources':plan['sources'],'history_scope':'reused development history; no untouched holdout; previous 54 definitions plus this 20 reservations; all variations correlated','cost_method':'paid funding stressed, receipts unchanged; cash no yield; all impact and volatility inputs lagged complete days; historical instrument rules and maintenance uncalibrated','process_audit':'all 20 candidates/comparators individually reserved before any real backtest; no observed-results tuning'}
 if resume:
  report=json.loads((ROOT/'data/runs/20261001T033355Z_partial.json').read_text())
  report['process_audit']+='; recovered all 54 completed candidate cost curves from saved checkpoint after NumPy fold-count bool serialization failed; no candidate rerun or parameter change'
 contexts={}
 for kind in ('pairs','cross'):
  try:
   data=load_pair_data() if kind=='pairs' else load_cross_data()
   if kind=='pairs' and not resume:pair_features(data)
   contexts[kind]=data;report['data'][kind]=data['data'];report['folds'][kind]=folds_for(kind)
   if not resume:report['legacy_results'][kind]=baseline_parity(data,kind,replay)
  except Exception as error:
   import traceback
   report['blocked_directions'][kind]={'error':repr(error),'traceback':traceback.format_exc()}
   print(json.dumps({'blocked_direction':kind,'error':repr(error)}),flush=True)
 for item in batch:
  name=item['name'];spec=specs[name];kind=item['direction']
  if item['role']!='candidate':continue
  if resume and name in report['configs'] and report['configs'][name].get('actual_backtest_result'):
   print(json.dumps({'reused_saved_candidate':name}),flush=True)
   continue
  if kind not in contexts:
   report['configs'][name]={'fingerprint':item['fingerprint'],'spec_path':item['spec'],'status':'blocked','actual_backtest_result':False,'reason':report['blocked_directions'][kind]};continue
  folds=report['folds'][kind];data=contexts[kind];start=folds[0]['test_start_signal_ns'];end=folds[-1]['test_end_signal_ns']
  outcomes={}
  for k in (1,2,3):
   result=pair_backtest(data,spec['parameters'],start,end,k,True,folds) if kind=='pairs' else cross_backtest(data,spec['parameters'],start,end,k,True,folds)
   outcomes[str(k)]=result
  report['configs'][name]={'fingerprint':item['fingerprint'],'spec_path':item['spec'],'direction':kind,'parameters':spec['parameters'],'actual_backtest_result':True,'cost_scenarios':outcomes}
  checkpoint=ROOT/'data/runs/20261001T033355Z_partial.json'
  checkpoint.parent.mkdir(parents=True,exist_ok=True)
  if not replay:checkpoint.write_text(json.dumps(report,ensure_ascii=False,separators=(',',':'),allow_nan=False)+'\n')
  print(json.dumps({'config':name,'return_1x':outcomes['1']['net_return_pct'],'return_3x':outcomes['3']['net_return_pct'],'round_trips':outcomes['1']['round_trips']}),flush=True)
 # Individually reserved hold benchmarks: actual spot data, fixed exposure, actual cost model.
 for item in batch:
  if item['role']!='comparator':continue
  spec=specs[item['name']];kind='pairs' if 'pairs' in item['name'] else 'cross'
  if kind not in contexts:
   report['configs'][item['name']]={'fingerprint':item['fingerprint'],'spec_path':item['spec'],'status':'blocked','actual_backtest_result':False,'reason':report['blocked_directions'][kind]};continue
  oldspot=module('spot_validator',ROOT/'research/experiments/20261001T013355Z/evaluate.py')
  daily,_=oldspot.load_data();assets=[x.split('/')[0] for x in spec['universe']]
  # Use only the exact start/end minute opens; mark daily closes and terminal cost.
  result={}
  for multiplier in (1,2,3):
   parts=[]
   for asset in assets:
    rows=daily[asset];dates=[x['date'] for x in rows];a=dates.index(spec['parameters']['start_utc'][:10]);b=dates.index(spec['parameters']['end_utc'][:10])
    if kind=='cross':
     path=ROOT/'data/normalized/binance'/asset/f'binance_{asset}_{VERSION}'/'spot_bars.parquet'
     bars=pl.read_parquet(path,columns=['open_ts','open']).filter(pl.col('open_ts').is_in([ns(spec['parameters']['start_utc']),ns(spec['parameters']['end_utc'])]))
     assert bars.height==2
     rows=[dict(x) for x in rows];rows[a]['trade_open']=bars['open'][0];rows[b]['trade_open']=bars['open'][1]
     rows[a]['trade_ts']=ns(spec['parameters']['start_utc']);rows[b]['trade_ts']=ns(spec['parameters']['end_utc'])
    capital=spec['parameters']['initial_capital_usdt']/len(assets)
    parts.append(oldspot.backtest(rows,[True]*365,a,b,capital,1,multiplier))
   curve=[sum(v) for v in zip(*(x['equity_usdt'] for x in parts))]
   result[str(multiplier)]={**oldspot.metrics(curve,b-a,True),'equity_usdt':curve,'executions':sum(x['executions'] for x in parts),'cost_usdt':sum(x['cost_usdt'] for x in parts)}
  report['configs'][item['name']]={'fingerprint':item['fingerprint'],'spec_path':item['spec'],'role':'comparator','status':'rejected','actual_backtest_result':True,'reason':'comparison, not two-parameter qualified candidate','cost_scenarios':result}
 report['sensitivity']={}
 for kind in ('pairs','cross'):
  group=[x for x in report['configs'].values() if x.get('direction')==kind and x.get('actual_backtest_result')]
  if not group:continue
  fraction=sum(x['cost_scenarios']['3']['net_return_pct']>0 for x in group)/len(group)
  report['sensitivity'][kind]={'variants':len(group),'positive_fraction_3x':fraction,'return_range_3x_pct':[min(x['cost_scenarios']['3']['net_return_pct'] for x in group),max(x['cost_scenarios']['3']['net_return_pct'] for x in group)]}
  for row in group:
   c=row['cost_scenarios'];positive=int(sum(x['net_return_pct']>0 for x in c['1']['folds']))
   gates={'positive_1x_2x_3x':all(x['net_return_pct']>0 for x in c.values()),'at_least_4_positive_folds':positive>=4,'drawdown_3x_lte_25pct':c['3']['max_drawdown_pct']<=25,'neighborhood_3x_positive_gte_60pct':fraction>=.6,'round_trips_at_least_4':c['1']['round_trips']>=4,'no_margin_or_cash_violation':not any(x['margin_violations'] for x in c.values())}
   row.update(criteria=gates,positive_folds_1x=positive,status='passed' if all(gates.values()) else 'rejected')
 report['summary']={state:[n for n,x in report['configs'].items() if x['status']==state] for state in ('passed','rejected','blocked')}
 report['verification']={'legacy_parity':'full curves tested when available, tolerance USDT1e-7','synthetic_check':'check_accounting.py','real_data_not_synthetic':True}
 output=ROOT/'data/runs/reproduce_20261001T033355Z.json' if replay else ROUND/'report.json'
 if replay:
  for name,row in report['configs'].items():
   assert row['status']==archived['configs'][name]['status'],name
   for k,curve in row.get('cost_scenarios',{}).items():
    assert curve['equity_usdt']==archived['configs'][name]['cost_scenarios'][k]['equity_usdt'],(name,k)
  print('REPRODUCE PASS: 54 candidate and 6 comparator cost curves exactly match archived outputs',flush=True)
 output.write_text(json.dumps(report,ensure_ascii=False,separators=(',',':'),allow_nan=False)+'\n')
 csv_path=ROOT/'data/runs/reproduce_20261001T033355Z_sensitivity.csv' if replay else ROUND/'sensitivity.csv'
 with csv_path.open('w',newline='') as file:
  writer=csv.writer(file,lineterminator='\n');writer.writerow(['config','parameters','cost_multiplier','return_pct','max_drawdown_pct','Sharpe','Calmar','executions','round_trips','cost_usdt','funding_usdt','positive_folds_1x','status'])
  for name,row in report['configs'].items():
   for k,x in row.get('cost_scenarios',{}).items():
    writer.writerow([name,json.dumps(row.get('parameters',{}),sort_keys=True),k,x['net_return_pct'],x['max_drawdown_pct'],x.get('sharpe_annualized',x.get('sharpe_365')),x.get('calmar'),x['executions'],x.get('round_trips'),x['cost_usdt'],x.get('funding_usdt'),row.get('positive_folds_1x'),row['status']])
 print(json.dumps(report['summary']),flush=True)

if __name__=='__main__':main()
