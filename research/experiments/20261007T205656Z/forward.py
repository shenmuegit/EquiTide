"""Append only completed real minute marks to the unchanged original per-cost observer."""
import copy,gzip,hashlib,json,sys,urllib.parse,urllib.request
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ms=lambda s:int(datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()*1000)
iso=lambda t:datetime.fromtimestamp(t/1000,timezone.utc).isoformat().replace('+00:00','Z')
def gzwrite(p,x):
 with p.open('wb') as f:
  with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as z:z.write(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def dd(v):
 peak=v[0];loss=0.
 for x in v:peak=max(peak,x);loss=max(loss,1-x/peak)
 return loss*100

def main():
 replay='--reproduce' in sys.argv;plan=json.loads((ROUND/'spec.json').read_text());p=plan['forward_resume'];batch=json.loads((ROUND/'forward_batch.json').read_text());ledger=registry.read_records(ROOT/'research/automation/registry.jsonl')
 for b in batch:assert ledger[b['fingerprint']]['status'] in (('rejected',) if replay else ('reserved',))
 assert sha(ROOT/p['source_report'])==p['report_sha256'] and sha(ROOT/p['source_state'])==p['state_sha256']
 old=json.loads((ROOT/p['source_report']).read_text());state=json.loads((ROOT/p['source_state']).read_text());assert state['last_completed_mark_utc']==old['cutoff_utc']==p['resume_utc'];assert sha(ROOT/old['frozen_plan_path'])==old['frozen_plan_sha256']==state['frozen_plan_sha256']
 begin,cut=ms(p['resume_utc']),ms(p['cutoff_utc']);assert cut<=int(datetime.now(timezone.utc).timestamp()*1000) and cut<ms(state['next_daily_decision_utc'])
 started=datetime.now(timezone.utc).isoformat();provenance=[];inputs={}
 if replay:
  expected=json.loads((ROUND/'forward_report.json').read_text());assert sha(ROUND/'forward_inputs.json.gz')==expected['input_sha256'];inputs=json.loads(gzip.decompress((ROUND/'forward_inputs.json.gz').read_bytes()));provenance=expected['provenance'];started=expected['observation_started_utc']
 else:
  for asset in ('BTC','ETH'):
   params={'symbol':asset+'USDT','interval':'1m','startTime':begin-60000,'endTime':cut-1,'limit':1000};url='https://data-api.binance.vision/api/v3/klines?'+urllib.parse.urlencode(params)
   with urllib.request.urlopen(url,timeout=25) as response:raw=response.read();status=response.status
   assert status==200;bars=json.loads(raw);inputs[asset]=bars;path=ROUND/f'forward_response_{asset}_1m.json.gz'
   with path.open('wb') as f:
    with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as z:z.write(raw)
   provenance.append({'asset':asset,'interval':'1m','url':url,'status':status,'retrieved_utc':datetime.now(timezone.utc).isoformat(),'raw_response_sha256':hashlib.sha256(raw).hexdigest(),'raw_gzip_path':str(path.relative_to(ROOT)),'raw_gzip_sha256':sha(path),'bars':len(bars),'timestamp_unit':'milliseconds','closed_by_fixed_cutoff':True,'delayed_shadow_reconstruction':True})
  gzwrite(ROUND/'forward_inputs.json.gz',inputs)
 previous_inputs=json.loads(gzip.decompress((ROOT/old['source_inputs_path']).read_bytes()));configs={};oldpoints=p['prior_NAV_points'];newpoints=p['new_minutes'];totalminutes=p['cumulative_minutes'];totalpoints=p['total_NAV_points']
 assert cut-begin==newpoints*60000 and totalpoints==oldpoints+newpoints and totalminutes==old['configs']['forward_snapshot_combo']['scenes']['1']['elapsed_minutes']+newpoints
 for b in batch[:2]:
  asset=b['asset'];bars=inputs[asset];prev=previous_inputs[asset];prev=prev['1m'] if isinstance(prev,dict) else prev
  assert bars[0]==prev[-1] and [z[0] for z in bars]==list(range(begin-60000,cut,60000)) and len(bars)==newpoints+1
  assert all(z[6]+1==z[0]+60000 and z[6]+1<=cut for z in bars)
  cfg=copy.deepcopy(old['configs'][b['name']]);cfg.update(b)
  for k,s in cfg['scenes'].items():
   pos=state['positions_by_asset_and_cost'][asset][k];assert s['cash_usdt']==pos['cash_usdt'] and s['units']==pos['units'] and s['desired_long']==pos['desired_long']
   assert len(s['equity_usdt'])==oldpoints and s['equity_usdt'][-1]==pos['cash_usdt']+pos['units']*float(bars[0][4]);previous=s['equity_usdt'][-1]
   s['equity_usdt'] += [pos['cash_usdt']+pos['units']*float(z[4]) for z in bars[1:]];assert len(s['equity_usdt'])==totalpoints
   s.update(net_return_pct=100*(s['equity_usdt'][-1]/b['capital_usdt']-1),max_drawdown_pct=dd(s['equity_usdt']),elapsed_minutes=totalminutes,elapsed_complete_days=totalminutes//1440,new_mark_minutes=newpoints,new_reference_points=0,new_executions=0,since_previous_mark_return_pct=100*(s['equity_usdt'][-1]/previous-1))
  cfg['reason']='Actual cumulative8449minute partial shadow result;only5complete days insufficient180day/sixfold;original plan collecting.';configs[b['name']]=cfg
 b=batch[-1];cfg=copy.deepcopy(old['configs'][b['name']]);cfg.update(b)
 for k,s in cfg['scenes'].items():
  aa=configs['forward_snapshot_BTC']['scenes'][k];bb=configs['forward_snapshot_ETH']['scenes'][k];v=[a+b for a,b in zip(aa['equity_usdt'],bb['equity_usdt'])];previous=s['equity_usdt'][-1];assert v[:oldpoints]==s['equity_usdt']
  s.update(equity_usdt=v,net_return_pct=100*(v[-1]/2000-1),max_drawdown_pct=dd(v),elapsed_minutes=totalminutes,elapsed_complete_days=totalminutes//1440,new_mark_minutes=newpoints,new_reference_points=0,new_executions=0,since_previous_mark_return_pct=100*(v[-1]/previous-1))
 cfg['reason']='Actual8449minute cumulative partial snapshot;5complete days insufficient180day/sixfold;original plan collecting.';configs[b['name']]=cfg
 axis=[{'kind':'closed_minute_mark','open_ts_ms':z[0],'available_utc':iso(z[6]+1),'NAV_index':oldpoints+i} for i,z in enumerate(inputs['BTC'][1:])]
 report={'observation_started_utc':started,'frozen_plan_path':old['frozen_plan_path'],'frozen_plan_sha256':old['frozen_plan_sha256'],'start_utc':old['start_utc'],'resume_utc':p['resume_utc'],'cutoff_utc':p['cutoff_utc'],'source_report':p['source_report'],'source_report_sha256':p['report_sha256'],'source_state':p['source_state'],'source_state_sha256':p['state_sha256'],'input_sha256':sha(ROUND/'forward_inputs.json.gz'),'source_inputs_path':str((ROUND/'forward_inputs.json.gz').relative_to(ROOT)),'provenance':provenance,'append_axis':axis,'configs':configs,'validation':{'walk_forward':'Incomplete8449minutes/5complete days;no180day/sixfold qualification','sensitivity':'Original frozenSMA65/band1percent75/25 unchanged;no new forward variants','costs':'Original1/2/3x trades,costs preserved,zero new fills;no TCA/capacity proof','continuity':'8326oldNAVpoints exact prefix including all6prior daily references;130closedmarks appended to8456points,no daily reference or decisions in interval;cash/units/desired/trades unchanged,no forced sell','interpretation':'Delayed real-bar shadow reconstruction,no live orders,real-time execution proof or stable profit'},'source_hashes':{str(q.relative_to(ROOT)):sha(q) for q in [ROUND/'forward.py',ROUND/'audit_forward.py']}}
 nextstate=copy.deepcopy(state);nextstate.update(source_report=str((ROUND/'forward_report.json').relative_to(ROOT)),last_completed_mark_utc=p['cutoff_utc'],previous_state=p['source_state'],previous_state_sha256=p['state_sha256'],next_round='Continue these exact original per-cost positions,trades,costs,desired;append new closed marks beforeOct8UTC00:01.Next daily decision uses frozenSMA65/1percent,completed daily data and lagged20day cost.No rescaling/rebalance/restart/forced exit.Reserve each new cutoff first.')
 if replay:
  assert report==expected;nextstate['source_report_sha256']=sha(ROUND/'forward_report.json');assert nextstate==json.loads((ROUND/'forward_state.json').read_text());print('PASS:all9 cumulative forward scenes exactly reproduced including8456point prefix/time axis and nextstate;noHTTP or ledger write');return
 (ROUND/'forward_report.json').write_text(json.dumps(report,ensure_ascii=False,separators=(',',':'))+'\n');nextstate['source_report_sha256']=sha(ROUND/'forward_report.json');(ROUND/'forward_state.json').write_text(json.dumps(nextstate,indent=2)+'\n')
 print(json.dumps({'configs':3,'cost_scenes':9,'cumulative_minutes':totalminutes,'complete_days':totalminutes//1440,'new_closed_minutes':newpoints,'NAV_points':totalpoints,'new_daily_decisions':0,'new_executions':0,'combo_net_returns_pct':{k:z['net_return_pct'] for k,z in configs['forward_snapshot_combo']['scenes'].items()}}),flush=True)
if __name__=='__main__':main()
