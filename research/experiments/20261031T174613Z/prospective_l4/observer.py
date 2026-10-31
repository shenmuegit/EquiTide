"""Real future data capture/reserved incremental replay; status is strictly read only.

Run under the outer branch broker. Never invoke run/capture before the frozen start.
No API keys or private exchange/order APIs are used.
"""
import argparse,copy,gzip,hashlib,json,os,subprocess,sys,time,urllib.parse,urllib.request
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
sys.dont_write_bytecode=True
import core as c
ROOT=c.ROOT;R=Path(__file__).resolve().parent;POINTER=ROOT/'research/automation/l4h02_forward_latest.json'
put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
rel=lambda p:str(p.relative_to(ROOT))
def gzput(p,x):p.write_bytes(gzip.compress(c.canonical(x),mtime=0))
def gzread(p):return json.loads(gzip.decompress(p.read_bytes()))
def now():return time.time_ns()

def owner(pid):
 assert subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=ROOT,text=True).strip()==str(ROOT)
 assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='main'
 lines=Path('/proc/locks').read_text().splitlines();ino=(ROOT/'research/automation/branch.lock').stat().st_ino
 assert any('FLOCK' in x and 'WRITE' in x and x.split()[4]==str(pid) and int(x.split()[5].split(':')[-1])==ino for x in lines),'outer branch broker must hold lock'

def prior(binding):
 if not POINTER.exists():
  # Never silently restart cash after a committed or pending first observation.
  sys.path.insert(0,str(ROOT/'research/automation'));import registry
  assert not any(x.get('spec',{}).get('name','').startswith('forward_snapshot_l4h02_') for x in registry.read_records(ROOT/'research/automation/registry.jsonl').values()),'candidate records exist without pointer: recover explicitly'
  return None,None
 p=json.loads(POINTER.read_text());assert p['plan_sha256']==binding['plan_sha256']
 for k in ['state','report','delta','complete']:
  assert c.sha(ROOT/p[k])==p[k+'_sha256'],'candidate chain changed'
 state=json.loads((ROOT/p['state']).read_text());assert state['cutoff_ns']==p['cutoff_ns'] and state['plan_sha256']==binding['plan_sha256']
 return p,state

def request(path,params,rawdir,receipts):
 url='https://fapi.binance.com'+path+('?' + urllib.parse.urlencode(params) if params else '')
 for attempt in range(2):
  started=datetime.now(timezone.utc).isoformat();cmd=['curl','--ipv4','--compressed','--http1.1','--tlsv1.2','--tls-max','1.2','--silent','--show-error','--connect-timeout','10','--max-time','30','--user-agent','EquiTide-ReadOnly-Research/1.0','--write-out','\n%{http_code}',url];p=subprocess.run(cmd,cwd=ROOT,capture_output=True,timeout=65);body,code=p.stdout.rsplit(b'\n',1) if b'\n' in p.stdout else(p.stdout,b'000');status=int(code);dest=rawdir/f'http_{len(receipts):04d}.gz';dest.write_bytes(gzip.compress(body,mtime=0));row={'url':url,'started_utc':started,'http_status':status,'curl_exit_code':p.returncode,'raw':rel(dest),'sha256':c.sha(dest),'bytes':len(body),'stderr':p.stderr.decode(errors='replace'),'transport':'verifiedTLS1.2HTTP1.1 bounded2attempts'};receipts.append(row)
  if p.returncode==0 and status==200:return json.loads(body)
 raise RuntimeError('Publiccapturefailedbothboundedattempts; preserveaccount/capturefailure, no fakefills')

def capture(cutoff,previous,binding,rawdir,receipts):
 c.check_window(previous,cutoff,now());rawdir.mkdir(parents=True,exist_ok=False)
 info=request('/fapi/v1/exchangeInfo',{},rawdir,receipts);server=request('/fapi/v1/time',{},rawdir,receipts);retrieved=min(now(),int(server['serverTime'])*c.MS)
 assert retrieved>=cutoff+c.MIN
 symbols={x['symbol']:x for x in info['symbols']};assets={};lo=previous['cutoff_ns'] if previous else c.START
 def bars(path,a,interval,step,start,end):
  rows=[];cursor=start//c.MS
  while cursor<=end//c.MS:
   data=request(path,{'symbol':a+'USDT','interval':interval,'startTime':cursor,'endTime':end//c.MS,'limit':1500},rawdir,receipts);assert isinstance(data,list) and data
   assert int(data[0][0])==cursor;rows.extend(data);cursor=int(data[-1][0])+step//c.MS
  assert int(rows[-1][0])*c.MS==end
  return rows
 for a in ['BTC','ETH']:
  sy=symbols[a+'USDT'];assert sy['status']=='TRADING' and sy['contractType']=='PERPETUAL' and sy['quoteAsset']=='USDT' and sy['marginAsset']=='USDT'
  fs={x['filterType']:x for x in sy['filters']};meta={'lot_size':fs['LOT_SIZE']['stepSize'],'tick_size':fs['PRICE_FILTER']['tickSize'],'min_notional':fs['MIN_NOTIONAL']['notional']}
  assert {k:c.D(v) for k,v in meta.items()}=={k:c.D(v) for k,v in binding['metadata'][a].items()},'metadata change blocks, no silent retrofit'
  minutes=bars('/fapi/v1/klines',a,'1m',c.MIN,lo-c.MIN if previous else c.WARMUP,cutoff)
  hours=bars('/fapi/v1/markPriceKlines',a,'1h',c.HOUR,(lo//c.HOUR)*c.HOUR-c.HOUR,(cutoff//c.HOUR-1)*c.HOUR)
  firstfund=int(previous['context'][a]['last_funding']['fundingTime']) if previous else (lo//(8*c.HOUR)*8*c.HOUR-8*c.HOUR)//c.MS
  funds=[];cursor=firstfund
  while cursor<=cutoff//c.MS:
   data=request('/fapi/v1/fundingRate',{'symbol':a+'USDT','startTime':cursor,'endTime':cutoff//c.MS,'limit':1000},rawdir,receipts);assert isinstance(data,list)
   if not data:break
   funds.extend(data);cursor=int(data[-1]['fundingTime'])+1
   if len(data)<1000:break
  assets[a]={'metadata':meta,'minutes':minutes,'hours':hours,'funding':funds}
 packet={'schema_version':1,'plan_sha256':binding['plan_sha256'],'cutoff_ns':cutoff,'retrieved_ns':retrieved,'assets':assets,'provenance':receipts,'mode':'real public closed-data delayed replay'}
 c.normalize(packet,previous,binding);return packet

def metrics(rows,daily,capital,start,end):
 v=np.asarray([r for _,r in rows],dtype=float);assert len(v) and np.isfinite(v).all() and (v>0).all();days=(end-start)/c.DAY;dd=100*float(np.max(1-v/np.maximum.accumulate(v)));rr=[b['equity_usdt']/a['equity_usdt']-1 for a,b in zip(daily,daily[1:])]
 sd=__import__('statistics').stdev(rr) if len(rr)>1 else None
 out={'initial_capital_usdt':capital,'final_NAV_usdt':float(v[-1]),'net_return_pct':100*(v[-1]/capital-1),'max_drawdown_pct':dd,'NAV_points':len(v),'NAV_sha256_f64le':hashlib.sha256(v.astype('<f8').tobytes()).hexdigest(),'daily_equity_usdt':daily,'sharpe_365':__import__('statistics').mean(rr)/sd*365**.5 if sd else None,'folds':[]}
 for j in range(6):
  a=start+j*30*c.DAY;b=a+30*c.DAY
  if b>end:break
  z=[v for key,v in rows if (a,0 if j==0 else 5)<=key<=(b,9 if b==c.END else 5)];bound_a=next(x['equity_usdt'] for x in daily if x['timestamp_ns']==a);bound_b=next(x['equity_usdt'] for x in daily if x['timestamp_ns']==b)
  out['folds'].append({'fold':j+1,'start_ns':a,'end_exclusive_ns':b,'duration_days':30,'net_return_pct':100*(bound_b/bound_a-1),'max_drawdown_pct':100*float(np.max(1-np.asarray(z)/np.maximum.accumulate(z)))})
 out['cagr_pct']=100*((v[-1]/capital)**(365/days)-1) if days>0 else None
 out['calmar']=out['cagr_pct']/dd if dd and out['cagr_pct'] is not None else None
 out['recent40']=None
 if end==c.END:
  a=end-40*c.DAY;d=[x for x in daily if x['timestamp_ns']>=a];vv=[(key,v) for key,v in rows if (a,5)<=key<=(end,9)];assert len(d)==41
  v40=np.asarray([v for _,v in vv]);out['recent40']={'net_return_pct':100*(v40[-1]/d[0]['equity_usdt']-1),'max_drawdown_pct':100*float(np.max(1-v40/np.maximum.accumulate(v40))),'folds':[{'fold':j+1,'duration_days':5,'net_return_pct':100*(d[(j+1)*5]['equity_usdt']/d[j*5]['equity_usdt']-1)} for j in range(8)]}
 return out

def all_deltas(pointer):
 out=[];seen=set()
 while pointer:
  assert pointer['delta'] not in seen;seen.add(pointer['delta']);assert c.sha(ROOT/pointer['delta'])==pointer['delta_sha256'];out.append(gzread(ROOT/pointer['delta']))
  previous=pointer.get('previous_pointer');
  if previous:assert c.sha(ROOT/previous['path'])==previous['sha256'];pointer=json.loads((ROOT/previous['path']).read_text())
  else:pointer=None
 return list(reversed(out))

def reports(state,deltas,specs,binding):
 configs={};cut=state['cutoff_ns'];mature=cut==c.END
 nav=[x for d in deltas for x in d['NAV']];assert len(nav)==state['nav_points'] and all((x['timestamp_ns'],x['event_code'])<(y['timestamp_ns'],y['event_code']) for x,y in zip(nav,nav[1:]))
 for a in ['BTC','ETH','COMBO']:
  name='forward_snapshot_l4h02_'+a;scenes={}
  for k in ['1','2','3']:
   z=metrics([((x['timestamp_ns'],x['event_code']),x['NAV'][a][k]) for x in nav],state['daily'][a][k],sum(binding['capitals'].values()) if a=='COMBO' else binding['capitals'][a],c.START,cut)
   counters=[state['counters'][x][k] for x in ['BTC','ETH']] if a=='COMBO' else [state['counters'][a][k]]
   for field in counters[0]:z[field]=sum(float(x[field]) for x in counters)
   z['gross_reference_PnL_to_execution_cost']=(z['gross_reference_price_PnL_usdt']+z['funding_usdt'])/z['cost_usdt'] if z['cost_usdt'] else None
   z['terminal_units']={x:state['books'][x][k]['signed_units'] for x in ['BTC','ETH']} if a=='COMBO' else state['books'][a][k]['signed_units'];scenes[k]=z
  one,three=scenes['1'],scenes['3'];criteria={'full180days':mature,'six_complete_folds':len(one['folds'])==6,'five_positive_30day_folds':sum(x['net_return_pct']>0 for x in one['folds'])>=5,'all_cost_net_positive':all(x['net_return_pct']>0 for x in scenes.values()),'whole_DD3_le25':three['max_drawdown_pct']<=25,'round_trips1_ge4':one['round_trips']>=4,'cost_safety_1x':one['gross_reference_PnL_to_execution_cost'] is not None and one['gross_reference_PnL_to_execution_cost']>=2.5,'no_cash_order_margin_violations':all(not any(z[f] for f in ['cash_violations','rejected_orders','margin_proxy_violations']) for z in scenes.values()),'recent40_6of8':mature and all(sum(x['net_return_pct']>0 for x in z['recent40']['folds'])>=6 for z in scenes.values()),'recent40_all_cost_positive':mature and all(z['recent40']['net_return_pct']>0 for z in scenes.values())}
  configs[name]={'name':name,'fingerprint':specs[a]['fingerprint'],'status':'passed' if all(criteria.values()) else 'rejected','result_available':True,'scenes':scenes,'criteria':criteria,'failed_criteria':[x for x,v in criteria.items() if not v],'observation_mode':'delayed closed-bar/funding replay, not paper10/live execution','partial_observation':not mature,'does_not_cancel_or_reset_frozen_plan':True,'parameters':specs[a]['spec']['parameters']}
 return {'schema_version':1,'result_available':True,'plan_sha256':binding['plan_sha256'],'cutoff_ns':cut,'elapsed_days':(cut-c.START)/c.DAY,'configs':configs,'new_strategy_trials':0,'actual_observation_configs':3,'NAV_chain_sha256':state['nav_chain_sha256'],'sensitivity':'Frozen original candidate and prior historical neighborhood; no future parameter retuning.','state_continuity':'Native collateral/quantity/entry/cost/funding and full NAV prefix carry; terminal close only on predeclared180dayend.'}

def observation_spec(a,cutoff_text,packetpath,packet_sha,binding,pointer,specs):
 name='forward_snapshot_l4h02_'+a
 spec={'kind':'combination' if a=='COMBO' else 'strategy','family':'prospectively-frozen-l4h02-candidate-observation','name':name,'logic':{'mode':'delayed real closed-bar/funding replay, not live quote execution','frozen_plan_sha256':binding['plan_sha256'],'rules':binding['rules'],'allocation':'WholeBTC5000/ETH15000banks,raw1/1,parent20000,N500/4500,no normalization/NAVresize/transfers/rebalance.','full_frozen_plan':json.loads(c.PLAN.read_text()),'partial_rejected_does_not_cancel_plan':True},'parameters':{'owner_automation_id':'btc-eth','observation_mode':'forward_snapshot_candidate','asset':a,'start_utc':'2026-11-01T00:01:00Z','end_utc':cutoff_text,'planned_terminal_utc':'2027-04-30T00:01:00Z','cost_multipliers':[1,2,3],'initial_capital_usdt':sum(binding['capitals'].values()) if a=='COMBO' else binding['capitals'][a],'input_hashes':{rel(packetpath):packet_sha},'previous_state_sha256':pointer['state_sha256'] if pointer else None},'components':([{'fingerprint':specs[x]['fingerprint'],'weight':1} for x in ['BTC','ETH']] if a=='COMBO' else []),'market':'binance-usdm-linear-perpetual','timeframe':'1d','universe':[x+'/USDT' for x in (['BTC','ETH'] if a=='COMBO' else [a])]}
 return spec

def main():
 ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['status','run']);ap.add_argument('--cutoff');ap.add_argument('--round');ap.add_argument('--lock-pid',type=int);args=ap.parse_args();binding=c.bindings()
 if args.mode=='status':
  status=c.ready_status(now());status['account_created']=POINTER.exists();status.update(binding=binding,canonical_pointer_present=POINTER.exists(),network_requests=0,filesystem_writes=0,registry_writes=0);print(json.dumps(status));return
 assert now()>=c.START,'before planned start: no accounts/capture/reservation'
 assert args.cutoff and args.round and args.lock_pid;owner(args.lock_pid);cut=c.ns(args.cutoff);pointer,previous=prior(binding);c.check_window(previous,cut,now())
 window=ROOT/'research/experiments'/args.round/'l4h02_observation';assert window.parent.is_dir() and args.round==window.parent.name and window.resolve().is_relative_to(ROOT/'research/experiments');window.mkdir(exist_ok=False)
 rawdir=ROOT/'data/raw/binance/l4h02_forward'/args.round;receipts=[];reserved=[];actual_result_saved=False
 try:
  packet=capture(cut,previous,binding,rawdir,receipts);packetpath=rawdir/'packet.json.gz';gzput(packetpath,packet);put(window/'input_manifest.json',{'packet':rel(packetpath),'sha256':c.sha(packetpath),'provenance':receipts,'plan_sha256':binding['plan_sha256']})
  sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
  specs={}
  for a in ['BTC','ETH','COMBO']:
   spec=observation_spec(a,args.cutoff,packetpath,c.sha(packetpath),binding,pointer,specs)
   path=window/(a+'_spec.json');put(path,spec);fp=reg.fingerprint(spec);p=subprocess.run([sys.executable,str(ROOT/'research/automation/registry.py'),'reserve',rel(path)],cwd=ROOT,capture_output=True,text=True);receipts.append({'command':['registry.py','reserve',rel(path)],'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr});assert p.returncode==0 and p.stdout.strip()==fp;reserved.append((path,fp));specs[a]={'spec':spec,'path':path,'fingerprint':fp}
  state,delta=c.advance(previous,packet,binding);deltas=all_deltas(pointer)+[delta];report=reports(state,deltas,specs,binding);gzput(window/'delta.json.gz',delta);put(window/'state.json',state);put(window/'report.json',report)
  complete={'plan_sha256':binding['plan_sha256'],'cutoff_ns':cut,'state_sha256':c.sha(window/'state.json'),'report_sha256':c.sha(window/'report.json'),'delta_sha256':c.sha(window/'delta.json.gz'),'previous_pointer_sha256':hashlib.sha256(c.canonical(pointer)).hexdigest() if pointer else None};put(window/'complete.json',complete);actual_result_saved=True
  for a,x in specs.items():
   status=report['configs']['forward_snapshot_l4h02_'+a]['status'];p=subprocess.run([sys.executable,str(ROOT/'research/automation/registry.py'),'finish',rel(x['path']),status,rel(window/'report.json')],cwd=ROOT,capture_output=True,text=True);receipts.append({'command':['registry.py','finish',rel(x['path']),status],'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr});assert p.returncode==0 and p.stdout.strip()==x['fingerprint']
  previous_ref=None
  if pointer:
   put(window/'previous_pointer.json',pointer);previous_ref={'path':rel(window/'previous_pointer.json'),'sha256':c.sha(window/'previous_pointer.json')}
  point={'plan_sha256':binding['plan_sha256'],'cutoff_ns':cut,'previous_pointer':previous_ref}
  for key,file in [('state','state.json'),('report','report.json'),('delta','delta.json.gz'),('complete','complete.json')]:point[key]=rel(window/file);point[key+'_sha256']=c.sha(window/file)
  put(window/'receipts.json',receipts);tmp=POINTER.with_suffix('.tmp');put(tmp,point);tmp.replace(POINTER)
  print(json.dumps({'observations_finished':3,'account_continued':previous is not None,'cutoff':args.cutoff,'report':rel(window/'report.json'),'shared_pointer_must_be_committed':rel(POINTER),'no_real_orders':True}))
 except Exception as error:
  # An unfinished reserved window is recoverable; never advance pointer/cash on failure.
  failure={'result_available':False,'error':repr(error),'receipts':receipts,'previous_state_preserved':True,'complete_actual_result_requires_finish_recovery':actual_result_saved};put(window/'failure.json',failure)
  for path,fp in ([] if actual_result_saved else reserved):
   p=subprocess.run([sys.executable,str(ROOT/'research/automation/registry.py'),'finish',rel(path),'blocked',rel(window/'failure.json')],cwd=ROOT,capture_output=True,text=True);receipts.append({'recovery_finish_fp':fp,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
  put(window/'failure_receipts.json',receipts);raise
if __name__=='__main__':main()
