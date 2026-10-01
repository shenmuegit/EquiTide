"""Independent cash/units, timing, full-vector and portfolio metric audit."""
import gzip
import hashlib
import importlib.util
import json
import math
import statistics
import sys
from datetime import datetime,timezone
from decimal import Decimal as D
from pathlib import Path
import numpy as np
import polars as pl

ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
SPAN=1441;POINTS=259382
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
navhash=lambda v:hashlib.sha256(v.astype('<f8',copy=False).tobytes()).hexdigest()

def check_metrics(v,s,days,terminal):
 ret=100*(v[-1]/v[0]-1);draw=100*float(np.max(1-v/np.maximum.accumulate(v)))
 assert abs(ret-s['net_return_pct'])<1e-10 and abs(draw-s['max_drawdown_pct'])<1e-10
 daily=[float(v[d*SPAN]) for d in range(days+1)]
 if terminal:daily.append(float(v[-1]))
 stat=daily[:-2]+[daily[-1]] if terminal else daily
 rr=[b/a-1 for a,b in zip(stat,stat[1:])];sd=statistics.stdev(rr)
 sharpe=statistics.mean(rr)/sd*math.sqrt(365) if sd else None
 assert sharpe==s['sharpe_365'] or (sharpe is not None and abs(sharpe-s['sharpe_365'])<1e-10)
 assert abs(s['cagr_pct']-100*((v[-1]/v[0])**(365/days)-1))<1e-10
 assert abs(s['daily_mark_drawdown_pct']-100*float(np.max(1-np.array(daily)/np.maximum.accumulate(daily))))<1e-10
 assert s['calmar'] is None if not draw else abs(s['calmar']-s['cagr_pct']/draw)<1e-10
 if 'daily_equity_usdt' in s:assert daily==s['daily_equity_usdt']

def main():
 report=json.loads((ROUND/'report.json').read_text());plan=report['plan'];batch=json.loads((ROUND/'batch.json').read_text())
 ledger=registry.read_records(ROOT/'research/automation/registry.jsonl');raw=[json.loads(x) for x in (ROOT/'research/automation/registry.jsonl').read_text().splitlines()]
 for p,h in report['source_hashes'].items():assert sha(ROOT/p)==h,p
 snapshot=json.loads(gzip.decompress((ROUND/'prior_summary.json.gz').read_bytes()))
 assert snapshot['lines']==520 and snapshot['canonical']==248
 before={registry.fingerprint(v['spec']) for v in snapshot['records'].values()}
 assert len(batch)==36 and not (before & {b['fingerprint'] for b in batch})
 for b in batch:
  reserve=[r for r in raw if r['fingerprint']==b['fingerprint'] and r['status']=='reserved'];assert len(reserve)==1
  assert reserve[0]['recorded_at_utc']<report['evaluation_started_utc']
  assert registry.fingerprint(json.loads((ROOT/b['spec']).read_text()))==b['fingerprint']
  lr=ledger[b['fingerprint']]
  if lr['status']!='reserved':assert lr['report_sha256']==sha(ROUND/'report.json') and lr['status']==report['configs'][b['name']]['status']
 vectors={};arcs={};source_scenes=0;signals_checked=0
 for y,p in plan['periods'].items():
  assert sha(ROOT/p['report'])==p['sha256'];old=json.loads((ROOT/p['report']).read_text());frames={}
  daily=json.loads(gzip.decompress((ROOT/'research/experiments'/p['source_round']/'daily_inputs.json.gz').read_bytes()))
  for asset,d in p['normalized_data'].items():
   path=ROOT/d['path'];assert sha(path)==d['sha256']
   frame=pl.read_parquet(path);assert frame.height==525600
   assert frame['is_closed'].all() and frame['open_ts'].is_sorted()
   assert (frame['open_ts'].diff().drop_nulls()==60000000000).all() and (frame['available_ts']-frame['open_ts']==60000000000).all()
   assert frame['open_ts'][0]==d['first_open_ns'] and frame['available_ts'][-1]==d['last_available_ns']
   frames[asset]=frame
  assert frames['BTC']['open_ts'].equals(frames['ETH']['open_ts'])
  assert datetime.fromtimestamp(daily['BTC'][183]['trade_ts']/1e9,timezone.utc).isoformat().replace('+00:00','Z')==p['oos_start_utc']
  assert datetime.fromtimestamp(daily['BTC'][363]['trade_ts']/1e9,timezone.utc).isoformat().replace('+00:00','Z')==p['terminal_exit_utc']
  for key,ref in report['component_sources'].items():
   if not key.startswith(y+'/'):continue
   name=key.split('/',1)[1];assert sha(ROOT/ref['archive'])==ref['archive_sha256'];a=json.loads(gzip.decompress((ROOT/ref['archive']).read_bytes()));arcs[(y,name)]=a
   assert a['fingerprint']==ref['fingerprint']==registry.fingerprint(a['spec'])
   frame=frames[ref['asset']];closes=np.asarray(frame['close'].cast(pl.Float64));capital=ref['capital_usdt'];lookback=a['spec']['parameters']['lookback_days'];rows=daily[ref['asset']]
   for k,s in a['scenes'].items():
    v=np.empty(POINTS);v[0]=capital;coverage=[];want=False
    for i,decision in zip(range(183,363),s['decisions']):
     available=rows[i-1]['close_available_ts'];assert available<rows[i]['trade_ts']
     avg=sum(float(rows[j]['close']) for j in range(i-lookback,i))/lookback;last=float(rows[i-1]['close'])
     if last>avg*1.01:want=True
     elif last<avg*.99:want=False
     assert decision['decision_index']==i and decision['long']==want
     assert rows[i]['trade_ts']==frame['open_ts'][i*1440+1];signals_checked+=1
    for state in s['position_segments']:
     c=D(state['cash']);u=D(state['units']);assert c>=0 and u>=0
     for d in range(state['day_offset'],state['end_day_exclusive']):
      coverage.append(d);i=183+d;assert frame['available_ts'][i*1440-1]<rows[i]['trade_ts']
      v[d*SPAN+1]=float(c+u*frame['open'][i*1440+1])
      v[d*SPAN+2:(d+1)*SPAN+1]=float(c)+float(u)*closes[i*1440+1:(i+1)*1440+1]
    assert coverage==list(range(180));v[-1]=float(D(s['terminal_cash'])+D(s['terminal_units'])*frame['open'][363*1440+1])
    assert navhash(v)==ref['NAV_sha256_by_cost'][k]==s['summary']['NAV_sha256_f64le']
    assert np.array_equal(v,np.load(ROOT/'data/runs'/p['source_round']/f'{name}_{k}.npy',allow_pickle=False))
    for t in s['trades']:
     idx=t['decision_index'];assert t['trade_ts_ns']==rows[idx]['trade_ts']
     assert D(t['reference'])==D(str(rows[idx]['trade_open'])) and t['cash_after'] is not None
     assert D(t['cash_after'])>=0 and D(t['units_after'])>=0
    vectors[(y,name,k)]=v;source_scenes+=1
 audited=0
 for b in batch:
  r=report['configs'][b['name']];assert sha(ROOT/r['archive'])==r['archive_sha256'];a=json.loads(gzip.decompress((ROOT/r['archive']).read_bytes()))
  assert a['fingerprint']==b['fingerprint'] and a['spec']==json.loads((ROOT/b['spec']).read_text())
  names=b['component_names'];y=b['year']
  assert [arcs[(y,n)]['spec']['parameters']['initial_capital_usdt'] for n in names]==[round(w*2000) for w in b['raw_weights']]
  for k,s in a['scenes'].items():
   v=vectors[(y,names[0],k)]+vectors[(y,names[1],k)]
   assert np.array_equal(v,np.load(ROOT/'data/runs'/ROUND.name/f'{b["name"]}_{k}.npy',allow_pickle=False))
   assert v[0]==2000 and navhash(v)==s['summary']['NAV_sha256_f64le'];assert s['summary']==r['scenes'][k]
   check_metrics(v,s['summary'],180,True)
   for j,f in enumerate(s['summary']['folds']):check_metrics(v[j*30*SPAN:(j+1)*30*SPAN+1+(j==5)],f,30,j==5)
   assert abs(math.prod(1+f['net_return_pct']/100 for f in s['summary']['folds'])-v[-1]/2000)<1e-12
   trades=[t for n in names for t in arcs[(y,n)]['scenes'][k]['trades']];assert trades==s['trades']
   cost=sum(float(sum(D(t['cost_parts'][part]) for t in trades if t['status']=='filled')) for part in ('fee','half_spread','slippage','impact','tick_rounding'))
   assert abs(cost-s['summary']['cost_usdt'])<1e-10
   assert all(D(arcs[(y,n)]['scenes'][k]['terminal_units'])==0 for n in names)
   assert abs(sum(float(D(t['quantity'])*D(t['reference']))*(1 if t['side']!='buy' else -1) for t in trades if t['status']=='filled')-cost-(v[-1]-2000))<1e-8
   audited+=1
  s=r['scenes'];ratio=s['1']['gross_reference_PnL_to_execution_cost']
  expected={'positive_all_costs':all(x['net_return_pct']>0 for x in s.values()),'four_positive_1x_folds':sum(f['net_return_pct']>0 for f in s['1']['folds'])>=4,'minute_DD3_lte25pct':s['3']['max_drawdown_pct']<=25,'neighbourhood_positive3_gte60pct':report['sensitivity'][f'{y}_w{b["raw_weights"][0]}']['metrics']['3']['positive_return_fraction']>=.6,'two_round_trips1':s['1']['round_trips']>=2,'gross_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'no_balance_violations':all(x['cash_or_units_violations']==0 for x in s.values()),'terminal_flat':all(D(x['terminal_units'])==0 for x in s.values())}
  assert r['criteria']==expected and (r['status']=='passed')==all(expected.values())
  assert r['both_periods_meet_full_gates']==(r['status']==report['configs'][r['other_period_config']]['status']=='passed')
 assert source_scenes==108 and audited==108
 for group,g in report['sensitivity'].items():
  y,weight=group.split('_w');rows=[r for r in {**report['configs'],**report['read_only_diagonals']}.values() if r['year']==y and r['raw_weights'][0]==float(weight)]
  assert len(rows)==9 and len(g['adjacent_edges'])==12
  for k in ('1','2','3'):assert g['metrics'][k]['positive_return_fraction']==sum(r['scenes'][k]['net_return_pct']>0 for r in rows)/9
 for n,r in report['read_only_diagonals'].items():
  old=json.loads((ROOT/r['source_report']).read_text())['configs'][n];assert old['scenes']==r['scenes'] and old['status']==r['status']
  assert len([x for x in raw if x['fingerprint']==r['fingerprint'] and x['status']=='reserved'])==1
 out={'passed':True,'source_component_scenes_rebuilt':source_scenes,'new_combination_scenes_audited':audited,'new_NAV_points_audited':audited*POINTS,'causal_component_decisions_checked':signals_checked,'read_only_diagonal_configs':18,'minute_data_hashes_verified':4,'report_sha256':sha(ROUND/'report.json'),'forward_plan_unchanged':sha(ROOT/plan['forward_plan']['path'])==plan['forward_plan']['sha256']}
 assert out['forward_plan_unchanged']
 print(json.dumps(out),flush=True)

if __name__=='__main__':main()
