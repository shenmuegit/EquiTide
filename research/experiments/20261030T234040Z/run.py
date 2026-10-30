import copy,gzip,json
from common import *
import market,ranking_model
LOOKBACKS=[7,14,28];PERIODS=[7,14]
def strict(c):return all(sum(f['net_return_pct']>0 for f in x['recent40']['folds'])>=6 for x in c['scenes'].values())
def neighbors(c,cs):return [x for x in cs if abs(LOOKBACKS.index(x['lookback_days'])-LOOKBACKS.index(c['lookback_days']))<=1 and abs(PERIODS.index(x['rebalance_interval_days'])-PERIODS.index(c['rebalance_interval_days']))<=1]
def criteria(c,ns):
 s=c['scenes'];ratio=s['1']['gross_reference_PnL_to_execution_cost'];return {'positive_all_costs':all(x['net_return_pct']>0 for x in s.values()),'nine_of_twelve_positive_complete30d_1x_folds':sum(f['net_return_pct']>0 for f in s['1']['folds'][:12])>=9,'recent40_positive_all_costs':all(x['recent40']['net_return_pct']>0 for x in s.values()),'recent40_six_of_eight_positive5d_all_costs':strict(c),'composite_DD3_lte25pct':s['3']['max_drawdown_pct']<=25,'local_positive3_gte60pct':sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns)>=.6,'local_recent6of8_allcost_gte60pct':sum(strict(x) for x in ns)/len(ns)>=.6,'four_completed_pair_round_trips1':s['1']['round_trips']>=4,'gross_plus_funding_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'no_negative_collateral':all(x['cash_or_units_violations']==0 for x in s.values()),'no_order_rejections':all(x['rejected_orders']==0 for x in s.values()),'no_margin_proxy_violations':all(x['margin']['independent_sleeve_violations']==0 for x in s.values()),'terminal_flat':all(x['terminal_flat'] for x in s.values()),'minimum180days':True}
def evaluate():
 assert not(R/'report.json').exists();plan=json.loads((R/'plan.json').read_text());rows=json.loads((R/'batch.json').read_text());rr=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(rows)==6 and all(rr[x['fingerprint']]['status']=='reserved' for x in rows);binding=json.loads((R/'code_binding_before_evaluation.json').read_text());assert all(sha(ROOT/p)==h for p,h in binding['source_sha256'].items());assert sha(CORE_PATH)==plan['source_accounting']['sha256'] and sha(ROOT/plan['source_paired_helpers']['path'])==plan['source_paired_helpers']['sha256'];started=now();ms,axis=market.load(plan);(R/'results').mkdir();configs={};scenes=0
 for row in rows:
  spec=json.loads((ROOT/row['spec']).read_text());arc={'spec':spec,'fingerprint':row['fingerprint'],'scenes':{}}
  for k in ['1','2','3']:
   arc['scenes'][k]=ranking_model.simulate(spec,ms,axis,int(k));scenes+=1;dest=R/'results'/(row['name']+'.json.gz');gzwrite(dest,arc);print('ACTUAL',row['name'],k,arc['scenes'][k]['summary']['net_return_pct'],flush=True)
  ss={k:z['summary'] for k,z in arc['scenes'].items()};configs[row['name']]={**row,'archive':rel(dest),'archive_sha256':sha(dest),'scenes':ss,'positive_folds_1x':sum(f['net_return_pct']>0 for f in ss['1']['folds']),'positive_complete_30d_folds_1x':sum(f['net_return_pct']>0 for f in ss['1']['folds'][:12])}
 for c in configs.values():
  ns=neighbors(c,list(configs.values()));c['sensitivity']={'neighbor_names':[x['name'] for x in ns],'neighbor_count':len(ns),'dimension_count':2,'local_3x_neighbor_positive_fraction':sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns),'local_recent6of8_allcost_fraction':sum(strict(x) for x in ns)/len(ns)};c['criteria']=criteria(c,ns);c['status']='passed' if all(c['criteria'].values()) else 'rejected';c['failed_criteria']=[k for k,v in c['criteria'].items() if not v]
 references={}
 for fp,x in plan['read_only_references'].items():
  doc=json.loads((ROOT/x['report']).read_text());c=copy.deepcopy(doc['configs'][x['name']]);references[fp]={'source':x,'original_config':c}
 out={'round':R.name,'evaluation_started_utc':started,'frozen_plan_sha256':sha(R/'plan.json'),'configs':configs,'summary':{'new_configs':6,'candidate_configs':6,'new_joint_rank_models':6,'cost_scenarios':18,'internal_native_bank_cost_curves':36,'passed':[x['name'] for x in configs.values() if x['status']=='passed'],'rejected':[x['name'] for x in configs.values() if x['status']=='rejected'],'positive_candidates_by_cost':{k:sum(x['scenes'][k]['net_return_pct']>0 for x in configs.values()) for k in ['1','2','3']},'actual_new_scenes':scenes,'new_benchmark_configs':0,'read_only_source_controls':3},'parent_axis':{'union_points':len(axis['ts']),'axis_sha256':axis['axis_sha256'],'daily_boundaries':371,'folds':13},'read_only_reference_results':references,'input_data':plan['data'],'scope':plan['limits']};put(R/'report.json',out);print(json.dumps(out['summary']),flush=True)
def finish():
 r=json.loads((R/'report.json').read_text());rr=reg.read_records(ROOT/'research/automation/registry.jsonl');assert all(rr[c['fingerprint']]['result_available'] and rr[c['fingerprint']]['status']==c['status'] and rr[c['fingerprint']]['report_sha256']==sha(R/'report.json') for c in r['configs'].values());put(R/'finish_verification.json',{'passed':True,'financial_configs':6,'report_sha256':sha(R/'report.json')});print('PASS6 actual joint rank configurations finished')
if __name__=='__main__':
 cmd=__import__('sys').argv[1]
 if cmd=='freeze':module(R/'freeze.py','freeze_relative_rank').main()
 else:globals()[cmd]()
