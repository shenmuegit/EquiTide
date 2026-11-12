"""Run22 reserved new-calendar configs exactly once, no original account changes."""
import argparse,copy,json
import numpy as np
from common import *
import market,engine
from portfolio import summary as parent_summary,sum_aligned_full_banks
fold_ok=lambda c:all(sum(f['net_return_pct']>0 for f in s['folds'])>=4 for s in c['scenes'].values())
def neighbors(c,p,full):
 if c.get('V') is None:return []
 rows=p['grid'] if c['scope']=='parent' else p['native_grid'];return [full[g['fingerprint']] for g in rows if abs(p['axes']['ETH_V'].index(g['V'])-p['axes']['ETH_V'].index(c['V']))<=1 and abs(p['axes']['ETH_VW'].index(g['VW'])-p['axes']['ETH_VW'].index(c['VW']))<=1]
def criteria(c,pos,rob):
 ss=list(c['scenes'].values());one,three=c['scenes']['1'],c['scenes']['3'];return {'not_a_benchmark_control':c['role'] not in ['benchmark','benchmark_component'],'positive_all_costs':all(z['net_return_pct']>0 for z in ss),'four_of_six_positive3d_folds_allcost':fold_ok(c),'whole_DD3_lte25pct':three['max_drawdown_pct']<=25,'local_positive3_gte60pct':pos is None or pos>=.6,'local_four_of_six_allcost_gte60pct':rob is None or rob>=.6,'four_underlying_native_closes1':one['round_trips']>=4,'gross_plus_funding_to_cost1_gte2_5':one['gross_reference_PnL_to_execution_cost'] is not None and one['gross_reference_PnL_to_execution_cost']>=2.5,'no_negative_native_collateral':all(z['cash_or_units_violations']==0 for z in ss),'no_native_order_rejections':all(z['rejected_orders']==0 for z in ss),'no_native_margin_proxy_violations':all(z['margin'].get('independent_sleeve_violations',z['margin'].get('violations'))==0 for z in ss),'native_terminal_flat':all(core.D(z['terminal_units'])==0 for z in ss),'minimum180days':DAYS>=180,'genuine_independent_prospective_validation':False}
def evaluate():
 assert not(R/'report.json').exists();p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');binding=json.loads((R/'code_binding_before_evaluation.json').read_text());assert len(batch)==22 and all(rs[z['fingerprint']]['status']=='reserved' for z in batch)
 for path,h in {**binding['source_sha256'],**binding['immutable_source_sha256']}.items():assert sha(ROOT/path)==h,path
 started=now();ms,cm=market.load(p);vectors={};summaries={};configs={};(R/'results').mkdir()
 for row in batch:
  sp=json.loads((ROOT/row['spec']).read_text());arc={'fingerprint':row['fingerprint'],'spec':sp,'scenes':{}};scenes={}
  for k in ['1','2','3']:
   if row['scope']=='native':
    m=ms[row['asset']];v,z=engine.simulate(sp,m,int(k));vectors[row['fingerprint'],k]=v[cm['projections'][row['asset']]];summaries[row['fingerprint'],k]=z['summary'];arc['scenes'][k]=z;scenes[k]=z['summary']
   else:
    fps=row['source_fingerprints'];v=sum_aligned_full_banks([vectors[f,k] for f in fps],[cm['keys'],cm['keys']]);z=parent_summary(v,[summaries[f,k] for f in fps],[1,1],cm);assert v[0]==18750;arc['scenes'][k]={'summary':z,'source_fingerprints':fps,'raw_component_multipliers':[1,1],'source_full_NAV_sha256':[summaries[f,k]['NAV_sha256_f64le'] for f in fps],'source_common_axis_sha256':cm['sha256']};scenes[k]=z
  path=R/'results'/(row['name']+'.json.gz');gzwrite(path,arc);configs[row['name']]={**row,'archive':rel(path),'archive_sha256':sha(path),'scenes':scenes,'positive_3d_folds_by_cost':{k:sum(f['net_return_pct']>0 for f in s['folds']) for k,s in scenes.items()}};print(row['name'],[scenes[k]['net_return_pct'] for k in ['1','2','3']],flush=True)
 full={c['fingerprint']:c for c in configs.values()}
 for c in configs.values():
  ns=neighbors(c,p,full);pos=sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns) if ns else None;rob=sum(fold_ok(x) for x in ns)/len(ns) if ns else None;c['sensitivity']={'dimension_count':2 if ns else 0,'neighbor_names':[x['name'] for x in ns],'neighbor_count':len(ns),'local_3x_neighbor_positive_fraction':pos,'local_four_of_six_allcost_fraction':rob,'scope':'BothETHV/VWapplicableforETHgrid/parents;fixedBTCandmatchedholdareprespecifiedreferenceswithnoin-cohortparametersearch.'};c['criteria']=criteria(c,pos,rob);c['status']='passed' if all(c['criteria'].values()) else 'rejected';c['failed_criteria']=[k for k,v in c['criteria'].items() if not v]
 grids={};ng={}
 for g in p['grid']+p['native_grid']:
  c=copy.deepcopy(full[g['fingerprint']]);c.update(g);c['current_grid_diagnostic_sensitivity']={'local_positive3_fraction':c['sensitivity']['local_3x_neighbor_positive_fraction'],'local_four_of_six_fraction':c['sensitivity']['local_four_of_six_allcost_fraction']};(grids if g['scope']=='parent' else ng)[g['fingerprint']]=c
 hold=full[p['benchmark_parent_fingerprint']];comp=[]
 for fp,c in grids.items():
  for k,z in c['scenes'].items():
   h=hold['scenes'][k];comp.append({'fingerprint':fp,'V':c['V'],'VW':c['VW'],'cost_multiplier':int(k),'net_return_pct':z['net_return_pct'],'hold_return_pct':h['net_return_pct'],'excess_to_matched_hold_pp':z['net_return_pct']-h['net_return_pct'],'matched_notional':True,'capital_usdt':18750,'BTC_N':1000,'ETH_N':4000,'cash_return_pct':0})
 report={'round':R.name,'evaluation_started_utc':started,'frozen_plan_sha256':sha(R/'plan.json'),'time_boundaries':p['time_boundaries'],'input_data':p['data'],'configs':configs,'all_current_grid':grids,'all_current_native_grid':ng,'read_only_grid':{},'read_only_native_grid':{},'read_only_sources':p['read_only_references'],'matched_hold_comparisons':comp,'benchmark_grid':{'matched_new_period_hold':hold},'parent_axis':{'union_points':len(cm['keys']),'union_axis_sha256':cm['sha256'],'folds':6,'daily_boundaries':19},'summary':{**p['expected_counts'],'passed':[c['name'] for c in configs.values() if c['scope']=='parent' and c['role']=='candidate' and c['status']=='passed'],'rejected':[c['name'] for c in configs.values() if c['status']=='rejected'],'candidate_rejected':[c['name'] for c in configs.values() if c['role']=='candidate' and c['status']=='rejected']},'execution_scope':{'new_native_models':12,'new_passive_parent_models':10,'old_annual_NAV_valuations_or_rescalings':0,'cold_start_lab_only':True,'original4accounts_reset_or_rule_adoption':False,'minimum180days_satisfied':False,'genuine_independent_future':False,'scope':'18dayretrospectivefollowup,six3daytimefolds,nofit/notuning. Allrealoutcomesfinishrejected;positivebacktestsnotstableliveprofit.'},'limits':p['limits']};put(R/'report.json',report);print(json.dumps(report['summary']),flush=True)
def reserve_batch():
 b=json.loads((R/'batch.json').read_text());assert not(R/'report.json').exists();rs=reg.read_records(ROOT/'research/automation/registry.jsonl');pending=[z for z in b if z['fingerprint'] not in rs];folder=R/'reserve_batches';folder.mkdir(exist_ok=True);path=folder/f'batch_{len(list(folder.glob("*.json"))):03d}.json';done=[]
 for z in pending[:8]:
  a=now();x=call('reserve',z);x.update(started_utc=a,finished_utc=now());done.append(x);put(path,{'actual_command_receipts':done})
 print('Reserved',len(done),'newactualcohortIDs,0financialcalculations')
def finish_batch():
 b=json.loads((R/'batch.json').read_text());r=json.loads((R/'report.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');pending=[z for z in b if rs[z['fingerprint']]['status']=='reserved'];folder=R/'finish_batches';folder.mkdir(exist_ok=True);path=folder/f'batch_{len(list(folder.glob("*.json"))):03d}.json';done=[]
 for z in pending[:8]:
  a=now();x=call('finish',z,r['configs'][z['name']]['status'],rel(R/'report.json'));x.update(started_utc=a,finished_utc=now());done.append(x);put(path,{'actual_command_receipts':done})
 print('Finished',len(done),'actualcohortresults,0recalculations')
if __name__=='__main__':globals()[argparse.ArgumentParser().parse_known_args()[1][0]]()
