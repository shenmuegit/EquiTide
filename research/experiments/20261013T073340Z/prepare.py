#!/usr/bin/env python3
"""Re-reserve the 20 exact no-result candle-turn definitions and freeze the run."""
import hashlib,json,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
SOURCE=ROOT/'research/experiments/20261012T232807Z';(R/'specs').mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'research/automation'));import registry
for src in sorted((SOURCE/'specs').glob('*.json')):
 shutil.copyfile(src,R/'specs'/src.name)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
rawrows=json.load(open(SOURCE/'reserve.json')); specs=[]
for x in rawrows:
 old=ROOT/x['spec']; new=R/'specs'/old.name
 spec=json.loads(new.read_text());fp=registry.fingerprint(spec)
 assert fp in x['output'] and x['exit_code']==3,(spec['name'],fp,x['output'])
 rec=registry.read_records(ROOT/'research/automation/registry.jsonl')[fp]
 assert rec['status']=='abandoned' and rec['result_available'] is False,(spec['name'],rec['status'],rec['result_available'])
 specs.append({'name':spec['name'],'asset':spec['universe'][0].split('/')[0],'fingerprint':fp,'spec':str(new.relative_to(ROOT)),'role':spec['logic'].get('control_role','buy_hold_comparator'),'parameters':spec['parameters']})
assert len(specs)==20 and len({x['fingerprint'] for x in specs})==20
prior_plan=json.loads((SOURCE/'plan.json').read_text())
resolution=json.loads((ROOT/'research/experiments/20261013T012732Z/pending_reservation_resolution.json').read_text())
assert resolution['result_available'] is False and resolution['action']=='abandoned' and resolution['count']==20
data_files=prior_plan['data_files']
for asset in ('BTC','ETH'):
 for item in data_files[asset]:
  p=ROOT/item['path'];assert p.stat().st_size==item['bytes'] and sha(p)==item['sha256']
filter_path=ROOT/'research/experiments/20261012T035429Z/report.json'
plan={'round':R.name,'reactivation_of_round':SOURCE.name,'frozen_at_utc':'2026-10-13T07:33:40Z','source_plan_sha256':sha(SOURCE/'plan.json'),'source_definitions_sha256':sha(SOURCE/'reserve.json'),
 'no_result_reconciliation':{'path':'research/experiments/20261013T012732Z/pending_reservation_resolution.json','sha256':sha(ROOT/'research/experiments/20261013T012732Z/pending_reservation_resolution.json'),'state':'20 exact definitions abandoned after duplicate-reserved responses; explicit reconciliation says no evaluation/report/data-run existed.'},
 'direction':'Resume the exact UTC 15-minute candle-turn effect falsification batch: phase-0 events are candidates; phase +1 and +2 minute events are predeclared controls.',
 'hypothesis':'A primary Bitcoin study reports minute returns concentrated at 15-minute candle boundaries, but its profitability depends on a Bitfinex-specific volume-based zero-fee tier around $5,000. This re-run checks the exact frozen BTC/ETH 1–3 minute long-only windows at $2,000 per account under Binance and repository costs. Falsification of transferability, not replication.',
 'source_paper':prior_plan['source_paper'],'grid':prior_plan['grid'],'rule':prior_plan['complete_rule'],'time_boundaries':prior_plan['time_boundaries'],'costs':prior_plan['costs'],'failure_gates':prior_plan['gates'],'frozen_specs':specs,'data_files':data_files,
 'execution':{'price_source':'Historical Binance spot 1m OHLCV open at event and scheduled exit, only for this historical backtest; never paper10 fills.','input_structure':'730 contiguous days of normalized Binance 1m bars from 2024-09-16 through 2026-09-16.','oos_start_day_index':368,'oos_end_day_index':728,'oos_days':360,'event_schedule':'UTC minute-of-hour 0/15/30/45 plus phase offset 0/1/2; hold 1/2/3 minutes; no overlap.','signal_available_seconds_before_entry':60,'exit_retry':'If a frozen filter rejects an exit, retry at each subsequent minute open until flat; no future price is used to decide the scheduled entry.','cost_engine':'research/experiments/20261001T133655Z/kernel.py::fill plus lagged_cost_inputs from 20261001T013355Z/evaluate.py.','filters_source':'research/experiments/20261012T035429Z/report.json','filters_sha256':sha(filter_path),'maximum_participation':0.001,'funding_borrow':'Not applicable, long-only spot.'},
 'sensitivity_axes':['phase_offset_minutes: 0 primary, 1/2 placebos','hold_minutes: 1/2/3'],'historical_disclosure':'The 2025-09-19/2026-09-14 OOS span is repeatedly used repository development/validation history, not an untouched final test. Preserve previous search count and report multiple-testing risk.',
 'previous_round_reservation_note':'The source reserve.json records exit code 3 for every item because each was still reserved. A later reconciliation marks them abandoned with result_available=false. No historical calculation is claimed or reused.',
 'reproduction':['python3 research/experiments/20261013T073340Z/prepare.py','python3 research/experiments/20261013T073340Z/evaluate.py','python3 research/experiments/20261013T073340Z/audit.py','python3 research/experiments/20261013T073340Z/result.py','python3 research/experiments/20261013T073340Z/finish.py']}
(R/'plan.json').write_text(json.dumps(plan,indent=2,ensure_ascii=False)+'\n')
(R/'source_no_result_history.json').write_text(json.dumps({'previous_batch':'research/experiments/20261012T232807Z','previous_plan_sha256':sha(SOURCE/'plan.json'),'previous_reserve_rows':rawrows,'resolution':resolution},indent=2,ensure_ascii=False)+'\n')
batch=[]
for x in specs:
 p=subprocess.run([sys.executable,str(ROOT/'research/automation/registry.py'),'reserve',str(ROOT/x['spec'])],cwd=ROOT,capture_output=True,text=True)
 y={**x,'exit_code':p.returncode,'output':p.stdout.strip(),'stderr':p.stderr.strip()};batch.append(y)
 if p.returncode:
  (R/'reserve_partial.json').write_text(json.dumps(batch,indent=2,ensure_ascii=False)+'\n')
  raise SystemExit(f"reserve failed {x['name']}: rc={p.returncode} {p.stdout} {p.stderr}")
(R/'batch.json').write_text(json.dumps(batch,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'reserved':len(batch),'unique':len({x['fingerprint'] for x in batch}),'primary':sum(x['role']=='primary_event' for x in batch),'controls':sum(x['role']=='predeclared_phase_placebo_control' for x in batch),'comparators':sum(x['role']=='buy_hold_comparator' for x in batch)}))
