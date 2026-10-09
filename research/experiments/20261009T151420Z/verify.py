"""Read-only final evidence verification;never evaluate a new signal or mutate accounts."""
from pathlib import Path
from datetime import datetime,timezone
import csv,gzip,hashlib,json,subprocess,sys,zipfile
T=Path(__file__).resolve().parent;R=T.parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sys.path.insert(0,str(R/'research/automation'));import registry
L=R/'research/automation/registry.jsonl';lines=L.read_bytes().splitlines(keepends=True);raw=[json.loads(x)for x in lines];records=registry.read_records(L)
prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));r=json.loads((T/'report.json').read_text());f=json.loads((T/'forward_report.json').read_text());cmp=json.loads((T/'comparison.json').read_text());h=json.loads((T/'history_paths.json').read_text())
assert hashlib.sha256(b''.join(lines[:prior['lines']])).hexdigest()==prior['ledger_sha256']
assert prior['lines']==5807 and len(lines)==5849 and len(records)==2877 and len({registry.fingerprint(v['spec'])for v in records.values()})==2875
for fp,v in prior['records'].items():assert records[fp]==v,fp
assert not [v for v in records.values()if v['status']=='reserved']
hist=json.loads((T/'batch.json').read_text());forward=json.loads((T/'forward_batch.json').read_text());assert len(hist)==18 and len(forward)==3
for batch,report,file in [(hist,r,'report.json'),(forward,f,'forward_report.json')]:
 for b in batch:
  sp=json.loads((R/b['spec']).read_text());fp=registry.fingerprint(sp);assert fp==b['fingerprint'] and fp not in prior['records']
  events=[x for x in raw[prior['lines']:]if x['fingerprint']==fp];assert len(events)==2 and events[0]['status']=='reserved'
  assert events[1]['status']==report['configs'][b['name']]['status'] and events[1]['result_available'] and events[1]['report_sha256']==sha(T/file)
  started=report['evaluation_started_utc']if batch is hist else report['observation_started_utc'];assert events[0]['recorded_at_utc']<started
assert len((T/'finish.log').read_text().splitlines())==21
audits=[json.loads((T/n).read_text())for n in ('audit.log','audit_forward.log')]
assert all(a['passed']for a in audits) and audits[0]['report_sha256']==sha(T/'report.json') and audits[1]['report_sha256']==sha(T/'forward_report.json')
assert audits[0]['source_component_scenes_rebuilt']==36 and audits[0]['volume_EMA_cost_scenes_audited']==54 and audits[0]['volume_EMA_NAV_points_audited']==14006628
assert r['summary']['new_configs']==18 and r['summary']['new_cost_scenes']==54 and r['summary']['new_component_backtests']==0 and r['summary']['new_live_orders']==0
assert len(r['summary']['passed'])==18 and not r['summary']['rejected'] and len(r['summary']['new_both_periods_passed_combination_pairs'])==9
for path,expected in r['source_hashes'].items():assert sha(R/path)==expected,path
for path,expected in r['plan']['reused_code_sha256'].items():assert sha(R/path)==expected,path
for b in hist:
 c=r['configs'][b['name']];sp=json.loads((R/b['spec']).read_text());assert sp['parameters']['initial_capital_usdt']==2000 and [x['weight']for x in sp['components']]==[.75,.25] and c['raw_weights']==[.75,.25]
 assert [ref['capital_usdt']for ref in b['component_refs']]==[1500,500] and all(c['criteria'].values())
 assert c['BTC_volume_lookback_days']in(20,30,40) and c['ETH_EMA_span_days']in(50,65,80)
for ref in r['component_sources'].values():
 for name,hkey in [('report','report_sha256'),('archive','archive_sha256'),('spec','spec_sha256')]:assert sha(R/ref[name])==ref[hkey]
 fp=ref['fingerprint'];assert records[fp]==prior['records'][fp]
 for y in r['plan']['periods'].values():
  for v in y['normalized_data'].values():assert sha(R/v['path'])==v['sha256']
assert len(cmp['matched_comparisons'])==36 and cmp['report_sha256']==sha(T/'report.json')
for row in cmp['matched_comparisons']:
 c=r['configs'][row['config']];o=r['read_only_comparators'][row['comparator']];original=json.loads((R/o['source_report']).read_text())['configs'][row['comparator']]
 assert row['return_differences_pp']=={k:c['scenes'][k]['net_return_pct']-o['scenes'][k]['net_return_pct']for k in ('1','2','3')}
 assert row['minute_DD3_difference_pp']==c['scenes']['3']['max_drawdown_pct']-o['scenes']['3']['max_drawdown_pct']
 assert row['all_cost_NAV_identical']==all(c['scenes'][k]['NAV_sha256_f64le']==o['scenes'][k]['NAV_sha256_f64le']for k in ('1','2','3'))
 assert o['scenes']==original['scenes'] and o['status']==original['status'] and sha(R/o['source_report'])==o['source_report_sha256']
for p in cmp['qualified_pairs_vs_matched_controls']:
 for kind,got in p['by_control_kind'].items():
  xs=[next(x for x in cmp['matched_comparisons']if x['config']==n and x['control_kind']==kind)for n in p['pair']];ret=[v for x in xs for v in x['return_differences_pp'].values()];dd=[x['minute_DD3_difference_pp']for x in xs]
  assert got['all_returns_nonworse_both_years']==all(v>=0 for v in ret) and got['DD3_nonworse_both_years']==all(v<=0 for v in dd)
  assert got['joint_improvement_both_years']==(all(v>=0 for v in ret)and all(v<=0 for v in dd)and(any(v>0 for v in ret)or any(v<0 for v in dd)))
 assert p['jointly_improves_both_controls_in_both_years']==all(v['joint_improvement_both_years']for v in p['by_control_kind'].values())
assert cmp['new_qualified_pairs_jointly_improve_both_controls']==0
assert cmp['source_component_path_signature_counts']=={'2025_BTC':2,'2025_ETH':3,'2026_BTC':1,'2026_ETH':3}
assert {y:v['descriptive_cliff_flags']for y,v in cmp['surface_diagnostics'].items()}=={'2025':6,'2026':3}
assert h['report_sha256']==sha(T/'report.json') and (h['new_scenes_already_in_any_prior_report'],h['new_scenes_not_in_any_prior_report'],h['new_2026_combo_3x_paths_not_in_any_prior_report'],h['qualified_cross_period_pairs_not_in_any_prior_report'])==(27,27,0,6)
for p,expected in h['all_prior_report_sha256'].items():assert sha(R/p)==expected,p
with (T/'folds.csv').open()as source:folds=list(csv.DictReader(source))
assert len(folds)==324
for row in folds:
 z=r['configs'][row['config']]['scenes'][row['cost']]['folds'][int(row['fold'])-1]
 for field,source in [('net_return_pct','net_return_pct'),('minute_DD_pct','max_drawdown_pct'),('daily_DD_pct','daily_mark_drawdown_pct'),('Sharpe365','sharpe_365'),('Calmar','calmar')]:assert row[field]==(''if z[source]is None else str(z[source]))
with (T/'sensitivity.csv').open()as source:assert len(list(csv.DictReader(source)))==54
fr=r['plan']['forward_resume'];assert f['resume_utc']=='2026-10-09T13:00:00Z' and f['cutoff_utc']=='2026-10-09T15:00:00Z'
assert fr['prior_NAV_points']==10868 and fr['total_NAV_points']==10988 and fr['cumulative_minutes']==10979
assert audits[1]['original_NAV_prefix']==10868 and audits[1]['new_executions']==audits[1]['new_daily_decisions']==audits[1]['new_reference_points']==0
assert sha(R/f['frozen_plan_path'])==f['frozen_plan_sha256']=='2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81'
oldstate=json.loads((R/f['source_state']).read_text());state=json.loads((T/'forward_state.json').read_text());assert oldstate['positions_by_asset_and_cost']==state['positions_by_asset_and_cost'] and state['next_daily_decision_utc']=='2026-10-10T00:01:00Z'
replay=json.loads((T/'reproduction_execution.json').read_text());execution=json.loads((T/'execution_steps.json').read_text());finalchecks=json.loads((T/'final_checks.json').read_text())
assert len(replay)==len(execution)==6 and len(finalchecks)==3 and all(x['exit_code']==0 for x in replay+execution+finalchecks)
assert 'PASS:all54 NEW volume-channel/EMA cost scenes exactly reproduced' in (T/'reproduce.log').read_text()
for p in prior['conclusions']:assert sha(R/p['path'])==p['sha256'] and (R/p['path']).read_text()==p['text']
for category in ('skills','oos_checks'):
 for p,v in prior[category].items():assert sha(R/p)==v['sha256'] and (R/p).read_text()==v['text']
for v in prior['freqtrade_results']:
 assert sha(R/v['path'])==v['sha256']
 if v['members']:
  with zipfile.ZipFile(R/v['path'])as z:
   for member in v['members']:assert hashlib.sha256(z.read(member['name'])).hexdigest()==member['sha256']
assert sha(R/'research/automation/task.md')==prior['read_task_sha256'] and sha(R/'research/monitor/README.md')==prior['read_monitor_README']['sha256']
entry=(T/'README_entry.md').read_text()+'\n';mark='## 最近完成的轮次\n\n';assert (R/'research/automation/README.md').read_text()==prior['read_automation_README']['text'].replace(mark,mark+entry,1)
assert sha(R/'research/paper10/plan.json')==prior['paper10_plan_sha256'] and sha(R/'research/paper10/state.json')==prior['paper10_state_sha256']
paper=json.loads((R/'research/paper10/state.json').read_text());assert paper['observations']==23 and paper['last_observation_id']=='20261009T145621565919Z'
P=R/'research/paper10/observations'/paper['last_observation_id'];paperpre=json.loads((P/'preflight.json').read_text())
for p,expected in paperpre['protected_sha256'].items():assert sha(R/p)==expected,p
assert sha(P/'state_after.json')==sha(R/'research/paper10/state.json') and json.loads((P/'complete.json').read_text())['report_sha256']==sha(P/'report.json')
initial=json.loads((T/'prior_evidence_audit.json').read_text());assert initial['missing_initial16']==[]
assert [v['fingerprint']for v in initial['initial16_actual_results_checked']]==[x['fingerprint']for x in raw[:16]]
for v in initial['initial16_actual_results_checked']:
 for ev in v['evidence']:assert sha(R/ev['path'])==ev['sha256']
feed=json.loads((R/'research/monitor/latest.json').read_text());monitor=json.loads((T/'monitor_check.log').read_text())
assert feed['research']['last_run']['id']==T.name and feed['research']['counts']=={'registered':2434,'results':2434,'passed':1313,'rejected':1116,'blocked':0,'legacy_tested':5,'ranked':2329,'unranked':105,'observation_records_excluded':441,'canonical_aliases_merged':2}
assert feed['paper']['observation_id']==paper['last_observation_id'] and monitor['ok'] and monitor['protected_inputs_unchanged'] and monitor['observations']==23 and monitor['paper_accounts']==10 and monitor['research_configs']==2329
base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip();assert base==prior['base_head']=='47af318ef1f7f0833f71751071b6fe961a6eec30'
files=sorted(p for p in T.rglob('*')if p.is_file()and'__pycache__'not in p.parts and p.name not in('verification.json','verify.log'))+[L,R/'research/automation/README.md',R/'research/monitor/latest.json',R/'research/monitor/configs.json.gz']
protected={**paperpre['protected_sha256'],**{str(p.relative_to(R)):sha(p)for p in P.rglob('*')if p.is_file()and'__pycache__'not in p.parts},'research/paper10/state.json':sha(R/'research/paper10/state.json')}
proof={'passed':True,'verified_at_utc':datetime.now(timezone.utc).isoformat(),'base_commit':base,'registry':{'rows':5849,'canonical':2875,'preserved_ids':2877,'unchanged_prior_rows':5807,'new_reserved_and_finished':21,'new_historical_trials':18,'new_legacy_cutoffs':3,'pending':0},'historical_summary':r['summary'],'new_cross_period_parameter_pairs':9,'new_cross_period_return_paths':6,'both_control_joint_improvements':0,'paper10_accounts_unchanged':True,'plot_visually_reviewed':True,'checks':{'all6_replay_phases_exit_zero':True,'all6_actual_execution_phases_exit_zero':True,'all3_final_checks_exit_zero':True,'source_NAV_money_and_whole_drawdown_audited':True,'both_matched_control_axes_verified':True,'full324folds_and54sensitivity_rows_verified':True,'old_results_criteria_and_ledger_prefix_unchanged':True,'initial16_actual_results_checked':True,'whole_path_novelty_and_local_peak_disclosed':True,'original_shadow_prefix_positions_costs_verified':True,'paper23_plan_accounts_journals_preserved':True,'monitor_snapshot_current_and_checked':True},'audits':audits,'protected_sha256':protected,'files_sha256':{str(p.relative_to(R)):sha(p)for p in files}}
(T/'verification.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'passed':True,**proof['registry'],'files_hashed':len(files),'protected_files':len(protected),'paper_observations':23,'new_cross_period_paths':6,'both_control_joint_improvements':0}))
