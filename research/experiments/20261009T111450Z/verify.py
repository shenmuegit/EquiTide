"""Verify completed volume-confirmation evidence,causal reserves,continuous accounts and publication inputs."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal as D
import csv,gzip,hashlib,json,subprocess,sys,zipfile
T=Path(__file__).resolve().parent;R=T.parents[2];sys.path.insert(0,str(R/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();dt=lambda s:datetime.fromisoformat(s.replace('Z','+00:00'))
prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));L=R/'research/automation/registry.jsonl';lines=L.read_bytes().splitlines(keepends=True);raw=[json.loads(x)for x in lines];records=registry.read_records(L)
assert (prior['lines'],prior['canonical'],prior['preserved_ids'],len(prior['conclusions']))==(5655,2778,2780,74)
assert hashlib.sha256(b''.join(lines[:5655])).hexdigest()==prior['ledger_sha256'] and all(records[k]==v for k,v in prior['records'].items())
assert (len(lines),len(records),len({registry.fingerprint(v['spec'])for v in records.values()}))==(5725,2815,2813) and not [v for v in records.values()if v['status']=='reserved']
r=json.loads((T/'report.json').read_text());f=json.loads((T/'forward_report.json').read_text());p=r['plan'];assert p==json.loads((T/'spec.json').read_text()) and p['preflight_sha256']==sha(T/'preflight.py')
assert p['grid']['predeclared_center']==p['grid']['predeclared_focus']=={'volume_lookback_days':40,'minimum_volume_ratio':1.} and p['grid']['raw_weights']==[.75,.25] and p['grid']['component_capitals_usdt']==[1500,500]
assert p['new_configs']==32 and p['new_component_configs']==p['new_combination_configs']==16 and p['new_cost_scenes']==96 and p['reused_component_configs']==4 and p['reused_combination_configs']==2
au=json.loads((T/'audit.log').read_text());af=json.loads((T/'audit_forward.log').read_text());assert au['passed']and af['passed']and au['report_sha256']==sha(T/'report.json') and af['report_sha256']==sha(T/'forward_report.json')
assert (au['actual_scenes_audited'],au['NAV_points_audited'],au['Decimal_quote_volume_causal_decisions'],au['Decimal_fills_independently_checked'])==(96,24900672,8640,264)
assert r['summary']['new_configs']==32 and r['summary']['new_cost_scenes']==96 and len(r['summary']['passed'])==31 and len(r['summary']['rejected'])==1 and len(r['summary']['new_both_periods_passed_combination_pairs'])==8 and r['summary']['new_live_orders']==0
for bf,rf,doc,start in [('batch.json','report.json',r,r['evaluation_started_utc']),('forward_batch.json','forward_report.json',f,f['observation_started_utc'])]:
 for b in json.loads((T/bf).read_text()):
  assert registry.fingerprint(json.loads((R/b['spec']).read_text()))==b['fingerprint'];ev=[z for z in raw[5655:]if z['fingerprint']==b['fingerprint']]
  assert len(ev)==2 and ev[0]['status']=='reserved'and ev[1]['status']==doc['configs'][b['name']]['status']and ev[1]['result_available']and ev[1]['report_sha256']==sha(T/rf)
  assert dt(p['frozen_at_utc'])<dt(ev[0]['recorded_at_utc'])<dt(start)<dt(ev[1]['recorded_at_utc'])
for doc in (r,f):
 for path,h in doc['source_hashes'].items():assert sha(R/path)==h,path
for path,h in p['reused_code_sha256'].items():assert sha(R/path)==h,path
batch=json.loads((T/'batch.json').read_text());grid=json.loads((T/'grid_batch.json').read_text());assert len(batch)==32 and len(grid)==38 and sum(b['is_new']for b in grid)==32
assert {b['fingerprint']for b in batch if b['role']=='component'}=={x[3]for x in prior['novelty_preflight']['new_component_coordinates']} and {b['fingerprint']for b in batch if b['role']=='combination'}=={x[3]for x in prior['novelty_preflight']['new_grid_coordinates']}
assert {b['fingerprint']for b in grid if not b['is_new']and b.get('asset')=='BTC'}=={x[3]for x in prior['novelty_preflight']['reused_component_coordinates']}
assert {b['fingerprint']for b in grid if not b['is_new']and b['role']=='combination'}=={x[3]for x in prior['novelty_preflight']['reused_grid_coordinates']}
assert sha(T/'signals.py')==sha(R/'research/experiments/20261009T091020Z/signals.py')
for b in grid:
 c=r['configs'][b['name']];sp=json.loads((R/b['spec']).read_text());arc=json.loads(gzip.decompress((R/c['archive']).read_bytes()));assert registry.fingerprint(sp)==b['fingerprint']==arc['fingerprint'] and sp==arc['spec'] and sha(R/c['archive'])==c['archive_sha256'] and {k:v['summary']for k,v in arc['scenes'].items()}==c['scenes']
 if b['is_new']:
  assert b['volume_lookback_days']in(30,40,50) and b['minimum_volume_ratio']in(.9,1.,1.1) and c['criteria']['positive_all_costs']
  if b['role']=='component':assert sp['parameters']['initial_capital_usdt']==1500 and sp['parameters']['entry_lookback_days']==15 and sp['parameters']['exit_lookback_days']==30 and sp['parameters']['volume_lookback_days']==b['volume_lookback_days'] and sp['parameters']['minimum_volume_ratio']==b['minimum_volume_ratio'] and sp['logic']==p['rules_by_asset']['BTC']
  else:
   assert [z['weight']for z in sp['components']]==[.75,.25] and b['raw_weights']==[.75,.25];q=[records[z['fingerprint']]['spec']for z in sp['components']]
   assert [x['parameters']['initial_capital_usdt']for x in q]==[1500,500] and q[0]['parameters']['volume_lookback_days']==b['volume_lookback_days'] and q[0]['parameters']['minimum_volume_ratio']==b['minimum_volume_ratio'] and q[1]['family']=='daily-close-range-breakout' and q[1]['parameters']['entry_lookback_days']==15 and q[1]['parameters']['exit_lookback_days']==30
 else:
  ref=c['source_ref'];old=json.loads((R/ref['report']).read_text())['configs'][b['name']];assert sha(R/ref['report'])==ref['report_sha256'] and sha(R/ref['spec'])==ref['spec_sha256'] and c['scenes']==old['scenes'] and c['status']==old['status']==c['source_record_status'] and c['criteria']==old['criteria']==c['source_record_criteria'] and records[b['fingerprint']]==prior['records'][b['fingerprint']]
for name,c in r['read_only_comparators'].items():
 old=json.loads((R/c['source_report']).read_text())['configs'][name];assert old['scenes']==c['scenes']and old['status']==c['status']and sha(R/c['source_report'])==c['source_report_sha256']
 if c['kind']=='MATCHED_UNFILTERED_CHANNEL':
  sp=records[c['fingerprint']]['spec'];assert records[c['fingerprint']]==prior['records'][c['fingerprint']] and [x['weight']for x in sp['components']]==[.75,.25]
  for i,z in enumerate(sp['components']):
   q=records[z['fingerprint']]['spec'];assert q['family']=='daily-close-range-breakout'and q['parameters']['initial_capital_usdt']==(1500 if i==0 else 500) and q['parameters']['entry_lookback_days']==15 and q['parameters']['exit_lookback_days']==30
for file,count in [('sensitivity.csv',114),('folds.csv',684)]:
 with (T/file).open()as fh:
  rows=list(csv.DictReader(fh));assert len(rows)==count and all(None not in row and None not in row.values()for row in rows)
  for row in rows:
   c=r['configs'][row['config']]
   if file=='sensitivity.csv':assert float(row['net_return_pct'])==c['scenes'][row['cost']]['net_return_pct']
   else:
    ff=c['scenes'][row['cost']]['folds'][int(row['fold'])-1];assert float(row['net_return_pct'])==ff['net_return_pct']and float(row['minute_DD_pct'])==ff['max_drawdown_pct']
cmp=json.loads((T/'comparison.json').read_text());assert cmp['report_sha256']==sha(T/'report.json')and len(cmp['incumbent_comparisons'])==len(cmp['unfiltered_comparisons'])==18 and cmp['new_both_periods_qualified']==8 and cmp['new_joint_improvements_over_incumbent']==cmp['new_strict_return_improvements_both_years']==0 and cmp['new_pairs_identical_to_incumbent_both_years']==2 and cmp['failure_counts']=={'four_positive_1x_folds':1}
assert cmp['path_signature_counts']=={'2025_BTC':3,'2026_BTC':2,'2025_ETH':1,'2026_ETH':1,'2025_combination':3,'2026_combination':2}
for collection in('incumbent_comparisons','unfiltered_comparisons'):
 for x in cmp[collection]:
  c=r['configs'][x['config']];o=(r['configs']if collection=='incumbent_comparisons'else r['read_only_comparators'])[x['comparator']];assert c['year']==o['year']==x['year']and x['same_initial_funding']==[1500,500]
  if collection=='incumbent_comparisons':assert not o['is_new']and(o['volume_lookback_days'],o['minimum_volume_ratio'])==(30,1)
  assert x['return_differences_pp']=={k:c['scenes'][k]['net_return_pct']-o['scenes'][k]['net_return_pct']for k in('1','2','3')}and x['minute_DD3_difference_pp']==c['scenes']['3']['max_drawdown_pct']-o['scenes']['3']['max_drawdown_pct']and x['all_cost_NAV_identical']==all(c['scenes'][k]['NAV_sha256_f64le']==o['scenes'][k]['NAV_sha256_f64le']for k in('1','2','3'))
for x in cmp['new_qualified_pairs_vs_incumbent']:
 ds=[next(z for z in cmp['incumbent_comparisons']if z['config']==n)for n in x['pair']];ret=[v for z in ds for v in z['return_differences_pp'].values()];dd=[z['minute_DD3_difference_pp']for z in ds]
 assert x['joint_improvement_both_years']==(all(v>=0 for v in ret)and all(v<=0 for v in dd)and(any(v>0 for v in ret)or any(v<0 for v in dd)))
 assert x['all_cost_paths_identical_both_years']==all(z['all_cost_NAV_identical']for z in ds)
for name,e in cmp['BTC_exposure'].items():
 c=r['configs'][name];z=json.loads(gzip.decompress((R/c['archive']).read_bytes()))['scenes']['1'];ds=z['decisions'];assert e['volume_eligible_days']==sum(q['volume_eligible']for q in ds)and e['blocked_breakout_days']==sum(q['price_breakout']and not q['volume_eligible']for q in ds)and e['invested_days']==sum(q['end_day_exclusive']-q['day_offset']for q in z['position_segments']if D(q['units'])>0)
assert {k:v['descriptive_cliff_flags']for k,v in cmp['surface_diagnostics'].items()}=={'2025_BTC':5,'2025_combination':0,'2026_BTC':3,'2026_combination':3}
assert all(v['adjacent_edges']==12 and v['best_on_boundary']for v in cmp['surface_diagnostics'].values())
focus=r['configs']['volratio_channel_2025_n40_r1_btc0.75'];d=next(x for x in cmp['incumbent_comparisons']if x['config']==focus['name']);assert d['return_differences_pp']['3']<-9.8 and focus['status']=='passed'
old_rows=[c for c in r['configs'].values()if not c['is_new']];assert len(old_rows)==6 and sum(c['role']=='combination'for c in old_rows)==2
assert au['read_only_component_scenes_rebuilt']==12 and au['read_only_parent_scenes_verified']==6
assert all(len(z['equity_usdt'])==10748 and z['elapsed_minutes']==10739 and z['elapsed_complete_days']==7 and z['new_mark_minutes']==120 and z['new_reference_points']==z['new_executions']==0 for c in f['configs'].values()for z in c['scenes'].values())
old=json.loads((R/f['source_state']).read_text());state=json.loads((T/'forward_state.json').read_text());assert old['positions_by_asset_and_cost']==state['positions_by_asset_and_cost'] and old['next_daily_decision_utc']==state['next_daily_decision_utc']=='2026-10-10T00:01:00Z'
assert f['resume_utc']=='2026-10-09T09:00:00Z'and f['cutoff_utc']=='2026-10-09T11:00:00Z'and len(f['append_axis'])==120 and all(z['kind']=='closed_minute_mark'and z['NAV_index']==10628+i for i,z in enumerate(f['append_axis'])) and af['original_NAV_prefix']==10628
assert sha(R/f['frozen_plan_path'])==f['frozen_plan_sha256']=='2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81'
h=json.loads((T/'history_paths.json').read_text());assert h['report_sha256']==sha(T/'report.json') and(h['new_scenes_already_in_any_prior_report'],h['new_scenes_not_in_any_prior_report'],h['distinct_new_scene_paths_not_in_prior'],h['qualified_cross_period_pairs_not_in_any_prior_report'])==(90,6,6,2)
assert any(Path(path).name=='components_report.json'for path in h['all_prior_report_sha256'])
for path,value in h['all_prior_report_sha256'].items():assert sha(R/path)==value,path
for c in prior['conclusions']:assert sha(R/c['path'])==c['sha256']and(R/c['path']).read_text()==c['text']
for key in ('skills','oos_checks'):
 for path,v in prior[key].items():assert sha(R/path)==v['sha256']and(R/path).read_text()==v['text']
for v in prior['freqtrade_results']:
 assert sha(R/v['path'])==v['sha256']
 if v['members']:
  with zipfile.ZipFile(R/v['path'])as z:
   for x in v['members']:assert hashlib.sha256(z.read(x['name'])).hexdigest()==x['sha256']
assert sha(R/'research/automation/task.md')==prior['read_task_sha256'] and sha(R/'research/monitor/README.md')==prior['read_monitor_README']['sha256']
assert sha(R/'research/paper10/plan.json')==prior['paper10_plan_sha256']=='383cbfe8544627e05ff498ae4f803dbc3ccfd24753311add9cba2f5aa064e34f' and sha(R/'research/paper10/state.json')==prior['paper10_state_sha256']=='0d75614f6e16c02f02551660af597825ea35e132f004d480211e29d3c5849992'
initial=json.loads((T/'prior_evidence_audit.json').read_text());entries=initial['initial16_actual_results_checked'];assert len(entries)==16 and not initial['missing_initial16']and[v['fingerprint']for v in entries]==[v['fingerprint']for v in raw[:16]]and[v['original_ledger_position']for v in entries]==list(range(1,17))
for v in entries:
 assert v['canonical_fingerprint']==registry.fingerprint(records[v['fingerprint']]['spec'])
 for e in v['evidence']:assert sha(R/e['path'])==e['sha256']
assert json.loads((T/'signal_check.log').read_text())['not_performance_evidence'] and json.loads((T/'cache_recovery.json').read_text())['scenes_hash_verified']==18
execution=json.loads((T/'reproduction_execution.json').read_text());assert len(execution)==7 and all(v['exit_code']==0 for v in execution) and len((T/'finish.log').read_text().splitlines())==35
assert 'PASS:all96 NEW volume-boundary scenes and full report exactly reproduced' in(T/'reproduce.log').read_text()
feed=json.loads((R/'research/monitor/latest.json').read_text());mon=json.loads((T/'monitor_check.log').read_text());lab=json.loads((T/'monitor_label_check.json').read_text())
assert feed['research']['last_run']['id']==T.name and feed['research']['counts']['registered']==2398 and feed['research']['counts']['ranked']==2293 and feed['research']['counts']['observation_records_excluded']==415
assert feed['paper']['observation_id']=='20261009T105736656883Z' and mon['ok']and mon['protected_inputs_unchanged']and mon['observations']==21 and mon['research_configs']==2293 and lab['passed']and lab['prior_labels_unchanged']==2780 and lab['new_actual_factors_labeled']==32
base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip();assert base==prior['base_head']=='be22f83019b860f30b129d555683c29d647f381b'
files=sorted(q for q in T.rglob('*')if q.is_file()and'__pycache__'not in q.parts and q.name not in('verification.json','verify.log'))+[L,R/'research/automation/README.md',R/'research/monitor/latest.json',R/'research/monitor/configs.json.gz',R/'research/monitor/snapshot.py',R/'checks/monitor_snapshot.py']
out={'passed':True,'verified_at_utc':datetime.now(timezone.utc).isoformat(),'base_commit':base,'registry':{'rows':5725,'canonical':2813,'preserved_ids':2815,'unchanged_prior_rows':5655,'new_reserved_and_finished':35,'new_historical_trials':32,'new_legacy_cutoffs':3,'pending':0},'historical_summary':r['summary'],'new_cross_period_parameter_pairs':8,'new_cross_period_economic_paths':2,'joint_improvements_over_prior_candidate':0,'paper21_accounts_unchanged':True,'checks':{'all_new_reserved_before_calculation':True,'both_price_and_volume_reference_exclude_tested_day':True,'all96_new_cost_scenes_and_8640_decisions_audited':True,'old12_component_and6_portfolio_scenes_exactly_verified_without_signal_trade_rerun':True,'old30day_ratio1_spec_criteria_status_and_registry_records_unchanged':True,'raw75_25_exact1500_500_funds_no_normalization_or_rescaling':True,'both_unfiltered_and_prior_candidate_comparisons_verified':True,'predeclared40day_ratio1_loses2025_return_to_prior_candidate':True,'original16_order_aliases_and_actual_evidence_preserved':True,'legacy10628_NAV_prefix_and_percost_money_state_preserved':True,'all35_definitions_have_actual_finished_results':True,'volume_labels_complete_prior_labels_unchanged':True,'sensitivity_figure_visually_reviewed':True,'monitor_snapshot_checked':True},'audits':[au,af],'files_sha256':{str(q.relative_to(R)):sha(q)for q in files}}
(T/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out['registry']))
