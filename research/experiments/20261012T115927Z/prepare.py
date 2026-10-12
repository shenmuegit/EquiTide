#!/usr/bin/env python3
"""Freeze and reserve BTC/ETH cross-sectional dual-momentum rotation tests."""
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]; ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation')); import registry

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
source=ROOT/'research/experiments/20261012T035429Z/report.json'
source_report=json.loads(source.read_text()); filters=source_report['plan']['execution']['filters']
prior_audit=ROOT/'research/experiments/20261012T035429Z/prior_evidence_audit.json'
prior=json.loads(prior_audit.read_text())
assert len(prior['initial16_actual_results_checked'])==16 and all(x['evidence'] for x in prior['initial16_actual_results_checked'])
files={}
for asset in ('BTC','ETH'):
 files[asset]=[]
 for suffix in (f'{asset}_20240916T000000Z_20250916T000000Z_transfer_20261001',f'{asset}_20250916T000000Z_20260916T000000Z_archive_20260929'):
  p=ROOT/f'data/normalized/binance/{asset}/binance_{suffix}/spot_bars.parquet'
  files[asset].append({'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size})

common={'literature':{'citation':'Gbadebo, A.D. (2026). Momentum Trading in Cryptocurrencies: A Comparative Study of Time-Series and Cross-Sectional Strategies. Buhalterinės apskaitos teorija ir praktika, 33, 1–25. DOI:10.15388/batp.2026.1.','url':'https://zurnalai.vu.lt/BATP/en/article/view/44540','accessed_utc':'2026-10-12','use':'The paper compares time-series and cross-sectional momentum on eight major cryptoassets (2020-01 to 2025-10), reporting high correlation and larger drawdowns for cross-sectional allocation. This smaller BTC/ETH long-only rotation with an absolute-return gate is a predeclared adaptation, not a reproduction.'},
 'data':{'source':'Binance spot 1m OHLCV, normalized closed bars','assets':files,'history_utc':'2024-09-16T00:00:00Z/2026-09-16T00:00:00Z','reuse_disclosure':'The interval is repeatedly used development/validation history and is not an untouched final holdout.'},
 'walk_forward':{'window_type':'rolling','train_days':365,'train_bars':365,'test_days':30,'test_bars':30,'step_days':30,'embargo_days':3,'embargo_bars':3,'folds':12,'continuous_oos':True,'first_test_index':368,'end_exclusive_index':728,'first_oos_execution_utc':'2025-09-19T00:01:00Z','terminal_execution_utc':'2026-09-14T00:01:00Z','parameter_fit':'None; all strategy parameters fixed before evaluation. Prior closes are used only for the declared momentum lookback and cost estimates. OOS starts with $2,000 cash and carries one position or cash continuously across folds.'},
 'execution':{'filters_source':'research/experiments/20261012T035429Z/report.json','filters_source_sha256':sha(source),'filters_by_symbol':filters,'reference_price':'Next UTC day 00:01 one-minute open. Switching first liquidates the held asset, then invests remaining cash in the new leader using the same observed historical timestamp; each leg incurs its own cost. Historical L2 is unavailable; spread/impact are estimated, not an exchange fill guarantee.'},
 'costs':{'fee_per_side':0.001,'half_spread_estimate_per_side':0.0001,'slippage_estimate_per_side':0.0002,'impact_coefficient':0.5,'impact_formula':'0.5 * sample std(previous 20 complete UTC daily log returns) * sqrt(order budget / mean quote turnover(previous 20 complete UTC days))','max_lagged_ADV_participation':0.001,'scenarios':[1,2,3],'spread_counted_once':True,'funding_borrow':'Not applicable; unlevered long-only spot.'},
 'prior_results':{'initial16_audit':str(prior_audit.relative_to(ROOT)),'initial16_audit_sha256':sha(prior_audit),'finding':'All 16 initial registry entries have actual result evidence; no exact missing-result initial configuration to rerun.'}}
plan={'round':ROUND.name,'frozen_at_utc':'2026-10-12T11:59:27Z','direction':'BTC/ETH daily cross-sectional relative-strength rotation with an absolute momentum hurdle','hypothesis':'When BTC and ETH have divergent trailing returns, holding the stronger asset may capture relative momentum; an absolute hurdle can keep the account in cash when both trends are weak. Correlated crypto assets may limit the benefit, and daily rotation costs may erase gross spread.', 'grid':{'lookback_days':[20,40,60],'absolute_return_hurdle':[0.0,0.02,0.04],'assets':['BTC','ETH'],'initial_capital_usdt':2000},'sensitivity_axes':['lookback_days','absolute_return_hurdle'],'rule':'At UTC daily decision index i use only completed close C[i-1]. Compute simple close-to-close return r_a=C_a[i-1]/C_a[i-1-L]-1 for BTC and ETH. Let winner be BTC on ties (rBTC >= rETH), otherwise ETH. Target the winner only if max(rBTC,rETH) is strictly greater than hurdle; otherwise target cash. Rebalance only when target differs from current holding. Execute after signal availability at next UTC day 00:01 one-minute open. A switch sells the old asset first and then buys the new asset from remaining cash at the same recorded timestamp, charging both legs. Rejected sells preserve the old holding; rejected buys leave cash and are reconsidered at the next daily decision. No shorting, leverage, simultaneous holdings, rebalance while winner is unchanged, cash yield, or pre-OOS position replay.', 'allocation':'One independent $2,000 account per parameter configuration; target is 100% of remaining account cash in one BTC or ETH asset, or 100% cash under the absolute hurdle. No raw BTC/ETH weights, cross-configuration transfer, or cash interest.', 'gates':{'all_1x_2x_3x_returns_positive':True,'minimum_positive_1x_folds':7,'maximum_3x_minute_close_sample_drawdown_pct':25,'minimum_3x_neighborhood_positive_fraction':0.60,'minimum_1x_round_trips':2,'minimum_1x_gross_reference_pnl_to_cost':2.5,'no_cash_or_units_violations':True,'terminal_flat':True,'interpretation':'Pass denotes this repeated-history validation screen only; it is not independent out-of-sample or live-profit evidence.'},**common}
(ROUND/'spec.json').write_text(json.dumps(plan,indent=2,ensure_ascii=False)+'\n')
rows=[]
for look in (20,40,60):
 for hurdle in (0.0,0.02,0.04):
  name=f'csdual_L{look}_H{int(hurdle*100):02d}'
  spec={'kind':'strategy','family':'spot-cross-sectional-dual-momentum-rotation','market':'spot','timeframe':'1d','universe':['BTC/USDT','ETH/USDT'],'name':name,
   'logic':{'signal':'For a completed UTC daily close i-1, compute each asset simple return C[i-1]/C[i-1-L]-1. Select the asset with the higher return (BTC breaks exact ties); set target cash unless the winning return is strictly above the configured absolute hurdle.', 'rebalance':'Trade only on target change. If rotating, sell held coin completely before buying the new leader using remaining cash; if threshold is not met, sell to cash. While desired asset is unchanged, do not rebalance. A failed leg remains in current cash/coin state and the next daily decision retries only if target still differs.', 'timing':'Signals use completed daily closes only. Trade at next UTC day 00:01 one-minute open after signal availability; terminal close is costed at the common endpoint.', 'sizing':'Independent $2,000 spot account, 100% one-asset-or-cash target, no simultaneous holdings, leverage, short, interest, cross-account transfers, or pre-OOS fills.'},
   'parameters':{'lookback_days':look,'absolute_return_hurdle':hurdle,'initial_capital_usdt':2000,'train_days':365,'test_days':30,'step_days':30,'embargo_days':3,'folds':12,'oos_first_test_index':368,'oos_end_exclusive_index':728,'cost_multipliers':[1,2,3]}}
  p=ROUND/'specs'/f'{name}.json';p.write_text(json.dumps(spec,indent=2)+'\n');rows.append({'name':name,'spec':str(p.relative_to(ROOT)),'fingerprint':registry.fingerprint(spec),'is_comparator':False})
for asset in ('BTC','ETH'):
 name=f'hold_360d_{asset}';spec={'kind':'strategy','family':'spot-rotation-hold-reference','market':'spot','timeframe':'1d','universe':[asset+'/USDT'],'name':name,'logic':{'entry':'Buy at first OOS 00:01 execution, independent of signal.','exit':'Hold through continuous OOS, then liquidate at the common terminal execution.','sizing':'Independent $2,000 unlevered spot benchmark, no yield.'},'parameters':{'initial_capital_usdt':2000,'oos_first_test_index':368,'oos_end_exclusive_index':728,'cost_multipliers':[1,2,3]}}
 p=ROUND/'specs'/f'{name}.json';p.write_text(json.dumps(spec,indent=2)+'\n');rows.append({'name':name,'spec':str(p.relative_to(ROOT)),'fingerprint':registry.fingerprint(spec),'is_comparator':True})
(ROUND/'batch.json').write_text(json.dumps(rows,indent=2)+'\n')
with (ROUND/'reserve.log').open('w') as log:
 for row in rows:
  cp=subprocess.run([sys.executable,str(ROOT/'research/automation/registry.py'),'reserve',str(ROOT/row['spec'])],cwd=ROOT,text=True,capture_output=True)
  log.write(json.dumps({'name':row['name'],'returncode':cp.returncode,'stdout':cp.stdout.strip(),'stderr':cp.stderr.strip()},ensure_ascii=False)+'\n');log.flush()
  if cp.returncode:raise SystemExit(f"reserve failed: {row['name']} rc={cp.returncode} {cp.stderr}")
print(f'reserved {len(rows)} unique configurations before evaluation')
