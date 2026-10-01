"""Preserve original script results, register comparator audits and finish all trials."""
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from importlib.util import spec_from_file_location,module_from_spec

ROOT=Path(__file__).resolve().parents[3]
ROUND=Path(__file__).resolve().parent
s=spec_from_file_location('evaluate_final',ROUND/'evaluate.py')
m=module_from_spec(s)
s.loader.exec_module(m)
registry=m.module('registry_final',ROOT/'research/automation/registry.py')
report=json.loads((ROUND/'report.json').read_text())
batch=json.loads((ROUND/'batch.json').read_text())
data,obv=m.load_data()
start=report['folds'][0]['test_start_index']
end=report['folds'][-1]['test_end_exclusive_index']

# Independent calculation parity: decimal legacy accounting vs our float engine.
legacy_results={}
for family,filename in [('sma','price_trend_oos_20260929.json'),('obv','obv_trend_oos_20260929.json')]:
 value=json.loads((ROOT/'data/runs'/filename).read_text())
 value['historical_holdout_note']='reused development history, not a pristine final test'
 value['reproduce']=f'.venv/bin/python checks/{"price" if family=="sma" else "obv"}_trend_oos.py'
 target=ROUND/(family+'_baseline.json')
 target.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
 legacy_results[family]=str(target.relative_to(ROOT))
 for asset in ('BTC','ETH'):
  spec=json.loads((ROUND/'specs'/f'{family}_{asset}.json').read_text())
  sig=m.rule_signals(spec,data[asset],obv)
  dates=[x['date'] for x in data[asset]]
  r=m.backtest(data[asset],sig,dates.index('2026-03-16'),dates.index('2026-09-15'),1000,1.0,1,impact=False)
  old=[1000]+value['assets'][asset]['equity_points_usdt']
  assert len(old)==len(r['equity_usdt'])
  assert max(abs(a-b) for a,b in zip(old,r['equity_usdt']))<1e-8,(family,asset)
 print(f'PARITY PASS: {family} engine matches full legacy Decimal equity curve',flush=True)
report['legacy_baseline_reports']=legacy_results
report['verification']={'decimal_legacy_full_curve_parity':'both assets, both strategy directions, tolerance USDT1e-8','synthetic_causality_and_accounting':'check_accounting.py','synthetic_tests_are_not_profit_evidence':True}

# All genuine strategy configurations are reserved. The initial benchmark-only evaluation
# was omitted from the candidate batch; explicitly audit this process lapse, then reserve
# comparator configurations before rerunning their full validation. Do not backdate.
comparators=[]
for asset in ('BTC','ETH'):
 name='benchmark_hold_'+asset
 spec={'kind':'strategy','family':'buy-hold-daily-comparator','market':'spot','universe':[asset+'/USDT'],'timeframe':'1d','logic':{'entry':'first 00:01 UTC minute open of fixed validation window','exit':'scheduled terminal 00:01 UTC exit','sizing':'unlevered 1000 USDT spot sleeve; cash yield zero'},'parameters':{'validation_start_utc':report['oos_start_utc'],'terminal_exit_utc':report['terminal_exit_utc'],'initial_capital_usdt':1000},'name':name,'validation_plan':'research/experiments/20261001T013355Z/plan.json','role':'comparison only, excluded from candidate selection'}
 path=ROUND/'specs'/(name+'.json')
 path.write_text(json.dumps(spec,indent=2)+'\n')
 p=subprocess.run(['python3',str(ROOT/'research/automation/registry.py'),'reserve',str(path)],cwd=ROOT,capture_output=True,text=True)
 assert p.returncode==0,p.stdout+p.stderr
 fp=registry.fingerprint(spec)
 report['benchmarks'][asset]={}
 for k in (1,2,3):
  r=m.backtest(data[asset],[True]*365,start,end,1000,1.0,k)
  r['folds']=m.fold_metrics(r['equity_usdt'],report['folds'],start)
  report['benchmarks'][asset][str(k)]=r
 positive=sum(f['net_return_pct']>0 for f in report['benchmarks'][asset]['1']['folds'])
 status='rejected'  # comparator is not qualified as a researched method (sensitivity absent).
 report['benchmarks'][asset]['registry']={'fingerprint':fp,'status':status,'positive_folds_1x':positive,'role':'comparator only; no complete two-parameter sensitivity qualification','spec_path':str(path.relative_to(ROOT))}
 comparators.append({'name':name,'fingerprint':fp,'spec':str(path.relative_to(ROOT)),'status':status})
(ROUND/'benchmark_batch.json').write_text(json.dumps(comparators,indent=2)+'\n')
report['process_audit']={'candidate_preregistration':'all 42 strategy/grid/portfolio candidates reserved before actual evaluation','benchmark_preregistration_lapse':'two buy-and-hold comparison curves were initially computed without individual reservation; explicitly recorded, then their distinct daily comparator specs were reserved at the actual later time and rerun. This is a workflow lapse, not prospective preregistration of the first comparator calculations. Comparator values excluded from candidate selection.','preparation_issue':'prepare.py initially named read_records incorrectly; fixed before successful reservations; no strategy calculation before reservations','data_failures':'transient TLS EOF recovered with HTTP/1.1 and retry; 54 archives verified; no missing/fabricated bars'}
report['historical_trial_counts']['ledger_distinct_before_round']=16
report['historical_trial_counts']['comparator_configs_reserved_after_initial_benchmark_calculation']=2
report['historical_trial_counts']['total_finished_configurations_this_round']=44
report['historical_trial_counts']['independent_parameter_signal_sets_note']='SMA: 3 lookbacks per asset, each with 3 risk allocations; allocation changes are valid configurations but not independent signal evidence. OBV: 9 short/long choices per asset. All tested on reused history.'
report['limitations']=['No untouched final holdout or live evidence; this history was already used before the round.','Daily equity marks plus terminal execution; intraday minute drawdowns are not the reported daily maximum drawdown.','Fee/spread/slippage and square-root impact are stated estimates; no historical level-2/order-fill calibration. Daily ADV participation is a capacity proxy, not a guaranteed minute fill.','No exchange lot/tick rounding, tax, USDT depeg or custody failure model; low nominal spot capital only.','Sensitivity grid is small, highly correlated, and not a multiple-testing-adjusted significance claim. SMA allocations do not create independent signals.','Walk-forward uses fixed parameters; training windows establish historical availability only, not fitted models or an OOS-tuned selection.']
# Keep readable report.json while limiting whitespace overhead; all outputs retained.
report_path=ROUND/'report.json'
report_path.write_text(json.dumps(report,ensure_ascii=False,separators=(',',':'),allow_nan=False)+'\n')
for item in batch+comparators:
 status=item.get('status') or report['configs'][item['name']]['status']
 p=subprocess.run(['python3',str(ROOT/'research/automation/registry.py'),'finish',str(ROOT/item['spec']),status,str(report_path.relative_to(ROOT))],cwd=ROOT,capture_output=True,text=True)
 assert p.returncode==0,p.stdout+p.stderr
 print(json.dumps({'finished':item['name'],'status':status,'fingerprint':item['fingerprint']}),flush=True)
# Resolve old combination IDs as append-only aliases, preserving original fingerprints/specs.
# Their updated signatures differ solely because the registry now preserves raw weights.
for old,name in [('bf8c57afa75b965ce47e0350ce1f2955b21101c2fbd161b503ef7d1db213b542','sma_equal'),('ab9452ab0b625ca6f7babc1529a4e06b4a3823fe865095d6b47a05727cf2557a','obv_equal')]:
 row={'fingerprint':old,'status':report['configs'][name]['status'],'result_available':True,'report':str(report_path.relative_to(ROOT)),'report_sha256':hashlib.sha256(report_path.read_bytes()).hexdigest(),'recovered_result_fingerprint':report['configs'][name]['fingerprint'],'recorded_at_utc':m.datetime.now(m.timezone.utc).isoformat(),'audit_note':'original missing-result combination recovered this round under current raw-weight signature; historical ID remains valid'}
 with (ROOT/'research/automation/registry.jsonl').open('a') as f:
  f.write(json.dumps(row,ensure_ascii=False)+'\n')
print(json.dumps({'finished':len(batch)+len(comparators),'report_bytes':report_path.stat().st_size}))
