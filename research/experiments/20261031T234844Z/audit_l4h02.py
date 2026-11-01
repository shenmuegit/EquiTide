"""Independent first-window raw-data, causal signal, native ledger and NAV audit.

No call to frozen normalize, target, trade, transition or advance. No writes to
accounts, reports, packets or registry; only this independent verification file.
"""
import copy,gzip,hashlib,json,math,statistics,urllib.parse
from collections import defaultdict
from decimal import Decimal as D,ROUND_FLOOR,ROUND_CEILING
from fractions import Fraction as F
from datetime import datetime
import numpy as np
from common import ROOT,R,sha,put,reg,MIN,HOUR,DAY
rd=lambda p:json.loads(p.read_text());gz=lambda p:json.loads(gzip.decompress(p.read_bytes()));canonical=lambda x:json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def near(a,b,tol=1e-11):assert abs(float(a)-float(b))<=tol*max(1,abs(float(a)),abs(float(b))),(a,b)
def numeric(b):return {k:D(v) for k,v in b.items()}
P=ROOT/'research/experiments/20261031T174613Z/prospective_l4';w=R/'l4h02_observation';ip=rd(R/'future_integration_plan.json');plan=rd(P/'plan.json');seal=rd(P/'binding.json');point=rd(ROOT/'research/automation/l4h02_forward_latest.json');state=rd(w/'state.json');report=rd(w/'report.json');delta=gz(w/'delta.json.gz');im=rd(w/'input_manifest.json');complete=rd(w/'complete.json');packet=gz(ROOT/im['packet'])
start=1793491260000000000;cut=ip['first_cutoff_ns'];assert start==ip['planned_start_ns'] and cut==1793491800000000000 and cut-start==9*MIN and point['cutoff_ns']==state['cutoff_ns']==report['cutoff_ns']==packet['cutoff_ns']==cut and point['previous_pointer'] is None
assert sha(P/'plan.json')==seal['plan_sha256']==point['plan_sha256']==state['plan_sha256']==report['plan_sha256']==packet['plan_sha256']=='08e650a257ec9a0dbe27fe545f796a061a8538c05b8f9512821dc71a9cce3462'
for path,h in ip['code_and_frozen_source_sha256'].items():assert sha(ROOT/path)==h,path
pre=rd(R/'future_prestart_status.json')['status'];assert state['binding_sha256']==hashlib.sha256(canonical(pre['binding'])).hexdigest() and len(plan['components'])==2 and all(x['weight']==1 for x in plan['components'])
assert complete['previous_pointer_sha256'] is None and not(w/'previous_pointer.json').exists()
for key,file in [('state','state.json'),('report','report.json'),('delta','delta.json.gz'),('complete','complete.json')]:assert point[key]==str((w/file).relative_to(ROOT)) and point[key+'_sha256']==sha(w/file)
assert complete['state_sha256']==sha(w/'state.json') and complete['report_sha256']==sha(w/'report.json') and complete['delta_sha256']==sha(w/'delta.json.gz') and im['sha256']==sha(ROOT/im['packet'])
rawby=defaultdict(list);exchange=server=None;http=0
for item in im['provenance']:
 assert item.get('http_status')==200 and item.get('curl_exit_code')==0 and sha(ROOT/item['raw'])==item['sha256'];raw=gzip.decompress((ROOT/item['raw']).read_bytes());assert len(raw)==item['bytes'];doc=json.loads(raw);u=urllib.parse.urlparse(item['url']);q=urllib.parse.parse_qs(u.query);assert u.scheme=='https' and u.netloc=='fapi.binance.com';http+=1
 if u.path=='/fapi/v1/exchangeInfo':exchange=doc
 elif u.path=='/fapi/v1/time':server=doc
 else:assert u.path in ['/fapi/v1/klines','/fapi/v1/markPriceKlines','/fapi/v1/fundingRate'];rawby[q['symbol'][0][:-4],u.path].extend(doc)
assert exchange and server and cut+MIN<=packet['retrieved_ns']<=server['serverTime']*1_000_000
symbols={x['symbol']:x for x in exchange['symbols']};caps={c['asset']:c['parameters']['initial_capital_usdt'] for c in plan['components']};assert caps=={'BTC':5000.0,'ETH':15000};meta={};contexts={};actions={};daily_by={};records=reg.read_records(ROOT/'research/automation/registry.jsonl');events=reg.read_events(ROOT/'research/automation/registry.jsonl')
def add(t,code,a,p):assert a not in actions.setdefault((t,code),{});actions[t,code][a]=p
for a in ['BTC','ETH']:
 ar=packet['assets'][a];mins=ar['minutes'];hours=ar['hours'];funds=ar['funding'];assert rawby[a,'/fapi/v1/klines']==mins and rawby[a,'/fapi/v1/markPriceKlines']==hours and rawby[a,'/fapi/v1/fundingRate']==funds
 sy=symbols[a+'USDT'];fs={x['filterType']:x for x in sy['filters']};meta[a]={'lot_size':fs['LOT_SIZE']['stepSize'],'tick_size':fs['PRICE_FILTER']['tickSize'],'min_notional':fs['MIN_NOTIONAL']['notional']};assert numeric(meta[a])==numeric(ar['metadata'])==numeric(pre['binding']['metadata'][a])
 by={};daily=[];partial=None
 for i,b in enumerate(mins):
  t=int(b[0])*1_000_000;end=(int(b[6])+1)*1_000_000;o,h,l,cl=[D(b[j]) for j in [1,2,3,4]];assert end-t==MIN and end<=packet['retrieved_ns'] and t%MIN==0 and o>0 and l>0 and l<=min(o,cl)<=max(o,cl)<=h and D(b[7])>=0
  if i:assert t==int(mins[i-1][0])*1_000_000+MIN
  by[t]=b
  if end>cut:continue
  if partial is None:assert t%DAY==0;partial={'day':t//DAY,'count':0,'quote_volume':'0'}
  assert partial['day']==t//DAY;partial['count']+=1;partial['quote_volume']=str(D(partial['quote_volume'])+D(b[7]));partial['close']=str(cl)
  if end%DAY==0:assert partial['count']==1440;daily.append(copy.deepcopy(partial));partial=None
  if end>start:add(end,1,a,{'price':str(cl)})
  if end==start:
   closes=[D(x['close']) for x in daily];adv=D(str(statistics.mean(float(x['quote_volume']) for x in daily[-20:])));sig=D(str(statistics.stdev([math.log(float(closes[j])/float(closes[j-1])) for j in range(len(closes)-20,len(closes))])));payload={'price':str(D(next(x for x in mins if int(x[0])*1_000_000==start)[1])),'closes':closes,'ADV':adv,'sigma':sig}
   for code in [5,6,7]:add(start,code,a,payload)
 assert int(mins[0][0])*1_000_000==1790640000000000000 and int(mins[-1][0])*1_000_000==cut and len(daily)==33
 ctx=state['context'][a];assert ctx['daily']==daily[-64:] and ctx['partial']==partial and ctx['last_bar']==by[cut-MIN] and ctx['reference_bar']==by[cut];daily_by[a]=daily
 add(start,0,a,{'price':str(D(by[start][1]))})
 assert int(hours[0][0])*1_000_000==start//HOUR*HOUR-HOUR and (int(hours[-1][6])+1)*1_000_000==cut//HOUR*HOUR
 for i,b in enumerate(hours):
  t=int(b[0])*1_000_000;end=(int(b[6])+1)*1_000_000;assert end-t==HOUR and end<=packet['retrieved_ns'] and (not i or t==int(hours[i-1][0])*1_000_000+HOUR)
  if start<end<=cut:add(end,2,a,{'price':b[4],'low':b[3],'high':b[2],'hour_open_ns':t})
 assert ctx['last_hour']==hours[-1]
 fts=[int(f['fundingTime'])*1_000_000 for f in funds];assert fts and fts==sorted(set(fts)) and fts[0]<=start and all(0<=t%(8*HOUR)<=2_000_000_000 for t in fts) and all(abs(y-x-8*HOUR)<=2_000_000_000 for x,y in zip(fts,fts[1:]));assert ctx['last_funding']==next(f for f,t in reversed(list(zip(funds,fts))) if t<=cut)
 for f,t in zip(funds,fts):
  assert f['symbol']==a+'USDT' and D(f['markPrice'])>0 and t<=packet['retrieved_ns']
  if start<t<=cut:
   for code in [3,4]:add(t,code,a,{'price':f['markPrice'],'rate':f['fundingRate']})
assert sorted(actions)==[(x['timestamp_ns'],x['event_code']) for x in delta['NAV']] and len(actions)==13 and not any(code==2 for t,code in actions)
books={a:{k:{'cash':str(caps[a]),'signed_units':'0','entry_price':'0','entry_reference':'0'} for k in ['1','2','3']} for a in ['BTC','ETH']};risk={a:{k:[{'t':start,'state':copy.deepcopy(b)}] for k,b in bb.items()} for a,bb in books.items()};counters={a:{k:{'executions':0,'round_trips':0,'rejected_orders':0,'cash_violations':0,'margin_proxy_violations':0,'margin_checks':0,'funding_settlements':0,'cost_usdt':'0','funding_usdt':'0','gross_reference_price_PnL_usdt':'0'} for k in ['1','2','3']} for a in books};journals=defaultdict(list)
for x in delta['journal']:journals[x['timestamp_ns'],x['event_code'],x['asset'],str(x['cost_multiplier'])].append(x)
prices={};wanted={};chain='0'*64;checks={'decisions':0,'fills':0,'funding':0};used=0
for row,(t,code) in zip(delta['NAV'],sorted(actions)):
 for a,p in actions[t,code].items():
  prices[a]=float(p['price'])
  for k,b in books[a].items():
   before=copy.deepcopy(b);z=counters[a][k];q=D(b['signed_units']);es=journals[t,code,a,k]
   if code==6:
    cls=p['closes'];i=len(cls);r=F(cls[-1])/F(cls[i-32] if a=='BTC' else cls[i-5])-1;current=(q>0)-(q<0)
    if a=='BTC':h=F('.04');e=F('.01');target=1 if r>h else -1 if r<-h else 1 if current==1 and r>-e else -1 if current==-1 and r<e else 0;returns=[str(r)]
    else:
     slow=F(cls[-1])/F(cls[i-29])-1;h=F('.02');base=-1 if r>h else 1 if r<-h else current if current==1 and r<0 or current==-1 and r>0 else 0;gate=(slow>0)-(slow<0);target=base if base==gate else 0;returns=[str(r),str(slow)]
    assert len(es)==1 and es[0]['kind']=='decision';x=es[0];assert x['wanted']==target and x['returns_exact']==returns and D(x['prior_complete_close'])==cls[-1] and D(x['ADV'])==p['ADV'] and D(x['sigma'])==p['sigma'];wanted[a,k]=target;checks['decisions']+=1;used+=1;assert q==0
   elif code==7 and wanted[a,k]:
    assert len(es)==1;tr=es[0];N=D(500 if a=='BTC' else 4500);lot=D(meta[a]['lot_size']);change=D(wanted[a,k])*(N/p['closes'][-1]/lot).to_integral_value(rounding=ROUND_FLOOR)*lot;qty=abs(change);ref=D(p['price']);part=qty*ref/p['ADV'];fee=D('.0005')*int(k);spread=D('.0001')*int(k);slip=D('.0002')*int(k);impact=D('.5')*p['sigma']*part.sqrt()*int(k);theory=ref*(1+(spread+slip+impact)*(1 if change>0 else -1));tick=D(meta[a]['tick_size']);px=(theory/tick).to_integral_value(rounding=ROUND_CEILING if change>0 else ROUND_FLOOR)*tick;parts={'fee':qty*px*fee,'half_spread':qty*ref*spread,'slippage':qty*ref*slip,'impact':qty*ref*impact,'tick_rounding':qty*abs(px-theory)};assert part<=D('.001') and qty%lot==0 and qty*px>=D(meta[a]['min_notional']) and qty*px<=D(b['cash'])-parts['fee']
    assert tr['kind']=='trade' and tr['opening'] and tr['status']=='filled' and numeric(tr['state_before'])==numeric(b) and D(tr['change_signed_units'])==change and D(tr['execution'])==px and D(tr['theoretical_execution'])==theory and D(tr['participation'])==part and D(tr['lagged_ADV'])==p['ADV'] and D(tr['lagged_sigma'])==p['sigma'] and all(D(tr['cost_parts'][n])==v for n,v in parts.items()) and D(tr['cost_usdt'])==sum(parts.values()) and D(tr['reference_price_PnL_usdt'])==D(tr['realized_price_PnL_usdt'])==0
    b.update(cash=str(D(b['cash'])-parts['fee']),signed_units=str(change),entry_price=str(px),entry_reference=str(ref));assert numeric(tr['state_after'])==numeric(b);z['executions']+=1;z['cost_usdt']=str(D(z['cost_usdt'])+sum(parts.values()));checks['fills']+=1;used+=1
   elif code==4:
    assert len(es)==1;x=es[0];base=-q*D(p['price'])*D(p['rate']);amount=base*int(k) if base<0 else base;assert x['kind']=='funding' and D(x['base_amount_usdt'])==base and D(x['amount_usdt'])==amount and D(x['cash_before'])==D(b['cash']);b['cash']=str(D(b['cash'])+amount) if amount else b['cash'];assert D(x['cash_after'])==D(b['cash']);z['funding_settlements']+=1;z['funding_usdt']=str(D(z['funding_usdt'])+amount);checks['funding']+=1;used+=1
   else:assert not es
   if before!=b:risk[a][k].append({'t':t,'state':copy.deepcopy(b)})
   z['cash_violations']+=int(D(b['cash'])<0)
 vals={a:{k:float(b['cash'])+float(b['signed_units'])*(prices[a]-float(b['entry_price'])) for k,b in bb.items()} for a,bb in books.items()};vals['COMBO']={k:vals['BTC'][k]+vals['ETH'][k] for k in ['1','2','3']};assert vals==row['NAV'];chain=hashlib.sha256(bytes.fromhex(chain)+canonical(row)).hexdigest()
assert used==len(delta['journal']) and checks['decisions']==6 and state['books']==books and state['counters']==counters and state['risk']==risk and state['last_prices']==prices and state['nav_points']==len(delta['NAV'])==13 and state['last_key']==[cut,1] and chain==state['nav_chain_sha256']==delta['nav_chain_sha256']==report['NAV_chain_sha256'] and delta['previous_nav_chain_sha256']=='0'*64
receipts=rd(w/'receipts.json');res=[x for x in receipts if x.get('command',[None,None])[1:2]==['reserve']];fin=[x for x in receipts if x.get('command',[None,None])[1:2]==['finish']];assert len(res)==len(fin)==3 and all(x['exit_code']==0 for x in res+fin)
for a in ['BTC','ETH','COMBO']:
 sp=rd(w/(a+'_spec.json'));fp=reg.fingerprint(sp);c=report['configs']['forward_snapshot_l4h02_'+a];rec=records[fp];ss=c['scenes'];one=ss['1'];three=ss['3'];expected={'full180days':False,'six_complete_folds':False,'five_positive_30day_folds':False,'all_cost_net_positive':all(x['net_return_pct']>0 for x in ss.values()),'whole_DD3_le25':three['max_drawdown_pct']<=25,'round_trips1_ge4':one['round_trips']>=4,'cost_safety_1x':one['gross_reference_PnL_to_execution_cost'] is not None and one['gross_reference_PnL_to_execution_cost']>=2.5,'no_cash_order_margin_violations':all(not any(z[f] for f in ['cash_violations','rejected_orders','margin_proxy_violations']) for z in ss.values()),'recent40_6of8':False,'recent40_all_cost_positive':False};assert c['criteria']==expected and c['failed_criteria']==[k for k,v in expected.items() if not v];assert rec['result_available'] and rec['status']==c['status']=='rejected' and rec['report_sha256']==sha(w/'report.json') and sp['parameters']['previous_state_sha256'] is None and c['partial_observation'] and c['does_not_cancel_or_reset_frozen_plan'] and not c['criteria']['full180days'] and not c['criteria']['six_complete_folds'];rs=[x for x in events if x['fingerprint']==fp and x['status']=='reserved'];assert len(rs)==1 and int(datetime.fromisoformat(rs[0]['recorded_at_utc'].replace('Z','+00:00')).timestamp()*1e9)<(w/'state.json').stat().st_mtime_ns
 for k,s in c['scenes'].items():
  cap=20000 if a=='COMBO' else caps[a];v=np.array([x['NAV'][a][k] for x in delta['NAV']]);assert v[0]==cap and s['NAV_points']==13 and s['NAV_sha256_f64le']==hashlib.sha256(v.astype('<f8').tobytes()).hexdigest();near(s['net_return_pct'],100*(v[-1]/cap-1));near(s['max_drawdown_pct'],100*max(1-v/np.maximum.accumulate(v)));assert s['sharpe_365'] is None and s['folds']==[] and s['recent40'] is None and s['daily_equity_usdt']==[{'timestamp_ns':start,'equity_usdt':float(cap)}]==state['daily'][a][k]
  cs=[counters[x][k] for x in ['BTC','ETH']] if a=='COMBO' else [counters[a][k]]
  for field in cs[0]:near(s[field],sum(float(x[field]) for x in cs))
  near(s['cagr_pct'],100*((v[-1]/cap)**(365/(9/1440))-1));assert not s['cash_violations'] and not s['rejected_orders'] and not s['margin_proxy_violations']
observer_source=(P/'observer.py').read_text();assert observer_source.index('reserved.append')<observer_source.index('state,delta=c.advance')<observer_source.index("put(window/'state.json'")
assert all(sha(ROOT/p)==h for p,h in rd(R/'context.json')['account_hashes_before'].items())
put(R/'l4h02_verification.json',{'passed':True,'first_actual_window':True,'actual_observation_configs':3,'start_utc':'2026-11-01T00:01:00Z','cutoff_utc':ip['first_cutoff_utc'],'elapsed_minutes':9,'cost_scenes':9,'NAV_points_per_scene':13,'NAV_points_checked':117,'independent_causal_decisions':checks['decisions'],'native_fills':checks['fills'],'funding_journal_entries':checks['funding'],'HTTP200_pages_verified':http,'warmup_complete_days':33,'first_partial_hour_is_not_liquidation_or_capacity_proof':True,'partial_annualized_metrics_not_interpreted':True,'unfiltered_original_L4H2_rules_and_source_hashes_unchanged':True,'actual_capitals':caps,'actual_entry_budgets':{'BTC':500,'ETH':4500},'independent_actual_books':books,'plan_sha256':sha(P/'plan.json'),'report_sha256':sha(w/'report.json'),'state_sha256':sha(w/'state.json'),'pointer_sha256':sha(ROOT/'research/automation/l4h02_forward_latest.json'),'future_180day_qualified':False,'completed_observation_reruns':0,'new_strategy_trials':0});print(json.dumps({'passed':True,'first_actual_window':True,'elapsed_minutes':9,**checks,'HTTP200_pages':http,'parent_returns_pct':{k:s['net_return_pct'] for k,s in report['configs']['forward_snapshot_l4h02_COMBO']['scenes'].items()}}),flush=True)
