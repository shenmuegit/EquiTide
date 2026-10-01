"""Fixed grid validation, reusing the repository's daily bars, OBV rule and splitter."""
from __future__ import annotations
import csv
import importlib.util
import json
import math
import statistics
import subprocess
import sys
from datetime import datetime, timezone
from decimal import Decimal as D
from pathlib import Path
import polars as pl

ROOT=Path(__file__).resolve().parents[3]
ROUND=Path(__file__).resolve().parent
DAY_NS=86_400_000_000_000
MINUTE_NS=60_000_000_000
VERSION='20250916T000000Z_20260916T000000Z_archive_20260929'


def module(name,path):
 s=importlib.util.spec_from_file_location(name,path)
 m=importlib.util.module_from_spec(s)
 sys.modules[name]=m
 s.loader.exec_module(m)
 return m


def sma_signals(closes,n):
 # Decision index i sees only completed days strictly before i.
 return [False if i<n else closes[i-1]>sum(closes[i-n:i])/n for i in range(len(closes))]


def lagged_cost_inputs(rows,i):
 if i<20:
  raise ValueError('20 complete historical days needed for cost estimation')
 adv=statistics.mean(float(x['quote_volume']) for x in rows[i-20:i])
 closes=[float(x['close']) for x in rows[i-21:i]] if i>=21 else [float(x['close']) for x in rows[:i]]
 log_returns=[math.log(b/a) for a,b in zip(closes,closes[1:])]
 sigma=statistics.stdev(log_returns)
 return adv,sigma


def metrics(equity,days,terminal_extra=False):
 if any(x<=0 for x in equity):
  raise ValueError('nonpositive equity')
 peak=equity[0]
 dd=0.0
 for x in equity:
  peak=max(peak,x)
  dd=max(dd,1-x/peak)
 stats_equity=equity[:-2]+[equity[-1]] if terminal_extra else equity
 returns=[b/a-1 for a,b in zip(stats_equity,stats_equity[1:])]
 sd=statistics.stdev(returns) if len(returns)>1 else 0
 sharpe=statistics.mean(returns)/sd*math.sqrt(365) if sd else None
 cagr=(equity[-1]/equity[0])**(365/days)-1
 return {'net_return_pct':100*(equity[-1]/equity[0]-1),'max_drawdown_pct':100*dd,'sharpe_365':sharpe,'cagr_pct':100*cagr,'calmar':cagr/dd if dd else None}


def backtest(rows,signals,start,end,capital,allocation,multiplier,impact=True):
 # end is an exclusive daily decision boundary; liquidate at its 00:01 open.
 permanent=float(capital)*(1-allocation)
 cash=float(capital)*allocation
 units=0.0
 equity=[float(capital)]
 trades=[]
 fee=.001*multiplier
 spread=.0001*multiplier
 slip=.0002*multiplier
 def execute(i,buy,terminal=False):
  nonlocal cash,units
  ref=float(rows[i]['trade_open'])
  adv,sigma=lagged_cost_inputs(rows,i) if impact else (float('inf'),0.0)
  budget=cash if buy else units*ref
  if budget/adv>.001:
   raise ValueError('capacity: reference order exceeds 0.1% of lagged daily ADV')
  # Conservative impact base is pre-cost cash budget for buys and reference notional for sells.
  # Actual buy reference notional is smaller; no intraday future volume enters sizing.
  imp=.5*sigma*math.sqrt(budget/adv)*multiplier if impact else 0.0
  adverse=spread+slip+imp
  if buy:
   execution=ref*(1+adverse)
   quantity=cash/(execution*(1+fee))
   cost=cash-quantity*ref
   units=quantity
   cash=0.0
  else:
   execution=ref*(1-adverse)
   quantity=units
   proceeds=units*execution*(1-fee)
   cost=quantity*ref-proceeds
   cash=proceeds
   units=0.0
  trades.append({'date':rows[i]['date'],'side':'buy' if buy else ('terminal_sell' if terminal else 'sell'),'reference':ref,'execution':execution,'quantity':quantity,'fee_rate':fee,'half_spread_rate':spread,'slippage_rate':slip,'impact_rate':imp,'lagged_daily_quote_ADV':adv if impact else None,'lagged_daily_volatility':sigma if impact else None,'estimated_daily_participation':budget/adv,'cost_usdt':cost})
 for i in range(start,end):
  if rows[i-1]['close_available_ts']>=rows[i]['trade_ts']:
   raise ValueError('previous close not available before execution')
  if signals[i] and units==0:
   execute(i,True)
  elif not signals[i] and units>0:
   execute(i,False)
  equity.append(permanent+cash+units*float(rows[i]['close']))
 if rows[end-1]['close_available_ts']>=rows[end]['trade_ts']:
  raise ValueError('terminal previous close not available before execution')
 if units>0:
  execute(end,False,True)
 equity.append(permanent+cash)
 cost=sum(t['cost_usdt'] for t in trades)
 result={**metrics(equity,end-start,True),'equity_usdt':equity,'executions':len(trades),'round_trips':sum(t['side']!='buy' for t in trades),'cost_usdt':cost,'cost_pct_initial':100*cost/capital,'trades':trades}
 return result


def fold_metrics(equity,folds,start):
 out=[]
 for j,f in enumerate(folds):
  a=f['test_start_index']-start
  b=f['test_end_exclusive_index']-start
  if j==len(folds)-1:
   b=len(equity)-1
  segment=equity[a:b+1]
  out.append({'fold':j+1,**metrics(segment,f['test_end_exclusive_index']-f['test_start_index'],b-a>f['test_end_exclusive_index']-f['test_start_index'])})
 return out


def load_data():
 obv=module('legacy_obv',ROOT/'checks/obv_trend_oos.py')
 data={}
 for asset in ('BTC','ETH'):
  path=ROOT/'data/normalized/binance'/asset/f'binance_{asset}_{VERSION}'/'spot_bars.parquet'
  rows,digest=obv.daily_data(path)
  frame=pl.read_parquet(path,columns=['open_ts','quote_volume'])
  daily=frame.group_by((pl.col('open_ts')//DAY_NS).alias('day')).agg(pl.col('quote_volume').sum()).sort('day')
  assert len(rows)==daily.height
  for row,volume in zip(rows,daily['quote_volume']):
   row['quote_volume']=volume
  data[asset]=rows
 return data,obv


def rule_signals(spec,rows,obv):
 p=spec['parameters']
 closes=[r['close'] for r in rows]
 if 'lookback_days' in p:
  return sma_signals(closes,p['lookback_days'])
 obv.SHORT_DAYS,obv.LONG_DAYS=p['short_days'],p['long_days']
 sig=obv.obv_signal(closes,[r['volume'] for r in rows])
 return [False if i<p['long_days'] else sig[i-p['long_days']] for i in range(len(rows))]


def main():
 batch=json.loads((ROUND/'batch.json').read_text())
 replay='--reproduce' in sys.argv
 if replay:
  archived=json.loads((ROUND/'report.json').read_text())
 plan=json.loads((ROUND/'plan.json').read_text())
 registry=module('registry_round',ROOT/'research/automation/registry.py')
 ledger=registry.read_records(ROOT/'research/automation/registry.jsonl')
 for item in batch:
  expected=('passed','rejected') if replay else ('reserved',)
  assert ledger[item['fingerprint']]['status'] in expected,item
 data,obv=load_data()
 wf=module('walk_forward_round',ROOT/'.agents/skills/walk-forward-validation/scripts/walk_forward.py')
 splitter=wf.WalkForwardValidator(wf.WalkForwardConfig(train_size=180,test_size=30,step_size=30,window_type='rolling',purge_size=0,embargo_size=3))
 folds=[]
 dates=[r['date'] for r in data['BTC']]
 for f in splitter.split(365):
  a,b=int(f.test_indices[0]),int(f.test_indices[-1])+1
  folds.append({'fold':f.fold_idx+1,'train_start_index':int(f.train_indices[0]),'train_end_exclusive_index':int(f.train_indices[-1])+1,'test_start_index':a,'test_end_exclusive_index':b,'train_start_utc':dates[int(f.train_indices[0])],'train_last_date_utc':dates[int(f.train_indices[-1])],'test_start_utc':dates[a]+'T00:01:00Z','test_last_signal_day_utc':dates[b-1],'test_mark_end_utc':dates[b]+'T00:00:00Z'})
 start,end=folds[0]['test_start_index'],folds[-1]['test_end_exclusive_index']
 assert len(folds)==6 and all(a['test_end_exclusive_index']==b['test_start_index'] for a,b in zip(folds,folds[1:]))
 report={'created_at_utc':datetime.now(timezone.utc).isoformat(),'plan':plan,'data_manifest':'research/experiments/20261001T013355Z/data_manifest.json','data_hashes':json.loads((ROUND/'data_manifest.json').read_text())['normalized'],'folds':folds,'oos_start_utc':dates[start]+'T00:01:00Z','terminal_exit_utc':dates[end]+'T00:01:00Z','oos_decision_days':end-start,'equity_timestamps_utc':[dates[start]+'T00:01:00Z']+[dates[i+1]+'T00:00:00Z' for i in range(start,end)]+[dates[end]+'T00:01:00Z'],'parameter_fitting':'none; grid fixed before results; no OOS ranking is an independent test','purge_rationale':'no forward labels/model fit; completed daily indicators only; 3-day train/test embargo; position carries between consecutive tests','cost_model_note':'fee/spread/slippage are estimates, not historical quotes; impact uses pre-cost buy cash as conservative reference-notional upper bound and actual sell notional, previous 20 complete days only; no funding/borrow in long-only unlevered spot','configs':{},'benchmarks':{},'sensitivity':{},'historical_trial_counts':{'ledger_distinct_before_round':16,'this_round_strategies':36,'this_round_combinations':6,'total_reserved_this_round':len(batch),'initial_16_backtest_available_before_round':5,'initial_missing_queued_this_round':6,'selection_bias':'development history was already used; do not infer a pristine final holdout or stable live profit'},'environment':{'python':sys.version,'polars':pl.__version__},'reproduce':['.venv/bin/python research/experiments/20261001T013355Z/download_data.py','.venv/bin/python research/experiments/20261001T013355Z/check_accounting.py','.venv/bin/python checks/price_trend_oos.py','.venv/bin/python checks/obv_trend_oos.py','.venv/bin/python research/experiments/20261001T013355Z/evaluate.py']}
 signals={}
 specs={}
 byfp={}
 for item in batch:
  spec=json.loads((ROOT/item['spec']).read_text())
  specs[item['name']]=spec
  byfp[item['fingerprint']]=item['name']
  if spec['kind']!='strategy':
   continue
  asset=spec['universe'][0].split('/')[0]
  allocation=spec['parameters'].get('initial_risky_sleeve_fraction',1.0)
  sig=rule_signals(spec,data[asset],obv)
  signals[item['name']]=sig
  results={}
  for mult in (1,2,3):
   r=backtest(data[asset],sig,start,end,1000,allocation,mult)
   r['folds']=fold_metrics(r['equity_usdt'],folds,start)
   results[str(mult)]=r
  report['configs'][item['name']]={'fingerprint':item['fingerprint'],'spec_path':item['spec'],'asset':asset,'parameters':spec['parameters'],'cost_scenarios':results}
  print(json.dumps({'completed':item['name'],'return_1x':results['1']['net_return_pct'],'return_3x':results['3']['net_return_pct']}),flush=True)
 # Costed buy-and-hold is a comparator, not a novel strategy candidate/reservation.
 for asset in ('BTC','ETH'):
  bspec=json.loads((ROUND/'specs'/('benchmark_hold_'+asset+'.json')).read_text())
  bfp=registry.fingerprint(bspec)
  assert ledger[bfp]['status'] in (('passed','rejected') if replay else ('reserved',)),bfp
  report['benchmarks'][asset]={str(k):backtest(data[asset],[True]*365,start,end,1000,1.0,k) for k in (1,2,3)}
 report['benchmarks']['cash']={'net_return_pct':0,'max_drawdown_pct':0,'cash_yield':0}
 for item in batch:
  spec=specs[item['name']]
  if spec['kind']!='combination':
   continue
  raw=[float(x['weight']) for x in spec['components']]
  if spec['parameters'].get('initial_capital_usdt')==2000:
   assert abs(sum(raw)-1)<1e-12
   capital=[2000*w for w in raw]
  else:
   # Legacy raw weights 1,1 are USDT1000 sleeve units, not auto-normalised.
   capital=[1000*w for w in raw]
  total=sum(capital)
  results={}
  for k in (1,2,3):
   parts=[]
   for component,c in zip(spec['components'],capital):
    name=byfp[component['fingerprint']]
    asset=report['configs'][name]['asset']
    if c==1000:
     parts.append(report['configs'][name]['cost_scenarios'][str(k)])
    else:
     # Reuse rules and execution calendar; reprice size-dependent costs at new sleeve capital.
     parts.append(backtest(data[asset],signals[name],start,end,c,1.0,k))
   equity=[sum(vals) for vals in zip(*(p['equity_usdt'] for p in parts))]
   r={**metrics(equity,end-start,True),'equity_usdt':equity,'executions':sum(p['executions'] for p in parts),'cost_usdt':sum(p['cost_usdt'] for p in parts),'cost_pct_initial':100*sum(p['cost_usdt'] for p in parts)/total,'initial_sleeve_capital_usdt':capital,'component_metrics':[{key:p[key] for key in ('net_return_pct','max_drawdown_pct','executions','cost_usdt')} for p in parts]}
   r['folds']=fold_metrics(equity,folds,start)
   results[str(k)]=r
  report['configs'][item['name']]={'fingerprint':item['fingerprint'],'spec_path':item['spec'],'parameters':spec['parameters'],'raw_weights':raw,'weight_semantics':spec['logic']['allocation'],'cost_scenarios':results,'reuse':'equal-capital directly sums existing component curves; changed capital weights reuse fixed signals and execution times, reprice impact for actual sleeve sizes'}
 for family in ('sma','obv'):
  for asset in ('BTC','ETH'):
   group=[(name,row) for name,row in report['configs'].items() if name.startswith(family+'_'+asset)]
   fraction=sum(row['cost_scenarios']['3']['net_return_pct']>0 for name,row in group)/len(group)
   report['sensitivity'][family+'_'+asset]={'variants':len(group),'positive_fraction_at_3x':fraction,'return_range_pct_3x':[min(row['cost_scenarios']['3']['net_return_pct'] for _,row in group),max(row['cost_scenarios']['3']['net_return_pct'] for _,row in group)],'metrics_file':'sensitivity.csv','parameters':plan['sensitivity'],'assessment':'positive platform' if fraction>=.6 else 'insufficient positive neighborhood; inspect full grid'}
 for name,row in report['configs'].items():
  costs=row['cost_scenarios']
  positive_folds=sum(f['net_return_pct']>0 for f in costs['1']['folds'])
  if 'asset' in row:
   family='sma' if name.startswith('sma') else 'obv'
   neighborhood=report['sensitivity'][family+'_'+row['asset']]['positive_fraction_at_3x']
  else:
   family='sma' if name.startswith('sma') else 'obv'
   neighborhood=min(report['sensitivity'][family+'_'+a]['positive_fraction_at_3x'] for a in ('BTC','ETH'))
  criteria={'positive_at_1x_2x_3x':all(r['net_return_pct']>0 for r in costs.values()),'at_least_4_positive_1x_folds':positive_folds>=4,'drawdown_3x_lte_25pct':costs['3']['max_drawdown_pct']<=25,'neighborhood_3x_positive_fraction_gte_0_6':neighborhood>=.6,'at_least_2_executions':costs['1']['executions']>=2}
  row['criteria']=criteria
  row['positive_folds_1x']=positive_folds
  row['status']='passed' if all(criteria.values()) else 'rejected'
  row['interpretation']='historical development validation only; future forward simulation required' if row['status']=='passed' else 'failed prespecified development validation gates'
 csv_path=ROOT/'data/runs/reproduce_20261001_sensitivity.csv' if replay else ROUND/'sensitivity.csv'
 csv_path.parent.mkdir(parents=True,exist_ok=True)
 with csv_path.open('w',newline='') as file:
  w=csv.writer(file,lineterminator="\n")
  w.writerow(['config','fingerprint','cost_multiplier','parameters_or_weights','net_return_pct','max_drawdown_pct','sharpe_365','calmar','executions','cost_pct_initial','positive_folds','status'])
  for name,row in report['configs'].items():
   for k,r in row['cost_scenarios'].items():
    w.writerow([name,row['fingerprint'],k,json.dumps(row.get('raw_weights',row['parameters']),sort_keys=True),r['net_return_pct'],r['max_drawdown_pct'],r['sharpe_365'],r['calmar'],r['executions'],r['cost_pct_initial'],row['positive_folds_1x'],row['status']])
 report['summary']={'passed':[name for name,row in report['configs'].items() if row['status']=='passed'],'rejected':[name for name,row in report['configs'].items() if row['status']=='rejected']}
 output=ROOT/'data/runs/reproduce_20261001T013355Z.json' if replay else ROUND/'report.json'
 output.parent.mkdir(parents=True,exist_ok=True)
 if replay:
  for name,row in report['configs'].items():
   assert row['status']==archived['configs'][name]['status'],name
   for k,value in row['cost_scenarios'].items():
    old=archived['configs'][name]['cost_scenarios'][k]
    assert value['equity_usdt']==old['equity_usdt'],(name,k)
  print('REPRODUCE PASS: all 126 candidate cost curves match archived outcomes exactly',flush=True)
 output.write_text(json.dumps(report,ensure_ascii=False,separators=(',',':'),allow_nan=False)+'\n')
 print(json.dumps(report['summary']),flush=True)

if __name__=='__main__':
 main()
