"""Freeze the batch and reserve every strategy, capital variant and portfolio."""
import hashlib
import importlib.util
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ROUND = Path(__file__).resolve().parent
rs = importlib.util.spec_from_file_location('registry_prepare', ROOT / 'research/automation/registry.py')
reg = importlib.util.module_from_spec(rs)
rs.loader.exec_module(reg)
ledger_path = ROOT / 'research/automation/registry.jsonl'
records = reg.read_records(ledger_path)  # Read the whole append-only history.
assert not any(r['status'] == 'reserved' for r in records.values())
assert all(r['result_available'] for r in records.values())
assert len({reg.fingerprint(r['spec']) for r in records.values()}) == 148
old = json.loads((ROOT / 'research/experiments/20261001T013355Z/report.json').read_text())
plan = {
 'round': '20261001T113625Z', 'frozen_at_utc': datetime.now(timezone.utc).isoformat(),
 'hypothesis': 'A symmetric SMA hysteresis band may reduce costly switching around the average; fixed BTC/ETH capital sleeves may diversify the resulting paths. This is a new extension, not a claim of replicating paper returns.',
 'directions': ['daily spot SMA hysteresis', 'fixed initial BTC/ETH capital combinations'],
 'data_start_utc': '2025-09-16T00:00:00Z', 'data_end_exclusive_utc': '2026-09-16T00:00:00Z',
 'oos_start_utc': '2026-03-18T00:01:00Z', 'terminal_exit_utc': '2026-09-14T00:01:00Z',
 'history_is_reused_development_data': True,
 'walk_forward': {'train_days': 180, 'test_days': 30, 'step_days': 30, 'embargo_days': 3, 'purge_days': 0, 'folds': 6,
  'fitting': 'No supervised labels, preprocessing or fitted parameters; rolling train boundaries are diagnostic, historical completed bars warm indicators; all parameters and weights fixed before OOS outcomes.',
  'state': 'Start cash at first OOS decision; indicator warmup may use earlier completed prices. Maintain signal/positions/NAV through every fold. Liquidate only at the terminal boundary.'},
 'grid': {'assets': ['BTC','ETH'], 'lookback_days': [50,65,80], 'symmetric_band_fraction': [0.005,0.01,0.02], 'core_capital_usdt': 1000,
  'supplemental_component_capital_usdt': [500,1500], 'supplemental_band_fraction': 0.01,
  'portfolio_capital_usdt': 2000, 'raw_BTC_capital_weights': [0.25,0.5,0.75], 'ETH_weight': '1 minus BTC weight explicitly frozen; no normalization',
  'portfolios': 'same lookback for BTC and ETH, band=0.01; use independently reserved component at exactly 2000*raw_weight initial capital'},
 'rules': {'entry': 'While cash, prior completed close strictly > mean of prior N completed daily closes * (1+band).',
  'exit': 'While long, prior completed close strictly < mean of prior N completed daily closes * (1-band). Equality/deadband preserves state.',
  'sizing': 'All available component cash buys spot at next 00:01 UTC minute open, after costs; no leverage, borrowing, periodic rebalance or transfers. USDT yield=0.',
  'portfolio': 'Weights specify fractions of initial 2000 USDT capital, not target weights later. Sum actual already-size-costed component NAVs on exactly identical timestamps; no second scaling, averaging Sharpe or new component backtests.'},
 'costs': {'fee_per_side':0.001,'half_spread_per_side':0.0001,'slippage_per_side':0.0002,
  'impact':'0.5 * strictly previous20completedUTCdays sample log-close volatility * sqrt(reference order upper-bound cash budget or sell reference notional / previous20day quote ADV)',
  'participation_max':0.001,'multipliers':[1,2,3], 'terminal_exit_costed':True,
  'funding_borrow':'Not applicable to unlevered long-only spot; no spot short or borrow.',
  'execution_limitations':'Reuse existing daily floating-quantity accounting; no historical L2, tick/lot/min-notional or minute capacity calibration. Daily close NAV does not include full intraday drawdown.'},
 'failure_criteria': {'positive_all_1x_2x_3x': True, 'minimum_positive_1x_folds':4, 'max_drawdown_3x_pct':25,
  'minimum_neighborhood_positive_3x_fraction':0.6, 'minimum_round_trips_1x':2, 'minimum_gross_reference_PnL_to_execution_cost_1x':2.5, 'no_negative_cash_or_units':True,
  'neighborhoods':'Strategy uses the full 3x3 lookback/band grid at1000 for its asset; portfolio uses the full 3x3 lookback/BTC-weight grid. All 500/1500 component variants additionally reported and never hidden.'},
 'comparators': 'Reuse completed 013355 BTC/ETH1000 hold 1/2/3 curves, exactly same timestamps, unchanged. Portfolio equal-capital BTC+ETH hold comparator sums these same1000 curves (2000 total); unequal weights are not an equal-risk comparison. Cash zero, no new comparator configuration calculated.',
 'counts': {'new_core_strategies':18,'new_capital_variants':12,'new_combinations':9,'all_new_registered_configs':39,'new_cost_scenes':117,'canonical_before':148,'historical_all_trials_unknown':True},
 'sources': [{'url':'https://www.monash.edu/__data/assets/pdf_file/0011/3744821/Trend-following-Strategies-for-Crypto-Investors.pdf','accessed':'2026-10-01','use':'SMA trend and transaction-cost motivation; hysteresis is our own explicitly frozen extension'}, {'url':'https://github.com/binance/binance-public-data','accessed':'2026-10-01','use':'Official cached real public data and checksum provenance'}]
}
(ROUND / 'spec.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2)+'\n')
summary = {'ledger_sha256_before':hashlib.sha256(ledger_path.read_bytes()).hexdigest(), 'lines_before':len(ledger_path.read_text().splitlines()),
 'canonical_before':148, 'no_pending_or_missing':True, 'prior_records':[{ 'fingerprint':f, 'canonical':reg.fingerprint(r['spec']), 'spec':r['spec'], 'status':r['status'], 'result_available':r['result_available'], 'report':r.get('report'), 'report_sha256':r.get('report_sha256')} for f,r in records.items()],
 'previous_sma_results':{n:{'status':r['status'],'return_3x':r['cost_scenarios']['3']['net_return_pct'],'positive_folds_1x':r['positive_folds_1x']} for n,r in old['configs'].items() if n.startswith('sma')},
 'legacy_walk_forward':{str(p.relative_to(ROOT)):{k:v for k,v in json.loads(p.read_text()).items() if k not in ('folds','data')} for p in (ROOT/'freqtrade_trial/results').glob('walk_forward*.json')}}
(ROUND / 'prior_summary.json').write_text(json.dumps(summary,ensure_ascii=False, separators=(',',':'))+'\n')
batch=[]; components={}
def reserve(name, spec, role):
 spec['name']=name; spec['validation_plan']=str((ROUND/'spec.json').relative_to(ROOT))
 path=ROUND/'specs'/f'{name}.json';path.parent.mkdir(exist_ok=True)
 path.write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
 result=subprocess.run(['python3',str(ROOT/'research/automation/registry.py'),'reserve',str(path)],cwd=ROOT,capture_output=True,text=True)
 print(name,result.returncode,result.stdout.strip(),result.stderr.strip(),flush=True)
 if result.returncode: raise RuntimeError('Reservation failed; do not compute '+name)
 item={'name':name,'fingerprint':reg.fingerprint(spec),'spec':str(path.relative_to(ROOT)),'role':role}
 batch.append(item);return item

for asset in ('BTC','ETH'):
 for n in plan['grid']['lookback_days']:
  for band in plan['grid']['symmetric_band_fraction']:
   capitals=[1000,500,1500] if band==0.01 else [1000]
   for capital in capitals:
    name=f'hyst_{asset}_n{n}_b{band}_c{capital}'
    sp={'kind':'strategy','family':'daily-sma-hysteresis','market':'spot','universe':[asset+'/USDT'],'timeframe':'1d',
      'logic':{k:plan['rules'][k] for k in ('entry','exit','sizing')},
      'parameters':{'lookback_days':n,'symmetric_band_fraction':band,'initial_capital_usdt':capital,
        'start_utc':plan['oos_start_utc'],'end_utc':plan['terminal_exit_utc'],'initial_state':'cash','costs':plan['costs']}}
    components[(asset,n,band,capital)] = reserve(name,sp,'core' if capital==1000 else 'size_variant')
for n in plan['grid']['lookback_days']:
 for w in plan['grid']['raw_BTC_capital_weights']:
  btc=components[('BTC',n,0.01,int(2000*w))];eth=components[('ETH',n,0.01,int(2000*(1-w)))]
  reserve(f'combo_n{n}_btc{w}',{'kind':'combination','family':'daily-sma-hysteresis-initial-capital',
    'logic':{'allocation':plan['rules']['portfolio'],'rebalance':'No transfers or rebalancing; component absolute NAVs already reflect their specified initial capital and all actual size-dependent costs.'},
    'parameters':{'initial_capital_usdt':2000,'start_utc':plan['oos_start_utc'],'end_utc':plan['terminal_exit_utc']},
    'components':[{'fingerprint':btc['fingerprint'],'weight':w},{'fingerprint':eth['fingerprint'],'weight':1-w}]},'combination')
assert len(batch)==39
(ROUND/'batch.json').write_text(json.dumps(batch,ensure_ascii=False,indent=2)+'\n')
print('RESERVED:39 configs,18core+12size_variants+9portfolios;117 new cost scenes')
