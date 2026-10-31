"""Fresh native cap/notional paths and unscaled actual-bank parent backtests."""
import argparse,copy,json
import numpy as np
from common import *
from recent import recent
from portfolio import summary as portfolio_summary
import engine,market
def recent_ok(c):return all(z['recent40']['net_return_pct']>0 and sum(f['net_return_pct']>0 for f in z['recent40']['folds'])>=6 for z in c['scenes'].values())
def criteria(c,positive,robust):
 ss=c['scenes'];one=ss['1'];margin=lambda s:s['margin'].get('violations',s['margin'].get('independent_sleeve_violations'));return {'positive_all_costs':all(z['net_return_pct']>0 for z in ss.values()),'nine_of_twelve_positive_complete30d_1x_folds':sum(f['net_return_pct']>0 for f in one['folds'][:12])>=9,'recent40_positive_all_costs':all(z['recent40']['net_return_pct']>0 for z in ss.values()),'recent40_six_of_eight_positive5d_all_costs':recent_ok(c),'composite_DD3_lte25pct':ss['3']['max_drawdown_pct']<=25,'local_positive3_gte60pct':positive>=.6,'local_recent6of8_allcost_gte60pct':robust>=.6,'four_underlying_native_closes1':one['round_trips']>=4,'gross_plus_funding_to_cost1_gte2_5':one['gross_reference_PnL_to_execution_cost'] is not None and one['gross_reference_PnL_to_execution_cost']>=2.5,'no_negative_native_collateral':all(z['cash_or_units_violations']==0 for z in ss.values()),'no_native_order_rejections':all(z['rejected_orders']==0 for z in ss.values()),'no_native_margin_proxy_violations':all(margin(z)==0 for z in ss.values()),'native_terminal_flat':all(core.D(z['terminal_units'])==0 for z in ss.values()),'minimum180days':True}
def neighborhood(c,plan,full):
 grid=plan['native_grid'] if c['scope']=='native' else plan['grid']
 return [full[g['fingerprint']] for g in grid if abs(plan['volatility_windows'].index(g['V'])-plan['volatility_windows'].index(c['V']))<=1 and abs(plan['volatility_caps'].index(g['C'])-plan['volatility_caps'].index(c['C']))<=1]
def evaluate():
 assert not(R/'report.json').exists();plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(batch)==plan['expected_counts']['new_configs'] and all(records[x['fingerprint']]['status']=='reserved' for x in batch);binding=json.loads((R/'code_binding_before_evaluation.json').read_text());assert all(sha(ROOT/p)==h for p,h in binding['source_sha256'].items()) and sha(R/'engine.py')==plan['new_engine_sha256'];started=now()
 ms,cm=market.load(plan);vectors,sources,old,oldarcs,diagnostics=market.recover(plan,ms,cm);put(R/'read_only_recent_slice_diagnostics.json',{'scope':'Read-only day330 slices of existing actual native full NAVs when original report lacked recent40; no strategy/signal/order rerun or old status/report write.','source_report_hashes':{fp:x['report_sha256'] for fp,x in plan['read_only_references'].items()},'diagnostics':diagnostics});configs={};(R/'results').mkdir()
 for row in batch:
  spec=json.loads((ROOT/row['spec']).read_text());arc={'fingerprint':row['fingerprint'],'spec':spec,'scenes':{}};ss={}
  for k in ['1','2','3']:
   if row['scope']=='native':
    m=ms[row['asset']];v,z=engine.simulate(spec,m,int(k));z['summary']['recent40']=recent(v,m);vectors[row['fingerprint'],k]=v[cm['projections'][row['asset']]];sources[row['fingerprint'],k]=z['summary']
   else:
    fps=row['source_fingerprints'];v=vectors[fps[0],k]+vectors[fps[1],k];s=portfolio_summary(v,[sources[fp,k] for fp in fps],[1,1],cm);z={'summary':s,'source_fingerprints':fps,'raw_component_multipliers':[1,1],'source_full_NAV_sha256':[sources[fp,k]['NAV_sha256_f64le'] for fp in fps]};vectors[row['fingerprint'],k]=v
   ss[k]=z['summary'];arc['scenes'][k]=z
  path=R/'results'/(row['name']+'.json.gz');gzwrite(path,arc);configs[row['name']]={**row,'archive':rel(path),'archive_sha256':sha(path),'scenes':ss,'positive_complete_30d_folds_1x':sum(f['net_return_pct']>0 for f in ss['1']['folds'][:12]),'recent40_positive_5d_folds_by_cost':{k:sum(f['net_return_pct']>0 for f in z['recent40']['folds']) for k,z in ss.items()}};print(row['name'],[round(ss[k]['net_return_pct'],7) for k in ['1','2','3']],flush=True)
 full={**old,**{c['fingerprint']:c for c in configs.values()}}
 for c in configs.values():
  ns=neighborhood(c,plan,full);p=sum(z['scenes']['3']['net_return_pct']>0 for z in ns)/len(ns);q=sum(recent_ok(z) for z in ns)/len(ns);c['sensitivity']={'neighbor_names':[z['name'] for z in ns],'neighbor_count':len(ns),'dimension_count':2,'local_3x_neighbor_positive_fraction':p,'local_recent_allcost_qualifying_fraction':q};c['criteria']=criteria(c,p,q);c['status']='passed' if all(c['criteria'].values()) else 'rejected';c['failed_criteria']=[k for k,v in c['criteria'].items() if not v]
 current={g['fingerprint']:full[g['fingerprint']] for g in [*plan['native_grid'],*plan['grid']]}
 for g in [*plan['native_grid'],*plan['grid']]:
  current[g['fingerprint']]=copy.deepcopy(current[g['fingerprint']]);current[g['fingerprint']].update(V=g['V'],C=g['C'],readonly=g['readonly']);c=current[g['fingerprint']];ns=neighborhood(c,plan,full);c['current_grid_diagnostic_sensitivity']={'scope':'Current outwardgrid diagnostics only; oldcanonical qualification/criteria unchanged.','neighbor_names':[x['name'] for x in ns],'neighbor_count':len(ns),'local_positive3_fraction':sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns),'local_strict_recent_fraction':sum(recent_ok(x) for x in ns)/len(ns)}
 comparisons=[];hold=old[plan['benchmark_parent_fingerprint']]
 for g in plan['grid']:
  for k in ['1','2','3']:
   s=current[g['fingerprint']]['scenes'][k];h=hold['scenes'][k];comparisons.append({'fingerprint':g['fingerprint'],'V':g['V'],'C':g['C'],'readonly':g['readonly'],'cost_multiplier':int(k),'net_return_pct':s['net_return_pct'],'hold_return_pct':h['net_return_pct'],'excess_to_hold_pp':s['net_return_pct']-h['net_return_pct'],'cash_return_pct':0,'DD_pct':s['max_drawdown_pct']})
 report={'round':R.name,'evaluation_started_utc':started,'frozen_plan_sha256':sha(R/'plan.json'),'time_boundaries':plan['time_boundaries'],'input_data':plan['data'],'configs':configs,'read_only_grid':{fp:c for fp,c in current.items() if c['readonly']},'all_current_grid':current,'read_only_sources':plan['read_only_references'],'matched_hold_comparisons':comparisons,'parent_axis':{'union_points':len(cm['keys']),'union_axis_sha256':cm['sha256'],'folds':13,'daily_boundaries':371},'summary':{**plan['expected_counts'],'passed':[c['name'] for c in configs.values() if c['status']=='passed'],'rejected':[c['name'] for c in configs.values() if c['status']=='rejected'],'positive_configs_by_scope_role_cost':{scope:{role:{k:sum(c['scenes'][k]['net_return_pct']>0 for c in configs.values() if c['scope']==scope and c['role']==role) for k in ['1','2','3']} for role in ['candidate','benchmark']} for scope in ['native','parent']}},'execution_scope':'Fresh ETH L/H policy paths with actual15000cash/4500budget/integer LOT/size-dependent impact, fees, funding, hourly marginproxy. Parents sum actual native5000/15000 wholebanks at rawmultipliers1/1. No linear NAV scaling or old-center backtest rerun/regrading. Model backtest, no real orders.','limits':plan['limits']};put(R/'report.json',report);print(json.dumps(report['summary']),flush=True)

def finish():
 rows=json.loads((R/'batch.json').read_text());rep=json.loads((R/'report.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');assert all(records[x['fingerprint']]['result_available'] and records[x['fingerprint']]['status']==rep['configs'][x['name']]['status'] and records[x['fingerprint']]['report_sha256']==sha(R/'report.json') for x in rows);put(R/'finish_verification.json',{'passed':True,'financial_IDs':len(rows),'report_sha256':sha(R/'report.json')});print('PASS all actual financial configurations finished')
if __name__=='__main__':globals()[argparse.ArgumentParser().parse_known_args()[1][0]]()
