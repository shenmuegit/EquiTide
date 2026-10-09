"""Actual new BTC-cap backtests via the existing guarded SMA/Decimal execution kernel."""
from pathlib import Path
from datetime import datetime,timezone
import gzip,importlib.util,json,math,sys
import numpy as np
import polars as pl
R=Path(__file__).resolve().parents[3];T=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'research/automation'));import registry
s=importlib.util.spec_from_file_location('new_guard_producer',R/'research/experiments/20261002T134733Z/evaluate.py');producer=importlib.util.module_from_spec(s);sys.modules[s.name]=producer;s.loader.exec_module(producer)
core=producer.core;sha=core.sha;CACHE=R/'data/runs'/T.name

def main():
 replay='--reproduce' in sys.argv;plan=json.loads((T/'spec.json').read_text());batch=json.loads((T/'component_batch.json').read_text());ledger=registry.read_records(R/'research/automation/registry.jsonl')
 for b in batch:assert ledger[b['fingerprint']]['status'] in (('passed','rejected') if replay else ('reserved',)) and registry.fingerprint(json.loads((R/b['spec']).read_text()))==b['fingerprint']
 started=datetime.now(timezone.utc).isoformat();data={};prices={};dailyrefs={};folds=None
 for year,p in plan['periods'].items():
  assert sha(R/p['report'])==p['sha256'];old=json.loads((R/p['report']).read_text())
  if folds is None:folds=old['folds']
  else:assert folds==old['folds']
  file=R/'research/experiments'/p['source_round']/'daily_inputs.json.gz';data[year]=json.loads(gzip.decompress(file.read_bytes()));dailyrefs[year]={'path':str(file.relative_to(R)),'sha256':sha(file)}
  for asset,md in p['normalized_data'].items():
   assert sha(R/md['path'])==md['sha256'];frame=pl.read_parquet(R/md['path']);assert frame.height==525600 and frame['is_closed'].all() and (frame['open_ts'].diff().drop_nulls()==60000000000).all() and (frame['available_ts']-frame['open_ts']==60000000000).all()
   if asset=='BTC':
    prices[year]=np.asarray(frame['close'].cast(pl.Float64))
    for i,row in enumerate(data[year][asset]):assert row['trade_ts']==frame['open_ts'][i*1440+1] and producer.D(str(row['trade_open']))==frame['open'][i*1440+1]
 CACHE.mkdir(parents=True,exist_ok=True)
 report={'evaluation_started_utc':started,'plan':plan,'daily_inputs':dailyrefs,'folds':folds,'curve_formula':old['curve_formula'],'configs':{},'sensitivity':{},'source_hashes':{},'summary':{}}
 for b in batch:
  sp=json.loads((R/b['spec']).read_text());arc={'spec':sp,'fingerprint':b['fingerprint'],'scenes':{}};scenes={}
  for k in ('1','2','3'):
   v,part=producer.component(sp,data[b['year']]['BTC'],prices[b['year']],int(k),folds);z=part['summary'];z['first_five_fold_return_pct']=100*(math.prod(1+q['net_return_pct']/100 for q in z['folds'][:5])-1);z['last_fold_return_pct']=z['folds'][-1]['net_return_pct'];arc['scenes'][k]=part;scenes[k]=z;npfile=CACHE/f'{b["name"]}_{k}.npy'
   if replay:assert core.navhash(np.load(npfile,allow_pickle=False))==core.navhash(v)
   else:np.save(npfile,v,allow_pickle=False)
  file=T/'results'/f'{b["name"]}.json.gz'
  if replay:assert json.loads(gzip.decompress(file.read_bytes()))==core.canonical(arc)
  else:core.gzwrite(file,arc)
  report['configs'][b['name']]={**b,'archive':str(file.relative_to(R)),'archive_sha256':sha(file),'scenes':scenes,'positive_folds_1x':sum(q['net_return_pct']>0 for q in scenes['1']['folds'])}
  print(json.dumps({'new_component':b['name'],'return1_pct':scenes['1']['net_return_pct'],'return3_pct':scenes['3']['net_return_pct'],'DD3_pct':scenes['3']['max_drawdown_pct']}),flush=True)
 for ref in plan['read_only_component_refs']:
  assert sha(R/ref['report'])==ref['report_sha256'] and sha(R/ref['archive'])==ref['archive_sha256'];oldrow=json.loads((R/ref['report']).read_text())['configs'][ref['name']]
  report['configs'][ref['name']]={**oldrow,'year':ref['year'],'asset':'BTC','role':'component','capital_usdt':1500,'lookback_days':65,'entry_band':.0125,'volatility_ceiling':.6,'is_new':False,'source_ref':ref,'source_record_status':oldrow['status'],'source_record_criteria':oldrow['criteria']}
 for year in ('2025','2026'):
  rows={c['volatility_ceiling']:c for c in report['configs'].values() if c['year']==year};assert set(rows)=={.4,.5,.6}
  stats={k:{'positive_return_fraction':sum(c['scenes'][k]['net_return_pct']>0 for c in rows.values())/3,'positive_sharpe_fraction':sum((c['scenes'][k]['sharpe_365'] or 0)>0 for c in rows.values())/3} for k in ('1','2','3')};edges=[{'a':rows[a]['name'],'b':rows[b]['name'],'return_difference_3x_pct':abs(rows[a]['scenes']['3']['net_return_pct']-rows[b]['scenes']['3']['net_return_pct'])} for a,b in [(.4,.5),(.5,.6)]]
  report['sensitivity'][year+'_BTC']={'axes':['annual_volatility_ceiling'],'cells':3,'metrics':stats,'adjacent_edges':edges,'scope':'Prerequisite component40/50/60cap neighbourhood;full study additionally varies ETHentry in portfolio3x3. Old60cap status retained.'}
 for c in report['configs'].values():
  if c['is_new']:
   c['criteria']=producer.rules.gates(c['scenes'],report['sensitivity'][c['year']+'_BTC']['metrics']['3']['positive_return_fraction']);c['status']='passed' if all(c['criteria'].values()) else 'rejected';c['failed_criteria']=[k for k,v in c['criteria'].items() if not v]
  other=next(o for o in report['configs'].values() if o['year']!=c['year'] and o['volatility_ceiling']==c['volatility_ceiling']);c['other_period_config']=other['name']
 for c in report['configs'].values():c['both_periods_meet_full_gates']=c['status']==report['configs'][c['other_period_config']]['status']=='passed'
 fresh=[c for c in report['configs'].values() if c['is_new']]
 report['summary']={'new_component_configs':4,'new_component_cost_scenes':12,'old_component_configs_read_only':2,'passed':[c['name'] for c in fresh if c['status']=='passed'],'rejected':[c['name'] for c in fresh if c['status']=='rejected'],'positive_1x':sum(c['scenes']['1']['net_return_pct']>0 for c in fresh),'positive_3x':sum(c['scenes']['3']['net_return_pct']>0 for c in fresh),'actual_component_fills':sum(c['scenes'][k]['executions'] for c in fresh for k in ('1','2','3')),'real_orders':0}
 report['source_hashes']={str(q.relative_to(R)):sha(q) for q in [T/'spec.json',T/'component_batch.json',T/'prepare.py',T/'evaluate_components.py',T/'audit_components.py',R/'research/experiments/20261002T134733Z/evaluate.py',R/'research/experiments/20261002T134733Z/signals.py',R/'research/experiments/20261001T133655Z/evaluate.py',R/'research/experiments/20261001T133655Z/kernel.py',R/'research/automation/registry.py']}
 if replay:
  expected=json.loads((T/'components_report.json').read_text());report['evaluation_started_utc']=expected['evaluation_started_utc'];assert core.canonical(report)==expected;print('PASS:all12 NEW BTC component cost scenes and full component report reproduced;noHTTP/ledger write');return
 (T/'components_report.json').write_text(json.dumps(core.canonical(report),ensure_ascii=False,separators=(',',':'))+'\n');print(json.dumps(report['summary']),flush=True)
if __name__=='__main__':main()
