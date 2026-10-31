"""One actual evaluation per newly reserved native or passive-parent configuration."""
import argparse,copy,gzip,json,math
import numpy as np
import engine
from common import *
parent=module(ROOT/'research/experiments/20261025T145537Z/run.py','passive_parent_metrics')
oldrun=module(ROOT/'research/experiments/20261026T070542Z/run.py','original_recent_metrics')

def load(plan):
 ms={a:engine.load_market(a,fs) for a,fs in plan['data']['assets'].items()}
 warm=plan['warmup'];assert sha(ROOT/warm['raw'])==warm['sha256']
 for a,m in ms.items():
  m['signal_closes']={j:v for j,v in enumerate(m['closes'])}
  if a=='ETH':m['signal_closes'].update({int(j):engine.D(v) for j,v in warm['explicit_context_day_index_to_close'].items()})
  m.update(first_ns=int(m['frame']['open_ts'][0]),fund_lookup={x['settlement_ts']:x for x in m['funds']},terminal_reference_decimal=m['frame']['open'][403*1440+1])
 common=parent.align(ms)
 return ms,common

def recover(plan,ms,common):
 vectors={};scenes={};cfgs={}
 for fp,ref in plan['read_only_references'].items():
  assert sha(ROOT/ref['archive'])==ref['archive_sha256'] and sha(ROOT/ref['report'])==ref['report_sha256']
  report=json.loads((ROOT/ref['report']).read_text());c=copy.deepcopy(next(x for x in report['configs'].values() if x['fingerprint']==fp));cfgs[fp]=c
  arc=json.loads(gzip.decompress((ROOT/ref['archive']).read_bytes()))
  if ref['scope']=='native':
   m=ms[ref['asset']]
   for k,z in arc['scenes'].items():
    v=np.empty(len(m['ts']));last=0
    for s in z['state_segments']:
     a,b=s['axis_start'],s['axis_end_exclusive'];assert a==last and a<b;v[a:b]=float(s['cash'])+float(s['signed_units'])*(m['axis_prices'][a:b]-float(s['entry_price']));last=b
    assert last==len(v) and engine.navhash(v)==z['summary']['NAV_sha256_f64le'] and z['summary']['daily_equity_usdt']==v[m['daily_indices']].tolist()
    vectors[fp,k]=v[common['projections'][ref['asset']]];scenes[fp,k]=z['summary']
 for fp,ref in plan['read_only_references'].items():
  if ref['scope']!='parent':continue
  arc=json.loads(gzip.decompress((ROOT/ref['archive']).read_bytes()))
  for k,z in arc['scenes'].items():
   fps=z['source_fingerprints'];v=vectors[fps[0],k]+vectors[fps[1],k];assert engine.navhash(v)==z['summary']['NAV_sha256_f64le'];vectors[fp,k]=v;scenes[fp,k]=z['summary']
 return vectors,scenes,cfgs

def grid_axes(c):return (c.get('trend_lookback_days',c.get('trend_filter_lookback_days')),c.get('return_hurdle',c.get('reversal_return_hurdle')))
def recent_ok(z):return all(s['recent40']['net_return_pct']>0 and sum(f['net_return_pct']>0 for f in s['recent40']['folds'])>=6 for s in z['scenes'].values())
def criteria(c,positive,robust):
 s=c['scenes'];margin=lambda z:z['margin'].get('violations',z['margin'].get('independent_sleeve_violations'))
 return {'positive_all_costs':all(z['net_return_pct']>0 for z in s.values()),'nine_of_twelve_positive_complete30d_1x_folds':sum(f['net_return_pct']>0 for f in s['1']['folds'][:12])>=9,'recent40_positive_all_costs':all(z['recent40']['net_return_pct']>0 for z in s.values()),'recent40_six_of_eight_positive5d_all_costs':recent_ok(c),'composite_DD3_lte25pct':s['3']['max_drawdown_pct']<=25,'local_positive3_gte60pct':positive>=.6,'local_recent6of8_allcost_gte60pct':robust>=.6,'four_native_or_summed_independent_bank_round_trips1':s['1']['round_trips']>=4,'gross_plus_funding_to_cost1_gte2_5':s['1']['gross_reference_PnL_to_execution_cost'] is not None and s['1']['gross_reference_PnL_to_execution_cost']>=2.5,'no_negative_collateral':all(z['cash_or_units_violations']==0 for z in s.values()),'no_order_rejections':all(z['rejected_orders']==0 for z in s.values()),'no_margin_proxy_violations':all(margin(z)==0 for z in s.values()),'terminal_flat':all(engine.D(z['terminal_units'])==0 for z in s.values()),'minimum180days':True}

def evaluate():
 assert not(R/'report.json').exists();plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(batch)==10 and all(records[x['fingerprint']]['status']=='reserved' for x in batch)
 assert sha(R/'engine.py')==plan['new_engine_sha256'];started=now();binding=json.loads((R/'code_binding_before_evaluation.json').read_text());assert all(sha(ROOT/p)==h for p,h in binding['source_sha256'].items())
 ms,cm=load(plan);vectors,source_scenes,old=recover(plan,ms,cm);configs={};(R/'results').mkdir()
 for row in batch:
  spec=json.loads((ROOT/row['spec']).read_text());arc={'spec':spec,'fingerprint':row['fingerprint'],'scenes':{}};ss={}
  for k in ['1','2','3']:
   if row['scope']=='native':
    v,z=engine.simulate(spec,ms['ETH'],int(k));z['summary']['recent40']=oldrun.recent(v,ms['ETH']);vectors[row['fingerprint'],k]=v[cm['projections']['ETH']];source_scenes[row['fingerprint'],k]=z['summary']
   else:
    fps=row['source_fingerprints'];v=vectors[fps[0],k]+vectors[fps[1],k];s=parent.summarize_parent(v,[source_scenes[fp,k] for fp in fps],cm);z={'summary':s,'source_fingerprints':fps,'source_full_NAV_sha256':[source_scenes[fp,k]['NAV_sha256_f64le'] for fp in fps]};vectors[row['fingerprint'],k]=v
   arc['scenes'][k]=z;ss[k]=z['summary']
  dest=R/'results'/(row['name']+'.json.gz');gzwrite(dest,arc);configs[row['name']]={**row,'archive':rel(dest),'archive_sha256':sha(dest),'scenes':ss,'positive_complete_30d_folds_1x':sum(f['net_return_pct']>0 for f in ss['1']['folds'][:12]),'recent40_positive_5d_folds_by_cost':{k:sum(f['net_return_pct']>0 for f in s['recent40']['folds']) for k,s in ss.items()}}
  print(row['name'],[round(ss[k]['net_return_pct'],7) for k in ['1','2','3']],flush=True)
 full={**old,**{c['fingerprint']:c for c in configs.values()}}
 for c in configs.values():
  S,H=grid_axes(c);ns=[full[g['fingerprint']] for g in plan['grid'] if g['scope']==c['scope'] and abs([21,28,35].index(g['S'])-[21,28,35].index(S))<=1 and abs([.01,.02,.03].index(g['H'])-[.01,.02,.03].index(H))<=1];positive=sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns);robust=sum(recent_ok(x) for x in ns)/len(ns)
  c['sensitivity']={'neighbor_names':[x['name'] for x in ns],'neighbor_count':len(ns),'dimension_count':2,'local_3x_neighbor_positive_fraction':positive,'local_recent_allcost_qualifying_fraction':robust};c['criteria']=criteria(c,positive,robust);c['status']='passed' if all(c['criteria'].values()) else 'rejected';c['failed_criteria']=[k for k,v in c['criteria'].items() if not v]
 report={'round':R.name,'evaluation_started_utc':started,'frozen_plan_sha256':sha(R/'plan.json'),'time_boundaries':plan['time_boundaries'],'input_data':plan['data'],'configs':configs,'read_only_grid':{g['fingerprint']:old[g['fingerprint']] for g in plan['grid'] if g['readonly']},'read_only_sources':plan['read_only_references'],'axis':{a:{'points':len(m['ts']),'axis_sha256':m['axis_sha256'],'axis_prices_sha256_f64le':m['axis_price_sha256_f64le']} for a,m in ms.items()},'parent_axis':{'union_points':len(cm['keys']),'union_axis_sha256':cm['sha256']},'summary':{'new_configs':len(configs),'new_native_components':5,'new_passive_parents':5,'cost_scenarios':30,'read_only_native_components':5,'read_only_parent_results':4,'passed':[c['name'] for c in configs.values() if c['status']=='passed'],'rejected':[c['name'] for c in configs.values() if c['status']=='rejected'],'positive_configs_by_cost':{k:sum(c['scenes'][k]['net_return_pct']>0 for c in configs.values()) for k in ['1','2','3']}},'roundtrip_meaning':'Native completed closing operations. Parent sums independent BTC and ETH closes, NOT synchronized paired trades.','limits':plan['limits']}
 put(R/'report.json',report);print(json.dumps(report['summary']),flush=True)

def finish():
 rows=json.loads((R/'batch.json').read_text());report=json.loads((R/'report.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');assert all(records[x['fingerprint']]['result_available'] and records[x['fingerprint']]['status']==report['configs'][x['name']]['status'] and records[x['fingerprint']]['report_sha256']==sha(R/'report.json') for x in rows);put(R/'finish_verification.json',{'passed':True,'financial_IDs':len(rows),'report_sha256':sha(R/'report.json')});print('PASS all10actual financial results finished')
if __name__=='__main__':globals()[argparse.ArgumentParser().parse_known_args()[1][0]]()
