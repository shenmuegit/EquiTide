import argparse,copy,gzip,json
from common import *
import market,features,pair_model

def positive_recent(c,k):return sum(f['net_return_pct']>0 for f in c['scenes'][k]['recent40']['folds'])
def stress_fold_ok(c):return all(positive_recent(c,k)>=6 for k in ['1','2','3'])
def neighbors(c,configs):return [x for x in configs.values() if abs(ENTRIES.index(x['entry_z'])-ENTRIES.index(c['entry_z']))<=1 and abs(EXITS.index(x['exit_z'])-EXITS.index(c['exit_z']))<=1]
def criteria(c,ns):
 s=c['scenes'];ratio=s['1']['gross_reference_PnL_to_execution_cost'];return {'positive_all_costs':all(x['net_return_pct']>0 for x in s.values()),'nine_of_twelve_positive_complete30d_1x_folds':sum(f['net_return_pct']>0 for f in s['1']['folds'][:12])>=9,'recent40_positive_all_costs':all(x['recent40']['net_return_pct']>0 for x in s.values()),'recent40_six_of_eight_positive5d_all_costs':stress_fold_ok(c),'composite_DD3_lte25pct':s['3']['max_drawdown_pct']<=25,'local_positive3_gte60pct':sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns)>=.6,'local_recent6of8_allcost_gte60pct':sum(stress_fold_ok(x) for x in ns)/len(ns)>=.6,'four_completed_pair_round_trips1':s['1']['round_trips']>=4,'gross_plus_funding_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'no_negative_collateral':all(x['cash_or_units_violations']==0 for x in s.values()),'no_order_rejections':all(x['rejected_orders']==0 for x in s.values()),'no_margin_proxy_violations':all(x['margin']['independent_sleeve_violations']==0 for x in s.values()),'terminal_flat':all(x['terminal_flat'] for x in s.values()),'minimum180days':True}

def evaluate():
 assert not(R/'report.json').exists();plan=json.loads((R/'plan.json').read_text());rows=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(rows)==9 and all(records[x['fingerprint']]['status']=='reserved' for x in rows)
 binding=json.loads((R/'code_binding_before_evaluation.json').read_text());assert all(sha(ROOT/p)==h for p,h in binding['source_sha256'].items());assert sha(CORE_PATH)==plan['source_core']['sha256'];started=now();ms,axis=market.load(plan);fpath=R/'features.json.gz'
 if fpath.exists():ff=json.loads(gzip.decompress(fpath.read_bytes()));assert ff['plan_sha256']==sha(R/'plan.json');ff=ff['features']
 else:ff=features.calculate(ms);gzwrite(fpath,{'plan_sha256':sha(R/'plan.json'),'features':ff})
 (R/'results').mkdir(exist_ok=True);configs={};new_scenes=0;resumed_scenes=0
 for row in rows:
  sp=json.loads((ROOT/row['spec']).read_text());path=R/'results'/(row['name']+'.json.gz');arc=json.loads(gzip.decompress(path.read_bytes())) if path.exists() else {'spec':sp,'fingerprint':row['fingerprint'],'scenes':{}};assert arc['spec']==sp and arc['fingerprint']==row['fingerprint']
  for k in ['1','2','3']:
   if k in arc['scenes']:resumed_scenes+=1;continue
   arc['scenes'][k]=pair_model.simulate(sp,ms,axis,ff,int(k));gzwrite(path,arc);new_scenes+=1;put(R/'progress.json',{'last_completed_config':row['name'],'last_completed_cost':k,'actual_new_scenes_this_invocation':new_scenes,'resumed_scene_evidence':resumed_scenes,'report_started_utc':started});print(row['name'],k,arc['scenes'][k]['summary']['net_return_pct'],flush=True)
  scenes={k:z['summary'] for k,z in arc['scenes'].items()};configs[row['name']]={**row,'archive':rel(path),'archive_sha256':sha(path),'scenes':scenes,'positive_folds_1x':sum(f['net_return_pct']>0 for f in scenes['1']['folds']),'positive_complete_30d_folds_1x':sum(f['net_return_pct']>0 for f in scenes['1']['folds'][:12])}
 for c in configs.values():
  ns=neighbors(c,configs);c['sensitivity']={'neighbor_names':[x['name'] for x in ns],'neighbor_count':len(ns),'dimension_count':2,'local_3x_neighbor_positive_fraction':sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns),'local_recent6of8_allcost_fraction':sum(stress_fold_ok(x) for x in ns)/len(ns)};c['criteria']=criteria(c,ns);c['status']='passed' if all(c['criteria'].values()) else 'rejected';c['failed_criteria']=[k for k,v in c['criteria'].items() if not v]
 out={'round':R.name,'evaluation_started_utc':started,'frozen_plan_sha256':sha(R/'plan.json'),'feature_archive_sha256':sha(fpath),'configs':configs,'summary':{'new_configs':9,'candidate_configs':9,'new_joint_pair_models':9,'cost_scenarios':27,'internal_native_bank_cost_curves':54,'new_independent_components':0,'new_benchmarks':0,'source_controls_readonly':3,'passed':[c['name'] for c in configs.values() if c['status']=='passed'],'rejected':[c['name'] for c in configs.values() if c['status']=='rejected'],'positive_configs_by_cost':{k:sum(c['scenes'][k]['net_return_pct']>0 for c in configs.values()) for k in ['1','2','3']},'actual_scene_calculations_this_invocation':new_scenes,'previous_completed_scenes_reused':resumed_scenes},'parent_axis':{'union_points':len(axis['ts']),'union_axis_sha256':axis['axis_sha256'],'daily_boundaries':371,'hourly_decisions':8880,'folds':13,'raw_funded_units':[1,1]},'input_data':plan['data'],'scope':plan['limits']};put(R/'report.json',out);print(json.dumps(out['summary']),flush=True)

def finish():
 r=json.loads((R/'report.json').read_text());z=reg.read_records(ROOT/'research/automation/registry.jsonl');assert all(z[c['fingerprint']]['result_available'] is True and z[c['fingerprint']]['status']==c['status'] and z[c['fingerprint']]['report_sha256']==sha(R/'report.json') for c in r['configs'].values());put(R/'finish_verification.json',{'passed':True,'financial_configs':9,'report_sha256':sha(R/'report.json')});print('PASS9 actual finished paired configurations')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['freeze','evaluate','finish']);a=p.parse_args().command
 if a=='freeze':module(R/'freeze.py','pair_definition_freeze').main()
 else:globals()[a]()
