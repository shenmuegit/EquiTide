"""Actual new combinations of previously executed native bank paths, no NAV resizing."""
import argparse,copy,json
import numpy as np
from common import *
import market
import engine
from recent import recent
from portfolio import summary as portfolio_summary,sum_aligned_full_banks
def recent_ok(c):return all(s['recent40']['net_return_pct']>0 and sum(f['net_return_pct']>0 for f in s['recent40']['folds'])>=6 for s in c['scenes'].values())
def neighborhood(c,p,full):
 grid=p['native_grid'] if c['scope']=='native' else p['grid']
 return [full[g['fingerprint']] for g in grid if abs(p['entry_hurdles'].index(g['H'])-p['entry_hurdles'].index(c['H']))<=1 and abs(p['funding_caps'].index(g['F'])-p['funding_caps'].index(c['F']))<=1]

def criteria(c,positive,robust):
 if c['role'].startswith('benchmark'):return {'benchmark_control_not_strategy_candidate':False}
 s=list(c['scenes'].values());one=c['scenes']['1'];three=c['scenes']['3'];return {'positive_all_costs':all(z['net_return_pct']>0 for z in s),'nine_of_twelve_positive_complete30d_1x_folds':sum(f['net_return_pct']>0 for f in one['folds'][:12])>=9,'recent40_positive_all_costs':all(z['recent40']['net_return_pct']>0 for z in s),'recent40_six_of_eight_positive5d_all_costs':recent_ok(c),'composite_DD3_lte25pct':three['max_drawdown_pct']<=25,'local_positive3_gte60pct':positive>=.6,'local_recent6of8_allcost_gte60pct':robust>=.6,'four_underlying_native_closes1':one['round_trips']>=4,'gross_plus_funding_to_cost1_gte2_5':one['gross_reference_PnL_to_execution_cost'] is not None and one['gross_reference_PnL_to_execution_cost']>=2.5,'no_negative_native_collateral':all(z['cash_or_units_violations']==0 for z in s),'no_native_order_rejections':all(z['rejected_orders']==0 for z in s),'no_native_margin_proxy_violations':all(z['margin'].get('independent_sleeve_violations',z['margin'].get('violations'))==0 for z in s),'native_terminal_flat':all(core.D(z['terminal_units'])==0 for z in s),'minimum180days':True}
def current_grid_row(source,g,scope):
 c=copy.deepcopy(source);c.update({k:g[k] for k in ['L','H','E','S','K','D','N','VC','F']});c.update(readonly=g['readonly'],scope=scope,role='candidate' if scope=='parent' else 'component',BTC_capital_usdt=3750);return c

def evaluate():
 assert not(R/'report.json').exists();p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(batch)==p['expected_counts']['new_configs'] and all(rs[x['fingerprint']]['status']=='reserved' for x in batch);binding=json.loads((R/'code_binding_before_evaluation.json').read_text());assert all(sha(ROOT/k)==h for k,h in binding['source_sha256'].items());started=now();ms,cm=market.load(p);vectors,ss,old,arcs,diag=market.recover(p,ms,cm);put(R/'read_only_recent_slice_diagnostics.json',{'scope':'Pastday330slices from actual fullnativeNAV only; no nativepolicy,order or newparameter evaluation.','diagnostics':diag});configs={};(R/'results').mkdir()
 for row in batch:
  sp=json.loads((ROOT/row['spec']).read_text());arc={'fingerprint':row['fingerprint'],'spec':sp,'scenes':{}};scenes={}
  for k in ['1','2','3']:
   if row['scope']=='native':
    m=ms[row['asset']];v,z=engine.simulate(sp,m,int(k));z['summary']['recent40']=recent(v,m);vectors[row['fingerprint'],k]=v[cm['projections'][row['asset']]];ss[row['fingerprint'],k]=z['summary'];arc['scenes'][k]=z;scenes[k]=z['summary']
   else:
    fps=row['source_fingerprints'];v=sum_aligned_full_banks([vectors[fp,k] for fp in fps],[cm['keys'],cm['keys']]);s=portfolio_summary(v,[ss[fp,k] for fp in fps],[1,1],cm);assert v[0]==row['capital_usdt'];arc['scenes'][k]={'summary':s,'source_fingerprints':fps,'raw_component_multipliers':[1,1],'source_full_NAV_sha256':[ss[fp,k]['NAV_sha256_f64le'] for fp in fps],'source_common_axis_sha256':cm['sha256']};scenes[k]=s
  path=R/'results'/(row['name']+'.json.gz');gzwrite(path,arc);configs[row['name']]={**row,'archive':rel(path),'archive_sha256':sha(path),'scenes':scenes,'positive_complete_30d_folds_1x':sum(f['net_return_pct']>0 for f in scenes['1']['folds'][:12]),'recent40_positive_5d_folds_by_cost':{k:sum(f['net_return_pct']>0 for f in s['recent40']['folds']) for k,s in scenes.items()}};print(row['name'],[scenes[k]['net_return_pct'] for k in ['1','2','3']],flush=True)
 full={**old,**{c['fingerprint']:c for c in configs.values()}}
 for c in configs.values():
  if c['role'] in ['candidate','component']:
   ns=neighborhood(c,p,full);pos=sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns);rob=sum(recent_ok(x) for x in ns)/len(ns);c['sensitivity']={'neighbor_names':[x['name'] for x in ns],'neighbor_count':len(ns),'dimension_count':2,'local_3x_neighbor_positive_fraction':pos,'local_recent_allcost_qualifying_fraction':rob}
  else:pos=rob=None;c['sensitivity']={'applicable':False,'reason':'Matchedcapital/notional constantlong control, not an optimized strategy; no extra parameter trials.'}
  c['criteria']=criteria(c,pos,rob);c['status']='passed' if all(c['criteria'].values()) else 'rejected';c['failed_criteria']=[k for k,v in c['criteria'].items() if not v]
 current={};native_current={}
 for g,scope in [(g,'parent') for g in p['grid']]+[(g,'native') for g in p['native_grid']]:
  c=current_grid_row(full[g['fingerprint']],g,scope);ns=neighborhood(c,p,full);c['current_grid_diagnostic_sensitivity']={'scope':'CurrentETH H/F diagnostics only,oldcanonicalstatus/criteria/sensitivityunchanged','neighbor_names':[x['name'] for x in ns],'neighbor_count':len(ns),'local_positive3_fraction':sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns),'local_strict_recent_fraction':sum(recent_ok(x) for x in ns)/len(ns)};(current if scope=='parent' else native_current)[g['fingerprint']]=c
 holds={str(g['N']):full[g['fingerprint']] for g in p['benchmarks']};comparisons=[]
 for g in p['grid']:
  for k,s in current[g['fingerprint']]['scenes'].items():
   h=holds[str(g['N'])]['scenes'][k];assert s['initial_capital_usdt']==h['initial_capital_usdt']==18750;comparisons.append({'fingerprint':g['fingerprint'],'L':g['L'],'S':g['S'],'K':g['K'],'D':g['D'],'N':g['N'],'E':g['E'],'F':g['F'],'VC':g['VC'],'H':g['H'],'readonly':g['readonly'],'cost_multiplier':int(k),'net_return_pct':s['net_return_pct'],'hold_return_pct':h['net_return_pct'],'excess_to_hold_pp':s['net_return_pct']-h['net_return_pct'],'cash_return_pct':0,'DD_pct':s['max_drawdown_pct']})
 report={'round':R.name,'evaluation_started_utc':started,'frozen_plan_sha256':sha(R/'plan.json'),'time_boundaries':p['time_boundaries'],'input_data':p['data'],'configs':configs,'all_current_grid':current,'all_current_native_grid':native_current,'read_only_native_grid':{fp:c for fp,c in native_current.items() if c['readonly']},'read_only_grid':{fp:c for fp,c in current.items() if c['readonly']},'read_only_sources':p['read_only_references'],'matched_hold_comparisons':comparisons,'benchmark_grid':holds,'parent_axis':{'union_points':len(cm['keys']),'union_axis_sha256':cm['sha256'],'folds':13,'daily_boundaries':371},'summary':{**p['expected_counts'],'passed':[c['name'] for c in configs.values() if c['role']=='candidate' and c['status']=='passed'],'rejected':[c['name'] for c in configs.values() if c['status']=='rejected'],'candidate_rejected':[c['name'] for c in configs.values() if c['role']=='candidate' and c['status']=='rejected'],'benchmark_rejected':[c['name'] for c in configs.values() if c['role'].startswith('benchmark')]},'execution_scope':{'new_native_models':p['expected_counts']['new_native'],'new_parent_models':p['expected_counts']['new_parents'],'native_asset':'ETH','varied_axes':['ETH_entry_hurdle_H','ETH_entry_funding_outflow_cap_F'],'bank_capitals_usdt':[3750,15000],'BTC_entry_notional_grid_usdt':p['entry_notionals'],'ETH_entry_notional_usdt':4500,'raw_child_weights':[1,1],'old_unique_results_readonly':len(p['read_only_references']),'no_linear_NAV_scaling':True,'parent_orders':0,'explanation':'SixnewETHfundingcaps0/.00005xH.0175/.02/.0225plus6parents/36costscenes;fixedE.0075L5K.0075VC5S16D3V10. OldcapOffthreeHcolumn,fixedBTC29H3E1bankandmatchedholdreadonly. No NAVscaling,normalization,parentorders,frozenadoption or independentholdout claim.'},'limits':p['limits']};put(R/'report.json',report);print(json.dumps(report['summary']),flush=True)
def finish():
 rows=json.loads((R/'batch.json').read_text());rep=json.loads((R/'report.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');assert all(rs[x['fingerprint']]['result_available'] and rs[x['fingerprint']]['status']==rep['configs'][x['name']]['status'] and rs[x['fingerprint']]['report_sha256']==sha(R/'report.json') for x in rows);put(R/'finish_verification.json',{'passed':True,'financial_IDs':len(rows),'report_sha256':sha(R/'report.json')});print('PASS all12 actual ETH native/parent IDs finished; oldcenter and source qualifications unchanged')
if __name__=='__main__':globals()[argparse.ArgumentParser().parse_known_args()[1][0]]()
