"""Independent joint signal/EMA, Decimal order costs and complete minute-price audit."""
import gzip,hashlib,importlib.util,json,math,statistics,sys
from datetime import datetime,timezone
from decimal import Decimal as D,ROUND_CEILING,ROUND_FLOOR
from pathlib import Path
import numpy as np
import pandas as pd
import polars as pl
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
s=importlib.util.spec_from_file_location('independent_metrics',ROOT/'research/experiments/20261001T213902Z/audit.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
sha=m.sha;navhash=m.navhash;SPAN=1441;POINTS=259382

def main():
 r=json.loads((ROUND/'report.json').read_text());plan=r['plan'];batch=json.loads((ROUND/'grid_batch.json').read_text());ledgerfile=ROOT/'research/automation/registry.jsonl';raw=[json.loads(x) for x in ledgerfile.read_text().splitlines()];ledger=registry.read_records(ledgerfile)
 for p,h in r['source_hashes'].items():assert sha(ROOT/p)==h,p
 assert sha(ROOT/plan['execution']['metadata_path'])==plan['execution']['metadata_sha256']
 prior=json.loads(gzip.decompress((ROUND/'prior_summary.json.gz').read_bytes()));assert prior['lines']==3397 and prior['canonical']==1649
 before={registry.fingerprint(x['spec']) for x in prior['records'].values()};assert not(before & {b['fingerprint'] for b in batch if b['is_new']})
 for b in batch:
  assert registry.fingerprint(json.loads((ROOT/b['spec']).read_text()))==b['fingerprint'];rec=ledger[b['fingerprint']]
  if b['is_new']:
   reserves=[x for x in raw if x['fingerprint']==b['fingerprint'] and x['status']=='reserved'];assert len(reserves)==1 and reserves[0]['recorded_at_utc']<r['evaluation_started_utc']
   if rec['status']!='reserved':assert rec['report_sha256']==sha(ROUND/'report.json') and rec['status']==r['configs'][b['name']]['status']
  else:
   ref=b['source_ref'];assert sha(ROOT/ref['report'])==ref['report_sha256'] and sha(ROOT/ref['archive'])==ref['archive_sha256'] and sha(ROOT/b['spec'])==ref['spec_sha256']
   old=json.loads((ROOT/ref['report']).read_text())['configs'][b['name']];c=r['configs'][b['name']]
   assert c['scenes']==old['scenes'] and c['source_record_status']==old['status'] and c['source_record_criteria']==old['criteria']
   assert rec['report']==ref['report'] and rec['report_sha256']==ref['report_sha256'] and rec['status']==old['status']
 frames={};daily={}
 for y,p in plan['periods'].items():
  assert sha(ROOT/p['report'])==p['sha256'];assert sha(ROOT/r['daily_inputs'][y]['path'])==r['daily_inputs'][y]['sha256']
  daily[y]=json.loads(gzip.decompress((ROOT/r['daily_inputs'][y]['path']).read_bytes()));frames[y]={}
  for asset,md in p['normalized_data'].items():
   assert sha(ROOT/md['path'])==md['sha256'];f=pl.read_parquet(ROOT/md['path']);assert f.height==525600 and f['is_closed'].all()
   assert f['open_ts'].is_sorted() and (f['open_ts'].diff().drop_nulls()==60000000000).all() and (f['available_ts']-f['open_ts']==60000000000).all()
   assert f['open_ts'][0]==md['first_open_ns'] and f['available_ts'][-1]==md['last_available_ns'];frames[y][asset]=f
   for i,row in enumerate(daily[y][asset]):
    assert D(row['close'])==f['close'][(i+1)*1440-1];assert row['close_available_ts']==f['available_ts'][(i+1)*1440-1]
    assert row['trade_ts']==f['open_ts'][i*1440+1] and D(row['trade_open'])==f['open'][i*1440+1]
   assert datetime.fromtimestamp(daily[y][asset][183]['trade_ts']/1e9,timezone.utc).isoformat().replace('+00:00','Z')==p['oos_start_utc']
   assert datetime.fromtimestamp(daily[y][asset][363]['trade_ts']/1e9,timezone.utc).isoformat().replace('+00:00','Z')==p['terminal_exit_utc']
  assert frames[y]['BTC']['open_ts'].equals(frames[y]['ETH']['open_ts'])
 vectors={};archives={};decisions=0;fills=0;scenes=0;causal_probes=0
 module_spec=importlib.util.spec_from_file_location('production_confirmation_probe',ROUND/'signals.py');prod=importlib.util.module_from_spec(module_spec);module_spec.loader.exec_module(prod)
 for b in batch:
  cfg=r['configs'][b['name']];assert sha(ROOT/cfg['archive'])==cfg['archive_sha256'];a=json.loads(gzip.decompress((ROOT/cfg['archive']).read_bytes()));archives[b['fingerprint']]=a
  sp=json.loads((ROOT/b['spec']).read_text());assert a['spec']==sp and a['fingerprint']==b['fingerprint']
  for k,scene in a['scenes'].items():
   if b['role']=='component':
    y=b['year'];asset=b['asset'];p=sp['parameters'];rows=daily[y][asset];f=frames[y][asset];closes=np.array([float(x['close']) for x in rows])
    exact=[D(x['close']) for x in rows];upper={j:sorted(exact[j-b['entry_days']-1:j-1])[-1] for j in range(183,363)};lower={j:sorted(exact[j-b['exit_days']-1:j-1])[0] for j in range(183,363)}
    assert p['EMA_span_days']==b['span_days'];assert p['EMA_symmetric_band']==b['EMA_band'] and p['exit_lookback_days']==b['exit_days']==30
    ema=pd.Series(closes).ewm(span=b['span_days'],adjust=False).mean().to_numpy();band=p['EMA_symmetric_band']
    if k=='1' and b['is_new']:
     actual=prod.filtered_channel([x['close'] for x in rows],b['entry_days'],b['exit_days'],b['span_days'],band)
     for cutoff in (183,222,362):
      changed=[x['close'] if j<cutoff else str(D(x['close'])*D('1.75')) for j,x in enumerate(rows)]
      assert prod.filtered_channel(changed,b['entry_days'],b['exit_days'],b['span_days'],band,end=cutoff+1)==actual[:cutoff-183+1];causal_probes+=1
    want=False;cash=D(p['initial_capital_usdt']);units=D(0);v=np.empty(POINTS);v[0]=float(cash);marks=np.asarray(f['close'].cast(pl.Float64));states={d:st for st in scene['position_segments'] for d in range(st['day_offset'],st['end_day_exclusive'])};assert sorted(states)==list(range(180))
    attempts={(t['day_offset'],t['terminal']):t for t in scene['trades']};assert len(attempts)==len(scene['trades'])
    def audit_order(i,buy,terminal):
     nonlocal cash,units,fills
     t=attempts[(i-183,terminal)];ref=D(rows[i]['trade_open']);assert t['trade_ts_ns']==rows[i]['trade_ts'] and D(t['reference'])==ref
     assert t['side']==('buy' if buy else 'sell') and t['cost_multiplier']==int(k)
     adv=statistics.mean(float(x['quote_volume']) for x in rows[i-20:i]);xx=[float(x['close']) for x in rows[i-21:i]];sigma=statistics.stdev([math.log(bb/aa) for aa,bb in zip(xx,xx[1:])])
     assert D(t['lagged_ADV'])==D(str(adv)) and D(t['lagged_sigma'])==D(str(sigma))
     vw=f.slice(i*1440-4,5);assert vw['available_ts'].max()<=rows[i]['trade_ts'];assert D(t['proxy_VWAP5'])==vw['quote_volume'].sum()/vw['base_volume'].sum()
     budget=cash if buy else units*ref;participation=budget/D(str(adv));assert D(t['budget'])==budget and D(t['participation'])==participation
     if t['status']=='rejected':assert D(t['cash_after'])==cash and D(t['units_after'])==units;return
     assert participation<=D('.001');fees=D('.001')*int(k);spread=D('.0001')*int(k);slip=D('.0002')*int(k);impact=D('.5')*D(str(sigma))*participation.sqrt()*int(k)
     theoretical=ref*(1+(spread+slip+impact)*(1 if buy else -1));filters=p['execution']['filters'][asset+'USDT'];tick=D(filters['PRICE_FILTER']['tickSize']);step=D(filters['LOT_SIZE']['stepSize'])
     price=(theoretical/tick).to_integral_value(rounding=ROUND_CEILING if buy else ROUND_FLOOR)*tick
     qty=((cash/(price*(1+fees)) if buy else units)/step).to_integral_value(rounding=ROUND_FLOOR)*step
     assert D(t['execution'])==price and D(t['quantity'])==qty and D(t['theoretical_execution'])==theoretical
     parts={'fee':qty*price*fees,'half_spread':qty*ref*spread,'slippage':qty*ref*slip,'impact':qty*ref*impact,'tick_rounding':qty*abs(price-theoretical)}
     assert all(D(t['cost_parts'][name])==value for name,value in parts.items());assert D(t['cost_usdt'])==sum(parts.values())
     cash=cash-qty*price-parts['fee'] if buy else cash+qty*price-parts['fee'];units=units+qty if buy else units-qty
     assert cash==D(t['cash_after']) and units==D(t['units_after']) and cash>=0 and units>=0;fills+=1
    for d,i in enumerate(range(183,363)):
     decision=scene['decisions'][d];assert decision['decision_index']==i and rows[i-1]['close_available_ts']<rows[i]['trade_ts']
     last=exact[i-1];assert D(decision['entry_channel_prior'])==upper[i] and D(decision['exit_channel_prior'])==lower[i] and D(decision['prior_close'])==last
     assert rows[i-2]['close_available_ts']<rows[i-1]['close_available_ts']<rows[i]['trade_ts']
     assert abs(decision['EMA_prior']-ema[i-1])<1e-7
     assert decision['channel_entry']==(last>upper[i]) and decision['channel_exit']==(last<lower[i])
     assert decision['EMA_entry']==(float(last)>ema[i-1]*(1+band)) and decision['EMA_exit']==(float(last)<ema[i-1]*(1-band))
     # Independent pandas EMA and last forcing event over every prefix; range ends at i-2.
     crossings=[]
     for j in range(183,i+1):
      if exact[j-1]<lower[j] or float(exact[j-1])<ema[j-1]*(1-band):crossings.append(False)
      elif exact[j-1]>upper[j] and float(exact[j-1])>ema[j-1]*(1+band):crossings.append(True)
     want=crossings[-1] if crossings else False
     assert decision['long']==want;decisions+=1
     need=(want and not units) or (not want and units>0);assert bool(need)==((d,False) in attempts)
     if need:audit_order(i,want,False)
     assert cash==D(states[d]['cash']) and units==D(states[d]['units'])
     v[d*SPAN+1]=float(cash+units*f['open'][i*1440+1]);v[d*SPAN+2:(d+1)*SPAN+1]=float(cash)+float(units)*marks[i*1440+1:(i+1)*1440+1]
    assert bool(units)==((180,True) in attempts)
    if units:audit_order(363,False,True)
    assert cash==D(scene['terminal_cash']) and units==D(scene['terminal_units']);v[-1]=float(cash+units*f['open'][363*1440+1])
   else:
    comps=sp['components'];assert all(archives[c['fingerprint']]['spec']['parameters']['EMA_span_days']==b['span_days'] for c in comps);assert all(archives[c['fingerprint']]['spec']['parameters']['EMA_symmetric_band']==b['EMA_band'] for c in comps);assert [c['weight'] for c in comps]==b['raw_weights'] and D(str(comps[0]['weight']))+D(str(comps[1]['weight']))==D(1)
    assert [archives[c['fingerprint']]['spec']['parameters']['initial_capital_usdt'] for c in comps]==[int(D(2000)*D(str(c['weight']))) for c in comps]
    v=vectors[(comps[0]['fingerprint'],k)]+vectors[(comps[1]['fingerprint'],k)]
    assert scene['trades']==[t for c in comps for t in archives[c['fingerprint']]['scenes'][k]['trades']]
   summ=scene['summary'];assert summ==cfg['scenes'][k] and navhash(v)==summ['NAV_sha256_f64le']
   assert np.array_equal(v,np.load(ROOT/'data/runs'/(ROUND.name if b['is_new'] else b['source_ref']['source_round'])/f'{b["name"]}_{k}.npy',allow_pickle=False));m.check_metrics(v,summ,180,True)
   for j,ff in enumerate(summ['folds']):m.check_metrics(v[j*30*SPAN:(j+1)*30*SPAN+1+(j==5)],ff,30,j==5)
   assert abs(math.prod(1+ff['net_return_pct']/100 for ff in summ['folds'])-v[-1]/v[0])<1e-12
   assert abs(100*(math.prod(1+ff['net_return_pct']/100 for ff in summ['folds'][:5])-1)-summ['first_five_fold_return_pct'])<1e-10
   parts=sum(float(sum(D(t['cost_parts'][key]) for t in scene['trades'] if t['status']=='filled')) for key in ('fee','half_spread','slippage','impact','tick_rounding'));assert abs(parts-summ['cost_usdt'])<1e-10
   vectors[(b['fingerprint'],k)]=v;scenes+=1
  ss=cfg['scenes'];ratio=ss['1']['gross_reference_PnL_to_execution_cost'];group=cfg.get('asset','combination');neighbour=r['sensitivity'][f'{cfg["year"]}_{group}']['metrics']['3']['positive_return_fraction']
  gates={'positive_all_costs':all(s['net_return_pct']>0 for s in ss.values()),'four_positive_1x_folds':sum(f['net_return_pct']>0 for f in ss['1']['folds'])>=4,'minute_DD3_lte25pct':ss['3']['max_drawdown_pct']<=25,'neighbourhood_positive3_gte60pct':neighbour>=.6,'two_round_trips1':ss['1']['round_trips']>=2,'gross_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'no_balance_violations':all(s['cash_or_units_violations']==0 for s in ss.values()),'terminal_flat':all(D(s['terminal_units'])==0 for s in ss.values())}
  assert cfg['criteria']==gates and (cfg['status']=='passed')==all(gates.values())
  assert cfg['both_periods_meet_full_gates']==(cfg['status']==r['configs'][cfg['other_period_config']]['status']=='passed')
 for group,sens in r['sensitivity'].items():
  y,asset=group.split('_');rows=[x for x in r['configs'].values() if x['year']==y and x.get('asset','combination')==asset];assert len(rows)==9 and len(sens['adjacent_edges'])==12
  for k in ('1','2','3'):
   assert sens['metrics'][k]['positive_return_fraction']==sum(x['scenes'][k]['net_return_pct']>0 for x in rows)/9
   assert sens['metrics'][k]['positive_sharpe_fraction']==sum((x['scenes'][k]['sharpe_365'] or 0)>0 for x in rows)/9
 for n,c in r['read_only_comparators'].items():assert json.loads((ROOT/c['source_report']).read_text())['configs'][n]['scenes']==c['scenes']
 assert scenes==162 and decisions==19440 and causal_probes==72 and fills==r['summary']['audited_component_fills']
 assert sha(ROOT/plan['forward_plan']['path'])==plan['forward_plan']['sha256']
 print(json.dumps({'passed':True,'all_scenes_audited':scenes,'new_scenes':108,'existing_scenes_read_only_audited':54,'current_or_future_close_perturbations':72,'NAV_points_audited':scenes*POINTS,'joint_channel_pandasEMA_causal_decisions':decisions,'Decimal_fills_independently_checked':fills,'new_actual_fills':r['summary']['actual_component_fills'],'real_minute_data_hashes':4,'report_sha256':sha(ROUND/'report.json'),'forward_plan_unchanged':True,'pandas_version':pd.__version__}),flush=True)

if __name__=='__main__':main()
