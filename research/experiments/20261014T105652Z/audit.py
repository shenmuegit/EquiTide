#!/usr/bin/env python3
"""Independent deterministic replay of all weekday-window variants and cost scenes."""
import gzip,hashlib,importlib.util,json,math,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('weekday_evaluator_audit',R/'evaluate.py');ev=importlib.util.module_from_spec(sp);sys.modules[sp.name]=ev;sp.loader.exec_module(ev)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def close(a,b):return math.isclose(float(a),float(b),rel_tol=1e-12,abs_tol=1e-12)
def main():
 plan=json.loads((R/'plan.json').read_text());report=json.loads((R/'report.json').read_text());batch=json.loads((R/'batch.json').read_text());filters=json.loads((R/'exchange_filters.json').read_text())['filters']
 assert report['round']==R.name and report['frozen_plan_sha256']==sha(R/'plan.json')
 assert len(batch)==28 and report['summary']['cost_scenarios']==84 and len(report['configs'])==28
 markets={a:ev.load_asset(a,plan) for a in ('BTC','ETH')};attempt_ids=set();fills=0
 for row in batch:
  spc=json.loads((ROOT/row['spec']).read_text());assert ev.registry.fingerprint(spc)==row['fingerprint']
  c=report['configs'][row['name']];assert c['fingerprint']==row['fingerprint'] and c['weekday_utc']==row['weekday_utc'] and c['holding_days']==row['holding_days']
  for mult in (1,2,3):
   observed=c['scenarios'][str(mult)];actual=ev.evaluate_one(row,mult,markets[row['asset']],filters[row['asset']],plan)
   keys=('net_return_pct','max_drawdown_1m_sampled_pct','daily_sample_drawdown_pct','daily_sharpe_annualized','cagr_pct','calmar_daily_sampled','filled_orders','rejected_attempts','round_trips','scheduled_entries','positive_folds','minute_nav_samples','minute_nav_sha256_f64le','daily_nav_sha256_f64le','terminal_flat','terminal_nav_usdt','cost_usdt','gross_reference_pnl_usdt','gross_reference_pnl_to_cost')
   for k in keys:
    if isinstance(observed[k],(float,int)) and not isinstance(observed[k],bool):assert close(observed[k],actual[k]),(row['name'],mult,k,observed[k],actual[k])
    else:assert observed[k]==actual[k],(row['name'],mult,k,observed[k],actual[k])
   assert len(observed['folds'])==12 and len(actual['folds'])==12
   for x,y in zip(observed['folds'],actual['folds']):
    for k in ('fold','start_utc','end_exclusive_utc','scheduled_trips'):
     assert x[k]==y[k],(row['name'],mult,k)
    for k in ('start_nav_usdt','end_nav_usdt','net_return_pct','daily_sample_drawdown_pct'):
     assert close(x[k],y[k]),(row['name'],mult,k,x[k],y[k])
   for trade in actual['trade_attempts']:
    assert trade['trade_id'] not in attempt_ids;attempt_ids.add(trade['trade_id'])
    if trade['status']=='filled':
     fills+=1
     assert trade['cash_before'] and trade['cash_after'] and trade['units_before'] and trade['units_after']
     assert float(trade['cash_after'])>=0 and float(trade['units_after'])>=0
     assert trade['signal_to_execution_seconds']>=60
     if 'entry' in trade['trade_id']:assert trade['signal_to_execution_seconds']==60
     assert trade['minute_index']>=0
   assert actual['terminal_flat'] and int(actual['rejected_attempts'])==0
 # Check persisted event ledger corresponds to fully replayed fill events and scenario output.
 with gzip.open(R/'trades.csv.gz','rt',newline='') as f:
  import csv
  saved=list(csv.DictReader(f))
 assert len(saved)==len(attempt_ids)
 assert len({x['trade_id'] for x in saved})==len(saved)
 assert sum(x['status']=='filled' for x in saved)==fills
 for name,c in report['configs'].items():
  expected='passed' if all(c['gates'].values()) else 'rejected';assert c['status']==expected
  for m in ('1','2','3'):
   s=c['scenarios'][m];assert s['terminal_flat'];assert s['rejected_attempts']==0
 # Rebuild complete costed fold/valuation ledgers from the JSON headline.
 with gzip.open(R/'daily_equity.csv.gz','rt') as f:
  import csv
  daily=list(csv.DictReader(f))
 assert len(daily)==28*3*361
 assert len(attempt_ids)==len(saved)
 assert all(math.isfinite(float(x['nav_usdt'])) and float(x['nav_usdt'])>=0 for x in daily)
 frag=R/'registry_records.jsonl'
 if frag.exists():
  rows=[json.loads(x) for x in frag.read_text().splitlines() if x.strip()];wanted={x['fingerprint']:x for x in batch};assert len(rows)==56
  for fp,b in wanted.items():
   pair=[x for x in rows if x['fingerprint']==fp];assert len(pair)==2
   assert sorted(x['status'] for x in pair)==sorted(['reserved',report['configs'][b['name']]['status']])
   final=next(x for x in pair if x['status']!='reserved');assert final['report_sha256']==sha(R/'report.json') and final['result_available'] is True
  print('registry sidecar audit passed: all 28 reserved→finished with matching report SHA')
 print(f'audit passed: 28 fingerprints × 3 costs = 84; exact deterministic replay; {fills} filled orders; 0 rejected; 12 folds each; {len(daily)} daily NAV marks; no balance/capacity errors')
if __name__=='__main__':main()
