"""Final read-only proof for new dual-window parents and unchanged prior sources/accounts."""
from pathlib import Path
from datetime import datetime,timezone
import csv,gzip,hashlib,json,subprocess,sys,zipfile
T=Path(__file__).resolve().parent;R=T.parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sys.path.insert(0,str(R/'research/automation'));import registry
L=R/'research/automation/registry.jsonl';lines=L.read_bytes().splitlines(keepends=True);raw=[json.loads(x)for x in lines];records=registry.read_records(L)
prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));r=json.loads((T/'report.json').read_text());f=json.loads((T/'forward_report.json').read_text());cmp=json.loads((T/'comparison.json').read_text());h=json.loads((T/'history_paths.json').read_text())
assert prior['lines']==6049 and prior['canonical']==2975 and len(lines)==6079 and len(records)==2992 and len({registry.fingerprint(v['spec'])for v in records.values()})==2990
assert hashlib.sha256(b''.join(lines[:prior['lines']])).hexdigest()==prior['ledger_sha256']
for fp,v in prior['records'].items():assert records[fp]==v,fp
assert not [v for v in records.values()if v['status']=='reserved']
hist=json.loads((T/'batch.json').read_text());forward=json.loads((T/'forward_batch.json').read_text());grid=json.loads((T/'grid_batch.json').read_text());assert len(hist)==12 and len(forward)==3 and len(grid)==18
for batch,report,file in [(hist,r,'report.json'),(forward,f,'forward_report.json')]:
 for b in batch:
  sp=json.loads((R/b['spec']).read_text());fp=registry.fingerprint(sp);assert fp==b['fingerprint']and fp not in prior['records']
  ev=[x for x in raw[prior['lines']:]if x['fingerprint']==fp];assert len(ev)==2 and ev[0]['status']=='reserved'and ev[1]['status']==report['configs'][b['name']]['status']and ev[1]['result_available']and ev[1]['report_sha256']==sha(T/file)
  start=report['evaluation_started_utc']if batch is hist else report['observation_started_utc'];assert ev[0]['recorded_at_utc']<start
assert len((T/'finish.log').read_text().splitlines())==15
audits=[json.loads((T/name).read_text())for name in('audit.log','audit_forward.log')];assert all(a['passed']for a in audits)
assert audits[0]['report_sha256']==sha(T/'report.json')and audits[0]['source_component_scenes_rebuilt']==36 and audits[0]['dual_volume_cost_scenes_audited']==54 and audits[0]['dual_volume_NAV_points_audited']==14006628
assert audits[1]['report_sha256']==sha(T/'forward_report.json')
summary=r['summary'];assert summary['new_configs']==12 and summary['new_cost_scenes']==36 and summary['new_minute_NAV_points']==9337752 and summary['reused_grid_configs']==6 and summary['reused_cost_scenes']==18 and summary['new_component_backtests']==summary['new_live_orders']==0
assert summary['positive_1x']==summary['positive_3x']==12 and len(summary['passed'])==12 and not summary['rejected']and len(summary['new_both_periods_passed_combination_pairs'])==6
for path,expected in r['source_hashes'].items():assert sha(R/path)==expected,path
for path,expected in r['plan']['reused_code_sha256'].items():assert sha(R/path)==expected,path
assert len(r['component_sources'])==12
for fp,ref in r['component_sources'].items():
 for name,hkey in [('report','report_sha256'),('archive','archive_sha256'),('spec','spec_sha256')]:assert sha(R/ref[name])==ref[hkey]
 sp=json.loads((R/ref['spec']).read_text());assert registry.fingerprint(sp)==fp and records[fp]==prior['records'][fp]
 assert sp['family']=='daily-close-range-relative-quote-volume'and sp['parameters']['initial_capital_usdt']==(1500 if ref['asset']=='BTC'else 500)
for b in grid:
 c=r['configs'][b['name']];sp=json.loads((R/b['spec']).read_text());assert registry.fingerprint(sp)==b['fingerprint']and sp['parameters']['initial_capital_usdt']==2000 and [q['weight']for q in sp['components']]==[.75,.25]
 assert c['BTC_volume_lookback_days']in(20,30,40)and c['ETH_volume_lookback_days']in(15,20,25)
 btc,eth=[records[q['fingerprint']]['spec']for q in sp['components']]
 assert btc['universe']==['BTC/USDT']and btc['parameters']['initial_capital_usdt']==1500 and btc['parameters']['minimum_volume_ratio']==1 and btc['parameters']['volume_lookback_days']==c['BTC_volume_lookback_days']
 assert eth['universe']==['ETH/USDT']and eth['parameters']['initial_capital_usdt']==500 and eth['parameters']['minimum_volume_ratio']==.875 and eth['parameters']['volume_lookback_days']==c['ETH_volume_lookback_days']
 if b['is_new']:assert c['BTC_volume_lookback_days']in(20,40)and c['status']=='passed'and all(c['criteria'].values())
 else:
  assert c['BTC_volume_lookback_days']==30;ref=b['source_ref'];old=json.loads((R/ref['report']).read_text())['configs'][b['name']]
  assert c['scenes']==old['scenes']and c['criteria']==old['criteria']and c['status']==old['status']and records[b['fingerprint']]==prior['records'][b['fingerprint']]
assert sum(not b['is_new']for b in grid)==6
assert len(cmp['matched_comparisons'])==18 and cmp['report_sha256']==sha(T/'report.json')
for row in cmp['matched_comparisons']:
 c=r['configs'][row['config']];o=r['read_only_comparators'][row['comparator']];old=json.loads((R/o['source_report']).read_text())['configs'][row['comparator']]
 assert o['kind']=='MATCHED_BTC30_SAME_ETH'and o['ETH_volume_lookback_days']==c['ETH_volume_lookback_days']and o['scenes']==old['scenes']and o['status']==old['status']and sha(R/o['source_report'])==o['source_report_sha256']
 assert row['return_differences_pp']=={k:c['scenes'][k]['net_return_pct']-o['scenes'][k]['net_return_pct']for k in('1','2','3')}
 assert row['minute_DD3_difference_pp']==c['scenes']['3']['max_drawdown_pct']-o['scenes']['3']['max_drawdown_pct']
 assert row['all_cost_NAV_identical']==all(c['scenes'][k]['NAV_sha256_f64le']==o['scenes'][k]['NAV_sha256_f64le']for k in('1','2','3'))
 if c['is_new']and c['year']=='2025':assert all(v<0 for v in row['return_differences_pp'].values())and row['minute_DD3_difference_pp']>0
 if c['year']=='2026':assert row['all_cost_NAV_identical']
for pair in cmp['qualified_pairs_vs_matched_controls']:
 xs=[next(x for x in cmp['matched_comparisons']if x['config']==name)for name in pair['pair']];ret=[v for x in xs for v in x['return_differences_pp'].values()];dd=[x['minute_DD3_difference_pp']for x in xs]
 assert pair['joint_improvement_both_years']==(all(v>=0 for v in ret)and all(v<=0 for v in dd)and(any(v>0 for v in ret)or any(v<0 for v in dd)))
assert cmp['new_pairs_jointly_improve_same_ETH_BTC30_controls']==0 and cmp['failure_counts']=={}
assert cmp['source_component_path_signature_counts']=={'2025_BTC':2,'2025_ETH':2,'2026_BTC':1,'2026_ETH':1}
assert cmp['surface_diagnostics']['2025']['descriptive_cliff_flags']==6 and cmp['surface_diagnostics']['2026']['descriptive_cliff_flags']==0 and cmp['surface_diagnostics']['2026']['whole_cost_path_signature_count']==1
assert h['report_sha256']==sha(T/'report.json')and (h['new_scenes_already_in_any_prior_report'],h['new_scenes_not_in_any_prior_report'],h['distinct_new_scene_paths_not_in_prior'],h['new_2026_combo_3x_paths_not_in_any_prior_report'],h['qualified_cross_period_pairs_not_in_any_prior_report'])==(24,12,3,0,1)
for path,expected in h['all_prior_report_sha256'].items():assert sha(R/path)==expected,path
with(T/'folds.csv').open()as source:folds=list(csv.DictReader(source))
assert len(folds)==324 and sum(row['is_new']=='True'for row in folds)==216
for row in folds:
 z=r['configs'][row['config']]['scenes'][row['cost']]['folds'][int(row['fold'])-1]
 for name,key in [('net_return_pct','net_return_pct'),('minute_DD_pct','max_drawdown_pct'),('Sharpe365','sharpe_365'),('Calmar','calmar')]:assert row[name]==(''if z[key]is None else str(z[key]))
with(T/'sensitivity.csv').open()as source:assert len(list(csv.DictReader(source)))==54
fr=r['plan']['forward_resume'];assert f['resume_utc']=='2026-10-09T19:00:00Z'and f['cutoff_utc']=='2026-10-09T21:00:00Z'and fr['prior_NAV_points']==11228 and fr['total_NAV_points']==11348 and fr['cumulative_minutes']==11339
assert audits[1]['original_NAV_prefix']==11228 and audits[1]['new_daily_decisions']==audits[1]['new_reference_points']==audits[1]['new_executions']==0
assert sha(R/f['frozen_plan_path'])==f['frozen_plan_sha256']=='2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81'
oldstate=json.loads((R/f['source_state']).read_text());state=json.loads((T/'forward_state.json').read_text());assert state['positions_by_asset_and_cost']==oldstate['positions_by_asset_and_cost']and state['next_daily_decision_utc']=='2026-10-10T00:01:00Z'
replay=json.loads((T/'reproduction_execution.json').read_text());execution=json.loads((T/'execution_steps.json').read_text());checks=json.loads((T/'final_checks.json').read_text());assert len(replay)==len(execution)==6 and len(checks)==3 and all(x['exit_code']==0 for x in replay+execution+checks)
assert 'PASS:all36 NEW dual-volume-window cost scenes exactly reproduced' in (T/'reproduce.log').read_text()
cache=json.loads((T/'cache_recovery.json').read_text());assert cache['new_backtests']==0 and cache['source_components']==12 and cache['component_scenes']==36 and cache['existing_combination_scenes']==18 and cache['scenes_hash_verified']==54
for item in prior['conclusions']:assert sha(R/item['path'])==item['sha256']and (R/item['path']).read_text()==item['text']
for category in ('skills','oos_checks'):
 for path,v in prior[category].items():assert sha(R/path)==v['sha256']and (R/path).read_text()==v['text']
for item in prior['freqtrade_results']:
 assert sha(R/item['path'])==item['sha256']
 if item['members']:
  with zipfile.ZipFile(R/item['path'])as z:
   for member in item['members']:assert hashlib.sha256(z.read(member['name'])).hexdigest()==member['sha256']
assert sha(R/'research/automation/task.md')==prior['read_task_sha256']and sha(R/'research/monitor/README.md')==prior['read_monitor_README']['sha256']
marker='## 最近完成的轮次\n\n';entry=(T/'README_entry.md').read_text()+'\n';assert (R/'research/automation/README.md').read_text()==prior['read_automation_README']['text'].replace(marker,marker+entry,1)
assert sha(R/'research/paper10/plan.json')==prior['paper10_plan_sha256']and sha(R/'research/paper10/state.json')==prior['paper10_state_sha256']
paper=json.loads((R/'research/paper10/state.json').read_text());assert paper['observations']==26 and paper['last_observation_id']=='20261009T205850547755Z'
P=R/'research/paper10/observations'/paper['last_observation_id'];paperpre=json.loads((P/'preflight.json').read_text())
for path,expected in paperpre['protected_sha256'].items():assert sha(R/path)==expected,path
assert sha(P/'state_after.json')==sha(R/'research/paper10/state.json')and json.loads((P/'complete.json').read_text())['report_sha256']==sha(P/'report.json')
initial=json.loads((T/'prior_evidence_audit.json').read_text());assert initial['missing_initial16']==[]and [v['fingerprint']for v in initial['initial16_actual_results_checked']]==[x['fingerprint']for x in raw[:16]]
for item in initial['initial16_actual_results_checked']:
 for ev in item['evidence']:assert sha(R/ev['path'])==ev['sha256']
feed=json.loads((R/'research/monitor/latest.json').read_text());monitor=json.loads((T/'monitor_check.log').read_text())
assert feed['research']['last_run']['id']==T.name and feed['research']['counts']=={'registered':2510,'results':2510,'passed':1373,'rejected':1132,'blocked':0,'legacy_tested':5,'ranked':2405,'unranked':105,'observation_records_excluded':480,'canonical_aliases_merged':2}
assert feed['paper']['observation_id']==paper['last_observation_id']and monitor['ok']and monitor['protected_inputs_unchanged']and monitor['observations']==26 and monitor['paper_accounts']==10 and monitor['research_configs']==2405
base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip();assert base==prior['base_head']=='4b6527bad86bf7362fad8cc0da839a413f011cf5'
protected={**paperpre['protected_sha256'],**{str(p.relative_to(R)):sha(p)for p in P.rglob('*')if p.is_file()and'__pycache__'not in p.parts},'research/paper10/state.json':sha(R/'research/paper10/state.json')}
files=sorted(p for p in T.rglob('*')if p.is_file()and'__pycache__'not in p.parts and p.name not in('verification.json','verify.log'))+[L,R/'research/automation/README.md',R/'research/monitor/latest.json',R/'research/monitor/configs.json.gz']
proof={'passed':True,'verified_at_utc':datetime.now(timezone.utc).isoformat(),'base_commit':base,'registry':{'rows':6079,'canonical':2990,'preserved_ids':2992,'unchanged_prior_rows':6049,'new_reserved_and_finished':15,'new_historical_trials':12,'new_legacy_cutoffs':3,'pending':0},'historical_summary':summary,'new_cross_period_parameter_pairs':6,'new_cross_period_return_paths':1,'jointly_improved_both_period_pairs':0,'prior_BTC30_candidate_still_dominates_new_cells_in2025_with2026_whole_paths_equal':True,'paper10_accounts_unchanged':True,'sensitivity_plot_visually_reviewed':True,'checks':{'all6_replay_phases_exit_zero':True,'all6_actual_execution_phases_exit_zero':True,'all3_final_checks_exit_zero':True,'all36source_and54grid_scenes_independently_audited':True,'exact1500_500_funding_original75_25_verified':True,'all324folds_54sensitivity_rows_preserved':True,'all6_old_parents_criteria_status_preserved':True,'all12_source_components_and_prior_ledger_unchanged':True,'matching_same_ETH_BTC30_controls_verified':True,'2026_whole_cost_paths_flat_verified':True,'whole_path_novelty_and_reused_history_disclosed':True,'initial16_actual_results_checked':True,'original_shadow_prefix_positions_costs_unchanged':True,'paper26_plan_accounts_and_journals_preserved':True,'monitor_snapshot_current_and_checked':True},'audits':audits,'protected_sha256':protected,'files_sha256':{str(p.relative_to(R)):sha(p)for p in files}}
(T/'verification.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'passed':True,**proof['registry'],'files_hashed':len(files),'protected_files':len(protected),'paper_observations':26,'new_cross_period_paths':1,'joint_both_year_improvements':0}))
