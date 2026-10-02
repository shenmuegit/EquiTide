"""Independent source-position reconstruction, hybrid metrics and first shadow audit."""
import gzip,hashlib,importlib.util,json,math,statistics,sys
from decimal import Decimal as D
from pathlib import Path
import numpy as np
import polars as pl
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
s=importlib.util.spec_from_file_location('hybrid_independent_metrics',ROOT/'research/experiments/20261001T213902Z/audit.py');metrics=importlib.util.module_from_spec(s);s.loader.exec_module(metrics)
sha=metrics.sha;SPAN=1441;POINTS=259382
def main():
 r=json.loads((ROUND/'report.json').read_text());batch=json.loads((ROUND/'batch.json').read_text());raw=[json.loads(x) for x in (ROOT/'research/automation/registry.jsonl').read_text().splitlines()];ledger=registry.read_records(ROOT/'research/automation/registry.jsonl')
 for p,h in r['source_hashes'].items():assert sha(ROOT/p)==h,p
 prior=json.loads(gzip.decompress((ROUND/'prior_summary.json.gz').read_bytes()));assert prior['lines']==700 and prior['canonical']==338
 before={registry.fingerprint(v['spec']) for v in prior['records'].values()};assert not(before & {b['fingerprint'] for b in batch})
 for b in batch:
  reserves=[v for v in raw if v['fingerprint']==b['fingerprint'] and v['status']=='reserved'];assert len(reserves)==1 and reserves[0]['recorded_at_utc']<r['evaluation_started_utc']
  record=ledger[b['fingerprint']]
  if record['status']!='reserved':assert record['status']==r['configs'][b['name']]['status'] and record['report_sha256']==sha(ROUND/'report.json')
 frames={}
 for year,p in r['plan']['periods'].items():
  frames[year]={}
  for asset,d in p['normalized_data'].items():
   assert sha(ROOT/d['path'])==d['sha256'];f=pl.read_parquet(ROOT/d['path']);assert f.height==525600 and f['is_closed'].all() and (f['open_ts'].diff().drop_nulls()==60000000000).all();assert (f['available_ts']-f['open_ts']==60000000000).all();frames[year][asset]=f
  assert frames[year]['BTC']['open_ts'].equals(frames[year]['ETH']['open_ts'])
 vectors={};archives={};source_scenes=0
 for fp,ref in r['component_sources'].items():
  assert sha(ROOT/ref['archive'])==ref['archive_sha256'] and sha(ROOT/ref['report'])==ref['report_sha256'] and sha(ROOT/ref['spec'])==ref['spec_sha256'];a=json.loads(gzip.decompress((ROOT/ref['archive']).read_bytes()));assert registry.fingerprint(a['spec'])==fp;archives[fp]=a
  f=frames[ref['year']][ref['asset']];closes=np.asarray(f['close'].cast(pl.Float64))
  for k,s in a['scenes'].items():
   v=np.empty(POINTS);v[0]=ref['capital_usdt'];coverage=[]
   for st in s['position_segments']:
    cash=D(st['cash']);units=D(st['units']);assert cash>=0 and units>=0
    for d in range(st['day_offset'],st['end_day_exclusive']):
     coverage.append(d);i=183+d;v[d*SPAN+1]=float(cash+units*f['open'][i*1440+1]);v[d*SPAN+2:(d+1)*SPAN+1]=float(cash)+float(units)*closes[i*1440+1:(i+1)*1440+1]
   assert coverage==list(range(180));v[-1]=float(D(s['terminal_cash'])+D(s['terminal_units'])*f['open'][363*1440+1]);assert metrics.navhash(v)==s['summary']['NAV_sha256_f64le'];vectors[(fp,k)]=v;source_scenes+=1
 checked=0
 for b in batch:
  cfg=r['configs'][b['name']];assert sha(ROOT/cfg['archive'])==cfg['archive_sha256'];a=json.loads(gzip.decompress((ROOT/cfg['archive']).read_bytes()));sp=json.loads((ROOT/b['spec']).read_text());assert sp==a['spec'] and registry.fingerprint(sp)==b['fingerprint'];fps=[c['fingerprint'] for c in sp['components']]
  assert [c['weight'] for c in sp['components']]==[.75,.25] and [r['component_sources'][f]['capital_usdt'] for f in fps]==[1500,500]
  for k,scene in a['scenes'].items():
   v=vectors[(fps[0],k)]+vectors[(fps[1],k)];summ=scene['summary'];assert summ==cfg['scenes'][k] and metrics.navhash(v)==summ['NAV_sha256_f64le'];assert np.array_equal(v,np.load(ROOT/'data/runs'/ROUND.name/f'{b["name"]}_{k}.npy',allow_pickle=False));metrics.check_metrics(v,summ,180,True)
   for j,fold in enumerate(summ['folds']):metrics.check_metrics(v[j*30*SPAN:(j+1)*30*SPAN+1+(j==5)],fold,30,j==5)
   assert abs(math.prod(1+f['net_return_pct']/100 for f in summ['folds'])-v[-1]/v[0])<1e-12
   trades=[t for fp in fps for t in archives[fp]['scenes'][k]['trades']];assert trades==scene['trades'];cost=sum(float(sum(D(t['cost_parts'][p]) for t in trades if t['status']=='filled')) for p in ('fee','half_spread','slippage','impact','tick_rounding'));assert abs(cost-summ['cost_usdt'])<1e-10
   assert abs(sum(float(D(t['quantity'])*D(t['reference']))*(1 if t['side']!='buy' else -1) for t in trades if t['status']=='filled')-cost-(v[-1]-2000))<1e-8
   checked+=1
  ss=cfg['scenes'];ratio=ss['1']['gross_reference_PnL_to_execution_cost'];fraction=r['sensitivity'][f'{b["year"]}_{b["direction"]}']['metrics']['3']['positive_return_fraction']
  gate={'positive_all_costs':all(s['net_return_pct']>0 for s in ss.values()),'four_positive_1x_folds':sum(f['net_return_pct']>0 for f in ss['1']['folds'])>=4,'minute_DD3_lte25pct':ss['3']['max_drawdown_pct']<=25,'neighbourhood_positive3_gte60pct':fraction>=.6,'two_round_trips1':ss['1']['round_trips']>=2,'gross_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'no_balance_violations':all(s['cash_or_units_violations']==0 for s in ss.values()),'terminal_flat':all(D(s['terminal_units'])==0 for s in ss.values())};assert gate==cfg['criteria'] and (cfg['status']=='passed')==all(gate.values())
  assert cfg['both_periods_meet_full_gates']==(cfg['status']==r['configs'][cfg['other_period_config']]['status']=='passed')
 for group,sens in r['sensitivity'].items():
  cells=[c for c in r['configs'].values() if f'{c["year"]}_{c["direction"]}'==group];assert len(cells)==9 and len(sens['adjacent_edges'])==12
  for k in ('1','2','3'):assert sens['metrics'][k]['positive_return_fraction']==sum(c['scenes'][k]['net_return_pct']>0 for c in cells)/9
 for name,cmp in r['read_only_comparators'].items():assert json.loads((ROOT/cmp['source_report']).read_text())['configs'][name]['scenes']==cmp['scenes']
 fr=json.loads((ROUND/'forward_report.json').read_text());assert sha(ROUND/'forward_report.json')==r['forward_observation']['sha256'];assert sha(ROUND/'forward_inputs.json.gz')==fr['input_sha256'];fi=json.loads(gzip.decompress((ROUND/'forward_inputs.json.gz').read_bytes()));fb=json.loads((ROUND/'forward_batch.json').read_text())
 for b in fb:
  assert registry.fingerprint(json.loads((ROOT/b['spec']).read_text()))==b['fingerprint']
  reserve=[v for v in raw if v['fingerprint']==b['fingerprint'] and v['status']=='reserved'];assert len(reserve)==1 and reserve[0]['recorded_at_utc']<fr['observation_started_utc']
  rec=ledger[b['fingerprint']]
  if rec['status']!='reserved':assert rec['status']=='rejected' and rec['report_sha256']==sha(ROUND/'forward_report.json')
 for asset in ('BTC','ETH'):
  daily=fi[asset]['1d'];minute=fi[asset]['1m'];cfg=fr['configs']['forward_snapshot_'+asset];mean=sum(D(z[4]) for z in daily)/65;want=D(daily[-1][4])>mean*D('1.01');assert cfg['decision']['long']==want and D(cfg['decision']['sma'])==mean
  assert len(daily)==65 and len(minute)==100 and all(z[6]+1==z[0]+86400000 for z in daily) and all(z[6]+1==z[0]+60000 for z in minute)
  assert daily[-1][6]+1<minute[1][0]
  for k,s in cfg['scenes'].items():
   capital=cfg['capital_usdt'];assert len(s['equity_usdt'])==101 and s['elapsed_minutes']==99 and s['elapsed_complete_days']==0
   if want:
    t=s['trades'][0];ref=float(minute[1][1]);adv=statistics.mean(float(z[7]) for z in daily[-20:]);cl=[float(z[4]) for z in daily[-21:]];sigma=statistics.stdev(math.log(b/a) for a,b in zip(cl,cl[1:]));impact=.5*sigma*math.sqrt(capital/adv)*int(k);execution=ref*(1+.0003*int(k)+impact);quantity=capital/(execution*(1+.001*int(k)))
    assert abs(quantity-s['units'])<1e-10 and abs(capital-quantity*ref-s['cost_usdt'])<1e-7
   expected=[float(capital),s['cash_usdt']+s['units']*float(minute[1][1])]+[s['cash_usdt']+s['units']*float(z[4]) for z in minute[1:]];assert expected==s['equity_usdt'];assert abs(s['net_return_pct']-100*(expected[-1]/capital-1))<1e-12
 for k,s in fr['configs']['forward_snapshot_combo']['scenes'].items():assert s['equity_usdt']==[a+b for a,b in zip(fr['configs']['forward_snapshot_BTC']['scenes'][k]['equity_usdt'],fr['configs']['forward_snapshot_ETH']['scenes'][k]['equity_usdt'])]
 assert sha(ROOT/fr['frozen_plan_path'])==fr['frozen_plan_sha256']==r['plan']['forward_plan']['sha256'];assert source_scenes==72 and checked==108
 print(json.dumps({'passed':True,'source_component_scenes_rebuilt':72,'hybrid_cost_scenes_audited':108,'hybrid_NAV_points_audited':108*POINTS,'forward_snapshot_cost_scenes_audited':9,'forward_minutes':99,'report_sha256':sha(ROUND/'report.json'),'forward_report_sha256':sha(ROUND/'forward_report.json'),'frozen_forward_plan_unchanged':True}),flush=True)
if __name__=='__main__':main()
