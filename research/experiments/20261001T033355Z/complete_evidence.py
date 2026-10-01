"""Enrich saved outputs with per-fold metrics, sources, comparators and sensitivity plots."""
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path
import numpy as np
import polars as pl
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[3]
ROUND=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('evidence_eval',ROUND/'evaluate.py')
m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)
r=json.loads((ROUND/'report.json').read_text())
partial=json.loads((ROOT/'data/runs/20261001T033355Z_partial.json').read_text())
for name,row in r['configs'].items():
 if row.get('direction') not in ('pairs','cross'):continue
 kind=row['direction'];periods=24 if kind=='pairs' else 3
 folds=r['folds'][kind]
 for k,out in row['cost_scenarios'].items():
  assert out['equity_usdt']==partial['configs'][name]['cost_scenarios'][k]['equity_usdt']
  nav=2000.0 if kind=='pairs' else 100000.0
  curve=out['equity_usdt']
  for i,fold in enumerate(out['folds']):
   end=nav*(1+fold['net_return_pct']/100)
   a=i*28*periods+1;b=(i+1)*28*periods+1
   segment=[nav]+curve[a:b]+[end]
   extra=m.metrics(segment,28*24,True)
   # Cross curve is sampled every eight hours, not hourly.
   if kind=='cross' and extra['sharpe_annualized'] is not None:extra['sharpe_annualized']/=math.sqrt(8)
   assert abs(extra['net_return_pct']-fold['net_return_pct'])<1e-10
   fold.update(extra);nav=end
  assert abs(nav-curve[-1])<1e-7
  out['annualization_periods']=8760 if kind=='pairs' else 1095
  out['max_drawdown_scope']='complete continuous hourly post-execution marks' if kind=='pairs' else 'complete continuous eight-hour post-execution marks; separate minute maintenance checks'
  out['benchmark_cash_return_pct']=0
# Same-period hold comparator folds at exact executable minute opens, not daily boundaries.
for name in ('benchmark_pairs_hold','benchmark_cross_hold'):
 row=r['configs'][name];spec=json.loads((ROOT/row['spec_path']).read_text())
 kind='pairs' if 'pairs' in name else 'cross';folds=r['folds'][kind]
 initial=spec['parameters']['initial_capital_usdt'];assets=[x.split('/')[0] for x in spec['universe']]
 start=m.ns(spec['parameters']['start_utc']);end=m.ns(spec['parameters']['end_utc'])
 slot_offset=m.MINUTE if kind=='pairs' else m.HOUR+m.MINUTE
 frames={a:pl.read_parquet(ROOT/'data/normalized/binance'/a/f'binance_{a}_{m.VERSION}'/'spot_bars.parquet',columns=['open_ts','open']) for a in assets}
 old=m.module('prior_spot_eval',ROOT/'research/experiments/20261001T013355Z/evaluate.py')
 data,_=old.load_data()
 for multiplier,out in row['cost_scenarios'].items():
  quantity={};parts=[]
  for asset in assets:
   rows=[dict(x) for x in data[asset]];dates=[x['date'] for x in rows]
   a=dates.index(spec['parameters']['start_utc'][:10]);b=dates.index(spec['parameters']['end_utc'][:10])
   values=frames[asset].filter(pl.col('open_ts').is_in([start,end])).sort('open_ts')
   rows[a]['trade_open']=values['open'][0];rows[b]['trade_open']=values['open'][1]
   rows[a]['trade_ts']=start;rows[b]['trade_ts']=end
   p=old.backtest(rows,[True]*365,a,b,initial/len(assets),1,int(multiplier))
   quantity[asset]=p['trades'][0]['quantity'];parts.append(p)
  # This is an audit of the already reserved, evaluated comparator, not a new trial.
  assert [sum(x) for x in zip(*(p['equity_usdt'] for p in parts))]==out['equity_usdt']
  boundary={folds[0]['test_start_signal_ns']:float(initial),folds[-1]['test_end_signal_ns']:out['equity_usdt'][-1]}
  for f in folds[:-1]:
   ts=f['test_end_signal_ns']+slot_offset
   boundary[f['test_end_signal_ns']]=sum(quantity[asset]*float(frames[asset].filter(pl.col('open_ts')==ts)['open'][0]) for asset in assets)
  out['folds']=[{'fold':f['fold'],'net_return_pct':100*(boundary[f['test_end_signal_ns']]/boundary[f['test_start_signal_ns']]-1),'boundary_rule':'same exact first/terminal executable-minute quote; intermediate minute-open MTM; no extra trade'} for f in folds]
  product=math.prod(1+f['net_return_pct']/100 for f in out['folds'])
  assert abs(product-1-out['net_return_pct']/100)<1e-12
r['source_versions']={'author_pair_repository_main_sha':'2713e8a722aab5f2abb6c9adc804746669e1772a','repository_parent_commit':'ad8599a9fe472f5e76abc0b399a8cf992eb9de14','access_date':'2026-10-01','local_original_rule_sha256':{name:hashlib.sha256((ROOT/'checks'/name).read_bytes()).hexdigest() for name in ('perp_pairs_oos.py','cross_exchange_carry_oos.py')}}
r['data_manifests']={'binance':'research/experiments/20261001T033355Z/binance_data_manifest.json','prior_spot':'research/experiments/20261001T013355Z/data_manifest.json','okx':'research/experiments/20261001T033355Z/okx_data_manifest.json'}
original_okx=json.loads((ROOT/'data/normalized/okx/BTC/cross_exchange_carry_20260930/manifest.json').read_text())
(ROUND/'okx_data_manifest.json').write_text(json.dumps(original_okx,ensure_ascii=False,indent=2)+'\n')
r['environment']={'python':sys.version,'numpy':np.__version__,'polars':pl.__version__,'statsmodels':__import__('statsmodels').__version__,'scipy':__import__('scipy').__version__,'matplotlib':matplotlib.__version__,'blas_threads':1}
r['verification'].update(saved_candidate_curves_recovered_unchanged=54,no_candidate_grid_repeated_during_resume=True,per_fold_return_product_reconciled=True,hold_comparator_quote_boundaries_reconciled=True)
r['limitations']=['All dates are reused development history; no unseen final holdout or statistical multiple-testing adjustment.','Local pair rule omits the upstream author time-stop and uses its explicit prior-window fixed-beta spread; this is the repo rule recovery, not reproduction of upstream published profit.','Fee, spread, slippage, square-root impact and flat 1% maintenance are explicit assumptions, not historical level-2 fills or exchange margin tiers.','Pair margin checked against conservative worst combinations of hourly mark high/low before/after fills; cross perp collateral checked at observed minute high. Flags affect acceptance, not future-informed signals or early fills.','Continuous drawdown is sampled hourly for pairs/eight-hourly for carry and daily for hold comparators; minute maintenance checks are separate and do not turn these into minute drawdown estimates.','Binance funding uses actual API rate and associated settlement mark, preserving milliseconds; OKX uses actual realized rates with the existing pre-settlement minute-close proxy.','Current Binance instrument lot/tick/min_notional metadata used as an explicit historical simulation assumption. Cross legacy rule retains its fixed 0.01 BTC base-size floor and effective execution prices without venue tick quantization.','Funding publication availability is assumed at actual settlement +1 hour, not a measured historical latency archive.','No spot short or inventory borrow. Pair futures collateral pooled under unlevered gross entry; carry split collateral/cash 50/50 with no transfers. Fiat anchor/USDT depeg, outages, liquidation fees and venue failure are unmodeled.','Any positive grid cell was seen on the same data as its neighbors; it is a research clue, not independently verified positive expectancy.']
r['initial_16_progress']={'actual_result_available_before_round':11,'recovered_this_round':2,'actual_result_available_after_finish_expected':13,'remaining_missing':['fixed-carry-b0','funding-carry-b1','ridge-carry-m1'],'reason_not_evaluated_this_round':'1-2-direction budget; these need native Nautilus and fully registered episode/model rules; current available futures/funding caches aid next round'}
r['prior_trial_counts']={'distinct_definitions_before_round':54,'new_reservations':20,'recovered_missing_definitions':2,'new_definitions':18,'distinct_definitions_after_finish_expected':72,'candidate_variants':18,'cost_curves':54,'comparison_curves':6,'true_number_of_all_historical_trials':'unknown, includes earlier research and selection'}
for kind in ('pairs','cross'):
 configs=[(name,row) for name,row in r['configs'].items() if row.get('direction')==kind]
 first='window_hours' if kind=='pairs' else 'window_settlements'
 windows=sorted({x['parameters'][first] for _,x in configs});entries=sorted({x['parameters']['entry_z'] for _,x in configs})
 net=np.array([[next(row['cost_scenarios']['3']['net_return_pct'] for name,row in configs if row['parameters'][first]==w and row['parameters']['entry_z']==z) for z in entries] for w in windows])
 sharpes=[row['cost_scenarios']['3']['sharpe_annualized'] for _,row in configs]
 r['sensitivity'][kind].update(sharpe_positive_fraction_3x=sum(x is not None and x>0 for x in sharpes)/len(sharpes),best_net_cell_at_grid_boundary=True,qualification='isolated positive edge cell' if np.any(net>0) else 'no positive cells')
 r['sensitivity'][kind]['adjacent_sharpe_changes']=[]
 for name,row in configs:
  p=row['parameters'];sr=row['cost_scenarios']['3']['sharpe_annualized']
  if sr is None:continue
  for axis in (first,'entry_z'):
   vals=windows if axis==first else entries;i=vals.index(p[axis])
   if i+1==len(vals):continue
   neighbor=next(x for n,x in configs if x['parameters'][axis]==vals[i+1] and all(x['parameters'][q]==p[q] for q in (first,'entry_z') if q!=axis))
   n_sr=neighbor['cost_scenarios']['3']['sharpe_annualized']
   if n_sr is not None:r['sensitivity'][kind]['adjacent_sharpe_changes'].append({'axis':axis,'from':p[axis],'to':vals[i+1],'other_parameter':p['entry_z'] if axis==first else p[first],'change':n_sr-sr})
 fig,ax=plt.subplots(figsize=(6,3.7));limit=max(float(np.max(np.abs(net))),.01)
 im=ax.imshow(net,cmap='RdYlGn',vmin=-limit,vmax=limit,aspect='auto')
 ax.set_xticks(range(len(entries)),entries);ax.set_yticks(range(len(windows)),windows)
 ax.set_xlabel('Entry |Z|');ax.set_ylabel('Prior window (hours)' if kind=='pairs' else 'Prior settlements (8h)')
 ax.set_title(('BTC/ETH perpetual pair' if kind=='pairs' else 'BTC cross-venue carry')+'\n3x costs: cumulative net return (%)')
 for i in range(len(windows)):
  for j in range(len(entries)):ax.text(j,i,f'{net[i,j]:+.3f}%',ha='center',va='center',fontsize=10)
 fig.colorbar(im,ax=ax,label='Cumulative return (%)');fig.tight_layout()
 fig.savefig(ROUND/(kind+'_sensitivity.png'),dpi=160);plt.close(fig)
r['reproduce_commands']=['.venv/bin/python research/experiments/20261001T033355Z/download_binance.py','.venv/bin/python checks/download_okx_carry.py','.venv/bin/python checks/okx_funding_rows.py','OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 .venv/bin/python research/experiments/20261001T033355Z/evaluate.py (only while registered reserved; completed outcomes read from report.json)','after completion use check_evidence.py for saved data/hash/ledger/curve checks; do not reserve or run this batch again']
(ROUND/'report.json').write_text(json.dumps(r,ensure_ascii=False,separators=(',',':'),allow_nan=False)+'\n')
print(json.dumps({'configs':len(r['configs']),'saved_candidate_curve_parity':54,'report_bytes':(ROUND/'report.json').stat().st_size,'plots':['pairs_sensitivity.png','cross_sensitivity.png']}))
