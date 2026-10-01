"""Verify real data hashes and independently reconcile every archived hourly NAV."""
import argparse,bisect,gzip,hashlib,json,math
from pathlib import Path
import numpy as np
from carry import ROOT,ROUND,HOUR,MINUTE,VERSION,FundingBook,module
reg=module('registry_check_evidence',ROOT/'research/automation/registry.py')
parser=argparse.ArgumentParser();parser.add_argument('--finished',action='store_true');args=parser.parse_args()
r=json.loads((ROUND/'report.json').read_text());batch=json.loads((ROUND/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');report_sha=hashlib.sha256((ROUND/'report.json').read_bytes()).hexdigest()
assert len(batch)==36 and len(r['trials'])==24 and len(r['native_recovery'])==8 and len(r['benchmarks'])==2
for b in batch:
 spec=json.loads((ROOT/b['spec']).read_text());assert reg.fingerprint(spec)==b['fingerprint'];row=records[b['fingerprint']]
 if args.finished:assert row['status']=='rejected' and row['result_available'] and row['report_sha256']==report_sha
 else:assert row['status']=='reserved'
for path,expected in r['source_code_sha256'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==expected
assert hashlib.sha256((ROUND/'plan.json').read_bytes()).hexdigest()==r['plan_sha256']
for a,detail in r['data'].items():
 d=ROOT/'data/normalized/binance'/a/f'binance_{a}_{VERSION}'
 for name,expected in detail['hashes'].items():assert hashlib.sha256((d/(name+'.parquet')).read_bytes()).hexdigest()==expected
for m in r['data_source_manifests']:
 p=ROOT/m['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==m['sha256'];manifest=json.loads(p.read_text())
 for row in manifest.get('archives',[]):
  assert row['sha256']==row['published_sha256'];assert hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest()==row['sha256']
 if 'merged_path' in manifest:assert hashlib.sha256((ROOT/manifest['frozen_snapshot']).read_bytes()).hexdigest()==manifest['merged_sha256']
curves=0;nav_points=0
for trial in r['trials']+r['benchmarks']+r['native_recovery']:
 p=ROOT/trial['full_result_path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==trial['full_result_sha256'];full=json.loads(gzip.decompress(p.read_bytes()))
 for m,s in full.items():
  curves+=1
  if trial['role']=='native':
   summary=s['summary'];fills=s['full_native_artifacts']['fills'];funds=s['full_native_artifacts']['funding'];eq=s['full_native_artifacts']['equity'];assert len(fills) in (0,4)
   for row in eq:
    total=sum(float(row[k]) for k in ('spot_cash_usdt','spot_base_value_usdt','perp_margin_balance_usdt','perp_unrealized_pnl_usdt'));assert abs(total-float(row['nav_usdt']))<5e-7
   actual={x['ts']:x for x in s['actual_source_funding']}
   for event in funds:
    source=actual[event['settlement_ts']];raw_rate=source['rate'];stressed=raw_rate*(int(m) if raw_rate<0 else 1)
    assert abs(float(event['realized_rate'])-stressed)<1e-15
    assert abs(float(event['mark_price'])-source['mark'])<1e-8
    expected=-float(event['signed_contracts'])*float(event['contract_multiplier'])*source['mark']*stressed
    assert abs(float(event['native_amount_usdt'])-expected)<1e-7
   assert abs(sum(float(x['native_amount_usdt']) for x in funds)-float(summary['funding_usdt']))<1e-7
   assert abs(sum(float(x['commission']) for x in fills)-float(summary['fees_usdt']))<1e-7
   assert abs(float(summary['final_nav_usdt'])-float(summary['reconciled_nav_usdt']))<1e-7
   continue
  eq=np.array(s['equity']);assert len(eq)==len(s['equity_signal_times'])+1 and len(eq)==4034;assert abs((eq[-1]/eq[0]-1)*100-s['net_return_pct'])<1e-9
  dd=(1-eq/np.maximum.accumulate(eq)).max()*100;assert abs(dd-s['max_drawdown_pct'])<1e-9
  assert abs(np.prod([x['end_nav']/x['start_nav'] for x in s['folds']])-eq[-1]/eq[0])<1e-9
  assert abs(sum(x['cost_usdt'] for x in s['trades'])-s['execution_cost_usdt'])<1e-7
  assert len(s['trades'])==s['executions']
  events=[]
  for x in s['trades']:events.append((x['ts'],1,'trade',x))
  for x in s.get('funding_events',[]):events.append((x['ts'],0,'funding',x))
  events.sort(key=lambda x:(x[0],x[1]));cash=10000.;spotq=perpq=0.;idx=0;prices={x['ts']:x for x in s['trades'] if x.get('leg','spot')=='spot'}
  asset=trial['name'].split('_')[1] if trial['role']=='candidate' else trial['name'].split('_')[-1]
  # Reconstruct independent combined cash flow: include short-sale credits,
  # then subtract marked short inventory. This differs from Ledger's entry-PnL method.
  from carry import load
  if 'datasets' not in globals():datasets={}
  if asset not in datasets:datasets[asset]=load(asset)
  ds=datasets[asset];bytime={row['ts']:row for row in ds['rows']}
  for j,t in enumerate(s['equity_signal_times']):
   while idx<len(events) and events[idx][0]<=t+MINUTE:
    _,_,kind,x=events[idx]
    if kind=='funding':
     assert abs(-perpq-x['quantity'])<1e-8;raw=-perpq*x['mark']*x['rate'];expected=raw if raw>=0 else raw*int(m)
     assert abs(raw-x['base_amount_usdt'])<1e-8 and abs(expected-x['amount_usdt'])<1e-8;cash+=x['amount_usdt']
    else:
     if trial['role']=='benchmark':change=x['quantity'];leg='spot'
     else:change=x['quantity']*(1 if x['side']=='buy' else -1);leg=x['leg']
     cash-=change*x['execution']+x['fee_usdt']
     if leg=='spot':spotq+=change
     else:perpq+=change
     assert x['participation']<=.001
    idx+=1
   row=bytime[t];value=cash+spotq*float(row['fill'])+perpq*float(row['fill_perp']);assert abs(value-eq[j+1])<1e-6,(trial['name'],m,j,value,eq[j+1]);nav_points+=1
  assert abs(spotq)<1e-8 and abs(perpq)<1e-8
  if trial['role']=='candidate':
   funding=ds['book'];p=trial['parameters']
   for decision in s['decisions']:
    assert decision['hourly_rate']==funding.hourly_rate(decision['ts'],21)
    if decision['action']=='enter':assert any(x['ts']==decision['ts']+MINUTE and x['reason']=='entry' for x in s['trades'])
if args.finished:
 original=[json.loads(x)['fingerprint'] for x in (ROOT/'research/automation/registry.jsonl').read_text().splitlines()[:16]];assert sum(bool(records[f].get('result_available')) for f in original)==15
 assert not any(x['status']=='reserved' for x in records.values())
 assert len({reg.fingerprint(x['spec']) for x in records.values()})==106
print('PASS:',curves,'archived scenarios;',nav_points,'independently reconciled hourly NAV points; reserves/specs, raw/normalized hashes, source snapshots, funding chronology/sign and six-fold products'+('; 15/16 initial actual results, 106 canonical configs, no pending reservations' if args.finished else ''))
