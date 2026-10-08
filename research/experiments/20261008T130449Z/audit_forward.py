"""Independent original frozen account, closed-bar provenance and prefix preservation audit."""
import gzip,hashlib,json,sys,urllib.parse
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ms=lambda s:int(datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()*1000)
iso=lambda t:datetime.fromtimestamp(t/1000,timezone.utc).isoformat().replace('+00:00','Z')
def main():
 r=json.loads((ROUND/'forward_report.json').read_text());prior=json.loads((ROOT/r['source_report']).read_text());state=json.loads((ROOT/r['source_state']).read_text());nextstate=json.loads((ROUND/'forward_state.json').read_text());data=json.loads(gzip.decompress((ROUND/'forward_inputs.json.gz').read_bytes()));oldinputs=json.loads(gzip.decompress((ROOT/prior['source_inputs_path']).read_bytes()));batch=json.loads((ROUND/'forward_batch.json').read_text());raw=[json.loads(x) for x in (ROOT/'research/automation/registry.jsonl').read_text().splitlines()];ledger=registry.read_records(ROOT/'research/automation/registry.jsonl')
 for p,h in r['source_hashes'].items():assert sha(ROOT/p)==h
 assert sha(ROOT/r['source_report'])==r['source_report_sha256'] and sha(ROOT/r['source_state'])==r['source_state_sha256'] and sha(ROUND/'forward_inputs.json.gz')==r['input_sha256']
 assert sha(ROOT/r['frozen_plan_path'])==r['frozen_plan_sha256']=='2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81'
 assert nextstate['positions_by_asset_and_cost']==state['positions_by_asset_and_cost'];assert nextstate['next_daily_decision_utc']==state['next_daily_decision_utc']=='2026-10-09T00:01:00Z'
 assert nextstate['source_report_sha256']==sha(ROUND/'forward_report.json') and nextstate['last_completed_mark_utc']==r['cutoff_utc'];begin,cut=ms(r['resume_utc']),ms(r['cutoff_utc']);assert cut-begin==120*60000 and cut<ms(state['next_daily_decision_utc'])
 assert len(r['provenance'])==2
 for p in r['provenance']:
  bb=gzip.decompress((ROOT/p['raw_gzip_path']).read_bytes());assert hashlib.sha256(bb).hexdigest()==p['raw_response_sha256'] and sha(ROOT/p['raw_gzip_path'])==p['raw_gzip_sha256'] and json.loads(bb)==data[p['asset']]
  q=urllib.parse.parse_qs(urllib.parse.urlparse(p['url']).query);assert q['symbol']==[p['asset']+'USDT'] and q['interval']==['1m'] and int(q['startTime'][0])==begin-60000 and int(q['endTime'][0])==cut-1
  assert p['status']==200 and p['timestamp_unit']=='milliseconds' and p['retrieved_utc']>r['cutoff_utc']
 for b in batch:
  fp=b['fingerprint'];assert registry.fingerprint(json.loads((ROOT/b['spec']).read_text()))==fp
  reserves=[x for x in raw if x['fingerprint']==fp and x['status']=='reserved'];assert len(reserves)==1 and reserves[0]['recorded_at_utc']<r['observation_started_utc']
  if ledger[fp]['status']!='reserved':assert ledger[fp]['status']=='rejected' and ledger[fp]['report_sha256']==sha(ROUND/'forward_report.json')
 axis=[{'kind':'closed_minute_mark','open_ts_ms':z[0],'available_utc':iso(z[6]+1),'NAV_index':9307+i} for i,z in enumerate(data['BTC'][1:])];assert r['append_axis']==axis and len(axis)==120
 for asset in ('BTC','ETH'):
  bars=data[asset];oldbars=oldinputs[asset];oldbars=oldbars['1m'] if isinstance(oldbars,dict) else oldbars
  assert bars[0]==oldbars[-1] and len(bars)==121 and [z[0] for z in bars]==list(range(begin-60000,cut,60000))
  assert all(z[6]+1==z[0]+60000 and z[6]+1<=cut and float(z[3])<=float(z[4])<=float(z[2]) and float(z[4])>0 for z in bars)
  c=r['configs']['forward_snapshot_'+asset];oldc=prior['configs']['forward_snapshot_'+asset];assert c['decision']==oldc['decision'] and c['latest_daily_decision']==oldc['latest_daily_decision']
  for k,s in c['scenes'].items():
   old=oldc['scenes'][k];pos=state['positions_by_asset_and_cost'][asset][k];v=old['equity_usdt']+[pos['cash_usdt']+pos['units']*float(z[4]) for z in bars[1:]]
   assert s['equity_usdt']==v and s['equity_usdt'][:9307]==old['equity_usdt']
   for field in ('cash_usdt','units','desired_long','trades','executions','round_trips','cost_usdt','cost_pct_initial'):assert s[field]==old[field],field
   assert s['cash_usdt']==pos['cash_usdt'] and s['units']==pos['units'] and s['desired_long']==pos['desired_long']
 assert [z[0] for z in data['BTC']]==[z[0] for z in data['ETH']]
 for k,s in r['configs']['forward_snapshot_combo']['scenes'].items():
  a=r['configs']['forward_snapshot_BTC']['scenes'][k];b=r['configs']['forward_snapshot_ETH']['scenes'][k];old=prior['configs']['forward_snapshot_combo']['scenes'][k]
  assert s['equity_usdt']==[x+y for x,y in zip(a['equity_usdt'],b['equity_usdt'])] and s['equity_usdt'][:9307]==old['equity_usdt']
  assert s['cost_usdt']==a['cost_usdt']+b['cost_usdt'] and s['executions']==a['executions']+b['executions'] and s['round_trips']==a['round_trips']+b['round_trips']
  assert s['component_states']==old['component_states'] and s['cost_usdt']==old['cost_usdt'] and s['cost_pct_initial']==old['cost_pct_initial']
 for c in r['configs'].values():
  for s in c['scenes'].values():
   v=s['equity_usdt'];assert len(v)==9427 and s['elapsed_minutes']==9419 and s['elapsed_complete_days']==6 and s['new_mark_minutes']==120 and s['new_reference_points']==0 and s['new_executions']==0
   assert abs(s['net_return_pct']-100*(v[-1]/c['capital_usdt']-1))<1e-12;loss=max(100*(1-x/max(v[:i+1])) for i,x in enumerate(v));assert abs(loss-s['max_drawdown_pct'])<1e-12;assert s['terminal_action']=='mark only;no forced exit'
 print(json.dumps({'passed':True,'forward_scenes':9,'new_closed_marks_per_asset':120,'cumulative_minutes':9419,'complete_days':6,'NAV_points_per_scene':9427,'original_NAV_prefix':9307,'new_daily_decisions':0,'new_reference_points':0,'new_executions':0,'original_cash_units_desired_trades_costs_unchanged':True,'next_daily_decision_utc':nextstate['next_daily_decision_utc'],'report_sha256':sha(ROUND/'forward_report.json')}),flush=True)
if __name__=='__main__':main()
