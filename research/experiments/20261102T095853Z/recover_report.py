"""Recover only metadata/report from all36 completed saved cost scenes; never rerun finance."""
import copy,gzip,json
from common import *
import run,engine,market
proof=json.loads((R/'report_recovery_plan.json').read_text());binding=json.loads((R/'report_recovery_binding.json').read_text());assert not(R/'report.json').exists()
assert sha(Path(__file__))==binding['source_sha256']
for item in proof['archives_preserved_before_recovery']:assert sha(ROOT/item['path'])==item['sha256']
for path,h in json.loads((R/'code_binding_before_evaluation.json').read_text())['source_sha256'].items():assert sha(ROOT/path)==h,path
forbidden=[]
def no_finance(*a,**k):forbidden.append('called');raise AssertionError('Recovery forbids any strategy/data/parent valuation')
engine.simulate=engine.decide=engine.trade=market.load=market.recover=run.evaluate=no_finance
p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());old={};diag=json.loads((R/'read_only_recent_slice_diagnostics.json').read_text())['diagnostics']
for fp,ref in p['read_only_references'].items():
 assert sha(ROOT/ref['report'])==ref['report_sha256'] and sha(ROOT/ref['archive'])==ref['archive_sha256'];doc=json.loads((ROOT/ref['report']).read_text());c=copy.deepcopy(next(z for z in doc['configs'].values() if z['fingerprint']==fp));c.update(scope=ref['scope'],asset=ref['asset'],capital_usdt=ref['capital_usdt'])
 for k,z in diag.get(fp,{}).items():c['scenes'][k]['recent40']=copy.deepcopy(z)
 old[fp]=c
configs={}
for row in batch:
 path=R/'results'/(row['name']+'.json.gz');arc=json.loads(gzip.decompress(path.read_bytes()));assert arc['fingerprint']==row['fingerprint'] and reg.fingerprint(arc['spec'])==row['fingerprint'];scenes={k:z['summary'] for k,z in arc['scenes'].items()}
 assert set(scenes)=={'1','2','3'} and all(len(s['daily_equity_usdt'])==371 and len(s['folds'])==13 for s in scenes.values())
 configs[row['name']]={**row,'archive':rel(path),'archive_sha256':sha(path),'scenes':scenes,'positive_complete_30d_folds_1x':sum(f['net_return_pct']>0 for f in scenes['1']['folds'][:12]),'recent40_positive_5d_folds_by_cost':{k:sum(f['net_return_pct']>0 for f in s['recent40']['folds']) for k,s in scenes.items()}}
full={**old,**{c['fingerprint']:c for c in configs.values()}}
regression=[]
for g,scope in [(g,'parent') for g in p['grid']]+[(g,'native') for g in p['native_grid']]:
 if not g['readonly']:continue
 wrong=copy.deepcopy(full[g['fingerprint']]);wrong.update(L=g['L'],HL=g['HS'],H=g['H'],scope=scope)
 try:run.neighborhood(wrong,p,full)
 except KeyError as e:assert e.args==('HS',)
 else:raise AssertionError('Old-key regression should fail for readonly row without HS')
 corrected=copy.deepcopy(full[g['fingerprint']]);corrected.update(L=g['L'],HS=g['HS'],H=g['H'],scope=scope);assert len(run.neighborhood(corrected,p,full))>=4;regression.append({'fp':g['fingerprint'],'scope':scope,'wrong_keyword_KeyError_HS_detected':True,'correct_HS_metadata_passed':True})
assert len(regression)==6
for c in configs.values():
 ns=run.neighborhood(c,p,full);pos=sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns);rob=sum(run.recent_ok(x) for x in ns)/len(ns);c['sensitivity']={'neighbor_names':[x['name'] for x in ns],'neighbor_count':len(ns),'dimension_count':2,'local_3x_neighbor_positive_fraction':pos,'local_recent_allcost_qualifying_fraction':rob};c['criteria']=run.criteria(c,pos,rob);c['status']='passed' if all(c['criteria'].values()) else 'rejected';c['failed_criteria']=[k for k,v in c['criteria'].items() if not v]
current={};native_current={}
for g,scope in [(g,'parent') for g in p['grid']]+[(g,'native') for g in p['native_grid']]:
 c=copy.deepcopy(full[g['fingerprint']]);c.update(L=g['L'],HS=g['HS'],HL=.015,H=g['H'],readonly=g['readonly'],scope=scope,role='candidate' if scope=='parent' else 'component',BTC_capital_usdt=3750);ns=run.neighborhood(c,p,full);c['current_grid_diagnostic_sensitivity']={'scope':'CurrentL/HSmetadata diagnostics only; old canonicalstatus/criteria/sensitivity unchanged','neighbor_names':[x['name'] for x in ns],'neighbor_count':len(ns),'local_positive3_fraction':sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns),'local_strict_recent_fraction':sum(run.recent_ok(x) for x in ns)/len(ns)};(current if scope=='parent' else native_current)[g['fingerprint']]=c
holds={3750:full[p['benchmark_parent_fingerprint']]};comparisons=[]
for g in p['grid']:
 for k,s in current[g['fingerprint']]['scenes'].items():
  h=holds[3750]['scenes'][k];assert s['initial_capital_usdt']==h['initial_capital_usdt']==18750;comparisons.append({'fingerprint':g['fingerprint'],'L':g['L'],'HS':g['HS'],'H':g['H'],'readonly':g['readonly'],'cost_multiplier':int(k),'net_return_pct':s['net_return_pct'],'hold_return_pct':h['net_return_pct'],'excess_to_hold_pp':s['net_return_pct']-h['net_return_pct'],'cash_return_pct':0,'DD_pct':s['max_drawdown_pct']})
priorpath=ROOT/p['prior_report']['path'];assert sha(priorpath)==p['prior_report']['sha256'];prior=json.loads(priorpath.read_text());axis=prior['parent_axis'];assert prior['input_data']==p['data'] and axis['union_points']==545013 and axis['daily_boundaries']==371
for c in configs.values():assert all(s['NAV_points']==axis['union_points'] for s in c['scenes'].values())
evalreceipt=json.loads((R/'evaluate_commands.json').read_text())[0];assert evalreceipt['exit_code']==1
report={'round':R.name,'evaluation_started_utc':evalreceipt['started_utc'],'evaluation_timestamp_provenance':'Exact actual evaluation command start is a conservative prevaluation bound. Internal evaluation start was not persisted before report-grid failure. No invented fill/event timestamp.','original_evaluation_command':evalreceipt,'report_recovery':{'code':rel(Path(__file__)),'source_sha256':sha(Path(__file__)),'binding_sha256':sha(R/'report_recovery_binding.json'),'initial_failure':'All36 cost-scenes finished; readonly-row metadata used HL keyword for HS grid and raised KeyError HS.','financial_reruns':0,'archives_bytes_unchanged':True,'rules_gates_weights_unchanged':True},'frozen_plan_sha256':sha(R/'plan.json'),'time_boundaries':p['time_boundaries'],'input_data':p['data'],'configs':configs,'all_current_grid':current,'all_current_native_grid':native_current,'read_only_native_grid':{fp:c for fp,c in native_current.items() if c['readonly']},'read_only_grid':{fp:c for fp,c in current.items() if c['readonly']},'read_only_sources':p['read_only_references'],'matched_hold_comparisons':comparisons,'benchmark_grid':holds,'parent_axis':axis,'summary':{**p['expected_counts'],'passed':[c['name'] for c in configs.values() if c['role']=='candidate' and c['status']=='passed'],'rejected':[c['name'] for c in configs.values() if c['status']=='rejected'],'candidate_rejected':[c['name'] for c in configs.values() if c['role']=='candidate' and c['status']=='rejected'],'benchmark_rejected':[]},'execution_scope':{'new_native_models':6,'new_parent_models':6,'native_asset':'ETH','varied_axes':['fastlookbackL','asymmetric_short_entry_hurdle_HS'],'bank_capitals_usdt':[3750,15000],'fixed_entry_notionals_usdt':[375,4500],'raw_child_weights':[1,1],'old_unique_results_readonly':10,'no_linear_NAV_scaling':True,'parent_orders':0,'explanation':'Saved six actual ETHshortHS2/3 ledgers with fixedlongHL1.5 and six passive actual BTC3750 parents. PreviousHS2.5/hold ledgers readonly. Metadata report recovery did not revalue signals/trades/NAV or parameters.'},'limits':p['limits']}
assert not forbidden
for item in proof['archives_preserved_before_recovery']:assert sha(ROOT/item['path'])==item['sha256']
put(R/'report_recovery_regression.json',{'passed':True,'six_old_field_failures_detected_and_HS_metadata_corrected':regression,'forbidden_financial_calls':len(forbidden),'real_archives_unchanged':12,'cost_scenes_unchanged':36,'new_evaluation_trials':0,'original_plan_sha256':sha(R/'plan.json'),'original_code_binding_sha256':sha(R/'code_binding_before_evaluation.json')});put(R/'report.json',report)
put(R/'report_recovery_verification.json',{'passed':True,'report_sha256':sha(R/'report.json'),'original_bound_code_unchanged':True,'frozen_rules_and_gates_unchanged':True,'preserved_archives':proof['archives_preserved_before_recovery'],'report_only':True,'forbidden_financial_calls':0,'actual_financial_configurations':12,'actual_cost_scenes':36,'financial_reruns':0,'parent_axis_descriptor_reused_from_same_hashed_input_data':axis})
print(json.dumps({'recovered_saved_actual_results':True,'new_financial_valuations':0,'all36costscenes_unchanged':True,**report['summary']}),flush=True)
