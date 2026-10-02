"""Independent closed-minute prefix, cumulative accounting and no-repeat-buy audit."""
import gzip,hashlib,json,math,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 r=json.loads((ROUND/'forward_report.json').read_text());prior=json.loads((ROOT/r['source_report']).read_text());state=json.loads((ROOT/r['source_state']).read_text());nextstate=json.loads((ROUND/'forward_state.json').read_text());data=json.loads(gzip.decompress((ROUND/'forward_inputs.json.gz').read_bytes()));batch=json.loads((ROUND/'forward_batch.json').read_text());raw=[json.loads(x) for x in (ROOT/'research/automation/registry.jsonl').read_text().splitlines()];ledger=registry.read_records(ROOT/'research/automation/registry.jsonl')
 assert sha(ROOT/r['source_report'])==r['source_report_sha256'] and sha(ROOT/r['source_state'])==r['source_state_sha256'] and sha(ROUND/'forward_inputs.json.gz')==r['input_sha256']
 assert sha(ROOT/r['frozen_plan_path'])==r['frozen_plan_sha256'];assert nextstate['positions_by_asset_and_cost']==state['positions_by_asset_and_cost'];assert nextstate['source_report_sha256']==sha(ROUND/'forward_report.json') and nextstate['last_completed_mark_utc']==r['cutoff_utc']
 cut=int(datetime.fromisoformat(r['cutoff_utc'].replace('Z','+00:00')).timestamp()*1000);begin=int(datetime.fromisoformat(r['resume_utc'].replace('Z','+00:00')).timestamp()*1000)
 for p in r['provenance']:
  b=gzip.decompress((ROOT/p['raw_gzip_path']).read_bytes());assert hashlib.sha256(b).hexdigest()==p['raw_response_sha256'];assert sha(ROOT/p['raw_gzip_path'])==p['raw_gzip_sha256'];assert json.loads(b)==data[p['asset']]
 for b in batch:
  fp=b['fingerprint'];assert registry.fingerprint(json.loads((ROOT/b['spec']).read_text()))==fp
  reserved=[x for x in raw if x['fingerprint']==fp and x['status']=='reserved'];assert len(reserved)==1 and reserved[0]['recorded_at_utc']<r['observation_started_utc']
  if ledger[fp]['status']!='reserved':assert ledger[fp]['status']=='rejected' and ledger[fp]['report_sha256']==sha(ROUND/'forward_report.json')
 for asset in ('BTC','ETH'):
  bars=data[asset];assert len(bars)==121 and [z[0] for z in bars]==list(range(begin-60000,cut,60000));assert all(z[6]+1==z[0]+60000 and float(z[3])<=float(z[4])<=float(z[2]) and float(z[4])>0 for z in bars)
  for k,s in r['configs']['forward_snapshot_'+asset]['scenes'].items():
   old=prior['configs']['forward_snapshot_'+asset]['scenes'][k];pos=state['positions_by_asset_and_cost'][asset][k]
   assert s['equity_usdt'][:821]==old['equity_usdt'];assert s['trades']==old['trades'] and s['cost_usdt']==old['cost_usdt'];assert s['units']==pos['units'] and s['cash_usdt']==pos['cash_usdt'] and s['executions']==1 and s['new_executions']==0 and s['elapsed_minutes']==939
   assert s['equity_usdt'][821:]==[pos['cash_usdt']+pos['units']*float(z[4]) for z in bars[1:]]
 for k,s in r['configs']['forward_snapshot_combo']['scenes'].items():
  a=r['configs']['forward_snapshot_BTC']['scenes'][k];b=r['configs']['forward_snapshot_ETH']['scenes'][k];assert s['equity_usdt']==[x+y for x,y in zip(a['equity_usdt'],b['equity_usdt'])] and s['cost_usdt']==a['cost_usdt']+b['cost_usdt'] and s['executions']==2 and s['new_executions']==0
 for cfg in r['configs'].values():
  for s in cfg['scenes'].values():
   v=s['equity_usdt'];assert len(v)==941 and abs(s['net_return_pct']-100*(v[-1]/cfg['capital_usdt']-1))<1e-12;drawdown=max(100*(1-x/max(v[:i+1])) for i,x in enumerate(v));assert abs(drawdown-s['max_drawdown_pct'])<1e-12
 print(json.dumps({'passed':True,'forward_scenes':9,'new_closed_marks_per_asset':120,'cumulative_minutes':939,'prior_NAV_prefix_and_positions_unchanged':True,'new_executions':0,'report_sha256':sha(ROUND/'forward_report.json')}),flush=True)
if __name__=='__main__':main()
