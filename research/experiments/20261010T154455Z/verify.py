"""Final read-only binding of all funded results,controls,ledger and preserved accounts."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal as D
import csv,gzip,hashlib,json,subprocess,sys
T=Path(__file__).resolve().parent;R=T.parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sys.path.insert(0,str(R/'research/automation'));import registry
sys.path.insert(0,str(T));from design import definitions
prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));r=json.loads((T/'report.json').read_text());f=json.loads((T/'forward_report.json').read_text());plan=json.loads((T/'spec.json').read_text());cmp=json.loads((T/'comparison.json').read_text());h=json.loads((T/'history_paths.json').read_text());L=R/'research/automation/registry.jsonl';lines=L.read_bytes().splitlines(keepends=True);raw=[json.loads(x)for x in lines];records=registry.read_records(L)
assert r['plan']==plan and (prior['lines'],prior['preserved_ids'],prior['canonical'])==(6543,3224,3222)
assert (len(lines),len(records),len({registry.fingerprint(v['spec'])for v in records.values()}))==(6605,3255,3253)
assert hashlib.sha256(b''.join(lines[:prior['lines']])).hexdigest()==prior['ledger_sha256']
for fp,rec in prior['records'].items():assert records[fp]==rec,fp
assert not [v for v in records.values()if v['status']=='reserved']
hist=json.loads((T/'batch.json').read_text());fb=json.loads((T/'forward_batch.json').read_text());grid=json.loads((T/'grid_batch.json').read_text());assert(len(hist),len(fb),len(grid))==(28,3,42)
assert sum(x['role']=='component'for x in hist)==16 and sum(x.get('asset')=='BTC'for x in hist)==4 and sum(x.get('asset')=='ETH'for x in hist)==12
expected={registry.fingerprint(sp):fields for sp,fields in definitions(registry.fingerprint)};assert set(expected)=={x['fingerprint']for x in grid}
for batch,report,name in [(hist,r,'report.json'),(fb,f,'forward_report.json')]:
 for b in batch:
  sp=json.loads((R/b['spec']).read_text());fp=registry.fingerprint(sp);assert fp==b['fingerprint']and fp not in prior['records'];events=[x for x in raw[prior['lines']:]if x['fingerprint']==fp];assert len(events)==2 and events[0]['status']=='reserved'and events[1]['status']==report['configs'][b['name']]['status'];assert events[1]['result_available']and events[1]['report_sha256']==sha(T/name)
  started=report['evaluation_started_utc']if batch is hist else report['observation_started_utc'];assert plan['frozen_at_utc']<=events[0]['recorded_at_utc']<started
assert len((T/'finish.log').read_text().splitlines())==len(hist)+len(fb)
fresh=[c for c in r['configs'].values()if c['is_new']];summary=r['summary'];assert summary['new_configs']==28 and summary['new_component_configs']==16 and summary['new_combination_configs']==12 and summary['new_cost_scenes']==84
assert summary['positive_1x']==sum(c['scenes']['1']['net_return_pct']>0 for c in fresh)and summary['positive_3x']==sum(c['scenes']['3']['net_return_pct']>0 for c in fresh)
assert set(summary['passed'])=={c['name']for c in fresh if all(c['criteria'].values())}and set(summary['rejected'])=={c['name']for c in fresh if not all(c['criteria'].values())}
for b in hist:
 c=r['configs'][b['name']];sp=json.loads((R/b['spec']).read_text());assert all(len(z['folds'])==6 for z in c['scenes'].values())and(c['status']=='passed')==all(c['criteria'].values());assert c['BTC_initial_weight']in(.6,.675)and c['raw_weights']in[[.6,.4],[.675,.325]]
 if c['role']=='component':
  assert c['capital_usdt']==sp['parameters']['initial_capital_usdt']==int(D(2000)*D(str(c['raw_weights'][0 if c['asset']=='BTC'else 1])))
  assert sp['universe']==[c['asset']+'/USDT']and sp['parameters']['entry_lookback_days']==15 and sp['parameters']['exit_lookback_days']==30
  if c['asset']=='BTC':assert sp['family']=='daily-close-range-relative-quote-volume'and sp['parameters']['volume_lookback_days']==30 and sp['parameters']['minimum_volume_ratio']==1
  else:assert sp['family']=='daily-channel-ema-confirmation'and sp['parameters']['EMA_span_days']==c['EMA_span_days']in(30,33,35)and sp['parameters']['EMA_symmetric_band']==.0125
 else:
  assert [q['weight']for q in sp['components']]==c['raw_weights']and sp['parameters']['initial_capital_usdt']==2000
  children=[records[q['fingerprint']]['spec']for q in sp['components']];assert [x['parameters']['initial_capital_usdt']for x in children]==[int(D(2000)*D(str(w)))for w in c['raw_weights']]
  assert children[0]['universe']==['BTC/USDT']and children[1]['universe']==['ETH/USDT']and children[1]['parameters']['EMA_span_days']==c['EMA_span_days']
for mapping in(r['source_hashes'],plan['reused_code_sha256']):
 for path,hsh in mapping.items():assert sha(R/path)==hsh,path
assert sha(T/'preflight.py')==plan['preflight_sha256']and plan['grid']['predeclared_focus']=={'EMA_span_days':30,'raw_weights':[.675,.325]}
assert len(plan['read_only_component_refs'])==8 and len(plan['read_only_grid_refs'])==6
for ref in plan['read_only_component_refs']+plan['read_only_grid_refs']:
 for field,hkey in [('spec','spec_sha256'),('report','report_sha256'),('archive','archive_sha256')]:assert sha(R/ref[field])==ref[hkey]
 c=r['configs'][ref['name']];old=json.loads((R/ref['report']).read_text())['configs'][ref['name']];assert not c['is_new']and c['status']==old['status']and c['criteria']==old['criteria']and c['scenes']==old['scenes'];assert records[ref['fingerprint']]==prior['records'][ref['fingerprint']]
assert len(r['read_only_background'])==len(plan['read_only_background_refs'])==4
for ref in plan['read_only_background_refs']:
 for field,hkey in [('spec','spec_sha256'),('report','report_sha256'),('archive','archive_sha256')]:assert sha(R/ref[field])==ref[hkey]
 old=json.loads((R/ref['report']).read_text())['configs'][ref['name']];bg=r['read_only_background'][ref['name']];assert bg['raw_weights']==old['raw_weights']and bg['status']==old['status']
 for k,z in bg['scenes'].items():assert all(value==old['scenes'][k][key]for key,value in z.items())
assert r['cash_reference']==plan['cash_reference']and r['cash_reference']['return_pct']==0
ah=json.loads((T/'audit.log').read_text());af=json.loads((T/'audit_forward.log').read_text());assert ah['passed']and af['passed']and ah['report_sha256']==sha(T/'report.json')and af['report_sha256']==sha(T/'forward_report.json')
assert(ah['actual_scenes_audited'],ah['NAV_points_audited'],ah['total_causal_decisions'],ah['ETH_pandasEMA_causal_decisions'],ah['BTC_disjoint_quote_volume_causal_decisions'])==(84,21788088,8640,6480,2160)
assert ah['Decimal_fills_independently_checked']==summary['new_component_fills']==sum(c['scenes'][k]['executions']for c in fresh if c['role']=='component'for k in('1','2','3'))and summary['new_live_orders']==0
assert cmp['report_sha256']==h['report_sha256']==sha(T/'report.json')and len(cmp['comparisons'])==36
for row in cmp['comparisons']:
 c=r['configs'][row['config']];o=r['configs'][row['comparator']];assert row['control_raw_weights']==o['raw_weights']==[.75,.25]and row['same_total_capital_usdt']==c['capital_usdt']==o['capital_usdt']==2000
 if row['kind']=='SAME_RULES_OLD75_25':assert c['EMA_span_days']==o['EMA_span_days']
 assert row['return_differences_pp']=={k:c['scenes'][k]['net_return_pct']-o['scenes'][k]['net_return_pct']for k in('1','2','3')};assert row['minute_DD3_difference_pp']==c['scenes']['3']['max_drawdown_pct']-o['scenes']['3']['max_drawdown_pct']
for pair in cmp['qualified_pair_comparisons']:
 xs=[next(x for x in cmp['comparisons']if x['config']==n and x['kind']==pair['kind'])for n in pair['pair']];rv=[v for x in xs for v in x['return_differences_pp'].values()];dd=[x['minute_DD3_difference_pp']for x in xs];assert pair['joint_improvement_both_years']==(all(v>=0 for v in rv)and all(v<=0 for v in dd)and(any(v>0 for v in rv)or any(v<0 for v in dd)))
for kind,key in [('SAME_RULES_OLD75_25','jointly_improved_pairs_vs_same_rules'),('OLD30DAY_75_25_CENTER','jointly_improved_pairs_vs_old_center')]:assert cmp[key]==sum(x['joint_improvement_both_years']for x in cmp['qualified_pair_comparisons']if x['kind']==kind)
assert h['new_scenes_already_in_any_prior_report']+h['new_scenes_not_in_any_prior_report']==84
for path,hsh in h['all_prior_report_sha256'].items():assert sha(R/path)==hsh,path
for filename,total,newcount in [('sensitivity.csv',126,84),('folds.csv',756,504)]:
 with(T/filename).open()as file:rows=list(csv.DictReader(file))
 assert len(rows)==total and sum(x['is_new']=='True'for x in rows)==newcount
 for row in rows:
  z=r['configs'][row['config']]['scenes'][row['cost']];z=z['folds'][int(row['fold'])-1]if filename=='folds.csv'else z
  for label,key in [('net_return_pct','net_return_pct'),('minute_DD_pct','max_drawdown_pct'),('Sharpe365','sharpe_365'),('Calmar','calmar')]:assert row[label]==(''if z[key]is None else str(z[key]))
fr=plan['forward_resume'];assert f['resume_utc']=='2026-10-10T13:00:00Z'and f['cutoff_utc']=='2026-10-10T15:00:00Z';assert(fr['prior_NAV_points'],fr['total_NAV_points'],fr['cumulative_minutes'])==(12309,12429,12419)
assert af['new_closed_marks_per_asset']==120 and af['new_daily_decisions']==af['new_reference_points']==af['new_executions']==0
assert sha(R/f['frozen_plan_path'])==f['frozen_plan_sha256']=='2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81'
replay=json.loads((T/'reproduction_execution.json').read_text());execution=json.loads((T/'execution_steps.json').read_text());checks=json.loads((T/'final_checks.json').read_text());assert(len(replay),len(execution),len(checks))==(7,6,3)and all(x['exit_code']==0 for x in replay+execution+checks)
assert 'PASS:all84 NEW funding-span scenes and full report exactly reproduced'in(T/'reproduce.log').read_text()
assert json.loads((T/'signal_check.log').read_text())['synthetic_fixture_checks']=='PASS'
for item in prior['conclusions']:assert sha(R/item['path'])==item['sha256']and(R/item['path']).read_text()==item['text']
for category in ('skills','oos_checks'):
 for path,item in prior[category].items():assert sha(R/path)==item['sha256']and(R/path).read_text()==item['text']
for item in prior['freqtrade_results']:assert sha(R/item['path'])==item['sha256']
for path,hsh in prior['protected_sha256'].items():assert sha(R/path)==hsh,path
assert sha(R/'research/paper10/plan.json')==prior['paper10_plan_sha256']and sha(R/'research/paper10/state.json')==prior['paper10_state_sha256']
paper=json.loads((R/'research/paper10/state.json').read_text());assert paper['observations']==34 and paper['last_observation_id']==prior['paper_observation']
marker='## 最近完成的轮次\n\n';assert(R/'research/automation/README.md').read_text()==prior['read_automation_README']['text'].replace(marker,marker+(T/'README_entry.md').read_text()+'\n',1)
assert sha(R/'research/automation/task.md')==prior['read_task_sha256']and sha(R/'research/monitor/README.md')==prior['read_monitor_README']['sha256']
initial=json.loads((T/'prior_evidence_audit.json').read_text());assert not initial['missing_initial16']and [x['fingerprint']for x in initial['initial16_actual_results_checked']]==[x['fingerprint']for x in raw[:16]]
feed=json.loads((R/'research/monitor/latest.json').read_text());counts=dict(prior['monitor_counts_before']);counts['registered']+=28;counts['results']+=28;counts['ranked']+=28;counts['passed']+=len(summary['passed']);counts['rejected']+=len(summary['rejected']);counts['observation_records_excluded']+=3
assert feed['research']['counts']==counts and feed['research']['last_run']['id']==T.name and feed['paper']['observation_id']==paper['last_observation_id']
monitor=json.loads((T/'monitor_check.log').read_text());assert monitor['ok']and monitor['protected_inputs_unchanged']and monitor['observations']==34 and monitor['research_configs']==2567
base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip();assert base==prior['base_head']=='45089f564dbffeed7feb14b2c379c75b75b5744c'
files=sorted(p for p in T.rglob('*')if p.is_file()and'__pycache__'not in p.parts and p.name not in('verification.json','verify.log'))+[L,R/'research/automation/README.md',R/'research/monitor/latest.json',R/'research/monitor/configs.json.gz']
out={'passed':True,'verified_at_utc':datetime.now(timezone.utc).isoformat(),'base_commit':base,'registry':{'rows':len(lines),'canonical':3253,'preserved_ids':len(records),'unchanged_prior_rows':prior['lines'],'new_reserved_and_finished':31,'new_historical_trials':28,'new_legacy_cutoffs':3,'pending':0},'historical_summary':summary,'new_qualified_cross_period_parameter_pairs':len(summary['new_both_periods_passed_combination_pairs']),'new_cross_period_return_paths':h['qualified_cross_period_pairs_not_in_any_prior_report'],'jointly_improved_both_period_pairs':cmp['jointly_improved_pairs_vs_same_rules'],'paper10_accounts_unchanged':True,'both_sensitivity_plots_visually_reviewed':True,'checks':{'all7_replay_phases_exit_zero':True,'all6_actual_phases_exit_zero':True,'all3_final_checks_exit_zero':True,'all84new_and42old_cost_scenes_verified':True,'funded_components_rerun_with_own_costs_no_NAV_rescaling':True,'explicit_raw_weights_preserved_no_rebalance':True,'all756folds_126cost_rows_verified':True,'old_results_criteria_and_all_prior_ledger_rows_preserved':True,'initial16_actual_evidence_complete':True,'paper34_plan_state_journals_UI_preserved':True},'audits':[ah,af],'protected_sha256':prior['protected_sha256'],'files_sha256':{str(p.relative_to(R)):sha(p)for p in files}}
(T/'verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'passed':True,**out['registry'],'joint_improvements':cmp['jointly_improved_pairs_vs_same_rules'],'new_qualified_paths':h['qualified_cross_period_pairs_not_in_any_prior_report'],'protected_files':len(prior['protected_sha256']),'files_hashed':len(files)}))
