#!/usr/bin/env python3
"""Archive full evaluator detail, retain compact summary JSON and compressed NAV/ledger artifacts."""
import csv,gzip,hashlib,io,json,sys
from datetime import datetime,timezone
from pathlib import Path
R=Path(__file__).resolve().parent
detail=R/'full_evaluation_report.json.gz'
report_path=R/'report.json'
if detail.exists():
    old=json.loads(gzip.decompress(detail.read_bytes()))
    cur=json.loads(report_path.read_text())
    if cur.get('full_detail_sha256')==hashlib.sha256(gzip.decompress(detail.read_bytes())).hexdigest():
        print('already_packaged');raise SystemExit(0)
    raise SystemExit('refuse to overwrite an existing full-detail archive')
raw=report_path.read_bytes();full=json.loads(raw);full_sha=hashlib.sha256(raw).hexdigest()
with detail.open('wb') as f:
    with gzip.GzipFile(filename='',mode='wb',fileobj=f,compresslevel=9,mtime=0) as z:z.write(raw)
csv_path=R/'equity_curves_daily.csv';csv_raw=csv_path.read_bytes()
curve_gz=R/'equity_curves_daily.csv.gz'
with curve_gz.open('wb') as f:
    with gzip.GzipFile(filename='',mode='wb',fileobj=f,compresslevel=9,mtime=0) as z:z.write(csv_raw)
ledger_fields=['config','fingerprint','cost_multiplier','asset','side','status','reason','date_utc','signal_available_utc',
 'execution_utc','reference','execution','quantity','budget','lagged_ADV','lagged_sigma','participation',
 'cash_before','cash_after','units_before','units_after','cost_usdt','fee_rate','half_spread_rate','slippage_rate',
 'impact_rate','terminal','cost_parts']
sink=io.StringIO(newline='');writer=csv.DictWriter(sink,fieldnames=ledger_fields,lineterminator='\n');writer.writeheader()
for name,cfg in full['configs'].items():
    for mult,scene in cfg['scenarios'].items():
        for t in scene.get('trades',[]):
            writer.writerow({**{k:t.get(k) for k in ledger_fields if k not in ('config','fingerprint','cost_multiplier','cost_parts')},
                'config':name,'fingerprint':cfg['fingerprint'],'cost_multiplier':mult,
                'cost_parts':json.dumps(t.get('cost_parts',{}),sort_keys=True,separators=(',',':'))})
ledger_raw=sink.getvalue().encode()
ledger_gz=R/'trade_ledger.csv.gz'
with ledger_gz.open('wb') as f:
    with gzip.GzipFile(filename='',mode='wb',fileobj=f,compresslevel=9,mtime=0) as z:z.write(ledger_raw)
scene_keep=('cost_multiplier','net_pnl_usdt','net_return_pct','terminal_nav_usdt','gross_reference_pnl_usdt',
 'gross_reference_pnl_to_cost','cost_usdt','cost_parts_usdt','executions','round_trips','signal_triggers',
 'positive_folds','folds','sampled_1m_nav_drawdown_pct','drawdown_sample_count','drawdown_scope',
 'daily_nav_drawdown_pct','minute_nav_sha256_f64le','minute_nav_samples','terminal_flat','rejected_orders',
 'capacity_rejections','rejection_reasons')
compact={k:full[k] for k in ('round','evaluation_started_utc','plan','data_manifest','summary',
 'matched_existing_buy_hold_50_50','integrity_audit','evaluation_recovery','cost_scenarios')}
compact['configs']={}
for name,cfg in full['configs'].items():
    item={k:cfg[k] for k in ('fingerprint','spec_path','parameters','signal_triggers','signal_trigger_counts','sensitivity')}
    item['scenarios']={m:{k:v[k] for k in scene_keep if k in v} for m,v in cfg['scenarios'].items()}
    compact['configs'][name]=item
compact['artifacts']=dict(full['artifacts'])
compact['artifacts'].update({
 'equity_curves_daily_csv':'research/experiments/'+R.name+'/equity_curves_daily.csv.gz',
 'trade_ledger_csv_gz':'research/experiments/'+R.name+'/trade_ledger.csv.gz',
 'full_evaluation_detail_gz':'research/experiments/'+R.name+'/full_evaluation_report.json.gz'})
compact['full_detail_sha256']=full_sha
compact['full_detail_archive_sha256']=hashlib.sha256(detail.read_bytes()).hexdigest()
report_path.write_text(json.dumps(compact,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
csv_path.unlink()
print(json.dumps({'full_detail_sha256':full_sha,'full_detail_archive_bytes':detail.stat().st_size,
 'compact_report_bytes':report_path.stat().st_size,'equity_curve_archive_bytes':curve_gz.stat().st_size,
 'trade_ledger_rows':len(ledger_raw.splitlines())-1,'trade_ledger_archive_bytes':ledger_gz.stat().st_size,
 'report_sha256':hashlib.sha256(report_path.read_bytes()).hexdigest()}))
