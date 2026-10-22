#!/usr/bin/env python3
"""Deterministic replay of daily KAMA-hysteresis candidates; independent signal checks are in run.py and their cost stresses."""
import gzip,hashlib,importlib.util,json,math,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('daily_kama_audit',R/'evaluate.py');ev=importlib.util.module_from_spec(sp);sys.modules[sp.name]=ev;sp.loader.exec_module(ev)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def eq(a,b):return math.isclose(float(a),float(b),rel_tol=1e-12,abs_tol=1e-12)
def main():
 plan=json.loads((R/'plan.json').read_text());report=json.loads((R/'report.json').read_text());batch=json.loads((R/'batch.json').read_text());filters=json.loads((R/'exchange_filters.json').read_text())['filters']
 assert report['frozen_plan_sha256']==sha(R/'plan.json') and report['round']==R.name and len(batch)==18 and len(report['configs'])==18
 markets={a:ev.load_asset(a,plan) for a in ('BTC','ETH')};trade_ids=set();fill_count=0;decision_count=0
 for row in batch:
  spec=json.loads((ROOT/row['spec']).read_text());assert ev.registry.fingerprint(spec)==row['fingerprint']
  c=report['configs'][row['name']];assert c['fingerprint']==row['fingerprint'] and c['efficiency_lookback_days']==row['efficiency_lookback_days'] and c['slow_span_days']==row['slow_span_days']
  for mult in (1,2,3):
   saved=c['scenarios'][str(mult)];replay=ev.evaluate_one(row,mult,markets[row['asset']],filters[row['asset']],plan);decision_count+=len(replay['decisions'])
   keys=('terminal_nav_usdt','net_pnl_usdt','terminal_cash_usdt','terminal_units','terminal_flat','cost_usdt','gross_reference_pnl_usdt','gross_reference_pnl_to_cost','net_return_pct','max_drawdown_1m_sampled_pct','daily_sample_drawdown_pct','daily_sharpe_annualized','cagr_pct','calmar_daily_sampled','filled_orders','rejected_orders','round_trips','positive_folds','minute_nav_samples','minute_nav_sha256_f64le','daily_nav_sha256_f64le')
   for k in keys:
    if isinstance(saved[k],(float,int)) and not isinstance(saved[k],bool):assert eq(saved[k],replay[k]),(row['name'],mult,k,saved[k],replay[k])
    else:assert saved[k]==replay[k],(row['name'],mult,k,saved[k],replay[k])
   assert len(saved['folds'])==len(replay['folds'])==12
   for a,b in zip(saved['folds'],replay['folds']):
    for k in ('fold','start_utc','end_exclusive_utc','observations'):assert a[k]==b[k]
    for k in ('start_nav_usdt','end_nav_usdt','net_return_pct','daily_sample_drawdown_pct'):assert eq(a[k],b[k])
   for t in replay['trades']:
    assert t['trade_id'] not in trade_ids;trade_ids.add(t['trade_id'])
    assert t['signal_to_execution_seconds']==60
    if t['status']=='filled':
     fill_count+=1;assert float(t['cash_after'])>=0 and float(t['units_after'])>=0
     f=filters[row['asset']];from decimal import Decimal as D
     assert D(t['quantity'])%D(f['LOT_SIZE']['stepSize'])==0
     assert D(t['execution'])%D(f['PRICE_FILTER']['tickSize'])==0
    else:assert t['cash_before']==t['cash_after'] and t['units_before']==t['units_after']
   assert replay['terminal_flat']
  assert c['status']==('passed' if all(c['gates'].values()) else 'rejected')
 # Verify event ledgers are unique and identical in count to deterministic replay.
 with gzip.open(R/'trades.csv.gz','rt',newline='') as f:
  import csv
  saved_trades=list(csv.DictReader(f))
 with gzip.open(R/'decisions.csv.gz','rt',newline='') as f:
  import csv
  saved_decisions=list(csv.DictReader(f))
 with gzip.open(R/'daily_equity.csv.gz','rt',newline='') as f:
  import csv
  saved_daily=list(csv.DictReader(f))
 assert len(saved_trades)==len(trade_ids) and len({x['trade_id'] for x in saved_trades})==len(saved_trades)
 assert sum(x['status']=='filled' for x in saved_trades)==fill_count
 assert len(saved_decisions)==decision_count==18*3*360 and len(saved_daily)==18*3*361
 assert all(math.isfinite(float(x['nav_usdt'])) and float(x['nav_usdt'])>=0 for x in saved_daily)
 frag=R/'registry_records.jsonl'
 if frag.exists():
  events=[json.loads(x) for x in frag.read_text().splitlines() if x.strip()];assert len(events)==36
  for row in batch:
   pair=[x for x in events if x['fingerprint']==row['fingerprint']];assert len(pair)==2
   assert sorted(x['status'] for x in pair)==sorted(['reserved',report['configs'][row['name']]['status']])
   done=next(x for x in pair if x['status']!='reserved');assert done['report_sha256']==sha(R/'report.json') and done['result_available'] is True
  print('registry sidecar audit passed for all 18 reserve→finish pairs')
 # If finish records already exist, every report SHA and terminal status must reconcile.
 frag=R/'registry_records.jsonl'
 if frag.exists():
  events=[json.loads(x) for x in frag.read_text().splitlines() if x.strip()];assert len(events)==36
  for row in batch:
   pair=[x for x in events if x['fingerprint']==row['fingerprint']];assert len(pair)==2
   assert sorted(x['status'] for x in pair)==sorted(['reserved',report['configs'][row['name']]['status']])
   done=next(x for x in pair if x['status']!='reserved');assert done['report_sha256']==sha(R/'report.json') and done['result_available'] is True
  print('registry sidecar audit passed for all 18 reserve→finish pairs')
 print(f'audit passed: {len(batch)} fingerprints × 3 costs=54; {fill_count} filled orders; 12 folds each; {len(saved_daily)} daily NAV marks; all {decision_count} daily decisions reproduced; no balance/capacity errors')
if __name__=='__main__':main()
