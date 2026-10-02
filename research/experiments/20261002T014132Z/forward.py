"""First delayed shadow snapshot of the original frozen floating-quantity plan."""
import copy,gzip,hashlib,importlib.util,json,math,statistics,subprocess,sys,urllib.request,urllib.parse
from datetime import datetime,timezone,timedelta
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
def module(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);sys.modules[n]=m;s.loader.exec_module(m);return m
engine=module('forward_original_engine',ROOT/'research/experiments/20261001T013355Z/evaluate.py')
sig=module('forward_original_signal',ROOT/'research/experiments/20261001T113625Z/signals.py')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def writegz(p,x):
 with p.open('wb') as f:
  with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as z:z.write(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
START=datetime(2026,10,2,0,1,tzinfo=timezone.utc);CUT=datetime(2026,10,2,1,40,tzinfo=timezone.utc)
ISO=lambda t:t.isoformat().replace('+00:00','Z')
def reserve():
 source=ROOT/'research/experiments/20261001T113625Z';batch=[]
 for asset,capital in [('BTC',1500),('ETH',500)]:
  p=source/'specs'/f'hyst_{asset}_n65_b0.01_c{capital}.json';sp=json.loads(p.read_text());sp['name']='forward_snapshot_'+asset;sp['validation_plan']=str((ROUND/'spec.json').relative_to(ROOT))
  sp['parameters'].update(start_utc=ISO(START),end_utc=ISO(CUT),observation_terminal_action='Mark only; no artificial liquidation; preserve units/cash for continuing frozen plan',qualification='Partial shadow snapshot; minimum180days not reached; no long-run pass/fail inference')
  path=ROUND/'specs'/f'forward_{asset}.json';path.write_text(json.dumps(sp,indent=2)+'\n');fp=registry.fingerprint(sp)
  result=subprocess.run(['python3','research/automation/registry.py','reserve',str(path)],cwd=ROOT,capture_output=True,text=True);assert result.returncode==0,result.stdout
  batch.append({'name':sp['name'],'spec':str(path.relative_to(ROOT)),'fingerprint':fp,'asset':asset,'capital_usdt':capital});print('reserved',asset,fp,flush=True)
 sp=json.loads((source/'specs/combo_n65_btc0.75.json').read_text());sp.update(name='forward_snapshot_combo',validation_plan=str((ROUND/'spec.json').relative_to(ROOT)))
 sp['parameters'].update(start_utc=ISO(START),end_utc=ISO(CUT),observation_terminal_action='Mark only; no artificial liquidation; preserve underlying units/cash')
 sp['components']=[{'fingerprint':b['fingerprint'],'weight':w} for b,w in zip(batch,(.75,.25))]
 path=ROUND/'specs/forward_combo.json';path.write_text(json.dumps(sp,indent=2)+'\n');result=subprocess.run(['python3','research/automation/registry.py','reserve',str(path)],cwd=ROOT,capture_output=True,text=True);assert result.returncode==0,result.stdout
 batch.append({'name':sp['name'],'spec':str(path.relative_to(ROOT)),'fingerprint':registry.fingerprint(sp),'capital_usdt':2000})
 (ROUND/'forward_batch.json').write_text(json.dumps(batch,indent=2)+'\n')

def observe(replay=False):
 batch=json.loads((ROUND/'forward_batch.json').read_text());records=registry.read_records(ROOT/'research/automation/registry.jsonl')
 for b in batch:assert records[b['fingerprint']]['status'] in (('rejected',) if replay else ('reserved',))
 started=datetime.now(timezone.utc).isoformat();inputs={};provenance=[]
 if replay:
  old=json.loads((ROUND/'forward_report.json').read_text());assert sha(ROUND/'forward_inputs.json.gz')==old['input_sha256'];inputs=json.loads(gzip.decompress((ROUND/'forward_inputs.json.gz').read_bytes()));provenance=old['provenance']
 else:
  for asset in ('BTC','ETH'):
   inputs[asset]={}
   for interval,begin,end in [('1d',START.replace(hour=0,minute=0)-timedelta(days=65),START.replace(hour=0,minute=0)),('1m',START.replace(hour=0,minute=0),CUT)]:
    params={'symbol':asset+'USDT','interval':interval,'startTime':int(begin.timestamp()*1000),'endTime':int(end.timestamp()*1000)-1,'limit':1000};url='https://data-api.binance.vision/api/v3/klines?'+urllib.parse.urlencode(params)
    with urllib.request.urlopen(url,timeout=20) as response:raw=response.read();status=response.status
    bars=json.loads(raw);assert status==200 and len(bars)==(65 if interval=='1d' else 100)
    step=86400000 if interval=='1d' else 60000
    assert [b[0] for b in bars]==list(range(params['startTime'],params['endTime']+1,step))
    assert all(b[6]==b[0]+step-1 and b[6]+1<=params['endTime']+1 for b in bars)
    inputs[asset][interval]=bars;provenance.append({'url':url,'status':status,'retrieved_utc':datetime.now(timezone.utc).isoformat(),'raw_response_sha256':hashlib.sha256(raw).hexdigest(),'bars':len(bars),'timestamp_unit':'milliseconds','closed_by_fixed_cutoff':True,'delayed_retrieval_after_start':True})
  writegz(ROUND/'forward_inputs.json.gz',inputs)
 original=json.loads(gzip.decompress((ROOT/'research/experiments/20261001T133655Z/daily_inputs.json.gz').read_bytes()))
 configs={};states={}
 for b in batch:
  if 'asset' not in b:continue
  asset=b['asset'];bars=inputs[asset]['1d'];minute=inputs[asset]['1m'];rows=[{'date':datetime.fromtimestamp(z[0]/1000,timezone.utc).strftime('%Y-%m-%d'),'close':z[4],'close_available_ts':(z[6]+1)*1000000,'quote_volume':z[7]} for z in bars]
  overlap={r['date']:r for r in original[asset]};matches=0
  for row in rows:
   if row['date'] in overlap:
    assert D(row['close'])==D(overlap[row['date']]['close']) and D(row['quote_volume'])==D(overlap[row['date']]['quote_volume']);matches+=1
  assert matches==49
  # The historical helper requires an extra completed daily row as an array bound.
  # At the first live day that row is unavailable; apply the identical one-step
  # rule directly to the65 real completed warmup closes,without inventing a bar.
  prior=[D(z['close']) for z in rows];sma=sum(prior)/65;mean=float(sma)
  desired,action=sig.step(False,prior[-1],sma,D('.01'))
  decision={'decision_index':65,'prior_close':str(prior[-1]),'sma':str(sma),'long':desired,'action':action}
  assert rows[-1]['close_available_ts']<int(START.timestamp()*1e9);adv,sigma=engine.lagged_cost_inputs(rows,65);ref=float(minute[1][1]);scenes={}
  for k in (1,2,3):
   cash=float(b['capital_usdt']);units=0.;trades=[];cost=0.
   if decision['long']:
    impact=.5*sigma*math.sqrt(cash/adv)*k;assert cash/adv<=.001;execution=ref*(1+(.0001+.0002)*k+impact);qty=cash/(execution*(1+.001*k));cost=cash-qty*ref
    trades=[{'side':'buy','reference':ref,'execution':execution,'quantity':qty,'fee_rate':.001*k,'half_spread_rate':.0001*k,'slippage_rate':.0002*k,'impact_rate':impact,'lagged_daily_quote_ADV':adv,'lagged_daily_volatility':sigma,'cost_usdt':cost,'executed_at_utc':ISO(START),'cash_after':0.,'units_after':qty}];cash=0.;units=qty
   vector=[float(b['capital_usdt']),cash+units*ref]+[cash+units*float(z[4]) for z in minute[1:]];assert len(vector)==101
   peak=vector[0];dd=0.
   for value in vector:peak=max(peak,value);dd=max(dd,1-value/peak)
   scenes[str(k)]={'net_return_pct':100*(vector[-1]/vector[0]-1),'max_drawdown_pct':dd*100,'equity_usdt':vector,'cost_usdt':cost,'cost_pct_initial':cost/b['capital_usdt']*100,'executions':len(trades),'round_trips':0,'trades':trades,'cash_usdt':cash,'units':units,'terminal_action':'mark only;no forced exit','Sharpe_CAGR_Calmar':None,'elapsed_complete_days':0,'elapsed_minutes':99}
  configs[b['name']]={**b,'decision':decision,'SMA_prior':mean,'prior_close':float(rows[-1]['close']),'49_prior_archive_days_matched':True,'scenes':scenes,'status':'rejected','reason':'Actual partial observation only;180days/sixfold qualification unavailable. Does not reject the frozen long-run plan.'};states[asset]=scenes
 b=batch[-1];scenes={}
 for k in ('1','2','3'):
  aa=states['BTC'][k];bb=states['ETH'][k];vector=[a+b for a,b in zip(aa['equity_usdt'],bb['equity_usdt'])];peak=vector[0];dd=0.
  for value in vector:peak=max(peak,value);dd=max(dd,1-value/peak)
  scenes[k]={'net_return_pct':100*(vector[-1]/2000-1),'max_drawdown_pct':dd*100,'equity_usdt':vector,'cost_usdt':aa['cost_usdt']+bb['cost_usdt'],'executions':aa['executions']+bb['executions'],'round_trips':0,'component_states':{'BTC':{'cash':aa['cash_usdt'],'units':aa['units']},'ETH':{'cash':bb['cash_usdt'],'units':bb['units']}},'elapsed_minutes':99,'elapsed_complete_days':0,'terminal_action':'mark only;no forced exit'}
 configs[b['name']]={**b,'scenes':scenes,'status':'rejected','reason':'Actual99minute snapshot;not eligible for180day/6fold validation;original plan remains active.'}
 report={'observation_started_utc':started,'frozen_plan_path':'research/experiments/20261001T113625Z/forward_plan.json','frozen_plan_sha256':sha(ROOT/'research/experiments/20261001T113625Z/forward_plan.json'),'start_utc':ISO(START),'cutoff_utc':ISO(CUT),'input_sha256':sha(ROUND/'forward_inputs.json.gz'),'provenance':provenance,'configs':configs,'validation':{'walk_forward':'Not available:99minutes,0complete days,not180days/sixfolds','sensitivity':'Original rules unchanged;no new forward sensitivity variants computed','costs':'All three stated cost scenes actually computed;zero fills,if present,do not empirically validate execution/capacity','interpretation':'Rules frozen before start,source data obtained after start:delayed shadow reconstruction,not real-time execution,live profit or untouched final historical holdout.'},'source_hashes':{str(p.relative_to(ROOT)):sha(p) for p in [ROUND/'forward.py',ROOT/'research/experiments/20261001T113625Z/signals.py',ROOT/'research/experiments/20261001T013355Z/evaluate.py']}}
 if replay:
  report['observation_started_utc']=old['observation_started_utc'];assert report==old;print('PASS:all9 frozen forward snapshot cost scenes exactly reproduced;no fresh request/ledger writes');return
 (ROUND/'forward_report.json').write_text(json.dumps(report,ensure_ascii=False,separators=(',',':'))+'\n');print(json.dumps({'snapshot_configs':3,'cost_scenes':9,'elapsed_minutes':99,'component_desired_long':{a:configs['forward_snapshot_'+a]['decision']['long'] for a in ('BTC','ETH')},'combo_return3_pct':scenes['3']['net_return_pct']}),flush=True)

if __name__=='__main__':
 if '--reserve' in sys.argv:reserve()
 else:observe('--reproduce' in sys.argv)
