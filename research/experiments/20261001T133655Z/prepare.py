"""Freeze the execution refinement and reserve ALL evaluated configurations."""
import hashlib
import importlib.util
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
ROUND=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('registry',ROOT/'research/automation/registry.py')
reg=importlib.util.module_from_spec(s);s.loader.exec_module(reg)
ledger=ROOT/'research/automation/registry.jsonl'
records=reg.read_records(ledger)
assert all(r.get('result_available') and r['status']!='reserved' for r in records.values())
assert len({reg.fingerprint(r['spec']) for r in records.values()})==188
metadata=ROOT/'research/experiments/20261001T053425Z/spot_metadata_snapshot.json'
filters={s['symbol']:{f['filterType']:f for f in s['filters']} for s in json.loads(metadata.read_text())['symbols']}
plan={
 'round':'20261001T133655Z','trigger_utc':'2026-10-01T13:36:55.932Z','actual_first_tool_utc':'2026-10-01T15:17:34Z',
 'frozen_at_utc':datetime.now(timezone.utc).isoformat(),'delayed_execution':True,
 'hypothesis':'Test whether the prior SMA65/1%/75:25 historical candidate has a profitable adjacent lookback/capital neighbourhood after explicit lot/tick/notional rounding; minute marks may expose drawdown missed by daily marks.',
 'grid':{'lookback_days':[60,65,70],'band':0.01,'weight_pairs':[[0.65,0.35],[0.75,0.25],[0.85,0.15]],'total_initial_usdt':2000,'component_capitals':{'BTC':[1300,1500,1700],'ETH':[700,500,300]}},
 'oos_start_utc':'2026-03-18T00:01:00Z','terminal_exit_utc':'2026-09-14T00:01:00Z','development_history_reused':True,
 'walk_forward':{'train_days':180,'embargo_days':3,'test_days':30,'step_days':30,'purge_days':0,'folds':6,'fit':'None: fixed rules, no supervised labels or OOS fitting; completed historical prices warm indicators. Capital/positions and desired signal state carry through folds.'},
 'rules':{'entry':'Start cash; prior completed daily close strictly above mean of prior N completed closes*(1+0.01) enters desired-long state.',
   'exit':'Prior close strictly below SMA*(1-0.01) exits desired-long; equality/deadband preserves desired state.',
   'sizing':'At next UTC00:01 real minute open, buy maximum affordable LOT_SIZE floored quantity; keep leftover USDT. Sell all lot-valid held units when desired-cash or terminal. Failed orders do not change holdings and are retried at later daily decisions. No leverage, borrow, funding, transfers, rebalancing or USDT yield.',
   'portfolio':'Explicit raw weights specify initial fractions of2000USDT, not maintained weights; sum corresponding already-costed absolute component NAVs with no second scaling.'},
 'execution':{'metadata_path':str(metadata.relative_to(ROOT)),'metadata_sha256':hashlib.sha256(metadata.read_bytes()).hexdigest(),
   'filters':filters,'simulation':'Hypothetical immediately filled marketable LIMIT IOC at estimated adverse execution price, buy rounded up/sell down to PRICE_FILTER tick; quantity floored to LOT_SIZE. Check static price/quantity bounds and NOTIONAL. Fee paid in USDT; no fee discounts.',
   'percent_price':'Check frozen PERCENT_PRICE_BY_SIDE against preceding5 fully closed minute quote-volume/base-volume VWAP proxy. Historical reference-price regime is unavailable; proxy is explicitly an assumption, not historical exchange order validation.',
   'limitations':'Snapshot taken October1, applied uniformly to reused historical data as execution stress assumption, not historical filters. No L2, queue, latency, partial fills or guarantee IOC fills; MARKET_LOT_SIZE does not apply to simulated limit IOC.'},
 'costs':{'fee_per_side':0.001,'half_spread':0.0001,'slippage':0.0002,'impact_coefficient':0.5,'impact_inputs':'Previous20 completed UTC day quote ADV and sample stdev20 log daily returns. Buy cash before costs is conservative notional upper bound; sell uses units*reference. Decimal sqrt of budget/ADV, sigma/ADV derived from existing lagged daily function.',
   'multipliers':[1,2,3],'max_lagged_ADV_participation':0.001,'all_costs_simultaneously_scaled':True,'rounding_cost_separately_recorded':True,'terminal_costed':True,'funding_borrow':'N/A unlevered long-only spot'},
 'nav':{'minute_marks':'Each fully closed minute after start until terminal boundary, plus all daily post-decision reference-open marks and final liquidation;259382 aligned points per scene. Initial pre-trade cash and post-trade NAV are both retained.',
   'risk':'Overall/fold DD from full continuous minute-close/post-order vector; Sharpe365 from180 daily boundary returns, terminal included once; Calmar uses minute DD.',
   'compact_storage':'Lossless cash/quantity daily segments plus hash-bound real minute close prices, daily reference opens, explicit construction formula/indexes and little-endian float64 NAV SHA. Complete vectors additionally cached in ignored data/runs; no market arrays in Git.',
   'intraminute_limit':'Minute-close and order marks are not tick/intraminute-low or executable liquidation-value risk.'},
 'failure_criteria':{'all_cost_returns_positive':True,'min_positive_1x_folds':4,'max_minute_DD_3x_pct':25,'min_3x_positive_neighbourhood_fraction':0.6,'min_1x_round_trips':2,'min_1x_reference_gross_PnL_to_cost':2.5,'no_negative_cash_or_units':True,
   'neighbourhoods':'Per asset: lookback x actual allocated capital3x3; portfolios: lookback x BTC raw initial weight3x3. Comparators recorded rejected solely comparator scope; this is reused historical research, not forward qualification.'},
 'counts':{'research_components':18,'research_portfolios':9,'comparator_components':2,'comparator_portfolios':1,'all_reserved':30,'actual_cost_scenes':90},
 'forward_plan':'Previous113625 frozen candidate/forward plan remains unchanged, startsOctober2; no forward data/results yet.',
 'sources':[{'url':'https://developers.binance.com/en/docs/products/spot/filters','accessed':'2026-10-01','use':'Official static filter definitions and prior-price percent constraints; assumptions explicitly separate.'},{'url':'https://github.com/binance/binance-public-data','accessed':'2026-10-01','use':'Hash-verified real cached spot data'}]
}
(ROUND/'spec.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
prior={'ledger_sha256':hashlib.sha256(ledger.read_bytes()).hexdigest(),'lines':len(ledger.read_text().splitlines()),'records':len(records),'canonical':188,'initial16_available':all(v['result_available'] for v in list(records.values())[:16]),'pending':[],
 'prior_reports':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'research/experiments').glob('*/result.md'))},
 'records':[{'fingerprint':k,'canonical':reg.fingerprint(v['spec']),'spec':v['spec'],'status':v['status'],'result_available':v['result_available'],'report':v.get('report')} for k,v in records.items()]}
(ROUND/'prior_summary.json').write_text(json.dumps(prior,ensure_ascii=False,separators=(',',':'))+'\n')
batch=[];parts={}
def reserve(name,sp,role):
 sp['name']=name;sp['validation_plan']=str((ROUND/'spec.json').relative_to(ROOT))
 path=ROUND/'specs'/f'{name}.json';path.parent.mkdir(exist_ok=True);path.write_text(json.dumps(sp,ensure_ascii=False,indent=2)+'\n')
 p=subprocess.run(['python3',str(ROOT/'research/automation/registry.py'),'reserve',str(path)],cwd=ROOT,capture_output=True,text=True)
 print(name,p.returncode,p.stdout.strip(),flush=True)
 if p.returncode:raise RuntimeError(p.stderr+p.stdout)
 b={'name':name,'spec':str(path.relative_to(ROOT)),'fingerprint':reg.fingerprint(sp),'role':role};batch.append(b);return b
def component(asset,n,capital,role):
 name=f'rounded_{asset}_n{n}_c{capital}' if n else f'rounded_hold_{asset}_c{capital}'
 logic=dict(plan['rules']);logic.pop('portfolio')
 if not n:logic.update(entry='Buy at first OOS decision and hold until terminal.',exit='Only terminal exit.')
 return reserve(name,{'kind':'strategy','family':'daily-sma-hysteresis' if n else 'spot-hold-comparator','market':'spot','timeframe':'1d','universe':[asset+'/USDT'],'logic':logic,
   'parameters':{'lookback_days':n,'symmetric_band_fraction':0.01 if n else None,'initial_capital_usdt':capital,'start_utc':plan['oos_start_utc'],'end_utc':plan['terminal_exit_utc'],'execution':plan['execution'],'costs':plan['costs']}},role)
for asset in ('BTC','ETH'):
 for n in plan['grid']['lookback_days']:
  for c in plan['grid']['component_capitals'][asset]:parts[(asset,n,c)]=component(asset,n,c,'component')
for asset in ('BTC','ETH'):parts[(asset,0,1000)]=component(asset,0,1000,'comparator')
def portfolio(name,btc,eth,weights,role):
 reserve(name,{'kind':'combination','family':'daily-sma-hysteresis-initial-capital','logic':{'allocation':plan['rules']['portfolio'],'rebalance':'None; no transfers; component execution independently uses actual capital, and absolute NAVs are summed.'},
  'parameters':{'initial_capital_usdt':2000,'start_utc':plan['oos_start_utc'],'end_utc':plan['terminal_exit_utc']},
  'components':[{'fingerprint':btc['fingerprint'],'weight':weights[0]},{'fingerprint':eth['fingerprint'],'weight':weights[1]}]},role)
for n in plan['grid']['lookback_days']:
 for w in plan['grid']['weight_pairs']:
  portfolio(f'rounded_combo_n{n}_btc{w[0]}',parts[('BTC',n,int(2000*w[0]))],parts[('ETH',n,int(2000*w[1]))],w,'combination')
portfolio('rounded_hold_equal2000',parts[('BTC',0,1000)],parts[('ETH',0,1000)],[0.5,0.5],'comparator_combination')
assert len(batch)==30
(ROUND/'batch.json').write_text(json.dumps(batch,indent=2)+'\n')
print('PASS:30 successfully reserved before evaluation;90 cost scenes frozen',flush=True)
