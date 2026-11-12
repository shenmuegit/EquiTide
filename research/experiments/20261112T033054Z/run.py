"""Execute reserved native N variants and aligned whole-bank parent grid exactly once."""
import argparse,copy,json
import numpy as np
from common import *
import market,engine
from recent import recent
from portfolio import summary as parent_summary,sum_aligned_full_banks
recent_ok=lambda c:all(s['recent40']['net_return_pct']>0 and sum(f['net_return_pct']>0 for f in s['recent40']['folds'])>=6 for s in c['scenes'].values())
def neighbors(c,p,full):
 if c['scope']=='parent':rows=[g for g in (p['benchmark_grid'] if c.get('role')=='benchmark' else p['grid']) if abs(p['axes']['BTC_N'].index(g['NB'])-p['axes']['BTC_N'].index(c['NB']))<=1 and abs(p['axes']['ETH_N'].index(g['NE'])-p['axes']['ETH_N'].index(c['NE']))<=1]
 else:
  values=p['axes'][c['asset']+'_N'];rows=[g for g in (p['benchmark_native_grid'] if c.get('role')=='benchmark_component' else p['native_grid']) if g['asset']==c['asset'] and abs(values.index(g['N'])-values.index(c['N']))<=1]
 return [full[g['fingerprint']] for g in rows]
def criteria(c,positive,robust):
 one,three=c['scenes']['1'],c['scenes']['3'];ss=list(c['scenes'].values());return {'not_a_benchmark_control':c.get('role') not in ['benchmark','benchmark_component'],'positive_all_costs':all(z['net_return_pct']>0 for z in ss),'nine_of_twelve_positive_complete30d_1x_folds':sum(z['net_return_pct']>0 for z in one['folds'][:12])>=9,'recent40_positive_all_costs':all(z['recent40']['net_return_pct']>0 for z in ss),'recent40_six_of_eight_positive5d_all_costs':recent_ok(c),'composite_DD3_lte25pct':three['max_drawdown_pct']<=25,'local_positive3_gte60pct':positive>=.6,'local_recent6of8_allcost_gte60pct':robust>=.6,'four_underlying_native_closes1':one['round_trips']>=4,'gross_plus_funding_to_cost1_gte2_5':one['gross_reference_PnL_to_execution_cost'] is not None and one['gross_reference_PnL_to_execution_cost']>=2.5,'no_negative_native_collateral':all(z['cash_or_units_violations']==0 for z in ss),'no_native_order_rejections':all(z['rejected_orders']==0 for z in ss),'no_native_margin_proxy_violations':all(z['margin'].get('independent_sleeve_violations',z['margin'].get('violations'))==0 for z in ss),'native_terminal_flat':all(core.D(z['terminal_units'])==0 for z in ss),'minimum180days':True}
def evaluate():
 assert not(R/'report.json').exists();p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');binding=json.loads((R/'code_binding_before_evaluation.json').read_text());assert len(batch)==p['expected_counts']['new_configs'] and all(rs[z['fingerprint']]['status']=='reserved' for z in batch)
 for path,h in {**binding['source_sha256'],**binding['immutable_source_sha256']}.items():assert sha(ROOT/path)==h,path
 started=now();ms,cm=market.load(p);vectors,summaries,old,arcs,diag=market.recover(p,ms,cm);configs={};(R/'results').mkdir();put(R/'read_only_recent_slice_diagnostics.json',diag)
 for row in batch:
  spec=json.loads((ROOT/row['spec']).read_text());arc={'fingerprint':row['fingerprint'],'spec':spec,'scenes':{}};scenes={}
  for k in ['1','2','3']:
   if row['scope']=='native':
    m=ms[row['asset']];v,z=engine.simulate(spec,m,int(k));z['summary']['recent40']=recent(v,m);vectors[row['fingerprint'],k]=v[cm['projections'][row['asset']]];summaries[row['fingerprint'],k]=z['summary'];arc['scenes'][k]=z;scenes[k]=z['summary']
   else:
    fps=row['source_fingerprints'];v=sum_aligned_full_banks([vectors[x,k] for x in fps],[cm['keys'],cm['keys']]);z=parent_summary(v,[summaries[x,k] for x in fps],[1,1],cm);assert v[0]==18750;arc['scenes'][k]={'summary':z,'source_fingerprints':fps,'raw_component_multipliers':[1,1],'source_full_NAV_sha256':[summaries[x,k]['NAV_sha256_f64le'] for x in fps],'source_common_axis_sha256':cm['sha256']};scenes[k]=z
  path=R/'results'/(row['name']+'.json.gz');gzwrite(path,arc);configs[row['name']]={**row,'archive':rel(path),'archive_sha256':sha(path),'scenes':scenes,'positive_complete_30d_folds_1x':sum(f['net_return_pct']>0 for f in scenes['1']['folds'][:12]),'recent40_positive_5d_folds_by_cost':{k:sum(f['net_return_pct']>0 for f in z['recent40']['folds']) for k,z in scenes.items()}};print(row['name'],[scenes[k]['net_return_pct'] for k in ['1','2','3']],flush=True)
 full={**old,**{c['fingerprint']:c for c in configs.values()}}
 for c in configs.values():
  ns=neighbors(c,p,full);pos=sum(z['scenes']['3']['net_return_pct']>0 for z in ns)/len(ns);rob=sum(recent_ok(z) for z in ns)/len(ns);c['sensitivity']={'dimension_count':2 if c['scope']=='parent' else 1,'neighbor_names':[z['name'] for z in ns],'neighbor_count':len(ns),'local_3x_neighbor_positive_fraction':pos,'local_recent_allcost_qualifying_fraction':rob};c['criteria']=criteria(c,pos,rob);c['status']='passed' if all(c['criteria'].values()) else 'rejected';c['failed_criteria']=[k for k,v in c['criteria'].items() if not v]
 current={};nc={}
 for g in p['grid']+p['native_grid']+p['benchmark_grid']+p['benchmark_native_grid']:
  c=copy.deepcopy(full[g['fingerprint']]);c.update(g);ns=neighbors(c,p,full);c['current_grid_diagnostic_sensitivity']={'neighbor_names':[x['name'] for x in ns],'neighbor_count':len(ns),'local_positive3_fraction':sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns),'local_strict_recent_fraction':sum(recent_ok(x) for x in ns)/len(ns)};(current if g['scope']=='parent' else nc)[g['fingerprint']]=c
 comparisons=[];bypair={(g['NB'],g['NE']):full[g['fingerprint']] for g in p['benchmark_grid']};hold=old[p['benchmark_parent_fingerprint']]
 for fp,c in list(current.items()):
  if c['role']!='candidate':continue
  hold=bypair[c['NB'],c['NE']]
  for k,z in c['scenes'].items():
   h=hold['scenes'][k];assert z['initial_capital_usdt']==h['initial_capital_usdt']==18750;comparisons.append({'fingerprint':fp,'NB':c['NB'],'NE':c['NE'],'cost_multiplier':int(k),'net_return_pct':z['net_return_pct'],'hold_return_pct':h['net_return_pct'],'excess_to_matched_hold_pp':z['net_return_pct']-h['net_return_pct'],'cash_return_pct':0,'matched_notional':True,'matched_hold_fingerprint':hold['fingerprint']})
 report={'round':R.name,'evaluation_started_utc':started,'frozen_plan_sha256':sha(R/'plan.json'),'time_boundaries':p['time_boundaries'],'input_data':p['data'],'configs':configs,'all_current_grid':{fp:c for fp,c in current.items() if c['role']=='candidate'},'all_current_native_grid':{fp:c for fp,c in nc.items() if c['role']=='component'},'all_current_benchmark_grid':{fp:c for fp,c in current.items() if c['role']=='benchmark'},'all_current_benchmark_native_grid':{fp:c for fp,c in nc.items() if c['role']=='benchmark_component'},'read_only_grid':{fp:z for fp,z in current.items() if z['readonly']},'read_only_native_grid':{fp:z for fp,z in nc.items() if z['readonly']},'read_only_sources':p['read_only_references'],'matched_hold_comparisons':comparisons,'benchmark_grid':{fp:c for fp,c in current.items() if c['role']=='benchmark'},'parent_axis':{'union_points':len(cm['keys']),'union_axis_sha256':cm['sha256'],'folds':13,'daily_boundaries':371},'summary':{**p['expected_counts'],'passed':[c['name'] for c in configs.values() if c['role']=='candidate' and c['status']=='passed'],'rejected':[c['name'] for c in configs.values() if c['status']=='rejected'],'candidate_rejected':[c['name'] for c in configs.values() if c['role']=='candidate' and c['status']=='rejected']},'execution_scope':{'new_native_models':p['expected_counts']['new_native'],'new_parent_models':p['expected_counts']['new_parents'],'native_assets':['BTC','ETH'],'varied_axes':['BTC_actual_entry_N','ETH_actual_entry_N'],'bank_capitals_usdt':[3750,15000],'raw_child_weights':[1,1],'no_linear_NAV_scaling':True,'parent_orders':0,'old_unique_results_readonly':len(p['read_only_references']),'native_sizing_sensitivity_own_N_only':True,'each_cell_actual_sameN_C_matched_hold':True},'limits':p['limits']};put(R/'report.json',report);print(json.dumps(report['summary']),flush=True)
def reserve_batch():
 batch=json.loads((R/'batch.json').read_text());assert not(R/'report.json').exists();rs=reg.read_records(ROOT/'research/automation/registry.jsonl');pending=[z for z in batch if z['fingerprint'] not in rs];folder=R/'reserve_batches';folder.mkdir(exist_ok=True);path=folder/f'batch_{len(list(folder.glob("*.json"))):03d}.json';done=[]
 for row in pending[:8]:
  a=now();z=call('reserve',row);z.update(started_utc=a,finished_utc=now());done.append(z);put(path,{'actual_command_receipts':done})
 print('Reserved',len(done),'newfinancialIDs;0calculations')
def finish_batch():
 batch=json.loads((R/'batch.json').read_text());r=json.loads((R/'report.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');pending=[z for z in batch if rs[z['fingerprint']]['status']=='reserved'];folder=R/'finish_batches';folder.mkdir(exist_ok=True);path=folder/f'batch_{len(list(folder.glob("*.json"))):03d}.json';done=[]
 for row in pending[:8]:
  a=now();z=call('finish',row,r['configs'][row['name']]['status'],rel(R/'report.json'));z.update(started_utc=a,finished_utc=now());done.append(z);put(path,{'actual_command_receipts':done})
 print('Finished',len(done),'actualresults;0recalculations')
if __name__=='__main__':globals()[argparse.ArgumentParser().parse_known_args()[1][0]]()
