"""Execute preregistered389day banks once, then reuse their dollar NAV for parents."""
import argparse,copy,json
import numpy as np
from common import *
import market,engine
from recent import recent
from portfolio import summary as parent_summary,sum_aligned_full_banks
def extension(v,m):
 ix=m['daily_indices'];daily=v[ix].tolist();a=int(ix[370]);tail=v[a:];z={**core.stats(tail,daily[370:],19),'start_utc':'2026-10-24T00:01:00Z','end_exclusive_utc':'2026-11-12T00:01:00Z','initial_NAV_usdt':float(tail[0]),'final_NAV_usdt':float(tail[-1]),'NAV_points':len(tail),'NAV_sha256_f64le':core.navhash(tail),'daily_equity_usdt':daily[370:],'state_policy':'Inherited actual day370 predecision cash/q; old Oct24 terminal exit is absent, no reset or diagnostic orders.','folds':[]}
 for j,(lo,hi) in enumerate(zip([370,375,380,385],[375,380,385,389])):
  aa,bb=ix[[lo,hi]];z['folds'].append({'fold':j+1,'start_utc':core.stamp(int(m['ts'][aa])),'end_exclusive_utc':core.stamp(int(m['ts'][bb])),'duration_days':hi-lo,**core.stats(v[aa:bb+1],daily[lo:hi+1],hi-lo)})
 assert len(daily[370:])==20 and abs(np.prod([1+f['net_return_pct']/100 for f in z['folds']])-tail[-1]/tail[0])<1e-12;return z
recent_ok=lambda c:all(z['recent40']['net_return_pct']>0 and sum(f['net_return_pct']>0 for f in z['recent40']['folds'])>=6 for z in c['scenes'].values())
def neighbors(c,p,full):
 rows=p['grid'] if c['scope']=='parent' else p['native_grid'];ns=[g for g in rows if abs(p['axes']['PREM_W'].index(g['W'])-p['axes']['PREM_W'].index(c['W']))<=1 and abs(p['axes']['PREM_CAP'].index(g['K'])-p['axes']['PREM_CAP'].index(c['K']))<=1];return [full[g['fingerprint']] for g in ns],2
def criteria(c,pos,rob):
 ss=list(c['scenes'].values());one,three=c['scenes']['1'],c['scenes']['3'];return {'positive_all_costs':all(z['net_return_pct']>0 for z in ss),'nine_of_twelve_positive_complete30d_1x_folds':sum(f['net_return_pct']>0 for f in one['folds'][:12])>=9,'recent40_positive_all_costs':all(z['recent40']['net_return_pct']>0 for z in ss),'recent40_six_of_eight_positive5d_all_costs':recent_ok(c),'composite_DD3_lte25pct':three['max_drawdown_pct']<=25,'local_positive3_gte60pct':pos>=.6,'local_recent6of8_allcost_gte60pct':rob>=.6,'four_underlying_native_closes1':one['round_trips']>=4,'gross_plus_funding_to_cost1_gte2_5':one['gross_reference_PnL_to_execution_cost'] is not None and one['gross_reference_PnL_to_execution_cost']>=2.5,'no_negative_native_collateral':all(z['cash_or_units_violations']==0 for z in ss),'no_native_order_rejections':all(z['rejected_orders']==0 for z in ss),'no_native_margin_proxy_violations':all(z['margin'].get('independent_sleeve_violations',z['margin'].get('violations'))==0 for z in ss),'native_terminal_flat':all(core.D(z['terminal_units'])==0 for z in ss),'minimum180days':True,'extension19_positive_all_costs':all(z['extension19']['net_return_pct']>0 for z in ss),'extension19_three_of_four_positive_folds_all_costs':all(sum(f['net_return_pct']>0 for f in z['extension19']['folds'])>=3 for z in ss)}
def evaluate():
 assert not (R/'report.json').exists();p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');binding=json.loads((R/'code_binding_before_evaluation.json').read_text());assert len(batch)==18 and all(rs[z['fingerprint']]['status']=='reserved' for z in batch)
 for path,h in {**binding['source_sha256'],**binding['immutable_source_sha256']}.items():assert sha(ROOT/path)==h,path
 started=now();ms,cm=market.load(p);vectors={};summaries={};configs={};
 for fp,d in p['read_only_references'].items():
  if d['scope']!='native':continue
  arc=json.loads(gzip.decompress((ROOT/d['archive']).read_bytes()));m=ms[d['asset']]
  for k,z in arc['scenes'].items():
   v=np.empty(len(m['ts']))
   for seg in z['state_segments']:v[seg['axis_start']:seg['axis_end_exclusive']]=float(seg['cash'])+float(seg['signed_units'])*(m['axis_prices'][seg['axis_start']:seg['axis_end_exclusive']]-float(seg['entry_price']))
   assert core.navhash(v)==z['summary']['NAV_sha256_f64le'];vectors[fp,k]=v[cm['projections'][d['asset']]];summaries[fp,k]=z['summary']
 (R/'results').mkdir();proxy={'ts':cm['start_ns']+cm['keys']//16,'daily_indices':cm['daily_indices']}
 for row in batch:
  sp=json.loads((ROOT/row['spec']).read_text());arc={'fingerprint':row['fingerprint'],'spec':sp,'scenes':{}};scenes={}
  for k in ['1','2','3']:
   if row['scope']=='native':
    m=ms[row['asset']];v,z=engine.simulate(sp,m,int(k));z['summary']['recent40']=recent(v,m);z['summary']['extension19']=extension(v,m);vectors[row['fingerprint'],k]=v[cm['projections'][row['asset']]];summaries[row['fingerprint'],k]=z['summary'];arc['scenes'][k]=z;scenes[k]=z['summary']
   else:
    fps=row['source_fingerprints'];v=sum_aligned_full_banks([vectors[f,k] for f in fps],[cm['keys'],cm['keys']]);z=parent_summary(v,[summaries[f,k] for f in fps],[1,1],cm);z['extension19']=extension(v,proxy);vectors[row['fingerprint'],k]=v;summaries[row['fingerprint'],k]=z;scenes[k]=z;arc['scenes'][k]={'summary':z,'source_fingerprints':fps,'raw_component_multipliers':[1,1],'source_full_NAV_sha256':[summaries[f,k]['NAV_sha256_f64le'] for f in fps],'source_common_axis_sha256':cm['sha256']}
  path=R/'results'/(row['name']+'.json.gz');gzwrite(path,arc);configs[row['name']]={**row,'archive':rel(path),'archive_sha256':sha(path),'scenes':scenes,'positive_complete_30d_folds_1x':sum(f['net_return_pct']>0 for f in scenes['1']['folds'][:12]),'recent40_positive_5d_folds_by_cost':{k:sum(f['net_return_pct']>0 for f in z['recent40']['folds']) for k,z in scenes.items()}};print(row['name'],[scenes[k]['net_return_pct'] for k in ['1','2','3']],'extension19',[scenes[k]['extension19']['net_return_pct'] for k in ['1','2','3']],flush=True)
 full={c['fingerprint']:c for c in configs.values()}
 for c in configs.values():
  ns,dims=neighbors(c,p,full);pos=sum(z['scenes']['3']['net_return_pct']>0 for z in ns)/len(ns);rob=sum(recent_ok(z) for z in ns)/len(ns);c['sensitivity']={'dimension_count':dims,'neighbor_names':[z['name'] for z in ns],'neighbor_count':len(ns),'local_3x_neighbor_positive_fraction':pos,'local_recent_allcost_qualifying_fraction':rob};c['criteria']=criteria(c,pos,rob);c['status']='passed' if all(c['criteria'].values()) else 'rejected';c['failed_criteria']=[k for k,z in c['criteria'].items() if not z];c['current_grid_diagnostic_sensitivity']={'local_strict_recent_fraction':rob,'local_positive3_fraction':pos}
 hd=p['read_only_references'][p['benchmark_parent_fingerprint']];hold=next(c for c in json.loads((ROOT/hd['report']).read_text())['configs'].values() if c['fingerprint']==p['benchmark_parent_fingerprint']);comparisons=[]
 for g in p['grid']:
  c=full[g['fingerprint']]
  for k,z in c['scenes'].items():comparisons.append({'fingerprint':g['fingerprint'],'W':g['W'],'K':g['K'],'cost_multiplier':int(k),'net_return_pct':z['net_return_pct'],'hold_return_pct':hold['scenes'][k]['net_return_pct'],'excess_to_matched_hold_pp':z['net_return_pct']-hold['scenes'][k]['net_return_pct'],'cash_return_pct':0,'matched_notional':True,'extension19_excess_to_hold_pp':z['extension19']['net_return_pct']-hold['scenes'][k]['extension19']['net_return_pct']})
 report={'round':R.name,'evaluation_started_utc':started,'frozen_plan_sha256':sha(R/'plan.json'),'time_boundaries':p['time_boundaries'],'input_data':p['data'],'configs':configs,'all_current_grid':{g['fingerprint']:full[g['fingerprint']] for g in p['grid']},'all_current_native_grid':{g['fingerprint']:full[g['fingerprint']] for g in p['native_grid']},'read_only_sources':p['read_only_references'],'matched_hold_comparisons':comparisons,'benchmark_grid':{'fixed_exposure':hold},'parent_axis':{'union_points':len(cm['keys']),'union_axis_sha256':cm['sha256'],'folds':13,'daily_boundaries':390},'summary':{**p['expected_counts'],'passed':[c['name'] for c in configs.values() if c['role']=='candidate' and c['status']=='passed'],'rejected':[c['name'] for c in configs.values() if c['status']=='rejected'],'candidate_rejected':[c['name'] for c in configs.values() if c['role']=='candidate' and c['status']=='rejected'],'passed_all':[c['name'] for c in configs.values() if c['status']=='passed'],'passed_source_components':[c['name'] for c in configs.values() if c['scope']=='native' and c['role']=='component' and c['status']=='passed'],'rejected_source_components':[c['name'] for c in configs.values() if c['scope']=='native' and c['status']=='rejected']},'execution_scope':{'new_native_models':9,'new_parent_models':9,'raw_child_weights':[1,1],'bank_capitals_usdt':[3750,15000],'no_linear_NAV_scaling':True,'read_only_BTC_bank_reused':True,'continuous389days':True,'old_results_kept_immutable':True,'new_data_not_untouched_final_or_independent_future':True},'limits':p['limits']};put(R/'report.json',report);print(json.dumps(report['summary']),flush=True)
def reserve_batch():
 batch=json.loads((R/'batch.json').read_text());assert not (R/'report.json').exists();rs=reg.read_records(ROOT/'research/automation/registry.jsonl');pending=[z for z in batch if z['fingerprint'] not in rs];folder=R/'reserve_batches';folder.mkdir(exist_ok=True);path=folder/f'batch_{len(list(folder.glob("*.json"))):03d}.json';done=[]
 for row in pending[:8]:
  a=now();z=call('reserve',row);z.update(started_utc=a,finished_utc=now());done.append(z);put(path,{'actual_command_receipts':done})
 print('Reserved',len(done),'newfinancialIDs;0calculations')
def finish_batch():
 r=json.loads((R/'report.json').read_text());batch=json.loads((R/'batch.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');pending=[z for z in batch if rs[z['fingerprint']]['status']=='reserved'];folder=R/'finish_batches';folder.mkdir(exist_ok=True);path=folder/f'batch_{len(list(folder.glob("*.json"))):03d}.json';done=[]
 for row in pending[:8]:
  a=now();z=call('finish',row,r['configs'][row['name']]['status'],rel(R/'report.json'));z.update(started_utc=a,finished_utc=now());done.append(z);put(path,{'actual_command_receipts':done})
 print('Finished',len(done),'actualresults;0recalculations')
if __name__=='__main__':globals()[argparse.ArgumentParser().parse_known_args()[1][0]]()
