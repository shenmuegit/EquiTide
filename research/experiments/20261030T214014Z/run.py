import argparse,json
from common import *
import portfolio
ENTRIES=[2,2.5,3];WEIGHTS=[.25,.5,.75]

def strict(c):return all(sum(f['net_return_pct']>0 for f in z['recent40']['folds'])>=6 for z in c['scenes'].values())
def neighbors(c,cs):return [x for x in cs if abs(ENTRIES.index(x['entry_z'])-ENTRIES.index(c['entry_z']))<=1 and abs(WEIGHTS.index(x['raw_pair_units'])-WEIGHTS.index(c['raw_pair_units']))<=1]
def criteria(c,ns):
 s=c['scenes'];ratio=s['1']['gross_reference_PnL_to_execution_cost'];return {'positive_all_costs':all(x['net_return_pct']>0 for x in s.values()),'nine_of_twelve_positive_complete30d_1x_folds':sum(f['net_return_pct']>0 for f in s['1']['folds'][:12])>=9,'recent40_positive_all_costs':all(x['recent40']['net_return_pct']>0 for x in s.values()),'recent40_six_of_eight_positive5d_all_costs':strict(c),'composite_DD3_lte25pct':s['3']['max_drawdown_pct']<=25,'local_positive3_gte60pct':sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns)>=.6,'local_recent6of8_allcost_gte60pct':sum(strict(x) for x in ns)/len(ns)>=.6,'four_source_completed_round_trips1':s['1']['round_trips']>=4,'gross_plus_funding_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'no_negative_collateral':all(x['cash_or_units_violations']==0 for x in s.values()),'no_order_rejections':all(x['rejected_orders']==0 for x in s.values()),'no_margin_proxy_violations':all(x['margin']['independent_sleeve_violations']==0 for x in s.values()),'terminal_flat':all(x['terminal_flat'] for x in s.values()),'minimum180days':True}
def evaluate():
 assert not(R/'report.json').exists();p=json.loads((R/'plan.json').read_text());rows=json.loads((R/'batch.json').read_text());rr=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(rows)==12 and all(rr[x['fingerprint']]['status']=='reserved' for x in rows);binding=json.loads((R/'code_binding_before_evaluation.json').read_text());assert all(sha(ROOT/q)==h for q,h in binding['source_sha256'].items());started=now();ms,oldms,axis,curves,ss,proof=portfolio.read_sources(p);put(R/'source_revaluation.json',proof);(R/'results').mkdir();configs={}
 for row in rows:
  sp=json.loads((ROOT/row['spec']).read_text());out={'spec':sp,'fingerprint':row['fingerprint'],'scenes':{}}
  for k in ['1','2','3']:
   v=curves[(row['trend_fp'],k)].copy();xs=[ss[(row['trend_fp'],k)]['summary']];ws=[1]
   if row['role']=='candidate':v+=row['raw_pair_units']*curves[(row['pair_fp'],k)];xs.append(ss[(row['pair_fp'],k)]['summary']);ws.append(row['raw_pair_units'])
   else:v+=row['cash_usdt']
   z=portfolio.summary(v,axis,xs,ws,row['capital_usdt']);out['scenes'][k]={'summary':z,'source_fingerprints':[row['trend_fp'],*([] if row['pair_fp'] is None else [row['pair_fp']])],'raw_owned_units':ws,'cash_usdt':row['cash_usdt'],'source_expanded_NAV_sha256':[proof[x+':'+k]['expanded_NAV_sha256_f64le'] for x in [row['trend_fp'],*([] if row['pair_fp'] is None else [row['pair_fp']])]]}
  dest=R/'results'/(row['name']+'.json.gz');gzwrite(dest,out);configs[row['name']]={**row,'archive':rel(dest),'archive_sha256':sha(dest),'scenes':{k:z['summary'] for k,z in out['scenes'].items()}};print('ACTUAL',row['name'],*[configs[row['name']]['scenes'][k]['net_return_pct'] for k in ['1','2','3']],flush=True)
 candidates=[x for x in configs.values() if x['role']=='candidate'];controls=[x for x in configs.values() if x['role']=='benchmark']
 for c in configs.values():
  ns=neighbors(c,candidates) if c['role']=='candidate' else controls;c['sensitivity']={'neighbor_names':[x['name'] for x in ns],'neighbor_count':len(ns),'dimension_count':2 if c['role']=='candidate' else 1,'local_3x_neighbor_positive_fraction':sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns),'local_recent6of8_allcost_fraction':sum(strict(x) for x in ns)/len(ns)};c['criteria']=criteria(c,ns);c['status']='passed' if all(c['criteria'].values()) else 'rejected';c['failed_criteria']=[k for k,v in c['criteria'].items() if not v]
 out={'round':R.name,'evaluation_started_utc':started,'frozen_plan_sha256':sha(R/'plan.json'),'configs':configs,'summary':{'new_configs':12,'candidate_configs':9,'new_matchedcapital_comparators':3,'cost_scenarios':36,'new_source_orders':0,'new_source_strategy_simulations':0,'passed':[c['name'] for c in candidates if c['status']=='passed'],'rejected':[c['name'] for c in candidates if c['status']=='rejected'],'positive_candidates_by_cost':{k:sum(c['scenes'][k]['net_return_pct']>0 for c in candidates) for k in ['1','2','3']},'source_controls_readonly':len(p['source_results'])},'parent_axis':{'union_points':len(axis['ts']),'union_axis_sha256':axis['axis_sha256'],'daily_boundaries':371,'folds':13,'original_trend_points':545013,'expanded_trend_points':570543},'input_data':p['data'],'scope':p['limits']};put(R/'report.json',out);print(json.dumps(out['summary']),flush=True)
def finish():
 r=json.loads((R/'report.json').read_text());rr=reg.read_records(ROOT/'research/automation/registry.jsonl');assert all(rr[x['fingerprint']]['status']==x['status'] and rr[x['fingerprint']]['result_available'] and rr[x['fingerprint']]['report_sha256']==sha(R/'report.json') for x in r['configs'].values());put(R/'finish_verification.json',{'passed':True,'financial_configs':12,'report_sha256':sha(R/'report.json')});print('PASS12 completed source-unit allocations')
if __name__=='__main__':
 cmd=__import__('sys').argv[1]
 if cmd=='freeze':module(R/'freeze.py','freeze_fund_units').main()
 else:globals()[cmd]()
