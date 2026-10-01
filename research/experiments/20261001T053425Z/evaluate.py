"""Run only reserved configurations; gzip full curves/events to keep evidence lightweight."""
from __future__ import annotations
import argparse,gzip,hashlib,json,math,sys,platform
from collections import Counter
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
import numpy as np
import polars as pl
from carry import *
registry=module('registry_this_round',ROOT/'research/automation/registry.py')

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def dump(path,value):
 raw=json.dumps(value,ensure_ascii=False,allow_nan=False,separators=(',',':')).encode()
 Path(path).parent.mkdir(parents=True,exist_ok=True)
 Path(path).write_bytes(gzip.compress(raw,compresslevel=9,mtime=0) if str(path).endswith('.gz') else raw+b'\n')

def benchmark(data,m,folds):
 start=folds[0]['test_start_signal_ns'];end=folds[-1]['test_end_signal_ns'];a=data['times'].index(start);b=data['times'].index(end);rows=data['rows'][a:b+1]
 l=Ledger(10000);q=math.floor(4500/float(rows[0]['close'])/data['meta']['spot_lot'])*data['meta']['spot_lot'];cash=10000;eq=[10000.];trades=[];bounds={};boundset={f['test_start_signal_ns'] for f in folds}|{end}
 for i,row in enumerate(rows):
  price=float(row['fill']);t=row['ts'];value=cash+q*price if i else cash
  if t in boundset:bounds[t]=value
  if i in (0,len(rows)-1):
   change=q if i==0 else -q;_,details=per_side(data,t,change,[price,float(row['fill_perp'])]);impact=details[0]['impact']*m
   px=old.execution_price(price,change,.001*m,.0001*m,.0002*m,impact,data['meta']['spot_tick']);fee=abs(change*px)*.001*m;cost=abs(change)*abs(px-price)+fee
   cash-=change*px+fee;trades.append({'ts':t+MINUTE,'quantity':change,'reference':price,'execution':px,'fee_usdt':fee,'cost_usdt':cost,**details[0]})
  eq.append(cash+(q*price if i<len(rows)-1 else 0))
 bounds[end]=eq[-1];fold_metrics=[]
 for f in folds:
  k=(f['test_start_signal_ns']-start)//HOUR;j=(f['test_end_signal_ns']-start)//HOUR
  curve=[bounds[f['test_start_signal_ns']]]+eq[k+1:j+1]+[bounds[f['test_end_signal_ns']]]
  fold_metrics.append({**f,**old.metrics(curve,28*24,True),'start_nav':curve[0],'end_nav':curve[-1]})
 assert abs(np.prod([x['end_nav']/x['start_nav'] for x in fold_metrics])-eq[-1]/10000)<1e-9
 return {**old.metrics(eq,(end-start)/HOUR,True),'initial_capital_usdt':10000,'final_NAV':eq[-1],'round_trips':1,'executions':2,'execution_cost_usdt':sum(t['cost_usdt'] for t in trades),'execution_cost_pct_initial':sum(t['cost_usdt'] for t in trades)/100,'funding_usdt':0,'cash_margin_violations':[],'folds':fold_metrics,'trades':trades,'equity':eq,'equity_signal_times':[r['ts'] for r in rows]}

@dataclass(frozen=True)
class StressedFundingPoint:
 settlement_ts:int
 available_ts:int
 realized_rate:Decimal
 mark_price:Decimal
 interval_hours:Decimal
 original_rate:Decimal
 def observation(self):
  from usdt_quant.strategy import FundingObservation
  return FundingObservation(self.settlement_ts,self.available_ts,self.original_rate,self.interval_hours)

def native(data,p,m):
 from usdt_quant.backtest import BacktestData,MarketPoint,InstrumentMetadata,run_backtest
 from usdt_quant.strategy import BacktestConfig
 start=ns(p['start_utc']);end=ns(p['end_utc']);d=Decimal
 market=tuple(MarketPoint.from_mid(r['ts'],r['close'],r['close_perp'],data['marks'][r['ts']-HOUR]['close'],d(0)) for r in data['rows'] if start<=r['ts']<=end)
 meta=data['meta'];metadata=InstrumentMetadata(d(1),d(str(meta['spot_lot'])),d(str(meta['perp_lot'])),d(str(meta['spot_tick'])),d(str(meta['perp_tick'])))
 events=tuple(StressedFundingPoint(e['ts'],e['available'],d(str(e['rate']*(m if e['rate']<0 else 1))),d(str(e['mark'])),d(str(e['hours'])),d(str(e['rate']))) for e in data['events'])
 history=tuple(e.observation() for e in events)
 q=math.floor(4500/float(market[0].spot_ask)/meta['common_lot'])*meta['common_lot']
 config=BacktestConfig(baseline=p['baseline'],data_version=VERSION,exchange='binance',base_asset=data['asset'],start_ns=start,end_ns=end,decision_interval_ns=HOUR,holding_period_ns=p['holding_hours']*HOUR,funding_window=21,initial_spot_usdt=d(5000),initial_perp_usdt=d(5000),target_spot_base=d(str(q)),spot_taker_fee=d('.001')*m,perp_taker_fee=d('.0002')*m,execution_bps_per_leg=d(5)*m,buffer_usdt=d(1))
 outdir=ROOT/'data/runs/20261001T053425Z_native'/f"{p['baseline']}_{data['asset']}_h{p['holding_hours']}_c{m}"
 result=run_backtest(config,BacktestData(market,events,history,metadata),outdir)
 result['full_native_artifacts']={name:[json.loads(line) for line in Path(path).read_text().splitlines()] for name,path in result['artifacts'].items() if name!='summary'}
 result['actual_source_funding']=[e for e in data['events'] if start<=e['ts']<=end]
 result['cost_pressure_note']='Paid negative funding rate scaled for native cash settlement; observation() preserves actual raw rate for forecasts. Native fee/execution gates respond to their declared stressed config. Flat original native execution does not include volume impact; continuous candidates include it.'
 return result

def summarize(result,role):
 if role=='native':
  s=result['summary'];return {'net_return_pct':float(Decimal(s['net_pnl_usdt'])/10000*100),'max_drawdown_pct':float(Decimal(s['max_drawdown_rate'])*100),'executions':s['fill_count'],'funding_usdt':float(s['funding_usdt']),'fee_usdt':float(s['fees_usdt']),'status':s['status'],'entry_fill_ts':s['entry_fill_ts'],'exit_fill_ts':s['exit_fill_ts']}
 excluded={'equity','equity_signal_times','trades','funding_events','decisions'}
 out={k:v for k,v in result.items() if k not in excluded}
 if 'decisions' in result:
  out['decision_counts']=dict(Counter(x['action'] for x in result['decisions']));out['decision_sha256']=hashlib.sha256(json.dumps(result['decisions'],sort_keys=True).encode()).hexdigest()
 out['max_participation']=max([x['participation'] for x in result['trades']] or [0]);return out

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--resume',action='store_true');parser.add_argument('--reproduce',action='store_true');args=parser.parse_args()
 batch=json.loads((ROUND/'batch.json').read_text());plan=json.loads((ROUND/'plan.json').read_text());records=registry.read_records(ROOT/'research/automation/registry.jsonl')
 for row in batch:
  s=json.loads((ROOT/row['spec']).read_text());assert registry.fingerprint(s)==row['fingerprint'];assert records[row['fingerprint']]['status'] in ('passed','rejected') if args.reproduce else records[row['fingerprint']]['status']=='reserved'
 folds=old.folds_for('pairs');data={asset:load(asset) for asset in ('BTC','ETH')}
 report={'round':plan['round'],'plan_sha256':sha(ROUND/'plan.json'),'parent_commit':plan['parent_commit'],'folds':folds,'method':'fixed parameters, causal rolling funding features; six chronological development folds; continuous holdings across boundaries; no supervised labels, purge=0','data':{a:{'hashes':x['hashes'],'metadata':x['meta'],'hourly_quotes':len(x['rows']),'funding_count':len(x['events'])} for a,x in data.items()},'trials':[],'native_recovery':[],'legacy_recovery':[],'benchmarks':[],'environment':{'python':platform.python_version(),'numpy':np.__version__,'polars':pl.__version__,'nautilus_trader':__import__('nautilus_trader').__version__,'sklearn':__import__('sklearn').__version__},'assumptions_and_limits':plan['limits']}
 for row in batch:
  if row['role']=='legacy_aggregate':continue
  spec=json.loads((ROOT/row['spec']).read_text());p=spec['parameters'];asset=spec['universe'][0].split('/')[0];role=row['role'];path=ROUND/'results'/(row['name']+'.json.gz')
  if args.resume and path.exists():
   results=json.loads(gzip.decompress(path.read_bytes()));print('RESUME',row['name'],flush=True)
  else:
   results={}
   for m in (1,2,3):
    results[str(m)]=native(data[asset],p,m) if role=='native' else (benchmark(data[asset],m,folds) if role=='benchmark' else simulate(data[asset],p,m,folds))
    print(json.dumps({'name':row['name'],'cost':m,**{k:v for k,v in summarize(results[str(m)],role).items() if k in ('net_return_pct','max_drawdown_pct','round_trips','executions','status')}}),flush=True)
   if args.reproduce:
    archived=json.loads(gzip.decompress(path.read_bytes()));assert results==archived,'full reproduction mismatch '+row['name']
   else:dump(path,results)
  entry={**row,'parameters':p,'full_result_path':str(path.relative_to(ROOT)),'full_result_sha256':sha(path),'scenarios':{str(m):summarize(results[str(m)],role) for m in (1,2,3)}}
  report[{'candidate':'trials','native':'native_recovery','benchmark':'benchmarks'}[role]].append(entry)
 # The legacy registry entries were broad scopes rather than fully specified cases.
 for row in batch:
  if row['role']=='legacy_aggregate':
   baseline=row['name'].split('_')[-1];children=[x['fingerprint'] for x in report['native_recovery'] if x['parameters']['baseline']==baseline]
   report['legacy_recovery'].append({**row,'concrete_children':children,'actual_backtest_available':True,'qualification':'original engineering scope now has archived real native cases; no long-run qualification from 72h case alone'})
 for asset in ('BTC','ETH'):
  for baseline in ('B0','B1'):
   group=[x for x in report['trials'] if x['parameters']['baseline']==baseline and asset in x['name']];share=sum(int(x['scenarios']['3']['net_return_pct']>0) for x in group)/len(group)
   for x in group:
    s=x['scenarios'];reasons=[]
    if not all(s[str(m)]['net_return_pct']>0 for m in (1,2,3)):reasons.append('cost_pressure_nonpositive')
    if s['1']['positive_folds_1x']<4:reasons.append('fewer_than_4_positive_folds')
    if s['3']['max_drawdown_pct']>25:reasons.append('drawdown_above_25_pct')
    if share<.6:reasons.append('parameter_neighborhood_below_60_pct_positive')
    if s['1']['round_trips']<4:reasons.append('fewer_than_4_round_trips')
    if any(s[str(m)]['cash_margin_violations'] for m in (1,2,3)):reasons.append('cash_or_margin_violation')
    x.update(neighborhood_positive_fraction_3x=share,qualification='rejected' if reasons else 'passed',failure_reasons=reasons)
 report['qualified']=sum(int(x['qualification']=='passed') for x in report['trials'])
 report['multiple_trials_note']='72 prior distinct definitions; 34 concrete new definitions and 2 initial incomplete scopes recovered this round; family naming is ignored by structural dedup; reused development history, total pre-registry trials unknown'
 report['native_cost_scope']='Native recovery has original flat spread/slippage only, paid-funding and execution stress. Volume impact, two-parameter sensitivity and long-window continuous folds assessed in registered repeated extensions; native 72h cases are not claimed to pass these gates.'
 if args.reproduce:
  print('REPRODUCE PASS: 24 continuous candidates, 8 native cases and 2 comparators; all 102 scenario outputs exactly match archived results');return
 dump(ROUND/'report.json',report)
 with (ROUND/'sensitivity.csv').open('w') as f:
  writer=csv.DictWriter(f,fieldnames=['name','asset','baseline','holding_hours','per_leg_fraction','buffer_usdt','cost_multiplier','net_return_pct','max_drawdown_pct','sharpe_annualized','calmar','round_trips','execution_cost_usdt','funding_usdt','positive_folds','neighborhood_positive_fraction_3x','qualification']);writer.writeheader()
  for trial in report['trials']:
   for m,s in trial['scenarios'].items():
    p=trial['parameters'];writer.writerow({'name':trial['name'],'asset':trial['name'].split('_')[1],**{k:p[k] for k in ('baseline','holding_hours','per_leg_fraction','buffer_usdt')},'cost_multiplier':m,**{k:s[k] for k in ('net_return_pct','max_drawdown_pct','sharpe_annualized','calmar','round_trips','execution_cost_usdt','funding_usdt')},'positive_folds':s['positive_folds_1x'],'neighborhood_positive_fraction_3x':trial['neighborhood_positive_fraction_3x'],'qualification':trial['qualification']})
 print('COMPLETED',len(report['trials']),len(report['native_recovery']),len(report['benchmarks']),'qualified',report['qualified'])

if __name__=='__main__':main()
