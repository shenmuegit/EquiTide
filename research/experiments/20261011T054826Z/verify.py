"""Bind the frozen paired-entry batch, independent auditor and all preserved state."""
from pathlib import Path
from decimal import Decimal as D
from datetime import datetime,timezone
from collections import Counter
import csv,gzip,hashlib,json,subprocess,sys
T=Path(__file__).resolve().parent;R=T.parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text())
sys.path.insert(0,str(R/'research/automation'));import registry
sys.path.insert(0,str(T));from design import definitions
prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));r,f,plan=[read(T/n)for n in('report.json','forward_report.json','spec.json')];cmp,h=[read(T/n)for n in('comparison.json','history_paths.json')]
L=R/'research/automation/registry.jsonl';lines=L.read_bytes().splitlines(keepends=True);raw=[json.loads(x)for x in lines];records=registry.read_records(L)
assert r['plan']==plan
assert (prior['lines'],prior['preserved_ids'],prior['canonical'])==(7081,3493,3491)
canonical=len({registry.fingerprint(v['spec'])for v in records.values()});assert (len(lines),len(records),canonical)==(7135,3520,3518)
assert hashlib.sha256(b''.join(lines[:prior['lines']])).hexdigest()==prior['ledger_sha256']
for fp,rec in prior['records'].items():assert records[fp]==rec,fp
assert not[v for v in records.values()if v['status']=='reserved']
hist,fb,grid=[read(T/n)for n in('batch.json','forward_batch.json','grid_batch.json')];assert(len(hist),len(fb),len(grid))==(24,3,30)
assert sum(x['role']=='component'for x in hist)==8 and sum(x.get('asset')=='BTC'for x in hist)==4 and sum(x.get('asset')=='ETH'for x in hist)==4
expected={registry.fingerprint(sp):fields for sp,fields in definitions(registry.fingerprint)};assert set(expected)=={x['fingerprint']for x in grid}
for b in grid:assert all(b[k]==v for k,v in expected[b['fingerprint']].items())
for batch,report,filename in((hist,r,'report.json'),(fb,f,'forward_report.json')):
 for b in batch:
  sp=read(R/b['spec']);fp=registry.fingerprint(sp);assert fp==b['fingerprint']and fp not in prior['records'];events=[x for x in raw[prior['lines']:]if x['fingerprint']==fp]
  assert len(events)==2 and events[0]['status']=='reserved'and events[1]['status']==report['configs'][b['name']]['status']
  assert events[1]['result_available']and events[1]['report_sha256']==sha(T/filename)
  started=report['evaluation_started_utc']if batch is hist else report['observation_started_utc'];assert plan['frozen_at_utc']<=events[0]['recorded_at_utc']<started
assert len((T/'finish.log').read_text().splitlines())==27
fresh=[c for c in r['configs'].values()if c['is_new']];summary=r['summary'];assert (summary['new_configs'],summary['new_component_configs'],summary['new_combination_configs'],summary['new_cost_scenes'],summary['new_minute_NAV_points'])==(24,8,16,72,18675504)
assert summary['positive_1x']==sum(c['scenes']['1']['net_return_pct']>0 for c in fresh)==24
assert summary['positive_3x']==sum(c['scenes']['3']['net_return_pct']>0 for c in fresh)==24
assert set(summary['passed'])=={c['name']for c in fresh if all(c['criteria'].values())}and len(summary['passed'])==20
assert set(summary['rejected'])=={c['name']for c in fresh if not all(c['criteria'].values())}and len(summary['rejected'])==4
assert cmp['failure_counts']==dict(Counter(k for c in fresh for k in c['failed_criteria']))=={'four_positive_1x_folds':4}
for b in hist:
 c,sp=r['configs'][b['name']],read(R/b['spec']);assert all(len(z['folds'])==6 and z['NAV_points']==259382 for z in c['scenes'].values())
 assert(c['status']=='passed')==all(c['criteria'].values())and c['BTC_initial_weight']==.55 and c['raw_weights']==[.55,.45]
 if c['role']=='component':
  asset=c['asset'];assert c['capital_usdt']==sp['parameters']['initial_capital_usdt']==(1100 if asset=='BTC'else 900)
  assert sp['universe']==[asset+'/USDT']and sp['parameters']['entry_lookback_days']==c[asset+'_entry_lookback_days']in(10,20) and sp['parameters']['exit_lookback_days']==30
  if asset=='BTC':
   assert sp['family']=='daily-close-range-relative-quote-volume'and sp['parameters']['volume_lookback_days']==c['BTC_volume_lookback_days']==40
   assert sp['parameters']['minimum_volume_ratio']==c['BTC_minimum_volume_ratio']==1.1 and f"same{c['capital_usdt']}USDT funds"in sp['logic']['sizing']
   assert f"C[i-{sp['parameters']['entry_lookback_days']+1}:i-1]"in sp['logic']['entry']
  else:assert sp['family']=='daily-channel-ema-confirmation'and sp['parameters']['EMA_span_days']==30 and sp['parameters']['EMA_symmetric_band']==.0125
 else:
  assert c['capital_usdt']==sp['parameters']['initial_capital_usdt']==2000 and [q['weight']for q in sp['components']]==[.55,.45]
  children=[records[q['fingerprint']]['spec']for q in sp['components']];assert [x['parameters']['initial_capital_usdt']for x in children]==[1100,900]
  assert children[0]['universe']==['BTC/USDT']and children[1]['universe']==['ETH/USDT']
  assert [x['parameters']['entry_lookback_days']for x in children]==[c['BTC_entry_lookback_days'],c['ETH_entry_lookback_days']] and all(x['parameters']['exit_lookback_days']==30 for x in children)
  assert children[0]['parameters']['volume_lookback_days']==40 and children[0]['parameters']['minimum_volume_ratio']==1.1
  assert children[1]['parameters']['EMA_span_days']==30 and children[1]['parameters']['EMA_symmetric_band']==.0125
 other=r['configs'][c['other_period_config']];assert c['year']!=other['year']
 for key in('role','asset','raw_weights','BTC_initial_weight','capital_usdt','BTC_entry_lookback_days','ETH_entry_lookback_days','BTC_volume_lookback_days','BTC_minimum_volume_ratio','EMA_span_days','EMA_symmetric_band'):assert c.get(key)==other.get(key),(c['name'],key)
for mapping in(r['source_hashes'],plan['reused_code_sha256']):
 for path,hsh in mapping.items():assert sha(R/path)==hsh,path
assert sha(T/'preflight.py')==plan['preflight_sha256'];g=plan['grid'];assert g['predeclared_focus']=={'BTC_entry_lookback_days':10,'ETH_entry_lookback_days':20}
assert g['BTC_entry_lookback_days']==g['ETH_entry_lookback_days']==[10,15,20]and g['raw_weights']==[.55,.45]and g['component_capitals_usdt']==[1100,900]
assert g['exit_lookback_days']==30 and g['BTC_volume_lookback_days']==40 and g['BTC_minimum_volume_ratio']==1.1 and g['ETH_EMA_span_days']==30 and g['ETH_symmetric_band']==.0125
assert len(plan['read_only_component_refs'])==4 and len(plan['read_only_grid_refs'])==2
for ref in plan['read_only_component_refs']+plan['read_only_grid_refs']:
 for field,hkey in(('spec','spec_sha256'),('report','report_sha256'),('archive','archive_sha256')):assert sha(R/ref[field])==ref[hkey]
 c,old=r['configs'][ref['name']],read(R/ref['report'])['configs'][ref['name']];assert not c['is_new']and c['status']==old['status']and c['criteria']==old['criteria']and c['scenes']==old['scenes']
 assert records[ref['fingerprint']]==prior['records'][ref['fingerprint']]
assert len(r['read_only_background'])==len(plan['read_only_background_refs'])==4
for ref in plan['read_only_background_refs']:
 for field,hkey in(('spec','spec_sha256'),('report','report_sha256'),('archive','archive_sha256')):assert sha(R/ref[field])==ref[hkey]
 old,bg=read(R/ref['report'])['configs'][ref['name']],r['read_only_background'][ref['name']];assert bg['raw_weights']==old['raw_weights']and bg['status']==old['status']
 for k,z in bg['scenes'].items():assert all(value==old['scenes'][k][key]for key,value in z.items())
assert r['cash_reference']==plan['cash_reference']and r['cash_reference']['return_pct']==0
ah,af=read(T/'audit.log'),read(T/'audit_forward.log');assert ah['passed']and af['passed']and ah['report_sha256']==sha(T/'report.json')and af['report_sha256']==sha(T/'forward_report.json')
assert (ah['actual_scenes_audited'],ah['NAV_points_audited'],ah['total_causal_decisions'],ah['ETH_pandasEMA_causal_decisions'],ah['BTC_disjoint_quote_volume_causal_decisions'])==(72,18675504,4320,2160,2160)
assert ah['Decimal_fills_independently_checked']==summary['new_component_fills']==102 and summary['new_live_orders']==0
assert ah['read_only_component_scenes']==12 and ah['read_only_portfolio_scenes']==6
external={};assert len(plan['read_only_comparator_refs'])==2
for ref in plan['read_only_comparator_refs']:
 for field,key in(('spec','spec_sha256'),('report','report_sha256'),('archive','archive_sha256')):assert sha(R/ref[field])==ref[key]
 old=read(R/ref['report'])['configs'][ref['name']];external[ref['name']]=old;saved=r['read_only_comparators'][ref['name']]
 assert saved['scenes']==old['scenes']and saved['status']==old['status']and records[ref['fingerprint']]==prior['records'][ref['fingerprint']]
lookup={**r['configs'],**external};assert cmp['report_sha256']==h['report_sha256']==sha(T/'report.json')and len(cmp['comparisons'])==36 and len(cmp['qualified_pair_comparisons'])==16
for row in cmp['comparisons']:
 c,o=lookup[row['config']],lookup[row['comparator']];assert c['year']==o['year']and c['capital_usdt']==o['capital_usdt']==row['same_total_capital_usdt']==2000
 assert row['config_raw_weights']==c['raw_weights']and row['control_raw_weights']==o['raw_weights']and not row['comparator_is_new']
 assert row['config_component_capitals']==[int(D(2000)*D(str(w)))for w in c['raw_weights']]
 assert row['control_component_capitals']==[int(D(2000)*D(str(w)))for w in o['raw_weights']]
 if row['kind']=='OLD_ENTRY15_15':assert c['raw_weights']==o['raw_weights']==[.55,.45]and not o['is_new']and o['BTC_entry_lookback_days']==o['ETH_entry_lookback_days']==15 and o['BTC_minimum_volume_ratio']==1.1 and o['BTC_volume_lookback_days']==40
 else:assert row['kind']=='OLD_N30_HALF'and o['name']in external and o['raw_weights']==[.5,.5]
 assert row['return_differences_pp']=={k:c['scenes'][k]['net_return_pct']-o['scenes'][k]['net_return_pct']for k in('1','2','3')}
 assert row['minute_DD3_difference_pp']==c['scenes']['3']['max_drawdown_pct']-o['scenes']['3']['max_drawdown_pct']
 assert row['all_cost_NAV_identical']==all(c['scenes'][k]['NAV_sha256_f64le']==o['scenes'][k]['NAV_sha256_f64le']for k in('1','2','3'))
for pair in cmp['qualified_pair_comparisons']:
 xs=[next(x for x in cmp['comparisons']if x['config']==n and x['kind']==pair['kind'])for n in pair['pair']];rv=[v for x in xs for v in x['return_differences_pp'].values()];dd=[x['minute_DD3_difference_pp']for x in xs]
 assert pair['joint_improvement_both_years']==(all(v>=0 for v in rv)and all(v<=0 for v in dd)and(any(v>0 for v in rv)or any(v<0 for v in dd)))
for kind,key in(('OLD_ENTRY15_15','jointly_improved_pairs_vs_old_entry15_15'),('OLD_N30_HALF','jointly_improved_pairs_vs_old_N30_half')):assert cmp[key]==sum(x['joint_improvement_both_years']for x in cmp['qualified_pair_comparisons']if x['kind']==kind)==0
assert len(summary['new_both_periods_passed_combination_pairs'])==8 and h['qualified_cross_period_pairs_not_in_any_prior_report']==3
assert h['new_scenes_already_in_any_prior_report']+h['new_scenes_not_in_any_prior_report']==72
for path,hsh in h['all_prior_report_sha256'].items():assert sha(R/path)==hsh,path
for filename,total,newcount in(('sensitivity.csv',90,72),('folds.csv',540,432)):
 with(T/filename).open()as file:rows=list(csv.DictReader(file))
 assert len(rows)==total and sum(x['is_new']=='True'for x in rows)==newcount
 for row in rows:
  c=r['configs'][row['config']];z=c['scenes'][row['cost']];z=z['folds'][int(row['fold'])-1]if filename=='folds.csv'else z
  for label,key in(('net_return_pct','net_return_pct'),('minute_DD_pct','max_drawdown_pct'),('Sharpe365','sharpe_365'),('Calmar','calmar')):assert row[label]==(''if z[key]is None else str(z[key]))
  for key in('BTC_entry_lookback_days','ETH_entry_lookback_days'):assert row[key]==(''if c[key]is None else str(c[key]))
fr=plan['forward_resume'];assert f['resume_utc']=='2026-10-11T03:00:00Z'and f['cutoff_utc']=='2026-10-11T05:00:00Z'
assert (fr['prior_NAV_points'],fr['total_NAV_points'],fr['cumulative_minutes'])==(13150,13270,13259)
assert af['new_closed_marks_per_asset']==120 and af['new_daily_decisions']==af['new_reference_points']==af['new_executions']==0
assert af['original_cash_units_desired_trades_costs_unchanged']and af['next_daily_decision_utc']=='2026-10-12T00:01:00Z'
assert read(T/'forward_state.json')['positions_by_asset_and_cost']==read(R/fr['source_state'])['positions_by_asset_and_cost']
assert sha(R/f['frozen_plan_path'])==f['frozen_plan_sha256']=='2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81'
assert read(T/'cache_recovery.json')['scenes_hash_verified']==18
assert read(T/'preparation_execution.json')['exit_code']==0
replay,execution,checks=[read(T/n)for n in('reproduction_execution.json','execution_steps.json','final_checks.json')]
assert(len(replay),len(execution),len(checks))==(7,6,3)and all(x['exit_code']==0 for x in replay+execution+checks)
assert execution[3]['command'][-1].endswith('audit.py')and execution[5]['command'][-1].endswith('finish.py')
assert replay[4]['command'][-1].endswith('audit.py')
assert 'PASS:all72 NEW paired-entry scenes and full report exactly reproduced'in(T/'reproduce.log').read_text()
assert read(T/'signal_check.log')['synthetic_fixture_checks']=='PASS'
for item in prior['conclusions']:assert sha(R/item['path'])==item['sha256']and(R/item['path']).read_text()==item['text']
for category in('skills','oos_checks'):
 for path,item in prior[category].items():assert sha(R/path)==item['sha256']and(R/path).read_text()==item['text']
for item in prior['freqtrade_results']:assert sha(R/item['path'])==item['sha256']
for path,hsh in prior['protected_sha256'].items():assert sha(R/path)==hsh,path
assert sha(R/'research/paper10/plan.json')==prior['paper10_plan_sha256']and sha(R/'research/paper10/state.json')==prior['paper10_state_sha256']
paper=read(R/'research/paper10/state.json');assert paper['observations']==prior['paper_observations']==41 and paper['last_observation_id']==prior['paper_observation']=='20261011T042222787905Z'
marker='## 最近完成的轮次\n\n';assert(R/'research/automation/README.md').read_text()==prior['read_automation_README']['text'].replace(marker,marker+(T/'README_entry.md').read_text()+'\n',1)
assert sha(R/'research/automation/task.md')==prior['read_task_sha256']and sha(R/'research/monitor/README.md')==prior['read_monitor_README']['sha256']
initial16=read(T/'prior_evidence_audit.json');assert not initial16['missing_initial16']and [x['fingerprint']for x in initial16['initial16_actual_results_checked']]==[x['fingerprint']for x in raw[:16]]
feed=read(R/'research/monitor/latest.json');counts=dict(prior['monitor_counts_before'])
for key in('registered','results','ranked'):counts[key]+=24
counts['passed']+=len(summary['passed']);counts['rejected']+=len(summary['rejected']);counts['observation_records_excluded']+=3
assert feed['research']['counts']==counts and feed['research']['last_run']['id']==T.name and feed['paper']['observation_id']==paper['last_observation_id']
monitor=read(T/'monitor_check.log');assert monitor['ok']and monitor['protected_inputs_unchanged']and monitor['observations']==41 and monitor['research_configs']==2741
base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip();assert base==prior['base_head']=='a2861500687bf20bd9d779bf765d66018660aee8'
files=sorted(p for p in T.rglob('*')if p.is_file()and '__pycache__'not in p.parts and p.name not in('verification.json','verify.log'))+[L,R/'research/automation/README.md',R/'research/monitor/latest.json',R/'research/monitor/configs.json.gz']
out={'passed':True,'verified_at_utc':datetime.now(timezone.utc).isoformat(),'base_commit':base,'registry':{'rows':len(lines),'canonical':canonical,'preserved_ids':len(records),'unchanged_prior_rows':prior['lines'],'new_reserved_and_finished':27,'new_historical_trials':24,'new_legacy_cutoffs':3,'pending':0},'historical_summary':summary,'new_qualified_cross_period_parameter_pairs':8,'new_cross_period_return_paths':3,'jointly_improved_both_period_pairs':cmp['jointly_improved_pairs_vs_old_entry15_15'],'paper10_accounts_unchanged':True,'both_sensitivity_plots_visually_reviewed':True,'checks':{'all7_replay_phases_exit_zero':True,'all6_final_actual_phases_exit_zero':True,'original_independent_auditor_first_execution_exit_zero':True,'all3_final_checks_exit_zero':True,'all72new_and18old_cost_scenes_verified':True,'all8_new_components_simulated_at_own_funding':True,'explicit_raw55_45_own1100_900_funds_preserved_no_rescaling_rebalance':True,'all540folds_90cost_rows_verified':True,'old_results_criteria_and_prior_ledger_rows_preserved':True,'initial16_actual_evidence_complete':True,'paper41_plan_state_journals_UI_preserved':True},'audits':[ah,af],'protected_sha256':prior['protected_sha256'],'files_sha256':{str(p.relative_to(R)):sha(p)for p in files}}
(T/'verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'passed':True,**out['registry'],'joint_improvements':out['jointly_improved_both_period_pairs'],'new_qualified_paths':out['new_cross_period_return_paths'],'protected_files':len(prior['protected_sha256']),'files_hashed':len(files)}))
