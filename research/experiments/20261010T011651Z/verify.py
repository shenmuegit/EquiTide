"""Read-only final evidence, temporal, registration and unchanged-account verification."""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import csv,gzip,hashlib,json,subprocess,sys,zipfile
T=Path(__file__).resolve().parent;R=T.parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sys.path.insert(0,str(R/'research/automation'));import registry
L=R/'research/automation/registry.jsonl';lines=L.read_bytes().splitlines(keepends=True);raw=[json.loads(x)for x in lines];records=registry.read_records(L)
prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));r=json.loads((T/'report.json').read_text());f=json.loads((T/'forward_report.json').read_text());cmp=json.loads((T/'comparison.json').read_text());h=json.loads((T/'history_paths.json').read_text())
hist=json.loads((T/'batch.json').read_text());forward=json.loads((T/'forward_batch.json').read_text());grid=json.loads((T/'grid_batch.json').read_text())
assert len(hist)==18 and grid==hist and len(forward)==3
assert prior['lines']==6149 and prior['canonical']==3025 and len(lines)==6191 and len(records)==3048 and len({registry.fingerprint(v['spec'])for v in records.values()})==3046
assert hashlib.sha256(b''.join(lines[:prior['lines']])).hexdigest()==prior['ledger_sha256']
for fp,v in prior['records'].items():assert records[fp]==v,fp
assert not[v for v in records.values()if v['status']=='reserved']
for batch,report,file in[(hist,r,'report.json'),(forward,f,'forward_report.json')]:
 for b in batch:
  sp=json.loads((R/b['spec']).read_text());fp=registry.fingerprint(sp);assert fp==b['fingerprint']and fp not in prior['records'];events=[x for x in raw[prior['lines']:]if x['fingerprint']==fp]
  assert len(events)==2 and events[0]['status']=='reserved'and events[1]['status']==report['configs'][b['name']]['status']and events[1]['result_available']and events[1]['report_sha256']==sha(T/file)
  started=report['evaluation_started_utc']if batch is hist else report['observation_started_utc'];assert events[0]['recorded_at_utc']<started
assert len((T/'finish.log').read_text().splitlines())==21
execution=json.loads((T/'execution_steps.json').read_text());replay=json.loads((T/'reproduction_execution.json').read_text());checks=json.loads((T/'final_checks.json').read_text());assert len(execution)==len(replay)==6 and len(checks)==3 and all(x['exit_code']==0 for x in execution+replay+checks)
audits=[json.loads((T/n).read_text())for n in('audit.log','audit_forward.log')];assert all(a['passed']for a in audits)
assert audits[0]['report_sha256']==sha(T/'report.json')and audits[0]['source_component_scenes_rebuilt']==36 and audits[0]['dual_volume_cost_scenes_audited']==54 and audits[0]['dual_volume_NAV_points_audited']==14006628
assert audits[1]['report_sha256']==sha(T/'forward_report.json')and audits[1]['original_daily_decisions_independently_checked']==6 and audits[1]['prior_NAV_prefix_preserved']==11468 and audits[1]['daily_reference_points_added']==1 and audits[1]['new_component_executions']==0
assert 'PASS:all54 NEW mixed-volume-EMA cost scenes exactly reproduced'in(T/'reproduce.log').read_text()
summary=r['summary'];assert summary['new_configs']==18 and summary['new_cost_scenes']==54 and summary['new_minute_NAV_points']==14006628 and summary['reused_grid_configs']==summary['reused_cost_scenes']==0 and summary['new_component_backtests']==summary['new_live_orders']==0
assert set(summary['passed'])=={n for n,c in r['configs'].items()if c['status']=='passed'}and set(summary['rejected'])=={n for n,c in r['configs'].items()if c['status']=='rejected'}
assert summary['positive_1x']==sum(c['scenes']['1']['net_return_pct']>0 for c in r['configs'].values())and summary['positive_3x']==sum(c['scenes']['3']['net_return_pct']>0 for c in r['configs'].values())
for mapping in(r['source_hashes'],r['plan']['reused_code_sha256']):
 for path,expected in mapping.items():assert sha(R/path)==expected,path
assert len(r['component_sources'])==12
for fp,ref in r['component_sources'].items():
 for n,hkey in [('report','report_sha256'),('archive','archive_sha256'),('spec','spec_sha256')]:assert sha(R/ref[n])==ref[hkey]
 assert registry.fingerprint(json.loads((R/ref['spec']).read_text()))==fp and records[fp]==prior['records'][fp]
for b in hist:
 c=r['configs'][b['name']];sp=json.loads((R/b['spec']).read_text());assert c['is_new']and registry.fingerprint(sp)==b['fingerprint']and sp['parameters']['initial_capital_usdt']==2000 and[c['weight']for c in sp['components']]==[.75,.25]
 btc,eth=[records[x['fingerprint']]['spec']for x in sp['components']];bp,ep=btc['parameters'],eth['parameters'];assert btc['family']=='daily-close-range-relative-quote-volume'and btc['universe']==['BTC/USDT']and bp['initial_capital_usdt']==1500 and bp['volume_lookback_days']==30 and bp['minimum_volume_ratio']==c['BTC_minimum_volume_ratio']in(.9,1,1.1)
 assert eth['family']=='daily-channel-ema-confirmation'and eth['universe']==['ETH/USDT']and ep['initial_capital_usdt']==500 and ep['EMA_span_days']==c['ETH_EMA_span_days']in(50,65,80)and ep['EMA_symmetric_band']==.015
 assert bp['entry_lookback_days']==ep['entry_lookback_days']==15 and bp['exit_lookback_days']==ep['exit_lookback_days']==30
 assert bp['start_utc']==ep['start_utc']==sp['parameters']['start_utc']==r['plan']['periods'][b['year']]['oos_start_utc']and bp['end_utc']==ep['end_utc']==sp['parameters']['end_utc']==r['plan']['periods'][b['year']]['terminal_exit_utc']
 assert len(c['criteria'])==8 and(c['status']=='passed')==all(c['criteria'].values())
assert len(cmp['matched_comparisons'])==18 and len(cmp['secondary_BTC1_same_EMA_span_comparisons'])==6 and cmp['report_sha256']==sha(T/'report.json')
for row in cmp['matched_comparisons']+cmp['secondary_BTC1_same_EMA_span_comparisons']:
 c=r['configs'][row['config']];o=r['read_only_comparators'][row['comparator']];old=json.loads((R/o['source_report']).read_text())['configs'][row['comparator']];assert o['scenes']==old['scenes']and o['status']==old['status']and sha(R/o['source_report'])==o['source_report_sha256']
 assert row['return_differences_pp']=={k:c['scenes'][k]['net_return_pct']-o['scenes'][k]['net_return_pct']for k in('1','2','3')}and row['minute_DD3_difference_pp']==c['scenes']['3']['max_drawdown_pct']-o['scenes']['3']['max_drawdown_pct']
 assert row['all_cost_NAV_identical']==all(c['scenes'][k]['NAV_sha256_f64le']==o['scenes'][k]['NAV_sha256_f64le']for k in('1','2','3'))
 if row['kind']=='MATCHED_BTC_VOLUME_PURE_ETH_CHANNEL':assert o['BTC_minimum_volume_ratio']==c['BTC_minimum_volume_ratio']
 else:assert row['kind']=='BTC_R1_PURE_ETH_EMA_SAME_SPAN'and c['BTC_minimum_volume_ratio']==1 and o['ETH_EMA_span_days']==c['ETH_EMA_span_days']
for pair in cmp['qualified_pairs_vs_matched_controls']:
 xs=[next(x for x in cmp['matched_comparisons']if x['config']==n)for n in pair['pair']];ret=[v for x in xs for v in x['return_differences_pp'].values()];dd=[x['minute_DD3_difference_pp']for x in xs]
 assert pair['joint_improvement_both_years']==(all(v>=0 for v in ret)and all(v<=0 for v in dd)and(any(v>0 for v in ret)or any(v<0 for v in dd)))
assert cmp['new_pairs_jointly_improve_same_BTC_pure_ETH_channel_controls']==sum(p['joint_improvement_both_years']for p in cmp['qualified_pairs_vs_matched_controls'])and cmp['source_component_path_signature_counts']==prior['existing_component_path_signature_counts']
assert cmp['failure_counts']==dict(Counter(k for c in r['configs'].values()for k in c['failed_criteria']))
for year in('2025','2026'):
 cells=[c for c in r['configs'].values()if c['year']==year];d=cmp['surface_diagnostics'][year];sens=r['sensitivity'][year+'_BTC_VOLUME_ETH_FILTERED_EMA'];assert len(cells)==9 and len(sens['adjacent_edges'])==12
 assert d['whole_cost_path_signature_count']==len({tuple(c['scenes'][k]['NAV_sha256_f64le']for k in('1','2','3'))for c in cells})and d['descriptive_cliff_flags']==sum(e['cliff_flag_2sd']for e in sens['adjacent_edges'])
assert h['report_sha256']==sha(T/'report.json')and h['new_scenes_already_in_any_prior_report']+h['new_scenes_not_in_any_prior_report']==54
for path,expected in h['all_prior_report_sha256'].items():assert sha(R/path)==expected,path
with(T/'folds.csv').open()as source:folds=list(csv.DictReader(source))
assert len(folds)==324 and all(row['is_new']=='True'for row in folds)
for row in folds:
 z=r['configs'][row['config']]['scenes'][row['cost']]['folds'][int(row['fold'])-1]
 for name,key in[('net_return_pct','net_return_pct'),('minute_DD_pct','max_drawdown_pct'),('Sharpe365','sharpe_365'),('Calmar','calmar')]:assert row[name]==(''if z[key]is None else str(z[key]))
with(T/'sensitivity.csv').open()as source:assert len(list(csv.DictReader(source)))==54
fr=r['plan']['forward_resume'];assert f['resume_utc']=='2026-10-09T23:00:00Z'and f['cutoff_utc']=='2026-10-10T01:00:00Z'and fr['prior_NAV_points']==11468 and fr['total_NAV_points']==11589 and fr['cumulative_minutes']==11579
assert sha(R/f['frozen_plan_path'])==f['frozen_plan_sha256']=='2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81'
oldstate=json.loads((R/f['source_state']).read_text());state=json.loads((T/'forward_state.json').read_text());assert state['positions_by_asset_and_cost']==oldstate['positions_by_asset_and_cost']and state['next_daily_decision_utc']=='2026-10-11T00:01:00Z'
for asset in('BTC','ETH'):assert f['daily_decisions_by_asset'][asset]['action']=='hold_long'
cache=json.loads((T/'cache_recovery.json').read_text());assert cache['new_backtests']==0 and cache['source_components']==12 and cache['component_scenes']==cache['scenes_hash_verified']==36 and cache['existing_combination_scenes']==0
for item in prior['conclusions']:assert sha(R/item['path'])==item['sha256']and(R/item['path']).read_text()==item['text']
for category in('skills','oos_checks'):
 for path,v in prior[category].items():assert sha(R/path)==v['sha256']and(R/path).read_text()==v['text']
for item in prior['freqtrade_results']:
 assert sha(R/item['path'])==item['sha256']
 if item['members']:
  with zipfile.ZipFile(R/item['path'])as z:
   for member in item['members']:assert hashlib.sha256(z.read(member['name'])).hexdigest()==member['sha256']
assert sha(R/'research/automation/task.md')==prior['read_task_sha256']and sha(R/'research/monitor/README.md')==prior['read_monitor_README']['sha256']
marker='## 最近完成的轮次\n\n';entry=(T/'README_entry.md').read_text()+'\n';assert(R/'research/automation/README.md').read_text()==prior['read_automation_README']['text'].replace(marker,marker+entry,1)
assert sha(R/'research/paper10/plan.json')==prior['paper10_plan_sha256']and sha(R/'research/paper10/state.json')==prior['paper10_state_sha256']=='8f886ba6a4958bd6c9e5d0defc6032229dd88beeab2681ae5cc9ea45c050c615'
paper=json.loads((R/'research/paper10/state.json').read_text());assert paper['observations']==28 and paper['last_observation_id']=='20261010T010108578337Z';P=R/'research/paper10/observations'/paper['last_observation_id'];paperpre=json.loads((P/'preflight.json').read_text())
for path,expected in paperpre['protected_sha256'].items():assert sha(R/path)==expected,path
assert sha(P/'state_after.json')==sha(R/'research/paper10/state.json')and json.loads((P/'complete.json').read_text())['report_sha256']==sha(P/'report.json')
initial=json.loads((T/'prior_evidence_audit.json').read_text());assert initial['missing_initial16']==[]and[x['fingerprint']for x in initial['initial16_actual_results_checked']]==[x['fingerprint']for x in raw[:16]]
for item in initial['initial16_actual_results_checked']:
 for ev in item['evidence']:assert sha(R/ev['path'])==ev['sha256']
recovery=json.loads((T/'engineering_recovery.json').read_text());assert recovery['frozen_plan_sha256_unchanged']==sha(T/'spec.json')and recovery['reserved_configs_at_failure']==recovery['actual_evaluations_at_failure']==0 and'family must be a stable lowercase ID'in(T/'prepare_failure_1.log').read_text()
feed=json.loads((R/'research/monitor/latest.json').read_text());monitor=json.loads((T/'monitor_check.log').read_text());expected=dict(prior['monitor_counts_before'])
for key,n in{'registered':18,'results':18,'passed':len(summary['passed']),'rejected':len(summary['rejected']),'ranked':18,'observation_records_excluded':3}.items():expected[key]+=n
assert feed['research']['last_run']['id']==T.name and feed['research']['counts']==expected and feed['paper']['observation_id']==paper['last_observation_id']
assert monitor['ok']and monitor['protected_inputs_unchanged']and monitor['observations']==28 and monitor['paper_accounts']==10 and monitor['research_configs']==expected['ranked']
base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip();assert base==prior['base_head']=='bf7046685c0b9d7d7bd630a5707d75522a0bdb05'
protected={**paperpre['protected_sha256'],**{str(p.relative_to(R)):sha(p)for p in P.rglob('*')if p.is_file()and'__pycache__'not in p.parts},'research/paper10/state.json':sha(R/'research/paper10/state.json')}
files=sorted(p for p in T.rglob('*')if p.is_file()and'__pycache__'not in p.parts and p.name not in('verification.json','verify.log'))+[L,R/'research/automation/README.md',R/'research/monitor/latest.json',R/'research/monitor/configs.json.gz']
proof={'passed':True,'verified_at_utc':datetime.now(timezone.utc).isoformat(),'base_commit':base,'registry':{'rows':len(lines),'canonical':3046,'preserved_ids':len(records),'unchanged_prior_rows':prior['lines'],'new_reserved_and_finished':21,'new_historical_trials':18,'new_legacy_cutoffs':3,'pending':0},'historical_summary':summary,'new_cross_period_parameter_pairs':len(summary['new_both_periods_passed_combination_pairs']),'new_cross_period_return_paths':h['qualified_cross_period_pairs_not_in_any_prior_report'],'jointly_improved_both_period_pairs':cmp['new_pairs_jointly_improve_same_BTC_pure_ETH_channel_controls'],'paper10_accounts_unchanged':True,'sensitivity_plot_visually_reviewed':True,'engineering_preparation_recovered_before_evaluation':True,'checks':{'all6_actual_execution_phases_exit_zero':True,'all6_replay_phases_exit_zero':True,'all3_final_checks_exit_zero':True,'all36source_and54new_scenes_independently_audited':True,'exact1500_500_funding_original75_25_verified':True,'all324new_folds_54sensitivity_rows_preserved':True,'all12_source_components_and_prior_ledger_unchanged':True,'matched_primary_and_secondary_controls_verified':True,'whole_path_novelty_and_reused_history_disclosed':True,'initial16_actual_evidence_complete':True,'original_daily6_decisions_65bars_64overlap_independently_audited':True,'original_shadow_prefix_positions_costs_and_nextdaily_preserved':True,'paper28_plan_accounts_and_journals_preserved':True,'monitor_snapshot_current_and_checked':True,'frozen_plan_before_engineering_recovery_unchanged':True},'audits':audits,'protected_sha256':protected,'files_sha256':{str(p.relative_to(R)):sha(p)for p in files}}
(T/'verification.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'passed':True,**proof['registry'],'files_hashed':len(files),'protected_files':len(protected),'new_cross_period_paths':proof['new_cross_period_return_paths'],'joint_control_improvements':proof['jointly_improved_both_period_pairs'],'paper_observations_unchanged':28}))
