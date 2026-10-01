"""Reuse frozen causal factors; new maturable7/14/28day labels and8h native cases."""
from __future__ import annotations
import bisect,hashlib,importlib.util,json,math,sys
from bisect import bisect_left,bisect_right
from dataclasses import replace
from decimal import Decimal
from pathlib import Path
import numpy as np
import polars as pl
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))

def module(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
previous=module('m1_prior_long0936',ROOT/'research/experiments/20261001T073555Z/ridge.py')
carry=previous.carry;old=carry.old;prev=previous.prev
Ledger,FundingBook,HOUR,MINUTE,DAY,VERSION=previous.Ledger,previous.FundingBook,previous.HOUR,previous.MINUTE,previous.DAY,previous.VERSION
per_side,load,ns,utc=previous.per_side,previous.load,previous.ns,previous.utc
FACTORS,train_mask=previous.FACTORS,previous.train_mask
native_data,run_backtest,BacktestData=previous.native_data,previous.run_backtest,previous.BacktestData
from usdt_quant.backtest import execution_points,position_quantities

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def events_between(events,entry,end):
 times=[x['ts'] for x in events];return events[bisect_right(times,entry):bisect_right(times,end)]

def make_folds():
 wf=module('wf_long0936',ROOT/'.agents/skills/walk-forward-validation/scripts/walk_forward.py');base=ns('2025-09-16T00:00:00Z');splitter=wf.WalkForwardValidator(wf.WalkForwardConfig(train_size=180,test_size=28,step_size=28,embargo_size=56,purge_size=0));out=[]
 for f in splitter.split(365):
  train_start=base+int(f.train_indices[0])*DAY;train_end=base+(int(f.train_indices[-1])+1)*DAY;start=base+int(f.test_indices[0])*DAY;end=base+(int(f.test_indices[-1])+1)*DAY
  out.append({'fold':f.fold_idx+1,'train_start_utc':utc(train_start),'train_end_exclusive_utc':utc(train_end),'train_end_exclusive_ns':train_end,'test_start_signal_ns':start,'test_end_signal_ns':end,'test_start_utc':utc(start+MINUTE),'test_end_utc':utc(end+MINUTE)})
 assert len(out)==4 and out[0]['test_start_signal_ns']==ns('2026-05-10T00:00:00Z') and out[-1]['test_end_signal_ns']==ns('2026-08-30T00:00:00Z');return out

def reused_features(data):
 report_path=ROOT/'research/experiments/20261001T073555Z/report.json';r=json.loads(report_path.read_text());entry=r['data'][data['asset']];path=ROOT/entry['derived_evidence_path']
 assert data['hashes']==entry['hashes'];assert sha(path)==entry['derived_evidence_sha256'];assert sha(ROOT/'src/usdt_quant/research.py')==r['source_code_sha256']['src/usdt_quant/research.py']
 import gzip
 e=json.loads(gzip.decompress(path.read_bytes()));f=pl.DataFrame(e['features'],schema={'decision_ts':pl.Int64,'input_max_available_ts':pl.Int64,**{n:pl.Float64 for n in FACTORS}})
 assert f['decision_ts'].to_list()==data['times'];assert not f.filter(pl.col('input_max_available_ts')>pl.col('decision_ts')).height
 return f,{'path':str(path.relative_to(ROOT)),'sha256':sha(path),'original_report':str(report_path.relative_to(ROOT)),'original_report_sha256':sha(report_path),'reuse_scope':'causal feature rows only; prior24h labels/models/strategy paths not evaluated again'}

def fitted_predictions(frame,folds,alpha,native=False):
 return previous.fitted_predictions(frame,folds,alpha,native=native)

def simulate(data,parameters,multiplier,folds,predictions):
 return previous.simulate(data,parameters,multiplier,folds,predictions)

def native_config(data,m=1,whole_history=False):
 return replace(previous.native_config(data,m,whole_history=whole_history),holding_period_ns=8*HOUR)

def native_run(data,m,predictions):
 cfg=native_config(data,m);directory=ROOT/'data/runs/20261001T093625Z_native'/f"M1_{data['asset']}_h8_c{m}"
 result=run_backtest(cfg,native_data(data,m),directory,{t:Decimal(str(v)) for t,v in predictions.items()});result['full_native_artifacts']={name:[json.loads(line) for line in Path(path).read_text().splitlines()] for name,path in result['artifacts'].items() if name!='summary'}
 result['actual_source_funding']=[e for e in data['events'] if cfg.start_ns<=e['ts']<=cfg.end_ns];result['forecast_source']='first180d pre3dayembargo mature8h-label training-only Ridge; basecost prediction frozen72h and acrosscoststress';return result

# Generic H labels preserve previous minute execution accounting.
def continuous_labels(data,h):
 rows=[];event_times=[e['ts'] for e in data['events']];span=h
 for i,r in enumerate(data['rows']):
  t=r['ts'];j=i+span
  if j>=len(data['rows']):continue
  exitrow=data['rows'][j];assert exitrow['ts']==t+h*HOUR
  if t//DAY not in data['costs'][0] or t//DAY not in data['costs'][1]:continue
  q=math.floor(2500/float(r['close'])/data['meta']['common_lot'])*data['meta']['common_lot']
  total=0.;execution_cost=0.;fees=0.
  for row,change in ((r,q),(exitrow,-q)):
   refs=[float(row['fill']),float(row['fill_perp'])];_,details=per_side(data,row['ts'],change,refs)
   for k in (0,1):
    sign=change if k==0 else -change;tick=data['meta']['spot_tick' if k==0 else 'perp_tick'];fee=details[k]['base_fee']
    px=old.execution_price(refs[k],sign,fee,.0001,.0002,details[k]['impact'],tick)
    paid=abs(change*px)*fee;total-=sign*px+paid;fees+=paid;execution_cost+=abs(change)*abs(px-refs[k])+paid
  entry=t+MINUTE;end=exitrow['ts']+MINUTE;events=data['events'][bisect.bisect_right(event_times,entry):bisect.bisect_right(event_times,end)]
  funding=sum(q*e['mark']*e['rate'] for e in events);net=total+funding
  rows.append({'decision_ts':t,'entry_ts':entry,'label_end_ts':end,'label_available_ts':max([end]+[e['available'] for e in events]),'y_net':net/10000,'target_quantity':q,'funding_usdt':funding,'fees_usdt':fees,'execution_cost_usdt':execution_cost})
 return pl.DataFrame(rows)


# Native8h labels preserve original Decimal cashflow and publication definition.
def native_labels(config, data: BacktestData, decisions: list[int]) -> pl.DataFrame:
    points = execution_points(config, data)
    times = [point.ts for point in points]
    settlement_times = [point.settlement_ts for point in data.funding]
    spot_qty, contracts = position_quantities(config, data.metadata)
    perp_qty = contracts * data.metadata.contract_multiplier
    nav = config.initial_spot_usdt + config.initial_perp_usdt
    precision = Decimal("0.00000001")
    rows = []
    for timestamp in decisions:
        for horizon, hours in (("8h", 8),):
            row = {"decision_ts": timestamp, "horizon": horizon, "entry_ts": None,
                   "label_end_ts": None, "label_available_ts": None, "y_funding": None,
                   "y_net": None, "y_flip": None, "y_loss": None, "fees_usdt": None,
                   "execution_cost_usdt": None, "max_basis_expansion": None, "reason": None}
            next_settlement = bisect_right(settlement_times, timestamp)
            if hours is None and next_settlement == len(settlement_times):
                row["reason"] = "next_settlement_unavailable"
                rows.append(row)
                continue
            target = timestamp + hours * HOUR if hours else settlement_times[next_settlement]
            entry_index, exit_index = bisect_right(times, timestamp), bisect_left(times, target)
            if exit_index >= len(times) or entry_index >= exit_index:
                row["reason"] = "incomplete_price_horizon"
                rows.append(row)
                continue
            entry, exit = points[entry_index], points[exit_index]
            if hours is not None and exit.ts != target:
                row["reason"] = "missing_horizon_exit_record"
                rows.append(row)
                continue
            events = data.funding[bisect_right(settlement_times, entry.ts):bisect_right(settlement_times, exit.ts)]
            if any(event.mark_price is None for event in events):
                row["reason"] = "settlement_mark_missing"
                rows.append(row)
                continue
            fees = sum((amount.quantize(precision) for amount in (
                spot_qty * entry.spot_ask * config.spot_taker_fee,
                spot_qty * exit.spot_bid * config.spot_taker_fee,
                perp_qty * entry.perp_bid * config.perp_taker_fee,
                perp_qty * exit.perp_ask * config.perp_taker_fee)), Decimal(0))
            funding = sum(((perp_qty * event.mark_price * event.realized_rate).quantize(precision)
                           for event in events), Decimal(0))
            pnl = spot_qty * (exit.spot_bid - entry.spot_ask) + perp_qty * (entry.perp_bid - exit.perp_ask)
            entry_mid = data.market[entry_index]
            exit_mid = data.market[exit_index]
            reference_spot = (entry_mid.spot_ask + entry_mid.spot_bid) / 2
            mid_pnl = spot_qty * ((exit_mid.spot_bid + exit_mid.spot_ask) / 2 - reference_spot)
            mid_pnl += perp_qty * ((entry_mid.perp_bid + entry_mid.perp_ask -
                                   exit_mid.perp_bid - exit_mid.perp_ask) / 2)
            basis_values = [float((point.perp_bid + point.perp_ask) /
                                  (point.spot_bid + point.spot_ask) - 1)
                            for point in data.market[entry_index:exit_index + 1]]
            net = (pnl + funding - fees).quantize(precision)
            row.update(entry_ts=entry.ts, label_end_ts=exit.ts,
                       label_available_ts=max([exit.ts] + [event.available_ts for event in events]),
                       y_funding=float(funding / (spot_qty * reference_spot)), y_net=float(net / nav),
                       y_flip=int(any(event.realized_rate < 0 for event in events)), y_loss=int(net < 0),
                       fees_usdt=float(fees), execution_cost_usdt=float(mid_pnl - pnl),
                       max_basis_expansion=max(basis_values) - basis_values[0])
            rows.append(row)
    schema = {"decision_ts": pl.Int64, "horizon": pl.String, "entry_ts": pl.Int64,
              "label_end_ts": pl.Int64, "label_available_ts": pl.Int64,
              **{name: pl.Float64 for name in ("y_funding", "y_net", "fees_usdt",
                                             "execution_cost_usdt", "max_basis_expansion")},
              "y_flip": pl.Int64, "y_loss": pl.Int64, "reason": pl.String}
    return pl.DataFrame(rows, schema=schema)



# Same execution comparator, predefined25% rather than previous45%.
def benchmark(data,m,folds):
 start=folds[0]['test_start_signal_ns'];end=folds[-1]['test_end_signal_ns'];a=data['times'].index(start);b=data['times'].index(end);rows=data['rows'][a:b+1]
 l=Ledger(10000);q=math.floor(2500/float(rows[0]['close'])/data['meta']['spot_lot'])*data['meta']['spot_lot'];cash=10000;eq=[10000.];trades=[];bounds={};boundset={f['test_start_signal_ns'] for f in folds}|{end}
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
