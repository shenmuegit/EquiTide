"""Incremental closed-data observer for the immutable 070542 candidate.

Pure transition functions: no HTTP, filesystem mutation, orders, or registry access.
Synthetic checks of this module are engineering checks, never financial trials.
"""
import copy,hashlib,importlib.util,json,math,statistics,struct
from datetime import datetime,timezone
from decimal import Decimal as D,ROUND_FLOOR
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
MIN=60_000_000_000;HOUR=60*MIN;DAY=24*HOUR;MS=1_000_000
ns=lambda s:int(datetime.fromisoformat(s.replace('Z','+00:00')).timestamp())*1_000_000_000
START=ns('2026-11-01T00:01:00Z');END=ns('2027-04-30T00:01:00Z');WARMUP=ns('2026-09-29T00:00:00Z')
PLAN=Path(__file__).resolve().parent/'plan.json'
FREEZE=Path(__file__).resolve().parent/'binding.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
canonical=lambda x:json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()

def load(path,name):
 s=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
TREND=load('research/experiments/20261025T065405Z/engine.py','candidate_trend_rules')
GATE=load('research/experiments/20261025T185633Z/engine.py','candidate_gate_rules')

def ready_status(now_ns):
 return {'status':'waiting_for_planned_start' if now_ns<START else 'planned_interval_ended' if now_ns>END else 'eligible_for_validated_real_window','planned_start_utc':'2026-11-01T00:01:00Z','planned_end_exclusive_utc':'2027-04-30T00:01:00Z','account_created':False,'actual_observations_created':0,'observation_mode':'delayed closed-bar/funding replay, not live quote execution'}

def check_window(previous,cutoff,retrieved):
 assert START<cutoff<=END and cutoff%MIN==0,'outside planned interval or non-minute cutoff'
 assert retrieved>=cutoff+MIN,'execution reference bar must really be closed by retrieval'
 assert previous is None or previous['cutoff_ns']<cutoff,'no duplicate, rewind, or restart'
 return previous['cutoff_ns'] if previous else START

def bindings():
 seal=json.loads(FREEZE.read_text());assert sha(PLAN)==seal['plan_sha256'];plan=json.loads(PLAN.read_text());assert ns(plan['time_boundaries']['planned_start_utc'])==START and ns(plan['time_boundaries']['planned_end_exclusive_utc'])==END and END-START==180*DAY
 for path,h in seal['code_and_source_sha256'].items():assert sha(ROOT/path)==h,path
 candidate=plan['original_candidate'];assert candidate['fingerprint']=='cd5df95d06288078d923a99ae210ab4cbe84ef03d32522b274a40d12120f9a37';assert sha(ROOT/candidate['spec'])==candidate['spec_sha256'] and sha(ROOT/candidate['historical_report'])==candidate['historical_report_sha256']
 sources={str(PLAN.relative_to(ROOT)):sha(PLAN),str(FREEZE.relative_to(ROOT)):sha(FREEZE)};meta={};caps={}
 for comp in plan['components']:
  a=comp['asset'];p=comp['parameters'];assert comp['weight']==1 and p['initial_capital_usdt']==(5000 if a=='BTC' else 15000);caps[a]=p['initial_capital_usdt'];assert sha(ROOT/comp['source_spec'])==comp['source_spec_sha256'];sources[comp['source_spec']]=comp['source_spec_sha256']
  if a=='BTC':assert (p['lookback_days'],p['return_hurdle'],p['exit_buffer_fraction'],p['fixed_entry_notional_usdt'])==(31,.04,.01,500)
  else:assert (p['trend_lookback_days'],p['lookback_days'],p['return_hurdle'],p['exit_buffer_fraction'],p['fixed_entry_notional_usdt'])==(28,4,.02,0,4500)
  path=next(x for x in p['input_hashes'] if x.endswith('perp_instrument_meta.parquet'));assert sha(ROOT/path)==p['input_hashes'][path];row=GATE.pl.read_parquet(ROOT/path).to_dicts()[0];assert row['contract_multiplier']==1;meta[a]={k:str(row[k]) for k in ['lot_size','tick_size','min_notional']}
 return {'plan_sha256':sha(PLAN),'original_candidate_fingerprint':candidate['fingerprint'],'sources_sha256':{**sources,**seal['code_and_source_sha256']},'metadata':meta,'capitals':caps,'rules':{'BTC':{'N':500,'L':31,'H':.04,'E':.01},'ETH':{'N':4500,'S':28,'L':4,'H':.02,'E':0}}}
def target_eth(values,i,current):
 from fractions import Fraction as F
 assert i-29>=0 and current in [-1,0,1];r=F(values[i-1])/F(values[i-5])-1;s=F(values[i-1])/F(values[i-29])-1;h=F('.02');base=-1 if r>h else 1 if r<-h else current if current==1 and r<0 or current==-1 and r>0 else 0;gate=(s>0)-(s<0);return base if base==gate else 0,str(r),str(s)

def closed_bars(raw,interval,retrieved):
 assert raw and isinstance(raw,list)
 out=[]
 for row in raw:
  assert isinstance(row,list) and len(row)>=12
  t=int(row[0])*MS;end=(int(row[6])+1)*MS
  assert t%interval==0 and end-t==interval and end<=retrieved,'unclosed or wrong timestamp units'
  o,h,l,c=[D(row[i]) for i in [1,2,3,4]];assert o>0 and l>0 and l<=min(o,c)<=max(o,c)<=h
  assert D(row[7])>=0
  out.append({'open_ns':t,'end_ns':end,'open':str(o),'high':str(h),'low':str(l),'close':str(c),'quote_volume':str(D(row[7])),'raw':row})
 assert all(b['open_ns']-a['open_ns']==interval for a,b in zip(out,out[1:])),'missing or duplicate bars'
 return out

def normalize(packet,previous,binding):
 cutoff=int(packet['cutoff_ns']);retrieved=int(packet['retrieved_ns']);lo=check_window(previous,cutoff,retrieved)
 assert packet['plan_sha256']==binding['plan_sha256']
 if previous:assert previous['plan_sha256']==binding['plan_sha256'] and previous['binding_sha256']==hashlib.sha256(canonical(binding)).hexdigest()
 assert set(packet['assets'])=={'BTC','ETH'}
 actions={};contexts={}
 def add(t,code,a,p):
  assert START<=t<=cutoff and (not previous or (t,code)>(previous['last_key'][0],previous['last_key'][1]));key=(t,code)
  assert a not in actions.setdefault(key,{});actions[key][a]=p
 for a,raw in packet['assets'].items():
  assert {k:D(v) for k,v in raw['metadata'].items()}=={k:D(v) for k,v in binding['metadata'][a].items()},'contract filters changed'
  bars=closed_bars(raw['minutes'],MIN,retrieved);hours=closed_bars(raw['hours'],HOUR,retrieved);by={b['open_ns']:b for b in bars}
  ctx=copy.deepcopy(previous['context'][a]) if previous else {'daily':[],'partial':None,'last_bar':None,'last_funding':None,'last_hour':None,'reference_bar':None}
  expected=lo-MIN if previous else WARMUP
  assert bars[0]['open_ns']==expected and bars[-1]['open_ns']==cutoff,'minute coverage lacks overlap/reference'
  if previous:
   assert bars[0]['raw']==ctx['last_bar'],'minute overlap revised'
   if ctx['reference_bar'] is not None:assert by[lo]['raw']==ctx['reference_bar'],'execution reference revised'
  processed=[b for b in bars if b['end_ns']<=cutoff and (not previous or b['end_ns']>lo)]
  for b in processed:
   d=b['open_ns']//DAY
   partial=ctx['partial']
   if partial is None:assert b['open_ns']%DAY==0;partial={'day':d,'count':0,'quote_volume':'0'}
   assert partial['day']==d
   partial['count']+=1;partial['quote_volume']=str(D(partial['quote_volume'])+D(b['quote_volume']));partial['close']=b['close']
   if b['end_ns']%DAY==0:
    assert partial['count']==1440
    ctx['daily'].append(copy.deepcopy(partial));ctx['daily']=ctx['daily'][-64:];ctx['partial']=None
   else:ctx['partial']=partial
   t=b['end_ns']
   if t>lo:add(t,1,a,{'price':b['close']})
   if t>=START and t%DAY==MIN and t<END and (not previous or t>lo):
    daily=ctx['daily'];assert len(daily)>=33 and daily[-1]['day']==t//DAY-1 and all(y['day']-x['day']==1 for x,y in zip(daily,daily[1:]))
    closes=[D(x['close']) for x in daily];adv=D(str(statistics.mean(float(x['quote_volume']) for x in daily[-20:])))
    vol=D(str(statistics.stdev([math.log(float(closes[j])/float(closes[j-1])) for j in range(len(closes)-20,len(closes))])))
    assert adv>0
    payload={'price':by[t]['open'],'closes':[str(x) for x in closes],'ADV':str(adv),'sigma':str(vol)}
    for code in [5,6,7]:add(t,code,a,payload)
  ctx['last_bar']=by[cutoff-MIN]['raw'];ctx['reference_bar']=by[cutoff]['raw']
  if not previous:
   assert by[START]['open_ns']==START;add(START,0,a,{'price':by[START]['open']})
  hstart=(lo//HOUR)*HOUR-HOUR
  assert hours[0]['open_ns']==hstart and hours[-1]['end_ns']==cutoff//HOUR*HOUR,'hour coverage'
  if previous and ctx['last_hour'] is not None:assert hours[0]['raw']==ctx['last_hour'],'hour overlap revised'
  for b in hours:
   if lo<b['end_ns']<=cutoff:add(b['end_ns'],2,a,{'price':b['close'],'hour_open_ns':b['open_ns'],'high':b['high'],'low':b['low']})
  ctx['last_hour']=hours[-1]['raw']
  funds=raw['funding'];assert isinstance(funds,list) and funds
  fts=[int(f['fundingTime'])*MS for f in funds];assert fts==sorted(set(fts))
  assert all(f.get('rateType','Regular')=='Regular' and f['symbol']==a+'USDT' and D(f['markPrice'])>0 for f in funds)
  assert all(0<=t%(8*HOUR)<=2_000_000_000 for t in fts),'unplanned funding cadence'
  if previous:assert funds[0]==ctx['last_funding'],'funding overlap revised'
  expected_slots=set(range((lo//(8*HOUR)+1)*8*HOUR,cutoff-2_000_000_000+1,8*HOUR))
  assert expected_slots<={t//(8*HOUR)*(8*HOUR) for t in fts},'missing settled funding'
  assert all(abs((y-x)-8*HOUR)<=2_000_000_000 for x,y in zip(fts,fts[1:]))
  assert fts[0]<=lo and fts[-1]<=retrieved
  for f,t in zip(funds,fts):
   if lo<t<=cutoff:
    p={'price':f['markPrice'],'rate':f['fundingRate'],'actual_settlement_ns':t,'raw':f}
    add(t,3,a,p);add(t,4,a,p)
  ctx['last_funding']=next(f for f,t in reversed(list(zip(funds,fts))) if t<=cutoff)
  if cutoff==END:
   payload={'price':by[END]['open'],'closes':[x['close'] for x in ctx['daily']],'ADV':str(statistics.mean(float(x['quote_volume']) for x in ctx['daily'][-20:]))}
   closes=[D(x) for x in payload['closes']];payload['sigma']=str(statistics.stdev([math.log(float(closes[j])/float(closes[j-1])) for j in range(len(closes)-20,len(closes))]))
   for code in [8,9]:add(END,code,a,payload)
  contexts[a]=ctx
 return lo,cutoff,actions,contexts

def new_state(binding):
 def book(a):return {'cash':str(binding['capitals'][a]),'signed_units':'0','entry_price':'0','entry_reference':'0'}
 return {'schema_version':1,'plan_sha256':binding['plan_sha256'],'binding_sha256':hashlib.sha256(canonical(binding)).hexdigest(),'cutoff_ns':START,'last_key':[START,-1],'last_prices':{},'books':{a:{str(k):book(a) for k in [1,2,3]} for a in ['BTC','ETH']},'nav_chain_sha256':'0'*64,'nav_points':0,'daily':{a:{str(k):[] for k in [1,2,3]} for a in ['BTC','ETH','COMBO']},'counters':{a:{str(k):{'executions':0,'round_trips':0,'rejected_orders':0,'cash_violations':0,'margin_proxy_violations':0,'margin_checks':0,'funding_settlements':0,'cost_usdt':'0','funding_usdt':'0','gross_reference_price_PnL_usdt':'0'} for k in [1,2,3]} for a in ['BTC','ETH']},'risk':{a:{str(k):[{'t':START,'state':book(a)}] for k in [1,2,3]} for a in ['BTC','ETH']}}

def transition(previous,actions,cutoff,binding,contexts=None):
 """Validated event transitions; shared keys sum native NAV, never average returns."""
 state=copy.deepcopy(previous) if previous else new_state(binding);journal=[];nav=[];wanted={}
 assert state['plan_sha256']==binding['plan_sha256'] and state['binding_sha256']==hashlib.sha256(canonical(binding)).hexdigest()
 def trade(a,k,p,change,opening,t,code):
  before=state['books'][a][k];after,record=GATE.trade(before,D(change),D(p['price']),D(p['ADV']),D(p['sigma']),binding['metadata'][a],int(k),opening)
  state['books'][a][k]=after;record.update(asset=a,cost_multiplier=int(k),timestamp_ns=t,event_code=code,terminal=code==9);journal.append({'kind':'trade',**record});counts=state['counters'][a][k]
  if record['status']=='filled':
   counts['executions']+=1;counts['round_trips']+=int(not opening)
   for out,key in [('cost_usdt','cost_usdt'),('gross_reference_price_PnL_usdt','reference_price_PnL_usdt')]:counts[out]=str(D(counts[out])+D(record[key]))
  else:counts['rejected_orders']+=1
 def risk_state(a,k,t,before):
  after=state['books'][a][k]
  if before!=after:state['risk'][a][k].append({'t':t,'state':copy.deepcopy(after)})
 for (t,code),assets in sorted(actions.items()):
  assert (t,code)>tuple(state['last_key']) and START<=t<=cutoff<=END
  for a,p in sorted(assets.items()):
   state['last_prices'][a]=float(p['price'])
   for k,book in state['books'][a].items():
    before=copy.deepcopy(book);q=D(book['signed_units']);counts=state['counters'][a][k]
    if code==4:
     base,amount=GATE.funding_amount(q,D(p['price']),D(p['rate']),int(k));book['cash']=str(D(book['cash'])+amount) if amount else book['cash'];counts['funding_settlements']+=1;counts['funding_usdt']=str(D(counts['funding_usdt'])+amount)
     journal.append({'kind':'funding','asset':a,'cost_multiplier':int(k),'timestamp_ns':t,'event_code':code,'signed_units':str(q),'mark_price':p['price'],'rate':p['rate'],'base_amount_usdt':str(base),'amount_usdt':str(amount),'cash_before':before['cash'],'cash_after':book['cash']})
    elif code==6:
     c=[D(x) for x in p['closes']];direction=1 if q>0 else -1 if q<0 else 0;rule=binding['rules'][a]
     result=TREND.target(c,len(c),31,.04,direction,.01) if a=='BTC' else target_eth(c,len(c),direction)
     wanted[a,k]=result[0];journal.append({'kind':'decision','asset':a,'cost_multiplier':int(k),'timestamp_ns':t,'event_code':code,'wanted':result[0],'returns_exact':list(result[1:]),'prior_complete_close':p['closes'][-1],'ADV':p['ADV'],'sigma':p['sigma']})
     if q and direction!=result[0]:trade(a,k,p,-q,False,t,code)
    elif code==7:
     assert (a,k) in wanted
     if wanted[a,k] and D(state['books'][a][k]['signed_units'])==0:
      lot=D(binding['metadata'][a]['lot_size']);q2=(D(binding['rules'][a]['N'])/D(p['closes'][-1])/lot).to_integral_value(rounding=ROUND_FLOOR)*lot
      assert q2>0;trade(a,k,p,wanted[a,k]*q2,True,t,code)
    elif code==9:
     assert t==END
     if q:trade(a,k,p,-q,False,t,code)
    elif code==2:
     stack=state['risk'][a][k];op=p['hour_open_ns'];low,high=D(p['low']),D(p['high'])
     if op>=START:
      for i,item in enumerate(stack):
       end=stack[i+1]['t'] if i+1<len(stack) else t
       b=item['state'];units=D(b['signed_units'])
       if units and item['t']<t and end>op and end>item['t']:
        adverse=low if units>0 else high;cushion=D(b['cash'])+units*(adverse-D(b['entry_price']))-D('.01')*abs(units)*adverse
        counts['margin_checks']+=1;counts['margin_proxy_violations']+=int(cushion<=0)
     state['risk'][a][k]=[{'t':t,'state':copy.deepcopy(state['books'][a][k])}]
    risk_state(a,k,t,before);counts['cash_violations']+=int(D(state['books'][a][k]['cash'])<0)
  assert set(state['last_prices'])=={'BTC','ETH'},'initial assets must share timestamp/code'
  values={a:{k:float(b['cash'])+float(b['signed_units'])*(state['last_prices'][a]-float(b['entry_price'])) for k,b in books.items()} for a,books in state['books'].items()}
  values['COMBO']={k:values['BTC'][k]+values['ETH'][k] for k in ['1','2','3']};assert all(math.isfinite(v) and v>0 for z in values.values() for v in z.values())
  row={'timestamp_ns':t,'event_code':code,'NAV':values};nav.append(row);state['nav_chain_sha256']=hashlib.sha256(bytes.fromhex(state['nav_chain_sha256'])+canonical(row)).hexdigest();state['nav_points']+=1;state['last_key']=[t,code]
  if code in [0,5,9]:
   for a in values:
    for k,v in values[a].items():
     daily=state['daily'][a][k]
     if code==5 and t==START:continue
     daily.append({'timestamp_ns':t,'equity_usdt':v})
 state['cutoff_ns']=cutoff
 if contexts is not None:state['context']=contexts
 assert nav and nav[-1]['timestamp_ns']==cutoff,'last closed minute must reach cutoff'
 if cutoff==END:assert all(D(b['signed_units'])==0 for x in state['books'].values() for b in x.values())
 return state,{'NAV':nav,'journal':journal,'from_exclusive_ns':previous['cutoff_ns'] if previous else START,'cutoff_ns':cutoff,'previous_nav_chain_sha256':previous['nav_chain_sha256'] if previous else '0'*64,'nav_chain_sha256':state['nav_chain_sha256']}

def advance(previous,packet,binding):
 lo,cut,actions,contexts=normalize(packet,previous,binding)
 return transition(previous,actions,cut,binding,contexts)
