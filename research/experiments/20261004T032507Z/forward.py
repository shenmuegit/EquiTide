"""Continue original frozen floating-quantity observer through one completed UTC daily decision."""
import copy,gzip,hashlib,importlib.util,json,math,sys,urllib.parse,urllib.request
from datetime import datetime,timezone,timedelta
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def module(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
engine=module('frozen_original_costs',ROOT/'research/experiments/20261001T013355Z/evaluate.py')
sig=module('frozen_original_signal',ROOT/'research/experiments/20261001T113625Z/signals.py')
def gzwrite(p,x):
 with p.open('wb') as f:
  with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as z:z.write(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def dd(v):
 peak=v[0];drawdown=0.
 for x in v:peak=max(peak,x);drawdown=max(drawdown,1-x/peak)
 return drawdown*100
ms=lambda s:int(datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()*1000)
iso=lambda t:datetime.fromtimestamp(t/1000,timezone.utc).isoformat().replace('+00:00','Z')
def main():
 replay='--reproduce' in sys.argv;plan=json.loads((ROUND/'spec.json').read_text());p=plan['forward_resume'];batch=json.loads((ROUND/'forward_batch.json').read_text());ledger=registry.read_records(ROOT/'research/automation/registry.jsonl')
 for b in batch:assert ledger[b['fingerprint']]['status'] in (('rejected',) if replay else ('reserved',))
 assert sha(ROOT/p['source_report'])==p['report_sha256'] and sha(ROOT/p['source_state'])==p['state_sha256']
 old=json.loads((ROOT/p['source_report']).read_text());state=json.loads((ROOT/p['source_state']).read_text());assert state['last_completed_mark_utc']==old['cutoff_utc']==p['resume_utc']
 assert sha(ROOT/old['frozen_plan_path'])==old['frozen_plan_sha256']==state['frozen_plan_sha256']
 begin,cut,event=map(ms,(p['resume_utc'],p['cutoff_utc'],p['daily_decision_utc']));day=event-60000
 assert begin<event<cut and p['daily_decision_utc']==state['next_daily_decision_utc'];assert cut<=int(datetime.now(timezone.utc).timestamp()*1000)
 started=datetime.now(timezone.utc).isoformat();provenance=[];inputs={}
 if replay:
  expected=json.loads((ROUND/'forward_report.json').read_text());assert sha(ROUND/'forward_inputs.json.gz')==expected['input_sha256'];inputs=json.loads(gzip.decompress((ROUND/'forward_inputs.json.gz').read_bytes()));provenance=expected['provenance'];started=expected['observation_started_utc']
 else:
  for asset in ('BTC','ETH'):
   inputs[asset]={}
   for interval,start,end in [('1m',begin-60000,cut),('1d',day-65*86400000,day)]:
    params={'symbol':asset+'USDT','interval':interval,'startTime':start,'endTime':end-1,'limit':1000};url='https://data-api.binance.vision/api/v3/klines?'+urllib.parse.urlencode(params)
    with urllib.request.urlopen(url,timeout=25) as response:raw=response.read();status=response.status
    assert status==200;bars=json.loads(raw);inputs[asset][interval]=bars;path=ROUND/f'forward_response_{asset}_{interval}.json.gz'
    with path.open('wb') as f:
     with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as z:z.write(raw)
    provenance.append({'asset':asset,'interval':interval,'url':url,'status':status,'retrieved_utc':datetime.now(timezone.utc).isoformat(),'raw_response_sha256':hashlib.sha256(raw).hexdigest(),'raw_gzip_path':str(path.relative_to(ROOT)),'raw_gzip_sha256':sha(path),'bars':len(bars),'timestamp_unit':'milliseconds','closed_by_endTime':True,'as_of_end_utc':iso(end),'delayed_shadow_reconstruction':True})
  gzwrite(ROUND/'forward_inputs.json.gz',inputs)
 prior_inputs=json.loads(gzip.decompress((ROOT/old['source_inputs_path']).read_bytes()));firstpath=ROOT/'research/experiments/20261003T015203Z/forward_inputs.json.gz';firstinputs=json.loads(gzip.decompress(firstpath.read_bytes()))
 oldpoints=p['prior_NAV_points'];axis=[]
 for z in inputs['BTC']['1m'][1:]:
  if z[0]==event:axis.append({'kind':'execution_reference','open_ts_ms':z[0],'available_utc':iso(z[0]),'NAV_index':oldpoints+len(axis)})
  axis.append({'kind':'closed_minute_mark','open_ts_ms':z[0],'available_utc':iso(z[6]+1),'NAV_index':oldpoints+len(axis)})
 assert len(axis)==241 and axis[51]['kind']=='execution_reference' and axis[51]['NAV_index']==2883
 configs={};decisions={};positions={}
 for b in batch[:2]:
  asset=b['asset'];bars=inputs[asset]['1m'];daily=inputs[asset]['1d'];priorbars=prior_inputs[asset];priorbars=priorbars['1m'] if isinstance(priorbars,dict) else priorbars
  assert bars[0]==priorbars[-1] and len(bars)==241 and [z[0] for z in bars]==list(range(begin-60000,cut,60000))
  assert [z[0] for z in daily]==list(range(day-65*86400000,day,86400000)) and len(daily)==65
  for seq,step,end in [(bars,60000,cut),(daily,86400000,day)]:assert all(z[6]+1==z[0]+step and z[6]+1<=end for z in seq)
  assert daily[:-1]==firstinputs[asset]['1d'][1:];assert D(daily[-1][4])==D(next(z for z in bars if z[0]==day-60000)[4])
  rows=[{'close':z[4],'quote_volume':z[7],'close_available_ts':(z[6]+1)*1000000} for z in daily];closes=[D(z['close']) for z in rows];sma=sum(closes)/65
  before=state['positions_by_asset_and_cost'][asset]['1']['desired_long'];assert all(v['desired_long']==before for v in state['positions_by_asset_and_cost'][asset].values())
  want,action=sig.step(before,closes[-1],sma,D('.01'));adv,sigma=engine.lagged_cost_inputs(rows,65)
  decisions[asset]={'executed_at_utc':iso(event),'prior_close':str(closes[-1]),'SMA65':str(sma),'before_desired_long':before,'desired_long':want,'action':action,'last_daily_close_available_utc':iso(daily[-1][6]+1),'daily_bars':65,'previous_daily_overlap_bars':64,'lagged_daily_quote_ADV':adv,'lagged_daily_volatility':sigma,'reference_minute_open':float(next(z for z in bars if z[0]==event)[1]),'reference_NAV_index':2883}
  cfg=copy.deepcopy(old['configs'][b['name']]);cfg.update(b);cfg['latest_daily_decision']=decisions[asset];positions[asset]={}
  for k,s in cfg['scenes'].items():
   pos=state['positions_by_asset_and_cost'][asset][k];cash,units=pos['cash_usdt'],pos['units'];assert s['cash_usdt']==cash and s['units']==units
   assert len(s['equity_usdt'])==oldpoints and s['equity_usdt'][-1]==cash+units*float(bars[0][4]);previous=s['equity_usdt'][-1];trades=[]
   for z in bars[1:]:
    if z[0]==event:
     ref=float(z[1]);buy=want and units==0;sell=not want and units>0
     if buy or sell:
      budget=cash if buy else units*ref;assert budget/adv<=.001
      multiplier=int(k);impact=.5*sigma*math.sqrt(budget/adv)*multiplier;fee=.001*multiplier;spread=.0001*multiplier;slip=.0002*multiplier
      execution=ref*(1+(spread+slip+impact)*(1 if buy else -1))
      qty=cash/(execution*(1+fee)) if buy else units
      if buy:cost=cash-qty*ref;cash=0.;units=qty
      else:cash=qty*execution*(1-fee);cost=qty*ref-cash;units=0.
      trades.append({'side':'buy' if buy else 'sell','reference':ref,'execution':execution,'quantity':qty,'fee_rate':fee,'half_spread_rate':spread,'slippage_rate':slip,'impact_rate':impact,'lagged_daily_quote_ADV':adv,'lagged_daily_volatility':sigma,'participation':budget/adv,'cost_usdt':cost,'executed_at_utc':iso(event),'cash_after':cash,'units_after':units})
     s['equity_usdt'].append(cash+units*ref)
    s['equity_usdt'].append(cash+units*float(z[4]));assert cash>=0 and units>=0
   s['trades']+=trades;s['cost_usdt']+=sum(t['cost_usdt'] for t in trades);s['executions']+=len(trades);s['round_trips']+=sum(t['side']=='sell' for t in trades)
   assert len(s['equity_usdt'])==p['total_NAV_points'];s.update(cash_usdt=cash,units=units,desired_long=want,cost_pct_initial=s['cost_usdt']/b['capital_usdt']*100,net_return_pct=100*(s['equity_usdt'][-1]/b['capital_usdt']-1),max_drawdown_pct=dd(s['equity_usdt']),elapsed_minutes=p['cumulative_minutes'],elapsed_complete_days=2,new_mark_minutes=240,new_reference_points=1,new_executions=len(trades),since_previous_mark_return_pct=100*(s['equity_usdt'][-1]/previous-1))
   positions[asset][k]={'cash_usdt':cash,'units':units,'desired_long':want}
  cfg['reason']='Actual cumulative3069minute partial shadow result;only2complete days,not180day/sixfold qualification.Original long-run plan collecting.';configs[b['name']]=cfg
 b=batch[-1];cfg=copy.deepcopy(old['configs'][b['name']]);cfg.update(b)
 for k,s in cfg['scenes'].items():
  aa=configs['forward_snapshot_BTC']['scenes'][k];bb=configs['forward_snapshot_ETH']['scenes'][k];v=[a+b for a,b in zip(aa['equity_usdt'],bb['equity_usdt'])];previous=s['equity_usdt'][-1]
  assert v[:oldpoints]==s['equity_usdt'];s.update(equity_usdt=v,net_return_pct=100*(v[-1]/2000-1),max_drawdown_pct=dd(v),cost_usdt=aa['cost_usdt']+bb['cost_usdt'],cost_pct_initial=(aa['cost_usdt']+bb['cost_usdt'])/2000*100,executions=aa['executions']+bb['executions'],round_trips=aa['round_trips']+bb['round_trips'],component_states={a:{'cash':positions[a][k]['cash_usdt'],'units':positions[a][k]['units']} for a in ('BTC','ETH')},elapsed_minutes=p['cumulative_minutes'],elapsed_complete_days=2,new_mark_minutes=240,new_reference_points=1,new_executions=aa['new_executions']+bb['new_executions'],since_previous_mark_return_pct=100*(v[-1]/previous-1))
 cfg['reason']='Actual3069minute cumulative partial observation;2full days insufficient180day/sixfold;long-run plan collecting.';configs[b['name']]=cfg
 report={'observation_started_utc':started,'frozen_plan_path':old['frozen_plan_path'],'frozen_plan_sha256':old['frozen_plan_sha256'],'start_utc':old['start_utc'],'resume_utc':p['resume_utc'],'cutoff_utc':p['cutoff_utc'],'source_report':p['source_report'],'source_report_sha256':p['report_sha256'],'source_state':p['source_state'],'source_state_sha256':p['state_sha256'],'input_sha256':sha(ROUND/'forward_inputs.json.gz'),'source_inputs_path':str((ROUND/'forward_inputs.json.gz').relative_to(ROOT)),'daily_overlap_source':{'path':str(firstpath.relative_to(ROOT)),'sha256':sha(firstpath)},'daily_decisions_by_asset':decisions,'append_axis':axis,'provenance':provenance,'configs':configs,'validation':{'walk_forward':'Incomplete3069minutes/2full days;no180day/sixfold qualification','sensitivity':'Original frozenSMA65/band1percent unchanged;no new forward variants','costs':'All original1/2/3x histories retained;daily fills if triggered use original floating budget/ADV impact model;no retrofit exchange rounding.TCA/capacity unvalidated.','continuity':'2832oldNAVpoints exact prefix;240closedminute marks plus1daily reference appended to3073points;cash/units/desired/trades/cost retained,no reset or forced exit.','interpretation':'Delayed shadow reconstruction from real completed bars;no live orders,real-time execution proof or stable profit'},'source_hashes':{str(path.relative_to(ROOT)):sha(path) for path in [ROUND/'forward.py',ROUND/'audit_forward.py',ROOT/'research/experiments/20261001T113625Z/signals.py',ROOT/'research/experiments/20261001T013355Z/evaluate.py']}}
 nextstate=copy.deepcopy(state);nextstate.update(source_report=str((ROUND/'forward_report.json').relative_to(ROOT)),last_completed_mark_utc=p['cutoff_utc'],next_daily_decision_utc=iso(event+86400000),positions_by_asset_and_cost=positions,previous_state=p['source_state'],previous_state_sha256=p['state_sha256'],next_round='Continue exact original positions/costs/desired;beforeOct5UTC00:01 append closed marks only;at next daily decision apply frozenSMA65 from complete preceding daily closes and lagged20daily cost inputs.No reset or parameter changes.Reserve any new cutoff first.')
 if replay:
  assert report==expected;nextstate['source_report_sha256']=sha(ROUND/'forward_report.json');assert nextstate==json.loads((ROUND/'forward_state.json').read_text());print('PASS:all9 cumulative forward scenes exactly reproduced including original daily decision,reference axis and nextstate;noHTTP or ledger write');return
 (ROUND/'forward_report.json').write_text(json.dumps(report,ensure_ascii=False,separators=(',',':'))+'\n');nextstate['source_report_sha256']=sha(ROUND/'forward_report.json');(ROUND/'forward_state.json').write_text(json.dumps(nextstate,indent=2)+'\n')
 print(json.dumps({'configs':3,'cost_scenes':9,'cumulative_minutes':3069,'complete_days':2,'new_closed_minutes':240,'NAV_points':3073,'daily_decisions':{a:d['action'] for a,d in decisions.items()},'new_component_executions':sum(s['new_executions'] for c in configs.values() if 'asset' in c for s in c['scenes'].values()),'combo_net_returns_pct':{k:s['net_return_pct'] for k,s in configs['forward_snapshot_combo']['scenes'].items()}}),flush=True)
if __name__=='__main__':main()
