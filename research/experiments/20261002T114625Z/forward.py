"""Continue original per-cost floating-quantity shadow positions without new orders."""
import copy,gzip,hashlib,json,math,sys,urllib.parse,urllib.request
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def gzwrite(p,x):
 with p.open('wb') as f:
  with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as z:z.write(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def dd(v):
 peak=v[0];drawdown=0.
 for x in v:peak=max(peak,x);drawdown=max(drawdown,1-x/peak)
 return drawdown*100

def main():
 replay='--reproduce' in sys.argv;plan=json.loads((ROUND/'spec.json').read_text());p=plan['forward_resume'];batch=json.loads((ROUND/'forward_batch.json').read_text());ledger=registry.read_records(ROOT/'research/automation/registry.jsonl')
 for b in batch:assert ledger[b['fingerprint']]['status'] in (('rejected',) if replay else ('reserved',))
 assert sha(ROOT/p['source_report'])==p['report_sha256'] and sha(ROOT/p['source_state'])==p['state_sha256']
 old=json.loads((ROOT/p['source_report']).read_text());state=json.loads((ROOT/p['source_state']).read_text());assert state['last_completed_mark_utc']==old['cutoff_utc']==p['resume_utc'];assert sha(ROOT/old['frozen_plan_path'])==old['frozen_plan_sha256']==state['frozen_plan_sha256']
 begin=int(datetime.fromisoformat(p['resume_utc'].replace('Z','+00:00')).timestamp()*1000);cut=int(datetime.fromisoformat(p['cutoff_utc'].replace('Z','+00:00')).timestamp()*1000);assert cut<=int(datetime.now(timezone.utc).timestamp()*1000)
 assert p['cutoff_utc']<state['next_daily_decision_utc'];started=datetime.now(timezone.utc).isoformat();provenance=[];inputs={}
 if replay:
  expected=json.loads((ROUND/'forward_report.json').read_text());assert sha(ROUND/'forward_inputs.json.gz')==expected['input_sha256'];inputs=json.loads(gzip.decompress((ROUND/'forward_inputs.json.gz').read_bytes()));provenance=expected['provenance'];started=expected['observation_started_utc']
 else:
  for asset in ('BTC','ETH'):
   params={'symbol':asset+'USDT','interval':'1m','startTime':begin-60000,'endTime':cut-1,'limit':1000};url='https://data-api.binance.vision/api/v3/klines?'+urllib.parse.urlencode(params)
   with urllib.request.urlopen(url,timeout=25) as response:raw=response.read();status=response.status
   assert status==200;bars=json.loads(raw);inputs[asset]=bars
   rawpath=ROUND/f'forward_response_{asset}_1m.json.gz'
   with rawpath.open('wb') as f:
    with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as z:z.write(raw)
   provenance.append({'asset':asset,'url':url,'status':status,'retrieved_utc':datetime.now(timezone.utc).isoformat(),'raw_response_sha256':hashlib.sha256(raw).hexdigest(),'raw_gzip_path':str(rawpath.relative_to(ROOT)),'raw_gzip_sha256':sha(rawpath),'bars':len(bars),'timestamp_unit':'milliseconds','closed_by_fixed_cutoff':True,'delayed_shadow_reconstruction':True})
  gzwrite(ROUND/'forward_inputs.json.gz',inputs)
 prior_inputs=json.loads(gzip.decompress((ROOT/old['source_inputs_path']).read_bytes())) if 'source_inputs_path' in old else json.loads(gzip.decompress((ROOT/Path(p['source_report']).parent/'forward_inputs.json.gz').read_bytes()))
 configs={}
 for b in batch[:2]:
  asset=b['asset'];bars=inputs[asset];assert [z[0] for z in bars]==list(range(begin-60000,cut,60000)) and len(bars)==121
  assert all(z[6]+1==z[0]+60000 and z[6]+1<=cut for z in bars)
  priorbars=prior_inputs[asset];priorbars=priorbars['1m'] if isinstance(priorbars,dict) else priorbars
  assert bars[0]==priorbars[-1]
  cfg=copy.deepcopy(old['configs'][b['name']]);cfg.update(b)
  for k,s in cfg['scenes'].items():
   position=state['positions_by_asset_and_cost'][asset][k];assert s['cash_usdt']==position['cash_usdt'] and s['units']==position['units'] and position['desired_long']
   assert s['equity_usdt'][-1]==s['cash_usdt']+s['units']*float(bars[0][4]);previous=s['equity_usdt'][-1]
   s['equity_usdt'] += [s['cash_usdt']+s['units']*float(z[4]) for z in bars[1:]]
   assert len(s['equity_usdt'])==701;s.update(net_return_pct=100*(s['equity_usdt'][-1]/b['capital_usdt']-1),max_drawdown_pct=dd(s['equity_usdt']),elapsed_minutes=699,new_mark_minutes=120,new_executions=0,since_previous_mark_return_pct=100*(s['equity_usdt'][-1]/previous-1))
  cfg['reason']='Actual cumulative699minute partial shadow result;not180day/sixfold qualification. Does not cancel frozen long-run plan.';configs[b['name']]=cfg
 b=batch[-1];cfg=copy.deepcopy(old['configs'][b['name']]);cfg.update(b)
 for k,s in cfg['scenes'].items():
  aa=configs['forward_snapshot_BTC']['scenes'][k];bb=configs['forward_snapshot_ETH']['scenes'][k];v=[a+b for a,b in zip(aa['equity_usdt'],bb['equity_usdt'])];prior=s['equity_usdt'][-1]
  assert v[:581]==s['equity_usdt'];s.update(equity_usdt=v,net_return_pct=100*(v[-1]/2000-1),max_drawdown_pct=dd(v),elapsed_minutes=699,new_mark_minutes=120,new_executions=0,since_previous_mark_return_pct=100*(v[-1]/prior-1))
 cfg['reason']='Actual cumulative699minute partial observation;not eligible for180days/sixfold;long-run plan remains collecting';configs[b['name']]=cfg
 report={'observation_started_utc':started,'frozen_plan_path':old['frozen_plan_path'],'frozen_plan_sha256':old['frozen_plan_sha256'],'start_utc':old['start_utc'],'resume_utc':p['resume_utc'],'cutoff_utc':p['cutoff_utc'],'source_report':p['source_report'],'source_report_sha256':p['report_sha256'],'source_state':p['source_state'],'source_state_sha256':p['state_sha256'],'input_sha256':sha(ROUND/'forward_inputs.json.gz'),'source_inputs_path':str((ROUND/'forward_inputs.json.gz').relative_to(ROOT)),'provenance':provenance,'configs':configs,'validation':{'walk_forward':'Incomplete:699minutes,0full days;no180day/6fold qualification','sensitivity':'Frozen original rule unchanged;no new forward sensitivity variants','costs':'Cumulative1/2/3x costs retained from actual initial simulated buys;zero NEW executions this interval,not empirical execution/capacity confirmation','continuity':'Original cash,units,desired-state and trade/cost history preserved;no reset or duplicate buy;old581NAVpoints exact prefix,new120closedmarks appended','interpretation':'Delayed shadow reconstruction;no real orders,real-time execution proof or stable live profit'},'source_hashes':{str((ROUND/'forward.py').relative_to(ROOT)):sha(ROUND/'forward.py')}}
 if replay:assert report==expected;print('PASS:all9 cumulative forward scenes exactly reproduced from archived new minutes and old positions;no fresh request or ledger write');return
 (ROUND/'forward_report.json').write_text(json.dumps(report,ensure_ascii=False,separators=(',',':'))+'\n')
 nextstate=copy.deepcopy(state);nextstate.update(source_report=str((ROUND/'forward_report.json').relative_to(ROOT)),source_report_sha256=sha(ROUND/'forward_report.json'),last_completed_mark_utc=p['cutoff_utc'],previous_state=p['source_state'],previous_state_sha256=p['state_sha256'])
 (ROUND/'forward_state.json').write_text(json.dumps(nextstate,indent=2)+'\n')
 print(json.dumps({'configs':3,'cost_scenes':9,'cumulative_minutes':699,'new_closed_minutes':120,'new_executions':0,'combo_net_returns_pct':{k:s['net_return_pct'] for k,s in configs['forward_snapshot_combo']['scenes'].items()}}),flush=True)
if __name__=='__main__':main()
