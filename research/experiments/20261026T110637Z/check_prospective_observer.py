"""Engineering fixtures only; no new real strategy evaluation or future account."""
from pathlib import Path
import importlib.util,json,hashlib,copy,tempfile,sys
R=Path(__file__).resolve().parent
assert (R/'prospective_core.py').exists(), 'incremental prospective observer has not been implemented'
s=importlib.util.spec_from_file_location('prospective_core',R/'prospective_core.py');c=importlib.util.module_from_spec(s);s.loader.exec_module(c)
assert c.ready_status(c.START-1)['account_created'] is False
assert c.ready_status(c.START-1)['status']=='waiting_for_planned_start'
assert c.ready_status(c.START)['status']=='eligible_for_validated_real_window'
for bad in [c.START-1,c.END+1]:
 try:c.check_window(None,bad,bad+c.MIN)
 except AssertionError:pass
 else:raise AssertionError('time guard accepted forbidden window')
print(json.dumps({'passed':True,'scope':'synthetic engineering guard checks, no financial results'}))

binding=c.bindings();D=c.D;S=c.START;M=c.MIN;H=c.HOUR
# Synthetic transitions exercise account continuity and event ordering only.
def p(price='100',closes=None):return {'price':price,'closes':closes or ['100']*32+['110'],'ADV':'1000000000','sigma':'.02'}
def pair(payload):return {a:copy.deepcopy(payload) for a in ['BTC','ETH']}
actions={(S,0):pair(p()),(S,5):pair(p()),(S,6):pair(p()),(S,7):pair(p()),(S+M,1):pair(p('101')),(S+2*M,1):pair(p('102'))}
one,all_delta=c.transition(None,actions,S+2*M,binding)
first,first_delta=c.transition(None,{k:v for k,v in actions.items() if k[0]<=S+M},S+M,binding)
second,second_delta=c.transition(first,{k:v for k,v in actions.items() if k[0]>S+M},S+2*M,binding)
assert one==second and all_delta['NAV']==first_delta['NAV']+second_delta['NAV'] and all_delta['journal']==first_delta['journal']+second_delta['journal']
assert D(second['books']['BTC']['1']['signed_units'])>0 and second['counters']['BTC']['1']['executions']==1
assert not any(x.get('terminal',False) for x in all_delta['journal'])
# Funding charges old signed exposure, before same-day decision, and outflows only scale.
fund_t=S+8*H-M+1_000_000
old=copy.deepcopy(first);old['cutoff_ns']=fund_t-M;old['last_key']=[fund_t-M,1]
f={'price':'100','rate':'.001'}
fund_actions={(fund_t,3):pair(f),(fund_t,4):pair(f),(fund_t+M,1):pair(p())}
funded,fd=c.transition(old,fund_actions,fund_t+M,binding)
for k in ['1','2','3']:
 q=D(old['books']['BTC'][k]['signed_units']);amount=-(q*100*D('.001'))*int(k)
 assert D(funded['books']['BTC'][k]['cash'])==D(old['books']['BTC'][k]['cash'])+amount
assert c.GATE.funding_amount(D('2'),D('100'),D('-.001'),3)[1]==D('.2')
assert c.GATE.funding_amount(D('-2'),D('100'),D('-.001'),3)[1]==D('-.6')
assert [x['event_code'] for x in fd['NAV']]==[3,4,1]
# Only declared terminal permits a terminal close; intermediate sampling keeps position.
terminal_old=copy.deepcopy(second);terminal_old['cutoff_ns']=c.END-M;terminal_old['last_key']=[c.END-M,1]
terminal,td=c.transition(terminal_old,{(c.END,8):pair(p()),(c.END,9):pair(p())},c.END,binding)
assert all(D(x['signed_units'])==0 for books in terminal['books'].values() for x in books.values())
assert sum(x.get('kind')=='trade' and x['terminal'] for x in td['journal'])==3
# Misbound state and duplicate events must fail before a new transition.
for bad_state,bad_actions in [(dict(first,plan_sha256='bad'),{(S+2*M,1):pair(p())}),(first,{(S+M,1):pair(p())})]:
 try:c.transition(bad_state,bad_actions,S+2*M,binding)
 except AssertionError:pass
 else:raise AssertionError('state binding/repeated event was accepted')
# Closed-bar units, missing minute, unclosed reference and price validity.
def bar(t,interval=M,price='100',volume='100000000'):
 return [t//c.MS,price,price,price,price,'1',(t+interval)//c.MS-1,volume,1,'0','0','0']
assert len(c.closed_bars([bar(S),bar(S+M)],M,S+2*M))==2
for raw,available in [([bar(S),bar(S+2*M)],S+3*M),([bar(S)],S+M-1),([bar(S//1000)],S+M),([bar(S,price='0')],S+M)]:
 try:c.closed_bars(raw,M,available)
 except AssertionError:pass
 else:raise AssertionError('bad raw data accepted')
# Realistic synthetic first packet and incremental overlap. No actual future returns saved.
def packet(cut):
 assets={}
 for a in ['BTC','ETH']:
  mins=[bar(t,price='100' if t<S else '999',volume='1000000' if t<S else '99999999999') for t in range(c.WARMUP,cut+M,M)]
  hrs=[bar(t,H) for t in range((S//H)*H-H,(cut//H)*H,H)]
  funds=[{'symbol':a+'USDT','fundingTime':t//c.MS,'fundingRate':'.0001','markPrice':'100'} for t in range((S//(8*H)-1)*8*H,(cut//(8*H))*8*H+1,8*H)]
  assets[a]={'metadata':binding['metadata'][a],'minutes':mins,'hours':hrs,'funding':funds}
 return {'plan_sha256':binding['plan_sha256'],'cutoff_ns':cut,'retrieved_ns':cut+M,'assets':assets}
pack=packet(S+2*M);lo,cut,normalized,ctx=c.normalize(pack,None,binding)
assert normalized[S,6]['BTC']['closes'][-1]=='100'
assert D(normalized[S,6]['BTC']['ADV'])==D('1440000000') # 1440 complete 1m bars/day, no partial current day.
state,delta=c.advance(None,pack,binding)
pack2=packet(S+4*M)
for a in ['BTC','ETH']:
 pack2['assets'][a]['minutes']=[r for r in pack2['assets'][a]['minutes'] if int(r[0])*c.MS>=state['cutoff_ns']-M]
 pack2['assets'][a]['funding']=[r for r in pack2['assets'][a]['funding'] if int(r['fundingTime'])>=int(state['context'][a]['last_funding']['fundingTime'])]
resumed,rd=c.advance(state,pack2,binding)
whole,wd=c.advance(None,packet(S+4*M),binding)
assert resumed==whole and delta['NAV']+rd['NAV']==wd['NAV']
changed=copy.deepcopy(pack2);changed['assets']['BTC']['minutes'][0][7]='1'
try:c.advance(state,changed,binding)
except AssertionError:pass
else:raise AssertionError('revised overlap accepted')
# Cross a daily decision, hourly extrema and three actual-time funding slots in two windows.
long_packet=packet(S+c.DAY+2*M)
for a in ['BTC','ETH']:
 long_packet['assets'][a]['minutes']=[r for r in long_packet['assets'][a]['minutes'] if int(r[0])*c.MS>=state['cutoff_ns']-M]
 long_packet['assets'][a]['funding']=[r for r in long_packet['assets'][a]['funding'] if int(r['fundingTime'])>=int(state['context'][a]['last_funding']['fundingTime'])]
crossed,cd=c.advance(state,long_packet,binding)
whole_day,whole_day_delta=c.advance(None,packet(S+c.DAY+2*M),binding)
assert crossed==whole_day and delta['NAV']+cd['NAV']==whole_day_delta['NAV']
assert crossed['counters']['BTC']['1']['funding_settlements']==3
assert sum(x['kind']=='decision' for x in whole_day_delta['journal'])==12
missing=copy.deepcopy(long_packet);missing['assets']['BTC']['funding'].pop(1)
try:c.advance(state,missing,binding)
except AssertionError:pass
else:raise AssertionError('missing eight-hour funding settlement accepted')
changed=copy.deepcopy(long_packet);changed['assets']['ETH']['metadata']=dict(changed['assets']['ETH']['metadata'],tick_size='1')
try:c.advance(state,changed,binding)
except AssertionError:pass
else:raise AssertionError('changed contract filters accepted')
# Build all three future specs and calculate structural fingerprints without writing any ledger.
import prospective_observer as observer
sys.path.insert(0,str(c.ROOT/'research/automation'));import registry
specs={}
for a in ['BTC','ETH','COMBO']:
 sp=observer.observation_spec(a,'2026-10-27T02:01:00Z',c.ROOT/'data/raw/fixture.json.gz','f'*64,binding,None,specs)
 fp=registry.fingerprint(sp);specs[a]={'spec':sp,'fingerprint':fp}
 assert sp['parameters']['input_hashes']=={'data/raw/fixture.json.gz':'f'*64}
 assert sp['name'].startswith('forward_snapshot_candidate_')
assert len({x['fingerprint'] for x in specs.values()})==3
assert [x['fingerprint'] for x in specs['COMBO']['spec']['components']]==[specs[a]['fingerprint'] for a in ['BTC','ETH']]
# Whole-curve drawdown must retain intra-day loss, even when both daily marks are unchanged.
rows=[((S,0),10000),((S+M,1),9000),((S+c.DAY,5),10000)]
met=observer.metrics(rows,[{'timestamp_ns':S,'equity_usdt':10000},{'timestamp_ns':S+c.DAY,'equity_usdt':10000}],10000,S,S+c.DAY)
assert abs(met['max_drawdown_pct']-10)<1e-12
# Exercise the real capture adapter with a deterministic fake public HTTP transport.
# The adapter writes temporary raw fixtures only; these are deleted after the check.
import tempfile
fake=packet(S+2*M);original_request=observer.request;original_now=observer.now
calls=[]
def fake_http(path,params,rawdir,receipts):
 calls.append((path,params))
 if path.endswith('exchangeInfo'):
  return {'symbols':[{'symbol':a+'USDT','status':'TRADING','contractType':'PERPETUAL','quoteAsset':'USDT','marginAsset':'USDT','filters':[{'filterType':'LOT_SIZE','stepSize':binding['metadata'][a]['lot_size']},{'filterType':'PRICE_FILTER','tickSize':binding['metadata'][a]['tick_size']},{'filterType':'MIN_NOTIONAL','notional':binding['metadata'][a]['min_notional']}]} for a in ['BTC','ETH']]}
 if path.endswith('/time'):return {'serverTime':fake['retrieved_ns']//c.MS}
 a=params['symbol'][:3]
 if path.endswith('fundingRate'):return [r for r in fake['assets'][a]['funding'] if params['startTime']<=r['fundingTime']<=params['endTime']][:params['limit']]
 data=fake['assets'][a]['hours' if path.endswith('markPriceKlines') else 'minutes']
 return [r for r in data if params['startTime']<=r[0]<=params['endTime']][:params['limit']]
try:
 observer.request=fake_http;observer.now=lambda:fake['retrieved_ns']
 with tempfile.TemporaryDirectory(prefix='candidate_engineering_',dir=c.ROOT/'data') as d:
  captured=observer.capture(fake['cutoff_ns'],None,binding,Path(d)/'raw',[])
  assert captured['assets']==fake['assets'] and len(calls)>60
finally:observer.request=original_request;observer.now=original_now
# Source ledger replay uses recorded execution prices/fees only, never signal/order reruns.
import gzip
real=[];frozen=json.loads(c.PLAN.read_text())
for component in frozen['components']:
 specpath=c.ROOT/component['source_spec'];spec=json.loads(specpath.read_text());reportpath=c.ROOT/('research/experiments/20261025T065405Z/report.json' if component['asset']=='BTC' else 'research/experiments/20261026T070542Z/report.json')
 report=json.loads(reportpath.read_text());cfg=report['configs'][spec['name']];arcpath=c.ROOT/cfg['archive'];assert c.sha(arcpath)==cfg['archive_sha256'];archive=json.loads(gzip.decompress(arcpath.read_bytes()))
 for k,scene in archive['scenes'].items():
  book={'cash':'10000','signed_units':'0','entry_price':'0','entry_reference':'0'};events=[]
  events.extend((int(t['trade_ts_ns']),6 if not t['opening'] else 7,'trade',t) for t in scene['trades'] if t['status']=='filled')
  events.extend((int(f['settlement_ts_ns']),4,'funding',f) for f in scene['funding_events'])
  for t,code,kind,event in sorted(events,key=lambda x:(x[0],x[1])):
   if kind=='funding':
    assert D(book['cash'])==D(event['cash_before']) and D(book['signed_units'])==D(event['signed_units'])
    book['cash']=str(D(book['cash'])+D(event['amount_usdt']));assert D(book['cash'])==D(event['cash_after'])
   else:
    assert all(D(book[key])==D(event['state_before'][key]) for key in book)
    q=D(book['signed_units']);cash=D(book['cash'])+(q*(D(event['execution'])-D(book['entry_price'])) if not event['opening'] else 0)-D(event['cost_parts']['fee'])
    book=copy.deepcopy(event['state_after']);assert D(book['cash'])==cash
  assert all(D(book[key])==D(scene['terminal_state'][key]) for key in book)
  real.append({'asset':component['asset'],'cost_multiplier':k,'recorded_events_replayed':len(events),'archive':str(arcpath.relative_to(c.ROOT)),'archive_sha256':c.sha(arcpath),'source_report_sha256':c.sha(reportpath)})
# status makes no HTTP/account/registry writes; actual run is blocked pre-start.
import subprocess,os
before={str(p):c.sha(p) for p in [c.ROOT/'research/automation/registry.jsonl',c.PLAN]}
env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
r=subprocess.run([sys.executable,str(R/'prospective_observer.py'),'status'],cwd=c.ROOT,env=env,capture_output=True,text=True);assert r.returncode==0,r.stderr
status=json.loads(r.stdout);assert status['network_requests']==status['filesystem_writes']==status['registry_writes']==0 and status['canonical_pointer_present'] is False
blocked=subprocess.run([sys.executable,str(R/'prospective_observer.py'),'run'],cwd=c.ROOT,env=env,capture_output=True,text=True);assert blocked.returncode==1 and 'before planned start' in blocked.stderr
assert not (c.ROOT/'research/automation/candidate_forward_latest.json').exists() and before=={p:c.sha(Path(p)) for p in before}
result={'passed':True,'synthetic_engineering_checks':['prestart guards','immutable original H4/E1 binding','raw ms/closed/continuous bars','strict overlap','complete-day-only signals/ADV','one-shot vs split NAV/state/journal equivalence','funding time and outflow-only stress','no repeated entry or intermediate close','terminal-only close','state binding and duplicate refusal','cross-day/hour/funding chunk equivalence','missing funding blocks','contract metadata changes block','capture adapter pagination','future structural fingerprints and parent references','intra-day whole-curve drawdown','no status network/writes/registry mutation'],'real_saved_native_cost_ledgers_replayed':real,'source_rules_rerun_on_real_history':False,'actual_future_observations':0,'new_financial_evaluations':0,'canonical_account_pointer_created':False,'original_plan_sha256':binding['plan_sha256']}
(R/'observer_checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result))
