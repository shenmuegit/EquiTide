"""Final read-only binding of actual ETH-volume trials,prior evidence,accounts and publication files."""
from pathlib import Path
from datetime import datetime,timezone
import csv,gzip,hashlib,json,subprocess,sys,zipfile
T=Path(__file__).resolve().parent;R=T.parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sys.path.insert(0,str(R/'research/automation'));import registry
L=R/'research/automation/registry.jsonl';lines=L.read_bytes().splitlines(keepends=True);raw=[json.loads(x)for x in lines];records=registry.read_records(L)
prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));r=json.loads((T/'report.json').read_text());f=json.loads((T/'forward_report.json').read_text());cmp=json.loads((T/'comparison.json').read_text());h=json.loads((T/'history_paths.json').read_text())
assert prior['lines']==5967 and prior['canonical']==2934 and len(lines)==6029 and len(records)==2967 and len({registry.fingerprint(v['spec'])for v in records.values()})==2965
assert hashlib.sha256(b''.join(lines[:prior['lines']])).hexdigest()==prior['ledger_sha256']
for fp,v in prior['records'].items():assert records[fp]==v,fp
assert not [v for v in records.values()if v['status']=='reserved']
hist=json.loads((T/'batch.json').read_text());forward=json.loads((T/'forward_batch.json').read_text());assert len(hist)==28 and len(forward)==3
for batch,report,file in [(hist,r,'report.json'),(forward,f,'forward_report.json')]:
 for b in batch:
  sp=json.loads((R/b['spec']).read_text());fp=registry.fingerprint(sp);assert fp==b['fingerprint'] and fp not in prior['records']
  ev=[x for x in raw[prior['lines']:]if x['fingerprint']==fp];assert len(ev)==2 and ev[0]['status']=='reserved' and ev[1]['status']==report['configs'][b['name']]['status']
  assert ev[1]['result_available'] and ev[1]['report_sha256']==sha(T/file)
  start=report['evaluation_started_utc']if batch is hist else report['observation_started_utc'];assert ev[0]['recorded_at_utc']<start
assert len((T/'finish.log').read_text().splitlines())==31
audits=[json.loads((T/name).read_text())for name in ('audit.log','audit_forward.log')];assert all(a['passed']for a in audits)
assert audits[0]['report_sha256']==sha(T/'report.json') and audits[0]['actual_scenes_audited']==84 and audits[0]['NAV_points_audited']==21788088 and audits[0]['Decimal_quote_volume_causal_decisions']==7560 and audits[0]['Decimal_fills_independently_checked']==180
assert audits[1]['report_sha256']==sha(T/'forward_report.json')
assert json.loads((T/'signal_check.log').read_text())['synthetic_fixture_checks']=='PASS'
summary=r['summary'];assert summary['new_configs']==28 and summary['new_component_configs']==summary['new_combination_configs']==14 and summary['new_cost_scenes']==84
assert summary['positive_1x']==summary['positive_3x']==28 and len(summary['passed'])==21 and len(summary['rejected'])==7 and len(summary['new_both_periods_passed_combination_pairs'])==7
assert summary['new_live_orders']==0 and summary['new_component_fills']==180 and summary['old_component_configs_read_only']==6 and summary['old_combination_configs_read_only']==4
for path,expected in r['source_hashes'].items():assert sha(R/path)==expected,path
for path,expected in r['plan']['reused_code_sha256'].items():assert sha(R/path)==expected,path
fixed={ref['year']:ref['fingerprint']for ref in r['plan']['read_only_component_refs']if ref['asset']=='BTC'};assert len(fixed)==2
for ref in r['plan']['read_only_component_refs']:
 assert ref['capital_usdt']==(1500 if ref['asset']=='BTC'else 500) and records[ref['fingerprint']]==prior['records'][ref['fingerprint']]
 for name,hkey in [('spec','spec_sha256'),('report','report_sha256'),('archive','archive_sha256')]:assert sha(R/ref[name])==ref[hkey]
 cfg=r['configs'][ref['name']];old=json.loads((R/ref['report']).read_text())['configs'][ref['name']]
 assert cfg['scenes']==old['scenes'] and cfg['status']==old['status'] and cfg['criteria']==old['criteria']
assert audits[0]['read_only_component_scenes']==18 and audits[0]['read_only_portfolio_scenes']==12
assert len(r['plan']['read_only_component_refs'])==6 and len(r['plan']['read_only_grid_refs'])==4
for ref in r['plan']['read_only_grid_refs']:
 for name,hkey in [('spec','spec_sha256'),('report','report_sha256'),('archive','archive_sha256')]:assert sha(R/ref[name])==ref[hkey]
 c=r['configs'][ref['name']];source=json.loads((R/ref['report']).read_text())['configs'][ref['name']];assert c['status']==source['status'] and c['criteria']==source['criteria'] and c['scenes']==source['scenes'] and records[ref['fingerprint']]==prior['records'][ref['fingerprint']]
assert len([c for c in r['configs'].values()if not c['is_new']])==10
for b in hist:
 c=r['configs'][b['name']];sp=json.loads((R/b['spec']).read_text());assert c['volume_lookback_days']in(15,20,25)and c['minimum_volume_ratio']in(.75,.875,1)
 assert all(s['net_return_pct']>0 for s in c['scenes'].values())
 if c['role']=='component':
  assert c['asset']=='ETH' and c['capital_usdt']==sp['parameters']['initial_capital_usdt']==500 and sp['universe']==['ETH/USDT']
  assert sp['parameters']['entry_lookback_days']==15 and sp['parameters']['exit_lookback_days']==30 and 'same500USDT' in sp['logic']['sizing']
  assert c['status']==('rejected'if c['year']=='2026'else'passed')
  if c['year']=='2026':assert c['failed_criteria']==['four_positive_1x_folds'] and c['positive_folds_1x']==3
 else:
  assert sp['parameters']['initial_capital_usdt']==2000 and [q['weight']for q in sp['components']]==[.75,.25] and sp['components'][0]['fingerprint']==fixed[c['year']] and c['status']=='passed'
  child=records[sp['components'][1]['fingerprint']]['spec'];assert child['universe']==['ETH/USDT'] and child['parameters']['initial_capital_usdt']==500
  assert child['parameters']['volume_lookback_days']==c['volume_lookback_days'] and child['parameters']['minimum_volume_ratio']==c['minimum_volume_ratio']
assert len(cmp['matched_comparisons'])==18 and cmp['report_sha256']==sha(T/'report.json')
for row in cmp['matched_comparisons']:
 c=r['configs'][row['config']];o=r['read_only_comparators'][row['comparator']];old=json.loads((R/o['source_report']).read_text())['configs'][row['comparator']]
 assert o['kind']=='MATCHED_UNFILTERED_ETH' and o['scenes']==old['scenes'] and o['status']==old['status'] and sha(R/o['source_report'])==o['source_report_sha256']
 assert row['return_differences_pp']=={k:c['scenes'][k]['net_return_pct']-o['scenes'][k]['net_return_pct']for k in ('1','2','3')}
 assert row['minute_DD3_difference_pp']==c['scenes']['3']['max_drawdown_pct']-o['scenes']['3']['max_drawdown_pct']
 assert row['all_cost_NAV_identical']==all(c['scenes'][k]['NAV_sha256_f64le']==o['scenes'][k]['NAV_sha256_f64le']for k in ('1','2','3'))
for pair in cmp['qualified_pairs_vs_matched_controls']:
 xs=[next(x for x in cmp['matched_comparisons']if x['config']==n)for n in pair['pair']];returns=[v for x in xs for v in x['return_differences_pp'].values()];dd=[x['minute_DD3_difference_pp']for x in xs]
 assert pair['joint_improvement_both_years']==(all(v>=0 for v in returns)and all(v<=0 for v in dd)and(any(v>0 for v in returns)or any(v<0 for v in dd)))
 assert pair['strict_return_gain_in_both_years']==all(any(v>0 for v in x['return_differences_pp'].values())for x in xs)
assert cmp['new_parameters_sharing_predeclared_focus_paired_path']==[[20,.875],[25,.75],[25,.875]]
for item in cmp['predeclared_focus_vs_old20_r1']:
 c=r['configs'][item['focus']];a=r['configs'][item['old_anchor']];assert not a['is_new'] and a['volume_lookback_days']==20 and a['minimum_volume_ratio']==1 and c['minimum_volume_ratio']==.875
 assert item['return_differences_pp']=={k:c['scenes'][k]['net_return_pct']-a['scenes'][k]['net_return_pct']for k in('1','2','3')}
 assert item['minute_DD3_difference_pp']==c['scenes']['3']['max_drawdown_pct']-a['scenes']['3']['max_drawdown_pct']
 assert sha(R/item['old_anchor_source_report'])==item['old_anchor_source_report_sha256']
 if item['year']=='2025':assert item['all_cost_NAV_identical'] and all(v==0 for v in item['return_differences_pp'].values())and item['minute_DD3_difference_pp']==0
 else:assert all(v>0 for v in item['return_differences_pp'].values())and item['minute_DD3_difference_pp']<0
assert cmp['new_qualified_pairs_jointly_nonworse_with_improvement']==cmp['new_qualified_pairs_strict_return_gain_in_both_years']==0
assert cmp['failure_counts']=={'four_positive_1x_folds':7} and cmp['path_signature_counts']=={'2025_ETH':2,'2026_ETH':2,'2025_BTC':1,'2026_BTC':1,'2025_combination':2,'2026_combination':2}
assert all(d['descriptive_cliff_flags']==(4 if k.startswith('2025')else 3)and d['adjacent_edges']==12 and d['positive3_fraction']==1 for k,d in cmp['surface_diagnostics'].items())
assert h['report_sha256']==sha(T/'report.json') and (h['new_scenes_already_in_any_prior_report'],h['new_scenes_not_in_any_prior_report'],h['distinct_new_scene_paths_not_in_prior'],h['new_2026_combo_3x_paths_not_in_any_prior_report'],h['qualified_cross_period_pairs_not_in_any_prior_report'])==(84,0,0,0,1)
for path,expected in h['all_prior_report_sha256'].items():assert sha(R/path)==expected,path
with (T/'folds.csv').open()as source:folds=list(csv.DictReader(source))
assert len(folds)==684 and sum(row['is_new']=='True'for row in folds)==504
for row in folds:
 z=r['configs'][row['config']]['scenes'][row['cost']]['folds'][int(row['fold'])-1]
 for name,key in [('net_return_pct','net_return_pct'),('minute_DD_pct','max_drawdown_pct'),('Sharpe365','sharpe_365'),('Calmar','calmar')]:assert row[name]==(''if z[key]is None else str(z[key]))
with (T/'sensitivity.csv').open()as source:assert len(list(csv.DictReader(source)))==114
fr=r['plan']['forward_resume'];assert f['resume_utc']=='2026-10-09T17:00:00Z' and f['cutoff_utc']=='2026-10-09T19:00:00Z'
assert fr['prior_NAV_points']==11108 and fr['total_NAV_points']==11228 and fr['cumulative_minutes']==11219
assert audits[1]['original_NAV_prefix']==11108 and audits[1]['new_daily_decisions']==audits[1]['new_reference_points']==audits[1]['new_executions']==0
assert sha(R/f['frozen_plan_path'])==f['frozen_plan_sha256']=='2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81'
oldstate=json.loads((R/f['source_state']).read_text());state=json.loads((T/'forward_state.json').read_text());assert state['positions_by_asset_and_cost']==oldstate['positions_by_asset_and_cost'] and state['next_daily_decision_utc']=='2026-10-10T00:01:00Z'
replay=json.loads((T/'reproduction_execution.json').read_text());execution=json.loads((T/'execution_steps.json').read_text());checks=json.loads((T/'final_checks.json').read_text());assert len(replay)==7 and len(execution)==6 and len(checks)==3 and all(x['exit_code']==0 for x in replay+execution+checks)
assert 'PASS:all84 NEW ETHvolume-boundary scenes and full report exactly reproduced;30oldsource/portfolio scenes read-only verified' in (T/'reproduce.log').read_text()
for item in prior['conclusions']:assert sha(R/item['path'])==item['sha256'] and (R/item['path']).read_text()==item['text']
for category in ('skills','oos_checks'):
 for path,v in prior[category].items():assert sha(R/path)==v['sha256'] and (R/path).read_text()==v['text']
for item in prior['freqtrade_results']:
 assert sha(R/item['path'])==item['sha256']
 if item['members']:
  with zipfile.ZipFile(R/item['path'])as z:
   for member in item['members']:assert hashlib.sha256(z.read(member['name'])).hexdigest()==member['sha256']
assert sha(R/'research/automation/task.md')==prior['read_task_sha256'] and sha(R/'research/monitor/README.md')==prior['read_monitor_README']['sha256']
marker='## 最近完成的轮次\n\n';entry=(T/'README_entry.md').read_text()+'\n';assert (R/'research/automation/README.md').read_text()==prior['read_automation_README']['text'].replace(marker,marker+entry,1)
assert sha(R/'research/paper10/plan.json')==prior['paper10_plan_sha256'] and sha(R/'research/paper10/state.json')==prior['paper10_state_sha256']
paper=json.loads((R/'research/paper10/state.json').read_text());assert paper['observations']==25 and paper['last_observation_id']=='20261009T185751028739Z'
P=R/'research/paper10/observations'/paper['last_observation_id'];paperpre=json.loads((P/'preflight.json').read_text())
for path,expected in paperpre['protected_sha256'].items():assert sha(R/path)==expected,path
assert sha(P/'state_after.json')==sha(R/'research/paper10/state.json') and json.loads((P/'complete.json').read_text())['report_sha256']==sha(P/'report.json')
initial=json.loads((T/'prior_evidence_audit.json').read_text());assert initial['missing_initial16']==[] and [v['fingerprint']for v in initial['initial16_actual_results_checked']]==[x['fingerprint']for x in raw[:16]]
for item in initial['initial16_actual_results_checked']:
 for ev in item['evidence']:assert sha(R/ev['path'])==ev['sha256']
feed=json.loads((R/'research/monitor/latest.json').read_text());monitor=json.loads((T/'monitor_check.log').read_text())
assert feed['research']['last_run']['id']==T.name and feed['research']['counts']=={'registered':2498,'results':2498,'passed':1361,'rejected':1132,'blocked':0,'legacy_tested':5,'ranked':2393,'unranked':105,'observation_records_excluded':467,'canonical_aliases_merged':2}
assert feed['paper']['observation_id']==paper['last_observation_id'] and monitor['ok'] and monitor['protected_inputs_unchanged'] and monitor['observations']==25 and monitor['paper_accounts']==10 and monitor['research_configs']==2393
base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip();assert base==prior['base_head']=='c15a03661816e152b37590129b4e1eaf6aa2e0f1'
protected={**paperpre['protected_sha256'],**{str(p.relative_to(R)):sha(p)for p in P.rglob('*')if p.is_file()and'__pycache__'not in p.parts},'research/paper10/state.json':sha(R/'research/paper10/state.json')}
files=sorted(p for p in T.rglob('*')if p.is_file()and'__pycache__'not in p.parts and p.name not in('verification.json','verify.log'))+[L,R/'research/automation/README.md',R/'research/monitor/latest.json',R/'research/monitor/configs.json.gz']
proof={'passed':True,'verified_at_utc':datetime.now(timezone.utc).isoformat(),'base_commit':base,'registry':{'rows':6029,'canonical':2965,'preserved_ids':2967,'unchanged_prior_rows':5967,'new_reserved_and_finished':31,'new_historical_trials':28,'new_legacy_cutoffs':3,'pending':0},'historical_summary':summary,'new_cross_period_parameter_pairs':7,'new_cross_period_return_paths':1,'jointly_improved_both_period_pairs':0,'predeclared_focus_repairs_old20_r1_in2026_with2025_whole_paths_unchanged':True,'paper10_accounts_unchanged':True,'both_sensitivity_plots_visually_reviewed':True,'checks':{'all7_replay_phases_exit_zero':True,'all6_actual_execution_phases_exit_zero':True,'all3_final_checks_exit_zero':True,'all84new_and30old_scenes_independently_audited':True,'new_ETH_signals_and_money_causally_verified':True,'exact1500_500_funding_original75_25_verified':True,'all684folds_114sensitivity_rows_preserved':True,'new504_and_old180folds_separated':True,'all7_new_ETH_rejections_and8_old_grid_cells_retained':True,'prior_records_results_criteria_unchanged':True,'matching_same_BTC_control_verified':True,'whole_path_novelty_and_reused_history_disclosed':True,'initial16_actual_results_checked':True,'original_shadow_prefix_positions_costs_unchanged':True,'paper25_plan_accounts_and_journals_preserved':True,'monitor_snapshot_current_and_checked':True},'audits':audits,'protected_sha256':protected,'files_sha256':{str(p.relative_to(R)):sha(p)for p in files}}
(T/'verification.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'passed':True,**proof['registry'],'new_cross_period_paths':1,'joint_both_year_improvements':0,'files_hashed':len(files),'protected_files':len(protected),'paper_observations':25}))
