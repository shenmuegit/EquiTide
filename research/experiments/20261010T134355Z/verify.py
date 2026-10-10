"""Bind all actual new results, old sources, cost/fold evidence and untouched paper accounts."""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import csv,gzip,hashlib,json,subprocess,sys,zipfile
T=Path(__file__).resolve().parent;R=T.parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sys.path.insert(0,str(R/'research/automation'));import registry
L=R/'research/automation/registry.jsonl';lines=L.read_bytes().splitlines(keepends=True);raw=[json.loads(x)for x in lines];records=registry.read_records(L)
prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));r=json.loads((T/'report.json').read_text());f=json.loads((T/'forward_report.json').read_text());cmp=json.loads((T/'comparison.json').read_text());h=json.loads((T/'history_paths.json').read_text());plan=json.loads((T/'spec.json').read_text())
assert r['plan']==plan and prior['lines']==6469 and prior['canonical']==3185
assert len(lines)==6523 and len(records)==3214 and len({registry.fingerprint(v['spec'])for v in records.values()})==3212
assert hashlib.sha256(b''.join(lines[:prior['lines']])).hexdigest()==prior['ledger_sha256']
for fp,v in prior['records'].items():assert records[fp]==v,fp
assert not [v for v in records.values()if v['status']=='reserved']
hist=json.loads((T/'batch.json').read_text());fb=json.loads((T/'forward_batch.json').read_text());grid=json.loads((T/'grid_batch.json').read_text())
assert len(hist)==24 and len(fb)==3 and len(grid)==38 and sum(b['is_new']for b in grid)==24
for batch,report,file in [(hist,r,'report.json'),(fb,f,'forward_report.json')]:
 for b in batch:
  sp=json.loads((R/b['spec']).read_text());fp=registry.fingerprint(sp);assert fp==b['fingerprint'] and fp not in prior['records']
  ev=[x for x in raw[prior['lines']:]if x['fingerprint']==fp];assert len(ev)==2 and ev[0]['status']=='reserved' and ev[1]['status']==report['configs'][b['name']]['status']
  assert ev[1]['result_available'] and ev[1]['report_sha256']==sha(T/file)
  start=report['evaluation_started_utc']if batch is hist else report['observation_started_utc'];assert plan['frozen_at_utc']<=ev[0]['recorded_at_utc']<start
assert len((T/'finish.log').read_text().splitlines())==len(hist)+len(fb)
summary=r['summary'];fresh=[c for c in r['configs'].values()if c['is_new']]
assert summary['new_configs']==24 and summary['new_component_configs']==summary['new_combination_configs']==12 and summary['new_cost_scenes']==72
assert summary['positive_1x']==sum(c['scenes']['1']['net_return_pct']>0 for c in fresh) and summary['positive_3x']==sum(c['scenes']['3']['net_return_pct']>0 for c in fresh)
assert set(summary['passed'])=={c['name']for c in fresh if all(c['criteria'].values())} and set(summary['rejected'])=={c['name']for c in fresh if not all(c['criteria'].values())}
assert summary['new_component_fills']==sum(c['scenes'][k]['executions']for c in fresh if c['role']=='component'for k in('1','2','3')) and summary['new_live_orders']==0
assert len(summary['new_both_periods_passed_combination_pairs'])==sum(c['year']=='2025'and c['role']=='combination'and c['both_periods_meet_full_gates']for c in fresh)
assert Counter(k for c in fresh for k in c['failed_criteria'])==Counter(k for c in fresh for k,v in c['criteria'].items()if not v)
for c in fresh:
 assert set(c['scenes'])=={'1','2','3'} and all(len(z['folds'])==6 for z in c['scenes'].values())
 assert (c['status']=='passed')==all(c['criteria'].values())
for path,expected in r['source_hashes'].items():assert sha(R/path)==expected,path
for path,expected in plan['reused_code_sha256'].items():assert sha(R/path)==expected,path
assert sha(T/'preflight.py')==plan['preflight_sha256']
fixed={ref['year']:ref['fingerprint']for ref in plan['read_only_component_refs']if ref['asset']=='BTC'}
assert len(fixed)==2 and len(plan['read_only_component_refs'])==8 and len(plan['read_only_grid_refs'])==6
for ref in plan['read_only_component_refs']+plan['read_only_grid_refs']:
 for name,hkey in [('spec','spec_sha256'),('report','report_sha256'),('archive','archive_sha256')]:assert sha(R/ref[name])==ref[hkey]
 assert records[ref['fingerprint']]==prior['records'][ref['fingerprint']]
 c=r['configs'][ref['name']];o=json.loads((R/ref['report']).read_text())['configs'][ref['name']]
 assert not c['is_new'] and c['scenes']==o['scenes'] and c['criteria']==o['criteria'] and c['status']==o['status']
assert len(plan['read_only_background_refs'])==4 and len(r['read_only_background'])==4
for ref in plan['read_only_background_refs']:
 for name,hkey in [('spec','spec_sha256'),('report','report_sha256'),('archive','archive_sha256')]:assert sha(R/ref[name])==ref[hkey]
 old=json.loads((R/ref['report']).read_text())['configs'][ref['name']];row=r['read_only_background'][ref['name']]
 assert old['raw_weights']==row['raw_weights']==ref['raw_weights'] and old['status']==row['status']
 for k,z in row['scenes'].items():assert all(z[key]==old['scenes'][k][key]for key in z)
assert r['cash_reference']==plan['cash_reference']and r['cash_reference']['return_pct']==0
for b in hist:
 c=r['configs'][b['name']];sp=json.loads((R/b['spec']).read_text());assert c['EMA_span_days']in(27,30,33)and c['EMA_symmetric_band']in(.01,.0125,.015)
 if c['role']=='component':
  assert c['asset']=='ETH'and sp['universe']==['ETH/USDT']and c['capital_usdt']==sp['parameters']['initial_capital_usdt']==500
  assert sp['family']=='daily-channel-ema-confirmation'and sp['logic']==plan['rules_by_asset']['ETH']
  assert sp['parameters']['entry_lookback_days']==15 and sp['parameters']['exit_lookback_days']==30
  assert sp['parameters']['EMA_span_days']==c['EMA_span_days'] and sp['parameters']['EMA_symmetric_band']==c['EMA_symmetric_band']
 else:
  assert sp['parameters']['initial_capital_usdt']==2000 and[c['weight']for c in sp['components']]==[.75,.25]and sp['components'][0]['fingerprint']==fixed[c['year']]
  child=records[sp['components'][1]['fingerprint']]['spec'];assert child['universe']==['ETH/USDT']and child['parameters']['initial_capital_usdt']==500
  assert child['parameters']['EMA_span_days']==c['EMA_span_days']and child['parameters']['EMA_symmetric_band']==c['EMA_symmetric_band']
assert plan['grid']['predeclared_focus']=={'EMA_span_days':27,'EMA_symmetric_band':.0125}and plan['grid']['predeclared_center']=={'EMA_span_days':30,'EMA_symmetric_band':.0125}
audits=[json.loads((T/name).read_text())for name in ('audit.log','audit_forward.log')];assert all(a['passed']for a in audits)
assert audits[0]['actual_scenes_audited']==72 and audits[0]['NAV_points_audited']==18675504 and audits[0]['joint_channel_pandasEMA_causal_decisions']==6480 and audits[0]['Decimal_fills_independently_checked']==summary['new_component_fills']
assert audits[0]['read_only_component_scenes']==24 and audits[0]['read_only_portfolio_scenes']==18 and audits[0]['report_sha256']==sha(T/'report.json')
assert audits[1]['report_sha256']==sha(T/'forward_report.json')
assert len(cmp['matched_comparisons'])==len(cmp['all_grid_vs_old_center'])==18 and cmp['report_sha256']==sha(T/'report.json')
for row in cmp['matched_comparisons']+cmp['all_grid_vs_old_center']:
 c=r['configs'][row['config']];o=r['configs'].get(row['comparator'],r['read_only_comparators'].get(row['comparator']));assert o
 assert row['return_differences_pp']=={k:c['scenes'][k]['net_return_pct']-o['scenes'][k]['net_return_pct']for k in('1','2','3')}
 assert row['minute_DD3_difference_pp']==c['scenes']['3']['max_drawdown_pct']-o['scenes']['3']['max_drawdown_pct']
 assert row['all_cost_NAV_identical']==all(c['scenes'][k]['NAV_sha256_f64le']==o['scenes'][k]['NAV_sha256_f64le']for k in('1','2','3'))
for key,rows_key in [('qualified_pairs_vs_matched_controls','matched_comparisons'),('qualified_pairs_vs_old_center','all_grid_vs_old_center')]:
 for pair in cmp[key]:
  xs=[next(x for x in cmp[rows_key]if x['config']==n)for n in pair['pair']];returns=[v for x in xs for v in x['return_differences_pp'].values()];dd=[x['minute_DD3_difference_pp']for x in xs]
  assert pair['joint_improvement_both_years']==(all(v>=0 for v in returns)and all(v<=0 for v in dd)and(any(v>0 for v in returns)or any(v<0 for v in dd)))
assert cmp['new_qualified_pairs_jointly_nonworse_with_improvement']==sum(x['joint_improvement_both_years']for x in cmp['qualified_pairs_vs_matched_controls'])
assert cmp['qualified_pairs_improving_old_center']==sum(x['joint_improvement_both_years']for x in cmp['qualified_pairs_vs_old_center'])
assert h['report_sha256']==sha(T/'report.json')
assert h['new_scenes_already_in_any_prior_report']+h['new_scenes_not_in_any_prior_report']==72 and h['distinct_new_scene_paths_not_in_prior']<=h['new_scenes_not_in_any_prior_report']
assert len(h['qualified_pair_histories'])==len(summary['new_both_periods_passed_combination_pairs'])
for p,expected in h['all_prior_report_sha256'].items():assert sha(R/p)==expected,p
with(T/'folds.csv').open()as source:folds=list(csv.DictReader(source))
assert len(folds)==684 and sum(row['is_new']=='True'for row in folds)==432
for row in folds:
 z=r['configs'][row['config']]['scenes'][row['cost']]['folds'][int(row['fold'])-1]
 for name,key in [('net_return_pct','net_return_pct'),('minute_DD_pct','max_drawdown_pct'),('Sharpe365','sharpe_365'),('Calmar','calmar')]:assert row[name]==(''if z[key]is None else str(z[key]))
with(T/'sensitivity.csv').open()as source:sens=list(csv.DictReader(source))
assert len(sens)==114 and sum(row['is_new']=='True'for row in sens)==72
for row in sens:
 z=r['configs'][row['config']]['scenes'][row['cost']]
 for name,key in [('net_return_pct','net_return_pct'),('minute_DD_pct','max_drawdown_pct'),('daily_DD_pct','daily_mark_drawdown_pct'),('Sharpe365','sharpe_365'),('Calmar','calmar')]:assert row[name]==(''if z[key]is None else str(z[key]))
fr=plan['forward_resume'];assert f['resume_utc']=='2026-10-10T11:00:00Z'and f['cutoff_utc']=='2026-10-10T13:00:00Z'
assert fr['prior_NAV_points']==12189 and fr['total_NAV_points']==12309 and fr['cumulative_minutes']==12299
assert audits[1]['original_NAV_prefix']==12189 and audits[1]['new_daily_decisions']==audits[1]['new_reference_points']==audits[1]['new_executions']==0 and audits[1]['complete_days']==8
assert sha(R/f['frozen_plan_path'])==f['frozen_plan_sha256']=='2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81'
oldstate=json.loads((R/f['source_state']).read_text());state=json.loads((T/'forward_state.json').read_text());assert state['positions_by_asset_and_cost']==oldstate['positions_by_asset_and_cost']and state['next_daily_decision_utc']=='2026-10-11T00:01:00Z'
replay=json.loads((T/'reproduction_execution.json').read_text());execution=json.loads((T/'execution_steps.json').read_text());checks=json.loads((T/'final_checks.json').read_text());assert len(replay)==7 and len(execution)==6 and len(checks)==3 and all(x['exit_code']==0 for x in replay+execution+checks)
assert 'PASS:all72 NEW ETHEMA-boundary scenes and full report exactly reproduced' in(T/'reproduce.log').read_text()
assert json.loads((T/'signal_check.log').read_text())['synthetic_fixture_checks']=='PASS'
for item in prior['conclusions']:assert sha(R/item['path'])==item['sha256']and(R/item['path']).read_text()==item['text']
for category in ('skills','oos_checks'):
 for p,item in prior[category].items():assert sha(R/p)==item['sha256']and(R/p).read_text()==item['text']
for item in prior['freqtrade_results']:
 assert sha(R/item['path'])==item['sha256']
 if item['members']:
  with zipfile.ZipFile(R/item['path'])as z:
   for member in item['members']:assert hashlib.sha256(z.read(member['name'])).hexdigest()==member['sha256']
assert sha(R/'research/automation/task.md')==prior['read_task_sha256']and sha(R/'research/monitor/README.md')==prior['read_monitor_README']['sha256']
marker='## 最近完成的轮次\n\n';entry=(T/'README_entry.md').read_text()+'\n';assert(R/'research/automation/README.md').read_text()==prior['read_automation_README']['text'].replace(marker,marker+entry,1)
for p,expected in prior['protected_sha256'].items():assert sha(R/p)==expected,p
assert sha(R/'research/paper10/plan.json')==prior['paper10_plan_sha256']and sha(R/'research/paper10/state.json')==prior['paper10_state_sha256']
paper=json.loads((R/'research/paper10/state.json').read_text());assert paper['observations']==33 and paper['last_observation_id']==prior['paper_observation']
initial=json.loads((T/'prior_evidence_audit.json').read_text());assert not initial['missing_initial16']and [v['fingerprint']for v in initial['initial16_actual_results_checked']]==[x['fingerprint']for x in raw[:16]]
for item in initial['initial16_actual_results_checked']:
 for ev in item['evidence']:assert sha(R/ev['path'])==ev['sha256']
feed=json.loads((R/'research/monitor/latest.json').read_text());monitor=json.loads((T/'monitor_check.log').read_text());counts=dict(prior['monitor_counts_before']);counts['registered']+=24;counts['results']+=24;counts['ranked']+=24;counts['passed']+=len(summary['passed']);counts['rejected']+=len(summary['rejected']);counts['observation_records_excluded']+=3
assert feed['research']['last_run']['id']==T.name and feed['research']['counts']==counts
assert feed['paper']['observation_id']==paper['last_observation_id']and monitor['ok']and monitor['protected_inputs_unchanged']and monitor['observations']==33 and monitor['research_configs']==2539
base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip();assert base==prior['base_head']=='9eb9f16a8d22dfddad39f612943d55943364bf6d'
files=sorted(p for p in T.rglob('*')if p.is_file()and'__pycache__'not in p.parts and p.name not in('verification.json','verify.log'))+[L,R/'research/automation/README.md',R/'research/monitor/latest.json',R/'research/monitor/configs.json.gz']
proof={'passed':True,'verified_at_utc':datetime.now(timezone.utc).isoformat(),'base_commit':base,'registry':{'rows':6523,'canonical':3212,'preserved_ids':3214,'unchanged_prior_rows':6469,'new_reserved_and_finished':27,'new_historical_trials':24,'new_legacy_cutoffs':3,'pending':0},'historical_summary':summary,'new_qualified_cross_period_parameter_pairs':len(summary['new_both_periods_passed_combination_pairs']),'new_cross_period_return_paths':h['qualified_cross_period_pairs_not_in_any_prior_report'],'jointly_improved_both_period_pairs':cmp['new_qualified_pairs_jointly_nonworse_with_improvement'],'paper10_accounts_unchanged':True,'both_sensitivity_plots_visually_reviewed':True,'checks':{'all7_replay_phases_exit_zero':True,'all6_actual_phases_exit_zero':True,'all3_final_checks_exit_zero':True,'all72new_and42old_scenes_audited':True,'pandasEMA_channel_causality_and_Decimal_money_verified':True,'exact1500_500_funding_raw75_25_verified':True,'all684folds_114sensitivity_rows_preserved':True,'new432_and_old252folds_separated':True,'all_actual_rejections_and12old_grid_cells_retained':True,'prior_records_results_criteria_unchanged':True,'matched_same_BTC_and_old_center_controls_verified':True,'whole_path_novelty_reused_history_and_boundary_cliffs_disclosed':True,'initial16_actual_results_checked':True,'original_shadow_prefix_positions_costs_unchanged':True,'paper33_plan_accounts_journals_UI_and_Site_preserved':True,'monitor_snapshot_current_and_checked':True},'audits':audits,'protected_sha256':prior['protected_sha256'],'files_sha256':{str(p.relative_to(R)):sha(p)for p in files}}
(T/'verification.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'passed':True,**proof['registry'],'new_qualified_paths':h['qualified_cross_period_pairs_not_in_any_prior_report'],'joint_both_period_improvements':cmp['new_qualified_pairs_jointly_nonworse_with_improvement'],'files_hashed':len(files),'protected_files':len(prior['protected_sha256']),'paper_observations':33}))
