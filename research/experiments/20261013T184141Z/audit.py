#!/usr/bin/env python3
"""Audit compact report against preserved full evaluator output, data, timing, fills and registry."""
from __future__ import annotations
import csv,gzip,hashlib,json,re,sys
from datetime import datetime,timedelta
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dt(s):return datetime.fromisoformat(s.replace('Z','+00:00'))
def close(a,b,tol=D('1e-18')):return abs(a-b)<=tol
plan=json.loads((ROUND/'plan.json').read_text());batch=json.loads((ROUND/'batch.json').read_text());report=json.loads((ROUND/'report.json').read_text());manifest=json.loads((ROUND/'data_manifest.json').read_text())
archive=ROUND/'full_evaluation_report.json.gz';archive_raw=gzip.decompress(archive.read_bytes());detail=json.loads(archive_raw)
assert plan['status']=='frozen_before_evaluation'
assert hashlib.sha256(archive_raw).hexdigest()==report['full_detail_sha256']==hashlib.sha256(archive_raw).hexdigest()
assert sha(archive)==report['full_detail_archive_sha256']
assert sha(ROUND/'exchange_filters.json')==plan['cost_model']['exchange_filter_snapshot_sha256']==manifest['exchange_filter_snapshot_sha256']
assert len(batch)==27 and len({x['name'] for x in batch})==27
assert len(report['configs'])==27 and len(detail['configs'])==27
assert report['summary']['walk_forward_folds']==12 and report['summary']['oos_days']==360
assert report['summary']['cost_scenes']==81 and report['summary']['candidate_passed']==0 and report['summary']['candidate_rejected']==27
for asset,meta in manifest['assets'].items():
    assert meta['minutes']==730*1440 and meta['daily_bars']==730
    for source in meta['source_files']:
        p=ROOT/source['path'];assert p.stat().st_size==source['bytes'] and sha(p)==source['sha256']
        assert source['bars']==365*1440 and source['last_open_ns']-source['first_open_ns']==(365*1440-1)*60_000_000_000
    assert meta['first_minute_utc']=='2024-09-16T00:00:00Z' and meta['last_minute_utc']=='2026-09-15T23:59:00Z'
records=registry.read_records(ROOT/'research/automation/registry.jsonl')
seen=set();trade_count=0;rejected_count=0
for item in batch:
    spec=json.loads((ROOT/item['spec']).read_text());fp=registry.fingerprint(spec)
    assert fp not in seen;seen.add(fp);assert fp==item['fingerprint']==report['configs'][item['name']]['fingerprint']==detail['configs'][item['name']]['fingerprint']
    assert records[fp]['status']=='rejected' and records[fp]['result_available'] is True
    assert records[fp]['report']=='research/experiments/20261013T184141Z/report.json'
    assert records[fp]['report_sha256']==sha(ROUND/'report.json')
    compact=report['configs'][item['name']];full=detail['configs'][item['name']]
    for asset,signals in full['signal_triggers'].items():
        for sig in signals:
            assert dt(sig['execution_utc'])==dt(sig['decision_utc'])+timedelta(minutes=1)
            assert dt(sig['decision_utc'])>=dt(plan['data']['oos_signal_start_utc'])
            assert dt(sig['decision_utc'])<dt(plan['data']['oos_signal_end_exclusive_utc'])
            assert sig['entry'] or sig['exit']
    for mult in ('1','2','3'):
        scene=compact['scenarios'][mult];original=full['scenarios'][mult]
        assert len(original['folds'])==12 and scene['cost_multiplier']==int(mult)
        assert len(scene['minute_nav_sha256_f64le'])==64 and re.fullmatch(r'[0-9a-f]{64}',scene['minute_nav_sha256_f64le'])
        assert scene['minute_nav_samples']>360*1440
        assert D(scene['net_pnl_usdt'])==D(scene['terminal_nav_usdt'])-D(2000)
        assert scene['net_return_pct']==original['net_return_pct']
        for trade in original['trades']:
            trade_count+=1
            assert dt(trade['execution_utc'])>=dt(trade['signal_available_utc'])
            before=D(trade['cash_before'])+D(trade['units_before'])*D(trade['reference'])
            after=D(trade['cash_after'])+D(trade['units_after'])*D(trade['reference'])
            assert D(trade['cash_before'])>=0 and D(trade['units_before'])>=0
            assert D(trade['cash_after'])>=0 and D(trade['units_after'])>=0
            if trade['status']=='filled':
                parts=sum((D(v) for v in trade['cost_parts'].values()),D(0))
                assert close(before-after,D(trade['cost_usdt'])) and close(parts,D(trade['cost_usdt']))
                assert int(trade['cost_multiplier'])==int(mult)
                if D(trade['participation'])>D('0.001'):raise AssertionError('filled order above participation cap')
            else:
                rejected_count+=1
                assert D(trade['cash_before'])==D(trade['cash_after']) and D(trade['units_before'])==D(trade['units_after'])
        assert scene['sampled_1m_nav_drawdown_pct']+1e-9>=scene['daily_nav_drawdown_pct']
with gzip.open(ROUND/'equity_curves_daily.csv.gz','rt',newline='') as f:curves=list(csv.DictReader(f))
with gzip.open(ROUND/'fold_results.csv.gz','rt',newline='') as f:foldrows=list(csv.DictReader(f))
with gzip.open(ROUND/'cost_scenarios.csv.gz','rt',newline='') as f:costrows=list(csv.DictReader(f))
with gzip.open(ROUND/'trade_ledger.csv.gz','rt',newline='') as f:ledgerrows=list(csv.DictReader(f))
assert len(curves)==27*3*362 and all(float(row['nav_usdt'])>0 for row in curves)
assert len(foldrows)==27*3*12 and all(row['start_utc']<row['end_exclusive_utc'] for row in foldrows)
assert len(costrows)==81 and len(ledgerrows)==trade_count==1434
assert all(m['last_minute_utc'].endswith('23:59:00Z') for m in manifest['assets'].values())
audit={'status':'passed','configs_reserved_before_evaluation':len(seen),'finished_rejected':27,'cost_scenes':81,
       'fold_rows':len(foldrows),'daily_equity_rows':len(curves),'recorded_order_events':trade_count,
       'rejected_virtual_orders':rejected_count,'source_parquet_files':4,
       'full_detail_sha256_verified':True,'compact_report_registry_sha256_verified':True,
       'data_hashes_verified':True,'signal_to_execution_causality_verified':True,
       'per_fill_balance_and_cost_identity_verified':True,'capacity_constraints_verified':True,
       'instrument_rules_hash_verified':True,'terminal_outcomes_and_12_folds_verified':True,
       'oos_scope':'daily UTC close signals, next 00:01 UTC minute-open execution; 360 days/12 consecutive 30-day folds; window has been repeatedly reused and is not a final holdout'}
(ROUND/'audit.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False)+'\n')
(ROUND/'audit.log').write_text(json.dumps(audit,ensure_ascii=False)+'\n')
print(json.dumps(audit,ensure_ascii=False))
