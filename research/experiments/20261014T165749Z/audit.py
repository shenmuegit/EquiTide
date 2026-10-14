#!/usr/bin/env python3
"""Independent deterministic replay of ATR-breakout variants, filters, costs, and ledgers."""
import gzip,hashlib,importlib.util,json,math,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('atr_trailing_auditor',R/'evaluate.py');ev=importlib.util.module_from_spec(sp);sys.modules[sp.name]=ev;sp.loader.exec_module(ev)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def eq(a,b):return math.isclose(float(a),float(b),rel_tol=1e-12,abs_tol=1e-12)
def main():
 plan=json.loads((R/'plan.json').read_text());report=json.loads((R/'report.json').read_text());batch=json.loads((R/'batch.json').read_text());filters=json.loads((R/'exchange_filters.json').read_text())['filters']
 assert report['round']==R.name and report['frozen_plan_sha256']==sha(R/'plan.json') and len(batch)==36 and len(report['configs'])==36
 markets={a:ev.load_asset(a,plan) for a in ('BTC','ETH')};tradeids=set();fill_count=0;decision_count=0
 for asset,m in markets.items():
  for n in plan['grid']['wilder_atr_periods']:
   atr,tr=ev.wilder_atr(m,n)
   assert len(atr)==len(tr)==730 and math.isnan(atr[n-1]) and eq(atr[n],sum(tr[1:n+1])/n)
   for j in range(n+1,len(tr)):assert eq(atr[j],((n-1)*atr[j-1]+tr[j])/n)
 for row in batch:
  spec=json.loads((ROOT/row['spec']).read_text());assert ev.registry.fingerprint(spec)==row['fingerprint']
  c=report['configs'][row['name']];assert c['fingerprint']==row['fingerprint'] and c['entry_lookback_days']==row['entry_lookback_days'] and c['atr_period']==row['atr_period'] and c['stop_multiple']==row['stop_multiple']
  for mult in (1,2,3):
   saved=c['scenarios'][str(mult)];replay=ev.evaluate_one(row,mult,markets[row['asset']],filters[row['asset']],plan);decision_count+=len(replay['decisions'])
   for k in ('terminal_nav_usdt','net_pnl_usdt','terminal_cash_usdt','terminal_units','terminal_flat','cost_usdt','gross_reference_pnl_usdt','gross_reference_pnl_to_cost','net_return_pct','max_drawdown_1m_sampled_pct','daily_sample_drawdown_pct','daily_sharpe_annualized','cagr_pct','calmar_daily_sampled','filled_orders','rejected_orders','round_trips','positive_folds','minute_nav_samples','minute_nav_sha256_f64le','daily_nav_sha256_f64le'):
    a=saved[k];b=replay[k]
    if isinstance(a,(int,float)) and not isinstance(a,bool):assert eq(a,b),(row['name'],mult,k,a,b)
    else:assert a==b,(row['name'],mult,k,a,b)
   assert len(saved['folds'])==len(replay['folds'])==12
   for a,b in zip(saved['folds'],replay['folds']):
    for k in ('fold','start_utc','end_exclusive_utc','observations'):assert a[k]==b[k]
    for k in ('start_nav_usdt','end_nav_usdt','net_return_pct','daily_sample_drawdown_pct'):assert eq(a[k],b[k])
   for t in replay['trades']:
    assert t['trade_id'] not in tradeids;tradeids.add(t['trade_id']);assert t['signal_to_execution_seconds']==60
    if t['status']=='filled':
     fill_count+=1;assert float(t['cash_after'])>=0 and float(t['units_after'])>=0
     f=filters[row['asset']];from decimal import Decimal as D
     assert D(t['quantity'])%D(f['LOT_SIZE']['stepSize'])==0 and D(t['execution'])%D(f['PRICE_FILTER']['tickSize'])==0
    else:assert t['cash_before']==t['cash_after'] and t['units_before']==t['units_after']
   assert replay['terminal_flat'] and replay['rejected_orders']==0
  assert c['status']==('passed' if all(c['gates'].values()) else 'rejected')
 with gzip.open(R/'trades.csv.gz','rt',newline='') as f:
  import csv
  saved_trades=list(csv.DictReader(f))
 with gzip.open(R/'decisions.csv.gz','rt',newline='') as f:
  import csv
  saved_decisions=list(csv.DictReader(f))
 with gzip.open(R/'daily_equity.csv.gz','rt',newline='') as f:
  import csv
  saved_daily=list(csv.DictReader(f))
 assert len(saved_trades)==len(tradeids) and len({x['trade_id'] for x in saved_trades})==len(saved_trades)
 assert sum(x['status']=='filled' for x in saved_trades)==fill_count
 assert len(saved_decisions)==decision_count==36*3*360 and len(saved_daily)==36*3*361
 assert all(math.isfinite(float(x['nav_usdt'])) and float(x['nav_usdt'])>=0 for x in saved_daily)
 frag=R/'registry_records.jsonl'
 if frag.exists():
  events=[json.loads(x) for x in frag.read_text().splitlines() if x.strip()];assert len(events)==72
  for row in batch:
   pair=[x for x in events if x['fingerprint']==row['fingerprint']];assert len(pair)==2
   assert sorted(x['status'] for x in pair)==sorted(['reserved',report['configs'][row['name']]['status']])
   done=next(x for x in pair if x['status']!='reserved');assert done['report_sha256']==sha(R/'report.json') and done['result_available'] is True
  print('registry sidecar audit passed for all 36 reserve→finish pairs')
 print(f'audit passed: 36 configs × 3 costs=108; {fill_count} filled orders; {len(saved_daily)} daily NAV marks; {decision_count} daily decisions replayed; 12 folds/config; exact Wilder ATR recursion; no balance/capacity failures')
if __name__=='__main__':main()
