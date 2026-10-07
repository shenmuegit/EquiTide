"""Actual public quotes + virtual funds. No private API or historical fills."""
import argparse,copy,fcntl,gzip,hashlib,importlib.util,json,math,os,statistics,subprocess,sys,urllib.parse,urllib.request
from datetime import datetime,timedelta,timezone
from decimal import Decimal as D
from pathlib import Path
R=Path(__file__).resolve().parents[2];T=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'research/automation'));import registry
PIN='4e8f986601e8e0fafb15c521dcfd9d657dc7ccc2';DAY=86400000
DEFAULT_COSTS={'fee_per_side':.001,'slippage':.0002,'impact_coefficient':.5,'max_ADV_participation':.001}
SOURCES=[('20261002T174933Z','channel_2026_combo_e15_x30_btc0.75'),('20261002T195003Z','channel_asma_2026_BTC_CHANNEL_ETH_ASMA_e0.015_d15'),('20261005T214041Z','filtered_span_2026_combo_e15_b0.03_x30_s25_btc0.675'),('20261002T154903Z','channel_2026_combo_e20_x30_btc0.75'),('20261002T215033Z','channel_ema_2026_BTC_CHANNEL_ETH_EMA_s65_d15'),('20261007T123850Z','filtered_span_2026_combo_e15_b0.03_x30_s29_btc0.675'),('20261002T195003Z','channel_asma_2026_BTC_CHANNEL_ETH_ASMA_e0.0125_d15'),('20261005T214041Z','filtered_span_2026_combo_e20_b0.03_x30_s25_btc0.675'),('20261002T174933Z','channel_2026_combo_e15_x40_btc0.75'),('20261002T195003Z','channel_asma_2026_BTC_ASMA_ETH_CHANNEL_e0.0125_d15')]
LABELS=['两币收盘通道15/30','BTC通道15/30；ETH SMA65 +1.5%/-0.5%','两币通道15/30+EMA25±3%','两币通道20/30','BTC通道15/30；ETH EMA65±1.5%','两币通道15/30+EMA29±3%','BTC通道15/30；ETH SMA65 +1.25%/-0.5%','两币通道20/30+EMA25±3%','两币通道15/40','BTC SMA65 +1.25%/-0.5%；ETH通道15/30']
def utc():return datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
def dt(s):return datetime.fromisoformat(s.replace('Z','+00:00'))
def iso_ms(x):return datetime.fromtimestamp(x/1000,timezone.utc).isoformat().replace('+00:00','Z')
def dumps(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n'
def digest(x):return hashlib.sha256(dumps(x).encode()).hexdigest()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write_once(p,x):
 b=(x+'\n' if p.suffix=='.md' else dumps(x)).encode();p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists():
  if p.read_bytes()!=b:raise ValueError('Immutable artifact differs: '+str(p))
  return
 with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def atomic(p,x):
 p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_suffix(p.suffix+'.tmp')
 with tmp.open('w') as f:f.write(dumps(x));f.flush();os.fsync(f.fileno())
 os.replace(tmp,p)
 # Flush directory metadata as well as contents before accepting a persisted account.
 fd=os.open(str(p.parent),os.O_DIRECTORY);os.fsync(fd);os.close(fd)
def module(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
kernel=module('paper10_lot',R/'research/experiments/20261001T133655Z/kernel.py')
SIGNAL_FILES={'daily-close-range-breakout':('20261002T174933Z','close_channel'),'daily-sma-asymmetric-hysteresis':('20261002T094655Z','asymmetric_sma_hysteresis'),'daily-ema-hysteresis':('20261001T234032Z','ema_hysteresis'),'daily-channel-ema-confirmation':('20261007T123850Z','filtered_channel')}
SIGNALS={family:module('paper10_signal_'+str(i),R/'research/experiments'/folder/'signals.py') for i,(family,(folder,fn)) in enumerate(SIGNAL_FILES.items())}
def signal_step(sp,values,previous):
 """values ends in the REAL unfinished daily candle; it never enters a decision."""
 p=sp['parameters'];family=sp['family'];i=len(values)-1;assert i>=66
 fn=getattr(SIGNALS[family],SIGNAL_FILES[family][1])
 if family=='daily-close-range-breakout':args=(p['entry_lookback_days'],p['exit_lookback_days'])
 elif family=='daily-sma-asymmetric-hysteresis':args=(p['lookback_days'],p['entry_band_fraction'],p['exit_band_fraction'])
 elif family=='daily-ema-hysteresis':args=(p['span_days'],p['symmetric_band_fraction'])
 else:args=(p['entry_lookback_days'],p['exit_lookback_days'],p['EMA_span_days'],p['EMA_symmetric_band'])
 z=fn(values,*args,start=i,end=i+1)[0];last=D(values[i-1]);want=previous
 if family=='daily-close-range-breakout':up=last>D(z['entry_channel_prior']);down=last<D(z['exit_channel_prior'])
 elif family=='daily-sma-asymmetric-hysteresis':up=last>D(z['SMA_prior'])*(1+D(str(p['entry_band_fraction'])));down=last<D(z['SMA_prior'])*(1-D(str(p['exit_band_fraction'])))
 elif family=='daily-ema-hysteresis':up=float(last)>z['EMA_prior']*(1+p['symmetric_band_fraction']);down=float(last)<z['EMA_prior']*(1-p['symmetric_band_fraction'])
 else:up=z['channel_entry'] and z['EMA_entry'];down=z['channel_exit'] or z['EMA_exit']
 if family=='daily-channel-ema-confirmation' and down:want=False
 elif up:want=True
 elif down:want=False
 z.update(long=bool(want),previous_desired_long=bool(previous),forcing_entry=bool(up),forcing_exit=bool(down),action='entry' if want and not previous else 'exit' if previous and not want else 'hold');return z

def paper_fill(cash,units,buy,quote,adv,sigma,mult,filters,avg_price,costs=None):
 costs=costs or DEFAULT_COSTS;bid,ask=D(quote['bid']),D(quote['ask'])
 if not (bid.is_finite() and ask.is_finite() and 0<bid<=ask and adv>0 and sigma>=0):raise ValueError('Invalid quote or lagged cost input')
 mid=(bid+ask)/2;budget=cash if buy else units*mid;participation=budget/adv
 t={'side':'buy' if buy else 'sell','reference':str(mid),'observed_bid':str(bid),'observed_ask':str(ask),'budget':str(budget),'lagged_ADV':str(adv),'lagged_sigma':str(sigma),'participation':str(participation),'cost_multiplier':mult,'cash_before':str(cash),'units_before':str(units),'average_price_reference':str(avg_price)}
 def reject(why):return cash,units,{**t,'status':'rejected','reason':why,'cash_after':str(cash),'units_after':str(units),'cost_usdt':'0'}
 if participation>D(str(costs['max_ADV_participation'])):return reject('participation')
 fee=D(str(costs['fee_per_side']))*mult;spread=(ask-bid)/(2*mid)*mult;slip=D(str(costs['slippage']))*mult;impact=D(str(costs['impact_coefficient']))*sigma*participation.sqrt()*mult
 pf=filters['PRICE_FILTER'];lf=filters['LOT_SIZE'];nf=filters.get('NOTIONAL',filters.get('MIN_NOTIONAL',{}));tick=D(pf['tickSize']);step=D(lf['stepSize'])
 theoretical=mid*(1+(spread+slip+impact)*(1 if buy else -1));price=kernel.adverse_tick(theoretical,tick,buy)
 if price<=0 or (D(pf['minPrice'])>0 and price<D(pf['minPrice'])) or (D(pf['maxPrice'])>0 and price>D(pf['maxPrice'])):return reject('price')
 qty=kernel.floor_step(cash/(price*(1+fee)) if buy else units,step)
 if qty<=0 or qty<D(lf['minQty']) or (D(lf['maxQty'])>0 and qty>D(lf['maxQty'])):return reject('quantity')
 notional=qty*price
 if notional<D(nf.get('minNotional','0')) or (D(nf.get('maxNotional','0'))>0 and notional>D(nf['maxNotional'])):return reject('notional')
 pp=filters.get('PERCENT_PRICE_BY_SIDE') or filters.get('PERCENT_PRICE')
 if pp:
  prefix=('bid' if buy else 'ask') if 'bidMultiplierUp' in pp else ''
  down=pp[prefix+'MultiplierDown'] if prefix else pp['multiplierDown'];up=pp[prefix+'MultiplierUp'] if prefix else pp['multiplierUp']
  if not avg_price*D(down)<=price<=avg_price*D(up):return reject('current_percent_price_reference')
 parts={'fee':notional*fee,'half_spread':qty*mid*spread,'slippage':qty*mid*slip,'impact':qty*mid*impact,'tick_rounding':qty*abs(price-theoretical)};cost=sum(parts.values())
 cash2=cash-notional-parts['fee'] if buy else cash+notional-parts['fee'];units2=units+qty if buy else units-qty
 assert cash2>=0 and units2>=0 and abs(cash+units*mid-(cash2+units2*mid)-cost)<D('1e-18')
 return cash2,units2,{**t,'status':'filled','execution':str(price),'theoretical_execution':str(theoretical),'quantity':str(qty),'fee_rate':str(fee),'half_spread_rate':str(spread),'slippage_rate':str(slip),'impact_rate':str(impact),'cost_usdt':str(cost),'cost_parts':{a:str(v) for a,v in parts.items()},'cash_after':str(cash2),'units_after':str(units2)}

def initial_state(plan,start):
 state={'schema':1,'plan_sha256':plan['_sha256'],'cohort_started_at_utc':start,'cohort_end_utc':(dt(start)+timedelta(days=plan['duration_days'])).isoformat().replace('+00:00','Z'),'last_observation_id':None,'last_observed_at_utc':None,'observations':0,'coverage_gaps':[],'portfolios':{}}
 for p in plan['portfolios']:
  assert sum(D(str(c['weight'])) for c in p['components'])==D(1)
  scenarios={}
  for k in plan['cost_multipliers']:
   sleeves={c['asset']:{'cash_usdt':str(D(p['capital_usdt'])*D(str(c['weight']))),'units':'0','desired_long':False,'last_signal_open_ms':None,'executions':0,'round_trips':0,'cost_usdt':'0','cost_parts':{a:'0' for a in ('fee','half_spread','slippage','impact','tick_rounding')}} for c in p['components']}
   scenarios[str(k)]={'sleeves':sleeves,'NAV_usdt':str(p['capital_usdt']),'peak_NAV_usdt':str(p['capital_usdt']),'max_drawdown_pct':0.,'fold_milestones':[]}
  state['portfolios'][p['id']]={'scenarios':scenarios}
 return state

def qualify(scenes,capital,elapsed,coverage):
 base=scenes['1'];marks=base['fold_milestones'];prev=D(capital);positive=0
 for point in marks:
  value=D(point['NAV_usdt']);positive+=int(value>prev);prev=value
 cost=D(base['cost_usdt']);gross=D(base['NAV_usdt'])-D(capital)+cost;ratio=float(gross/cost) if cost>0 else None
 gates={'minimum180days':elapsed>=180*86400,'six_observed_folds':len(marks)==6,'positive_all_costs':all(x['net_return_pct']>0 for x in scenes.values()),'four_positive_folds1':positive>=4,'sampled_drawdown3_lte25pct':scenes['3']['observed_sample_max_drawdown_pct']<=25,'two_round_trips1':base['round_trips']>=2,'gross_reference_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'coverage_gte95pct':coverage>=.95,'fold_boundary_delay_lte3h':all(x['boundary_late_seconds']<=10800 for x in marks),'no_negative_balances':all(D(st['cash_usdt'])>=0 and D(st['units'])>=0 for x in scenes.values() for st in x['sleeves'].values()),'terminal_flat':all(D(st['units'])==0 for x in scenes.values() for st in x['sleeves'].values())}
 return gates,positive,ratio

def advance(plan,prior,market,observation_id):
 if prior and prior['last_observation_id']==observation_id:return copy.deepcopy(prior),{'already_applied':True,'trades':[]}
 state=copy.deepcopy(prior) if prior else initial_state(plan,market['quote_capture_start_utc']);assert state['plan_sha256']==plan['_sha256']
 observed=market['evaluated_at_utc'];assert dt(observed)>=dt(state['cohort_started_at_utc'])
 gap=None
 if state['last_observed_at_utc']:
  seconds=(dt(observed)-dt(state['last_observed_at_utc'])).total_seconds();assert seconds>0
  if seconds>plan['maximum_observation_gap_seconds']:
   gap={'from_utc':state['last_observed_at_utc'],'to_utc':observed,'seconds':seconds};state['coverage_gaps'].append(gap)
 trades=[];decisions=[];configs={};terminal=dt(observed)>=dt(state['cohort_end_utc'])
 for p in plan['portfolios']:
  ps=state['portfolios'][p['id']];summaries={}
  for k in plan['cost_multipliers']:
   ss=ps['scenarios'][str(k)]
   for c in p['components']:
    asset=c['asset'];sp=plan['components'][c['source_fingerprint']];st=ss['sleeves'][asset];rows=market['daily'][asset];closed=rows[:-1];latest=closed[-1];new_day=st['last_signal_open_ms']!=latest['open_ms']
    if new_day:
     if st['last_signal_open_ms'] is not None and latest['open_ms']-st['last_signal_open_ms']>DAY:
      decisions.append({'portfolio':p['id'],'cost_multiplier':k,'asset':asset,'unprocessed_daily_bars':(latest['open_ms']-st['last_signal_open_ms'])//DAY-1,'action':'process latest closed day only;no backfilled orders'})
     z=signal_step(sp,[x['close'] for x in rows],st['desired_long']);st['desired_long']=z['long'];st['last_signal_open_ms']=latest['open_ms']
     decisions.append({'portfolio':p['id'],'cost_multiplier':k,'asset':asset,'signal_available_at_utc':iso_ms(latest['available_ms']),'simulated_decision_at_utc':observed,'execution_delay_seconds':(dt(observed)-dt(iso_ms(latest['available_ms']))).total_seconds(),'context':z})
    if terminal:st['desired_long']=False
    cash,units=D(st['cash_usdt']),D(st['units']);want=st['desired_long']
    if (new_day or terminal) and ((want and units==0) or (not want and units>0)):
     adv=D(str(statistics.mean(float(x['quote_volume']) for x in closed[-20:])));vv=[float(x['close']) for x in closed[-21:]];sigma=D(str(statistics.stdev([math.log(b/a) for a,b in zip(vv,vv[1:])])))
     cash2,units2,trade=paper_fill(cash,units,want,market['quotes'][asset],adv,sigma,k,market['filters'][asset],D(market['average_prices'][asset]),plan.get('costs'))
     trade.update(trade_id=f'{observation_id}:{p["id"]}:{k}:{asset}',portfolio=p['id'],asset=asset,quote_observed_at_utc=market['quotes'][asset]['observed_at_utc'],simulated_at_utc=observed,signal_available_at_utc=iso_ms(latest['available_ms']),terminal=terminal)
     assert dt(trade['simulated_at_utc'])>=dt(trade['quote_observed_at_utc']) and dt(trade['simulated_at_utc'])>=dt(trade['signal_available_at_utc'])
     trades.append(trade);st.update(cash_usdt=str(cash2),units=str(units2))
     if trade['status']=='filled':
      st['executions']+=1;st['round_trips']+=int(not want and units>0 and units2==0);st['cost_usdt']=str(D(st['cost_usdt'])+D(trade['cost_usdt']))
      for a,v in trade['cost_parts'].items():st['cost_parts'][a]=str(D(st['cost_parts'][a])+D(v))
   nav=sum(D(st['cash_usdt'])+D(st['units'])*(D(market['quotes'][a]['bid'])+D(market['quotes'][a]['ask']))/2 for a,st in ss['sleeves'].items());peak=max(D(ss['peak_NAV_usdt']),nav)
   ss.update(NAV_usdt=str(nav),peak_NAV_usdt=str(peak),max_drawdown_pct=max(ss['max_drawdown_pct'],float(100*(1-nav/peak))))
   elapsed=(dt(observed)-dt(state['cohort_started_at_utc'])).total_seconds();matured=min(6,int(elapsed//(30*86400)))
   while len(ss['fold_milestones'])<matured:
    n=len(ss['fold_milestones'])+1;ss['fold_milestones'].append({'fold':n,'scheduled_boundary_utc':(dt(state['cohort_started_at_utc'])+timedelta(days=n*30)).isoformat().replace('+00:00','Z'),'actual_observed_boundary_utc':observed,'NAV_usdt':str(nav),'boundary_late_seconds':elapsed-n*30*86400,'contains_coverage_gap':bool(state['coverage_gaps'])})
   cost=sum(D(st['cost_usdt']) for st in ss['sleeves'].values());parts={a:str(sum(D(st['cost_parts'][a]) for st in ss['sleeves'].values())) for a in ('fee','half_spread','slippage','impact','tick_rounding')}
   summaries[str(k)]={'NAV_usdt':str(nav),'net_PnL_usdt':str(nav-D(p['capital_usdt'])),'net_return_pct':float(100*(nav/D(p['capital_usdt'])-1)),'observed_sample_max_drawdown_pct':ss['max_drawdown_pct'],'drawdown_scope':'actual quote-snapshot NAV sampling only;not minute/tick maximum','executions':sum(st['executions'] for st in ss['sleeves'].values()),'round_trips':sum(st['round_trips'] for st in ss['sleeves'].values()),'cost_usdt':str(cost),'cost_pct_initial':float(100*cost/D(p['capital_usdt'])),'cost_parts':parts,'sleeves':copy.deepcopy(ss['sleeves']),'fold_milestones':copy.deepcopy(ss['fold_milestones'])}
  elapsed=(dt(observed)-dt(state['cohort_started_at_utc'])).total_seconds();configs[p['id']]={'name':p['id'],'label':p['label'],'raw_weights':[c['weight'] for c in p['components']],'capital_usdt':p['capital_usdt'],'scenes':summaries,'status':'rejected','reason':'actual partial live-quote paper observation;180days/sixfold not yet complete;account continues','observed_elapsed_seconds':elapsed}
  expected=max(1,int(elapsed//7200)+1);count_coverage=min(1.,(state['observations']+1)/expected)
  missing=sum(max(0.,x['seconds']-7200) for x in state['coverage_gaps']);time_coverage=max(0.,1-missing/max(1.,elapsed));coverage=min(count_coverage,time_coverage)
  gates,positive,ratio=qualify(summaries,p['capital_usdt'],elapsed,coverage)
  configs[p['id']].update(criteria=gates,positive_fold_count1=positive,gross_reference_PnL_to_cost1=ratio,observation_coverage_fraction=coverage)
  if terminal:
   configs[p['id']]['status']='passed' if all(gates.values()) else 'rejected'
   configs[p['id']]['reason']='180day sampled-paper criteria assessed;not minute-risk/exchange execution proof;review actual gaps and boundary delays'

 state.update(last_observation_id=observation_id,last_observed_at_utc=observed,observations=state['observations']+1)
 report={'observation_id':observation_id,'mode':market['mode'],'already_applied':False,'plan_sha256':plan['_sha256'],'cohort_started_at_utc':state['cohort_started_at_utc'],'cohort_end_utc':state['cohort_end_utc'],'observed_at_utc':observed,'configs':configs,'trades':trades,'decisions':decisions,'new_gap':gap,'coverage_gaps':copy.deepcopy(state['coverage_gaps']),'new_filled_virtual_orders':sum(t['status']=='filled' for t in trades),'real_orders':0,'interpretation':'real public market quotes with virtual funds;no historical fills,no exchange execution guarantee;unmatured paper results do not qualify stable profit'}
 report['state_before_sha256']=digest(prior);report['state_after_sha256']=digest(state);report['market_sha256']=digest(market)
 report['source_hashes']={str(q.relative_to(R)):sha(q) for q in [T/'run.py',T/'check.py',R/'research/automation/registry.py']}
 return state,report

PUBLIC={'/api/v3/time','/api/v3/exchangeInfo','/api/v3/klines','/api/v3/avgPrice','/api/v3/ticker/bookTicker'}
def get_public(path,params,folder,name,provenance):
 if path not in PUBLIC:raise ValueError('Only allowlisted public GET market endpoints are permitted')
 url='https://data-api.binance.vision'+path+('?' +urllib.parse.urlencode(params) if params else '');started=utc()
 request=urllib.request.Request(url,method='GET',headers={'User-Agent':'EquiTide-Paper10/1.0','Cache-Control':'no-cache'})
 with urllib.request.urlopen(request,timeout=25) as response:raw=response.read();status=response.status;header_date=response.headers.get('Date')
 received=utc();assert status==200;target=folder/(name+'.json.gz')
 with target.open('wb') as f:
  with gzip.GzipFile(filename='',fileobj=f,mode='wb',mtime=0) as gz:gz.write(raw)
 provenance.append({'url':url,'method':'GET','status':status,'requested_at_utc':started,'received_at_utc':received,'http_date':header_date,'raw_response_sha256':hashlib.sha256(raw).hexdigest(),'archive':str(target.relative_to(R)),'archive_sha256':sha(target)})
 atomic(folder/'http_provenance.json',provenance)
 return json.loads(raw),received

def capture(plan,folder):
 provenance=[];before,_=get_public('/api/v3/time',{},folder,'time_before',provenance)
 meta,_=get_public('/api/v3/exchangeInfo',{'symbols':json.dumps(['BTCUSDT','ETHUSDT'],separators=(',',':'))},folder,'exchange_info',provenance)
 daily={};filters={};average={};quotes={};seed=plan['warmup_seed_open_ms'];day=int(before['serverTime'])//DAY
 for asset in ('BTC','ETH'):
  item=next(x for x in meta['symbols'] if x['symbol']==asset+'USDT');assert item['status']=='TRADING' and item.get('isSpotTradingAllowed',True)
  filters[asset]={x['filterType']:x for x in item['filters']}
  bars,_=get_public('/api/v3/klines',{'symbol':asset+'USDT','interval':'1d','startTime':seed,'limit':1000},folder,asset+'_daily',provenance)
  assert bars[0][0]==seed and len(bars)>66 and len(bars)<1000
  assert [b[0] for b in bars]==list(range(seed,day*DAY+1,DAY)) and all(b[6]+1==b[0]+DAY for b in bars)
  for b in bars:
   assert all(D(str(b[i])).is_finite() for i in (1,2,3,4,5,7)) and 0<D(b[3])<=D(b[4])<=D(b[2]) and D(b[5])>=0 and D(b[7])>=0
  daily[asset]=[{'open_ms':b[0],'available_ms':b[6]+1,'close':b[4],'quote_volume':b[7]} for b in bars]
  avg,_=get_public('/api/v3/avgPrice',{'symbol':asset+'USDT'},folder,asset+'_average',provenance);assert D(avg['price'])>0;average[asset]=avg['price']
  percent=filters[asset].get('PERCENT_PRICE_BY_SIDE') or filters[asset].get('PERCENT_PRICE')
  if percent and int(percent['avgPriceMins'])>0:assert int(avg['mins'])==int(percent['avgPriceMins'])
 for asset in ('BTC','ETH'):
  q,received=get_public('/api/v3/ticker/bookTicker',{'symbol':asset+'USDT'},folder,asset+'_quote',provenance)
  assert q['symbol']==asset+'USDT' and 0<D(q['bidPrice'])<=D(q['askPrice']) and D(q['bidQty'])>0 and D(q['askQty'])>0
  quotes[asset]={'bid':q['bidPrice'],'ask':q['askPrice'],'bid_qty':q['bidQty'],'ask_qty':q['askQty'],'observed_at_utc':received,'provider_event_time':'not supplied by bookTicker;receipt timestamp is recorded'}
 after,received=get_public('/api/v3/time',{},folder,'time_after',provenance);assert int(after['serverTime'])//DAY==day
 assert abs(int(after['serverTime'])-int(dt(received).timestamp()*1000))<=10000,'Exchange/local clock mismatch'
 evaluated=utc();assert all(0<=(dt(evaluated)-dt(q['observed_at_utc'])).total_seconds()<=30 for q in quotes.values())
 market={'mode':'live_public_quotes','quote_capture_start_utc':min(q['observed_at_utc'] for q in quotes.values()),'evaluated_at_utc':evaluated,'server_time_before_ms':before['serverTime'],'server_time_after_ms':after['serverTime'],'daily':daily,'filters':filters,'average_prices':average,'quotes':quotes,'provenance':provenance}
 write_once(folder/'market.json',market);return market

def ensure_plan():
 path=T/'plan.json'
 if path.exists():plan=json.loads(path.read_text());plan['_sha256']=sha(path);return plan
 records=registry.read_records(R/'research/automation/registry.jsonl');components={};portfolios=[]
 for n,((stamp,name),label) in enumerate(zip(SOURCES,LABELS),1):
  source='research/experiments/'+stamp+'/specs/'+name+'.json';raw=subprocess.check_output(['git','show',PIN+':'+source],cwd=R);sp=json.loads(raw);assert (R/source).read_bytes()==raw and registry.fingerprint(sp) in records
  refs=[]
  for comp in sp['components']:
   fp=comp['fingerprint'];rec=records[fp];cs=copy.deepcopy(rec['spec']);assert registry.fingerprint(cs)==fp and rec['result_available'];asset=cs['universe'][0].split('/')[0]
   old=json.loads((R/rec['report']).read_text());row=next(x for x in old['configs'].values() if x['fingerprint']==fp);cp=row['spec'];cr=subprocess.check_output(['git','show',PIN+':'+cp],cwd=R);assert json.loads(cr)==cs
   components[fp]={**cs,'asset':asset,'source_path':cp,'source_sha256':hashlib.sha256(cr).hexdigest()}
   assert D(cs['parameters']['initial_capital_usdt'])==D(2000)*D(str(comp['weight']))
   refs.append({'source_fingerprint':fp,'asset':asset,'weight':comp['weight']})
  portfolios.append({'id':f'P{n:02}','label':label,'capital_usdt':2000,'source_path':source,'source_sha256':hashlib.sha256(raw).hexdigest(),'source_fingerprint':registry.fingerprint(sp),'source_spec':sp,'components':refs})
 assert len(portfolios)==10
 seed=int(datetime(2025,9,16,tzinfo=timezone.utc).timestamp()*1000)
 plan={'schema':1,'created_at_utc':utc(),'registry_at_cohort_freeze':{'sha256':sha(R/'research/automation/registry.jsonl'),'rows':len((R/'research/automation/registry.jsonl').read_bytes().splitlines()),'preserved_ids':len(records)},'source_pin':PIN,'mode':'real Binance public spot quotes plus virtual funds','start_policy':'first valid quote receipt in initial successful observation;warmup never creates old trades','warmup_seed_open_ms':seed,'duration_days':180,'fold_days':30,'cost_multipliers':[1,2,3],'costs':DEFAULT_COSTS,'maximum_observation_gap_seconds':10800,'quote_max_age_seconds':30,'initial_state':'Each sleeve begins cash and desired-cash;process latest closed daily bar only;no warmup trade/state replay','execution':'Actual observed bid/ask around mid,estimated slip/impact and fee simultaneously scaled1/2/3;adverse PRICE tick and LOT floor;independent original sleeve funds,no transfer/rebalance. All fills simulated at actual calculation timestamp after quotes/reservation;no historical fill price. Immediate full IOC is an assumption,not exchange acceptance.','qualification':'Observe at least180days and6x30day windows;all costs net-positive,>=4 positive1x folds,sampled3xDD<=25%,>=2 roundtrips,no negative balances,terminal liquidation and>=95percent expected observation coverage. No stable-live or minute-risk proof from sampled virtual accounts. Fixed historical sensitivity retained only as prior reference.','components':components,'portfolios':portfolios,'frozen_reused_code_sha256':{str(p.relative_to(R)):sha(p) for p in [R/'research/experiments'/x[0]/'signals.py' for x in SIGNAL_FILES.values()]+[R/'research/experiments/20261001T133655Z/kernel.py']}}
 write_once(path,plan);plan['_sha256']=sha(path);return plan

def audit_observation(folder):
 plan=json.loads((T/'plan.json').read_text());plan['_sha256']=sha(T/'plan.json')
 before=json.loads((folder/'state_before.json').read_text());after=json.loads((folder/'state_after.json').read_text());report=json.loads((folder/'report.json').read_text());market=json.loads((folder/'market.json').read_text())
 assert report['mode']=='live_public_quotes' and report['plan_sha256']==plan['_sha256']
 assert report['state_before_sha256']==digest(before) and report['state_after_sha256']==digest(after) and report['market_sha256']==digest(market)
 for path,h in report['source_hashes'].items():assert sha(R/path)==h
 assert json.loads((folder/'trade_ledger.json').read_text())==report['trades']
 for path,h in plan['frozen_reused_code_sha256'].items():assert sha(R/path)==h
 for pr in market['provenance']:
  raw=gzip.decompress((R/pr['archive']).read_bytes());assert hashlib.sha256(raw).hexdigest()==pr['raw_response_sha256'] and sha(R/pr['archive'])==pr['archive_sha256'] and pr['method']=='GET' and pr['status']==200
  assert urllib.parse.urlparse(pr['url']).path in PUBLIC
 for a in ('BTC','ETH'):
  raw=json.loads(gzip.decompress((folder/(a+'_quote.json.gz')).read_bytes()));q=market['quotes'][a];assert q['bid']==raw['bidPrice'] and q['ask']==raw['askPrice']
  assert all(x['available_ms']<=market['server_time_before_ms'] for x in market['daily'][a][:-1])
 for b in json.loads((folder/'batch.json').read_text()):
  rows=[json.loads(x) for x in (R/'research/automation/registry.jsonl').read_text().splitlines()];ev=[x for x in rows if x['fingerprint']==b['fingerprint'] and x['status']=='reserved'];assert len(ev)==1
  assert ev[0]['recorded_at_utc']<min(x['requested_at_utc'] for x in market['provenance'])<market['evaluated_at_utc']
 for tr in report['trades']:
  assert dt(tr['simulated_at_utc'])>=dt(tr['quote_observed_at_utc']) and dt(tr['simulated_at_utc'])>=dt(tr['signal_available_at_utc'])
  if tr['status']!='filled':assert tr['cash_before']==tr['cash_after'] and tr['units_before']==tr['units_after'];continue
  q=D(tr['quantity']);px=D(tr['execution']);mid=(D(tr['observed_bid'])+D(tr['observed_ask']))/2;k=tr['cost_multiplier'];participation=D(tr['budget'])/D(tr['lagged_ADV']);sigma=D(tr['lagged_sigma'])
  spread=(D(tr['observed_ask'])-D(tr['observed_bid']))/2*k;slip=mid*D('.0002')*k;imp=mid*D('.5')*sigma*participation.sqrt()*k;theoretical=mid+(spread+slip+imp)*(1 if tr['side']=='buy' else -1)
  assert abs(theoretical-D(tr['theoretical_execution']))<D('1e-18')
  parts={'fee':q*px*D('.001')*k,'half_spread':q*spread,'slippage':q*slip,'impact':q*imp,'tick_rounding':q*abs(px-theoretical)}
  assert all(abs(v-D(tr['cost_parts'][key]))<D('1e-18') for key,v in parts.items())
  c,u=D(tr['cash_before']),D(tr['units_before']);ca,ua=D(tr['cash_after']),D(tr['units_after']);fee=parts['fee']
  assert ca==c-q*px-fee if tr['side']=='buy' else ca==c+q*px-fee
  assert ua==u+q if tr['side']=='buy' else ua==u-q
  assert ca>=0 and ua>=0 and abs(c+u*mid-(ca+ua*mid)-sum(parts.values()))<D('1e-18')
  fs=market['filters'][tr['asset']];assert q%D(fs['LOT_SIZE']['stepSize'])==0 and px%D(fs['PRICE_FILTER']['tickSize'])==0
 assert len({t['trade_id'] for t in report['trades']})==len(report['trades'])
 rebuilt,rr=advance(plan,before,market,folder.name);assert rebuilt==after and rr==report
 for c in report['configs'].values():
  for k,ss in c['scenes'].items():
   nav=sum(D(st['cash_usdt'])+D(st['units'])*(D(market['quotes'][a]['bid'])+D(market['quotes'][a]['ask']))/2 for a,st in ss['sleeves'].items());assert D(ss['NAV_usdt'])==nav
 print(dumps({'passed':True,'actual_portfolios':len(report['configs']),'cost_scenes':len(report['configs'])*3,'filled_virtual_orders':report['new_filled_virtual_orders'],'real_orders':0,'reproduced_exact_state_and_report':True,'receipt_times_and_raw_quotes_verified':True,'independent_money_identities_checked':True,'report_sha256':sha(folder/'report.json')}),end='')

def reserve_observations(plan,folder,before):
 batch=[];start=utc();deadline=(dt(start)+timedelta(minutes=15)).isoformat().replace('+00:00','Z')
 for p in plan['portfolios']:
  sp={'name':'paper10_'+folder.name+'_'+p['id'],'kind':'strategy','family':'paper-live-portfolio-observation','market':'spot','universe':['BTC/USDT','ETH/USDT'],'timeframe':'1d','logic':{'signals':'Fixed asset-specific source rules in immutable plan SHA;latest closed UTC daily bar once,previous desired persists;no warmup fills','allocation':'Raw initial sleeve weights times2000USDT,independent cash/coin accounts,no normalization/transfers/rebalance','execution':plan['execution'],'observation':'First valid public quotes after reserve and before fixed capture deadline;actual timestamp retained,never selected from returns. Outcome is cumulative state plus this actual observation;short-window rejection never resets account.'},'parameters':{'owner_automation_id':'btc-eth-2','portfolio_id':p['id'],'source_fingerprint':p['source_fingerprint'],'plan_sha256':plan['_sha256'],'raw_weights':[c['weight'] for c in p['components']],'initial_capital_usdt':2000,'state_before_sha256':digest(before),'observation_id':folder.name,'capture_not_before_utc':start,'capture_deadline_utc':deadline,'actual_cutoff_policy':'Actual quote-snapshot evaluation time within this predeclared capture window;not a backfilled historical timestamp','cost_multipliers':[1,2,3]}}
  path=folder/'specs'/(p['id']+'.json');write_once(path,sp);fp=registry.fingerprint(sp)
  x=subprocess.run([sys.executable,'research/automation/registry.py','reserve',str(path.relative_to(R))],cwd=R,capture_output=True,text=True)
  with (folder/'reserve.log').open('a') as log:log.write(p['id']+' '+str(x.returncode)+' '+x.stdout.strip()+'\n'+x.stderr)
  if x.returncode:raise RuntimeError('Reservation failed before evaluation: '+p['id']+' '+x.stdout)
  batch.append({'name':p['id'],'fingerprint':fp,'spec':str(path.relative_to(R))})
  write_once(folder/'batch.partial.json',batch) if not (folder/'batch.partial.json').exists() else atomic(folder/'batch.partial.json',batch)
 write_once(folder/'batch.json',batch);return batch

def finish_batch(folder,report):
 batch=json.loads((folder/'batch.json').read_text());records=registry.read_records(R/'research/automation/registry.jsonl')
 for b in batch:
  status=report['configs'][b['name']]['status'];rec=records[b['fingerprint']]
  if rec['status']!='reserved':assert rec.get('report_sha256')==sha(folder/'report.json') and rec['status']==status;continue
  x=subprocess.run([sys.executable,'research/automation/registry.py','finish',b['spec'],status,str((folder/'report.json').relative_to(R))],cwd=R,capture_output=True,text=True)
  with (folder/'finish.log').open('a') as f:f.write(b['name']+' '+status+' '+str(x.returncode)+' '+x.stdout.strip()+'\n'+x.stderr)
  if x.returncode:raise RuntimeError('Finish failed: '+x.stdout+x.stderr)

def promote(folder):
 after=json.loads((folder/'state_after.json').read_text());before=json.loads((folder/'state_before.json').read_text());current=json.loads((T/'state.json').read_text()) if (T/'state.json').exists() else None
 if current==after:return
 if current!=before:raise ValueError('State continuity conflict;do not reset or overwrite')
 atomic(T/'state.json',after)

def recover():
 for folder in sorted((T/'observations').glob('*')) if (T/'observations').exists() else []:
  if (folder/'complete.json').exists():
   current=json.loads((T/'state.json').read_text()) if (T/'state.json').exists() else None;after=json.loads((folder/'state_after.json').read_text());before=json.loads((folder/'state_before.json').read_text())
   if current==before and (current is None or current.get('last_observation_id')!=folder.name):promote(folder)
   continue
  if not (folder/'batch.json').exists():continue
  if (folder/'report.json').exists() and (folder/'state_after.json').exists():
   report=json.loads((folder/'report.json').read_text());write_once(folder/'trade_ledger.json',report['trades']);document(folder,report);audit_observation(folder);finish_batch(folder,report);write_once(folder/'complete.json',{'report_sha256':sha(folder/'report.json'),'state_after_sha256':sha(folder/'state_after.json')});promote(folder)
  else:
   existing=json.loads((folder/'report.json').read_text()) if (folder/'report.json').exists() else None
   if existing and existing.get('mode')=='blocked':finish_batch(folder,existing);continue
   blocked={'mode':'blocked','observation_id':folder.name,'configs':{b['name']:{'status':'blocked','reason':'Interrupted before a complete actual evaluation/report;do not execute old captured quotes'} for b in json.loads((folder/'batch.json').read_text())},'real_orders':0};write_once(folder/'report.json',blocked);finish_batch(folder,blocked)

 # The current account must be exactly the last completed journal, never a reset/new cash account.
 completed=sorted((T/'observations').glob('*/complete.json')) if (T/'observations').exists() else []
 if completed:
  expected=json.loads((completed[-1].parent/'state_after.json').read_text())
  if not (T/'state.json').exists() or json.loads((T/'state.json').read_text())!=expected:raise ValueError('Current state does not match latest completed journal')

def document(folder,report):
 lines=['# 十策略实盘行情＋模拟资金：'+folder.name,'', '真实Binance现货公开买卖报价；每组主账户2000USDT，2x/3x为独立成本压力副本；没有真实下单。','',f"账户起点UTC {report['cohort_started_at_utc']}；本轮观察UTC {report['observed_at_utc']}。实际观察次数见state_after.json。本轮虚拟成交{report['new_filled_virtual_orders']}笔，真实订单0笔。历史日线仅用于指标暖机，未产生开始之前的交易。",'', '|账户|技术指标与参数|BTC/ETH原始比例|主账户净收益%|主账户总盈亏USDT|主账户采样回撤%|1x/2x/3x净收益%|累计主账户成交数|主账户累计成本USDT|主账户持仓|','|---|---|---|---|---|---|---|---|---|---|']
 for name,c in sorted(report['configs'].items(),key=lambda item:-item[1]['scenes']['1']['net_return_pct']):
  z=c['scenes']['1'];positions=', '.join(a+':'+st['units'] for a,st in z['sleeves'].items());weights='/'.join(f'{100*w:g}%' for w in c['raw_weights']);returns='/'.join(f"{c['scenes'][k]['net_return_pct']:.6f}" for k in ('1','2','3'))
  lines.append(f"|{name}|{c['label']}|{weights}|{z['net_return_pct']:.6f}|{z['net_PnL_usdt']}|{z['observed_sample_max_drawdown_pct']:.6f}|{returns}|{z['executions']}|{z['cost_usdt']}|{positions}|")
 lines+=['', '净收益含未实现盈亏；费用/点差/滑点/成交量冲击/取整分别保存。回撤仅来自本次及后续实际报价快照采样，不是分钟或逐tick最大回撤。手续费按默认10bp/侧，无真实账户费率校准；即刻全额IOC为虚拟模型假设。', '', '当前不足180天与6个30天窗口；登记rejected仅表示这段实际观察不具长期资格，账户保持连续、不淘汰或重启。固定参数敏感性只引用历史来源，不用前向观察改参数/择优换组。', '', f"覆盖缺口数{len(report['coverage_gaps'])}；延迟日线决策与实际报价时间完整保存。行情不可用或机器离线时不倒填交易。旧回测收益及原SMA延迟shadow结果均未计入本账本。", '', f"离线重放：`.venv/bin/python research/paper10/run.py --reproduce {folder.name}`；实际数据审计：`.venv/bin/python research/paper10/check.py {folder.relative_to(R)}`。所有失败、零交易和负收益均保留。"]
 write_once(folder/'result.md','\n'.join(lines))


def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--reproduce');ap.add_argument('--hold-lock',action='store_true');args=ap.parse_args()
 if args.reproduce:audit_observation(T/'observations'/args.reproduce);return
 lock=R/'research/automation/branch.lock'
 with lock.open('a') as f:
  fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB);plan=ensure_plan();recover();before=json.loads((T/'state.json').read_text()) if (T/'state.json').exists() else None
  folder=T/'observations'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ');folder.mkdir(parents=True);write_once(folder/'state_before.json',before)
  batch=reserve_observations(plan,folder,before)
  try:market=capture(plan,folder)
  except Exception as error:
   blocked={'mode':'blocked','observation_id':folder.name,'configs':{b['name']:{'status':'blocked','reason':type(error).__name__+': '+str(error)} for b in batch},'real_orders':0};write_once(folder/'report.json',blocked);finish_batch(folder,blocked);raise
  assert all(dt(market['evaluated_at_utc'])<=dt(json.loads((R/b['spec']).read_text())['parameters']['capture_deadline_utc']) for b in batch)
  after,report=advance(plan,before,market,folder.name);write_once(folder/'state_after.json',after);write_once(folder/'report.json',report)
  write_once(folder/'trade_ledger.json',report['trades']);document(folder,report)
  with (folder/'audit.log').open('w') as out:
   x=subprocess.run([sys.executable,str(T/'check.py'),str(folder)],cwd=R,stdout=out,stderr=subprocess.STDOUT)
  if x.returncode:raise RuntimeError('Actual observation audit failed;state not promoted;see '+str(folder/'audit.log'))
  finish_batch(folder,report);write_once(folder/'complete.json',{'report_sha256':sha(folder/'report.json'),'state_after_sha256':sha(folder/'state_after.json')});promote(folder)
  print(dumps({'started':True,'observation':str(folder.relative_to(R)),'cohort_started_at_utc':after['cohort_started_at_utc'],'portfolios':len(after['portfolios']),'cost_scenes':30,'filled_virtual_orders':report['new_filled_virtual_orders'],'real_orders':0,'state_sha256':sha(T/'state.json'),'report_sha256':sha(folder/'report.json'),'lock_held':args.hold_lock}),flush=True)
  if args.hold_lock:
   print('PAPER10_READY_LOCK_HELD: publish only paper10 evidence and registry;send release to finish.',flush=True)
   for line in sys.stdin:
    if line.strip()=='release':break
if __name__=='__main__':main()
