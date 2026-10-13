#!/usr/bin/env python3
"""Regenerate the Git-friendly summary from the immutable gzip-compressed full evaluator report."""
import gzip,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parent
archive=R/'full_evaluation_report.json.gz'
raw=gzip.decompress(archive.read_bytes());full=json.loads(raw);full_sha=hashlib.sha256(raw).hexdigest()
report={k:full[k] for k in ('round','evaluation_started_utc','plan','data_manifest','summary',
 'matched_existing_buy_hold_50_50','integrity_audit','evaluation_recovery')}
report['configs']={}
fields=('cost_multiplier','net_pnl_usdt','net_return_pct','terminal_nav_usdt','gross_reference_pnl_usdt',
 'gross_reference_pnl_to_cost','cost_usdt','cost_parts_usdt','executions','round_trips','signal_triggers',
 'positive_folds','sampled_1m_nav_drawdown_pct','drawdown_sample_count','drawdown_scope',
 'daily_nav_drawdown_pct','minute_nav_sha256_f64le','minute_nav_samples','terminal_flat','rejected_orders',
 'capacity_rejections','rejection_reasons')
for name,cfg in full['configs'].items():
    slim={k:cfg[k] for k in ('fingerprint','spec_path','parameters','signal_trigger_counts','sensitivity')}
    slim['scenarios']={}
    for mult,scene in cfg['scenarios'].items():
        slim['scenarios'][mult]={k:scene[k] for k in fields if k in scene}
        slim['scenarios'][mult]['max_drawdown_pct']=scene['sampled_1m_nav_drawdown_pct']
    report['configs'][name]=slim
report['artifacts']={
 'fold_results_csv_gz':'research/experiments/'+R.name+'/fold_results.csv.gz',
 'cost_scenarios_csv_gz':'research/experiments/'+R.name+'/cost_scenarios.csv.gz',
 'equity_curves_daily_csv_gz':'research/experiments/'+R.name+'/equity_curves_daily.csv.gz',
 'sensitivity_csv':'research/experiments/'+R.name+'/sensitivity.csv',
 'sensitivity_surface_svg':'research/experiments/'+R.name+'/sensitivity_surface.svg',
 'trade_ledger_csv_gz':'research/experiments/'+R.name+'/trade_ledger.csv.gz',
 'full_evaluation_detail_gz':'research/experiments/'+R.name+'/full_evaluation_report.json.gz',
 'data_manifest':'research/experiments/'+R.name+'/data_manifest.json'}
report['full_detail_sha256']=full_sha
report['full_detail_archive_sha256']=hashlib.sha256(archive.read_bytes()).hexdigest()
path=R/'report.json';path.write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
print(json.dumps({'report_bytes':path.stat().st_size,'report_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                  'detail_sha256':full_sha,'config_count':len(report['configs'])}))
